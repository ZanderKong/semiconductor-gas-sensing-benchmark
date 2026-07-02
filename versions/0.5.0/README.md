# Semiconductor Gas-Sensing Mini-Benchmark 0.5.0

## 项目概述

0.5.0 以 **SGS152** 作为 active main benchmark。它由 legacy SGS100 半导体气敏研发题库和 52 道 failure-mined design items 合并而成，用于评估模型在材料研发判断、通用化学规则、专家科学推理和定量科学题中的稳定性。

新增题不再做气敏“换皮”，而是保留真实失败机制，并在题目元数据中记录设计心得、干扰项意图和评分要点。这样可以避免过度改写削弱原题的压力结构。

## 核心交付

| 模块 | 交付内容 |
|---|---:|
| Active main benchmark | 152 items |
| Multiple-choice | 122 items |
| Free-response | 30 items |
| Legacy SGS100 clean export | 100 items |
| Failure-mined design bank | 52 items |
| Robustness variants | 40 items |
| Hard diagnostic set | 50 MCQ items |
| Free-response rubrics | 30 rubrics |
| 覆盖领域 | 10 chemistry/materials/science domains |
| 真实模型评测 | DeepSeek V4 Pro, GPT-5.5, MiMo v2.5 Pro |

## 设计亮点

- Active MCQ 从 82 道扩展到 122 道，free-response 从 18 道扩展到 30 道。
- 新增 52 题统一编号为 `SGS-FM-001` 到 `SGS-FM-052`，只记录题目机制、设计心得和评分规则。
- 保留 `data/benchmark_sgs100_clean.json` 作为 legacy SGS100 对照集。
- 保留 40 道 robustness variants 和 SGS-Hard-50 诊断集，用于稳定性与边界判断分析。
- Validation/lint 已支持 SGS152、failure-mined items、二选一题、E 选项和新增开放题 rubric。

## Recommended Reading

| File | Focus |
|---|---|
| `reports/project_strategy_report.md` | 0.5.0 项目定位与题库结构 |
| `reports/model_evaluation_recap.md` | 三模型 SGS152 评测复盘 |
| `reports/question_design_notes.md` | 题目设计原则、干扰项和失败机制 |
| `reports/optimization_retrospective.md` | 换皮失败与后续优化心得 |
| `docs/dataset_card.md` | 数据集组成与使用边界 |
| `docs/reviewer_guide.md` | 审阅路径 |

## Results

### Active SGS152 MCQ

| Model | Correct / Total | Accuracy | Safety Fail Rate |
|---|---:|---:|---:|
| DeepSeek V4 Pro | 98 / 122 | 80.3% | 0.0% |
| GPT-5.5 | 95 / 122 | 77.9% | 0.0% |
| MiMo v2.5 Pro | 93 / 122 | 76.2% | 6.2% |

Breakdown:

| Model | Legacy SGS MCQ | Failure-mined MCQ |
|---|---:|---:|
| DeepSeek V4 Pro | 77 / 82 (93.9%) | 21 / 40 (52.5%) |
| GPT-5.5 | 80 / 82 (97.6%) | 15 / 40 (37.5%) |
| MiMo v2.5 Pro | 77 / 82 (93.9%) | 16 / 40 (40.0%) |

### Robustness

| Model | Correct / Total | Accuracy |
|---|---:|---:|
| MiMo v2.5 Pro | 36 / 40 | 90.0% |
| GPT-5.5 | 35 / 40 | 87.5% |
| DeepSeek V4 Pro | 30 / 40 | 75.0% |

### SGS-Hard-50

| Model | Correct / Total | Accuracy | Main failure modes |
|---|---:|---:|---|
| DeepSeek V4 Pro | 48 / 50 | 96.0% | condition update, safety gate |
| GPT-5.5 | 48 / 50 | 96.0% | condition update, safety gate |
| MiMo v2.5 Pro | 47 / 50 | 94.0% | safety gate, condition update |

## Repository Map

| Path | Description |
|---|---|
| `data/benchmark.json` | Active SGS152 main benchmark |
| `data/benchmark.csv` | Reviewer-friendly SGS152 table export |
| `data/benchmark_sgs152_merged.json` | SGS152 alias/export |
| `data/failure_mined_bank.json` | 52-item failure-mined design bank |
| `data/benchmark_sgs100_clean.json` | Legacy SGS100 clean export |
| `data/benchmark_sgs100_robustness.json` | Robustness variant set |
| `data/benchmark_sgs_hard50.json` | Hard diagnostic MCQ set |
| `data/free_response_rubrics.json` | Detailed rubrics for all 30 free-response items |
| `results/sgs152_merged/scored/` | Scored SGS152 summaries and diagnostic report |
| `scripts/build_sgs152_merged.py` | Rebuild active SGS152 from legacy SGS100 + failure-mined design bank |
| `scripts/validate_benchmark.py` | Active SGS152 validation gate |
| `scripts/lint_sgs100_benchmark.py` | 0.5.0 acceptance lint |
| `eval/run_eval.py` | Model evaluation runner |
| `eval/score_mcq.py` | MCQ scoring utility |

## Validation

```bash
make validate
make validate-hard50
make lint
make lint-sgs100
make score-mcq
```

## Review Value

SGS152 的价值在于把领域化气敏研发判断和 failure-mined 高压题机制放在同一套评测中。旧 SGS100 展示专业场景建模能力，新增设计库提供更强的头部模型区分度，两者共同支持更清晰的错误归因。
