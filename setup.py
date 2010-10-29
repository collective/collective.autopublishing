from setuptools import setup, find_packages

version = '0.5'

setup(name='headnet.autopublish',
      version=version,
      description="Sets the workflow state to 'published' on publishing date if is specified",
      long_description="""\
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Mustapha Benali',
      author_email='mustapha@headnet.dk',
      url='http://www.headnet.dk',
      license='GPL',
      packages=find_packages('src'),
      package_dir = {'':'src'},
      namespace_packages=['headnet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'headnet.cronmanager', 
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
