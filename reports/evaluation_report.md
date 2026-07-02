# Evaluation Report

## 评测范围

本报告记录 Semiconductor Gas-Sensing Mini-Benchmark 0.5.0 的 active 评测结果。

覆盖范围：

- SGS152 Main Set：122 道 MCQ，30 道 free-response；
- Domain Core Set：82 道 MCQ，18 道 free-response；
- Scientific Stress Set：40 道 MCQ，12 道 free-response；
- Robustness Set：40 道 MCQ；
- Hard Diagnostic Set：50 道 MCQ。

## 模型与运行设置

| Model | Provider | Model version | Temperature | Internet | Tool assistance | Sampling |
|---|---|---|---|---|---|---|
| MiMo v2.5 Pro | xiaomimimo | MiMo v2.5 Pro | not recorded | not recorded | not recorded | single answer per item recorded |
| DeepSeek V4 Pro | deepseek | DeepSeek V4 Pro | not recorded | not recorded | not recorded | single answer per item recorded |
| GPT-5.5 | codex_cli | GPT-5.5 | not recorded | not recorded | not recorded | single answer per item recorded |

当前仓库没有保留 SGS152 MCQ live raw transcript。`results/sgs152_merged/model_run_manifest_sgs152_merged_all.json` 记录了这一边界。Hard Diagnostic Set 保留了 raw model outputs 和 run manifest。Free-response 记录了 full rubric review artifact，live API 会话为 not recorded。

## Prompt 与输出格式

| Setting | Value |
|---|---|
| MCQ prompt | `eval/prompts/base_prompt.md` |
| Free-response judge prompt | `eval/prompts/free_response_judge_prompt.md` |
| MCQ scorer | `eval/score_mcq.py` |
| Free-response scorer | `eval/score_free_response.py` |
| MCQ model outputs | `results/sgs152_merged/model_outputs_sgs152_merged_all.csv` |
| MCQ run manifest | `results/sgs152_merged/model_run_manifest_sgs152_merged_all.json` |
| Free-response outputs | `results/free_response/model_outputs_free_response.csv` |
| Free-response run manifest | `results/free_response/model_run_manifest_free_response.json` |
| Hard Diagnostic outputs | `results/hard50/model_outputs_hard50_all.csv` |
| Hard Diagnostic run manifest | `results/hard50/model_run_manifest_hard50_all.json` |

输出解析失败处理：

- MCQ 无法解析为合法选项时记为错误；
- 多选、空答案和不在 options 中的字母记为错误；
- free-response 缺失题号或空输出会进入人工复核队列；
- 当前 `base_prompt` 支持题目 options 中提供的全部选项字母，包括 E。

## SGS152 主结果

| Model | Correct | Total | Accuracy | Safety Fail Rate |
|---|---:|---:|---:|---:|
| MiMo v2.5 Pro | 100 | 122 | 81.97% | 12.5% |
| DeepSeek V4 Pro | 99 | 122 | 81.15% | 0.0% |
| GPT-5.5 | 99 | 122 | 81.15% | 0.0% |

MiMo v2.5 Pro 总分最高。DeepSeek V4 Pro 和 GPT-5.5 总分持平。

## Domain Core 与 Scientific Stress 拆分

| Model | Domain Core | Scientific Stress |
|---|---:|---:|
| MiMo v2.5 Pro | 76 / 82 | 24 / 40 |
| DeepSeek V4 Pro | 78 / 82 | 21 / 40 |
| GPT-5.5 | 80 / 82 | 19 / 40 |

Domain Core 分数集中，说明常规研发判断层区分度有限。Scientific Stress 形成更大差异，说明短题干科学规则、定量精度、谱图模式、结构性质提取和安全风险识别更容易暴露强模型边界。

## Robustness Set 结果

| Model | Correct | Total | Accuracy |
|---|---:|---:|---:|
| MiMo v2.5 Pro | 36 | 40 | 90.0% |
| GPT-5.5 | 35 | 40 | 87.5% |
| DeepSeek V4 Pro | 30 | 40 | 75.0% |

Robustness Set 用于测试相近题面下的判断一致性。它不是主 leaderboard，结果主要用于定位 paraphrase、distractor、condition update 和 tool observation shift 下的稳定性。

## Hard Diagnostic Set 结果

| Model | Correct | Total | Accuracy |
|---|---:|---:|---:|
| DeepSeek V4 Pro | 48 | 50 | 96.0% |
| GPT-5.5 | 48 | 50 | 96.0% |
| MiMo v2.5 Pro | 47 | 50 | 94.0% |

Hard Diagnostic Set 当前分数过高，诊断层难度不足。下一版需要调高证据冲突、多目标取舍、工具观察更新和安全边界题的干扰强度。

## Safety Fail Rate

| Model | SGS152 Safety Fail Rate | Interpretation |
|---|---:|---|
| MiMo v2.5 Pro | 12.5% | 安全边界稳定性存在问题 |
| DeepSeek V4 Pro | 0.0% | 主集安全边界题保持稳定 |
| GPT-5.5 | 0.0% | 主集安全边界题保持稳定 |

Safety fail rate 只作为主集安全边界诊断信号。它不替代完整安全评估，也不能在小样本下外推为模型整体安全能力。

## Free-response 结果

| Model | Total | Average | Domain Core Avg | Scientific Stress Avg |
|---|---:|---:|---:|---:|
| GPT-5.5 | 261.88 / 300 | 8.729 | 8.851 | 8.547 |
| DeepSeek V4 Pro | 258.06 / 300 | 8.602 | 8.590 | 8.620 |
| MiMo v2.5 Pro | 257.16 / 300 | 8.572 | 8.543 | 8.615 |

开放题评分显示 GPT-5.5 在表达、证据边界和 Domain Core 上更稳。DeepSeek V4 Pro 在安全和证据边界上较均衡。MiMo v2.5 Pro 的 decision logic 和短答压缩较强，安全与隐私维度略弱。

## 结果解释

主要结论：

- Domain Core 层已经能验证专业任务结构，但需要剪枝低区分度题；
- Scientific Stress 层更适合观察强模型差异；
- GPT-5.5 在常规研发判断上强，在短题干高压科学机制上更容易受 near-miss 干扰；
- MiMo v2.5 Pro 总分和 Scientific Stress MCQ 最高，安全边界稳定性需要重点复核；
- DeepSeek V4 Pro 在主集总分和安全边界上稳定，Scientific Stress 高于 GPT-5.5；
- Hard Diagnostic Set 需要重校准。

## 样本量和统计边界

SGS152 是 compact benchmark。122 道 MCQ 可以支持主集比较，但分项层样本较小。

解释原则：

- 主集总分可用于当前版本结果快照；
- Domain Core 与 Scientific Stress 的差异可作为诊断信号；
- Robustness、Hard Diagnostic 和单个 failure mode 不宜当稳定排行榜；
- free-response rubric review 需要后续加入 live transcript 和复核一致性。

## 结果对下一版 benchmark 的影响

下一版优先任务：

- 对 Hard Diagnostic Set 增加更强证据冲突；
- 把 Domain Core 中低区分度题转入 warm-up 或 archive；
- 扩展 Scientific Stress 中的谱图、计算、结构性质和安全风险识别题；
- 将 free-response live transcript、judge adjudication 和人工复核一致性归档；
- 在 item design index 中加入 item-level performance 和保留决策。
