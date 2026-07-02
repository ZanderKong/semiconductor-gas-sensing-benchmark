# Review Item Profile

Evaluation date: 2026-07-01

The following review items identify where answer choices create the strongest contrast.

| Model | Item | Scenario | Prediction | Gold | Review Pattern |
|---|---|---|---|---|---|
| deepseek-v4-pro | SGS-MINED2-017 | 局部结构 | B | A | hybridization_local_context_miss |
| mimo-v2.5-pro | SGS-MINED2-001 | 兼容性判断 | B | A | acid_metal_reactivity_miss |
| mimo-v2.5-pro | SGS-MINED2-017 | 局部结构 | B | A | hybridization_local_context_miss |

## Extension Patterns

| Target pattern | Stress-test idea |
|---|---|
| evidence_scope_mismatch | Add items where XPS O 1s shifts, EPR signals, and gas-response curves point to different interpretations. |
| metric_overoptimization | Add items where higher response changes recovery, drift, selectivity, or manufacturability. |
| safe_in_general_unsafe_here | Add options that are chemically valid in general but unsafe under the stated facility constraints. |
| table_analysis | Add compact tables that require LOD, drift, humidity correction, or batch-variance calculation. |
| mechanism_transfer_error | Add paired n-type / p-type and paper-tape / MOS transfer traps. |
