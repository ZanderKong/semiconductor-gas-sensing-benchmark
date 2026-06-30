.PHONY: demo validate lint lint-sgs100 build-sgs100 report eval-mcq eval-mcq-frontier eval-robustness-frontier eval-kimi-attempt eval-gpt55-kimi26 eval-robustness-gpt55-kimi26 score-mcq

demo:
	python3 eval/runner.py

build-sgs100:
	python3 scripts/build_sgs100_revision.py

validate:
	python3 scripts/validate_benchmark.py

lint:
	python3 scripts/lint_benchmark.py

lint-sgs100:
	python3 scripts/lint_sgs100_benchmark.py

report:
	python3 -m eval.reporting.generate_report --run-dir results/runs/demo

eval-mcq:
	python3 eval/run_eval.py --models 'openai_compatible|deepseek-v4-pro|https://api.deepseek.com|DEEPSEEK_API_KEY|thinking=enabled|reasoning_effort=high|omit_temperature=true'

eval-mcq-frontier:
	python3 eval/run_eval.py --out results/model_outputs_frontier.csv --raw-dir results/raw_model_outputs_frontier --manifest results/model_run_manifest_frontier.json --timeout 1800 --models 'openai_compatible|deepseek-v4-pro|https://api.deepseek.com|DEEPSEEK_API_KEY|thinking=enabled|reasoning_effort=high|omit_temperature=true' 'openai_compatible|mimo-v2.5-pro|https://api.xiaomimimo.com/v1|MIMO_API_KEY|auth=api-key|omit_temperature=true' 'openai_compatible|kimi-k2.7-code|https://api.moonshot.cn/v1|MOONSHOT_API_KEY|omit_temperature=true'

eval-robustness-frontier:
	python3 eval/run_eval.py --benchmark data/benchmark_sgs100_robustness.json --out results/robustness/model_outputs_robustness_frontier.csv --raw-dir results/robustness/raw_model_outputs_robustness_frontier --manifest results/robustness/model_run_manifest_robustness_frontier.json --timeout 1800 --models 'openai_compatible|deepseek-v4-pro|https://api.deepseek.com|DEEPSEEK_API_KEY|thinking=enabled|reasoning_effort=high|omit_temperature=true' 'openai_compatible|mimo-v2.5-pro|https://api.xiaomimimo.com/v1|MIMO_API_KEY|auth=api-key|omit_temperature=true' 'openai_compatible|kimi-k2.7-code|https://api.moonshot.cn/v1|MOONSHOT_API_KEY|omit_temperature=true'

eval-kimi-attempt:
	python3 eval/run_eval.py --out results/kimi_attempt/model_outputs_kimi_attempt.csv --raw-dir results/kimi_attempt/raw_model_outputs_kimi_attempt --manifest results/kimi_attempt/model_run_manifest_kimi_attempt.json --timeout 300 --models 'openai_compatible|kimi-k2.7-code|https://api.moonshot.cn/v1|MOONSHOT_API_KEY|omit_temperature=true'

eval-gpt55-kimi26:
	python3 eval/run_eval.py --out results/gpt55_kimi26/model_outputs_gpt55_kimi26.csv --raw-dir results/gpt55_kimi26/raw_model_outputs_gpt55_kimi26 --manifest results/gpt55_kimi26/model_run_manifest_gpt55_kimi26.json --timeout 1200 --models gpt-5.5 'openai_compatible|kimi-k2.6|https://api.moonshot.cn/v1|MOONSHOT_API_KEY|omit_temperature=true'

eval-robustness-gpt55-kimi26:
	python3 eval/run_eval.py --benchmark data/benchmark_sgs100_robustness.json --out results/gpt55_kimi26/model_outputs_robustness_gpt55_kimi26.csv --raw-dir results/gpt55_kimi26/raw_model_outputs_robustness_gpt55_kimi26 --manifest results/gpt55_kimi26/model_run_manifest_robustness_gpt55_kimi26.json --timeout 1200 --models gpt-5.5 'openai_compatible|kimi-k2.6|https://api.moonshot.cn/v1|MOONSHOT_API_KEY|omit_temperature=true'

score-mcq:
	python3 eval/score_mcq.py --run-date 2026-06-29 --scope-label '82 MCQ with contextual plausible distractors final' --interpretation 'Final MCQ validation after rewriting options so distractors are plausible standalone research actions and only contextually non-optimal.'
