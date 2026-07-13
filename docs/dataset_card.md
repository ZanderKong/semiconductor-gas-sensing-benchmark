# Dataset Card — SGS152 v0.6.0

## Intended use

SGS152 用于诊断半导体气敏材料研发中的专业推理，包括文献解释、机理证据边界、实验设计、数据质量、工艺放大、安全和路线选择。它不是实验室安全授权系统，也不能替代 SOP、培训、机构审批或工程控制。

## Composition and reporting

- Main set：152 题，其中 122 道 MCQ 是唯一主排行榜，30 道 free-response 单独报告；
- Robustness：40 道可选一致性诊断；
- Hard50：50 道 regression diagnostic，因 47–48/50 的饱和结果不作为 hard leaderboard；
- participating models：GPT-5.5、Seed-2.1、DeepSeek V4 Pro、MiMo v2.5 Pro；
- Judge：GPT-5.6-sol，仅用于 free-response 固定 rubric 评分，不是参赛模型。

## Review coverage

专家 X 完成 242 题有效性审核、488 个 MCQ 选项审核、30 个 Reference Answer 与 112 条 claim-level 证据审核，以及 120 条 free-response 的 960 条维度评分复核。项目负责人确认冻结边界与评分政策。

## Frozen content and limitations

v0.6.0 不修改题干、选项、Gold、Reference Answer、题目 ID 或原始模型输出。已知问题保留并公开披露：

- 5 个 P0：`SGS-FM-034`、`SGS-007-R03`、`SGS-097-R03`、`SGS-HARD-016`、`SGS-HARD-028`；
- 56 个可辩护的非 Gold 选项；
- 2 个 Robustness P0 和 2 个 Hard50 P0；
- 部分工程 gate 和脱敏规则是项目规范，不是可由外部文献单独证明的科学事实；
- CuO–H₂S 相变归因与一项纸带负载根因仍需直接证据；
- 本轮未采用独立盲审设计。

完整逐题记录见 [`review/v0.6.0/`](../review/v0.6.0/)。
