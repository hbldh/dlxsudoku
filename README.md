# hbldhdoku

[![Build Status](https://travis-ci.org/hbldh/hbldhdoku.svg?branch=master)](https://travis-ci.org/hbldh/hbldhdoku)

Sudoku Solver written in pure Python with no dependencies except 
[Six: Python 2 and 3 Compatibility Library](https://pythonhosted.org/six/). 

It can solve `9 x 9` Sudokus, by pure induction from possible values but also 
with an optional Brute Force methodology which is used for difficult specimens.

It is designed for solution of Sudokus of arbitrary order, but this is as of yet
rather untested.

## Installation

Install by calling:

    pip install https://github.com/hbldh/hbldhdoku

## Testing

Tests can be run using `nosetests`:

    nosetests tests

The tests make a HTTP request to a fiel containign several Sudokus on 
[Project Euler](https://projecteuler.net/project/resources/p096_sudoku.txt).

## Usage

An Sudoku can be solved as such:

```python
from hbldhdoku import Sudoku

s = Sudoku.load_file('path/to/sudoku.sud')
print(s)
s.solve(verbose=True, allow_brute_force=True)
print(s)

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
