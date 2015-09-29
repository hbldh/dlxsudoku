#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`test_sudoku`
==================

.. module:: test_sudoku
    :platform: Unix, Windows
    :synopsis: 

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>

Created on 2015-09-29, 23:31

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from hbldhdoku.sudoku import Sudoku
from hbldhdoku.exceptions import SudokuException


class TestSudoku(object):
    """Test Suite for Sukoku solver."""

    def test_solve_simple_sudoku(self):
        s = Sudoku.load_sudoku('./simple.sud')
        s.solve()
        correct_solution = Sudoku.load_sudoku('./simple_sol.sud')
        assert s == correct_solution

    def test_solve_medium_sudoku(self):
        s = Sudoku.load_sudoku('./medium.sud')
        s.solve()
        correct_solution = Sudoku.load_sudoku('./medium_sol.sud')
        assert s == correct_solution
