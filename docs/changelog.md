# Changelog

## v4.1.0 - Real-Model MCQ Validation

- Ran `gpt-5.5` through Codex CLI and `deepseek-chat` through the DeepSeek OpenAI-compatible endpoint.
- Added a sanitized MCQ run manifest under `results/model_run_manifest.json`.
- Updated MCQ scoring to generate leaderboard, badcase review, failure-mode breakdown, and diagnostic report files.
- Clarified that `SGS-mini-benchmark V4` is the portfolio package name and that the benchmark method remains V3-alpha.
- Updated reader-facing documentation to separate pipeline validation from model capability ranking.

## v4.0.0 - Portfolio-Ready V3 Iteration

- Added V3-alpha task set with 46 auditable task units.
- Added V3 task schema under `data/schema/task_schema_v3.json`.
- Added scoring protocol, Hard Gate definitions, judge protocol, trace requirements, and agent mode documentation.
- Added API-free demo runner with manifest, trace, judge outputs, aggregate metrics, report, and badcase gallery.
- Added schema validation, benchmark lint, Makefile commands, and GitHub Actions workflow.
- Updated README and overview documentation for clearer project entry.

## v1.0.0 - Repository Release

- Created a 100-item semiconductor gas-sensing benchmark.
- Added 82 multiple-choice and 18 free-response items.
- Added workflow fields: `scenario_stage`, `workflow_task`, `expected_output`, `tool_type`.
- Added per-option rationale and trap profiles.
- Added dataset card, schema, scoring rubric, taxonomy, safety/privacy documentation.
- Added evaluation scripts and example config.
