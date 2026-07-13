#!/usr/bin/env python3
"""Judge live free-response benchmark outputs with a fixed rubric prompt."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import tempfile
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any

from codex_cli import resolve_codex_cli


ROOT = Path(__file__).resolve().parents[1]
DIMENSIONS = [
    "final_answer_alignment",
    "professional_accuracy",
    "reasoning_path",
    "evidence_boundary",
    "experimental_design",
    "decision_logic",
    "safety_and_privacy",
    "conciseness_and_traceability",
]
DIM_MAX = 1.25


def display_path(path: str | Path) -> str:
    path = Path(path)
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def sha256_file(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def current_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unknown"


def working_tree_dirty() -> bool | None:
    try:
        status = subprocess.check_output(
            ["git", "status", "--porcelain"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        )
        return bool(status.strip())
    except Exception:
        return None


def extract_json(text: str) -> Any:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.S)
        if not match:
            raise
        return json.loads(match.group(0))


def call_codex(model_id: str, prompt: str, timeout: int) -> tuple[str, float]:
    codex = resolve_codex_cli()
    started = time.time()
    with tempfile.TemporaryDirectory(prefix="sgs_judge_") as tmp:
        tmp_path = Path(tmp)
        prompt_path = tmp_path / "prompt.txt"
        out_path = tmp_path / "last_message.txt"
        prompt_path.write_text(prompt, encoding="utf-8")
        cmd = [
            str(codex),
            "exec",
            "--skip-git-repo-check",
            "--ephemeral",
            "--sandbox",
            "read-only",
            "--ignore-rules",
            "-m",
            model_id,
            "-c",
            'model_reasoning_effort="low"',
            "--output-last-message",
            str(out_path),
            "-",
        ]
        with prompt_path.open("r", encoding="utf-8") as stdin:
            proc = subprocess.run(
                cmd,
                cwd=tmp_path,
                stdin=stdin,
                text=True,
                capture_output=True,
                timeout=timeout,
            )
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr[-2000:])
        return out_path.read_text(encoding="utf-8"), round(time.time() - started, 2)


def load_free_response_items(path: Path) -> dict[str, dict[str, Any]]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    return {row["id"]: row for row in rows if row.get("question_type") == "free_response"}


def load_outputs(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as f:
        return [row for row in csv.DictReader(f) if row.get("id")]


def item_payload(item: dict[str, Any], answer: str) -> dict[str, Any]:
    return {
        "id": item["id"],
        "question": item["question"],
        "domain": item.get("domain"),
        "scenario_stage": item.get("scenario_stage"),
        "tool_type": item.get("tool_type"),
        "rubric": item.get("rubric"),
        "key_points": item.get("key_points", []),
        "hard_fails": item.get("hard_fails", []),
        "common_failure_modes": item.get("common_failure_modes", []),
        "reference_answer": item.get("answer") or item.get("answer_rationale"),
        "model_answer": answer,
    }


def build_prompt(judge_prompt: Path, model_id: str, rows: list[dict[str, Any]]) -> str:
    intro = judge_prompt.read_text(encoding="utf-8")
    schema = {
        "reviews": [
            {
                "id": "SGS-018",
                "model_id": model_id,
                "hard_fail": False,
                "hard_fail_reasons": [],
                "scores": {dimension: 1.0 for dimension in DIMENSIONS},
                "total": 8.0,
                "comment": "一句话说明主要依据和扣分点。",
            }
        ]
    }
    return (
        intro
        + "\n\n请一次性评分下面同一个模型的全部开放题回答。"
        + "\n必须输出一个 JSON object，顶层键为 reviews；reviews 中每个题目一条记录。"
        + "\n每个 scores 只能包含指定 8 个维度，每个维度 0 到 1.25。"
        + "\n不要输出 Markdown，不要输出推理过程。"
        + "\n\n输出 schema 示例：\n"
        + json.dumps(schema, ensure_ascii=False)
        + "\n\n待评分数据：\n"
        + json.dumps({"model_id": model_id, "items": rows}, ensure_ascii=False)
    )


def normalize_review(raw: dict[str, Any], expected_id: str, model_id: str) -> dict[str, Any]:
    scores = raw.get("scores") if isinstance(raw.get("scores"), dict) else {}
    normalized_scores: dict[str, float] = {}
    for dimension in DIMENSIONS:
        try:
            value = float(scores.get(dimension, 0))
        except (TypeError, ValueError):
            value = 0.0
        normalized_scores[dimension] = round(max(0.0, min(DIM_MAX, value)), 2)
    total = round(sum(normalized_scores.values()), 2)
    return {
        "id": str(raw.get("id") or expected_id),
        "model_id": str(raw.get("model_id") or model_id),
        "hard_fail": bool(raw.get("hard_fail", False)),
        "hard_fail_reasons": raw.get("hard_fail_reasons") or [],
        "scores": normalized_scores,
        "total": total,
        "comment": str(raw.get("comment", "")),
    }


def parse_reviews(text: str, expected_ids: list[str], model_id: str) -> list[dict[str, Any]]:
    payload = extract_json(text)
    reviews = payload.get("reviews", payload if isinstance(payload, list) else [])
    if not isinstance(reviews, list):
        raise ValueError(f"{model_id}: judge output reviews must be a list")
    valid = [review for review in reviews if isinstance(review, dict) and review.get("id")]
    raw_ids = [str(review["id"]) for review in valid]
    if len(raw_ids) != len(set(raw_ids)):
        raise ValueError(f"{model_id}: judge output contains duplicate item IDs")
    missing = sorted(set(expected_ids) - set(raw_ids))
    unexpected = sorted(set(raw_ids) - set(expected_ids))
    if missing or unexpected:
        raise ValueError(f"{model_id}: judge item mismatch; missing={missing}, unexpected={unexpected}")
    by_id = {str(review["id"]): review for review in valid}
    parsed = []
    for qid in expected_ids:
        raw = by_id[qid]
        raw_model_id = str(raw.get("model_id", ""))
        if raw_model_id != model_id:
            raise ValueError(f"{model_id}: judge returned model_id={raw_model_id!r} for {qid}")
        parsed.append(normalize_review(raw, qid, model_id))
    return parsed


def no_rescue_review(review: dict[str, Any], answer: str) -> dict[str, Any]:
    if answer.strip():
        return review
    return {
        "id": review["id"],
        "model_id": review["model_id"],
        "hard_fail": False,
        "hard_fail_reasons": [],
        "scores": {dimension: 0.0 for dimension in DIMENSIONS},
        "total": 0.0,
        "comment": "Missing model answer; deterministic no-rescue score is 0.",
    }


def judge_bias_note(judge_model: str, candidate_models: list[str]) -> str:
    if judge_model in candidate_models:
        return "Judge model is also a participating model; exact self-judge overlap must be considered."
    if judge_model.startswith("gpt-") and any(model.startswith("gpt-") for model in candidate_models):
        return "Judge is not a participating model, but same-family correlation with the participating GPT model may remain; results await independent human review."
    return "Judge is not a participating model; automated rubric scores still await independent human review."


def write_csvs(out_dir: Path, reviews: list[dict[str, Any]], items: dict[str, dict[str, Any]]) -> None:
    by_item = out_dir / "scored_free_response_by_item.csv"
    by_dimension = out_dir / "scored_free_response_by_dimension.csv"
    summary = out_dir / "scored_free_response_summary.csv"
    review_list = out_dir / "manual_review_queue.csv"

    with by_item.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "id",
                "model_id",
                "set",
                "hard_fail",
                "hard_fail_reasons",
                "total_score",
                "max_score",
                "comment",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        for review in reviews:
            item = items[review["id"]]
            writer.writerow(
                {
                    "id": review["id"],
                    "model_id": review["model_id"],
                    "set": "Scientific Stress" if item.get("subset") == "scientific_stress" else "Domain Core",
                    "hard_fail": review["hard_fail"],
                    "hard_fail_reasons": "; ".join(map(str, review["hard_fail_reasons"])),
                    "total_score": review["total"],
                    "max_score": 10.0,
                    "comment": review["comment"],
                }
            )

    with by_dimension.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "model_id", "dimension", "score", "max_score"],
            lineterminator="\n",
        )
        writer.writeheader()
        for review in reviews:
            for dimension, score in review["scores"].items():
                writer.writerow(
                    {
                        "id": review["id"],
                        "model_id": review["model_id"],
                        "dimension": dimension,
                        "score": score,
                        "max_score": DIM_MAX,
                    }
                )

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for review in reviews:
        grouped[review["model_id"]].append(review)
    with summary.open("w", encoding="utf-8", newline="") as f:
        fields = ["model_id", "items", "total_score", "average_score", "hard_fail_count"] + DIMENSIONS
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for model_id, rows in sorted(grouped.items()):
            row = {
                "model_id": model_id,
                "items": len(rows),
                "total_score": round(sum(review["total"] for review in rows), 2),
                "average_score": round(mean(review["total"] for review in rows), 3),
                "hard_fail_count": sum(1 for review in rows if review["hard_fail"]),
            }
            for dimension in DIMENSIONS:
                row[dimension] = round(mean(review["scores"][dimension] for review in rows), 3)
            writer.writerow(row)

    with review_list.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "model_id", "reason", "total_score", "comment"],
            lineterminator="\n",
        )
        writer.writeheader()
        for review in reviews:
            low_score = review["total"] < 7.0
            if review["hard_fail"] or low_score:
                writer.writerow(
                    {
                        "id": review["id"],
                        "model_id": review["model_id"],
                        "reason": "hard_fail" if review["hard_fail"] else "low_or_disputed_score",
                        "total_score": review["total"],
                        "comment": review["comment"],
                    }
                )


def write_report(out_dir: Path, reviews: list[dict[str, Any]], args: argparse.Namespace) -> None:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for review in reviews:
        grouped[review["model_id"]].append(review)
    lines = [
        "# Live Free-response Judge Report",
        "",
        f"This report scores live model free-response outputs with the fixed `{args.judge_model}` judge.",
        "",
        f"Bias note: {judge_bias_note(args.judge_model, sorted(grouped))}",
        "",
        "| Model | Items | Total | Average | Hard Fails |",
        "|---|---:|---:|---:|---:|",
    ]
    for model_id, rows in sorted(grouped.items()):
        lines.append(
            f"| {model_id} | {len(rows)} | {sum(review['total'] for review in rows):.2f} | "
            f"{mean(review['total'] for review in rows):.3f} | {sum(1 for review in rows if review['hard_fail'])} |"
        )
    lines.extend(
        [
            "",
            "Manual review queue includes hard-fail items and low/disputed-score items.",
            "",
            "Inputs:",
            f"- Benchmark: `{display_path(args.benchmark)}`",
            f"- Model outputs: `{display_path(args.outputs)}`",
            f"- Judge prompt: `{display_path(args.judge_prompt)}`",
            "",
        ]
    )
    (out_dir / "judge_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", default=str(ROOT / "data/benchmark.json"))
    parser.add_argument("--outputs", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--judge-model", default="gpt-5.6-sol")
    parser.add_argument("--judge-prompt", default=str(ROOT / "eval/prompts/free_response_judge_prompt.md"))
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--reuse-raw", action="store_true", help="Rebuild parsed artifacts from existing raw judge outputs without another model call.")
    args = parser.parse_args()

    started_at = datetime.now(timezone.utc)
    initial_dirty = working_tree_dirty()
    benchmark = Path(args.benchmark)
    outputs = Path(args.outputs)
    out_dir = Path(args.out_dir)
    raw_dir = out_dir / "raw_judge_outputs"
    existing_manifest_path = out_dir / "judge_manifest.json"
    existing_manifest = json.loads(existing_manifest_path.read_text(encoding="utf-8")) if existing_manifest_path.exists() else {}
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    items = load_free_response_items(benchmark)
    output_rows = load_outputs(outputs)
    by_model: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in output_rows:
        if row["id"] in items:
            by_model[row["model_id"]].append(row)
    if not by_model:
        raise SystemExit("No participating-model free-response rows found")
    if args.judge_model == "gpt-5.6-sol" and args.judge_model in by_model:
        raise SystemExit("gpt-5.6-sol is judge-only and must not appear in participating-model outputs")
    expected_ids = set(items)
    for model_id, rows in by_model.items():
        row_ids = [row["id"] for row in rows]
        missing = sorted(expected_ids - set(row_ids))
        duplicates = sorted({item_id for item_id in row_ids if row_ids.count(item_id) > 1})
        if missing or duplicates or len(row_ids) != len(expected_ids):
            raise SystemExit(f"{model_id}: incomplete free-response inputs; missing={missing}, duplicates={duplicates}")

    all_reviews: list[dict[str, Any]] = []
    model_status: dict[str, dict[str, Any]] = {}
    for model_id, rows in sorted(by_model.items()):
        rows = sorted(rows, key=lambda row: list(items).index(row["id"]))
        payload_rows = [item_payload(items[row["id"]], row.get("answer", "")) for row in rows]
        prompt = build_prompt(Path(args.judge_prompt), model_id, payload_rows)
        status = {"rows": len(rows), "reviews": 0, "errors": 0, "elapsed_seconds": None}
        try:
            raw_path = raw_dir / f"{model_id.replace('/', '_')}.txt"
            if args.reuse_raw:
                if not raw_path.exists():
                    raise RuntimeError(f"Missing raw judge output for {model_id}: {raw_path}")
                raw_text = raw_path.read_text(encoding="utf-8")
                elapsed = existing_manifest.get("model_status", {}).get(model_id, {}).get("elapsed_seconds")
            else:
                raw_text, elapsed = call_codex(args.judge_model, prompt, args.timeout)
                raw_path.write_text(raw_text, encoding="utf-8")
            reviews = parse_reviews(raw_text, [row["id"] for row in rows], model_id)
            reviews = [no_rescue_review(review, row.get("answer", "")) for review, row in zip(reviews, rows)]
            all_reviews.extend(reviews)
            status["reviews"] = len(reviews)
            status["elapsed_seconds"] = elapsed
        except Exception as exc:
            status["errors"] = 1
            status["error"] = str(exc)
        model_status[model_id] = status

    (out_dir / "judge_reviews.json").write_text(json.dumps(all_reviews, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csvs(out_dir, all_reviews, items)
    write_report(out_dir, all_reviews, args)
    finished_at = datetime.now(timezone.utc)
    manifest = {
        "run_id": existing_manifest.get("run_id", f"free-response-judge-{started_at.strftime('%Y%m%dT%H%M%SZ')}") if args.reuse_raw else f"free-response-judge-{started_at.strftime('%Y%m%dT%H%M%SZ')}",
        "created_at": existing_manifest.get("created_at", started_at.isoformat()) if args.reuse_raw else started_at.isoformat(),
        "finished_at": existing_manifest.get("finished_at", finished_at.isoformat()) if args.reuse_raw else finished_at.isoformat(),
        "benchmark_version": "mini-benchmark-0.5.0",
        "task_file": display_path(benchmark),
        "task_set_hash": sha256_file(benchmark),
        "model_outputs": display_path(outputs),
        "model_outputs_hash": sha256_file(outputs),
        "judge_model": args.judge_model,
        "judge_prompt_file": display_path(args.judge_prompt),
        "judge_prompt_hash": sha256_file(args.judge_prompt),
        "temperature": 0,
        "internet_access": False,
        "tool_assistance": False,
        "sampling": "single judge pass per model batch; no retry or manual answer repair",
        "bias_note": judge_bias_note(args.judge_model, sorted(by_model)),
        "model_status": model_status,
        "raw_output_dir": display_path(raw_dir),
        "code_commit": existing_manifest.get("code_commit", current_commit()) if args.reuse_raw else current_commit(),
        "working_tree_dirty": existing_manifest.get("working_tree_dirty", initial_dirty) if args.reuse_raw else initial_dirty,
        "artifact_rebuilt_from_raw": args.reuse_raw,
        "artifact_generation_working_tree_dirty": initial_dirty,
    }
    (out_dir / "judge_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    failed_models = [model_id for model_id, status in model_status.items() if status["errors"]]
    if failed_models:
        raise SystemExit(f"Free-response judge failed for: {failed_models}")
    print(f"Wrote live free-response judge artifacts to {display_path(out_dir)}")


if __name__ == "__main__":
    main()
