# Project Strategy Report

## 目标

0.5.0 的目标不是单纯扩题，而是建立一套能同时展示专业场景能力和强模型区分度的 mini-benchmark。SGS152 将 legacy SGS100 与 failure-mined design bank 合并，形成一个更适合迭代筛题的 active set。

## 结构选择

| Layer | Role | Why It Matters |
|---|---|---|
| Legacy SGS100 | 半导体气敏材料研发语境 | 保留项目主题和专业判断基础 |
| Failure-mined design bank | 强模型失败机制 | 提高区分度，暴露规则、单位、干扰项和多步推理错误 |
| Robustness variants | 相近题面稳定性 | 检查模型是否坚持同一判断原则 |
| SGS-Hard-50 | 额外诊断 | 聚焦条件更新、证据冲突、安全 gate 和研发取舍 |

## 核心判断

强模型在常规专业题上已经接近满分；如果题目过度“解释清楚”或换成更熟悉的领域语境，难度会下降。因此 0.5.0 采用“专业主线 + 失败机制主线”的组合，而不是把所有题都改写成统一风格。

## 当前结果

| Model | SGS152 MCQ | Failure-mined MCQ |
|---|---:|---:|
| DeepSeek V4 Pro | 98 / 122 | 21 / 40 |
| GPT-5.5 | 95 / 122 | 15 / 40 |
| MiMo v2.5 Pro | 93 / 122 | 16 / 40 |

结果说明 SGS152 已经从 0.4.0 的高分聚集状态，转向更有错误结构的强模型比较。
