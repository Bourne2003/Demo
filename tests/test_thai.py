from demo_utils.thai import from_thai_digits, to_thai_digits


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
