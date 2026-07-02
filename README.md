# Semiconductor Gas-Sensing Mini-Benchmark

本仓库按版本归档半导体气敏材料 benchmark 项目。当前工作版本是 `versions/0.5.0/`，active main benchmark 为 **SGS152**。

## Version Map

| Version | Path | Status | Notes |
|---|---|---|---|
| 0.1.0 | `versions/0.1.0/` | archived | 早期 benchmark_v1 数据草案 |
| 0.2.0 | `versions/0.2.0/` | archived | 早期 SGS-V2 模型输出与 smoke results |
| 0.3.0 | `versions/0.3.0/` | archived | V3-alpha schema、能力单元和 tool-use 设计 |
| 0.4.0 | `versions/0.4.0/` | archived release | 100 题 mini-benchmark 版本 |
| 0.5.0 | `versions/0.5.0/` | active | SGS152、robustness、Hard-50、题目设计复盘 |

## Active 0.5.0

SGS152 由 legacy SGS100 专业气敏题库和 52 道 failure-mined design items 合并而成。新增题保留模型真实失败机制，并在元数据中记录设计心得、干扰项意图和评分逻辑。

| Component | Count |
|---|---:|
| Active benchmark | 152 |
| Multiple-choice | 122 |
| Free-response | 30 |
| Legacy SGS100 export | 100 |
| Failure-mined design bank | 52 |
| Robustness variants | 40 |
| Hard diagnostic set | 50 |

### Main MCQ Results

| Model | Correct / Total | Accuracy | Failure-mined MCQ |
|---|---:|---:|---:|
| DeepSeek V4 Pro | 98 / 122 | 80.3% | 21 / 40 |
| GPT-5.5 | 95 / 122 | 77.9% | 15 / 40 |
| MiMo v2.5 Pro | 93 / 122 | 76.2% | 16 / 40 |

### Reproduce

```bash
cd versions/0.5.0
make validate
make lint-sgs100
make lint
make score-mcq
```

The root `Makefile` forwards common validation targets to `versions/0.5.0/`.
