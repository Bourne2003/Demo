"""Thai language helpers."""

import datetime

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


def _read_below_million(number: int, after_higher: bool = False) -> str:
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
        elif place == 0 and digit == 1 and (len(digits) > 1 or after_higher):
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
        words += _read_below_million(rest, after_higher=bool(millions))
    return words


BUDDHIST_ERA_OFFSET = 543


def ce_to_be(year: int) -> int:
    """Convert a Common Era (ค.ศ.) year to a Buddhist Era (พ.ศ.) year.

    >>> ce_to_be(2026)
    2569
    """
    return year + BUDDHIST_ERA_OFFSET


def be_to_ce(year: int) -> int:
    """Convert a Buddhist Era (พ.ศ.) year to a Common Era (ค.ศ.) year.

    >>> be_to_ce(2569)
    2026
    """
    return year - BUDDHIST_ERA_OFFSET


def is_valid_thai_id(value: str) -> bool:
    """Validate a 13-digit Thai national ID number using its check digit.

    Spaces and dashes are ignored, e.g. ``"1-2345-67890-12-1"``.
    """
    digits = value.replace("-", "").replace(" ", "")
    if len(digits) != 13 or not digits.isascii() or not digits.isdigit():
        return False
    total = sum(int(digit) * (13 - index) for index, digit in enumerate(digits[:12]))
    return (11 - total % 11) % 10 == int(digits[12])


THAI_MONTHS = [
    "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
    "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม",
]
THAI_MONTHS_SHORT = [
    "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
    "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค.",
]


THAI_WEEKDAYS = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]


def format_thai_date(
    value: datetime.date,
    short: bool = False,
    thai_digits: bool = False,
    weekday: bool = False,
) -> str:
    """Format a date in Thai with a Buddhist Era year.

    >>> format_thai_date(datetime.date(2026, 9, 29))
    '29 กันยายน 2569'
    >>> format_thai_date(datetime.date(2026, 9, 29), weekday=True)
    'วันอังคารที่ 29 กันยายน 2569'
    """
    months = THAI_MONTHS_SHORT if short else THAI_MONTHS
    text = f"{value.day} {months[value.month - 1]} {ce_to_be(value.year)}"
    if weekday:
        text = f"วัน{THAI_WEEKDAYS[value.weekday()]}ที่ {text}"
    return to_thai_digits(text) if thai_digits else text


def baht_text(amount: float) -> str:
    """Read an amount of money in Thai baht and satang.

    >>> baht_text(121.5)
    'หนึ่งร้อยยี่สิบเอ็ดบาทห้าสิบสตางค์'
    """
    satang_total = round(abs(amount) * 100)
    baht, satang = divmod(satang_total, 100)
    prefix = "ลบ" if amount < 0 and satang_total else ""
    if satang == 0:
        return f"{prefix}{number_to_thai_words(baht)}บาทถ้วน"
    satang_words = number_to_thai_words(satang) + "สตางค์"
    if baht == 0:
        return prefix + satang_words
    return f"{prefix}{number_to_thai_words(baht)}บาท{satang_words}"


def _is_thai_char(char: str) -> bool:
    return "฀" <= char <= "๿"


def contains_thai(value: str) -> bool:
    """Return ``True`` if the text contains any Thai character.

    >>> contains_thai("hello สวัสดี")
    True
    """
    return any(_is_thai_char(char) for char in value)


def thai_ratio(value: str) -> float:
    """Return the share of letters in the text that are Thai (0.0 to 1.0).

    Spaces, digits and punctuation are ignored.
    """
    letters = [char for char in value if char.isalpha() or _is_thai_char(char)]
    if not letters:
        return 0.0
    return sum(_is_thai_char(char) for char in letters) / len(letters)


_THAI_TONE_MARKS = "่้๊๋"  # ่ ้ ๊ ๋


def remove_thai_tone_marks(value: str) -> str:
    """Remove Thai tone marks (ไม้เอก, ไม้โท, ไม้ตรี, ไม้จัตวา).

    Useful for loose matching of Thai text typed without tone marks.

    >>> remove_thai_tone_marks("ก่อน")
    'กอน'
    """
    return value.translate({ord(mark): None for mark in _THAI_TONE_MARKS})
