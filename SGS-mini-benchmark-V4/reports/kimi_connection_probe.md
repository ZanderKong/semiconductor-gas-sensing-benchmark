# Kimi Connection Probe

## Probe Date

2026-06-30.

## Purpose

This probe records why Kimi scoring is not available in the current local environment.

## Documentation Checked

The Kimi documentation index at `https://platform.kimi.com/docs/llms.txt` was fetched on 2026-06-30.

The index lists the API overview, chat-completions reference, model-list reference, Kimi K2.6 quickstart, Kimi K2.7 Code quickstart, benchmark best practice, and OpenAI migration pages.

The API overview states that SDK clients should use `https://api.moonshot.cn/v1` and that direct HTTP calls should use paths such as `https://api.moonshot.cn/v1/chat/completions`.

The local probe used the documented `.cn` base URL and the `Authorization: Bearer $MOONSHOT_API_KEY` header.

## Configured Models

`kimi-k2.7-code` was tested as the requested strongest Kimi coding model.

`kimi-k2.7-code-highspeed` was tested as a documented high-speed variant.

`kimi-k2.6` was tested after the user requested Kimi 2.6 coverage.

## Endpoint Results

| Endpoint | Probe | Result |
|---|---|---|
| `https://api.moonshot.cn/v1/models` | `curl` model-list request | TLS connection failed before HTTP response |
| `https://api.moonshot.cn/v1/chat/completions` | benchmark runner request | TLS EOF before model output |
| `https://api.moonshot.ai/v1/models` | `curl` model-list request | HTTP 401 invalid authentication |
| `https://api.moonshot.ai/v1/chat/completions` | minimal chat request with `kimi-k2.7-code` | Empty reply from server; HTTP status 000 |
| `https://api.moonshot.ai/v1/chat/completions` | minimal chat request with `kimi-k2.7-code-highspeed` | Empty reply from server; HTTP status 000 |
| `https://api.moonshot.cn/v1/chat/completions` | benchmark runner request with `kimi-k2.6` | TLS EOF before model output |
| `https://api.moonshot.cn/v1/users/me/balance` | direct HTTP probe after checking official docs | TLS EOF before HTTP response |
| `https://api.moonshot.cn/v1/models` | direct HTTP probe after checking official docs | TLS EOF before HTTP response |
| `https://api.moonshot.cn/v1/chat/completions` | direct HTTP probe with `kimi-k2.6` after checking official docs | TLS EOF before HTTP response |

## Runner Evidence

The main-set Kimi attempt is recorded in `results/model_run_manifest_frontier.json`.

The robustness Kimi attempt is recorded in `results/robustness/model_run_manifest_robustness_frontier.json`.

The Kimi-only attempt is recorded in `results/kimi_attempt/model_run_manifest_kimi_attempt.json`.

The Kimi 2.6 main-set attempt is recorded in `results/gpt55_kimi26/model_run_manifest_gpt55_kimi26.json`.

The Kimi 2.6 robustness attempt is recorded in `results/gpt55_kimi26/model_run_manifest_robustness_gpt55_kimi26.json`.

## Interpretation

The failure occurs before any benchmark answer is returned.

The failure is not a scoring failure.

The failure is not caused by missing benchmark files.

The failure is consistent with an external API endpoint, network, or credential acceptance problem.

Kimi scoring requires a reachable Moonshot endpoint and a key accepted by that endpoint.
