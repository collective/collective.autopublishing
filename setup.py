from setuptools import setup, find_packages
import os

version = '0.7'

def read(*pathnames):
    return open(os.path.join(os.path.dirname(__file__), *pathnames)).read().\
           decode('utf-8')

setup(name='collective.autopublishing',
      version=version,
      description="Publishes and retracts on effective or expired dates.",
      long_description='\n'.join([
          read('README.md'),
          read('CHANGES.rst'),
          ]),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
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
            'collective.testcaselayer',
        ]
      ),
      install_requires=[
          'setuptools',
          'plone.app.registry>=1.2',
          'plone.z3cform',
          'Products.AdvancedQuery',
          'collective.timedevents>=0.3',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
