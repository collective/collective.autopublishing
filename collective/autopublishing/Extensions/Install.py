from Products.CMFCore.utils import getToolByName


def install(self):
    setup_tool = getToolByName(self, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-collective.autopublishing:default')
    return "Imported install profile."


def uninstall(self, reinstall=False):
    if reinstall:
        return "Uninstall profile skipped"
    setup_tool = getToolByName(self, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-collective.autopublishing:uninstall')
    return "Imported uninstall profile."
