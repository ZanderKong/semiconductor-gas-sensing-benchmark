# Version History

本仓库使用 Git 历史追踪完整版本演化，当前文件只保留轻量版本摘要。active benchmark 位于根目录。

| Version | 状态 | 关键变化 |
|---|---|---|
| 0.1.0 | historical | 早期题库草稿和结构探索 |
| 0.2.0 | historical | 增加半导体气敏材料任务分类 |
| 0.3.0 | historical | 收敛 schema、题型和初步报告结构 |
| 0.4.0 | archived summary | 形成 100 题 Domain Core Set 和 robustness 结果 |
| 0.5.0 | active | 根目录 active SGS152 Main Set，加入 Scientific Stress Set、Hard Diagnostic Set 和 free-response 全量 rubric review |

## 迁移原则

当前仓库只展示最新 active benchmark。0.1.0 到 0.4.0 的完整文件通过 Git 历史追溯，不再以完整目录形式打包在仓库主体中。

保留的历史信息：

- 版本变化摘要；
- 0.4.0 主集分数；
- 0.4.0 robustness 分数；
- 迁移原因；
- 轻量 legacy result CSV。

## 迁移原因

完整历史目录会削弱根目录入口，增加重复数据和维护成本。active package 放在根目录后，README、data、docs、reports、eval、scripts 和 results 都直接指向当前 SGS152 Main Set。
