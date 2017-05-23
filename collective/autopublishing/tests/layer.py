# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneSandboxLayer


class AutoPublishingLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.timedevents
        self.loadZCML('configure.zcml', package=collective.timedevents)
        import collective.autopublishing
        self.loadZCML('configure.zcml', package=collective.autopublishing)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.autopublishing:default')


C_AUTOPUBLISHING_FIXTURE = AutoPublishingLayer()


C_AUTOPUBLISHING_LAYER = FunctionalTesting(
    bases=(C_AUTOPUBLISHING_FIXTURE,),
    name='CollectiveAutopublishingLayer:FunctionalTesting')

# EOF
