# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, absolute_import, division)
from functools import wraps


# def no_missing(columns=None, check_input=False, check_output=True):
#     """Asserts that no missing values (NaN) are found"""
#     def decorate(func):
#         @wraps(func)
#         def wrapper(func, *args, **kwargs):
#             df = _extract_frame(func, *args, **kwargs)
#             if check_input:
#                 _no_missing(df)
#             result = func(*args, **kwargs)
#             if check_output:
#                 _no_missing(result)
#             return result
#         return wrapper
#     return decorate

def no_missing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if _any_missing(result):
            raise ValueError("Missing Values")
        return result
    return wrapper


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


def _any_missing(df):
    return df.isnull().any().any()


def _extract_frame(func, *args, **kwargs):
    try:
        df = args[0]
    except IndexError:
        # TODO: argspec
        df = kwargs.get('df')
    return df
