#!/usr/bin/env python

"""Setting up script for Reltools."""

import os

import setuptools

from reltools import (
    __version__ as VERSION,
    __author__ as AUTHOR,
    __author_email__ as AUTHOR_EMAIL,
)


URL = 'https://github.com/ymoch/reltools'


def load_long_description():
    """Load the long description."""
    readme_file_path = os.path.join(os.path.dirname(__file__), 'README.rst')
    with open(readme_file_path) as readme_file:
        return readme_file.read()


setuptools.setup(
    name='reltools',
    description='Relation tools for Python.',
    long_description=load_long_description(),
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license='MIT',
    py_modules=[
        'reltools',
    ],
    install_requires=[
        'more-itertools',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-pep8',
        'pytest-flakes',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
