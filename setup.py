from setuptools import setup, find_packages

long_description = (
    open('README.rst').read() +
    '\n' +
    'Contributors\n' +
    '============\n' +
    '\n' +
    open('CONTRIBUTORS.rst').read() +
    '\n' +
    open('CHANGES.rst').read() +
    '\n')

setup(name='collective.autopublishing',
      version='1.0.3',
      description="Publishes and retracts on effective or expired dates.",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        ],
      keywords='plone workflow publishing',
      author='Mustapha Benali',
      author_email='mustapha@headnet.dk',
      url='http://pypi.python.org/pypi/collective.autopublishing',
      license='GPLv2+',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages = ['collective'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
        test=[
            'plone.app.testing',
            'plone.app.robotframework[debug]',
            'interlude',
        ]
      ),
      install_requires=[
          'setuptools',
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
