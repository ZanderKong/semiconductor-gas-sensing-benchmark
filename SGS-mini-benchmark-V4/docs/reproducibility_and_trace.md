# Reproducibility And Trace

## 中文

0.4.0 版本用文件级结构和自动化脚本支持可复核评测。

| Artifact | Role |
|---|---|
| `data/benchmark.json` | 主评测集 |
| `data/benchmark_sgs100_robustness.json` | Robustness 层 |
| `data/free_response_rubrics.json` | Free-response rubric |
| `scripts/validate_benchmark.py` | 主集结构校验 |
| `scripts/lint_sgs100_benchmark.py` | 0.4.0 acceptance lint |
| `eval/run_eval.py` | 模型调用与结果记录 |
| `eval/score_mcq.py` | MCQ 评分与汇总 |
| `results/evaluation_summary.json` | 结果汇总 |

推荐验收命令：

```bash
make validate
make lint
make lint-sgs100
```

## English

Version 0.4.0 supports auditable evaluation through file-level structure and automated scripts.

| Artifact | Role |
|---|---|
| `data/benchmark.json` | Main benchmark |
| `data/benchmark_sgs100_robustness.json` | Robustness layer |
| `data/free_response_rubrics.json` | Free-response rubric |
| `scripts/validate_benchmark.py` | Main-set validation |
| `scripts/lint_sgs100_benchmark.py` | 0.4.0 acceptance lint |
| `eval/run_eval.py` | Model execution and result recording |
| `eval/score_mcq.py` | MCQ scoring and aggregation |
| `results/evaluation_summary.json` | Curated result summary |

Recommended acceptance commands:

```bash
make validate
make lint
make lint-sgs100
```
