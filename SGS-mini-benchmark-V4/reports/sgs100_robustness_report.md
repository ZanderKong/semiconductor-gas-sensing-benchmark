# SGS-100 Robustness Report

Report date: 2026-06-30

## Summary

The robustness layer contains 40 variants across 12 consistency groups.

Variant-type distribution is {'adversarial_safety': 2, 'contradiction': 12, 'distractor': 12, 'paraphrase': 12, 'tool_observation_shift': 2}.
Expected-consistency distribution is {'changed_answer': 12, 'safety_refusal': 2, 'same_answer': 24, 'tool_result_followed': 2}.

## Groups

| Group | Parent Task | Variant Types | Expected Consistency |
|---|---|---|---|
| RG-SGS-001-SOLUBILITY | SGS-001 | contradiction, distractor, paraphrase | changed_answer, same_answer |
| RG-SGS-002-HUMIDITY | SGS-002 | contradiction, distractor, paraphrase | changed_answer, same_answer |
| RG-SGS-003-HUMIDITY-ARRAY | SGS-003 | contradiction, distractor, paraphrase | changed_answer, same_answer |
| RG-SGS-004-OXIDANT | SGS-004 | contradiction, distractor, paraphrase, tool_observation_shift | changed_answer, same_answer, tool_result_followed |
| RG-SGS-007-WATER-COMPETITION | SGS-007 | contradiction, distractor, paraphrase | changed_answer, same_answer |
| RG-SGS-009-SUBSTITUENT | SGS-009 | contradiction, distractor, paraphrase | changed_answer, same_answer |
| RG-SGS-028-METRIC-DIRECTION | SGS-028 | contradiction, distractor, paraphrase, tool_observation_shift | changed_answer, same_answer, tool_result_followed |
| RG-SGS-034-NTYPE-REDUCING | SGS-034 | contradiction, distractor, paraphrase | changed_answer, same_answer |
| RG-SGS-035-PTYPE-REDUCING | SGS-035 | contradiction, distractor, paraphrase | changed_answer, same_answer |
| RG-SGS-036-NTYPE-OXIDIZING | SGS-036 | contradiction, distractor, paraphrase | changed_answer, same_answer |
| RG-SGS-086-TOXIC-GAS-GATE | SGS-086 | adversarial_safety, contradiction, distractor, paraphrase | changed_answer, safety_refusal, same_answer |
| RG-SGS-097-CHLORINE-SAFETY | SGS-097 | adversarial_safety, contradiction, distractor, paraphrase | changed_answer, safety_refusal, same_answer |

## Representative Variants

- SGS-001-R01 uses `paraphrase` and expects `same_answer`.
- SGS-001-R02 uses `distractor` and expects `same_answer`.
- SGS-001-R03 uses `contradiction` and expects `changed_answer`.
- SGS-002-R01 uses `paraphrase` and expects `same_answer`.
- SGS-002-R02 uses `distractor` and expects `same_answer`.
- SGS-002-R03 uses `contradiction` and expects `changed_answer`.

## Follow-Up Metrics

consistency_rate is the share of paraphrase variants that preserve the parent answer.
distractor_resistance is the share of distractor variants that preserve the parent answer despite irrelevant information.
contradiction_sensitivity is the share of contradiction variants that change to the revised expected answer.
safety_regression_rate is the share of adversarial safety variants that fail to keep safety refusal behavior.
tool_integration_consistency is the share of tool-observation variants that follow the supplied tool result.

## Latest Robustness Evaluation

| Model | Overall | Consistency | Distractor Resistance | Contradiction Sensitivity | Safety Refusal | Tool Integration |
|---|---:|---:|---:|---:|---:|---:|
| deepseek-v4-pro | 75.0% | 91.7% | 75.0% | 66.7% | 100.0% | 0.0% |
| gpt-5.5 | 87.5% | 83.3% | 83.3% | 91.7% | 100.0% | 100.0% |
| mimo-v2.5-pro | 90.0% | 100.0% | 100.0% | 83.3% | 50.0% | 50.0% |
