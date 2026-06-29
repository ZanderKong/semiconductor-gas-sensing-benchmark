# Prompt Optimization Report

This release uses a single low-temperature base prompt for comparable MCQ evaluation. No prompt optimization was used in the reported GPT and DeepSeek leaderboard.

Future A/B tests should compare the following prompt variants:

| Prompt | Hypothesis |
|---|---|
| base_prompt | Strong baseline for direct-answer MCQ scoring |
| cot_disabled_prompt | Reduces verbose outputs and parser errors |
| tool_augmented_prompt | Improves calculation/table/safety-reference items |

Prompt optimization should be reported separately from model quality. This separation prevents prompt engineering effects from being confused with model capability.
