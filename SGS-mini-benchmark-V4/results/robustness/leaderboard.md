# Leaderboard

Evaluation date: 2026-06-30

Scope: 40 robustness variants for SGS-100 V4.

Interpretation: Robustness validation scores paraphrase stability, distractor resistance, contradiction sensitivity, adversarial safety behavior, and tool-observation following. Kimi was attempted but the local environment could not complete a TLS connection to the Moonshot endpoint, so this report scores completed DeepSeek and MiMo rows only.

| Model | Provider | Correct / Total | MCQ Accuracy | Safety Fail Rate | Notes |
|---|---|---:|---:|---:|---|
| mimo-v2.5-pro | openai_compatible | 36 / 40 | 90.0% | 25.0% | completed all MCQ items; stronger stress tests are required |
| deepseek-v4-pro | openai_compatible | 30 / 40 | 75.0% | 12.5% | completed all MCQ items; stronger stress tests are required |
