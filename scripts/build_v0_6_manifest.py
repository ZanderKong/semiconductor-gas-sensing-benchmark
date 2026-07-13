#!/usr/bin/env python3
"""Build the deterministic public v0.6.0 review manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "review/v0.6.0"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    files = []
    for path in sorted(REVIEW.rglob("*")):
        if path.is_file() and path.name != "manifest.json":
            files.append(
                {"path": str(path.relative_to(REVIEW)), "size": path.stat().st_size, "sha256": sha256(path)}
            )
    manifest = {
        "release": "v0.6.0",
        "release_date": "2026-07-13",
        "frozen_baseline_commit": "dfa28407e5130dbc4328ac006a5368f18bdbff7d",
        "judge_model": "GPT-5.6-sol",
        "judge_role": "judge-only; not a participating model",
        "main_leaderboard": "SGS152 122-item MCQ",
        "file_count": len(files),
        "files": files,
    }
    (REVIEW / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote v0.6.0 manifest for {len(files)} files.")


if __name__ == "__main__":
    main()
