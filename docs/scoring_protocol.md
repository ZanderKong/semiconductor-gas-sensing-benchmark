# Scoring Protocol v0.6.0

## MCQ

122 道 SGS152 MCQ 是唯一主排行榜。评分采用冻结 Gold 的 exact match；空输出、无法解析、多选或不在当前 options 中的字母均计错。v0.6.0 不根据审计结果改写历史 Gold，因此应结合 488 选项审计和 56 个可辩护非 Gold 选项解释分数。

## Free-response

30 道 free-response 不并入主排行榜。GPT-5.6-sol 仅作为 Judge，为每条回答生成 provisional rubric 评分。每条回答按以下 8 个维度评分，每维最高 1.25，总分 10：

1. `final_answer_alignment`；
2. `professional_accuracy`；
3. `reasoning_path`；
4. `evidence_boundary`；
5. `experimental_design`；
6. `decision_logic`；
7. `safety_and_privacy`；
8. `conciseness_and_traceability`。

专家 X 对 120 条回答和 960 条维度分进行复核。普通缺陷——如缺公式、单位、空白、实验矩阵、go/no-go、证据边界或回答过短——只通过维度扣分处理，不自动归零。

## Missing answer and confirmed Hard Fail

自动 Judge 的 Hard Fail 只视为 provisional。官方逐题分按以下确定性规则计算：

```text
if no_answer:
    official_item_score = 0
elif confirmed_hard_fail:
    official_item_score = 0
else:
    official_item_score = reviewed_dimension_total
```

已确认 3 条 MiMo Hard Fail：

- `SGS-082`：数据完整性；
- `SGS-FM-FR-007`：安全；
- `SGS-FM-FR-011`：数据完整性。

其余 12 条历史 Hard Fail 降级为普通维度问题。DeepSeek `SGS-081` 为原始缺答，按 no-rescue 规则计 0。

## Official free-response averages

| Model | Reviewed | Official |
|---|---:|---:|
| GPT-5.5 | 8.213 | 8.213 |
| Seed-2.1 | 7.545 | 7.545 |
| DeepSeek V4 Pro | 6.732 | 6.732 |
| MiMo v2.5 Pro | 5.257 | 4.952 |

逐题、逐维度和 override 记录见 [`review/v0.6.0/04_free_response_adjudication/`](../review/v0.6.0/04_free_response_adjudication/)。
