# -*- coding: utf-8 -*-
import logging
from plone import api


log = logging.getLogger('collective.autopublishing')


def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('collective.autopublishing_various.txt') is None:
        return

    site = context.getSite()
    setup_indexes(site)


def setup_indexes(portal):
    ct = api.portal.get_tool(name='portal_catalog')
    catalog_indexes = ({'name': 'enableAutopublishing',
                        'type': 'FieldIndex', }, )
    catalog_columns = ()
    purge_existing_indexes = ()
    purge_existing_columns = ()
    new_metadata = False

    for idx in catalog_indexes:
        if idx['name'] in purge_existing_indexes and \
                idx['name'] in ct.indexes():
            ct.delIndex(idx['name'])
        if idx['name'] in ct.indexes():
            log.info("Found the '%s' index in the catalog, nothing changed.\n",  # noqa
                     idx['name'])
        else:
            ct.addIndex(**idx)
            print "Added '%s' (%s) to the catalog.\n" % (idx['name'],
                                                         idx['type'])
    for entry in catalog_columns:
        if entry in purge_existing_columns and entry in ct.schema():
            ct.delColumn(entry)
        if entry in ct.schema():
            log.info("Found '%s' in the catalog metadatas, nothing changed.\n",  # noqa
                     entry)
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

    if context.readDataFile('collective.autopublishing_migrate_various.txt') is None:  # noqa
        return


def variousUninstallSteps(context):
    """
    """

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('collective.autopublishing_uninstall_various.txt') is None:  # noqa
        return

# EOF
