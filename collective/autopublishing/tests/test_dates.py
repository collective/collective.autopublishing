# -*- coding: utf-8 -*-
from collective.autopublishing.eventhandler import autopublish_handler
from collective.autopublishing.eventhandler import transition_handler
from collective.autopublishing.tests.layer import C_AUTOPUBLISHING_LAYER
from Products.DCWorkflow.Transitions import TransitionDefinition
from DateTime import DateTime
from plone.app.event.testing import set_env_timezone
from plone.app.event.testing import set_timezone
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone import api

import unittest

TZ = 'Europe/Zurich'


class DummyTransitionEvent(object):
    """ A dummy transition event with just object and transition
    """

    def __init__(self, obj, transition):
        self.object = obj
        self.transition = transition


class TimeZoneTest(unittest.TestCase):

    layer = C_AUTOPUBLISHING_LAYER

    def setUp(self):
        print(set_env_timezone(TZ))
        print(set_timezone(TZ))
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager', ])
        self.doc1 = api.content.create(portal, 'Document', title='Document 1')

    def test_effective_tz(self):
        retract = TransitionDefinition('publish')
        retract_event = DummyTransitionEvent(self.doc1, transition=retract)
        effective = DateTime(2016, 5, 5)
        self.doc1.setEffectiveDate(effective)
        transition_handler(retract_event)
        print(self.doc1.EffectiveDate())

    def X_test_expires_tz(self):
        effective = DateTime(2016, 5, 5)
        self.doc1.setEffectiveDate(effective)
        autopublish_handler(self.event1)
        print(self.doc1.EffectiveDate())

# EOF
