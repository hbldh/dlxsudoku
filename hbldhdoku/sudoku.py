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
import random
import copy
import math

import six

from hbldhdoku.exceptions import SudokuHasNoSolutionError, SudokuTooDifficultError
from hbldhdoku import utils
from hbldhdoku.dancing_links import DancingLinksSolver


class Sudoku(object):
    """Sudoku solver.

    Uses set methods to discern possible values in each cell of the Sudoku and then
    selects Naked and Hidden singles based on these possibility sets.

    Uses Brute Force methods when faced with a Sudoku too advanced for the simple tools
    described above. Note that this can take some time for Sudokus of order greater than 3!

    """

    def __init__(self, order=3):
        self.comment = ''
        self.order = order
        self.side = order**2
        self.solution_steps = []

        self._matrix = utils.get_list_of_lists(self.side, self.side, fill_with=0)
        self._values = tuple(six.moves.range(0, (order ** 2) + 1))
        self._poss_rows = {}
        self._poss_cols = {}
        self._poss_box = {}
        self._possibles = {}

    def __str__(self):
        if self.comment:
            prefix = "{0}".format(self.comment)
        else:
            prefix = ''
        return prefix + "\n".join(["".join([str(v) for v in row]).replace('0', '*') for row in self.row_iter()])

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, Sudoku):
            if self.order != other.order:
                return False
            for i in six.moves.range(self.side):
                for j in six.moves.range(self.side):
                    if self[i][j] != other[i][j]:
                        return False
            return True
        return False

    def __ne__(self, other):
        return not (self == other)

    def __getitem__(self, item):
        return self._matrix[item]

    def row(self, n):
        """Get the n:th row of the Sudoku"""
        return self[n]

    def row_iter(self):
        """Get an iterator over all rows in the Sudoku"""
        for k in six.moves.range(self.side):
            yield self.row(k)

    def col(self, n):
        """Get the n:th column of the Sudoku"""
        return [r[n] for r in self.row_iter()]

    def col_iter(self):
        """Get an iterator over all columns in the Sudoku"""
        for k in six.moves.range(self.side):
            yield self.col(k)

    def box(self, row, col):
        """Get the values of the box pertaining to the specified row and column of the Sudoku"""
        box = []
        box_i = (row // self.order) * self.order
        box_j = (col // self.order) * self.order
        for i in six.moves.range(box_i, box_i + self.order):
            for j in six.moves.range(box_j, box_j + self.order):
                box.append(self[i][j])
        return box

    def box_iter(self):
        """Get an iterator over all boxes in the Sudoku"""
        for i in six.moves.range(self.order):
            for j in six.moves.range(self.order):
                yield self.box(i * 3, j * 3)

    def set_cell(self, i, j, value):
        """Set a cell's value, with a series of safety checks.
        
        :param i: The row number
        :type i: int 
        :param j: The column number
        :type j: int
        :param value: The value to set
        :type value: int 
        :raises: :py:class:`hbldhdoku.exceptions.SudokuHasNoSolutionError`

        """
        bool_tests = [
            value in self._possibles[i][j],
            value in self._poss_rows[i],
            value in self._poss_cols[j],
            value in self._poss_box[(i // self.order) * self.order + (j // self.order)],
            value not in self.row(i),
            value not in self.col(j),
            value not in self.box(i, j)
        ]

        if all(bool_tests):
            self[i][j] = value
        else:
            raise SudokuHasNoSolutionError("This value cannot be set here!")

    def random_guess(self):
        """Make a random guess on first encountered cell with fewest possibles.
         
         Used by Brute Force method.
         
        """
        n_to_look_for = 2
        while True:
            for i in six.moves.range(self.side):
                for j in six.moves.range(self.side):
                    if len(self._possibles[i][j]) == n_to_look_for:
                        self.set_cell(
                            i, j, list(self._possibles[i][j])[random.randint(0, len(self._possibles[i][j])) - 1])
                        self.solution_steps.append(self._format_step("RANDOM", (i, j), self[i][j]))
                        return
            n_to_look_for += 1

    @property
    def is_solved(self):
        """Returns ``True`` if all cells are filled with a number."""
        return all([(0 not in row) for row in self.row_iter()])

    @classmethod
    def load_file(cls, file_path):
        """Load a Sudoku from file.

        :param file_path: The path to the file to load_file.
        :type file_path: str, unicode
        :return: A Sudoku instance with the parsed information from the file.
        :rtype: :py:class:`hbldhdoku.sudoku.Sudoku`

        """
        with open(os.path.abspath(file_path), 'rt') as f:
            s = cls.parse_from_file_object(f)
        return s

    @classmethod
    def parse_from_file_object(cls, f):
        """Reads a Sudoku from a FileType object and parses it into a Sudoku instance.

        :param f: Any FileType object containing readable data.
        :type f: :py:class:`types.FileType`
        :return: The parsed Sudoku
        :rtype: :py:class:`hbldhdoku.sudoku.Sudoku`

        """
        read_lines = f.readlines()
        # Check if comment line is present.
        if read_lines[0].startswith('#'):
            comment = read_lines.pop(0)
        else:
            comment = ''

        if len(read_lines) > 1:
            # Assume that Sudoku is defined over several rows.
            order = int(math.sqrt(len(read_lines)))
        else:
            # Sudoku is defined on one line.
            order = int(math.sqrt(math.sqrt(len(read_lines[0]))))
            read_lines = filter(lambda x: len(x) == (order ** 2), [read_lines[0][i:(i + order ** 2)] for
                                i in six.moves.xrange(len(read_lines[0])) if i % (order ** 2) == 0])

        out = cls(order)
        out.comment = comment
        for i, line in enumerate(read_lines):
            line = line.strip()
            for j, value in enumerate(line):
                if value.isdigit() and int(value):
                    out._matrix[i][j] = int(value)
                else:
                    out._matrix[i][j] = 0
        return out

    def solve(self, verbose=False, allow_brute_force=True):
        while not self.is_solved:
            # Update possibles arrays.
            self._update()

            # See if any position can be singled out.
            singles_found = False or self._fill_naked_singles() or self._fill_hidden_singles()

            # If singles_found is False, then no new uniquely defined cells were found
            # and this solver cannot solve the Sudoku. We either use brute force or throw an error.
            # Else, if singles_found is True, run another iteration to see if new singles have shown up.
            if not singles_found:
                if allow_brute_force:
                    dlxs = DancingLinksSolver(copy.deepcopy(self._matrix))
                    solutions = list(dlxs.solve())
                    if len(solutions) == 1:
                        self._matrix = solutions[0]
                    elif len(solutions) > 1:
                        print("This Sudoku has multiple solutions!")
                        self._matrix = solutions[0]
                    else:
                        raise SudokuHasNoSolutionError("Brute Force method failed.")
                    self.solution_steps.append("BRUTE FORCE - Dancing Links")
                    break
                else:
                    print(self)
                    raise SudokuTooDifficultError("This Sudoku requires more advanced methods!")
        if verbose:
            print("Sudoku solved in {0} iterations!\n{1}".format(len(self.solution_steps), self))
            for step in self.solution_steps:
                print(step)

    def _update(self):
        """Calculate remaining values for each row, column, box and finally cell."""
        # Update possible values in each row and each column.
        for i in six.moves.range(self.side):
            self._poss_cols[i] = set(self._values).difference(set(self.col(i)))
            self._poss_rows[i] = set(self._values).difference(self.row(i))
        # Update possible values for each of the boxes.
        for i, box in enumerate(self.box_iter()):
            self._poss_box[i] = set(self._values).difference(set(box))

        # Iterate over the entire Sudoku and combine information about possible values
        # from rows, columns and boxes to get a set of possible values for each cell.
        for i in six.moves.range(self.side):
            self._possibles[i] = {}
            box_i = (i // self.order)
            for j in six.moves.range(self.side):
                self._possibles[i][j] = set()
                box_j = (j // self.order)
                this_box_index = (box_i * self.order) + box_j
                if self[i][j] > 0:
                    continue
                self._possibles[i][j] = self._poss_rows[i].intersection(
                    self._poss_cols[j]).intersection(self._poss_box[this_box_index])

    def _fill_naked_singles(self):
        """Look for naked singles, i.e. cells with ony one possible value.

        :return: If any Naked Single has been found.
        :rtype: bool

        """
        simple_found = False
        for i in six.moves.range(self.side):
            for j in six.moves.range(self.side):
                if self[i][j] > 0:
                    continue
                p = self._possibles[i][j]
                if len(p) == 1:
                    self.set_cell(i, j, list(p)[0])
                    self.solution_steps.append(self._format_step("NAKED", (i, j), self[i][j]))
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
            box_i = (i // self.order) * self.order
            for j in six.moves.range(self.side):
                box_j = (j // self.order) * self.order
                # Skip if this cell is determined already.
                if self[i][j] > 0:
                    continue

                # Look for hidden single in rows.
                p = self._possibles[i][j]
                for k in six.moves.range(self.side):
                    if k == j:
                        continue
                    p = p.difference(self._possibles[i][k])
                if len(p) == 1:
                    # Found a hidden single in a row!
                    self.set_cell(i, j, p.pop())
                    self.solution_steps.append(self._format_step("HIDDEN-ROW", (i, j), self[i][j]))
                    return True

                # Look for hidden single in columns
                p = self._possibles[i][j]
                for k in six.moves.range(self.side):
                    if k == i:
                        continue
                    p = p.difference(self._possibles[k][j])
                if len(p) == 1:
                    # Found a hidden single in a column!
                    self.set_cell(i, j, p.pop())
                    self.solution_steps.append(self._format_step("HIDDEN-COL", (i, j), self[i][j]))
                    return True

                # Look for hidden single in box
                p = self._possibles[i][j]
                for k in six.moves.range(box_i, box_i + self.order):
                    for kk in six.moves.range(box_j, box_j + self.order):
                        if k == i and kk == j:
                            continue
                        p = p.difference(self._possibles[k][kk])
                if len(p) == 1:
                    # Found a hidden single in a box!
                    self.set_cell(i, j, p.pop())
                    self.solution_steps.append(self._format_step("HIDDEN-BOX", (i, j), self[i][j]))
                    return True

        return False

    def _format_step(self, step_name, indices, value):
        """Help method for formatting solution step history."""
        return "[{0},{1}] = {2}, {3}".format(indices[0] + 1, indices[1] + 1, value, step_name)

