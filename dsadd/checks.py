# -*- coding: utf-8 -*-
"""
checks.py

Each function in here should

- Take a DataFrame as its first argument, maybe optional arguments
- Makes its assert
- Return the original DataFrame
"""
import operator

import numpy as np

def none_missing(df):
    """
    Asserts that there are no missing values (NaNs) in the DataFrame.
    """
    assert not df.isnull().any().any()
    return df

def is_monotonic(df, increasing=None, strict=False):
    """
    Asserts that the DataFrame is monotonic

    Parameters
    ==========

    df : Series or DataFrame
    increasing : None or bool
        None is either increasing or decreasing.
    strict: whether the comparison should be strict
    """
    delta = df.diff().iloc[1:]

    dispatch = {(True, False): operator.ge,
                (True, True): operator.gt,
                (False, False): operator.le,
                (False, True): operator.lt,
                (None, False): (lambda x, y: operator.ge(x, y),
                                lambda x, y: operator.le(x, y)),
                (None, True): (lambda x, y: operator.gt(x, y),
                               lambda x, y: operator.lt(x, y))}

    # tough to do generically
    if increasing is not None:
        func = dispatch[(increasing, strict)]
        assert func(delta, 0).all().all()
    else:
        f1, f2 = dispatch[(increasing, strict)]
        assert np.all(f1(delta, 0).all() | f2(delta, 0).all())
    return df

def is_shape(df, shape):
    """
    Asserts that the DataFrame is of a known shape.

    Parameters
    ==========

    df: DataFrame
    shape : tuple (n_rows, n_columns)
    """
    assert df.shape == shape
    return df

def unique_index(df):
    """Assert that the index is unique"""
    assert df.index.is_unique
    return df


def within_set(df, items=None):
    """
    Assert that df is a subset of items

    Parameters
    ==========

    df : DataFrame
    items : dict
        mapping of columns (k) to array-like of values (v) that
        ``df[k]`` is expected to be a subset of
    """
    for k, v in items.items():
        if not df[k].isin(v).all():
            raise AssertionError
    return df

def within_range(df, items=None):
    """
    Assert that a DataFrame is within a range.

    Parameters
    ==========
    df : DataFame
    items : dict
        mapping of columns (k) to a (low, high) tuple (v)
        that ``df[k]`` is expected to be between.
    """
    for k, (lower, upper) in items.items():
        if (lower > df[k]).any() or (upper < df[k]).any():
            raise AssertionError
    return df

def within_n_std(df, n=3):
    means = df.means()
    stds = df.std()
    if not (np.abs(df - means) < n * stds).all().all():
        raise AssertionError
    return df

__all__ = [is_monotonic, is_shape, none_missing, unique_index, within_n_std,
           within_range, within_set]
