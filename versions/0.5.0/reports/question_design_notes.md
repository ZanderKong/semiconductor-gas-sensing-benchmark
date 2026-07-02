# Question Design Notes

## 设计原则

题目设计的核心不是让模型“看不懂”，而是让模型在看似熟悉的科学语境中暴露错误选择路径。有效题目通常具备三个特征：决定性约束清晰、干扰项局部合理、错误原因可复盘。

## 选项设计

| Option Type | Purpose |
|---|---|
| Best answer | 必须对应题干中的决定性约束，而不是泛泛正确 |
| Near-miss distractor | 与关键词或相邻概念相关，但忽略一个关键条件 |
| Over-generalized answer | 科学上可能成立，但不适用于当前条件 |
| Intermediate-value trap | 数值或过程正确一半，但不是最终答案 |
| Safety-adjacent distractor | 看似谨慎，但没有命中当前一阶风险 |

## Failure-Mined Item Families

| Family | Design Insight |
|---|---|
| high_information_pattern_rule | 短题干压缩高信息规则，模型容易用关键词替代专家约定 |
| structure_property_preference | 需要从结构或候选性质中提取决定变量，泛泛开发语言会失效 |
| specific_safety_hazard | 多个选项都与安全相关，但只有一个对应当前条件下的一阶风险 |
| expert_multistep_reasoning | 正确答案依赖隐藏前提、跨步骤公式或专家概念边界 |
| quantitative_precision | 公式、单位、符号、数量级和最终答案格式必须同时正确 |
| domain_rule_boundary | 相邻概念都合理，但只有一个满足题干边界 |

## 两道人工实验现象题的启发

4-苯氧基苯胺纸带题的关键不在“喷洒次氯酸钠变色”，而在实验员把不水溶物质当作水溶液浸渍。正确下一步是检查溶解与分散均匀性，而不是继续解释显色机制。

硝酸银纸基材料题的关键不在氧化物路径，而在光照产物粒径和颜色之间的经验关系。正确下一步可以是增加硝酸银用量，以改变反应物颗粒尺度和最终颜色。

这类题适合继续扩展，因为它们来自真实实验观察，答案依赖隐含物性、制备路径和经验判断，不容易被模板化科学常识直接覆盖。
