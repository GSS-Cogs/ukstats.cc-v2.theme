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
                                    "title": "Annual mean temperature (\u00b0C) for the UK",
                                    "topic": "Climate and weather",
                                    "data_source": [
                                        {
                                            "@id": "/overview-data/tile-uk-annual-mean-temperature",
                                            "@type": "sparql_dataconnector",
                                            "CreationDate": "2022-05-18T08:23:07+00:00",
                                            "Creator": "aa750921-8eed-4a64-9f39-f1f7a33027c7",
                                            "Date": "2022-05-18T13:13:18+00:00",
                                            "Description": "",
                                            "EffectiveDate": "2022-05-18T13:13:18+00:00",
                                            "ExpirationDate": "None",
                                            "ModificationDate": "2022-06-15T21:06:58+00:00",
                                            "Subject": [],
                                            "Title": "Tile; SparkLine; UK annual mean temperature",
                                            "Type": "SPARQL Data Connector",
                                            "UID": "2b4bab1f95f74e68a44251b049c7b65a",
                                            "author_name": None,
                                            "cmf_uid": None,
                                            "commentators": [],
                                            "created": "2022-05-18T08:23:07+00:00",
                                            "description": "",
                                            "effective": "2022-05-18T13:13:18+00:00",
                                            "end": None,
                                            "exclude_from_nav": False,
                                            "expires": "2499-12-31T00:00:00+00:00",
                                            "getIcon": None,
                                            "getId": "tile-uk-annual-mean-temperature",
                                            "getObjSize": "0 KB",
                                            "getPath": "/Plone/overview-data/tile-uk-annual-mean-temperature",
                                            "getRemoteUrl": None,
                                            "getURL": "http://climate-change.data.gov.uk/api/overview-data/tile-uk-annual-mean-temperature",
                                            "hasPreviewImage": None,
                                            "head_title": None,
                                            "id": "tile-uk-annual-mean-temperature",
                                            "in_response_to": None,
                                            "is_folderish": True,
                                            "last_comment_date": None,
                                            "lead_image": None,
                                            "listCreators": [
                                                "aa750921-8eed-4a64-9f39-f1f7a33027c7"
                                            ],
                                            "location": None,
                                            "meta_type": "Dexterity Container",
                                            "mime_type": "text/plain",
                                            "modified": "2022-06-15T21:06:58+00:00",
                                            "nav_title": None,
                                            "portal_type": "sparql_dataconnector",
                                            "review_state": "published",
                                            "start": None,
                                            "sync_uid": None,
                                            "title": "Tile; SparkLine; UK annual mean temperature",
                                            "total_comments": 0
                                        }
                                    ],
                                    "vis_type": "spark_line"
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
                                "688fd38c-8228-4be4-a27f-4f8c48078155": {
                                    "@type": "slate"
                                },
                                "b6b5ff1f-96cf-44ae-a9dc-e3d6e9341450": {
                                    "@type": "dashboardTile",
                                    "topic": "Emissions",
                                    "title": "Greenhouse gas emissions (Mt CO2e)",
                                    "data_source": [
                                        {
                                            "@id": "/overview-data/tile-sparkline-greenhouse-gas-emissions",
                                            "@type": "sparql_dataconnector",
                                            "CreationDate": "2022-06-08T13:02:18+00:00",
                                            "Creator": "2bdc1d87-83ae-4549-8ebf-ffdd7eb572ee",
                                            "Date": "2022-06-08T13:04:00+00:00",
                                            "Description": "",
                                            "EffectiveDate": "2022-06-08T13:04:00+00:00",
                                            "ExpirationDate": "None",
                                            "ModificationDate": "2022-06-15T21:06:59+00:00",
                                            "Subject": [],
                                            "Title": "Tile; Sparkline; Greenhouse Gas Emissions",
                                            "Type": "SPARQL Data Connector",
                                            "UID": "fa8d1afba4574c22a70767000fdc52e7",
                                            "author_name": None,
                                            "cmf_uid": None,
                                            "commentators": [],
                                            "created": "2022-06-08T13:02:18+00:00",
                                            "description": "",
                                            "effective": "2022-06-08T13:04:00+00:00",
                                            "end": None,
                                            "exclude_from_nav": False,
                                            "expires": "2499-12-31T00:00:00+00:00",
                                            "getIcon": None,
                                            "getId": "tile-sparkline-greenhouse-gas-emissions",
                                            "getObjSize": "0 KB",
                                            "getPath": "/Plone/overview-data/tile-sparkline-greenhouse-gas-emissions",
                                            "getRemoteUrl": None,
                                            "getURL": "http://climate-change.data.gov.uk/api/overview-data/tile-sparkline-greenhouse-gas-emissions",
                                            "hasPreviewImage": None,
                                            "head_title": None,
                                            "id": "tile-sparkline-greenhouse-gas-emissions",
                                            "in_response_to": None,
                                            "is_folderish": True,
                                            "last_comment_date": None,
                                            "lead_image": None,
                                            "listCreators": [
                                                "2bdc1d87-83ae-4549-8ebf-ffdd7eb572ee"
                                            ],
                                            "location": None,
                                            "meta_type": "Dexterity Container",
                                            "mime_type": "text/plain",
                                            "modified": "2022-06-15T21:06:59+00:00",
                                            "nav_title": None,
                                            "portal_type": "sparql_dataconnector",
                                            "review_state": "published",
                                            "start": None,
                                            "sync_uid": None,
                                            "title": "Tile; Sparkline; Greenhouse Gas Emissions",
                                            "total_comments": 0
                                        }
                                    ],
                                    "vis_type": "spark_line"
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
                                "2d1d85d9-2432-414b-9ebc-41c4d0885712": {
                                    "@type": "slate"
                                },
                                "d974efdc-e9ae-4c89-a5ee-217886bc91a2": {
                                    "@type": "dashboardTile",
                                    "title": "Fossil fuel energy use (Mtoe) for the four highest sectors in the UK",
                                    "topic": "Drivers",
                                    "data_source": [
                                        {
                                            "@id": "/overview-data/use-of-carbon-based-fuels-by-industry-1990-to-2019",
                                            "@type": "sparql_dataconnector",
                                            "CreationDate": "2022-05-18T08:23:07+00:00",
                                            "Creator": "aa750921-8eed-4a64-9f39-f1f7a33027c7",
                                            "Date": "2022-05-18T13:13:18+00:00",
                                            "Description": "Aggregated to match the totals here: https://www.ons.gov.uk/economy/environmentalaccounts/datasets/ukenvironmentalaccountsfuelusebytypeandindustry",
                                            "EffectiveDate": "2022-05-18T13:13:18+00:00",
                                            "ExpirationDate": "None",
                                            "ModificationDate": "2022-06-15T21:06:58+00:00",
                                            "Subject": [],
                                            "Title": "Tile; SparkLine; Use of carbon based fuels by industry, 1990 to 2019",
                                            "Type": "SPARQL Data Connector",
                                            "UID": "c064d3c42ed64d33a91cc65dd44b4a70",
                                            "author_name": None,
                                            "cmf_uid": None,
                                            "commentators": [],
                                            "created": "2022-05-18T08:23:07+00:00",
                                            "description": "Aggregated to match the totals here: https://www.ons.gov.uk/economy/environmentalaccounts/datasets/ukenvironmentalaccountsfuelusebytypeandindustry",
                                            "effective": "2022-05-18T13:13:18+00:00",
                                            "end": None,
                                            "exclude_from_nav": False,
                                            "expires": "2499-12-31T00:00:00+00:00",
                                            "getIcon": None,
                                            "getId": "use-of-carbon-based-fuels-by-industry-1990-to-2019",
                                            "getObjSize": "0 KB",
                                            "getPath": "/Plone/overview-data/use-of-carbon-based-fuels-by-industry-1990-to-2019",
                                            "getRemoteUrl": None,
                                            "getURL": "http://climate-change.data.gov.uk/api/overview-data/use-of-carbon-based-fuels-by-industry-1990-to-2019",
                                            "hasPreviewImage": None,
                                            "head_title": None,
                                            "id": "use-of-carbon-based-fuels-by-industry-1990-to-2019",
                                            "in_response_to": None,
                                            "is_folderish": True,
                                            "last_comment_date": None,
                                            "lead_image": None,
                                            "listCreators": [
                                                "aa750921-8eed-4a64-9f39-f1f7a33027c7"
                                            ],
                                            "location": None,
                                            "meta_type": "Dexterity Container",
                                            "mime_type": "text/plain",
                                            "modified": "2022-06-15T21:06:58+00:00",
                                            "nav_title": None,
                                            "portal_type": "sparql_dataconnector",
                                            "review_state": "published",
                                            "start": None,
                                            "sync_uid": None,
                                            "title": "Tile; SparkLine; Use of carbon based fuels by industry, 1990 to 2019",
                                            "total_comments": 0
                                        }
                                    ],
                                    "vis_type": "spark_line"
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
                                "74559b24-2586-4682-b5d0-972b8ae43719": {
                                    "@type": "slate"
                                },
                                "9b1ac3c4-5a7a-4e04-a772-96ea053e8562": {
                                    "@type": "dashboardTile",
                                    "title": "Ecological status of surface waters in England, 2019",
                                    "topic": "Impacts",
                                    "data_source": [
                                        {
                                            "@id": "/overview-data/tile-status-of-the-ecological-environment",
                                            "@type": "sparql_dataconnector",
                                            "CreationDate": "2022-05-18T08:23:36+00:00",
                                            "Creator": "aa750921-8eed-4a64-9f39-f1f7a33027c7",
                                            "Date": "2022-05-18T13:13:16+00:00",
                                            "Description": "",
                                            "EffectiveDate": "2022-05-18T13:13:16+00:00",
                                            "ExpirationDate": "None",
                                            "ModificationDate": "2022-06-15T21:06:58+00:00",
                                            "Subject": [],
                                            "Title": "Tile; Bar; Status of the Ecological Environment",
                                            "Type": "SPARQL Data Connector",
                                            "UID": "88ddb08d26354715b5d9a4e86debc173",
                                            "author_name": None,
                                            "cmf_uid": None,
                                            "commentators": [],
                                            "created": "2022-05-18T08:23:36+00:00",
                                            "description": "",
                                            "effective": "2022-05-18T13:13:16+00:00",
                                            "end": None,
                                            "exclude_from_nav": False,
                                            "expires": "2499-12-31T00:00:00+00:00",
                                            "getIcon": None,
                                            "getId": "tile-status-of-the-ecological-environment",
                                            "getObjSize": "0 KB",
                                            "getPath": "/Plone/overview-data/tile-status-of-the-ecological-environment",
                                            "getRemoteUrl": None,
                                            "getURL": "http://climate-change.data.gov.uk/api/overview-data/tile-status-of-the-ecological-environment",
                                            "hasPreviewImage": None,
                                            "head_title": None,
                                            "id": "tile-status-of-the-ecological-environment",
                                            "in_response_to": None,
                                            "is_folderish": True,
                                            "last_comment_date": None,
                                            "lead_image": None,
                                            "listCreators": [
                                                "aa750921-8eed-4a64-9f39-f1f7a33027c7"
                                            ],
                                            "location": None,
                                            "meta_type": "Dexterity Container",
                                            "mime_type": "text/plain",
                                            "modified": "2022-06-15T21:06:58+00:00",
                                            "nav_title": None,
                                            "portal_type": "sparql_dataconnector",
                                            "review_state": "published",
                                            "start": None,
                                            "sync_uid": None,
                                            "title": "Tile; Bar; Status of the Ecological Environment",
                                            "total_comments": 0
                                        }
                                    ],
                                    "vis_type": "bar"
                                },
                            },
                            "blocks_layout": {
                                "items": [
                                    "9b1ac3c4-5a7a-4e04-a772-96ea053e8562",
                                    "74559b24-2586-4682-b5d0-972b8ae43719",
                                ]
                            },
                        },
                        "6a8f62cd-d6d2-4277-bfed-c35e04a81137": {
                            "blocks": {
                                "93a12089-b230-4d41-b911-415f03a00ee1": {
                                    "@type": "dashboardTile",
                                    "title": "New planting of UK woodlands, thousand hectares",
                                    "topic": "Adaptation",
                                    "data_source": [
                                        {
                                            "@id": "/overview-data/new-planting-of-uk-woodlands-thousand-hectares-1976-to-2021",
                                            "@type": "sparql_dataconnector",
                                            "CreationDate": "2022-05-18T08:23:07+00:00",
                                            "Creator": "aa750921-8eed-4a64-9f39-f1f7a33027c7",
                                            "Date": "2022-05-18T13:13:18+00:00",
                                            "Description": "",
                                            "EffectiveDate": "2022-05-18T13:13:18+00:00",
                                            "ExpirationDate": "None",
                                            "ModificationDate": "2022-06-15T21:06:59+00:00",
                                            "Subject": [],
                                            "Title": "Tile; SparkLine; New planting of UK woodlands, thousand hectares, 1976 to 2021",
                                            "Type": "SPARQL Data Connector",
                                            "UID": "304c40ebebe2402b86d8f277d7328f77",
                                            "author_name": None,
                                            "cmf_uid": None,
                                            "commentators": [],
                                            "created": "2022-05-18T08:23:07+00:00",
                                            "description": "",
                                            "effective": "2022-05-18T13:13:18+00:00",
                                            "end": None,
                                            "exclude_from_nav": False,
                                            "expires": "2499-12-31T00:00:00+00:00",
                                            "getIcon": None,
                                            "getId": "new-planting-of-uk-woodlands-thousand-hectares-1976-to-2021",
                                            "getObjSize": "0 KB",
                                            "getPath": "/Plone/overview-data/new-planting-of-uk-woodlands-thousand-hectares-1976-to-2021",
                                            "getRemoteUrl": None,
                                            "getURL": "http://climate-change.data.gov.uk/api/overview-data/new-planting-of-uk-woodlands-thousand-hectares-1976-to-2021",
                                            "hasPreviewImage": None,
                                            "head_title": None,
                                            "id": "new-planting-of-uk-woodlands-thousand-hectares-1976-to-2021",
                                            "in_response_to": None,
                                            "is_folderish": True,
                                            "last_comment_date": None,
                                            "lead_image": None,
                                            "listCreators": [
                                                "aa750921-8eed-4a64-9f39-f1f7a33027c7"
                                            ],
                                            "location": None,
                                            "meta_type": "Dexterity Container",
                                            "mime_type": "text/plain",
                                            "modified": "2022-06-15T21:06:59+00:00",
                                            "nav_title": None,
                                            "portal_type": "sparql_dataconnector",
                                            "review_state": "published",
                                            "start": None,
                                            "sync_uid": None,
                                            "title": "Tile; SparkLine; New planting of UK woodlands, thousand hectares, 1976 to 2021",
                                            "total_comments": 0
                                        }
                                    ],
                                    "vis_type": "spark_line"
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
                        "bee4bcab-ac18-4af0-ae8c-5f13270a441d": {
                            "blocks": {
                                "b32a4481-1694-4202-9a75-1b68d13f7dab": {
                                    "@type": "dashboardTile",
                                    "title": "Renewable energy share in total energy consumption, UK, 2020",
                                    "topic": "Mitigation",
                                    "data_source": [
                                        {
                                            "@id": "/overview-data/renewable-energy-share-in-total-energy-consumption-uk-2020",
                                            "@type": "sparql_dataconnector",
                                            "CreationDate": "2022-05-18T08:23:36+00:00",
                                            "Creator": "aa750921-8eed-4a64-9f39-f1f7a33027c7",
                                            "Date": "2022-05-18T13:13:16+00:00",
                                            "Description": "17%, not 16%...",
                                            "EffectiveDate": "2022-05-18T13:13:16+00:00",
                                            "ExpirationDate": "None",
                                            "ModificationDate": "2022-06-15T21:06:58+00:00",
                                            "Subject": [],
                                            "Title": "Tile; Bar; Renewable energy share in total energy consumption, UK, 2020",
                                            "Type": "SPARQL Data Connector",
                                            "UID": "d84d31651d3e4a7093316cc5c744c770",
                                            "author_name": None,
                                            "cmf_uid": None,
                                            "commentators": [],
                                            "created": "2022-05-18T08:23:36+00:00",
                                            "description": "17%, not 16%...",
                                            "effective": "2022-05-18T13:13:16+00:00",
                                            "end": None,
                                            "exclude_from_nav": False,
                                            "expires": "2499-12-31T00:00:00+00:00",
                                            "getIcon": None,
                                            "getId": "renewable-energy-share-in-total-energy-consumption-uk-2020",
                                            "getObjSize": "0 KB",
                                            "getPath": "/Plone/overview-data/renewable-energy-share-in-total-energy-consumption-uk-2020",
                                            "getRemoteUrl": None,
                                            "getURL": "http://climate-change.data.gov.uk/api/overview-data/renewable-energy-share-in-total-energy-consumption-uk-2020",
                                            "hasPreviewImage": None,
                                            "head_title": None,
                                            "id": "renewable-energy-share-in-total-energy-consumption-uk-2020",
                                            "in_response_to": None,
                                            "is_folderish": True,
                                            "last_comment_date": None,
                                            "lead_image": None,
                                            "listCreators": [
                                                "aa750921-8eed-4a64-9f39-f1f7a33027c7"
                                            ],
                                            "location": None,
                                            "meta_type": "Dexterity Container",
                                            "mime_type": "text/plain",
                                            "modified": "2022-06-15T21:06:58+00:00",
                                            "nav_title": None,
                                            "portal_type": "sparql_dataconnector",
                                            "review_state": "published",
                                            "start": None,
                                            "sync_uid": None,
                                            "title": "Tile; Bar; Renewable energy share in total energy consumption, UK, 2020",
                                            "total_comments": 0
                                        }
                                    ],
                                    "vis_type": "bar"
                                },
                                "c49a4c55-e28f-469f-b0b5-cf0e11e3c208": {
                                    "@type": "slate"
                                }
                            },
                            "blocks_layout": {
                                "items": [
                                    "b32a4481-1694-4202-9a75-1b68d13f7dab",
                                    "c49a4c55-e28f-469f-b0b5-cf0e11e3c208"
                                ]
                            }
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
