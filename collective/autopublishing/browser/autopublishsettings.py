from z3c.form import field
from zope.interface import Interface
from zope import schema

from plone.z3cform import layout
from plone.app.registry.browser import controlpanel

from collective.autopublishing import MyMessageFactory as _

class IAutopublishSettingsSchema(Interface):

    initial_states_publishing = schema.List(
        value_type=schema.TextLine(
            title=u'State'),
        title=_(u'Initial states for publishing'),
        description=_(u"The states need to supply a publish action."),
        required=False)
    initial_states_retracting = schema.List(
        value_type=schema.TextLine(
            title=u'State'),
        title=_(u'Initial states for retracting'),
        description=_(u"The states need to supply a retract action."),
        required=False)
    overwrite_expiration_on_retract = schema.Bool(
        title=_(u'Set expiration date on retraction'),
        description=_(u"If this is set, the expiration date "
                      u"will be overwritten with the current time "
                      u"when reatrcting an item, to avoid republication if "
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
        title=_(u'Dry run'),
        description=_(u"Dry run simulates the publishing process. "
                      u"Nothing is actually published."),
        default=False)


class AutopublishControlPanelEditForm(controlpanel.RegistryEditForm):
    schema = IAutopublishSettingsSchema
    fields = field.Fields(IAutopublishSettingsSchema)

    label = _(u"Autopublishing")
    description = _(
        u"Controls the initial workflow states autopublishing will make transitions from."
        )


AutopublishControlPanel = layout.wrap_form(
    AutopublishControlPanelEditForm,
    controlpanel.ControlPanelFormWrapper
    )
