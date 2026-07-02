#!/usr/bin/env python3
"""Lightweight repository lint for review-facing benchmark files."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "README.md",
    "docs/dataset_card.md",
    "docs/methodology.md",
    "docs/scoring_protocol.md",
    "docs/risk_gates.md",
    "docs/reproducibility.md",
    "reports/evaluation_report.md",
    "reports/iteration_notes.md",
    "reports/model_error_analysis.md",
    "data/benchmark.json",
    "data/benchmark.csv",
    "data/benchmark_sgs100_clean.json",
    "data/scientific_stress_bank.json",
    "data/benchmark_sgs100_robustness.json",
    "data/benchmark_sgs_hard50.json",
    "data/free_response_rubrics.json",
    "eval/runner.py",
    "eval/reporting/generate_report.py",
    "eval/configs/demo.yaml",
    "scripts/validate_benchmark.py",
    "scripts/validate_hard50.py",
    "Makefile",
]
FORBIDDEN_PHRASES = [
    "\u9762\u8bd5\u5b98" + "\u4e09\u5206\u949f",
    "\u9762\u8bd5\u5b98" + "\u5341\u5206\u949f",
    "smoke" + " test",
    "模型" + "与模型",
    "真实" + "项目",
    "不是" + "……而是",
    "HR review guide",
    "HR readers",
    "HR",
    "简历",
    "岗位",
    "求职",
    "作品集",
    "能力自评",
    "用户记忆",
    "delivery audit",
    "release readiness",
    "Reviewer",
    "reviewer",
    "请按我设计好的路径",
    "投递版",
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
        path
        for path in list((ROOT / "docs").glob("*.md"))
        + list((ROOT / "reports").glob("*.md"))
        + [ROOT / "README.md"]
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

    tasks = json.loads((ROOT / "data/benchmark.json").read_text(encoding="utf-8"))
    for task in tasks:
        for field in ["question", "answer_rationale", "rationale", "workflow_task"]:
            value = str(task.get(field, ""))
            for phrase in PRIVATE_TERMS:
                if phrase in value:
                    errors.append(f"{task['id']} contains private-looking term: {phrase}")

    if errors:
        raise SystemExit("\n".join(errors))
    print("Benchmark lint passed")


if __name__ == "__main__":
    main()
