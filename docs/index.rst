.. Django-inspect-model documentation master file, created by
   sphinx-quickstart on Wed Jun  1 14:29:39 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django-inspect-model
====================

Django-inspect-model is a model inspection utility for Django. It allows you to
easily list all available "items" on a model, and get their value.

An item is either:

* a django field (standard field or relation field)
* a standard attribute
* a method that only takes one attribute: 'self'

The code is generic enough to be applied on just any python object, so Django
isn't a requirement. However, it was tailored towards Django models.

The source code is `available on Github`_ under the 3-clause BSD licence.

.. _available on Github: https://github.com/magopian/django-inspect-model


Installation
------------

::

    pip install django-inspect-model


Usage
-----

Instantiate ``inspect_model.InspectModel`` with your model class or instance, and profit.

:: 

    >>> from django.contrib.comments.models import Comment
    >>> from inspect_model import InspectModel
    >>> im = InspectModel(Comment)
    >>> im.fields
    ['id', 'content_type', 'object_pk', 'site', 'user', 'user_name',
    'user_email', 'user_url', 'comment', 'submit_date', 'ip_address',
    'is_public', 'is_removed']
    >>> im.attributes
    []
    >>> im.methods
    ['get_as_text', 'get_content_object_url']
    >>> im.items
    ['id', 'content_type', 'object_pk', 'site', 'user', 'user_name',
    'user_email', 'user_url', 'comment', 'submit_date', 'ip_address',
    'is_public', 'is_removed', 'get_as_text', 'get_content_object_url']

.. toctree::
   :maxdepth: 2


Changes
-------

* 0.2: added self.items
* 0.1: initial version


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

