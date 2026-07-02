# Model Diagnostic Report

## Summary

This report records a real-model MCQ validation run for the Semiconductor Gas-Sensing Benchmark Mini.

## Run Setup

| Setting | Value |
|---|---|
| Date | 2026-07-01 |
| Benchmark | `data/benchmark_realistic_seed2.json` |
| Scored subset | mini-benchmark 0.5.0 realistic human-seed 2-item MCQ probe |
| Prompt | `eval/prompts/base_prompt.md` |
| Temperature | 0 |
| Runner | `eval/run_eval.py` |
| Scorer | `eval/score_mcq.py` |
| Model outputs | `results/realistic_seed2/model_outputs.csv` |

## Results

| Model | Provider | Correct / Total | MCQ Accuracy | Safety Boundary Review | Elapsed Seconds |
|---|---|---:|---:|---:|---:|
| gpt-5.5 | codex_cli | 2 / 2 | 100.0% | n/a | 8.82 |

## Interpretation

Human-written realistic experiment observation probe for solubility-context and silver-photochromism particle-size reasoning.

## Extension Tracks

1. Score the 18 free-response items with the bilingual judge protocol.
2. Expand table-heavy, calculation-heavy, and conflicting-evidence tasks.
3. Add adversarial distractors where every option is locally plausible.
4. Review consistency groups to profile principle stability across nearby variants.

## SGS-100 Status

The active benchmark is a single 100-item dataset with 82 MCQ items and 18 free-response items. MCQ scoring is automatic; free-response and consistency review are handled through the rubric and review protocol.
