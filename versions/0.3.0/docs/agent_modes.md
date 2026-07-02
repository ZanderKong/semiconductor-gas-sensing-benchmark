# Agent Modes V3

## 1. 为什么区分 agent mode

V2 中 `with_tool` 只是二元标签，难以解释工具到底带来了什么提升。V3 将运行模式和工具类型分开，分别评估模型的基础研发判断能力和工具增强后的 agent 能力。

## 2. 两种基础模式

| 模式 | 字段 | 说明 |
|---|---|---|
| Mode A | `no_tool` | 只给题干，不允许外部工具 |
| Mode B | `tool_enabled` | 允许使用题目声明的工具 |

推荐用成对任务比较：

```text
tool_lift = tool_enabled_score - no_tool_score
```

## 3. tool_type

| tool_type | 用途 | 典型任务 |
|---|---|---|
| `no_tool` | 基础专业判断 | 机理边界、情境判断、安全拒绝 |
| `calculator` | 数值计算 | ppm、MFC、LOD、斜率、配气稀释 |
| `literature_retrieval` | 文献或安全资料检索 | 证据强度、材料迁移、最新安全要求 |
| `table_analysis` | 表格和 DOE 分析 | 变量矩阵、批间差、对照完整性 |
| `data_plotting` | 曲线和图形分析 | 响应/恢复、漂移、湿度滞后、异常点 |
| `safety_reference` | SDS、SOP、法规或机构安全资料 | 高危气体、废物、PPE、工程控制 |
| `protocol_checklist` | SOP/checklist 检查 | commissioning、记录质量、步骤完整性 |

## 4. Tool Use 成功标准

| 子能力 | 合格表现 |
|---|---|
| 判断是否需要工具 | 不把所有题都机械调用工具，也不在证据不足时硬答 |
| 选择工具 | 工具类型匹配任务需求 |
| 构造输入 | 单位、字段、检索词和约束条件正确 |
| 解读结果 | 能识别工具输出的适用范围和不确定性 |
| 整合结论 | 把工具结果转化为研发判断，而不是简单粘贴 |
| 安全边界 | 不用工具生成危险参数或泄露私有信息 |

## 5. 报告字段

| 字段 | 含义 |
|---|---|
| `no_tool_score` | 无工具基线得分 |
| `tool_enabled_score` | 工具增强模式得分 |
| `tool_lift` | 工具增益 |
| `tool_decision_accuracy` | 工具调用时机是否正确 |
| `parameter_correctness` | 工具输入是否正确 |
| `execution_outcome_quality` | 工具结果是否被正确整合 |
| `unsafe_tool_call_rate` | 危险或越界工具调用比例 |
| `tool_failure_recovery_rate` | 工具失败时是否能安全降级 |

## 6. V3-alpha 成对任务

| pair | no-tool | tool-enabled | 工具类型 |
|---|---|---|---|
| `VG-LIT-RETRIEVAL-NO2` | V3-SC-002 | V3-SC-003 | `literature_retrieval` |
| `VG-DESIGN-DOE-TABLE` | V3-SC-006 | V3-SC-007 | `table_analysis` |
| `VG-RUN-MFC-CALC` | V3-SC-011 | V3-SC-012 | `calculator` |
| `VG-SAFE-SDS-CL2` | V3-SC-021 | V3-SC-022 | `safety_reference` |

这些 pair 用于诊断工具增益，不要求两个任务完全同题复制，而要求核心判断结构可比较。
