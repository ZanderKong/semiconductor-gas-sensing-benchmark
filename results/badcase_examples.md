# Badcase Examples

No wrong multiple-choice answers were observed for `gpt-5.5` or `deepseek-chat` in the current 82-item MC run.

This is itself diagnostic: the current MC set is useful for checking professional coverage and safety-boundary behavior, but it is not discriminative enough for strong models.

## Recommended Stress Badcases for v1.1

| Target failure mode | Stress-test idea |
|---|---|
| evidence_scope_mismatch | Add items where XPS O 1s changes, EPR, and gas response conflict. |
| metric_overoptimization | Add tradeoffs where higher response worsens recovery or drift. |
| safe_in_general_unsafe_here | Add choices that are chemically valid but unsafe under given facilities. |
| table_analysis | Add small data tables requiring LOD, drift, or batch-variance calculation. |
| mechanism_transfer_error | Add paired n-type / p-type or paper-tape / MOS transfer traps. |
