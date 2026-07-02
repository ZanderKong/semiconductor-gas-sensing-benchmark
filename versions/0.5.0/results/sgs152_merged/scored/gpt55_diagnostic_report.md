# Model Diagnostic Report

## Summary

This report records a real-model MCQ validation run for the Semiconductor Gas-Sensing Benchmark Mini.

## Run Setup

| Setting | Value |
|---|---|
| Date | 2026-07-02 |
| Benchmark | `data/benchmark.json` |
| Scored subset | SGS152 active MCQ - GPT-5.5 |
| Prompt | `eval/prompts/base_prompt.md` |
| Temperature | 0 |
| Runner | `eval/run_eval.py` |
| Scorer | `eval/score_mcq.py` |
| Model outputs | `results/sgs152_merged/gpt55_model_outputs_sgs152_merged.csv` |

## Results

| Model | Provider | Correct / Total | MCQ Accuracy | Safety Boundary Review | Elapsed Seconds |
|---|---|---:|---:|---:|---:|
| gpt-5.5 | codex_cli | 95 / 122 | 77.9% | 0.0% | 36.02 |

## Interpretation

GPT-5.5 rerun for active SGS152 after local usage reset.

## Extension Tracks

1. Score the 30 free-response items with the bilingual judge protocol.
2. Expand table-heavy, calculation-heavy, and conflicting-evidence tasks.
3. Add adversarial distractors where every option is locally plausible.
4. Review consistency groups to profile principle stability across nearby variants.

## Active Benchmark Status

The active 0.5.0 benchmark is SGS152: 152 total items, including 122 MCQ items and 30 free-response items. MCQ scoring is automatic; free-response and consistency review are handled through the rubric and review protocol. The legacy SGS100 clean export remains available for historical comparison.
