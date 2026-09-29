"""Text helpers."""

import re
import unicodedata


def slugify(value: str, separator: str = "-") -> str:
    """Convert text to a lowercase URL-friendly slug.

    >>> slugify("Hello, World!")
    'hello-world'
    """
    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    words = re.findall(r"[a-z0-9]+", ascii_text.lower())
    return separator.join(words)


def word_count(value: str) -> int:
    """Count whitespace-separated words.

    >>> word_count("one two  three")
    3
    """
    return len(value.split())


def truncate(value: str, length: int, suffix: str = "...") -> str:
    """Shorten text to at most ``length`` characters, including ``suffix``.

    >>> truncate("Hello, World!", 8)
    'Hello...'
    """
    if length < 0:
        raise ValueError("length must be non-negative")
    if len(value) <= length:
        return value
    if length <= len(suffix):
        return suffix[:length]
    return value[: length - len(suffix)] + suffix
