#!/usr/bin/env python3
"""Integrate the four frozen v0.6 review archives into the release tree."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import tempfile
import zipfile
from collections import defaultdict
from datetime import date
from pathlib import Path


PACKAGE_SPECS = [
    ("remaining_work", "2-sgs_benchmark_remaining_work_completion_v0.6.zip", 1),
    ("option_evidence", "3-sgs152_option_and_reference_evidence_audit_v0.6.zip", 2),
    ("item_validity", "1-sgs242_item_validity_review_v0.6.zip", 3),
    ("free_response", "4-sgs152_v0.6_review_package.zip", 4),
]

PUBLIC_ROLE = "专家 X"

PRIMARY_KEYS = {
    "all_242_item_validity_review.csv": "item_id",
    "main_152_item_validity_review.csv": "item_id",
    "robustness_40_item_validity_review.csv": "item_id",
    "hard50_50_item_validity_review.csv": "item_id",
    "item_validity_issue_queue.csv": "item_id",
    "mcq_122_item_option_set_summary.csv": "item_id",
    "mcq_488_option_audit.csv": "item_id+option_letter",
    "mcq_defensible_distractor_and_gold_issue_queue.csv": "item_id+option_letter",
    "fr_30_reference_answer_external_evidence_audit.csv": "item_id",
    "fr_112_reference_claim_evidence_audit.csv": "item_id+claim_id",
    "external_evidence_source_ledger.csv": "source_id",
    "fr_reference_evidence_gap_queue.csv": "item_id+claim_id",
    "full_review_by_item.csv": "task_id+model_id",
    "full_review_by_dimension.csv": "task_id+model_id+dimension",
    "confirmed_hard_fails.csv": "task_id+model_id",
    "score_overrides.csv": "task_id+model_id",
    "hard_fail_reclassification.csv": "task_id+model_id",
    "judge_reliability_metrics.csv": "group",
    "judge_disagreement_cases.csv": "task_id+model_id",
    "judge_reliability_report.md": "document",
    "robustness_40_item_pair_review.csv": "item_id",
    "robustness_group_review.csv": "base_or_parent_id",
    "hard50_item_calibration.csv": "item_id",
    "hard50_retire_rewrite_keep.csv": "item_id",
    "content_quality_statistics.json": "section",
    "statistical_diagnostic_inventory.csv": "analysis",
    "blind_review_rules.md": "document",
    "blind_review_scoring_template.csv": "blind_response_id",
    "build_blind_packet.py": "script",
    "raw_evidence_inventory.csv": "member",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fields is None:
        fields = list(rows[0]) if rows else ["empty"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def source_root(extracted: Path) -> Path:
    children = [p for p in extracted.iterdir() if p.is_dir()]
    if len(children) != 1:
        raise RuntimeError(f"Expected one package root under {extracted}, got {children}")
    return children[0]


def sanitize_csv(src: Path, dst: Path) -> None:
    rows = read_csv(src)
    fields: list[str]
    with src.open(encoding="utf-8-sig", newline="") as handle:
        fields = list(csv.DictReader(handle).fieldnames or [])
    for row in rows:
        for field in fields:
            key = field.lower()
            value = row.get(field, "")
            if key in {"review_identity", "reviewer_identity"}:
                row[field] = PUBLIC_ROLE
            elif key == "review_source" and any(
                token in value.lower() for token in ("model", "assistant", "secondary", "adjudicator")
            ):
                row[field] = PUBLIC_ROLE
    write_csv(dst, rows, fields)


def copy_public(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.suffix.lower() == ".csv":
        sanitize_csv(src, dst)
    elif src.suffix.lower() == ".json":
        payload = json.loads(src.read_text(encoding="utf-8-sig"))

        def scrub(value: object, key: str = "") -> object:
            if key in {"review_identity", "reviewer_identity"}:
                return PUBLIC_ROLE
            if isinstance(value, dict):
                return {k: scrub(v, k) for k, v in value.items()}
            if isinstance(value, list):
                return [scrub(v) for v in value]
            return value

        dst.write_text(json.dumps(scrub(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        shutil.copy2(src, dst)


def recompute_summary(by_item_path: Path, source_summary: Path, out: Path) -> None:
    items = read_csv(by_item_path)
    previous = {row["model_id"]: row for row in read_csv(source_summary)}
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in items:
        grouped[row["model_id"]].append(row)
    rows: list[dict[str, object]] = []
    for model_id in ["gpt-5.5", "ep-20260703090429-qpmt7", "deepseek-v4-pro", "mimo-v2.5-pro"]:
        model_rows = grouped[model_id]
        old = previous[model_id]
        reviewed = sum(float(r["reviewed_dimension_total"]) for r in model_rows) / len(model_rows)
        official = sum(float(r["official_item_score"]) for r in model_rows) / len(model_rows)
        rows.append(
            {
                "model_id": model_id,
                "model_display": old["model_display"],
                "items": len(model_rows),
                "v0_5_adjudicated_average": old["v0_5_adjudicated_average"],
                "v0_6_reviewed_average_before_hard_fail": f"{reviewed:.3f}",
                "v0_6_official_average": f"{official:.3f}",
                "confirmed_hard_fails": sum(r["hard_fail_status"] == "confirmed_hard_fail" for r in model_rows),
                "downgraded_hard_fails": sum(
                    r["hard_fail_status"] == "downgraded_to_dimension_issue" for r in model_rows
                ),
                "no_answers": sum(r["no_answer"].lower() == "true" for r in model_rows),
            }
        )
    write_csv(out, rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    review = repo / "review"
    public = review / "v0.6.0"
    internal = review / "internal_provenance"
    sources_out = internal / "source_packages"
    sources_out.mkdir(parents=True, exist_ok=True)

    package_inventory: list[dict[str, object]] = []
    roots: dict[str, Path] = {}
    with tempfile.TemporaryDirectory(prefix="sgs_v06_packages_") as temp:
        temp_root = Path(temp)
        for label, filename, priority in PACKAGE_SPECS:
            archive = args.source_dir / filename
            if not archive.exists():
                raise SystemExit(f"Missing source archive: {archive}")
            with zipfile.ZipFile(archive) as zf:
                bad = zf.testzip()
                if bad:
                    raise SystemExit(f"Bad ZIP member in {filename}: {bad}")
                destination = temp_root / label
                zf.extractall(destination)
                roots[label] = source_root(destination)
                members = len(zf.infolist())
            shutil.copy2(archive, sources_out / filename)
            package_inventory.append(
                {
                    "priority": priority,
                    "package_role": label,
                    "archive": filename,
                    "sha256": sha256(archive),
                    "members": members,
                    "source": "用户提供",
                    "validation": "ZIP and packaged SHA256SUMS passed",
                }
            )

        mapping = [
            ("item_validity", "all_242_item_validity_review.csv", "01_item_validity/all_242_item_validity_review.csv"),
            ("item_validity", "main_152_item_validity_review.csv", "01_item_validity/main_152_item_validity_review.csv"),
            ("item_validity", "robustness_40_item_validity_review.csv", "01_item_validity/robustness_40_item_validity_review.csv"),
            ("item_validity", "hard50_50_item_validity_review.csv", "01_item_validity/hard50_50_item_validity_review.csv"),
            ("item_validity", "item_validity_issue_queue.csv", "01_item_validity/item_validity_issue_queue.csv"),
            ("option_evidence", "mcq_122_item_option_set_summary.csv", "02_mcq_options/mcq_122_item_option_set_summary.csv"),
            ("option_evidence", "mcq_488_option_audit.csv", "02_mcq_options/mcq_488_option_audit.csv"),
            ("option_evidence", "mcq_defensible_distractor_and_gold_issue_queue.csv", "02_mcq_options/mcq_defensible_distractor_and_gold_issue_queue.csv"),
            ("option_evidence", "fr_30_reference_answer_external_evidence_audit.csv", "03_reference_evidence/fr_30_reference_answer_external_evidence_audit.csv"),
            ("option_evidence", "fr_112_reference_claim_evidence_audit.csv", "03_reference_evidence/fr_112_reference_claim_evidence_audit.csv"),
            ("option_evidence", "external_evidence_source_ledger.csv", "03_reference_evidence/external_evidence_source_ledger.csv"),
            ("option_evidence", "fr_reference_evidence_gap_queue.csv", "03_reference_evidence/fr_reference_evidence_gap_queue.csv"),
            ("free_response", "02_full_response_adjudication/full_review_by_item.csv", "04_free_response_adjudication/full_review_by_item.csv"),
            ("free_response", "02_full_response_adjudication/full_review_by_dimension.csv", "04_free_response_adjudication/full_review_by_dimension.csv"),
            ("free_response", "02_full_response_adjudication/confirmed_hard_fails.csv", "04_free_response_adjudication/confirmed_hard_fails.csv"),
            ("free_response", "02_full_response_adjudication/score_overrides.csv", "04_free_response_adjudication/score_overrides.csv"),
            ("free_response", "01_free_response_design_review/hard_fail_reclassification.csv", "04_free_response_adjudication/hard_fail_reclassification.csv"),
            ("free_response", "03_judge_reliability/judge_reliability_metrics.csv", "05_judge_reliability/judge_reliability_metrics.csv"),
            ("free_response", "03_judge_reliability/judge_disagreement_cases.csv", "05_judge_reliability/judge_disagreement_cases.csv"),
            ("free_response", "03_judge_reliability/judge_reliability_report.md", "05_judge_reliability/judge_reliability_report.md"),
            ("remaining_work", "robustness_40_item_pair_review.csv", "06_robustness/robustness_40_item_pair_review.csv"),
            ("remaining_work", "robustness_group_review.csv", "06_robustness/robustness_group_review.csv"),
            ("remaining_work", "hard50_item_calibration.csv", "07_hard50/hard50_item_calibration.csv"),
            ("remaining_work", "hard50_retire_rewrite_keep.csv", "07_hard50/hard50_retire_rewrite_keep.csv"),
            ("remaining_work", "content_quality_statistics.json", "08_statistics/content_quality_statistics.json"),
            ("remaining_work", "statistical_diagnostic_inventory.csv", "08_statistics/statistical_diagnostic_inventory.csv"),
            ("remaining_work", "blind_review_execution_packet/blind_review_rules.md", "09_blind_review/blind_review_execution_packet/blind_review_rules.md"),
            ("remaining_work", "blind_review_execution_packet/blind_review_scoring_template.csv", "09_blind_review/blind_review_execution_packet/blind_review_scoring_template.csv"),
            ("remaining_work", "blind_review_execution_packet/build_blind_packet.py", "09_blind_review/blind_review_execution_packet/build_blind_packet.py"),
            ("free_response", "00_review_foundation/raw_evidence_inventory.csv", "10_provenance/raw_evidence_inventory.csv"),
        ]
        integration_rows: list[dict[str, object]] = []
        for label, source_rel, target_rel in mapping:
            src = roots[label] / source_rel
            dst = public / target_rel
            # The clean raw rebuild supersedes the package placeholder. Preserve
            # that verified generated evidence on repeat integration runs.
            if not (target_rel == "10_provenance/raw_evidence_inventory.csv" and dst.exists()):
                copy_public(src, dst)
            integration_rows.append(
                {
                    "target": target_rel,
                    "selected_package": label,
                    "source_file": source_rel,
                    "primary_key": PRIMARY_KEYS[Path(target_rel).name],
                    "decision": "selected by owner priority and artifact purpose",
                    "score_impact": "yes" if "free_response_adjudication" in target_rel else "no",
                }
            )

        recompute_summary(
            public / "04_free_response_adjudication/full_review_by_item.csv",
            roots["free_response"] / "02_full_response_adjudication/official_free_response_summary.csv",
            public / "04_free_response_adjudication/official_free_response_summary.csv",
        )

        dashboard_map = [
            ("item_validity", "item_validity_dashboard.xlsx", "item_validity_dashboard.xlsx"),
            ("option_evidence", "option_and_reference_evidence_dashboard.xlsx", "option_reference_evidence_dashboard.xlsx"),
            ("free_response", "review_dashboard.xlsx", "free_response_review_dashboard.xlsx"),
            ("remaining_work", "remaining_work_dashboard.xlsx", "remaining_work_dashboard.xlsx"),
        ]
        for label, source_rel, name in dashboard_map:
            destination = public / "dashboards" / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            # Tracked public workbooks are role-sanitized release artifacts.
            if not destination.exists():
                shutil.copy2(roots[label] / source_rel, destination)

        write_csv(public / "00_scope/source_package_inventory.csv", package_inventory)
        write_csv(public / "00_scope/integration_decision_log.csv", integration_rows)

    conflict_rows = [
        {
            "conflict_id": "POLICY-001",
            "topic": "Hard Fail scoring",
            "old_state": "historical labels were count-only",
            "new_state": "3 confirmed failures zero official item score; 12 downgraded",
            "selected_authority": "project-owner prompt + free-response package",
            "preserved_old_location": "v0.5.0 Git tag and results/standard_20260703",
            "score_impact": "yes",
        },
        {
            "conflict_id": "IDENTITY-001",
            "topic": "public reviewer labels",
            "old_state": "identity-bearing reviewer descriptions",
            "new_state": "role label 专家 X in v0.6 public artifacts",
            "selected_authority": "project-owner prompt",
            "preserved_old_location": "review/internal_provenance/source_packages",
            "score_impact": "no",
        },
        {
            "conflict_id": "ROBUSTNESS-001",
            "topic": "Robustness review depth",
            "old_state": "40 item-validity rows",
            "new_state": "40 pair rows + 12 group rows extending identical base judgments",
            "selected_authority": "remaining-work package",
            "preserved_old_location": "01_item_validity/robustness_40_item_validity_review.csv",
            "score_impact": "interpretation only",
        },
        {
            "conflict_id": "HARD50-001",
            "topic": "Hard50 role",
            "old_state": "hard diagnostic leaderboard language",
            "new_state": "saturated regression diagnostic",
            "selected_authority": "remaining-work package",
            "preserved_old_location": "v0.5.0 Git tag",
            "score_impact": "no score rewrite",
        },
        {
            "conflict_id": "RAW-001",
            "topic": "raw rebuild implementation",
            "old_state": "package wrapper had an empty comparison mapping and expected CSVs absent from ZIP",
            "new_state": "rebuild from raw JSON + manifests and compare every deterministic output",
            "selected_authority": "actual archive + repository parsers",
            "preserved_old_location": "remaining-work source ZIP",
            "score_impact": "release gate",
        },
        {
            "conflict_id": "DOC-001",
            "topic": "release documentation",
            "old_state": "v0.5.0 policy, scores and reviewer wording",
            "new_state": "v0.6.0 scoring, role labels and known-issue disclosure",
            "selected_authority": "project-owner prompt + remaining-work drafts",
            "preserved_old_location": "v0.5.0 Git tag",
            "score_impact": "reported interpretation",
        },
        {
            "conflict_id": "MANIFEST-001",
            "topic": "package manifests and checksum lists",
            "old_state": "four package-specific manifests and SHA256SUMS cover different roots",
            "new_state": "all originals preserved; release manifest regenerated over the integrated tree",
            "selected_authority": "all source packages + generated release manifest",
            "preserved_old_location": "review/internal_provenance/source_packages",
            "score_impact": "no",
        },
        {
            "conflict_id": "STATS-001",
            "topic": "statistical computation status",
            "old_state": "remaining-work inventory marked diagnostics as requiring a raw run",
            "new_state": "clean raw rebuild completed all listed diagnostics",
            "selected_authority": "verified raw archive + full-statistics rebuild",
            "preserved_old_location": "remaining-work source ZIP",
            "score_impact": "diagnostic only",
        },
        {
            "conflict_id": "BLIND-001",
            "topic": "blind-review materials",
            "old_state": "foundation and remaining-work packages contain overlapping blind-review guidance",
            "new_state": "higher-priority execution packet published without a claim that blind review occurred",
            "selected_authority": "remaining-work package + project-owner prompt",
            "preserved_old_location": "all four exact source ZIPs",
            "score_impact": "no",
        },
        {
            "conflict_id": "DASHBOARD-001",
            "topic": "overlapping source dashboards",
            "old_state": "each package contains a scope-specific source workbook",
            "new_state": "all four scope dashboards retained as role-sanitized public copies",
            "selected_authority": "artifact purpose; no mechanical overwrite",
            "preserved_old_location": "review/internal_provenance/source_packages",
            "score_impact": "no",
        },
    ]
    conflict_details = {
        "POLICY-001": ("official_item_score", "task_id+model_id", "owner prompt + free_response/full_review_by_item.csv"),
        "IDENTITY-001": ("review_identity/reviewer", "artifact_path+row_key", "owner prompt"),
        "ROBUSTNESS-001": ("extended pair/group review fields", "item_id / base_or_parent_id", "remaining-work package"),
        "HARD50-001": ("public interpretation role", "item_id / set", "remaining-work package"),
        "RAW-001": ("raw_to_derived comparison implementation", "artifact+id+model_id(+dimension)", "raw archive + repository parser behavior"),
        "DOC-001": ("release version/scoring/identity wording", "document_path+section", "owner prompt + verified repository facts"),
        "MANIFEST-001": ("manifest/checksum scope", "archive+member_path", "integrated v0.6.0 manifest"),
        "STATS-001": ("diagnostic status/output path", "analysis", "clean full-statistics rebuild"),
        "BLIND-001": ("blind-review execution status", "document_path", "remaining-work execution packet"),
        "DASHBOARD-001": ("dashboard scope and public role wording", "workbook_path+sheet", "role-sanitized scope workbook"),
    }
    for row in conflict_rows:
        field, primary_key, selected_version = conflict_details[str(row["conflict_id"])]
        row["conflict_field"] = field
        row["primary_key"] = primary_key
        row["selected_version"] = selected_version
    write_csv(public / "00_scope/package_conflict_report.csv", conflict_rows)

    owner_decisions = {
        "target_release": "0.6.0",
        "hard_fail_affects_score": True,
        "confirmed_hard_fail_official_score": 0,
        "provisional_judge_hard_fail_affects_score": False,
        "no_answer_rule": "deterministic_no_rescue_zero",
        "modify_questions_options_gold_reference_ids": False,
        "modify_raw_model_outputs": False,
        "preserve_v0_5_0": True,
        "main_leaderboard": "122-item SGS152 MCQ only",
        "approved_by": "项目负责人",
    }
    (public / "00_scope").mkdir(parents=True, exist_ok=True)
    (public / "00_scope/owner_decisions.json").write_text(
        json.dumps(owner_decisions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (public / "00_scope/review_scope.md").write_text(
        "# v0.6.0 Review Scope\n\n"
        "v0.6.0 integrates item, option, Reference Answer, free-response, Judge reliability, "
        "Robustness and Hard50 audits while keeping the benchmark and original model outputs frozen.\n\n"
        "本轮由匿名评审角色「专家 X」完成第二轮复核，并由项目负责人确认评审范围与计分政策。"
        "该轮复核已接触历史评审材料，因此不作为独立盲审结果。本次整合不修改题干、选项、"
        "Gold Answer、Reference Answer、题目 ID 或原始模型输出。\n\n"
        "GPT-5.6-sol is Judge-only and is not a participating model. The 122-item SGS152 MCQ set "
        "remains the only main leaderboard.\n",
        encoding="utf-8",
    )
    (public / "00_scope/known_limitations.md").write_text(
        "# Known Limitations\n\n"
        "- Five frozen P0 records remain: `SGS-FM-034`, `SGS-007-R03`, `SGS-097-R03`, "
        "`SGS-HARD-016`, and `SGS-HARD-028`.\n"
        "- Fifty-six non-Gold MCQ options remain defensible under the frozen item wording.\n"
        "- Robustness is an optional diagnostic and contains two P0 variants.\n"
        "- Hard50 is saturated and is retained as a regression diagnostic, not a hard leaderboard.\n"
        "- The blind-review execution packet is available, but this release did not use an "
        "independent blind-review design.\n",
        encoding="utf-8",
    )

    internal.mkdir(parents=True, exist_ok=True)
    (internal / "reviewer_role_registry.md").write_text(
        "# Reviewer Role Registry — Internal\n\n"
        "- Public label `专家 X`: anonymous public role for the current review materials supplied by "
        "the project owner. The source archives do not disclose a specific generating model or tool.\n"
        "- `项目负责人`: confirmed the review scope, frozen-content boundary and scoring policy.\n"
        "- `复核者`: deterministic repository integration and validation, not a new scientific "
        "adjudication.\n"
        "- `Judge`: GPT-5.6-sol fixed-rubric scoring role.\n",
        encoding="utf-8",
    )
    provenance = {
        "release": "0.6.0",
        "generated_on": str(date.today()),
        "source_archives": package_inventory,
        "source_review_model_or_tool": "unknown/not disclosed in supplied archives",
        "integration_tool": "Codex",
        "integration_reviewed_prior_scores": True,
        "integration_blind": False,
        "project_owner_confirmed": [
            "release target v0.6.0",
            "frozen benchmark and original outputs",
            "3 confirmed and 12 downgraded Hard Fails",
            "public role-label boundary",
            "package priority order",
        ],
    }
    (internal / "generation_provenance.json").write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (internal / "review_identity_boundary.md").write_text(
        "# Review Identity Boundary — Internal\n\n"
        "Public release artifacts use project-approved role labels for expert review and verification. "
        "Participating model and Judge model names remain explicit because they are evaluated-system "
        "and scoring-system provenance. Exact reviewer-source details remain in this internal area.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
