#!/usr/bin/env python3
"""Validate the active 152-item SGS 0.5.0 benchmark."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "data/benchmark.json"
FORBIDDEN_OPTION_TERMS = [
    "只要",
    "直接",
    "一定",
    "完全",
    "无需",
    "忽略",
    "综合",
    "同时",
    "系统评估",
    "多指标",
    "形成" + "判定依据",
    "作为" + "阶段参考",
    "用于" + "指标摸底",
    "用于" + "数据整理",
    "作为" + "后续比较",
    "作为" + "候选解释",
    "作为" + "机理假设",
    "作为" + "边界假设",
    "用于" + "边界参考",
]
EXPECTED_TYPES = {"multiple_choice": 122, "free_response": 30}
EXPECTED_DOMAINS = {
    "organic_chemistry": 19,
    "physical_chemistry": 14,
    "inorganic_chemistry": 14,
    "materials_science": 14,
    "general_chemistry": 43,
    "analytical_chemistry": 10,
    "technical_chemistry": 10,
    "toxicity_and_safety": 8,
    "expert_science_reasoning": 12,
    "quantitative_science": 8,
}


def chinese_len(value: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", value))


def main() -> None:
    rows = json.loads(BENCHMARK.read_text(encoding="utf-8"))
    errors: list[str] = []

    if len(rows) != 152:
        errors.append(f"Expected 152 items, got {len(rows)}")

    type_counts = Counter(row.get("question_type") for row in rows)
    if dict(type_counts) != EXPECTED_TYPES:
        errors.append(f"Question type distribution mismatch: {dict(type_counts)}")

    domain_counts = Counter(row.get("domain") for row in rows)
    if dict(domain_counts) != EXPECTED_DOMAINS:
        errors.append(f"Domain distribution mismatch: {dict(domain_counts)}")

    mcq_answers = Counter()
    answer_longest = 0
    for row in rows:
        qid = row.get("id", "")
        is_failure_mined = str(qid).startswith("SGS-FM-")
        if not re.fullmatch(r"(?:SGS-\d{3}|SGS-FM-\d{3})", qid):
            errors.append(f"{row.get('id')} has non-canonical id")
        if row.get("question_type") != "multiple_choice":
            continue
        answer = row.get("answer", "")
        mcq_answers[answer] += 1
        options = row.get("options", {})
        allowed = [chr(ord("A") + idx) for idx in range(len(options))]
        min_options = 2 if is_failure_mined else 4
        if list(options.keys()) != allowed or len(options) < min_options:
            errors.append(f"{row['id']} options are not sequential from A or has too few options")
            continue
        lengths = {key: chinese_len(value) for key, value in options.items()}
        if not is_failure_mined:
            shortest = min(lengths.values())
            longest = max(lengths.values())
            if shortest < 10:
                errors.append(f"{row['id']} has option shorter than 10 Chinese characters: {lengths}")
            if longest / shortest > 1.5:
                errors.append(f"{row['id']} option length ratio exceeds 1.5: {lengths}")
            if lengths[answer] == longest:
                answer_longest += 1
        for key, value in options.items():
            if is_failure_mined:
                continue
            hits = [term for term in FORBIDDEN_OPTION_TERMS if term in value]
            if hits:
                errors.append(f"{row['id']} option {key} contains forbidden terms: {hits}")
        rationales = row.get("option_rationales", {})
        for key in options:
            if not rationales.get(key):
                errors.append(f"{row['id']} option {key} missing rationale")

    if mcq_answers != Counter({"A": 34, "B": 29, "C": 29, "D": 29, "E": 1}):
        errors.append(f"MCQ answer distribution mismatch: {dict(mcq_answers)}")
    if answer_longest:
        errors.append(f"{answer_longest} MCQ answers are tied for longest option")

    if errors:
        raise SystemExit("\n".join(errors))
    print("Active benchmark validation passed: 152 items, 122 MCQ, 30 free-response")


if __name__ == "__main__":
    main()
