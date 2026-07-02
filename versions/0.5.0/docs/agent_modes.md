# Agent Modes

## 中文

mini-benchmark 0.5.0 支持两种评测模式。

| Mode | Purpose |
|---|---|
| No-tool mode | 评估模型基于题干、选项和已有证据做专业判断的能力 |
| Tool-allowed mode | 评估模型在计算、表格、文献、安全参考和 protocol checklist 支持下整合工具观察的能力 |

报告中建议分开展示 no-tool judgment、tool-update alignment 和 safety-boundary index，使模型能力画像更加清晰。

## English

mini-benchmark 0.5.0 supports two evaluation modes.

| Mode | Purpose |
|---|---|
| No-tool mode | Measures professional judgment from the prompt, options, and provided evidence |
| Tool-allowed mode | Measures integration of calculators, tables, literature, safety references, and protocol checklists |

Reports separate no-tool judgment, tool-update alignment, and safety-boundary index for clearer capability profiling.
