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

        self.fields = []  # standard django model fields
        self.relation_fields = []  # OneToOne or ForeignKey fields
        self.many_fields = []  # ManyToMany fields
        self.attributes = []  # standard python class attributes
        self.methods = []  # standard python class methods
        self.items = []  # groups all of the above for convenience
        self.properties = []  # properties

        self.update_fields()
        self.update_attributes()
        self.update_methods()
        self.update_properties()

    def update_fields(self):
        """Set the list of django.db.models fields

        Three different types of fields:
        * standard model fields: Char, Integer...
        * relation fields: OneToOne (back and forth) and ForeignKey
        * many fields: ManyToMany (back and forth)

        """
        self.fields = []
        self.relation_fields = []
        self.many_fields = []
        opts = getattr(self.model, '_meta', None)
        if opts:
            for f in opts.get_all_field_names():
                field, model, direct, m2m = opts.get_field_by_name(f)
                name = field.name
                if not direct:  # relation or many field from another model
                    name = field.get_accessor_name()
                    field = field.field
                    if field.rel.multiple:  # m2m or fk to this model
                        self.add_item(name, self.many_fields)
                    else:  # one to one
                        self.add_item(name, self.relation_fields)
                else:  # relation, many or field from this model
                    if field.rel:  # relation or many field
                        if hasattr(field.rel, 'through'):  # m2m
                            self.add_item(name, self.many_fields)
                        else:
                            self.add_item(name, self.relation_fields)
                    else:  # standard field
                        self.add_item(name, self.fields)

    def update_attributes(self):
        """Return the list of class attributes which are not fields"""
        self.attributes = []
        for a in dir(self.model):
            if a.startswith('_') or a in self.fields:
                continue
            item = getattr(self.model, a, None)
            try:
                from django.db.models.manager import Manager
                if isinstance(item, Manager):
                    continue
            except:
                pass
            if any([check(item) for check in ALL_BUT_ATTRIBUTES]):
                continue
            self.add_item(a, self.attributes)

    def update_methods(self):
        """Return the list of class methods"""
        self.methods = []
        for m in dir(self.model):
            if m.startswith('_') or m in self.fields:
                continue
            if m in DJANGO_GENERATED_METHODS:
                continue
            if is_method_without_args(getattr(self.model, m, None)):
                self.add_item(m, self.methods)

    def update_properties(self):
        """Return the list of properties"""
        self.properties = []
        for name in dir(self.model):
            if isinstance(getattr(self.model, name, None), property):
                self.add_item(name, self.properties)

    def add_item(self, item, item_type):
        item_type.append(item)
        # we only want each item once
        s = set(self.items)
        s.add(item)
        self.items = list(sorted(s))


def is_method_without_args(func):
    """Check if func is a method callable with only one param (self)"""
    if not inspect.isfunction(func) and not inspect.ismethod(func):
        return False
    args, var, named, defaults = inspect.getargspec(func)
    if defaults:
        args = args[:-len(defaults)]  # args with defaults don't count
    return len(args) == 1
