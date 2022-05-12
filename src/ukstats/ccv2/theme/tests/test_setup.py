# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from ukstats.ccv2.theme.testing import (
    UKSTATS_CCV2_THEME_INTEGRATION_TESTING  # noqa: E501,
)

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that ukstats.ccv2.theme is properly installed."""

    layer = UKSTATS_CCV2_THEME_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if ukstats.ccv2.theme is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'ukstats.ccv2.theme'))

    def test_browserlayer(self):
        """Test that IUkstatsCcv2ThemeLayer is registered."""
        from ukstats.ccv2.theme.interfaces import (
            IUkstatsCcv2ThemeLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IUkstatsCcv2ThemeLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = UKSTATS_CCV2_THEME_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['ukstats.ccv2.theme'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if ukstats.ccv2.theme is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'ukstats.ccv2.theme'))

    def test_browserlayer_removed(self):
        """Test that IUkstatsCcv2ThemeLayer is removed."""
        from ukstats.ccv2.theme.interfaces import \
            IUkstatsCcv2ThemeLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IUkstatsCcv2ThemeLayer,
            utils.registered_layers())
