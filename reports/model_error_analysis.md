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
| GPT-5.5 | 117 / 122 | 7.485 |
| DeepSeek V4 Pro | 115 / 122 | 6.303 |

Free-response values are judge-scored plus assistant-assisted project-owner confirmed adjudication. GPT-5.5/ChatGPT was used as judge, so judge overlap bias remains disclosed; four GPT-5.5 high-score samples were adjusted downward.

## Model Notes

### MiMo v2.5 Pro

MiMo has the highest SGS152 MCQ result at 119 / 122 and ties GPT-5.5 on Robustness at 34 / 40. Its free-response result is much lower, with three retained hard fails after adjudication. Hard fail rows retain their original judge totals and are counted separately.

### Seed-2.1

Seed-2.1 has the second-highest SGS152 MCQ result at 118 / 122 and the strongest optional Hard50 result tied with GPT-5.5 at 48 / 50. Its free-response average is 6.888.

### GPT-5.5

GPT-5.5 scored 117 / 122 on SGS152 MCQ and has the highest adjudicated free-response average, 7.485. Because GPT-5.5 also served as the free-response judge, four high-score GPT-5.5 samples were conservatively adjusted downward: `SGS-030`, `SGS-032`, `SGS-099`, and `SGS-FM-FR-004`.

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

Integrated diagnostic reading: MiMo leads the MCQ main leaderboard but has the weakest free-response profile and 3 retained hard fails. GPT-5.5 has the strongest adjudicated free-response average and ties Seed-2.1 on Hard50. Seed-2.1 is the most balanced MCQ runner-up. DeepSeek is lowest on SGS152 MCQ and Robustness, and has the preserved `SGS-081` no-rescue missing answer.

## Review Priorities

Confirmed adjudication highlights:

- `SGS-082`, `SGS-FM-FR-007`, and `SGS-FM-FR-011` for MiMo remain hard fail.
- DeepSeek `SGS-081` remains no-rescue 0.
- DeepSeek `SGS-FM-FR-007` remains reviewed borderline / needs_human_attention at 4.9 and is not upgraded to hard fail.
- GPT-5.5 overlap-bias adjustments lowered four high-score samples.

## Next Calibration Targets

- Preserve SGS152 MCQ as the main 0.5.0 leaderboard.
- Treat free-response as judge-scored plus assistant-assisted project-owner confirmed adjudication, not as an independent blind review.
- Recalibrate Robustness and Hard50 as diagnostics rather than leaderboard extensions.
