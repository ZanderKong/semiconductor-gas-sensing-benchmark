# Leaderboard

Evaluation date: 2026-06-27

Scope: 82 automatically scored multiple-choice questions. The 18 free-response questions are kept for human or LLM-as-judge review.

Interpretation: the current MCQ pipeline has been validated end to end, but the completed runs show insufficient discriminative power for strong models. These numbers should be treated as pipeline evidence, not as a stable capability ranking.

| Model | Correct / Total | MCQ Run Status | Safety Fail Rate | Notes |
|---|---:|---:|---:|---|
| deepseek-chat | 82 / 82 | completed all MCQ items | 0.0% | pipeline completed; MCQ subset not discriminative enough |
| gpt-5.5 | 82 / 82 | completed all MCQ items | 0.0% | pipeline completed; MCQ subset not discriminative enough |
