# Changelog

## mini-benchmark 0.4.0

### 中文

- 发布 SGS-100 主评测集，包含 82 道 multiple-choice 和 18 道 free-response。
- 建立 40 道 robustness variants，用于检验表达改写、干扰信息、条件变化、安全诱导和工具观察更新。
- 为全部 free-response 题目配置 10 分制 rubric、key points、risk gates 和 common scoring notes。
- 完成 MCQ 选项重构，实现四选项长度均衡、答案分布均衡和局部合理 distractor。
- 完成自动化验收脚本，覆盖题量比例、领域分布、选项质量、rubric 结构、robustness parent linkage 和安全抽象规则。
- 完成 GPT-5.5、MiMo v2.5 Pro 和 DeepSeek V4 Pro 的主集与 robustness 评测摘要。
- 重构 README、dataset card、HR review guide 和报告体系，形成适合 GitHub、简历项目集和技术面试使用的专业展示版本。

### English

- Released the SGS-100 main benchmark with 82 multiple-choice items and 18 free-response items.
- Added 40 robustness variants covering paraphrase, distractor, contradiction, adversarial safety, and tool-observation shifts.
- Added 10-point rubrics, key points, risk gates, and scoring notes for all free-response items.
- Rebuilt MCQ options with balanced option length, balanced answer distribution, and locally plausible distractors.
- Added automated acceptance checks for dataset size, domain distribution, option quality, rubric structure, robustness linkage, and safety abstraction.
- Curated main-set and robustness evaluation summaries for GPT-5.5, MiMo v2.5 Pro, and DeepSeek V4 Pro.
- Rebuilt the reader-facing documentation for GitHub, portfolio review, and technical interviews.
