# Benchmark Design Report

## Design Goal

Build a compact benchmark that turns semiconductor gas-sensing R&D judgment into structured, testable, and reproducible model-evaluation artifacts.

## Key Design Decisions

- Use ChemBench-style domain sampling, but rewrite all content for semiconductor gas-sensing materials.
- Use abstracted gas paper tape workflows with private details removed.
- Include per-option rationales to show why distractors are plausible but flawed.
- Add workflow-stage and tool-type labels to support more explanatory model evaluation.
- Treat safety and privacy as first-class evaluation dimensions.

## Product Architecture

The project treats a benchmark as a data product. The core architecture is:

- A stable dataset schema with question text, answer, rationale, option-level design notes, workflow labels, tool labels, and failure-mode labels.
- A quality-control layer that checks domain balance, answer-position balance, option leakage, workflow-field completeness, and privacy dependency levels.
- An evaluation layer that separates model invocation, output parsing, automatic MCQ scoring, and human review for free-response items.
- A reporting layer that explains results by domain, workflow stage, tool type, safety boundary, and likely error source.

## V3-Alpha Implementation

The project contains a V3-alpha task set and a portfolio-ready repository structure. The public benchmark version is V3-alpha.

| Layer | Implementation |
|---|---|
| Task data | `data/benchmark_v3_alpha.json` and `data/benchmark_v3_alpha.csv` |
| Schema | `data/schema/task_schema_v3.json` |
| Scoring | `docs/scoring_v3.md` and `docs/dimension_definition.md` |
| Hard Gate | `docs/hard_gates.md` |
| Judge protocol | `docs/judge_protocol.md` |
| Trace and reproducibility | `docs/reproducibility_and_trace.md` |
| Agent mode | `docs/agent_modes.md` |
| Demo runner | `eval/runner.py` |
| Real-model MCQ runner | `eval/run_eval.py` |
| MCQ scorer | `eval/score_mcq.py` |
| Validation | `scripts/validate_tasks.py`, `scripts/validate_v3_alpha_distribution.py`, and `scripts/lint_benchmark.py` |
| CI | `.github/workflows/validate.yml` |

The V3-alpha demo runner uses a local deterministic mock model. It verifies the task-unit evaluation flow without requiring model API credentials.

The MCQ runner has been validated with `gpt-5.5` through Codex CLI and `deepseek-v4-pro` through the DeepSeek OpenAI-compatible endpoint. The run confirms that model invocation, parsing, scoring, and reporting work end to end.
