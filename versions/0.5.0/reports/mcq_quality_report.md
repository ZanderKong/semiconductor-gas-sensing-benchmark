# MCQ Quality Report

## Scope

Active SGS152 contains 122 MCQ items:

| Layer | MCQ Count | Role |
|---|---:|---|
| Legacy SGS100 | 82 | 半导体气敏研发专业判断 |
| Failure-mined design bank | 40 | 强模型失败机制复测 |

## Quality Controls

| Check | Status |
|---|---|
| Sequential option keys | Passed |
| Answer key coverage | Passed |
| Option rationale coverage | Passed |
| Domain distribution check | Passed |
| Answer distribution check | Passed |
| Safety/private recipe lint | Passed |

## Answer Distribution

| Answer | Count |
|---|---:|
| A | 34 |
| B | 29 |
| C | 29 |
| D | 29 |
| E | 1 |

## Design Assessment

Legacy SGS MCQ 使用较均衡的四选项结构，适合评估真实研发语境中的材料选择、证据边界和安全 gate。Failure-mined MCQ 保留不同选项数量和更强的近邻干扰项，适合观察模型是否被关键词匹配、相邻概念或中间量诱导。

两层题目共同解决一个问题：只靠领域题容易让强模型接近满分，只靠高压短题又缺少项目主题。SGS152 将二者合并后，既保留气敏 benchmark 的专业性，也提高了强模型区分度。
