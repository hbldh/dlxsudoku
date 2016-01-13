#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`dancing_links`
==================

.. module:: dancing_links
    :platform: Unix, Windows
    :synopsis: An implementation of Donald Knuth's Dancing Links in Python.

Created on 2015-10-19, 22:53

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import copy
import math
from itertools import product


class DancingLinksSolver(object):
    """A Dancing Links Algorithm solver for Sudokus.

    This code has been adapted from http://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html,
    only modified slightly to accommodate class structure and Python 2.6.

    # Author: Ali Assaf <ali.assaf.mail@gmail.com>
    # Copyright: (C) 2010 Ali Assaf
    # License: GNU General Public License <http://www.gnu.org/licenses/>

    """

    def __init__(self, sudoku):
        self.sudoku = sudoku

    def solve(self):
        """Runs the Dancing Links/Algorithm X solver on the Sudoku.

        This code has been adapted from http://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html

        :return: List of lists with the same size as the input Sudoku, representing solutions.
        :rtype: list

        """

        R, C = int(math.sqrt(len(self.sudoku))), int(math.sqrt(len(self.sudoku[0])))
        N = R * C

        X = ([("rc", rc) for rc in product(range(N), range(N))] +
             [("rn", rn) for rn in product(range(N), range(1, N + 1))] +
             [("cn", cn) for cn in product(range(N), range(1, N + 1))] +
             [("bn", bn) for bn in product(range(N), range(1, N + 1))])
        Y = dict()

        for r, c, n in product(range(N), range(N), range(1, N + 1)):
            b = (r // R) * R + (c // C)  # Box number
            Y[(r, c, n)] = [
                ("rc", (r, c)),
                ("rn", (r, n)),
                ("cn", (c, n)),
                ("bn", (b, n))]

        X, Y = self._exact_cover(X, Y)

        for i, row in enumerate(self.sudoku):
            for j, n in enumerate(row):
                if n:
                    self._select(X, Y, (i, j, n))

        for solution in self._solve(X, Y, []):
            grid = copy.deepcopy(self.sudoku)
            for (r, c, n) in solution:
                grid[r][c] = n
            yield grid

    @staticmethod
    def _exact_cover(X, Y):
        # Dict comprehension does not exist in Python 2.6...
        # X = {j: set() for j in X}
        X_out = {}
        for j in X:
            X_out[j] = set()

        for i, row in Y.items():
            for j in row:
                X_out[j].add(i)
        return X_out, Y

    def _solve(self, X, Y, solution):
        if not X:
            yield list(solution)
        else:
            c = min(X, key=lambda c: len(X[c]))
            for r in list(X[c]):
                solution.append(r)
                cols = self._select(X, Y, r)
                for s in self._solve(X, Y, solution):
                    yield s
                self._deselect(X, Y, r, cols)
                solution.pop()

    @staticmethod
    def _select(X, Y, r):
        cols = []
        for j in Y[r]:
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].remove(i)
            cols.append(X.pop(j))
        return cols

    @staticmethod
    def _deselect(X, Y, r, cols):
        for j in reversed(Y[r]):
            X[j] = cols.pop()
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].add(i)
