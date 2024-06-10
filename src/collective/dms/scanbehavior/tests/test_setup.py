# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from collective.dms.scanbehavior.testing import IntegrationTestCase
from plone.base.utils import get_installer


class TestInstall(IntegrationTestCase):
    """Test installation of collective.dms.scanbehavior into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.installer = get_installer(self.portal, self.request)

    def test_product_installed(self):
        """Test if collective.dms.scanbehavior is installed."""
        self.assertTrue(
            self.installer.is_product_installed("collective.dms.scanbehavior")
        )

    def test_uninstall(self):
        """Test if collective.dms.scanbehavior is cleanly uninstalled."""
        self.installer.uninstall_product("collective.dms.scanbehavior")
        self.assertFalse(
            self.installer.is_product_installed("collective.dms.scanbehavior")
        )

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that ICollectiveDmsScanbehaviorLayer is registered."""
        from collective.dms.scanbehavior.interfaces import ICollectiveDmsScanbehaviorLayer
        from plone.browserlayer import utils

        self.assertIn(ICollectiveDmsScanbehaviorLayer, utils.registered_layers())
