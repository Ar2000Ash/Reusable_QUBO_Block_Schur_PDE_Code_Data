PYTHON ?= python

.PHONY: all data figures verify audit large-block b8 clean

all: verify figures audit

data:
	$(PYTHON) analysis/build_processed_data.py

figures: data
	$(PYTHON) analysis/generate_figures.py

verify: data
	$(PYTHON) analysis/verify_results.py

audit:
	$(PYTHON) analysis/audit_dirac3.py

large-block:
	$(PYTHON) experiments/run_large_block.py

b8:
	$(PYTHON) experiments/run_b8_optimizer.py

clean:
	rm -rf outputs __pycache__ analysis/__pycache__ experiments/__pycache__ src/qpde_schur/__pycache__
