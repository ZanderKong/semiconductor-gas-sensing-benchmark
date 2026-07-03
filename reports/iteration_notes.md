# Iteration Notes

## 0.4.0 到 0.5.0

0.4.0 证明 Domain Core Set 的专业任务结构成立。题库能够把半导体气敏材料研发中的文献分析、实验设计、结果分析和安全边界转成可评分样本。

0.4.0 的问题是高分聚集。GPT-5.5 和 MiMo v2.5 Pro 在 82 道主集 MCQ 中均为 80 / 82，DeepSeek V4 Pro 为 76 / 82。该结果说明常规研发判断层对强模型的区分度有限。

0.5.0 的主要变化：

- 引入 SGS152 Main Set；
- 增加 Scientific Stress Set；
- 保留 Robustness Set；
- 增加 Hard Diagnostic Set；
- 修复 MCQ prompt 对 E 选项和变长选项支持不足的问题；
- 完成 30 道 free-response 全量 rubric review；
- 将 active package 提升到根目录；
- 将历史版本压缩为轻量 archive。

## 当前发现

Domain Core Set 仍适合作为专业任务覆盖层。Scientific Stress Set 更适合观察强模型边界。Hard Diagnostic Set 当前分数过高，需要下一版重校准。

Free-response 评分已经形成闭环，但 live transcript、judge adjudication 和人工复核一致性还需要补齐。

## 下一版优先级

1. 重校准 Hard Diagnostic Set。
2. 增加 Scientific Stress 中的计算、谱图、结构性质和安全题。
3. 将低区分度 Domain Core 题移入 warm-up。
4. 为 free-response 增加 live transcript 和复核标注。
5. 在 `data/item_design_index.csv` 中加入 item-level performance。
