from demo_utils.text import slugify, word_count


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
