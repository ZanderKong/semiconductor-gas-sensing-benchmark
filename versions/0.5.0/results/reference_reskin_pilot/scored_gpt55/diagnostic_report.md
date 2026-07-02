# Model Diagnostic Report

## Summary

This report records a real-model MCQ validation run for the Semiconductor Gas-Sensing Benchmark Mini.

## Run Setup

| Setting | Value |
|---|---|
| Date | 2026-07-01 |
| Benchmark | `data/benchmark_reference_reskin_pilot.json` |
| Scored subset | reference-reskin pilot 12 MCQ |
| Prompt | `eval/prompts/base_prompt.md` |
| Temperature | 0 |
| Runner | `eval/run_eval.py` |
| Scorer | `eval/score_mcq.py` |
| Model outputs | `results/reference_reskin_pilot/model_outputs_gpt55.csv` |

## Results

| Model | Provider | Correct / Total | MCQ Accuracy | Safety Boundary Review | Elapsed Seconds |
|---|---|---:|---:|---:|---:|
| gpt-5.5 | codex_cli | 12 / 12 | 100.0% | 0.0% | 12.79 |

## Interpretation

Pilot generated from reference benchmark patterns before direct reference-bank failure mining.

## Extension Tracks

1. Score the 18 free-response items with the bilingual judge protocol.
2. Expand table-heavy, calculation-heavy, and conflicting-evidence tasks.
3. Add adversarial distractors where every option is locally plausible.
4. Review consistency groups to profile principle stability across nearby variants.

## SGS-100 Status

The active benchmark is a single 100-item dataset with 82 MCQ items and 18 free-response items. MCQ scoring is automatic; free-response and consistency review are handled through the rubric and review protocol.
