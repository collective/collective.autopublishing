# Changelog

<!-- towncrier release notes start -->

## 2.0.0 (unreleased)


- Breaking: replace the `pkg_resources` namespace of `collective` with a
  PEP 420 native namespace, and move the package to a `src/` layout.
  Support Plone 6.1 only on Python 3.10 to 3.13, and Plone 6.2 on Python
  3.10 to 3.14. Use 1.1b1 for Plone 5.2 and 6.0.
  [remdub]

- Register the views for `IPloneSiteRoot` from `plone.base` instead of the
  alias Plone 6.2 deprecates. The test layer no longer imports
  `plone.app.contenttypes.testing`, which needs `plone.app.robotframework`.
  New tests for the control panel and the report view. Drop the
  superfluous `for` of the behavior registration.
  [remdub]

- Make the report view translatable (it used the `eva.content` domain and
  had no i18n markup) and translate it in French. Fix the "What actions
  will be taken" link text.
  [remdub]

- Configure the package with plone.meta 2.12.0 (test matrix on Plone 6.2.3
  and 6.1), move its metadata to `pyproject.toml`, convert the documentation
  to Markdown and run the development environment on Plone 6.2.3 with uv
  instead of buildout. Drop the buildout configuration and the hand-written
  GitHub workflow. Until collective.timedevents is released without
  `pkg_resources`, the tests and the development environment use its
  `plone62` branch.
  [remdub]


## 1.1b1 (2022-11-25)

- Drop Python 2 / Archetypes compatibility
  [laulaz]

- Python 3 / Plone 6 compatibility
  [boulch, laulaz]

- Fix traceback / improve & harmonize log messages
  [laulaz]


## 1.0.3 (2019-07-18)

- Added French translation
  [laulaz]


## 1.0.2 (2017-05-23)

- Fix travis and buildout for Plone 5.0 and 5.1
  [tomgross]


## 1.0.1 (2016-02-18)

- Move README to rst
  [tomgross]


## 1.0 (2016-02-18)

- Plone 5 compatibility
  [tomgross]


## 0.6 (2013-11-05) Unreleased

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


## 0.5 (2013-10-21) Unreleased

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


## 0.4

- Plone 4 compatibility
  [kroman0]


## 0.1

- Initial package
  [mustap]
