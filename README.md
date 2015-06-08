Data Scientists Against Dirty Data (DSADD)
==========================================

A python package for defensive data analysis.

Dependencies
============

- pandas

Supports python 2.7+ and 3.4+

Examples
========

There are two main ways of using the library.
First, as decorators:

```python
from dsadd.decorators import none_missing, unique_index, is_shape

@no_missing
def f(df1, df2):
    return df1.add(df2)

@is_shape_shape(input=(1293, 10), output=(1290, 10))
@unique_index
def make_design_matrix('data.csv'):
    out = ...
    return out
```

Second, interactively (probably with the ``[pipe](http://pandas-docs.github.io/pandas-docs-travis/basics.html#tablewise-function-application)`` method).

```python
>>> import dsadd.checks as dc
>>> (df1.reindex_like(df2))
...     .pipe(dc.unique_index)
...     .cumsum()
...     .pipe(dc.within_range(0, 100))
... )
```

Overall Design
==============

Functions take a DataFrame (and optionally arguments) and return a DataFrame.
If used as a decorator, the *result* for the decorated function is checked.
Any failed check raises with an `AssertionError`.



TODO:
====

- better NaN ignoring (e.g. is_monotonic)
- better subsetting / column-specific things
- better error messages


See Also
========

[assertr](https://github.com/tonyfischetti/assertr)
