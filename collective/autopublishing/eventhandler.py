import logging
from zope.component import ComponentLookupError, getUtility

from plone.registry.interfaces import IRegistry
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.AdvancedQuery import Eq, In, Le

from browser.autopublishsettings import IAutopublishSettingsSchema
from collective.autopublishing import has_enableautopublishing_field

logger = logging.getLogger('collective.autopublishing')

#
# Event handler.
#
# Should be registered in zcml as subscribers to
# one of the tick events from collective.timedevents

def AutoPublishHandler(event):
    '''
    '''
    context = event.context
    catalog = context.portal_catalog
    wf = context.portal_workflow

    try:
        settings = getUtility(IRegistry).forInterface(IAutopublishSettingsSchema)
    except (ComponentLookupError, KeyError):
        logger.info('The product needs to be installed. No settings in the registry.')
        return

    has_field = has_enableautopublishing_field()

    if has_field and 'enableAutopublishing' not in catalog.indexes():
        logger.info('Catalog does not have a enableAutopublishing index')
        return

    states_to_publish = settings.initial_states_publishing
    if not states_to_publish:
        logger.info('You have to define state-to-publish in the plone control panel')
        return

    now = context.ZopeTime()
    query = (In('review_state', states_to_publish)
             & Eq('effectiveRange', now))

    if has_field:
        query = query & Eq('enableAutopublishing', True)

    brains = catalog.evalAdvancedQuery(query)

    affected = 0
    total = 0
    for brain in brains:
        logger.info('Found %s' % brain.getURL())
        o = brain.getObject()
        eff_date = o.getEffectiveDate()
        exp_date = o.getExpirationDate()
        # The dates in the indexes are always set!
        # So unless we test for actual dates on the
        # objects, objects with no EffectiveDate are also published.
        # ipdb> brain.effective
        # Out[0]: DateTime('1000/01/01')
        # ipdb> brain.expires
        # Out[0]: DateTime('2499/12/31')

        # we only publish if:
        # a) the effective date is set and is in the past, and if
        # b) the expiration date has not been set or is in the future:
        if eff_date is not None and eff_date < now and \
          (exp_date is None or exp_date > now):
            logger.info('Publishing %s' % brain.getURL())
            total += 1
            if not settings.dry_run:
                try:
                    # this is a naive approach - and will throw an exception if the state
                    # don't provide the publish workflow action.
                    if has_field:
                        o.setEnableAutopublishing(False)
                    wf.doActionFor(o, 'publish')
                    o.reindexObject()
                    affected += 1
                except WorkflowException:
                    logger.info("""The state '%s' of the workflow associated with the
                                   object at '%s' does not provide the publish action
                                """ % (brain.review_state, o.getURL()))

    logger.info("""Ran collective.autopublishing. %d objects found, %d affected
                """ % (total, affected))
