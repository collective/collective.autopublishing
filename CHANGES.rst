Changes
=======

1.0.3 (2019-07-18)
------------------

- Added French translation
  [laulaz]


1.0.2 (2017-05-23)
------------------

- Fix travis and buildout for Plone 5.0 and 5.1
  [tomgross]


1.0.1 (2016-02-18)
------------------

- Move README to rst
  [tomgross]


1.0 (2016-02-18)
----------------

- Plone 5 compatibility
  [tomgross]

0.6 (2013-11-05) Unreleased
---------------------------

Features:

- Added buildout configuration for test this package in plone 4
  [macagua]

- Added bash script for update po file
  [macagua]

- Added Spanish translation
  [macagua]

- Now it is possible to make time-based transitions of any workflow transition, and for individual content types.
  Rules are triggered on either the publication date or the retraction date.
  [sunew]

- Added initial dexterity support. date_index, date_index_method removed in the branch, needs to be reimplemented to support
  both dexterity and archetypes.
  [bosim]

0.5 (2013-10-21) Unreleased
---------------------------

Features:

- Added retracting
- Added modern control panel
- Replaced persistent utility with p.a.registry based settings
- Require event ticks to run as manager
- Depend on collective.timedevents
  [sunew]

Bugfixes:
 - don't make testing other modules fail
   [sunew]

0.4
----------------

 - Plone 4 compatibility
   [kroman0]

0.1
----------------
 - Initial package
   [mustap]

