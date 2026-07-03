# Dataset Card

## Dataset Summary

| Field | Value |
|---|---|
| Name | Semiconductor Gas-Sensing Mini-Benchmark |
| Active version | 0.5.0 |
| Active set | SGS152 Main Set |
| Language | 中文主导，保留必要英文术语 |
| Domain | Semiconductor gas-sensing materials R&D |
| Main task types | MCQ, free-response |
| Main scoring | MCQ exact-match, free-response rubric review |
| Repository layout | 根目录为 active package，历史版本轻量归档 |

SGS152 Main Set 将半导体气敏材料研发中的专业判断转化为可评分、可复核、可归因样本。数据集关注文献分析、机理判断、实验设计、表征解释、数据质量、安全边界和路线取舍。

## Data Layers

| Layer | File | Items | MCQ | Free-response |
|---|---|---:|---:|---:|
| SGS152 Main Set | `data/benchmark.json` | 152 | 122 | 30 |
| Domain Core Set | `data/benchmark_sgs100_clean.json` | 100 | 82 | 18 |
| Scientific Stress Set | `data/scientific_stress_bank.json` | 52 | 40 | 12 |
| Robustness Set | `data/benchmark_sgs100_robustness.json` | 40 | 40 | 0 |
| Hard Diagnostic Set | `data/benchmark_sgs_hard50.json` | 50 | 50 | 0 |
| Free-response Rubrics | `data/free_response_rubrics.json` | 30 | 0 | 30 |

## Intended Use

适用用途：

- 评估模型在半导体气敏材料研发场景中的专业判断；
- 诊断模型是否能处理证据边界、实验约束和安全 gate；
- 对比模型在 Domain Core 和 Scientific Stress 中的差异；
- 为题库扩写、剪枝、robustness 设计和错误归因提供依据；
- 支持面向人阅读的 benchmark 复盘。

## Out-of-scope Use

不适用用途：

- 真实实验 SOP；
- 高危气体操作指导；
- 私有配方复现；
- 供应链或协作信息披露；
- 对模型实验执行能力的完整认证；
- 对全部化学、材料科学或传感器工程能力的总体排名。

## Domain Coverage

覆盖领域：

- 有机化学；
- 物理化学；
- 无机化学；
- 材料科学；
- 通用化学；
- 分析化学；
- 技术化学；
- 毒性与安全。

覆盖任务：

- 显色纸带受体和纸带负载；
- MOS 表面反应和吸附氧；
- 导电聚合物与低温响应；
- 湿度、漂移、恢复和选择性；
- 谱图、表征和结构性质；
- 定量计算和单位控制；
- 实验矩阵和数据质量；
- 安全、隐私和公开边界。

## Item Fields

核心字段：

- `id`
- `question_type`
- `domain`
- `domain_cn`
- `scenario_stage`
- `tool_type`
- `question`
- `options`
- `answer`
- `answer_rationale`
- `option_profiles`
- `option_rationales`
- `difficulty`
- `scoring_type`
- `evaluation_dimensions`
- `failure_mode`
- `private_dependency_level`
- `tags`
- `rubric`
- `key_points`
- `hard_fails`
- `common_failure_modes`

逐题设计索引：

- `data/item_design_index.csv`
- `reports/item_design_index.md`

## Scoring Status

| Layer | Status |
|---|---|
| SGS152 MCQ | completed |
| Domain Core MCQ | completed |
| Scientific Stress MCQ | completed |
| Robustness Set | completed |
| Hard Diagnostic Set | completed, needs recalibration |
| Free-response | full 30-item rubric review completed |

当前 MCQ leaderboard 覆盖 122 道选择题。Free-response 已生成三模型 30 题回答、模型级汇总、逐维评分和 review samples。

## Safety and Privacy Boundary

数据集不提供：

- 私有配方比例；
- 供应商批号；
- 外部协作敏感信息；
- 可执行高危气体步骤；
- 绕过通风、报警、联锁或授权的建议；
- 可复现实验危险条件。

安全相关题目只评估高层级 go-no-go 判断、设施检查项、证据边界和公开表达边界。

## Limitations

SGS152 是 compact benchmark。它强调可追踪题目机制和错误归因，不覆盖全部气敏材料体系、气体类型、器件结构或实验条件。

Domain Core Set 当前分数偏高，强模型区分度有限。Scientific Stress Set 更适合观察强模型边界，但样本量仍小。Hard Diagnostic Set 当前分数过高，下一版需要增强难度。

开放题评分完成了全量 rubric review，但 live transcript、judge adjudication 和复核一致性需要后续补齐。

## Maintenance Plan

下一版维护计划：

- 增加 live run manifest；
- 归档 free-response 原始模型会话；
- 对 Hard Diagnostic Set 重校准；
- 将低区分度题转入 warm-up 或 archive；
- 扩展表格、谱图、工具观察更新和安全边界题；
- 增加逐题设计索引中的人工复核字段。

## Version History

| Version | Summary |
|---|---|
| 0.4.0 | Domain Core Set 成型，主集分数高分聚集 |
| 0.5.0 | active SGS152 Main Set，加入 Scientific Stress Set 和 free-response 全量 rubric review |

完整历史通过 Git 追溯。仓库主体只保留 active benchmark 和轻量 archive。
