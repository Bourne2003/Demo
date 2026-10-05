import pytest

from demo_utils.collections import (
    chunk,
    deep_merge,
    first,
    flatten,
    group_by,
    partition,
    sliding_window,
    unique,
)


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


def test_group_by_first_letter():
    assert group_by(["apple", "banana", "avocado"], key=lambda word: word[0]) == {
        "a": ["apple", "avocado"],
        "b": ["banana"],
    }


def test_group_by_keeps_key_order():
    assert list(group_by([3, 1, 4, 2], key=lambda n: n % 2)) == [1, 0]


def test_group_by_empty():
    assert group_by([], key=len) == {}


def test_partition_even_odd():
    assert partition(range(6), lambda n: n % 2 == 0) == ([0, 2, 4], [1, 3, 5])


def test_partition_all_match():
    assert partition("abc", str.isalpha) == (["a", "b", "c"], [])


def test_partition_empty():
    assert partition([], bool) == ([], [])


def test_sliding_window_pairs():
    assert list(sliding_window([1, 2, 3, 4], 2)) == [(1, 2), (2, 3), (3, 4)]


def test_sliding_window_size_equals_length():
    assert list(sliding_window("abc", 3)) == [("a", "b", "c")]


def test_sliding_window_too_short():
    assert list(sliding_window([1, 2], 3)) == []


def test_sliding_window_generator_input():
    assert list(sliding_window((n for n in range(4)), 3)) == [(0, 1, 2), (1, 2, 3)]


def test_sliding_window_invalid_size():
    with pytest.raises(ValueError):
        list(sliding_window([1], 0))


def test_first_without_predicate():
    assert first([3, 4]) == 3


def test_first_with_predicate():
    assert first([1, 4, 6], lambda n: n % 2 == 0) == 4


def test_first_default_when_empty():
    assert first([], default="none") == "none"


def test_first_default_when_no_match():
    assert first([1, 3], lambda n: n > 5, default=0) == 0


def test_first_stops_early():
    def numbers():
        yield 1
        raise AssertionError("should not be consumed")

    assert first(numbers()) == 1


def test_deep_merge_nested():
    base = {"db": {"host": "a", "port": 1}, "debug": False}
    override = {"db": {"port": 2}, "debug": True}
    assert deep_merge(base, override) == {"db": {"host": "a", "port": 2}, "debug": True}


def test_deep_merge_replaces_non_dict_values():
    assert deep_merge({"a": {"b": 1}}, {"a": [1, 2]}) == {"a": [1, 2]}


def test_deep_merge_adds_new_keys():
    assert deep_merge({"a": 1}, {"b": {"c": 2}}) == {"a": 1, "b": {"c": 2}}


def test_deep_merge_does_not_modify_inputs():
    base = {"a": {"b": 1}}
    override = {"a": {"c": 2}}
    deep_merge(base, override)
    assert base == {"a": {"b": 1}}
    assert override == {"a": {"c": 2}}


def test_deep_merge_does_not_share_nested_values():
    base = {"settings": {"tags": ["stable"]}}
    result = deep_merge(base, {})

    result["settings"]["tags"].append("new")

    assert base == {"settings": {"tags": ["stable"]}}
