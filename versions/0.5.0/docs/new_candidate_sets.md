# New Candidate Sets

0.5.0 保留多组候选题库，用于后续筛题和扩展。

| File | Purpose |
|---|---|
| `data/benchmark_realistic_seed2.json` | 两道人工真实实验现象种子题 |
| `data/benchmark_sgs_failure_mined_v1.json` | failure-mechanism transfer v1 |
| `data/benchmark_sgs_failure_mined_v2.json` | failure-mechanism transfer v2 |
| `data/benchmark_sgs_hard50.json` | 50 道 hard diagnostic MCQ |
| `data/benchmark_sgs200_design_table.csv` | SGS200 扩展槽位设计表 |
| `data/failure_mined_bank.json` | 0.5.0 active SGS152 新增设计库 |

## Screening Rule

候选题进入 active set 前，应至少满足一个条件：能让强模型出现稳定差异、能暴露清晰错误机制、或能代表真实实验现象中的关键判断。
