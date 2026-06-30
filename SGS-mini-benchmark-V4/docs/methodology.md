# Methodology

## Design Goal

SGS-100 V4 is designed as a compact, portfolio-facing benchmark for semiconductor gas-sensing materials R&D. It keeps the total size at 100 items while preserving a ChemBench-like balance between automatically scored MCQ items and open-ended reasoning items.

## Proportioning

The active dataset uses the ChemBench mini subset as the reference for broad chemistry coverage:

- 82 multiple-choice items.
- 18 free-response items.
- 8 chemistry/materials domains mapped into gas-sensing scenarios.

The domain counts are rounded to 100 items and then rewritten as semiconductor gas-sensing tasks.

## MCQ Hardening

The MCQ layer was rewritten to reduce answer leakage:

- four options have similar Chinese-character lengths;
- every option is locally plausible under some premise;
- wrong options represent stage errors, overextended evidence, unresolved uncertainty, secondary metrics, conservative-but-unanswering safety moves, or process changes that introduce new confounders;
- correct answers are balanced across A/B/C/D;
- option rationales explain both local plausibility and current-context priority.

## Consistency Probes

Some items are deliberately grouped into nearby variants. These groups test whether the model maintains stable principles across related settings, for example humidity drift, n-type/p-type response direction, data-boundary claims, and toxic-gas safety escalation.
