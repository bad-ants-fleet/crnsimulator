#!/usr/bin/env python

from setuptools import setup, find_packages

LONG_DESCRIPTION = """
Simulate chemical recation networks (CRNs) using ordinary differential
equations (ODEs).
"""

setup(
    name='crnsimulator',
    version="0.5",
    description='Simulate CRNs using ODEs.',
    long_description=LONG_DESCRIPTION,
    author='Stefan Badelt',
    author_email='badelt@caltech.edu',
    url='https://github.com/bad-ants-fleet/crnsimulator',
    license='MIT',
    install_requires=[
        'scipy>=0.16.1',
        'sympy>=0.7.6.1',
        'pyparsing',
        'numpy',
        'matplotlib',
        'seaborn',
        'networkx>=1.1'],
    test_suite='tests',
    packages=['crnsimulator'],
    scripts=['scripts/crnsimulator']
)

