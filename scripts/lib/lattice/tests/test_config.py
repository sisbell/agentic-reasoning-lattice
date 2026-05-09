"""Tests for lib.lattice.config — LatticeConfig + per-path loader."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from lib.lattice.config import (
    DEFAULT_LABEL_PREFIX,
    LatticeConfig,
    load_lattice_config,
)


def _write(tmp_path: Path, body: str) -> Path:
    cfg = tmp_path / "config.yaml"
    cfg.write_text(textwrap.dedent(body).lstrip())
    return cfg


def test_missing_file_returns_defaults(tmp_path: Path) -> None:
    cfg = load_lattice_config(tmp_path / "no-such.yaml")
    assert cfg == LatticeConfig()
    assert cfg.label_prefix == DEFAULT_LABEL_PREFIX
    assert cfg.default_campaign is None


def test_empty_file_returns_defaults(tmp_path: Path) -> None:
    path = _write(tmp_path, "")
    cfg = load_lattice_config(path)
    assert cfg == LatticeConfig()


def test_label_prefix_loaded(tmp_path: Path) -> None:
    path = _write(tmp_path, "label_prefix: MAT\n")
    cfg = load_lattice_config(path)
    assert cfg.label_prefix == "MAT"


def test_default_campaign_loaded(tmp_path: Path) -> None:
    path = _write(tmp_path, "default_campaign: foo\n")
    cfg = load_lattice_config(path)
    assert cfg.default_campaign == "foo"


def test_both_fields_loaded(tmp_path: Path) -> None:
    path = _write(
        tmp_path,
        """
        label_prefix: MAT
        default_campaign: dulong-petit
        """,
    )
    cfg = load_lattice_config(path)
    assert cfg.label_prefix == "MAT"
    assert cfg.default_campaign == "dulong-petit"


def test_unknown_fields_ignored(tmp_path: Path) -> None:
    path = _write(
        tmp_path,
        """
        label_prefix: ASN
        future_field: ignored
        """,
    )
    cfg = load_lattice_config(path)
    assert cfg.label_prefix == "ASN"


def test_config_is_frozen() -> None:
    cfg = LatticeConfig(label_prefix="ASN")
    with pytest.raises(Exception):
        cfg.label_prefix = "MAT"  # type: ignore[misc]
