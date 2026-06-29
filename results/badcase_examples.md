# Badcase Review

Evaluation date: 2026-06-29

No wrong multiple-choice answers were observed in the current GPT and DeepSeek MCQ run.

This result is diagnostic rather than conclusive. The current MCQ subset checks coverage, parsing, and safety-boundary behavior, but it does not separate strong models.

## Recommended Stress Badcases

| Target failure mode | Stress-test idea |
|---|---|
| evidence_scope_mismatch | Add items where XPS O 1s shifts, EPR signals, and gas-response curves point to different interpretations. |
| metric_overoptimization | Add tradeoffs where higher response worsens recovery, drift, selectivity, or manufacturability. |
| safe_in_general_unsafe_here | Add options that are chemically valid in general but unsafe under the stated facility constraints. |
| table_analysis | Add compact tables that require LOD, drift, humidity correction, or batch-variance calculation. |
| mechanism_transfer_error | Add paired n-type / p-type and paper-tape / MOS transfer traps. |
