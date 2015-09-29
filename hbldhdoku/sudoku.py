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
import numpy as np

from hbldhdoku.exceptions import SudokuException


class Sudoku(object):

    def __init__(self, n=3):
        self.order = n
        self.side = n**2
        self.matrix = np.zeros((n**2, n**2), 'int8')
        self._values = np.array(range(0, (n**2)+1), 'int8')
        self.solution_steps = []

        self._poss_rows = {}
        self._poss_cols = {}
        self._poss_mats = {}

    def __str__(self):
        pass

    def __eq__(self, other):
        if isinstance(other, Sudoku):
            return np.abs((self.matrix - other.matrix)).sum().sum() == 0
        return False

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
        sudoku = np.zeros((self.side, self.side), 'int8')
        s_lines = []
        pattern = re.compile(r"([1-9\*]{9,9})")
        for line in read_lines:
            res = pattern.search(line)
            if res:
                s_lines.append(res.groups()[0])
        # TODO: Make it work for larger Sudokus as well...
        if len(s_lines) != 9:
            raise SudokuException("File did not contain a correctly defined sudoku.")
        for n, row in enumerate(s_lines):
            sudoku[n, :] = eval(",".join([char for char in row.replace('*', '0')]))
        return sudoku

    def solve(self):
        n = 0
        while 0 in self.matrix:
            n += 1
            self._update()
            # See if any position can be singled out.
            singles_found = False or self._fill_naked_singles() or self._fill_hidden_singles()

            if singles_found:
                # Found some uniquely defined. Rerun to see if new ones have shown up.
                continue
            else:
                print(self.matrix)
                raise SudokuException("This sudoku requires more advanced methods!")
        print("Sudoku solved in {0} iterations!\n{1}".format(n,self.matrix))
        for step in self.solution_steps:
            print(step)

    def _update(self):
        # TODO: Use previously stored information.
        for i in xrange(self.side):
            self._poss_rows[i] = {}
            mat_i = (i // 3) * 3
            self._poss_mats[mat_i] = {}
            for j in xrange(self.side):
                if j not in self._poss_cols:
                    self._poss_cols[j] = {}
                mat_j = (j // 3) * 3
                if not self.matrix[i, j]:
                    possible_values = np.setdiff1d(
                        self._values, self.matrix[i, :])
                    possible_values = np.setdiff1d(
                        possible_values, self.matrix[:, j])
                    possible_values = np.setdiff1d(
                        possible_values, self.matrix[mat_i:mat_i + 3, mat_j: mat_j + 3])
                    self._poss_rows[i][j] = possible_values
                    self._poss_cols[j][i] = possible_values
                    self._poss_mats[mat_i] = possible_values

    def _fill_naked_singles(self):
        simple_found = False
        for ind_i in self._poss_rows:
            for ind_j in self._poss_rows[ind_i]:
                if len(self._poss_rows[ind_i][ind_j]) == 1:
                    # Only one possible value. Assign.
                    self.matrix[ind_i, ind_j] = self._poss_rows[ind_i][ind_j][0]
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
                        possibles = np.setdiff1d(possibles, self._poss_rows[ind_i][ind_k])
                if len(possibles) == 1:
                    # Found a hidden single in a row!
                    self.matrix[ind_i, ind_j] = possibles[0]
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
                        possibles = np.setdiff1d(possibles, self._poss_cols[ind_j][ind_k])
                if len(possibles) == 1:
                    # Found a hidden single in a row!
                    self.matrix[ind_i, ind_j] = possibles[0]
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
