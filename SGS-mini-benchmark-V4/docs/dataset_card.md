# Dataset Card

## Active Dataset

The active V4 dataset is `data/benchmark.json`, a 100-item Chinese benchmark for semiconductor gas-sensing materials R&D. `data/benchmark.csv` is the table-review export of the same items.

`data/benchmark_sgs100_clean.csv` is the clean main-set export with consistency fields.

`data/free_response_rubrics.json` stores detailed rubrics for the 18 free-response items.

`data/benchmark_sgs100_robustness.csv` stores a separate robustness layer and is not mixed into primary accuracy.

## Size

| Split | Count |
|---|---:|
| Multiple-choice | 82 |
| Free-response | 18 |
| Total | 100 |

## Domain Distribution

| Domain | Count |
|---|---:|
| organic_chemistry | 19 |
| physical_chemistry | 14 |
| inorganic_chemistry | 14 |
| materials_science | 14 |
| general_chemistry | 11 |
| analytical_chemistry | 10 |
| technical_chemistry | 10 |
| toxicity_and_safety | 8 |

The type and domain distributions follow the ChemBench mini subset proportions after rounding to a 100-item semiconductor gas-sensing benchmark.

## MCQ Constraints

All active MCQ items use four options. The active validation gate checks that:

- every option has at least 10 Chinese characters;
- longest / shortest option length is at most 1.5;
- the correct option is not the longest option;
- A/B/C/D answers are balanced at 21 / 21 / 20 / 20;
- option text avoids obvious answer-leakage terms;
- every option has a rationale explaining when it is locally plausible and why it is or is not the best current action.

## Consistency Groups

Every main-set item includes `variant_type`, `parent_task_id`, `expected_consistency`, `consistency_group_id`, and `consistency_check`.

Main-set items use `variant_type=base`.

Selected base items anchor robustness groups.

Robustness variants test paraphrase stability, distractor resistance, contradiction sensitivity, adversarial safety behavior, and tool-result integration.

## Free-Response Rubrics

Each free-response item contains a richer materials R&D scenario.

Each free-response item has a 10-point rubric.

Each rubric scores problem framing, evidence boundary, experimental design, decision logic, and safety/privacy.

Each free-response item includes key points, hard fails, and common failure modes.

## Safety And Privacy

The dataset uses public knowledge and abstracted R&D situations. It does not include private formulas, customer information, sensitive procurement data, or actionable hazardous-gas SOPs.
