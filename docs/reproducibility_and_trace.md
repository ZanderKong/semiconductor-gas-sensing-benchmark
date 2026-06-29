# Reproducibility And Trace

## 1. 目标

V3 评测需要能回答：同一题集、同一模型配置、同一工具配置下，结果是否可复查、可复跑、可定位问题。

Trace 记录的是可审计事件，不记录模型私有思维链。

## 2. 推荐运行目录

```text
results/runs/
└── 2026-06-29_provider_model_taskset/
    ├── run_manifest.json
    ├── trace.jsonl
    ├── model_outputs.jsonl
    ├── judge_outputs.jsonl
    ├── aggregate_metrics.json
    └── report.md
```

## 3. run_manifest.json

| 字段 | 说明 |
|---|---|
| `run_id` | 单次运行 ID |
| `created_at` | 运行时间 |
| `benchmark_version` | 如 `v3-alpha` |
| `task_file` | 题集文件路径 |
| `task_set_hash` | 题集 hash |
| `schema_hash` | schema hash |
| `model_provider` | 模型服务商 |
| `model_id` | 模型名称和版本 |
| `temperature` / `top_p` | 采样配置 |
| `prompt_hash` | prompt hash |
| `tool_schema_hash` | 工具 schema hash |
| `retrieval_corpus_hash` | 检索语料 hash，没有则为空 |
| `judge_protocol_version` | judge protocol 版本 |
| `judge_model` | judge 模型或人工评分 |
| `code_commit` | 仓库 commit |

## 4. trace.jsonl

trace 每行记录一个可审计事件。

| 字段 | 说明 |
|---|---|
| `run_id` | 运行 ID |
| `task_id` | 任务 ID |
| `event_index` | 事件序号 |
| `event_type` | `input`、`tool_call`、`tool_result`、`model_output`、`judge_result` |
| `visible_input` | 给模型或工具的可公开输入 |
| `tool_name` | 工具名称 |
| `arguments` | 工具参数 |
| `observation_hash` | 工具返回或证据片段 hash |
| `state_before_hash` | 状态变更前 hash |
| `state_after_hash` | 状态变更后 hash |
| `visible_output` | 模型最终可见输出 |
| `judge_result` | 评分、gate、failure mode |

不记录：

- 模型私有思维链。
- API key、账号、内部路径、未脱敏实验记录。
- 私有配方比例、样品编号或未公开结论。

## 5. 可复跑检查

| 指标 | 定义 |
|---|---|
| `trace_completeness_rate` | 必要事件是否齐全 |
| `replay_pass_rate` | 固定 manifest 复跑是否得到一致或等价结论 |
| `state_invariant_pass_rate` | 有状态任务的状态 hash 是否自洽 |
| `tool_observation_coverage` | 工具题是否保存工具结果 hash |
| `provenance_coverage` | 关键结论是否能追溯到题干、工具结果或 gold note |

## 6. 鲁棒性与动态题库

两个下降指标需要分开：

| 指标 | 定义 |
|---|---|
| `robustness_drop` | robustness variant 相对 parent/base task 的分数下降 |
| `performance_drop_on_live_tasks` | live_extension 相对 static_core 的分数下降 |

鲁棒性变体用于测试同一任务在改写、干扰、矛盾证据、多轮追问或安全诱导下是否稳定。Live extension 用于观察模型面对新近或可替换任务时的泛化能力。

## 7. 结果归档

一次完整运行至少应保存：

- 输入题集和 schema hash。
- 模型输出。
- 工具 trace。
- judge 输出。
- 聚合指标。
- badcase 列表。
- 人工复核记录。

缺少 trace 的运行可以用于调试，但不应作为正式 leaderboard 结果。

