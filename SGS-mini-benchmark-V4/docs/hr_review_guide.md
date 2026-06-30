# HR Review Guide

## Purpose

This guide provides the recommended reading path for a non-specialist reviewer who needs to assess the V4 benchmark package quickly and fairly.

## Project Positioning

SGS-100 V4 is a local benchmark package for evaluating large language models in semiconductor gas-sensing research workflows.

The benchmark focuses on judgment quality, evidence boundaries, safety awareness, experimental reasoning, and robustness under scenario changes.

The project does not provide hazardous gas synthesis procedures, proprietary formulas, supplier batch details, or executable laboratory recipes.

## Recommended Reading Order

| Step | File | What To Check |
|---:|---|---|
| 1 | `README.md` | Overall scope, dataset composition, available commands, and safety boundary |
| 2 | `reports/sgs100_completion_audit.md` | Completion status against V4 requirements |
| 3 | `reports/model_evaluation_recap.md` | Main model results, robustness results, and Kimi blocker status |
| 4 | `reports/benchmark_design_report.md` | Benchmark design intent and evaluation dimensions |
| 5 | `reports/sgs100_revision_report.md` | Dataset cleanup and V4 iteration work |
| 6 | `reports/sgs100_robustness_report.md` | Robustness variant design and model comparison |
| 7 | `reports/kimi_connection_probe.md` | Why Kimi was attempted but not scored |

## Main Evidence

| Evidence Type | File |
|---|---|
| Active benchmark dataset | `data/benchmark.json` |
| Reviewer-friendly table | `data/benchmark.csv` |
| Clean SGS-100 export | `data/benchmark_sgs100_clean.csv` |
| Robustness variants | `data/benchmark_sgs100_robustness.csv` |
| Free-response rubrics | `data/free_response_rubrics.json` |
| Validation scripts | `scripts/validate_benchmark.py`, `scripts/lint_benchmark.py`, `scripts/lint_sgs100_benchmark.py` |
| Model runner | `eval/run_eval.py` |

## Current Result Summary

| Layer | Model | Result |
|---|---|---:|
| Main MCQ | `mimo-v2.5-pro` | 80 / 82 |
| Main MCQ | `gpt-5.5` | 80 / 82 |
| Main MCQ | `deepseek-v4-pro` | 76 / 82 |
| Robustness | `mimo-v2.5-pro` | 36 / 40 |
| Robustness | `gpt-5.5` | 35 / 40 |
| Robustness | `deepseek-v4-pro` | 30 / 40 |

Kimi was attempted through the Moonshot OpenAI-compatible API, but the local environment did not receive a model answer from the endpoint.

The failed Kimi attempt is recorded as an external API connection or credential acceptance blocker, not as a model-performance score.

## Validation Commands

```bash
make validate
make lint
make lint-sgs100
```

The V4 package is designed so that these commands can be run from the `SGS-mini-benchmark-V4` folder.

## Reviewer Notes

The main benchmark reports MCQ accuracy only on the 82 multiple-choice items.

The 18 free-response items are rubric-complete and require human or judge scoring before they can be reported as model performance.

The robustness layer is separate from main accuracy because it tests stability, resistance to distractors, contradiction handling, safety refusal, and tool-observation updates.

The V4 folder is self-contained for local review.
