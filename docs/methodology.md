# Methodology

## 构建目标

Semiconductor Gas-Sensing Mini-Benchmark 评估模型在半导体气敏材料研发语境中的专业判断能力。构建目标包括：

- 把材料研发任务拆成可评分题目；
- 让每道题具有明确 decisive constraint；
- 让错误选项携带可归因的 failure mode；
- 让选择题、开放题、robustness variants 和 diagnostic sets 形成互补；
- 支持按 domain、scenario stage、tool type、failure mode 和 option profile 汇总。

题目不是知识点堆砌。每道题都需要体现一个研发判断：当前证据能支持什么，不能支持什么，下一步最应该做什么，安全边界在哪里。

## 任务来源

题目来自半导体气敏材料研发中的常见任务类型：

- 文献分析：判断文献条件能否迁移到当前材料或器件；
- 实验设计：设计能区分假设的最小对照矩阵；
- 结果分析：解释响应曲线、恢复曲线、漂移、谱图和批内统计；
- 工艺放大：判断浸渍、干燥、基膜批次、读数窗口和工艺窗口；
- 安全边界：识别高危气体、强腐蚀溶剂、授权 SOP、通风、尾气和公开脱敏要求；
- 数据质量：处理异常点、批间差异、校准残差和工具表格观察。

## Domain Core Set 设计

Domain Core Set 包含 100 题，其中 82 道 MCQ 和 18 道 free-response。它评估半导体气敏材料研发的核心判断：

- 有机受体、显色纸带和成膜均匀性；
- MOS、氧空位、吸附氧和表面反应；
- 湿度、漂移、选择性、恢复和基线稳定性；
- 传感器验证表、异常点处理和数据完整性；
- 毒性、安全、隐私和公开说明边界。

Domain Core Set 的设计重心是研发语境的适配性。一个动作在通用化学上正确，仍可能因为当前阶段、证据等级或安全条件不匹配而成为错误答案。

## Scientific Stress Set 设计

Scientific Stress Set 包含 52 题，其中 40 道 MCQ 和 12 道 free-response。它用于观察强模型边界，重点覆盖：

- 科学规则边界；
- 定量精度；
- 谱图模式；
- 结构性质提取；
- 安全风险识别；
- near-miss distractor 抵抗。

Scientific Stress Set 的目标是增加错误可观察性。该层题干更短，干扰项更靠近正确答案，模型需要精确处理单位、符号、条件、表征证据和安全优先级。

## 题目筛选标准

题目进入 active set 需要满足以下条件：

- 有明确 decisive constraint；
- 正确答案能由题干信息和公开科学规则支持；
- 错误选项局部合理；
- 错误选项能映射到 failure mode；
- 不泄露私有配方比例、供应敏感信息或可执行危险步骤；
- MCQ 可自动评分；
- free-response 有 10 分制 rubric、key points、risk gates 和 common failure modes；
- 题目能落入 domain、scenario stage 和 tool type。

低区分度题后续进入 warm-up 或 archive。高分聚集题可以继续保留为基础能力检查，但不宜作为 frontier model 排名的主要依据。

## 题目设计流程

1. 定义研发任务：明确题目来自文献分析、实验设计、结果分析、工艺放大、安全评审或数据质量判断。
2. 提炼 decisive constraint：找到决定答案的单一优先约束。
3. 编写题干：保留必要条件，去除私有比例和可执行危险细节。
4. 定义正确项：确保正确项能处理当前主约束，保留证据边界。
5. 构造干扰项：每个错误选项都局部合理，并对应一个短板。
6. 写 option rationales：解释正确项和每个错误项的诊断含义。
7. 标注 failure mode：把错误归因映射到可汇总字段。
8. 设置 rubric 或 exact-match key：让题目可以评分和复核。
9. 运行 validation 和 lint：检查题量、题型、选项、rubric、risk gates 和安全表达。
10. 根据评测结果决定保留、扩写、剪枝或移入 archive。

## 干扰项设计原则

错误选项必须局部合理。简单荒谬的选项无法诊断强模型短板。

常见干扰项设计：

- 单项指标推进：高响应、快恢复或短期颜色变化被过度放大；
- 上下文错配：科学规则正确，但题干条件不支持；
- 证据范围扩张：把谱图、EPR 或单次曲线写成因果闭环；
- 安全边界弱化：用低浓度、小量、短时等表述替代授权和工程控制；
- 公式路径错误：对数、倒数差、单位或数量级错误；
- 工具观察忽略：表格、空白、湿度或批间信息改变了判断，模型仍沿用初判；
- 过早归因：把问题提前归因到纸基、基底、载体或读数窗口。

## 错误归因字段

每道题至少包含以下归因字段：

- `domain`
- `domain_cn`
- `scenario_stage`
- `tool_type`
- `failure_mode`
- `option_profiles`
- `option_rationales`
- `evaluation_dimensions`
- `private_dependency_level`
- `tags`

MCQ 选错后，scorer 会读取模型选择的 option profile。开放题评分会读取 rubric、key points、risk gates 和 common failure modes。

## 与通用 benchmark 的差异

本 benchmark 重视研发场景中的判断质量：

- 关注证据能否支撑下一步，而非只问事实；
- 关注当前条件是否适配，而非只问一般规律；
- 关注风险和授权边界，而非只问方案是否可行；
- 关注错误选项的诊断含义，而非只统计对错；
- 关注版本复盘和题库维护，而非一次性分数。

## 代表性题型

| 类型 | 代表题 | 诊断点 |
|---|---|---|
| 纸带负载 | SGS-FM-037 | 水相浸渍、负载均匀性、读数步骤归因 |
| 湿度漂移 | SGS-027 | 湿度滞后、基线分段、路径依赖 |
| 定量压力 | SGS-FM-025 | Arrhenius 估算、单位、数量级 |
| 安全边界 | SGS-095、SGS-099 | 溶剂暴露、高危气体 go-no-go |
| 证据冲突 | SGS-HARD-001 | XPS 假设、高湿漂移、恢复 |

## 局限性

SGS152 是 compact benchmark。它覆盖关键研发判断，但不能覆盖全部材料体系、气体类型、器件结构和实验条件。

Domain Core Set 当前分数较高，说明常规研发判断层对强模型的区分度有限。Scientific Stress Set 增加了错误可观察性，但 40 道 MCQ 和 12 道开放题仍属于小样本压力层。

Hard Diagnostic Set 当前分数过高。下一版需要强化证据冲突、工具观察更新、安全边界和多目标取舍题。
