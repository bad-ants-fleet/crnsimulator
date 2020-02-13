#!/usr/bin/env python

from setuptools import setup, find_packages

LONG_DESCRIPTION = """
Simulate chemical recation networks (CRNs) using ordinary differential
equations (ODEs).
"""

setup(
    name = 'crnsimulator',
    version = "0.7.1",
    description = 'Simulate CRNs using ODEs.',
    long_description = LONG_DESCRIPTION,
    author = 'Stefan Badelt',
    author_email = 'badelt@caltech.edu',
    url = 'https://github.com/bad-ants-fleet/crnsimulator',
    download_url = 'https://github.com/bad-ants-fleet/crnsimulator/archive/v0.7.1.tar.gz',
    license = 'MIT',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.7',
        ],
    install_requires = [
        'scipy>=0.16.1',
        'sympy>=0.7.6.1',
        'pyparsing',
        'numpy',
        'matplotlib',
        'seaborn',
        'networkx>=2.2'],
    packages = ['crnsimulator'],
    scripts = ['scripts/crnsimulator'],
    test_suite='tests'
)

