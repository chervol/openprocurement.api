import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

requires = [
    'setuptools',
    'cornice',
    'waitress',
    'couchdb-schematics',
    'sphinxcontrib-httpdomain',
    'jsonpatch',
]
test_requires = requires + [
    'webtest',
    'python-coveralls',
]

entry_points = """\
[paste.app_factory]
main = openprocurement.api:main
"""

setup(name='openprocurement.api',
      version='0.2',
      description='openprocurement.api',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pylons",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
      ],
      keywords="web services",
      author='',
      author_email='',
      url='',
      package_dir = {'': 'src'},
      packages=find_packages('src'),
      namespace_packages = ['openprocurement'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=test_requires,
      extras_require={'test': test_requires},
      test_suite="openprocurement.api.tests.main.suite",
      entry_points = entry_points)
