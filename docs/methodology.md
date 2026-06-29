# Methodology

## 1. 设计定位

本 benchmark 用于测试模型能否在半导体气敏材料研发流程中做出专业、审慎、可执行的判断。

题目围绕材料研发闭环组织：

| scenario_stage | 说明 |
|---|---|
| 文献分析 | 从材料、机理、表征或安全资料中抽取可迁移结论 |
| 实验设计 | 设计变量、对照、验证矩阵和判定规则 |
| 实验进行 | 判断配气、涂布、煅烧、浸渍、设备上线等操作风险 |
| 结果分析 | 解释响应、恢复、漂移、湿度干扰、异常值和表征证据 |
| 下一步计划 | 在材料路线、产品化 gate、工艺放大之间做取舍 |
| 安全边界 | 识别高危气体、有毒溶剂、氧化剂、纳米粉体和废物风险 |

## 2. 参考框架如何转化

| 参考 | 借鉴点 | 本项目转化 |
|---|---|---|
| ChemBench-mini | domain/subfield/task 结构与题型比例 | 缩放为 100 题，保留 8 个 domain，但内容重写为气敏材料方向 |
| HELM | 多指标、按场景看模型能力 | V3 使用 Hard Gate、主评分维度和 Meta Eval 三层结构 |
| LAB-Bench | 科研任务来自 workflow | 将孤立知识点转化为研发判断、实验验证和异常诊断 |
| OpenAI Evals | 工程化样本、答案、评分和报告 | 产出 JSON/CSV、scorer、model runner、run manifest 和评测报告 |

## 3. 题目生成原则

### 3.1 抽象问题类型与去私有化

题库使用抽象问题类型，去除私有细节后保留材料研发中可迁移的判断结构。主要来源包括：

- 场景类型，如气体纸带、显色体系、反射率、基膜、浸渍、老化、配气。
- 实体集合，如 H2S、PH3、Cl2、O3、NO2、NH3、SnO2、CuO、PANI、银盐、DMF、MFC。
- workflow 结构，如文献分析、实验设计、实验异常、结果归因、下一轮计划。

题目主体覆盖更广泛的半导体气敏材料研发，不写入私有配方比例、样品编号或未公开结论。

### 3.2 Domain 抽样

按 ChemBench-mini 的 8 个 domain 等比例缩放到 100 题：

| domain | 题量 | 方向 |
|---|---:|---|
| organic_chemistry | 19 | 显色剂、有机受体、导电聚合物、溶剂/酸化效应 |
| physical_chemistry | 14 | 吸附、脱附、动力学、扩散、湿度竞争 |
| inorganic_chemistry | 14 | 金属氧化物、二维材料、贵金属修饰、氧空位 |
| materials_science | 14 | 纳米结构、薄膜、孔结构、基底、封装、批间差 |
| general_chemistry | 11 | 氧化还原、酸碱、ppm、MFC、沉淀、混合气 |
| analytical_chemistry | 10 | LOD、校准、XPS、XRD、SEM/EDS、GC、Raman |
| technical_chemistry | 10 | 涂布、丝印、煅烧、连续浸渍、设备 commissioning |
| toxicity_and_safety | 8 | 高危气体、DMF、银盐废物、纳米粉体、安全 gate |

### 3.3 选项设计

选择题避免“一个显然正确、三个明显错误”的低区分度结构。干扰项主要是：

- 单独看成立，但放入题目条件后存在隐藏问题。
- 化学机理正确但缺少控制变量。
- 小试可行但放大后有隐藏风险。
- 响应值更高但牺牲恢复、稳定、选择性或安全。
- 表征结论可能成立但证据强度不够。
- 一般实验动作可行但在高危气体或有毒试剂情境下不安全。

每个选项都带有 `option_profiles` 和 `option_rationales`，用于人类审题和后续错误归因。

## 4. V3 评价体系

V3 将评价体系拆成三层：

| 层级 | 目的 |
|---|---|
| G 层 Hard Gate | 先识别安全、事实、证据、指令、工具和隐私硬失败 |
| S 层主评分 | 按 D0-D6 七个维度计算模型回答质量 |
| M 层 Meta Eval | 评估本次横评是否可复查、可复跑、可审计 |

S 层主评分为 100 分：

| 维度 | 权重 |
|---|---:|
| D0 指令遵循与输出完整性 | 10 |
| D1 专业准确性 | 20 |
| D2 情境化研发判断 | 15 |
| D3 证据锚定与不确定性 | 15 |
| D4 可执行研发方案 | 15 |
| D5 Tool Use 质量 | 10 |
| D6 安全与合规边界 | 15 |

当前仓库保留 V1/V2 的 100 题主集，同时新增 V3-alpha 并行题库。V3-alpha 以 46 个可审计 task unit 组织，字段已经迁移到 `target_dimensions`、`hard_gate_checks`、`tool_mode`、`variant_type` 等 V3 结构。

## 5. workflow 与 tool 字段

| 字段 | 目的 |
|---|---|
| `scenario_stage` | 对应材料研发闭环中的阶段 |
| `workflow_task` | 说明这题在研发流程里考什么 |
| `expected_output` | 说明模型应该输出的能力结果 |
| `tool_type` | 细分工具类型，便于分析工具增益 |

V3 区分两种运行模式：

| 模式 | 说明 | 报告字段 |
|---|---|---|
| no-tool baseline | 只给题干，不提供工具 | `no_tool_score` |
| tool-enabled agent | 提供 calculator、literature_retrieval、table_analysis、data_plotting、safety_reference、protocol_checklist 等工具 | `tool_enabled_score` |

建议报告 `tool_lift = tool_enabled_score - no_tool_score`，并单独统计 `tool_decision_accuracy`、`parameter_correctness`、`execution_outcome_quality` 和 `unsafe_tool_call_rate`。

## 6. 质量控制

构建脚本执行以下验证：

| 检查 | 规则 |
|---|---|
| 题量 | 总题量必须为 100 |
| domain 分布 | 必须符合 19/14/14/14/11/10/10/8 |
| 题型分布 | 82 道选择题、18 道简答题 |
| 工具 split | 51 道 with_tool、49 道 without_tool |
| 答案位置 | A/B/C/D 基本均衡，目前为 21/21/20/20 |
| 选项长度 | 单个选项不超过 36 字，同题长度差不超过 18 字 |
| 答案长度泄漏 | 正确答案不能明显长于干扰项均值 |
| 选项理由 | 每个选择题选项必须有 profile 和 rationale |
| workflow 字段 | 每题必须有 scenario_stage、workflow_task、expected_output、tool_type |
| 隐私控制 | seed_entity + analog 不超过 25，private_combination 为 0 |

V3 后续新增质量控制：

| 检查 | 规则 |
|---|---|
| gate 标注 | 触发 Hard Gate 的样本必须记录 `hard_gate_type` |
| 维度映射 | 每题至少映射到一个 D0-D6 主维度 |
| tool 模式 | 工具题需标明 no-tool / tool-enabled 的评估方式 |
| trace 完整性 | 工具题和简答题应保存 input、output、tool_call、judge_result |
| judge 可靠性 | 简答题和高风险题需定义人工复核或 judge 一致性策略 |

## 7. 评分流程

选择题使用 exact match，并通过 `option_profiles` 和 `failure_mode` 解释错因。简答题和后续 V3 多步任务使用“先 Hard Gate、后 D0-D6 主评分”的流程。

建议横评流程：

1. 固定题目顺序和统一 prompt。
2. 记录模型版本、调用日期、temperature、工具配置和 prompt hash。
3. 选择题自动判分，并映射错因维度。
4. 简答题先检查 Hard Gate，再按 D0-D6 rubric 评分。
5. 安全、隐私、Hard Gate 样本做人工复核。
6. 按 domain、scenario_stage、tool_type、failure_mode 和 D0-D6 聚合结果。
7. 输出模型画像：强项、短板、工具收益、安全风险、证据边界问题和典型 badcase。
8. 输出 Meta Eval 指标：trace 完整性、复跑能力、证据可追溯性和评分器可靠性。

## 8. 动态题库与鲁棒性

V3 后续可拆成两类题集：

| 题集 | 用途 |
|---|---|
| Static Core Set | 固定核心题，用于长期回归和模型横向可比 |
| Live Extension Set | 定期新增题，用于降低污染和观察新能力 |

建议报告 `static_core_score`、`live_extension_score`、`performance_drop_on_live_tasks`，并通过 paraphrase、干扰条件、矛盾证据和多轮追问测试 `consistency_rate`、`overconfidence_rate` 和 `safety_regression_rate`。

## 9. 当前局限

- 当前题目仍以选择题为主，强模型结果显示流程已跑通，但选择题区分度不足。
- 简答题为 18 题，后续可提高到 25 题以增强开放式评估。
- tool_type 目前由规则推断，后续可人工精修。
- V3-alpha 已完成并行题库、schema、本地 deterministic demo runner、评分协议和 trace 设计。
- 当前已完成 gpt-5.5 和 deepseek-v4-pro 的 MCQ 流程验证；后续可扩展更多模型和 V3 trace-based 真实工具 harness。
