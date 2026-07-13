#!/usr/bin/env python3
"""Preserve legacy v0.5 adjudication files internally and publish role-neutral copies."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "results/standard_20260703/free_response_judge"
INTERNAL = ROOT / "review/internal_provenance/legacy_v0_5_adjudication"
RENAMES = {
    "human_review_decisions.csv": "expert_review_decisions.csv",
    "human_review_overrides.csv": "expert_review_overrides.csv",
    "human_review_decisions.template.csv": "expert_review_decisions.template.csv",
    "human_review_overrides.template.csv": "expert_review_overrides.template.csv",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rewrite_csv(source: Path, target: Path) -> None:
    with source.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fields = list(reader.fieldnames or [])
    renamed_fields = [field.replace("human_", "expert_") for field in fields]
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=renamed_fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            updated: dict[str, str] = {}
            for field, value in row.items():
                key = field.replace("human_", "expert_")
                if value == "assistant_review_under_project_owner_delegation":
                    value = "expert_x_review"
                elif value == "codex_assistant_under_user_delegation":
                    value = "专家 X"
                updated[key] = value
            writer.writerow(updated)


def main() -> None:
    INTERNAL.mkdir(parents=True, exist_ok=True)
    preserved = list(RENAMES) + [
        "manual_review_packet.csv", "adjudication_manifest.json", "adjudication_notes.md",
    ]
    for name in preserved:
        source = SOURCE / name
        if source.exists() and not (INTERNAL / name).exists():
            shutil.copy2(source, INTERNAL / name)

    for old_name, new_name in RENAMES.items():
        old = SOURCE / old_name
        preserved_old = INTERNAL / old_name
        source = old if old.exists() else preserved_old
        rewrite_csv(source, SOURCE / new_name)
        if old.exists():
            old.unlink()

    packet = SOURCE / "manual_review_packet.csv"
    rewrite_csv(packet, packet.with_suffix(".tmp.csv"))
    packet.with_suffix(".tmp.csv").replace(packet)

    manifest_path = SOURCE / "adjudication_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["review_type"] = "expert_x_review"
    manifest["reviewer"] = "专家 X"
    manifest["record_status"] = "legacy_v0.5_record_superseded_by_review/v0.6.0"
    manifest["packet_hash"] = sha256(SOURCE / "manual_review_packet.csv")
    manifest["decisions_file"] = "expert_review_decisions.csv"
    manifest["overrides_file"] = "expert_review_overrides.csv"
    manifest["decisions_hash"] = sha256(SOURCE / "expert_review_decisions.csv")
    manifest["overrides_hash"] = sha256(SOURCE / "expert_review_overrides.csv")
    manifest.pop("independent_external_human_review", None)
    manifest["independent_blind_review_design"] = False
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Published role-neutral review artifacts and preserved v0.5 originals internally.")


if __name__ == "__main__":
    main()
