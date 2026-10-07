# -*- coding: utf-8 -*-
from collective.dms.scanbehavior.behaviors.behaviors import IScanFields
from collective.dms.scanbehavior.testing import INTEGRATION
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.autoform.interfaces import IFormFieldProvider
from plone.behavior.interfaces import IBehavior
from plone.supermodel.interfaces import FIELDSETS_KEY
from Products.CMFPlone.utils import getFSVersionTuple
from zope.component import getUtility
from zope.i18n import translate
from zope.schema import Datetime
from zope.schema import getFieldsInOrder
from zope.schema import Int
from zope.schema import TextLine
from zope.schema.interfaces import TooBig
from zope.schema.interfaces import TooSmall

import datetime
import unittest


# known Plone 6 regressions (MIGRATION.md Known issues): pass on Plone 4, fail on Plone 6
plone6_regression = unittest.expectedFailure if getFSVersionTuple()[0] >= 6 else (lambda func: func)


class TestIScanFields(unittest.TestCase):

    layer = INTEGRATION

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_registration(self):
        # short name and dotted interface name (used by the imio.dms.mail types)
        for name in (
            "collective.dms.scanbehavior.behaviors.IScanFields",
            "collective.dms.scanbehavior.behaviors.behaviors.IScanFields",
        ):
            behavior = getUtility(IBehavior, name=name)
            self.assertIs(behavior.interface, IScanFields)
            self.assertEqual(behavior.title, "Scan metadata")
            self.assertEqual(translate(behavior.title, target_language="fr"), "Métadonnées de numérisation")
        self.assertTrue(IFormFieldProvider.providedBy(IScanFields))
        doc = api.content.create(container=self.portal, type="ScannedDocument", id="doc", title="Doc")
        self.assertTrue(IScanFields.providedBy(doc))

    def test_fields(self):
        fields = [
            (name, field.__class__, field.required, field.default, translate(field.title, target_language="fr"))
            for name, field in getFieldsInOrder(IScanFields)
        ]
        self.assertEqual(
            fields,
            [
                ("scan_id", TextLine, False, None, "Identifiant de scan"),
                ("version", Int, False, 0, "Version"),
                ("pages_number", Int, False, None, "Nombre de pages"),
                ("scan_date", Datetime, False, None, "Date de scan"),
                ("scan_user", TextLine, False, None, "Opérateur"),
                ("scanner", TextLine, False, None, "Scanner"),
            ],
        )
        fieldset = IScanFields.queryTaggedValue(FIELDSETS_KEY)[0]
        self.assertEqual(fieldset.__name__, "scan")
        self.assertEqual(translate(fieldset.label, target_language="fr"), "Scan")
        self.assertEqual(list(fieldset.fields), [name for name, field in getFieldsInOrder(IScanFields)])
        # default value on new content
        doc = api.content.create(container=self.portal, type="ScannedDocument", id="doc", title="Doc")
        self.assertEqual(doc.version, 0)
        self.assertIsNone(doc.scan_id)

    def test_scan_date(self):
        scan_date = IScanFields["scan_date"]
        self.assertEqual(scan_date.min, datetime.datetime(1990, 1, 1))
        # max is computed at import time: today + 7 days
        today = datetime.datetime.today()
        self.assertGreater(scan_date.max, today + datetime.timedelta(days=6))
        self.assertLessEqual(scan_date.max, today + datetime.timedelta(days=7))
        scan_date.validate(datetime.datetime(1990, 1, 1))
        scan_date.validate(today)
        self.assertRaises(TooSmall, scan_date.validate, datetime.datetime(1989, 12, 31, 23, 59))
        self.assertRaises(TooBig, scan_date.validate, today + datetime.timedelta(days=8))


class TestBehaviors(unittest.TestCase):

    layer = INTEGRATION

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_scan_id_indexer(self):
        catalog = api.portal.get_tool("portal_catalog")
        doc = api.content.create(
            container=self.portal, type="ScannedDocument", id="doc", title="Doc", scan_id="IMIO-123"
        )
        # empty values are not indexed
        api.content.create(container=self.portal, type="ScannedDocument", id="doc2", title="Doc 2")
        api.content.create(container=self.portal, type="ScannedDocument", id="doc3", title="Doc 3", scan_id="")
        self.assertEqual([b.getObject() for b in catalog(scan_id="IMIO-123")], [doc])
        self.assertEqual(tuple(catalog.uniqueValuesFor("scan_id")), ("IMIO-123",))
        # searches process the Plone 6 indexing queue, uniqueValuesFor doesn't
        doc.scan_id = "IMIO-456"
        doc.reindexObject()
        self.assertEqual([b.getObject() for b in catalog(scan_id="IMIO-456")], [doc])
        self.assertEqual(tuple(catalog.uniqueValuesFor("scan_id")), ("IMIO-456",))

    @plone6_regression
    def test_scan_id_indexer_cleared_value(self):
        """Separate method: Plone 6 regression, see MIGRATION.md Known issues."""
        catalog = api.portal.get_tool("portal_catalog")
        doc = api.content.create(
            container=self.portal, type="ScannedDocument", id="doc", title="Doc", scan_id="IMIO-123"
        )
        api.content.create(
            container=self.portal, type="ScannedDocument", id="doc2", title="Doc 2", scan_id="IMIO-456"
        )
        self.assertEqual(len(catalog(scan_id="IMIO-123")), 1)
        doc.scan_id = None
        doc.reindexObject()
        self.assertEqual(len(catalog(scan_id="IMIO-123")), 0)
        self.assertEqual(tuple(catalog.uniqueValuesFor("scan_id")), ("IMIO-456",))
