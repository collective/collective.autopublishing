from Acquisition import aq_base
#from Products.CMFPlone.CatalogTool import registerIndexableAttribute
from plone.indexer.decorator import indexer
from zope.i18nmessageid import MessageFactory
MyMessageFactory = MessageFactory('headnet.autopublish')
from zope.interface import Interface

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

@indexer(Interface)
def _publish_on_date(obj, **kwargs):
    """for portal_catalog to index publishOnDate field"""

    if obj.schema.has_key('publishOnDate'):
        return obj.getPublishOnDate()
    return False

from cron import has_publishondate_index

if has_publishondate_index():
    #registerIndexableAttribute('publishOnDate', _publish_on_date)

    # patch ATCT Types
    from patch_types import makeATCTTypesAutoPublishAware
    makeATCTTypesAutoPublishAware()

    # Make the function makeTypesAutoPublishAware available
    # from the root package so other products can patch their types
    # easily like this:
    # from headnet.autopublish import makeTypesAutoPublishAware
    # makeTypesAutoPublishAware([MyType1, MyType2])

    from patch_types import makeTypesAutoPublishAware


