# Semiconductor Gas-Sensing Benchmark Mini

## Executive Summary

- 一个面向半导体气敏材料研发的 100 题 mini diagnostic benchmark，覆盖有机、物化、无机、材料、通用、分析、技术化学和安全 8 个 domain。
- 题目不复刻个人实验笔记，而是用真实气体纸带项目作为场景锚点，扩展到公开、通用、可迁移的气敏材料研发任务。
- 每题包含答案、标准理由、逐选项设计思路、研发流程阶段、真实 workflow task、期望模型输出和细分 tool type。
- 已完成 gpt-5.5 与 deepseek-chat 的 82 道选择题实测；Kimi/GLM 接口尝试失败并已在报告中记录。
- The benchmark is designed for human review, model evaluation, error attribution, and portfolio demonstration for data/product roles in scientific AI.

## 中文

### 项目背景

本项目是一个面向半导体气敏材料研发场景的小型诊断型评测集。它参考 ChemBench-mini 的 domain 抽样方式和工程化字段结构，但题目内容完全重写为气敏材料、气体纸带、分析表征、工艺放大和实验安全相关任务。

V2 不是“个人笔记挖空题”。真实气体纸带项目只提供场景锚点和实体种子，题库主体来自半导体气敏材料研发中常见的公开知识、仪器方法和可迁移实验逻辑。

### 目标

- 评估模型是否具备材料研发场景中的专业判断，而不仅是化学常识问答。
- 测试模型能否识别“单看正确但情境错误”的选项。
- 区分机理解释、实验设计、实验执行、数据分析、下一步计划和安全边界能力。
- 支持后续接入 DeepSeek、Kimi、GLM、OpenAI/Codex 等模型进行横向评测。

### 核心亮点

- **100 题固定规模**：按 ChemBench-mini 的 8 个 domain 等比例缩放。
- **逐选项设计理由**：每个选项都有 `option_profiles` 和 `option_rationales`。
- **真实研发流程标签**：新增 `scenario_stage`、`workflow_task`、`expected_output`。
- **细分工具类型**：新增 `tool_type`，包括 `calculator`、`literature_retrieval`、`table_analysis`、`data_plotting`、`safety_reference`、`protocol_checklist` 和 `no_tool`。
- **隐私控制**：`private_combination=0`，不包含真实配方组合、比例或样品结论。

### 快速开始

```bash
cd benchmark_v2_semiconductor_gas_sensing
python3 scripts/build_benchmark_v2.py
python3 scripts/build_review_html.py
```

如果使用最终 GitHub 作品集目录：

```bash
cd semiconductor-gas-sensing-benchmark
python3 eval/run_eval.py --models gpt-5.5
python3 eval/score_mcq.py
```

主要文件：

| 文件 | 用途 |
|---|---|
| `benchmark_v1.json` | 兼容命名的主评测集 JSON |
| `benchmark_v1.csv` | 兼容命名的主评测集 CSV |
| `data/benchmark_v2.json` | V2 原始 JSON |
| `data/benchmark_v2.csv` | V2 原始 CSV |
| `README.md` | 项目介绍 |
| `methodology.md` | 题目设计、生成流程和质量控制 |
| `dimension_definition.md` | 评价维度定义和打分标准 |
| `benchmark_v2_review.html` | 便于人类逐题审阅的离线页面 |
| `docs/dataset_card.md` | 数据集内容、用途、风险和限制 |
| `eval/run_eval.py` | 模型调用脚本 |
| `eval/score_mcq.py` | 选择题自动评分脚本 |
| `reports/benchmark_design_report.md` | benchmark 设计报告 |
| `reports/model_diagnostic_report.md` | 模型实测诊断报告 |
| `reports/prompt_optimization_report.md` | prompt 优化分析报告 |

---

## English

### What is this?

This repository contains a mini diagnostic benchmark for evaluating large language models in semiconductor gas-sensing material R&D scenarios.

It is inspired by the sampling philosophy of ChemBench-mini, but all questions are rewritten around gas-sensing materials, paper-tape detection, analytical characterisation, process scale-up, and laboratory safety.

The benchmark is not a memorisation test of private lab notes. Real R&D work only serves as a scenario anchor. The actual tasks are based on public, generalisable, and transferable scientific reasoning.

### What does it evaluate?

The benchmark evaluates whether a model can:

- reason within applied materials R&D scenarios;
- avoid superficially correct but contextually wrong answers;
- distinguish mechanism explanation, experimental design, execution planning, data analysis, next-step planning, and safety judgement;
- provide outputs useful for scientific workflow support rather than generic chemistry QA.

### Dataset structure

Each item includes:

- domain;
- question type;
- options and answer;
- standard explanation;
- option-level design rationale;
- scenario stage;
- workflow task;
- expected output type;
- tool type;
- privacy flag.

### Current evaluation status

Smoke tests and partial model evaluations have been completed for:

- gpt-5.5;
- deepseek-chat.

Attempts to run Kimi and GLM are recorded in the diagnostic report. Their API execution was not completed due to request or authentication issues.

### Intended use

This project can be used for:

- portfolio demonstration;
- scientific AI product evaluation;
- prompt and workflow design;
- error attribution;
- human review of model behaviour in applied R&D tasks.

### Privacy note

This public version removes or abstracts private experimental formulations, confidential ratios, specific sample conclusions, and sensitive internal process details.
