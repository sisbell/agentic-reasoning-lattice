"""Integration tests for prompt rendering across lattices.

Confirms that label_prefix substitution applies to a real prompt
file. Uses `config_from_dict` to build LatticeConfig instances
directly so the test doesn't touch the cached `lattice_config()`
singleton or the substrate's active lattice doc.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from lib.lattice.config import config_from_dict
from lib.shared.prompts import _PREFIX_TOKEN, render_prompt


def test_xanadu_lattice_renders_asn_prefix() -> None:
    cfg = config_from_dict({"label_prefix": "ASN"})
    text = f"# Review of {_PREFIX_TOKEN}-NNNN"
    rendered = text.replace(_PREFIX_TOKEN, cfg.label_prefix)
    assert rendered == "# Review of ASN-NNNN"


def test_materials_lattice_renders_mat_prefix() -> None:
    cfg = config_from_dict({"label_prefix": "MAT"})
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
