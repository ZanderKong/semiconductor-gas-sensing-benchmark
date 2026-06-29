# Model Evaluation Recap

## Purpose

This recap documents the real-model MCQ validation run for the portfolio version of the Semiconductor Gas-Sensing Benchmark Mini.

The run verifies that the repository can call external models, parse structured answers, score MCQ outputs, and generate reader-facing result artifacts.

## Run Scope

| Item | Value |
|---|---|
| Run date | 2026-06-29 |
| Benchmark file | `data/benchmark_v1.json` |
| Scored subset | 82 multiple-choice questions |
| Prompt file | `eval/prompts/base_prompt.md` |
| Temperature | 0 |
| GPT path | `gpt-5.5` through Codex CLI |
| DeepSeek path | `deepseek-chat` through DeepSeek OpenAI-compatible API |
| Output file | `results/model_outputs.csv` |
| Run manifest | `results/model_run_manifest.json` |
| Scorer | `eval/score_mcq.py` |

## Result

| Model | Correct / Total | Safety Fail Rate | Interpretation |
|---|---:|---:|---|
| `gpt-5.5` | 82 / 82 | 0.0% | The GPT call, parse, and scoring path completed successfully. |
| `deepseek-chat` | 82 / 82 | 0.0% | The DeepSeek call, parse, and scoring path completed successfully. |

No parser errors, missing answers, or wrong MCQ answers were observed in this run.

## Interpretation

The result validates the evaluation pipeline. It does not prove that the benchmark can rank strong models.

The current MCQ subset is effective as a smoke test for coverage, safety-boundary recognition, and scoring reproducibility. The current MCQ subset is not difficult enough to expose meaningful differences between strong models.

The V3-alpha task-unit layer is the correct next surface for stronger comparisons. It supports Hard Gates, D0-D6 scoring, tool-use assessment, trace capture, and badcase review.

## Follow-Up Work

1. Score the 18 free-response items with the judge protocol and human audit.
2. Add compact table-analysis tasks that require calculation, trend comparison, and evidence reconciliation.
3. Add conflicting-evidence items where every answer option is locally plausible.
4. Run the V3-alpha task units against real models after the tool harness is connected.
5. Report prompt experiments separately from model capability results.
