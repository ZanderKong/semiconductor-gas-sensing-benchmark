# Semiconductor Gas-Sensing Mini-Benchmark 0.5.0

## Scope

Semiconductor Gas-Sensing Mini-Benchmark 是一个面向半导体气敏材料研发任务的领域 benchmark，用于评估大模型在机理推理、实验设计、证据边界、数据解释、安全约束和科学表达中的专业判断能力。

The benchmark converts semiconductor gas-sensing R&D tasks into scoreable, reviewable, and reproducible evaluation samples.

## Dataset Composition

| Logical Layer | File | Items | Purpose |
|---|---|---:|---|
| SGS152 Main Set | `data/benchmark.json` | 152 | Active benchmark |
| Domain Core Set | `data/benchmark_sgs100_clean.json` | 100 | Semiconductor gas-sensing R&D judgment |
| Scientific Stress Set | `data/scientific_stress_bank.json` | 52 | Rule-boundary, quantitative, structure-property, spectrum-pattern, and safety-risk stress testing |
| Robustness Set | `data/benchmark_sgs100_robustness.json` | 40 | Judgment consistency under paraphrase, distractors, condition updates, and tool observations |
| Hard Diagnostic Set | `data/benchmark_sgs_hard50.json` | 50 | Condition update, evidence conflict, safety gate, tradeoff, and tool-observation diagnostics |
| Free-response Rubrics | `data/free_response_rubrics.json` | 30 | Rubric definitions for open-ended review |

SGS152 Main Set contains 122 multiple-choice items and 30 free-response items. The automated leaderboard covers the 122 multiple-choice items. 30 free-response items are rubric-defined and are not included in the current automated MCQ leaderboard.

## Item Design Methodology

Each item is built around a decisive constraint: a material mechanism, experimental condition, evidence boundary, safety rule, quantitative relation, or domain convention that determines the answer.

Distractors are designed as locally plausible alternatives. Common distractor types include over-generalized scientific claims, intermediate-value traps, evidence-scope mismatches, safety-adjacent choices, and options that optimize one metric while violating a higher-priority constraint.

Scientific Stress Set items add compact high-pressure mechanisms. They test whether a model can preserve exact rules, units, signs, structure-property preferences, spectral patterns, and expert boundary conditions without relying on broad semantic familiarity.

## Scoring and Review Protocol

Multiple-choice scoring uses exact-match answer keys through `eval/score_mcq.py`. Reports aggregate results by model, domain, scenario stage, tool type, and failure mode.

Free-response scoring uses a 10-point rubric. The review dimensions are final answer alignment, rule or calculation path, unit and format control, distractor resistance, and traceability. Risk gates are applied before rubric scoring for safety, evidence integrity, privacy, tool use, and task-scope compliance.

## Model Evaluation Results

| Model | SGS152 MCQ | Accuracy | Domain Core MCQ | Scientific Stress MCQ |
|---|---:|---:|---:|---:|
| MiMo v2.5 Pro | 100 / 122 | 82.0% | 76 / 82 | 24 / 40 |
| DeepSeek V4 Pro | 99 / 122 | 81.2% | 78 / 82 | 21 / 40 |
| GPT-5.5 | 99 / 122 | 81.2% | 80 / 82 | 19 / 40 |

Robustness Set:

| Model | Correct / Total | Accuracy |
|---|---:|---:|
| MiMo v2.5 Pro | 36 / 40 | 90.0% |
| GPT-5.5 | 35 / 40 | 87.5% |
| DeepSeek V4 Pro | 30 / 40 | 75.0% |

Hard Diagnostic Set:

| Model | Correct / Total | Accuracy |
|---|---:|---:|
| DeepSeek V4 Pro | 48 / 50 | 96.0% |
| GPT-5.5 | 48 / 50 | 96.0% |
| MiMo v2.5 Pro | 47 / 50 | 94.0% |

## Error Analysis

The main separation comes from the Scientific Stress Set. Domain Core MCQ scores remain high, while Scientific Stress MCQ scores fall to 47.5% to 60.0%. The dominant model errors are high-information rule compression, quantitative precision loss, near-miss distractor selection, expert boundary-condition transfer, and safety specificity errors.

## Iteration Logic

0.5.0 keeps the benchmark in a pruning-ready state. Items that create stable model separation and traceable error modes should remain in the active set. Items that all frontier models answer correctly with shallow or identical reasoning should be moved to warm-up or archival status in a future release.

Next iterations should expand realistic lab-observation items, table-heavy calculations, spectrum interpretation, and paired variants that isolate one decisive experimental condition.

## Reproducibility

```bash
make build-sgs152
make validate
make validate-hard50
make lint
make lint-sgs100
make score-mcq
```

Root-level commands forward to `versions/0.5.0/`.

## Repository Map

| Path | Description |
|---|---|
| `data/` | Main datasets, diagnostic sets, and rubrics |
| `docs/dataset_card.md` | Dataset composition, intended use, and limitations |
| `docs/methodology.md` | Item design and benchmark construction method |
| `docs/scoring_protocol.md` | MCQ scoring, free-response review, and reporting protocol |
| `docs/risk_gates.md` | Safety, evidence, privacy, and tool-use review gates |
| `docs/reproducibility.md` | Build, validation, scoring, and result reproduction |
| `reports/evaluation_report.md` | Model results and split analysis |
| `reports/model_error_analysis.md` | Failure modes and error mechanisms |
| `reports/iteration_notes.md` | Version iteration logic and pruning plan |
| `eval/` | Runner and scoring utilities |
| `scripts/` | Build, validation, and lint scripts |
| `results/` | Scored summaries and model-output tables |

## Limitations

The current automated leaderboard covers multiple-choice items only. Free-response quality requires rubric-based review. The benchmark is designed for domain R&D judgment and should not be interpreted as a complete measure of general chemical intelligence or laboratory execution capability.
