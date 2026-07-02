#!/usr/bin/env python3
"""Build a local original-question test bank from ChemBench rows API."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/reference_original_bank/chembench_original_mcq80.json"
META = ROOT / "results/reference_original_bank/chembench_original_mcq80_sources.json"

CONFIGS = [
    "general_chemistry",
    "organic_chemistry",
    "inorganic_chemistry",
    "physical_chemistry",
    "analytical_chemistry",
    "materials_science",
    "technical_chemistry",
    "toxicity_and_safety",
]


def fetch_rows(config: str, length: int = 80) -> list[dict]:
    params = urllib.parse.urlencode(
        {
            "dataset": "jablonkagroup/ChemBench",
            "config": config,
            "split": "train",
            "offset": 0,
            "length": length,
        }
    )
    url = f"https://datasets-server.huggingface.co/rows?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return [row["row"] for row in payload["rows"]]


def parse_example(row: dict) -> tuple[str, dict[str, str], str] | None:
    examples = row.get("examples") or []
    if not examples:
        return None
    example = examples[0]
    question = example.get("input")
    scores_raw = example.get("target_scores")
    if not question or not scores_raw:
        return None
    scores = json.loads(scores_raw)
    if len(scores) < 2 or len(scores) > 4:
        return None
    labels = list("ABCD")
    options = {labels[i]: str(option) for i, option in enumerate(scores.keys())}
    correct = [labels[i] for i, score in enumerate(scores.values()) if float(score) == 1.0]
    if len(correct) != 1:
        return None
    return question, options, correct[0]


def main() -> None:
    items: list[dict] = []
    sources: list[dict] = []
    for config in CONFIGS:
        kept = 0
        for row in fetch_rows(config):
            parsed = parse_example(row)
            if not parsed:
                continue
            question, options, answer = parsed
            qid = f"CHEMBENCH-ORIG-{len(items) + 1:03d}"
            item = {
                "id": qid,
                "question_type": "multiple_choice",
                "domain": config,
                "domain_cn": config,
                "scenario_stage": "reference_original",
                "tool_type": "no_tool",
                "question": question,
                "options": options,
                "answer": answer,
                "answer_rationale": "Original ChemBench MCQ answer from target_scores.",
                "option_profiles": {key: ("best" if key == answer else "distractor") for key in options},
                "option_rationales": {key: "Original option from ChemBench." for key in options},
                "difficulty": infer_difficulty(row),
                "scoring_type": "exact_match",
                "evaluation_dimensions": ["reference_original", config],
                "failure_mode": f"reference_original_{config}",
                "private_dependency_level": "none",
                "tags": row.get("keywords", []),
                "benchmark_version": "reference-original-chembench-local",
                "variant_type": "base",
                "reference_benchmark": "ChemBench",
                "reference_license": "MIT",
                "reference_uuid": row.get("uuid", ""),
                "reference_name": row.get("name", ""),
                "reference_subfield": row.get("subfield", ""),
            }
            items.append(item)
            sources.append(
                {
                    "id": qid,
                    "reference_benchmark": "ChemBench",
                    "reference_license": "MIT",
                    "reference_config": config,
                    "reference_uuid": row.get("uuid", ""),
                    "reference_name": row.get("name", ""),
                    "reference_subfield": row.get("subfield", ""),
                    "canary_present": bool(row.get("canary")),
                }
            )
            kept += 1
            if kept == 10:
                break
        if kept < 10:
            raise SystemExit(f"Only kept {kept} rows for {config}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    META.write_text(json.dumps(sources, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(items)} original ChemBench MCQ items to {OUT.relative_to(ROOT)}")


def infer_difficulty(row: dict) -> str:
    joined = " ".join(str(x) for x in row.get("keywords", []))
    if "difficulty-advanced" in joined:
        return "advanced"
    if "difficulty-basic" in joined:
        return "basic"
    return "intermediate"


if __name__ == "__main__":
    main()
