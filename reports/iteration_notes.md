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
- free-response judge output and confirmed adjudication files.

## 0.5.0 Evidence

The formal 0.5.0 evidence source is `results/standard_20260703`.

Main leaderboard:

| Model | SGS152 MCQ |
|---|---:|
| MiMo v2.5 Pro | 119 / 122 |
| Seed-2.1 | 118 / 122 |
| GPT-5.5 | 117 / 122 |
| DeepSeek V4 Pro | 115 / 122 |

Free-response is judge-scored plus assistant-assisted project-owner confirmed adjudication. GPT-5.5 judge overlap bias is disclosed, and four GPT-5.5 high-score samples were adjusted downward.

## Current Boundaries

- DeepSeek `SGS-081` free-response is missing and remains unrescued.
- GPT-5.5 judge overlap bias must be disclosed for free-response.
- Robustness and Hard50 are diagnostic layers only; no full-suite aggregate score should be reported.

## Finalization Status

1. Confirmed free-response decisions are stored in `results/standard_20260703/free_response_judge/human_review_decisions.csv`.
2. Confirmed score overrides are stored in `results/standard_20260703/free_response_judge/human_review_overrides.csv`.
3. Adjudication notes are stored in `results/standard_20260703/free_response_judge/adjudication_notes.md`.
4. `scripts/final_provenance_audit.py` must pass before publishing.
