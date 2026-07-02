#!/usr/bin/env python3
"""Build the active 0.5.0 benchmark from SGS100 + failure-mined design bank."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

BASE_PATH = ROOT / "data" / "benchmark_sgs100_clean.json"
FAILURE_BANK_PATH = ROOT / "data" / "failure_mined_bank.json"

ACTIVE_JSON = ROOT / "data" / "benchmark.json"
ACTIVE_CSV = ROOT / "data" / "benchmark.csv"
OUT_JSON = ROOT / "data" / "benchmark_sgs152_merged.json"
OUT_CSV = ROOT / "data" / "benchmark_sgs152_merged.csv"
OUT_REPORT = ROOT / "reports" / "sgs152_merged_build_report.md"
FR_RUBRICS = ROOT / "data" / "free_response_rubrics.json"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = sorted({key for row in rows for key in row.keys()})
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            encoded = {}
            for key, value in row.items():
                if isinstance(value, (dict, list)):
                    encoded[key] = json.dumps(value, ensure_ascii=False)
                elif isinstance(value, str):
                    encoded[key] = "\n".join(line.rstrip() for line in value.splitlines())
                else:
                    encoded[key] = value
            writer.writerow(encoded)


def sync_free_response_rubrics(failure_items: list[dict[str, Any]]) -> None:
    rubrics = json.loads(FR_RUBRICS.read_text(encoding="utf-8"))
    rubrics = {
        key: value
        for key, value in rubrics.items()
        if not key.startswith("SGS-FM-")
    }
    for item in failure_items:
        if item["question_type"] == "free_response":
            rubrics[item["id"]] = {
                "answer": item["answer"],
                "rubric": item["rubric"],
                "key_points": item["key_points"],
                "hard_fails": item["hard_fails"],
                "common_failure_modes": item["common_failure_modes"],
                "ability_target": item["ability_target"],
            }
    FR_RUBRICS.write_text(json.dumps(rubrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    base = json.loads(BASE_PATH.read_text(encoding="utf-8"))
    failure_items = json.loads(FAILURE_BANK_PATH.read_text(encoding="utf-8"))
    merged = base + failure_items

    ACTIVE_JSON.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_JSON.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(ACTIVE_CSV, merged)
    write_csv(OUT_CSV, merged)
    sync_free_response_rubrics(failure_items)

    mcq_count = sum(1 for item in merged if item["question_type"] == "multiple_choice")
    free_count = sum(1 for item in merged if item["question_type"] == "free_response")
    fm_mcq = sum(1 for item in failure_items if item["question_type"] == "multiple_choice")
    fm_free = sum(1 for item in failure_items if item["question_type"] == "free_response")
    OUT_REPORT.write_text(
        "\n".join(
            [
                "# SGS152 Merged Build Report",
                "",
                f"- Base source: `{BASE_PATH.relative_to(ROOT)}` ({len(base)} items)",
                f"- Failure-mined design bank: `{FAILURE_BANK_PATH.relative_to(ROOT)}` ({len(failure_items)} items)",
                f"- Active JSON: `{ACTIVE_JSON.relative_to(ROOT)}`",
                f"- Active CSV: `{ACTIVE_CSV.relative_to(ROOT)}`",
                f"- Alias JSON: `{OUT_JSON.relative_to(ROOT)}`",
                f"- Alias CSV: `{OUT_CSV.relative_to(ROOT)}`",
                f"- Total items: {len(merged)}",
                f"- Multiple-choice items: {mcq_count}",
                f"- Free-response items: {free_count}",
                f"- Added failure-mined items: {len(failure_items)} ({fm_mcq} MCQ, {fm_free} free-response)",
                "",
                "The merged set preserves the legacy SGS100 professional layer and appends a failure-mined design bank with explicit design notes.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {ACTIVE_JSON}")
    print(f"Wrote {ACTIVE_CSV}")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_CSV}")
    print(f"Updated {FR_RUBRICS}")
    print(f"Wrote {OUT_REPORT}")
    print(f"total={len(merged)} mcq={mcq_count} free_response={free_count}")


if __name__ == "__main__":
    main()
