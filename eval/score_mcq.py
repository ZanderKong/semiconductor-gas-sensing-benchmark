#!/usr/bin/env python3
import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def normalize(value):
    return str(value or "").strip().upper().replace("，", ",").replace(" ", "")


def load_benchmark(path):
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    return {row["id"]: row for row in rows if row["question_type"] == "multiple_choice"}


def load_outputs(path):
    with Path(path).open(encoding="utf-8") as f:
        return [row for row in csv.DictReader(f) if row.get("id")]


def pct(n, d):
    return round(n / d, 4) if d else None


def grouped(records, field):
    acc = defaultdict(lambda: [0, 0])
    for item, pred, ok in records:
        acc[item[field]][0] += int(ok)
        acc[item[field]][1] += 1
    return {
        key: {"correct": c, "total": t, "accuracy": pct(c, t)}
        for key, (c, t) in sorted(acc.items())
    }


def summarize(benchmark, outputs):
    by_model = defaultdict(list)
    for row in outputs:
        qid = row["id"]
        if qid not in benchmark:
            continue
        item = benchmark[qid]
        pred = normalize(row["answer"])
        ok = pred == normalize(item["answer"])
        by_model[row["model_id"]].append((item, row, ok))

    summaries = []
    badcases = []
    for model_id, records in sorted(by_model.items()):
        total = len(records)
        correct = sum(ok for _, _, ok in records)
        wrong = [(item, pred, ok) for item, pred, ok in records if not ok]
        failure_modes = Counter(item["failure_mode"] for item, _, _ in wrong)
        selected_profiles = Counter()
        safety_wrong = 0
        safety_total = 0
        for item, pred_row, ok in records:
            if item["scenario_stage"] == "安全边界" or item["tool_type"] == "safety_reference":
                safety_total += 1
                safety_wrong += int(not ok)
            pred = normalize(pred_row["answer"])
            profile = item.get("option_profiles", {}).get(pred)
            if profile and not ok:
                selected_profiles[profile] += 1

        summaries.append(
            {
                "model_id": model_id,
                "total": total,
                "correct": correct,
                "mc_accuracy": pct(correct, total),
                "safety_fail_rate": pct(safety_wrong, safety_total),
                "accuracy_by_domain": grouped(records, "domain"),
                "accuracy_by_scenario_stage": grouped(records, "scenario_stage"),
                "accuracy_by_tool_type": grouped(records, "tool_type"),
                "top_failure_modes": dict(failure_modes.most_common(10)),
                "wrong_option_profiles": dict(selected_profiles.most_common(10)),
                "wrong_ids": [item["id"] for item, _, _ in wrong],
            }
        )
        for item, pred_row, _ in wrong[:8]:
            pred = normalize(pred_row["answer"])
            badcases.append(
                {
                    "model_id": model_id,
                    "id": item["id"],
                    "domain": item["domain"],
                    "scenario_stage": item["scenario_stage"],
                    "question": item["question"],
                    "pred": pred,
                    "gold": item["answer"],
                    "selected_profile": item.get("option_profiles", {}).get(pred, ""),
                    "failure_mode": item["failure_mode"],
                    "rationale": item["answer_rationale"],
                }
            )
    return summaries, badcases


def write_breakdowns(summary, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    for field, filename in [
        ("accuracy_by_domain", "domain_breakdown.csv"),
        ("accuracy_by_scenario_stage", "scenario_stage_breakdown.csv"),
        ("accuracy_by_tool_type", "tool_type_breakdown.csv"),
    ]:
        rows = []
        for model in summary:
            for key, value in model[field].items():
                rows.append(
                    {
                        "model_id": model["model_id"],
                        "group": key,
                        "correct": value["correct"],
                        "total": value["total"],
                        "accuracy": value["accuracy"],
                    }
                )
        with (out_dir / filename).open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["model_id", "group", "correct", "total", "accuracy"])
            writer.writeheader()
            writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", default=str(ROOT / "data/benchmark_v1.json"))
    parser.add_argument("--outputs", default=str(ROOT / "results/model_outputs.csv"))
    parser.add_argument("--summary", default=str(ROOT / "results/model_results_summary.json"))
    parser.add_argument("--badcases", default=str(ROOT / "results/badcases.json"))
    args = parser.parse_args()

    benchmark = load_benchmark(args.benchmark)
    outputs = load_outputs(args.outputs)
    summary, badcases = summarize(benchmark, outputs)
    Path(args.summary).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    Path(args.badcases).write_text(json.dumps(badcases, ensure_ascii=False, indent=2), encoding="utf-8")
    write_breakdowns(summary, Path(args.summary).parent)

    with (Path(args.summary).parent / "model_results_summary.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["model_id", "total", "correct", "mc_accuracy", "safety_fail_rate"])
        writer.writeheader()
        for row in summary:
            writer.writerow({k: row[k] for k in ["model_id", "total", "correct", "mc_accuracy", "safety_fail_rate"]})
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
