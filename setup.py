#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

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
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.7',
        ],
    test_suite='tests',
    install_requires = [
        'scipy>=0.16.1',
        'sympy>=0.7.6.1',
        'pyparsing',
        'numpy',
        'matplotlib',
        'seaborn',
        'networkx>=2.2'],
    packages = ['crnsimulator'],
    entry_points = {
        'console_scripts': [
            'crnsimulator=crnsimulator.simulator:main'
            ],
        }
)

