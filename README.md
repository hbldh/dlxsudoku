# DLXSudoku

[![Build Status](https://travis-ci.org/hbldh/dlxsudoku.svg)](https://travis-ci.org/hbldh/dlxsudoku)
[![PyPi version](https://img.shields.io/pypi/v/dlxsudoku.svg)](https://pypi.python.org/pypi/dlxsudoku)
[![PyPi downloads](https://img.shields.io/pypi/dm/dlxsudoku.svg)](https://pypi.python.org/pypi/dlxsudoku)
[![PyPi license](https://img.shields.io/pypi/l/dlxsudoku.svg)](https://pypi.python.org/pypi/dlxsudoku)
[![Coverage Status](https://coveralls.io/repos/github/hbldh/dlxsudoku/badge.svg?branch=master)](https://coveralls.io/github/hbldh/dlxsudoku?branch=master)

Sudoku Solver written in pure Python with no dependencies.

It solves Sudokus of sizes `N x N` by pure induction as 
far as is possible, and then uses an optional 
[Dancing Links](https://en.wikipedia.org/wiki/Dancing_Links) 
solver, which is a brute force methodology, when the basic 
induction is not enough. 

## Installation

Install by calling:

    pip install dlxsudoku

## Testing

Tests can be run using `pytest`:

    py.test tests

The tests make a HTTP request to a file containing several 
Sudokus on [Project Euler](https://projecteuler.net/project/resources/p096_sudoku.txt).

## Usage

A Sudoku stored in a file can be solved as such:

```python
from dlxsudoku import Sudoku

s = Sudoku.load_file('path/to/sudoku.sud')
s.solve(verbose=True, allow_brute_force=True)

```

Alternatively, if your Sudoku is stored in string variable 
it can be solved in the following fashion:
```python
from dlxsudoku import Sudoku

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
print(s1.to_oneliner())

s2 = Sudoku(sudoku_string_2)
s2.solve()
print(s2)

```

### Sudoku formatting

A Sudoku file or string should be structured in the following manner:

    # Optional comment or metadata
    *72****6*
    ***72*9*4
    *9*1****2
    *******4*
    82*4*71**
    **9*6*8**
    ***9**6**
    **3*72*9*
    *6*843*7*

or as a one-liner:

    030467050920010006067300148301006027400850600090200400005624001203000504040030702

Any character other than `[1-9]` may be used as a placeholder for unknowns.

## References

The Dancing Links code has been adapted from 
[Algorithm X in 30 lines!](http://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html), 
only modified slightly to accommodate class structure and Python 2.6.
