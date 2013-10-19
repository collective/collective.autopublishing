from setuptools import setup, find_packages

version = '0.5'

setup(name='collective.autopublishing',
      version=version,
      description="Publishes and retracts on effective or expired dates.",
      long_description="""\
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Mustapha Benali',
      author_email='mustapha@headnet.dk',
      url='http://pypi.python.org/pypi/collective.autopublishing',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages = ['collective'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
        test=[
            'Products.PloneTestCase',
        ]
      ),
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'headnet.cronmanager',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
