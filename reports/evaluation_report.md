# Evaluation Report

## 评测范围

本报告记录 Semiconductor Gas-Sensing Mini-Benchmark 0.5.0 live standard run 和 confirmed free-response adjudication。

正式证据来源：

`results/standard_20260703`

主榜只基于 `data/benchmark.json`，即 SGS152 Main Set 的 152 题。其中 122 道 MCQ 是当前 main leaderboard；30 道 free-response 是 GPT-5.5/ChatGPT judge-scored + assistant-assisted project-owner confirmed adjudication。

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
| GPT-5.5 | 7.485 | 0 |
| Seed-2.1 | 6.888 | 0 |
| DeepSeek V4 Pro | 6.303 | 0 |
| MiMo v2.5 Pro | 4.843 | 3 |

Free-response was judged by GPT-5.5/ChatGPT and then confirmed through assistant-assisted project-owner adjudication. Because GPT-5.5 is also a participating model, judge overlap bias remains disclosed; four GPT-5.5 high-score samples were adjusted downward:

- `SGS-030 + gpt-5.5`: 7.65 -> 7.15
- `SGS-032 + gpt-5.5`: 8.10 -> 7.35
- `SGS-099 + gpt-5.5`: 8.45 -> 7.85
- `SGS-FM-FR-004 + gpt-5.5`: 8.40 -> 7.75

Hard-fail score policy: hard fail rows retain the original judge total; they are not zeroed, capped, or excluded from averages. Hard fail count is reported separately.

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

Integrated diagnostic reading: MiMo leads SGS152 MCQ and ties GPT-5.5 on Robustness, but its free-response profile contains 3 retained hard fails. GPT-5.5 remains strongest on adjudicated free-response and ties Seed-2.1 on Hard50 after four overlap-bias downward adjustments. Seed-2.1 is the most balanced runner-up across SGS152 MCQ and Hard50. DeepSeek trails on SGS152 MCQ and Robustness and retains one no-rescue missing free-response answer.

## Evidence Files

| Artifact | Path |
|---|---|
| SGS152 MCQ outputs | `results/standard_20260703/sgs152_mcq/model_outputs.csv` |
| SGS152 MCQ manifest | `results/standard_20260703/sgs152_mcq/manifest.json` |
| SGS152 MCQ scored summary | `results/standard_20260703/sgs152_mcq/scored/model_results_summary.csv` |
| Free-response live outputs | `results/standard_20260703/sgs152_free_response/model_outputs.csv` |
| Free-response adjudicated summary | `results/standard_20260703/free_response_judge/scored_free_response_summary.csv` |
| Manual review queue | `results/standard_20260703/free_response_judge/manual_review_queue.csv` |
| Human review decisions | `results/standard_20260703/free_response_judge/human_review_decisions.csv` |
| Human review overrides | `results/standard_20260703/free_response_judge/human_review_overrides.csv` |
| Adjudication notes | `results/standard_20260703/free_response_judge/adjudication_notes.md` |
| Robustness scored summary | `results/standard_20260703/robustness/scored/model_results_summary.csv` |
| Hard50 scored summary | `results/standard_20260703/hard50/scored/model_results_summary.csv` |

Raw outputs exist locally under `results/standard_20260703/**/raw_model_outputs/` and `results/standard_20260703/free_response_judge/raw_judge_outputs/`. They are ignored by git and not committed.

## Release Interpretation

The SGS152 MCQ leaderboard is the 0.5.0 main benchmark result. Free-response is reported as judge-scored + assistant-assisted project-owner confirmed adjudication. Robustness and Hard50 are optional diagnostic layers.
