# Manual Review Plan

## Status

GPT-5.6-sol has scored all 120 free-response answers. Independent human review is pending; no confirmed decisions or overrides exist in the current evidence directory.

## Review Packet

`results/standard_20260703/free_response_judge/manual_review_packet.csv`

The 58-row packet includes:

- every judge hard fail;
- every score below 7.0;
- the DeepSeek `SGS-081` no-rescue missing answer;
- risk-focused supplemental samples until every model reaches at least 9 of 30 answers.

| Model | Review Rows |
|---|---:|
| DeepSeek V4 Pro | 13 |
| Seed-2.1 | 9 |
| GPT-5.5 | 9 |
| MiMo v2.5 Pro | 27 |

## Human Review Policy

- Compare only the frozen question, rubric, reference answer, original model answer and judge record.
- Do not add missing content or rescue a participating model's answer.
- Keep a missing answer at 0.
- Record every changed dimension, total and reason.
- Do not change the current status from pending until all required human fields are complete.

Templates:

- `human_review_decisions.template.csv`
- `human_review_overrides.template.csv`
- `adjudication_notes.template.md`

The historical GPT-5.5 judge adjudication is preserved under `archive/judge_history/gpt-5.5_20260703/` and must not be copied into the new scoring baseline.
