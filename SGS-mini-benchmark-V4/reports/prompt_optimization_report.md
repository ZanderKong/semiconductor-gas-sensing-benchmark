# Prompt Strategy Report

## 中文

### 设计定位

mini-benchmark 0.4.0 使用统一的 `base_prompt.md` 作为主评测 prompt，以保证模型横评时的输入结构一致。Prompt 设计服务于三类目标：稳定解析 MCQ 答案、引导模型关注半导体气敏材料研发语境、强化证据边界和安全边界的表达。

### Prompt 结构

| Design Element | Purpose |
|---|---|
| Direct answer format | 提高 MCQ 解析稳定性 |
| Domain-grounded instruction | 引导模型关注材料、机理、测试和表征语境 |
| Safety-aware wording | 强化高风险气体和实验边界中的合规判断 |
| Evidence-boundary framing | 鼓励区分事实、假设、机制解释和决策建议 |
| Concise reasoning expectation | 让输出保持可评分、可复核、可横向比较 |

### 评测模式

项目同时保留 `cot_disabled_prompt.md` 和 `tool_augmented_prompt.md` 作为可控评测模式。前者强调直接答案输出，适合 MCQ 自动评分；后者强调工具观察和结构化证据整合，适合模拟真实研发中“数据表 + 实验备注 + 决策建议”的判断链路。

### 方法价值

该 prompt 策略体现了评测工程中的输入控制意识：同一任务集、同一输出格式、同一评分入口，使模型结果具备可比较性。Prompt 并不替代题库质量，而是让题库中的专业变量更清晰地进入模型判断过程，包括材料类型、气体类别、测试阶段、表征证据、工艺约束和安全 gate。

## English

### Design Positioning

mini-benchmark 0.4.0 uses a single `base_prompt.md` for the main evaluation to keep model comparisons structurally consistent. The prompt serves three goals: stable MCQ answer parsing, domain anchoring in semiconductor gas-sensing R&D, and clear expression of evidence and safety boundaries.

### Prompt Structure

| Design Element | Purpose |
|---|---|
| Direct answer format | Improve MCQ parsing stability |
| Domain-grounded instruction | Anchor reasoning in materials, mechanism, testing, and characterization context |
| Safety-aware wording | Reinforce compliant judgment in high-risk gas and experiment-boundary scenarios |
| Evidence-boundary framing | Separate facts, hypotheses, mechanistic interpretations, and decisions |
| Concise reasoning expectation | Keep outputs scoreable, auditable, and comparable across models |

### Evaluation Modes

The package also includes `cot_disabled_prompt.md` and `tool_augmented_prompt.md` for controlled evaluation modes. The former emphasizes direct-answer output for MCQ scoring. The latter supports tool observations and structured evidence integration, matching the common R&D pattern of table data, experiment notes, and decision recommendations.

### Method Value

The prompt strategy demonstrates input-control discipline in evaluation engineering. A shared task set, shared output format, and shared scoring entrypoint make model results comparable. The prompt complements dataset quality by making the professional variables explicit: material class, gas category, testing stage, characterization evidence, process constraints, and safety gates.
