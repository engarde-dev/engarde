# -*- coding: utf-8 -*-
"""
checks.py

Each function in here should

- Take a DataFrame as its first argument, maybe optional arguments
- Makes its assert on the result
- Return the original DataFrame
"""
import numpy as np
import pandas as pd

def none_missing(df, columns=None):
    """
    Asserts that there are no missing values (NaNs) in the DataFrame.
    """
    if columns is None:
        columns = df.columns
    assert not df[columns].isnull().any().any()
    return df

def is_monotonic(df, items=None, increasing=None, strict=False):
    """
    Asserts that the DataFrame is monotonic

    Parameters
    ==========

    df : Series or DataFrame
    items : dict
        mapping columns to conditions (increasing, strict)
    increasing : None or bool
        None is either increasing or decreasing.
    strict: whether the comparison should be strict
    """
    if items is None:
        items = {k: (increasing, strict) for k in df}

    for col, (increasing, strict) in items.items():
        s = pd.Index(df[col])
        if increasing:
            good = getattr(s, 'is_monotonic_increasing')
        elif increasing is None:
            good = getattr(s, 'is_monotonic') | getattr(s, 'is_monotonic_decreasing')
        else:
            good = getattr(s, 'is_monotonic_decreasing')
        if strict:
            if increasing:
                good = good & (s.to_series().diff().dropna() > 0).all()
            elif increasing is None:
                good = good & ((s.to_series().diff().dropna() > 0).all() |
                               (s.to_series().diff().dropna() < 0).all())
            else:
                good = good & (s.to_series().diff().dropna() < 0).all()
        if not good:
            raise AssertionError
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
