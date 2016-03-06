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
import copy
import math
from collections import Counter

from dlxsudoku.exceptions import SudokuHasNoSolutionError, SudokuTooDifficultError, SudokuHasMultipleSolutionsError
from dlxsudoku import utils
from dlxsudoku.dancing_links import DancingLinksSolver


class Sudoku(object):
    """Sudoku solver.

    Uses set methods to discern possible values in each cell of the Sudoku and then
    selects Naked and Hidden singles based on these possibility sets.

    Uses Brute Force methods when faced with a Sudoku too advanced for the simple tools
    described above. Note that this can take some time for Sudokus of order greater than 3!

    """

    def __init__(self, string_input):

        self.order, self.comment, self._matrix = \
            self._parse_from_string(string_input)

        self.side = self.order ** 2
        self.solution_steps = []

        self._values = tuple(utils.range_(0, (self.order ** 2) + 1))
        self._poss_rows = {}
        self._poss_cols = {}
        self._poss_box = {}
        self._possibles = {}

        self._check_sudoku_validity()

    @classmethod
    def load_file(cls, file_path):
        """Load a Sudoku from file.

        :param file_path: The path to the file to load_file.
        :type file_path: str, unicode
        :return: A Sudoku instance with the parsed
                 information from the file.
        :rtype: :py:class:`dlxsudoku.sudoku.Sudoku`

        """
        with open(os.path.abspath(file_path), 'rt') as f:
            s = Sudoku(f.read().strip())
        return s

    @staticmethod
    def _parse_from_string(string_input):
        """Parses a Sudoku instance from string input.

        :param string_input: A string containing the Sudoku to parse.
        :type string_input: str
        :return: The parsed Sudoku.
        :rtype: :py:class:`dlxsudoku.sudoku.Sudoku`

        """
        # Check if comment line is present.
        read_lines = string_input.split('\n')
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
                                i in utils.range_(len(read_lines[0])) if i % (order ** 2) == 0])
        matrix = utils.get_list_of_lists(
            order ** 2, order ** 2, fill_with=0)

        for i, line in enumerate(read_lines):
            line = line.strip()
            for j, value in enumerate(line):
                if value.isdigit() and int(value):
                    matrix[i][j] = int(value)
                else:
                    matrix[i][j] = 0
        return order, comment, matrix

    def __str__(self):
        if len(self.comment) > 0:
            prefix = "{0}\n".format(self.comment)
        else:
            prefix = ''
        sudoku = ''
        for i, row in enumerate(self.row_iter()):
            if i % self.order == 0 and i > 0:
                str_row = '-' * self.side
                sudoku += "+".join([str_row[j:j + self.order] for j in range(0, len(str_row), self.order)]) + '\n'
            str_row = "".join([str(v) for v in row]).replace('0', '*')
            sudoku += "|".join([str_row[j:j + self.order] for j in range(0, len(str_row), self.order)]) + '\n'
        return prefix + sudoku

    def __repr__(self):
        return str(self)

    def to_oneliner(self):
        return "".join(["".join([str(value) for value in row]) for row in self.row_iter()])

    def __eq__(self, other):
        if isinstance(other, Sudoku):
            if self.order != other.order:
                return False
            for i in utils.range_(self.side):
                for j in utils.range_(self.side):
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
        for k in utils.range_(self.side):
            yield self.row(k)

    def col(self, n):
        """Get the n:th column of the Sudoku"""
        return [r[n] for r in self.row_iter()]

    def col_iter(self):
        """Get an iterator over all columns in the Sudoku"""
        for k in utils.range_(self.side):
            yield self.col(k)

    def box(self, row, col):
        """Get the values of the box pertaining to the specified row and column of the Sudoku"""
        box = []
        box_i = (row // self.order) * self.order
        box_j = (col // self.order) * self.order
        for i in utils.range_(box_i, box_i + self.order):
            for j in utils.range_(box_j, box_j + self.order):
                box.append(self[i][j])
        return box

    def box_iter(self):
        """Get an iterator over all boxes in the Sudoku"""
        for i in utils.range_(self.order):
            for j in utils.range_(self.order):
                yield self.box(i * 3, j * 3)

    def set_cell(self, i, j, value):
        """Set a cell's value, with a series of safety checks

        :param i: The row number
        :type i: int
        :param j: The column number
        :type j: int
        :param value: The value to set
        :type value: int
        :raises: :py:class:`dlxsudoku.exceptions.SudokuHasNoSolutionError`

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

    @property
    def is_solved(self):
        """Returns ``True`` if all cells are filled with a number."""
        return all([(0 not in row) for row in self.row_iter()])

    def solve(self, verbose=False, allow_brute_force=True):
        """Solve the Sudoku.

        :param verbose: If the steps used for solving the Sudoku
                        should be printed. Default is `False`
        :type verbose: bool
        :param allow_brute_force: If Dancing Links Brute Force method
                                  should be used if necessary. Default is `True`
        :type allow_brute_force: bool

        """
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
                    solution = None
                    try:
                        dlxs = DancingLinksSolver(copy.deepcopy(self._matrix))
                        solutions = dlxs.solve()
                        solution = next(solutions)
                        more_solutions = next(solutions)
                    except StopIteration as e:
                        if solution is not None:
                            self._matrix = solution
                        else:
                            raise SudokuHasNoSolutionError("Dancing Links solver could not find any solution.")
                    except Exception as e:
                        raise SudokuHasNoSolutionError("Brute Force method failed.")
                    else:
                        # We end up here if the second `next(solutions)` works,
                        # i.e. if multiple solutions exist.
                        raise SudokuHasMultipleSolutionsError("This Sudoku has multiple solutions!")
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
        # Update possible values in each row, column and box.
        for i, (row, col, box) in enumerate(zip(self.row_iter(), self.col_iter(), self.box_iter())):
            self._poss_rows[i] = set(self._values).difference(set(row))
            self._poss_cols[i] = set(self._values).difference(set(col))
            self._poss_box[i] = set(self._values).difference(set(box))

        # Iterate over the entire Sudoku and combine information about possible values
        # from rows, columns and boxes to get a set of possible values for each cell.
        for i in utils.range_(self.side):
            self._possibles[i] = {}
            for j in utils.range_(self.side):
                self._possibles[i][j] = set()
                if self[i][j] > 0:
                    continue
                this_box_index = ((i // self.order) * self.order) + (j // self.order)
                self._possibles[i][j] = self._poss_rows[i].intersection(
                    self._poss_cols[j]).intersection(self._poss_box[this_box_index])

    def _fill_naked_singles(self):
        """Look for naked singles, i.e. cells with ony one possible value.

        :return: If any Naked Single has been found.
        :rtype: bool

        """
        simple_found = False
        for i in utils.range_(self.side):
            for j in utils.range_(self.side):
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
        for i in utils.range_(self.side):
            box_i = (i // self.order) * self.order
            for j in utils.range_(self.side):
                box_j = (j // self.order) * self.order
                # Skip if this cell is determined already.
                if self[i][j] > 0:
                    continue

                # Look for hidden single in rows.
                p = self._possibles[i][j]
                for k in utils.range_(self.side):
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
                for k in utils.range_(self.side):
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
                for k in utils.range_(box_i, box_i + self.order):
                    for kk in utils.range_(box_j, box_j + self.order):
                        if k == i and kk == j:
                            continue
                        p = p.difference(self._possibles[k][kk])
                if len(p) == 1:
                    # Found a hidden single in a box!
                    self.set_cell(i, j, p.pop())
                    self.solution_steps.append(self._format_step("HIDDEN-BOX", (i, j), self[i][j]))
                    return True

        return False

    def _check_sudoku_validity(self):
        def check_item(item):
            c = Counter(item)
            if 0 in c:
                c.pop(0)
            assert all([x == 1 for x in c.values()])

        try:
            for row in self.row_iter():
                check_item(row)
            for col in self.col_iter():
                check_item(col)
            for box in self.box_iter():
                check_item(box)
        except AssertionError:
            raise SudokuHasNoSolutionError("The input Sudoku was not valid!")

    @staticmethod
    def _format_step(step_name, indices, value):
        """Help method for formatting solution step history."""
        return "[{0},{1}] = {2}, {3}".format(indices[0] + 1, indices[1] + 1, value, step_name)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--sudoku', type=str, default=None, help="The raw text Sudoku to solve.")
    group.add_argument('--path', type=str, default=None, help="Path to the Sudoku to solve.")
    parser.add_argument('-v', action='store_true', help="Print solution steps.")
    parser.add_argument('--no-brute-force', action='store_false', help="Disable Dancing Links algorithm solving.")
    parser.add_argument('--oneliner', action='store_true', help="Print oneliner solution.")
    args = parser.parse_args()

    if args.path is not None:
        s = Sudoku.load_file(os.path.abspath(os.path.expanduser(args.path)))
    else:
        s = Sudoku(args.sudoku)
    s.solve(verbose=args.v, allow_brute_force=args.no_brute_force)

    if args.oneliner:
        return s.to_oneliner()
    else:
        return s

if __name__ == "__main__":
    main()
