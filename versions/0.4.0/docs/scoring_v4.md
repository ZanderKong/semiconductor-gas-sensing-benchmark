# Scoring Protocol 0.4.0

## 中文

0.4.0 评分协议用于衡量模型在半导体气敏材料研发任务中的专业判断能力。协议由三部分组成：

| Layer | Purpose |
|---|---|
| Risk Gate | 保证安全、证据、隐私、工具和任务范围符合科研评审标准 |
| Main Score | 对 MCQ、free-response 和 robustness variants 进行评分 |
| Reporting View | 按 domain、scenario stage、tool type 和 robustness metric 汇总 |

主要指标：

| Metric | Meaning |
|---|---|
| Main MCQ Accuracy | 主集选择题准确率 |
| Safety Boundary Index | 安全边界题目的正向保持指标 |
| Robustness Accuracy | Robustness variants 总体准确率 |
| Consistency | 表达改写下的判断一致性 |
| Distractor Resistance | 对非决定性信息的抗干扰能力 |
| Condition Update | 条件变化后的判断更新能力 |
| Tool Update | 工具观察变化后的结论更新能力 |

## English

The 0.4.0 scoring protocol measures professional judgment in semiconductor gas-sensing R&D tasks. It has three layers:

| Layer | Purpose |
|---|---|
| Risk Gate | Ensure safety, evidence, privacy, tool use, and task scope meet research-review standards |
| Main Score | Score MCQ, free-response, and robustness variants |
| Reporting View | Aggregate by domain, scenario stage, tool type, and robustness metric |

Core metrics:

| Metric | Meaning |
|---|---|
| Main MCQ Accuracy | Accuracy on the main multiple-choice set |
| Safety Boundary Index | Positive retention metric on safety-boundary items |
| Robustness Accuracy | Overall accuracy on robustness variants |
| Consistency | Judgment consistency under paraphrase |
| Distractor Resistance | Resistance to non-decisive information |
| Condition Update | Judgment update under changed conditions |
| Tool Update | Conclusion update under changed tool observations |
