# Final Release Audit

## Scope

This audit covers the unchanged four-model live run and the GPT-5.6-sol replacement judge evidence in `results/standard_20260703`.

## Evidence Status

- Four participating models; GPT-5.6-sol is judge-only.
- SGS152 MCQ: 122 answers per model and the only main leaderboard.
- Free-response: 30 answers and 30 GPT-5.6-sol reviews per model, 120 reviews total.
- Robustness and Hard50 remain separate diagnostics.
- Task, prompt, participating-model-output and judge-prompt hashes are recorded.
- Judge run baseline commit: `ee04eff7...`; `working_tree_dirty=false`.
- Raw judge outputs exist locally and remain ignored by git.

## Free-response Status

| Model | Average | Hard Fails |
|---|---:|---:|
| GPT-5.5 | 8.150 | 0 |
| Seed-2.1 | 7.522 | 4 |
| DeepSeek V4 Pro | 6.762 | 0 |
| MiMo v2.5 Pro | 5.448 | 11 |

DeepSeek `SGS-081` remains a no-rescue zero. Hard-fail rows retain the judge total and are counted separately.

## Review State

The project owner delegated all 58 packet rows to the assistant. Decisions are complete: 33 agree, 15 hard-fail confirmed, 1 missing kept zero and 9 score adjustments. All adjustments affect only `safety_and_privacy`, with explicit reasons and hashes. There are no unresolved items. This is a delegated assistant review, not an independent external blind review.

## Historical Judge

The prior GPT-5.5 judge artifacts, human decisions, overrides and notes are preserved under `archive/judge_history/gpt-5.5_20260703/`. They are historical evidence and do not modify the current GPT-5.6-sol score baseline.

## Release Decision

The MCQ leaderboard and optional diagnostics remain valid. The replacement judge evidence and delegated review are complete and auditable. Free-response results must be described as project-owner-delegated assistant review, not as independent external human confirmation.
