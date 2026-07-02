# MCQ Quality Report

## 中文

### 质量目标

MCQ 设计目标是让模型必须利用题干语境、研发阶段和证据边界做判断。选项并非简单反义项，而是来自真实研发讨论中的可行动作、局部合理解释或阶段性备选方案。

### 自动化质量指标

| Check | Result |
|---|---:|
| MCQ count | 82 |
| Options per item | 4 |
| Answer distribution | A=21, B=21, C=20, D=20 |
| Option length ratio gate | Passed |
| Option-level rationales | 82 / 82 |
| Consistency fields | 100 / 100 main-set items |

### 设计价值

该 MCQ 层能够评估模型是否真正理解材料研发语境。例如，模型需要区分“响应强”与“可逆性可靠”、“表征相关”与“机理闭环”、“低浓度”与“安全合规 gate”、“单次曲线”与“可复核证据链”。这种设计比单纯知识问答更接近科研和工程判断。

## English

### Quality Objective

The MCQ layer requires models to use question context, R&D stage, and evidence boundaries. Options represent feasible actions, locally plausible explanations, or stage-specific alternatives drawn from realistic research discussions.

### Automated Quality Metrics

| Check | Result |
|---|---:|
| MCQ count | 82 |
| Options per item | 4 |
| Answer distribution | A=21, B=21, C=20, D=20 |
| Option length ratio gate | Passed |
| Option-level rationales | 82 / 82 |
| Consistency fields | 100 / 100 main-set items |

### Design Value

The MCQ layer evaluates whether a model understands materials R&D context. It asks models to separate strong response from reliable reversibility, characterization correlation from mechanistic closure, low concentration from compliance gates, and single curves from auditable evidence chains. This design is closer to scientific and engineering judgment than simple knowledge recall.
