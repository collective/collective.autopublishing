from App.config import getConfiguration
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from plone.indexer.decorator import indexer


MyMessageFactory = MessageFactory('collective.autopublishing')


@indexer(Interface)
def _enableautopublishing(obj, **kwargs):
    """for portal_catalog to index enableAutopublishing field"""

    if hasattr(obj, 'schema'):
        if obj.schema.has_key('enableAutopublishing'):
            return obj.getEnableAutopublishing()

    from collective.autopublishing.behavior import IAutoPublishing
    if IAutoPublishing.providedBy(obj):
        return getattr(obj, 'enableAutopublishing', True)

    return False

