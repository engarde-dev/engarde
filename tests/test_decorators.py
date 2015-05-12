import unittest

import numpy as np
import pandas as pd

import dsadd.decorators as d


class TestDecorators(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame([[1, 2], [3, np.nan]])

        def f(x):
            return x

        self.noop = f

    def test_no_missing(self):

        with self.assertRaises(ValueError):
            # this is why we have decorators
            # equiv to @d.no_missing()
            #          def f(df)
            d.no_missing()(self.noop)(self.df)

        d.no_missing()(self.noop)(self.df.fillna(0))

    def test_no_missing_badout(self):
        df = pd.DataFrame({'A': [1, 2], 'B': [1, 2]})
        with self.assertRaises(ValueError):
            d.no_missing()(lambda x: x.diff())(df)
        df.loc[0, 'A'] = np.nan
        with self.assertRaises(ValueError):
            d.no_missing(columns=['A'], check_input=True,
                         check_output=True)(self.noop)(df)

    def test_know_snape(self):

        @d.known_shape((2, 2))
        def f(x):
            return x

        f(self.df)

        df = self.df.append([2, 2])
        with self.assertRaises(ValueError):
            f(df)

    def test_unique_index(self):
        @d.unique_index
        def f(x):
            return x
        f(self.df)
        self.df.index = np.ones(len(self.df))
        with self.assertRaises(ValueError):
            f(self.df)

    def test_monotonic(self):
        df = pd.DataFrame({'A': [1, 2], 'B': [1, 1]})

        @d.monotonic
        def f(x):
            return x
        f(df)
        df = pd.DataFrame({'A': [1, 3, 1]})
        with self.assertRaises(ValueError):
            f(df)

    def test_monotonic_increasing(self):
        pass

    def test_within_set(self):
        df = pd.DataFrame({'A': [1, 2], 'B': ['a', 'b']})

        @d.within_set({'A': [1, 2, 3], 'B': ['a', 'b']})
        def f(x):
            return x
        f(df)

        @d.within_set({'A': [1]})
        def f(x):
            return x
        with self.assertRaises(ValueError):
            f(df)
