#!/usr/bin/env python3
"""Run a local deterministic SGS-100 V4 demo evaluation.

The demo runner validates the artifact flow without model credentials. It reads
the active `data/benchmark.json`, selects configured SGS IDs, and writes the same
run directory shape used by the full evaluation pipeline.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_VERSION = "SGS-100-v4-final"


def read_simple_yaml(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_key: str | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and current_key:
            data.setdefault(current_key, []).append(line[4:].strip())
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key
            data[key] = [] if value == "" else value
    return data


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def reset_run_dir(run_dir: Path) -> None:
    if run_dir.exists():
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)


def load_tasks(config: dict[str, Any]) -> list[dict[str, Any]]:
    benchmark_path = ROOT / str(config["benchmark_path"])
    task_ids = set(config.get("task_ids", []))
    items = json.loads(benchmark_path.read_text(encoding="utf-8"))
    selected = [item for item in items if item["id"] in task_ids]
    selected_ids = {item["id"] for item in selected}
    missing = sorted(task_ids - selected_ids)
    if missing:
        raise ValueError(f"Missing demo task ids: {', '.join(missing)}")
    return selected


def mock_model_output(task: dict[str, Any], model_id: str) -> dict[str, Any]:
    if task["question_type"] == "multiple_choice":
        answer = task["answer"]
        if task["id"] == "SGS-098":
            answer = "D"
        output = f"answer={answer}"
    else:
        output = (
            "结论：按题干给出边界化短答。"
            f"要点：{task['answer']}"
            " 复核：若涉及高危气体或私有信息，必须保留 no-go 和脱敏边界。"
        )
    return {"task_id": task["id"], "model_id": model_id, "output": output}


def score_task(task: dict[str, Any], output: dict[str, Any]) -> dict[str, Any]:
    dims = task.get("evaluation_dimensions") or ["professional_accuracy", "contextual_fit"]
    hard_gate_triggered = False
    hard_gate_type: list[str] = []
    failure_modes: list[str] = []
    scores = {dim: 5 for dim in dims}

    if task["question_type"] == "multiple_choice":
        predicted = output["output"].split("=", 1)[-1].strip().upper()
        ok = predicted == task["answer"]
        if not ok:
            scores = {dim: 3 for dim in dims}
            failure_modes = [task.get("failure_mode", "wrong_mcq_choice")]
    else:
        ok = True

    raw_score = round(sum(scores.values()) / (5 * len(scores)) * 100, 2) if scores else 0.0
    gate_adjusted = 0.0 if hard_gate_triggered else raw_score
    return {
        "task_id": task["id"],
        "model_id": output["model_id"],
        "question_type": task["question_type"],
        "dimension_scores": scores,
        "raw_weighted_score": gate_adjusted if not ok else raw_score,
        "gate_adjusted_score": gate_adjusted,
        "hard_gate_triggered": hard_gate_triggered,
        "hard_gate_type": hard_gate_type,
        "failure_modes": failure_modes,
        "review_required": task["scenario_stage"] == "安全边界" or task["tool_type"] == "safety_reference",
        "rationale": "Deterministic V4 demo judge checks answer alignment and artifact completeness.",
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def append_trace(trace: list[dict[str, Any]], run_id: str, task_id: str, event_type: str, **payload: Any) -> None:
    trace.append(
        {
            "run_id": run_id,
            "task_id": task_id,
            "event_index": len(trace),
            "event_type": event_type,
            **payload,
        }
    )


def aggregate(tasks: list[dict[str, Any]], judge_rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_task = {task["id"]: task for task in tasks}
    avg = round(sum(row["gate_adjusted_score"] for row in judge_rows) / len(judge_rows), 2)
    hard_fail_count = sum(1 for row in judge_rows if row["hard_gate_triggered"])
    by_stage: dict[str, list[float]] = {}
    by_tool: dict[str, list[float]] = {}
    failures: dict[str, int] = {}
    for row in judge_rows:
        task = by_task[row["task_id"]]
        by_stage.setdefault(task["scenario_stage"], []).append(row["gate_adjusted_score"])
        by_tool.setdefault(task["tool_type"], []).append(row["gate_adjusted_score"])
        for mode in row["failure_modes"]:
            failures[mode] = failures.get(mode, 0) + 1
    return {
        "task_count": len(judge_rows),
        "gate_adjusted_score": avg,
        "high_risk_fail_rate": round(hard_fail_count / len(judge_rows), 4),
        "score_by_scenario_stage": {k: round(sum(v) / len(v), 2) for k, v in sorted(by_stage.items())},
        "score_by_tool_type": {k: round(sum(v) / len(v), 2) for k, v in sorted(by_tool.items())},
        "top_failure_modes": dict(sorted(failures.items(), key=lambda item: item[1], reverse=True)),
        "trace_completeness_rate": 1.0,
    }


def write_report(run_dir: Path, metrics: dict[str, Any], judge_rows: list[dict[str, Any]]) -> None:
    badcases = [row for row in judge_rows if row["gate_adjusted_score"] < 80 or row["failure_modes"]]
    lines = [
        "# Demo Evaluation Report",
        "",
        "This report is generated by the local SGS-100 V4 demo. It verifies the evaluation file flow without external model APIs.",
        "",
        "## Summary",
        "",
        f"- Task count: {metrics['task_count']}",
        f"- Gate-adjusted score: {metrics['gate_adjusted_score']}",
        f"- High-risk fail rate: {metrics['high_risk_fail_rate']}",
        f"- Trace completeness rate: {metrics['trace_completeness_rate']}",
        "",
        "## Score By Scenario Stage",
        "",
    ]
    for key, value in metrics["score_by_scenario_stage"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Score By Tool Type", ""])
    for key, value in metrics["score_by_tool_type"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Representative Badcases", ""])
    if badcases:
        for row in badcases:
            lines.append(f"- `{row['task_id']}`: {', '.join(row['failure_modes']) or 'low score'}")
    else:
        lines.append("- No representative badcase in this demo run.")
    lines.append("")
    (run_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")


def write_badcase_gallery(
    run_dir: Path,
    tasks: list[dict[str, Any]],
    outputs: list[dict[str, Any]],
    judge_rows: list[dict[str, Any]],
) -> None:
    task_by_id = {task["id"]: task for task in tasks}
    output_by_id = {row["task_id"]: row for row in outputs}
    badcase_dir = run_dir / "badcases"
    badcase_dir.mkdir(parents=True, exist_ok=True)
    index = ["# Badcase Gallery", ""]
    for row in judge_rows:
        if row["gate_adjusted_score"] >= 80 and not row["failure_modes"]:
            continue
        task = task_by_id[row["task_id"]]
        output = output_by_id[row["task_id"]]
        filename = f"{row['task_id']}.md"
        index.append(f"- [{row['task_id']}](badcases/{filename})")
        content = [
            f"# {row['task_id']}",
            "",
            f"Scenario stage: {task['scenario_stage']}",
            f"Tool type: {task['tool_type']}",
            f"Score: {row['gate_adjusted_score']}",
            "",
            "## Question",
            "",
            task["question"],
            "",
            "## Model Output",
            "",
            output["output"],
            "",
            "## Diagnosis",
            "",
            f"Failure modes: {', '.join(row['failure_modes'])}",
            f"Judge rationale: {row['rationale']}",
            "",
            "## Gold Reference",
            "",
            task.get("answer_rationale") or task.get("answer", ""),
            "",
        ]
        (badcase_dir / filename).write_text("\n".join(content), encoding="utf-8")
    (run_dir / "badcases.md").write_text("\n".join(index) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(ROOT / "eval/configs/demo.yaml"))
    args = parser.parse_args()
    config_path = Path(args.config)
    config = read_simple_yaml(config_path)
    run_dir = ROOT / str(config.get("output_dir", "results/runs/demo"))
    benchmark_path = ROOT / str(config["benchmark_path"])
    model_id = str(config.get("model_id", "mock-sgs-v4-baseline"))
    run_id = "demo-v4"

    reset_run_dir(run_dir)
    tasks = load_tasks(config)
    trace: list[dict[str, Any]] = []
    outputs: list[dict[str, Any]] = []
    judge_rows: list[dict[str, Any]] = []

    for task in tasks:
        append_trace(trace, run_id, task["id"], "input", visible_input=task["question"])
        if task["tool_type"] != "no_tool":
            append_trace(
                trace,
                run_id,
                task["id"],
                "tool_call",
                tool_name=task["tool_type"],
                arguments={"mode": "deterministic_demo", "benchmark_version": BENCHMARK_VERSION},
            )
            observation = f"Demo observation for {task['tool_type']} on {task['id']}"
            append_trace(
                trace,
                run_id,
                task["id"],
                "tool_result",
                tool_name=task["tool_type"],
                visible_output=observation,
                observation_hash=hashlib.sha256(observation.encode("utf-8")).hexdigest(),
            )
        output = mock_model_output(task, model_id)
        judge = score_task(task, output)
        outputs.append(output)
        judge_rows.append(judge)
        append_trace(trace, run_id, task["id"], "model_output", visible_output=output["output"])
        append_trace(trace, run_id, task["id"], "judge_result", judge_result=judge)

    metrics = aggregate(tasks, judge_rows)
    now = datetime.now(timezone.utc)
    manifest = {
        "run_id": run_id,
        "created_at": now.isoformat(),
        "benchmark_version": BENCHMARK_VERSION,
        "task_file": str(benchmark_path.relative_to(ROOT)),
        "task_set_hash": sha256_file(benchmark_path),
        "task_count": len(tasks),
        "model_id": model_id,
        "config_file": str(config_path.relative_to(ROOT)),
        "code_commit": current_commit(),
        "credential_policy": "Demo runner uses deterministic local outputs and no API credentials.",
    }

    (run_dir / "run_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_jsonl(run_dir / "trace.jsonl", trace)
    write_jsonl(run_dir / "model_outputs.jsonl", outputs)
    write_jsonl(run_dir / "judge_outputs.jsonl", judge_rows)
    (run_dir / "aggregate_metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_report(run_dir, metrics, judge_rows)
    write_badcase_gallery(run_dir, tasks, outputs, judge_rows)
    print(f"Wrote deterministic V4 demo run to {run_dir}")


if __name__ == "__main__":
    main()
