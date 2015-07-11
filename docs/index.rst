.. engarde documentation master file, created by
   sphinx-quickstart on Wed Jul  8 20:37:13 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Engarde!
========

Engarde is a package for defensive data analysis.

Why?
====

The *raison d'être* for engarde is the fact of life that data are messy.
To do our analysis, we often have certain assumptions about our data
that *should* be invariant across updates to your dataset.
`engarde` is a lightweight way to explicitly state your assumptions
and check that they're *actually* true.

Here's a quick example of a nice little pipeline to calculate
the 7-day moving average for a few stocks.

.. code-block:: python

   >>> from engarde import checks
   >>> from pandas.io.data import DataReader
   >>> stocks = ['AAPL', 'F', 'GOOG']
   >>> df = (DataReader(stocks, data_source='yahoo',
                        start='2010-01-01', end='2015-06-01')
             .to_frame(filter_observations=False)
             .swaplevel('minor', 'Date')
             .sort_index()
             .groupby(level='minor')
             .apply(pd.rolling_mean, 7))

This is an example that we can potentially update each day.
But the web is an unreliable place. Yahoo could change the API
on us at any time, or perhaps one of the Series isn't returned
correctly. Let's make sure we get the correct columns.

.. code-block:: python

   >>> df = (DataReader(stocks, data_source='yahoo',
                        start='2010-01-01', end='2015-06-01')
             .to_frame(filter_observations=False)
             .swaplevel('minor', 'Date')
             .sort_index())
   >>> assert np.all(df.index.levels[0] == stocks)
   >>> df.groupby(level='minor').apply(pd.rolling_mean, 7)

OK, that's fine, but it broke up our nice chain. Let's use
engarde to make the check.

.. code-block:: python

   >>> df = (DataReader(stocks, data_source='yahoo',
                        start='2010-01-01', end='2015-06-01')
             .to_frame(filter_observations=False)
             .swaplevel('minor', 'Date')
             .sort_index()
             .pipe(checks.verify_all, lambda df: df.index.levels[0] == stocks)
             .groupby(level='minor').apply(pd.rolling_mean, 7))

Cool! Well, maybe not breaking chains isn't most compelling reason
to use engarde.
The real reason I wrote engarde was because I was sick of rewriting
the same set of basic checks for each project I worked on.

Structure
=========

Engarde defines a bunch of checks in ``engarde.checks``. Each of these
checks take a ``DataFrame`` (and maybe positional and keyword arguments),
asserts that the check is true, and returns the input ``DataFrame``.


Usage
=====

There are two main ways to use engarde, depending on whether you're
working interactively or not.
For interactive use, I'd suggest using ``DataFrame.pipe`` to run the
check.
For non-interactive use, each of the checks are wrapped into a
decorator. You can decorate the functions that makeup your ETL pipeline
with the checks that should hold true at that stage in the pipeline.

Contents:

.. toctree::
   :maxdepth: 1

   install.rst
   example.rst
   checks.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

