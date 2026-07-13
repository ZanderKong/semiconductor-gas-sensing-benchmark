#!/usr/bin/env python3
"""Build a true blind review packet from the frozen free-response outputs."""
from __future__ import annotations
import argparse, csv, hashlib, json, random
from pathlib import Path

def read_csv(p):
    with open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def write_csv(p, rows, fields):
    with open(p, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-outputs", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--seed", type=int, default=20260713)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    rows = read_csv(args.model_outputs)
    required = {"id","model_id","answer"}
    if not required.issubset(rows[0]):
        raise SystemExit(f"Missing columns: {required-set(rows[0])}")
    if len(rows) != 120:
        raise SystemExit(f"Expected 120 answers, got {len(rows)}")

    rng = random.Random(args.seed)
    by_task = {}
    for r in rows:
        by_task.setdefault(r["id"], []).append(r)

    blind, mapping = [], []
    n = 1
    for task in sorted(by_task):
        candidates = by_task[task][:]
        rng.shuffle(candidates)
        for r in candidates:
            bid = f"BR-{n:03d}"
            blind.append({
                "blind_response_id": bid,
                "task_id": task,
                "response_text": r.get("answer",""),
            })
            mapping.append({
                "blind_response_id": bid,
                "task_id": task,
                "model_id": r["model_id"],
            })
            n += 1

    write_csv(args.out_dir/"blind_answers.csv", blind,
              ["blind_response_id","task_id","response_text"])
    write_csv(args.out_dir/"UNBLIND_MAPPING_KEEP_PRIVATE.csv", mapping,
              ["blind_response_id","task_id","model_id"])
    packet_hash = hashlib.sha256((args.out_dir/"blind_answers.csv").read_bytes()).hexdigest()
    (args.out_dir/"blind_packet_manifest.json").write_text(
        json.dumps({"seed":args.seed,"rows":len(blind),"blind_answers_sha256":packet_hash}, indent=2),
        encoding="utf-8")
if __name__ == "__main__":
    main()
