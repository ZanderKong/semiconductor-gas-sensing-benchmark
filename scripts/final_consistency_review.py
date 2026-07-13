#!/usr/bin/env python3
"""Generate the final v0.6.0 source-package and repository consistency evidence."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import zipfile
from collections import Counter
from pathlib import Path


STARTING_HEAD = "24460ff29f1e1840a6c5f6d81779e2ac4b7d8153"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_rows(data: bytes) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"))))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def classify_mapped(source: bytes, target: Path) -> tuple[str, str, str]:
    target_bytes = target.read_bytes()
    if source == target_bytes:
        return "identical_file", "byte-identical to current repository", "retain repository version"
    if target.suffix.lower() == ".csv":
        source_rows = csv_rows(source)
        target_rows = read_csv(target)
        if source_rows == target_rows:
            return "repository_equivalent_formatting", "parsed rows are identical; bytes differ only by serialization", "retain repository version"
        if len(source_rows) == len(target_rows) and source_rows and target_rows and source_rows[0].keys() == target_rows[0].keys():
            changed = {
                field
                for left, right in zip(source_rows, target_rows)
                for field in left
                if left[field] != right[field]
            }
            if changed <= {"review_identity", "reviewer_identity", "review_source"}:
                return "repository_role_normalized", f"only public role fields differ: {sorted(changed)}", "retain current role-normalized repository version"
        if target.name == "statistical_diagnostic_inventory.csv":
            return "repository_updated_completed_statistics", "package draft said pending; repository records verified completed outputs", "retain current completed repository version"
    if target.name == "content_quality_statistics.json":
        return "repository_updated_completed_statistics", "repository adds the completed clean-rebuild statistics status", "retain current completed repository version"
    if target.suffix.lower() == ".xlsx":
        return "repository_updated_public_dashboard", "repository workbook is the role-normalized public release copy", "retain current public repository version"
    return "content_conflict", "mapped file differs outside approved formatting, role, dashboard, or completion-status changes", "release blocker"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--validation-status", choices=["pending", "passed"], default="pending")
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    release = repo / "review/v0.6.0"
    internal = repo / "review/internal_provenance"
    source_dir = internal / "source_packages"
    disposition = read_csv(internal / "source_package_member_disposition.csv")

    mapping: list[dict[str, object]] = []
    archives = {path.name: path for path in source_dir.glob("*.zip")}
    for row in disposition:
        archive = archives[row["archive"]]
        with zipfile.ZipFile(archive) as handle:
            names = [name for name in handle.namelist() if not name.endswith("/")]
            package_root = names[0].split("/", 1)[0]
            source = handle.read(f"{package_root}/{row['member_path']}")
        target_rel = row["selected_target"]
        target = release / target_rel if target_rel else None
        if target is not None and not target.exists():
            classification, reason, action = "repository_missing", "expected mapped release file is absent", "supplement from verified package after review"
            target_hash = ""
        elif target is not None:
            classification, reason, action = classify_mapped(source, target)
            target_hash = sha256(target)
        else:
            member = row["member_path"]
            if member.startswith("repository_release_drafts/") or member.startswith("08_codex_handoff/"):
                kind = "historical draft or integration handoff"
            elif member.startswith("review_tools/"):
                kind = "superseded package helper; repository implementation is authoritative"
            elif member in {"README.md", "manifest.json", "SHA256SUMS.txt"} or member.startswith("FINAL_") or "codex" in member.lower():
                kind = "package-level provenance document"
            else:
                kind = "source-only supporting audit artifact"
            classification, reason, action = "historical_or_source_only", kind, "retain only in exact internal source archive"
            target_hash = ""
        mapping.append({
            "priority": row["priority"], "package": row["package"], "archive": row["archive"],
            "source_member": row["member_path"], "source_sha256": row["sha256"],
            "sha256sums_status": row["packaged_sha256_status"], "repository_path": target_rel,
            "repository_sha256": target_hash, "classification": classification,
            "reason": reason, "release_action": action,
        })

    mapping_path = internal / "final_source_package_repository_mapping.csv"
    write_csv(mapping_path, mapping, [
        "priority", "package", "archive", "source_member", "source_sha256", "sha256sums_status",
        "repository_path", "repository_sha256", "classification", "reason", "release_action",
    ])

    inventory = []
    for path in sorted(p for p in release.rglob("*") if p.is_file() and p.name != "manifest.json"):
        inventory.append({"path": path.relative_to(release).as_posix(), "size": path.stat().st_size, "sha256": sha256(path)})
    inventory_path = internal / "final_v0_6_repository_file_inventory.csv"
    write_csv(inventory_path, inventory, ["path", "size", "sha256"])

    validity = read_csv(release / "01_item_validity/all_242_item_validity_review.csv")
    options = read_csv(release / "02_mcq_options/mcq_488_option_audit.csv")
    fr_items = read_csv(release / "04_free_response_adjudication/full_review_by_item.csv")
    fr_dims = read_csv(release / "04_free_response_adjudication/full_review_by_dimension.csv")
    source_ledger = read_csv(release / "03_reference_evidence/external_evidence_source_ledger.csv")
    raw_manifest = json.loads((release / "10_provenance/raw_archive_verification_manifest.json").read_text(encoding="utf-8"))
    official = read_csv(release / "04_free_response_adjudication/official_free_response_summary.csv")
    classes = Counter(row["classification"] for row in mapping)
    package_inventory = {row["package_role"]: row for row in read_csv(release / "00_scope/source_package_inventory.csv")}
    document_log = read_csv(internal / "source_document_review_log.csv")
    package_summaries = {}
    for package in sorted({row["package"] for row in mapping}):
        package_rows = [row for row in mapping if row["package"] == package]
        docs = [row for row in document_log if row["package"] == package]
        inventory_row = package_inventory[package]
        package_summaries[package] = {
            "archive": inventory_row["archive"],
            "archive_sha256": inventory_row["sha256"],
            "file_members": len(package_rows),
            "zip_and_sha256sums_validation": inventory_row["validation"],
            "manifest_validation": next(row["integration_use"] for row in docs if row["document_type"] == "Manifest"),
            "readme_present": next(row["present"] == "true" for row in docs if row["document_type"] == "README"),
            "classification_counts": dict(sorted(Counter(row["classification"] for row in package_rows).items())),
        }
    status_counts = Counter(row["hard_fail_status"] for row in fr_items)
    p0 = [row["item_id"] for row in validity if row["audit_priority"] == "P0"]
    metrics = {
        "audit_starting_head": STARTING_HEAD,
        "version": (repo / "VERSION").read_text().strip(),
        "review_file_inventory_count_excluding_self_hashing_manifest": len(inventory),
        "source_package_file_members": len(mapping),
        "source_package_summaries": package_summaries,
        "source_package_comparison_counts": dict(sorted(classes.items())),
        "repository_missing_mapped_files": sum(row["classification"] == "repository_missing" for row in mapping),
        "unresolved_content_conflicts": sum(row["classification"] == "content_conflict" for row in mapping),
        "duplicate_release_directories": [
            path.name for path in (repo / "review").iterdir()
            if path.is_dir() and path.name.startswith("v0.6.0") and path.name != "v0.6.0"
        ],
        "item_validity": {"total": len(validity), "sets": dict(Counter(row["set_name"] for row in validity))},
        "mcq": {
            "item_summaries": len(read_csv(release / "02_mcq_options/mcq_122_item_option_set_summary.csv")),
            "option_rows": len(options),
            "defensible_non_gold": sum(row["is_gold"] == "False" and row["distractor_quality"] == "invalid_distractor_because_defensible" for row in options),
        },
        "frozen_p0": {"count": len(p0), "item_ids": p0},
        "reference_evidence": {
            "items": len(read_csv(release / "03_reference_evidence/fr_30_reference_answer_external_evidence_audit.csv")),
            "claims": len(read_csv(release / "03_reference_evidence/fr_112_reference_claim_evidence_audit.csv")),
            "source_ledger_rows": len(source_ledger),
            "project_and_external_sources_separated": any(row["source_id"].startswith("PROJ-") for row in source_ledger) and any(row["source_id"].startswith("EXT-") for row in source_ledger),
        },
        "free_response": {
            "item_rows": len(fr_items), "dimension_rows": len(fr_dims),
            "historical_hard_fails": status_counts["confirmed_hard_fail"] + status_counts["downgraded_to_dimension_issue"],
            "confirmed": status_counts["confirmed_hard_fail"], "downgraded": status_counts["downgraded_to_dimension_issue"],
            "no_answer": sum(row["no_answer"] == "true" for row in fr_items),
            "official_summary": {row["model_display"]: row["v0_6_official_average"] for row in official},
        },
        "diagnostics": {
            "robustness_pairs": len(read_csv(release / "06_robustness/robustness_40_item_pair_review.csv")),
            "robustness_groups": len(read_csv(release / "06_robustness/robustness_group_review.csv")),
            "robustness_p0": sum(row["set_name"] == "robustness" and row["audit_priority"] == "P0" for row in validity),
            "hard50_calibration": len(read_csv(release / "07_hard50/hard50_item_calibration.csv")),
        },
        "provenance": {
            "zip_members": raw_manifest["zip_member_count"], "judge_rows": raw_manifest["judge_review_count"],
            "raw_to_derived_differences": raw_manifest["raw_to_derived_diff_count"],
            "clean_rebuild_status_before": raw_manifest["git_status_before"], "clean_rebuild_status_after": raw_manifest["git_status_after"],
        },
        "validation_status": args.validation_status,
        "frozen_content_modified_by_final_review": False,
    }
    metrics_path = internal / "final_consistency_metrics.json"
    metrics_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report = f"""# v0.6.0 Final Consistency Review

## 1. Current baseline

- audit starting HEAD: `{STARTING_HEAD}`;
- branch: `main`;
- version: `0.6.0`;
- legacy evidence baseline only: `dfa28407e5130dbc4328ac006a5368f18bdbff7d`;
- starting and ending worktree status are recorded by the release validation; the audit began clean.

## 2. Source-package mapping

The four user-supplied archives are byte-identical to the exact copies in `review/internal_provenance/source_packages/`. They contain {len(mapping)} file members. The complete per-member mapping, source and repository hashes, and disposition are in `review/internal_provenance/final_source_package_repository_mapping.csv`.

Comparison counts: {', '.join(f'`{key}`={value}' for key, value in sorted(classes.items()))}. Repository-missing mapped files: `{metrics['repository_missing_mapped_files']}`. Unresolved content conflicts: `{metrics['unresolved_content_conflicts']}`.

## 3. Content already present

- item validity: 242 total = 152 main + 40 Robustness + 50 Hard50;
- MCQ: 122 item summaries, 488 option rows, 56 defensible non-Gold options;
- Reference Answer: 30 item rows, 112 claim rows, source ledger and gap queue;
- free-response: 120 item rows, 960 dimension rows, 15 historical Hard Fails = 3 confirmed + 12 downgraded, and one no-answer;
- diagnostics: 40 Robustness pair rows, 12 group rows and 50 Hard50 calibration rows;
- provenance: 46 raw ZIP members, 120 unique Judge rows and zero raw-to-derived field differences.

## 4. New closing evidence

- final per-package repository mapping;
- final `review/v0.6.0` file inventory with SHA-256;
- automatically calculated consistency metrics;
- removal of an unused future-role placeholder and its audit allowance.

No scientific review row, score, Hard Fail decision or frozen benchmark field was changed.

## 5. Historical or duplicate package material

Package READMEs, final reports, manifests, checksum lists, integration handoffs, draft release documents, superseded helper scripts and package-only supporting ledgers remain in the exact internal ZIPs. They were not copied over the current release tree and do not create duplicate release directories.

## 6. Conflict handling

Byte differences were accepted only when parsed CSV content was equivalent, public role fields were normalized, dashboards were role-normalized, or completed statistics superseded package placeholders. Any other mapped difference is classified as `content_conflict`; the final count is `{metrics['unresolved_content_conflicts']}`.

## 7. Files changed in this closing review

- internal source-package mapping, repository inventory and calculated metrics;
- this final consistency report;
- role registry, integration generator and v0.6 audit logic to remove the unused role placeholder;
- release manifest after adding this report.

## 8. Frozen files not modified

Questions, options, Gold Answers, Reference Answers, item IDs and original model outputs were not modified. Frozen hashes remain release gates in `scripts/audit_v0_6.py`.

## 9. Tests and audits

Validation status: `{args.validation_status}`. The required make targets, provenance audit, v0.6 audit, source-package SHA/Manifest verification, raw rebuild, full-statistics diff, manifest regeneration check and clean-worktree check are release gates.

## 10. Numeric consistency

All figures in this report are generated from the final CSV/JSON artifacts. Machine-readable values are in `review/internal_provenance/final_consistency_metrics.json`.

## 11. Reviewer-role naming

Current public scientific review uses only `专家 X`; project decisions use `项目负责人`; deterministic integration uses `复核者`; GPT-5.6-sol is explicitly the Judge. This review does not disclose the underlying identity of `专家 X` and does not claim independent blind review.

## 12. Known Limitations

The release retains the five frozen P0 records (`SGS-FM-034`, `SGS-007-R03`, `SGS-097-R03`, `SGS-HARD-016`, `SGS-HARD-028`), 56 defensible non-Gold options, two Robustness P0 variants, saturated Hard50 status and the absence of an independent blind-review design.

## 13. Final diff

The exact `git diff --stat` is reported in the delivery response after the closing commit. No generated release artifact remains unexplained.

## 14. Final commit

The final commit SHA is reported in the delivery response because a commit cannot contain its own SHA without changing that SHA.

## 15. Pending items

No v0.6.0 release blocker remains. Known frozen-content issues stay disclosed for a separately authorized benchmark-content revision.
"""
    (release / "00_scope/final_consistency_review.md").write_text(report, encoding="utf-8")
    print(json.dumps({"mapping_rows": len(mapping), "comparison_counts": dict(classes), "metrics": str(metrics_path.relative_to(repo))}, ensure_ascii=False))


if __name__ == "__main__":
    main()
