# Reproducibility

## Build And Validation

```bash
make build-sgs100
make build-sgs152
make validate
make validate-hard50
make lint
make lint-sgs100
```

These commands validate SGS152 structure, Domain Core and Scientific Stress composition, free-response rubric coverage, Hard50 structure, and prompt support for variable MCQ option letters.

## Standard Live Run

The 0.5.0 RC evidence was generated with:

```bash
python3 scripts/run_standard_benchmark.py --out-root results/standard_20260703 --smoke-timeout 900 --timeout 2400
```

The run used:

- temperature 0;
- no internet access inside benchmark prompts;
- no tool assistance;
- same commit;
- same prompt;
- same item order;
- single sampling;
- no manual retry or rescue.

## Evidence Artifacts

| Artifact | Description |
|---|---|
| `results/standard_20260703/preflight_manifest.json` | Preflight and smoke-test record |
| `results/standard_20260703/sgs152_mcq/manifest.json` | SGS152 MCQ live-run manifest |
| `results/standard_20260703/sgs152_mcq/scored/model_results_summary.csv` | Main MCQ leaderboard |
| `results/standard_20260703/sgs152_free_response/manifest.json` | Free-response live-run manifest |
| `results/standard_20260703/free_response_judge/judge_manifest.json` | GPT-5.5 judge manifest |
| `results/standard_20260703/free_response_judge/scored_free_response_summary.csv` | Provisional free-response summary |
| `results/standard_20260703/free_response_judge/manual_review_queue.csv` | Human review queue |
| `results/standard_20260703/robustness/scored/model_results_summary.csv` | Optional Robustness diagnostics |
| `results/standard_20260703/hard50/scored/model_results_summary.csv` | Optional Hard50 diagnostics |

Raw outputs are present locally under `raw_model_outputs/` and `raw_judge_outputs/`. They are ignored by git to avoid committing raw model transcripts.

## Provenance Audit

Run:

```bash
python3 scripts/final_provenance_audit.py
```

The audit checks live-run manifests, expected results, Kimi exclusion, DeepSeek `SGS-081` missing-answer handling, judge bias disclosure, deprecated artifact isolation, and API-key leakage.

## Release Boundary

The main 0.5.0 leaderboard is SGS152 MCQ only. Free-response is judge-scored provisional until manual review is complete. Robustness and Hard50 are optional diagnostic layers and must not be aggregated into the main score.
