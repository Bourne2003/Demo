"""Unit formatting and parsing helpers."""

import re

_BYTE_UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]


def format_bytes(size: int, precision: int = 1) -> str:
    """Format a byte count using binary (1024-based) units.

    >>> format_bytes(1536)
    '1.5 KB'
    """
    if size < 0:
        raise ValueError("size must be non-negative")
    value = float(size)
    for unit in _BYTE_UNITS:
        if value < 1024 or unit == _BYTE_UNITS[-1]:
            if unit == "B":
                return f"{int(value)} B"
            return f"{value:.{precision}f} {unit}"
        value /= 1024
    raise AssertionError("unreachable")


_DURATION_UNITS = {"d": 86400, "h": 3600, "m": 60, "s": 1}
_DURATION_PART = re.compile(r"(\d+)([dhms])")


def parse_duration(value: str) -> int:
    """Parse a duration such as ``"1h30m"`` into seconds.

    Supported units: ``d``, ``h``, ``m``, ``s``.

    >>> parse_duration("1h30m")
    5400
    """
    text = value.replace(" ", "").lower()
    if not text or _DURATION_PART.sub("", text):
        raise ValueError(f"invalid duration: {value!r}")
    return sum(
        int(amount) * _DURATION_UNITS[unit]
        for amount, unit in _DURATION_PART.findall(text)
    )
