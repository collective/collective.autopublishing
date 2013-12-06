from zope.interface import Interface, implements
from zope.component import getUtility
from zope import schema
from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent

from z3c.form import field
from z3c.form.object import FactoryAdapter

from plone.z3cform import layout
from plone.app.registry.browser import controlpanel
from plone.registry.interfaces import IRegistry
from plone.registry.recordsproxy import RecordsProxy

from collective.autopublishing import MyMessageFactory as _


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
                       "module when the publishing date is met."),
        required=False,
        default=(),
        missing_value=())
    retract_actions = schema.Tuple(
        value_type=schema.Object(
            title=_(u'Action'),
            schema=IAutopublishSpecification),
        title=_(u'Retract actions'),
        description=_(u"Workflow actions initiated by the autopublishing "
                       "module when the expiration date is met."),
        required=False,
        default=(),
        missing_value=())
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


_marker = object()

class ComplexRecordsProxy(RecordsProxy):

    object_fields = ('publish_actions', 'retract_actions')

    def __getattr__(self, name):
        reg = self.__registry__
        if name not in self.__schema__:
            raise AttributeError(name)
        if name in self.object_fields:
            coll_prefix = IAutopublishSpecification.__identifier__ + '.' + name
            collection = reg.collectionOfInterface(
                           IAutopublishSpecification,
                           prefix=coll_prefix)
            value = [
                AutopublishSpecification({'portal_types': item.portal_types,
                                          'initial_state': item.initial_state,
                                          'transition': item.transition
                                         })
                for item in collection.values()
                ] or _marker
        else:
            value = reg.get(self.__prefix__ + name, _marker)
        if value is _marker:
            value = self.__schema__[name].missing_value
        return value

    def __setattr__(self, name, value):
        if name in self.__schema__:
            reg = self.__registry__
            if name in self.object_fields:
                # create a new record in the collection for the object interface:
                coll_prefix = IAutopublishSpecification.__identifier__ + '.' + name
                collection = reg.collectionOfInterface(
                               IAutopublishSpecification,
                               prefix=coll_prefix)
                # existing values? Clear all and reapply? Better: have some id.
                for idx, val in enumerate(value):
                    # the value is a tuple in our case - is this always so?
                    collection['r' + str(idx)] = val
            else:
                full_name = self.__prefix__ + name
                if full_name not in reg:
                    raise AttributeError(name)
                reg[full_name] = value
        else:
            self.__dict__[name] = value


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


AutopublishControlPanel = layout.wrap_form(
    AutopublishControlPanelEditForm,
    controlpanel.ControlPanelFormWrapper
    )
