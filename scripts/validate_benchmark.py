#!/usr/bin/env python3
"""Validate the active SGS152 benchmark."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "data/benchmark.json"
DOMAIN_CORE = ROOT / "data/benchmark_sgs100_clean.json"
SCIENTIFIC_STRESS = ROOT / "data/scientific_stress_bank.json"
FREE_RESPONSE_RUBRICS = ROOT / "data/free_response_rubrics.json"
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
EXPECTED_COMPONENTS = {
    "domain_core": {"items": 100, "multiple_choice": 82, "free_response": 18},
    "scientific_stress": {"items": 52, "multiple_choice": 40, "free_response": 12},
}
EXPECTED_DOMAINS = {
    "organic_chemistry",
    "physical_chemistry",
    "inorganic_chemistry",
    "materials_science",
    "general_chemistry",
    "analytical_chemistry",
    "technical_chemistry",
    "toxicity_and_safety",
}


def chinese_len(value: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", value))


def main() -> None:
    rows = json.loads(BENCHMARK.read_text(encoding="utf-8"))
    domain_core = json.loads(DOMAIN_CORE.read_text(encoding="utf-8"))
    scientific_stress = json.loads(SCIENTIFIC_STRESS.read_text(encoding="utf-8"))
    rubrics = json.loads(FREE_RESPONSE_RUBRICS.read_text(encoding="utf-8"))
    errors: list[str] = []

    if len(rows) != 152:
        errors.append(f"Expected 152 items, got {len(rows)}")

    type_counts = Counter(row.get("question_type") for row in rows)
    if dict(type_counts) != EXPECTED_TYPES:
        errors.append(f"Question type distribution mismatch: {dict(type_counts)}")

    for name, component_rows in [("domain_core", domain_core), ("scientific_stress", scientific_stress)]:
        expected = EXPECTED_COMPONENTS[name]
        component_types = Counter(row.get("question_type") for row in component_rows)
        if len(component_rows) != expected["items"]:
            errors.append(f"{name} expected {expected['items']} items, got {len(component_rows)}")
        if component_types.get("multiple_choice", 0) != expected["multiple_choice"]:
            errors.append(f"{name} MCQ mismatch: {dict(component_types)}")
        if component_types.get("free_response", 0) != expected["free_response"]:
            errors.append(f"{name} free-response mismatch: {dict(component_types)}")

    domain_values = {row.get("domain") for row in rows}
    missing_domains = EXPECTED_DOMAINS - domain_values
    if missing_domains:
        errors.append(f"Missing expected domains: {sorted(missing_domains)}")

    mcq_answers = Counter()
    ids = set()
    for row in rows:
        qid = row.get("id", "")
        is_domain_core = bool(re.fullmatch(r"SGS-\d{3}", qid or ""))
        if not qid:
            errors.append("Item missing id")
        if qid in ids:
            errors.append(f"Duplicate id: {qid}")
        ids.add(qid)
        if row.get("question_type") == "free_response":
            if qid not in rubrics:
                errors.append(f"{qid} missing from free_response_rubrics.json")
            if not row.get("rubric"):
                errors.append(f"{qid} missing inline rubric")
            if not row.get("hard_fails"):
                errors.append(f"{qid} missing hard_fails")
            continue
        if row.get("question_type") != "multiple_choice":
            errors.append(f"{qid} invalid question_type: {row.get('question_type')}")
            continue
        answer = row.get("answer", "")
        mcq_answers[answer] += 1
        options = row.get("options", {})
        if not 2 <= len(options) <= 5:
            errors.append(f"{qid} must have 2 to 5 options")
            continue
        if answer not in options:
            errors.append(f"{qid} answer {answer} not in options")
            continue
        lengths = {key: chinese_len(value) for key, value in options.items()}
        shortest = min(lengths.values())
        longest = max(lengths.values())
        if is_domain_core and shortest < 2:
            errors.append(f"{qid} has very short option: {lengths}")
        if is_domain_core and shortest >= 6 and longest / shortest > 3.5:
            errors.append(f"{qid} option length ratio exceeds 3.5: {lengths}")
        if is_domain_core:
            for key, value in options.items():
                hits = [term for term in FORBIDDEN_OPTION_TERMS if term in value]
                if hits:
                    errors.append(f"{qid} option {key} contains forbidden terms: {hits}")
        rationales = row.get("option_rationales", {})
        for key in options:
            if not rationales.get(key):
                errors.append(f"{qid} option {key} missing rationale")

    if sum(mcq_answers.values()) != 122:
        errors.append(f"MCQ answer count mismatch: {dict(mcq_answers)}")

    prompt = (ROOT / "eval/prompts/base_prompt.md").read_text(encoding="utf-8")
    if "A、B、C、D 或 E" not in prompt and "options 中提供" not in prompt:
        errors.append("Base prompt must support variable option letters including E")

    if errors:
        raise SystemExit("\n".join(errors))
    print("Active benchmark validation passed: SGS152, 122 MCQ, 30 free-response")


if __name__ == "__main__":
    main()
