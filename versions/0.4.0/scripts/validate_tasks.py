#!/usr/bin/env python3
"""Compatibility validator for the active mini-benchmark 0.4.0 task file."""

from __future__ import annotations

import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    runpy.run_path(str(ROOT / "scripts/validate_benchmark.py"), run_name="__main__")


if __name__ == "__main__":
    main()
