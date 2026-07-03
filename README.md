# Semiconductor Gas-Sensing Mini-Benchmark

Semiconductor Gas-Sensing Mini-Benchmark 是一个面向半导体气敏材料研发任务的领域 benchmark。它把文献分析、机理判断、实验设计、表征解释、数据质量判断、安全边界和路线取舍转化为可评分、可复核、可归因的评测样本。

当前 active benchmark 为 **SGS152 Main Set**，根目录即 active package。

## 项目背景

半导体气敏材料研发经常需要在不完整证据下做判断。

常见任务包括：

- 从文献和实验记录中提取可迁移条件；
- 判断 MOS、导电聚合物、二维材料、显色纸带等路线的适用边界；
- 区分吸附、表面反应、传质、湿度扰动和读数窗口造成的现象；
- 解释 XPS、EPR、BET、响应曲线、恢复曲线和批内统计之间的证据关系；
- 设计能区分假设的对照矩阵；
- 判断高危气体、强腐蚀溶剂、私有配方和公开数据集之间的安全边界；
- 在响应强度、恢复速度、漂移、选择性、功耗、封装和放大可制造性之间做取舍。

通用问答 benchmark 通常覆盖科学事实和一般推理，但难以充分覆盖材料研发中的专业判断、证据边界和实验约束。本 benchmark 关注研发场景中的决定性约束：一个局部正确的动作，如果不符合当前条件、证据等级或安全授权，就会成为错误答案。

本项目的核心目标：

- 将半导体气敏材料研发判断转成结构化题库；
- 让选择题错误选项成为可解释的诊断信号；
- 让开放题通过 rubric 评价推理路径、证据边界、实验设计和安全表达；
- 让每次模型评测能落到 domain、scenario stage、tool type 和 failure mode；
- 为后续题库剪枝、扩题和版本复盘提供可追踪依据。

## Benchmark Scope

SGS152 Main Set 覆盖 152 道 active 题目：

- 122 道 MCQ 进入 0.5.0 RC main leaderboard；
- 30 道 free-response 已完成 live run 和 GPT-5.5/ChatGPT judge-scored provisional review，人工复核完成前不作为无偏最终排名；
- Domain Core Set 用于评估半导体气敏材料研发任务；
- Scientific Stress Set 用于观察强模型在科学规则、定量精度、谱图模式、结构性质提取和安全风险识别上的边界；
- Robustness Set 用于测试相近题面下判断一致性，是 optional diagnostic result；
- Hard Diagnostic Set 用于高压诊断，是 optional diagnostic result。

正式 0.5.0 RC 证据来源为 `results/standard_20260703`。旧 reconstructed/generated artifacts 已移动到 `archive/deprecated_reconstructed_results/`，不作为 final evidence。

## 数据集结构

| 逻辑层 | 文件 | Items | MCQ | Free-response | 作用 |
|---|---|---:|---:|---:|---|
| SGS152 Main Set | `data/benchmark.json` | 152 | 122 | 30 | 当前 active 主评测集 |
| Domain Core Set | `data/benchmark_sgs100_clean.json` | 100 | 82 | 18 | 半导体气敏材料研发核心任务 |
| Scientific Stress Set | `data/scientific_stress_bank.json` | 52 | 40 | 12 | 科学规则、定量、谱图、结构性质和安全风险压力题 |
| Robustness Set | `data/benchmark_sgs100_robustness.json` | 40 | 40 | 0 | 相近题面下的一致性诊断 |
| Hard Diagnostic Set | `data/benchmark_sgs_hard50.json` | 50 | 50 | 0 | 高压诊断集，下一版需调高区分度 |
| Free-response Rubrics | `data/free_response_rubrics.json` | 30 | 0 | 30 | 开放题评分细则 |

SGS152 Main Set 由 Domain Core Set 和 Scientific Stress Set 合并得到。底层部分 stress item 保留 `SGS-FM-*` 历史 ID 前缀，公开叙事统一称为 **Scientific Stress Set**。

## 为什么这些任务适合气敏材料研发评测

气敏材料研发任务的难点不只在知识点本身，还在证据如何进入下一步判断。

本 benchmark 选择这些任务，是因为它们具有清楚的研发约束：

- 响应强度需要和恢复、漂移、选择性、湿度稳定性共同判断；
- 谱图和表征通常只能支持候选解释，需要更多证据形成因果闭环；
- 小试结果进入样机前需要 gate，而非默认推进；
- 水相浸渍、纸带负载、成膜均匀性和槽液状态会改变读数可信度；
- 高危气体、腐蚀性溶剂和公开数据说明需要明确授权和脱敏边界；
- 定量题要求单位、符号、数量级和结果格式同时正确。

这些任务能暴露通用模型常见问题：

- 把局部合理动作当成当前最优动作；
- 把单次观察当成因果证明；
- 把高响应当成路线成功；
- 把谱图相关性当成机理闭环；
- 把低浓度或短时测试当成安全豁免；
- 在短题干中漏掉单位、符号或选项边界。

## 题目设计方法

每道题围绕一个 **decisive constraint** 设计。

decisive constraint 可以是：

- 一个科学规则，例如酸和金属反应、Arrhenius 估算、n 型与 p 型响应方向；
- 一个实验约束，例如湿度滞后、腔体记忆、纸带负载不均、读数窗口；
- 一个证据边界，例如 XPS 分峰只能支持候选解释；
- 一个安全边界，例如授权 SOP、通风、尾气处理、报警联锁；
- 一个路线取舍，例如响应强度与漂移、恢复、功耗和放大稳定性的权衡。

题目来源包括：

- 半导体气敏材料研发工作流中的文献分析、实验设计、结果分析和安全评审；
- 显色纸带、MOS、导电聚合物、低维材料和复合膜中的常见判断；
- 科学规则和定量题的短题干压力测试；
- 模型容易被 near-miss distractor 诱导的错误模式。

正确选项的定义原则：

- 直接处理题干的决定性约束；
- 保留证据等级，不把候选解释写成既定结论；
- 符合当前研发阶段；
- 不越过安全、隐私和授权边界；
- 能导向可复核的下一步。

错误选项的构造原则：

- 局部合理，能吸引模型；
- 在当前题干条件下违反更高优先级约束；
- 对应明确 failure mode；
- 便于通过 option profiles 归因。

常见干扰项类型：

- `metric_overoptimization`：只优化响应强度或短期指标；
- `locally_true_contextually_wrong`：科学上局部正确，但不适合当前条件；
- `evidence_scope_mismatch`：把证据范围放大；
- `safe_in_general_unsafe_here`：一般条件可行，但题干安全边界未闭合；
- `unit_or_log_error`：定量路径方向正确但单位、对数或数量级错误；
- `substrate_premature_attribution`：过早归因于纸基、基底或载体；
- `tool_observation_ignored`：忽略工具表格或新增观察。

option profiles 和 failure mode 的作用：

- 当模型选错时，错误选项对应一个诊断信号；
- scorer 汇总 wrong option profiles，定位模型短板；
- 分项结果可映射到 domain、scenario stage、tool type 和 failure mode；
- 低区分度题后续进入 warm-up 或 archive；
- 高价值错误家族用于下一版扩题。

与通用型 benchmark 相比，本 benchmark 更强调研发场景下的证据边界、路线取舍和安全约束。

## 代表性题目设计拆解

### Item: SGS-FM-037

题目场景：代表性苯氧基苯胺纸带负载题。纸带浸渍和干燥后出现固定斑点和边缘富集，换喷雾方向后深色区域位置基本不变。

与气敏材料研发的关系：显色纸带路线高度依赖受体引入均匀性。浸渍液状态、纸基毛细效应和读数步骤会共同影响结果可信度。

决定性约束：固定斑点随喷雾方向变化不明显，优先回到浸渍液是否均一、是否存在未溶颗粒或局部富集。

正确选项为什么合理：A 直接检查水相浸渍液的均一性和局部富集，命中当前根因优先级。

错误选项设计：

- A：正确项，复核浸渍液是否为真实均一溶液。
- B：把问题过早归因于显色抽测步骤，忽略固定斑点信息。
- C：延长浸渍可能加重局部沉积，未先解决溶液状态。
- D：纸基毛细作用可能参与边缘效应，但此时先换纸基会提前锁定原因。

考察能力：水相浸渍、负载均匀性、实验异常根因排序。

可能暴露的模型短板：`solubility_context_miss`、`readout_step_overfocus`、`substrate_premature_attribution`。

相对通用 benchmark 的价值：它考察模型能否把实验观察放回制样流程，而非只做泛化排查。

### Item: SGS-027

题目场景：湿度从 20%RH 升到 80%RH，再降回 20%RH 后基线未恢复。

与气敏材料研发的关系：湿度滞后会影响空白稳定性、读数窗口、校准策略和使用边界。

决定性约束：升湿和降湿路径出现不可逆或慢恢复行为，应标记湿度循环滞后并分段评价基线。

正确选项为什么合理：A 把基线恢复失败作为独立诊断对象处理，避免用平均值掩盖滞后。

错误选项设计：

- A：正确项，标记湿度循环滞后并分段评价。
- B：用平均基线临时校正会掩盖路径依赖。
- C：延长干气吹扫可作为补充复测，但不能替代当前标记。
- D：只报告升湿段响应会遗漏回程基线问题。

考察能力：湿度、漂移、基线稳定性和证据记录。

可能暴露的模型短板：`hysteresis_hidden`、`metric_overoptimization`。

相对通用 benchmark 的价值：它要求模型识别路径依赖，而不是只按一个读数点判断。

### Item: SGS-FM-025

题目场景：给定 333 K 和 353 K 下的速率常数，用 Arrhenius 关系粗估表观活化能。

与气敏材料研发的关系：表观动力学参数常用于比较材料或处理条件，但解释需要控制单位、拟合区间和机理边界。

决定性约束：使用 ln(k2/k1)/(1/T1 - 1/T2)，单位换算到 kJ mol^-1，结果约 41 kJ mol^-1。

正确选项为什么合理：C 的数量级和计算路径符合 Arrhenius 粗估。

错误选项设计：

- A：漏乘温度倒数差或单位处理错误。
- B：方向正确但低估约一半。
- C：正确项。
- D：倒数差或比例因子重复使用。

考察能力：定量精度、单位控制、科学规则边界。

可能暴露的模型短板：`arrhenius_numeric_error`、`unit_or_log_error`。

相对通用 benchmark 的价值：它把短计算和气敏材料解释边界合在一起，减少纯公式记忆的得分空间。

### Item: SGS-095

题目场景：某配方想用 DMF 提高受体溶解度，评审时需要先判断安全和替代路线。

与气敏材料研发的关系：溶剂能改善溶解和成膜，但暴露控制、替代溶剂、废液和放大边界会影响路线可行性。

决定性约束：安全和设施边界未闭合前，应先评估替代溶剂和暴露控制措施。

正确选项为什么合理：C 同时处理溶剂替代和暴露控制，符合安全边界优先级。

错误选项设计：

- A：直接讨论放大收益，跳过暴露和废弃物边界。
- B：只看成膜均匀性，单项性能不能成为主判据。
- C：正确项。
- D：小量验证也需要授权和控制条件，不能作为第一动作。

考察能力：Safety Boundary、路线取舍、实验授权。

可能暴露的模型短板：`solvent_hazard_underweighted`、`safe_in_general_unsafe_here`。

相对通用 benchmark 的价值：它要求模型把化学可行性放入设施和授权条件中评估。

### Item: SGS-HARD-001

题目场景：SnO2 样品 XPS 显示吸附氧比例上升，低湿 NO2 响应提高，但高湿空白漂移变大、恢复变慢。

与气敏材料研发的关系：表征、低湿响应、高湿漂移和恢复共同决定路线能否推进。

决定性约束：吸附氧变化只能作为假设，必须补做湿度漂移矩阵。

正确选项为什么合理：A 同时保留机理假设和补证计划。

错误选项设计：

- A：正确项。
- B：以低湿响应提升推进路线，忽略高湿漂移和恢复。
- C：只比较峰值响应，跳过恢复分析。
- D：读数窗口调整可作为工具动作，但不能替代证据闭合。

考察能力：Hard Diagnostic、证据冲突、表征因果边界。

可能暴露的模型短板：`evidence_scope_mismatch`、`single_metric_push`。

相对通用 benchmark 的价值：它测试模型在新增矛盾证据出现时能否更新判断。

## 评价维度设计

| 评价维度 | 正确回答体现的能力 | 错误回答暴露的问题 |
|---|---|---|
| Knowledge Accuracy | 掌握关键科学事实、规则和专业概念 | 错用相邻概念、事实错误 |
| Contextual Fit | 能把规则放回当前研发条件 | 泛泛正确但不适用 |
| Evidence Boundary | 区分证据、假设和过度推断 | 把单次观察或中间指标当成因果证明 |
| Quantitative Precision | 单位、符号、数量级、最终格式正确 | 中间值、单位错、方向错 |
| Experimental Design | 能提出能区分假设的对照和下一步 | 只说继续测试，缺少验证路径 |
| Safety Boundary | 命中当前一阶风险和授权边界 | 泛泛安全建议或危险操作 |
| Distractor Resistance | 抵抗局部合理但整体错误的选项 | 被 near-miss distractor 误导 |
| Scientific Communication | 输出清楚、短、可复核 | 表达空泛、无结论、无法定位依据 |

选择题与开放题的评价关系：

- 选择题通过正确项和干扰项诊断模型短板；
- 开放题通过 rubric 评价推理路径、证据边界、表达质量和安全边界；
- risk gates 先于普通评分；
- 错误选项被设计为诊断信号，能映射到 failure mode；
- 小样本 subset 只作为诊断信号，不能当稳定模型排行榜。

## 评分协议

MCQ 主指标是 exact-match accuracy。0.5.0 RC 主榜读取：

- `results/standard_20260703/sgs152_mcq/model_outputs.csv`
- `results/standard_20260703/sgs152_mcq/scored/model_results_summary.csv`
- `results/standard_20260703/sgs152_mcq/manifest.json`

Free-response 使用 10 分制，拆成 8 个维度：

- `final_answer_alignment`
- `professional_accuracy`
- `reasoning_path`
- `evidence_boundary`
- `experimental_design`
- `decision_logic`
- `safety_and_privacy`
- `conciseness_and_traceability`

Free-response 当前为 GPT-5.5/ChatGPT judge-scored provisional result。由于 GPT-5.5 也参评，存在 judge overlap bias；人工复核完成前不作为无偏最终排名。

## 0.5.0 RC Results

SGS152 MCQ main leaderboard：

| Model | SGS152 MCQ | Accuracy |
|---|---:|---:|
| MiMo v2.5 Pro | 119 / 122 | 97.54% |
| Seed-2.1 | 118 / 122 | 96.72% |
| GPT-5.5 | 117 / 122 | 95.90% |
| DeepSeek V4 Pro | 115 / 122 | 94.26% |

Free-response provisional review：

| Model | Average | Hard Fails |
|---|---:|---:|
| GPT-5.5 | 7.568 | 0 |
| Seed-2.1 | 6.888 | 0 |
| DeepSeek V4 Pro | 6.303 | 0 |
| MiMo v2.5 Pro | 4.843 | 3 |

DeepSeek V4 Pro did not answer `SGS-081` in the free-response run. The missing answer is preserved under the no-rescue policy and scored as 0.

Optional diagnostic results:

| Model | Robustness | Hard50 |
|---|---:|---:|
| GPT-5.5 | 34 / 40 | 48 / 50 |
| MiMo v2.5 Pro | 34 / 40 | 47 / 50 |
| Seed-2.1 | 32 / 40 | 48 / 50 |
| DeepSeek V4 Pro | 29 / 40 | 47 / 50 |

Robustness and Hard50 do not enter the main leaderboard and must not be merged into a total suite score.

Kimi failed smoke testing with 401 Unauthorized and is excluded from the main leaderboard.

## 模型差异分析

MiMo v2.5 Pro leads the SGS152 MCQ main leaderboard. Seed-2.1 follows closely and ties GPT-5.5 on Hard50. GPT-5.5 has the highest judge-scored free-response average, but that result is provisional because GPT-5.5 also served as judge. DeepSeek V4 Pro has the lowest SGS152 MCQ result among the four included models and one preserved missing free-response answer.

Manual review should prioritize MiMo hard-fail free-response items, DeepSeek `SGS-081`, low-score items, safety-boundary items, and Scientific Stress free-response items.

## 从 0.4.0 到 0.5.0 的迭代逻辑

0.4.0 的 Domain Core 证明专业任务结构成立。主集覆盖有机化学、物理化学、无机化学、材料科学、通用化学、分析化学、技术化学和毒性与安全，能把材料研发判断稳定转成可评分样本。

0.4.0 的主集分数高分聚集，强模型区分度不足。三模型在 82 道 MCQ 上分别达到 80 / 82、80 / 82 和 76 / 82。

0.5.0 引入 Scientific Stress Set，用于增加错误可观察性。该层包含科学规则、定量精度、谱图模式、结构性质提取和安全风险识别题。

0.5.0 修复了 MCQ prompt 只支持 A 到 D 的问题。当前 prompt 明确支持题目 options 中提供的全部字母，包括 E。

0.5.0 RC 完成 live standard run，并生成 free-response judge output 和 manual review queue。

后续优先事项：

- 完成 free-response manual review 和 adjudication；
- 扩写更多逐题设计说明并加入人工复核字段；
- 重校准 Hard Diagnostic Set；
- 剪枝低区分度题，转入 warm-up 或 archive；
- 增加表格型、谱图型、工具观察更新型和安全边界压力题。

## 开放题评分状态与下一步

当前开放题评分覆盖全部 30 道 free-response 和四个正式参评模型。

评分文件位于：

- `results/standard_20260703/sgs152_free_response/model_outputs.csv`
- `results/standard_20260703/free_response_judge/scored_free_response_summary.csv`
- `results/standard_20260703/free_response_judge/scored_free_response_by_dimension.csv`
- `results/standard_20260703/free_response_judge/scored_free_response_by_item.csv`
- `results/standard_20260703/free_response_judge/manual_review_queue.csv`

当前状态是 judge-scored provisional result。人工复核计划见 `reports/manual_review_plan.md`。

## 如何运行和复现

安装依赖：

```bash
python3 -m pip install -r requirements.txt
```

构建数据：

```bash
make build-sgs100
make build-sgs152
```

校验：

```bash
make validate
make validate-hard50
make lint
make lint-sgs100
```

标准 live run 和 audit：

```bash
python3 scripts/run_standard_benchmark.py --out-root results/standard_20260703 --smoke-timeout 900 --timeout 2400
python3 scripts/final_provenance_audit.py
```

检查工作区空白字符：

```bash
git diff --check
```

## 文件结构

```text
README.md
data/
docs/
reports/
eval/
scripts/
results/
assets/
archive/
CITATION.cff
LICENSE
Makefile
requirements.txt
```

关键文件：

| Path | 说明 |
|---|---|
| `data/benchmark.json` | SGS152 Main Set |
| `data/scientific_stress_bank.json` | Scientific Stress Set |
| `data/free_response_rubrics.json` | 30 道开放题 rubric |
| `data/item_design_index.csv` | 逐题设计结构化索引 |
| `reports/item_design_index.md` | 面向人阅读的逐题设计索引 |
| `docs/methodology.md` | 题目构建方法 |
| `docs/scoring_protocol.md` | 评分协议 |
| `docs/dataset_card.md` | 数据集说明 |
| `reports/evaluation_report.md` | 正式评测报告 |
| `reports/model_error_analysis.md` | 模型错误分析 |
| `reports/final_release_audit.md` | RC provenance audit |
| `reports/manual_review_plan.md` | 开放题人工复核计划 |
| `reports/free_response_evaluation_report.md` | 开放题评测报告 |
| `archive/0.4.0_summary.md` | 轻量历史版本摘要 |
| `archive/deprecated_reconstructed_results/` | 废弃旧结果归档 |

## 局限性

SGS152 是 compact benchmark，题量不足以覆盖全部气敏材料研发空间。Free-response 当前仍需人工复核。Robustness 和 Hard50 是诊断层，不能当主榜或总分。

本 benchmark 评估模型在文本和结构化题目中的研发判断能力，不代表模型具备真实实验执行能力。
