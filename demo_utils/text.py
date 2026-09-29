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
