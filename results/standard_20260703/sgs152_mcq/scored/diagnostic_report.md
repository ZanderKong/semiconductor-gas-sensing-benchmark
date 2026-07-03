# Model Diagnostic Report

## Summary

This report records a real-model MCQ validation run for the Semiconductor Gas-Sensing Benchmark Mini.

## Run Setup

| Setting | Value |
|---|---|
| Date | 2026-07-03 |
| Benchmark | `data/benchmark.json` |
| Scored subset | standard SGS152 MCQ set |
| Prompt | `eval/prompts/base_prompt.md` |
| Temperature | 0 |
| Runner | `eval/run_eval.py` |
| Scorer | `eval/score_mcq.py` |
| Model outputs | `results/standard_20260703/sgs152_mcq/model_outputs.csv` |

## Results

| Model | Provider | Correct / Total | MCQ Accuracy | Safety Boundary Review | Elapsed Seconds |
|---|---|---:|---:|---:|---:|
| deepseek-v4-pro | openai_compatible | 115 / 122 | 94.3% | 0.0% | 98.95 |
| ep-20260703090429-qpmt7 | openai_compatible | 118 / 122 | 96.7% | 6.2% | 414.92 |
| gpt-5.5 | codex_cli | 117 / 122 | 95.9% | 6.2% | 35.04 |
| mimo-v2.5-pro | openai_compatible | 119 / 122 | 97.5% | 6.2% | 343.28 |

## Interpretation

Core SGS152 MCQ scoring under a single prompt, single sampling, no-tool standard run.

## Extension Tracks

1. Score the 30 free-response items with the judge protocol.
2. Expand table-heavy, calculation-heavy, and conflicting-evidence tasks.
3. Add adversarial distractors where every option is locally plausible.
4. Review consistency groups to profile principle stability across nearby variants.

## SGS152 Status

The active benchmark contains 152 items: 122 MCQ items and 30 free-response items. MCQ scoring is automatic; free-response review is handled through the rubric and review protocol.
