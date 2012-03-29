PYTHON := python2.7
SCRIPT := config.py
BASE_DIR := $(shell $(PYTHON) $(SCRIPT) get base-dir)
INSTALL_DIR := $(shell $(PYTHON) $(SCRIPT) get install-dir)

install: install-repo-deps

check:
	trial dreambuilder

.PHONY: install-repo-deps dev-repos install check
