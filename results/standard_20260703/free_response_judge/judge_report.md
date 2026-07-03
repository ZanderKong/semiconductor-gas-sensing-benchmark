# Free-response Judge + Adjudication Report

This report starts from live model free-response outputs scored by a fixed ChatGPT/GPT-5.5 judge and applies assistant-assisted project-owner confirmed adjudication.

Bias note: the judge model overlaps with one participating model family. Four GPT-5.5 high-score samples were conservatively adjusted downward during adjudication.

Hard-fail score policy: hard fail rows retain the original judge total; they are not zeroed, capped, or excluded from averages. Hard fail count is reported separately.

| Model | Items | Total | Average | Hard Fails |
|---|---:|---:|---:|---:|
| deepseek-v4-pro | 30 | 189.10 | 6.303 | 0 |
| ep-20260703090429-qpmt7 | 30 | 206.65 | 6.888 | 0 |
| gpt-5.5 | 30 | 224.55 | 7.485 | 0 |
| mimo-v2.5-pro | 30 | 145.30 | 4.843 | 3 |

Adjudication files:

- `human_review_decisions.csv`
- `human_review_overrides.csv`
- `adjudication_notes.md`
