.PHONY: demo validate lint report eval-mcq score-mcq

V4_DIR := SGS-mini-benchmark-V4

demo:
	$(MAKE) -C $(V4_DIR) demo

validate:
	$(MAKE) -C $(V4_DIR) validate

lint:
	$(MAKE) -C $(V4_DIR) lint
	$(MAKE) -C $(V4_DIR) lint-sgs100

report:
	$(MAKE) -C $(V4_DIR) report

eval-mcq:
	$(MAKE) -C $(V4_DIR) eval-mcq

score-mcq:
	$(MAKE) -C $(V4_DIR) score-mcq
