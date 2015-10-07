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

import six


def get_list(n_rows, fill_with=0.0):
    return [fill_with, ] * n_rows


def get_list_of_lists(n_rows, n_cols, fill_with=0):
    return [get_list(n_rows, fill_with) for k in six.moves.range(n_cols)]


def get_lists_array(n_rows):
    """Returns a list of empty lists.

    :param n_rows: Desired length of the array.
    :type n_rows: int
    :return: A list of length n_rows with empty lists at each position.
    :rtype: list

    """
    return [list() for x in six.moves.range(n_rows)]


def get_lists_matrix(n_rows, n_cols):
    """Returns a list of lists of empty lists.

    :param n_rows: Desired row length of the matrix.
    :type n_rows: int
    :param n_rows: Desired column length of the matrix.
    :type n_rows: int
    :return: A list of length n_rows with lists of length n_cols with
             empty lists at each position.
    :rtype: list

    """
    return [get_lists_array(n_rows) for k in six.moves.range(n_cols)]


def sum_lists_matrix(A):
    out = 0
    for row in A:
        for element in row:
            out += sum(element)
    return out


def sum_lists_matrix_row(A, i):
    out = 0
    for element in A[i]:
        out += sum(element)
    return out


def sum_lists_matrix_column(A, j):
    out = 0
    for row in A:
        out += sum(row[j])
    return out

