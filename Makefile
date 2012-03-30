clean:
	find . -name "*.pyc" -exec rm -v {} \;
	rm -rfv _trial_temp
	rm -f twistd.log twistd.pid

install: install-repo-deps

check:
	trial dreambuilder

run:
	twistd -n packager install repos

.PHONY: install-repo-deps dev-repos install check
