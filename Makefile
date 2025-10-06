# Makefile SyntheData Suite (stub)

PYTHON?=python
VENV_DIR=.venv
ACTIVATE=. $(VENV_DIR)/Scripts/activate

.PHONY: help venv install dev-install ui cli test lint fmt clean generate-sample

help:
	@echo "Targets: venv, install, dev-install, ui, cli, test, lint, fmt, clean, generate-sample"

venv:
	$(PYTHON) -m venv $(VENV_DIR)

install: venv
	$(ACTIVATE); pip install -r requirements.txt

dev-install: install
	$(ACTIVATE); pip install -r requirements-optional.txt -e .

ui:
	$(ACTIVATE); streamlit run apps/ui-desktop/app.py

cli:
	$(ACTIVATE); synthedata list-domains

generate-sample:
	$(ACTIVATE); synthedata generate --domain hr_core --rows 1000 --output outputs

lint:
	@echo "(stub) agregar ruff/flake8"

fmt:
	@echo "(stub) agregar black/ruff format"

test:
	$(ACTIVATE); pytest -q || echo "Pytest no instalado todavía (stub)"

clean:
	rm -rf outputs/* || true
