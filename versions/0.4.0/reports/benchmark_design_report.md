# Benchmark Design Report

## 中文

### 设计定位

Semiconductor Gas-Sensing Mini-Benchmark 0.4.0 将半导体气敏材料研发中的核心判断任务转化为结构化评测资产。它关注模型在专业问题中的判断质量，而非单纯事实回忆。评测对象包括材料路线取舍、传感机理解释、表征证据边界、实验对照设计、数据质量评估、工艺放大判断和安全合规表达。

### 任务结构

| Layer | Count | 设计作用 |
|---|---:|---|
| Main MCQ | 82 | 自动评分，检验专业判断和局部语境优先级 |
| Free-response | 18 | Rubric 评分，检验研究问题组织和实验设计能力 |
| Robustness variants | 40 | 检验表达改写、干扰信息、条件变化和工具观察更新 |

### 学术训练映射

该 benchmark 把生化环材训练中的通用能力转化为可测量维度：

- 文献阅读中的证据等级判断。
- 材料机理分析中的变量控制和边界意识。
- 实验设计中的对照矩阵、重复性和 go/no-go 规则。
- 分析化学中的校准、LOD、基线、干扰和数据完整性。
- 环境与安全训练中的风险抽象、合规 gate 和公开写作脱敏。

### 工程实现

项目通过 JSON/CSV 数据文件、schema、validation scripts、lint scripts、model runner、MCQ scorer 和 bilingual reports 形成完整交付链路。数据结构支持自动评分、人工审阅、rubric 评审和 robustness 分层分析。

## English

### Design Positioning

Semiconductor Gas-Sensing Mini-Benchmark 0.4.0 converts core R&D judgment tasks in semiconductor gas-sensing materials into a structured evaluation asset. It focuses on professional reasoning quality rather than factual recall. The benchmark evaluates materials route selection, sensing-mechanism interpretation, evidence boundaries, experimental controls, data quality, scale-up reasoning, and safety-aware communication.

### Task Structure

| Layer | Count | Purpose |
|---|---:|---|
| Main MCQ | 82 | Automatic scoring for domain judgment and local-context prioritization |
| Free-response | 18 | Rubric-based review for research framing and experimental design |
| Robustness variants | 40 | Stability checks under paraphrase, distractors, condition changes, and tool-observation updates |

### Academic Skill Mapping

The benchmark operationalizes transferable academic skills from chemistry, materials science, environmental safety, and biomedical-style evidence discipline:

- Evidence-level judgment in literature reading.
- Variable control and boundary awareness in mechanistic analysis.
- Control matrices, reproducibility, and go/no-go logic in experimental design.
- Calibration, LOD, baseline, interference, and data integrity in analytical chemistry.
- Safety abstraction, compliance gates, and de-identified public communication.

### Engineering Implementation

The package provides JSON/CSV datasets, schema, validation scripts, lint scripts, a model runner, an MCQ scorer, and bilingual reports. The structure supports automatic scoring, table review, rubric-based review, and layered robustness analysis.
