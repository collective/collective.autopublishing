from App.config import getConfiguration
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from plone.indexer.decorator import indexer

from .behavior import IAutoPublishing

MyMessageFactory = MessageFactory('collective.autopublishing')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

@indexer(Interface)
def _enableautopublishing(obj, **kwargs):
    """for portal_catalog to index enableAutopublishing field"""

    if hasattr(obj, 'schema'):
        if obj.schema.has_key('enableAutopublishing'):
            return obj.getEnableAutopublishing()

    if IAutoPublishing.providedBy(obj):
        return getattr(obj, 'enableAutopublishing', True)

    return False

# patch ATCT Types
from patch_types import makeATCTTypesAutoPublishAware
makeATCTTypesAutoPublishAware()

# Make the function makeTypesAutoPublishAware available
# from the root package so other products can patch their types
# easily like this:
# from collective.autopublishing import makeTypesAutoPublishAware
# makeTypesAutoPublishAware([MyType1, MyType2])

from patch_types import makeTypesAutoPublishAware
