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


_THAI_NUMBERS = ["ศูนย์", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
_THAI_PLACES = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน"]


def _read_below_million(number: int) -> str:
    digits = str(number)
    words = []
    for index, char in enumerate(digits):
        digit = int(char)
        place = len(digits) - index - 1
        if digit == 0:
            continue
        if place == 1 and digit == 1:
            words.append("สิบ")
        elif place == 1 and digit == 2:
            words.append("ยี่สิบ")
        elif place == 0 and digit == 1 and len(digits) > 1:
            words.append("เอ็ด")
        else:
            words.append(_THAI_NUMBERS[digit] + _THAI_PLACES[place])
    return "".join(words)


def number_to_thai_words(number: int) -> str:
    """Read a whole number aloud in Thai.

    >>> number_to_thai_words(121)
    'หนึ่งร้อยยี่สิบเอ็ด'
    """
    if number < 0:
        return "ลบ" + number_to_thai_words(-number)
    if number == 0:
        return _THAI_NUMBERS[0]
    millions, rest = divmod(number, 1_000_000)
    words = ""
    if millions:
        words = number_to_thai_words(millions) + "ล้าน"
    if rest:
        words += _read_below_million(rest)
    return words
