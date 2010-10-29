#from plone.fieldsets.fieldsets import FormFieldsets
from zope.formlib.form import FormFields


from zope.interface import Interface
from zope.component import adapts
from zope.interface import implements
from zope import schema
from zope.app.form import CustomWidgetFactory
from zope.app.form.browser import ObjectWidget
from zope.app.form.browser import ListSequenceWidget
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from persistent.dict import PersistentDict
from persistent.list import PersistentList

from Products.Five import BrowserView

from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
#from Products.PortalTransforms.transforms.safe_html import VALID_TAGS

from plone.app.controlpanel.form import ControlPanelForm

from headnet.autopublish import MyMessageFactory as _


class IAutopublishSettingsSchema(Interface):

    initial_states = schema.Text(
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
    def initial_states():
        def get(self):
            return '\n'.join(self.settings.initial_states)
        def set(self, value):
            initial_states = PersistentList(value.split('\n'))
            self.settings.initial_states = initial_states
        return property(get, set)


class AutopublishSettingsControlPanel(ControlPanelForm):

    form_fields = FormFields(IAutopublishSettingsSchema)

    label = _("Autopublishing")
    description = _("")
    form_name = _("")

class AutopublishSettingsView(BrowserView):
    
    def initial_states(self):
        myutil = getUtility(IAutopublishSettingsSchema)
        initial_states = myutil.initial_states
        return initial_states

