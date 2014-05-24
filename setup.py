#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='curses-2048',
    version='1.4',
    description='2048 implementation with python and ncurses',
    long_description=readme + '\n\n' + history,
    author='Pablo Martin Medrano',
    author_email='pablo@odkq.com',
    url='https://github.com/odkq/curses-2048/',
    py_modules = ['2048'],
    include_package_data=True,
    install_requires=[
    ],
    license="GPL",
    zip_safe=False,
    keywords='2048',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console :: Curses',
        'Topic :: Games/Entertainment :: Puzzle Games',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    entry_points={'console_scripts': ['2048 = 2048:main']}
)
