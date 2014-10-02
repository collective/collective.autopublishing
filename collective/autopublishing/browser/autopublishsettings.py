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
    date_field = schema.TextLine(
        title=_(u"Transaction trigger date field id"),
        description=_(u"By default publishing date is used for "
                      u"'publish actions', and expiration date is "
                      u"used for 'retract actions'."),
        required=False,
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
        title=_(u'Publish actions'),
        description=_(u"Workflow actions initiated by the autopublishing "
                      u"module when the publishing date is met."),
        required=False,
        default=(),
        missing_value=())
    retract_actions = schema.Tuple(
        value_type=schema.Object(
            title=_(u'Action'),
            schema=IAutopublishSpecification),
        title=_(u'Retract actions'),
        description=_(u"Workflow actions initiated by the autopublishing "
                      u"module when the expiration date is met."),
        required=False,
        default=(),
        missing_value=())
    overwrite_expiration_on_retract = schema.Bool(
        title=_(u'Set expiration date on retraction'),
        description=_(u"If this is set, the expiration date "
                      u"will be overwritten with the current time "
                      u"when manually retracting an item, to avoid "
                      u" republication if there is a publication date "
                      u"in the past."),
        default=False)
    clear_expiration_on_publish = schema.Bool(
        title=_(u'Clear expiration date on publication'),
        description=_(u"If this is set, an expiration date "
                      u"in the past will be cleared "
                      u"when manually publishing an item, to avoid "
                      u"immediate retraction."),
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

    def getContent(self):
        return getUtility(IRegistry).forInterface(
            self.schema,
            omit=('publish_actions', 'retract_actions'),
            prefix=self.schema_prefix,
            factory=ComplexRecordsProxy)


class ControlPanelFormWrapper(layout.FormWrapper):
    """
    """

    index = ViewPageTemplateFile('controlpanel_layout.pt')

AutopublishControlPanel = layout.wrap_form(
    AutopublishControlPanelEditForm,
    ControlPanelFormWrapper
    )
