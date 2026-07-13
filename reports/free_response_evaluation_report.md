# Free-response Evaluation Report — v0.6.0

30 道 free-response 对四个参赛模型产生 120 条回答。GPT-5.6-sol 仅作为 Judge 生成 provisional 八维评分；专家 X 完成逐题与逐维度复核，项目负责人确认官方评分政策。

| Model | Reviewed | Official | Confirmed HF | Downgraded HF | No answer |
|---|---:|---:|---:|---:|---:|
| GPT-5.5 | 8.213 | 8.213 | 0 | 0 | 0 |
| Seed-2.1 | 7.545 | 7.545 | 0 | 4 | 0 |
| DeepSeek V4 Pro | 6.732 | 6.732 | 0 | 0 | 1 |
| MiMo v2.5 Pro | 5.257 | 4.952 | 3 | 8 | 0 |

普通遗漏和证据边界问题只通过维度扣分处理。三个 confirmed Hard Fail 与 DeepSeek 缺答按 [`docs/scoring_protocol.md`](../docs/scoring_protocol.md) 归零。本轮未采用独立盲审设计。
