import pytest

from demo_utils.thai import (
    be_to_ce,
    ce_to_be,
    from_thai_digits,
    number_to_thai_words,
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
