#!/usr/bin/env python3
"""Build the active 0.5.0 benchmark from SGS100 + Scientific Stress Set."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

BASE_PATH = ROOT / "data" / "benchmark_sgs100_clean.json"
STRESS_BANK_PATH = ROOT / "data" / "scientific_stress_bank.json"

ACTIVE_JSON = ROOT / "data" / "benchmark.json"
ACTIVE_CSV = ROOT / "data" / "benchmark.csv"
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


def sync_free_response_rubrics(stress_items: list[dict[str, Any]]) -> None:
    rubrics = json.loads(FR_RUBRICS.read_text(encoding="utf-8"))
    rubrics = {
        key: value
        for key, value in rubrics.items()
        if not key.startswith("SGS-FM-")
    }
    for item in stress_items:
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
    stress_items = json.loads(STRESS_BANK_PATH.read_text(encoding="utf-8"))
    merged = base + stress_items

    ACTIVE_JSON.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(ACTIVE_CSV, merged)
    sync_free_response_rubrics(stress_items)

    mcq_count = sum(1 for item in merged if item["question_type"] == "multiple_choice")
    free_count = sum(1 for item in merged if item["question_type"] == "free_response")
    print(f"Wrote {ACTIVE_JSON}")
    print(f"Wrote {ACTIVE_CSV}")
    print(f"Updated {FR_RUBRICS}")
    print(f"total={len(merged)} mcq={mcq_count} free_response={free_count}")


if __name__ == "__main__":
    main()
