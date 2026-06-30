# Leaderboard

Evaluation date: 2026-06-30

Scope: 82 MCQ after SGS-100 clean revision, GPT-5.5 plus Kimi 2.6 attempt.

Interpretation: This run adds GPT-5.5 and attempts Kimi 2.6 on the cleaned SGS-100 main set. Kimi 2.6 failed before returning answers because the local environment could not complete a TLS connection to the Moonshot endpoint.

| Model | Provider | Correct / Total | MCQ Accuracy | Safety Fail Rate | Notes |
|---|---|---:|---:|---:|---|
| gpt-5.5 | codex_cli | 80 / 82 | 97.6% | 0.0% | completed all MCQ items; stronger stress tests are required |
