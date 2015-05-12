# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import, division)

import inspect
from functools import wraps
from itertools import zip_longest

import pandas.core.common as com


def no_missing(columns=None, check_input=False, check_output=True):
    """Asserts that no missing values (NaN) are found"""
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            df = _extract_frame(func, *args, **kwargs)
            if check_input:
                if _any_missing(df):
                    raise ValueError("Missing Values")
            result = func(*args, **kwargs)
            if check_output:
                if _any_missing(result):
                    raise ValueError("Missing Values")
            return result
        return wrapper
    return decorate


def known_shape(shape):

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            df = args[0]
            if not df.shape == shape:
                raise ValueError("Bad shape")
            return func(*args, **kwargs)
        return wrapper
    return decorate


def unique_index(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if not result.index.is_unique:
            raise ValueError("Non-unique Index!")
        return result
    return wrapper


def monotonic(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if not _is_monotonic(result):
            raise ValueError("Not monotionic!")
        return result
    return wrapper


def within_set(items):
    """
    Check that DataFrame values are within set.

    @within_set({'A': {1, 3}})
    def f(df):
        return df
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            for k, v in items.items():
                if not result[k].isin(v).all():
                    raise ValueError("Not in Set!")
            return result
        return wrapper
    return decorate


def within_range(items, columns=None, check_input=False, check_output=True):
    """
    Check that a DataFrame's values are within a range.

    Parameters
    ==========

    items : dict or array-like
        dict maps columss to (lower, upper)
        array-like checks the same (lower, upper) for each column
    columns : list
        columns to limit the check to
    check_input : bool
    check_output : bool

    Raises
    ======

    ValueError
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            df = _extract_frame(func, args, kwargs)
            if check_input:
                eitems = _ensure_items_input(items=items, columns=columns)
                _is_within_range(df, eitems)
            result = func(*args, **kwargs)
            if check_output:
                eitems = _ensure_items_input(items=items, columns=columns)
                _is_within_range(result, eitems)
            return result
        return wrapper
    return decorate


def _is_monotonic(df, increasing=True, decreasing=True, strictly=False):
    from operator import gt, lt, ge, le
    change = df.diff().iloc[1:]
    ops = []

    if strictly and increasing:
        ops.append(gt)
    elif strictly and decreasing:
        ops.append(lt)
    elif not strictly and increasing:
        ops.append(ge)
    elif not strictly and decreasing:
        ops.append(le)

    return all(op(change, 0).all().all() for op in ops)


def _is_within_range(df, items):
    for col, (lower, upper) in items.items():
        if (lower > df[col]).any() or (upper < df[col]).any():
            return False
    return True


def _any_missing(df):
    return df.isnull().any().any()


def _ensure_items_input(df, items, columns=None):
    if columns is None:
        columns = df.columns
    if com.is_list_like(items):
        items = dict(zip_longest(columns, [items], fillvalue=items))

    return items

def _extract_frame(func, *args, **kwargs):
    try:
        df = args[0]
    except IndexError:
        df = kwargs.get(inspect.getargspec(func).args[0])
    return df
