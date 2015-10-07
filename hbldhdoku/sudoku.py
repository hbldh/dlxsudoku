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

from hbldhdoku.exceptions import SudokuException
from hbldhdoku import utils


class Sudoku(object):

    def __init__(self, n=3):
        self.order = n
        self.side = n**2
        self.matrix = utils.get_list_of_lists(self.side, self.side, fill_with=0)
        self._values = six.moves.range(0, (n ** 2) + 1)
        self.solution_steps = []

        self._poss_rows = {}
        self._poss_cols = {}
        self._poss_mats = {}

    def __str__(self):
        pass

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
            n += 1
            self._update()
            # See if any position can be singled out.
            singles_found = False or self._fill_naked_singles() or self._fill_hidden_singles()

            if singles_found:
                # Found some uniquely defined. Rerun to see if new ones have shown up.
                continue
            else:
                print(self.matrix)
                raise SudokuException("This Sudoku requires more advanced methods!")
        if verbose:
            print("Sudoku solved in {0} iterations!\n{1}".format(n, self.matrix))
            for step in self.solution_steps:
                print(step)

    def _update(self):
        # TODO: Use previously stored information.
        for i in six.moves.range(self.side):
            self._poss_rows[i] = {}
            mat_i = (i // 3) * 3
            self._poss_mats[mat_i] = {}
            for j in six.moves.range(self.side):
                if j not in self._poss_cols:
                    self._poss_cols[j] = {}
                mat_j = (j // 3) * 3
                if not self.matrix[i][j]:
                    possible_values = set(self._values).difference(self.matrix[i])
                    possible_values = possible_values.difference(set([row[j] for row in self.matrix]))
                    box = []
                    for k in six.moves.range(mat_i, mat_i + 3):
                        for kk in six.moves.range(mat_j, mat_j + 3):
                            box.append(self.matrix[k][kk])
                    possible_values = list(possible_values.difference(set(box)))
                    self._poss_rows[i][j] = possible_values
                    self._poss_cols[j][i] = possible_values
                    self._poss_mats[mat_i] = possible_values

    def _fill_naked_singles(self):
        simple_found = False
        for ind_i in self._poss_rows:
            for ind_j in self._poss_rows[ind_i]:
                if len(self._poss_rows[ind_i][ind_j]) == 1:
                    # Only one possible value. Assign.
                    self.matrix[ind_i][ind_j] = self._poss_rows[ind_i][ind_j][0]
                    self.solution_steps.append(self._format_step("NAKED",
                                                                 (ind_i, ind_j),
                                                                 self._poss_rows[ind_i][ind_j][0]))
                    simple_found = True
                elif len(self._poss_rows[ind_i][ind_j]) == 0:
                    raise SudokuException("Error made! No possible value for ({0},{1})!",
                                          ind_i + 1, ind_j + 1)
        return simple_found

    def _fill_hidden_singles(self):
        simple_found = False
        # Go through each row.
        for ind_i in self._poss_rows:
            for ind_j in self._poss_rows[ind_i]:
                possibles = self._poss_rows[ind_i][ind_j]
                for ind_k in self._poss_rows[ind_i]:
                    if ind_k != ind_j:
                        possibles = list(set(possibles).difference(self._poss_rows[ind_i][ind_k]))
                if len(possibles) == 1:
                    # Found a hidden single in a row!
                    self.matrix[ind_i][ind_j] = possibles[0]
                    self.solution_steps.append(self._format_step("HIDDEN-ROW",
                                                                 (ind_i, ind_j),
                                                                 possibles[0]))
                    simple_found = True

        # Go through each column.
        for ind_j in self._poss_cols:
            for ind_i in self._poss_cols[ind_j]:
                possibles = self._poss_cols[ind_j][ind_i]
                for ind_k in self._poss_cols[ind_j]:
                    if ind_k != ind_i:
                        possibles = list(set(possibles).difference(self._poss_cols[ind_j][ind_k]))
                if len(possibles) == 1:
                    # Found a hidden single in a row!
                    self.matrix[ind_i][ind_j] = possibles[0]
                    self.solution_steps.append(self._format_step("HIDDEN-COL",
                                                                 (ind_i, ind_j),
                                                                 possibles[0]))
                    simple_found = True

        # Go through each block.
        # TODO: Write block checker.

        return simple_found

    def _format_step(self, step_name, indices, value):
        return "[{0},{1}] = {2}, {3}".format(indices[0] + 1, indices[1] + 1, value, step_name)


def main():
    pass

if __name__ == "__main__":
    main()
