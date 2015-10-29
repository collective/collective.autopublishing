# -*- coding: utf-8 -*-
from logging import getLogger


log = getLogger('collective.autopublishing:upgrades')


def runProfiles(site, profile_ids):
    """ """
    setup_tool = getattr(site, 'portal_setup')

    for profile_id in profile_ids:
        if hasattr(setup_tool, 'runAllImportStepsFromProfile'):
            if not profile_id.startswith('profile-'):
                profile_id = "profile-%s" % profile_id
            setup_tool.runAllImportStepsFromProfile(profile_id)
        else:
            setup_tool.setImportContext(profile_id)
            setup_tool.runAllImportSteps()
        log.info("Ran profile " + profile_id)


def runDefaultProfile(tool):
    """ Run default profile """
    site = tool.aq_parent
    runProfiles(site, ('collective.autopublishing:default',))


def runMigrateProfile(tool):
    """  """
    site = tool.aq_parent
    runProfiles(site, ('collective.autopublishing:migrate',))


def importDefaultProfileRegistry(tool):
    """ """
    site = tool.aq_parent
    setup_tool = getattr(site, 'portal_setup')
    setup_tool.runImportStepFromProfile(
        'profile-collective.autopublishing:default', 'plone.app.registry',
        run_dependencies=False)

# EOF
