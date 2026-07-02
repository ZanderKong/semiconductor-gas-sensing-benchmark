# Reviewer Guide

这份指南用于帮助 reviewer、interviewer 和 technical reader 快速理解 Semiconductor Gas-Sensing Mini-Benchmark 0.5.0。

## 推荐阅读顺序

| Step | File | 阅读重点 |
|---:|---|---|
| 1 | `README.md` | 项目定位、题库组成、模型结果 |
| 2 | `reports/project_strategy_report.md` | 0.5.0 为什么采用 SGS152 |
| 3 | `reports/question_design_notes.md` | 题目、选项、陷阱和设计心得 |
| 4 | `reports/model_evaluation_recap.md` | DeepSeek、GPT-5.5、MiMo 主集结果 |
| 5 | `reports/optimization_retrospective.md` | 换皮失败、保留失败机制的原因 |
| 6 | `docs/dataset_card.md` | 数据构成、评分方式和边界 |
| 7 | `reports/release_readiness_audit.md` | 完整性、一致性和验证记录 |

## 审阅要点

- SGS152 是 active 主集；legacy SGS100 保留专业气敏研发场景，failure-mined design bank 提供强模型压力测试。
- 新增题的公开来源信息不写入题库；元数据只记录设计机制、干扰项意图和评分逻辑。
- Robustness variants 用于检查相近题面下的判断稳定性；SGS-Hard-50 用于额外诊断条件更新、证据冲突、安全 gate 和研发取舍。
- 所有发布必要数据均在仓库内，`scripts/build_sgs152_merged.py` 可从仓库内输入重建 active benchmark。
