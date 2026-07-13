#!/usr/bin/env python3
"""CLI for the deterministic raw-evidence rebuild."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from raw_evidence import rebuild_all


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--publish-dir", type=Path)
    args = parser.parse_args()
    result = rebuild_all(args.repo_root, args.archive, args.out)
    if args.publish_dir:
        args.publish_dir.mkdir(parents=True, exist_ok=True)
        for name in [
            "raw_archive_verification_manifest.json",
            "raw_to_derived_diff.csv",
            "raw_evidence_inventory.csv",
            "raw_archive_verification_report.md",
        ]:
            shutil.copy2(args.out / name, args.publish_dir / name)
    print(
        f"Verified {result['zip_member_count']} ZIP members, "
        f"{result['judge_review_count']} Judge rows, and zero raw-to-derived differences."
    )


if __name__ == "__main__":
    main()
