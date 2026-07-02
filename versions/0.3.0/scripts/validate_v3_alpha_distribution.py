#!/usr/bin/env python3
"""Validate the fixed V3-alpha release distribution."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    task_path = ROOT / "data/benchmark_v3_alpha.json"
    csv_path = ROOT / "data/benchmark_v3_alpha.csv"
    tasks = json.loads(task_path.read_text(encoding="utf-8"))
    errors: list[str] = []

    if len(tasks) != 46:
        errors.append(f"Expected 46 V3-alpha tasks, got {len(tasks)}")

    split = Counter(task["benchmark_split"] for task in tasks)
    if split != {"static_core": 24, "robustness": 16, "live_extension": 6}:
        errors.append(f"Unexpected split distribution: {dict(split)}")

    stage = Counter(task["scenario_stage"] for task in tasks if task["benchmark_split"] == "static_core")
    for expected_stage in ["文献分析", "实验设计", "实验进行", "结果分析", "下一步计划", "安全边界"]:
        if stage[expected_stage] != 4:
            errors.append(f"Static core stage {expected_stage} has {stage[expected_stage]} tasks, expected 4")

    static = [task for task in tasks if task["benchmark_split"] == "static_core"]
    tool_related = [task for task in static if task["task_type"] == "tool_use" or task["tool_mode"] == "tool_enabled"]
    if len(tool_related) < 8:
        errors.append("Expected at least 8 tool-related static-core tasks")

    by_group: dict[str, list[dict]] = defaultdict(list)
    for task in static:
        by_group[task["variant_group_id"]].append(task)
    paired = [group for group, rows in by_group.items() if {"no_tool", "tool_enabled"} <= {row["tool_mode"] for row in rows}]
    if len(paired) < 4:
        errors.append("Expected at least 4 no-tool/tool-enabled task pairs")

    with csv_path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 46:
        errors.append(f"Expected 46 CSV rows, got {len(rows)}")

    if errors:
        fail("\n".join(errors))
    print("V3-alpha distribution validation passed")
    print(f"split={dict(split)}")
    print(f"static_stage={dict(stage)}")
    print(f"tool_pairs={paired}")


if __name__ == "__main__":
    main()
