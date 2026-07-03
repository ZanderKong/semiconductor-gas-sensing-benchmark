# Manual Review Plan

## Source

Manual review queue:

`results/standard_20260703/free_response_judge/manual_review_queue.csv`

The queue is generated from GPT-5.5/ChatGPT judge output and includes hard-fail items plus low or disputed-score items.

Prepared review packet:

`results/standard_20260703/free_response_judge/manual_review_packet.csv`

The packet includes every item in `manual_review_queue.csv` plus deterministic supplemental spot checks so that each participating model has at least 9 of 30 free-response answers queued for human review.

## Sampling Rule

Review at least 30% of each model's 30 free-response answers.

The prepared packet currently includes:

| Model | Packet rows |
|---|---:|
| DeepSeek V4 Pro | 24 |
| Seed-2.1 | 17 |
| GPT-5.5 | 9 |
| MiMo v2.5 Pro | 30 |

The sample must include:

- hard-fail items;
- low-score items;
- high-score spot checks;
- safety-boundary items;
- Scientific Stress free-response items;
- judge comments that appear ambiguous or unusually severe;
- the missing-answer case `DeepSeek V4 Pro / SGS-081`.

## Required Items

`DeepSeek V4 Pro / SGS-081` must appear in the review record. It remains a missing answer under the no-rescue policy and should not be replaced with a manual answer.

## Human Override Policy

Human reviewers may correct judge scores when the written model answer and rubric support a different score. Corrections must not add missing model content or repair model answers.

Recommended override file:

`results/standard_20260703/free_response_judge/human_review_overrides.csv`

Blank template:

`results/standard_20260703/free_response_judge/human_review_overrides.template.csv`

Required columns:

```text
id,model_id,dimension,judge_score,human_score,override_reason,reviewer,date
```

Use `dimension=total_score` only when the reviewer is overriding the item-level total directly.

## Adjudication Notes

Recommended notes file:

`results/standard_20260703/free_response_judge/adjudication_notes.md`

Blank template:

`results/standard_20260703/free_response_judge/adjudication_notes.template.md`

Each note should include:

- item id;
- model id;
- reviewed answer evidence;
- rubric criterion;
- judge score and human decision;
- whether the change affects model-level summary.

## Release Impact

Manual review has been applied through `human_review_decisions.csv`, `human_review_overrides.csv`, and `adjudication_notes.md`. The SGS152 MCQ leaderboard remains the 0.5.0 main leaderboard. Free-response is reported as judge-scored plus assistant-assisted project-owner confirmed adjudication, with GPT-5.5 judge overlap bias disclosed and four GPT-5.5 high-score samples adjusted downward.
