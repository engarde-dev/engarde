# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

import pytest
import engarde.decorators as ed

def _noop(df):
    return df

def _plus_n(df, n):
    return df + n

def is_pos(x, offset=0):
    assert np.all(x - offset >= 0)


def test_decoratize():
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [2, 3, 4]})

    w = ed.decoratize(is_pos)

    @w
    def _plus_n(df, n):
        return df + n
    _plus_n(df, 1)

    with pytest.raises(AssertionError):
        _plus_n(df, -10)

    check = ed.decoratize(is_pos)

    @check(offset=1)
    def _plus_n(df, n):
        return df + n
    _plus_n(df, 0)

    # import ipdb; ipdb.set_trace()
    with pytest.raises(AssertionError):
        _plus_n(df, -0.1)
