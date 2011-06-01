Django-inspect-model
====================

Django-inspect-model is a model inspection utility for Django. It allows you to
easily list all available "items" on a model, and get their value.

An item is either:
* a django field
* a standard attribute
* a method that only takes one attribute: 'self'
* a foreign key
* an item on the related model (FK or one-to-one)
* a many-to-many relation

* Authors: see AUTHORS
* Licence: BSD
* Compatibility: Django 1.3+
* Requirements: none
* Documentation: http://django-inspect-model.readthedocs.org/en/latest/
