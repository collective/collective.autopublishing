import logging
from App.config import getConfiguration
from AccessControl.SecurityManagement import newSecurityManager
from zope.component import getUtility
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.AdvancedQuery import Eq, In, Le, Ge, And
from browser.autopublishsettings import IAutopublishSettingsSchema


logger = logging.getLogger('collective.autopublishing')

#
# Cron job handler
#
# should be registered in the ZCML file as subscribers to
# one of:
#  headnet.cronmanager.interfaces.ICronHourlyEvent
#  headnet.cronmanager.interfaces.ICronDailyEvent
#  headnet.cronmanager.interfaces.ICronWeeklyEvent
#  headnet.cronmanager.interfaces.ICronMonthlyEvent
# events


def get_config_value(key, default=None):
    """return a package config param"""
    config = getConfiguration().product_config
    autopublish_config = config.get('collective.autopublishing', {})
    value = autopublish_config.get(key, default)
    return value

def getStatesToPublish():
    """Get state to publish from the persistent utility"""
    myutil = getUtility(IAutopublishSettingsSchema)
    return [s.encode('utf-8') for s in myutil.initial_states_publishing]

# TODO rename
def has_enableautopublishing_field():
    return get_config_value('add-enableautopublishing-field', 'yes') in ['yes', 'true', 'on']

def dry_run():
    return get_config_value('dry-run', 'yes') in ['yes', 'true', 'on']


def CronAutoPublishHandler(event):
    '''
    '''
    context = event.context

    catalog = context.portal_catalog
    wf = context.portal_workflow

    #wrap with new security
    originalUser = context.portal_membership.getAuthenticatedMember()
    newSecurityManager(context.REQUEST, originalUser)
    user = context.getWrappedOwner()
    newSecurityManager(context.REQUEST, user)

    has_enableautopublishing_field = has_enableautopublishing_field()

    if has_enableautopublishing_field and 'enableAutopublishing' not in catalog.indexes():
        logger.info('Catalog does not have a enableAutopublishing index')
        return

    states_to_publish = getStatesToPublish()
    if not states_to_publish:
        logger.info('You have to define state-to-publish in the plone control panel')
        return

    # TODO: move to eva
    # For EvaProject instances we need to look at the date in the
    # field projectPublicationDate.
    query_normal = (In('review_state', states_to_publish) \
            & Eq('effectiveRange', context.ZopeTime()) \
            & ~ Eq('portal_type', 'EvaProject'))

    query_project = (Eq('review_state', 'in_progress') \
            & Le('getProjectPublicationDate', context.ZopeTime()) \
            & Eq('portal_type', 'EvaProject'))

    if has_enableautopublishing_field:
        query_normal = query_normal & Eq('enableAutopublishing', True)
        query_project = query_project & Eq('enableAutopublishing', True)

    query = query_normal | query_project
    brains = catalog.evalAdvancedQuery(query)

    affected = 0
    total = 0
    for brain in brains:
        logger.debug('Found %s' % brain.getURL())
        o = brain.getObject()
        eff_date = o.getEffectiveDate()
        # The dates in the indexes are always set, see below. So unless we test for actual
        # dates on the objects, objects with no EffectiveDate are also published.
        # ipdb> brain.effective
        # Out[0]: DateTime('1000/01/01')
        # ipdb> brain.expires
        # Out[0]: DateTime('2499/12/31')
        if eff_date:
            logger.info('Publishing %s' % brain.getURL())
            total += 1
            if not dry_run():
                try:
                    # this is a naive approach - and will throw an exception if the state
                    # don't provide the publish workflow action.
                    if has_enableautopublishing_field:
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
    #set back the security
    newSecurityManager(context.REQUEST, originalUser)

