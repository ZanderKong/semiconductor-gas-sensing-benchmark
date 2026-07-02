# Reproducibility

## 构建

先构建 Domain Core Set，再构建 SGS152 Main Set：

```bash
make build-sgs100
make build-sgs152
```

`make build-sgs152` 会生成或刷新：

- `data/benchmark.json`
- `data/benchmark.csv`
- `data/scientific_stress_bank.json`
- `data/free_response_rubrics.json`
- `data/item_design_index.csv`
- `reports/item_design_index.md`
- `results/sgs152_merged/model_outputs_sgs152_merged_all.csv`
- `results/sgs152_merged/model_run_manifest_sgs152_merged_all.json`

## 校验

```bash
make validate
make validate-hard50
make lint
make lint-sgs100
```

这些检查覆盖：

- SGS152 题量；
- Domain Core Set 和 Scientific Stress Set 题量；
- MCQ 和 free-response 分布；
- options 字母和答案合法性；
- free-response rubric 覆盖；
- Hard Diagnostic Set 结构；
- 展示类文档中的禁用表达；
- prompt 对变长选项的支持。

## 评分

MCQ：

```bash
make score-mcq
```

Hard Diagnostic：

```bash
make score-hard50-all
```

Free-response：

```bash
make eval-free-response
make score-free-response
```

## 结果产物

| Artifact | 说明 |
|---|---|
| `results/sgs152_merged/scored/model_results_summary.csv` | SGS152 MCQ 模型汇总 |
| `results/sgs152_merged/scored/diagnostic_report.md` | MCQ 诊断报告 |
| `results/free_response/scored_free_response_summary.csv` | 开放题模型汇总 |
| `results/free_response/scored_free_response_by_dimension.csv` | 开放题逐维分数 |
| `results/hard50/scored_all/model_results_summary.csv` | Hard Diagnostic Set 汇总 |
| `results/robustness_model_summary.csv` | Robustness Set 汇总 |

## 运行边界

SGS152 MCQ 当前仓库保留的是可复现 score artifact；live raw transcript 未保留，manifest 中记录为 `not recorded`。Hard Diagnostic Set 保留 raw outputs。Free-response 当前为全量 rubric review artifact，下一版需要补 live transcript 和 judge adjudication。
