# SGS-100 Revision Report

## 中文

### 修订目标

0.4.0 版本将题库收敛为结构清晰、比例稳定、可自动校验的 SGS-100 主集。修订重点包括题型比例、选项质量、rubric 结构、consistency fields 和安全抽象表达。

### 主集结构

| Metric | Value |
|---|---:|
| Main-set item count | 100 |
| Multiple-choice items | 82 |
| Free-response items | 18 |
| Answer distribution | A=21, B=21, C=20, D=20 |
| Domain coverage | 8 domains |

### 修订成果

- MCQ 选项完成长度均衡和局部合理性重构。
- 每道 MCQ 配置 option-level rationale，用于解释选项在当前语境中的优先级。
- 每道主集题目配置 consistency fields，为 robustness 扩展提供 parent linkage。
- 每道 free-response 配置 10 分制 rubric、key points、risk gates 和 scoring notes。
- 数据文件同时提供 JSON 与 CSV 版本，服务自动评测和人工审阅。

## English

### Revision Objective

Version 0.4.0 consolidates the benchmark into a clean, proportionally stable, and automatically validated SGS-100 main set. The revision focuses on type balance, option quality, rubric structure, consistency fields, and safety-aware abstraction.

### Main-Set Structure

| Metric | Value |
|---|---:|
| Main-set item count | 100 |
| Multiple-choice items | 82 |
| Free-response items | 18 |
| Answer distribution | A=21, B=21, C=20, D=20 |
| Domain coverage | 8 domains |

### Revision Outcomes

- Rebuilt MCQ options for length balance and local plausibility.
- Added option-level rationales to explain priority within each local context.
- Added consistency fields to every main-set item for robustness linkage.
- Added 10-point rubrics, key points, risk gates, and scoring notes to every free-response item.
- Provided both JSON and CSV exports for automatic evaluation and table-based review.
