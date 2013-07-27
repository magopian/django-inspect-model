Django-inspect-model
====================

Django-inspect-model is a model inspection utility for Django. It allows you to
easily list all available "items" on a model, and get their value.

An item is either:

* a django field (standard field or relation field)
* a standard attribute
* a method that only takes one attribute: 'self'
* a property

The code is generic enough to be applied on just any python object, so Django
isn't a requirement. However, it was tailored towards Django models.

Usage
-----

Instantiate ``inspect_model.InspectModel`` with your model class or instance, and profit.

::

    >>> from django.contrib.comments.models import Comment
    >>> from inspect_model import InspectModel
    >>> im = InspectModel(Comment)
    >>> im.fields
    ['comment', 'id', 'ip_address', 'is_public', 'is_removed', 'object_pk',
    'submit_date', 'user_email', 'user_name', 'user_url']
    >>> im.relation_fields
    ['content_type', 'site', 'user']
    >>> im.many_fields
    ['flags']
    >>> im.attributes
    []
    >>> im.methods
    ['get_as_text', 'get_content_object_url']
    >>> im.properties
    ['email', 'name', 'pk', 'url', 'userinfo']
    >>> im.items
    ['comment', 'content_type', 'email', 'flags', 'get_as_text',
    'get_content_object_url', u'id', 'ip_address', 'is_public', 'is_removed',
    'name', 'object_pk', 'pk', 'site', 'submit_date', 'url', 'user',
    'user_email', 'user_name', 'user_url', 'userinfo']

* Authors: https://github.com/magopian/django-inspect-model/graphs/contributors
* Licence: BSD
* Compatibility: Python 2.7, Django 1.3+
* Requirements: none
* Documentation: http://django-inspect-model.readthedocs.org/en/latest/
