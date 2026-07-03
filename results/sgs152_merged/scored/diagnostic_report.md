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
| DeepSeek V4 Pro | deepseek | 99 / 122 | 81.2% | 0.0% | n/a |
| GPT-5.5 | codex_cli | 99 / 122 | 81.2% | 0.0% | n/a |
| MiMo v2.5 Pro | xiaomimimo | 100 / 122 | 82.0% | 12.5% | n/a |

## Interpretation

Active SGS152 validation combines semiconductor gas-sensing R&D judgment with Scientific Stress Set mechanisms.

## Extension Tracks

1. Score the 30 free-response items with the judge protocol.
2. Expand table-heavy, calculation-heavy, and conflicting-evidence tasks.
3. Add adversarial distractors where every option is locally plausible.
4. Review consistency groups to profile principle stability across nearby variants.

## SGS152 Status

The active benchmark contains 152 items: 122 MCQ items and 30 free-response items. MCQ scoring is automatic; free-response review is handled through the rubric and review protocol.
