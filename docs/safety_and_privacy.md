# Safety and Privacy

## Privacy Principles

This benchmark is built from abstract materials R&D problem types with private details removed. It does not disclose proprietary experimental details.

The dataset does not include:

- Private formulation ratios.
- Private sample IDs.
- Customer or supplier-sensitive information.
- Internal experimental raw data.
- Non-public performance conclusions.
- Reproducible hazardous procedures.

## Private Dependency Levels

| Level | Meaning |
|---|---|
| `none` | Public or general domain knowledge |
| `analog` | Similar workflow pattern, abstracted and de-identified |
| `seed_entity` | A reagent, gas, instrument, or method used as a generic entity seed |
| `private_combination` | A private formulation combination, ratio, sample ID, or conclusion |

Current dataset counts:

- `none`: 86
- `analog`: 6
- `seed_entity`: 8
- `private_combination`: 0

## Safety Scope

Safety questions are evaluation items, not SOPs. They are intentionally written to test whether a model recognizes when to refuse, escalate, or require engineering controls.

The benchmark avoids giving actionable hazardous procedures. It emphasizes:

- Go/no-go conditions.
- Engineering controls.
- Tail-gas treatment.
- Authorization and SOP requirements.
- Waste classification.
- Evidence and safety boundaries.

## High-Risk Failure Examples

- Recommending open-bench chlorine generation.
- Suggesting toxic gas tests without alarm, ventilation, and tail-gas controls.
- Treating odor as a safety monitor.
- Disposing silver-containing waste down the drain.
- Scaling hazardous solvent use without substitution and exposure review.
