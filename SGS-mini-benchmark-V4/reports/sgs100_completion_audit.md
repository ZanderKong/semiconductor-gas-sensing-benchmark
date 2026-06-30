# SGS-100 Delivery Audit

## 中文

### 交付清单

| Area | Evidence | Status |
|---|---|---|
| Main benchmark | `data/benchmark.json` | Complete |
| Reviewer table | `data/benchmark.csv` | Complete |
| Clean export | `data/benchmark_sgs100_clean.json` | Complete |
| Robustness layer | `data/benchmark_sgs100_robustness.json` | Complete |
| Free-response rubrics | `data/free_response_rubrics.json` | Complete |
| Validation scripts | `scripts/validate_benchmark.py`, `scripts/lint_sgs100_benchmark.py` | Complete |
| Model evaluation summary | `results/` | Complete |
| Bilingual reports | `reports/` | Complete |
| HR review guide | `docs/hr_review_guide.md` | Complete |

### 自动化验收

| Check | Scope |
|---|---|
| `make validate` | 主集题量、题型比例、领域分布、选项约束和答案分布 |
| `make lint` | 文档结构、核心文件和公开写作安全规则 |
| `make lint-sgs100` | Rubric、robustness linkage、consistency fields 和安全抽象 |

### 项目状态

mini-benchmark 0.4.0 已形成完整的本地评测包。它包含数据、schema、rubric、robustness variants、评测脚本、结果摘要、双语报告和 HR/面试阅读路径。

## English

### Delivery Checklist

| Area | Evidence | Status |
|---|---|---|
| Main benchmark | `data/benchmark.json` | Complete |
| Reviewer table | `data/benchmark.csv` | Complete |
| Clean export | `data/benchmark_sgs100_clean.json` | Complete |
| Robustness layer | `data/benchmark_sgs100_robustness.json` | Complete |
| Free-response rubrics | `data/free_response_rubrics.json` | Complete |
| Validation scripts | `scripts/validate_benchmark.py`, `scripts/lint_sgs100_benchmark.py` | Complete |
| Model evaluation summary | `results/` | Complete |
| Bilingual reports | `reports/` | Complete |
| HR review guide | `docs/hr_review_guide.md` | Complete |

### Automated Acceptance

| Check | Scope |
|---|---|
| `make validate` | Main-set size, type ratio, domain distribution, option constraints, and answer distribution |
| `make lint` | Documentation structure, core files, and public-writing safety rules |
| `make lint-sgs100` | Rubrics, robustness linkage, consistency fields, and safety abstraction |

### Project Status

mini-benchmark 0.4.0 is a complete local evaluation package. It includes data, schema, rubrics, robustness variants, evaluation scripts, curated result summaries, bilingual reports, and an HR/interview reading path.
