# -*- coding: utf-8 -*-
"""Base module for unittesting."""

from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import zope

import collective.dms.scanbehavior
import unittest


class CollectiveDmsScanbehaviorLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        self.loadZCML(package=collective.dms.scanbehavior, name="testing.zcml")
        zope.installProduct(app, "collective.dms.scanbehavior")

    def setUpPloneSite(self, portal):
        """Install the testing profile: default profile + ScannedDocument test type."""
        applyProfile(portal, "collective.dms.scanbehavior:testing")

    def tearDownZope(self, app):
        """Tear down Zope."""
        zope.uninstallProduct(app, "collective.dms.scanbehavior")


FIXTURE = CollectiveDmsScanbehaviorLayer(name="FIXTURE")


INTEGRATION = IntegrationTesting(bases=(FIXTURE,), name="INTEGRATION")


ACCEPTANCE = FunctionalTesting(
    bases=(FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, zope.WSGI_SERVER_FIXTURE),
    name="ACCEPTANCE",
)


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION

    def setUp(self):
        super(IntegrationTestCase, self).setUp()
        self.portal = self.layer["portal"]
