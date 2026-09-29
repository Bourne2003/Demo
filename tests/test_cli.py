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
    ],
)
def test_commands(argv, expected, capsys):
    assert main(argv) == 0
    assert capsys.readouterr().out.strip() == expected


def test_invalid_input_returns_error(capsys):
    assert main(["seconds", "soon"]) == 1
    assert "invalid duration" in capsys.readouterr().err


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
