#!/usr/bin/env python
# -*- coding: utf-8 -*-

from inspect_model.utils import InspectModel  # noqa

pkg_resources = __import__('pkg_resources')
distribution = pkg_resources.get_distribution('django-inspect-model')

__version__ = distribution.version
