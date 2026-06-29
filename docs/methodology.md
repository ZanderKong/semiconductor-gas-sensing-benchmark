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
| HELM | 多指标、按场景看模型能力 | 每题保留 workflow、tool、failure mode 和 evaluation dimension |
| LAB-Bench | 科研任务来自 workflow | 将孤立知识点转化为研发判断、实验验证和异常诊断 |
| OpenAI Evals | 工程化样本、答案、评分和报告 | 产出 JSON/CSV、可接 scorer 和 model runner |

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

## 4. 新增 workflow 字段

| 字段 | 目的 |
|---|---|
| `scenario_stage` | 对应材料研发闭环中的阶段 |
| `workflow_task` | 说明这题在研发流程里考什么 |
| `expected_output` | 说明模型应该输出的能力结果 |
| `tool_type` | 细分工具类型，便于分析工具增益 |

`tool_type` 不再只是 with-tool / without-tool，而分为：

| tool_type | 说明 |
|---|---|
| `no_tool` | 闭卷专业判断 |
| `calculator` | 需要计算、稀释、LOD、斜率或 Arrhenius 估算 |
| `literature_retrieval` | 需要查阅表征、材料机理或安全资料 |
| `table_analysis` | 需要表格、矩阵、批间差或验证表分析 |
| `data_plotting` | 需要曲线、漂移、响应/恢复、基线趋势分析 |
| `safety_reference` | 需要安全资料、SOP、危害和废物处置判断 |
| `protocol_checklist` | 需要步骤、gate、检查表或实验流程约束 |

## 5. 质量控制

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

## 6. 评分流程

选择题使用 exact match。简答题使用 5 分 rubric，并优先检查 hard fail。

建议横评流程：

1. 固定题目顺序和统一 prompt。
2. 记录模型版本、调用日期、temperature 和工具配置。
3. 选择题自动判分。
4. 简答题使用人工评分或 LLM-as-judge，人工抽检安全题和高风险错题。
5. 按 domain、scenario_stage、tool_type、failure_mode 聚合结果。
6. 输出模型画像：强项、短板、工具收益、安全风险和典型 badcase。

## 7. 当前局限

- V2 仍以选择题为主，当前强模型结果显示流程已跑通，但选择题区分度不足。
- 简答题为 18 题，后续可提高到 25 题以增强开放式评估。
- tool_type 目前由规则推断，后续可人工精修。
- 当前已完成 gpt-5.5 和 deepseek-chat 的 MCQ 流程验证；后续可在接口配置稳定后扩展更多模型。
