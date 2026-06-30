# Overview

SGS-100 V4 is a 100-item Chinese benchmark for semiconductor gas-sensing materials R&D.

The benchmark evaluates model behavior across:

- literature and evidence transfer;
- mechanism-boundary judgment;
- experiment and control design;
- abnormal-result diagnosis;
- gas-mixing and table calculation;
- safety-boundary decisions;
- process scale-up and productization gates;
- tool-use judgment.

## Active Files

| File | Purpose |
|---|---|
| `data/benchmark.json` | Active 100-item benchmark |
| `data/benchmark.csv` | Table-review export of the same benchmark |
| `data/benchmark_sgs100_clean.csv` | Clean main-set export with consistency fields |
| `data/free_response_rubrics.json` | Detailed 10-point rubrics for all free-response items |
| `data/benchmark_sgs100_robustness.csv` | Separate robustness variants for consistency diagnostics |
| `docs/dataset_card.md` | Dataset size, distribution, constraints, and safety notes |
| `docs/robustness_variant_design.md` | Robustness variant definitions and reporting logic |
| `docs/free_response_rubric_design.md` | Free-response rubric structure and hard-fail policy |
| `scripts/validate_benchmark.py` | Active benchmark validation |
| `scripts/lint_sgs100_benchmark.py` | Acceptance lint for main set, rubrics, variants, reports, and docs |
| `eval/run_eval.py` | Real-model MCQ runner |
| `eval/score_mcq.py` | MCQ scorer and report generator |

## Dataset Shape

SGS-100 follows the ChemBench mini proportions after rounding:

| Type | Count |
|---|---:|
| Multiple-choice | 82 |
| Free-response | 18 |
| Total | 100 |

The 82 MCQ items are designed to be more discriminative for strong models by using locally plausible distractors and balanced option lengths.

## Diagnostic Layers

The main set remains the source for primary MCQ accuracy and free-response judging.

The robustness layer is reported separately from main-set accuracy.

The free-response layer uses 10-point rubrics with explicit problem framing, evidence boundary, experimental design, decision logic, and safety/privacy criteria.
