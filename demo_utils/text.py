"""Text helpers."""

import re
import unicodedata
from collections import Counter
from typing import List, Tuple


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


def is_palindrome(value: str) -> bool:
    """Check whether text reads the same backwards, ignoring case and punctuation.

    >>> is_palindrome("A man, a plan, a canal: Panama")
    True
    """
    letters = [char.casefold() for char in value if char.isalnum()]
    return letters == letters[::-1]


def camel_to_snake(value: str) -> str:
    """Convert ``camelCase`` or ``PascalCase`` to ``snake_case``.

    >>> camel_to_snake("parseHTTPResponse")
    'parse_http_response'
    """
    value = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", value)
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    return value.lower()


def snake_to_camel(value: str, upper_first: bool = False) -> str:
    """Convert ``snake_case`` to ``camelCase`` (or ``PascalCase``).

    >>> snake_to_camel("parse_http_response")
    'parseHttpResponse'
    """
    words = [word for word in value.split("_") if word]
    if not words:
        return ""
    head = words[0].capitalize() if upper_first else words[0].lower()
    return head + "".join(word.capitalize() for word in words[1:])


def normalize_whitespace(value: str) -> str:
    """Collapse runs of whitespace (including tabs, newlines and NBSP) to one space.

    >>> normalize_whitespace("  hello \\t\\n world  ")
    'hello world'
    """
    return " ".join(value.split())


def mask(value: str, visible: int = 4, char: str = "*") -> str:
    """Hide all but the last ``visible`` characters, e.g. for card or phone numbers.

    >>> mask("0812345678")
    '******5678'
    """
    if visible < 0:
        raise ValueError("visible must be non-negative")
    hidden = max(len(value) - visible, 0)
    return char * hidden + value[hidden:]


def levenshtein(a: str, b: str) -> int:
    """Return the edit distance (insertions, deletions, substitutions) between two strings.

    >>> levenshtein("kitten", "sitting")
    3
    """
    if len(a) < len(b):
        a, b = b, a
    previous = list(range(len(b) + 1))
    for i, char_a in enumerate(a, start=1):
        current = [i]
        for j, char_b in enumerate(b, start=1):
            current.append(
                min(
                    previous[j] + 1,
                    current[j - 1] + 1,
                    previous[j - 1] + (char_a != char_b),
                )
            )
        previous = current
    return previous[-1]


def similarity(a: str, b: str) -> float:
    """Return a similarity score from 0.0 (different) to 1.0 (identical).

    Based on ``levenshtein`` normalized by the longer string's length.

    >>> similarity("kitten", "sitting")
    0.5714285714285714
    """
    longest = max(len(a), len(b))
    if longest == 0:
        return 1.0
    return 1 - levenshtein(a, b) / longest


def char_frequency(
    value: str, top: int = 0, ignore_case: bool = True, ignore_space: bool = True
) -> List[Tuple[str, int]]:
    """Count characters, most common first (ties keep first-seen order).

    ``top`` limits the result; 0 returns every character.

    >>> char_frequency("Hello", top=2)
    [('l', 2), ('h', 1)]
    """
    text = value.lower() if ignore_case else value
    if ignore_space:
        text = "".join(char for char in text if not char.isspace())
    counts = Counter(text).most_common()
    return counts[:top] if top else counts
