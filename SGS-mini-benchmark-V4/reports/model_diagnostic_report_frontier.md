# Model Diagnostic Report

## Summary

This report records a real-model MCQ validation run for the Semiconductor Gas-Sensing Benchmark Mini.

## Run Setup

| Setting | Value |
|---|---|
| Date | 2026-06-30 |
| Benchmark | `data/benchmark.json` |
| Scored subset | 82 MCQ after SGS-100 clean revision |
| Prompt | `eval/prompts/base_prompt.md` |
| Temperature | 0 |
| Runner | `eval/run_eval.py` |
| Scorer | `eval/score_mcq.py` |
| Model outputs | `results/model_outputs_frontier.csv` |

## Results

| Model | Provider | Correct / Total | MCQ Accuracy | Safety Fail Rate | Elapsed Seconds |
|---|---|---:|---:|---:|---:|
| deepseek-v4-pro | openai_compatible | 76 / 82 | 92.7% | 12.5% | 94.96 |
| mimo-v2.5-pro | openai_compatible | 80 / 82 | 97.6% | 0.0% | 37.64 |

## Interpretation

Frontier external-model MCQ validation on the cleaned SGS-100 main set. Kimi was attempted in the runner but the local environment could not complete a TLS connection to the Moonshot endpoint, so this report scores completed DeepSeek and MiMo rows only.

## Recommended Next Steps

1. Score the 18 free-response items with a judge protocol and human audit.
2. Add table-heavy, calculation-heavy, and conflicting-evidence tasks.
3. Add adversarial distractors where every option is locally plausible.
4. Review consistency groups to detect principle flips across nearby variants.

## SGS-100 Status

The active benchmark is a single 100-item dataset with 82 MCQ items and 18 free-response items. MCQ scoring is automatic; free-response and consistency review should be audited with the rubric.
