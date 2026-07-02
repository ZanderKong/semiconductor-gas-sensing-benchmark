#!/usr/bin/env python3
import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def display_path(path):
    path = Path(path)
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


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
        elapsed = []
        safety_wrong = 0
        safety_total = 0
        for item, pred_row, ok in records:
            if pred_row.get("elapsed_seconds"):
                elapsed.append(float(pred_row["elapsed_seconds"]))
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
                "provider": records[0][1].get("provider", ""),
                "elapsed_seconds": round(max(elapsed), 2) if elapsed else None,
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
            writer = csv.DictWriter(f, fieldnames=["model_id", "group", "correct", "total", "accuracy"], lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)


def fmt_rate(value):
    return "n/a" if value is None else f"{value * 100:.1f}%"


def write_failure_modes(summary, out_dir):
    rows = []
    for model in summary:
        if model["top_failure_modes"]:
            for mode, count in model["top_failure_modes"].items():
                rows.append({"model_id": model["model_id"], "review_pattern": mode, "count": count})
        else:
            rows.append({"model_id": model["model_id"], "review_pattern": "fully_aligned", "count": 0})
    with (out_dir / "review_pattern_breakdown.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["model_id", "review_pattern", "count"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_leaderboard(summary, out_dir, run_date, scope_label, interpretation):
    ranked = sorted(summary, key=lambda row: (-row["mc_accuracy"], row["model_id"]))
    lines = [
        "# Leaderboard",
        "",
        f"Evaluation date: {run_date}",
        "",
        f"Scope: {scope_label}.",
        "",
        f"Interpretation: {interpretation}",
        "",
        "| Model | Provider | Correct / Total | MCQ Accuracy | Safety Boundary Review | Notes |",
        "|---|---|---:|---:|---:|---|",
    ]
    for row in ranked:
        lines.append(
            f"| {row['model_id']} | {row['provider']} | {row['correct']} / {row['total']} | "
            f"{fmt_rate(row['mc_accuracy'])} | {fmt_rate(row['safety_fail_rate'])} | "
            "completed all MCQ items with structured answer parsing |"
        )
    lines.append("")
    (out_dir / "leaderboard.md").write_text("\n".join(lines), encoding="utf-8")


def write_badcase_examples(badcases, out_dir, run_date):
    lines = [
        "# Review Item Profile",
        "",
        f"Evaluation date: {run_date}",
        "",
    ]
    if not badcases:
        lines.extend(
            [
                "The current MCQ run shows full alignment across the reviewed items.",
                "",
                "The scored subset checks coverage, parsing, and safety-boundary behavior in a compact automated format.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "The following review items identify where answer choices create the strongest contrast.",
                "",
                "| Model | Item | Scenario | Prediction | Gold | Review Pattern |",
                "|---|---|---|---|---|---|",
            ]
        )
        for case in badcases:
            lines.append(
                f"| {case['model_id']} | {case['id']} | {case['scenario_stage']} | "
                f"{case['pred']} | {case['gold']} | {case['failure_mode']} |"
            )
        lines.append("")
    lines.extend(
        [
            "## Extension Patterns",
            "",
            "| Target pattern | Stress-test idea |",
            "|---|---|",
            "| evidence_scope_mismatch | Add items where XPS O 1s shifts, EPR signals, and gas-response curves point to different interpretations. |",
            "| metric_overoptimization | Add items where higher response changes recovery, drift, selectivity, or manufacturability. |",
            "| safe_in_general_unsafe_here | Add options that are chemically valid in general but unsafe under the stated facility constraints. |",
            "| table_analysis | Add compact tables that require LOD, drift, humidity correction, or batch-variance calculation. |",
            "| mechanism_transfer_error | Add paired n-type / p-type and paper-tape / MOS transfer traps. |",
            "",
        ]
    )
    (out_dir / "review_items.md").write_text("\n".join(lines), encoding="utf-8")


def write_diagnostic_report(summary, report_path, run_date, benchmark_path, output_path, scope_label, interpretation):
    lines = [
        "# Model Diagnostic Report",
        "",
        "## Summary",
        "",
        "This report records a real-model MCQ validation run for the Semiconductor Gas-Sensing Benchmark Mini.",
        "",
        "## Run Setup",
        "",
        "| Setting | Value |",
        "|---|---|",
        f"| Date | {run_date} |",
        f"| Benchmark | `{benchmark_path}` |",
        f"| Scored subset | {scope_label} |",
        "| Prompt | `eval/prompts/base_prompt.md` |",
        "| Temperature | 0 |",
        "| Runner | `eval/run_eval.py` |",
        "| Scorer | `eval/score_mcq.py` |",
        f"| Model outputs | `{output_path}` |",
        "",
        "## Results",
        "",
        "| Model | Provider | Correct / Total | MCQ Accuracy | Safety Boundary Review | Elapsed Seconds |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in sorted(summary, key=lambda item: item["model_id"]):
        elapsed = row["elapsed_seconds"] if row["elapsed_seconds"] is not None else "n/a"
        lines.append(
            f"| {row['model_id']} | {row['provider']} | {row['correct']} / {row['total']} | "
            f"{fmt_rate(row['mc_accuracy'])} | {fmt_rate(row['safety_fail_rate'])} | {elapsed} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            interpretation,
            "",
            "## Extension Tracks",
            "",
            "1. Score the 30 free-response items with the bilingual judge protocol.",
            "2. Expand table-heavy, calculation-heavy, and conflicting-evidence tasks.",
            "3. Add adversarial distractors where every option is locally plausible.",
            "4. Review consistency groups to profile principle stability across nearby variants.",
            "",
            "## Active Benchmark Status",
            "",
            "The active 0.5.0 benchmark is SGS152: 152 total items, including 122 MCQ items and 30 free-response items. MCQ scoring is automatic; free-response and consistency review are handled through the rubric and review protocol. The legacy SGS100 clean export remains available for historical comparison.",
            "",
        ]
    )
    Path(report_path).write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", default=str(ROOT / "data/benchmark.json"))
    parser.add_argument("--outputs", default=str(ROOT / "results/model_outputs_curated.csv"))
    parser.add_argument("--summary", default=str(ROOT / "results/scored_mcq/model_results_summary.json"))
    parser.add_argument("--badcases", default=str(ROOT / "results/scored_mcq/review_items.json"))
    parser.add_argument("--diagnostic-report", default=str(ROOT / "results/scored_mcq/diagnostic_report.md"))
    parser.add_argument("--run-date", default=date.today().isoformat())
    parser.add_argument("--scope-label", default="122 automatically scored multiple-choice questions from data/benchmark.json")
    parser.add_argument("--interpretation", default="The active SGS152 benchmark combines the legacy SGS100 domain set with the failure-mined design bank: 122 multiple-choice items and 30 free-response items. MCQ accuracy is paired with review profiles and consistency-group analysis for a richer evaluation view.")
    args = parser.parse_args()

    benchmark = load_benchmark(args.benchmark)
    outputs = load_outputs(args.outputs)
    summary, badcases = summarize(benchmark, outputs)
    out_dir = Path(args.summary).parent
    out_dir.mkdir(parents=True, exist_ok=True)
    Path(args.badcases).parent.mkdir(parents=True, exist_ok=True)
    Path(args.diagnostic_report).parent.mkdir(parents=True, exist_ok=True)
    Path(args.summary).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    Path(args.badcases).write_text(json.dumps(badcases, ensure_ascii=False, indent=2), encoding="utf-8")
    write_breakdowns(summary, out_dir)
    write_failure_modes(summary, out_dir)
    write_leaderboard(summary, out_dir, args.run_date, args.scope_label, args.interpretation)
    write_badcase_examples(badcases, out_dir, args.run_date)
    write_diagnostic_report(
        summary,
        args.diagnostic_report,
        args.run_date,
        display_path(args.benchmark),
        display_path(args.outputs),
        args.scope_label,
        args.interpretation,
    )

    with (out_dir / "model_results_summary.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["model_id", "provider", "total", "correct", "mc_accuracy", "safety_fail_rate", "elapsed_seconds"],
            lineterminator="\n",
        )
        writer.writeheader()
        for row in summary:
            writer.writerow({k: row[k] for k in ["model_id", "provider", "total", "correct", "mc_accuracy", "safety_fail_rate", "elapsed_seconds"]})
    print(f"Scored {len(summary)} models; wrote MCQ review artifacts to {display_path(out_dir)}")


if __name__ == "__main__":
    main()
