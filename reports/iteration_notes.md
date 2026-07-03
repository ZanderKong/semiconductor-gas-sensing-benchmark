# Iteration Notes

## 0.4.0 To 0.5.0

0.4.0 established the Domain Core structure and showed that semiconductor gas-sensing R&D judgment can be converted into structured, scoreable tasks.

0.5.0 adds:

- SGS152 Main Set;
- Scientific Stress Set;
- Robustness Set as optional diagnostics;
- Hard50 as optional diagnostics;
- variable option-letter support in the MCQ prompt;
- live standard-run provenance under `results/standard_20260703`;
- free-response judge output and manual review queue.

## 0.5.0 RC Evidence

The formal 0.5.0 RC evidence source is `results/standard_20260703`.

Main leaderboard:

| Model | SGS152 MCQ |
|---|---:|
| MiMo v2.5 Pro | 119 / 122 |
| Seed-2.1 | 118 / 122 |
| GPT-5.5 | 117 / 122 |
| DeepSeek V4 Pro | 115 / 122 |

Free-response is judge-scored provisional. Human review is pending.

## Current Boundaries

- Kimi failed smoke testing with 401 Unauthorized and is excluded from the main leaderboard.
- DeepSeek `SGS-081` free-response is missing and remains unrescued.
- GPT-5.5 judge overlap bias must be disclosed for free-response.
- Robustness and Hard50 are diagnostic layers only; no full-suite aggregate score should be reported.

## Before Final v0.5.0

1. Complete human review for `results/standard_20260703/free_response_judge/manual_review_queue.csv`.
2. Apply any human-review overrides in the prescribed override file.
3. Re-run `scripts/final_provenance_audit.py`.
4. Mark the package as final only after the audit passes.
