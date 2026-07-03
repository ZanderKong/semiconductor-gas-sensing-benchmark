# Model Diagnostic Report

## Summary

This report records a real-model MCQ validation run for the Semiconductor Gas-Sensing Benchmark Mini.

## Run Setup

| Setting | Value |
|---|---|
| Date | 2026-07-03 |
| Benchmark | `data/benchmark_sgs_hard50.json` |
| Scored subset | standard Hard50 diagnostic MCQ set |
| Prompt | `eval/prompts/base_prompt.md` |
| Temperature | 0 |
| Runner | `eval/run_eval.py` |
| Scorer | `eval/score_mcq.py` |
| Model outputs | `results/standard_20260703/hard50/model_outputs.csv` |

## Results

| Model | Provider | Correct / Total | MCQ Accuracy | Safety Boundary Review | Elapsed Seconds |
|---|---|---:|---:|---:|---:|
| deepseek-v4-pro | openai_compatible | 47 / 50 | 94.0% | 25.0% | 37.35 |
| ep-20260703090429-qpmt7 | openai_compatible | 48 / 50 | 96.0% | 12.5% | 171.56 |
| gpt-5.5 | codex_cli | 48 / 50 | 96.0% | 12.5% | 21.01 |
| mimo-v2.5-pro | openai_compatible | 47 / 50 | 94.0% | 25.0% | 137.85 |

## Interpretation

Hard diagnostic layer for evidence conflict, safety gates, condition updates, and mechanism-transfer traps.

## Extension Tracks

1. Score the 30 free-response items with the judge protocol.
2. Expand table-heavy, calculation-heavy, and conflicting-evidence tasks.
3. Add adversarial distractors where every option is locally plausible.
4. Review consistency groups to profile principle stability across nearby variants.

## SGS152 Status

The active benchmark contains 152 items: 122 MCQ items and 30 free-response items. MCQ scoring is automatic; free-response review is handled through the rubric and review protocol.
