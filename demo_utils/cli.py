"""Command-line interface: ``python -m demo_utils <command> <text>``."""

import argparse
import sys
from typing import List, Optional

from demo_utils import __version__
from demo_utils.text import (
    camel_to_snake,
    normalize_whitespace,
    slugify,
    snake_to_camel,
    strip_html_tags,
    word_count,
)
from demo_utils.thai import (
    baht_text,
    format_thai_mobile,
    from_thai_digits,
    is_valid_thai_id,
    number_to_thai_words,
    parse_thai_date,
    remove_thai_tone_marks,
    to_thai_digits,
)
from demo_utils.units import format_bytes, format_duration, parse_bytes, parse_duration

COMMANDS = {
    "slugify": slugify,
    "words": word_count,
    "thai-digits": to_thai_digits,
    "arabic-digits": from_thai_digits,
    "bytes": lambda value: format_bytes(int(value)),
    "seconds": parse_duration,
    "size": parse_bytes,
    "snake": camel_to_snake,
    "camel": snake_to_camel,
    "thai-words": lambda value: number_to_thai_words(int(value)),
    "thai-id": lambda value: "valid" if is_valid_thai_id(value) else "invalid",
    "baht": lambda value: baht_text(float(value.replace(",", ""))),
    "mobile": format_thai_mobile,
    "thai-date": lambda value: parse_thai_date(value).isoformat(),
    "no-tones": remove_thai_tone_marks,
    "duration": lambda value: format_duration(int(value)),
    "squeeze": normalize_whitespace,
    "strip-html": strip_html_tags,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="demo_utils", description=__doc__)
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("command", choices=sorted(COMMANDS))
    parser.add_argument("text", nargs="+", help="input (joined with spaces)")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = COMMANDS[args.command](" ".join(args.text))
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(result)
    return 0
