# Full Benchmark Analysis

Scope: SGS152, Robustness, and Hard50. Robustness and Hard50 remain diagnostic layers and are not collapsed into a single headline score.

| Model | SGS152 MCQ | Free-response Avg | Robustness | Hard50 |
|---|---:|---:|---:|---:|
| deepseek-v4-pro | 115 / 122 | 6.303 | 29 / 40 | 47 / 50 |
| ep-20260703090429-qpmt7 | 118 / 122 | 6.888 | 32 / 40 | 48 / 50 |
| gpt-5.5 | 117 / 122 | 7.485 | 34 / 40 | 48 / 50 |
| mimo-v2.5-pro | 119 / 122 | 4.843 | 34 / 40 | 47 / 50 |

Integrated reading: MiMo leads SGS152 MCQ but has the weakest adjudicated free-response average and 3 hard fails. GPT-5.5 ties the strongest Hard50 diagnostic result and leads the adjudicated free-response average after conservative overlap-bias adjustments. Seed-2.1 is the most balanced MCQ runner-up with strong Hard50 diagnostics. DeepSeek trails on SGS152 MCQ and Robustness and preserves one no-rescue missing free-response answer.

This analysis only uses current standard-run artifacts and does not reuse reconstructed or legacy outputs.
