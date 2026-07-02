# Mechanism Transfer Protocol

早期换皮实验表明，把高压题完整改写成气敏语境会显著降低难度。因此 0.5.0 不再把 failure-mined items 强行换皮，而是保留题目机制，并只在元数据中记录设计心得。

## When Transfer Is Acceptable

| Condition | Requirement |
|---|---|
| Key constraint preserved | 改写后仍由同一个决定性约束确定答案 |
| Distractors remain close | 干扰项仍局部合理，不能被表面排除 |
| No extra cueing | 题干不能因为加入领域背景而提示答案 |
| Error remains attributable | 模型答错后能明确归因到规则、单位、边界或干扰项 |

## When To Avoid Transfer

- 原题难度来自短题干压缩信息，扩写会直接降低难度。
- 原题干扰项几何结构很强，替换选项会破坏误导性。
- 领域化后正确答案变成“保守综合评估”等模板化选项。
- 改写后只剩常识判断，失去专家规则或定量精度。
