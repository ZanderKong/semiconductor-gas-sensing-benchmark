# SGS-100 Robustness Report

## 中文

### Robustness 结构

| Metric | Value |
|---|---:|
| Total variants | 40 |
| Consistency groups | 12 |
| Paraphrase variants | 12 |
| Distractor variants | 12 |
| Contradiction variants | 12 |
| Adversarial safety variants | 2 |
| Tool-observation variants | 2 |

### 设计目标

Robustness 层用于检验模型是否真正抓住题目的专业原则，而不是依赖表面措辞。40 道 variants 以主集题目为 parent，围绕表达改写、干扰信息、条件更新、安全诱导和工具观察更新构造相邻场景。每个 variant 保留明确 parent linkage、variant type、evidence cue 和评分答案，便于审阅者追踪题目设计逻辑。

### 指标解释

| Metric | Meaning |
|---|---|
| Consistency | 表达改写后保持同一判断原则 |
| Distractor Resistance | 面对真实但非决定性信息时保持主变量优先级 |
| Condition Update | 新增关键条件后更新判断 |
| Safety Boundary | 诱导式表达下保持安全边界 |
| Tool Update | 工具观察改变证据权重后更新结论 |

### 聚合结果

| Model | Correct / Total | Accuracy |
|---|---:|---:|
| MiMo v2.5 Pro | 36 / 40 | 90.0% |
| GPT-5.5 | 35 / 40 | 87.5% |
| DeepSeek V4 Pro | 30 / 40 | 75.0% |

### 学术与工程意义

Robustness 设计把材料研发中的“同一原则、多种语境”转化为可评分结构。例如，在湿度、表面反应、气体流量、表征证据和安全 gate 场景中，模型需要同时处理机理逻辑、数据边界和实验阶段。该层让 benchmark 具备更高的区分度，也体现了题库设计者对科研场景复杂性的理解。

## English

### Robustness Structure

| Metric | Value |
|---|---:|
| Total variants | 40 |
| Consistency groups | 12 |
| Paraphrase variants | 12 |
| Distractor variants | 12 |
| Contradiction variants | 12 |
| Adversarial safety variants | 2 |
| Tool-observation variants | 2 |

### Design Goal

The robustness layer tests whether a model captures the professional principle behind an item rather than relying on surface wording. The 40 variants are linked to main-set parent items and cover paraphrase, distractors, condition updates, safety-oriented persuasion, and tool-observation updates. Each variant includes parent linkage, variant type, evidence cue, and scored answer, making the design logic auditable.

### Metric Interpretation

| Metric | Meaning |
|---|---|
| Consistency | Preserve the same judgment principle under paraphrase |
| Distractor Resistance | Maintain priority of the decisive variable under realistic distractors |
| Condition Update | Update judgment when key conditions change |
| Safety Boundary | Preserve safety-aware judgment under persuasive phrasing |
| Tool Update | Update conclusions when tool observations change evidence weight |

### Aggregate Results

| Model | Correct / Total | Accuracy |
|---|---:|---:|
| MiMo v2.5 Pro | 36 / 40 | 90.0% |
| GPT-5.5 | 35 / 40 | 87.5% |
| DeepSeek V4 Pro | 30 / 40 | 75.0% |

### Academic and Engineering Value

The robustness design converts the research pattern of one principle across multiple contexts into a scoreable structure. In humidity, surface reaction, gas-flow, characterization evidence, and safety-gate scenarios, models must combine mechanistic logic, evidence boundaries, and experiment-stage awareness. This layer increases benchmark discrimination and demonstrates a strong understanding of scientific R&D complexity.
