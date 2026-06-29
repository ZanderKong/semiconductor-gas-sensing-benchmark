# Semiconductor Gas-Sensing Agent Benchmark

## Executive Summary

- 本项目是一个面向半导体气敏材料研发场景的中文 agent benchmark。
- 项目评估模型在文献理解、机理边界、实验设计、异常诊断、安全判断和工具使用中的可靠性。
- V3-alpha 将题目升级为可审计 task unit，并引入 Hard Gate、D0-D6 加权评分、Tool Use 评分和 trace-based audit。
- 本仓库提供本地 deterministic V3 demo、真实模型 MCQ runner、schema validation、benchmark lint、CI workflow 和自动报告生成器。
- 题目来自公开知识和抽象问题类型，不包含私有配方、样品编号、敏感采购信息或未公开实验结论。

## 中文

### 项目背景

材料研发中的模型评测需要覆盖完整工作流。研究人员通常需要判断文献结论是否能迁移到当前体系，实验方案是否包含关键对照，异常现象应如何排查，结果证据是否足够支持下一步决策，以及某个操作是否越过安全边界。

Semiconductor Gas-Sensing Agent Benchmark 将半导体气敏材料研发拆解为一组可测试、可评分、可审计的小任务。题目覆盖气体纸带、金属氧化物、导电聚合物、二维材料、分析表征、工艺放大、配气计算、数据曲线、安全资料和实验室边界判断。

### 版本说明

当前公开 benchmark 版本统一标记为 V3-alpha。V3-alpha 表示可审计 task unit、schema、评分协议和 trace 设计版本。

### 项目内容

| 模块 | 内容 |
|---|---|
| V1/V2 主题库 | 100 题中文 mini benchmark，用于覆盖 domain、研发阶段、工具类型和错误模式 |
| V3-alpha 题库 | 46 个可审计 task unit，包括 static core、robustness variants 和 live extension |
| 评分协议 | Hard Gate、D0-D6 加权维度、Tool Use 评分、Meta Eval 和人工复核协议 |
| Demo runner | 本地 deterministic evaluation，无需模型 API key，生成 manifest、trace、judge outputs 和报告 |
| Real-model MCQ runner | 调用 GPT 与 DeepSeek 模型，自动记录输出、manifest、leaderboard 和诊断报告 |
| Validation/CI | schema validation、benchmark lint、GitHub Actions workflow 和 one-command demo |
| Report generator | 自动生成诊断报告和 badcase gallery |

### 评估能力

| 能力 | 说明 |
|---|---|
| 文献分析 | 判断公开结论能否迁移到当前材料体系 |
| 机理解释 | 区分候选机理、确定机理和证据不足 |
| 实验设计 | 给出变量、对照、指标、重复和 go/no-go 标准 |
| 实验进行 | 检查 SOP、配气、仪器、记录质量和安全边界 |
| 结果分析 | 诊断漂移、恢复不足、湿度干扰、异常点和表征证据 |
| 下一步计划 | 在材料路线、工艺放大和产品化 gate 之间做取舍 |
| 安全边界 | 识别高危气体、有毒溶剂、强氧化剂、废物和隐私风险 |
| 工具使用 | 评价 calculator、literature retrieval、table analysis、data plotting、safety reference 和 protocol checklist 的使用质量 |

### V3 设计要点

| 设计 | 用途 |
|---|---|
| Hard Gate | 先识别安全、事实、证据、指令、工具和隐私硬失败 |
| D0-D6 Rubric | 按指令遵循、专业准确性、情境判断、证据边界、可执行性、工具使用和安全边界评分 |
| Tool Use Evaluation | 区分 no-tool baseline 和 tool-enabled agent，报告 `tool_lift` |
| Trace-Based Audit | 记录 visible input、tool call、tool result、model output 和 judge result |
| Robustness Variants | 通过改写、干扰、矛盾、多轮和安全诱导测试稳定性 |
| Live Extension | 保留可替换扩展题，用于观察新任务泛化和污染风险 |

### 快速开始

```bash
git clone https://github.com/ZanderKong/semiconductor-gas-sensing-benchmark.git
cd semiconductor-gas-sensing-benchmark
make demo
make validate
make lint
make report
make score-mcq
```

`make demo` 不需要任何模型 API key。它使用本地 mock model 跑通 V3 评测流程，并生成：

```text
results/runs/demo/
├── run_manifest.json
├── model_outputs.jsonl
├── judge_outputs.jsonl
├── trace.jsonl
├── aggregate_metrics.json
├── report.md
├── diagnostic_report.md
└── badcases/
```

真实模型 MCQ 评测需要可用模型凭据。`make eval-mcq` 默认使用 Codex CLI 的 `gpt-5.5` 和 DeepSeek OpenAI-compatible endpoint 的 `deepseek-v4-pro`。

```bash
export CODEX_CLI=/path/to/codex  # optional; defaults to the Codex desktop app bundle on macOS
export DEEPSEEK_API_KEY=...
make eval-mcq
make score-mcq
```

### 主要文件

| 文件 | 用途 |
|---|---|
| `data/benchmark_v1.json` | V1/V2 100 题主评测集 |
| `data/benchmark_v3_alpha.json` | V3-alpha 可审计 task unit 题库 |
| `data/schema/task_schema_v3.json` | V3 task schema |
| `docs/overview.md` | 项目概览 |
| `docs/methodology.md` | 题目设计、生成流程和质量控制 |
| `docs/task_design_v3.md` | V3-alpha 题库结构说明 |
| `docs/scoring_v3.md` | V3 评分协议 |
| `docs/hard_gates.md` | Hard Gate 判定规则 |
| `docs/judge_protocol.md` | judge 与人工复核协议 |
| `docs/agent_modes.md` | no-tool / tool-enabled 运行模式 |
| `docs/reproducibility_and_trace.md` | 运行记录、trace 与可复现要求 |
| `eval/runner.py` | 本地 deterministic V3 demo runner |
| `eval/run_eval.py` | GPT / DeepSeek MCQ runner |
| `eval/score_mcq.py` | MCQ scorer and result-page generator |
| `eval/reporting/generate_report.py` | 报告生成器 |
| `scripts/validate_tasks.py` | V3 task structure validation |
| `scripts/validate_v3_alpha_distribution.py` | V3-alpha release distribution validation |
| `scripts/lint_benchmark.py` | 文档、元数据和隐私边界 lint |
| `results/model_run_manifest.json` | 真实模型 MCQ 运行元数据 |
| `reports/model_diagnostic_report.md` | 真实模型 MCQ 结果诊断 |
| `reports/model_evaluation_recap.md` | 测试复盘与后续改进计划 |
| `.github/workflows/validate.yml` | GitHub Actions validation workflow |

### 仓库结构

```text
semiconductor-gas-sensing-benchmark/
├── data/        # benchmark JSON/CSV and schemas
├── docs/        # methodology, scoring protocol, gates, judge, trace, agent modes
├── eval/        # demo runner, prompts, reporting utilities, legacy scoring scripts
├── scripts/     # validation and lint scripts
├── results/     # leaderboard, breakdowns, demo runs, badcases
├── reports/     # design and diagnostic reports
├── assets/      # review HTML and overview images
└── README.md
```

### 当前结果状态

2026-06-29 的真实模型 MCQ run 已完成。`gpt-5.5` 通过 Codex CLI 完成 82 / 82，`deepseek-v4-pro` 通过 DeepSeek API 完成 82 / 82。

这个结果证明调用、解析、自动评分和报告生成链路已经跑通。这个结果不应被解读为稳定能力排名，因为当前 MCQ 子集对强模型区分度不足。

V3-alpha 的重点是可审计 task unit。当前版本已经完成题库结构、schema、评分协议、demo runner、validation、CI 和报告生成流程。后续真实模型横评应接入 V3 trace runner 和真实工具 harness。

### 适用边界

本项目用于评估模型在抽象材料研发场景中的判断质量。项目文件不构成危险气体实验 SOP，不提供高危气体开放制备步骤，不用于复原私有实验条件。

## English

### Summary

Semiconductor Gas-Sensing Agent Benchmark is a Chinese diagnostic benchmark for semiconductor gas-sensing materials R&D workflows. It evaluates whether a model can handle literature interpretation, mechanism boundaries, experiment design, abnormal-result diagnosis, next-step planning, safety judgment, and tool use.

### What It Evaluates

- Literature analysis and evidence transfer.
- Mechanism explanation with uncertainty boundaries.
- Experimental design with variables, controls, metrics, and go/no-go criteria.
- Operational judgment around SOP, gas mixing, instruments, and record quality.
- Result analysis for drift, recovery failure, humidity interference, and evidence mismatch.
- Safety-boundary recognition for hazardous gases, toxic solvents, oxidizers, waste, and privacy.
- Tool-use quality across calculator, retrieval, table analysis, plotting, safety reference, and checklist workflows.

### Quick Start

```bash
make demo
make validate
make lint
make report
make score-mcq
```

The demo is local and deterministic. It writes an auditable run under `results/runs/demo/`.

### Design

V3-alpha introduces auditable task units, Hard Gate checks, D0-D6 weighted scoring, tool-use evaluation, trace-based audit, robustness variants, and live extension tasks. The repository also includes a real-model MCQ runner for GPT and DeepSeek validation. The benchmark uses public knowledge and abstract problem types with private details removed.
