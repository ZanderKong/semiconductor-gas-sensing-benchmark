#!/usr/bin/env python3
"""Lightweight repository lint for active benchmark files."""

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
    "data/benchmark.json",
    "data/benchmark.csv",
    "data/scientific_stress_bank.json",
    "data/item_design_index.csv",
    "data/benchmark_sgs_hard50.json",
    "reports/evaluation_report.md",
    "reports/model_error_analysis.md",
    "reports/free_response_evaluation_report.md",
    "reports/item_design_index.md",
    "archive/history.md",
    "archive/0.4.0_summary.md",
    "eval/runner.py",
    "eval/score_free_response.py",
    "eval/prompts/base_prompt.md",
    "eval/prompts/free_response_judge_prompt.md",
    "scripts/validate_benchmark.py",
    "scripts/validate_hard50.py",
    "scripts/build_sgs152_merged.py",
    "Makefile",
]
BLOCKED_TERMS = [
    "H" + "R",
    "简" + "历",
    "面" + "试",
    "岗位" + "适配",
    "作品集" + "包装",
    "candi" + "date",
    "reviewer " + "sees",
    "用户" + "记忆",
    "vi" + "be",
    "交付" + "完成",
    "为了展示" + "能力",
    "该求" + "职者",
    "这不" + "是",
    "并" + "非",
    "与其" + "说",
    "不如" + "说",
    "赋" + "能",
    "抓" + "手",
    "沉" + "淀",
    "壁" + "垒",
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
        for folder in ["docs", "reports", "archive"]
        for path in (ROOT / folder).glob("*.md")
        if path.exists()
    ] + [ROOT / "README.md"]
    for path in text_files:
        text = path.read_text(encoding="utf-8")
        for phrase in BLOCKED_TERMS:
            if phrase in text:
                errors.append(f"{path.relative_to(ROOT)} contains forbidden phrase: {phrase}")
        for phrase in PRIVATE_TERMS:
            if phrase in text:
                errors.append(f"{path.relative_to(ROOT)} contains private-looking term: {phrase}")

    tasks = json.loads((ROOT / "data/benchmark.json").read_text(encoding="utf-8"))
    if len(tasks) != 152:
        errors.append(f"data/benchmark.json should contain 152 items, got {len(tasks)}")
    if sum(1 for task in tasks if task.get("question_type") == "multiple_choice") != 122:
        errors.append("data/benchmark.json should contain 122 MCQ items")
    if sum(1 for task in tasks if task.get("question_type") == "free_response") != 30:
        errors.append("data/benchmark.json should contain 30 free-response items")
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
