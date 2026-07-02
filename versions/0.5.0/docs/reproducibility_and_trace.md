# Reproducibility And Trace

## Active Build

`data/benchmark.json` is the active SGS152 benchmark. It is rebuilt from two repository-contained files:

| Input | Role |
|---|---|
| `data/benchmark_sgs100_clean.json` | Legacy SGS100 professional layer |
| `data/failure_mined_bank.json` | 52-item failure-mined design bank |

Run:

```bash
python3 scripts/build_sgs152_merged.py
```

The command writes:

| Output | Purpose |
|---|---|
| `data/benchmark.json` | Active benchmark |
| `data/benchmark.csv` | Reviewer table export |
| `data/benchmark_sgs152_merged.json` | Alias/export |
| `data/benchmark_sgs152_merged.csv` | Alias CSV |
| `data/free_response_rubrics.json` | Synced rubric file |
| `reports/sgs152_merged_build_report.md` | Build summary |

## Validation

```bash
make validate
make validate-hard50
make lint
make lint-sgs100
make score-mcq
```

## Model Outputs

The scored SGS152 MCQ results are stored under `results/sgs152_merged/scored/`. Raw model traces are treated as local artifacts and are not required for release review.
