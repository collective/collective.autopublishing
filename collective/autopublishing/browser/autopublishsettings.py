# -*- coding: utf-8 -*-
import logging
from zope.interface import Interface, implements
from zope.component import getUtility
from zope import schema
from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent

from z3c.form import field
from z3c.form.object import FactoryAdapter

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.z3cform import layout
from plone.app.registry.browser import controlpanel
from plone.registry.interfaces import IRegistry

from collective.complexrecordsproxy import ComplexRecordsProxy
from collective.autopublishing import MyMessageFactory as _

logger = logging.getLogger('collective.autopublishing')


class IAutopublishSpecification(Interface):
    portal_types = schema.Tuple(
        title=_(u"Content types"),
        description=_('help_ap_portaltypes',
                      default=u"Content types this rule applies to."),
        required=True,
        missing_value=(),
        value_type=schema.Choice(
            vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes"))
    initial_state = schema.TextLine(
        title=_('label_initial_state', default=u"Initial workflow state"),
        required=True,
        )
    transition = schema.TextLine(
        title=_('label_transition', default=u"Transition from initial state"),
        required=True,
        )
    date_index = schema.TextLine(
        title=_('label_date_index',
                default=u"Transaction trigger date catalog index / method"),
        description=_(
            'help_date_index',
            default=u"By default publishing date (the 'effective' index) is "
                    u"used for 'publish actions', and expiration date (the "
                    u"'expires' index) is used for 'retract actions'."
                    u" If a custom method is to be used for the date, enter"
                    u" index_id|object_method_id. If index_id = method_id "
                    u" just enter index_id."),
        required=False,
        default=u'effective',
        missing_value=u'effective'
        )


class AutopublishSpecification(object):
    implements(IAutopublishSpecification)

    def __init__(self, value):
        self.portal_types = value["portal_types"]
        self.initial_state = value["initial_state"]
        self.transition = value["transition"]


class AutopublishSpecificationFactory(FactoryAdapter):

    def __call__(self, value):
        obj = AutopublishSpecification(value)
        notify(ObjectCreatedEvent(obj))
        return obj


class IAutopublishSettingsSchema(Interface):

    publish_actions = schema.Tuple(
        value_type=schema.Object(
            title=_(u'Action'),
            schema=IAutopublishSpecification),
        title=_('label_publish_actions', default=u'Publish actions'),
        description=_(
            'help_publish_actions',
            default=u"Workflow actions initiated by the autopublishing "
                    u"module when the publishing date is met."),
        required=False,
        default=(),
        missing_value=())
    retract_actions = schema.Tuple(
        value_type=schema.Object(
            title=_(u'Action'),
            schema=IAutopublishSpecification),
        title=_('label_retract_actions', default=u'Retract actions'),
        description=_(
            'help_retract_actions',
            default=u"Workflow actions initiated by the autopublishing "
                    u"module when the expiration date is met."),
        required=False,
        default=(),
        missing_value=())
    overwrite_expiration_on_retract = schema.Bool(
        title=_('label_overwrite_expiration',
                default=u'Set expiration date on retraction'),
        description=_(
            'help_overwrite_expiration',
            default=u"If this is set, the expiration date "
                    u"will be overwritten with the current time "
                    u"when manually retracting an item, to avoid "
                    u" republication if there is a publication date "
                    u"in the past."),
        default=False)
    clear_expiration_on_publish = schema.Bool(
        title=_('label_clear_expiration',
                default=u'Clear expiration date on publication'),
        description=_(
            'help_clear_expiration',
            default=u"If this is set, an expiration date "
                    u"in the past will be cleared "
                    u"when manually publishing an item, to avoid "
                    u"immediate retraction."),
        default=False)
    email_log = schema.List(
        value_type=schema.TextLine(title=u'Email'),
        title=_('label_email_log',
                default=u'Email addresses for audit log'),
        description=_(
            'help_email_log',
            default=u"If one or more email addresses is supplied, "
                    u"an audit log of the actions taken is sent."),
        required=False)
    dry_run = schema.Bool(
        title=_('label_dry_run', default=u'Simulate'),
        description=_(
            'help_dry_run',
            default=u"Simulates the process of changing workflow state. "
                    u"Nothing actually changes state, but it is possible to "
                    u"review what actions will be taken. To activate "
                    u"the module, remove the checkmark."),
        default=True)


class AutopublishControlPanelEditForm(controlpanel.RegistryEditForm):
    schema = IAutopublishSettingsSchema
    fields = field.Fields(IAutopublishSettingsSchema)

    label = _('label_ap_contolpanel', default=u"Autopublishing settings")
    description = _(
        'help_ap_controlpanel',
        default=u"Controls the workflow actions autopublishing will make."
        )

    def getContent(self):
        return getUtility(IRegistry).forInterface(
            self.schema,
            omit=('publish_actions', 'retract_actions'),
            factory=ComplexRecordsProxy)


class ControlPanelFormWrapper(layout.FormWrapper):
    """
    """

    index = ViewPageTemplateFile('controlpanel_layout.pt')

AutopublishControlPanel = layout.wrap_form(
    AutopublishControlPanelEditForm,
    ControlPanelFormWrapper
    )
