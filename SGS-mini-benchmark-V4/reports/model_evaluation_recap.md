# Model Evaluation Recap

## 中文

### 评测配置

| Item | Value |
|---|---|
| Version | mini-benchmark 0.4.0 |
| Main benchmark | `data/benchmark.json` |
| Main scored subset | 82 MCQ |
| Robustness benchmark | `data/benchmark_sgs100_robustness.json` |
| Robustness scored subset | 40 MCQ variants |
| Prompt | `eval/prompts/base_prompt.md` |
| Runner | `eval/run_eval.py` |
| Scorer | `eval/score_mcq.py` |

### 主集结果

| Model | Correct / Total | Accuracy | Safety Boundary Index |
|---|---:|---:|---:|
| MiMo v2.5 Pro | 80 / 82 | 97.6% | 100.0% |
| GPT-5.5 | 80 / 82 | 97.6% | 100.0% |
| DeepSeek V4 Pro | 76 / 82 | 92.7% | 87.5% |

### Robustness 结果

| Model | Correct / Total | Accuracy |
|---|---:|---:|
| MiMo v2.5 Pro | 36 / 40 | 90.0% |
| GPT-5.5 | 35 / 40 | 87.5% |
| DeepSeek V4 Pro | 30 / 40 | 75.0% |

### 结果解读

mini-benchmark 0.4.0 的主集结果显示，该题库能够稳定衡量模型在半导体气敏材料研发中的专业判断能力。题目并非围绕单点事实记忆展开，而是要求模型在局部语境中识别关键变量，例如湿度耦合、吸附/反应路径、载流子类型、配气边界、表征因果链、响应/恢复窗口和安全 gate。

Robustness 层进一步检验模型在表达改写、合理干扰信息、条件更新、诱导式安全表达和工具观察变化下的判断一致性。该层设计体现了科研训练中的一项核心能力：同一个材料现象在不同表述、不同数据切片和不同实验阶段下，需要保持原则稳定，同时对关键新证据保持敏感。

### 项目展示价值

本评测结果可以直接用于 portfolio 和面试材料：主集展示题库的专业判别力，robustness 层展示评测设计的层次感，安全边界指标展示对高风险研发场景的规范意识。结果文件与报告相互对应，便于审阅者从 README 快速进入数据、方法和复盘材料。

## English

### Evaluation Configuration

| Item | Value |
|---|---|
| Version | mini-benchmark 0.4.0 |
| Main benchmark | `data/benchmark.json` |
| Main scored subset | 82 MCQ |
| Robustness benchmark | `data/benchmark_sgs100_robustness.json` |
| Robustness scored subset | 40 MCQ variants |
| Prompt | `eval/prompts/base_prompt.md` |
| Runner | `eval/run_eval.py` |
| Scorer | `eval/score_mcq.py` |

### Main Results

| Model | Correct / Total | Accuracy | Safety Boundary Index |
|---|---:|---:|---:|
| MiMo v2.5 Pro | 80 / 82 | 97.6% | 100.0% |
| GPT-5.5 | 80 / 82 | 97.6% | 100.0% |
| DeepSeek V4 Pro | 76 / 82 | 92.7% | 87.5% |

### Robustness Results

| Model | Correct / Total | Accuracy |
|---|---:|---:|
| MiMo v2.5 Pro | 36 / 40 | 90.0% |
| GPT-5.5 | 35 / 40 | 87.5% |
| DeepSeek V4 Pro | 30 / 40 | 75.0% |

### Interpretation

The main-set results show that mini-benchmark 0.4.0 provides a stable measure of professional judgment in semiconductor gas-sensing R&D. The items go beyond single-fact recall and ask models to identify decisive variables in local context, including humidity coupling, adsorption/reaction pathways, carrier type, gas-flow boundaries, characterization evidence chains, response/recovery windows, and safety gates.

The robustness layer further measures judgment consistency under paraphrase, realistic distractors, condition updates, persuasive safety phrasing, and tool-observation changes. This mirrors a core research skill: preserving stable principles across different descriptions and data slices while responding precisely to decisive new evidence.

### Portfolio Value

The evaluation results are suitable for portfolio and interview review. The main set demonstrates domain-level discrimination, the robustness layer demonstrates layered benchmark design, and the safety-boundary index demonstrates professional judgment in high-risk R&D contexts. The result files and bilingual reports form a coherent review path from README to data, methodology, and project reflection.
