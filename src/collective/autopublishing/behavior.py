from collective.autopublishing import MyMessageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IAutoPublishing(model.Schema):

    model.fieldset("dates", fields=("enableAutopublishing",))

    enableAutopublishing = schema.Bool(
        title=_("enableAutopublishing", default="Enable autopublishing?"),
        required=False,
        default=False,
    )
