# -*- coding: utf-8 -*-
from collective.dms.scanbehavior.behaviors.behaviors import IScanFields
from collective.dms.scanbehavior.behaviors.behaviors import scan_id_indexer
from collective.dms.scanbehavior.testing import INTEGRATION
from Products.ZCatalog.ZCatalogIndexes import _marker
from zope.interface import alsoProvides
from zope.schema import getFieldsInOrder

import datetime
import unittest


class Dummy(object):
    pass


class TestBehaviorSchema(unittest.TestCase):
    layer = INTEGRATION

    def test_scan_date(self):
        fields = dict(getFieldsInOrder(IScanFields))
        scan_date = fields["scan_date"]
        self.assertEqual(scan_date.min, datetime.datetime(1990, 1, 1))
        today = datetime.datetime.today()
        self.assertGreaterEqual(scan_date.max, today)
        self.assertLessEqual(scan_date.max, today + datetime.timedelta(days=8))


class TestIndexer(unittest.TestCase):
    layer = INTEGRATION

    def make_obj(self, **attrs):
        obj = Dummy()
        for k, v in list(attrs.items()):
            setattr(obj, k, v)
        alsoProvides(obj, IScanFields)
        return obj

    def test_scan_id(self):
        obj = self.make_obj(scan_id="ABC-123")
        self.assertEqual(scan_id_indexer(obj)(), "ABC-123")
        obj = self.make_obj()
        self.assertIs(scan_id_indexer(obj)(), _marker)
        obj = self.make_obj(scan_id="")
        self.assertIs(scan_id_indexer(obj)(), _marker)
        obj = self.make_obj(scan_id=None)
        self.assertIs(scan_id_indexer(obj)(), _marker)
