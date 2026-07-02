.PHONY: demo validate validate-hard50 lint lint-sgs100 report eval-mcq score-mcq

ACTIVE_DIR := versions/0.5.0

demo:
	$(MAKE) -C $(ACTIVE_DIR) demo

validate:
	$(MAKE) -C $(ACTIVE_DIR) validate
	$(MAKE) -C $(ACTIVE_DIR) validate-hard50

validate-hard50:
	$(MAKE) -C $(ACTIVE_DIR) validate-hard50

lint:
	$(MAKE) -C $(ACTIVE_DIR) lint
	$(MAKE) -C $(ACTIVE_DIR) lint-sgs100

lint-sgs100:
	$(MAKE) -C $(ACTIVE_DIR) lint-sgs100

report:
	$(MAKE) -C $(ACTIVE_DIR) report

eval-mcq:
	$(MAKE) -C $(ACTIVE_DIR) eval-mcq

score-mcq:
	$(MAKE) -C $(ACTIVE_DIR) score-mcq
