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
Engarde is a lightweight way to explicitly state your assumptions
and check that they're *actually* true.

.. code-block:: python

   @is_shape(-1, 10)
   @is_monotonic(strict=True)
   @none_missing()
   def compute(df):
       ...
       return result

We state our assumptions as decorators, and verify that they are true
upon the result of the function.

Usage
=====

There are two main ways to use engarde, depending on whether you're
working interactively or not.
For interactive use, I'd suggest using ``DataFrame.pipe`` to run the
check.
For non-interactive use, each of the checks are wrapped into a
decorator. You can decorate the functions that makeup your ETL pipeline
with the checks that should hold true at that stage in the pipeline.
Checkout :any:`example` to see engarde in action.

Contents
========

.. toctree::
   :maxdepth: 2

   install.rst
   example.rst
   api.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

