.. _design:

Design
======

It's important that ``engarde`` not get in your way.
Your task is hard enough without a bunch of assertions
cluttering up the logic of the code.
And yet, it does help to explicitly state the assumptions
fundamental to your analysis. Decorators provide a nice
compromise.

Checks
------

Each :ref:`checks` takes a DataFrame, arguments necessary for the check,
asserts the truth of the check, and returns the original DataFrame.
If the assertion fails, an ``AssertionError`` is raised and ``engarde``
tries to print out some informative information about where the failure
occurred.

The exceptions to the above rule are for generic assertions ``verify``,
``verify_all``, and ``verify_any``. These take an additional argument,
``assertion_func``, a function taking a DataFrame and returning some
kind of booleans. You can think of any of the built-in checks, like
``none_missing`` as special cases of the generic verify functions
where ``assertion_func`` has been fixed.

Decorators
----------

Each ``check`` has an associated decorator. The decorator simply marshals
arguments, allowing you to make your assertions *outside* the actual logic
of your code. Personally, this is the most compelling use-case for ``engarde``.
You have a data source that pushes updates to a dataset. The updates are
(or should be) similarly shaped. Perhaps you have some automated reporting
derived from the dataset, and you wish to fail early if a crucial assumption
is violated.

