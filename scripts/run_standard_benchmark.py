#!/usr/bin/env python3
"""Run the standardized full SGS benchmark evaluation."""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

MODEL_SPECS = {
    "gpt-5.5": "gpt-5.5",
    "deepseek-v4-pro": "openai_compatible|deepseek-v4-pro|https://api.deepseek.com|DEEPSEEK_API_KEY|thinking=enabled|reasoning_effort=high|omit_temperature=true",
    "mimo-v2.5-pro": "openai_compatible|mimo-v2.5-pro|https://api.xiaomimimo.com/v1|MIMO_API_KEY|auth=api-key|omit_temperature=true",
    "seed-2.1": "openai_compatible|ep-20260703090429-qpmt7|https://ark.cn-beijing.volces.com/api/v3|VOLCENGINE_API_KEY|omit_temperature=true",
    "kimi-k2.6": "openai_compatible|kimi-k2.6|https://api.moonshot.ai/v1|KIMI_API_KEY|thinking=disabled|omit_temperature=true",
}
REQUIRED_MODELS = {"gpt-5.5", "deepseek-v4-pro", "mimo-v2.5-pro", "seed-2.1"}
OPTIONAL_MODELS = {"kimi-k2.6"}


def run(cmd: list[str], *, env: dict[str, str] | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    print("+ " + " ".join(cmd), flush=True)
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, env=env)
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)
    if check and proc.returncode != 0:
        raise SystemExit(proc.returncode)
    return proc


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def git_clean() -> bool:
    status = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True)
    return not status.strip()


def count_checks() -> dict[str, Any]:
    expected = {
        "data/benchmark.json": {"items": 152, "multiple_choice": 122, "free_response": 30},
        "data/benchmark_sgs100_robustness.json": {"items": 40, "multiple_choice": 40, "free_response": 0},
        "data/benchmark_sgs_hard50.json": {"items": 50, "multiple_choice": 50, "free_response": 0},
    }
    results = {}
    for rel, want in expected.items():
        rows = json.loads((ROOT / rel).read_text(encoding="utf-8"))
        got = {
            "items": len(rows),
            "multiple_choice": sum(1 for row in rows if row.get("question_type") == "multiple_choice"),
            "free_response": sum(1 for row in rows if row.get("question_type") == "free_response"),
        }
        if got != want:
            raise SystemExit(f"{rel} count mismatch: got {got}, expected {want}")
        results[rel] = got
    return results


def read_model_outputs(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def smoke_model(model_id: str, spec: str, out_dir: Path, env: dict[str, str], timeout: int) -> dict[str, Any]:
    model_dir = out_dir / model_id
    out_file = model_dir / "model_outputs.csv"
    manifest = model_dir / "manifest.json"
    raw_dir = model_dir / "raw_model_outputs"
    model_dir.mkdir(parents=True, exist_ok=True)
    proc = run(
        [
            "python3",
            "eval/run_eval.py",
            "--benchmark",
            "data/benchmark.json",
            "--question-type",
            "multiple_choice",
            "--limit",
            "2",
            "--out",
            str(out_file),
            "--raw-dir",
            str(raw_dir),
            "--manifest",
            str(manifest),
            "--timeout",
            str(timeout),
            "--temperature",
            "0",
            "--models",
            spec,
        ],
        env=env,
        check=False,
    )
    ok = proc.returncode == 0
    error = ""
    rows = []
    if out_file.exists():
        rows = read_model_outputs(out_file)
        ok = ok and len([row for row in rows if row.get("id")]) == 2 and all(row.get("answer") for row in rows)
        errors = [row.get("error", "") for row in rows if row.get("error")]
        if errors:
            error = "; ".join(errors)
            ok = False
    else:
        ok = False
        error = "missing smoke output file"
    return {
        "model_id": model_id,
        "ok": ok,
        "error": error,
        "returncode": proc.returncode,
        "rows": len(rows),
        "output_file": display_path(out_file),
    }


def run_stage(stage: dict[str, str], specs: list[str], out_root: Path, env: dict[str, str], timeout: int) -> None:
    stage_dir = out_root / stage["name"]
    out_file = stage_dir / "model_outputs.csv"
    manifest = stage_dir / "manifest.json"
    raw_dir = stage_dir / "raw_model_outputs"
    stage_dir.mkdir(parents=True, exist_ok=True)
    run(
        [
            "python3",
            "eval/run_eval.py",
            "--benchmark",
            stage["benchmark"],
            "--question-type",
            stage["question_type"],
            "--out",
            str(out_file),
            "--raw-dir",
            str(raw_dir),
            "--manifest",
            str(manifest),
            "--timeout",
            str(timeout),
            "--temperature",
            "0",
            "--models",
            *specs,
        ],
        env=env,
    )


def score_mcq(stage_dir: Path, benchmark: str, scope: str, interpretation: str) -> None:
    scored = stage_dir / "scored"
    run(
        [
            "python3",
            "eval/score_mcq.py",
            "--benchmark",
            benchmark,
            "--outputs",
            str(stage_dir / "model_outputs.csv"),
            "--summary",
            str(scored / "model_results_summary.json"),
            "--badcases",
            str(scored / "review_items.json"),
            "--diagnostic-report",
            str(scored / "diagnostic_report.md"),
            "--run-date",
            date.today().isoformat(),
            "--scope-label",
            scope,
            "--interpretation",
            interpretation,
        ]
    )


def write_smoke_report(out_dir: Path, rows: list[dict[str, Any]]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "smoke_summary.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["model_id", "ok", "error", "returncode", "rows", "output_file"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (out_dir / "smoke_summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_analysis(out_root: Path, smoke_rows: list[dict[str, Any]]) -> None:
    core_dir = out_root / "analysis_core"
    full_dir = out_root / "analysis_full"
    core_dir.mkdir(parents=True, exist_ok=True)
    full_dir.mkdir(parents=True, exist_ok=True)

    mcq = load_json(out_root / "sgs152_mcq/scored/model_results_summary.json")
    fr_summary = list(csv.DictReader((out_root / "free_response_judge/scored_free_response_summary.csv").open(encoding="utf-8")))
    robustness = load_json(out_root / "robustness/scored/model_results_summary.json")
    hard50 = load_json(out_root / "hard50/scored/model_results_summary.json")

    fr_by_model = {row["model_id"]: row for row in fr_summary}
    lines = [
        "# Core SGS152 Analysis",
        "",
        "Scope: SGS152 MCQ plus live free-response outputs judged by GPT-5.5/ChatGPT.",
        "",
        "Bias note: free-response judge overlaps with one candidate model family.",
        "",
        "| Model | SGS152 MCQ | Free-response Avg | FR Hard Fails |",
        "|---|---:|---:|---:|",
    ]
    for row in sorted(mcq, key=lambda item: item["model_id"]):
        fr = fr_by_model.get(row["model_id"], {})
        lines.append(
            f"| {row['model_id']} | {row['correct']} / {row['total']} ({row['mc_accuracy'] * 100:.1f}%) | "
            f"{fr.get('average_score', 'n/a')} | {fr.get('hard_fail_count', 'n/a')} |"
        )
    lines.extend(
        [
            "",
            "This analysis only uses artifacts produced in this standard run directory.",
            "",
        ]
    )
    (core_dir / "core_analysis.md").write_text("\n".join(lines), encoding="utf-8")

    rb = {row["model_id"]: row for row in robustness}
    hd = {row["model_id"]: row for row in hard50}
    lines = [
        "# Full Benchmark Analysis",
        "",
        "Scope: SGS152, Robustness, and Hard50. Robustness and Hard50 remain diagnostic layers and are not collapsed into a single headline score.",
        "",
        "| Model | SGS152 MCQ | Free-response Avg | Robustness | Hard50 |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in sorted(mcq, key=lambda item: item["model_id"]):
        model = row["model_id"]
        fr = fr_by_model.get(model, {})
        rob = rb.get(model, {})
        hard = hd.get(model, {})
        lines.append(
            f"| {model} | {row['correct']} / {row['total']} | {fr.get('average_score', 'n/a')} | "
            f"{rob.get('correct', 'n/a')} / {rob.get('total', 'n/a')} | {hard.get('correct', 'n/a')} / {hard.get('total', 'n/a')} |"
        )
    failed_smoke = [row for row in smoke_rows if not row["ok"]]
    if failed_smoke:
        lines.extend(["", "## Smoke Failures", ""])
        for row in failed_smoke:
            lines.append(f"- {row['model_id']}: {row.get('error') or 'failed smoke test'}")
    lines.extend(["", "This analysis only uses current standard-run artifacts and does not reuse reconstructed or legacy outputs.", ""])
    (full_dir / "full_analysis.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-root", default=str(ROOT / f"results/standard_{date.today().strftime('%Y%m%d')}"))
    parser.add_argument("--skip-preflight", action="store_true")
    parser.add_argument("--smoke-timeout", type=int, default=900)
    parser.add_argument("--timeout", type=int, default=2400)
    parser.add_argument("--allow-dirty", action="store_true")
    args = parser.parse_args()

    out_root = Path(args.out_root)
    env = os.environ.copy()
    started = datetime.now(timezone.utc)
    out_root.mkdir(parents=True, exist_ok=True)

    if not args.allow_dirty and not git_clean():
        raise SystemExit("Working tree must be clean before standard benchmark run. Commit the baseline first.")

    preflight: dict[str, Any] = {
        "created_at": started.isoformat(),
        "out_root": display_path(out_root),
        "count_checks": count_checks(),
        "python": sys.version,
        "models": list(MODEL_SPECS),
    }
    if not args.skip_preflight:
        run(["python3", "scripts/validate_benchmark.py"])
        run(["python3", "scripts/lint_benchmark.py"])
        run(["python3", "scripts/validate_hard50.py"])

    smoke_dir = out_root / "smoke"
    smoke_rows = [smoke_model(model_id, spec, smoke_dir, env, args.smoke_timeout) for model_id, spec in MODEL_SPECS.items()]
    write_smoke_report(smoke_dir, smoke_rows)
    preflight["smoke"] = smoke_rows
    (out_root / "preflight_manifest.json").write_text(json.dumps(preflight, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    failed_required = [row for row in smoke_rows if row["model_id"] in REQUIRED_MODELS and not row["ok"]]
    if failed_required:
        raise SystemExit(f"Required model smoke failed: {[row['model_id'] for row in failed_required]}")
    passing_models = [row["model_id"] for row in smoke_rows if row["ok"] and (row["model_id"] in REQUIRED_MODELS or row["model_id"] in OPTIONAL_MODELS)]
    specs = [MODEL_SPECS[model_id] for model_id in passing_models]

    stages = [
        {
            "name": "sgs152_mcq",
            "benchmark": "data/benchmark.json",
            "question_type": "multiple_choice",
            "scope": "standard SGS152 MCQ set",
            "interpretation": "Core SGS152 MCQ scoring under a single prompt, single sampling, no-tool standard run.",
        },
        {
            "name": "sgs152_free_response",
            "benchmark": "data/benchmark.json",
            "question_type": "free_response",
        },
        {
            "name": "robustness",
            "benchmark": "data/benchmark_sgs100_robustness.json",
            "question_type": "multiple_choice",
            "scope": "standard robustness MCQ set",
            "interpretation": "Robustness diagnostics under paraphrase, distractor, condition update, safety, and tool-observation shifts.",
        },
        {
            "name": "hard50",
            "benchmark": "data/benchmark_sgs_hard50.json",
            "question_type": "multiple_choice",
            "scope": "standard Hard50 diagnostic MCQ set",
            "interpretation": "Hard diagnostic layer for evidence conflict, safety gates, condition updates, and mechanism-transfer traps.",
        },
    ]
    for stage in stages:
        run_stage(stage, specs, out_root, env, args.timeout)
        if stage["question_type"] == "multiple_choice":
            score_mcq(out_root / stage["name"], stage["benchmark"], stage["scope"], stage["interpretation"])

    run(
        [
            "python3",
            "eval/judge_free_response_live.py",
            "--benchmark",
            "data/benchmark.json",
            "--outputs",
            str(out_root / "sgs152_free_response/model_outputs.csv"),
            "--out-dir",
            str(out_root / "free_response_judge"),
            "--judge-model",
            "gpt-5.5",
            "--timeout",
            str(args.timeout),
        ],
        env=env,
    )
    write_analysis(out_root, smoke_rows)
    print(f"Standard benchmark run complete: {display_path(out_root)}")


if __name__ == "__main__":
    main()
