# Delivery Audit

## Delivery Scope

mini-benchmark 0.5.0 已形成 active SGS152 本地评测包。

| Asset | Status |
|---|---|
| `data/benchmark.json` | Active SGS152, 152 items |
| `data/failure_mined_bank.json` | 52-item design bank |
| `data/benchmark_sgs100_clean.json` | Legacy 100-item export |
| `data/benchmark_sgs100_robustness.json` | 40 robustness variants |
| `data/benchmark_sgs_hard50.json` | 50-item hard diagnostic set |
| `data/free_response_rubrics.json` | 30 free-response rubrics |
| `results/sgs152_merged/scored/` | Three-model SGS152 MCQ summaries |
| `reports/` | Project, model, design, retrospective, readiness reports |

## Validation Evidence

Required before release:

```bash
make validate
make validate-hard50
make lint
make lint-sgs100
make score-mcq
```

## Language And Consistency

- Active wording uses “failure-mined design bank” and “design insight” instead of source provenance.
- Added items use `SGS-FM-*` IDs and contain no source benchmark fields.
- README, dataset card, overview, evaluation recap, and build report describe the same SGS152 structure.
- Raw local model traces and external scratch data are not required for release review.

## Current Result Snapshot

| Model | SGS152 MCQ | Failure-mined MCQ |
|---|---:|---:|
| DeepSeek V4 Pro | 98 / 122 | 21 / 40 |
| GPT-5.5 | 95 / 122 | 15 / 40 |
| MiMo v2.5 Pro | 93 / 122 | 16 / 40 |
