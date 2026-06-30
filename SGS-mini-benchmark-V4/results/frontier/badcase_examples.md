# Badcase Review

Evaluation date: 2026-06-30

The following cases were incorrectly answered in the current MCQ run.

| Model | Item | Scenario | Prediction | Gold | Failure Mode |
|---|---|---|---|---|---|
| deepseek-v4-pro | SGS-027 | 结果分析 | C | A | hysteresis_hidden |
| deepseek-v4-pro | SGS-028 | 结果分析 | C | B | metric_direction_error |
| deepseek-v4-pro | SGS-037 | 结果分析 | D | C | xps_vacancy_overclaim |
| deepseek-v4-pro | SGS-039 | 实验设计 | B | A | dopant_environment_interaction |
| deepseek-v4-pro | SGS-080 | 实验设计 | A | C | selectivity_claim_missing_matrix |
| deepseek-v4-pro | SGS-094 | 安全边界 | A | B | oxidizer_waste_mishandled |
| mimo-v2.5-pro | SGS-009 | 文献分析 | D | A | substituent_overlook |
| mimo-v2.5-pro | SGS-028 | 结果分析 | C | B | metric_direction_error |

## Recommended Stress Badcases

| Target failure mode | Stress-test idea |
|---|---|
| evidence_scope_mismatch | Add items where XPS O 1s shifts, EPR signals, and gas-response curves point to different interpretations. |
| metric_overoptimization | Add tradeoffs where higher response worsens recovery, drift, selectivity, or manufacturability. |
| safe_in_general_unsafe_here | Add options that are chemically valid in general but unsafe under the stated facility constraints. |
| table_analysis | Add compact tables that require LOD, drift, humidity correction, or batch-variance calculation. |
| mechanism_transfer_error | Add paired n-type / p-type and paper-tape / MOS transfer traps. |
