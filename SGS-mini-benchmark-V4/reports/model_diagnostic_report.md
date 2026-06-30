# Model Diagnostic Report

## 中文

### 评测范围

本报告汇总 mini-benchmark 0.4.0 的主集 MCQ 与 robustness 层评测结果。主集用于衡量模型在半导体气敏材料研发判断中的准确性，robustness 层用于衡量模型在相邻场景中的原则一致性和条件敏感性。

### Main MCQ

| Model | Correct / Total | Accuracy | Safety Boundary Index |
|---|---:|---:|---:|
| MiMo v2.5 Pro | 80 / 82 | 97.6% | 100.0% |
| GPT-5.5 | 80 / 82 | 97.6% | 100.0% |
| DeepSeek V4 Pro | 76 / 82 | 92.7% | 87.5% |

### Robustness

| Model | Correct / Total | Accuracy |
|---|---:|---:|
| MiMo v2.5 Pro | 36 / 40 | 90.0% |
| GPT-5.5 | 35 / 40 | 87.5% |
| DeepSeek V4 Pro | 30 / 40 | 75.0% |

### 结果解读

三组模型在主集上均表现出较强的领域理解能力。MiMo v2.5 Pro 与 GPT-5.5 在主集上达到 97.6% accuracy，体现了对材料路线取舍、数据判断和安全边界题目的稳定处理能力。Robustness 层进一步区分了模型在 paraphrase、distractor、contradiction、safety 和 tool-observation shift 场景中的判断风格。

## English

### Scope

This report summarizes the main MCQ and robustness evaluation results for mini-benchmark 0.4.0. The main set measures domain judgment in semiconductor gas-sensing R&D, while the robustness layer measures principle consistency and condition sensitivity across neighboring scenarios.

### Main MCQ

| Model | Correct / Total | Accuracy | Safety Boundary Index |
|---|---:|---:|---:|
| MiMo v2.5 Pro | 80 / 82 | 97.6% | 100.0% |
| GPT-5.5 | 80 / 82 | 97.6% | 100.0% |
| DeepSeek V4 Pro | 76 / 82 | 92.7% | 87.5% |

### Robustness

| Model | Correct / Total | Accuracy |
|---|---:|---:|
| MiMo v2.5 Pro | 36 / 40 | 90.0% |
| GPT-5.5 | 35 / 40 | 87.5% |
| DeepSeek V4 Pro | 30 / 40 | 75.0% |

### Interpretation

All evaluated models show strong domain comprehension on the main set. MiMo v2.5 Pro and GPT-5.5 reach 97.6% accuracy, demonstrating stable handling of materials route selection, data judgment, and safety-boundary items. The robustness layer further separates model behavior under paraphrase, distractor, contradiction, safety, and tool-observation-shift scenarios.
