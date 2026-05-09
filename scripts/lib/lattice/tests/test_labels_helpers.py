"""Tests for lattice-aware label helpers — label_pattern, format_label,
extract_label_digits.
"""

from __future__ import annotations

from lib.lattice.labels import (
    extract_label_digits,
    format_label,
    label_pattern,
)


def test_label_pattern_with_explicit_prefix() -> None:
    p = label_pattern("ASN")
    assert p.search("ASN-0034").group(1) == "0034"
    assert p.search("MAT-0001") is None


def test_label_pattern_different_prefix() -> None:
    p = label_pattern("MAT")
    assert p.search("MAT-0001").group(1) == "0001"
    assert p.search("ASN-0034") is None


def test_label_pattern_caches_compiled() -> None:
    a = label_pattern("ASN")
    b = label_pattern("ASN")
    assert a is b


def test_format_label_default_width() -> None:
    assert format_label(34, "ASN") == "ASN-0034"


def test_format_label_custom_width() -> None:
    assert format_label(34, "ASN", width=6) == "ASN-000034"


def test_format_label_different_prefix() -> None:
    assert format_label(1, "MAT") == "MAT-0001"


def test_extract_label_digits_returns_match() -> None:
    assert extract_label_digits("path/ASN-0034/T0.md", "ASN") == "0034"


def test_extract_label_digits_no_match_returns_none() -> None:
    assert extract_label_digits("path/T0.md", "ASN") is None


def test_extract_label_digits_wrong_prefix() -> None:
    assert extract_label_digits("path/ASN-0034/T0.md", "MAT") is None


def test_helpers_default_to_active_lattice_prefix() -> None:
    """Without explicit prefix, helpers read from lattice_config()."""
    # The active lattice (xanadu) is configured with label_prefix=ASN.
    assert format_label(34) == "ASN-0034"
    assert extract_label_digits("ASN-0034") == "0034"
    assert label_pattern().search("ASN-0034").group(1) == "0034"
