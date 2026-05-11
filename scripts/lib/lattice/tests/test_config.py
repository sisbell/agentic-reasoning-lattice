"""Tests for lib.lattice.config — LatticeConfig + loaders."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from lib.lattice.config import (
    DEFAULT_LABEL_PREFIX,
    LatticeConfig,
    config_from_dict,
    config_from_doc,
)


# ─── config_from_dict: structural mapping ──────────────────────────


def test_empty_dict_returns_defaults() -> None:
    cfg = config_from_dict({})
    assert cfg == LatticeConfig()
    assert cfg.label_prefix == DEFAULT_LABEL_PREFIX
    assert cfg.default_campaign is None


def test_label_prefix_mapped() -> None:
    cfg = config_from_dict({"label_prefix": "MAT"})
    assert cfg.label_prefix == "MAT"
    assert cfg.default_campaign is None


def test_default_campaign_mapped() -> None:
    cfg = config_from_dict({"default_campaign": "foo"})
    assert cfg.label_prefix == DEFAULT_LABEL_PREFIX
    assert cfg.default_campaign == "foo"


def test_both_fields_mapped() -> None:
    cfg = config_from_dict(
        {"label_prefix": "MAT", "default_campaign": "dulong-petit"},
    )
    assert cfg.label_prefix == "MAT"
    assert cfg.default_campaign == "dulong-petit"


def test_unknown_fields_ignored() -> None:
    cfg = config_from_dict(
        {"label_prefix": "ASN", "future_field": "ignored"},
    )
    assert cfg.label_prefix == "ASN"


def test_config_is_frozen() -> None:
    cfg = LatticeConfig(label_prefix="ASN")
    with pytest.raises(Exception):
        cfg.label_prefix = "MAT"  # type: ignore[misc]


# ─── config_from_doc: file walk + frontmatter parse ────────────────


def test_missing_doc_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        config_from_doc(tmp_path / "missing.md")


def test_reads_frontmatter_from_doc(tmp_path: Path) -> None:
    doc = tmp_path / "xanadu.md"
    doc.write_text(textwrap.dedent("""
        ---
        label_prefix: MAT
        default_campaign: dulong-petit
        ---

        # Lattice body
        """).lstrip())
    cfg = config_from_doc(doc)
    assert cfg.label_prefix == "MAT"
    assert cfg.default_campaign == "dulong-petit"
