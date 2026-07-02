# Model Diagnostic Report

## Summary

SGS152 的三模型结果显示，legacy SGS100 已不足以稳定区分头部模型；failure-mined design bank 是 0.5.0 的主要区分来源。

| Model | SGS152 MCQ | Legacy SGS MCQ | Failure-mined MCQ |
|---|---:|---:|---:|
| DeepSeek V4 Pro | 98 / 122 | 77 / 82 | 21 / 40 |
| GPT-5.5 | 95 / 122 | 80 / 82 | 15 / 40 |
| MiMo v2.5 Pro | 93 / 122 | 77 / 82 | 16 / 40 |

## Failure Drivers

| Driver | Why It Hurts Models |
|---|---|
| High-information rule compression | 题干短，但答案依赖谱图模式、学科约定或隐藏条件；模型容易抓关键词而忽略决定性特征。 |
| Quantitative precision | 单位、符号、数量级和最终答案格式必须同时正确；模型常把中间量或近似量当最终答案。 |
| Near-miss distractors | 干扰项与题面关键词高度相关，局部合理但整体错误，容易诱导语义匹配式选择。 |
| Expert boundary conditions | 题目需要先识别适用前提，再套公式或规则；模型常把相邻概念迁移到不适用场景。 |
| Safety specificity | 多个选项都“看起来安全相关”，但只有一个是当前条件下的一阶风险。 |

## Model Notes

DeepSeek 在 failure-mined MCQ 上最高，说明其对部分规则型和定量型题目的恢复能力更强；但 legacy SGS 中仍有少量材料研发语境判断错误。

GPT-5.5 在 legacy SGS 上最高，但 failure-mined MCQ 最低，说明强通用推理不等于对高压短题、强干扰项和精确答案格式的稳定恢复。

MiMo 在 robustness 上最好，但 SGS152 active MCQ 最低，说明其相近题面稳定性较好，但面对新增高压机制时仍会被局部合理干扰项带偏。

## Design Implication

后续题库应继续采用两层结构：一层保留气敏研发真实工作流，另一层保留能让强模型出错的失败机制。真正有价值的题目不是“难懂”，而是能够让模型在看似熟悉的科学语境中暴露错误选择路径。
