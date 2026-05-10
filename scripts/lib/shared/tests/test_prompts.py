"""Tests for lib.shared.prompts — render_prompt + read_prompt."""

from __future__ import annotations

from pathlib import Path

from lib.shared.prompts import read_prompt, render_prompt


def test_render_substitutes_prefix_token() -> None:
    assert render_prompt("{{label_prefix}}-NNNN") == "ASN-NNNN"


def test_render_replaces_all_occurrences() -> None:
    text = "head: {{label_prefix}}-0001 / tail: {{label_prefix}}-0002"
    assert render_prompt(text) == "head: ASN-0001 / tail: ASN-0002"


def test_render_leaves_other_braces_alone() -> None:
    text = "Use {{title}} and {{question}}; prefix is {{label_prefix}}."
    out = render_prompt(text)
    assert "{{title}}" in out
    assert "{{question}}" in out
    assert "ASN" in out


def test_render_no_token_passthrough() -> None:
    text = "no placeholder here"
    assert render_prompt(text) == text


def test_read_prompt_substitutes_on_disk(tmp_path: Path) -> None:
    p = tmp_path / "x.md"
    p.write_text("# {{label_prefix}}-NNNN body\n")
    assert read_prompt(p) == "# ASN-NNNN body\n"
