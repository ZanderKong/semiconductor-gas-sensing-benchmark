# Leaderboard

Evaluation date: 2026-06-29

Scope: 82 automatically scored multiple-choice questions from `data/benchmark_v1.json`.

Interpretation: the MCQ pipeline was validated with real GPT and DeepSeek model calls. The 100% scores show that the current MCQ subset is useful as a pipeline check but is not discriminative enough for strong models.

| Model | Provider | Correct / Total | MCQ Accuracy | Safety Fail Rate | Notes |
|---|---|---:|---:|---:|---|
| deepseek-chat | openai_compatible | 82 / 82 | 100.0% | 0.0% | completed all MCQ items; stronger stress tests are required |
| gpt-5.5 | codex_cli | 82 / 82 | 100.0% | 0.0% | completed all MCQ items; stronger stress tests are required |
