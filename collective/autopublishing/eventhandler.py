# -*- coding: utf-8 -*-
import logging
from zope.component import ComponentLookupError, getUtility

from plone.registry.interfaces import IRegistry
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.AdvancedQuery import Eq, In, Le
from Products.CMFCore.utils import getToolByName

from collective.complexrecordsproxy import ComplexRecordsProxy
from browser.autopublishsettings import IAutopublishSettingsSchema

logger = logging.getLogger('collective.autopublishing')

#
# Event handler.
#
# Should be registered in zcml as subscribers to
# one of the tick events from collective.timedevents

def autopublish_handler(event):
    catalog = event.context.portal_catalog

    try:
        settings = getUtility(IRegistry).forInterface(
            IAutopublishSettingsSchema,
            omit=('publish_actions', 'retract_actions'),
            factory=ComplexRecordsProxy)
    except (ComponentLookupError, KeyError):
        logger.info('The product needs to be installed. No settings in the registry.')
        return

    if 'enableAutopublishing' not in catalog.indexes():
        logger.info('Catalog does not have a enableAutopublishing index')
        return

    p_result = handle_publishing(event, settings)
    r_result = handle_retracting(event, settings)

    if settings.email_log and (p_result or r_result):
        # Send audit mail
        messageText = 'Autopublishing results:\n' + p_result + '\n' + r_result
        email_addresses = settings.email_log
        mh = getToolByName(event.context, 'MailHost')
        portal = getToolByName(event.context, 'portal_url').getPortalObject()
        mh.send(messageText,
                mto=email_addresses,
                mfrom=portal.getProperty('email_from_address'),
                subject='Autopublishing results',
                encode=None,
                immediate=False,
                charset='utf8',
                msg_type=None)

def handle_publishing(event, settings):
    '''
    '''
    catalog = event.context.portal_catalog
    wf = event.context.portal_workflow
    now = event.context.ZopeTime()

    actions = settings.publish_actions
    action_taken = False
    audit = ''
    for a in actions:
        audit += ('\n\nAction triggered by Publishing Date:\n' + \
                 '  content types: \n%s\n' + \
                 '  initial state: %s\n' + \
                 '  transition: %s\n' + \
                 '  date_field: %s\n')\
                 % (str(a.portal_types), str(a.initial_state), str(a.transition),
                   str(a.date_field))

        query = (Eq('review_state', a.initial_state)
                 & Eq('effectiveRange', now)
                 & Eq('enableAutopublishing', True)
                 & In('portal_type', a.portal_types))

        brains = catalog.evalAdvancedQuery(query)
        affected = 0
        total = 0
        for brain in brains:
            o = brain.getObject()
            eff_date = o.getEffectiveDate()
            if a.date_field:
                try:
                    eff_date = o.getField(a.date_field).get(o)
                except:
                    pass
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
                logger.info('Transitioning (%s) %s' % (
                            brain.getURL(),
                            a.transition))
                audit += 'Transitioning (%s) %s\n' % (
                            brain.getURL(),
                            a.transition)
                total += 1
                action_taken = True
                if not settings.dry_run:
                    try:
                        wf.doActionFor(o, a.transition)
                        o.reindexObject()
                        affected += 1
                    except WorkflowException:
                        logger.info("""The state '%s' of the workflow associated with the
                                       object at '%s' does not provide the '%s' action
                                    """ % (brain.review_state,
                                           o.getURL()),
                                           str(a.transition))

        logger.info("""Ran collective.autopublishing (publish): %d objects found, %d affected
                    """ % (total, affected))
    if action_taken:
        return audit
    else:
        return ''

def handle_retracting(event, settings):
    '''
    '''
    catalog = event.context.portal_catalog
    wf = event.context.portal_workflow
    now = event.context.ZopeTime()

    actions = settings.retract_actions
    action_taken = False
    audit = ''
    for a in actions:
        audit += ('\n\nAction triggered by Expiration Date:\n' + \
                 '  content types: \n%s\n' + \
                 '  initial state: %s\n' + \
                 '  transition: %s\n') \
                 % (str(a.portal_types), str(a.initial_state), str(a.transition))

        query = (In('review_state', a.initial_state)
                 & Le('expires', now)
                 & Eq('enableAutopublishing', True)
                 & In('portal_type', a.portal_types))

        brains = catalog.evalAdvancedQuery(query)

        affected = 0
        total = 0
        for brain in brains:
            o = brain.getObject()
            exp_date = o.getExpirationDate()
            # The dates in the indexes are always set.
            # So we need to test on the objects if the dates
            # are set.

            # we only retract if:
            # the expiration date is set and is in the past:
            if exp_date is not None and exp_date < now:
                logger.info('Transitioning (%s) %s' % (
                            brain.getURL(),
                            a.transition))
                audit += 'Transitioning (%s) %s\n' % (
                            brain.getURL(),
                            a.transition)
                total += 1
                action_taken = True
                if not settings.dry_run:
                    try:
                        wf.doActionFor(o, a.transition)
                        o.reindexObject()
                        affected += 1
                    except WorkflowException:
                        logger.info("""The state '%s' of the workflow associated with the
                                       object at '%s' does not provide the '%s' action
                                    """ % (brain.review_state,
                                           o.getURL()),
                                           str(a.transition))

        logger.info("""Ran collective.autopublishing (retract): %d objects found, %d affected
                    """ % (total, affected))
    if action_taken:
        return audit
    else:
        return ''

def transition_handler(event):
    # set expiration date if not already set, when
    # depublishing, to make sure we do not autopublish
    # again if an effective date is set. Really, it is
    # the editors responsibility (the effective date should
    # be checked, but it is a common mistake
    # to expect withdrawal to private to be final.
    if not event.transition:
        return
    if not event.object:
        return
    now = event.object.ZopeTime()
    # todo: make states into a setting
    if event.transition.id in ['retract', 'reject']:
        overwrite = False
        try:
            settings = getUtility(IRegistry).forInterface(
                IAutopublishSettingsSchema,
                omit=('publish_actions', 'retract_actions'),
                factory=ComplexRecordsProxy)
        except (ComponentLookupError, KeyError):
            logger.info('The product needs to be installed. No settings in the registry.')
            settings = None
        if settings and settings.overwrite_expiration_on_retract:
            overwrite = True
        if event.object.getExpirationDate() is None or overwrite:
            event.object.setExpirationDate(now)
    if event.transition.id in ['publish']:
        overwrite = False
        try:
            settings = getUtility(IRegistry).forInterface(
                IAutopublishSettingsSchema,
                omit=('publish_actions', 'retract_actions'),
                factory=ComplexRecordsProxy)
        except (ComponentLookupError, KeyError):
            logger.info('collective.autopublishing needs to be installed. No settings in the registry.')
            settings = None
        if settings and settings.clear_expiration_on_publish:
            overwrite = True
        if overwrite:
            if event.object.getExpirationDate() < now:
                # to avoid immediate re-retraction
                event.object.setExpirationDate(None)

