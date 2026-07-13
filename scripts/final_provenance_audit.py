#!/usr/bin/env python3
"""Final provenance gate for the active SGS v0.6.0 release."""

from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "artifacts/SGS152_raw_evidence_20260713.zip"
EXPECTED_ARCHIVE_SHA256 = "9cbaba75d0ade9b2c8673cf54c06e991e616b3e1180d416ae374101debccc103"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    errors: list[str] = []
    if not ARCHIVE.exists() or sha256(ARCHIVE) != EXPECTED_ARCHIVE_SHA256:
        errors.append("raw evidence archive is missing or has a different SHA-256")
    else:
        with zipfile.ZipFile(ARCHIVE) as handle:
            if handle.testzip() is not None:
                errors.append("raw evidence ZIP integrity failed")
            if len(handle.infolist()) != 46:
                errors.append("raw evidence ZIP must contain 46 members")
    verification = ROOT / "review/v0.6.0/10_provenance/raw_archive_verification_manifest.json"
    if not verification.exists():
        errors.append("raw archive verification manifest is missing")
    else:
        payload = json.loads(verification.read_text(encoding="utf-8"))
        if payload.get("raw_to_derived_diff_count") != 0:
            errors.append("raw-to-derived differences are not zero")
        if payload.get("judge_review_count") != 120 or not payload.get("judge_primary_keys_unique"):
            errors.append("Judge review count or primary-key uniqueness differs")
        if payload.get("deepseek_sgs_081_raw_answer") != "" or payload.get("deepseek_sgs_081_no_rescue_total") != 0.0:
            errors.append("DeepSeek SGS-081 raw missing-answer/no-rescue evidence differs")
    if errors:
        print("Final provenance audit failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)
    print("Final provenance audit passed: archive, member count, raw rebuild and no-rescue evidence verified.")


if __name__ == "__main__":
    main()
