# Model Diagnostic Report

## Summary

This report records a real-model MCQ validation run for the Semiconductor Gas-Sensing Benchmark Mini.

## Run Setup

| Setting | Value |
|---|---|
| Date | 2026-07-01 |
| Benchmark | `data/benchmark_sgs_failure_mined_v1.json` |
| Scored subset | SGS failure-mined v1 12-item MCQ set |
| Prompt | `eval/prompts/base_prompt.md` |
| Temperature | 0 |
| Runner | `eval/run_eval.py` |
| Scorer | `eval/score_mcq.py` |
| Model outputs | `results/failure_mined_v1_validated/model_outputs.csv` |

## Results

| Model | Provider | Correct / Total | MCQ Accuracy | Safety Boundary Review | Elapsed Seconds |
|---|---|---:|---:|---:|---:|
| deepseek-v4-pro | openai_compatible | 12 / 12 | 100.0% | 0.0% | 9.61 |
| gpt-5.5 | codex_cli | 12 / 12 | 100.0% | 0.0% | 14.91 |
| mimo-v2.5-pro | openai_compatible | 12 / 12 | 100.0% | 0.0% | 49.89 |

## Interpretation

SGS candidate questions generated from failure-mechanism seed patterns.

## Extension Tracks

1. Score the 18 free-response items with the bilingual judge protocol.
2. Expand table-heavy, calculation-heavy, and conflicting-evidence tasks.
3. Add adversarial distractors where every option is locally plausible.
4. Review consistency groups to profile principle stability across nearby variants.

## SGS-100 Status

The active benchmark is a single 100-item dataset with 82 MCQ items and 18 free-response items. MCQ scoring is automatic; free-response and consistency review are handled through the rubric and review protocol.
