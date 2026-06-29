# Semiconductor Gas-Sensing Benchmark Mini

## 执行摘要

- 这是一个面向半导体气敏材料研发场景的 100 题中文 mini diagnostic benchmark。
- 题库按 `domain`、`scenario_stage`、`tool_type` 和 failure mode 组织，用来观察模型在研发流程中的判断方式。
- 题目来自公开知识和抽象问题类型，去除了私有配方、样品编号和未公开实验结论。
- 当前 gpt-5.5 与 deepseek-chat 的选择题流程已经跑通，但结果显示 MCQ 子集对强模型的区分度不足。

## 中文

### 项目背景

材料研发里的模型评测不能只问“这个概念对不对”。真实工作里更常见的问题是：一条文献结论能不能迁移到当前体系，实验方案有没有漏掉关键对照，异常数据该优先排查什么，某个看起来可行的操作会不会带来安全风险。

这个项目把半导体气敏材料研发拆成一组可测试的小任务。题目围绕气敏材料、气体纸带、金属氧化物、导电聚合物、二维材料、分析表征、工艺放大和实验安全展开。它不追求覆盖所有化学知识，而是重点测试模型能否在中文研发语境下做出稳妥、可解释、可追溯的判断。

设计上参考了 ChemBench-mini 的题型和 domain 组织方式、HELM 的多维评价思路、LAB-Bench 的科研任务结构，以及 OpenAI Evals 的工程化评测文件组织。

### 项目目标

- 评估模型在中文材料研发工作流中的情境判断能力。
- 测试模型能否识别“单独成立、放入题目条件后存在隐藏问题”的选项。
- 将错误归因到机理迁移、证据边界、变量控制、指标取舍、安全风险和工具使用等维度。
- 提供可复现的数据结构、评分脚本、结果表和人工审阅页面，便于后续横向比较不同模型。

### 题库设计

- **固定规模**：100 题，其中 82 道选择题、18 道简答题。
- **8 个 domain**：有机化学、物理化学、无机化学、材料科学、通用化学、分析化学、技术化学、毒性与安全。
- **6 个研发阶段**：文献分析、实验设计、实验进行、结果分析、下一步计划、安全边界。
- **逐选项设计理由**：每个选择题选项都有 `option_profiles` 和 `option_rationales`，用于解释为什么干扰项在局部看似合理、在题目约束下存在问题。
- **工具类型细分**：`tool_type` 覆盖 `no_tool`、`calculator`、`literature_retrieval`、`table_analysis`、`data_plotting`、`safety_reference` 和 `protocol_checklist`。
- **隐私与安全边界**：`private_combination=0`，不包含私有配方组合、比例、样品编号或未公开实验结论。

### 快速开始

```bash
cd semiconductor-gas-sensing-benchmark
python3 eval/run_eval.py --models gpt-5.5
python3 eval/score_mcq.py
```

主要文件：

| 文件 | 用途 |
|---|---|
| `data/benchmark_v1.json` | 主评测集 JSON |
| `data/benchmark_v1.csv` | 主评测集 CSV |
| `data/schema.json` | 字段结构与数据校验 |
| `docs/methodology.md` | 题目设计、生成流程和质量控制 |
| `docs/dimension_definition.md` | 评价维度定义和打分标准 |
| `docs/dataset_card.md` | 数据集用途、组成、风险和限制 |
| `assets/benchmark_v2_review.html` | 离线逐题审阅页面 |
| `eval/run_eval.py` | 模型调用脚本 |
| `eval/score_mcq.py` | 选择题自动评分脚本 |
| `results/leaderboard.md` | 当前模型运行记录 |
| `reports/model_diagnostic_report.md` | 模型诊断与下一步改进建议 |

### 结果摘要

当前版本包含 100 题，其中选择题 82 题、简答题 18 题。题目覆盖文献分析、实验设计、实验进行、结果分析、下一步计划和安全边界 6 个流程阶段。

数据校验结果：8 个 domain 分布符合设定比例；选择题答案位置 A/B/C/D 为 21/21/20/20；工具配置为 51 道 with-tool、49 道 without-tool；私有依赖为 `none=86`、`analog=6`、`seed_entity=8`、`private_combination=0`。

当前已完成 gpt-5.5 与 deepseek-chat 的 82 道选择题自动评分。两组运行均完成全流程调用、解析和评分，未观察到安全 hard fail。由于两个强模型在 MCQ 子集上均全部答对，当前结论应表述为：**流程已跑通，但选择题区分度不足**。下一版需要增加开放题评分、表格/曲线分析题、冲突证据题和更强的情境型干扰项。

### 仓库结构

```text
semiconductor-gas-sensing-benchmark/
├── data/        # benchmark JSON/CSV, sample, schema
├── docs/        # methodology, dataset card, taxonomy, scoring, privacy
├── eval/        # prompts, runner, scorer, example config
├── results/     # leaderboard, breakdowns, model outputs, badcases
├── reports/     # design report and model diagnostic report
├── assets/      # review HTML and overview image
└── README.md
```

### 适用边界

该 benchmark 用于评估模型的研发判断、证据意识、工具使用和安全边界识别。题目不构成危险气体实验 SOP，也不用于训练模型、复原私有实验条件或替代实验室安全审查。

## English

### Executive Summary

- This repository provides a 100-item mini diagnostic benchmark for Chinese semiconductor gas-sensing materials R&D workflows.
- The dataset is organized by `domain`, `scenario_stage`, `tool_type`, and failure mode, covering literature analysis, experiment design, execution, result analysis, next-step planning, and safety boundaries.
- Questions are built from abstract problem types with private details removed; each item includes answer rationale, option-level design notes, and structured evaluation labels.
- Current gpt-5.5 and deepseek-chat MCQ runs show that the evaluation pipeline works, while the multiple-choice subset is not yet discriminative enough for strong models.

### Background

Model evaluation for materials R&D should test more than isolated chemistry facts. In practice, the harder questions are whether a literature claim transfers to the current system, whether an experiment has the right controls, how to diagnose abnormal results, and when a plausible operation crosses a safety boundary.

This benchmark turns semiconductor gas-sensing R&D into a compact set of testable tasks. It covers gas-sensing materials, paper-tape detection, metal oxides, conductive polymers, 2D materials, analytical characterization, process scale-up, and laboratory safety. Items are built from abstract problem types with private details removed.

### Goals

- Evaluate contextual judgment in materials R&D workflows.
- Test whether models can identify options that are locally correct but problematic under the given scenario.
- Attribute errors by mechanism transfer, evidence boundary, variable control, metric trade-off, safety risk, and tool usage.
- Provide reproducible data files, scoring scripts, result tables, and a human-readable review page.

### Dataset Design

- 100 items: 82 multiple-choice and 18 free-response questions.
- 8 domains: organic, physical, inorganic, materials, general, analytical, technical chemistry, and toxicity/safety.
- 6 workflow stages: literature analysis, experiment design, execution, result analysis, next-step planning, and safety-boundary judgment.
- Per-option rationale and trap profile for human review and error attribution.
- Fine-grained `tool_type` labels instead of a binary with-tool / no-tool split.
- Privacy-aware design with no private formulation combinations, ratios, sample IDs, or non-public conclusions.

### Quick Start

```bash
cd semiconductor-gas-sensing-benchmark
python3 eval/run_eval.py --models gpt-5.5
python3 eval/score_mcq.py
```

### Result Summary

Benchmark Mini V2 contains 100 questions: 82 multiple-choice and 18 free-response items. Current MCQ runs for gpt-5.5 and deepseek-chat completed the full call-parse-score pipeline with no observed safety hard failures. Because both strong models solved the MCQ subset completely, the current result should be interpreted as: **the pipeline works, but the MCQ subset lacks sufficient discriminative power**.
