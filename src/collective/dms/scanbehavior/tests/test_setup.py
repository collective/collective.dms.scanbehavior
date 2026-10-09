# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from collective.dms.scanbehavior.interfaces import ICollectiveDmsScanbehaviorLayer
from collective.dms.scanbehavior.testing import IntegrationTestCase
from plone import api
from plone.browserlayer import utils

import unittest


try:
    from plone.base.utils import get_installer
except ImportError:  # Plone 4: portal_quickinstaller, no uninstall profile
    get_installer = None


class TestInstall(IntegrationTestCase):
    """Test installation of collective.dms.scanbehavior into Plone."""

    def test_default_profile(self):
        setup = api.portal.get_tool("portal_setup")
        self.assertEqual(setup.getLastVersionForProfile("collective.dms.scanbehavior:default"), ("4",))
        self.assertIn(ICollectiveDmsScanbehaviorLayer, utils.registered_layers())
        catalog = api.portal.get_tool("portal_catalog")
        self.assertIn("scan_id", catalog.indexes())
        self.assertEqual(catalog.Indexes["scan_id"].meta_type, "FieldIndex")
        self.assertNotIn("scan_id", catalog.schema())

    @unittest.skipIf(get_installer is None, "uninstall profile added on Plone 6")
    def test_uninstall_profile(self):
        installer = get_installer(self.portal, self.layer["request"])
        self.assertTrue(installer.is_product_installed("collective.dms.scanbehavior"))
        installer.uninstall_product("collective.dms.scanbehavior")
        self.assertFalse(installer.is_product_installed("collective.dms.scanbehavior"))
        self.assertNotIn(ICollectiveDmsScanbehaviorLayer, utils.registered_layers())
        self.assertNotIn("scan_id", api.portal.get_tool("portal_catalog").indexes())
