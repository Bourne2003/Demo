"""Thai language helpers."""

_ARABIC = "0123456789"
_THAI = "๐๑๒๓๔๕๖๗๘๙"

_TO_THAI = str.maketrans(_ARABIC, _THAI)
_TO_ARABIC = str.maketrans(_THAI, _ARABIC)


def to_thai_digits(value) -> str:
    """Replace Arabic digits with Thai digits.

    >>> to_thai_digits("2026")
    '๒๐๒๖'
    """
    return str(value).translate(_TO_THAI)


def from_thai_digits(value: str) -> str:
    """Replace Thai digits with Arabic digits.

    >>> from_thai_digits("๒๐๒๖")
    '2026'
    """
    return value.translate(_TO_ARABIC)
