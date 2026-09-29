from demo_utils.text import slugify


def test_slugify_basic():
    assert slugify("Hello, World!") == "hello-world"


def test_slugify_accents_and_spaces():
    assert slugify("  Café   au  lait ") == "cafe-au-lait"


def test_slugify_custom_separator():
    assert slugify("Demo Utils 2026", separator="_") == "demo_utils_2026"


def test_slugify_empty():
    assert slugify("!!!") == ""
