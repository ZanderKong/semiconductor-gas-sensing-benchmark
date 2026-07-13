# Evaluation Report

## 评测范围

本报告记录 Semiconductor Gas-Sensing Mini-Benchmark 0.5.0 live standard run。正式证据位于 `results/standard_20260703`。

主榜只使用 SGS152 Main Set 的 122 道 MCQ。30 道 free-response 由不参评的 GPT-5.6-sol 按固定 rubric 评分；40 道 Robustness 和 50 道 Hard50 是 optional diagnostics。开放题和诊断层均不进入主榜，也不生成 full-suite aggregate score。

## 运行设置

- 候选模型答案沿用已冻结的 live run，不重跑、不补答；
- temperature 0、single sampling、no retry、no rescue；
- internet access 与 tool assistance 均为 false；
- task、prompt、participating-model outputs 和 judge prompt 均记录 SHA-256；
- GPT-5.6-sol judge 对四模型各评分 30 条，共 120 条，运行错误为 0。

## SGS152 MCQ Main Leaderboard

| Model | Correct / Total | Accuracy |
|---|---:|---:|
| MiMo v2.5 Pro | 119 / 122 | 97.54% |
| Seed-2.1 | 118 / 122 | 96.72% |
| GPT-5.5 | 117 / 122 | 95.90% |
| DeepSeek V4 Pro | 115 / 122 | 94.26% |

## Free-response Judge Result

| Model | Average | Hard Fails |
|---|---:|---:|
| GPT-5.5 | 8.150 | 0 |
| Seed-2.1 | 7.522 | 4 |
| DeepSeek V4 Pro | 6.762 | 0 |
| MiMo v2.5 Pro | 5.448 | 11 |

GPT-5.6-sol 只担任 judge，不是参评模型。项目负责人将 58 条复核委托给 Codex assistant：33 条同意、15 条 hard fail 确认、1 条缺答维持 0、9 条安全/隐私维度调整。该结果不是外部独立盲审。

Hard fail 表示回答命中题目定义的 risk gate；原 judge total 保留，不归零、不封顶、不从平均值中排除，hard-fail count 单独报告。DeepSeek V4 Pro 未回答 `SGS-081`，按 no-rescue 规则确定性计 0。

## Optional Diagnostic Results

| Model | Robustness | Hard50 |
|---|---:|---:|
| GPT-5.5 | 34 / 40 | 48 / 50 |
| MiMo v2.5 Pro | 34 / 40 | 47 / 50 |
| Seed-2.1 | 32 / 40 | 48 / 50 |
| DeepSeek V4 Pro | 29 / 40 | 47 / 50 |

MiMo 领先主榜，但开放题的 decision logic、evidence boundary、experimental design 较弱，并触发 11 条 risk gate。Seed-2.1 是 MCQ runner-up，但在关键对照、定量关系和工艺取样控制上触发 4 条 risk gate。GPT-5.5 的开放题平均分最高，但同家族 judge 相关性仍需人工复核。DeepSeek 的主要问题是缺答、决策条件和证据边界。

## Evidence Files

| Artifact | Path |
|---|---|
| Main MCQ score | `results/standard_20260703/sgs152_mcq/scored/model_results_summary.csv` |
| Participating-model free-response outputs | `results/standard_20260703/sgs152_free_response/model_outputs.csv` |
| GPT-5.6-sol judge manifest | `results/standard_20260703/free_response_judge/judge_manifest.json` |
| Free-response summary | `results/standard_20260703/free_response_judge/scored_free_response_summary.csv` |
| Delegated-review manifest | `results/standard_20260703/free_response_judge/adjudication_manifest.json` |
| Adjudicated summary | `results/standard_20260703/free_response_judge/adjudicated_free_response_summary.csv` |
| Historical GPT-5.5 judge | `archive/judge_history/gpt-5.5_20260703/` |

Raw participating-model and judge outputs exist locally in ignored `raw_model_outputs/` and `raw_judge_outputs/` directories. Parsed evidence, manifests, reports and delegated-review decisions are intended for version control.

## Release Interpretation

The SGS152 MCQ table is the only main leaderboard. Free-response is GPT-5.6-sol judge-scored plus project-owner-delegated assistant review. Robustness and Hard50 remain optional diagnostics.
