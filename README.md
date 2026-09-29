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
import datetime

from demo_utils.text import slugify, word_count, truncate, is_palindrome
from demo_utils.text import camel_to_snake, snake_to_camel
from demo_utils.thai import to_thai_digits, from_thai_digits
from demo_utils.thai import number_to_thai_words, ce_to_be, be_to_ce
from demo_utils.thai import is_valid_thai_id, format_thai_date
from demo_utils.collections import chunk, flatten, unique, group_by
from demo_utils.units import format_bytes, parse_bytes, parse_duration

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
camel_to_snake("parseHTTPResponse") # 'parse_http_response'
snake_to_camel("parse_http_response")  # 'parseHttpResponse'
number_to_thai_words(121)           # 'หนึ่งร้อยยี่สิบเอ็ด'
ce_to_be(2026)                      # 2569
be_to_ce(2569)                      # 2026
is_valid_thai_id("1-2345-67890-12-1")  # True
format_thai_date(datetime.date(2026, 9, 29))  # '29 กันยายน 2569'
list(unique([3, 1, 3, 2, 1]))       # [3, 1, 2]
group_by(["apple", "avocado", "banana"], key=lambda w: w[0])
# {'a': ['apple', 'avocado'], 'b': ['banana']}
parse_bytes("1.5 KB")               # 1536
```

### Command line

```bash
python -m demo_utils slugify "Hello, World!"   # hello-world
python -m demo_utils words "one two three"     # 3
python -m demo_utils thai-digits 2026          # ๒๐๒๖
python -m demo_utils arabic-digits ๒๕๖๙        # 2569
python -m demo_utils bytes 1536                # 1.5 KB
python -m demo_utils seconds 1h30m             # 5400
python -m demo_utils size "1.5 KB"             # 1536
python -m demo_utils snake parseHTTPResponse   # parse_http_response
python -m demo_utils camel parse_http_response # parseHttpResponse
python -m demo_utils thai-words 2569           # สองพันห้าร้อยหกสิบเก้า
python -m demo_utils thai-id 1-2345-67890-12-1 # valid
```

## Contributing

1. Create a branch from `main`
2. Commit your changes and add tests under `tests/`
3. Run `python -m pytest`
4. Open a pull request into `main`

Formatting rules live in `.editorconfig`.
