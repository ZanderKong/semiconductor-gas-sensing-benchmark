Deprecated reconstructed artifact. Not used as 0.5.0 final evidence.
# Review Item Profile

Evaluation date: 2026-07-02

The following review items identify where answer choices create the strongest contrast.

| Model | Item | Scenario | Prediction | Gold | Review Pattern |
|---|---|---|---|---|---|
| DeepSeek V4 Pro | SGS-005 | 文献分析 | B | A | solution_to_film_overclaim |
| DeepSeek V4 Pro | SGS-006 | 结果分析 | A | B | partition_recovery_tradeoff |
| DeepSeek V4 Pro | SGS-007 | 结果分析 | A | C | humidity_competition_miss |
| DeepSeek V4 Pro | SGS-009 | 文献分析 | B | A | substituent_overlook |
| DeepSeek V4 Pro | SGS-FM-009 | 燃烧计量 | A | B | combustion_ratio_error |
| DeepSeek V4 Pro | SGS-FM-010 | 燃烧计量 | A | B | combustion_ratio_error |
| DeepSeek V4 Pro | SGS-FM-011 | 单元排列 | A | B | reactor_arrangement_method_miss |
| DeepSeek V4 Pro | SGS-FM-012 | 单元排列 | B | A | reactor_arrangement_method_miss |
| GPT-5.5 | SGS-010 | 文献分析 | A | B | reversibility_not_validated |
| GPT-5.5 | SGS-011 | 结果分析 | A | C | percolation_repeatability_miss |
| GPT-5.5 | SGS-FM-003 | 结构判断 | A | B | oxidation_state_structure_overreach |
| GPT-5.5 | SGS-FM-004 | 结构判断 | A | B | oxidation_state_structure_overreach |
| GPT-5.5 | SGS-FM-005 | 清洗风险 | A | C | oxidizing_acid_passivation_miss |
| GPT-5.5 | SGS-FM-006 | 清洗风险 | A | B | oxidizing_acid_passivation_miss |
| GPT-5.5 | SGS-FM-007 | 聚合条件 | B | A | cationic_polymerization_solvent_error |
| GPT-5.5 | SGS-FM-008 | 聚合条件 | A | B | cationic_polymerization_solvent_error |
| MiMo v2.5 Pro | SGS-001 | 文献分析 | B | A | solubility_context_miss |
| MiMo v2.5 Pro | SGS-002 | 结果分析 | A | B | humidity_mechanism_blur |
| MiMo v2.5 Pro | SGS-003 | 实验设计 | A | C | cross_sensitivity_misuse |
| MiMo v2.5 Pro | SGS-004 | 实验设计 | A | D | oxidant_selectivity_gap |
| MiMo v2.5 Pro | SGS-008 | 安全边界 | A | D | safety_priority_miss |
| MiMo v2.5 Pro | SGS-017 | 结果分析 | B | A | dynamic_range_miss |
| MiMo v2.5 Pro | SGS-FM-001 | 兼容性判断 | B | A | acid_metal_reactivity_miss |
| MiMo v2.5 Pro | SGS-FM-002 | 兼容性判断 | A | B | acid_metal_reactivity_miss |

## Extension Patterns

| Target pattern | Stress-test idea |
|---|---|
| evidence_scope_mismatch | Add items where XPS O 1s shifts, EPR signals, and gas-response curves point to different interpretations. |
| metric_overoptimization | Add items where higher response changes recovery, drift, selectivity, or manufacturability. |
| safe_in_general_unsafe_here | Add options that are chemically valid in general but unsafe under the stated facility constraints. |
| table_analysis | Add compact tables that require LOD, drift, humidity correction, or batch-variance calculation. |
| mechanism_transfer_error | Add paired n-type / p-type and paper-tape / MOS transfer traps. |
