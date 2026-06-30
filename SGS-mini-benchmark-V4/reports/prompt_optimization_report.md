# Prompt Optimization Report

SGS-100 V4 uses a single base prompt for comparable MCQ evaluation.

The 2026-06-30 clean-revision main-set run did not use prompt optimization.

The 2026-06-30 robustness run did not use prompt optimization.

DeepSeek and MiMo were scored with the same prompt file.

Kimi was attempted with the same prompt file, but the local environment could not complete a usable Moonshot API connection.

Future A/B tests should compare the following prompt variants:

| Prompt | Hypothesis |
|---|---|
| base_prompt | Strong baseline for direct-answer MCQ scoring |
| cot_disabled_prompt | Reduces verbose outputs and parser errors |
| tool_augmented_prompt | Improves calculation/table/safety-reference items |

Prompt optimization should be reported separately from model quality. This separation prevents prompt engineering effects from being confused with model capability.
