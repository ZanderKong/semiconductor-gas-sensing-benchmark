# Dataset Card

## Dataset Summary

| Field | Value |
|---|---|
| Name | Semiconductor Gas-Sensing Mini-Benchmark |
| Active version | 0.5.0 RC |
| Active set | SGS152 Main Set |
| Language | 中文主导，保留必要英文术语 |
| Domain | Semiconductor gas-sensing materials R&D |
| Main task types | MCQ, free-response |
| Main leaderboard | SGS152 MCQ from `data/benchmark.json` |
| RC evidence | `results/standard_20260703` |

SGS152 Main Set 将半导体气敏材料研发中的专业判断转化为可评分、可复核、可归因样本。数据集关注文献分析、机理判断、实验设计、表征解释、数据质量、安全边界和路线取舍。

## Data Layers

| Layer | File | Items | MCQ | Free-response | Release role |
|---|---|---:|---:|---:|---|
| SGS152 Main Set | `data/benchmark.json` | 152 | 122 | 30 | Main benchmark |
| Domain Core Set | `data/benchmark_sgs100_clean.json` | 100 | 82 | 18 | SGS152 component |
| Scientific Stress Set | `data/scientific_stress_bank.json` | 52 | 40 | 12 | SGS152 component |
| Robustness Set | `data/benchmark_sgs100_robustness.json` | 40 | 40 | 0 | Optional diagnostic |
| Hard Diagnostic Set | `data/benchmark_sgs_hard50.json` | 50 | 50 | 0 | Optional diagnostic |
| Free-response Rubrics | `data/free_response_rubrics.json` | 30 | 0 | 30 | Provisional judge scoring |

## Intended Use

- Evaluate model judgment in semiconductor gas-sensing R&D contexts.
- Diagnose evidence-boundary, experimental-design, and safety-gate behavior.
- Compare models on the SGS152 MCQ main leaderboard.
- Use Robustness and Hard50 as diagnostic layers without creating a total suite score.
- Support release review and future benchmark calibration.

## Out-of-scope Use

- Real experimental SOPs.
- Hazardous gas operation guidance.
- Private recipe reconstruction.
- Supplier, collaboration, or private project disclosure.
- A full certification of model experimental execution capability.

## Scoring Status

| Layer | Status |
|---|---|
| SGS152 MCQ | Live standard run completed |
| Free-response | GPT-5.6-sol judge-scored + project-owner-delegated assistant review completed |
| Robustness Set | Live standard diagnostic run completed |
| Hard50 | Live standard diagnostic run completed |

Free-response uses GPT-5.6-sol as judge. The judge is not a participating model, but same-family correlation with the participating GPT-5.5 model may remain. The project owner delegated the 58-row review packet to the assistant; 15 hard fails and the missing-answer zero were confirmed, and 9 dimension scores were adjusted. This is not an independent external blind review.

## Safety and Privacy Boundary

The dataset does not provide private recipe ratios, supplier batch identifiers, executable hazardous-gas steps, alarm/interlock bypass instructions, or reconstructable dangerous procedures.

Safety-related items evaluate high-level go/no-go judgment, facility checks, evidence boundaries, and public communication boundaries.

## Limitations

SGS152 is a compact benchmark and does not cover the full gas-sensing materials space.

Free-response results combine automated judge scores with a completed project-owner-delegated assistant review. Robustness and Hard50 are optional diagnostics, not leaderboard extensions.

## Version History

| Version | Summary |
|---|---|
| 0.4.0 | Domain Core Set established |
| 0.5.0 | Live SGS152 standard run completed, optional diagnostics recorded, GPT-5.6-sol judge review and delegated assistant adjudication added |
