# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import ukstats.cc-v2.theme


class UkstatsCc-V2ThemeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=ukstats.cc-v2.theme)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ukstats.cc-v2.theme:default')


UKSTATS_CC-V2_THEME_FIXTURE = UkstatsCc-V2ThemeLayer()


UKSTATS_CC-V2_THEME_INTEGRATION_TESTING = IntegrationTesting(
    bases=(UKSTATS_CC-V2_THEME_FIXTURE,),
    name='UkstatsCc-V2ThemeLayer:IntegrationTesting',
)


UKSTATS_CC-V2_THEME_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(UKSTATS_CC-V2_THEME_FIXTURE,),
    name='UkstatsCc-V2ThemeLayer:FunctionalTesting',
)


UKSTATS_CC-V2_THEME_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        UKSTATS_CC-V2_THEME_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='UkstatsCc-V2ThemeLayer:AcceptanceTesting',
)
