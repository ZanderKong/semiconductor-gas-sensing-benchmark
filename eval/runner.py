#!/usr/bin/env python3
"""Run a local, API-free V3 demo evaluation.

The demo runner uses deterministic mock outputs so the repository can be
validated without model credentials. It writes the same artifacts expected from
a real run: manifest, trace, model outputs, judge outputs, aggregate metrics,
report, and badcase notes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DIMENSION_WEIGHTS = {
    "instruction_following": 10,
    "professional_accuracy": 20,
    "contextual_research_judgment": 15,
    "evidence_grounding_uncertainty": 15,
    "actionable_research_plan": 15,
    "tool_use_quality": 10,
    "safety_compliance_boundary": 15,
}


def read_simple_yaml(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_key = None
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


def load_tasks(config: dict[str, Any]) -> list[dict[str, Any]]:
    benchmark_path = ROOT / str(config["benchmark_path"])
    task_ids = set(config.get("task_ids", []))
    items = json.loads(benchmark_path.read_text(encoding="utf-8"))
    selected = [item for item in items if item["task_id"] in task_ids]
    selected_ids = {item["task_id"] for item in selected}
    missing = sorted(task_ids - selected_ids)
    if missing:
        raise ValueError(f"Missing demo task ids: {', '.join(missing)}")
    return selected


def mock_model_output(task: dict[str, Any]) -> dict[str, Any]:
    expected = task.get("gold_response", {}).get("expected", "")
    if task["task_id"] == "V3-SC-014":
        # Intentional medium-quality answer for the demo badcase gallery.
        answer = (
            "可以继续做下一轮配方优化，因为三次循环都有响应。"
            "需要再观察恢复曲线，但当前结果已经说明材料方向有效。"
        )
    else:
        answer = (
            f"结论：{expected} "
            "依据：回答只使用题干和允许工具语境。"
            "边界：不把候选机理、检索趋势或计算结果直接写成确定实验结论。"
            "下一步：补充对照、记录关键元数据，并按安全和证据边界推进。"
        )
    return {
        "task_id": task["task_id"],
        "model_id": "mock-v4-baseline",
        "output": answer,
    }


def score_task(task: dict[str, Any], output: dict[str, Any]) -> dict[str, Any]:
    dims = task["target_dimensions"]
    hard_gate_triggered = False
    hard_gate_type: list[str] = []
    failure_modes: list[str] = []
    scores = {dim: 5 for dim in dims}

    if task["task_id"] == "V3-SC-014":
        scores = {dim: 3 for dim in dims}
        if "evidence_grounding_uncertainty" in scores:
            scores["evidence_grounding_uncertainty"] = 2
        if "contextual_research_judgment" in scores:
            scores["contextual_research_judgment"] = 2
        failure_modes = ["data_quality_trap", "premature_optimization"]

    enabled_weight = sum(DIMENSION_WEIGHTS[dim] for dim in scores)
    raw_score = 0.0
    for dim, score in scores.items():
        raw_score += (score / 5) * DIMENSION_WEIGHTS[dim]
    raw_score = round(raw_score / enabled_weight * 100, 2) if enabled_weight else 0.0
    gate_adjusted = 0.0 if hard_gate_triggered else raw_score

    return {
        "task_id": task["task_id"],
        "model_id": output["model_id"],
        "dimension_scores": scores,
        "raw_weighted_score": raw_score,
        "gate_adjusted_score": gate_adjusted,
        "hard_gate_triggered": hard_gate_triggered,
        "hard_gate_type": hard_gate_type,
        "failure_modes": failure_modes,
        "review_required": task["risk_level"] == "high" or bool(task["hard_gate_checks"]),
        "rationale": (
            "Mock judge compares the visible answer with task key points. "
            "Scores are deterministic for demo reproducibility."
        ),
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def aggregate(tasks: list[dict[str, Any]], judge_rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_task = {task["task_id"]: task for task in tasks}
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
        "This report is generated by the local mock V4 demo. It verifies the evaluation file flow without using external model APIs.",
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


def write_badcase_gallery(run_dir: Path, tasks: list[dict[str, Any]], outputs: list[dict[str, Any]], judge_rows: list[dict[str, Any]]) -> None:
    task_by_id = {task["task_id"]: task for task in tasks}
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
            "## Prompt",
            "",
            task["prompt"],
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
            task.get("gold_response", {}).get("expected", ""),
            "",
        ]
        (badcase_dir / filename).write_text("\n".join(content), encoding="utf-8")
    (run_dir / "badcases.md").write_text("\n".join(index) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(ROOT / "eval/configs/demo.yaml"))
    args = parser.parse_args()
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = ROOT / config_path
    config = read_simple_yaml(config_path)
    run_dir = ROOT / str(config["output_dir"])
    run_dir.mkdir(parents=True, exist_ok=True)

    tasks = load_tasks(config)
    benchmark_path = ROOT / str(config["benchmark_path"])
    schema_path = ROOT / str(config["schema_path"])
    model_id = str(config.get("model_id", "mock-v4-baseline"))

    manifest = {
        "run_id": "demo",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "benchmark_version": "v4-demo",
        "task_file": str(benchmark_path.relative_to(ROOT)),
        "task_set_hash": sha256_file(benchmark_path),
        "schema_hash": sha256_file(schema_path),
        "model_provider": "local_mock",
        "model_id": model_id,
        "temperature": 0,
        "top_p": 1,
        "prompt_hash": "local-demo",
        "tool_schema_hash": "no-live-tools",
        "retrieval_corpus_hash": "",
        "judge_protocol_version": "v3",
        "judge_model": "deterministic_mock_judge",
        "code_commit": current_commit(),
    }

    outputs = []
    trace = []
    judge_rows = []
    for index, task in enumerate(tasks):
        output = mock_model_output(task)
        output["model_id"] = model_id
        judge = score_task(task, output)
        judge["model_id"] = model_id
        outputs.append(output)
        judge_rows.append(judge)
        trace.append({"task_id": task["task_id"], "event_index": index * 3, "event_type": "input", "visible_input": task["prompt"]})
        if task["tool_mode"] == "tool_enabled":
            trace.append({
                "task_id": task["task_id"],
                "event_index": index * 3 + 1,
                "event_type": "tool_call",
                "tool_name": task["tool_type"],
                "arguments": {"mode": "mock", "expected_behavior": task["expected_tool_behavior"]},
                "observation_hash": hashlib.sha256(task["expected_tool_behavior"].encode("utf-8")).hexdigest(),
            })
        trace.append({"task_id": task["task_id"], "event_index": index * 3 + 2, "event_type": "model_output", "visible_output": output["output"]})
        trace.append({"task_id": task["task_id"], "event_index": index * 3 + 3, "event_type": "judge_result", "judge_result": judge})

    metrics = aggregate(tasks, judge_rows)
    (run_dir / "run_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    write_jsonl(run_dir / "model_outputs.jsonl", outputs)
    write_jsonl(run_dir / "judge_outputs.jsonl", judge_rows)
    write_jsonl(run_dir / "trace.jsonl", trace)
    (run_dir / "aggregate_metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(run_dir, metrics, judge_rows)
    write_badcase_gallery(run_dir, tasks, outputs, judge_rows)
    print(f"Demo run written to {run_dir}")


if __name__ == "__main__":
    main()
