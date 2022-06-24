# -*- coding: utf-8 -*-
import json

import logging

from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFPlone.utils import get_installer
from kitconcept.volto.setuphandlers import (
    enable_content_type,
    add_behavior,
    default_lrf_home,
)
from plone import api
from zope.interface import implementer

from importlib import resources
from . import content

logger = logging.getLogger("ukstats.ccv2.theme")


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "ukstats.ccv2.theme:uninstall",
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def import_initial_content(context, default_home=default_lrf_home):
    """This method allows to pass a dict with the homepage blocks and blocks_layout keys"""
    portal = api.portal.get()
    # Test for PAM installed
    try:
        is_pam_installed = get_installer(portal, context.REQUEST).isProductInstalled(
            "plone.app.multilingual"
        )
    except:  # noqa
        is_pam_installed = get_installer(portal, context.REQUEST).is_product_installed(
            "plone.app.multilingual"
        )

    if is_pam_installed:
        # Make sure that the LRFs have the blocks enabled
        add_behavior("LRF", "volto.blocks")

        for lang in api.portal.get_registry_record("plone.available_languages"):
            # Do not write them if there are blocks set already
            # Get the attr first, in case it's not there yet (error in docker image)
            if getattr(portal[lang], "blocks", {}) == {} and (
                getattr(portal[lang], "blocks_layout", {}).get("items") is None
                or getattr(portal[lang], "blocks_layout", {}).get("items") == []
            ):
                logger.info(
                    "Creating default homepage for {} - PAM enabled".format(lang)
                )
                portal[lang].blocks = default_home["blocks"]
                portal[lang].blocks_layout = default_home["blocks_layout"]

    else:
        create_root_homepage(context)


def create_root_homepage(context, default_home=None):
    """It takes a default object:
    {
        "title": "The title",
        "description": "The description",
        "blocks": {...},
        "blocks_layout": [...]
    }
    and sets it as default page in the Plone root object.
    """

    portal = api.portal.get()

    if default_home:
        blocks = default_home["blocks"]
        blocks_layout = default_home["blocks_layout"]
        portal.setTitle(default_home["title"])
        portal.setDescription(default_home["description"])

        logger.info(
            "Creating custom default homepage in Plone site root - not PAM enabled"
        )
    else:
        blocks = resources.read_text(content, 'front_blocks.json')
        blocks_layout = resources.read_text(content, 'front_blocks_layout.json')

        portal.setTitle("Climate Change Statistics")
        portal.setDescription(
            "A prototype portal for data and insights on climate change."
        )

        logger.info("Creating default homepage in Plone site root - not PAM enabled")

    # Common part
    if not getattr(portal, "blocks", False):
        portal.manage_addProperty("blocks", blocks, "string")

    if not getattr(portal, "blocks_layout", False):
        portal.manage_addProperty(
            "blocks_layout", blocks_layout, "string"
        )  # noqa
