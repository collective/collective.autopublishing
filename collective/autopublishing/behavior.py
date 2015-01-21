# encoding: utf-8
from zope import schema
from zope.interface import alsoProvides

from plone.directives import form

from plone.namedfile.field import NamedBlobImage

from headnet.base.i18n import MessageFactory as _


class IAutoPublishing(form.Schema):

    form.fieldset(
        'settings',
        fields=('enableAutopublishing', )
    )

    enableAutopublishing = schema.Bool(
        title=_(u'enableAutopublishing', default=u"Enable autopublishing?"),
        required=False,
        default=True
    )

alsoProvides(IAutoPublishing, form.IFormFieldProvider)
