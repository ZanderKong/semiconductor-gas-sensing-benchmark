# Overview

Semiconductor Gas-Sensing Mini-Benchmark 0.5.0 的 active main set 是 **SGS152**。

SGS152 包含 100 道 legacy SGS 领域题和 52 道 failure-mined design items。legacy 部分评估半导体气敏材料研发中的机理、表征、实验设计、数据质量和安全边界；failure-mined 部分保留强模型真实失败过的专家规则、定量计算、谱图模式、安全识别和多步推理机制。

0.5.0 的核心变化不是简单增加题量，而是把“领域真实感”和“强模型区分度”合在同一套主集中。早期换皮实验显示，过度领域化会降低题目原有压力；因此 SGS152 对新增题保留题面机制，并用设计心得解释为什么它能诱导模型出错。

## Main Assets

| Asset | Purpose |
|---|---|
| `data/benchmark.json` | Active SGS152 benchmark |
| `data/failure_mined_bank.json` | 52-item failure-mined design bank |
| `data/benchmark_sgs100_clean.json` | Legacy SGS100 export |
| `data/benchmark_sgs100_robustness.json` | Robustness variants |
| `data/benchmark_sgs_hard50.json` | Hard diagnostic set |
| `reports/model_evaluation_recap.md` | Model results and interpretation |
| `reports/question_design_notes.md` | Item design principles |
| `reports/optimization_retrospective.md` | Iteration lessons |

## Result Snapshot

| Model | SGS152 MCQ | Failure-mined MCQ |
|---|---:|---:|
| DeepSeek V4 Pro | 98 / 122 | 21 / 40 |
| GPT-5.5 | 95 / 122 | 15 / 40 |
| MiMo v2.5 Pro | 93 / 122 | 16 / 40 |
