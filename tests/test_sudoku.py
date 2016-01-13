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
try:
    import urllib.request as urlrequest
except ImportError:
    import urllib as urlrequest

from nose.tools import raises

from dlxsudoku.sudoku import Sudoku
from dlxsudoku.utils import range_
from dlxsudoku.exceptions import SudokuException, SudokuHasNoSolutionError, SudokuTooDifficultError


class TestSudoku(object):
    """Test Suite for Sudoku solver."""

    def __init__(self):
        self.test_dir = os.path.dirname(os.path.abspath(__file__))

    def test_solve_simple_sudoku(self):
        s = Sudoku.load_file(os.path.join(self.test_dir, 'simple.sud'))
        s.solve()
        correct_solution = Sudoku.load_file(os.path.join(self.test_dir, 'simple_sol.sud'))
        assert s == correct_solution

    def test_solve_simple_sudoku_read_from_flat_file(self):
        s = Sudoku.load_file(os.path.join(self.test_dir, 'simple_flat.sud'))
        s.solve()
        correct_solution = Sudoku.load_file(os.path.join(self.test_dir, 'simple_sol.sud'))
        assert s == correct_solution

    def test_solve_medium_sudoku(self):
        s = Sudoku.load_file(os.path.join(self.test_dir, 'medium.sud'))
        s.solve()
        correct_solution = Sudoku.load_file(os.path.join(self.test_dir, 'medium_sol.sud'))
        assert s == correct_solution

    def test_solve_hard_sudoku(self):
        s = Sudoku.load_file(os.path.join(self.test_dir, 'hard.sud'))
        s.solve(verbose=True)
        correct_solution = Sudoku.load_file(os.path.join(self.test_dir, 'hard_sol.sud'))
        assert s == correct_solution

    def test_to_oneliner_method(self):
        s = Sudoku.load_file(os.path.join(self.test_dir, 'hard.sud'))
        s.solve(verbose=True)
        correct_solution = Sudoku.load_file(os.path.join(self.test_dir, 'hard_sol.sud'))
        assert s == correct_solution
        oneliner = s.to_oneliner()
        oneliner_parsed = Sudoku(oneliner)
        assert oneliner_parsed == correct_solution

    @raises(SudokuTooDifficultError)
    def test_solve_very_hard_sudoku_raises_error_if_brute_force_disallowed(self):
        s = Sudoku.load_file(os.path.join(self.test_dir, 'very_hard.sud'))
        s.solve(verbose=True, allow_brute_force=False)
        correct_solution = Sudoku.load_file(os.path.join(self.test_dir, 'very_hard_sol.sud'))
        assert s == correct_solution

    def test_solve_very_hard_sudoku_with_brute_force(self):
        s = Sudoku.load_file(os.path.join(self.test_dir, 'very_hard.sud'))
        s.solve(verbose=True, allow_brute_force=True)
        correct_solution = Sudoku.load_file(os.path.join(self.test_dir, 'very_hard_sol.sud'))
        assert s == correct_solution
        assert 'BRUTE FORCE' in "".join(s.solution_steps)

    @raises(SudokuHasNoSolutionError)
    def test_raises_error_when_unsolvable(self):
        s = Sudoku.load_file(os.path.join(self.test_dir, 'hard.sud'))
        s._matrix[0][0] = 2
        s.solve()

    @raises(SudokuHasNoSolutionError)
    def test_raises_error_when_unsolvable_2(self):
        s = Sudoku.load_file(os.path.join(self.test_dir, 'hard.sud'))
        s._matrix[2][7] = 6
        s.solve()

    def test_equality(self):
        s = Sudoku.load_file(os.path.join(self.test_dir, 'hard_sol.sud'))
        s2 = Sudoku.load_file(os.path.join(self.test_dir, 'medium_sol.sud'))
        s3 = Sudoku.load_file(os.path.join(self.test_dir, 'hard_sol.sud'))
        assert s != s2
        assert s == s3
        assert s != 5

    def test_printing(self):
        s = Sudoku.load_file(os.path.join(self.test_dir, 'hard_sol.sud'))
        print(s)
        s = Sudoku.load_file(os.path.join(self.test_dir, 'simple_flat.sud'))
        print(s)
        assert str(s) == repr(s)

    def test_project_euler_sudokus(self):
        def test_fcn(input):
            input[0] = b"# " + input[0]
            s = Sudoku("".join([i.decode("utf-8") for i in input]).strip())
            s.solve()
            assert s.is_solved
        r = urlrequest.urlopen("https://projecteuler.net/project/resources/p096_sudoku.txt")
        sudokus = r.readlines()
        for k in range_(0, len(sudokus), 10):
            yield test_fcn, sudokus[k:k+10]

    def test_README_code(self):
        sudoku_string_1 = "030467050920010006067300148301006027400850600090200400005624001203000504040030702"
        sudoku_string_2 = "# Example Sudoku\n" + \
                          "*72****6*\n" + \
                          "***72*9*4\n" + \
                          "*9*1****2\n" + \
                          "*******4*\n" + \
                          "82*4*71**\n" + \
                          "**9*6*8**\n" + \
                          "***9**6**\n" + \
                          "**3*72*9*\n" + \
                          "*6*843*7*"

        s1 = Sudoku(sudoku_string_1)
        s1.solve()
        assert s1.is_solved

        s2 = Sudoku(sudoku_string_2)
        s2.solve()
        assert s2.is_solved
