# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import, division)

import inspect
from functools import wraps
from itertools import zip_longest

import numpy as np
import pandas.core.common as com


import dsadd.checks as checks

def none_missing(columns=None):
    """Asserts that no missing values (NaN) are found"""
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            none_missing(df)
            return result
        return wrapper
    return decorate


def known_shape(shape):

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            checks.known_shape(result, shape)
        return wrapper
    return decorate


def unique_index(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        checks.unique_index(result)
        return result
    return wrapper


def is_monotonic(increasing=None, strict=False):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            checks.is_monotonic(result, increasing=increasing, strict=strict)
            return result
        return wrapper
    return decorate

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
            within_set(df, items)
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

    Raises
    ======

    ValueError
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            within_range(result, items)
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
            within_n_std(result, n=n)
            return result
        return wrapper
    return decorate

