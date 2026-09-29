import pytest

from demo_utils.text import (
    camel_to_snake,
    is_palindrome,
    slugify,
    snake_to_camel,
    truncate,
    word_count,
)


def test_slugify_basic():
    assert slugify("Hello, World!") == "hello-world"


def test_slugify_accents_and_spaces():
    assert slugify("  Café   au  lait ") == "cafe-au-lait"


def test_slugify_custom_separator():
    assert slugify("Demo Utils 2026", separator="_") == "demo_utils_2026"


def test_slugify_empty():
    assert slugify("!!!") == ""


def test_word_count():
    assert word_count("one two  three") == 3


def test_word_count_newlines_and_tabs():
    assert word_count("a\nb\tc ") == 3


def test_word_count_empty():
    assert word_count("   ") == 0


def test_truncate_short_text_unchanged():
    assert truncate("Hi", 8) == "Hi"


def test_truncate_adds_suffix():
    assert truncate("Hello, World!", 8) == "Hello..."


def test_truncate_custom_suffix():
    assert truncate("Hello, World!", 6, suffix="…") == "Hello…"


def test_truncate_length_shorter_than_suffix():
    assert truncate("Hello", 2) == ".."


def test_truncate_negative_length():
    with pytest.raises(ValueError):
        truncate("Hello", -1)


@pytest.mark.parametrize(
    "value", ["A man, a plan, a canal: Panama", "racecar", "12321", "", "ปิป"]
)
def test_is_palindrome_true(value):
    assert is_palindrome(value)


@pytest.mark.parametrize("value", ["hello", "12345", "ab"])
def test_is_palindrome_false(value):
    assert not is_palindrome(value)


@pytest.mark.parametrize(
    "value, expected",
    [
        ("camelCase", "camel_case"),
        ("PascalCase", "pascal_case"),
        ("parseHTTPResponse", "parse_http_response"),
        ("version2Update", "version2_update"),
        ("already_snake", "already_snake"),
    ],
)
def test_camel_to_snake(value, expected):
    assert camel_to_snake(value) == expected


@pytest.mark.parametrize(
    "value, upper_first, expected",
    [
        ("snake_case", False, "snakeCase"),
        ("snake_case", True, "SnakeCase"),
        ("__private_value__", False, "privateValue"),
        ("single", False, "single"),
        ("", False, ""),
    ],
)
def test_snake_to_camel(value, upper_first, expected):
    assert snake_to_camel(value, upper_first=upper_first) == expected
