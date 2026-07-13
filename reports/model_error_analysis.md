# Model Error Analysis — v0.6.0

## Cross-model findings

- Main MCQ scores are saturated at 94.26–97.54%; a few ambiguous or incorrect frozen Gold records can affect rank interpretation.
- The option audit identifies 56 defensible non-Gold answers, concentrated in overlapping mechanisms, complementary validation steps and under-specified best-action questions.
- Free-response deductions most often concern missing evidence boundaries, incomplete experimental matrices and absent go/no-go conditions. These are dimension issues, not automatic zeros.
- Confirmed material failures are limited to three MiMo responses: two data-integrity failures and one safety failure.
- DeepSeek `SGS-081` is a missing answer rather than a scientific judgment error and remains 0 under no-rescue scoring.

## Model-level summary

- GPT-5.5 has the highest reviewed free-response average, 8.213.
- Seed-2.1 averages 7.545; four historical gate labels were downgraded to dimension issues.
- DeepSeek V4 Pro averages 6.732 and has one missing answer.
- MiMo v2.5 Pro averages 5.257 before confirmed Hard Fail handling and 4.952 officially.

Detailed item-level rationales are in [`review/v0.6.0/04_free_response_adjudication/full_review_by_item.csv`](../review/v0.6.0/04_free_response_adjudication/full_review_by_item.csv).
