# SGS-Hard-50 Design Note

## 中文

SGS-Hard-50 是 0.5.0 新增的诊断型 MCQ 集。它不是为了把模型分数做低，而是为了提升头部模型区分度、失败模式解释力和研发场景真实性。公开目标是识别模型在材料研发判断中的具体薄弱点；内部压力指标是让强模型在 hard set 上落在约 70% 到 85%，并且错题能归因到明确 failure mode。

### 结构

| Diagnostic type | Items | 主要检查点 |
|---|---:|---|
| evidence_conflict | 10 | 多源证据冲突时是否保留证据边界 |
| condition_update | 10 | 新证据出现后是否更新原判断 |
| safety_boundary | 8 | 是否拒绝未闭合的高风险研发推进 |
| tool_observation_update | 8 | 是否根据表格、曲线、图像和日志修正结论 |
| multi_objective_tradeoff | 8 | 是否平衡响应、恢复、寿命、工艺和稳定性 |
| mechanism_transfer_trap | 6 | 是否把 MOS、纸带、聚合物、光学读数机理混用 |

### 选项设计规则

- 四个选项都应是单独看可执行或可解释的研发动作。
- 错误选项不是文字游戏，而是绑定真实 failure mode，例如单指标优化、局部正确但当前不优先、机理外推、工具观察忽略或安全 gate 过弱。
- 正确选项不能长期成为最长或最短选项；`scripts/validate_hard50.py` 会检查选项长度、答案分布和 diagnostic type 覆盖。
- 安全题保留高层级 go/no-go 判断，不写危险气体操作步骤、设施绕行或可复现实验路线。

### 文件

| File | Purpose |
|---|---|
| `scripts/build_sgs_hard50.py` | Source generator for JSON and CSV exports |
| `data/benchmark_sgs_hard50.json` | Scored hard-set source |
| `data/benchmark_sgs_hard50.csv` | Reviewer-friendly table export |
| `scripts/validate_hard50.py` | Hard-set validation gate |

## English

SGS-Hard-50 is the 0.5.0 diagnostic MCQ layer. Its goal is not to lower scores for their own sake. It is designed to improve top-model discrimination, make failures attributable, and make the benchmark closer to real R&D decision work. The internal stress target is roughly 70% to 85% accuracy for strong models, with each miss attributable to a clear failure mode.

### Structure

| Diagnostic type | Items | What It Tests |
|---|---:|---|
| evidence_conflict | 10 | Whether the model preserves evidence boundaries under conflicting signals |
| condition_update | 10 | Whether the model revises an earlier judgment after new evidence |
| safety_boundary | 8 | Whether the model blocks unsafe or under-specified R&D escalation |
| tool_observation_update | 8 | Whether tables, curves, images, and logs change the model's conclusion |
| multi_objective_tradeoff | 8 | Whether the model balances response, recovery, lifetime, process, and stability |
| mechanism_transfer_trap | 6 | Whether the model avoids mixing MOS, paper tape, polymer, and optical mechanisms |

### Option Rules

- Every option should be locally plausible as an R&D action or interpretation.
- Distractors are not word games; each maps to a realistic failure mode such as single-metric optimization, locally true but currently premature action, mechanism overreach, ignored tool observation, or weak safety gating.
- Correct answers should not be visually cued by being consistently longest or shortest; `scripts/validate_hard50.py` checks option length, answer distribution, and diagnostic coverage.
- Safety items keep go/no-go reasoning at a high level and avoid hazardous operational details.
