# Final Release Audit

## Scope

This audit covers the 0.5.0 live standard run and confirmed free-response adjudication in `results/standard_20260703`.

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

Free-response results are judge-scored plus assistant-assisted project-owner confirmed adjudication:

| Model | Average | Hard Fails |
|---|---:|---:|
| DeepSeek V4 Pro | 6.303 | 0 |
| Seed-2.1 | 6.888 | 0 |
| GPT-5.5 | 7.485 | 0 |
| MiMo v2.5 Pro | 4.843 | 3 |

Free-response was first judged by GPT-5.5/ChatGPT and then confirmed through assistant-assisted project-owner adjudication. Because GPT-5.5 is also a participating model, judge overlap bias remains disclosed; four GPT-5.5 high-score samples were adjusted downward in `human_review_overrides.csv`.

Hard-fail score policy: hard fail rows retain the original judge total; they are not zeroed, capped, or excluded from averages. Hard fail count is reported separately.

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

## Missing Answer Handling

DeepSeek V4 Pro did not return an answer for `SGS-081` in the free-response run. The missing answer was preserved under the no-rescue policy and scored as 0 by the judge workflow. No manual answer was inserted.

## Deprecated Artifacts

Deprecated artifacts include old reconstructed SGS152 MCQ outputs, pre-final open-ended scoring artifacts, pre-standard Hard50 outputs, and old summary files. They are preserved under `archive/deprecated_reconstructed_results/`.

README, evaluation report, model error analysis, iteration notes, and results README now use `results/standard_20260703` as the formal evidence source.

## Manual Review Plan

Manual review packet: `results/standard_20260703/free_response_judge/manual_review_packet.csv`.

Confirmed decisions: `results/standard_20260703/free_response_judge/human_review_decisions.csv`.

Confirmed overrides: `results/standard_20260703/free_response_judge/human_review_overrides.csv`.

Adjudication notes: `results/standard_20260703/free_response_judge/adjudication_notes.md`.

Final adjudication counts: agree 71, adjust_score 4, hard_fail 3, missing_kept_zero 1, needs_human_attention 1.

## Release Decision

Current status: v0.5.0 release evidence is ready after confirmed free-response adjudication.

The SGS152 MCQ table remains the main leaderboard. Free-response is reported as judge-scored plus assistant-assisted project-owner confirmed adjudication. Robustness and Hard50 remain optional diagnostics and are not combined into a benchmark-wide aggregate leaderboard.

## Commands Run

```bash
python3 scripts/validate_benchmark.py
python3 scripts/lint_benchmark.py
python3 scripts/validate_hard50.py
python3 scripts/run_standard_benchmark.py --out-root results/standard_20260703 --smoke-timeout 900 --timeout 2400
python3 scripts/final_provenance_audit.py
make validate
make lint
git diff --check
```
