Example
=======

Engarde really shines when you have a dataset that regularly receives updates.
We'll work with a data set of customer preferences on trains, available here_.
This is a static dataset and isn't being updated, but you could imagine that each month the Dutch authorities upload a new month's worth of data.

.. _here: http://vincentarelbundock.github.io/Rdatasets/doc/Ecdat/Train.html

We can start by making some very basic assertions, that the dataset is the correct shape, and that a few columns are the correct dtypes. Assertions are made as decorators to functions that return a DataFrame.

.. ipython:: python

   import pandas as pd
   import engarde.decorators as ed

   pd.set_option('display.max_rows', 10)

   dtypes = dict(
       price1=int,
       price2=int,
       time1=int,
       time2=int,
       change1=int,
       change2=int,
       comfort1=int,
       comfort2=int
   )

   @ed.is_shape((-1, 11))
   @ed.has_dtypes(items=dtypes)
   def unload():
       trains = pd.read_csv("data/trains.csv", index_col=0)
       return trains

One very important part of the design of Engarde is that your code, the code actually
doing the work, shouldn't have to change. I don't want a bunch of asserts cluttering
up the logic of what's happening. This is a perfect case for decorators.

The order of execution here is ``unload`` returns the ``DataFrame``, ``trains``.
Next, ``ed.has_dtypes`` asserts that ``trains`` has the correct dtypes, as specified with ``dtypes``. Once that assert passes, ``has_dtypes`` passes ``trains`` along to the next check, and so on, until the original caller gets back ``unload``.

Since people are rational, their first choice is surely going to be better in *at least* one way than their second choice (faster, more comfortable, ...). This is fundamental to our analysis later on, so we'll explicitly state it in our code, and check it in our data.

.. ipython:: python

   def rational(df):
       """
       Check that at least one criteria is better.
       """
       r = ((df.price1 < df.price2) | (df.time1 < df.time2) |
            (df.change1 < df.change2) | (df.comfort1 > df.comfort2))
       return r

   @ed.is_shape((-1, 11))
   @ed.has_dtypes(items=dtypes)
   @ed.verify_all(rational)
   def unload():
       trains = pd.read_csv("data/trains.csv", index_col=0)
       return trains

    df = unload()
    df.head()

OK, so apparently people aren't rational... We'll fix this problem by ignoring those people (why change your mind when you can change the data?).

.. ipython:: python

   @ed.verify_all(rational)
   def drop_silly_people(df):
       r = ((df.price1 < df.price2) | (df.time1 < df.time2) |
            (df.change1 < df.change2) | (df.comfort1 > df.comfort2))
       return df[r]


   @ed.is_shape((-1, 11))
   @ed.has_dtypes(items=dtypes)
   def unload():
       trains = pd.read_csv("data/trains.csv", index_col=0)
       return trains

    df = unload().pipe(drop_silly_people)
    df.head()

