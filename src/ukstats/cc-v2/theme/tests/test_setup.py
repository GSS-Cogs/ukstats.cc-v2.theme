# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from ukstats.cc-v2.theme.testing import (
    UKSTATS_CC-V2_THEME_INTEGRATION_TESTING  # noqa: E501,
)

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that ukstats.cc-v2.theme is properly installed."""

    layer = UKSTATS_CC-V2_THEME_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if ukstats.cc-v2.theme is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'ukstats.cc-v2.theme'))

    def test_browserlayer(self):
        """Test that IUkstatsCc-V2ThemeLayer is registered."""
        from ukstats.cc-v2.theme.interfaces import (
            IUkstatsCc-V2ThemeLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IUkstatsCc-V2ThemeLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = UKSTATS_CC-V2_THEME_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['ukstats.cc-v2.theme'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if ukstats.cc-v2.theme is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'ukstats.cc-v2.theme'))

    def test_browserlayer_removed(self):
        """Test that IUkstatsCc-V2ThemeLayer is removed."""
        from ukstats.cc-v2.theme.interfaces import \
            IUkstatsCc-V2ThemeLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IUkstatsCc-V2ThemeLayer,
            utils.registered_layers())
