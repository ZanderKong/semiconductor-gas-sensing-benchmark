.PHONY: demo validate validate-hard50 lint lint-sgs100 build-sgs100 build-sgs152 build-hard50 report eval-mcq eval-frontier eval-robustness-frontier eval-hard50-frontier eval-hard50-gpt55 eval-hard50-all eval-gpt55 eval-robustness-gpt55 score-mcq score-hard50-all score-hard50-gpt55

demo:
	python3 eval/runner.py

build-sgs100:
	python3 scripts/build_sgs100_revision.py

build-sgs152:
	python3 scripts/build_sgs152_merged.py

build-hard50:
	python3 scripts/build_sgs_hard50.py

validate:
	python3 scripts/validate_benchmark.py

validate-hard50: build-hard50
	python3 scripts/validate_hard50.py

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

eval-hard50-frontier:
	python3 eval/run_eval.py --benchmark data/benchmark_sgs_hard50.json --out results/hard50/model_outputs_hard50_frontier.csv --raw-dir results/hard50/raw_model_outputs_hard50_frontier --manifest results/hard50/model_run_manifest_hard50_frontier.json --timeout 1800 --models 'openai_compatible|deepseek-v4-pro|https://api.deepseek.com|DEEPSEEK_API_KEY|thinking=enabled|reasoning_effort=high|omit_temperature=true' 'openai_compatible|kimi-k2.6|https://api.moonshot.ai/v1|KIMI_API_KEY|thinking=disabled|omit_temperature=true' 'openai_compatible|mimo-v2.5-pro|https://api.xiaomimimo.com/v1|MIMO_API_KEY|auth=api-key|omit_temperature=true'

eval-gpt55:
	python3 eval/run_eval.py --out results/gpt55/model_outputs_gpt55.csv --raw-dir results/gpt55/raw_model_outputs_gpt55 --manifest results/gpt55/model_run_manifest_gpt55.json --timeout 1200 --models gpt-5.5

eval-robustness-gpt55:
	python3 eval/run_eval.py --benchmark data/benchmark_sgs100_robustness.json --out results/gpt55/model_outputs_robustness_gpt55.csv --raw-dir results/gpt55/raw_model_outputs_robustness_gpt55 --manifest results/gpt55/model_run_manifest_robustness_gpt55.json --timeout 1200 --models gpt-5.5

eval-hard50-gpt55:
	python3 eval/run_eval.py --benchmark data/benchmark_sgs_hard50.json --out results/hard50/model_outputs_hard50_gpt55.csv --raw-dir results/hard50/raw_model_outputs_hard50_gpt55 --manifest results/hard50/model_run_manifest_hard50_gpt55.json --timeout 1200 --models gpt-5.5

eval-hard50-all:
	python3 eval/run_eval.py --benchmark data/benchmark_sgs_hard50.json --out results/hard50/model_outputs_hard50_all.csv --raw-dir results/hard50/raw_model_outputs_hard50_all --manifest results/hard50/model_run_manifest_hard50_all.json --timeout 1800 --models gpt-5.5 'openai_compatible|deepseek-v4-pro|https://api.deepseek.com|DEEPSEEK_API_KEY|thinking=enabled|reasoning_effort=high|omit_temperature=true' 'openai_compatible|kimi-k2.6|https://api.moonshot.ai/v1|KIMI_API_KEY|thinking=disabled|omit_temperature=true' 'openai_compatible|mimo-v2.5-pro|https://api.xiaomimimo.com/v1|MIMO_API_KEY|auth=api-key|omit_temperature=true'

score-mcq:
	python3 eval/score_mcq.py --outputs results/sgs152_merged/model_outputs_sgs152_merged_all.csv --summary results/sgs152_merged/scored/model_results_summary.json --badcases results/sgs152_merged/scored/review_items.json --diagnostic-report results/sgs152_merged/scored/diagnostic_report.md --scope-label 'mini-benchmark 0.5.0 SGS152 active MCQ set' --interpretation 'Active SGS152 validation combines semiconductor gas-sensing R&D judgment with Scientific Stress Set mechanisms.'

score-hard50-all:
	python3 eval/score_mcq.py --benchmark data/benchmark_sgs_hard50.json --outputs results/hard50/model_outputs_hard50_all.csv --summary results/hard50/scored_all/model_results_summary.json --badcases results/hard50/scored_all/review_items.json --diagnostic-report results/hard50/scored_all/diagnostic_report.md --run-date 2026-06-30 --scope-label 'mini-benchmark 0.5.0 SGS-Hard-50 diagnostic MCQ set' --interpretation 'Hard-set scoring focuses on top-model discrimination and failure attribution across evidence conflict, condition update, safety boundary, tool observation, tradeoff, and mechanism-transfer traps.'

score-hard50-gpt55:
	python3 eval/score_mcq.py --benchmark data/benchmark_sgs_hard50.json --outputs results/hard50/model_outputs_hard50_gpt55.csv --summary results/hard50/scored_gpt55/model_results_summary.json --badcases results/hard50/scored_gpt55/review_items.json --diagnostic-report results/hard50/scored_gpt55/diagnostic_report.md --run-date 2026-06-30 --scope-label 'mini-benchmark 0.5.0 SGS-Hard-50 diagnostic MCQ set' --interpretation 'Hard-set scoring focuses on whether a strong model updates judgment under conflicting evidence, tool observations, safety boundaries, and realistic R&D tradeoffs.'
