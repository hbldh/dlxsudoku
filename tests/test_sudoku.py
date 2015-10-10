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
from hbldhdoku.exceptions import SudokuException, SudokuHasNoSolutionError, SudokuTooDifficultError


class TestSudoku(object):
    """Test Suite for Sudoku solver."""

    def __init__(self):
        self.test_dir = os.path.dirname(os.path.abspath(__file__))

    def test_solve_simple_sudoku(self):
        s = Sudoku.load(os.path.join(self.test_dir, 'simple.sud'))
        s.solve()
        correct_solution = Sudoku.load(os.path.join(self.test_dir, 'simple_sol.sud'))
        assert s == correct_solution

    def test_solve_medium_sudoku(self):
        s = Sudoku.load(os.path.join(self.test_dir, 'medium.sud'))
        s.solve()
        correct_solution = Sudoku.load(os.path.join(self.test_dir, 'medium_sol.sud'))
        assert s == correct_solution

    def test_solve_hard_sudoku(self):
        s = Sudoku.load(os.path.join(self.test_dir, 'hard.sud'))
        s.solve(verbose=True)
        correct_solution = Sudoku.load(os.path.join(self.test_dir, 'hard_sol.sud'))
        assert s == correct_solution

    @raises(SudokuTooDifficultError)
    def test_solve_very_hard_sudoku(self):
        s = Sudoku.load(os.path.join(self.test_dir, 'very_hard.sud'))
        s.solve(verbose=True)
        correct_solution = Sudoku.load(os.path.join(self.test_dir, 'very_hard_sol.sud'))
        assert s == correct_solution

    @raises(SudokuHasNoSolutionError)
    def test_raises_error_when_unsolvable(self):
        s = Sudoku.load(os.path.join(self.test_dir, 'hard.sud'))
        s._matrix[0][0] = 2
        s.solve()

    def test_equality(self):
        s = Sudoku.load(os.path.join(self.test_dir, 'hard_sol.sud'))
        s2 = Sudoku.load(os.path.join(self.test_dir, 'medium_sol.sud'))
        s3 = Sudoku.load(os.path.join(self.test_dir, 'hard_sol.sud'))
        assert s != s2
        assert s == s3
        assert s != 5

    def test_print(self):
        s = Sudoku.load(os.path.join(self.test_dir, 'hard_sol.sud'))
        print(s)
