# Evaluation Report

## Evaluation Scope

| Field | Value |
|---|---|
| Version | 0.5.0 |
| Main set | SGS152 Main Set |
| Automated leaderboard | 122 MCQ items |
| Free-response status | 30 free-response items are rubric-defined and are not included in the current automated MCQ leaderboard. |
| Prompt | `eval/prompts/base_prompt.md` |
| Scorer | `eval/score_mcq.py` |

## SGS152 Main Set Results

| Model | Correct / Total | Accuracy | Safety Fail Rate |
|---|---:|---:|---:|
| DeepSeek V4 Pro | 99 / 122 | 81.2% | 0.0% |
| GPT-5.5 | 99 / 122 | 81.2% | 0.0% |
| MiMo v2.5 Pro | 100 / 122 | 82.0% | 12.5% |

## Split Results

| Model | Domain Core MCQ | Scientific Stress MCQ |
|---|---:|---:|
| DeepSeek V4 Pro | 78 / 82 | 21 / 40 |
| GPT-5.5 | 80 / 82 | 19 / 40 |
| MiMo v2.5 Pro | 76 / 82 | 24 / 40 |

## Robustness Set

| Model | Correct / Total | Accuracy |
|---|---:|---:|
| MiMo v2.5 Pro | 36 / 40 | 90.0% |
| GPT-5.5 | 35 / 40 | 87.5% |
| DeepSeek V4 Pro | 30 / 40 | 75.0% |

## Hard Diagnostic Set

| Model | Correct / Total | Accuracy |
|---|---:|---:|
| DeepSeek V4 Pro | 48 / 50 | 96.0% |
| GPT-5.5 | 48 / 50 | 96.0% |
| MiMo v2.5 Pro | 47 / 50 | 94.0% |

## Interpretation

Domain Core MCQ results show that the tested models handle most routine semiconductor gas-sensing R&D judgments. Scientific Stress MCQ results create stronger separation. The score gap indicates that exact rules, quantitative precision, structure-property extraction, expert boundary conditions, and safety specificity remain useful pressure points for frontier-model comparison.

Hard Diagnostic Set accuracy remains high. This result suggests that the current hard layer is useful for failure attribution but should be made more selective in the next version.
