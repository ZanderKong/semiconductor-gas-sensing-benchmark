#!/usr/bin/env python3
"""Acceptance lint for the SGS-100 V4 cleaned release."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAIN_JSON = ROOT / "data/benchmark.json"
CLEAN_CSV = ROOT / "data/benchmark_sgs100_clean.csv"
ROBUSTNESS_CSV = ROOT / "data/benchmark_sgs100_robustness.csv"
ROBUSTNESS_JSON = ROOT / "data/benchmark_sgs100_robustness.json"
FR_RUBRICS = ROOT / "data/free_response_rubrics.json"

ALLOWED_VARIANTS = {
    "paraphrase",
    "distractor",
    "contradiction",
    "adversarial_safety",
    "tool_observation_shift",
}
ALLOWED_EXPECTED = {
    "same_answer",
    "changed_answer",
    "safety_refusal",
    "tool_result_followed",
}
REQUIRED_REPORTS = [
    "reports/sgs100_revision_report.md",
    "reports/sgs100_robustness_report.md",
    "reports/sgs100_completion_audit.md",
    "reports/kimi_connection_probe.md",
]
REQUIRED_DOCS = [
    "docs/robustness_variant_design.md",
    "docs/free_response_rubric_design.md",
    "docs/hr_review_guide.md",
]
PRIVATE_OR_RECIPE_PATTERNS = [
    r"\d+(?:\.\d+)?\s*(?:g|mg|kg|mL|L)\b",
    r"\d+(?:\.\d+)?\s*(?:wt%|vol%)",
    r"质量百分比",
    r"具体克数",
    r"供应商批号[:：][A-Za-z0-9_-]+",
    r"内部项目代号",
    r"私有配方比例[:：]",
]
HAZARDOUS_EXECUTION_PATTERNS = [
    r"酸化漂白液",
    r"关闭.*通风",
    r"直接释放",
]
ANSWER_LEAKAGE_TERMS = [
    "唯一正确",
    "显然正确",
    "标准答案",
    "一定优于",
    "无需验证",
]


def chinese_len(value: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", value))


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check_text_safety(label: str, text: str, errors: list[str]) -> None:
    for pattern in PRIVATE_OR_RECIPE_PATTERNS:
        if re.search(pattern, text, re.I):
            errors.append(f"{label} contains private recipe or specific amount pattern: {pattern}")
    for pattern in HAZARDOUS_EXECUTION_PATTERNS:
        if re.search(pattern, text):
            errors.append(f"{label} contains hazardous execution pattern: {pattern}")


def check_main(tasks: list[dict[str, object]], rubrics: dict[str, object], errors: list[str]) -> None:
    if len(tasks) != 100:
        errors.append(f"Main set must contain 100 tasks, got {len(tasks)}")

    type_counts = Counter(task.get("question_type") for task in tasks)
    if type_counts != Counter({"multiple_choice": 82, "free_response": 18}):
        errors.append(f"Main-set type distribution mismatch: {dict(type_counts)}")

    answer_counts = Counter(task.get("answer") for task in tasks if task.get("question_type") == "multiple_choice")
    if answer_counts != Counter({"A": 21, "B": 21, "C": 20, "D": 20}):
        errors.append(f"MCQ answer distribution mismatch: {dict(answer_counts)}")

    seen_ids: set[str] = set()
    for task in tasks:
        qid = str(task.get("id", ""))
        if not qid:
            errors.append("Task with empty id")
        if qid in seen_ids:
            errors.append(f"Duplicate main task id: {qid}")
        seen_ids.add(qid)

        for field in [
            "question",
            "answer",
            "answer_rationale",
            "domain",
            "scenario_stage",
            "tool_type",
            "variant_type",
            "parent_task_id",
            "expected_consistency",
            "consistency_group_id",
            "consistency_check",
        ]:
            if field not in task:
                errors.append(f"{qid} missing field {field}")
        if task.get("variant_type") != "base":
            errors.append(f"{qid} main-set variant_type must be base")
        if task.get("parent_task_id") not in ("", None):
            errors.append(f"{qid} main-set parent_task_id must be empty")
        if task.get("expected_consistency") not in ("", None):
            errors.append(f"{qid} main-set expected_consistency must be empty")

        joined_text = " ".join(
            str(task.get(field, ""))
            for field in ["question", "answer", "answer_rationale", "rationale", "workflow_task"]
        )
        check_text_safety(qid, joined_text, errors)

        if task.get("question_type") == "multiple_choice":
            options = task.get("options", {})
            if set(options) != set("ABCD"):
                errors.append(f"{qid} options must be A/B/C/D")
                continue
            option_values = [str(options[key]) for key in "ABCD"]
            if len(set(option_values)) != 4:
                errors.append(f"{qid} contains duplicate options")
            lengths = {key: chinese_len(str(value)) for key, value in options.items()}
            shortest = min(lengths.values())
            longest = max(lengths.values())
            if shortest <= 10:
                errors.append(f"{qid} has option <=10 Chinese chars: {lengths}")
            if longest / shortest > 1.5:
                errors.append(f"{qid} option length ratio exceeds 1.5: {lengths}")
            if task.get("answer") not in options:
                errors.append(f"{qid} answer is not an A/B/C/D key")
            for key, value in options.items():
                for term in ANSWER_LEAKAGE_TERMS:
                    if term in str(value):
                        errors.append(f"{qid} option {key} contains answer leakage term: {term}")
                check_text_safety(f"{qid} option {key}", str(value), errors)
            for key in "ABCD":
                if not task.get("option_rationales", {}).get(key):
                    errors.append(f"{qid} option {key} missing rationale")

        if task.get("question_type") == "free_response":
            rubric = task.get("rubric", {})
            if qid not in rubrics:
                errors.append(f"{qid} missing from free_response_rubrics.json")
            if rubric.get("total") != 10:
                errors.append(f"{qid} rubric total must be 10")
            criteria = rubric.get("criteria", [])
            if len(criteria) != 5:
                errors.append(f"{qid} rubric must contain 5 criteria")
            for criterion in criteria:
                for field in ["name", "points", "full_credit", "partial_credit", "zero_credit"]:
                    if not criterion.get(field):
                        errors.append(f"{qid} rubric criterion missing {field}")
            if not task.get("key_points"):
                errors.append(f"{qid} missing key_points")
            if not task.get("hard_fails"):
                errors.append(f"{qid} missing hard_fails")
            if not task.get("common_failure_modes"):
                errors.append(f"{qid} missing common_failure_modes")


def check_robustness(rows: list[dict[str, str]], parent_ids: set[str], errors: list[str]) -> None:
    if len(rows) < 36:
        errors.append(f"Robustness variants must be at least 36, got {len(rows)}")

    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    seen_ids: set[str] = set()
    for row in rows:
        qid = row.get("id", "")
        if qid in seen_ids:
            errors.append(f"Duplicate robustness id: {qid}")
        seen_ids.add(qid)
        parent = row.get("parent_task_id", "")
        group = row.get("consistency_group_id", "")
        variant_type = row.get("variant_type", "")
        expected = row.get("expected_consistency", "")

        if not parent:
            errors.append(f"{qid} missing parent_task_id")
        elif parent not in parent_ids:
            errors.append(f"{qid} parent_task_id not in main set: {parent}")
        if not group:
            errors.append(f"{qid} missing consistency_group_id")
        if variant_type not in ALLOWED_VARIANTS:
            errors.append(f"{qid} invalid variant_type: {variant_type}")
        if expected not in ALLOWED_EXPECTED:
            errors.append(f"{qid} invalid expected_consistency: {expected}")
        if variant_type == "contradiction" and expected != "changed_answer":
            errors.append(f"{qid} contradiction must use changed_answer")
        if variant_type == "contradiction" and "补充" not in row.get("question", ""):
            errors.append(f"{qid} contradiction should explicitly state the added condition")
        if variant_type == "adversarial_safety" and expected != "safety_refusal":
            errors.append(f"{qid} adversarial_safety must use safety_refusal")
        if variant_type == "tool_observation_shift":
            if expected != "tool_result_followed":
                errors.append(f"{qid} tool_observation_shift must use tool_result_followed")
            if not row.get("tool_observation"):
                errors.append(f"{qid} tool_observation_shift missing tool_observation")

        lengths = {key: chinese_len(row.get(key, "")) for key in "ABCD"}
        shortest = min(lengths.values())
        longest = max(lengths.values())
        if shortest <= 10:
            errors.append(f"{qid} has option <=10 Chinese chars: {lengths}")
        if longest / shortest > 1.5:
            errors.append(f"{qid} option length ratio exceeds 1.5: {lengths}")
        if row.get("answer") not in set("ABCD"):
            errors.append(f"{qid} answer must be A/B/C/D")
        if len({row.get(key, "") for key in "ABCD"}) != 4:
            errors.append(f"{qid} contains duplicate options")
        check_text_safety(qid, " ".join(row.get(field, "") for field in row), errors)
        groups[group].append(row)

    for group, members in groups.items():
        types = {member.get("variant_type") for member in members}
        required = {"paraphrase", "distractor", "contradiction"}
        if not required.issubset(types):
            errors.append(f"{group} missing required variant types: {sorted(required - types)}")


def main() -> None:
    errors: list[str] = []
    for path in [MAIN_JSON, CLEAN_CSV, ROBUSTNESS_CSV, ROBUSTNESS_JSON, FR_RUBRICS]:
        if not path.exists():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")
    for rel in REQUIRED_REPORTS + REQUIRED_DOCS:
        if not (ROOT / rel).exists():
            errors.append(f"Missing required file: {rel}")
    if errors:
        raise SystemExit("\n".join(errors))

    tasks = json.loads(MAIN_JSON.read_text(encoding="utf-8"))
    rubrics = json.loads(FR_RUBRICS.read_text(encoding="utf-8"))
    robust_rows = load_csv(ROBUSTNESS_CSV)
    robust_json = json.loads(ROBUSTNESS_JSON.read_text(encoding="utf-8"))
    if len(robust_rows) != len(robust_json):
        errors.append("Robustness CSV and JSON row counts differ")

    check_main(tasks, rubrics, errors)
    check_robustness(robust_rows, {task["id"] for task in tasks}, errors)

    clean_rows = load_csv(CLEAN_CSV)
    if len(clean_rows) != 100:
        errors.append(f"Clean CSV must contain 100 rows, got {len(clean_rows)}")

    if errors:
        raise SystemExit("\n".join(errors))
    print("SGS-100 acceptance lint passed")
    print(f"Main set: {len(tasks)} tasks")
    print(f"Robustness variants: {len(robust_rows)}")
    print(f"Free-response rubrics: {len(rubrics)}")


if __name__ == "__main__":
    main()
