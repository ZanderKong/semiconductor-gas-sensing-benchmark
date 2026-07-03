# Review Item Profile

Evaluation date: 2026-07-03

The following review items identify where answer choices create the strongest contrast.

| Model | Item | Scenario | Prediction | Gold | Review Pattern |
|---|---|---|---|---|---|
| deepseek-v4-pro | SGS-001 | 文献分析 | D | A | solubility_context_miss |
| deepseek-v4-pro | SGS-009 | 文献分析 | B | A | substituent_overlook |
| deepseek-v4-pro | SGS-027 | 结果分析 | C | A | hysteresis_hidden |
| deepseek-v4-pro | SGS-028 | 结果分析 | C | B | metric_direction_error |
| deepseek-v4-pro | SGS-058 | 结果分析 | B | D | packaging_transport_miss |
| deepseek-v4-pro | SGS-080 | 实验设计 | A | C | selectivity_claim_missing_matrix |
| deepseek-v4-pro | SGS-FM-017 | 局部结构 | B | A | hybridization_local_context_miss |
| ep-20260703090429-qpmt7 | SGS-027 | 结果分析 | C | A | hysteresis_hidden |
| ep-20260703090429-qpmt7 | SGS-057 | 结果分析 | A | C | product_constraint_ignored |
| ep-20260703090429-qpmt7 | SGS-094 | 安全边界 | A | B | oxidizer_waste_mishandled |
| ep-20260703090429-qpmt7 | SGS-FM-017 | 局部结构 | B | A | hybridization_local_context_miss |
| gpt-5.5 | SGS-001 | 文献分析 | D | A | solubility_context_miss |
| gpt-5.5 | SGS-017 | 结果分析 | D | A | dynamic_range_miss |
| gpt-5.5 | SGS-028 | 结果分析 | C | B | metric_direction_error |
| gpt-5.5 | SGS-051 | 实验进行 | D | A | grain_stability_tradeoff_miss |
| gpt-5.5 | SGS-FM-009 | 燃烧计量 | A | B | combustion_ratio_error |
| mimo-v2.5-pro | SGS-014 | 结果分析 | C | B | mediator_blank_drift_miss |
| mimo-v2.5-pro | SGS-067 | 安全边界 | B | C | single_property_selection |
| mimo-v2.5-pro | SGS-FM-017 | 局部结构 | B | A | hybridization_local_context_miss |

## Extension Patterns

| Target pattern | Stress-test idea |
|---|---|
| evidence_scope_mismatch | Add items where XPS O 1s shifts, EPR signals, and gas-response curves point to different interpretations. |
| metric_overoptimization | Add items where higher response changes recovery, drift, selectivity, or manufacturability. |
| safe_in_general_unsafe_here | Add options that are chemically valid in general but unsafe under the stated facility constraints. |
| table_analysis | Add compact tables that require LOD, drift, humidity correction, or batch-variance calculation. |
| mechanism_transfer_error | Add paired n-type / p-type and paper-tape / MOS transfer traps. |
