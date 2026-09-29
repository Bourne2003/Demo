"""Command-line interface: ``python -m demo_utils <command> <text>``."""

import argparse
import sys
from typing import List, Optional

from demo_utils import __version__
from demo_utils.text import slugify, word_count
from demo_utils.thai import from_thai_digits, to_thai_digits
from demo_utils.units import format_bytes, parse_duration

COMMANDS = {
    "slugify": slugify,
    "words": word_count,
    "thai-digits": to_thai_digits,
    "arabic-digits": from_thai_digits,
    "bytes": lambda value: format_bytes(int(value)),
    "seconds": parse_duration,
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
