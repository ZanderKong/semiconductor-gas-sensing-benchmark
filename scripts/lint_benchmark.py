#!/usr/bin/env python3
"""Lightweight repository lint for portfolio-facing benchmark files."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "README.md",
    "docs/overview.md",
    "docs/scoring_v3.md",
    "docs/hard_gates.md",
    "docs/judge_protocol.md",
    "docs/reproducibility_and_trace.md",
    "docs/agent_modes.md",
    "docs/task_design_v3.md",
    "data/benchmark_v3_alpha.json",
    "data/benchmark_v3_alpha.csv",
    "data/schema/task_schema_v3.json",
    "eval/runner.py",
    "eval/reporting/generate_report.py",
    "eval/configs/demo.yaml",
    "Makefile",
]
FORBIDDEN_PHRASES = [
    "\u9762\u8bd5\u5b98" + "\u4e09\u5206\u949f",
    "\u9762\u8bd5\u5b98" + "\u5341\u5206\u949f",
    "smoke" + " test",
    "Kimi" + " 与 GLM",
    "真实" + "项目",
    "不是" + "……而是",
]
PRIVATE_TERMS = [
    "私有配方" + "比例：",
    "客户名称",
    "供应商敏感",
    "供应链敏感" + "信息：",
]


def main() -> None:
    errors: list[str] = []
    for file in REQUIRED_FILES:
        if not (ROOT / file).exists():
            errors.append(f"Missing required file: {file}")

    text_files = [
        path for path in list((ROOT / "docs").glob("*.md")) + [ROOT / "README.md"]
        if path.exists()
    ]
    for path in text_files:
        text = path.read_text(encoding="utf-8")
        for phrase in FORBIDDEN_PHRASES:
            if phrase in text:
                errors.append(f"{path.relative_to(ROOT)} contains forbidden phrase: {phrase}")
        for phrase in PRIVATE_TERMS:
            if phrase in text:
                errors.append(f"{path.relative_to(ROOT)} contains private-looking term: {phrase}")

    tasks = json.loads((ROOT / "data/benchmark_v3_alpha.json").read_text(encoding="utf-8"))
    for task in tasks:
        for field in ["prompt", "privacy_note", "audit_notes"]:
            value = str(task.get(field, ""))
            for phrase in PRIVATE_TERMS:
                if phrase in value:
                    errors.append(f"{task['task_id']} contains private-looking term: {phrase}")

    if errors:
        raise SystemExit("\n".join(errors))
    print("Benchmark lint passed")


if __name__ == "__main__":
    main()
