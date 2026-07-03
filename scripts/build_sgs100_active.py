#!/usr/bin/env python3
"""Refresh Domain Core Set artifacts without changing the SGS152 active set."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOMAIN_CORE_JSON = ROOT / "data/benchmark_sgs100_clean.json"
DOMAIN_CORE_CSV = ROOT / "data/benchmark_sgs100_clean.csv"


def csv_value(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    if value is None:
        return ""
    return str(value)


def main() -> None:
    rows = json.loads(DOMAIN_CORE_JSON.read_text(encoding="utf-8"))
    if len(rows) != 100:
        raise SystemExit(f"Domain Core Set must contain 100 items, got {len(rows)}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with DOMAIN_CORE_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: csv_value(row.get(key, "")) for key in fieldnames})
    print("Refreshed Domain Core Set CSV: 100 items")


if __name__ == "__main__":
    main()
