REPOS := $(shell python config.py get repos)

install-repo-deps:
	sudo apt-get install -y python-yaml bzr git

dev-repos: install-repo-deps
	echo $(REPOS)
