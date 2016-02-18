=========================
collective.autopublishing
=========================

Overview
========

.. image:: https://travis-ci.org/collective/collective.autopublishing.svg?branch=master
       :target: https://travis-ci.org/collective/collective.autopublishing

Publishes or retracts Plone content items depending on the effective and expiration dates.

This package depends on collective.timedevents to supply zope3-style events with specific intervals.

Setup
=====

The module supplies an event handler. In your own module you have to register this handler for an event, for instance one of the time-based events from collective.timedevents.

Example: ::

     <subscriber
        for="collective.timedevents.interfaces.IIntervalTicks15Event"
        handler="collective.autopublishing.eventhandler.autopublish_handler"

To enable the event ticks from collective.timedevents you can either use zope clockserver or a cronjob as the trigger. (See the documentation for collective.timedevents to set this up).

The module adds a plone control panel, where intitial workflow states for both publishing and retracting has to be set.

In addition, simulating the publishing process is possible with the dry-run setting in the control panel.

The publishing process
======================

All items that are in the workflow states set in the control panel, having an effective date in the past, and no expiration date or an expiration date in the future, are published. (The workflow transition 'publish' are tried).

All items that are in the workflow states set in the control panel, having an expiration date in the past are retracted. (The workflow transition 'retract' are tried).

Archetypes field
================

The module adds a field `enableAutopublishing` to Archetypes content types, with default set to True.

When am autopublishing event happens to an item, this is set to False, to mark that autopublishing has run.

Setting the expiration date on retraction
=========================================

In some cases, the automatic publication can republish an item that is retracted.

For instance: if private is added to initial publication states, and we have a published content object with a publication date in the past.

If the expiration date is not set, and the item is (manually) retracted, the publication machinery will republish the item unless the editor clears the publication date or turns of autopublishing for the item with the `enableAutopublishing` option.

To solve that problem an event handler for workflow transitions sets the expiration date, if it is not already set, when withdrawing an item.

There is a control panel setting to allow overwriting the expiration date.

Audit
=====
A very simple form of audit logging can be done: If email addresses are supplied in the control panel a mail will be sent with info about published and retracted items.

Todo
====

 - What if an object is in the state published, but effective date are in the future? Should we retract, to enforce that the workflow state always mirrors the setting of the dates?

 - What if the effective date is larger that expiration date? Can this happen?

