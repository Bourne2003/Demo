import datetime

import pytest

from demo_utils.thai import (
    baht_text,
    be_to_ce,
    ce_to_be,
    contains_thai,
    format_thai_date,
    from_thai_digits,
    is_valid_thai_id,
    number_to_thai_words,
    remove_thai_tone_marks,
    thai_ratio,
    to_thai_digits,
)


def test_to_thai_digits():
    assert to_thai_digits("2026") == "๒๐๒๖"


def test_to_thai_digits_accepts_numbers():
    assert to_thai_digits(1234567890) == "๑๒๓๔๕๖๗๘๙๐"


def test_to_thai_digits_keeps_other_text():
    assert to_thai_digits("ราคา 99 บาท") == "ราคา ๙๙ บาท"


def test_from_thai_digits():
    assert from_thai_digits("พ.ศ. ๒๕๖๙") == "พ.ศ. 2569"


def test_round_trip():
    assert from_thai_digits(to_thai_digits("0123456789")) == "0123456789"


@pytest.mark.parametrize(
    "number, expected",
    [
        (0, "ศูนย์"),
        (1, "หนึ่ง"),
        (10, "สิบ"),
        (11, "สิบเอ็ด"),
        (20, "ยี่สิบ"),
        (21, "ยี่สิบเอ็ด"),
        (101, "หนึ่งร้อยเอ็ด"),
        (121, "หนึ่งร้อยยี่สิบเอ็ด"),
        (2569, "สองพันห้าร้อยหกสิบเก้า"),
        (1_000_000, "หนึ่งล้าน"),
        (1_000_001, "หนึ่งล้านเอ็ด"),
        (21_000_000, "ยี่สิบเอ็ดล้าน"),
        (-5, "ลบห้า"),
    ],
)
def test_number_to_thai_words(number, expected):
    assert number_to_thai_words(number) == expected


def test_ce_to_be():
    assert ce_to_be(2026) == 2569


def test_be_to_ce():
    assert be_to_ce(2569) == 2026


def test_era_round_trip():
    assert be_to_ce(ce_to_be(1999)) == 1999


@pytest.mark.parametrize("value", ["1234567890121", "1-2345-67890-12-1", "1 2345 67890 12 1"])
def test_is_valid_thai_id_accepts_valid_numbers(value):
    assert is_valid_thai_id(value)


@pytest.mark.parametrize(
    "value",
    [
        "1234567890122",  # wrong check digit
        "123456789012",  # too short
        "12345678901234",  # too long
        "12345678901a1",  # not a digit
        "๑๒๓๔๕๖๗๘๙๐๑๒๑",  # Thai digits are not accepted
        "",
    ],
)
def test_is_valid_thai_id_rejects_invalid_numbers(value):
    assert not is_valid_thai_id(value)


def test_format_thai_date():
    assert format_thai_date(datetime.date(2026, 9, 29)) == "29 กันยายน 2569"


def test_format_thai_date_short():
    assert format_thai_date(datetime.date(2026, 1, 5), short=True) == "5 ม.ค. 2569"


def test_format_thai_date_thai_digits():
    assert (
        format_thai_date(datetime.date(2026, 12, 31), thai_digits=True)
        == "๓๑ ธันวาคม ๒๕๖๙"
    )


def test_format_thai_date_accepts_datetime():
    assert format_thai_date(datetime.datetime(2026, 4, 13, 8, 30)) == "13 เมษายน 2569"


@pytest.mark.parametrize(
    "amount, expected",
    [
        (0, "ศูนย์บาทถ้วน"),
        (1, "หนึ่งบาทถ้วน"),
        (121.5, "หนึ่งร้อยยี่สิบเอ็ดบาทห้าสิบสตางค์"),
        (0.25, "ยี่สิบห้าสตางค์"),
        (1_000_000.01, "หนึ่งล้านบาทหนึ่งสตางค์"),
        (-20, "ลบยี่สิบบาทถ้วน"),
    ],
)
def test_baht_text(amount, expected):
    assert baht_text(amount) == expected


@pytest.mark.parametrize(
    "value, expected",
    [("สวัสดี", True), ("hello สวัสดี", True), ("hello", False), ("๑๒๓", True), ("", False)],
)
def test_contains_thai(value, expected):
    assert contains_thai(value) is expected


def test_thai_ratio_all_thai():
    assert thai_ratio("สวัสดี") == 1.0


def test_thai_ratio_mixed():
    assert thai_ratio("ab กข") == 0.5


def test_thai_ratio_ignores_digits_and_punctuation():
    assert thai_ratio("123 !!!") == 0.0


@pytest.mark.parametrize(
    "value, expected",
    [
        ("ก่อน", "กอน"),
        ("น้ำ", "นำ"),
        ("โต๊ะ", "โตะ"),
        ("จ๋า", "จา"),
        ("hello", "hello"),
    ],
)
def test_remove_thai_tone_marks(value, expected):
    assert remove_thai_tone_marks(value) == expected
