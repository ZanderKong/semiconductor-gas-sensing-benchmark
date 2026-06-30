# Leaderboard

Evaluation date: 2026-06-30

Scope: 82 MCQ after SGS-100 clean revision.

Interpretation: Frontier external-model MCQ validation on the cleaned SGS-100 main set. Kimi was attempted in the runner but the local environment could not complete a TLS connection to the Moonshot endpoint, so this report scores completed DeepSeek and MiMo rows only.

| Model | Provider | Correct / Total | MCQ Accuracy | Safety Fail Rate | Notes |
|---|---|---:|---:|---:|---|
| mimo-v2.5-pro | openai_compatible | 80 / 82 | 97.6% | 0.0% | completed all MCQ items; stronger stress tests are required |
| deepseek-v4-pro | openai_compatible | 76 / 82 | 92.7% | 12.5% | completed all MCQ items; stronger stress tests are required |
