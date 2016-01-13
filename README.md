# DLXSudoku

[![Build Status](https://travis-ci.org/hbldh/dlxsudoku.svg)](https://travis-ci.org/hbldh/dlxsudoku)

Sudoku Solver written in pure Python with no dependencies (tests require  
[Six: Python 2 and 3 Compatibility Library](https://pythonhosted.org/six/)).
It can solve Sudokus of sizes `N x N` by pure induction from possible values, but also 
with an optional [Dancing Links](https://en.wikipedia.org/wiki/Dancing_Links) solver 
which is a brute force methodology used for difficult specimens.

## Installation

Install by calling:

    pip install git+https://github.com/hbldh/dlxsudoku

## Testing

Tests can be run using `nosetests`:

    nosetests tests

The tests make a HTTP request to a file containing several Sudokus on 
[Project Euler]("https://projecteuler.net/project/resources/p096_sudoku.txt").

## Usage

An Sudoku can be solved as such:

```python
from dlxsudoku import Sudoku

s = Sudoku.load_file('path/to/sudoku.sud')
s.solve(verbose=True, allow_brute_force=True)

```

A Sudoku file should be structured in the following manner:

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

or as a one-liner with optional comment:

    # Optional comment or metadata.
    030467050920010006067300148301006027400850600090200400005624001203000504040030702

Any character other than `[1-9]` may be used as a placeholder for unknowns.
