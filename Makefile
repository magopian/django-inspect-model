.PHONY: test flake8 docs

bin/python:
	virtualenv . --python python2
	bin/python setup.py develop

bin/django-admin.py:
	bin/pip install django

bin/flake8:
	bin/pip install flake8

test: bin/django-admin.py
	bin/django-admin.py test --settings=inspect_model.test_settings

flake8: bin/flake8
	bin/flake8 inspect_model

docs:
	bin/pip install sphinx
	SPHINXBUILD=../bin/sphinx-build $(MAKE) -C docs html $^
