Name Change
===========

Hi. I changed the name of this library to `engarde`. Check it out [here](www.github.com/TomAugspurger/engarde).

Data Scientists Against Dirty Data (DSADD)
==========================================

A python package for defensive data analysis. (Name to be determined.)

Dependencies
============

- pandas

Supports python 2.7+ and 3.4+

Why?
====

Data are messy. You want to assert that certain invariants about your data
across operations or updates to the raw data. This is a lightweight way
of placing some additional structure on semi-structured data sources like CSVs.

Examples
========

There are two main ways of using the library.
First, as decorators:

```python
from dsadd.decorators import none_missing, unique_index, is_shape

@none_missing
def f(df1, df2):
    return df1.add(df2)

@is_shape((1290, 10))
@unique_index
def make_design_matrix('data.csv'):
    out = ...
    return out
```

Second, interactively (probably with the [``pipe``](http://pandas-docs.github.io/pandas-docs-travis/basics.html#tablewise-function-application) method,
which requires pandas>=0.16.2).

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
