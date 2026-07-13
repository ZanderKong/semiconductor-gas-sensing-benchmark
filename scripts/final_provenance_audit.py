#!/usr/bin/env python3
"""Audit the 0.5.0 RC evidence chain."""

from __future__ import annotations

import csv
import hashlib
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
    ROOT / "docs/scoring_protocol.md",
    ROOT / "reports/evaluation_report.md",
    ROOT / "reports/model_error_analysis.md",
    ROOT / "reports/iteration_notes.md",
    ROOT / "results/README.md",
    ROOT / "reports/final_release_audit.md",
    ROOT / "reports/free_response_evaluation_report.md",
    ROOT / "reports/manual_review_plan.md",
    RUN / "analysis_core/core_analysis.md",
    RUN / "analysis_full/full_analysis.md",
    RUN / "free_response_judge/judge_report.md",
]
EXPECTED_COMMIT_PREFIX = "70b77e8"
EXPECTED_JUDGE_COMMIT_PREFIX = "ee04eff"
EXPECTED_RESULTS = {
    "deepseek-v4-pro": {"mcq": (115, 122), "fr": "6.762", "robustness": (29, 40), "hard50": (47, 50)},
    "ep-20260703090429-qpmt7": {"mcq": (118, 122), "fr": "7.522", "robustness": (32, 40), "hard50": (48, 50)},
    "gpt-5.5": {"mcq": (117, 122), "fr": "8.15", "robustness": (34, 40), "hard50": (48, 50)},
    "mimo-v2.5-pro": {"mcq": (119, 122), "fr": "5.448", "robustness": (34, 40), "hard50": (47, 50)},
}
EXPECTED_HARD_FAILS = {
    "deepseek-v4-pro": 0,
    "ep-20260703090429-qpmt7": 4,
    "gpt-5.5": 0,
    "mimo-v2.5-pro": 11,
}
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
    RUN / "free_response_judge/human_review_decisions.template.csv",
    RUN / "free_response_judge/human_review_overrides.template.csv",
    RUN / "free_response_judge/adjudication_notes.template.md",
    RUN / "free_response_judge/human_review_decisions.csv",
    RUN / "free_response_judge/human_review_overrides.csv",
    RUN / "free_response_judge/adjudication_notes.md",
    RUN / "free_response_judge/adjudication_manifest.json",
    RUN / "free_response_judge/adjudicated_free_response_summary.csv",
    RUN / "free_response_judge/adjudicated_free_response_by_item.csv",
    RUN / "free_response_judge/adjudicated_free_response_by_dimension.csv",
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


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    require(str(judge.get("code_commit", "")).startswith(EXPECTED_JUDGE_COMMIT_PREFIX), "judge manifest commit mismatch", errors)
    require(judge.get("working_tree_dirty") is False, "judge manifest dirty must be false", errors)
    require(judge.get("internet_access") is False, "judge internet_access must be false", errors)
    require(judge.get("tool_assistance") is False, "judge tool_assistance must be false", errors)
    require(judge.get("judge_model") == "gpt-5.6-sol", "free-response judge must be gpt-5.6-sol", errors)
    require("not a participating model" in str(judge.get("bias_note", "")), "judge non-participant bias note missing", errors)
    for model_id in EXPECTED_RESULTS:
        status = judge.get("model_status", {}).get(model_id, {})
        require(status.get("rows") == 30, f"judge input count mismatch for {model_id}", errors)
        require(status.get("reviews") == 30, f"judge review count mismatch for {model_id}", errors)
        require(status.get("errors") == 0, f"judge error recorded for {model_id}", errors)
    require("gpt-5.6-sol" not in judge.get("model_status", {}), "judge must not appear as a candidate model", errors)


def result_map(path: Path) -> dict[str, dict[str, str]]:
    return {row["model_id"]: row for row in read_csv(path)}


def check_results(errors: list[str]) -> None:
    mcq = result_map(RUN / "sgs152_mcq/scored/model_results_summary.csv")
    fr = result_map(RUN / "free_response_judge/adjudicated_free_response_summary.csv")
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


def check_judge_not_candidate(errors: list[str]) -> None:
    candidate_files = [
        RUN / "sgs152_mcq/model_outputs.csv",
        RUN / "sgs152_free_response/model_outputs.csv",
        RUN / "robustness/model_outputs.csv",
        RUN / "hard50/model_outputs.csv",
    ]
    expected_models = set(EXPECTED_RESULTS)
    for path in candidate_files:
        models = {row["model_id"] for row in read_csv(path) if row.get("model_id")}
        require("gpt-5.6-sol" not in models, f"judge appears as candidate in {rel(path)}", errors)
        require(models == expected_models, f"candidate model set mismatch in {rel(path)}: {sorted(models)}", errors)


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
    decisions_template = RUN / "free_response_judge/human_review_decisions.template.csv"
    overrides_template = RUN / "free_response_judge/human_review_overrides.template.csv"
    notes_template = RUN / "free_response_judge/adjudication_notes.template.md"
    require(packet_path.exists(), "manual review packet missing", errors)
    require(decisions_template.exists(), "human review decisions template missing", errors)
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
    for row in packet:
        for field in ["human_decision", "human_total_score", "override_reason", "reviewer", "review_date", "affects_summary"]:
            require(not row.get(field), f"pending review packet field {field} must be blank for {(row['id'], row['model_id'])}", errors)

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


def check_delegated_adjudication(errors: list[str]) -> None:
    judge_dir = RUN / "free_response_judge"
    decisions_path = judge_dir / "human_review_decisions.csv"
    overrides_path = judge_dir / "human_review_overrides.csv"
    notes_path = judge_dir / "adjudication_notes.md"
    manifest_path = judge_dir / "adjudication_manifest.json"
    for path in [decisions_path, overrides_path, notes_path, manifest_path]:
        require(path.exists(), f"delegated review artifact missing: {rel(path)}", errors)
    if all(path.exists() for path in [decisions_path, overrides_path, notes_path, manifest_path]):
        decisions = read_csv(decisions_path)
        overrides = read_csv(overrides_path)
        manifest = load_json(manifest_path)
        decision_counts: dict[str, int] = {}
        for row in decisions:
            decision_counts[row["review_decision"]] = decision_counts.get(row["review_decision"], 0) + 1
            require(row["review_type"] == "assistant_review_under_project_owner_delegation", "delegated review type mismatch", errors)
            require(row["reviewer"] == "codex_assistant_under_user_delegation", "delegated reviewer mismatch", errors)
            require(row["review_date"] == "2026-07-13", "delegated review date mismatch", errors)
        require(len(decisions) == 58, "delegated review must contain 58 decisions", errors)
        require(len({(row["id"], row["model_id"]) for row in decisions}) == 58, "delegated review decisions must be unique", errors)
        require(
            decision_counts == {"agree": 33, "hard_fail_confirmed": 15, "missing_kept_zero": 1, "adjust_score": 9},
            f"delegated decision counts mismatch: {decision_counts}",
            errors,
        )
        require(len(overrides) == 9, "delegated review must contain 9 dimension overrides", errors)
        for row in overrides:
            require(row["dimension"] == "safety_and_privacy", "delegated override must target safety_and_privacy", errors)
            require(float(row["review_score"]) > float(row["judge_score"]), "delegated safety override must correct an over-penalty", errors)
            require(bool(row["override_reason"]), "delegated override reason missing", errors)
        require(manifest.get("reviewed_items") == 58, "adjudication manifest reviewed count mismatch", errors)
        require(manifest.get("dimension_overrides") == 9, "adjudication manifest override count mismatch", errors)
        require(manifest.get("unresolved_items") == 0, "adjudication manifest must have no unresolved items", errors)
        require(manifest.get("independent_external_human_review") is False, "delegated review must not claim external human review", errors)
        require(manifest.get("decisions_hash") == sha256_file(decisions_path), "delegated decisions hash mismatch", errors)
        require(manifest.get("overrides_hash") == sha256_file(overrides_path), "delegated overrides hash mismatch", errors)
        require(
            manifest.get("adjudicated_summary_hash") == sha256_file(judge_dir / "adjudicated_free_response_summary.csv"),
            "adjudicated summary hash mismatch",
            errors,
        )
        notes = notes_path.read_text(encoding="utf-8")
        require("not an independent external human blind review" in notes, "delegated review boundary missing", errors)
        require("unresolved items requiring project-owner discussion: 0" in notes, "unresolved-item statement missing", errors)

    history = ROOT / "archive/judge_history/gpt-5.5_20260703"
    require(history.exists(), "GPT-5.5 judge history archive missing", errors)
    history_manifest = history / "judge_manifest.json"
    require(history_manifest.exists(), "GPT-5.5 judge history manifest missing", errors)
    if history_manifest.exists():
        require(load_json(history_manifest).get("judge_model") == "gpt-5.5", "judge history archive is not GPT-5.5", errors)


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
        "GPT-5.5/ChatGPT",
        "assistant-assisted project-owner confirmed adjudication",
        "7.485",
        "6.888",
        "6.303",
        "4.843",
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
        require(path.exists(), f"{rel(path)} parsed/manifest evidence missing", errors)
        require(rel(path) in tracked or not git_check_ignore(path), f"{rel(path)} must be available for commit", errors)
    for raw_dir in RAW_DIRS:
        require(raw_dir.exists(), f"{rel(raw_dir)} missing locally", errors)
        require(git_check_ignore(raw_dir), f"{rel(raw_dir)} should be ignored, not committed", errors)
        tracked_raw = [path for path in tracked if path.startswith(rel(raw_dir) + "/")]
        require(not tracked_raw, f"{rel(raw_dir)} contains tracked raw outputs", errors)


def check_api_keys(errors: list[str]) -> None:
    tracked_paths = {ROOT / rel_path for rel_path in git_ls_files()}
    standard_run_paths = {path for path in RUN.rglob("*") if path.is_file()}
    paths_to_scan = sorted(path for path in tracked_paths | standard_run_paths if path.exists())
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
    check_judge_not_candidate(errors)
    check_missing_answer(errors)
    check_manual_review_packet(errors)
    check_delegated_adjudication(errors)
    check_public_docs(errors)
    check_deprecated_artifacts(errors)
    check_standard_git_policy(errors)
    check_api_keys(errors)
    if errors:
        raise SystemExit("Final provenance audit failed:\n" + "\n".join(f"- {error}" for error in errors))
    print("Final provenance audit passed")


if __name__ == "__main__":
    main()
