PYTHON = $(shell which python3)
SHELL = /bin/bash
VENV_DIR = venv

.PHONY: install
install: $(VENV_DIR)

$(VENV_DIR): setup.py
	@$(PYTHON) -m venv $@
	@$@/bin/pip install --quiet --upgrade pip
	@$@/bin/pip install --quiet .

.PHONY: lint
lint: $(VENV_DIR)
	@$</bin/pip install --quiet pre-commit
	@$</bin/pre-commit install
	@$</bin/pre-commit run --all-files

.PHONY: clean
clean:
	@git clean -fdfx
