# Optimization Retrospective

## What Changed

0.5.0 曾尝试把外部失败机制迁移成气敏材料语境题。测试显示，换皮后的题反而更容易，被强模型快速答对。原因不是模型突然更强，而是改写过程改变了原题的压力结构。

## Why Reskinning Failed

| Issue | Effect |
|---|---|
| Added domain context | 让模型获得更多提示，降低短题干压力 |
| Softer wording | 把强约束改成常规研发建议，削弱唯一答案 |
| Removed original distractor geometry | 干扰项不再贴近正确项，模型更容易排除 |
| Over-aligned with safety language | 让“保守综合评估”类答案变得过于显眼 |

## 0.5.0 Adjustment

SGS152 保留失败机制本身，只清理元数据和评分说明。新增题不写来源，改为记录设计心得：该题为什么会误导模型，干扰项利用了哪些相邻概念，正确答案依赖什么关键约束。

## Practical Lesson

强模型区分题应该先保留有效失败机制，再考虑领域化表达。若必须改写，应逐项验证：题干是否仍短、选项是否仍近、答案是否仍唯一、错误是否仍可归因。

## Next Iteration

- 扩展人工真实实验现象题。
- 保留能让至少一个强模型稳定出错的题。
- 删除三模型全对且错误机制不清晰的题。
- 对 free-response 增加人工评分样例，验证 rubric 是否足够稳定。
