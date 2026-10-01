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

More helpers:

```python
from demo_utils.text import normalize_whitespace, mask, levenshtein, similarity
from demo_utils.text import char_frequency, strip_html_tags
from demo_utils.thai import baht_text, contains_thai, thai_ratio, remove_thai_tone_marks
from demo_utils.thai import parse_thai_date, is_valid_thai_mobile, format_thai_mobile
from demo_utils.thai import extract_numbers
from demo_utils.collections import partition, sliding_window, first, deep_merge
from demo_utils.units import format_duration, format_number
from demo_utils.units import celsius_to_fahrenheit, fahrenheit_to_celsius

baht_text(121.5)                    # 'หนึ่งร้อยยี่สิบเอ็ดบาทห้าสิบสตางค์'
contains_thai("hello สวัสดี")        # True
thai_ratio("ab กข")                 # 0.5
remove_thai_tone_marks("ก่อน")       # 'กอน'
format_thai_date(datetime.date(2026, 9, 29), weekday=True)
# 'วันอังคารที่ 29 กันยายน 2569'
parse_thai_date("29 ก.ย. 2569")      # datetime.date(2026, 9, 29)
is_valid_thai_mobile("+66 81 234 5678")  # True
format_thai_mobile("0812345678")    # '081-234-5678'
extract_numbers("ราคา ๑,๒๕๐ บาท")    # [1250.0]
normalize_whitespace(" a \n b ")     # 'a b'
mask("0812345678")                  # '******5678'
levenshtein("kitten", "sitting")    # 3
similarity("kitten", "sitting")     # 0.571...
char_frequency("Hello", top=2)      # [('l', 2), ('h', 1)]
strip_html_tags("<p>Fish &amp; <b>chips</b></p>")  # 'Fish & chips'
partition(range(6), lambda n: n % 2 == 0)  # ([0, 2, 4], [1, 3, 5])
list(sliding_window([1, 2, 3, 4], 2))      # [(1, 2), (2, 3), (3, 4)]
first([1, 4, 6], lambda n: n % 2 == 0)     # 4
deep_merge({"db": {"host": "a", "port": 1}}, {"db": {"port": 2}})
# {'db': {'host': 'a', 'port': 2}}
format_duration(5400)               # '1h30m'
format_number(1234567.891, 2)       # '1,234,567.89'
celsius_to_fahrenheit(100)          # 212.0
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
python -m demo_utils baht 1,250.50             # หนึ่งพันสองร้อยห้าสิบบาทห้าสิบสตางค์
python -m demo_utils mobile "+66 81 234 5678"  # 081-234-5678
python -m demo_utils thai-date "29 ก.ย. 2569"  # 2026-09-29
python -m demo_utils no-tones ก่อน              # กอน
python -m demo_utils duration 5400             # 1h30m
python -m demo_utils squeeze "a    b"          # a b
python -m demo_utils strip-html "<b>hi</b>"    # hi
```

## Contributing

1. Create a branch from `main`
2. Commit your changes and add tests under `tests/`
3. Run `python -m pytest`
4. Open a pull request into `main`

Formatting rules live in `.editorconfig`.
