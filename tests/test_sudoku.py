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
import sys

try:
    import urllib.request as urlrequest
except ImportError:
    import urllib as urlrequest

import pytest

from dlxsudoku import Sudoku
from dlxsudoku.sudoku import main
from dlxsudoku.utils import range_
from dlxsudoku.exceptions import SudokuException, SudokuHasNoSolutionError, SudokuTooDifficultError, SudokuHasMultipleSolutionsError


_test_dir = os.path.dirname(os.path.abspath(__file__))


def test_solve_simple_sudoku():
    s = Sudoku.load_file(os.path.join(_test_dir, 'simple.sud'))
    s.solve()
    correct_solution = Sudoku.load_file(os.path.join(_test_dir, 'simple_sol.sud'))
    assert s == correct_solution


def test_solve_simple_sudoku_read_from_flat_file():
    s = Sudoku.load_file(os.path.join(_test_dir, 'simple_flat.sud'))
    s.solve()
    correct_solution = Sudoku.load_file(os.path.join(_test_dir, 'simple_sol.sud'))
    assert s == correct_solution


def test_solve_medium_sudoku():
    s = Sudoku.load_file(os.path.join(_test_dir, 'medium.sud'))
    s.solve()
    correct_solution = Sudoku.load_file(os.path.join(_test_dir, 'medium_sol.sud'))
    assert s == correct_solution


def test_solve_hard_sudoku():
    s = Sudoku.load_file(os.path.join(_test_dir, 'hard.sud'))
    s.solve(verbose=True)
    correct_solution = Sudoku.load_file(os.path.join(_test_dir, 'hard_sol.sud'))
    assert s == correct_solution


def test_to_oneliner_method():
    s = Sudoku.load_file(os.path.join(_test_dir, 'hard.sud'))
    s.solve(verbose=True)
    correct_solution = Sudoku.load_file(os.path.join(_test_dir, 'hard_sol.sud'))
    assert s == correct_solution
    oneliner = s.to_oneliner()
    oneliner_parsed = Sudoku(oneliner)
    assert oneliner_parsed == correct_solution


def test_solve_very_hard_sudoku_raises_error_if_brute_force_disallowed():
    s = Sudoku.load_file(os.path.join(_test_dir, 'very_hard.sud'))
    with pytest.raises(SudokuTooDifficultError):
        s.solve(verbose=True, allow_brute_force=False)
    correct_solution = Sudoku.load_file(os.path.join(_test_dir, 'very_hard_sol.sud'))
    assert s != correct_solution


def test_solve_very_hard_sudoku_with_brute_force():
    s = Sudoku.load_file(os.path.join(_test_dir, 'very_hard.sud'))
    s.solve(verbose=True, allow_brute_force=True)
    correct_solution = Sudoku.load_file(os.path.join(_test_dir, 'very_hard_sol.sud'))
    assert s == correct_solution
    assert 'BRUTE FORCE' in "".join(s.solution_steps)


def test_solve_multiple_solutions():
    with pytest.raises(SudokuHasMultipleSolutionsError):
        s = Sudoku("***4*******9*******3**7*******7*********5*32*4**86***55*3****8*7983**4****6**9***")
        s.solve(verbose=True, allow_brute_force=True)


def test_raises_error_when_unsolvable():
    with pytest.raises(SudokuHasNoSolutionError):
        s = Sudoku.load_file(os.path.join(_test_dir, 'hard.sud'))
        s._matrix[0][0] = 2
        s.solve()


def test_raises_error_when_unsolvable_2():
    with pytest.raises(SudokuHasNoSolutionError):
        s = Sudoku.load_file(os.path.join(_test_dir, 'hard.sud'))
        s._matrix[2][7] = 6
        s.solve()


def test_raises_error_when_input_is_invalid():
    with pytest.raises(SudokuHasNoSolutionError):
        s = Sudoku("***4*******9***5***3**7***2***7*********5*32*4**86***55*3****8*7983**4*2**6**9***")
        s.solve(verbose=True, allow_brute_force=True)


def test_equality():
    s = Sudoku.load_file(os.path.join(_test_dir, 'hard_sol.sud'))
    s2 = Sudoku.load_file(os.path.join(_test_dir, 'medium_sol.sud'))
    s3 = Sudoku.load_file(os.path.join(_test_dir, 'hard_sol.sud'))
    assert s != s2
    assert s == s3
    assert s != 5


def test_str_repr():
    s = Sudoku.load_file(os.path.join(_test_dir, 'hard_sol.sud'))
    assert str(s) == repr(s)


def project_euler_sudokus():
    try:
        r = urlrequest.urlopen("https://projecteuler.net/project/resources/p096_sudoku.txt")
        sudokus = r.readlines()
        sudokus = [sudokus[k:k+10] for k in range_(0, len(sudokus), 10)]
    except:
        sudokus = []
    return sudokus


@pytest.mark.parametrize('sudoku', project_euler_sudokus())
def test_project_euler_sudokus(sudoku):
    sudoku[0] = b"# " + sudoku[0]
    s = Sudoku("".join([i.decode("utf-8") for i in sudoku]).strip())
    s.solve()
    assert s.is_solved


def test_README_code():
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


def test_command_line_solver_1(capsys):
    sudoku_string = "030467050920010006067300148301006027400850600090200400005624001203000504040030702"
    sys.argv = ["solve-sudoku", "--sudoku", sudoku_string, '--oneliner']
    main()
    out, err = capsys.readouterr()
    assert out.strip() == "138467259924518376567392148351946827472851693896273415785624931213789564649135782"


def test_command_line_solver_2(capsys):
    sudoku_string = "# Example Sudoku\n" + \
                    "*72****6*\n" + \
                    "***72*9*4\n" + \
                    "*9*1****2\n" + \
                    "*******4*\n" + \
                    "82*4*71**\n" + \
                    "**9*6*8**\n" + \
                    "***9**6**\n" + \
                    "**3*72*9*\n" + \
                    "*6*843*7*"
    sys.argv = ["solve-sudoku", "--sudoku", sudoku_string, '--oneliner']
    main()
    out, err = capsys.readouterr()
    assert Sudoku(out).is_solved


def test_command_line_solver_3(capsys):
    sys.argv = ["solve-sudoku", "--path",
                os.path.join(_test_dir, 'simple.sud'), '--oneliner']
    main()
    out, err = capsys.readouterr()
    assert Sudoku(out).is_solved

