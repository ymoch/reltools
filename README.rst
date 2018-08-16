reltools
========

.. image:: https://travis-ci.org/ymoch/reltools.svg?branch=master
    :target: https://travis-ci.org/ymoch/reltools
.. image:: https://codecov.io/gh/ymoch/reltools/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/ymoch/reltools

Relation tools for Python.
This relates two data (sorted by certain keys) like SQL joining.

Inspired by [itertools.groupby](https://docs.python.org/3.6/library/itertools.html#itertools.groupby),
as long as input data are sorted, almost all processes are evaluated lazily,
which results in the reduction of memory usage.
This feature is for the big data joining without SQL engine.

Samples
-------

First, import `reltools`.

    >>> from reltools import relate_one_to_many

Here is a sample code for one-to-many relations.

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
    >>> one_to_many_related = relate_one_to_many(lhs, rhs)
    >>> for left, right in one_to_many_related:
    ...     left, list(right)
    ((1, 'a', 's'), [(1, 'a', 'v'), (1, 'b', 'w')])
    ((2, 'a', 't'), [])
    ((3, 'b', 'u'), [(3, 'b', 'x')])
