#!/usr/bin/env python3
"""Regenerate a markdown report from a saved run directory."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", default=str(ROOT / "results/runs/demo"))
    args = parser.parse_args()
    run_dir = Path(args.run_dir)
    if not run_dir.is_absolute():
        run_dir = ROOT / run_dir

    manifest = json.loads((run_dir / "run_manifest.json").read_text(encoding="utf-8"))
    metrics = json.loads((run_dir / "aggregate_metrics.json").read_text(encoding="utf-8"))
    judge_rows = load_jsonl(run_dir / "judge_outputs.jsonl")
    badcases = [row for row in judge_rows if row["gate_adjusted_score"] < 80 or row["failure_modes"]]

    lines = [
        "# Diagnostic Report",
        "",
        f"Run ID: `{manifest['run_id']}`",
        f"Model: `{manifest['model_id']}`",
        f"Benchmark version: `{manifest['benchmark_version']}`",
        "",
        "## Metrics",
        "",
        f"- Gate-adjusted score: {metrics['gate_adjusted_score']}",
        f"- High-risk fail rate: {metrics['high_risk_fail_rate']}",
        f"- Trace completeness rate: {metrics['trace_completeness_rate']}",
        "",
        "## Stage Breakdown",
        "",
    ]
    for key, value in metrics["score_by_scenario_stage"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Tool Breakdown", ""])
    for key, value in metrics["score_by_tool_type"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Badcase Summary", ""])
    if badcases:
        for row in badcases:
            lines.append(f"- `{row['task_id']}`: score {row['gate_adjusted_score']}; {', '.join(row['failure_modes'])}")
    else:
        lines.append("- No badcases selected.")
    lines.append("")
    out_path = run_dir / "diagnostic_report.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()

