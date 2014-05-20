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
    version='0.2.0',
    description='2048 implementation with python and ncurses',
    long_description=readme + '\n\n' + history,
    author='Pablo Martin <>',
    author_email='pablo@odkq.com',
    url='https://github.com/odkq/curses-2048/',
    py_modules = ['2048'],
    include_package_data=True,
    install_requires=[
    ],
    license="GPL",
    zip_safe=False,
    keywords='pyxkcdpass',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    entry_points={'console_scripts': ['2048 = 2048:main']}
)
