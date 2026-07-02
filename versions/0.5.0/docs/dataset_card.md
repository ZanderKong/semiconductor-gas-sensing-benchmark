# Dataset Card

## 中文

| Item | Value |
|---|---:|
| Dataset | Semiconductor Gas-Sensing Mini-Benchmark |
| Version | 0.5.0 |
| Active main set | SGS152 |
| Total items | 152 |
| Multiple-choice | 122 |
| Free-response | 30 |
| Legacy SGS100 clean export | 100 |
| Failure-mined design bank | 52 |
| Robustness layer | 40 variants |
| Hard diagnostic set | 50 MCQ |
| Language | Chinese and English |

### 数据构成

| Component | Items | MCQ | Free-response |
|---|---:|---:|---:|
| Legacy SGS100 domain set | 100 | 82 | 18 |
| Failure-mined design bank | 52 | 40 | 12 |
| Active SGS152 | 152 | 122 | 30 |

领域分布：organic_chemistry 19, physical_chemistry 14, inorganic_chemistry 14, materials_science 14, general_chemistry 43, analytical_chemistry 10, technical_chemistry 10, toxicity_and_safety 8, expert_science_reasoning 12, quantitative_science 8。

### 设计原则

- Legacy SGS100 评估半导体气敏材料研发中的材料选择、机理判断、表征解释、实验设计、数据质量和安全边界。
- Failure-mined design bank 保留模型真实失败过的题目机制，元数据只记录设计心得、干扰项意图和评分规则。
- MCQ 采用 exact-match 自动评分；free-response 使用 10 分制 rubric。
- Robustness variants 与 active main set 分离，用于检验相近题面下判断原则是否稳定。
- 数据集不包含私有配方比例、实验室内部项目号、供应商批号或危险操作步骤。

## English

SGS152 is the active 0.5.0 benchmark. It combines the legacy SGS100 domain set with a 52-item failure-mined design bank. The added items preserve hard failure mechanisms and expose design notes instead of source provenance.

MCQ scoring is exact-match against the item answer key. Free-response scoring uses 10-point rubrics covering final-answer alignment, rule/calculation path, unit and format control, distractor resistance, and traceability.
