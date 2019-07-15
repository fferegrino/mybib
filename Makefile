PIPENV := pipenv run

BLACK_TARGETS := $(shell find . -name "*.py" -not -path "*/.venv/*" -not -path "*/.tox/*")
MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_DIR := $(notdir $(patsubst %/,%,$(dir $(MAKEFILE_PATH))))

.EXPORT_ALL_VARIABLES:
PIPENV_VENV_IN_PROJECT = 1

experiment:
	$(PIPENV) jupyter
.PHONY: experiment

create_env:
	pipenv install --dev
.PHONY: create_env

run_tests:
	PYTHONPATH=. $(PIPENV) pytest --cov=mybib --cov-report html:htmlcov test/
.PHONY: run_tests

format:
	$(PIPENV) isort --apply
	$(PIPENV) black $(BLACK_TARGETS)
.PHONY: format

lint:
	$(PIPENV) isort --check-only
	$(PIPENV) black --check $(BLACK_TARGETS)
.PHONY: lint
