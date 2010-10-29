from Products.Archetypes import atapi
from Products.ATContentTypes import content
from Products.Archetypes.ClassGen import generateMethods

PublishOnDateField = atapi.BooleanField('publishOnDate',
                                  default = False,
                                  required = False,
                                  languageIndependent = True,
                                  isMetadata = True,
                                  schemata = 'settings',
                                  widget = atapi.BooleanWidget(
                                            description="If selected and the publishing date is set, the workflow of this item will be set to published at the publishing date",
                                            description_msgid = "help_publish_on_date",
                                            label = "Set workflow to published",
                                            label_msgid = "label_publish_on_date",
                                            i18n_domain = "headnet.autopublish",
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
               content.favorite.ATFavorite,
               content.topic.ATTopic,
             )


def makeTypesAutoPublishAware(types):
    """Adds PublishOnDateField to types

    @param types: the classes to patch their schema
    @type types: list
    """
    for t in types:
        t.schema.addField(PublishOnDateField.copy())
        t.schema.moveField('publishOnDate', after='effectiveDate')
        generateMethods(t, t.schema.fields())


def makeATCTTypesAutoPublishAware():
    """Adds PublishOnDateField to ATCT types"""
    makeTypesAutoPublishAware(atct_types)
    print "---------- PATCH: ADDED PublishOnDate TO ATCT TYPES ----------"
    
