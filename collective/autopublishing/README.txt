headnet.autopublish
===================


setup
=====

First we check that our patch is applied to all atct types::

    >>> from headnet.autopublish.patch_types import atct_types, PublishOnDateField
    >>> False in ['publishOnDate' in tp.schema for tp in atct_types]
    False

that our package is installed::

    >>> portal.portal_quickinstaller.isProductInstalled('headnet.autopublish')
    True

and that a catalog index named ``publishOnDate`` is added::

    >>> 'publishOnDate' in portal.portal_catalog.indexes() 
    True


Add objects for testing
=======================

Let's create some objects for our tests::

    >>> self.loginAsPortalOwner()

    >>> portal.invokeFactory(id='document1', type_name='Document', title='Document 1')
    'document1'

    >>> portal.invokeFactory(id='news1', type_name='News Item', title='News 1')
    'news1'

Set their 'PuplishOndate' field to true and their review state to pending. 
First here is what we have. Our objects have their publishOnDate set to false
and their review state set to private::

    >>> wf = portal.portal_workflow

    >>> portal['document1'].getPublishOnDate(), wf.getInfoFor(portal['document1'], 'review_state')
    (False, 'private')

    >>> portal['news1'].getPublishOnDate(), wf.getInfoFor(portal['news1'], 'review_state')
    (False, 'private')

and modify them::

    >>> portal['document1'].setPublishOnDate(True)
    >>> portal['news1'].setPublishOnDate(True)

    >>> wf.doActionFor(portal['document1'], 'submit')
    >>> wf.doActionFor(portal['news1'], 'submit')

    >>> portal['document1'].getPublishOnDate(), wf.getInfoFor(portal['document1'], 'review_state')
    (True, 'pending')

    >>> portal['news1'].getPublishOnDate(), wf.getInfoFor(portal['news1'], 'review_state')
    (True, 'pending')

we have to reindex the objects::

    >>> portal['document1'].reindexObject()
    >>> portal['news1'].reindexObject()

tests
=====

Let's fire the hourly cronjob as anonymous use. Am I already anonymous user?::
 
    >>> bool(portal.portal_membership.isAnonymousUser())
    False

No, let's logout::

    >>> self.logout()
    >>> bool(portal.portal_membership.isAnonymousUser())
    True

Now let's fire the cronjob::

    >>> portal.restrictedTraverse('@@cron_hourly')()
    'done...'

Check that our test objects are published and their publishOnDate fields are
set to False::

    >>> portal['document1'].getPublishOnDate(), wf.getInfoFor(portal['document1'], 'review_state')
    (False, 'published')

    >>> portal['news1'].getPublishOnDate(), wf.getInfoFor(portal['news1'], 'review_state')
    (False, 'published')


