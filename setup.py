from setuptools import setup

long_description = (
    open('README.md').read() +
    '\n' +
    open('CONTRIBUTORS.md').read() +
    '\n' +
    open('CHANGES.md').read() +
    '\n')

setup(name='collective.autopublishing',
      version='2.0.0.dev0',
      description="Publishes and retracts on effective or expired dates.",
      long_description=long_description,
      long_description_content_type='text/markdown',
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 6.1",
        "Framework :: Plone :: 6.2",
        "Framework :: Plone :: Addon",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3 :: Only",
        ],
      keywords='plone workflow publishing',
      author='Mustapha Benali',
      author_email='mustapha@headnet.dk',
      url='http://pypi.python.org/pypi/collective.autopublishing',
      license='GPLv2+',
      include_package_data=True,
      zip_safe=False,
      python_requires='>=3.10',
      extras_require=dict(
        test=[
            'plone.app.testing',
            'plone.app.robotframework[debug]',
            'interlude',
        ]
      ),
      install_requires=[
          'plone.api',
          'plone.app.registry>=1.2',
          'plone.z3cform',
          'collective.timedevents>=0.3',
          'collective.complexrecordsproxy',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
