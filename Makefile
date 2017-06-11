BASE=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))
VENV=$(BASE)/venv
VBIN=$(VENV)/bin
VLIB=$(VENV)/lib
PYTHON=$(VBIN)/python
PYTEST=$(VBIN)/pytest
PIP=$(VBIN)/pip
FLAKE8=$(VBIN)/flake8
PYLIB=$(VLIB)/python*/site-packages
PYMARKER=$(VLIB)/.marker


all: venv

bins: bin/*.in

bin/%: bin/%.in
	sed "s?/usr/bin/env python?${PYTHON}?" $< > $@
	chmod +x $@

venv: $(PYMARKER)
$(PYMARKER): requirements.txt $(PYTHON)
	$(PIP) install -r requirements.txt
	touch $@

$(PYTHON):
	virtualenv -p python3 venv

$(PYTEST): requirements-test.txt
	$(PIP) install -r requirements-test.txt

devel: $(PYLIB)/codepunks.egg-link flake8

$(PYLIB)/codepunks.egg-link: venv/bin/python setup.py setup.cfg README.md
	$(PYTHON) setup.py develop
	touch $@

flake8: $(FLAKE8)
$(FLAKE8):
	$(PIP) install flake8

check: $(FLAKE8)
	$(FLAKE8)

tests: $(PYTEST) tests-clean
	$(PYTHON) setup.py test $(FTF)

testsv: $(PYTEST) tests-clean
	$(PYTHON) setup.py test --addopts -s $(FTF)

dist: sdist
sdist:
	$(PYTHON) setup.py sdist

dist-clean:
	rm -rf venv .eggs

tests-clean:
	rm -f tests/tmp

.PHONY: bins venv flake8 check tests dist sdist clean dist-clean tests-clean
