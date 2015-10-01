from abc import ABCMeta, abstractmethod

import pandas as pd
from pandas.core.frame import NDFrame
from functools import wraps

class Guard(metaclass=ABCMeta):

    def __new__(cls, *args, **kwargs):
        if len(args) > 0 and isinstance(args[0], NDFrame):
            return cls.check(*args, **kwargs)
        else:
            # we're a decorator
            def decorate(func):
                @wraps(func)
                def wrapper(*args, **kwargs):
                    result = func(*args, **kwargs)
                    cls.check(result)
                    return result
                return wrapper
            return decorate

    @staticmethod
    @abstractmethod
    def check(*args, **kwargs):
        pass

class none_missing(Guard):

    @classmethod
    def check(cls, df, columns=None):
        columns = df.columns if columns is None else columns
        assert not pd.isnull(df[columns]).any().any()
        return df

class is_monotonic(Guard):

    @staticmethod
    def check(df, items=None, increasing=None, strict=False):
        """
        Asserts that the DataFrame is monotonic.

        Parameters
        ==========

        df : Series or DataFrame
        items : dict
            mapping columns to conditions (increasing, strict)
        increasing : None or bool
            None is either increasing or decreasing.
        strict : whether the comparison should be strict

        Returns
        =======
        df : DataFrame
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

class is_shape(Guard):

    @staticmethod
    def check(df, shape):
        """
        Asserts that the DataFrame is of a known shape.

        Parameters
        ==========

        df : DataFrame
        shape : tuple
        (n_rows, n_columns). Use None or -1 if you don't care
        about a dimension.

        Returns
        =======
        df : DataFrame
        """
        try:
            check = np.all(np.equal(df.shape, shape) | (np.equal(shape, [-1, -1]) |
                                                        np.equal(shape, [None, None])))
            assert check
        except AssertionError as e:
            msg = ("Expected shape: {}\n"
                "\t\tActual shape:   {}".format(shape, df.shape))
            e.args = (msg,)
            raise
        return df

class unique_index(Guard):

    @staticmethod
    def check(df):
        """
        Assert that the index is unique

        Parameters
        ==========
        df : DataFrame

        Returns
        =======
        df : DataFrame
        """
        try:
            assert df.index.is_unique
        except AssertionError as e:
            e.args = df.index.get_duplicates()
            raise
        return df


class within_set(Guard):

    @staticmethod
    def check(df, items=None):
        """
        Assert that df is a subset of items

        Parameters
        ==========
        df : DataFrame
        items : dict
        mapping of columns (k) to array-like of values (v) that
        ``df[k]`` is expected to be a subset of

        Returns
        =======
        df : DataFrame
        """
        for k, v in items.items():
            if not df[k].isin(v).all():
                bad = df.loc[~df[k].isin(v), k]
                raise AssertionError('Not in set', bad)
        return df


class within_range(Guard):

    @staticmethod
    def check(df, items=None):
        """
        Assert that a DataFrame is within a range.

        Parameters
        ==========
        df : DataFame
        items : dict
        mapping of columns (k) to a (low, high) tuple (v)
        that ``df[k]`` is expected to be between.

        Returns
        =======
        df : DataFrame
        """
        for k, (lower, upper) in items.items():
            if (lower > df[k]).any() or (upper < df[k]).any():
                bad = (lower > df[k]) | (upper < df[k])
                raise AssertionError("Outside range", bad)
        return df


class within_n_std(Guard):

    @staticmethod
    def within_n_std(df, n=3):
        """
        Assert that every value is within ``n`` standard
        deviations of its column's mean.

        Parameters
        ==========
        df : DataFame
        n : int
        number of standard devations from the mean

        Returns
        =======
        df : DatFrame
        """
        means = df.mean()
        stds = df.std()
        inliers = (np.abs(df - means) < n * stds)
        if not np.all(inliers):
            msg = generic.bad_locations(~inliers)
            raise AssertionError(msg)
        return df



class has_dtypes(Guard):

    @staticmethod
    def check(df, items):
        """
        Assert that a DataFrame has ``dtypes``

        Parameters
        ==========
        df: DataFrame
        items: dict
        mapping of columns to dtype.

        Returns
        =======
        df : DataFrame
        """
        dtypes = df.dtypes
        for k, v in items.items():
            if not dtypes[k] == v:
                raise AssertionError("{} has the wrong dtype ({})".format(k, v))
        return df


class one_to_many(Guard):

    @staticmethod
    def one_to_many(df, unitcol, manycol):
        """
        Assert that a many-to-one relationship is preserved between two
        columns. For example, a retail store will have have distinct
        departments, each with several employees. If each employee may
        only work in a single department, then the relationship of the
        department to the employees is one to many.

        Parameters
        ==========
        df : DataFrame
        unitcol : str
            The column that encapulates the groups in ``manycol``.
        manycol : str
            The column that must remain unique in the distict pairs
            between ``manycol`` and ``unitcol``

        Returns
        =======
        df : DataFrame

        """
        subset = df[[manycol, unitcol]].drop_duplicates()
        for many in subset[manycol].unique():
            if subset[subset[manycol] == many].shape[0] > 1:
                msg = "{} in {} has multiple values for {}".format(many, manycol, unitcol)
                raise AssertionError(msg)

        return df


class verify(Guard):

    @staticmethod
    def verify(func, *args, **kwargs):
        """
        Assert that `func(df, *args, **kwargs)` is true.
        """
        return _verify(func, None, *args, **kwargs)

class verify_all(Guard):

    @staticmethod
    def check(func, *args, **kwargs):
        """
        Assert that all of `func(*args, **kwargs)` are true.
        """
        result = check(df, *args, **kwargs)
        try:
            assert np.all(result)
        except AssertionError as e:
            msg = "{} not true for all".format(check.__name__)
            e.args = (msg, df[~result])
            raise
        return df

class verify_any(Guard):

    @staticmethod
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


__all__ = ['is_monotonic', 'is_shape', 'none_missing', 'unique_index', 'within_n_std',
           'within_range', 'within_set', 'has_dtypes',
           'verify', 'verify_all', 'verify_any']




