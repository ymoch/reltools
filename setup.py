#!/usr/bin/env python

"""Setting up script for Reltools."""

import setuptools

from reltools import (
    __version__ as VERSION,
    __author__ as AUTHOR,
    __author_email__ as AUTHOR_EMAIL,
)


URL = 'https://github.com/ymoch/reltools'


# TODO: Set the long description.
setuptools.setup(
    name='reltools',
    description='Relation tools for Python.',
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    py_modules=['reltools'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov', 'pytest-pep8'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
