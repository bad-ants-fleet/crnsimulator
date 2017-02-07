#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
  readme = f.read()

with open('LICENSE') as f:
  license = f.read()

# Dynamically figure out the version
version = __import__('crnsimulator').__version__

setup(
    name='crnsimulator',
    version=version,
    description='CRN-to-ODE translator',
    long_description=readme,
    author='Stefan Badelt',
    author_email='badelt@caltech.edu',
    #url='http://github...',
    license=license,
    install_requires=[
        'sympy>=0.7.6.1', 
        'argparse>=1.2.1', 
        'scipy>=0.16.1', 
        'networkx>=1.10'],
    test_suite='tests',
    packages=['crnsimulator'],
    include_package_data=True,
    scripts=['scripts/crnsimulator']
)

