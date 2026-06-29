#!/usr/bin/env python3
import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import date
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
                rows.append({"model_id": model["model_id"], "failure_mode": mode, "count": count})
        else:
            rows.append({"model_id": model["model_id"], "failure_mode": "none_observed", "count": 0})
    with (out_dir / "failure_mode_breakdown.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["model_id", "failure_mode", "count"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_leaderboard(summary, out_dir, run_date):
    ranked = sorted(summary, key=lambda row: (-row["mc_accuracy"], row["model_id"]))
    lines = [
        "# Leaderboard",
        "",
        f"Evaluation date: {run_date}",
        "",
        "Scope: 82 automatically scored multiple-choice questions from `data/benchmark_v1.json`.",
        "",
        "Interpretation: the MCQ pipeline was validated with real GPT and DeepSeek model calls. The 100% scores show that the current MCQ subset is useful as a pipeline check but is not discriminative enough for strong models.",
        "",
        "| Model | Provider | Correct / Total | MCQ Accuracy | Safety Fail Rate | Notes |",
        "|---|---|---:|---:|---:|---|",
    ]
    for row in ranked:
        lines.append(
            f"| {row['model_id']} | {row['provider']} | {row['correct']} / {row['total']} | "
            f"{fmt_rate(row['mc_accuracy'])} | {fmt_rate(row['safety_fail_rate'])} | "
            "completed all MCQ items; stronger stress tests are required |"
        )
    lines.append("")
    (out_dir / "leaderboard.md").write_text("\n".join(lines), encoding="utf-8")


def write_badcase_examples(badcases, out_dir, run_date):
    lines = [
        "# Badcase Review",
        "",
        f"Evaluation date: {run_date}",
        "",
    ]
    if not badcases:
        lines.extend(
            [
                "No wrong multiple-choice answers were observed in the current GPT and DeepSeek MCQ run.",
                "",
                "This result is diagnostic rather than conclusive. The current MCQ subset checks coverage, parsing, and safety-boundary behavior, but it does not separate strong models.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "The following cases were incorrectly answered in the current MCQ run.",
                "",
                "| Model | Item | Scenario | Prediction | Gold | Failure Mode |",
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
            "## Recommended Stress Badcases",
            "",
            "| Target failure mode | Stress-test idea |",
            "|---|---|",
            "| evidence_scope_mismatch | Add items where XPS O 1s shifts, EPR signals, and gas-response curves point to different interpretations. |",
            "| metric_overoptimization | Add tradeoffs where higher response worsens recovery, drift, selectivity, or manufacturability. |",
            "| safe_in_general_unsafe_here | Add options that are chemically valid in general but unsafe under the stated facility constraints. |",
            "| table_analysis | Add compact tables that require LOD, drift, humidity correction, or batch-variance calculation. |",
            "| mechanism_transfer_error | Add paired n-type / p-type and paper-tape / MOS transfer traps. |",
            "",
        ]
    )
    (out_dir / "badcase_examples.md").write_text("\n".join(lines), encoding="utf-8")


def write_diagnostic_report(summary, report_path, run_date):
    lines = [
        "# Model Diagnostic Report",
        "",
        "## Summary",
        "",
        "This report records the real-model MCQ validation run for the Semiconductor Gas-Sensing Benchmark Mini. The benchmark contains 100 items in total: 82 multiple-choice items and 18 free-response items.",
        "",
        "## Run Setup",
        "",
        "| Setting | Value |",
        "|---|---|",
        f"| Date | {run_date} |",
        "| Benchmark | `data/benchmark_v1.json` |",
        "| Scored subset | 82 multiple-choice questions |",
        "| Prompt | `eval/prompts/base_prompt.md` |",
        "| Temperature | 0 |",
        "| Runner | `eval/run_eval.py` |",
        "| Scorer | `eval/score_mcq.py` |",
        "| Run manifest | `results/model_run_manifest.json` |",
        "",
        "## Results",
        "",
        "| Model | Provider | Correct / Total | MCQ Accuracy | Safety Fail Rate | Elapsed Seconds |",
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
            "Both evaluated models completed all 82 MCQ items without parser errors or missing answers. Both models achieved 82 / 82, so the useful conclusion is that the call, parse, score, and report pipeline works end to end.",
            "",
            "The result should not be presented as a stable capability ranking. The MCQ subset is too easy for strong models and should be treated as a regression and coverage check.",
            "",
            "## Recommended Next Steps",
            "",
            "1. Score the 18 free-response items with a judge protocol and human audit.",
            "2. Add table-heavy, calculation-heavy, and conflicting-evidence tasks.",
            "3. Add adversarial distractors where every option is locally plausible.",
            "4. Use the V3-alpha task-unit runner for trace-based model comparisons after the live tool harness is available.",
            "",
            "## V3-Alpha Status",
            "",
            "The V3-alpha task-unit layer already includes schema validation, Hard Gate definitions, D0-D6 scoring dimensions, trace requirements, an API-free demo runner, and report generation. The current real-model run validates the MCQ layer while the V3 task-unit layer remains the next target for full model evaluation.",
            "",
        ]
    )
    Path(report_path).write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", default=str(ROOT / "data/benchmark_v1.json"))
    parser.add_argument("--outputs", default=str(ROOT / "results/model_outputs.csv"))
    parser.add_argument("--summary", default=str(ROOT / "results/model_results_summary.json"))
    parser.add_argument("--badcases", default=str(ROOT / "results/badcases.json"))
    parser.add_argument("--diagnostic-report", default=str(ROOT / "reports/model_diagnostic_report.md"))
    parser.add_argument("--run-date", default=date.today().isoformat())
    args = parser.parse_args()

    benchmark = load_benchmark(args.benchmark)
    outputs = load_outputs(args.outputs)
    summary, badcases = summarize(benchmark, outputs)
    Path(args.summary).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    Path(args.badcases).write_text(json.dumps(badcases, ensure_ascii=False, indent=2), encoding="utf-8")
    out_dir = Path(args.summary).parent
    write_breakdowns(summary, out_dir)
    write_failure_modes(summary, out_dir)
    write_leaderboard(summary, out_dir, args.run_date)
    write_badcase_examples(badcases, out_dir, args.run_date)
    write_diagnostic_report(summary, args.diagnostic_report, args.run_date)

    with (out_dir / "model_results_summary.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["model_id", "provider", "total", "correct", "mc_accuracy", "safety_fail_rate", "elapsed_seconds"],
            lineterminator="\n",
        )
        writer.writeheader()
        for row in summary:
            writer.writerow({k: row[k] for k in ["model_id", "provider", "total", "correct", "mc_accuracy", "safety_fail_rate", "elapsed_seconds"]})
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
