"""Helpers for lists and other iterables."""

from itertools import islice
from typing import Iterable, Iterator, List, TypeVar

T = TypeVar("T")


def chunk(items: Iterable[T], size: int) -> Iterator[List[T]]:
    """Split ``items`` into lists of at most ``size`` elements.

    >>> list(chunk([1, 2, 3, 4, 5], 2))
    [[1, 2], [3, 4], [5]]
    """
    if size < 1:
        raise ValueError("size must be at least 1")
    iterator = iter(items)
    while True:
        batch = list(islice(iterator, size))
        if not batch:
            return
        yield batch
