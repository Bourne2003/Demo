import pytest

from demo_utils.units import (
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    format_bytes,
    format_duration,
    format_number,
    parse_bytes,
    parse_duration,
)


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


@pytest.mark.parametrize(
    "seconds, expected",
    [(0, "0s"), (45, "45s"), (5400, "1h30m"), (86400, "1d"), (93784, "1d2h3m4s")],
)
def test_format_duration(seconds, expected):
    assert format_duration(seconds) == expected


@pytest.mark.parametrize("seconds", [1, 59, 61, 3600, 90061, 10**6])
def test_format_duration_round_trips_parse_duration(seconds):
    assert parse_duration(format_duration(seconds)) == seconds


def test_format_duration_negative():
    with pytest.raises(ValueError):
        format_duration(-1)


@pytest.mark.parametrize(
    "celsius, fahrenheit", [(0, 32), (100, 212), (-40, -40), (37, 98.6)]
)
def test_temperature_conversions(celsius, fahrenheit):
    assert celsius_to_fahrenheit(celsius) == pytest.approx(fahrenheit)
    assert fahrenheit_to_celsius(fahrenheit) == pytest.approx(celsius)


@pytest.mark.parametrize(
    "value, decimals, expected",
    [
        (0, 0, "0"),
        (999, 0, "999"),
        (1000, 0, "1,000"),
        (1234567.891, 2, "1,234,567.89"),
        (-9876543, 0, "-9,876,543"),
        (0.5, 1, "0.5"),
    ],
)
def test_format_number(value, decimals, expected):
    assert format_number(value, decimals) == expected


def test_format_number_custom_separator():
    assert format_number(1234567, separator=" ") == "1 234 567"


def test_format_number_negative_decimals():
    with pytest.raises(ValueError):
        format_number(1, -1)
