#!/usr/bin/env python3
"""Validate V3-alpha task files with standard-library checks."""

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
    schema_path = ROOT / "data/schema/task_schema_v3.json"
    legacy_schema_path = ROOT / "data/schema_v3_alpha.json"
    tasks = json.loads(task_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    legacy_schema = json.loads(legacy_schema_path.read_text(encoding="utf-8"))
    errors: list[str] = []

    if schema != legacy_schema:
        errors.append("data/schema/task_schema_v3.json differs from data/schema_v3_alpha.json")
    if len(tasks) != 46:
        errors.append(f"Expected 46 V3-alpha tasks, got {len(tasks)}")

    required = schema["items"]["required"]
    props = schema["items"]["properties"]
    ids = [task.get("task_id") for task in tasks]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate task_id found")

    for task in tasks:
        tid = task.get("task_id", "<missing>")
        for key in required:
            if key not in task or task[key] in ("", None):
                errors.append(f"{tid}: missing {key}")
        for key in ["benchmark_split", "task_type", "scenario_stage", "expected_output", "tool_mode", "tool_type", "risk_level", "variant_type", "source_policy", "difficulty"]:
            enum = props[key].get("enum")
            if enum and task.get(key) not in enum:
                errors.append(f"{tid}: invalid {key}={task.get(key)}")
        for dim in task.get("target_dimensions", []):
            if dim not in props["target_dimensions"]["items"]["enum"]:
                errors.append(f"{tid}: invalid dimension {dim}")
        for gate in task.get("hard_gate_checks", []):
            if gate not in props["hard_gate_checks"]["items"]["enum"]:
                errors.append(f"{tid}: invalid hard gate {gate}")
        if task.get("tool_mode") == "no_tool" and task.get("tool_type") != "no_tool":
            errors.append(f"{tid}: no_tool mode must use no_tool type")
        if task.get("tool_mode") == "tool_enabled" and task.get("tool_type") == "no_tool":
            errors.append(f"{tid}: tool_enabled mode needs a concrete tool_type")
        if task.get("benchmark_split") == "robustness" and not task.get("parent_task_id"):
            errors.append(f"{tid}: robustness task missing parent_task_id")
        if not isinstance(task.get("gold_response"), dict):
            errors.append(f"{tid}: gold_response must be an object")
        rubric = task.get("scoring_rubric", {})
        if not rubric.get("key_points") or not rubric.get("dimension_focus"):
            errors.append(f"{tid}: scoring_rubric missing key_points or dimension_focus")

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
    print("V3-alpha validation passed")
    print(f"split={dict(split)}")
    print(f"static_stage={dict(stage)}")
    print(f"tool_pairs={paired}")


if __name__ == "__main__":
    main()

