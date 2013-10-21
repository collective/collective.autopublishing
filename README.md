# collective.autopublishing

## Package under construction

## Overview

Publishes or retracts Plone content items depending on the effective and expiration dates.

This package depends on collective.timedevents to supply zope3-style events with specific intervals.

## Setup

The module supplies an event handler. In your own module you have to register this handler for an event, for instance one of the time-based events from collective.timedevents.

Example:

     <subscriber
        for="collective.timedevents.interfaces.IIntervalTicks15Event"
        handler="collective.autopublishing.eventhandler.AutoPublishHandler"

To enable the event ticks from collective.timedevents you can either use zope clockserver or a cronjob as the trigger. (See the documentation for collective.timedevents to set this up).

The module adds a plone control panel, where intitial workflow states for both publishing and retracting has to be set.

In addition, simulating the publishing process is possible with the dry-run setting in the control panel.

## The publishing process

All items that are in the workflow states set in the control panel, having an effective date in the past, and no expiration date or an expiration date in the future, are published. (The workflow transition 'publish' are tried).

All items that are in the workflow states set in the control panel, having an expiration date in the past are retracted. (The workflow transition 'retract' are tried).

## Archetypes field

Unless disabled in zope.conf, the module adds a field `enableAutopublishing` to Archetypes content types.

To enable autopublishing (or retracting) this has to be set on every content instance.

The use of the field can be disabled in zope.conf. You can do that via buildout by adding this bit to your instance section:

    zope-conf-additional =
        <product-config collective.autopublishing>
          add-enableautopublishing-field off
        </product-config>

If disabled, only the initial workflow states and the effective and expiration dates control the publishing or retracting of content.


## Todo

Add a behavior for dexterity.

Modernize the patching of types.

What if an object is published, but effective date are in the future? Should we retract, to enforce that the workflow state always mirrors the setting of the dates?

What if the effective date is larger that expiration date? Can this happen?


