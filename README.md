# Semiconductor Gas-Sensing Mini-Benchmark

Semiconductor Gas-Sensing Mini-Benchmark 是一个面向半导体气敏材料研发任务的领域 benchmark，用于评估大模型在机理推理、实验设计、证据边界、数据解释、安全约束和科学表达中的专业判断能力。

当前 active version 是 `versions/0.5.0/`，主评测集为 **SGS152 Main Set**。

## Version Map

| Version | Path | Status | Notes |
|---|---|---|---|
| 0.1.0 | `versions/0.1.0/` | archived | Early benchmark_v1 data drafts |
| 0.2.0 | `versions/0.2.0/` | archived | Early SGS-V2 outputs |
| 0.3.0 | `versions/0.3.0/` | archived | V3-alpha schema and task design |
| 0.4.0 | `versions/0.4.0/` | archived release | 100-item mini-benchmark |
| 0.5.0 | `versions/0.5.0/` | active | SGS152 Main Set, Scientific Stress Set, Robustness Set, and Hard Diagnostic Set |

## Result Snapshot

| Model | SGS152 MCQ | Scientific Stress MCQ |
|---|---:|---:|
| MiMo v2.5 Pro | 100 / 122 | 24 / 40 |
| DeepSeek V4 Pro | 99 / 122 | 21 / 40 |
| GPT-5.5 | 99 / 122 | 19 / 40 |

## Reproduce

```bash
cd versions/0.5.0
make build-sgs152
make validate
make lint
make score-mcq
```

Root-level `make validate`, `make lint`, and `make score-mcq` forward to `versions/0.5.0/`.
