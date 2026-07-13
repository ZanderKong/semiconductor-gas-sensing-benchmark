# Evaluation Report — SGS152 v0.6.0

## Main leaderboard

122 道 SGS152 MCQ 是唯一主排行榜。四个参赛模型得分为 115–119/122，说明主集高度饱和；差异由少数题目决定，并受冻结 Gold 中已披露问题影响。

| Model | Correct | Accuracy |
|---|---:|---:|
| MiMo v2.5 Pro | 119 | 97.54% |
| Seed-2.1 | 118 | 96.72% |
| GPT-5.5 | 117 | 95.90% |
| DeepSeek V4 Pro | 115 | 94.26% |

## Free-response

GPT-5.6-sol 仅作为 Judge，不是参赛模型。专家 X 对 120 条回答和 960 条维度评分完成逐条复核。

| Model | Reviewed average | Official average |
|---|---:|---:|
| GPT-5.5 | 8.213 | 8.213 |
| Seed-2.1 | 7.545 | 7.545 |
| DeepSeek V4 Pro | 6.732 | 6.732 |
| MiMo v2.5 Pro | 5.257 | 4.952 |

MiMo 有 3 个 confirmed Hard Fail，官方逐题分归零；12 个其他历史 Hard Fail 降级为维度问题。DeepSeek `SGS-081` 为原始缺答并保持 0。

## Diagnostic sets

- Robustness：四模型 29–34/40；有 2 个冻结 P0，仅作可选诊断；
- Hard50：四模型 47–48/50，高度饱和，仅作 regression diagnostic；
- 56 个可辩护非 Gold 选项说明 MCQ exact match 需与选项审计共同解释。

## Evidence boundary

v0.6.0 不修改题库内容或原始输出。原始证据 46 个 ZIP 成员已逐哈希验证；四个任务层和 Judge 产物可确定性重建，逐字段差异为 0。本轮未采用独立盲审设计。
