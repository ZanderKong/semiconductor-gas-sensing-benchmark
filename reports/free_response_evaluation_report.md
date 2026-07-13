# Free-response Evaluation Report

## 评测范围

本报告覆盖 SGS152 Main Set 的全部 30 道 free-response：18 道 Domain Core 和 12 道 Scientific Stress。四个参评模型各有 30 条冻结输出；GPT-5.6-sol 仅担任 judge。

## 评分协议

每题按 8 个维度评分，每维 0–1.25，总分 10：final answer alignment、professional accuracy、reasoning path、evidence boundary、experimental design、decision logic、safety and privacy、conciseness and traceability。先检查题目定义的 risk gates；hard fail 单独计数但不改写原总分。

Judge 设置为 temperature 0、无联网、无工具、每模型一批单次采样、无重试或人工修复。四批均返回 30 条唯一评分。

## 汇总结果

| Model | Average | Hard Fails |
|---|---:|---:|
| GPT-5.5 | 8.150 | 0 |
| Seed-2.1 | 7.493 | 4 |
| DeepSeek V4 Pro | 6.722 | 0 |
| MiMo v2.5 Pro | 5.440 | 11 |

## 主要观察

- 四模型共同的薄弱环节是明确的 decision logic、证据边界和可判别实验设计。
- MiMo 的开放题结果与其主榜表现差异最大，说明 exact-match MCQ 不能替代过程性研发判断。
- Seed-2.1 的 risk gates 主要来自缺少决定性对照、定量关系或工艺取样控制。
- DeepSeek `SGS-081` 缺答，按 no-rescue 规则计 0。
- GPT-5.5 得分最高，但 GPT-5.6-sol 与其同属 GPT 家族，仍需独立人工抽查可能的家族相关性。

## 当前边界

结果是 GPT-5.6-sol automated judge score，不是独立盲审。58 条 review packet 已生成，所有人工字段保持为空。旧 GPT-5.5 judge 裁决仅作为历史证据归档，不沿用到当前分数。
