from persistent import Persistent
from persistent.list import PersistentList
from zope.interface import implements
from zope.component import getUtility

from headnet.autopublish.browser.autopublishsettings import IAutopublishSettingsSchema

class AutopublishSettings(Persistent):
    """We use raw fields here so that we can more easily use a zope.formlib
    form in the control panel to configure it. This is registered as a
    persistent local utility
    """

    implements(IAutopublishSettingsSchema)

    initial_states_publishing = PersistentList()

