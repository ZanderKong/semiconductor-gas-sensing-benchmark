# Overview

## 中文

Semiconductor Gas-Sensing Mini-Benchmark 0.4.0 是一个面向半导体气敏材料研发任务的中文 benchmark。它把材料选择、传感机理、表征解释、实验设计、数据质量、安全边界和公开写作脱敏转化为结构化评测任务。

项目的核心目标是评价模型能否在专业场景中做出可靠判断：能否识别证据边界，能否设计必要对照，能否处理湿度、温度、流量、基线漂移、选择性和可逆性等真实研发变量，能否在高风险场景中保持安全抽象和合规意识。

SGS-100 主集包含 100 道题，其中 82 道 MCQ 用于自动评分，18 道 free-response 用于 rubric-based 评审。Robustness 层包含 40 道 variants，用于检验模型在表达变化、干扰信息、条件改写和工具观察变化下的判断稳定性。

## English

Semiconductor Gas-Sensing Mini-Benchmark 0.4.0 is a Chinese benchmark for semiconductor gas-sensing R&D reasoning. It converts materials selection, sensing mechanisms, characterization interpretation, experimental design, data quality, safety boundaries, and public-facing research abstraction into structured evaluation tasks.

The benchmark evaluates whether a model can make grounded professional judgments: identify evidence boundaries, design useful controls, reason about humidity, temperature, flow rate, baseline drift, selectivity, reversibility, and maintain safety-aware abstraction in high-risk scenarios.

The SGS-100 main set contains 100 items: 82 multiple-choice items for automatic scoring and 18 free-response items for rubric-based review. The robustness layer adds 40 variants to measure stability under paraphrase, distractors, condition changes, and tool-observation updates.
