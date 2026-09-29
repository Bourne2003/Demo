"""Unit formatting and parsing helpers."""

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
