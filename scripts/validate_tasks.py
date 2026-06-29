#!/usr/bin/env python3
"""Validate V3 task structure with standard-library checks."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    task_path = ROOT / "data/benchmark_v3_alpha.json"
    schema_path = ROOT / "data/schema/task_schema_v3.json"
    legacy_schema_path = ROOT / "data/schema_v3_alpha.json"
    tasks = json.loads(task_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    legacy_schema = json.loads(legacy_schema_path.read_text(encoding="utf-8"))
    errors: list[str] = []

    if schema != legacy_schema:
        errors.append("data/schema/task_schema_v3.json differs from data/schema_v3_alpha.json")

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

    if errors:
        fail("\n".join(errors))
    print(f"V3 task structure validation passed: {len(tasks)} tasks")


if __name__ == "__main__":
    main()
