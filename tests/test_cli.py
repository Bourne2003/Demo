import subprocess
import sys

import pytest

from demo_utils.cli import main


@pytest.mark.parametrize(
    "argv, expected",
    [
        (["slugify", "Hello", "World!"], "hello-world"),
        (["words", "one two three"], "3"),
        (["thai-digits", "2026"], "๒๐๒๖"),
        (["arabic-digits", "๒๕๖๙"], "2569"),
        (["bytes", "1536"], "1.5 KB"),
        (["seconds", "1h30m"], "5400"),
        (["size", "1.5 KB"], "1536"),
        (["snake", "parseHTTPResponse"], "parse_http_response"),
        (["camel", "parse_http_response"], "parseHttpResponse"),
        (["thai-words", "2569"], "สองพันห้าร้อยหกสิบเก้า"),
        (["thai-id", "1-2345-67890-12-1"], "valid"),
        (["thai-id", "1234567890122"], "invalid"),
    ],
)
def test_commands(argv, expected, capsys):
    assert main(argv) == 0
    assert capsys.readouterr().out.strip() == expected


def test_invalid_input_returns_error(capsys):
    assert main(["seconds", "soon"]) == 1
    assert "invalid duration" in capsys.readouterr().err


def test_non_numeric_thai_words_returns_error(capsys):
    assert main(["thai-words", "many"]) == 1
    assert "error:" in capsys.readouterr().err


def test_unknown_command_exits():
    with pytest.raises(SystemExit):
        main(["nope", "x"])


def test_module_entry_point():
    result = subprocess.run(
        [sys.executable, "-m", "demo_utils", "slugify", "Café Latte"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "cafe-latte"
