import pytest

from demo_utils.text import (
    camel_to_snake,
    char_frequency,
    is_palindrome,
    levenshtein,
    mask,
    normalize_whitespace,
    similarity,
    slugify,
    snake_to_camel,
    strip_html_tags,
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


@pytest.mark.parametrize(
    "value, expected",
    [
        ("  hello \t\n world  ", "hello world"),
        ("a\u00a0\u00a0b", "a b"),
        ("single", "single"),
        ("   ", ""),
    ],
)
def test_normalize_whitespace(value, expected):
    assert normalize_whitespace(value) == expected


def test_mask_default():
    assert mask("0812345678") == "******5678"


def test_mask_custom_visible_and_char():
    assert mask("secret", visible=2, char="#") == "####et"


def test_mask_short_value_unchanged():
    assert mask("abc") == "abc"


def test_mask_zero_visible():
    assert mask("abc", visible=0) == "***"


def test_mask_negative_visible():
    with pytest.raises(ValueError):
        mask("abc", visible=-1)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        ("kitten", "sitting", 3),
        ("", "abc", 3),
        ("abc", "", 3),
        ("same", "same", 0),
        ("flaw", "lawn", 2),
        ("สวัสดี", "สวสดี", 1),
    ],
)
def test_levenshtein(a, b, expected):
    assert levenshtein(a, b) == expected


def test_levenshtein_is_symmetric():
    assert levenshtein("abcdef", "azced") == levenshtein("azced", "abcdef")


def test_similarity_identical():
    assert similarity("hello", "hello") == 1.0


def test_similarity_completely_different():
    assert similarity("abc", "xyz") == 0.0


def test_similarity_partial():
    assert similarity("kitten", "sitting") == pytest.approx(4 / 7)


def test_similarity_empty_strings():
    assert similarity("", "") == 1.0


def test_char_frequency_top():
    assert char_frequency("Hello", top=2) == [("l", 2), ("h", 1)]


def test_char_frequency_all_ignores_spaces():
    assert char_frequency("a b a") == [("a", 2), ("b", 1)]


def test_char_frequency_case_sensitive():
    assert char_frequency("Aa", ignore_case=False) == [("A", 1), ("a", 1)]


def test_char_frequency_keep_spaces():
    assert char_frequency("a  a", ignore_space=False) == [("a", 2), (" ", 2)]


def test_char_frequency_empty():
    assert char_frequency("") == []


@pytest.mark.parametrize(
    "value, expected",
    [
        ("<p>Fish &amp; <b>chips</b></p>", "Fish & chips"),
        ("<ul><li>one</li><li>two</li></ul>", "one two"),
        ("<script>alert(1)</script>Hello", "Hello"),
        ("<STYLE type='text/css'>p{}</STYLE>Hi", "Hi"),
        ("no tags", "no tags"),
        ("สวัสดี&nbsp;<br/>ครับ", "สวัสดี ครับ"),
    ],
)
def test_strip_html_tags(value, expected):
    assert strip_html_tags(value) == expected
