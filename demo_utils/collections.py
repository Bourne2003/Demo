"""Helpers for lists and other iterables."""

from itertools import islice
from typing import Any, Callable, Iterable, Iterator, List, Optional, TypeVar

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


def flatten(items: Iterable[Any]) -> Iterator[Any]:
    """Recursively flatten nested lists and tuples.

    Strings and bytes are treated as single values.

    >>> list(flatten([1, [2, (3, [4])], "ab"]))
    [1, 2, 3, 4, 'ab']
    """
    for item in items:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item


def unique(
    items: Iterable[T], key: Optional[Callable[[T], Any]] = None
) -> Iterator[T]:
    """Yield items in their original order, skipping duplicates.

    ``key`` decides what counts as a duplicate; values it returns must be hashable.

    >>> list(unique([3, 1, 3, 2, 1]))
    [3, 1, 2]
    """
    seen = set()
    for item in items:
        marker = key(item) if key else item
        if marker not in seen:
            seen.add(marker)
            yield item
