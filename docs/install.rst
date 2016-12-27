Installation and Dependencies
=============================

Engarde itself is pure python, so I'd just use ``pip``::

    pip install engarde

It does depend on ``pandas``, which may be more difficult to pip
install. You might consider conda_ if you have trouble installing
pandas and its dependencies. Once you have the dependencies sorted out
a ``pip install engarde`` should work.

.. _conda: http://conda.pydata.org

If you're using conda, ``engarde`` is available in the `conda-forge` channel::

    conda install -c conda-forge engarde
