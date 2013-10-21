from Products.Archetypes import atapi
from Products.ATContentTypes import content
from Products.Archetypes.ClassGen import generateMethods

enableAutopublishingField = atapi.BooleanField('enableAutopublishing',
            default = True,
            required = False,
            languageIndependent = True,
            isMetadata = True,
            schemata = 'dates',
            widget = atapi.BooleanWidget(
                description="Enables automatically publishing or retracting "
                            "this item when the publishing or the expiration date is "
                            "met. After an autopublishing event on this item, this "
                            "setting is set to false.",
                description_msgid = "help_enable_autopublishing",
                label = "Enable autopublishing",
                label_msgid = "label_enable_autopublishing",
                i18n_domain = "collective.autopublishing",
                visible={'view' : 'hidden',
                         'edit' : 'visible'},
                ),
            )

atct_types = (
               content.link.ATLink,
               content.image.ATImage,
               content.document.ATDocument,
               content.file.ATFile,
               content.event.ATEvent,
               content.newsitem.ATNewsItem,
               content.folder.ATFolder,
               content.topic.ATTopic,
             )


def makeTypesAutoPublishAware(types):
    """Adds enableAutopublishing field to types

    @param types: the classes to patch their schema
    @type types: list
    """
    for t in types:
        t.schema.addField(enableAutopublishingField.copy())
        t.schema.moveField('enableAutopublishing', after='expirationDate')
        generateMethods(t, t.schema.fields())


def makeATCTTypesAutoPublishAware():
    """Adds enableAutopublishing field to ATCT types"""
    makeTypesAutoPublishAware(atct_types)
    print "---------- PATCH: ADDED enableAutopublishing field TO ATCT TYPES ----------"

