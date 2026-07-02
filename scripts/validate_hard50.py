#!/usr/bin/env python3
"""Validate the SGS-Hard-50 diagnostic set."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HARD_JSON = ROOT / "data/benchmark_sgs_hard50.json"
HARD_CSV = ROOT / "data/benchmark_sgs_hard50.csv"

EXPECTED_TYPES = Counter(
    {
        "evidence_conflict": 10,
        "condition_update": 10,
        "safety_boundary": 8,
        "tool_observation_update": 8,
        "multi_objective_tradeoff": 8,
        "mechanism_transfer_trap": 6,
    }
)
EXPECTED_ANSWERS = Counter({"A": 13, "B": 13, "C": 12, "D": 12})
FORBIDDEN_TERMS = [
    "只要",
    "直接",
    "一定",
    "完全",
    "无需",
    "忽略",
    "唯一正确",
    "显然正确",
    "标准答案",
]
REQUIRED_FIELDS = [
    "id",
    "question_type",
    "diagnostic_type",
    "domain",
    "scenario_stage",
    "tool_type",
    "question",
    "options",
    "answer",
    "answer_rationale",
    "option_profiles",
    "option_rationales",
    "difficulty",
    "failure_mode",
    "benchmark_version",
    "hard_set_goal",
]


def chinese_len(value: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", value))


def main() -> None:
    errors: list[str] = []
    if not HARD_JSON.exists():
        errors.append(f"Missing required file: {HARD_JSON.relative_to(ROOT)}")
    if not HARD_CSV.exists():
        errors.append(f"Missing required file: {HARD_CSV.relative_to(ROOT)}")
    if errors:
        raise SystemExit("\n".join(errors))

    rows = json.loads(HARD_JSON.read_text(encoding="utf-8"))
    if len(rows) != 50:
        errors.append(f"Expected 50 hard-set items, got {len(rows)}")

    answer_counts = Counter()
    type_counts = Counter()
    answer_longest = 0
    answer_shortest = 0
    seen_ids: set[str] = set()

    for row in rows:
        qid = str(row.get("id", ""))
        if qid in seen_ids:
            errors.append(f"Duplicate id: {qid}")
        seen_ids.add(qid)
        if not re.fullmatch(r"SGS-HARD-\d{3}", qid):
            errors.append(f"{qid} has non-canonical hard-set id")
        for field in REQUIRED_FIELDS:
            if field not in row:
                errors.append(f"{qid} missing field {field}")

        if row.get("question_type") != "multiple_choice":
            errors.append(f"{qid} must be multiple_choice")
        diagnostic_type = row.get("diagnostic_type")
        type_counts[diagnostic_type] += 1
        answer = row.get("answer")
        answer_counts[answer] += 1
        if answer not in set("ABCD"):
            errors.append(f"{qid} answer must be A/B/C/D")

        options = row.get("options", {})
        if set(options) != set("ABCD"):
            errors.append(f"{qid} options must be A/B/C/D")
            continue
        if len(set(options.values())) != 4:
            errors.append(f"{qid} contains duplicate options")

        lengths = {key: chinese_len(str(value)) for key, value in options.items()}
        shortest = min(lengths.values())
        longest = max(lengths.values())
        if shortest <= 10:
            errors.append(f"{qid} has option <=10 Chinese chars: {lengths}")
        if longest / shortest > 1.45:
            errors.append(f"{qid} option length ratio exceeds 1.45: {lengths}")
        if lengths.get(answer) == longest:
            answer_longest += 1
        if lengths.get(answer) == shortest:
            answer_shortest += 1

        joined = " ".join(
            [str(row.get("question", "")), str(row.get("answer_rationale", ""))]
            + [str(value) for value in options.values()]
        )
        for term in FORBIDDEN_TERMS:
            if term in joined:
                errors.append(f"{qid} contains forbidden shortcut term: {term}")

        profiles = row.get("option_profiles", {})
        rationales = row.get("option_rationales", {})
        for key in "ABCD":
            if not profiles.get(key):
                errors.append(f"{qid} option {key} missing profile")
            if not rationales.get(key):
                errors.append(f"{qid} option {key} missing rationale")
        if profiles.get(answer) != "best":
            errors.append(f"{qid} answer profile must be best")

    if type_counts != EXPECTED_TYPES:
        errors.append(f"Diagnostic type distribution mismatch: {dict(type_counts)}")
    if answer_counts != EXPECTED_ANSWERS:
        errors.append(f"Answer distribution mismatch: {dict(answer_counts)}")
    if answer_longest > 18:
        errors.append(f"Too many answers are longest options: {answer_longest}")
    if answer_shortest > 18:
        errors.append(f"Too many answers are shortest options: {answer_shortest}")

    if errors:
        raise SystemExit("\n".join(errors))
    print("SGS-Hard-50 validation passed: 50 MCQ items with diagnostic coverage and balanced options")


if __name__ == "__main__":
    main()
