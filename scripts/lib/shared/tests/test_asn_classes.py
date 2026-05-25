"""Tests for lib.shared.asn_classes — generalized class membership."""

from __future__ import annotations

import pytest

from lib.shared import asn_classes
from lib.shared.asn_classes import (
    apply_exclude,
    class_for,
    parse_exclude_arg,
)


@pytest.fixture
def yaml_at(tmp_path, monkeypatch):
    """Yields a function that writes YAML content to a tmp file and
    points the module's CLASSES_YAML at it."""
    def _write(content: str):
        path = tmp_path / "asn-classes.yaml"
        path.write_text(content)
        monkeypatch.setattr(asn_classes, "CLASSES_YAML", path)
    return _write


def test_empty_yaml_all_core(yaml_at):
    yaml_at("")
    assert class_for(34) == "core"
    assert class_for(86) == "core"


def test_legacy_operations_and_protocols(yaml_at):
    yaml_at(
        "operations:\n  - 87\n  - 88\nprotocols:\n  - 86\n"
    )
    assert class_for(87) == "operations"
    assert class_for(86) == "protocols"
    assert class_for(34) == "core"


def test_arbitrary_class_name(yaml_at):
    yaml_at(
        "consult:\n  - 68\n  - 69\noperations:\n  - 87\n"
    )
    assert class_for(68) == "consult"
    assert class_for(69) == "consult"
    assert class_for(87) == "operations"
    assert class_for(34) == "core"


def test_class_with_hyphen(yaml_at):
    yaml_at("operations-consult-batch:\n  - 68\n")
    assert class_for(68) == "operations-consult-batch"


def test_inline_comments_in_section(yaml_at):
    yaml_at("consult:    # the bounded batch\n  - 68\n  - 69  # FOLLOWLINK\n")
    assert class_for(68) == "consult"
    assert class_for(69) == "consult"


def test_explicit_core_section_silently_ignored(yaml_at):
    """`core` cannot be declared explicitly; the section is ignored
    and any items inside it get assigned to no class (i.e., default
    to core via the fall-through)."""
    yaml_at("core:\n  - 99\noperations:\n  - 87\n")
    assert class_for(99) == "core"
    assert class_for(87) == "operations"


def test_parse_exclude_empty_inputs(yaml_at):
    yaml_at("operations:\n  - 87\n")
    assert parse_exclude_arg(None) == set()
    assert parse_exclude_arg("") == set()
    assert parse_exclude_arg("   ") == set()
    assert parse_exclude_arg("none") == set()
    assert parse_exclude_arg("NONE") == set()


def test_parse_exclude_accepts_declared(yaml_at):
    yaml_at(
        "consult:\n  - 68\noperations:\n  - 87\nprotocols:\n  - 86\n"
    )
    assert parse_exclude_arg("operations") == {"operations"}
    assert parse_exclude_arg("consult") == {"consult"}
    assert parse_exclude_arg("operations,protocols") == {"operations", "protocols"}
    assert parse_exclude_arg("operations, consult") == {"operations", "consult"}


def test_parse_exclude_accepts_core(yaml_at):
    """core can be excluded — acts as 'drop all implicit-default ASNs'."""
    yaml_at("operations:\n  - 87\n")
    assert parse_exclude_arg("core") == {"core"}
    assert parse_exclude_arg("core,operations") == {"core", "operations"}


def test_apply_exclude_drops_core_when_listed(yaml_at):
    yaml_at("consult:\n  - 68\n  - 69\n")
    labels = ["ASN-0034", "ASN-0068", "ASN-0069"]
    out = apply_exclude(labels, {"core"})
    assert out == ["ASN-0068", "ASN-0069"]


def test_parse_exclude_rejects_undeclared(yaml_at):
    yaml_at("operations:\n  - 87\n")
    with pytest.raises(ValueError, match="invalid --exclude class 'foo'"):
        parse_exclude_arg("foo")
    with pytest.raises(ValueError, match="must be one of: core, operations"):
        parse_exclude_arg("foo")


def test_apply_exclude_filters_correct_class(yaml_at):
    yaml_at(
        "consult:\n  - 68\n  - 69\noperations:\n  - 87\n  - 88\n"
    )
    labels = ["ASN-0034", "ASN-0068", "ASN-0087", "ASN-0088"]
    # Exclude operations → leaves core + consult
    out = apply_exclude(labels, {"operations"})
    assert out == ["ASN-0034", "ASN-0068"]
    # Exclude consult + operations → leaves only core
    out = apply_exclude(labels, {"consult", "operations"})
    assert out == ["ASN-0034"]
    # Exclude nothing → identity
    assert apply_exclude(labels, set()) == labels


def test_apply_exclude_preserves_order(yaml_at):
    yaml_at("operations:\n  - 87\n  - 88\n")
    labels = ["ASN-0087", "ASN-0034", "ASN-0088", "ASN-0036"]
    out = apply_exclude(labels, {"operations"})
    assert out == ["ASN-0034", "ASN-0036"]


def test_multi_class_membership_returns_first_match(yaml_at):
    """An ASN listed under two classes resolves to the first declared
    class (Python dict insertion order)."""
    yaml_at("consult:\n  - 68\noperations:\n  - 68\n")
    assert class_for(68) == "consult"
