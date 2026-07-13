
# GPT-5.6-sol Judge Reliability Report

## 样本

- 120 条开放题回答；
- Judge 基线：GPT-5.6-sol；
- 复核基线：v0.6.0 post-hoc evidence-assisted secondary adjudication。

## 分数一致性

详细 MAE、RMSE、Pearson 和 Spearman 见 `judge_reliability_metrics.csv`。

由于第二轮评分参考了现有 Judge 结果，本报告中的相关系数会高估真正独立评审一致性。它适合发现异常和政策错配，不能替代外部盲评一致性研究。

## Hard Fail

- Judge/provided adjudication positive：15
- v0.6.0 confirmed：3
- true positive：3
- false positive：12
- precision：20.0%
- recall：100.0%
- Cohen's kappa：0.304

主要问题是 **Hard Fail 定义过宽**。多条回答只是缺少公式、对照、矩阵或决策条件，却被归入一票否决。

## 同家族偏差观察

GPT-5.5 的平均复核减 Judge 差值为 `+0.063`，其他模型为 `-0.066`。

这一差异不能单独证明同家族偏差，因为：

- 本轮不是独立盲评；
- 模型回答质量不同；
- 评分调整以风险门政策变化为主；
- 样本只有 30 题/模型。

v0.6.0 应把它写为 `same-family correlation risk investigated but not conclusively estimated`。

## 结论

GPT-5.6-sol 的普通分数排序可作为有用基线；Hard Fail 分类需要项目级政策层和二次确认。v0.6.0 不应允许自动 Judge 的 provisional gate 直接归零。
