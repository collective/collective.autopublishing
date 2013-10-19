from persistent.list import PersistentList

from zope.formlib.form import FormFields
from zope.interface import Interface
from zope.component import adapts
from zope.interface import implements
from zope import schema
from zope.component import getUtility

from Products.Five import BrowserView
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.controlpanel.form import ControlPanelForm

from collective.autopublishing import MyMessageFactory as _


class IAutopublishSettingsSchema(Interface):

    initial_states_publishing = schema.Text(
        title=_(u'Initial states'),
        description=_(u"The states need to supply a publish action."),
        required=False)

class AutopublishSettingsControlPanelAdapter(SchemaAdapterBase):
    adapts(IPloneSiteRoot)
    implements(IAutopublishSettingsSchema)

    def __init__(self, context):
        super(AutopublishSettingsControlPanelAdapter, self).__init__(context)
        self.context = context
        self.settings = getUtility(IAutopublishSettingsSchema)

    @apply
    def initial_states_publishing():
        def get(self):
            return '\n'.join(self.settings.initial_states_publishing)
        def set(self, value):
            initial_states_publishing = PersistentList(value.split('\n'))
            self.settings.initial_states_publishing = initial_states_publishing
        return property(get, set)


class AutopublishSettingsControlPanel(ControlPanelForm):

    form_fields = FormFields(IAutopublishSettingsSchema)

    label = _("Autopublishing")
    description = _("Controls the initial workflow states autopublishing will make transitions from.")
    form_name = _("")

class AutopublishSettingsView(BrowserView):

    def initial_states_publishing(self):
        myutil = getUtility(IAutopublishSettingsSchema)
        initial_states_publishing = myutil.initial_states_publishing
        return initial_states_publishing

