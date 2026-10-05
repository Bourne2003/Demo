# Changelog

## Unreleased

### Fixed
- `units.parse_duration` now rejects inputs that repeat a time unit instead of silently adding them.

## 0.4.0 - 2026-10-01

### Added
- `thai`: `baht_text`, `contains_thai`, `thai_ratio`, `remove_thai_tone_marks`, `parse_thai_date`, `is_valid_thai_mobile`, `format_thai_mobile`, `extract_numbers`
- `thai`: `weekday=True` option for `format_thai_date`
- `text`: `normalize_whitespace`, `mask`, `levenshtein`, `similarity`, `char_frequency`, `strip_html_tags`
- `collections`: `partition`, `sliding_window`, `first`, `deep_merge`
- `units`: `format_duration`, `format_number`, `celsius_to_fahrenheit`, `fahrenheit_to_celsius`
- CLI commands: `baht`, `mobile`, `thai-date`, `no-tones`, `duration`, `squeeze`, `strip-html`

## 0.3.0 - 2026-09-30

### Added
- `thai`: `number_to_thai_words`, `ce_to_be`, `be_to_ce`, `is_valid_thai_id`, `format_thai_date`
- `text`: `camel_to_snake`, `snake_to_camel`
- `collections`: `unique`, `group_by`
- `units`: `parse_bytes`
- CLI commands: `size`, `snake`, `camel`, `thai-words`, `thai-id`

## 0.2.0 - 2026-09-29

### Added
- `text`: `slugify`, `word_count`, `truncate`, `is_palindrome`
- `thai`: `to_thai_digits`, `from_thai_digits`
- `collections`: `chunk`, `flatten`
- `units`: `format_bytes`, `parse_duration`
- Command-line interface: `python -m demo_utils <command> <text>`
- Usage documentation in the README

## 0.1.0 - 2026-09-29

### Added
- Package scaffold with pytest
