# Live Free-response Judge Report

This report scores live model free-response outputs with the fixed `gpt-5.6-sol` judge.

Bias note: Judge is not a participating model, but same-family correlation with the participating GPT model may remain; automated scores require clearly labeled review context.

| Model | Items | Total | Average | Hard Fails |
|---|---:|---:|---:|---:|
| deepseek-v4-pro | 30 | 201.65 | 6.722 | 0 |
| ep-20260703090429-qpmt7 | 30 | 224.80 | 7.493 | 4 |
| gpt-5.5 | 30 | 244.50 | 8.150 | 0 |
| mimo-v2.5-pro | 30 | 163.20 | 5.440 | 11 |

Manual review queue includes hard-fail items and low/disputed-score items.

Inputs:
- Benchmark: `data/benchmark.json`
- Model outputs: `results/standard_20260703/sgs152_free_response/model_outputs.csv`
- Judge prompt: `eval/prompts/free_response_judge_prompt.md`
