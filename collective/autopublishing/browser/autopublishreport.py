# -*- coding: utf-8 -*-
import logging
from zope.component import ComponentLookupError, getUtility

from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.registry.interfaces import IRegistry

from collective.complexrecordsproxy import ComplexRecordsProxy
from autopublishsettings import IAutopublishSettingsSchema
from collective.autopublishing.eventhandler import (
    handle_publishing,
    handle_retracting
    )

logger = logging.getLogger('collective.autopublishing')


class AutopublishReport(BrowserView):

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    __call__ = ViewPageTemplateFile('autopublish_report.pt')

    @property
    def report(self):
        catalog = getToolByName(self.context, 'portal_catalog')

        try:
            settings = getUtility(IRegistry).forInterface(
                IAutopublishSettingsSchema,
                omit=('publish_actions', 'retract_actions'),
                factory=ComplexRecordsProxy)
        except (ComponentLookupError, KeyError):
            logger.info('The product needs to be installed. No settings in the'
                        ' registry.')
            return

        if 'enableAutopublishing' not in catalog.indexes():
            logger.info('Catalog does not have a enableAutopublishing index')
            return

        p_result = handle_publishing(self.context, settings,
                                     dry_run=True, log=False)
        r_result = handle_retracting(self.context, settings,
                                     dry_run=True, log=False)

        result = {}
        result['p_result'] = p_result
        result['r_result'] = r_result
        return result
