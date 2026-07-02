# Model Evaluation Recap

## 评测配置

| Item | Value |
|---|---|
| Version | mini-benchmark 0.5.0 |
| Active benchmark | `data/benchmark.json` |
| Active main set | SGS152 |
| Scored subset | 122 MCQ |
| Free-response items | 30 rubric-scored items |
| Prompt | `eval/prompts/base_prompt.md` |
| Runner | `eval/run_eval.py` |
| Scorer | `eval/score_mcq.py` |

## Active SGS152 MCQ

| Model | Correct / Total | Accuracy | Safety Fail Rate |
|---|---:|---:|---:|
| DeepSeek V4 Pro | 98 / 122 | 80.3% | 0.0% |
| GPT-5.5 | 95 / 122 | 77.9% | 0.0% |
| MiMo v2.5 Pro | 93 / 122 | 76.2% | 6.2% |

## Split Diagnosis

| Model | Legacy SGS MCQ | Failure-mined MCQ |
|---|---:|---:|
| DeepSeek V4 Pro | 77 / 82 (93.9%) | 21 / 40 (52.5%) |
| GPT-5.5 | 80 / 82 (97.6%) | 15 / 40 (37.5%) |
| MiMo v2.5 Pro | 77 / 82 (93.9%) | 16 / 40 (40.0%) |

SGS152 的区分度主要来自新增的 failure-mined 40 道 MCQ。Legacy SGS 部分三模型都接近满分；新增部分则把三模型拉到 37.5% 到 52.5%，更容易观察强模型在精确规则、定量抽取、多步推理和强干扰项上的失败。

## Memory Check

用户记忆与 0.4.0 归档记录一致：

| Model | 0.4.0 Main MCQ | Robustness |
|---|---:|---:|
| MiMo v2.5 Pro | 80 / 82 | 36 / 40 |
| GPT-5.5 | 80 / 82 | 35 / 40 |
| DeepSeek V4 Pro | 76 / 82 | 30 / 40 |

SGS152 split 中 DeepSeek 和 MiMo 的 legacy SGS 分数为 77 / 82，这是本轮 SGS152 合并输出中的实际拆分结果；它不覆盖 0.4.0 归档结果。

## Robustness And Hard Set

| Model | Robustness | SGS-Hard-50 |
|---|---:|---:|
| MiMo v2.5 Pro | 36 / 40 | 47 / 50 |
| GPT-5.5 | 35 / 40 | 48 / 50 |
| DeepSeek V4 Pro | 30 / 40 | 48 / 50 |

## Interpretation

SGS100 证明模型已经具备较强的常规专业场景解题能力；SGS152 进一步加入失败机制明确的高压题，使模型差异从“接近满分”变成可观察的错误分布。后续迭代应优先保留能造成稳定差异的题，并删除三模型同时稳定答对、解释路径单一的低区分度题。
