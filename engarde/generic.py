# -*- coding: utf-8 -*-
"""
Module for useful generic functions.
"""
from itertools import chain, cycle

import numpy as np
import pandas as pd


# --------------
# Generic verify
# --------------

def verify(df, check, *args, **kwargs):
    """
    Generic verify. Assert that check(df, **kwargs) is True

    Parameters
    ==========
    df : DataFrame
    check : function
        Should take DataFrame and **kwargs. Returns bool

    Returns
    =======
    df : DataFrame
        same as the input.
    """
    result = check(df, *args, **kwargs)
    try:
        assert result
    except AssertionError as e:
        msg = '{} is not true'.format(check.__name__)
        e.args = (msg, df)
        raise
    return df

def verify_all(df, check, *args, **kwargs):
    result = check(df, *args, **kwargs)
    try:
        assert np.all(result)
    except AssertionError as e:
        msg = "{} not true for all".format(check.__name__)
        e.args = (msg, df[~result])
        raise
    return df

def verify_any(df, check, *args, **kwargs):
    result = check(df, *args, **kwargs)
    try:
        assert np.any(result)
    except AssertionError as e:
        msg = '{} not true for any'.format(check.__name__)
        e.args = (msg, df)
        raise
    return df

# ---------------
# Error reporting
# ---------------

def bad_locations(df):
    columns = df.columns
    all_locs = chain.from_iterable(zip(df.index, cycle([col])) for col in columns)
    bad = pd.Series(list(all_locs))[np.asarray(df).ravel(1)]
    msg = bad.values
    return msg

__all__ = [verify, verify_all, verify_any, bad_locations]

