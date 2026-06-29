.PHONY: demo validate lint report

demo:
	python3 -m eval.runner --config eval/configs/demo.yaml

validate:
	python3 scripts/validate_tasks.py

lint:
	python3 scripts/lint_benchmark.py

report:
	python3 -m eval.reporting.generate_report --run-dir results/runs/demo

