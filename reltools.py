"""Relation tools for Python."""

from itertools import dropwhile, groupby
from operator import itemgetter
from typing import (
    Callable, Generic, Iterable, Iterator, Optional, Tuple, TypeVar
)

from more_itertools import peekable

__version__ = '0.0.0'
__author__ = 'Yu Mochizuki'
__author_email__ = 'ymoch.dev@gmail.com'


K = TypeVar('K')
T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')


class UnidirectionalFinder(Generic[V, K]):
    """
    This class finds items unidirectionally.

    Note that the key type `K` must be 'comparable'
    (supports `__lt__()` and  `__gt__()`)
    and `iterable` must be sorted by `key`.

    When not given the key, then default key `operator.itemgetter(0)` is used.

    Normal case:

    >>> iterable = [(0, 'a'), (1, 'b'), (1, 'c'), (2, 'd')]
    >>> finder = UnidirectionalFinder(iterable)

    Able to find waiting keys and group by the key.
    >>> list(finder.find(1))
    [(1, 'b'), (1, 'c')]

    Unable to find passed keys.
    >>> list(finder.find(1))
    []
    >>> list(finder.find(0))
    []

    Unable to find too large keys.
    >>> list(finder.find(3))
    []

    Once given a too large key, unable to find existing keys.
    >>> list(finder.find(2))
    []

    Given a custom key, then find and group items by it.
    >>> finder = UnidirectionalFinder(iterable, lambda x: x[0] // 2)
    >>> list(finder.find(0))
    [(0, 'a'), (1, 'b'), (1, 'c')]

    Seminormal case:

    Given an empty collection, then unable to find any items.
    >>> finder = UnidirectionalFinder([])
    >>> list(finder.find(0))
    []
    """
    __EMPTY_LIST = []

    def __init__(
            self, iterable: Iterable[V], key: Optional[Callable[[V], K]]=None):
        """Initialize"""
        self._groups = groupby(iterable, key or itemgetter(0))

    def find(self, key: K) -> Iterator[V]:
        """Find items that have the given key."""
        self.seek_to(key)

        try:
            group = self._groups.peek()
        except StopIteration:
            return iter(self.__EMPTY_LIST)

        group_key, group_items = group
        if group_key > key:
            return iter(self.__EMPTY_LIST)

        return group_items

    def seek_to(self, key: K) -> None:
        """Seek to the given key."""
        seeked_groups = dropwhile(lambda group: group[0] < key, self._groups)
        self._groups = peekable(seeked_groups)


def relate_one_to_many(
        lhs: Iterable[T],
        rhs: Iterable[U],
) -> Iterator[Tuple[T, Iterator[U]]]:
    """
    Relates `rhs` items to each `lhs` items.

    Normal case:
    >>> lhs = [(0, 'a'), (1, 'b'), (2, 'c')]
    >>> rhs = [(1, 's'), (2, 't'), (2, 'u'), (3, 'v')]
    >>> relations = relate_one_to_many(lhs, rhs)
    >>> for relation in relations:
    ...     relation[0], list(relation[1])
    ((0, 'a'), [])
    ((1, 'b'), [(1, 's')])
    ((2, 'c'), [(2, 't'), (2, 'u')])

    Seminormal case:
    >>> lhs = []
    >>> rhs = [(1, 'a')]
    >>> relations = relate_one_to_many(lhs, rhs)
    >>> next(relations)
    Traceback (most recent call last):
        ...
    StopIteration
    """
    lhs_key = itemgetter(0)
    rhs_key = itemgetter(0)

    rhs_finder = UnidirectionalFinder(rhs, rhs_key)
    return ((l, rhs_finder.find(lhs_key(l))) for l in lhs)
