# Final Release Audit — v0.6.0

## Completed gates

- item validity: 242/242；
- MCQ option review: 488/488；
- Reference Answer review: 30/30 and 112/112 claims；
- free-response review: 120/120 and 960/960 dimension rows；
- Hard Fail classification: 3 confirmed, 12 downgraded, 1 no-answer；
- Robustness: 40/40；
- Hard50: 50/50；
- raw archive: 46 members, each member SHA-256 recorded；
- raw-to-derived: 0 field differences；
- full diagnostic statistics: generated with fixed seed `20260713`；
- public reviewer-role boundary: audited；
- frozen benchmark and original-output hashes: audited.

## Release interpretation

122 道 MCQ 是唯一主排行榜。Free-response、Robustness 和 Hard50 均单独报告；Hard50 仅作 regression diagnostic。GPT-5.6-sol 是 Judge-only，不是参赛模型。

本轮未采用独立盲审设计，因此不报告该类一致性结论。当前已知科学和内容问题留在冻结数据中，并通过 v0.6.0 审计队列公开披露。
