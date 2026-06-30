# SGS-100 Completion Audit

## Audit Date

2026-06-30.

## Scope

This audit maps the requested SGS-100 V4 completion requirements to current project evidence.

## Dataset Requirements

| Requirement | Evidence | Status |
|---|---|---|
| Main set remains 100 items | `data/benchmark.json`; `make validate` | Complete |
| Main set contains 82 MCQ and 18 free-response items | `data/benchmark.json`; `make validate` | Complete |
| Main-set items include consistency fields | `data/benchmark.json`; `scripts/lint_sgs100_benchmark.py` | Complete |
| Main-set items use `variant_type=base` | `data/benchmark.json`; `scripts/lint_sgs100_benchmark.py` | Complete |
| Main-set free-response count remains 18 | `data/free_response_rubrics.json`; `make lint-sgs100` | Complete |
| Every free-response item has a detailed 10-point rubric | `data/free_response_rubrics.json`; `make lint-sgs100` | Complete |
| Every free-response item has hard fails | `data/free_response_rubrics.json`; `make lint-sgs100` | Complete |
| Every free-response item has common failure modes | `data/free_response_rubrics.json`; `make lint-sgs100` | Complete |
| Clean CSV exists | `data/benchmark_sgs100_clean.csv` | Complete |
| Robustness CSV exists | `data/benchmark_sgs100_robustness.csv` | Complete |

## Robustness Requirements

| Requirement | Evidence | Status |
|---|---|---|
| Robustness variants are at least 36 items | `data/benchmark_sgs100_robustness.csv`; 40 variants | Complete |
| Every variant has `parent_task_id` | `scripts/lint_sgs100_benchmark.py` | Complete |
| Every parent task exists in the main set | `scripts/lint_sgs100_benchmark.py` | Complete |
| Every variant has `consistency_group_id` | `scripts/lint_sgs100_benchmark.py` | Complete |
| Variant types are controlled | `scripts/lint_sgs100_benchmark.py` | Complete |
| Expected consistency values are controlled | `scripts/lint_sgs100_benchmark.py` | Complete |
| Every group contains paraphrase, distractor, and contradiction variants | `scripts/lint_sgs100_benchmark.py` | Complete |
| Safety variants avoid hazardous execution details | `scripts/lint_sgs100_benchmark.py` | Complete |
| Tool-observation variants include explicit tool observations | `scripts/lint_sgs100_benchmark.py` | Complete |

## Report And Documentation Requirements

| Requirement | Evidence | Status |
|---|---|---|
| Revision report exists and covers requested fields | `reports/sgs100_revision_report.md` | Complete |
| Robustness report exists and covers requested fields | `reports/sgs100_robustness_report.md` | Complete |
| Robustness design doc exists | `docs/robustness_variant_design.md` | Complete |
| Free-response rubric design doc exists | `docs/free_response_rubric_design.md` | Complete |
| HR review guide exists | `docs/hr_review_guide.md` | Complete |
| Reader-facing overview reflects new artifacts | `README.md`, `docs/overview.md`, `docs/dataset_card.md` | Complete |
| Historical MCQ reports are marked as historical audits | `reports/sgs100_contextual_options_report.md`, `reports/sgs100_mcq_leakage_report.md` | Complete |

## Test Requirements

| Requirement | Evidence | Status |
|---|---|---|
| Acceptance lint passes | `make lint-sgs100` | Complete |
| Legacy validation passes | `make validate` | Complete |
| Repository lint passes | `make lint` | Complete |
| DeepSeek main-set MCQ test completes | `results/model_run_manifest_frontier.json` | Complete |
| MiMo main-set MCQ test completes | `results/model_run_manifest_frontier.json` | Complete |
| DeepSeek robustness test completes | `results/robustness/model_run_manifest_robustness_frontier.json` | Complete |
| MiMo robustness test completes | `results/robustness/model_run_manifest_robustness_frontier.json` | Complete |
| Kimi main-set MCQ test completes | `results/kimi_attempt/model_run_manifest_kimi_attempt.json` | Blocked by external API connection |
| Kimi 2.6 main-set MCQ test completes | `results/gpt55_kimi26/model_run_manifest_gpt55_kimi26.json` | Blocked by external API connection |
| Kimi 2.6 robustness test completes | `results/gpt55_kimi26/model_run_manifest_robustness_gpt55_kimi26.json` | Blocked by external API connection |
| Kimi connection diagnostics are recorded | `reports/kimi_connection_probe.md` | Complete |

## Latest Model Results

| Layer | Model | Result |
|---|---|---:|
| Main MCQ | `mimo-v2.5-pro` | 80 / 82 |
| Main MCQ | `gpt-5.5` | 80 / 82 |
| Main MCQ | `deepseek-v4-pro` | 76 / 82 |
| Robustness | `mimo-v2.5-pro` | 36 / 40 |
| Robustness | `gpt-5.5` | 35 / 40 |
| Robustness | `deepseek-v4-pro` | 30 / 40 |

## Kimi Blocker

The requested Kimi model test has been attempted and has not produced a score.

The configured model is `kimi-k2.7-code`.

The documented regional endpoint `https://api.moonshot.cn/v1` fails from the local environment during TLS connection setup.

The fallback endpoint `https://api.moonshot.ai/v1` is reachable but does not complete an authenticated chat-completions request with the supplied key.

The documented high-speed variant `kimi-k2.7-code-highspeed` was also tested with a minimal chat request and returned an empty server reply.

The Kimi 2.6 model `kimi-k2.6` was also tested on the main set and robustness set.

`kimi-k2.6` returned the same TLS EOF before any benchmark answer was produced.

The official documentation index at `https://platform.kimi.com/docs/llms.txt` was checked before the final direct HTTP probe.

The final direct probe used `https://api.moonshot.cn/v1`, which is the documented SDK base URL.

The project records this as an external API connection or credential blocker rather than a benchmark failure.

## Current Project Status

The benchmark design, local validation, clean main set, robustness layer, free-response rubric layer, DeepSeek tests, MiMo tests, reports, and documentation are complete.

The only incomplete item is Kimi scoring.

Kimi scoring requires a reachable Moonshot endpoint and a key accepted by that endpoint.
