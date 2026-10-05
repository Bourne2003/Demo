"""Helpers for lists and other iterables."""

from copy import deepcopy
from collections import deque
from itertools import islice
from typing import (
    Any,
    Callable,
    Dict,
    Hashable,
    Iterable,
    Iterator,
    List,
    Optional,
    Tuple,
    TypeVar,
)

T = TypeVar("T")
K = TypeVar("K", bound=Hashable)


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


def group_by(items: Iterable[T], key: Callable[[T], K]) -> Dict[K, List[T]]:
    """Group items into lists by ``key``, keeping first-seen key order.

    >>> group_by(["apple", "avocado", "banana"], key=lambda word: word[0])
    {'a': ['apple', 'avocado'], 'b': ['banana']}
    """
    groups: Dict[K, List[T]] = {}
    for item in items:
        groups.setdefault(key(item), []).append(item)
    return groups


def partition(
    items: Iterable[T], predicate: Callable[[T], bool]
) -> Tuple[List[T], List[T]]:
    """Split items into ``(matching, not_matching)`` lists, keeping order.

    >>> partition(range(6), lambda n: n % 2 == 0)
    ([0, 2, 4], [1, 3, 5])
    """
    matching: List[T] = []
    rest: List[T] = []
    for item in items:
        (matching if predicate(item) else rest).append(item)
    return matching, rest


def sliding_window(items: Iterable[T], size: int) -> Iterator[Tuple[T, ...]]:
    """Yield overlapping tuples of ``size`` consecutive items.

    >>> list(sliding_window([1, 2, 3, 4], 2))
    [(1, 2), (2, 3), (3, 4)]
    """
    if size < 1:
        raise ValueError("size must be at least 1")
    iterator = iter(items)
    window = deque(islice(iterator, size), maxlen=size)
    if len(window) < size:
        return
    yield tuple(window)
    for item in iterator:
        window.append(item)
        yield tuple(window)


def first(
    items: Iterable[T],
    predicate: Optional[Callable[[T], bool]] = None,
    default: Any = None,
) -> Any:
    """Return the first item (matching ``predicate`` if given), else ``default``.

    >>> first([1, 4, 6], lambda n: n % 2 == 0)
    4
    """
    for item in items:
        if predicate is None or predicate(item):
            return item
    return default


def deep_merge(base: Dict[Any, Any], override: Dict[Any, Any]) -> Dict[Any, Any]:
    """Recursively merge ``override`` into a copy of ``base``.

    Nested dicts are merged; any other value in ``override`` replaces the one
    in ``base``. Neither input is modified.

    >>> deep_merge({"db": {"host": "a", "port": 1}}, {"db": {"port": 2}})
    {'db': {'host': 'a', 'port': 2}}
    """
    merged = deepcopy(base)
    for key, value in override.items():
        if isinstance(merged.get(key), dict) and isinstance(value, dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged
