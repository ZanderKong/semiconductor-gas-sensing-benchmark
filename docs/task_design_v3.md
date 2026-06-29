# V3-alpha Task Design

## 1. 设计目标

V3-alpha 将题库从“题干 + 答案”的形式升级为可审计的 evaluation unit。每道题都要说明它测试哪个研发阶段、需要什么输出、是否允许工具、可能触发哪些 Hard Gate、对应 D0-D6 哪些评分维度，以及评分器如何判断答案是否合格。

本轮新增 `benchmark_v3_alpha`，不覆盖 `benchmark_v1`。V3-alpha 题库用于后续题目迭代和评测 harness 设计；当前不做模型测试。

## 2. 文件结构

| 文件 | 用途 |
|---|---|
| `data/benchmark_v3_alpha.json` | V3-alpha 主数据文件 |
| `data/benchmark_v3_alpha.csv` | 便于人工查看的扁平表格 |
| `data/schema_v3_alpha.json` | V3-alpha task schema，保留在旧位置兼容现有脚本 |
| `data/schema/task_schema_v3.json` | V3 task schema 的稳定入口 |
| `docs/task_design_v3.md` | 题库设计说明 |

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

- 来自公开知识、抽象问题类型或合成数据，不包含私有配方、私有实验标识、敏感采购信息或未公开结论。
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

## 8. 后续迁移说明

当前 V3-alpha 是并行新题库。后续如果要进入正式 V3，可继续做：

- 将题目字段接入 eval runner。
- 增加 judge protocol 和 run manifest。
- 为 tool-enabled 题实现真实工具 harness。
- 将 HTML review 页面扩展到 V3 schema。
- 运行模型横评并生成 V3 报告。
