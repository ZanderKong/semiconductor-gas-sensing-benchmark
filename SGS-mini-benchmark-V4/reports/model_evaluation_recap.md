# Model Evaluation Recap

## Purpose

This recap documents the 2026-06-30 SGS-100 clean-revision model evaluation.

## Main-Set Run Scope

| Item | Value |
|---|---|
| Run date | 2026-06-30 |
| Benchmark file | `data/benchmark.json` |
| Scored subset | 82 multiple-choice questions |
| Prompt file | `eval/prompts/base_prompt.md` |
| Runner | `eval/run_eval.py` |
| Output file | `results/model_outputs_frontier.csv` |
| Run manifest | `results/model_run_manifest_frontier.json` |
| Scorer | `eval/score_mcq.py` |

## Main-Set Results

| Model | Correct / Total | MCQ Accuracy | Safety Fail Rate | Wrong IDs |
|---|---:|---:|---:|---|
| `mimo-v2.5-pro` | 80 / 82 | 97.6% | 0.0% | SGS-009, SGS-028 |
| `gpt-5.5` | 80 / 82 | 97.6% | 0.0% | SGS-001, SGS-028 |
| `deepseek-v4-pro` | 76 / 82 | 92.7% | 12.5% | SGS-027, SGS-028, SGS-037, SGS-039, SGS-080, SGS-094 |

## Robustness Results

| Model | Correct / Total | Robustness Accuracy | Notes |
|---|---:|---:|---|
| `mimo-v2.5-pro` | 36 / 40 | 90.0% | Strong paraphrase and distractor stability; weaker safety and tool-shift behavior |
| `gpt-5.5` | 35 / 40 | 87.5% | Strong tool-observation and safety variants; weaker paraphrase and distractor variants on SGS-001 and SGS-035 |
| `deepseek-v4-pro` | 30 / 40 | 75.0% | Strong safety-refusal variants; weak tool-observation-shift variants |

## Kimi Attempt

`kimi-k2.7-code` was configured with the Moonshot OpenAI-compatible endpoint from the Kimi documentation.

The Kimi documentation index at `https://platform.kimi.com/docs/llms.txt` was fetched on 2026-06-30 before the final probe.

The final probe used the documented `https://api.moonshot.cn/v1` base URL and `Authorization: Bearer $MOONSHOT_API_KEY` header.

The local environment could not complete a TLS connection to `https://api.moonshot.cn/v1`.

The fallback endpoint `https://api.moonshot.ai/v1` was also tested.

The fallback endpoint returned invalid authentication on `/v1/models`.

The fallback endpoint returned an empty server reply on a minimal chat-completions request.

The `kimi-k2.7-code-highspeed` variant was also tested with a minimal chat-completions request and returned an empty server reply.

The Kimi attempt is recorded in `results/model_run_manifest_frontier.json` and `results/robustness/model_run_manifest_robustness_frontier.json`.

A Kimi-only attempt is recorded in `results/kimi_attempt/model_run_manifest_kimi_attempt.json`.

The Kimi 2.6 attempt is recorded in `results/gpt55_kimi26/model_run_manifest_gpt55_kimi26.json` and `results/gpt55_kimi26/model_run_manifest_robustness_gpt55_kimi26.json`.

The connection probe is recorded in `reports/kimi_connection_probe.md`.

## Interpretation

The clean revision keeps the main set compact and professionally plausible.

The main-set MCQ results still require badcase review because high overall accuracy can hide safety, metric-direction, and evidence-boundary failures.

The robustness layer exposes stronger separation between models than the main set.

The free-response layer is rubric-complete, but it still requires human or judge scoring before it can be reported as model performance.
