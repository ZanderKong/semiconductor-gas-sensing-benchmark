#!/usr/bin/env python3
"""Rebuild frozen outputs and compute the complete v0.6 diagnostic inventory."""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import shutil
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from raw_evidence import STAGES, read_csv, rebuild_all, write_csv


MODEL_DISPLAY = {
    "gpt-5.5": "GPT-5.5",
    "ep-20260703090429-qpmt7": "Seed-2.1",
    "deepseek-v4-pro": "DeepSeek V4 Pro",
    "mimo-v2.5-pro": "MiMo v2.5 Pro",
}


def load_items(path: Path, question_type: str = "multiple_choice") -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [row for row in payload if row.get("question_type") == question_type]


def rank(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda index: values[index])
    result = [0.0] * len(values)
    position = 0
    while position < len(order):
        end = position + 1
        while end < len(order) and values[order[end]] == values[order[position]]:
            end += 1
        average_rank = (position + 1 + end) / 2
        for index in order[position:end]:
            result[index] = average_rank
        position = end
    return result


def pearson(left: list[float], right: list[float]) -> float | None:
    if len(left) < 2:
        return None
    lmean, rmean = mean(left), mean(right)
    numerator = sum((x - lmean) * (y - rmean) for x, y in zip(left, right))
    denominator = math.sqrt(sum((x - lmean) ** 2 for x in left) * sum((y - rmean) ** 2 for y in right))
    return numerator / denominator if denominator else None


def percentile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    index = (len(ordered) - 1) * probability
    lower = math.floor(index)
    upper = math.ceil(index)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] * (upper - index) + ordered[upper] * (index - lower)


def stage_matrix(repo: Path, stage: str, task_file: str) -> tuple[list[dict[str, Any]], list[str], dict[tuple[str, str], int]]:
    tasks = load_items(repo / task_file)
    rows = read_csv(repo / STAGES[stage] / "model_outputs.csv")
    models = list(dict.fromkeys(row["model_id"] for row in rows))
    gold = {row["id"]: str(row["answer"]).strip().upper() for row in tasks}
    correct = {
        (row["id"], row["model_id"]): int(row["answer"].strip().upper() == gold[row["id"]])
        for row in rows
    }
    return tasks, models, correct


def compute(repo: Path, output: Path, bootstrap_samples: int = 20000) -> dict[str, Any]:
    output.mkdir(parents=True, exist_ok=True)
    stage_specs = {
        "sgs152_mcq": "data/benchmark.json",
        "robustness": "data/benchmark_sgs100_robustness.json",
        "hard50": "data/benchmark_sgs_hard50.json",
    }
    stages: dict[str, tuple[list[dict[str, Any]], list[str], dict[tuple[str, str], int]]] = {
        name: stage_matrix(repo, name, task_file) for name, task_file in stage_specs.items()
    }
    main_tasks, models, main_correct = stages["sgs152_mcq"]

    difficulty_rows: list[dict[str, Any]] = []
    for item in main_tasks:
        count = sum(main_correct[(item["id"], model)] for model in models)
        difficulty_rows.append(
            {
                "item_id": item["id"], "domain": item.get("domain", ""),
                "scenario_stage": item.get("scenario_stage", ""), "correct_models": count,
                "models": len(models), "proportion_correct": round(count / len(models), 4),
                "saturation_class": "all_correct" if count == len(models) else "all_wrong" if count == 0 else "discriminating",
            }
        )
    write_csv(
        output / "mcq_item_difficulty.csv", difficulty_rows,
        ["item_id", "domain", "scenario_stage", "correct_models", "models", "proportion_correct", "saturation_class"],
    )

    disagreement_rows: list[dict[str, Any]] = []
    for stage, (tasks, stage_models, correct) in stages.items():
        raw_rows = read_csv(repo / STAGES[stage] / "model_outputs.csv")
        answers = {(row["id"], row["model_id"]): row["answer"] for row in raw_rows}
        for index, left in enumerate(stage_models):
            for right in stage_models[index + 1 :]:
                answer_disagree = sum(answers[(task["id"], left)] != answers[(task["id"], right)] for task in tasks)
                correctness_disagree = sum(correct[(task["id"], left)] != correct[(task["id"], right)] for task in tasks)
                disagreement_rows.append(
                    {"set": stage, "model_a": left, "model_b": right, "items": len(tasks),
                     "answer_disagreement_count": answer_disagree,
                     "answer_disagreement_rate": round(answer_disagree / len(tasks), 4),
                     "correctness_disagreement_count": correctness_disagree,
                     "correctness_disagreement_rate": round(correctness_disagree / len(tasks), 4)}
                )
    write_csv(
        output / "model_disagreement_matrix.csv", disagreement_rows,
        ["set", "model_a", "model_b", "items", "answer_disagreement_count", "answer_disagreement_rate", "correctness_disagreement_count", "correctness_disagreement_rate"],
    )

    scores_by_set: dict[str, dict[str, float]] = {}
    score_rows: list[dict[str, Any]] = []
    for stage, (tasks, stage_models, correct) in stages.items():
        scores_by_set[stage] = {}
        for model in stage_models:
            correct_count = sum(correct[(task["id"], model)] for task in tasks)
            accuracy = correct_count / len(tasks)
            scores_by_set[stage][model] = accuracy
            score_rows.append(
                {"set": stage, "model_id": model, "model_display": MODEL_DISPLAY[model],
                 "items": len(tasks), "correct": correct_count, "accuracy": round(accuracy, 6)}
            )
    write_csv(output / "model_set_scores.csv", score_rows, ["set", "model_id", "model_display", "items", "correct", "accuracy"])

    full_order = sorted(models, key=lambda model: (-scores_by_set["sgs152_mcq"][model], model))
    loo_rows: list[dict[str, Any]] = []
    for item in main_tasks:
        remaining = {
            model: (sum(main_correct[(other["id"], model)] for other in main_tasks if other["id"] != item["id"]) / (len(main_tasks) - 1))
            for model in models
        }
        order = sorted(models, key=lambda model: (-remaining[model], model))
        loo_rows.append(
            {"removed_item_id": item["id"], "full_ranking": " > ".join(full_order),
             "leave_one_out_ranking": " > ".join(order), "ranking_changed": order != full_order,
             "top_model_changed": order[0] != full_order[0]}
        )
    write_csv(output / "leave_one_item_out_ranking.csv", loo_rows, ["removed_item_id", "full_ranking", "leave_one_out_ranking", "ranking_changed", "top_model_changed"])

    rng = random.Random(20260713)
    sampled_scores: dict[str, list[float]] = {model: [] for model in models}
    first_counts = {model: 0 for model in models}
    task_ids = [item["id"] for item in main_tasks]
    for _ in range(bootstrap_samples):
        sampled = [task_ids[rng.randrange(len(task_ids))] for _ in task_ids]
        scores = {model: mean(main_correct[(item_id, model)] for item_id in sampled) for model in models}
        for model, value in scores.items():
            sampled_scores[model].append(value)
        best = max(scores.values())
        leaders = [model for model, value in scores.items() if value == best]
        for model in leaders:
            first_counts[model] += 1 / len(leaders)
    bootstrap_rows = [
        {"model_id": model, "model_display": MODEL_DISPLAY[model], "samples": bootstrap_samples,
         "mean_accuracy": round(mean(sampled_scores[model]), 6),
         "ci95_low": round(percentile(sampled_scores[model], 0.025), 6),
         "ci95_high": round(percentile(sampled_scores[model], 0.975), 6),
         "first_place_probability_ties_split": round(first_counts[model] / bootstrap_samples, 6)}
        for model in models
    ]
    write_csv(output / "bootstrap_rank_stability.csv", bootstrap_rows, ["model_id", "model_display", "samples", "mean_accuracy", "ci95_low", "ci95_high", "first_place_probability_ties_split"])

    group_members: dict[str, list[str]] = defaultdict(list)
    for item in main_tasks:
        group = item.get("consistency_group_id") or item["id"]
        group_members[group].append(item["id"])
    weighted_rows: list[dict[str, Any]] = []
    for model in models:
        group_scores = [mean(main_correct[(item_id, model)] for item_id in members) for members in group_members.values()]
        weighted_rows.append(
            {"model_id": model, "model_display": MODEL_DISPLAY[model],
             "groups": len(group_scores), "group_equal_weight_accuracy": round(mean(group_scores), 6),
             "ordinary_item_accuracy": round(scores_by_set["sgs152_mcq"][model], 6)}
        )
    write_csv(output / "same_source_group_weighting.csv", weighted_rows, ["model_id", "model_display", "groups", "group_equal_weight_accuracy", "ordinary_item_accuracy"])

    reviewed = {row["model_id"]: float(row["v0_6_official_average"]) for row in read_csv(repo / "review/v0.6.0/04_free_response_adjudication/official_free_response_summary.csv")}
    correlation_rows: list[dict[str, Any]] = []
    for label, left, right in [
        ("main_mcq_vs_official_free_response", scores_by_set["sgs152_mcq"], reviewed),
        ("main_mcq_vs_robustness", scores_by_set["sgs152_mcq"], scores_by_set["robustness"]),
        ("main_mcq_vs_hard50", scores_by_set["sgs152_mcq"], scores_by_set["hard50"]),
    ]:
        common = [model for model in models if model in left and model in right]
        x, y = [left[model] for model in common], [right[model] for model in common]
        correlation_rows.append(
            {"analysis": label, "n_models": len(common),
             "pearson": round(pearson(x, y), 6) if pearson(x, y) is not None else "",
             "spearman": round(pearson(rank(x), rank(y)), 6) if pearson(rank(x), rank(y)) is not None else "",
             "interpretation_limit": "descriptive only; n=4 models"}
        )
    write_csv(output / "cross_set_correlations.csv", correlation_rows, ["analysis", "n_models", "pearson", "spearman", "interpretation_limit"])

    summary = {
        "bootstrap_seed": 20260713,
        "bootstrap_samples": bootstrap_samples,
        "main_mcq_items": len(main_tasks),
        "models": models,
        "all_correct_items": sum(row["correct_models"] == len(models) for row in difficulty_rows),
        "discriminating_items": sum(row["saturation_class"] == "discriminating" for row in difficulty_rows),
        "leave_one_out_ranking_changes": sum(bool(row["ranking_changed"]) for row in loo_rows),
        "correlation_warning": "All cross-set correlations are descriptive because n=4.",
        "outputs": sorted(path.name for path in output.glob("*.csv")),
    }
    (output / "full_statistics_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--publish-dir", type=Path)
    parser.add_argument("--bootstrap-samples", type=int, default=20000)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    out = args.out.resolve()
    raw_checks = rebuild_all(repo, args.archive, out / "raw_rebuild")
    generated = out / "generated_statistics"
    summary = compute(repo, generated, args.bootstrap_samples)
    checks = {
        "raw_rebuild": raw_checks,
        "statistics": summary,
        "status": "pass",
    }
    (out / "raw_rebuild_checks.json").write_text(json.dumps(checks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.publish_dir:
        target = args.publish_dir.resolve()
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(generated, target)
    print(f"Computed {args.bootstrap_samples} bootstrap samples and {len(summary['outputs'])} CSV diagnostics.")


if __name__ == "__main__":
    main()
