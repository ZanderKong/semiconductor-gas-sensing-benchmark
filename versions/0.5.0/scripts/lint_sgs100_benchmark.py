#!/usr/bin/env python3
"""Acceptance lint for mini-benchmark 0.5.0."""

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
HARD_JSON = ROOT / "data/benchmark_sgs_hard50.json"
HARD_CSV = ROOT / "data/benchmark_sgs_hard50.csv"
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
    "reports/benchmark_design_report.md",
    "reports/mcq_quality_report.md",
    "reports/model_diagnostic_report.md",
    "reports/model_evaluation_recap.md",
    "reports/hard_set_evaluation_report.md",
    "reports/project_review_report.md",
    "reports/sgs100_revision_report.md",
    "reports/sgs100_robustness_report.md",
    "reports/delivery_audit.md",
]
REQUIRED_DOCS = [
    "docs/robustness_variant_design.md",
    "docs/free_response_rubric_design.md",
    "docs/reviewer_guide.md",
    "docs/hard_set_design.md",
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
    if len(tasks) != 152:
        errors.append(f"Main set must contain 152 tasks, got {len(tasks)}")

    type_counts = Counter(task.get("question_type") for task in tasks)
    if type_counts != Counter({"multiple_choice": 122, "free_response": 30}):
        errors.append(f"Main-set type distribution mismatch: {dict(type_counts)}")

    answer_counts = Counter(task.get("answer") for task in tasks if task.get("question_type") == "multiple_choice")
    if answer_counts != Counter({"A": 34, "B": 29, "C": 29, "D": 29, "E": 1}):
        errors.append(f"MCQ answer distribution mismatch: {dict(answer_counts)}")

    seen_ids: set[str] = set()
    for task in tasks:
        qid = str(task.get("id", ""))
        is_failure_mined = qid.startswith("SGS-FM-")
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
        if is_failure_mined:
            if task.get("variant_type") != "failure_mined_case":
                errors.append(f"{qid} failure-mined item variant_type must be failure_mined_case")
        elif task.get("variant_type") != "base":
            errors.append(f"{qid} main-set variant_type must be base")
        if not is_failure_mined and task.get("parent_task_id") not in ("", None):
            errors.append(f"{qid} main-set parent_task_id must be empty")
        if not is_failure_mined and task.get("expected_consistency") not in ("", None):
            errors.append(f"{qid} main-set expected_consistency must be empty")

        joined_text = " ".join(
            str(task.get(field, ""))
            for field in ["question", "answer", "answer_rationale", "rationale", "workflow_task"]
        )
        check_text_safety(qid, joined_text, errors)

        if task.get("question_type") == "multiple_choice":
            options = task.get("options", {})
            allowed = [chr(ord("A") + idx) for idx in range(len(options))]
            min_options = 2 if is_failure_mined else 4
            if list(options.keys()) != allowed or len(options) < min_options:
                errors.append(f"{qid} options must be sequential from A and have enough options")
                continue
            if len(set(str(value) for value in options.values())) != len(options):
                errors.append(f"{qid} contains duplicate options")
            lengths = {key: chinese_len(str(value)) for key, value in options.items()}
            if not is_failure_mined:
                shortest = min(lengths.values())
                longest = max(lengths.values())
                if shortest <= 10:
                    errors.append(f"{qid} has option <=10 Chinese chars: {lengths}")
                if longest / shortest > 1.5:
                    errors.append(f"{qid} option length ratio exceeds 1.5: {lengths}")
            if task.get("answer") not in options:
                errors.append(f"{qid} answer is not an option key")
            for key, value in options.items():
                if not is_failure_mined:
                    for term in ANSWER_LEAKAGE_TERMS:
                        if term in str(value):
                            errors.append(f"{qid} option {key} contains answer leakage term: {term}")
                    check_text_safety(f"{qid} option {key}", str(value), errors)
            for key in options:
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


def check_hard_set(rows: list[dict[str, object]], errors: list[str]) -> None:
    if len(rows) != 50:
        errors.append(f"Hard set must contain 50 tasks, got {len(rows)}")
    type_counts = Counter(row.get("diagnostic_type") for row in rows)
    expected_types = Counter(
        {
            "evidence_conflict": 10,
            "condition_update": 10,
            "safety_boundary": 8,
            "tool_observation_update": 8,
            "multi_objective_tradeoff": 8,
            "mechanism_transfer_trap": 6,
        }
    )
    if type_counts != expected_types:
        errors.append(f"Hard-set diagnostic distribution mismatch: {dict(type_counts)}")
    answer_counts = Counter(row.get("answer") for row in rows)
    if answer_counts != Counter({"A": 13, "B": 13, "C": 12, "D": 12}):
        errors.append(f"Hard-set answer distribution mismatch: {dict(answer_counts)}")
    for row in rows:
        qid = str(row.get("id", ""))
        if not re.fullmatch(r"SGS-HARD-\d{3}", qid):
            errors.append(f"{qid} has non-canonical hard-set id")
        if row.get("question_type") != "multiple_choice":
            errors.append(f"{qid} hard-set task must be multiple_choice")
        options = row.get("options", {})
        if set(options) != set("ABCD"):
            errors.append(f"{qid} hard-set options must be A/B/C/D")
            continue
        lengths = {key: chinese_len(str(value)) for key, value in options.items()}
        shortest = min(lengths.values())
        longest = max(lengths.values())
        if shortest <= 10:
            errors.append(f"{qid} hard-set option <=10 Chinese chars: {lengths}")
        if longest / shortest > 1.45:
            errors.append(f"{qid} hard-set option length ratio exceeds 1.45: {lengths}")
        if row.get("option_profiles", {}).get(row.get("answer")) != "best":
            errors.append(f"{qid} hard-set answer profile must be best")


def main() -> None:
    errors: list[str] = []
    for path in [MAIN_JSON, CLEAN_CSV, ROBUSTNESS_CSV, ROBUSTNESS_JSON, HARD_JSON, HARD_CSV, FR_RUBRICS]:
        if not path.exists():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")
    for rel in REQUIRED_REPORTS + REQUIRED_DOCS:
        if not (ROOT / rel).exists():
            errors.append(f"Missing required file: {rel}")
    if errors:
        raise SystemExit("\n".join(errors))

    tasks = json.loads(MAIN_JSON.read_text(encoding="utf-8"))
    rubrics = json.loads(FR_RUBRICS.read_text(encoding="utf-8"))
    hard_rows = json.loads(HARD_JSON.read_text(encoding="utf-8"))
    robust_rows = load_csv(ROBUSTNESS_CSV)
    robust_json = json.loads(ROBUSTNESS_JSON.read_text(encoding="utf-8"))
    if len(robust_rows) != len(robust_json):
        errors.append("Robustness CSV and JSON row counts differ")

    check_main(tasks, rubrics, errors)
    check_robustness(robust_rows, {task["id"] for task in tasks}, errors)
    check_hard_set(hard_rows, errors)

    clean_rows = load_csv(CLEAN_CSV)
    if len(clean_rows) != 100:
        errors.append(f"Legacy SGS100 clean CSV must contain 100 rows, got {len(clean_rows)}")

    if errors:
        raise SystemExit("\n".join(errors))
    print("mini-benchmark 0.5.0 acceptance lint passed")
    print(f"Main set: {len(tasks)} tasks")
    print("Legacy SGS100 clean export remains available for historical comparison")
    print(f"Robustness variants: {len(robust_rows)}")
    print(f"Hard-set items: {len(hard_rows)}")
    print(f"Free-response rubrics: {len(rubrics)}")


if __name__ == "__main__":
    main()
