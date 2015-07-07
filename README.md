Engarde
=======

[![Build Status](https://travis-ci.org/TomAugspurger/engarde.svg?branch=ci)](https://travis-ci.org/TomAugspurger/engarde)

A python package for defensive data analysis.

Dependencies
============

- pandas

Supports python 2.7+ and 3.4+

Why?
====

Data are messy.
But, our analysis often depends on certain assumptions about our data
that *should* be invariant across updates to your dataset.
`engarde` is a lightweight way to explicitly state your assumptions
and check that they're *actually* true.

This is especially important when working with flat files like CSV
that aren't bound for a more structured destination (e.g. SQL or HDF5).

Examples
========

There are two main ways of using the library, which correspond to the
two main ways I use pandas: writing small scripts or interactively at
the interpreter.

First, as decorators, which are most useful in `.py` scripts
The basic idea is to  write each step of your ETL process as a function
that takes and returns a DataFrame. These functions can be decorated with
the invariants that should be true at that step in the process.

```python
from engarde.decorators import none_missing, unique_index, is_shape

@none_missing
def f(df1, df2):
    return df1.add(df2)

@is_shape((1290, 10))
@unique_index
def make_design_matrix('data.csv'):
    out = ...
    return out
```

Second, interactively.
The cleanest way to integrate this is through the [``pipe``](http://pandas-docs.github.io/pandas-docs-travis/basics.html#tablewise-function-application) method,
introduced in pandas 0.16.2 (June 2015).

```python
>>> import engarde.checks as dc
>>> (df1.reindex_like(df2))
...     .pipe(dc.unique_index)
...     .cumsum()
...     .pipe(dc.within_range, (0, 100))
... )
```

Overall Design
==============

Functions take a DataFrame (and optionally arguments) and return a DataFrame.
If used as a decorator, the *result* for the decorated function is checked.
Any failed check raises with an `AssertionError` (for now).


TODO:
====

- better NaN ignoring (e.g. is_monotonic)
- better subsetting / column-specific things
- better error messages (a la pytest? How much can we use their machinery?)


See Also
========

[assertr](https://github.com/tonyfischetti/assertr)

