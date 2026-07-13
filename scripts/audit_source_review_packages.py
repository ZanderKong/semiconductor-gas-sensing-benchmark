#!/usr/bin/env python3
"""Verify and inventory every member of the four v0.6 source review packages."""

from __future__ import annotations

import csv
import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "review/internal_provenance/source_packages"
OUT_DIR = ROOT / "review/internal_provenance"
PUBLIC_SCOPE = ROOT / "review/v0.6.0/00_scope"
PACKAGES = [
    (1, "remaining_work", "2-sgs_benchmark_remaining_work_completion_v0.6.zip"),
    (2, "option_evidence", "3-sgs152_option_and_reference_evidence_audit_v0.6.zip"),
    (3, "item_validity", "1-sgs242_item_validity_review_v0.6.zip"),
    (4, "free_response", "4-sgs152_v0.6_review_package.zip"),
]
SELECTED = {
    "remaining_work": {
        "robustness_40_item_pair_review.csv": "06_robustness/robustness_40_item_pair_review.csv",
        "robustness_group_review.csv": "06_robustness/robustness_group_review.csv",
        "hard50_item_calibration.csv": "07_hard50/hard50_item_calibration.csv",
        "hard50_retire_rewrite_keep.csv": "07_hard50/hard50_retire_rewrite_keep.csv",
        "content_quality_statistics.json": "08_statistics/content_quality_statistics.json",
        "statistical_diagnostic_inventory.csv": "08_statistics/statistical_diagnostic_inventory.csv",
        "blind_review_execution_packet/blind_review_rules.md": "09_blind_review/blind_review_execution_packet/blind_review_rules.md",
        "blind_review_execution_packet/blind_review_scoring_template.csv": "09_blind_review/blind_review_execution_packet/blind_review_scoring_template.csv",
        "blind_review_execution_packet/build_blind_packet.py": "09_blind_review/blind_review_execution_packet/build_blind_packet.py",
        "remaining_work_dashboard.xlsx": "dashboards/remaining_work_dashboard.xlsx",
    },
    "option_evidence": {
        "mcq_122_item_option_set_summary.csv": "02_mcq_options/mcq_122_item_option_set_summary.csv",
        "mcq_488_option_audit.csv": "02_mcq_options/mcq_488_option_audit.csv",
        "mcq_defensible_distractor_and_gold_issue_queue.csv": "02_mcq_options/mcq_defensible_distractor_and_gold_issue_queue.csv",
        "fr_30_reference_answer_external_evidence_audit.csv": "03_reference_evidence/fr_30_reference_answer_external_evidence_audit.csv",
        "fr_112_reference_claim_evidence_audit.csv": "03_reference_evidence/fr_112_reference_claim_evidence_audit.csv",
        "external_evidence_source_ledger.csv": "03_reference_evidence/external_evidence_source_ledger.csv",
        "fr_reference_evidence_gap_queue.csv": "03_reference_evidence/fr_reference_evidence_gap_queue.csv",
        "option_and_reference_evidence_dashboard.xlsx": "dashboards/option_reference_evidence_dashboard.xlsx",
    },
    "item_validity": {
        "all_242_item_validity_review.csv": "01_item_validity/all_242_item_validity_review.csv",
        "main_152_item_validity_review.csv": "01_item_validity/main_152_item_validity_review.csv",
        "robustness_40_item_validity_review.csv": "01_item_validity/robustness_40_item_validity_review.csv",
        "hard50_50_item_validity_review.csv": "01_item_validity/hard50_50_item_validity_review.csv",
        "item_validity_issue_queue.csv": "01_item_validity/item_validity_issue_queue.csv",
        "item_validity_dashboard.xlsx": "dashboards/item_validity_dashboard.xlsx",
    },
    "free_response": {
        "02_full_response_adjudication/full_review_by_item.csv": "04_free_response_adjudication/full_review_by_item.csv",
        "02_full_response_adjudication/full_review_by_dimension.csv": "04_free_response_adjudication/full_review_by_dimension.csv",
        "02_full_response_adjudication/confirmed_hard_fails.csv": "04_free_response_adjudication/confirmed_hard_fails.csv",
        "02_full_response_adjudication/score_overrides.csv": "04_free_response_adjudication/score_overrides.csv",
        "01_free_response_design_review/hard_fail_reclassification.csv": "04_free_response_adjudication/hard_fail_reclassification.csv",
        "03_judge_reliability/judge_reliability_metrics.csv": "05_judge_reliability/judge_reliability_metrics.csv",
        "03_judge_reliability/judge_disagreement_cases.csv": "05_judge_reliability/judge_disagreement_cases.csv",
        "03_judge_reliability/judge_reliability_report.md": "05_judge_reliability/judge_reliability_report.md",
        "02_full_response_adjudication/official_free_response_summary.csv": "04_free_response_adjudication/official_free_response_summary.csv",
        "review_dashboard.xlsx": "dashboards/free_response_review_dashboard.xlsx",
    },
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def packaged_hashes(zf: zipfile.ZipFile, root: str) -> dict[str, str]:
    name = f"{root}/SHA256SUMS.txt"
    if name not in zf.namelist():
        raise RuntimeError(f"missing {name}")
    result = {}
    for line in zf.read(name).decode("utf-8-sig").splitlines():
        if line.strip():
            expected, relative = line.split(maxsplit=1)
            result[relative.lstrip("* ")] = expected
    return result


def main() -> None:
    members: list[dict[str, object]] = []
    documents: list[dict[str, object]] = []
    for priority, label, archive_name in PACKAGES:
        archive = SOURCE_DIR / archive_name
        with zipfile.ZipFile(archive) as zf:
            bad = zf.testzip()
            if bad:
                raise SystemExit(f"ZIP integrity failed: {archive_name}: {bad}")
            names = [name for name in zf.namelist() if not name.endswith("/")]
            roots = {name.split("/", 1)[0] for name in names}
            if len(roots) != 1:
                raise SystemExit(f"unexpected roots in {archive_name}: {sorted(roots)}")
            root = next(iter(roots))
            sums = packaged_hashes(zf, root)
            relatives = [name[len(root) + 1 :] for name in names]
            manifest_entries = 0
            manifest_name = f"{root}/manifest.json"
            if manifest_name in names:
                manifest = json.loads(zf.read(manifest_name).decode("utf-8-sig"))
                files = manifest.get("files", {})
                if not isinstance(files, dict):
                    raise SystemExit(f"unexpected manifest files shape: {archive_name}")
                manifest_entries = len(files)
                for relative, expected in files.items():
                    member_name = f"{root}/{relative}"
                    if member_name not in names or digest(zf.read(member_name)) != expected:
                        raise SystemExit(f"manifest hash mismatch: {archive_name}: {relative}")
            for name, relative in zip(names, relatives):
                actual = digest(zf.read(name))
                hash_state = "not_listed_self_manifest"
                if relative in sums:
                    if sums[relative] != actual:
                        raise SystemExit(f"packaged SHA mismatch: {archive_name}: {relative}")
                    hash_state = "verified"
                target = SELECTED.get(label, {}).get(relative, "")
                required_doc = relative in {"README.md", "manifest.json", "SHA256SUMS.txt"} or relative.startswith("FINAL_") or "codex" in relative.lower() or relative.startswith("08_codex_handoff/")
                members.append({
                    "priority": priority, "package": label, "archive": archive_name,
                    "member_path": relative, "sha256": actual, "packaged_sha256_status": hash_state,
                    "category": "required_document" if required_doc else "release_input",
                    "disposition": "selected_and_integrated" if target else "reviewed_and_preserved_in_exact_source_archive",
                    "selected_target": target, "conflict_basis": "owner priority plus artifact purpose",
                    "preserved_location": f"review/internal_provenance/source_packages/{archive_name}",
                    "score_impact": "possible" if label == "free_response" and "adjudication" in relative else "none",
                })

            categories = {
                "README": ["README.md"],
                "Manifest": ["manifest.json"],
                "SHA256SUMS": ["SHA256SUMS.txt"],
                "final_report": [p for p in relatives if p.startswith("FINAL_")],
                "Codex_integration": [p for p in relatives if "codex" in p.lower()],
            }
            if label == "free_response":
                categories["Codex_integration"] = [p for p in relatives if p.startswith("08_codex_handoff/")]
            for doc_type, candidates in categories.items():
                existing = [p for p in candidates if p in relatives]
                if not existing:
                    documents.append({
                        "priority": priority, "package": label, "document_type": doc_type, "member_path": "",
                        "present": "false", "sha256": "", "review_status": "not present in source package",
                        "integration_use": "absence recorded; no replacement identity or content inferred",
                    })
                for relative in existing:
                    documents.append({
                        "priority": priority, "package": label, "document_type": doc_type, "member_path": relative,
                        "present": "true", "sha256": digest(zf.read(f"{root}/{relative}")),
                        "review_status": "read and incorporated into conflict/selection review",
                        "integration_use": f"verified {manifest_entries} member hashes" if doc_type == "Manifest" else "release integration evidence",
                    })

    write_csv(OUT_DIR / "source_package_member_disposition.csv", members, [
        "priority", "package", "archive", "member_path", "sha256", "packaged_sha256_status", "category",
        "disposition", "selected_target", "conflict_basis", "preserved_location", "score_impact",
    ])
    write_csv(OUT_DIR / "source_document_review_log.csv", documents, [
        "priority", "package", "document_type", "member_path", "present", "sha256", "review_status", "integration_use",
    ])
    existing_path = PUBLIC_SCOPE / "integration_decision_log.csv"
    existing: dict[tuple[str, str], dict[str, str]] = {}
    if existing_path.exists():
        with existing_path.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                existing[(row["selected_package"], row["source_file"])] = row
    integration_rows = []
    for row in members:
        if not row["selected_target"]:
            continue
        previous = existing.get((str(row["package"]), str(row["member_path"])), {})
        default_key = "archive+member_path"
        if str(row["selected_target"]).endswith("official_free_response_summary.csv"):
            default_key = "model_id"
        elif str(row["selected_target"]).endswith(".xlsx"):
            default_key = "workbook"
        elif str(row["selected_target"]).endswith("robustness_group_review.csv"):
            default_key = "base_or_parent_id"
        elif str(row["selected_target"]).endswith("score_overrides.csv"):
            default_key = "task_id+model_id"
        decision = "selected by owner priority and artifact purpose"
        score_impact = previous.get("score_impact", row["score_impact"])
        if str(row["selected_target"]).endswith("official_free_response_summary.csv"):
            decision = "source schema retained; values recomputed from reviewed item rows under the official formula"
            score_impact = "yes"
        elif str(row["selected_target"]).startswith("08_statistics/"):
            decision = "higher-priority skeleton retained; completion status updated from the verified clean statistics run"
        elif str(row["selected_target"]).endswith(".xlsx"):
            decision = "scope workbook retained as a role-sanitized public copy"
        integration_rows.append({
            "target": row["selected_target"],
            "selected_package": row["package"],
            "source_file": row["member_path"],
            "primary_key": default_key if default_key != "archive+member_path" else previous.get("primary_key", default_key),
            "decision": decision,
            "score_impact": score_impact,
        })
    integration_rows.append({
        "target": "10_provenance/raw_evidence_inventory.csv",
        "selected_package": "raw_archive_and_repository",
        "source_file": "artifacts/SGS152_raw_evidence_20260713.zip + repository parsers",
        "primary_key": "member",
        "decision": "rebuilt from the verified raw archive; package placeholder retained only in the exact source ZIP",
        "score_impact": "release gate",
    })
    write_csv(existing_path, integration_rows, [
        "target", "selected_package", "source_file", "primary_key", "decision", "score_impact",
    ])
    print(f"Verified {len(PACKAGES)} packages and recorded {len(members)} file members.")


if __name__ == "__main__":
    main()
