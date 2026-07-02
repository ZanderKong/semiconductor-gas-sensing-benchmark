# Review Item Profile

Evaluation date: 2026-07-02

The following review items identify where answer choices create the strongest contrast.

| Model | Item | Scenario | Prediction | Gold | Review Pattern |
|---|---|---|---|---|---|
| deepseek-v4-pro | SGS-009 | 文献分析 | B | A | substituent_overlook |
| deepseek-v4-pro | SGS-027 | 结果分析 | C | A | hysteresis_hidden |
| deepseek-v4-pro | SGS-028 | 结果分析 | D | B | metric_direction_error |
| deepseek-v4-pro | SGS-035 | 文献分析 | B | A | p_type_mechanism_transfer |
| deepseek-v4-pro | SGS-080 | 实验设计 | A | C | selectivity_claim_missing_matrix |
| deepseek-v4-pro | SGS-FM-001 | 失败机制复测 | C | A | domain_rule_boundary |
| deepseek-v4-pro | SGS-FM-003 | 失败机制复测 | B | A | specific_safety_hazard |
| deepseek-v4-pro | SGS-FM-004 | 失败机制复测 | A | B | domain_rule_boundary |
| gpt-5.5 | SGS-001 | 文献分析 | D | A | solubility_context_miss |
| gpt-5.5 | SGS-028 | 结果分析 | C | B | metric_direction_error |
| gpt-5.5 | SGS-FM-001 | 失败机制复测 | C | A | domain_rule_boundary |
| gpt-5.5 | SGS-FM-002 | 失败机制复测 | A | B | high_information_pattern_rule |
| gpt-5.5 | SGS-FM-004 | 失败机制复测 | A | B | domain_rule_boundary |
| gpt-5.5 | SGS-FM-005 | 失败机制复测 | D | C | domain_rule_boundary |
| gpt-5.5 | SGS-FM-006 | 失败机制复测 | B | A | structure_property_preference |
| gpt-5.5 | SGS-FM-007 | 失败机制复测 | C | E | domain_rule_boundary |
| mimo-v2.5-pro | SGS-004 | 实验设计 | A | D | oxidant_selectivity_gap |
| mimo-v2.5-pro | SGS-014 | 结果分析 | C | B | mediator_blank_drift_miss |
| mimo-v2.5-pro | SGS-057 | 结果分析 | A | C | product_constraint_ignored |
| mimo-v2.5-pro | SGS-058 | 结果分析 | B | D | packaging_transport_miss |
| mimo-v2.5-pro | SGS-067 | 安全边界 | B | C | single_property_selection |
| mimo-v2.5-pro | SGS-FM-002 | 失败机制复测 | D | B | high_information_pattern_rule |
| mimo-v2.5-pro | SGS-FM-003 | 失败机制复测 | B | A | specific_safety_hazard |
| mimo-v2.5-pro | SGS-FM-004 | 失败机制复测 | A | B | domain_rule_boundary |

## Extension Patterns

| Target pattern | Stress-test idea |
|---|---|
| evidence_scope_mismatch | Add items where XPS O 1s shifts, EPR signals, and gas-response curves point to different interpretations. |
| metric_overoptimization | Add items where higher response changes recovery, drift, selectivity, or manufacturability. |
| safe_in_general_unsafe_here | Add options that are chemically valid in general but unsafe under the stated facility constraints. |
| table_analysis | Add compact tables that require LOD, drift, humidity correction, or batch-variance calculation. |
| mechanism_transfer_error | Add paired n-type / p-type and paper-tape / MOS transfer traps. |
