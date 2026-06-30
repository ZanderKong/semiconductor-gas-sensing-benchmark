# Dataset Card

## 中文

| Item | Value |
|---|---:|
| Dataset | Semiconductor Gas-Sensing Mini-Benchmark |
| Version | 0.4.0 |
| Main set | 100 items |
| Multiple-choice | 82 items |
| Free-response | 18 items |
| Robustness layer | 40 items |
| Language | Chinese |
| Domain | Semiconductor gas-sensing materials R&D |

### 数据构成

主集按照 ChemBench mini 的题型比例映射到半导体气敏材料场景，覆盖有机化学、物理化学、无机化学、材料科学、通用化学、分析化学、技术化学、毒性与安全八个领域。

| Domain | Count |
|---|---:|
| organic_chemistry | 19 |
| physical_chemistry | 14 |
| inorganic_chemistry | 14 |
| materials_science | 14 |
| general_chemistry | 11 |
| analytical_chemistry | 10 |
| technical_chemistry | 10 |
| toxicity_and_safety | 8 |

### 设计原则

- MCQ 采用四选项结构，答案分布为 A=21、B=21、C=20、D=20。
- 选项保持长度均衡，并以真实研发中可能出现的局部合理动作构造 distractor。
- Free-response 采用 10 分制 rubric，强调问题框定、证据边界、实验设计、决策逻辑和安全隐私。
- Robustness variants 与主集分离，用于检验判断原则在相邻场景中的稳定性与条件敏感性。
- 数据采用安全抽象表达，保留专业判断变量、证据关系和合规 gate。

## English

| Item | Value |
|---|---:|
| Dataset | Semiconductor Gas-Sensing Mini-Benchmark |
| Version | 0.4.0 |
| Main set | 100 items |
| Multiple-choice | 82 items |
| Free-response | 18 items |
| Robustness layer | 40 items |
| Language | Chinese |
| Domain | Semiconductor gas-sensing materials R&D |

### Composition

The main set maps ChemBench mini-style proportions into semiconductor gas-sensing materials scenarios. It covers organic chemistry, physical chemistry, inorganic chemistry, materials science, general chemistry, analytical chemistry, technical chemistry, and toxicity/safety.

### Design Principles

- MCQ items use four options with an answer distribution of A=21, B=21, C=20, D=20.
- Options are length-balanced and use locally plausible distractors grounded in realistic R&D actions.
- Free-response items use 10-point rubrics for problem framing, evidence boundaries, experimental design, decision logic, and safety/privacy.
- Robustness variants are evaluated separately from main-set accuracy to measure stability and condition sensitivity.
- The dataset uses safety-aware abstraction while preserving professional reasoning variables, evidence relationships, and compliance gates.
