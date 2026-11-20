from collective.autopublishing.browser.autopublishsettings import (
    AutopublishSpecification,
)
from collective.autopublishing.browser.autopublishsettings import (
    IAutopublishSettingsSchema,
)
from collective.autopublishing.interfaces import IBrowserLayer
from collective.autopublishing.tests.layer import C_AUTOPUBLISHING_LAYER
from collective.complexrecordsproxy import ComplexRecordsProxy
from DateTime import DateTime
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import alsoProvides

import re
import unittest


class TestViews(unittest.TestCase):

    layer = C_AUTOPUBLISHING_LAYER

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        alsoProvides(self.request, IBrowserLayer)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def save_publish_action(self):
        settings = getUtility(IRegistry).forInterface(
            IAutopublishSettingsSchema,
            omit=("publish_actions", "retract_actions"),
            factory=ComplexRecordsProxy,
        )
        settings.publish_actions = (
            AutopublishSpecification(
                {
                    "portal_types": ("Document",),
                    "initial_state": "private",
                    "transition": "publish",
                }
            ),
        )

    def test_controlpanel(self):
        html = self.portal.restrictedTraverse("@@autopublish-controlpanel")()
        self.assertIn("Autopublishing settings", html)
        self.assertIn("@@autopublish-report", html)

    def test_controlpanel_shows_saved_portal_types(self):
        # https://github.com/collective/collective.autopublishing/issues/9
        self.save_publish_action()
        html = self.portal.restrictedTraverse("@@autopublish-controlpanel")()
        selected = re.search(
            r'<select name="form\.widgets\.publish_actions\.0\.widgets'
            r'\.portal_types\.to".*?</select>',
            html,
            re.DOTALL,
        ).group()
        self.assertIn('value="Document"', selected)

    def test_report(self):
        self.save_publish_action()
        self.portal.invokeFactory("Document", id="document1", title="Document 1")
        document = self.portal["document1"]
        document.enableAutopublishing = True
        document.setEffectiveDate(DateTime() - 1)
        document.reindexObject()

        html = self.portal.restrictedTraverse("@@autopublish-report")()
        self.assertIn("Autopublishing: Report of next actions taken", html)
        # The report lists the URL as link text (the navigation only links it)
        self.assertIn(f">{document.absolute_url()}</a>", html)
