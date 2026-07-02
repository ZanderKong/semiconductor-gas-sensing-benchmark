# SGS-Hard-50 Evaluation Report

## 中文

### Run Setup

| Setting | Value |
|---|---|
| Date | 2026-06-30 |
| Benchmark | `data/benchmark_sgs_hard50.json` |
| Runner | `eval/run_eval.py` |
| Scorer | `eval/score_mcq.py` |
| Outputs | `results/hard50/model_outputs_hard50_all.csv` |
| Scored artifacts | `results/hard50/scored_all/` |

### Results

| Model | Correct / Total | Accuracy | Main failure modes |
|---|---:|---:|---|
| DeepSeek V4 Pro | 48 / 50 | 96.0% | condition update, safety gate |
| GPT-5.5 | 48 / 50 | 96.0% | condition update, safety gate |
| MiMo v2.5 Pro | 47 / 50 | 94.0% | safety gate, condition update |

### Interpretation

SGS-Hard-50 已经提供了可复核的诊断层：每道题绑定 diagnostic type、failure mode、option profile 和 option-level rationale，能够把错误归因到条件更新、安全 gate、证据冲突、工具观察或机理迁移等具体模式。

但 2026-06-30 的真实模型运行也说明，当前 hard set 仍然偏容易。强模型准确率集中在 94.0% 到 96.0%，没有达到内部压力目标 70% 到 85%。这不是负面结论，而是 0.5.0 的关键发现：新增 hard set 解决了结构化诊断问题，但还需要下一轮难度校准。

### Next Difficulty Pass

下一轮应优先增加以下题型：

1. 更密集的表格型判断，要求同时比较响应、漂移、RSD、恢复、湿度和批间差异。
2. 混合方向的条件更新题，其中新增证据有时支持原路线，有时要求转向，避免模型总是选择保守答案。
3. 更弱提示的安全边界题，让所有选项都以合规措辞出现，但只有一个真正闭合授权、联锁和尾气边界。
4. 需要计算或排序的多目标取舍题，使错误能归因到单指标优化、稳定性忽略或工艺放大误判。

## English

### Run Setup

| Setting | Value |
|---|---|
| Date | 2026-06-30 |
| Benchmark | `data/benchmark_sgs_hard50.json` |
| Runner | `eval/run_eval.py` |
| Scorer | `eval/score_mcq.py` |
| Outputs | `results/hard50/model_outputs_hard50_all.csv` |
| Scored artifacts | `results/hard50/scored_all/` |

### Results

| Model | Correct / Total | Accuracy | Main failure modes |
|---|---:|---:|---|
| DeepSeek V4 Pro | 48 / 50 | 96.0% | condition update, safety gate |
| GPT-5.5 | 48 / 50 | 96.0% | condition update, safety gate |
| MiMo v2.5 Pro | 47 / 50 | 94.0% | safety gate, condition update |

### Interpretation

SGS-Hard-50 now provides a reproducible diagnostic layer: each item has a diagnostic type, failure mode, option profile, and option-level rationale. Misses can be attributed to concrete patterns such as condition-update stickiness, weak safety gating, evidence conflict, ignored tool observations, or mechanism transfer.

The 2026-06-30 real-model run also shows that the current hard set is still too easy. Strong-model accuracy is 94.0% to 96.0%, above the internal stress target of 70% to 85%. This is a useful 0.5.0 finding: the hard-set structure is in place, but the next iteration should calibrate difficulty more aggressively.
