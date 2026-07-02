# Model Diagnostic Report

## Summary

This report records a real-model MCQ validation run for the Semiconductor Gas-Sensing Benchmark Mini.

## Run Setup

| Setting | Value |
|---|---|
| Date | 2026-07-02 |
| Benchmark | `data/benchmark.json` |
| Scored subset | mini-benchmark 0.5.0 SGS152 active MCQ set |
| Prompt | `eval/prompts/base_prompt.md` |
| Temperature | 0 |
| Runner | `eval/run_eval.py` |
| Scorer | `eval/score_mcq.py` |
| Model outputs | `results/sgs152_merged/model_outputs_sgs152_merged_all.csv` |

## Results

| Model | Provider | Correct / Total | MCQ Accuracy | Safety Boundary Review | Elapsed Seconds |
|---|---|---:|---:|---:|---:|
| deepseek-v4-pro | openai_compatible | 99 / 122 | 81.2% | 0.0% | 192.5 |
| gpt-5.5 | codex_cli | 99 / 122 | 81.2% | 0.0% | 37.49 |
| mimo-v2.5-pro | openai_compatible | 100 / 122 | 82.0% | 12.5% | 321.4 |

## Interpretation

Active SGS152 validation combines semiconductor gas-sensing R&D judgment with Scientific Stress Set mechanisms.

## Extension Tracks

1. Pair MCQ errors with sampled rubric review where free-response items are part of the versioned dataset.
2. Expand table-heavy, calculation-heavy, and conflicting-evidence tasks.
3. Add adversarial distractors where every option is locally plausible.
4. Review consistency groups to profile principle stability across nearby variants.

## Active Benchmark Status

The active 0.5.0 main set is SGS152: 152 total items, including 122 MCQ items and 30 rubric-defined free-response items. This diagnostic report may score the main set or a diagnostic MCQ subset; the scored subset is defined in the run setup table.
