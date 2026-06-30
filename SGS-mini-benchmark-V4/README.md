# Semiconductor Gas-Sensing Benchmark V4

## Executive Summary

- 本项目是一个面向半导体气敏材料研发场景的中文 benchmark。
- 当前活跃版本为 **V4 / SGS-100**，题库收拢为 100 个评测题目。
- SGS-100 按 ChemBench mini 题型比例组织：82 道 multiple-choice，18 道 free-response。
- 题目覆盖文献理解、机理边界、实验设计、异常诊断、安全判断、数据分析、工艺放大和工具使用。
- MCQ 选项按强模型压力测试规则重写：选项长度接近、错误项局部合理、答案分布均衡，并加入一致性检查组。
- V4 增加独立 robustness 诊断层，用于测试 paraphrase、distractor、contradiction、安全诱导和工具观察变化。
- 18 道 free-response 均包含研发背景、10 分制 rubric、key points、hard fails 和 common failure modes。

## Dataset

| 文件 | 内容 |
|---|---:|
| `data/benchmark.json` | SGS-100 活跃题库 |
| `data/benchmark.csv` | SGS-100 表格审阅版 |
| `data/benchmark_sgs100_clean.csv` | SGS-100 clean 主集导出版 |
| `data/free_response_rubrics.json` | 18 道主观题详细 rubric |
| `data/benchmark_sgs100_robustness.csv` | 40 道 robustness variants |
| `scripts/validate_benchmark.py` | 题量、比例、选项硬约束和一致性字段校验 |
| `scripts/lint_sgs100_benchmark.py` | 主集、主观题、robustness 和报告验收校验 |
| `eval/run_eval.py` | 真实模型 MCQ runner |
| `eval/score_mcq.py` | MCQ scorer and report generator |

## HR Review Path

建议先阅读 `docs/hr_review_guide.md`。该文件给出非技术评审的阅读顺序、核心证据文件、最新模型结果、Kimi 未计分原因和本地验证命令。

核心状态如下：

| 项目 | 状态 |
|---|---|
| V4 独立文件夹 | Complete |
| SGS-100 主集 | 100 items |
| MCQ / Free-response | 82 / 18 |
| Robustness variants | 40 |
| Free-response rubrics | 18 |
| DeepSeek / MiMo / GPT-5.5 results | Complete |
| Kimi results | Blocked by external API connection |

## Composition

| 类型 | 数量 |
|---|---:|
| Multiple-choice | 82 |
| Free-response | 18 |
| Total | 100 |

领域分布按 ChemBench mini 子集比例映射到半导体气敏材料场景：

| Domain | Count |
|---|---:|
| organic_chemistry | 19 |
| physical_chemistry | 14 |
| inorganic_chemistry | 14 |
| materials_science | 14 |
| general_chemistry | 11 |
| analytical_chemistry | 10 |
| technical_chemistry | 10 |
| toxicity_and_safety | 8 |

## MCQ Design Rules

每道 MCQ 有 4 个选项，并满足以下硬约束：

- 最长选项汉字数 / 最短选项汉字数 <= 1.5。
- 最短选项不少于 10 个汉字。
- 正确项不作为最长选项。
- A/B/C/D 正确答案分布接近均衡：21 / 21 / 20 / 20。
- 错误项必须是局部合理但当前不优先的动作，例如方法阶段错误、证据外推过度、指标不是当前主指标、工艺会引入新混杂变量。
- 选项避免答案泄露词和模板词。

## Consistency Checks

SGS-100 主集中的每道题都包含 `variant_type`、`parent_task_id`、`expected_consistency`、`consistency_group_id` 和 `consistency_check` 字段。主集题目的 `variant_type` 均为 `base`。

Robustness variants 不混入主集 accuracy。该诊断层用于观察模型是否能在相邻场景中保持、修正或拒绝相应判断原则：

| Group | Focus |
|---|---|
| `paraphrase` | 表达改写后应保持原判断 |
| `distractor` | 加入真实但非决定性信息后应抵抗干扰 |
| `contradiction` | 新增关键条件后应改变答案或主要理由 |
| `adversarial_safety` | 安全诱导下仍应拒绝危险执行细节 |
| `tool_observation_shift` | 工具观察改变证据时应修正结论 |

## Quick Start

```bash
make validate
make lint
make build-sgs100
make lint-sgs100
make demo
make report
make eval-mcq
make score-mcq
```

真实模型 MCQ 评测需要可用模型凭据。`make eval-mcq` 默认使用 Codex CLI 的 `gpt-5.5` 和 DeepSeek OpenAI-compatible endpoint 的 `deepseek-v4-pro`。

```bash
export CODEX_CLI=/path/to/codex
export DEEPSEEK_API_KEY=...
make eval-mcq
make score-mcq
```

## Boundary

本项目用于评估模型在抽象材料研发场景中的判断质量。项目文件不构成危险气体实验 SOP，不提供高危气体开放制备步骤，不用于复原私有实验条件。V3 项目保留在仓库根目录，V4 作为独立子项目维护。
