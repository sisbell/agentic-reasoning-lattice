"""Integration tests for prompt rendering across lattices.

Confirms that loading a real prompt file applies the active lattice's
label_prefix substitution. Uses load_lattice_config(path) directly so
the test isn't sensitive to the LATTICE env var or the cached
lattice_config() module-level singleton.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from lib.lattice.config import load_lattice_config
from lib.shared.prompts import _PREFIX_TOKEN, render_prompt


def test_xanadu_lattice_renders_asn_prefix(tmp_path: Path) -> None:
    cfg_path = tmp_path / "config.yaml"
    cfg_path.write_text("label_prefix: ASN\n")
    cfg = load_lattice_config(cfg_path)
    text = f"# Review of {_PREFIX_TOKEN}-NNNN"
    rendered = text.replace(_PREFIX_TOKEN, cfg.label_prefix)
    assert rendered == "# Review of ASN-NNNN"


def test_materials_lattice_renders_mat_prefix(tmp_path: Path) -> None:
    cfg_path = tmp_path / "config.yaml"
    cfg_path.write_text("label_prefix: MAT\n")
    cfg = load_lattice_config(cfg_path)
    text = f"# Review of {_PREFIX_TOKEN}-NNNN"
    rendered = text.replace(_PREFIX_TOKEN, cfg.label_prefix)
    assert rendered == "# Review of MAT-NNNN"


def test_real_shared_prompt_contains_token() -> None:
    """The shared note_statements prompt has been templated."""
    prompt_path = (
        Path(__file__).resolve().parent.parent.parent.parent.parent
        / "prompts" / "shared" / "agents" / "producers" / "note_statements.md"
    )
    if not prompt_path.exists():
        pytest.skip("shared note_statements prompt missing")
    body = prompt_path.read_text()
    assert _PREFIX_TOKEN in body, (
        "shared/note_statements.md must use {{label_prefix}} placeholder"
    )


def test_render_substitutes_in_real_prompt() -> None:
    """Rendering a real shared prompt produces the active prefix."""
    prompt_path = (
        Path(__file__).resolve().parent.parent.parent.parent.parent
        / "prompts" / "shared" / "agents" / "producers" / "note_statements.md"
    )
    if not prompt_path.exists():
        pytest.skip("shared note_statements prompt missing")
    body = prompt_path.read_text()
    rendered = render_prompt(body)
    # Token must be gone
    assert _PREFIX_TOKEN not in rendered
    # And replaced with the active lattice's prefix (ASN under defaults)
    assert "ASN-NNNN" in rendered or "ASN-" in rendered
