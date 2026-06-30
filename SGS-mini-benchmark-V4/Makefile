.PHONY: demo validate lint lint-sgs100 build-sgs100 report eval-mcq eval-frontier eval-robustness-frontier eval-gpt55 eval-robustness-gpt55 score-mcq

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

eval-frontier:
	python3 eval/run_eval.py --out results/model_outputs_frontier.csv --raw-dir results/raw_model_outputs_frontier --manifest results/model_run_manifest_frontier.json --timeout 1800 --models 'openai_compatible|deepseek-v4-pro|https://api.deepseek.com|DEEPSEEK_API_KEY|thinking=enabled|reasoning_effort=high|omit_temperature=true' 'openai_compatible|mimo-v2.5-pro|https://api.xiaomimimo.com/v1|MIMO_API_KEY|auth=api-key|omit_temperature=true'

eval-robustness-frontier:
	python3 eval/run_eval.py --benchmark data/benchmark_sgs100_robustness.json --out results/robustness/model_outputs_robustness_frontier.csv --raw-dir results/robustness/raw_model_outputs_robustness_frontier --manifest results/robustness/model_run_manifest_robustness_frontier.json --timeout 1800 --models 'openai_compatible|deepseek-v4-pro|https://api.deepseek.com|DEEPSEEK_API_KEY|thinking=enabled|reasoning_effort=high|omit_temperature=true' 'openai_compatible|mimo-v2.5-pro|https://api.xiaomimimo.com/v1|MIMO_API_KEY|auth=api-key|omit_temperature=true'

eval-gpt55:
	python3 eval/run_eval.py --out results/gpt55/model_outputs_gpt55.csv --raw-dir results/gpt55/raw_model_outputs_gpt55 --manifest results/gpt55/model_run_manifest_gpt55.json --timeout 1200 --models gpt-5.5

eval-robustness-gpt55:
	python3 eval/run_eval.py --benchmark data/benchmark_sgs100_robustness.json --out results/gpt55/model_outputs_robustness_gpt55.csv --raw-dir results/gpt55/raw_model_outputs_robustness_gpt55 --manifest results/gpt55/model_run_manifest_robustness_gpt55.json --timeout 1200 --models gpt-5.5

score-mcq:
	python3 eval/score_mcq.py --run-date 2026-06-30 --scope-label 'mini-benchmark 0.4.0 SGS-100 main MCQ set' --interpretation 'Domain-grounded MCQ validation for semiconductor gas-sensing R&D judgment.'
