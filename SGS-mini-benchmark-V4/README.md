# Semiconductor Gas-Sensing Mini-Benchmark 0.4.0

## 项目概述

Semiconductor Gas-Sensing Mini-Benchmark 0.4.0 是一个面向半导体气敏材料研发场景的中文专业评测集。项目将材料化学、分析化学、传感器工程、安全合规和数据判断转化为可复核的 benchmark 结构，用于评估大语言模型在科研问题建模、实验设计、证据边界和安全决策中的专业判断能力。

The benchmark translates semiconductor gas-sensing R&D reasoning into a compact, auditable evaluation package. It measures how language models handle mechanistic evidence, experimental controls, data interpretation, safety boundaries, and research communication in a domain-specific setting.

## 核心成果

| 模块 | 交付内容 |
|---|---:|
| 主评测集 | 100 items |
| Multiple-choice | 82 items |
| Free-response | 18 items |
| Robustness variants | 40 items |
| Free-response rubrics | 18 rubrics |
| 覆盖领域 | 8 chemistry/materials domains |
| 自动化校验 | validation, lint, acceptance lint |
| 真实模型评测 | GPT-5.5, MiMo v2.5 Pro, DeepSeek V4 Pro |

## 技术亮点

- 构建了面向半导体气敏材料研发的 SGS-100 任务集，覆盖显色纸带、MOS 电阻式传感器、导电聚合物、金属氧化物、二维材料、表征解释、配气判断、工艺放大和安全评审。
- 将 ChemBench mini 的题型比例映射到专业场景，形成 82 道 MCQ 与 18 道 free-response 的紧凑评测结构。
- 为每道 MCQ 建立四选项、长度均衡、答案分布均衡、局部合理 distractor 和 option-level rationale。
- 为 18 道 free-response 设计 10 分制 rubric，覆盖 problem framing、evidence boundary、experimental design、decision logic、safety and privacy。
- 增加 40 道 robustness variants，用 paraphrase、distractor、contradiction、adversarial safety 和 tool-observation shift 检验模型判断的一致性与条件敏感性。
- 建立 validation 和 lint 脚本，将题量、比例、选项长度、答案分布、rubric 完整性、robustness parent linkage 和安全抽象规则纳入自动化验收。

## Results

### Main MCQ Evaluation

| Model | Correct / Total | Accuracy | Safety Boundary Index |
|---|---:|---:|---:|
| MiMo v2.5 Pro | 80 / 82 | 97.6% | 100.0% |
| GPT-5.5 | 80 / 82 | 97.6% | 100.0% |
| DeepSeek V4 Pro | 76 / 82 | 92.7% | 87.5% |

### Robustness Evaluation

| Model | Correct / Total | Accuracy |
|---|---:|---:|
| MiMo v2.5 Pro | 36 / 40 | 90.0% |
| GPT-5.5 | 35 / 40 | 87.5% |
| DeepSeek V4 Pro | 30 / 40 | 75.0% |

## Repository Map

| Path | Description |
|---|---|
| `data/benchmark.json` | SGS-100 main benchmark |
| `data/benchmark.csv` | Reviewer-friendly table export |
| `data/benchmark_sgs100_clean.json` | Clean main-set export with consistency fields |
| `data/benchmark_sgs100_robustness.json` | Robustness variant set |
| `data/free_response_rubrics.json` | Detailed rubrics for all free-response items |
| `docs/overview.md` | Bilingual project overview |
| `docs/dataset_card.md` | Bilingual dataset card |
| `docs/hr_review_guide.md` | HR and interview reading guide |
| `reports/` | Bilingual reports, audits, and project review |
| `results/` | Curated evaluation summaries |
| `scripts/validate_benchmark.py` | Main-set validation gate |
| `scripts/lint_sgs100_benchmark.py` | SGS-100 acceptance lint |
| `eval/run_eval.py` | Model evaluation runner |
| `eval/score_mcq.py` | MCQ scoring utility |

## Validation

```bash
make validate
make lint
make lint-sgs100
```

## Model Evaluation Commands

```bash
make eval-frontier
make eval-robustness-frontier
make eval-gpt55
make eval-robustness-gpt55
```

## Professional Value

本项目体现了跨学科问题抽象、材料研发场景建模、实验设计意识、数据质量控制、安全边界判断、rubric 工程、自动化校验和技术写作能力。它把生化环材领域的学术训练转化为工程化评测资产，适合用于简历项目、GitHub portfolio、技术面试材料和模型评测方法展示。

The package demonstrates domain-grounded benchmark design, scientific abstraction, evaluation engineering, safety-aware data construction, reproducible validation, and professional technical communication.
