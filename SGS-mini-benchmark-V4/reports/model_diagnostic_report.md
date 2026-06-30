# Model Diagnostic Report

## Summary

This report records the latest completed SGS-100 clean-revision MCQ evaluation.

## Run Setup

| Setting | Value |
|---|---|
| Date | 2026-06-30 |
| Benchmark | `data/benchmark.json` |
| Scored subset | 82 MCQ after SGS-100 clean revision |
| Prompt | `eval/prompts/base_prompt.md` |
| Runner | `eval/run_eval.py` |
| Scorer | `eval/score_mcq.py` |
| Model outputs | `results/model_outputs_frontier.csv` |
| Manifest | `results/model_run_manifest_frontier.json` |

## Results

| Model | Provider | Correct / Total | MCQ Accuracy | Safety Fail Rate | Elapsed Seconds |
|---|---|---:|---:|---:|---:|
| deepseek-v4-pro | openai_compatible | 76 / 82 | 92.7% | 12.5% | 94.96 |
| gpt-5.5 | codex_cli | 80 / 82 | 97.6% | 0.0% | 28.29 |
| mimo-v2.5-pro | openai_compatible | 80 / 82 | 97.6% | 0.0% | 37.64 |

## Kimi Status

`kimi-k2.7-code` was attempted through the Moonshot OpenAI-compatible API.

The local environment could not complete a TLS connection to `api.moonshot.cn`.

The fallback `api.moonshot.ai` endpoint was reachable but did not accept the supplied key on `/v1/models`.

The fallback `api.moonshot.ai` endpoint returned an empty reply for a minimal chat-completions request.

The `kimi-k2.7-code-highspeed` variant returned the same empty reply on a minimal chat-completions request.

`kimi-k2.6` was also attempted on the main set and robustness set.

`kimi-k2.6` failed with the same TLS EOF before returning any benchmark answer.

The failed Kimi attempt is retained in the run manifest and is not scored.

The connection probe is retained in `reports/kimi_connection_probe.md`.

## Badcase Summary

DeepSeek missed six items: SGS-027, SGS-028, SGS-037, SGS-039, SGS-080, and SGS-094.

GPT-5.5 missed two items: SGS-001 and SGS-028.

MiMo missed two items: SGS-009 and SGS-028.

SGS-028 remains a shared metric-direction trap for n-type and p-type response comparison.

## SGS-100 Status

The main set contains 100 tasks.

The main set contains 82 automatically scored MCQ items and 18 rubric-scored free-response items.

The robustness layer is scored separately in `reports/model_diagnostic_report_robustness_frontier.md`.

The free-response items are rubric-complete and still require human or model-judge scoring for reported performance.
