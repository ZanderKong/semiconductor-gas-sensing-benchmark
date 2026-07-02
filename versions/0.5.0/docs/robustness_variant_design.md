# Robustness Variant Design

## 中文

Robustness layer 包含 40 道 variants，围绕 12 个 consistency groups 构建。每组从主集中的一个 base item 出发，扩展出表达改写、干扰信息、条件变化、安全诱导或工具观察变化。

| Variant Type | 设计目标 |
|---|---|
| paraphrase | 检验同一证据结构在不同表达方式下的判断稳定性 |
| distractor | 检验模型对真实但非决定性信息的抗干扰能力 |
| contradiction | 检验新增关键条件后模型是否更新判断 |
| adversarial_safety | 检验安全边界在诱导式表达下的保持能力 |
| tool_observation_shift | 检验工具观察改变证据权重时的结论更新能力 |

该层把“答对单题”扩展为“在相邻场景中保持判断原则”，使 benchmark 更接近真实研发讨论中的动态证据环境。

## English

The robustness layer contains 40 variants across 12 consistency groups. Each group starts from a base item in the main set and expands it through paraphrase, distractor information, condition changes, adversarial safety prompts, or tool-observation shifts.

| Variant Type | Purpose |
|---|---|
| paraphrase | Measure judgment stability under equivalent wording |
| distractor | Measure resistance to realistic but non-decisive information |
| contradiction | Measure conclusion updates when key conditions change |
| adversarial_safety | Measure safety-boundary retention under persuasive phrasing |
| tool_observation_shift | Measure evidence updates when tool observations change |

This layer extends evaluation from single-item accuracy to principle consistency across neighboring research scenarios.
