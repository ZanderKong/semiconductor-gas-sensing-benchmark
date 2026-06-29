.PHONY: demo validate lint report eval-mcq score-mcq

demo:
	python3 -m eval.runner --config eval/configs/demo.yaml

validate:
	python3 scripts/validate_tasks.py
	python3 scripts/validate_v3_alpha_distribution.py

lint:
	python3 scripts/lint_benchmark.py

report:
	python3 -m eval.reporting.generate_report --run-dir results/runs/demo

eval-mcq:
	python3 eval/run_eval.py --models gpt-5.5 'openai_compatible|deepseek-v4-pro|https://api.deepseek.com|DEEPSEEK_API_KEY|disabled'

score-mcq:
	python3 eval/score_mcq.py
