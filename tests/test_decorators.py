import unittest

import numpy as np
import pandas as pd

import dsadd.decorators as d


class TestDecorators(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame([[1, 2], [3, np.nan]])

    def test_no_missing(self):

        @d.no_missing
        def f(x):
            return x

        with self.assertRaises(ValueError):
            f(self.df)

        f(self.df.fillna(0))

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
