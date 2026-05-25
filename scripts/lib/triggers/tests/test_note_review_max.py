"""Tests for the MAX_REVIEWS env-var cap in note_review's predicate.

Pure-helper tests for `_max_reviews_cap`. The predicate-integration
end is exercised via the live runner (substrate-level), so isolated
unit tests focus on the env-parsing layer where breakage is most
likely (typos, bad config).
"""

from __future__ import annotations

import pytest

from lib.triggers.note_review import _max_reviews_cap


def test_unset_returns_none(monkeypatch):
    monkeypatch.delenv("MAX_REVIEWS", raising=False)
    assert _max_reviews_cap() is None


def test_empty_returns_none(monkeypatch):
    monkeypatch.setenv("MAX_REVIEWS", "")
    assert _max_reviews_cap() is None


def test_whitespace_returns_none(monkeypatch):
    monkeypatch.setenv("MAX_REVIEWS", "   ")
    assert _max_reviews_cap() is None


def test_zero_returns_zero(monkeypatch):
    """MAX_REVIEWS=0 caps at zero (no reviews fire); distinct from unset."""
    monkeypatch.setenv("MAX_REVIEWS", "0")
    assert _max_reviews_cap() == 0


def test_positive_int(monkeypatch):
    monkeypatch.setenv("MAX_REVIEWS", "5")
    assert _max_reviews_cap() == 5


def test_leading_trailing_whitespace_accepted(monkeypatch):
    monkeypatch.setenv("MAX_REVIEWS", "  3  ")
    assert _max_reviews_cap() == 3


def test_non_numeric_loud_failure(monkeypatch, capsys):
    monkeypatch.setenv("MAX_REVIEWS", "abc")
    with pytest.raises(SystemExit):
        _max_reviews_cap()
    err = capsys.readouterr().err
    assert "MAX_REVIEWS" in err
    assert "not numeric" in err


def test_negative_loud_failure(monkeypatch, capsys):
    monkeypatch.setenv("MAX_REVIEWS", "-1")
    with pytest.raises(SystemExit):
        _max_reviews_cap()
    err = capsys.readouterr().err
    assert "MAX_REVIEWS" in err
    assert ">= 0" in err
