# hbldhdoku

[![Build Status](https://travis-ci.org/hbldh/hbldhdoku.svg?branch=master)](https://travis-ci.org/hbldh/hbldhdoku)

Sudoku Solver in Python.

## Installation

Install by calling:

    pip install https://github.com/hbldh/hbldhdoku

## Testing

Tests can be run using `nosetests`:

    nosetests tests

## Usage

An Sudoku can be solved as such:

```python
from hbldhdoku import Sudoku

s = Sudoku.load_sudoku('path/to/sudoku.sud')
print(s)
s.solve()
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
