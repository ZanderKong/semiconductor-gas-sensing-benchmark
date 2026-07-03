# Full Benchmark Analysis

Scope: SGS152, Robustness, and Hard50. Robustness and Hard50 remain diagnostic layers and are not collapsed into a single headline score.

| Model | SGS152 MCQ | Free-response Avg | Robustness | Hard50 |
|---|---:|---:|---:|---:|
| deepseek-v4-pro | 115 / 122 | 6.303 | 29 / 40 | 47 / 50 |
| ep-20260703090429-qpmt7 | 118 / 122 | 6.888 | 32 / 40 | 48 / 50 |
| gpt-5.5 | 117 / 122 | 7.568 | 34 / 40 | 48 / 50 |
| mimo-v2.5-pro | 119 / 122 | 4.843 | 34 / 40 | 47 / 50 |

## Smoke Failures

- kimi-k2.6: HTTP Error 401: Unauthorized

This analysis only uses current standard-run artifacts and does not reuse reconstructed or legacy outputs.
