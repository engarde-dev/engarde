# -*- coding: utf-8 -*-
from itertools import chain, cycle

import numpy as np
import pandas as pd

def bad_locations(df):
    columns = df.columns
    all_locs = chain.from_iterable(zip(df.index, cycle([col])) for col in columns)
    bad = pd.Series(list(all_locs))[np.asarray(df).ravel(1)]
    msg = bad.values
    return msg

