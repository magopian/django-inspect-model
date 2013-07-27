.PHONY: test flake8 docs

bin/python:
	virtualenv . --python python2
	bin/python setup.py develop

bin/tox:
	bin/pip install tox

bin/flake8:
	bin/pip install flake8

test: bin/tox
	bin/tox

flake8: bin/flake8
	bin/flake8 inspect_model

docs:
	bin/pip install sphinx
	SPHINXBUILD=../bin/sphinx-build $(MAKE) -C docs html $^
