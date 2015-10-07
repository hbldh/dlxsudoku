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

import os

from nose.tools import raises

from hbldhdoku.sudoku import Sudoku
from hbldhdoku.exceptions import SudokuException


class TestSudoku(object):
    """Test Suite for Sudoku solver."""

    def __init__(self):
        self.test_dir = os.path.dirname(os.path.abspath(__file__))

    def test_solve_simple_sudoku(self):
        s = Sudoku.load_sudoku(os.path.join(self.test_dir, 'simple.sud'))
        s.solve()
        correct_solution = Sudoku.load_sudoku(os.path.join(self.test_dir, 'simple_sol.sud'))
        assert s == correct_solution

    def test_solve_medium_sudoku(self):
        s = Sudoku.load_sudoku(os.path.join(self.test_dir, 'medium.sud'))
        s.solve()
        correct_solution = Sudoku.load_sudoku(os.path.join(self.test_dir, 'medium_sol.sud'))
        assert s == correct_solution

    @raises(SudokuException)
    def test_solve_hard_sudoku(self):
        s = Sudoku.load_sudoku(os.path.join(self.test_dir, 'hard.sud'))
        s.solve()
        correct_solution = Sudoku.load_sudoku(os.path.join(self.test_dir, 'hard_sol.sud'))
        assert s == correct_solution