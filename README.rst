reltools
========
.. image:: https://circleci.com/gh/ymoch/reltools.svg?style=svg
    :target: https://circleci.com/gh/ymoch/reltools
.. image:: https://codecov.io/gh/ymoch/reltools/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ymoch/reltools
.. image:: https://badge.fury.io/py/reltools.svg
    :target: https://badge.fury.io/py/reltools
.. image:: https://img.shields.io/badge/python-3.6+-blue.svg
    :target: https://www.python.org/
.. image:: https://img.shields.io/lgtm/grade/python/g/ymoch/reltools.svg
    :target: https://lgtm.com/projects/g/ymoch/reltools/context:python

Relation tools for Python.
This relates two data (sorted by certain keys) like SQL joining.

Inspired by `itertools.groupby <https://docs.python.org/3.6/library/itertools.html#itertools.groupby>`_,
as long as input data are sorted, almost all processes are evaluated lazily,
which results in the reduction of memory usage.
This feature is for the big data joining without any SQL engines.

Installation
------------
Install with `pip <https://pypi.org/project/pip/>`_.

.. code-block:: sh

   pip install reltools

Features
--------

One-To-Many
***********
*One-to-many* relationing is provided by ``relate_one_to_many``.

Here, input left-hand-side (``lhs``) and right-hand-side (``rhs``)
are sorted in 1st (and also 2nd) keys.

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

``relate_one_to_many`` relates ``rhs`` items
to each ``lhs`` item using the first items as keys.

>>> from reltools import relate_one_to_many
>>> one_to_many_related = relate_one_to_many(lhs, rhs)
>>> for left, right in one_to_many_related:
...     left, list(right)
((1, 'a', 's'), [(1, 'a', 'v'), (1, 'b', 'w')])
((2, 'a', 't'), [])
((3, 'b', 'u'), [(3, 'b', 'x')])

You can use custom key functions
for not only ``relate_one_to_many`` but also API functions.

>>> import operator
>>> custom_key = operator.itemgetter(0, 1)
>>> one_to_many_related = relate_one_to_many(
...     lhs, rhs, lhs_key=custom_key, rhs_key=custom_key)
>>> for left, right in one_to_many_related:
...     left, list(right)
((1, 'a', 's'), [(1, 'a', 'v')])
((2, 'a', 't'), [])
((3, 'b', 'u'), [(3, 'b', 'x')])

``OneToManyChainer`` helps to relate many ``rhs`` iterables to ``lhs``.

>>> another_rhs = [
...     ('s', 'f'),
...     ('t', 'g'),
...     ('t', 'h'),
... ]
>>> from reltools import OneToManyChainer
>>> chainer = OneToManyChainer(lhs)
>>> chainer.append(rhs)
>>> chainer.append(
...     another_rhs,
...     lhs_key=operator.itemgetter(2),
...     rhs_key=operator.itemgetter(0),
... )
>>> for left, right, another_right in chainer.chain():
...     left, list(right), list(another_right)
((1, 'a', 's'), [(1, 'a', 'v'), (1, 'b', 'w')], [('s', 'f')])
((2, 'a', 't'), [], [('t', 'g'), ('t', 'h')])
((3, 'b', 'u'), [(3, 'b', 'x')], [])

Left Outer Join
***************
Left outer joining is provided by ``left_join``.
While SQL left outer joining returns all the combinations,
this returns the pair of items.
Note that the ``right`` can empty, like SQL left joining.

>>> from reltools import left_join
>>> lhs = [(1, 'a'), (1, 'b'), (2, 'c'), (4, 'd')]
>>> rhs = [(1, 's'), (1, 't'), (3, 'u'), (4, 'v')]
>>> relations = left_join(lhs, rhs)
>>> for left, right in relations:
...     list(left), list(right)
([(1, 'a'), (1, 'b')], [(1, 's'), (1, 't')])
([(2, 'c')], [])
([(4, 'd')], [(4, 'v')])

Right Outer Join
****************
Right outer joining is not supported
because it is left-and-right-opposite of left joining.
Use ``left_join(rhs, lhs, rhs_key, lhs_key)``.

Full Outer Join
***************
Full outer joining, which is an original feature of *reltools*,
is provided by ``outer_join``.
In contrast to ``left_join``, full outer joining preserve keys
that are only in ``rhs``.

>>> from reltools import outer_join
>>> lhs = [(1, 'a'), (1, 'b'), (2, 'c'), (4, 'd')]
>>> rhs = [(1, 's'), (1, 't'), (3, 'u'), (4, 'v')]
>>> relations = outer_join(lhs, rhs)
>>> for left, right in relations:
...     list(left), list(right)
([(1, 'a'), (1, 'b')], [(1, 's'), (1, 't')])
([(2, 'c')], [])
([], [(3, 'u')])
([(4, 'd')], [(4, 'v')])

Inner Join
**********
Inner joining is provided by ``inner_join``.
In contrast to ``left_join``, ``right`` cannot be empty,
like SQL inner joining.

>>> from reltools import inner_join
>>> relations = inner_join(lhs, rhs)
>>> for left, right in relations:
...     list(left), list(right)
([(1, 'a'), (1, 'b')], [(1, 's'), (1, 't')])
([(4, 'd')], [(4, 'v')])

Many-To-Many
************
SQL-like *many-to-many* relationing using an internal table is not supported.
This is because *reltools* supports only sorted data
and does not prefer random accessing.
To achieve *many-to-many* relationing, unnormalize data on preproceing and
use outer joining or inner joining.

Memory Efficiency
*****************
Almost all processes are evaluated lazily,
which results in the reduction of memory usage.
(You can try the efficiency by commands like
``RELTOOLS_TRY_COUNT=10000000 python3 -m doctest README.rst``)

>>> import os
>>> n = int(os.environ.get('RELTOOLS_TRY_COUNT', 1000))
>>> lhs = ((i, 'left') for i in range(n))
>>> rhs = ((i, 'right') for i in range(n))
>>> for left, right in relate_one_to_many(lhs, rhs):
...     assert len(list(right)) == 1

Development
-----------
This project's structure is based on `Poetry <https://poetry.eustace.io/>`_.
All tests are written with `doctest <https://docs.python.jp/3/library/doctest.html>`_
and run with `pytest <https://docs.pytest.org/en/latest/>`_.

.. code-block:: sh

    poetry install
    poetry run pytest

For stability, following checks are also run when testing.

- `pyflakes <https://github.com/PyCQA/pyflakes>`_
- `pycodestyle <https://pycodestyle.readthedocs.io/en/latest/>`_
- `mypy <https://mypy.readthedocs.io/en/stable/index.html>`_

License
-------
.. image:: https://img.shields.io/badge/License-MIT-brightgreen.svg
    :target: https://opensource.org/licenses/MIT

Copyright (c) 2018 Yu MOCHIZUKI
