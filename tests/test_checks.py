# -*- coding: utf-8 -*-
import pytest
import numpy as np
import pandas as pd
import pandas.util.testing as tm

import engarde.checks as ck
import engarde.decorators as dc


def _add_n(df, n=1):
    return df + n

def _noop(df):
    return df

def test_none_missing():
    df = pd.DataFrame(np.random.randn(5, 3))
    result = ck.none_missing(df)
    tm.assert_frame_equal(df, result)

    result = dc.none_missing()(_add_n)(df, 2)
    tm.assert_frame_equal(result, df + 2)
    result = dc.none_missing()(_add_n)(df, n=2)
    tm.assert_frame_equal(result, df + 2)

def test_none_missing_raises():
    df = pd.DataFrame(np.random.randn(5, 3))
    df.iloc[0, 0] = np.nan
    with pytest.raises(AssertionError):
        ck.none_missing(df)

    with pytest.raises(AssertionError):
        dc.none_missing()(_add_n)(df, n=2)

def test_monotonic_increasing_lax():
    df = pd.DataFrame([1, 2, 2])
    tm.assert_frame_equal(df, ck.is_monotonic(df, increasing=True))
    result = dc.is_monotonic(increasing=True)(_add_n)(df)
    tm.assert_frame_equal(result, df + 1)

    df = pd.DataFrame([1, 2, 1])
    with pytest.raises(AssertionError):
        ck.is_monotonic(df, increasing=True)
    with pytest.raises(AssertionError):
        dc.is_monotonic(increasing=True)(_add_n)(df)

    df = pd.DataFrame([3, 2, 1])
    with pytest.raises(AssertionError):
        ck.is_monotonic(df, increasing=True)
    with pytest.raises(AssertionError):
        dc.is_monotonic(increasing=True)(_add_n)(df)

def test_monotonic_increasing_strict():
    df = pd.DataFrame([1, 2, 3])
    tm.assert_frame_equal(df, ck.is_monotonic(df, increasing=True, strict=True))
    result = dc.is_monotonic(increasing=True, strict=True)(_add_n)(df)
    tm.assert_frame_equal(result, df + 1)

    df = pd.DataFrame([1, 2, 2])
    with pytest.raises(AssertionError):
        ck.is_monotonic(df, increasing=True, strict=True)
    with pytest.raises(AssertionError):
        dc.is_monotonic(increasing=True, strict=True)(_add_n)(df)

    df = pd.DataFrame([3, 2, 1])
    with pytest.raises(AssertionError):
        ck.is_monotonic(df, increasing=True, strict=True)
    with pytest.raises(AssertionError):
        dc.is_monotonic(increasing=True, strict=True)(_add_n)(df)

def test_monotonic_decreasing():
    df = pd.DataFrame([2, 2, 1])
    tm.assert_frame_equal(df, ck.is_monotonic(df, increasing=False))
    result = dc.is_monotonic(increasing=False)(_add_n)(df)
    tm.assert_frame_equal(result, df + 1)

    df = pd.DataFrame([1, 2, 1])
    with pytest.raises(AssertionError):
        ck.is_monotonic(df, increasing=False)
    with pytest.raises(AssertionError):
        dc.is_monotonic(increasing=False)(_add_n)(df)

    df = pd.DataFrame([1, 2, 3])
    with pytest.raises(AssertionError):
        ck.is_monotonic(df, increasing=False)
    with pytest.raises(AssertionError):
        dc.is_monotonic(increasing=False)(_add_n)(df)

def test_monotonic_decreasing_strict():
    df = pd.DataFrame([3, 2, 1])
    tm.assert_frame_equal(df, ck.is_monotonic(df, increasing=False,
                                              strict=True))
    result = dc.is_monotonic(increasing=False, strict=True)(_add_n)(df)
    tm.assert_frame_equal(result, df + 1)

    df = pd.DataFrame([2, 2, 1])
    with pytest.raises(AssertionError):
        ck.is_monotonic(df, increasing=False, strict=True)
    with pytest.raises(AssertionError):
        dc.is_monotonic(increasing=False, strict=True)(_add_n)(df)

    df = pd.DataFrame([1, 2, 3])
    with pytest.raises(AssertionError):
        ck.is_monotonic(df, increasing=False, strict=True)
    with pytest.raises(AssertionError):
        dc.is_monotonic(increasing=False, strict=True)(_add_n)(df)

def test_monotonic_either():
    df = pd.DataFrame({'A': [1, 2, 2], 'B': [3, 2, 2]})
    tm.assert_frame_equal(df, ck.is_monotonic(df))
    result = dc.is_monotonic()(_add_n)(df)
    tm.assert_frame_equal(result, df + 1)

    df = pd.DataFrame({'A': [1, 2, 3], 'B': [1, 2, 1]})
    with pytest.raises(AssertionError):
        ck.is_monotonic(df)
    with pytest.raises(AssertionError):
        dc.is_monotonic()(_add_n)(df)

def test_monotonic_either_stict():
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [3, 2, 1]})
    tm.assert_frame_equal(df, ck.is_monotonic(df, strict=True))
    result = dc.is_monotonic(strict=True)(_add_n)(df)
    tm.assert_frame_equal(result, df + 1)

    df = pd.DataFrame({'A': [1, 2, 2], 'B': [3, 2, 2]})
    with pytest.raises(AssertionError):
        ck.is_monotonic(df, strict=True)
    with pytest.raises(AssertionError):
        dc.is_monotonic(strict=True)(_add_n)(df)

def test_monotonic_items():
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [3, 2, 3]})
    tm.assert_frame_equal(df, ck.is_monotonic(df, items={'A': (True, True)}))
    tm.assert_frame_equal(dc.is_monotonic(items={'A': (True, True)}, strict=True)(_add_n)(
        df), df + 1)

def test_is_shape():
    shape = 10, 2
    ig_0 = -1, 2
    ig_1 = 10, -1
    ig_2 = None, 2
    ig_3 = 10, None
    shapes = [shape, ig_0, ig_1, ig_2, ig_3]
    df = pd.DataFrame(np.random.randn(*shape))
    for shp in shapes:
        tm.assert_frame_equal(df, ck.is_shape(df, shp))
    for shp in shapes:
        result = dc.is_shape(shape=shp)(_add_n)(df)
        tm.assert_frame_equal(result, df + 1)

    with pytest.raises(AssertionError):
        ck.is_shape(df, (9, 2))
    with pytest.raises(AssertionError):
        dc.is_shape((9, 2))(_add_n)(df)

def test_unique_index():
    df = pd.DataFrame([1, 2, 3], index=['a', 'b', 'c'])
    tm.assert_frame_equal(df, ck.unique_index(df))
    result = dc.unique_index()(_add_n)(df)
    tm.assert_frame_equal(result, df + 1)

    with pytest.raises(AssertionError):
        ck.unique_index(df.reindex(['a', 'a', 'b']))
    with pytest.raises(AssertionError):
        dc.unique_index()(_add_n)(df.reindex(['a', 'a', 'b']))

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

def test_within_n_std():
    df = pd.DataFrame({'A': np.arange(10)})
    tm.assert_frame_equal(df, ck.within_n_std(df))
    tm.assert_frame_equal(df, dc.within_n_std()(_noop)(df))

    with pytest.raises(AssertionError):
        ck.within_n_std(df, .5)
    with pytest.raises(AssertionError):
        dc.within_n_std(.5)(_noop)(df)

def test_has_dtypes():
    df = pd.DataFrame({'A': np.random.randint(0, 10, 10),
                       'B': np.random.randn(10),
                       'C': list('abcdefghij'),
                       'D': pd.Categorical(np.random.choice(['a', 'b'], 10))})
    dtypes = {'A': int, 'B': 'float', 'C': object, 'D': 'category'}
    tm.assert_frame_equal(df, ck.has_dtypes(df, dtypes))
    tm.assert_frame_equal(df, dc.has_dtypes(items=dtypes)(_noop)(df))

    with pytest.raises(AssertionError):
        ck.has_dtypes(df, {'A': float})

    with pytest.raises(AssertionError):
        dc.has_dtypes(items={'A': bool})(_noop)(df)

def test_one_to_many():
    df = pd.DataFrame({
        'parameter': ['Cu', 'Cu', 'Pb', 'Pb'],
        'units': ['ug/L', 'ug/L', 'ug/L', 'ug/L'],
        'res': [2.0, 4.0, 6.0, 8.0]
    })
    result = ck.one_to_many(df, 'units', 'parameter')
    tm.assert_frame_equal(df, result)

def test_one_to_many_raises():
    df = pd.DataFrame({
        'parameter': ['Cu', 'Cu', 'Pb', 'Pb'],
        'units': ['ug/L', 'ug/L', 'ug/L', 'mg/L'],
        'res': [2.0, 4.0, 6.0, 0.008]
    })
    with pytest.raises(AssertionError):
        ck.one_to_many(df, 'units', 'parameter')

def test_verify():
    f = lambda x, n: len(x) > n
    df = pd.DataFrame({'A': [1, 2, 3]})
    tm.assert_frame_equal(df, ck.verify(df, f, n=2))
    tm.assert_frame_equal(df, ck.verify(df, f, 2))

    # order is verify_func, verif_kwargs, decorated_func
    tm.assert_frame_equal(df, dc.verify(f, n=2)(_noop)(df))
    tm.assert_frame_equal(df, dc.verify(f, 2)(_noop)(df))

    with pytest.raises(AssertionError):
        ck.verify(df, f, n=4)
        dc.verify(f, n=4)(_noop)(df)

def test_verify_all():
    f = lambda x, n: x > n
    df = pd.DataFrame({'A': [1, 2, 3]})
    tm.assert_frame_equal(df, ck.verify_all(df, f, 0))
    tm.assert_frame_equal(df, ck.verify_all(df, f, n=0))

    with pytest.raises(AssertionError):
        ck.verify_all(df, f, n=2)
        dc.verify_all(f, n=2)(df)

def test_verify_any():
    f = lambda x, n: x > n
    df = pd.DataFrame({'A': [1, 2, 3]})
    tm.assert_frame_equal(df, ck.verify_any(df, f, 2))
    tm.assert_frame_equal(df, ck.verify_any(df, f, n=2))

    with pytest.raises(AssertionError):
        ck.verify_any(df, f, n=4)
        dc.verify_any(f, n=4)(df)


