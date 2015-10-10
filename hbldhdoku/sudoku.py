# -*- coding: utf-8 -*-
"""
.. module:: sudoku
   :platform: Unix, Windows
   :synopsis: A class for handling and solving Sudoku.

.. moduleauthor:: Henrik Blidh <henrik.blidh@nedomkull.com>

Created on 2013-01-15, 19:26
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import os
import re

import six

from hbldhdoku.exceptions import SudokuException, SudokuHasNoSolutionError, SudokuTooDifficultError
from hbldhdoku import utils


class Sudoku(object):

    def __init__(self, n=3):
        self.order = n
        self.side = n**2
        self.matrix = utils.get_list_of_lists(self.side, self.side, fill_with=0)
        self.solution_steps = []

        self._values = tuple(six.moves.range(0, (n ** 2) + 1))
        self._poss_rows = {}
        self._poss_cols = {}
        self._poss_mats = {}
        self._possibles = {}

    def __str__(self):
        for row in self.matrix:
            print("".join([str(v) for v in row]).replace('0', '*'))

    def __eq__(self, other):
        if isinstance(other, Sudoku):
            if self.order != other.order:
                return False
            for i in six.moves.range(self.side):
                for j in six.moves.range(self.side):
                    if self.matrix[i][j] != other.matrix[i][j]:
                        return False
            return True
        return False

    @property
    def is_solved(self):
        for row in self.matrix:
            for value in row:
                if value == 0:
                    return False
        return True

    @classmethod
    def load_sudoku(cls, file_path, n=3):
        out = cls(n)
        out.matrix = out._read_to_matrix(file_path)
        return out

    def _read_to_matrix(self, file_path):
        with open(os.path.abspath(file_path), 'rt') as f:
            read_lines = f.read()

        # TODO: Parse metadata in textfile as well.
        read_lines = read_lines.split('\n')
        sudoku = utils.get_list_of_lists(self.side, self.side, fill_with=0)
        s_lines = []
        pattern = re.compile(r"([1-9\*]{9,9})")
        for line in read_lines:
            res = pattern.search(line)
            if res:
                s_lines.append(res.groups()[0])

        # TODO: Make it work for larger Sudokus as well...
        if len(s_lines) != 9:
            raise SudokuException("File did not contain a correctly defined sudoku.")
        for i, row in enumerate(s_lines):
            for j, value in enumerate([int(c) for c in row.replace('*', '0')]):
                sudoku[i][j] = value
        return sudoku

    def solve(self, verbose=False):
        n = 0
        while not self.is_solved:
            # Increase counter and update possibles arrays.
            n += 1
            self._update()

            # See if any position can be singled out.
            singles_found = False or self._fill_naked_singles() or self._fill_hidden_singles()

            if singles_found:
                # Found some uniquely defined. Run another iteration to see if new ones have shown up.
                continue
            else:
                # Could not solve this Sudoku.
                print(self.matrix)
                raise SudokuTooDifficultError("This Sudoku requires more advanced methods!")
        if verbose:
            print("Sudoku solved in {0} iterations!\n{1}".format(n, self.matrix))
            for step in self.solution_steps:
                print(step)

    def _update(self):
        # Update possible values in each row and each column.
        for i in six.moves.range(self.side):
            self._poss_cols[i] = set(self._values).difference(set([row[i] for row in self.matrix]))
            self._poss_rows[i] = set(self._values).difference(self.matrix[i])
        # Update possible values for each of the boxes.
        for i in six.moves.range(self.order):
            for j in six.moves.range(self.order):
                this_box_index = (i * self.order) + j
                box = []
                for k in six.moves.range(i * self.order, (i * self.order) + self.order):
                    for kk in six.moves.range(j * self.order, (j * self.order) + self.order):
                        box.append(self.matrix[k][kk])
                self._poss_mats[this_box_index] = set(self._values).difference(set(box))

        # Iterate over the entire Sudoku and combine information about possible values
        # from rows, columns and boxes to get a set of possible values for each cell.
        for i in six.moves.range(self.side):
            self._possibles[i] = {}
            mat_i = (i // self.order)
            for j in six.moves.range(self.side):
                self._possibles[i][j] = set()
                mat_j = (j // self.order)
                this_box_index = (mat_i * self.order) + mat_j
                if self.matrix[i][j] > 0:
                    continue
                self._possibles[i][j] = self._poss_rows[i].intersection(
                    self._poss_cols[j]).intersection(self._poss_mats[this_box_index])

    def _fill_naked_singles(self):
        """Look for naked singles, i.e. cells with ony one possible value.

        :return: If any Naked Single has been found.
        :rtype: bool

        """
        simple_found = False
        for i in six.moves.range(self.side):
            for j in six.moves.range(self.side):
                if self.matrix[i][j] > 0:
                    continue
                p = self._possibles[i][j]
                if len(p) == 1:
                    self.matrix[i][j] = p.pop()
                    self.solution_steps.append(self._format_step("NAKED", (i, j), self.matrix[i][j]))
                    simple_found = True
                elif len(p) == 0:
                    raise SudokuHasNoSolutionError("Error made! No possible value for ({0},{1})!".format(i + 1, j + 1))

        return simple_found

    def _fill_hidden_singles(self):
        """Look for hidden singles, i.e. cells with only one unique possible value in row, column or box.

        :return: If any Hidden Single has been found.
        :rtype: bool

        """
        for i in six.moves.range(self.side):
            mat_i = (i // self.order) * self.order
            for j in six.moves.range(self.side):
                mat_j = (j // self.order) * self.order
                # Skip if this cell is determined already.
                if self.matrix[i][j] > 0:
                    continue

                # Look for hidden single in rows.
                p = self._possibles[i][j]
                for k in six.moves.range(self.side):
                    if k == j:
                        continue
                    p = p.difference(self._possibles[i][k])
                if len(p) == 1:
                    # Found a hidden single in a row!
                    self.matrix[i][j] = p.pop()
                    self.solution_steps.append(self._format_step("HIDDEN-ROW", (i, j), self.matrix[i][j]))
                    return True

                # Look for hidden single in columns
                p = self._possibles[i][j]
                for k in six.moves.range(self.side):
                    if k == i:
                        continue
                    p = p.difference(self._possibles[k][j])
                if len(p) == 1:
                    # Found a hidden single in a column!
                    self.matrix[i][j] = p.pop()
                    self.solution_steps.append(self._format_step("HIDDEN-COL", (i, j), self.matrix[i][j]))
                    return True

                # Look for hidden single in box
                p = self._possibles[i][j]
                for k in six.moves.range(mat_i, mat_i + self.order):
                    for kk in six.moves.range(mat_j, mat_j + self.order):
                        if k == i and kk == j:
                            continue
                        p = p.difference(self._possibles[k][kk])
                if len(p) == 1:
                    # Found a hidden single in a column!
                    self.matrix[i][j] = p.pop()
                    self.solution_steps.append(self._format_step("HIDDEN-BOX", (i, j), self.matrix[i][j]))
                    return True

        return False

    def _format_step(self, step_name, indices, value):
        return "[{0},{1}] = {2}, {3}".format(indices[0] + 1, indices[1] + 1, value, step_name)

