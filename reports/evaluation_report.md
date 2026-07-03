# Evaluation Report

## 评测范围

本报告记录 Semiconductor Gas-Sensing Mini-Benchmark 0.5.0 live RC run。

正式证据来源：

`results/standard_20260703`

主榜只基于 `data/benchmark.json`，即 SGS152 Main Set 的 152 题。其中 122 道 MCQ 是当前主 leaderboard；30 道 free-response 是 GPT-5.5/ChatGPT judge-scored provisional result，完成人工复核前不作为无偏最终排名。

Robustness 40 和 Hard50 50 是 optional diagnostic results，不进入主榜，不生成 full-suite aggregate score。

## 运行设置

正式阶段 manifest 记录：

- commit：`70b77e8f...`
- `working_tree_dirty=false`
- `internet_access=false`
- `tool_assistance=false`
- temperature：0
- same prompt
- same item order
- single sampling
- no rescue / no manual retry

Kimi smoke test failed with 401 Unauthorized, so Kimi is excluded from the main leaderboard.

## SGS152 MCQ Main Leaderboard

| Model | Provider | Correct / Total | Accuracy | Safety Fail Rate |
|---|---|---:|---:|---:|
| MiMo v2.5 Pro | xiaomimimo | 119 / 122 | 97.54% | 6.25% |
| Seed-2.1 | volcengine | 118 / 122 | 96.72% | 6.25% |
| GPT-5.5 | codex_cli | 117 / 122 | 95.90% | 6.25% |
| DeepSeek V4 Pro | deepseek | 115 / 122 | 94.26% | 0.00% |

## Free-response Status

| Model | Average | Hard Fails |
|---|---:|---:|
| GPT-5.5 | 7.568 | 0 |
| Seed-2.1 | 6.888 | 0 |
| DeepSeek V4 Pro | 6.303 | 0 |
| MiMo v2.5 Pro | 4.843 | 3 |

Free-response was judged by GPT-5.5/ChatGPT. Because GPT-5.5 is also a participating model, these scores have judge overlap bias. `manual_review_queue.csv` has been generated, and human review is pending.

DeepSeek V4 Pro did not return `SGS-081`; the missing answer is preserved under the no-rescue policy and scored as 0.

## Optional Diagnostic Results

Robustness:

| Model | Correct / Total | Accuracy |
|---|---:|---:|
| GPT-5.5 | 34 / 40 | 85.0% |
| MiMo v2.5 Pro | 34 / 40 | 85.0% |
| Seed-2.1 | 32 / 40 | 80.0% |
| DeepSeek V4 Pro | 29 / 40 | 72.5% |

Hard50:

| Model | Correct / Total | Accuracy |
|---|---:|---:|
| GPT-5.5 | 48 / 50 | 96.0% |
| Seed-2.1 | 48 / 50 | 96.0% |
| DeepSeek V4 Pro | 47 / 50 | 94.0% |
| MiMo v2.5 Pro | 47 / 50 | 94.0% |

These diagnostic results are useful for failure-mode analysis and follow-up item calibration. They should not be merged into a single total score.

## Evidence Files

| Artifact | Path |
|---|---|
| SGS152 MCQ outputs | `results/standard_20260703/sgs152_mcq/model_outputs.csv` |
| SGS152 MCQ manifest | `results/standard_20260703/sgs152_mcq/manifest.json` |
| SGS152 MCQ scored summary | `results/standard_20260703/sgs152_mcq/scored/model_results_summary.csv` |
| Free-response live outputs | `results/standard_20260703/sgs152_free_response/model_outputs.csv` |
| Free-response judge summary | `results/standard_20260703/free_response_judge/scored_free_response_summary.csv` |
| Manual review queue | `results/standard_20260703/free_response_judge/manual_review_queue.csv` |
| Robustness scored summary | `results/standard_20260703/robustness/scored/model_results_summary.csv` |
| Hard50 scored summary | `results/standard_20260703/hard50/scored/model_results_summary.csv` |

Raw outputs exist locally under `results/standard_20260703/**/raw_model_outputs/` and `results/standard_20260703/free_response_judge/raw_judge_outputs/`. They are ignored by git and not committed.

## Release Interpretation

0.5.0 is currently a live RC. The SGS152 MCQ leaderboard is the main benchmark result. Free-response should remain provisional until manual review resolves hard-fail and disputed-score samples. Robustness and Hard50 are optional diagnostic layers.
