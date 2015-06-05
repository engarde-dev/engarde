Data Scientists Against Dirty Data (DSADD)
==========================================

A python package for defensive data analysis.

Dependencies
============

- pandas

Supports python 2.7+ and 3.4+

Overall Design
==============

Functions take a DataFrame (and optionally arguments) and return a DataFrame.

Decorators should take input / output flags, columns.

Examples
========

Primarily used as decorators

```python
from dsadd import no_missing

@no_missing
def f(df):
    return df
```

or

```python
from dsadd import known_shape, unique_index

@known_shape(input=(1293, 10), output=(1290, 10))
@unique_index
def make_design_matrix('data.csv'):
    out = ...
    return out
```

Should also go well with the new `.pipe` method


```python
pd.concat([df1, df2]).pipe(unique_index).cumsum()
```


TODO: Error type. I'm thinking have specific errors (e.g. `MissingDataError`), all of which
subclass `ValueError`.

Single-table vs. Two-table
==========================

functions should take a DataFrame and return a DataFrame
Preference for checking input or output? Toggleable?

Pronunciation
=============

I've always wanted to start a pronunciation war (it's "gif" with a hard "g" by the way).


Implement

- no_missing (table)
- known_shape (table)
- unique_index (index)
- non_negative (columns)
- monotonic (columns)
- monotonic_increasing
- monotonic_decreasing
- withn_range ([columns] -> [set])
- within_set ([columns -> [set])
- within_n_std

See Also
========

[assertr](https://github.com/tonyfischetti/assertr)
