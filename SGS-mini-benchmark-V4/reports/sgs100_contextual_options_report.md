# SGS-100 V4 Contextual MCQ Options Report

Date: 2026-06-29

This report records the 2026-06-29 contextual-option rewrite audit.

The current clean-revision status is recorded in `reports/sgs100_revision_report.md`.

The current model-evaluation status is recorded in `reports/model_evaluation_recap.md`.

## What Changed

- Rewrote all 82 `multiple_choice.options` to remove option-only solvability.
- Kept question text, answers, metadata, and free-response items unchanged.
- Made distractors plausible standalone research actions, mechanism interpretations, controls, or safety/process choices.
- Wrong options are intended to be non-prioritized, insufficient, or overextended only in the local question context.

## Hard Checks

| Check | Result |
|---|---:|
| Answer distribution | A=21, B=21, C=20, D=20 |
| Option length ratio violations | 0 |
| Forbidden template phrase hits in options | 0 |
| Correct option length rank, longest=1 | {'2': 51, '3': 16, '4': 15} |
| Project validator | `python3 scripts/validate_benchmark.py` passed |
| Project linter | `python3 scripts/lint_benchmark.py` passed |

## Semantic Review

- GPT-5.5 option-plausibility reviewer score: `4/5`
- Reviewer verdict: 整体选项语义区分度较好，大多数错误项都是合理研发动作或边界判断，只是在题干情境下不优先。
- Final manual follow-up addressed the reviewer’s remaining flagged IDs: `SGS-009`, `SGS-096`, `SGS-097`, `SGS-098`.

## Model Evaluation

| Model | Correct / Total | MCQ Accuracy | Safety Fail Rate | Wrong IDs |
|---|---:|---:|---:|---|
| deepseek-v4-pro | 78 / 82 | 95.1% | 12.5% | SGS-009, SGS-028, SGS-097, SGS-098 |
| gpt-5.5 | 80 / 82 | 97.6% | 0.0% | SGS-001, SGS-028 |

Interpretation: the previous perfect-score pattern has been broken without reintroducing template leakage. The observed misses are now mainly context-priority errors such as substituent expectation, response metric direction, and safety/process boundary choices.

## Examples Of 10 Rewritten Questions

### SGS-001

某氯气显色纸带使用芳香胺作受体。配方在水加入后变浑浊，但干燥后仍能变色。下一步最稳妥的判断是？

Answer: `A`

Lengths: `{'A': 15, 'B': 15, 'C': 17, 'D': 15}`; ratio=1.133

- A. 复配澄清窗口并验证干膜均匀显色
- B. 保留微浑浊配方并做批间重复制样
- C. 提高芳香胺浓度并比较显色动力学曲线
- D. 调整酸度和溶剂比例评估析出边界

### SGS-002

PANI 薄膜对 NH3 响应很强，但 80%RH 下基线持续上移。最适合先排查的是？

Answer: `B`

Lengths: `{'A': 15, 'B': 15, 'C': 16, 'D': 14}`; ratio=1.143

- A. 增加膜厚并比较高湿下峰值保持率
- B. 拆分去质子化响应与吸水膨胀漂移
- C. 做湿度阶跃曲线并提取峰值滞后特征
- D. 调整酸掺杂水平并观察基线恢复

### SGS-003

金属卟啉阵列用于胺类气体识别。若某通道对水汽也响应，最合理的处理是？

Answer: `C`

Lengths: `{'A': 16, 'B': 15, 'C': 14, 'D': 14}`; ratio=1.143

- A. 在干燥样本集中剔除水敏通道再分类
- B. 提高卟啉负载以扩大量程内胺响应
- C. 引入湿度校正通道参与阵列模型
- D. 更换金属中心组合减少水汽亲和

### SGS-004

三芳甲烷类染料遇强氧化气体褪色明显。若目标是 NO2 定量，最需要加入的验证是？

Answer: `D`

Lengths: `{'A': 12, 'B': 14, 'C': 15, 'D': 13}`; ratio=1.25

- A. 补充高浓度 NO2 点确认响应上限
- B. 校准光源漂移并重复反射率读数
- C. 延长曝光窗口观察褪色动力学曲线
- D. 加入臭氧和氯气共存干扰验证

### SGS-005

某荧光受体在极性溶剂中长波发射增强。把它用于气敏薄膜时，最不能直接推出的是？

Answer: `A`

Lengths: `{'A': 12, 'B': 13, 'C': 14, 'D': 13}`; ratio=1.167

- A. 把薄膜气体响应归因为 TICT 主导
- B. 把极性扰动列为响应机制线索
- C. 评估薄膜微环境对谱带位置影响
- D. 补做湿度和溶剂残留干扰对照

### SGS-006

VOC 传感膜改用更亲有机溶剂的粘结剂后，甲苯响应增大但恢复变慢。最佳解释是？

Answer: `B`

Lengths: `{'A': 15, 'B': 14, 'C': 15, 'D': 14}`; ratio=1.071

- A. 导电通道重构放大响应并拖慢回稳
- B. 吸附分配增强但脱附动力学受限
- C. 膜内溶胀提高扩散阻力并延长恢复
- D. 腔体滞留造成表观恢复时间拉长

### SGS-007

氨基硅烷修饰 SiO2 载体用于酸性气体捕获。高湿下响应反而下降，优先考虑什么？

Answer: `C`

Lengths: `{'A': 14, 'B': 14, 'C': 14, 'D': 16}`; ratio=1.143

- A. 用干态酸气复测硅烷层捕获活性
- B. 提高温度降低水覆盖并观察恢复
- C. 验证水竞争吸附或硅烷水解贡献
- D. 降低载气湿度建立干态响应基线参照

### SGS-008

醛酮类 VOC 检测拟采用肼类衍生物显色。方案评审中最应优先追问的是？

Answer: `D`

Lengths: `{'A': 15, 'B': 14, 'C': 13, 'D': 13}`; ratio=1.154

- A. 量化摩尔吸光系数和显色线性范围
- B. 比较衍生物色相与读数窗口匹配
- C. 确认肉眼报警阈值和响应时间
- D. 评审肼类暴露控制和废液处置

### SGS-009

比较甲氧基苯胺和硝基苯胺作氧化显色受体，最稳妥的预期是？

Answer: `A`

Lengths: `{'A': 14, 'B': 16, 'C': 16, 'D': 16}`; ratio=1.143

- A. 甲氧基供电子使芳胺更易被氧化
- B. 硝基降低电子云密度但可能改变色相
- C. 溶解稳定性差异会影响表观显色强度
- D. 两者自氧化风险主要受保存条件影响

### SGS-010

酸碱指示剂膜对 NH3 可逆变色。若用于报警纸带，最应补充哪项测试？

Answer: `B`

Lengths: `{'A': 14, 'B': 14, 'C': 13, 'D': 16}`; ratio=1.231

- A. 测单次颜色差确定初始报警阈值
- B. 做循环暴露恢复和基线漂移测试
- C. 补干燥空气空白评估载气扰动
- D. 调整采样距离比较报警触发时间窗口
