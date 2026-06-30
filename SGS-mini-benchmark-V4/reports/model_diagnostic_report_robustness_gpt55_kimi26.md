# Model Diagnostic Report

## Summary

This report records a real-model MCQ validation run for the Semiconductor Gas-Sensing Benchmark Mini.

## Run Setup

| Setting | Value |
|---|---|
| Date | 2026-06-30 |
| Benchmark | `data/benchmark_sgs100_robustness.json` |
| Scored subset | 40 robustness variants, GPT-5.5 plus Kimi 2.6 attempt |
| Prompt | `eval/prompts/base_prompt.md` |
| Temperature | 0 |
| Runner | `eval/run_eval.py` |
| Scorer | `eval/score_mcq.py` |
| Model outputs | `results/gpt55_kimi26/model_outputs_robustness_gpt55_kimi26.csv` |

## Results

| Model | Provider | Correct / Total | MCQ Accuracy | Safety Fail Rate | Elapsed Seconds |
|---|---|---:|---:|---:|---:|
| gpt-5.5 | codex_cli | 35 / 40 | 87.5% | 12.5% | 18.21 |

## Interpretation

This run adds GPT-5.5 and attempts Kimi 2.6 on SGS-100 robustness variants. Kimi 2.6 failed before returning answers because the local environment could not complete a TLS connection to the Moonshot endpoint.

## Recommended Next Steps

1. Score the 18 free-response items with a judge protocol and human audit.
2. Add table-heavy, calculation-heavy, and conflicting-evidence tasks.
3. Add adversarial distractors where every option is locally plausible.
4. Review consistency groups to detect principle flips across nearby variants.

## SGS-100 Status

The active benchmark is a single 100-item dataset with 82 MCQ items and 18 free-response items. MCQ scoring is automatic; free-response and consistency review should be audited with the rubric.
