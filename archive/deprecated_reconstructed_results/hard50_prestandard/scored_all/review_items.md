Deprecated reconstructed artifact. Not used as 0.5.0 final evidence.
# Review Item Profile

Evaluation date: 2026-06-30

The following review items identify where answer choices create the strongest contrast.

| Model | Item | Scenario | Prediction | Gold | Review Pattern |
|---|---|---|---|---|---|
| deepseek-v4-pro | SGS-HARD-016 | 条件更新 | B | D | condition_update_stickiness |
| deepseek-v4-pro | SGS-HARD-028 | 安全边界 | C | D | safety_gate_too_weak |
| gpt-5.5 | SGS-HARD-016 | 条件更新 | B | D | condition_update_stickiness |
| gpt-5.5 | SGS-HARD-028 | 安全边界 | C | D | safety_gate_too_weak |
| mimo-v2.5-pro | SGS-HARD-016 | 条件更新 | B | D | condition_update_stickiness |
| mimo-v2.5-pro | SGS-HARD-022 | 安全边界 | A | B | safety_gate_too_weak |
| mimo-v2.5-pro | SGS-HARD-028 | 安全边界 | C | D | safety_gate_too_weak |

## Extension Patterns

| Target pattern | Stress-test idea |
|---|---|
| evidence_scope_mismatch | Add items where XPS O 1s shifts, EPR signals, and gas-response curves point to different interpretations. |
| metric_overoptimization | Add items where higher response changes recovery, drift, selectivity, or manufacturability. |
| safe_in_general_unsafe_here | Add options that are chemically valid in general but unsafe under the stated facility constraints. |
| table_analysis | Add compact tables that require LOD, drift, humidity correction, or batch-variance calculation. |
| mechanism_transfer_error | Add paired n-type / p-type and paper-tape / MOS transfer traps. |
