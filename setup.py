# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

import inspect_model


setup(
    name='django-inspect-model',
    version=inspect_model.__version__,
    author=u'Mathieu agopian',
    author_email='mathieu.agopian@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/magopian/django-inspect-model',
    license='BSD licence, see LICENCE file',
    description='Model inspection for Django',
    long_description=open('README.rst').read(),
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
    ],
    zip_safe=False,
)
