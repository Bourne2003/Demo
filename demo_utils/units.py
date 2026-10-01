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


_BYTES_PATTERN = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*([kmgtp]?)i?b?\s*$", re.IGNORECASE)


def parse_bytes(value: str) -> int:
    """Parse a size such as ``"1.5 KB"`` into bytes (1024-based, like ``format_bytes``).

    >>> parse_bytes("1.5 KB")
    1536
    """
    match = _BYTES_PATTERN.match(value)
    if not match:
        raise ValueError(f"invalid size: {value!r}")
    amount, prefix = match.groups()
    power = "BKMGTP".index(prefix.upper() or "B")
    return int(round(float(amount) * 1024**power))


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


def format_duration(seconds: int) -> str:
    """Format seconds as a compact duration such as ``"1h30m"`` (inverse of ``parse_duration``).

    >>> format_duration(5400)
    '1h30m'
    """
    if seconds < 0:
        raise ValueError("seconds must be non-negative")
    if seconds == 0:
        return "0s"
    parts = []
    for unit, size in _DURATION_UNITS.items():
        amount, seconds = divmod(seconds, size)
        if amount:
            parts.append(f"{amount}{unit}")
    return "".join(parts)
