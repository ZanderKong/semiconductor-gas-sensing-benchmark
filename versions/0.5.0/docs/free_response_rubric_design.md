# Free-Response Rubric Design

0.5.0 共有 30 道 free-response 题，每题使用 10 分制 rubric。Rubric 目标是让人工审阅能稳定区分“最终答案正确但过程不清”“过程接近但单位/格式错误”“被相邻概念诱导”等常见情况。

## Rubric Structure

| Criterion | Points | Purpose |
|---|---:|---|
| final_answer_alignment | 3 | 最终答案是否匹配参考答案 |
| calculation_or_rule_path | 2 | 是否使用正确公式、规则或学科约定 |
| unit_and_format_control | 2 | 单位、符号、数量级和格式是否可比 |
| distractor_resistance | 2 | 是否避开已知失败机制或中间量陷阱 |
| conciseness_and_traceability | 1 | 推理是否便于审阅、最终答案是否可定位 |

## Design Notes

- Legacy SGS free-response 偏向实验方案、证据链和安全边界，需要检查回答是否可执行、可验证且不暴露私有配方。
- Failure-mined free-response 偏向精确规则、单位控制和最终答案抽取，重点检查模型是否把中间量误当最终答案。
- 所有 rubric 均保存在 `data/free_response_rubrics.json`，并同步嵌入 active benchmark 的 free-response item 中。
