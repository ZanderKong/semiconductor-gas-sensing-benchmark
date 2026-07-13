#!/usr/bin/env python3
"""Build a pending expert-review packet from canonical Judge artifacts."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "results/standard_20260703"
JUDGE = RUN / "free_response_judge"
MIN_PER_MODEL = 9


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    tasks = {row["id"]: row for row in json.loads((ROOT / "data/benchmark.json").read_text(encoding="utf-8"))}
    outputs = {(row["id"], row["model_id"]): row for row in read_csv(RUN / "sgs152_free_response/model_outputs.csv") if row.get("id")}
    reviews = json.loads((JUDGE / "judge_reviews.json").read_text(encoding="utf-8"))
    review_by_key = {(row["id"], row["model_id"]): row for row in reviews}
    queue = read_csv(JUDGE / "manual_review_queue.csv")
    queue_by_key = {(row["id"], row["model_id"]): row for row in queue}

    selected = set(queue_by_key)
    missing_keys = {key for key, row in outputs.items() if not row.get("answer", "").strip()}
    selected.update(missing_keys)

    reviews_by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for review in reviews:
        reviews_by_model[review["model_id"]].append(review)
    for model_id, model_reviews in reviews_by_model.items():
        current = sum(1 for _, selected_model in selected if selected_model == model_id)
        candidates = sorted(
            (review for review in model_reviews if (review["id"], model_id) not in selected),
            key=lambda review: (review["total"], review["id"]),
        )
        for review in candidates[: max(0, MIN_PER_MODEL - current)]:
            selected.add((review["id"], model_id))

    fields = [
        "id", "model_id", "review_source", "review_reason", "set", "domain", "subfield",
        "question", "expected_answer", "rubric_criteria_json", "model_answer", "model_error",
        "judge_total_score", "judge_max_score", "judge_hard_fail", "judge_hard_fail_reasons",
        "judge_comment", "dimension_scores_json", "expert_decision", "expert_total_score",
        "expert_dimension_overrides", "override_reason", "reviewer", "review_date", "affects_summary",
    ]
    packet: list[dict[str, Any]] = []
    task_order = {task_id: index for index, task_id in enumerate(tasks)}
    for key in sorted(selected, key=lambda item: (item[1], task_order[item[0]])):
        task_id, model_id = key
        task = tasks[task_id]
        output = outputs[key]
        review = review_by_key[key]
        queued = queue_by_key.get(key)
        if key in missing_keys:
            source, reason = "no_rescue_policy", "missing_answer_kept_zero"
        elif queued:
            source, reason = "manual_review_queue", queued["reason"]
        else:
            source, reason = "deterministic_risk_spot_check", "lowest_remaining_score_to_reach_30pct"
        packet.append(
            {
                "id": task_id,
                "model_id": model_id,
                "review_source": source,
                "review_reason": reason,
                "set": "Scientific Stress" if task.get("subset") == "scientific_stress" else "Domain Core",
                "domain": task.get("domain", ""),
                "subfield": task.get("subfield", ""),
                "question": task.get("question", ""),
                "expected_answer": task.get("answer") or task.get("answer_rationale", ""),
                "rubric_criteria_json": json.dumps(task.get("rubric", []), ensure_ascii=False, separators=(",", ":")),
                "model_answer": output.get("answer", ""),
                "model_error": output.get("error", ""),
                "judge_total_score": review["total"],
                "judge_max_score": 10.0,
                "judge_hard_fail": review["hard_fail"],
                "judge_hard_fail_reasons": "; ".join(map(str, review["hard_fail_reasons"])),
                "judge_comment": review["comment"],
                "dimension_scores_json": json.dumps(review["scores"], ensure_ascii=False, separators=(",", ":")),
                "expert_decision": "",
                "expert_total_score": "",
                "expert_dimension_overrides": "",
                "override_reason": "",
                "reviewer": "",
                "review_date": "",
                "affects_summary": "",
            }
        )
    write_csv(JUDGE / "manual_review_packet.csv", fields, packet)

    decision_fields = [
        "id", "model_id", "judge_total_score", "judge_hard_fail", "expert_decision",
        "expert_total_score", "override_reason", "reviewer", "review_date", "affects_summary",
    ]
    decision_rows = [{field: row.get(field, "") for field in decision_fields} for row in packet]
    write_csv(JUDGE / "expert_review_decisions.template.csv", decision_fields, decision_rows)
    write_csv(
        JUDGE / "expert_review_overrides.template.csv",
        ["id", "model_id", "dimension", "judge_score", "expert_score", "override_reason", "reviewer", "date"],
        [],
    )

    counts = Counter(row["model_id"] for row in packet)
    hard_fails = sum(str(row["judge_hard_fail"]).lower() == "true" for row in packet)
    notes = [
        "# GPT-5.6-sol Adjudication Template",
        "",
        "Status: pending separately evidenced expert review.",
        "",
        "The packet contains every judge hard fail and score below 7.0, the deterministic no-rescue missing answer, and risk-focused supplemental samples until each model reaches at least 9 of 30 answers.",
        "",
        "## Coverage",
        "",
    ]
    for model_id, count in sorted(counts.items()):
        notes.append(f"- {model_id}: {count} / 30")
    notes.extend(
        [
            f"- Judge hard-fail rows in packet: {hard_fails}",
            "",
            "## Review Policy",
            "",
            "- Review against the frozen question, rubric, reference answer, and original model answer.",
            "- Do not repair or infer missing model content.",
            "- Keep a missing answer at 0 under the no-rescue policy.",
            "- Record every changed score and reason; do not label results confirmed until all required fields are complete.",
            "",
        ]
    )
    (JUDGE / "adjudication_notes.template.md").write_text("\n".join(notes), encoding="utf-8")
    print(f"Wrote pending review packet with {len(packet)} rows: {dict(sorted(counts.items()))}")


if __name__ == "__main__":
    main()
