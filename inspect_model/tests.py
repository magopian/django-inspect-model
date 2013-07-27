#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.test import TestCase
from inspect_model import InspectModel


class OtherModel(models.Model):
    name = models.CharField(max_length=10, blank=True)


class LinkedModel(models.Model):
    name = models.CharField(max_length=10, blank=True)
    toinspect = models.OneToOneField('ModelToInspect', blank=True, null=True)


class ModelToInspect(models.Model):
    # "standard" fields
    #id = models.AutoField(primary_key=True)
    bigint = models.BigIntegerField(blank=True, null=True)
    boolean = models.BooleanField(default=True)
    char = models.CharField(max_length=10, blank=True)
    comma = models.CommaSeparatedIntegerField(max_length=10, blank=True)
    date = models.DateField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    decimal = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    email = models.EmailField(max_length=75, blank=True)
    filefield = models.FileField(upload_to='media', max_length=100, blank=True)
    filepath = models.FilePathField(path="/tmp", blank=True)
    floatfield = models.FloatField(blank=True, null=True)
    # do not test image, as it needs the PIL or Pillow dependency
    #image = models.ImageField(upload_to='media', blank=True)
    intfield = models.IntegerField(blank=True, null=True)
    ipaddress = models.IPAddressField(blank=True, null=True)
    nullboolean = models.NullBooleanField(blank=True, null=True)
    positiveint = models.PositiveIntegerField(blank=True, null=True)
    positivesmallint = models.PositiveSmallIntegerField(blank=True, null=True)
    slug = models.SlugField(max_length=50, blank=True)
    smallint = models.SmallIntegerField(blank=True, null=True)
    text = models.TextField(blank=True)
    time = models.TimeField(blank=True, null=True)
    url = models.URLField(blank=True)
    # relationship fields
    foreign = models.ForeignKey(OtherModel, blank=True, null=True)
    many = models.ManyToManyField(OtherModel, related_name='many')
    one = models.OneToOneField(
        OtherModel,
        related_name='one',
        blank=True,
        null=True)

    # class attributes
    attribute = 'foo'
    _hidden = 'bar'

    # class methods that can be called "as is"
    def __unicode__(self):  # implicit calling by printing
        return 'model to inspect'

    def method_one_arg(self):
        return 'bar'

    def method_args_with_defaults(self, foo='bar'):
        return foo

    # class methods that can't be called "as is"
    def method_args(self, foo):
        return 'bar'

    def method_args_mixed(self, foo, bar='baz'):
        return 'bar'

    def _hidden_method(self):
        return 'bar'

    @property
    def a_property(self):
        return 'bar'


class ManyRelatedModel(models.Model):
    name = models.CharField(max_length=10, blank=True)
    many = models.ManyToManyField(ModelToInspect)


class ModelInspectTest(TestCase):

    def setUp(self):
        self.om = OtherModel.objects.create()
        self.mti = ModelToInspect.objects.create(foreign=self.om, one=self.om)
        self.mti.many.add(self.om)
        self.lm = LinkedModel.objects.create(toinspect=self.mti)

        self.im = InspectModel(self.mti)

    def test_fields(self):
        # 21 fields + the automatically generated id field
        self.assertEqual(len(self.im.fields), 22)
        self.assertFalse('attribute' in self.im.fields)
        self.assertFalse('_hidden' in self.im.fields)

    def test_relation_fields(self):
        # 2 'local' fields + a OneToOneField on LinkedModel
        self.assertEqual(len(self.im.relation_fields), 3)
        self.assertTrue('foreign' in self.im.relation_fields)
        self.assertTrue('linkedmodel' in self.im.relation_fields)
        self.assertTrue('one' in self.im.relation_fields)
        self.assertFalse('many' in self.im.relation_fields)

    def test_many_fields(self):
        # 1 local + 1 on the ManyRelatedModel
        self.assertEqual(len(self.im.many_fields), 2)
        self.assertTrue('manyrelatedmodel_set' in self.im.many_fields)
        self.assertTrue('many' in self.im.many_fields)
        self.assertFalse('one' in self.im.many_fields)

    def test_attributes(self):
        self.assertEqual(len(self.im.attributes), 1)

    def test_properties(self):
        self.assertEqual(len(self.im.properties), 2)

    def test_methods(self):
        self.assertEqual(len(self.im.methods), 2)
        self.assertFalse('method_args' in self.im.methods)
        self.assertFalse('_hidden_method' in self.im.methods)

    def test_items(self):
        # make sure all the items are indeed part of a ModelToInspect instance
        items = [getattr(self.mti, f) for f in self.im.items]
        self.assertEqual(len(items), 32)

    def test_multiple_calls(self):
        """Multiple calls to get_FOO"""
        self.im.update_fields()
        self.assertEqual(len(self.im.fields), 22)
        self.assertEqual(len(self.im.relation_fields), 3)
        self.assertEqual(len(self.im.many_fields), 2)
        self.im.update_attributes()
        self.assertEqual(len(self.im.attributes), 1)
        self.im.update_methods()
        self.assertEqual(len(self.im.methods), 2)
        self.assertEqual(len(self.im.items), 32)
