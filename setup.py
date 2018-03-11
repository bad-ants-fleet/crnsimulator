# Python 3 compatibility
from __future__ import absolute_import

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

version = "0.3"

setup(
    name='crnsimulator',
    version=version,
    description='Simulate CRNs using ODEs.',
    long_description=readme,
    author='Stefan Badelt',
    author_email='badelt@caltech.edu',
    url='https://github.com/bad-ants-fleet/crnsimulator',
    license=license,
    install_requires=[
        'sympy>=0.7.6.1',
        'matplotlib',
        'scipy>=0.16.1',
        'networkx>=1.1'],
    test_suite='tests',
    packages=['crnsimulator'],
    scripts=['scripts/crnsimulator']
)
