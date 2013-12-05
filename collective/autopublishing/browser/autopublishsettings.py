from zope.interface import Interface, implements
from zope.component import adapts
from zope import schema
from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent

from z3c.form import field
from z3c.form.interfaces import IObjectFactory, IFormLayer, IWidget
from z3c.form.object import FactoryAdapter

from plone.z3cform import layout
from plone.app.registry.browser import controlpanel
from plone.registry.field import PersistentField

from collective.autopublishing import MyMessageFactory as _


class PersistentObject(PersistentField, schema.Object):
    pass


class IAutopublishSpecification(Interface):
    portal_types = schema.Tuple(
        title=_(u"Content types"),
        description=_(u"Content types this rule applies to."),
        required=True,
        missing_value=tuple(),
        value_type=schema.Choice(
            vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes"))
    initial_state = schema.TextLine(
        title=_(u"Initial workflow state"),
        required=True,
        )
    transition = schema.TextLine(
        title=_(u"Transition from initial state"),
        required=True,
        )


class AutopublishSpecification(object):
     implements(IAutopublishSpecification)

     def __init__(self, value):
         self.portal_types = value["portal_types"]
         self.initial_state = value["initial_state"]
         self.transition = value["transition"]


class AutopublishSpecificationFactory(FactoryAdapter):
     # adapts(Interface,     #context
     #        IFormLayer,    #request
     #        Interface,     #form -- but can become None easily (in tests)
     #        IWidget)       #widget
     # implements(IObjectFactory)

     # def __init__(self, context, request, form, widget):
     #     pass

     def __call__(self, value):
        obj = AutopublishSpecification(value)
        notify(ObjectCreatedEvent(obj))
        return obj

# registerFactoryAdapter(IAutopublishSpecification,
#                        AutopublishSpecification)


class IAutopublishSettingsSchema(Interface):

    publish_actions = schema.Tuple(
        value_type=PersistentObject(
            title=_(u'Action'),
            schema=IAutopublishSpecification),
        title=_(u'Publish actions'),
        description=_(u"Workflow actions initiated by the autopublishing "
                       "module when the publishing date is met."),
        required=False,
        default=(),
        missing_value=())
    retract_actions = schema.Tuple(
        value_type=PersistentObject(
            title=_(u'Action'),
            schema=IAutopublishSpecification),
        title=_(u'Retract actions'),
        description=_(u"Workflow actions initiated by the autopublishing "
                       "module when the expiration date is met."),
        required=False,
        default=(),
        missing_value=())
    # initial_states_retracting = schema.List(
    #     value_type=schema.TextLine(
    #         title=u'State'),
    #     title=_(u'Initial states for retracting'),
    #     description=_(u"The states need to supply a retract action."),
    #     required=False)
    overwrite_expiration_on_retract = schema.Bool(
        title=_(u'Set expiration date on retraction'),
        description=_(u"If this is set, the expiration date "
                      u"will be overwritten with the current time "
                      u"when retracting an item, to avoid republication if "
                      u"there is a publication date or the expiration "
                      u"date is in the future."),
        default=False)
    email_log = schema.List(
        value_type=schema.TextLine(
            title=u'Email'),
        title=_(u'Email addresses for audit log'),
        description=_(u"If one or more email addresses is supplied, "
                      u"an audit log of the actions taken is sent."),
        required=False)
    dry_run = schema.Bool(
        title=_(u'Simulate'),
        description=_(u"Simulates the process of changing workflow state. "
                      u"Nothing actually changes state, but it is possible to "
                      u"review what actions will be taken. To activate "
                      u"the module, remove the checkmark."),
        default=True)


class AutopublishControlPanelEditForm(controlpanel.RegistryEditForm):
    schema = IAutopublishSettingsSchema
    fields = field.Fields(IAutopublishSettingsSchema)

    label = _(u"Autopublishing")
    description = _(
        u"Controls the workflow actions autopublishing will make."
        )


AutopublishControlPanel = layout.wrap_form(
    AutopublishControlPanelEditForm,
    controlpanel.ControlPanelFormWrapper
    )
