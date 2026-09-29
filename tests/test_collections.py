import pytest

from demo_utils.collections import chunk


def test_chunk_uneven():
    assert list(chunk([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]


def test_chunk_even():
    assert list(chunk("abcdef", 3)) == [["a", "b", "c"], ["d", "e", "f"]]


def test_chunk_generator_input():
    assert list(chunk((n for n in range(3)), 5)) == [[0, 1, 2]]


def test_chunk_empty():
    assert list(chunk([], 3)) == []


def test_chunk_invalid_size():
    with pytest.raises(ValueError):
        list(chunk([1], 0))
