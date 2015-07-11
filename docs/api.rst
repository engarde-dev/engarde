API
===

checks
------

This file contains the functions doing the actual asserts.
You can potentially use this file during interactive sessions,
probably via the ``pipe`` method.

.. automodule:: engarde.checks
   :members:


decorators
----------

.. automodule:: engarde.decorators
   :members:

This file provides a nice API for each of the checks, designed to fit
seamlessly into an ETL pipeline. Each of the functions defined here
can be applied to a functino that returns a DataFrame.

