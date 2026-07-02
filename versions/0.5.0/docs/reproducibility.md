# Reproducibility

## Build

```bash
make build-sgs152
```

The build command reconstructs `data/benchmark.json`, `data/benchmark.csv`, and `data/free_response_rubrics.json` from repository-contained inputs:

| Input | Role |
|---|---|
| `data/benchmark_sgs100_clean.json` | Domain Core Set |
| `data/scientific_stress_bank.json` | Scientific Stress Set |

## Validate

```bash
make validate
make validate-hard50
make lint
make lint-sgs100
```

These checks verify item counts, ID format, answer distribution, domain distribution, option structure, rubric coverage, safety/privacy patterns, robustness variants, and Hard Diagnostic Set coverage.

## Score

```bash
make score-mcq
```

The scoring target reads `results/sgs152_merged/model_outputs_sgs152_merged_all.csv` and writes scored summaries under `results/sgs152_merged/scored/`.

## Re-running Models

Model evaluation requires external model access for hosted models and the local Codex CLI path for GPT-5.5. The prompt is `eval/prompts/base_prompt.md`, and the runner is `eval/run_eval.py`.

## Current Artifacts

`results/sgs152_merged/scored/` contains the current MCQ summary artifacts. `results/hard50/scored_all/` contains Hard Diagnostic Set summaries. Robustness aggregate metrics are stored in `results/robustness_metrics.csv` and `results/robustness_model_summary.csv`.
