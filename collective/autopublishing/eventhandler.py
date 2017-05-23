# -*- coding: utf-8 -*-
import logging
from zope.component import ComponentLookupError, getUtility

from plone.registry.interfaces import IRegistry
from plone import api
from Products.CMFCore.WorkflowCore import WorkflowException

from collective.complexrecordsproxy import ComplexRecordsProxy
from browser.autopublishsettings import IAutopublishSettingsSchema
from interfaces import IBrowserLayer


logger = logging.getLogger('collective.autopublishing')

#
# Event handler.
#
# Should be registered in zcml as subscribers to
# one of the tick events from collective.timedevents


def getExpirationDate(obj):
    # Archetypes
    try:
        date = obj.getExpirationDate()
        return date
    # Handle dexterity
    except AttributeError:
        date = obj.expires()
        return date

    return None


def setExpirationDate(obj, date):
    obj.setExpirationDate(date)


def getEffectiveDate(obj):
    # Archetypes
    try:
        date = obj.getEffectiveDate()
        return date
    # Handle dexterity
    except AttributeError:
        date = obj.effective
        return date

    return None


def assemble_mail_text(record):
    messageText = record['header'] + '\n'
    messageText += "Content types:" + str(record['content_types'])
    messageText += "\nInitial state:" + str(record['initial_state'])
    messageText += "\nTransition:" + str(record['transition'])
    messageText += "\nActions:" + '\n'
    for action in record['actions']:
        messageText += "Transition:" + str(action['transition'])
        messageText += "\nPortal type:" + str(action['portal_type'])
        messageText += "\nTitle:" + str(action['title'])
        messageText += "\nUrl:" + str(action['url']) + '\n\n'
        messageText += '\n\n'
    return messageText


def autopublish_handler(event):
    catalog = api.portal.get_tool(name='portal_catalog')

    try:
        settings = getUtility(IRegistry).forInterface(
            IAutopublishSettingsSchema,
            omit=('publish_actions', 'retract_actions'),
            factory=ComplexRecordsProxy)
    except (ComponentLookupError, KeyError):
        logger.info('The product needs to be installed. '
                    'No settings in the registry.')
        return

    if 'enableAutopublishing' not in catalog.indexes():
        logger.info('Catalog does not have a enableAutopublishing index')
        return

    p_result = handle_publishing(event.context, settings,
                                 dry_run=settings.dry_run)
    r_result = handle_retracting(event.context, settings,
                                 dry_run=settings.dry_run)

    if settings.email_log and (p_result or r_result):
        # Send audit mail
        messageText = 'Autopublishing results.\n\n'

        messageText += 'Publish actions:\n'
        for record in p_result:
            messageText += assemble_mail_text(record)

        messageText += '\n\nRetract actions:\n'
        for record in r_result:
            messageText += assemble_mail_text(record)

        api.portal.send_email(
            body=messageText,
            recipient=settings.email_log,
            subject='Autopublishing results')


def handle_publishing(context, settings, dry_run=True, log=True):
    '''
    '''
    catalog = api.portal.get_tool(name='portal_catalog')
    wf = api.portal.get_tool(name='portal_workflow')
    now = context.ZopeTime()

    actions = settings.publish_actions
    action_taken = False
    audit = []
    for a in actions:
        audit_record = {}

        date_index = getattr(a, 'date_index', 'effective')

        audit_record['header'] = 'Actions triggered by "%s"' % str(date_index)
        audit_record['content_types'] = str(a.portal_types)
        audit_record['initial_state'] = str(a.initial_state)
        audit_record['transition'] = str(a.transition)
        audit_record['actions'] = []

        query = {'review_state': a.initial_state,
                 date_index: {'query': now, 'range': 'max'},
                 'enableAutopublishing': True,
                 'portal_type': a.portal_types}

        brains = catalog(**query)
        affected = 0
        total = 0
        for brain in brains:
            eff_date = brain.effective
            exp_date = brain.expires
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
            if (eff_date is not None and eff_date < now and
               (exp_date is None or exp_date > now)):
                audit_action = {}
                audit_action['portal_type'] = brain.portal_type
                audit_action['url'] = brain.getURL()
                audit_action['title'] = brain.Title
                audit_action['transition'] = a.transition
                if log:
                    logger.info(str(audit_action))
                total += 1
                action_taken = True
                if not dry_run:
                    try:
                        o = brain.getObject()
                        wf.doActionFor(o, a.transition)
                        o.reindexObject()
                        affected += 1
                    except WorkflowException:
                        logger.info(
                            """The state '%s' of the workflow associated with the
                               object at '%s' does not provide the '%s' action
                            """ % (brain.review_state,
                                   o.getURL()),
                            str(a.transition))
                audit_record['actions'].append(audit_action)

        if log:
            logger.info("""Ran collective.autopublishing (publish): %d objects found, %d affected
                    """ % (total, affected))
        audit.append(audit_record)
    if action_taken:
        return audit
    else:
        return []


def handle_retracting(context, settings, dry_run=True, log=True):
    '''
    '''
    catalog = api.portal.get_tool(name='portal_catalog')
    wf = api.portal.get_tool(name='portal_workflow')
    now = context.ZopeTime()

    actions = settings.retract_actions
    action_taken = False
    audit = []
    for a in actions:
        audit_record = {}

        date_index = getattr(a, 'date_index', 'effective')

        audit_record['header'] = 'Actions triggered by "%s"' % str(date_index)
        audit_record['content_types'] = str(a.portal_types)
        audit_record['initial_state'] = str(a.initial_state)
        audit_record['transition'] = str(a.transition)
        audit_record['actions'] = []

        query = {'review_state': a.initial_state,
                 date_index: {'query': now, 'range': 'max'},
                 'enableAutopublishing': True,
                 'portal_type': a.portal_types}
        brains = catalog(**query)

        affected = 0
        total = 0
        for brain in brains:

            exp_date = brain.expires
            # The dates in the indexes are always set.
            # So we need to test on the objects if the dates
            # are actually set.

            # we only retract if:
            # the expiration date is set and is in the past:
            if exp_date is not None and exp_date < now:
                audit_action = {}
                audit_action['portal_type'] = brain.portal_type
                audit_action['url'] = brain.getURL()
                audit_action['title'] = brain.Title
                audit_action['transition'] = a.transition
                if log:
                    logger.info(str(audit_action))
                total += 1
                action_taken = True
                if not dry_run:
                    try:
                        o = brain.getObject()
                        wf.doActionFor(o, a.transition)
                        o.reindexObject()
                        affected += 1
                    except WorkflowException:
                        logger.info(
                            """The state '%s' of the workflow associated with the
                               object at '%s' does not provide the '%s' action
                            """, brain.review_state, brain.getPath(), str(a.transition))  # noqa
                audit_record['actions'].append(audit_action)

        if log:
            logger.info("Ran collective.autopublishing (retract): %d objects found, %d affected",  # noqa
                        total, affected)
        audit.append(audit_record)
    if action_taken:
        return audit
    else:
        return []


def transition_handler(event):
    # set expiration date if not already set, when
    # depublishing, to make sure we do not autopublish
    # again if an effective date is set. Really, it is
    # the editors responsibility (the effective date should
    # be checked, but it is a common mistake
    # to expect withdrawal to private to be final.
    if not IBrowserLayer.providedBy(event.object.REQUEST):
        return
    if not event.transition:
        return
    if not event.object:
        return
    now = event.object.ZopeTime()
    # todo: make states into a setting
    if event.transition.id in ['retract', 'reject']:
        try:
            settings = getUtility(IRegistry).forInterface(
                IAutopublishSettingsSchema,
                omit=('publish_actions', 'retract_actions'),
                factory=ComplexRecordsProxy)
        except (ComponentLookupError, KeyError):
            logger.info('The product needs to be installed.'
                        ' No settings in the registry.')
            settings = None
        overwrite = settings and settings.overwrite_expiration_on_retract
        if getExpirationDate(event.object) is None or overwrite:
            setExpirationDate(event.object, now)
    if event.transition.id in ['publish']:
        try:
            settings = getUtility(IRegistry).forInterface(
                IAutopublishSettingsSchema,
                omit=('publish_actions', 'retract_actions'),
                factory=ComplexRecordsProxy)
        except (ComponentLookupError, KeyError):
            logger.info('collective.autopublishing needs to be installed.'
                        ' No settings in the registry.')
            settings = None
        if settings and settings.clear_expiration_on_publish:
            if getExpirationDate(event.object) < now:
                # to avoid immediate re-retraction
                setExpirationDate(event.object, None)
