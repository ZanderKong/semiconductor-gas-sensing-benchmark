# V3-alpha Task Design

## 1. 设计目标

V3-alpha 将题库从“题干 + 答案”的形式升级为可审计的 evaluation unit。每道题都要说明它测试哪个研发阶段、需要什么输出、是否允许工具、可能触发哪些 Hard Gate、对应 D0-D6 哪些评分维度，以及评分器如何判断答案是否合格。

本轮新增 `benchmark_v3_alpha`，不覆盖 `benchmark_v1`。V3-alpha 题库用于可审计任务设计、demo trace、评分协议和后续真实工具 harness。

## 2. 文件结构

| 文件 | 用途 |
|---|---|
| `data/benchmark_v3_alpha.json` | V3-alpha 主数据文件 |
| `data/benchmark_v3_alpha.csv` | 便于人工查看的扁平表格 |
| `data/schema_v3_alpha.json` | V3-alpha task schema，保留在旧位置兼容现有脚本 |
| `data/schema/task_schema_v3.json` | V3 task schema 的稳定入口 |
| `docs/task_design_v3.md` | 题库设计说明 |
| `eval/runner.py` | 本地 deterministic V3 demo runner |
| `eval/run_eval.py` | 真实模型 MCQ runner |
| `results/runs/demo/` | V3 demo trace 和报告样例 |

## 3. 规模与拆分

| split | 数量 | 目的 |
|---|---:|---|
| `static_core` | 24 | 固定核心题，用于长期横向比较 |
| `robustness` | 16 | 从 8 道核心题派生的鲁棒性变体 |
| `live_extension` | 6 | 后续可替换/更新的动态扩展题 |

Static core 按 6 个 `scenario_stage` 均衡分布，每个阶段 4 题。

## 4. 能力单元题型

V3-alpha 不再以选择题/简答题作为主要设计轴，而以能力单元组织题目：

| task_type | 评价重点 |
|---|---|
| `professional_judgment` | 基础专业判断和硬事实 |
| `contextual_decision` | 材料、工艺、设备、安全约束下的研发决策 |
| `evidence_boundary` | 证据强度、不确定性和过度推断 |
| `experiment_design` | 变量、对照、指标和 go/no-go |
| `tool_use` | 工具选择、参数、结果整合和工具增益 |
| `robustness_variant` | 改写、干扰、矛盾、多轮和安全诱导稳定性 |

## 5. Tool Use 设计

V3-alpha 至少包含 8 道 tool-related base task，并设计 4 组 no-tool / tool-enabled 成对任务，用于计算 `tool_lift`。

| pair | no-tool | tool-enabled | 工具重点 |
|---|---|---|---|
| `VG-LIT-RETRIEVAL-NO2` | V3-SC-002 | V3-SC-003 | literature_retrieval |
| `VG-DESIGN-DOE-TABLE` | V3-SC-006 | V3-SC-007 | table_analysis |
| `VG-RUN-MFC-CALC` | V3-SC-011 | V3-SC-012 | calculator |
| `VG-SAFE-SDS-CL2` | V3-SC-021 | V3-SC-022 | safety_reference |

此外，V3-SC-009 覆盖 `protocol_checklist`，V3-SC-014 覆盖 `data_plotting`。

## 6. Task Validity

每道题必须满足：

- 来自通用知识、抽象问题类型或合成数据，不包含私有配方、私有实验标识、敏感采购信息或未公开结论。
- 合格的材料研发 agent 应能根据题干和允许工具给出可审计回答。
- 题目能暴露至少一种具体 failure mode，而不是只考百科记忆。
- 安全相关题必须包含 Hard Gate 检查项。

## 7. Outcome Validity

评分时遵循：

1. 先检查 `hard_gate_checks`。
2. 再按 D0-D6 的 `target_dimensions` 评分。
3. Tool-enabled 题必须检查工具选择、参数和结果整合。
4. 鲁棒性变体应与 parent task 的核心判断保持一致。
5. live extension 题不替代 static core，只用于观察新情境下的能力变化。

## 8. 当前完成状态

当前 V3-alpha 已完成：

- V3-alpha task schema。
- Scoring protocol、Hard Gates 和 D0-D6 维度定义。
- Judge protocol 和人工复核说明。
- 本地 deterministic demo runner。
- Demo manifest、trace、model outputs、judge outputs、aggregate metrics、report 和 badcase gallery。
- 真实模型 MCQ runner、run manifest、leaderboard 和 diagnostic report。
- Schema validation、V3-alpha distribution validation、benchmark lint 和 CI workflow。

## 9. 后续工作

后续工作应集中在真实 V3 task-unit 评测，而不是继续扩展选择题展示层。

- 为 V3-alpha free-response 和 tool-enabled task 接入 judge runner。
- 为 calculator、retrieval、table analysis、data plotting、safety reference 和 protocol checklist 接入真实工具 harness。
- 运行 trace-based real-model V3 evaluation。
- 增加 human audit sample 和 judge-human agreement 记录。
- 将 HTML review 页面扩展到 V3 schema。
