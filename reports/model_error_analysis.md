# Model Error Analysis

## Evidence Source

This analysis uses only `results/standard_20260703`.

Deprecated reconstructed MCQ outputs and pre-final open-ended scoring artifacts are not used as 0.5.0 final evidence.

## Summary

SGS152 MCQ remains the main leaderboard. The live run shows a tight cluster among four participating models:

| Model | SGS152 MCQ | Free-response Avg |
|---|---:|---:|
| MiMo v2.5 Pro | 119 / 122 | 4.843 |
| Seed-2.1 | 118 / 122 | 6.888 |
| GPT-5.5 | 117 / 122 | 7.568 |
| DeepSeek V4 Pro | 115 / 122 | 6.303 |

Free-response values are judge-scored provisional results. GPT-5.5/ChatGPT was used as judge, so judge overlap bias is present.

## Model Notes

### MiMo v2.5 Pro

MiMo has the highest SGS152 MCQ result at 119 / 122 and ties GPT-5.5 on Robustness at 34 / 40. Its free-response result is much lower, with three hard fails in the judge output. Manual review should prioritize MiMo hard-fail and low-score free-response items before any final open-ended conclusion.

### Seed-2.1

Seed-2.1 has the second-highest SGS152 MCQ result at 118 / 122 and the strongest optional Hard50 result tied with GPT-5.5 at 48 / 50. Its free-response average is 6.888. It is included in the main run because smoke testing passed.

### GPT-5.5

GPT-5.5 scored 117 / 122 on SGS152 MCQ and has the highest judge-scored free-response average, 7.568. Because GPT-5.5 also served as the free-response judge, this open-ended advantage must be treated as provisional and potentially biased.

### DeepSeek V4 Pro

DeepSeek scored 115 / 122 on SGS152 MCQ, 29 / 40 on Robustness, and 47 / 50 on Hard50. It had one missing free-response answer, `SGS-081`, which was preserved under the no-rescue policy and scored as 0.

## Diagnostic Layers

Robustness and Hard50 are optional diagnostic layers:

| Model | Robustness | Hard50 |
|---|---:|---:|
| GPT-5.5 | 34 / 40 | 48 / 50 |
| MiMo v2.5 Pro | 34 / 40 | 47 / 50 |
| Seed-2.1 | 32 / 40 | 48 / 50 |
| DeepSeek V4 Pro | 29 / 40 | 47 / 50 |

These results should guide item-level review and future calibration. They should not be combined with SGS152 into a full-suite total score.

## Review Priorities

Manual review should focus on:

- MiMo hard-fail free-response items;
- DeepSeek `SGS-081` missing answer;
- low-score free-response items in `manual_review_queue.csv`;
- safety-boundary items;
- Scientific Stress free-response items;
- cases where the GPT-5.5 judge may favor concise GPT-style answers.

## Next Calibration Targets

- Preserve SGS152 MCQ as the main 0.5.0 leaderboard.
- Treat free-response as provisional until human adjudication is complete.
- Recalibrate Robustness and Hard50 as diagnostics rather than leaderboard extensions.
- Add item-level performance fields after final human review is complete.
