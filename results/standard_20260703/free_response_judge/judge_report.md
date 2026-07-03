# Live Free-response Judge Report

This report scores live model free-response outputs with a fixed ChatGPT/GPT-5.5 judge.

Bias note: the judge model overlaps with one participating model family, so judge scores must be interpreted with this stated bias.

| Model | Items | Total | Average | Hard Fails |
|---|---:|---:|---:|---:|
| deepseek-v4-pro | 30 | 189.10 | 6.303 | 0 |
| ep-20260703090429-qpmt7 | 30 | 206.65 | 6.888 | 0 |
| gpt-5.5 | 30 | 227.05 | 7.568 | 0 |
| mimo-v2.5-pro | 30 | 145.30 | 4.843 | 3 |

Manual review queue includes hard-fail items and low/disputed-score items.

Inputs:
- Benchmark: `data/benchmark.json`
- Model outputs: `results/standard_20260703/sgs152_free_response/model_outputs.csv`
- Judge prompt: `eval/prompts/free_response_judge_prompt.md`
