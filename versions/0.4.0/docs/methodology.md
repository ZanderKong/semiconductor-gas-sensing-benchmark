# Methodology

## 中文

mini-benchmark 0.4.0 的方法论由三层组成。

| Layer | Method |
|---|---|
| Domain abstraction | 从半导体气敏材料研发中抽象任务变量、证据关系和安全边界 |
| Evaluation construction | 将任务组织为 MCQ、free-response 和 robustness variants |
| Validation engineering | 用 schema、validation、lint 和 scorer 保证数据结构和评测流程可复核 |

题目设计强调真实研发语境：同一材料现象可能同时涉及吸附、扩散、载流子、湿度、表征分辨率、读数窗口和工艺约束。评测要求模型在这些变量之间做出阶段性取舍。

## English

mini-benchmark 0.4.0 uses a three-layer methodology.

| Layer | Method |
|---|---|
| Domain abstraction | Extract task variables, evidence relations, and safety boundaries from semiconductor gas-sensing R&D |
| Evaluation construction | Organize tasks into MCQ, free-response, and robustness variants |
| Validation engineering | Use schema, validation, linting, and scoring utilities for auditable evaluation |

The item design reflects realistic R&D context: one material observation can involve adsorption, diffusion, carrier behavior, humidity, characterization resolution, readout windows, and process constraints. The benchmark asks models to make stage-aware balanced decisions across these variables.
