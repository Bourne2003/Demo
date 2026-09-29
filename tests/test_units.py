import pytest

from demo_utils.units import format_bytes, parse_bytes, parse_duration


@pytest.mark.parametrize(
    "size, expected",
    [
        (0, "0 B"),
        (1023, "1023 B"),
        (1024, "1.0 KB"),
        (1536, "1.5 KB"),
        (5 * 1024**2, "5.0 MB"),
        (3 * 1024**4, "3.0 TB"),
        (2048 * 1024**5, "2048.0 PB"),
    ],
)
def test_format_bytes(size, expected):
    assert format_bytes(size) == expected


def test_format_bytes_precision():
    assert format_bytes(1234567, precision=2) == "1.18 MB"


def test_format_bytes_negative():
    with pytest.raises(ValueError):
        format_bytes(-1)


@pytest.mark.parametrize(
    "value, expected",
    [
        ("45s", 45),
        ("1h30m", 5400),
        ("2d", 172800),
        ("1D 2H 3M 4S", 93784),
    ],
)
def test_parse_duration(value, expected):
    assert parse_duration(value) == expected


@pytest.mark.parametrize("value", ["", "10", "5x", "1h-2m", "h"])
def test_parse_duration_invalid(value):
    with pytest.raises(ValueError):
        parse_duration(value)


@pytest.mark.parametrize(
    "value, expected",
    [
        ("0", 0),
        ("512 B", 512),
        ("1.5 KB", 1536),
        ("1.5kb", 1536),
        ("2 MiB", 2 * 1024**2),
        ("3G", 3 * 1024**3),
        ("1 TB", 1024**4),
    ],
)
def test_parse_bytes(value, expected):
    assert parse_bytes(value) == expected


@pytest.mark.parametrize("size", [0, 1023, 1536, 5 * 1024**2, 3 * 1024**4])
def test_parse_bytes_round_trips_format_bytes(size):
    assert parse_bytes(format_bytes(size)) == size


@pytest.mark.parametrize("value", ["", "KB", "-1 KB", "1.5 XB", "ten MB"])
def test_parse_bytes_invalid(value):
    with pytest.raises(ValueError):
        parse_bytes(value)
