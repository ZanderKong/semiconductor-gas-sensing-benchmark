# Manual Review Plan

## Source

Manual review queue:

`results/standard_20260703/free_response_judge/manual_review_queue.csv`

The queue is generated from GPT-5.5/ChatGPT judge output and includes hard-fail items plus low or disputed-score items.

## Sampling Rule

Review at least 30% of each model's 30 free-response answers.

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

Required columns:

```text
id,model_id,dimension,judge_score,human_score,override_reason,reviewer,date
```

Use `dimension=total_score` only when the reviewer is overriding the item-level total directly.

## Adjudication Notes

Recommended notes file:

`results/standard_20260703/free_response_judge/adjudication_notes.md`

Each note should include:

- item id;
- model id;
- reviewed answer evidence;
- rubric criterion;
- judge score and human decision;
- whether the change affects model-level summary.

## Release Impact

Until manual review is complete, free-response results remain judge-scored provisional results. The SGS152 MCQ leaderboard can be used as the 0.5.0 main leaderboard, but free-response ranking should not be presented as unbiased final evidence.
