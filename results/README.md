# Results

`results/standard_20260703` is the 0.5.0 live standard evidence source.

## Formal Evidence

| Path | Purpose | Git status |
|---|---|---|
| `standard_20260703/sgs152_mcq/model_outputs.csv` | Parsed SGS152 MCQ model outputs | committed |
| `standard_20260703/sgs152_mcq/manifest.json` | SGS152 MCQ live-run manifest | committed |
| `standard_20260703/sgs152_mcq/scored/` | SGS152 MCQ scored summaries | committed |
| `standard_20260703/sgs152_free_response/model_outputs.csv` | Parsed live free-response outputs | committed |
| `standard_20260703/sgs152_free_response/manifest.json` | Free-response live-run manifest | committed |
| `standard_20260703/free_response_judge/` | GPT-5.6-sol judge outputs and completed delegated-review evidence | committed except raw judge outputs |
| `standard_20260703/robustness/` | Optional Robustness diagnostic results | committed except raw outputs |
| `standard_20260703/hard50/` | Optional Hard50 diagnostic results | committed except raw outputs |
| `standard_20260703/analysis_core/` | SGS152 core analysis | committed |
| `standard_20260703/analysis_full/` | Full diagnostic analysis | committed |

Raw outputs exist locally under `raw_model_outputs/` and `raw_judge_outputs/` directories. They are ignored by git and should not be force-added.

GPT-5.6-sol is Judge-only and must not appear in participating-model output tables or leaderboards. Expert review records are published separately from Judge outputs; this iteration did not use an independent blind-review design. The prior GPT-5.5 Judge evidence is retained under `archive/judge_history/gpt-5.5_20260703/`.

## Main Leaderboard Scope

The 0.5.0 main leaderboard uses only `data/benchmark.json` / SGS152 Main Set.

Robustness and Hard50 are optional diagnostics. They do not enter the main leaderboard and must not be combined into a full-suite aggregate score.

## Deprecated Results

Pre-final reconstructed or generated artifacts have been moved to `archive/deprecated_reconstructed_results/`. They are preserved for traceability only and are not used as 0.5.0 final evidence.
