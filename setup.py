# -*- coding: utf-8 -*-
"""
:mod:`setup`
============

.. module:: setup
    :platform: Unix, Windows
    :synopsis: The Python Packaging setup file for Empyrean.

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2015-09-17, 12:39

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from setuptools import setup, find_packages

setup(
    name='hbldhdoku',
    version='0.1.0',
    author='Henrik Blidh',
    author_email='henrik.blidh@nedomkull.com',
    description='Sudoku Solver',
    long_description="TBD",
    license='MIT',
    url='https://github.com/hbldh/hbldhdoku',
    packages=find_packages(),
    install_requires=[line.strip() for line in open("requirements.txt")],
    package_data={'tests': ['*.sud', ]},
    dependency_links=[],
    ext_modules=[],
)
