#!/usr/bin/env python3
"""Release-gate audit for the integrated SGS Benchmark v0.6.0 package."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "review/v0.6.0"
INTERNAL = ROOT / "review/internal_provenance"
FROZEN_HASHES = {
    "data/benchmark.json": "e0d4d634f94a15ebf43a9d80beebc2613c9063f30dd5f3f5a11291b12d50ea9c",
    "data/benchmark_sgs100_robustness.json": "435bed00b2296e385e6bc9484c1f5711d19256e9145f4d9e622eb841cf46dc73",
    "data/benchmark_sgs_hard50.json": "0d21b89dc7f0f703e9c0a10e627a62a4e74f56c4eb0fc6f31083c31c210d15d3",
    "data/free_response_rubrics.json": "05d1dcef541de4d934a38c5aeb1f79b88620b793695f9d54b80ca64df0433bce",
}
SOURCE_ARCHIVES = {
    "1-sgs242_item_validity_review_v0.6.zip": "2b6bae353d210e5c3f9a82e82e334e654d1af9c8bc17cc1284323aa106e008b5",
    "2-sgs_benchmark_remaining_work_completion_v0.6.zip": "944591d3481f3c1a957aa535df2b0ca31b9cbf8f1e7faecb76d7bd9528d2a795",
    "3-sgs152_option_and_reference_evidence_audit_v0.6.zip": "8249881a42c4fe133aedcca6c381f0ee28b00019410242de4abb16c146b109c7",
    "4-sgs152_v0.6_review_package.zip": "3c61b49315acf5b0879e42ffde03e7d51cc4e2be3359fef47fa3a177c4a24805",
}
DIMENSIONS = {
    "final_answer_alignment", "professional_accuracy", "reasoning_path", "evidence_boundary",
    "experimental_design", "decision_logic", "safety_and_privacy", "conciseness_and_traceability",
}
ALLOWED_ROLES = {"", "专家 X", "项目负责人", "复核者", "Judge"}
FORBIDDEN_PUBLIC = re.compile(
    r"model[- ]assisted|assistant[-_ ]review|codex[_ ]assistant|human[-_ ]review|human[-_ ]reviewed|"
    r"human[-_ ]expert|human[-_ ]blind|independent external human|independent human|AI[-_ ]review|"
    r"AI[-_ ]reviewer|独立人类专家|真人专家|外部人类专家|人类专家共识|人工复核|专家\s*Y|Expert\s*Y",
    re.I,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def unique(rows: list[dict[str, str]], keys: list[str]) -> bool:
    values = [tuple(row[key] for key in keys) for row in rows]
    return len(values) == len(set(values))


def audit_counts(errors: list[str]) -> None:
    conflicts = read_csv(REVIEW / "00_scope/package_conflict_report.csv")
    require(
        bool(conflicts) and all(
            all(row.get(field, "") for field in ["conflict_id", "conflict_field", "primary_key", "selected_version", "preserved_old_location", "score_impact"])
            for row in conflicts
        ),
        "package conflict report is missing field/key/version/preservation decisions",
        errors,
    )
    integration = read_csv(REVIEW / "00_scope/integration_decision_log.csv")
    require(bool(integration) and all(row.get("primary_key") and row["primary_key"] != "defined by v0.6 audit" for row in integration), "integration decision log has unresolved primary keys", errors)
    for decision in integration:
        target = REVIEW / decision["target"]
        require(target.exists(), f"integration target is missing: {decision['target']}", errors)
        if target.suffix.lower() == ".csv":
            with target.open(encoding="utf-8-sig", newline="") as handle:
                fields = set(csv.DictReader(handle).fieldnames or [])
            declared = set(decision["primary_key"].split("+"))
            require(declared <= fields, f"integration primary key is not present in {decision['target']}: {decision['primary_key']}", errors)
    member_disposition = read_csv(INTERNAL / "source_package_member_disposition.csv")
    source_files = 0
    for archive_name in SOURCE_ARCHIVES:
        with zipfile.ZipFile(INTERNAL / "source_packages" / archive_name) as archive:
            source_files += sum(not name.endswith("/") for name in archive.namelist())
    require(len(member_disposition) == source_files, "source package disposition does not cover every ZIP file member", errors)
    require(unique(member_disposition, ["archive", "member_path"]), "source package disposition has duplicate member keys", errors)
    require(all(row["sha256"] and row["preserved_location"] for row in member_disposition), "source package disposition lacks hash/preservation evidence", errors)
    final_mapping = read_csv(INTERNAL / "final_source_package_repository_mapping.csv")
    require(len(final_mapping) == source_files and unique(final_mapping, ["archive", "source_member"]), "final source-package mapping does not cover every file member", errors)
    require(not any(row["classification"] in {"repository_missing", "content_conflict"} for row in final_mapping), "final source-package mapping has a missing file or unresolved conflict", errors)
    document_log = read_csv(INTERNAL / "source_document_review_log.csv")
    package_names = {"remaining_work", "option_evidence", "item_validity", "free_response"}
    document_types = {"README", "Manifest", "SHA256SUMS", "final_report", "Codex_integration"}
    require(len({row["package"] for row in document_log}) == 4, "source document review log must cover four packages", errors)
    require(all(any(row["package"] == package and row["document_type"] == kind for row in document_log) for package in package_names for kind in document_types), "source document review log lacks a required document category", errors)
    stats_inventory = read_csv(REVIEW / "08_statistics/statistical_diagnostic_inventory.csv")
    require(stats_inventory and all(row["status"] == "completed" for row in stats_inventory), "statistical diagnostic inventory still has incomplete entries", errors)
    require(all((REVIEW / "08_statistics" / row["output_field"]).exists() for row in stats_inventory), "statistical diagnostic inventory points to a missing output", errors)
    content_stats = json.loads((REVIEW / "08_statistics/content_quality_statistics.json").read_text(encoding="utf-8-sig"))
    require(content_stats.get("full_statistics_computation", {}).get("status") == "completed", "content quality statistics still reports an uncomputed raw run", errors)
    validity = read_csv(REVIEW / "01_item_validity/all_242_item_validity_review.csv")
    require(len(validity) == 242 and unique(validity, ["item_id"]), "item validity must be 242 unique IDs", errors)
    require(Counter(row["set_name"] for row in validity) == {"main": 152, "robustness": 40, "hard50": 50}, "item validity set counts differ", errors)
    for name, expected in [("main_152_item_validity_review.csv", 152), ("robustness_40_item_validity_review.csv", 40), ("hard50_50_item_validity_review.csv", 50)]:
        split_rows = read_csv(REVIEW / "01_item_validity" / name)
        require(len(split_rows) == expected and unique(split_rows, ["item_id"]), f"{name} count/keys differ", errors)
    option_summary = read_csv(REVIEW / "02_mcq_options/mcq_122_item_option_set_summary.csv")
    require(len(option_summary) == 122 and unique(option_summary, ["item_id"]), "MCQ option summary must be 122 unique items", errors)
    options = read_csv(REVIEW / "02_mcq_options/mcq_488_option_audit.csv")
    require(len(options) == 488 and unique(options, ["item_id", "option_letter"]), "MCQ option audit must be 488 unique rows", errors)
    require(len({row["item_id"] for row in options}) == 122, "MCQ option audit must cover 122 items", errors)
    require(all(count == 4 for count in Counter(row["item_id"] for row in options).values()), "each MCQ must have four audited options", errors)
    require(
        sum(row["is_gold"] == "False" and row["distractor_quality"] == "invalid_distractor_because_defensible" for row in options) == 56,
        "defensible non-Gold option count must be 56",
        errors,
    )
    require(
        {row["item_id"] for row in validity if row["audit_priority"] == "P0"}
        == {"SGS-FM-034", "SGS-007-R03", "SGS-097-R03", "SGS-HARD-016", "SGS-HARD-028"},
        "frozen P0 item set differs",
        errors,
    )
    refs = read_csv(REVIEW / "03_reference_evidence/fr_112_reference_claim_evidence_audit.csv")
    require(len(refs) == 112 and unique(refs, ["item_id", "claim_id"]), "Reference claims must be 112 unique rows", errors)
    require(len({row["item_id"] for row in refs}) == 30, "Reference claims must cover 30 items", errors)
    reference_items = read_csv(REVIEW / "03_reference_evidence/fr_30_reference_answer_external_evidence_audit.csv")
    require(len(reference_items) == 30 and unique(reference_items, ["item_id"]), "Reference Answer audit must be 30 unique items", errors)
    source_ledger = read_csv(REVIEW / "03_reference_evidence/external_evidence_source_ledger.csv")
    require(any(row["source_id"].startswith("PROJ-") for row in source_ledger) and any(row["source_id"].startswith("EXT-") for row in source_ledger), "project and external evidence sources are not explicitly separated", errors)
    robustness_pairs = read_csv(REVIEW / "06_robustness/robustness_40_item_pair_review.csv")
    robustness_groups = read_csv(REVIEW / "06_robustness/robustness_group_review.csv")
    require(len(robustness_pairs) == 40 and unique(robustness_pairs, ["item_id"]), "Robustness pair review must be 40 unique items", errors)
    require(len(robustness_groups) == 12 and unique(robustness_groups, ["base_or_parent_id"]), "Robustness group review must be 12 unique groups", errors)
    hard50 = read_csv(REVIEW / "07_hard50/hard50_item_calibration.csv")
    require(len(hard50) == 50 and unique(hard50, ["item_id"]), "Hard50 calibration must be 50 unique items", errors)
    items = read_csv(REVIEW / "04_free_response_adjudication/full_review_by_item.csv")
    dims = read_csv(REVIEW / "04_free_response_adjudication/full_review_by_dimension.csv")
    require(len(items) == 120 and unique(items, ["task_id", "model_id"]), "free-response item review must be 120 unique rows", errors)
    require(len(dims) == 960 and unique(dims, ["task_id", "model_id", "dimension"]), "dimension review must be 960 unique rows", errors)
    by_item: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in dims:
        by_item[(row["task_id"], row["model_id"])].append(row)
        score = float(row["score"])
        require(0 <= score <= 1.25 and abs(score * 20 - round(score * 20)) < 1e-8, f"invalid dimension step at {row['task_id']} {row['model_id']}", errors)
    for row in items:
        key = (row["task_id"], row["model_id"])
        require({entry["dimension"] for entry in by_item[key]} == DIMENSIONS, f"dimension set differs at {key}", errors)
        total = round(sum(float(entry["score"]) for entry in by_item[key]), 2)
        require(abs(total - float(row["reviewed_dimension_total"])) < 1e-8, f"dimension sum differs at {key}", errors)
        expected = 0.0 if row["no_answer"].lower() == "true" or row["hard_fail_status"] == "confirmed_hard_fail" else total
        require(abs(expected - float(row["official_item_score"])) < 1e-8, f"official formula differs at {key}", errors)
    statuses = Counter(row["hard_fail_status"] for row in items)
    require(statuses["confirmed_hard_fail"] == 3, "confirmed Hard Fail count must be 3", errors)
    require(statuses["downgraded_to_dimension_issue"] == 12, "downgraded Hard Fail count must be 12", errors)
    require(sum(row["no_answer"].lower() == "true" for row in items) == 1, "no-answer count must be 1", errors)
    confirmed = {(row["task_id"], row["model_id"], row["hard_fail_category"]) for row in items if row["hard_fail_status"] == "confirmed_hard_fail"}
    require(confirmed == {("SGS-082", "mimo-v2.5-pro", "data_integrity"), ("SGS-FM-FR-007", "mimo-v2.5-pro", "safety"), ("SGS-FM-FR-011", "mimo-v2.5-pro", "data_integrity")}, "confirmed Hard Fail identities differ", errors)
    missing = [row for row in items if row["no_answer"].lower() == "true"]
    require(len(missing) == 1 and missing[0]["task_id"] == "SGS-081" and missing[0]["model_id"] == "deepseek-v4-pro" and float(missing[0]["official_item_score"]) == 0, "DeepSeek SGS-081 no-rescue record differs", errors)


def audit_frozen_content(errors: list[str]) -> None:
    for relative, expected in FROZEN_HASHES.items():
        require(sha256(ROOT / relative) == expected, f"frozen hash differs: {relative}", errors)
    benchmark = json.loads((ROOT / "data/benchmark.json").read_text(encoding="utf-8"))
    mcq = {row["id"]: row for row in benchmark if row["question_type"] == "multiple_choice"}
    options = read_csv(REVIEW / "02_mcq_options/mcq_488_option_audit.csv")
    for row in options:
        item = mcq[row["item_id"]]
        require(row["option_text"] == item["options"][row["option_letter"]], f"frozen option text differs: {row['item_id']} {row['option_letter']}", errors)
        require(row["gold_letter"] == item["answer"], f"frozen Gold differs: {row['item_id']}", errors)
    for name, expected in SOURCE_ARCHIVES.items():
        path = INTERNAL / "source_packages" / name
        require(path.exists() and sha256(path) == expected, f"source review archive differs: {name}", errors)


def public_paths() -> list[Path]:
    roots = [ROOT / "README.md", ROOT / "CHANGELOG.md", ROOT / "RELEASE_NOTES.md", ROOT / "docs", ROOT / "reports", ROOT / "results", ROOT / "eval", REVIEW]
    paths: list[Path] = []
    for root in roots:
        if root.is_file():
            paths.append(root)
        elif root.exists():
            paths.extend(path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".csv", ".json", ".xlsx"})
    return paths


def text_from_xlsx(path: Path) -> str:
    with zipfile.ZipFile(path) as handle:
        chunks = []
        for name in handle.namelist():
            if name.endswith(".xml"):
                chunks.append(handle.read(name).decode("utf-8", errors="ignore"))
        return "\n".join(chunks)


def audit_identity(errors: list[str]) -> None:
    for path in public_paths():
        content = text_from_xlsx(path) if path.suffix.lower() == ".xlsx" else path.read_text(encoding="utf-8-sig", errors="ignore")
        match = FORBIDDEN_PUBLIC.search(content)
        require(match is None, f"public identity wording in {path.relative_to(ROOT)}: {match.group(0) if match else ''}", errors)
        if path.suffix.lower() == ".csv":
            rows = read_csv(path)
            for row in rows:
                for field, value in row.items():
                    if field.lower() in {"review_identity", "reviewer_identity", "reviewer"}:
                        require(value in ALLOWED_ROLES, f"unapproved public reviewer role {value!r} in {path.relative_to(ROOT)}", errors)
    registry = (INTERNAL / "reviewer_role_registry.md").read_text(encoding="utf-8")
    require("专家 Y" not in registry and "Expert Y" not in registry, "unused Expert Y description remains in internal role registry", errors)


def audit_public_documents(errors: list[str]) -> None:
    required = {
        "README.md": ["152", "122", "30", "40", "50", "242/242", "488/488", "112/112", "120/120", "960/960"],
        "docs/dataset_card.md": ["152", "122", "30", "40", "50", "242", "488", "112", "120", "960", "56", "5 个 P0", "2 个 Robustness P0", "未采用独立盲审"],
        "docs/scoring_protocol.md": ["122", "488", "56", "30", "120", "960", "3 条", "12 条", "SGS-081"],
        "docs/risk_gates.md": ["15 个历史", "3 个确认为", "12 个降级"],
        "docs/reproducibility.md": ["46", "122×4", "30×4", "40×4", "50×4", "120 条", "差异 0"],
        "reports/evaluation_report.md": ["122", "120", "960", "3 个 confirmed", "12 个", "56", "46", "差异为 0"],
        "reports/model_error_analysis.md": ["56", "three MiMo", "SGS-081", "8.213", "7.545", "6.732", "4.952"],
        "review/v0.6.0/05_judge_reliability/judge_reliability_report.md": ["120", "15", "confirmed：3", "false positive：12"],
        "reports/final_release_audit.md": ["242/242", "488/488", "30/30", "112/112", "120/120", "960/960", "3 confirmed", "12 downgraded", "1 no-answer", "40/40", "50/50", "46 members", "0 field differences"],
        "RELEASE_NOTES.md": ["242", "488", "112", "120", "960", "3 个 confirmed", "12 个", "122", "5 个冻结 P0", "56", "46", "差异为 0"],
        "CHANGELOG.md": ["242", "488", "112", "120", "960", "3 confirmed", "12 downgraded"],
    }
    for relative, tokens in required.items():
        content = (ROOT / relative).read_text(encoding="utf-8-sig")
        for token in tokens:
            require(token in content, f"canonical document {relative} is missing consistency token {token!r}", errors)
    limitations = (REVIEW / "00_scope/known_limitations.md").read_text(encoding="utf-8")
    for token in ["SGS-FM-034", "SGS-007-R03", "SGS-097-R03", "SGS-HARD-016", "SGS-HARD-028", "Fifty-six", "two P0 variants", "Hard50 is saturated", "did not use an independent blind-review design"]:
        require(token in limitations, f"Known Limitations is missing {token!r}", errors)
    metrics = json.loads((INTERNAL / "final_consistency_metrics.json").read_text(encoding="utf-8"))
    require(metrics.get("validation_status") == "passed", "final consistency metrics are not marked validated", errors)
    require(metrics.get("repository_missing_mapped_files") == 0 and metrics.get("unresolved_content_conflicts") == 0, "final consistency metrics contain a release blocker", errors)
    require(metrics.get("duplicate_release_directories") == [], "duplicate v0.6.0 release directory detected", errors)


def audit_judge_and_manifest(errors: list[str]) -> None:
    judge = json.loads((ROOT / "results/standard_20260703/free_response_judge/judge_manifest.json").read_text(encoding="utf-8"))
    require(judge["judge_model"] == "gpt-5.6-sol", "Judge model must be gpt-5.6-sol", errors)
    outputs = []
    for stage in ["sgs152_mcq", "sgs152_free_response", "robustness", "hard50"]:
        outputs.extend(read_csv(ROOT / f"results/standard_20260703/{stage}/model_outputs.csv"))
    require(all(row["model_id"] != "gpt-5.6-sol" for row in outputs), "Judge appears in participating-model outputs", errors)
    verification = json.loads((REVIEW / "10_provenance/raw_archive_verification_manifest.json").read_text(encoding="utf-8"))
    require(verification["zip_member_count"] == 46 and verification["raw_to_derived_diff_count"] == 0, "raw rebuild verification is incomplete", errors)
    require(verification["judge_review_count"] == 120 and verification["judge_primary_keys_unique"], "Judge raw rebuild count/keys differ", errors)
    require(verification.get("git_status_before") == [] and verification.get("git_status_after") == [], "raw rebuild was not recorded from a clean worktree", errors)
    manifest_path = REVIEW / "manifest.json"
    require(manifest_path.exists(), "v0.6.0 manifest is missing", errors)
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        require(manifest["release"] == "v0.6.0" and manifest["judge_model"] == "GPT-5.6-sol", "public manifest release/Judge differs", errors)
        for entry in manifest["files"]:
            path = REVIEW / entry["path"]
            require(path.exists() and sha256(path) == entry["sha256"], f"manifest hash differs: {entry['path']}", errors)


def main() -> None:
    errors: list[str] = []
    require((ROOT / "VERSION").read_text().strip() == "0.6.0", "VERSION must be 0.6.0", errors)
    audit_counts(errors)
    audit_frozen_content(errors)
    audit_identity(errors)
    audit_public_documents(errors)
    audit_judge_and_manifest(errors)
    if errors:
        print("v0.6.0 audit failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)
    print("v0.6.0 audit passed: frozen content, counts, scoring, provenance, roles and Judge boundary verified.")


if __name__ == "__main__":
    main()
