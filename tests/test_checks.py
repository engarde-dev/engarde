# -*- coding: utf-8 -*-
import pytest
import numpy as np
import pandas as pd
import pandas.util.testing as tm

import engarde.checks as ck
import engarde.decorators as dc


def _add_one(df):
    return df + 1

def _noop(df):
    return df

def test_none_missing():
    df = pd.DataFrame(np.random.randn(5, 3))
    result = ck.none_missing(df)
    tm.assert_frame_equal(df, result)

    result = dc.none_missing()(_add_one)(df)
    tm.assert_frame_equal(result, df + 1)


def test_none_missing_raises():
    df = pd.DataFrame(np.random.randn(5, 3))
    df.iloc[0, 0] = np.nan
    with pytest.raises(AssertionError):
        ck.none_missing(df)

    with pytest.raises(AssertionError):
        dc.none_missing()(_add_one)(df)

def test_monotonic_increasing_lax():
    df = pd.DataFrame([1, 2, 2])
    tm.assert_frame_equal(df, ck.is_monotonic(df, increasing=True))
    result = dc.is_monotonic(increasing=True)(_add_one)(df)
    tm.assert_frame_equal(result, df + 1)

    df = pd.DataFrame([1, 2, 1])
    with pytest.raises(AssertionError):
        ck.is_monotonic(df, increasing=True)
    with pytest.raises(AssertionError):
        dc.is_monotonic(increasing=True)(_add_one)(df)

    df = pd.DataFrame([3, 2, 1])
    with pytest.raises(AssertionError):
        ck.is_monotonic(df, increasing=True)
    with pytest.raises(AssertionError):
        dc.is_monotonic(increasing=True)(_add_one)(df)

def test_monotonic_increasing_strict():
    df = pd.DataFrame([1, 2, 3])
    tm.assert_frame_equal(df, ck.is_monotonic(df, increasing=True, strict=True))
    result = dc.is_monotonic(increasing=True, strict=True)(_add_one)(df)
    tm.assert_frame_equal(result, df + 1)

    df = pd.DataFrame([1, 2, 2])
    with pytest.raises(AssertionError):
        ck.is_monotonic(df, increasing=True, strict=True)
    with pytest.raises(AssertionError):
        dc.is_monotonic(increasing=True, strict=True)(_add_one)(df)

    df = pd.DataFrame([3, 2, 1])
    with pytest.raises(AssertionError):
        ck.is_monotonic(df, increasing=True, strict=True)
    with pytest.raises(AssertionError):
        dc.is_monotonic(increasing=True, strict=True)(_add_one)(df)

def test_monotonic_decreasing():
    df = pd.DataFrame([2, 2, 1])
    tm.assert_frame_equal(df, ck.is_monotonic(df, increasing=False))
    result = dc.is_monotonic(increasing=False)(_add_one)(df)
    tm.assert_frame_equal(result, df + 1)

    df = pd.DataFrame([1, 2, 1])
    with pytest.raises(AssertionError):
        ck.is_monotonic(df, increasing=False)
    with pytest.raises(AssertionError):
        dc.is_monotonic(increasing=False)(_add_one)(df)

    df = pd.DataFrame([1, 2, 3])
    with pytest.raises(AssertionError):
        ck.is_monotonic(df, increasing=False)
    with pytest.raises(AssertionError):
        dc.is_monotonic(increasing=False)(_add_one)(df)

def test_monotonic_decreasing_strict():
    df = pd.DataFrame([3, 2, 1])
    tm.assert_frame_equal(df, ck.is_monotonic(df, increasing=False,
                                              strict=True))
    result = dc.is_monotonic(increasing=False, strict=True)(_add_one)(df)
    tm.assert_frame_equal(result, df + 1)

    df = pd.DataFrame([2, 2, 1])
    with pytest.raises(AssertionError):
        ck.is_monotonic(df, increasing=False, strict=True)
    with pytest.raises(AssertionError):
        dc.is_monotonic(increasing=False, strict=True)(_add_one)(df)

    df = pd.DataFrame([1, 2, 3])
    with pytest.raises(AssertionError):
        ck.is_monotonic(df, increasing=False, strict=True)
    with pytest.raises(AssertionError):
        dc.is_monotonic(increasing=False, strict=True)(_add_one)(df)

def test_monotonic_either():
    df = pd.DataFrame({'A': [1, 2, 2], 'B': [3, 2, 2]})
    tm.assert_frame_equal(df, ck.is_monotonic(df))
    result = dc.is_monotonic()(_add_one)(df)
    tm.assert_frame_equal(result, df + 1)

    df = pd.DataFrame({'A': [1, 2, 3], 'B': [1, 2, 1]})
    with pytest.raises(AssertionError):
        ck.is_monotonic(df)
    with pytest.raises(AssertionError):
        dc.is_monotonic()(_add_one)(df)

def test_monotonic_either_stict():
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [3, 2, 1]})
    tm.assert_frame_equal(df, ck.is_monotonic(df, strict=True))
    result = dc.is_monotonic(strict=True)(_add_one)(df)
    tm.assert_frame_equal(result, df + 1)

    df = pd.DataFrame({'A': [1, 2, 2], 'B': [3, 2, 2]})
    with pytest.raises(AssertionError):
        ck.is_monotonic(df, strict=True)
    with pytest.raises(AssertionError):
        dc.is_monotonic(strict=True)(_add_one)(df)

def test_monotonic_items():
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [3, 2, 3]})
    tm.assert_frame_equal(df, ck.is_monotonic(df, items={'A': (True, True)}))
    tm.assert_frame_equal(dc.is_monotonic(items={'A': (True, True)}, strict=True)(_add_one)(
        df), df + 1)

def test_is_shape():
    shape = 10, 2
    df = pd.DataFrame(np.random.randn(*shape))
    tm.assert_frame_equal(df, ck.is_shape(df, shape))
    result = dc.is_shape(shape=shape)(_add_one)(df)
    tm.assert_frame_equal(result, df + 1)

    with pytest.raises(AssertionError):
        ck.is_shape(df, (9, 2))
    with pytest.raises(AssertionError):
        dc.is_shape((9, 2))(_add_one)(df)

def test_unique_index():
    df = pd.DataFrame([1, 2, 3], index=['a', 'b', 'c'])
    tm.assert_frame_equal(df, ck.unique_index(df))
    result = dc.unique_index()(_add_one)(df)
    tm.assert_frame_equal(result, df + 1)

    with pytest.raises(AssertionError):
        ck.unique_index(df.reindex(['a', 'a', 'b']))
    with pytest.raises(AssertionError):
        dc.unique_index()(_add_one)(df.reindex(['a', 'a', 'b']))

def test_within_set():
    df = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c']})
    items = {'A': [1, 2, 3], 'B': ['a', 'b', 'c']}
    tm.assert_frame_equal(df, ck.within_set(df, items))
    tm.assert_frame_equal(df, dc.within_set(items=items)(_noop)(df))

    items.pop('A')
    tm.assert_frame_equal(df, ck.within_set(df, items))
    tm.assert_frame_equal(df, dc.within_set(items=items)(_noop)(df))

    items['A'] = [1, 2]
    with pytest.raises(AssertionError):
        ck.within_set(df, items)
    with pytest.raises(AssertionError):
        dc.within_set(items=items)(_noop)(df)

def test_within_range():
    df = pd.DataFrame({'A': [-1, 0, 1]})
    items = {'A': (-1, 1)}
    tm.assert_frame_equal(df, ck.within_range(df, items))
    tm.assert_frame_equal(df, dc.within_range(items)(_noop)(df))

    items['A'] = (0, 1)
    with pytest.raises(AssertionError):
        ck.within_range(df, items)
    with pytest.raises(AssertionError):
        dc.within_range(items)(_noop)(df)

def within_n_std(df):
    df = pd.DataFrame({'A': np.arange(10)})
    tm.assert_frame_equal(df, ck.within_n_std(df))
    tm.assert_frame_equal(df, dc.within_n_std()(_noop)(df))

    with pytest.raisers(AssertionError):
        ck.within_n_std(df, 2)
    with pytest.raisers(AssertionError):
        dc.within_n_std(2)(_noop)(df)

