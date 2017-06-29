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
    description='Simulate CRNs using ODEs.',
    long_description=readme,
    author='Stefan Badelt',
    author_email='badelt@caltech.edu',
    url='https://github.com/bad-ants-fleet/crnsimulator',
    license=license,
    install_requires=[
        'sympy>=0.7.6.1', 
        'scipy>=0.16.1', 
        'networkx>=1.10'],
    test_suite='tests',
    packages=['crnsimulator'],
    scripts=['scripts/crnsimulator']
)

