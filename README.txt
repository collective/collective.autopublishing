collective.autopublishing Package Readme
========================================

Overview
--------

Sets the workflow state to 'published' on publishing date if is specified

This package depends on headnet.cronmanager

Install
=======

You have to add the state to publish and if we have to patch
atct types in your buildout.cfg file in the zope instance section.
For example, to publish the ``pending``
state::

   zope-conf-additional =
                 <product-config headnet.autopublish>
                      state-to-publish pending
                      add-publishondate-index yes
                 </product-config>



