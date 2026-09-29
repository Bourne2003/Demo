import pytest

from demo_utils.collections import chunk, flatten, unique


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


def test_flatten_nested():
    assert list(flatten([1, [2, (3, [4])], 5])) == [1, 2, 3, 4, 5]


def test_flatten_keeps_strings_whole():
    assert list(flatten(["ab", ["cd"]])) == ["ab", "cd"]


def test_flatten_empty_lists():
    assert list(flatten([[], [[]], ()])) == []


def test_unique_keeps_first_occurrence_order():
    assert list(unique([3, 1, 3, 2, 1])) == [3, 1, 2]


def test_unique_with_key():
    assert list(unique(["Apple", "apple", "Banana"], key=str.lower)) == ["Apple", "Banana"]


def test_unique_empty():
    assert list(unique([])) == []
