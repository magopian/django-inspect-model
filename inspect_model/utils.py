#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect


# list of methods that check everything other than attributes
ALL_BUT_ATTRIBUTES = [
    inspect.ismodule,
    inspect.isclass,
    inspect.ismethod,
    inspect.isfunction,
    inspect.isgeneratorfunction,
    inspect.isgenerator,
    inspect.istraceback,
    inspect.isframe,
    inspect.iscode,
    inspect.isroutine,
    inspect.isabstract,
    inspect.ismethoddescriptor,
    inspect.isdatadescriptor,
    inspect.isgetsetdescriptor,
    inspect.ismemberdescriptor,
]

DJANGO_GENERATED_METHODS = [
    'clean',
    'clean_fields',
    'delete',
    'full_clean',
    'save',
    'save_base',
    'validate_unique'
]

class InspectModel(object):
    def __init__(self, model):
        self.model = model
        if not inspect.isclass(model):
            self.model = model.__class__

        self.fields = self.get_fields()
        self.attributes = self.get_attributes()
        self.methods = self.get_methods()
        self.items = self.fields + self.attributes + self.methods

    def get_fields(self):
        """Return the list fo django.db.models fields"""

        opts = getattr(self.model, '_meta', None)
        if opts:
            return [f.name for f in opts.fields + opts.many_to_many]
        return []

    def get_attributes(self):
        """Return the list of class attributes which are not fields"""

        attrs = []
        for a in dir(self.model):
            if a.startswith('_') or a in self.fields:
                continue

            item = getattr(self.model, a)

            try:
                from django.db.models.manager import Manager
                if isinstance(item, Manager):
                    continue
            except:
                pass
            if any([check(item) for check in ALL_BUT_ATTRIBUTES]):
                continue

            attrs.append(a)
        return attrs

    def get_methods(self):
        """Return the list of class methods"""

        methods = []
        for m in dir(self.model):
            if m.startswith('_') or m in self.fields:
                continue
            if m in DJANGO_GENERATED_METHODS:
                continue
            if is_method_without_args(getattr(self.model, m)):
                methods.append(m)
        return methods

def is_method_without_args(func):
    """Check if func is a method callable with only one param (self)"""

    if not inspect.ismethod(func):
        return False

    args, var, named, defaults = inspect.getargspec(func)
    if defaults:
        args = args[:-len(defaults)] # args with defaults don't count
    return len(args) == 1

