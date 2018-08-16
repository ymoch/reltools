"""Relation tools for Python."""

from itertools import dropwhile
from operator import itemgetter
from typing import Callable, Generic, Iterable, Iterator, Tuple, TypeVar

from more_itertools import peekable

__version__ = '0.0.0'
__author__ = 'Yu Mochizuki'
__author_email__ = 'ymoch.dev@gmail.com'


T = TypeVar('T')
U = TypeVar('U')


def partition(
        predicate: Callable[[T], bool],
        iterable: Iterable[T],
) -> Tuple[Iterator[T], Iterator[T]]:
    items = peekable(iterable)

    def head() -> Iterator[T]:
        for item in items:
            if not predicate(item):
                items.prepend(item)
                break
            yield item

    head = list(head())
    remaining = list(dropwhile(predicate, items))
    return head, remaining


def relate_one_to_many(
        lhs: Iterable[T],
        rhs: Iterable[U],
) -> Iterator[Tuple[T, Iterator[U]]]:
    """
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

    rhs = iter(rhs)
    for lhs_curr in lhs:
        lhs_key_curr = lhs_key(lhs_curr)
        rhs = dropwhile(lambda item: rhs_key(item) < lhs_key_curr, rhs)
        rhs_curr, rhs = partition(
                lambda item: rhs_key(item) == lhs_key_curr, rhs)
        yield (lhs_curr, rhs_curr)
