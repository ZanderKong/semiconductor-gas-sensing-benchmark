# Final Release Audit

## Scope

This audit covers the 0.5.0 live RC run in `results/standard_20260703`.

The main leaderboard is based only on `data/benchmark.json`, the SGS152 Main Set. Robustness 40 and Hard50 50 are optional diagnostic results. They are not included in the main leaderboard and are not collapsed into a full-suite aggregate score.

## Evidence Source

The formal evidence source is `results/standard_20260703`.

Deprecated reconstructed or generated artifacts are preserved under `archive/deprecated_reconstructed_results/` for traceability only. They are not used as 0.5.0 final evidence.

Raw model outputs exist locally under the standard run directory. They are intentionally ignored by git because they are raw model transcripts. Parsed outputs, manifests, scored summaries, judge outputs, analysis files, and audit files are intended to be committed.

## Main Leaderboard Status

SGS152 MCQ main leaderboard:

| Model | Correct / Total |
|---|---:|
| DeepSeek V4 Pro | 115 / 122 |
| Seed-2.1 | 118 / 122 |
| GPT-5.5 | 117 / 122 |
| MiMo v2.5 Pro | 119 / 122 |

## Free-response Status

Judge-scored provisional free-response results:

| Model | Average |
|---|---:|
| DeepSeek V4 Pro | 6.303 |
| Seed-2.1 | 6.888 |
| GPT-5.5 | 7.568 |
| MiMo v2.5 Pro | 4.843 |

Free-response was judged by GPT-5.5/ChatGPT. Because GPT-5.5 is also a participating model, these scores have judge overlap bias. `results/standard_20260703/free_response_judge/manual_review_queue.csv` has been generated. Until human review is complete, free-response should be treated as a judge-scored provisional result rather than an unbiased final ranking.

## Optional Diagnostic Results

Robustness:

| Model | Correct / Total |
|---|---:|
| DeepSeek V4 Pro | 29 / 40 |
| Seed-2.1 | 32 / 40 |
| GPT-5.5 | 34 / 40 |
| MiMo v2.5 Pro | 34 / 40 |

Hard50:

| Model | Correct / Total |
|---|---:|
| DeepSeek V4 Pro | 47 / 50 |
| Seed-2.1 | 48 / 50 |
| GPT-5.5 | 48 / 50 |
| MiMo v2.5 Pro | 47 / 50 |

These diagnostic sets are used for failure-mode review only. They do not enter the main leaderboard and do not produce a total benchmark score.

## Kimi Exclusion

Kimi smoke test failed with 401 Unauthorized. Kimi is excluded from the main leaderboard and appears only in the smoke/failure record.

## Missing Answer Handling

DeepSeek V4 Pro did not return an answer for `SGS-081` in the free-response run. The missing answer was preserved under the no-rescue policy and scored as 0 by the judge workflow. No manual answer was inserted.

## Deprecated Artifacts

Deprecated artifacts include old reconstructed SGS152 MCQ outputs, pre-final open-ended scoring artifacts, pre-standard Hard50 outputs, and old summary files. They are preserved under `archive/deprecated_reconstructed_results/`.

README, evaluation report, model error analysis, iteration notes, and results README now use `results/standard_20260703` as the formal evidence source.

## Manual Review Plan

Manual review plan: `reports/manual_review_plan.md`.

Review queue: `results/standard_20260703/free_response_judge/manual_review_queue.csv`.

Prepared review packet: `results/standard_20260703/free_response_judge/manual_review_packet.csv`.

The packet includes every queue item and supplemental spot checks so each model has at least 9 free-response answers ready for human review.

Human review is pending. Human reviewers may correct judge scores through `results/standard_20260703/free_response_judge/human_review_overrides.csv` and explain decisions in `results/standard_20260703/free_response_judge/adjudication_notes.md`.

## Release Decision

Current status: 0.5.0 live RC.

Do not mark this as final until human review of free-response judge-risk items is complete and final documentation is refreshed. After manual review and final documentation update, this package can be marked as v0.5.0.

## Commands Run

```bash
python3 scripts/validate_benchmark.py
python3 scripts/lint_benchmark.py
python3 scripts/validate_hard50.py
python3 scripts/run_standard_benchmark.py --out-root results/standard_20260703 --smoke-timeout 900 --timeout 2400
python3 scripts/final_provenance_audit.py
```
