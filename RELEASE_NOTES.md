# SGS Benchmark v0.6.0 Release Notes

v0.6.0 是审计与评分政策迭代，不是题库内容改版。题干、选项、Gold、Reference Answer、题目 ID 和原始模型输出均未修改。

本版本新增 242 题逐题审核、488 选项审核、112 条 Reference claim 证据审核、120 条 free-response 与 960 条维度评分复核。专家 X 将 15 个历史 Hard Fail 重分类为 3 个 confirmed 和 12 个普通维度问题；3 个 confirmed 项按官方规则归零。DeepSeek `SGS-081` 继续按原始缺答计 0。

GPT-5.6-sol 仅作为 Judge，不是参赛模型。122 道 MCQ 仍是唯一主排行榜；free-response 单独报告；Robustness 是可选诊断；Hard50 因高度饱和仅作 regression diagnostic。

发布同时披露 5 个冻结 P0 和 56 个可辩护非 Gold 选项。raw archive 的 46 个成员已完成逐哈希验证和确定性重建，raw-to-derived 逐字段差异为 0。本轮未采用独立盲审设计。
