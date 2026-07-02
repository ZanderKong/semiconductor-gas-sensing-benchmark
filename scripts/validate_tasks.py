#!/usr/bin/env python3
"""Compatibility entrypoint for the active mini-benchmark 0.5.0 validator."""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_DIR = ROOT / "versions/0.5.0"


def main() -> None:
    subprocess.run(["python3", "scripts/validate_benchmark.py"], cwd=ACTIVE_DIR, check=True)
    subprocess.run(["python3", "scripts/validate_hard50.py"], cwd=ACTIVE_DIR, check=True)


if __name__ == "__main__":
    main()
