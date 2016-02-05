#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`exceptions`
==================

.. module:: exceptions
    :platform: Unix, Windows
    :synopsis: 

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2015-09-29, 23:18

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import


class SudokuException(Exception):
    pass


class SudokuTooDifficultError(SudokuException):
    """Raised when this solver is too incompetent to solve this Sudoku."""
    pass


class SudokuHasNoSolutionError(SudokuException):
    """Raised when no solution is possible for this Sudoku."""
    pass


class SudokuHasMultipleSolutionsError(SudokuException):
    """Raised when more than one solution is available for this Sudoku."""
    pass
