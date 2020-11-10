#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name = 'crnsimulator',
    version = "0.9",
    description = 'Simulate CRNs using ODEs.',
    long_description = LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author = 'Stefan Badelt',
    author_email = 'bad-ants-fleet@posteo.eu',
    maintainer = 'Stefan Badelt',
    maintainer_email = 'bad-ants-fleet@posteo.eu',
    url = 'https://github.com/bad-ants-fleet/crnsimulator',
    license = 'MIT',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Science/Research',
        ],
    python_requires = '>=3.7',
    install_requires = [
        'scipy>=0.16.1',
        'sympy>=0.7.6.1',
        'pyparsing',
        'numpy',
        'matplotlib',
        'seaborn'],
    packages = find_packages(),
    test_suite = 'tests',
    entry_points = {
        'console_scripts': [
            'crnsimulator=crnsimulator.simulator:main'
            ],
        }
)

