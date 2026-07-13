# Iteration Notes

## 0.5.0 Evidence Update

The participating-model run remains unchanged: 122 MCQ and 30 free-response answers for each of four participating models, plus separate Robustness and Hard50 diagnostics.

GPT-5.6-sol now replaces GPT-5.5 as the current free-response judge. GPT-5.6-sol is not a participating model and has no model score or leaderboard entry. The prior GPT-5.5 judge artifacts and confirmed decisions are retained only in `archive/judge_history/gpt-5.5_20260703/`.

## Current Results

| Model | SGS152 MCQ | FR Avg | FR Hard Fails |
|---|---:|---:|---:|
| MiMo v2.5 Pro | 119 / 122 | 5.448 | 11 |
| Seed-2.1 | 118 / 122 | 7.522 | 4 |
| GPT-5.5 | 117 / 122 | 8.150 | 0 |
| DeepSeek V4 Pro | 115 / 122 | 6.762 | 0 |

## Current Boundaries

- MCQ remains the only main leaderboard.
- Free-response includes a completed project-owner-delegated assistant review of all 58 packet rows; external independent blind review was not performed.
- DeepSeek `SGS-081` remains missing and deterministically scores 0.
- Judge hard fails retain their original total and are counted separately.
- Robustness and Hard50 are diagnostics, not leaderboard extensions.
