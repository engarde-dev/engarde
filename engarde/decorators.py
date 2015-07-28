# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import, division)

from functools import wraps

import engarde.checks as ck

def none_missing():
    """Asserts that no missing values (NaN) are found"""
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            ck.none_missing(result)
            return result
        return wrapper
    return decorate


def is_shape(shape):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            ck.is_shape(result, shape)
            return result
        return wrapper
    return decorate


def unique_index():
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            ck.unique_index(result)
            return result
        return wrapper
    return decorate

def is_monotonic(items=None, increasing=None, strict=False):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            ck.is_monotonic(result, items=items, increasing=increasing,
                            strict=strict)
            return result
        return wrapper
    return decorate

def within_set(items):
    """
    Check that DataFrame values are within set.

    >>> @within_set({'A': {1, 3}})
    >>> def f(df):
            return df
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            ck.within_set(result, items)
            return result
        return wrapper
    return decorate


def within_range(items):
    """
    Check that a DataFrame's values are within a range.

    Parameters
    ==========
    items : dict or array-like
        dict maps columss to (lower, upper)
        array-like checks the same (lower, upper) for each column

    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            ck.within_range(result, items)
            return result
        return wrapper
    return decorate


def within_n_std(n=3):
    """
    Tests that all values are within 3 standard deviations
    of their mean.
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            ck.within_n_std(result, n=n)
            return result
        return wrapper
    return decorate

def has_dtypes(items):
    """
    Tests that the dtypes are as specified in items.
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            ck.has_dtypes(result, items)
            return result
        return wrapper
    return decorate


def one_to_many(unitcol, manycol):
    """ Tests that each value in ``manycol`` only is associated with
    just a single value in ``unitcol``.
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            ck.one_to_many(results, unitcol, manycol)
            return result
        return wrapper
    return decorate


def verify(func, *args, **kwargs):
    """
    Assert that `func(df, *args, **kwargs)` is true.
    """
    return _verify(func, None, *args, **kwargs)

def verify_all(func, *args, **kwargs):
    """
    Assert that all of `func(*args, **kwargs)` are true.
    """
    return _verify(func, 'all', *args, **kwargs)

def verify_any(func, *args, **kwargs):
    """
    Assert that any of `func(*args, **kwargs)` are true.
    """
    return _verify(func, 'any', *args, **kwargs)

def _verify(func, _kind, *args, **kwargs):
    d = {None: ck.verify, 'all': ck.verify_all, 'any': ck.verify_any}
    vfunc = d[_kind]

    def decorate(operation_func):
        @wraps(operation_func)
        def wrapper(*operation_args, **operation_kwargs):
            result = operation_func(*operation_args, **operation_kwargs)
            vfunc(result, func, *args, **kwargs)
            return result
        return wrapper
    return decorate

__all__ = ['is_monotonic', 'is_shape', 'none_missing', 'unique_index',
           'within_range', 'within_set', 'has_dtypes', 'verify', 'verify_all',
           'verify_any', 'within_n_std']

