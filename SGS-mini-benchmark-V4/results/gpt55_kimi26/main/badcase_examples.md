# Badcase Review

Evaluation date: 2026-06-30

The following cases were incorrectly answered in the current MCQ run.

| Model | Item | Scenario | Prediction | Gold | Failure Mode |
|---|---|---|---|---|---|
| gpt-5.5 | SGS-001 | 文献分析 | D | A | solubility_context_miss |
| gpt-5.5 | SGS-028 | 结果分析 | C | B | metric_direction_error |

## Recommended Stress Badcases

| Target failure mode | Stress-test idea |
|---|---|
| evidence_scope_mismatch | Add items where XPS O 1s shifts, EPR signals, and gas-response curves point to different interpretations. |
| metric_overoptimization | Add tradeoffs where higher response worsens recovery, drift, selectivity, or manufacturability. |
| safe_in_general_unsafe_here | Add options that are chemically valid in general but unsafe under the stated facility constraints. |
| table_analysis | Add compact tables that require LOD, drift, humidity correction, or batch-variance calculation. |
| mechanism_transfer_error | Add paired n-type / p-type and paper-tape / MOS transfer traps. |
