from App.config import getConfiguration
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from plone.indexer.decorator import indexer

MyMessageFactory = MessageFactory('collective.autopublishing')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

def get_config_value(key, default=None):
    """return a package config param"""
    try:
        config = getConfiguration().product_config
        autopublish_config = config.get('collective.autopublishing', {})
        value = autopublish_config.get(key, default)
    except AttributeError:
        value = default
    return value

def has_enableautopublishing_field():
    return get_config_value('add-enableautopublishing-field', 'yes') in ['yes', 'true', 'on']

@indexer(Interface)
def _enableautopublishing(obj, **kwargs):
    """for portal_catalog to index enableAutopublishing field"""

    if obj.schema.has_key('enableAutopublishing'):
        return obj.getEnableAutopublishing()
    return False

if has_enableautopublishing_field():
    # patch ATCT Types
    from patch_types import makeATCTTypesAutoPublishAware
    makeATCTTypesAutoPublishAware()

    # Make the function makeTypesAutoPublishAware available
    # from the root package so other products can patch their types
    # easily like this:
    # from collective.autopublishing import makeTypesAutoPublishAware
    # makeTypesAutoPublishAware([MyType1, MyType2])

    from patch_types import makeTypesAutoPublishAware
