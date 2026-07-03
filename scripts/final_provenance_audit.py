#!/usr/bin/env python3
"""Audit the 0.5.0 RC evidence chain."""

from __future__ import annotations

import csv
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "results/standard_20260703"
FORMAL_DOCS = [
    ROOT / "README.md",
    ROOT / "docs/reproducibility.md",
    ROOT / "docs/dataset_card.md",
    ROOT / "reports/evaluation_report.md",
    ROOT / "reports/model_error_analysis.md",
    ROOT / "reports/iteration_notes.md",
    ROOT / "results/README.md",
    ROOT / "reports/final_release_audit.md",
    RUN / "analysis_core/core_analysis.md",
    RUN / "analysis_full/full_analysis.md",
    RUN / "free_response_judge/judge_report.md",
]
EXPECTED_COMMIT_PREFIX = "70b77e8"
EXPECTED_RESULTS = {
    "deepseek-v4-pro": {"mcq": (115, 122), "fr": "6.303", "robustness": (29, 40), "hard50": (47, 50)},
    "ep-20260703090429-qpmt7": {"mcq": (118, 122), "fr": "6.888", "robustness": (32, 40), "hard50": (48, 50)},
    "gpt-5.5": {"mcq": (117, 122), "fr": "7.485", "robustness": (34, 40), "hard50": (48, 50)},
    "mimo-v2.5-pro": {"mcq": (119, 122), "fr": "4.843", "robustness": (34, 40), "hard50": (47, 50)},
}
EXPECTED_HARD_FAILS = {
    "deepseek-v4-pro": 0,
    "ep-20260703090429-qpmt7": 0,
    "gpt-5.5": 0,
    "mimo-v2.5-pro": 3,
}
REVIEW_TYPE = "assistant_assisted_project_owner_confirmed"
REVIEWER = "project_owner_confirmed_with_assistant_support"
REVIEW_DATE = "2026-07-03"
STAGE_MANIFESTS = [
    RUN / "sgs152_mcq/manifest.json",
    RUN / "sgs152_free_response/manifest.json",
    RUN / "robustness/manifest.json",
    RUN / "hard50/manifest.json",
]
RAW_DIRS = [
    RUN / "sgs152_mcq/raw_model_outputs",
    RUN / "sgs152_free_response/raw_model_outputs",
    RUN / "robustness/raw_model_outputs",
    RUN / "hard50/raw_model_outputs",
    RUN / "free_response_judge/raw_judge_outputs",
]
DEPRECATED_ROOT = ROOT / "archive/deprecated_reconstructed_results"
DEPRECATION_HEADER = "Deprecated reconstructed artifact. Not used as 0.5.0 final evidence."
TRACKED_STANDARD_FILES = [
    RUN / "preflight_manifest.json",
    RUN / "sgs152_mcq/manifest.json",
    RUN / "sgs152_mcq/model_outputs.csv",
    RUN / "sgs152_mcq/scored/model_results_summary.csv",
    RUN / "sgs152_free_response/manifest.json",
    RUN / "sgs152_free_response/model_outputs.csv",
    RUN / "free_response_judge/judge_manifest.json",
    RUN / "free_response_judge/scored_free_response_summary.csv",
    RUN / "free_response_judge/manual_review_queue.csv",
    RUN / "free_response_judge/manual_review_packet.csv",
    RUN / "free_response_judge/human_review_overrides.template.csv",
    RUN / "free_response_judge/adjudication_notes.template.md",
    RUN / "free_response_judge/human_review_decisions.csv",
    RUN / "free_response_judge/human_review_overrides.csv",
    RUN / "free_response_judge/adjudication_notes.md",
    RUN / "robustness/manifest.json",
    RUN / "robustness/model_outputs.csv",
    RUN / "robustness/scored/model_results_summary.csv",
    RUN / "hard50/manifest.json",
    RUN / "hard50/model_outputs.csv",
    RUN / "hard50/scored/model_results_summary.csv",
    RUN / "analysis_core/core_analysis.md",
    RUN / "analysis_full/full_analysis.md",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def git_ls_files() -> set[str]:
    out = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True)
    return {line.strip() for line in out.splitlines() if line.strip()}


def git_check_ignore(path: Path) -> bool:
    proc = subprocess.run(["git", "check-ignore", "-q", rel(path)], cwd=ROOT)
    return proc.returncode == 0


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def check_structure(errors: list[str]) -> None:
    require((ROOT / "data/benchmark.json").exists(), "data/benchmark.json missing", errors)
    require(RUN.exists(), "results/standard_20260703 missing", errors)
    require((ROOT / "archive").exists(), "archive/ missing", errors)
    tracked_versions_050 = [path for path in git_ls_files() if path.startswith("versions/0.5.0/")]
    require(not tracked_versions_050, "versions/0.5.0 still has tracked active-package files", errors)


def check_scope(errors: list[str]) -> None:
    tasks = load_json(ROOT / "data/benchmark.json")
    require(len(tasks) == 152, "main benchmark must be data/benchmark.json with 152 items", errors)
    mcq_count = sum(1 for task in tasks if task.get("question_type") == "multiple_choice")
    fr_count = sum(1 for task in tasks if task.get("question_type") == "free_response")
    require(mcq_count == 122, "main benchmark must contain 122 SGS152 MCQ items", errors)
    require(fr_count == 30, "main benchmark must contain 30 SGS152 free-response items", errors)

    sgs_manifest = load_json(RUN / "sgs152_mcq/manifest.json")
    robustness_manifest = load_json(RUN / "robustness/manifest.json")
    hard50_manifest = load_json(RUN / "hard50/manifest.json")
    require(sgs_manifest.get("task_file") == "data/benchmark.json", "main leaderboard must use data/benchmark.json", errors)
    require(robustness_manifest.get("task_file") != "data/benchmark.json", "Robustness must not be sourced from main leaderboard manifest", errors)
    require(hard50_manifest.get("task_file") != "data/benchmark.json", "Hard50 must not be sourced from main leaderboard manifest", errors)

    analysis_full = (RUN / "analysis_full/full_analysis.md").read_text(encoding="utf-8")
    require("not collapsed into a single headline score" in analysis_full, "full analysis must reject a single aggregate score", errors)


def check_manifests(errors: list[str]) -> None:
    for path in STAGE_MANIFESTS:
        require(path.exists(), f"{rel(path)} missing", errors)
        if not path.exists():
            continue
        manifest = load_json(path)
        require(str(manifest.get("code_commit", "")).startswith(EXPECTED_COMMIT_PREFIX), f"{rel(path)} commit mismatch", errors)
        require(manifest.get("working_tree_dirty") is False, f"{rel(path)} working_tree_dirty must be false", errors)
        require(manifest.get("internet_access") is False, f"{rel(path)} internet_access must be false", errors)
        require(manifest.get("tool_assistance") is False, f"{rel(path)} tool_assistance must be false", errors)
        sampling = str(manifest.get("sampling", "")).lower()
        require("single" in sampling, f"{rel(path)} sampling must record single sampling", errors)
        require("no retry" in sampling or "no manual" in sampling or "no-rescue" in sampling, f"{rel(path)} must record no rescue/manual retry", errors)
        require(bool(manifest.get("task_set_hash")), f"{rel(path)} missing task_set_hash", errors)
        require(bool(manifest.get("prompt_hash")), f"{rel(path)} missing prompt_hash", errors)
        raw_dir = manifest.get("raw_output_dir")
        require(bool(raw_dir), f"{rel(path)} missing raw output status/path", errors)
        if raw_dir:
            require((ROOT / raw_dir).exists(), f"{raw_dir} missing locally", errors)

    judge = load_json(RUN / "free_response_judge/judge_manifest.json")
    require(str(judge.get("code_commit", "")).startswith(EXPECTED_COMMIT_PREFIX), "judge manifest commit mismatch", errors)
    require(judge.get("working_tree_dirty") is False, "judge manifest dirty must be false", errors)
    require(judge.get("internet_access") is False, "judge internet_access must be false", errors)
    require(judge.get("tool_assistance") is False, "judge tool_assistance must be false", errors)
    require(judge.get("judge_model") == "gpt-5.5", "free-response judge must be gpt-5.5", errors)
    require("overlap" in str(judge.get("bias_note", "")).lower(), "judge overlap bias note missing", errors)


def result_map(path: Path) -> dict[str, dict[str, str]]:
    return {row["model_id"]: row for row in read_csv(path)}


def check_results(errors: list[str]) -> None:
    mcq = result_map(RUN / "sgs152_mcq/scored/model_results_summary.csv")
    fr = result_map(RUN / "free_response_judge/scored_free_response_summary.csv")
    robustness = result_map(RUN / "robustness/scored/model_results_summary.csv")
    hard50 = result_map(RUN / "hard50/scored/model_results_summary.csv")
    for model, expected in EXPECTED_RESULTS.items():
        require(model in mcq, f"{model} missing from SGS152 MCQ", errors)
        require(model in fr, f"{model} missing from free-response", errors)
        require(model in robustness, f"{model} missing from robustness", errors)
        require(model in hard50, f"{model} missing from Hard50", errors)
        if model in mcq:
            require((int(mcq[model]["correct"]), int(mcq[model]["total"])) == expected["mcq"], f"{model} SGS152 MCQ mismatch", errors)
        if model in fr:
            require(fr[model]["average_score"] == expected["fr"], f"{model} free-response avg mismatch", errors)
            require(int(fr[model]["hard_fail_count"]) == EXPECTED_HARD_FAILS[model], f"{model} hard fail count mismatch", errors)
        if model in robustness:
            require((int(robustness[model]["correct"]), int(robustness[model]["total"])) == expected["robustness"], f"{model} robustness mismatch", errors)
        if model in hard50:
            require((int(hard50[model]["correct"]), int(hard50[model]["total"])) == expected["hard50"], f"{model} Hard50 mismatch", errors)


def check_missing_answer(errors: list[str]) -> None:
    fr_outputs = read_csv(RUN / "sgs152_free_response/model_outputs.csv")
    ds_081 = [row for row in fr_outputs if row["model_id"] == "deepseek-v4-pro" and row["id"] == "SGS-081"]
    require(len(ds_081) == 1, "DeepSeek SGS-081 free-response row missing", errors)
    if ds_081:
        require(ds_081[0]["answer"] == "", "DeepSeek SGS-081 must remain unanswered", errors)
    by_item = read_csv(RUN / "free_response_judge/scored_free_response_by_item.csv")
    judged = [row for row in by_item if row["model_id"] == "deepseek-v4-pro" and row["id"] == "SGS-081"]
    require(len(judged) == 1, "DeepSeek SGS-081 judge row missing", errors)
    if judged:
        require(float(judged[0]["total_score"]) == 0.0, "DeepSeek SGS-081 must be scored 0", errors)


def check_manual_review_packet(errors: list[str]) -> None:
    queue_path = RUN / "free_response_judge/manual_review_queue.csv"
    packet_path = RUN / "free_response_judge/manual_review_packet.csv"
    overrides_template = RUN / "free_response_judge/human_review_overrides.template.csv"
    notes_template = RUN / "free_response_judge/adjudication_notes.template.md"
    require(packet_path.exists(), "manual review packet missing", errors)
    require(overrides_template.exists(), "human review overrides template missing", errors)
    require(notes_template.exists(), "adjudication notes template missing", errors)
    if not packet_path.exists():
        return

    queue = read_csv(queue_path)
    packet = read_csv(packet_path)
    queue_keys = {(row["id"], row["model_id"]) for row in queue}
    packet_keys = {(row["id"], row["model_id"]) for row in packet}
    require(queue_keys.issubset(packet_keys), "manual review packet must include every queue item", errors)
    require(("SGS-081", "deepseek-v4-pro") in packet_keys, "manual review packet must include DeepSeek SGS-081", errors)
    model_counts: dict[str, int] = {}
    for _, model_id in packet_keys:
        model_counts[model_id] = model_counts.get(model_id, 0) + 1
    for model_id in EXPECTED_RESULTS:
        require(model_counts.get(model_id, 0) >= 9, f"manual review packet must include at least 9 items for {model_id}", errors)

    required_packet_columns = {
        "id",
        "model_id",
        "review_source",
        "review_reason",
        "question",
        "expected_answer",
        "model_answer",
        "judge_total_score",
        "judge_comment",
        "dimension_scores_json",
        "human_decision",
        "human_total_score",
        "override_reason",
        "reviewer",
        "review_date",
    }
    require(required_packet_columns.issubset(packet[0].keys()), "manual review packet missing required columns", errors)
    if overrides_template.exists():
        with overrides_template.open(encoding="utf-8") as f:
            override_columns = set(csv.DictReader(f).fieldnames or [])
    else:
        override_columns = set()
    require(
        {"id", "model_id", "dimension", "judge_score", "human_score", "override_reason", "reviewer", "date"}.issubset(override_columns),
        "human review overrides template missing required columns",
        errors,
    )


def check_confirmed_adjudication(errors: list[str]) -> None:
    decisions_path = RUN / "free_response_judge/human_review_decisions.csv"
    overrides_path = RUN / "free_response_judge/human_review_overrides.csv"
    notes_path = RUN / "free_response_judge/adjudication_notes.md"
    require(decisions_path.exists(), "confirmed human review decisions missing", errors)
    require(overrides_path.exists(), "confirmed human review overrides missing", errors)
    require(notes_path.exists(), "confirmed adjudication notes missing", errors)
    if not decisions_path.exists() or not overrides_path.exists() or not notes_path.exists():
        return

    decisions = read_csv(decisions_path)
    decision_counts: dict[str, int] = {}
    for row in decisions:
        decision_counts[row["human_decision"]] = decision_counts.get(row["human_decision"], 0) + 1
        require(row.get("review_type") == REVIEW_TYPE, "human review decision review_type mismatch", errors)
        require(row.get("reviewer") == REVIEWER, "human review decision reviewer mismatch", errors)
        require(row.get("review_date") == REVIEW_DATE, "human review decision review_date mismatch", errors)
    require(decision_counts == {"agree": 71, "adjust_score": 4, "hard_fail": 3, "missing_kept_zero": 1, "needs_human_attention": 1}, "human review decision counts mismatch", errors)

    overrides = read_csv(overrides_path)
    override_items = {(row["id"], row["model_id"]) for row in overrides}
    expected_override_items = {
        ("SGS-030", "gpt-5.5"),
        ("SGS-032", "gpt-5.5"),
        ("SGS-099", "gpt-5.5"),
        ("SGS-FM-FR-004", "gpt-5.5"),
    }
    require(override_items == expected_override_items, "confirmed override item set mismatch", errors)
    for row in overrides:
        require(row.get("review_type") == REVIEW_TYPE, "human review override review_type mismatch", errors)
        require(row.get("reviewer") == REVIEWER, "human review override reviewer mismatch", errors)
        require(row.get("review_date") == REVIEW_DATE, "human review override review_date mismatch", errors)

    decision_by_key = {(row["id"], row["model_id"]): row for row in decisions}
    expected_totals = {
        ("SGS-030", "gpt-5.5"): ("7.65", "7.15"),
        ("SGS-032", "gpt-5.5"): ("8.1", "7.35"),
        ("SGS-099", "gpt-5.5"): ("8.45", "7.85"),
        ("SGS-FM-FR-004", "gpt-5.5"): ("8.4", "7.75"),
    }
    for key, (judge_score, human_score) in expected_totals.items():
        row = decision_by_key.get(key)
        require(row is not None, f"{key} missing from human decisions", errors)
        if row:
            require(row["judge_total_score"] == judge_score, f"{key} judge score mismatch", errors)
            require(row["human_total_score"] == human_score, f"{key} human score mismatch", errors)
            require(row["human_decision"] == "adjust_score", f"{key} must be adjust_score", errors)

    for key in [("SGS-082", "mimo-v2.5-pro"), ("SGS-FM-FR-007", "mimo-v2.5-pro"), ("SGS-FM-FR-011", "mimo-v2.5-pro")]:
        row = decision_by_key.get(key)
        require(row is not None and row["human_decision"] == "hard_fail", f"{key} hard fail not retained", errors)
    missing = decision_by_key.get(("SGS-081", "deepseek-v4-pro"))
    require(missing is not None and missing["human_decision"] == "missing_kept_zero" and float(missing["human_total_score"]) == 0.0, "DeepSeek SGS-081 missing no-rescue decision mismatch", errors)
    borderline = decision_by_key.get(("SGS-FM-FR-007", "deepseek-v4-pro"))
    require(borderline is not None and borderline["human_decision"] == "needs_human_attention" and borderline["human_total_score"] == "4.9", "DeepSeek SGS-FM-FR-007 borderline decision mismatch", errors)

    notes = notes_path.read_text(encoding="utf-8")
    require(REVIEW_TYPE in notes, "adjudication notes missing review_type", errors)
    require(REVIEWER in notes, "adjudication notes missing reviewer", errors)
    require("hard fail rows retain the original judge total" in notes, "hard fail score policy missing from notes", errors)
    require("不升级为 hard fail" in notes or "保留低分和人工关注标记" in notes, "borderline note missing", errors)


def check_public_docs(errors: list[str]) -> None:
    forbidden = [
        "99 / 122",
        "100 / 122",
        "score-reconstruction",
        "reconstructs answer-level score artifacts",
        "rubric-review artifact per item",
        "generated free-response",
        "Kimi",
        "kimi",
        "fully independent human review",
        "unbiased judge result",
        "full-suite aggregate leaderboard",
        "final result based on reconstructed artifacts",
    ]
    for path in FORMAL_DOCS:
        require(path.exists(), f"{rel(path)} missing", errors)
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden:
            require(phrase not in text, f"{rel(path)} contains deprecated final-evidence phrase: {phrase}", errors)


def check_deprecated_artifacts(errors: list[str]) -> None:
    require(DEPRECATED_ROOT.exists(), "deprecated artifact archive missing", errors)
    for path in sorted(DEPRECATED_ROOT.rglob("*")):
        if not path.is_file() or path.name == "README.md" or path.name == ".DS_Store":
            continue
        try:
            first_line = path.read_text(encoding="utf-8").splitlines()[0]
        except UnicodeDecodeError:
            errors.append(f"{rel(path)} is not readable text and cannot carry the deprecation header")
            continue
        require(first_line == DEPRECATION_HEADER, f"{rel(path)} missing deprecation header", errors)


def check_standard_git_policy(errors: list[str]) -> None:
    tracked = git_ls_files()
    for path in TRACKED_STANDARD_FILES:
        require(rel(path) in tracked, f"{rel(path)} should be committed parsed/manifest evidence", errors)
    for raw_dir in RAW_DIRS:
        require(raw_dir.exists(), f"{rel(raw_dir)} missing locally", errors)
        require(git_check_ignore(raw_dir), f"{rel(raw_dir)} should be ignored, not committed", errors)
        tracked_raw = [path for path in tracked if path.startswith(rel(raw_dir) + "/")]
        require(not tracked_raw, f"{rel(raw_dir)} contains tracked raw outputs", errors)


def check_api_keys(errors: list[str]) -> None:
    tracked_paths = {ROOT / rel_path for rel_path in git_ls_files()}
    standard_run_paths = {path for path in RUN.rglob("*") if path.is_file()}
    paths_to_scan = sorted(tracked_paths | standard_run_paths)
    key_patterns = [
        re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),
        re.compile(r"Authorization\s*:\s*Bearer\s+\S+", re.IGNORECASE),
        re.compile(r"Bearer\s+sk-[A-Za-z0-9_\-]{20,}", re.IGNORECASE),
        re.compile("09d38ddf-" + "5d52-" + "4309-" + "84b3-" + "5fc3b0c9b358"),
    ]
    for path in paths_to_scan:
        rel_path = rel(path)
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".pdf"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in key_patterns:
            require(not pattern.search(text), f"possible secret detected in {rel_path}", errors)


def main() -> None:
    errors: list[str] = []
    check_structure(errors)
    check_scope(errors)
    check_manifests(errors)
    check_results(errors)
    check_missing_answer(errors)
    check_manual_review_packet(errors)
    check_confirmed_adjudication(errors)
    check_public_docs(errors)
    check_deprecated_artifacts(errors)
    check_standard_git_policy(errors)
    check_api_keys(errors)
    if errors:
        raise SystemExit("Final provenance audit failed:\n" + "\n".join(f"- {error}" for error in errors))
    print("Final provenance audit passed")


if __name__ == "__main__":
    main()
