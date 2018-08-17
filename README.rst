reltools
========

.. image:: https://travis-ci.org/ymoch/reltools.svg?branch=master
    :target: https://travis-ci.org/ymoch/reltools
.. image:: https://codecov.io/gh/ymoch/reltools/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/ymoch/reltools

Relation tools for Python.
This relates two data (sorted by certain keys) like SQL joining.

Inspired by `itertools.groupby <https://docs.python.org/3.6/library/itertools.html#itertools.groupby>`_,
as long as input data are sorted, almost all processes are evaluated lazily,
which results in the reduction of memory usage.
This feature is for the big data joining without any SQL engines.

Installation
------------

Choose one from the following.

- Install with `pip <https://pypi.org/project/pip/>`_.
    - Run :code:`pip install reltools`.
- Put `reltools.py` into your project.

Samples
-------

First, import `reltools`.

>>> from reltools import relate_one_to_many

Here, input data are sorted in 1st and 2nd keys.

>>> lhs = [
...     (1, 'a', 's'),
...     (2, 'a', 't'),
...     (3, 'b', 'u'),
... ]
>>> rhs = [
...     (1, 'a', 'v'),
...     (1, 'b', 'w'),
...     (3, 'b', 'x'),
... ]

One-To-Many
***********

Here is a sample for *one-to-many* relations.

>>> one_to_many_related = relate_one_to_many(lhs, rhs)
>>> for left, right in one_to_many_related:
...     left, list(right)
((1, 'a', 's'), [(1, 'a', 'v'), (1, 'b', 'w')])
((2, 'a', 't'), [])
((3, 'b', 'u'), [(3, 'b', 'x')])

You can use custom keys for all API functions.

>>> import operator
>>> custom_key = operator.itemgetter(0, 1)
>>> one_to_many_related = relate_one_to_many(
...     lhs, rhs, lhs_key=custom_key, rhs_key=custom_key)
>>> for left, right in one_to_many_related:
...     left, list(right)
((1, 'a', 's'), [(1, 'a', 'v')])
((2, 'a', 't'), [])
((3, 'b', 'u'), [(3, 'b', 'x')])

License
-------

.. image:: https://img.shields.io/badge/License-MIT-brightgreen.svg
    :target: https://opensource.org/licenses/MIT

Copyright (c) 2018 Yu MOCHIZUKI
