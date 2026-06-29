# Model Diagnostic Report

## Summary

This report evaluates models on the automatically scored multiple-choice subset of the Semiconductor Gas-Sensing Benchmark Mini. The benchmark contains 100 items in total: 82 MCQ and 18 free-response items.

## Run Setup

| Setting | Value |
|---|---|
| Date | 2026-06-27 |
| Benchmark | `data/benchmark_v1.json` |
| Scored subset | 82 multiple-choice questions |
| Prompt | `eval/prompts/base_prompt.md` |
| Temperature | 0 |
| Scorer | `eval/score_mcq.py` |

## Results

| Model | Correct / Total | MCQ Run Status | Safety Fail Rate |
|---|---:|---:|---:|
| deepseek-chat | 82 / 82 | completed all MCQ items | 0.0% |
| gpt-5.5 | 82 / 82 | completed all MCQ items | 0.0% |

## Interpretation

Both completed models solved all 82 MCQ items with zero observed safety failures. The useful conclusion is that the call-parse-score pipeline has been validated, while the MCQ subset is not yet discriminative enough for strong models.

The next version should add more table-based items, conflicting evidence items, and free-response grading to expose subtler weaknesses.

## Recommended Next Steps

1. Run the 18 free-response items with human scoring or LLM-as-judge plus human audit.
2. Increase calculation-heavy and table-analysis tasks.
3. Add adversarial distractors where every option is locally plausible.
4. Expand the model set after endpoint configuration and scoring policy are stable.

## V3-alpha Status

V3-alpha has shifted the project from answer-only items to auditable task units. The local demo runner now produces manifest, trace, judge outputs, aggregate metrics, report, and badcase gallery. Future model runs can reuse the same scoring and trace structure.
