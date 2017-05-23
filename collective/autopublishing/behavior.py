# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import provider
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from collective.autopublishing import MyMessageFactory as _


@provider(IFormFieldProvider)
class IAutoPublishing(model.Schema):

    model.fieldset(
        'dates',
        fields=('enableAutopublishing', )
    )

    enableAutopublishing = schema.Bool(
        title=_(u'enableAutopublishing', default=u"Enable autopublishing?"),
        required=False,
        default=False)
