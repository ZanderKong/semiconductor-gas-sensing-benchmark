# Model Diagnostic Report

## Summary

This report records the real-model MCQ validation run for the Semiconductor Gas-Sensing Benchmark Mini. The benchmark contains 100 items in total: 82 multiple-choice items and 18 free-response items.

## Run Setup

| Setting | Value |
|---|---|
| Date | 2026-06-29 |
| Benchmark | `data/benchmark_v1.json` |
| Scored subset | 82 multiple-choice questions |
| Prompt | `eval/prompts/base_prompt.md` |
| Temperature | 0 |
| Runner | `eval/run_eval.py` |
| Scorer | `eval/score_mcq.py` |
| Run manifest | `results/model_run_manifest.json` |

## Results

| Model | Provider | Correct / Total | MCQ Accuracy | Safety Fail Rate | Elapsed Seconds |
|---|---|---:|---:|---:|---:|
| deepseek-chat | openai_compatible | 82 / 82 | 100.0% | 0.0% | 6.8 |
| gpt-5.5 | codex_cli | 82 / 82 | 100.0% | 0.0% | 28.54 |

## Interpretation

Both evaluated models completed all 82 MCQ items without parser errors or missing answers. Both models achieved 82 / 82, so the useful conclusion is that the call, parse, score, and report pipeline works end to end.

The result should not be presented as a stable capability ranking. The MCQ subset is too easy for strong models and should be treated as a regression and coverage check.

## Recommended Next Steps

1. Score the 18 free-response items with a judge protocol and human audit.
2. Add table-heavy, calculation-heavy, and conflicting-evidence tasks.
3. Add adversarial distractors where every option is locally plausible.
4. Use the V3-alpha task-unit runner for trace-based model comparisons after the live tool harness is available.

## V3-Alpha Status

The V3-alpha task-unit layer already includes schema validation, Hard Gate definitions, D0-D6 scoring dimensions, trace requirements, an API-free demo runner, and report generation. The current real-model run validates the MCQ layer while the V3 task-unit layer remains the next target for full model evaluation.
