from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer


class AutoPublishingLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # What PLONE_APP_CONTENTTYPES_FIXTURE does, without importing
        # plone.app.contenttypes.testing, which needs plone.app.robotframework.
        import plone.app.contenttypes

        self.loadZCML(package=plone.app.contenttypes)

        import collective.timedevents

        self.loadZCML("configure.zcml", package=collective.timedevents)
        import collective.autopublishing

        self.loadZCML("configure.zcml", package=collective.autopublishing)

    def setUpPloneSite(self, portal):
        portal.portal_workflow.setDefaultChain("simple_publication_workflow")
        applyProfile(portal, "collective.autopublishing:default")


C_AUTOPUBLISHING_FIXTURE = AutoPublishingLayer()


C_AUTOPUBLISHING_LAYER = FunctionalTesting(
    bases=(C_AUTOPUBLISHING_FIXTURE,),
    name="CollectiveAutopublishingLayer:FunctionalTesting",
)
