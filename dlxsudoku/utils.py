#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`utils`
==================

.. module:: utils
    :platform: Unix, Windows
    :synopsis:

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2015-10-07, 09:22

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

try:
    range_ = xrange
except NameError:
    range_ = range


def get_list(n_rows, fill_with=0):
    return [fill_with, ] * n_rows


def get_list_of_lists(n_rows, n_cols, fill_with=0):
    return [get_list(n_rows, fill_with) for k in range(n_cols)]
