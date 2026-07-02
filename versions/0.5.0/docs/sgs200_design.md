# SGS200 Design Notes

SGS200 是 0.5.x 到 0.6.0 的扩展方向。当前 active SGS152 已覆盖半导体气敏材料研发判断、失败机制复测、robustness variants 和 Hard-50 诊断；下一版应在不削弱题目压力结构的前提下继续扩充。

## Expansion Targets

| Target | Design Need |
|---|---|
| Explicit calculation | 增加 LOD/LOQ、Arrhenius、标准曲线、XRD、漂移和响应恢复计算 |
| Evidence retrieval | 加入文献证据定位、表征证据冲突和引用边界判断 |
| Structured extraction | 从表格、实验记录、配方摘要和批次数据中抽取关键变量 |
| Realistic lab observations | 增加人工编写的真实实验现象题，答案依赖隐含物性和实验路径 |
| Failure-mechanism preservation | 保留短题干、高信息规则、强干扰项和中间量陷阱 |
| Multi-modal future work | 为图谱、图像和传感曲线理解预留任务槽 |

## Design Principle

扩展题库时不要为了统一主题而削弱原有压力结构。能区分强模型的题目通常依赖一个清晰但容易被忽略的关键约束；改写时必须确保该约束仍然是唯一决定因素。
