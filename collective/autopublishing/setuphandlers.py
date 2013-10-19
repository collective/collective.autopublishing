# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from zope.component import getSiteManager
from Products.GenericSetup.utils import _resolveDottedName

def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('collective.autopublishing_various.txt') is None:
        return

    site = context.getSite()
    setup_components(site)
    setup_indexes(site)

def setup_components(site):
    myfactory="collective.autopublishing.settingsutil.AutopublishSettings"
    myinterface="collective.autopublishing.browser.autopublishsettings.IAutopublishSettingsSchema"
    provided = _resolveDottedName(myinterface)
    myfactory = myfactory and _resolveDottedName(myfactory) or None
    sm = getSiteManager(site)
    utilities = sm.registeredUtilities()

    for i in utilities:
        if provided == i.provided:
            print 'Utility implementing IAutopublishSettingsSchema already exists'
            return
    sm.registerUtility(myfactory(), provided, '')


def setup_indexes(portal):
    ct = getToolByName(portal, 'portal_catalog')

    catalog_indexes = ()
    catalog_indexes = (
      { 'name'  : 'enableAutopublishing',
        'type'  : 'FieldIndex',
        },
       )
    catalog_columns = ()
    purge_existing_indexes = ()
    purge_existing_columns = ()
    new_metadata = False

    for idx in catalog_indexes:
        if idx['name'] in purge_existing_indexes and idx['name'] in ct.indexes():
            ct.delIndex(idx['name'])
        if idx['name'] in ct.indexes():
            print "Found the '%s' index in the catalog, nothing changed.\n" % idx['name']
        else:
            ct.addIndex(**idx)
            print "Added '%s' (%s) to the catalog.\n" % (idx['name'], idx['type'])
    for entry in catalog_columns:
        if entry in purge_existing_columns and entry in ct.schema():
            ct.delColumn(entry)
        if entry in ct.schema():
            print "Found '%s' in the catalog metadatas, nothing changed.\n" % entry
        else:
            ct.addColumn(entry)
            print "Added '%s' to the catalog metadatas.\n" % entry
            new_metadata = True

    if new_metadata:
        print "Reindexing catalog... "
        ct.refreshCatalog()
        print "Done.\n"

def variousMigrateSteps(context):
    """ For migrating to newer versions of modules / other implementations etc.
    """

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('collective.autopublishing_migrate_various.txt') is None:
        return

    # Add additional setup code here
    portal = context.getSite()

    # EMPTY SO FAR.
