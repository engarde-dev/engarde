Example
=======

Engarde really shines when you have a dataset that regularly receives updates.
We'll work with a data set of customer preferences on trains, available here_.
This is a static dataset and isn't being updated, but you could imagine that each month the Dutch authorities upload a new month's worth of data.

.. _here: http://vincentarelbundock.github.io/Rdatasets/doc/Ecdat/Train.html

We can start by making some very basic assertions, that the dataset is the correct shape, and that a few columns are the correct dtypes. Assertions are made as decorators to functions that return a DataFrame.

.. code-block:: python

   In [1]: import pandas as pd

   In [2]: import engarde.decorators as ed

   In [3]: pd.set_option('display.max_rows', 10)

   In [4]: dtypes = dict(
      ...:     price1=int,
      ...:     price2=int,
      ...:     time1=int,
      ...:     time2=int,
      ...:     change1=int,
      ...:     change2=int,
      ...:     comfort1=int,
      ...:     comfort2=int
      ...: )

   In [5]: @ed.is_shape((None, 11))
      ...: @ed.has_dtypes(items=dtypes)
      ...: def unload():
      ...:         trains = pd.read_csv("data/trains.csv", index_col=0)
      ...:         return trains

   In [6]: unload()
   Out[6]:
        id  choiceid   choice  price1  time1  change1  comfort1  price2  time2  \
   1     1         1  choice1    2400    150        0         1    4000    150
   2     1         2  choice1    2400    150        0         1    3200    130
   3     1         3  choice1    2400    115        0         1    4000    115
   4     1         4  choice2    4000    130        0         1    3200    150
   5     1         5  choice2    2400    150        0         1    3200    150
   ..   ..       ...      ...     ...    ...      ...       ...     ...    ...
   347  30         7  choice1    2100    135        1         1    2800    135
   348  30         8  choice1    2100    125        1         1    3500    125
   349  30         9  choice1    2100    150        0         0    2800    125
   350  30        10  choice1    2800    125        0         1    2800    135
   351  30        11  choice2    3500    125        1         0    2800    135

        change2  comfort2
   1          0         1
   2          0         1
   3          0         0
   4          0         0
   5          0         0
   ..       ...       ...
   347        1         0
   348        1         0
   349        0         1
   350        1         0
   351        1         0

   [351 rows x 11 columns]

One very important part of the design of Engarde is that your code, the code actually
doing the work, shouldn't have to change. I don't want a bunch of asserts cluttering
up the logic of what's happening. This is a perfect case for decorators.

The order of execution here is ``unload`` returns the ``DataFrame``, ``trains``.
Next, ``ed.has_dtypes`` asserts that ``trains`` has the correct dtypes, as specified with ``dtypes``. Once that assert passes, ``has_dtypes`` passes ``trains`` along to the next check, and so on, until the original caller gets back ``trains``.

Each row of this dataset contains a passengers preference over two routes. Each route has an associated cost,
travel time, comfort level, and number of changes.
Like any good economist, we'll assume people are rational: their first choice is surely going to be better in *at least* one way than their second choice (faster, more comfortable, ...). This is fundamental to our analysis later on, so we'll explicitly state it in our code, and check it in our data.

.. code-block:: python

   In [7]: def rational(df):
      ...:     """
      ...:     Check that at least one criteria is better.
      ...:     """
      ...:     r = ((df.price1 < df.price2) | (df.time1 < df.time2) |
      ...:          (df.change1 < df.change2) | (df.comfort1 > df.comfort2))
      ...:     return r
      ...:

   In [8]: @ed.is_shape((None, 11))
      ...: @ed.has_dtypes(items=dtypes)
      ...: @ed.verify_all(rational)
      ...: def unload():
      ...:     trains = pd.read_csv("data/trains.csv", index_col=0)
      ...:     return trains
      ...:

   In [9]: df = unload()
   ---------------------------------------------------------------------------
   AssertionError                            Traceback (most recent call last)
   <ipython-input-9-b108f050ce4e> in <module>()
   ----> 1 df = unload()

   /Users/tom.augspurger/sandbox/engarde/engarde/decorators.py in wrapper(*args, **kwargs)
        22         @wraps(func)
        23         def wrapper(*args, **kwargs):
   ---> 24             result = func(*args, **kwargs)
        25             ck.is_shape(result, shape)
        26             return result

   /Users/tom.augspurger/sandbox/engarde/engarde/decorators.py in wrapper(*args, **kwargs)
       115         @wraps(func)
       116         def wrapper(*args, **kwargs):
   --> 117             result = func(*args, **kwargs)
       118             ck.has_dtypes(result, items)
       119             return result

   /Users/tom.augspurger/sandbox/engarde/engarde/decorators.py in wrapper(*operation_args, **operation_kwargs)
       147         def wrapper(*operation_args, **operation_kwargs):
       148             result = operation_func(*operation_args, **operation_kwargs)
   --> 149             vfunc(result, func, *args, **kwargs)
       150             return result
       151         return wrapper

   /Users/tom.augspurger/sandbox/engarde/engarde/generic.py in verify_all(df, check, *args, **kwargs)
        40     result = check(df, *args, **kwargs)
        41     try:
   ---> 42         assert np.all(result)
        43     except AssertionError as e:
        44         msg = "{} not true for all".format(check.__name__)

   AssertionError: ('rational not true for all',      id  choiceid   choice  price1  time1  change1  comfort1  price2  time2  \
   13    2         3  choice2    2450    121        0         0    2450     93
   18    2         8  choice2    2975    108        0         0    2450    108
   27    3         6  choice2    1920    106        0         0    1440     96
   28    3         7  choice1    1920    106        0         0    1920     96
   33    4         1  choice2     545    105        1         1     545     85
   ..   ..       ...      ...     ...    ...      ...       ...     ...    ...
   306  27         9  choice1    3920    140        1         1    3920    125
   319  28         8  choice2    2450    133        1         1    2450    108
   325  28        14  choice2    2450    123        0         1    2450    108
  328  28        17  choice2    2815    108        0         1    2450    108
  330  29         2  choice2    2800    140        2         0    2800    120

       change2  comfort2
  13         0         1
  18         0         1
  27         0         1
  28         0         1
  33         1         1
  ..       ...       ...
  306        0         2
  319        0         2
  325        0         2
  328        0         2
  330        0         1

  [42 rows x 11 columns])

So our check failed, apparently people aren't rational...
Engarde has printed the name of the failed assertion and the rows that are False.
We're simply resusing pandas printing machinery, so set ``pd.options.display.max_rows`` to display
more or fewer rows.

We'll fix this problem by ignoring those people (why change your mind when you can change the data?).

.. code-block:: python

   In [16]: @ed.verify_all(rational)
      ....: def drop_silly_people(df):
      ....:     r = ((df.price1 < df.price2) | (df.time1 < df.time2) |
      ....:          (df.change1 < df.change2) | (df.comfort1 > df.comfort2))
      ....:     return df[r]
      ....:

   In [17]: @ed.is_shape((None, 11))
      ....: @ed.has_dtypes(items=dtypes)
      ....: def unload():
      ....:     trains = pd.read_csv("data/trains.csv", index_col=0)
      ....:     return trains

   In [18]: df = unload().pipe(drop_silly_people)

   In [19]: df.head()
   Out[19]:
      id  choiceid   choice  price1  time1  change1  comfort1  price2  time2  \
   1   1         1  choice1    2400    150        0         1    4000    150
   2   1         2  choice1    2400    150        0         1    3200    130
   3   1         3  choice1    2400    115        0         1    4000    115
   4   1         4  choice2    4000    130        0         1    3200    150
   5   1         5  choice2    2400    150        0         1    3200    150

      change2  comfort2
   1        0         1
   2        0         1
   3        0         0
   4        0         0
   5        0         0
