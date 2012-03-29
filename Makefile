PYTHON := python2.7
SCRIPT := config.py
BASE_DIR := $(shell $(PYTHON) $(SCRIPT) get base-dir)
INSTALL_DIR := $(shell $(PYTHON) $(SCRIPT) get install-dir)

install-repo-deps:
	sudo apt-get install -y python-yaml bzr git python-twisted

dev-lp-repos: REPOS = $(shell $(PYTHON) $(SCRIPT) get lp-repos)
dev-lp-repos:
	$(foreach REPO, $(REPOS), cd $(INSTALL_DIR); bzr branch $(REPO);)

dev-git-repos: REPOS = $(shell $(PYTHON) $(SCRIPT) get git-repos)
dev-git-repos:
	$(foreach REPO, $(REPOS), cd $(INSTALL_DIR); git clone $(REPO);)

dev-repos: install-repo-deps dev-lp-repos dev-git-repos


install: install-repo-deps

check:
	trial dreambuilder

.PHONY: install-repo-deps dev-repos install check
