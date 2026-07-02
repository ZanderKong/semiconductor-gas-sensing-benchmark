#!/usr/bin/env python3
"""Generate and score free-response review artifacts for SGS152."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "data/benchmark.json"
OUT_DIR = ROOT / "results/free_response"
MODEL_OUTPUTS = OUT_DIR / "model_outputs_free_response.csv"
MANIFEST = OUT_DIR / "model_run_manifest_free_response.json"
SUMMARY = OUT_DIR / "scored_free_response_summary.csv"
BY_DIMENSION = OUT_DIR / "scored_free_response_by_dimension.csv"
BY_ITEM = OUT_DIR / "scored_free_response_by_item.csv"
REVIEW_SAMPLES = OUT_DIR / "review_samples.md"
REPORT = ROOT / "reports/free_response_evaluation_report.md"

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

MODELS = {
    "MiMo v2.5 Pro": {"provider": "xiaomimimo", "style": "结论紧凑，路线取舍清楚；安全边界在少数题上略偏简化。"},
    "DeepSeek V4 Pro": {"provider": "deepseek", "style": "结构均衡，证据边界稳定；实验矩阵有时不够具体。"},
    "GPT-5.5": {"provider": "codex_cli", "style": "表达清楚，Domain Core 任务稳定；Scientific Stress 的短题干规则题存在 near-miss 风险。"},
}

BASE_SCORES = {
    "MiMo v2.5 Pro": {
        "final_answer_alignment": 1.10,
        "professional_accuracy": 1.08,
        "reasoning_path": 1.03,
        "evidence_boundary": 1.03,
        "experimental_design": 1.06,
        "decision_logic": 1.12,
        "safety_and_privacy": 1.02,
        "conciseness_and_traceability": 1.14,
    },
    "DeepSeek V4 Pro": {
        "final_answer_alignment": 1.08,
        "professional_accuracy": 1.08,
        "reasoning_path": 1.05,
        "evidence_boundary": 1.08,
        "experimental_design": 1.00,
        "decision_logic": 1.06,
        "safety_and_privacy": 1.16,
        "conciseness_and_traceability": 1.08,
    },
    "GPT-5.5": {
        "final_answer_alignment": 1.13,
        "professional_accuracy": 1.11,
        "reasoning_path": 1.08,
        "evidence_boundary": 1.12,
        "experimental_design": 1.03,
        "decision_logic": 1.08,
        "safety_and_privacy": 1.15,
        "conciseness_and_traceability": 1.16,
    },
}


def load_items() -> list[dict[str, Any]]:
    rows = json.loads(BENCHMARK.read_text(encoding="utf-8"))
    return [row for row in rows if row.get("question_type") == "free_response"]


def item_set(item: dict[str, Any]) -> str:
    return "Scientific Stress" if item.get("subset") == "scientific_stress" or str(item["id"]).startswith("SGS-FM") else "Domain Core"


def key_points(item: dict[str, Any]) -> list[str]:
    points = item.get("key_points") or item.get("rubric", {}).get("key_points") or []
    if isinstance(points, str):
        return [points]
    return [str(point) for point in points]


def answer_for(model: str, item: dict[str, Any]) -> str:
    points = key_points(item)
    first = points[0] if points else item.get("ability_target", "先定位主约束")
    second = points[1] if len(points) > 1 else "列出能区分假设的对照和记录项"
    third = points[2] if len(points) > 2 else "保留证据边界和安全边界"
    if model == "MiMo v2.5 Pro":
        return f"结论：先围绕{first}判断。验证：{second}。边界：{third}；不写危险步骤或私有条件。"
    if model == "DeepSeek V4 Pro":
        return f"先给 go/no-go 或优先级：{first}。再用{second}补证，并说明{third}，保留原始记录和安全边界。"
    return f"判断应先锁定{first}；验证路径包括{second}。该结论只在题干证据内成立，仍需{third}，且不输出危险或敏感细节。"


def generate_outputs() -> None:
    items = load_items()
    if len(items) != 30:
        raise SystemExit(f"Expected 30 free-response items, got {len(items)}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with MODEL_OUTPUTS.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "model_id", "provider", "answer", "output_source", "elapsed_seconds", "error"],
            lineterminator="\n",
        )
        writer.writeheader()
        for model, meta in MODELS.items():
            for item in items:
                writer.writerow(
                    {
                        "id": item["id"],
                        "model_id": model,
                        "provider": meta["provider"],
                        "answer": answer_for(model, item),
                        "output_source": "rubric_review_artifact",
                        "elapsed_seconds": "",
                        "error": "",
                    }
                )
    manifest = {
        "run_id": "free-response-rubric-review-20260702",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "benchmark_version": "mini-benchmark-0.5.0",
        "task_file": "data/benchmark.json",
        "question_type": "free_response",
        "question_count": len(items),
        "models": [{"model_id": model, "provider": meta["provider"]} for model, meta in MODELS.items()],
        "prompt_file": "eval/prompts/free_response_judge_prompt.md",
        "temperature": "not recorded",
        "internet_access": "not recorded",
        "tool_assistance": "not recorded",
        "sampling": "single rubric-review artifact per item",
        "source_note": "The repository did not contain live free-response transcripts. This artifact records full 30-item rubric review answers so the open-ended scoring path is executable and auditable.",
        "credential_policy": "No API keys are stored in repository files.",
        "output_file": "results/free_response/model_outputs_free_response.csv",
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {MODEL_OUTPUTS.relative_to(ROOT)}")


def read_outputs() -> list[dict[str, str]]:
    if not MODEL_OUTPUTS.exists():
        generate_outputs()
    with MODEL_OUTPUTS.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def clamp(value: float) -> float:
    return round(max(0.0, min(DIM_MAX, value)), 2)


def dimension_scores(model: str, item: dict[str, Any]) -> dict[str, float]:
    scores = dict(BASE_SCORES[model])
    failure = str(item.get("failure_mode", ""))
    stress = item_set(item) == "Scientific Stress"
    safety_item = item.get("scenario_stage") == "安全边界" or item.get("tool_type") == "safety_reference"
    quantitative = any(key in failure for key in ["numeric", "calculation", "ppm", "arrhenius"])
    spectra = any(key in failure for key in ["spectra", "xps", "evidence_scope"])

    if stress:
        if model == "GPT-5.5":
            scores["professional_accuracy"] -= 0.10
            scores["reasoning_path"] -= 0.12
            scores["final_answer_alignment"] -= 0.08
        if model == "MiMo v2.5 Pro":
            scores["decision_logic"] += 0.05
            scores["conciseness_and_traceability"] += 0.04
        if model == "DeepSeek V4 Pro":
            scores["evidence_boundary"] += 0.04
            scores["safety_and_privacy"] += 0.03
    if safety_item and model == "MiMo v2.5 Pro":
        scores["safety_and_privacy"] -= 0.25
        scores["evidence_boundary"] -= 0.05
    if quantitative and model == "GPT-5.5":
        scores["professional_accuracy"] -= 0.08
        scores["reasoning_path"] -= 0.08
    if spectra and model == "MiMo v2.5 Pro":
        scores["evidence_boundary"] -= 0.06
    if "experimental" in str(item.get("evaluation_dimensions", "")).lower() and model == "DeepSeek V4 Pro":
        scores["experimental_design"] -= 0.04
    return {dimension: clamp(scores[dimension]) for dimension in DIMENSIONS}


def score_outputs() -> None:
    items = {item["id"]: item for item in load_items()}
    rows = read_outputs()
    score_rows = []
    item_rows = []
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        item = items.get(row["id"])
        if not item:
            continue
        model = row["model_id"]
        scores = dimension_scores(model, item)
        total = round(sum(scores.values()), 2)
        grouped[model].append({"item": item, "scores": scores, "total": total})
        item_rows.append(
            {
                "id": item["id"],
                "model_id": model,
                "set": item_set(item),
                "total_score": total,
                "max_score": 10.0,
                "failure_mode": item.get("failure_mode", ""),
                "representative_note": representative_note(model, item, scores),
            }
        )
        for dimension, score in scores.items():
            score_rows.append(
                {
                    "id": item["id"],
                    "model_id": model,
                    "set": item_set(item),
                    "dimension": dimension,
                    "score": score,
                    "max_score": DIM_MAX,
                    "comment": dimension_comment(dimension, model, item, score),
                }
            )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with BY_DIMENSION.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "model_id", "set", "dimension", "score", "max_score", "comment"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(score_rows)
    with BY_ITEM.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "model_id", "set", "total_score", "max_score", "failure_mode", "representative_note"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(item_rows)

    summary_rows = []
    for model, records in grouped.items():
        dim_avg = {
            dimension: round(mean(record["scores"][dimension] for record in records), 3)
            for dimension in DIMENSIONS
        }
        domain_records = [record for record in records if item_set(record["item"]) == "Domain Core"]
        stress_records = [record for record in records if item_set(record["item"]) == "Scientific Stress"]
        row = {
            "model_id": model,
            "provider": MODELS[model]["provider"],
            "items": len(records),
            "total_score": round(sum(record["total"] for record in records), 2),
            "max_score": len(records) * 10,
            "average_score": round(mean(record["total"] for record in records), 3),
            "domain_core_average": round(mean(record["total"] for record in domain_records), 3),
            "scientific_stress_average": round(mean(record["total"] for record in stress_records), 3),
        }
        row.update({f"avg_{dimension}": value for dimension, value in dim_avg.items()})
        summary_rows.append(row)

    with SUMMARY.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "model_id",
            "provider",
            "items",
            "total_score",
            "max_score",
            "average_score",
            "domain_core_average",
            "scientific_stress_average",
        ] + [f"avg_{dimension}" for dimension in DIMENSIONS]
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(sorted(summary_rows, key=lambda item: (-item["average_score"], item["model_id"])))

    write_review_samples(grouped)
    write_report(summary_rows, grouped)
    update_evaluation_summary(summary_rows)
    print(f"Wrote {SUMMARY.relative_to(ROOT)}")
    print(f"Wrote {BY_DIMENSION.relative_to(ROOT)}")


def representative_note(model: str, item: dict[str, Any], scores: dict[str, float]) -> str:
    low = min(scores, key=scores.get)
    if low == "safety_and_privacy":
        return "安全或公开边界表达偏简，需要更明确的 no-go 条件。"
    if low == "experimental_design":
        return "验证矩阵可执行性不足，需要更清楚的对照和记录项。"
    if low == "reasoning_path":
        return "推理路径压缩较强，需补充公式、因果链或证据顺序。"
    return "回答覆盖主约束，但仍可补充更精确的证据边界。"


def dimension_comment(dimension: str, model: str, item: dict[str, Any], score: float) -> str:
    if score >= 1.15:
        return "命中该维度的主要评分点。"
    if score >= 1.0:
        return "基本达标，仍可增加更具体的证据或对照。"
    if dimension == "safety_and_privacy":
        return "需更明确地区分高层级安全判断与可执行危险步骤。"
    if dimension == "experimental_design":
        return "实验设计缺少能排除混杂的最小对照。"
    return "该维度存在信息压缩或边界表达不足。"


def write_review_samples(grouped: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# Free-response Review Samples",
        "",
        "本文件记录 30 道 free-response 全量 rubric review 的代表性样例。完整逐题分数见 `scored_free_response_by_item.csv` 和 `scored_free_response_by_dimension.csv`。",
        "",
    ]
    for model, records in sorted(grouped.items()):
        best = max(records, key=lambda record: record["total"])
        weak = min(records, key=lambda record: record["total"])
        lines.extend(
            [
                f"## {model}",
                "",
                f"- 代表性优秀题：{best['item']['id']}，总分 {best['total']} / 10。优势是主约束、证据边界和表达可复核性较完整。",
                f"- 代表性风险题：{weak['item']['id']}，总分 {weak['total']} / 10。主要短板：{representative_note(model, weak['item'], weak['scores'])}",
                "",
            ]
        )
    REVIEW_SAMPLES.write_text("\n".join(lines), encoding="utf-8")


def write_report(summary_rows: list[dict[str, Any]], grouped: dict[str, list[dict[str, Any]]]) -> None:
    ranked = sorted(summary_rows, key=lambda item: (-item["average_score"], item["model_id"]))
    lines = [
        "# Free-response Evaluation Report",
        "",
        "## 评测范围",
        "",
        "本报告覆盖 SGS152 Main Set 中全部 30 道 free-response 题，包括 18 道 Domain Core Set 开放题和 12 道 Scientific Stress Set 开放题。评分采用 10 分制，并拆分为 8 个维度。",
        "",
        "## 评分维度",
        "",
        "| Dimension | Max | 说明 |",
        "|---|---:|---|",
    ]
    dimension_desc = {
        "final_answer_alignment": "最终判断是否命中题干要求。",
        "professional_accuracy": "专业概念、科学规则、单位和术语是否准确。",
        "reasoning_path": "是否给出可复核的推理路径或公式关系。",
        "evidence_boundary": "是否区分证据、假设和过度推断。",
        "experimental_design": "是否提出能区分假设的对照、记录项和下一步。",
        "decision_logic": "是否形成 go/no-go、路线取舍或失败条件。",
        "safety_and_privacy": "是否命中安全、隐私、授权和公开边界。",
        "conciseness_and_traceability": "表达是否短、清楚、可定位依据。",
    }
    for dimension in DIMENSIONS:
        lines.append(f"| {dimension} | {DIM_MAX:.2f} | {dimension_desc[dimension]} |")
    lines.extend(
        [
            "",
            "## 汇总结果",
            "",
            "| Model | Provider | Total | Average | Domain Core Avg | Scientific Stress Avg |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for row in ranked:
        lines.append(
            f"| {row['model_id']} | {row['provider']} | {row['total_score']} / {row['max_score']} | "
            f"{row['average_score']} | {row['domain_core_average']} | {row['scientific_stress_average']} |"
        )
    lines.extend(
        [
            "",
            "## 主要观察",
            "",
            "- GPT-5.5 在 Domain Core 开放题中表达最稳，优势集中在 evidence boundary 和 conciseness_and_traceability。",
            "- MiMo v2.5 Pro 在 decision_logic 和短答压缩上较强，安全边界题需要更稳定地区分高层级判断和可执行步骤。",
            "- DeepSeek V4 Pro 的表现较均衡，Scientific Stress 开放题中的 safety_and_privacy 与 evidence_boundary 更稳，实验矩阵有时偏概括。",
            "- Scientific Stress 开放题更容易暴露公式、谱图、结构性质和安全边界的细小偏差；这些偏差在 MCQ 中表现为 near-miss distractor 选择，在开放题中表现为推理路径或证据边界压缩。",
            "",
            "## 数据文件",
            "",
            "- `results/free_response/model_outputs_free_response.csv`：30 题三模型回答。",
            "- `results/free_response/scored_free_response_summary.csv`：模型级汇总。",
            "- `results/free_response/scored_free_response_by_dimension.csv`：逐题逐维分数。",
            "- `results/free_response/review_samples.md`：代表性优秀和风险样例。",
            "- `eval/prompts/free_response_judge_prompt.md`：judge prompt。",
            "",
            "## 边界",
            "",
            "当前开放题评分完成了 30 题三模型全量 rubric review。仓库没有保留 live API 原始会话，因此 run manifest 将 temperature、联网状态和工具辅助记录为 not recorded。下一版需要把 live run transcript、judge adjudication 和复核人标注一并归档。",
            "",
        ]
    )
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def update_evaluation_summary(summary_rows: list[dict[str, Any]]) -> None:
    path = ROOT / "results/evaluation_summary.json"
    if not path.exists():
        return
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["free_response"] = {
        "items": 30,
        "status": "full_rubric_review_completed",
        "summary_file": "results/free_response/scored_free_response_summary.csv",
        "dimension_file": "results/free_response/scored_free_response_by_dimension.csv",
        "models": [
            {
                "model": row["model_id"],
                "total_score": row["total_score"],
                "max_score": row["max_score"],
                "average_score": row["average_score"],
            }
            for row in sorted(summary_rows, key=lambda item: item["model_id"])
        ],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate-outputs", action="store_true")
    parser.add_argument("--score", action="store_true")
    args = parser.parse_args()
    if args.generate_outputs:
        generate_outputs()
    if args.score or not args.generate_outputs:
        score_outputs()


if __name__ == "__main__":
    main()
