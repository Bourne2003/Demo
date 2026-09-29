# Demo

Demo repository by [Bourne2003](https://github.com/Bourne2003): `demo_utils`, a small collection of text and data utilities.

## Getting started

```bash
git clone https://github.com/Bourne2003/Demo.git
cd Demo
pip install -e ".[test]"
python -m pytest
```

## Usage

### Python

```python
from demo_utils.text import slugify, word_count, truncate, is_palindrome
from demo_utils.thai import to_thai_digits, from_thai_digits
from demo_utils.collections import chunk, flatten
from demo_utils.units import format_bytes, parse_duration

slugify("Hello, World!")            # 'hello-world'
word_count("one two three")         # 3
truncate("Hello, World!", 8)        # 'Hello...'
is_palindrome("racecar")            # True
to_thai_digits("2026")              # '๒๐๒๖'
from_thai_digits("๒๕๖๙")            # '2569'
list(chunk([1, 2, 3, 4, 5], 2))     # [[1, 2], [3, 4], [5]]
list(flatten([1, [2, (3, [4])]]))   # [1, 2, 3, 4]
format_bytes(1536)                  # '1.5 KB'
parse_duration("1h30m")             # 5400
```

### Command line

```bash
python -m demo_utils slugify "Hello, World!"   # hello-world
python -m demo_utils words "one two three"     # 3
python -m demo_utils thai-digits 2026          # ๒๐๒๖
python -m demo_utils arabic-digits ๒๕๖๙        # 2569
python -m demo_utils bytes 1536                # 1.5 KB
python -m demo_utils seconds 1h30m             # 5400
```

## Contributing

1. Create a branch from `main`
2. Commit your changes and add tests under `tests/`
3. Run `python -m pytest`
4. Open a pull request into `main`

Formatting rules live in `.editorconfig`.
