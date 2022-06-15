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
        blocks = {
            "1c396c10-f67e-40ba-8b63-9b8ef3cdb72d": {
                "@type": "heroHeader",
                "summary": "The UK is required to report its estimated greenhouse gas (GHG) emissions on a range of different bases to fulfil a wide range of international agreements as well as for domestic policy making purposes.",
                "title": "Measuring greenhouse gas emissions",
            },
            "5e32f9d6-9647-4b6d-a866-b03aa9ec5b26": {
                "@type": "columnsBlock",
                "data": {
                    "blocks": {
                        "0d982eaa-0c91-4447-b61b-a1e4ee20e9c2": {
                            "blocks": {
                                "0e5927c5-2e92-48cf-8fb5-573da68d4511": {
                                    "@type": "dashboardTile",
                                    "topic": "Climate and weather",
                                    "title": "Annual mean temperature (\u00b0C) for the UK",
                                },
                                "ebcd7f8b-1ec5-4423-885e-e1824c28ec3c": {
                                    "@type": "slate"
                                },
                            },
                            "blocks_layout": {
                                "items": [
                                    "0e5927c5-2e92-48cf-8fb5-573da68d4511",
                                    "ebcd7f8b-1ec5-4423-885e-e1824c28ec3c",
                                ]
                            },
                        },
                        "0e3ef5e8-3806-4217-b539-cc71482effce": {
                            "blocks": {
                                "b6b5ff1f-96cf-44ae-a9dc-e3d6e9341450": {
                                    "@type": "dashboardTile",
                                    "topic": "Emissions",
                                    "title": "Greenhouse gas emissions (Mt CO2e)",
                                },
                                "688fd38c-8228-4be4-a27f-4f8c48078155": {
                                    "@type": "slate"
                                },
                            },
                            "blocks_layout": {
                                "items": [
                                    "b6b5ff1f-96cf-44ae-a9dc-e3d6e9341450",
                                    "688fd38c-8228-4be4-a27f-4f8c48078155",
                                ]
                            },
                        },
                        "4cb32900-e164-4e7c-a0f7-46e03a86cc9e": {
                            "blocks": {
                                "d974efdc-e9ae-4c89-a5ee-217886bc91a2": {
                                    "@type": "dashboardTile",
                                    "topic": "Drivers",
                                    "title": "Fossil fuel energy use (Mtoe) for the four highest sectors in the UK",
                                },
                                "2d1d85d9-2432-414b-9ebc-41c4d0885712": {
                                    "@type": "slate"
                                },
                            },
                            "blocks_layout": {
                                "items": [
                                    "d974efdc-e9ae-4c89-a5ee-217886bc91a2",
                                    "2d1d85d9-2432-414b-9ebc-41c4d0885712",
                                ]
                            },
                        },
                    },
                    "blocks_layout": {
                        "items": [
                            "0d982eaa-0c91-4447-b61b-a1e4ee20e9c2",
                            "0e3ef5e8-3806-4217-b539-cc71482effce",
                            "4cb32900-e164-4e7c-a0f7-46e03a86cc9e",
                        ]
                    },
                },
                "gridSize": 12,
                "gridCols": ["oneThird", "oneThird", "oneThird"],
            },
            "874c31fc-01b9-4d19-8ceb-66e93686ed24": {
                "@type": "columnsBlock",
                "data": {
                    "blocks": {
                        "088756e2-a183-4ea7-866f-35fffcf3a453": {
                            "blocks": {
                                "9b1ac3c4-5a7a-4e04-a772-96ea053e8562": {
                                    "@type": "dashboardTile",
                                    "topic": "Impacts",
                                    "title": "Ecological status of surface waters in England, 2019",
                                },
                                "74559b24-2586-4682-b5d0-972b8ae43719": {
                                    "@type": "slate"
                                },
                            },
                            "blocks_layout": {
                                "items": [
                                    "9b1ac3c4-5a7a-4e04-a772-96ea053e8562",
                                    "74559b24-2586-4682-b5d0-972b8ae43719",
                                ]
                            },
                        },
                        "bee4bcab-ac18-4af0-ae8c-5f13270a441d": {
                            "blocks": {
                                "b32a4481-1694-4202-9a75-1b68d13f7dab": {
                                    "@type": "dashboardTile",
                                    "topic": "Mitigation",
                                    "title": "Renewable energy share in total energy consumption, UK, 2020",
                                },
                                "c49a4c55-e28f-469f-b0b5-cf0e11e3c208": {
                                    "@type": "slate"
                                },
                            },
                            "blocks_layout": {
                                "items": [
                                    "b32a4481-1694-4202-9a75-1b68d13f7dab",
                                    "c49a4c55-e28f-469f-b0b5-cf0e11e3c208",
                                ]
                            },
                        },
                        "6a8f62cd-d6d2-4277-bfed-c35e04a81137": {
                            "blocks": {
                                "93a12089-b230-4d41-b911-415f03a00ee1": {
                                    "@type": "dashboardTile",
                                    "topic": "Adaptation",
                                    "title": "New planting of UK woodlands, thousand hectares",
                                },
                                "d6b358d4-6c7c-4851-9c94-7949d8575956": {
                                    "@type": "slate"
                                },
                            },
                            "blocks_layout": {
                                "items": [
                                    "93a12089-b230-4d41-b911-415f03a00ee1",
                                    "d6b358d4-6c7c-4851-9c94-7949d8575956",
                                ]
                            },
                        },
                    },
                    "blocks_layout": {
                        "items": [
                            "088756e2-a183-4ea7-866f-35fffcf3a453",
                            "bee4bcab-ac18-4af0-ae8c-5f13270a441d",
                            "6a8f62cd-d6d2-4277-bfed-c35e04a81137",
                        ]
                    },
                },
                "gridSize": 12,
                "gridCols": ["oneThird", "oneThird", "oneThird"],
            },
            "e03c688a-6e8e-4405-8e60-2c89780274a5": {
                "@type": "title"
            },
            "4e16924c-5bd8-4cd9-82ec-6470d10f5ca4": {
                "@type": "columnsBlock",
                "block_title": "Columns",
                "data": {
                    "blocks": {
                        "846d9bfb-9253-489b-bdfa-63d415264ea8": {
                            "blocks": {
                                "aae2a30b-a08f-41c1-946f-26edd8a4e748": {"@type": "slate"}
                            },
                            "blocks_layout": {
                                "items": ["aae2a30b-a08f-41c1-946f-26edd8a4e748"]
                            }
                        },
                        "0100b4a0-fa99-4076-8a2e-123d554e455f": {
                            "blocks": {
                                "de28e1f3-8811-4b0c-a53b-480bfa98d26a": {
                                    "@type": "html", "html": "<h2 class=\"cc-related-links\">Related Links</h2>"
                                },
                                "8ea48dad-d359-4512-a52e-16757aaa39fb": {
                                    "@type": "listing",
                                    "query": [],
                                    "block": "8ea48dad-d359-4512-a52e-16757aaa39fb",
                                    "variation": "default",
                                    "querystring": {
                                        "query": [{
                                            "i": "portal_type",
                                            "o": "plone.app.querystring.operation.selection.any",
                                            "v": ["Link"]
                                        }, {
                                            "i": "path",
                                            "o": "plone.app.querystring.operation.string.absolutePath",
                                            "v": "/references"
                                        }], "sort_order": "ascending"
                                    }
                                }
                            },
                            "blocks_layout": {
                                "items": [
                                    "de28e1f3-8811-4b0c-a53b-480bfa98d26a",
                                    "8ea48dad-d359-4512-a52e-16757aaa39fb"
                                ]
                            },
                            "selected": "8ea48dad-d359-4512-a52e-16757aaa39fb"
                        }
                    },
                    "blocks_layout": {
                        "items": [
                            "846d9bfb-9253-489b-bdfa-63d415264ea8",
                            "0100b4a0-fa99-4076-8a2e-123d554e455f",
                        ]
                    },
                },
                "gridSize": 12,
                "gridCols": ["twoThirds", "oneThird"]
            },
        }
        blocks_layout = {
            "items": [
                "1c396c10-f67e-40ba-8b63-9b8ef3cdb72d",
                "5e32f9d6-9647-4b6d-a866-b03aa9ec5b26",
                "874c31fc-01b9-4d19-8ceb-66e93686ed24",
                "e03c688a-6e8e-4405-8e60-2c89780274a5",
                "4e16924c-5bd8-4cd9-82ec-6470d10f5ca4"
            ]
        }

        portal.setTitle("Climate Change Statistics")
        portal.setDescription(
            "A prototype portal for data and insights on climate change."
        )

        logger.info("Creating default homepage in Plone site root - not PAM enabled")

    # Common part
    if not getattr(portal, "blocks", False):
        portal.manage_addProperty("blocks", json.dumps(blocks), "string")

    if not getattr(portal, "blocks_layout", False):
        portal.manage_addProperty(
            "blocks_layout", json.dumps(blocks_layout), "string"
        )  # noqa
