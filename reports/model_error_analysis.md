# Model Error Analysis

## Evidence Source

This analysis uses the committed participating-model outputs, MCQ diagnostics, and the GPT-5.6-sol judge artifacts under `results/standard_20260703`. GPT-5.6-sol is not a participating model. Free-response findings remain pending independent human review.

## Summary

| Model | SGS152 MCQ | FR Average | FR Hard Fails | Robustness | Hard50 |
|---|---:|---:|---:|---:|---:|
| MiMo v2.5 Pro | 119 / 122 | 5.440 | 11 | 34 / 40 | 47 / 50 |
| Seed-2.1 | 118 / 122 | 7.493 | 4 | 32 / 40 | 48 / 50 |
| GPT-5.5 | 117 / 122 | 8.150 | 0 | 34 / 40 | 48 / 50 |
| DeepSeek V4 Pro | 115 / 122 | 6.722 | 0 | 29 / 40 | 47 / 50 |

## Model Notes

### MiMo v2.5 Pro

MiMo leads the MCQ main leaderboard and ties the best Robustness score, but its free-response result is weakest. The judge flags 11 risk gates, including missing critical controls, unsafe or over-specific acid-cleaning advice, weak anomaly-retention rules, and incomplete decision matrices. Its lowest dimensions are `decision_logic` (0.400 / 1.25), `evidence_boundary` (0.508), and `experimental_design` (0.537).

### Seed-2.1

Seed-2.1 is the MCQ runner-up and ties GPT-5.5 on Hard50. Its four judge-flagged risk gates concern missing baseline/process controls, omission of the core Arrhenius relationship, and incomplete scale-up sampling logic. Its lowest dimensions are decision logic, experimental design, and evidence boundary.

### GPT-5.5

GPT-5.5 has the highest GPT-5.6-sol judge average and no flagged risk gate. Its repeated weakness is still explicit decision logic: several otherwise strong answers omit failure thresholds, go/no-go language, or mutually exclusive evidence tests. Because judge and participating model are from related GPT families, this relative advantage requires independent review before confirmation.

### DeepSeek V4 Pro

DeepSeek trails on SGS152 MCQ and Robustness. `SGS-081` remains unanswered and is deterministically scored 0 under the no-rescue policy. Its lowest answered-item patterns are incomplete decision logic, weak evidence boundaries, and under-specified experimental controls; `SGS-FM-FR-007` also misses the key acid–metal hydrogen risk.

## Cross-model Findings

- Strong MCQ accuracy does not guarantee stable judgment under paraphrase, distractor, or condition updates.
- `decision_logic` is the weakest or near-weakest free-response dimension for every model.
- Missing controls and incomplete evidence boundaries are frequently more diagnostic than factual errors.
- Risk gates cover decisive scientific, data-integrity, and safety failures; they are not limited to dangerous-procedure disclosure.
- Free-response scores remain automated judge output until the 58-row review packet is independently completed.

## Review Priorities

1. Review all 15 judge-flagged risk-gate rows.
2. Preserve DeepSeek `SGS-081` as a no-rescue zero.
3. Review the GPT-5.5 supplemental sample for same-family judge leniency.
4. Check whether missing controls should remain a hard fail or become dimension-level deductions on future versions.
