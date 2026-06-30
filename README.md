# Semiconductor Gas-Sensing Mini-Benchmark

## 中文

本仓库发布 `mini-benchmark 0.4.0`：一个面向半导体气敏材料研发场景的中文专业评测项目。项目将材料化学、传感机理、实验设计、数据质量、安全边界和技术写作能力转化为可复核的 benchmark 资产。

主项目位于：

```text
SGS-mini-benchmark-V4/
```

### 核心成果

| Module | Deliverable |
|---|---:|
| 主评测集 | 100 items |
| Multiple-choice | 82 items |
| Free-response | 18 items |
| Robustness variants | 40 items |
| Free-response rubrics | 18 rubrics |
| 自动化验收 | validate, lint, acceptance lint |
| 模型评测摘要 | GPT-5.5, MiMo v2.5 Pro, DeepSeek V4 Pro |

### 项目价值

- 将半导体气敏材料研发中的真实判断任务抽象为结构化评测集。
- 覆盖有机化学、物理化学、无机化学、材料科学、分析化学、工艺放大和安全合规等维度。
- 通过 MCQ、free-response rubric 和 robustness variants 同时衡量专业准确性、证据边界、实验设计和安全判断。
- 提供 GitHub/简历/面试可直接阅读的双语报告体系。

### 快速开始

```bash
cd SGS-mini-benchmark-V4
make validate
make lint
make lint-sgs100
```

### 推荐阅读

| File | Focus |
|---|---|
| `SGS-mini-benchmark-V4/README.md` | 项目概览和结果摘要 |
| `SGS-mini-benchmark-V4/docs/hr_review_guide.md` | HR 与面试阅读路径 |
| `SGS-mini-benchmark-V4/reports/project_review_report.md` | 项目复盘和能力展示 |
| `SGS-mini-benchmark-V4/reports/model_evaluation_recap.md` | 模型评测结果 |

## English

This repository publishes `mini-benchmark 0.4.0`, a Chinese benchmark for semiconductor gas-sensing materials R&D. The project converts materials chemistry, sensing mechanisms, experimental design, data quality, safety boundaries, and technical communication into an auditable benchmark package.

The active project lives in:

```text
SGS-mini-benchmark-V4/
```

### Highlights

| Module | Deliverable |
|---|---:|
| Main benchmark | 100 items |
| Multiple-choice | 82 items |
| Free-response | 18 items |
| Robustness variants | 40 items |
| Free-response rubrics | 18 rubrics |
| Automated acceptance | validate, lint, acceptance lint |
| Model summaries | GPT-5.5, MiMo v2.5 Pro, DeepSeek V4 Pro |

### Value

- Converts real R&D judgment tasks in semiconductor gas-sensing materials into a structured benchmark.
- Covers organic chemistry, physical chemistry, inorganic chemistry, materials science, analytical chemistry, process scale-up, and safety compliance.
- Measures professional accuracy, evidence boundaries, experimental design, and safety judgment through MCQ, free-response rubrics, and robustness variants.
- Provides bilingual reports designed for GitHub portfolios, resumes, and technical interviews.
