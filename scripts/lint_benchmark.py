#!/usr/bin/env python3
"""Compatibility entrypoint for the active mini-benchmark 0.4.0 lint suite."""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V4_DIR = ROOT / "SGS-mini-benchmark-V4"


def main() -> None:
    subprocess.run(["python3", "scripts/lint_benchmark.py"], cwd=V4_DIR, check=True)
    subprocess.run(["python3", "scripts/lint_sgs100_benchmark.py"], cwd=V4_DIR, check=True)


if __name__ == "__main__":
    main()
