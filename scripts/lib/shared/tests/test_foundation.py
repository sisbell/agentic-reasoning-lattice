"""Tests for lib.shared.foundation — new load_foundation contract.

Unit tests cover pure validation layers (input + frontmatter dep id
validation). Integration test exercises the live substrate against
every active ASN, asserting each one either resolves to non-empty
content OR raises FoundationError with a clear message — never a
silent zero return.

These tests cover the NEW loader (`load_foundation`) only. The old
`load_foundation_for_note` is the bug we're replacing and is not
covered here.
"""

from __future__ import annotations

import pytest

from lib.shared.foundation import (
    FoundationError,
    _validate_asn_id,
    _validate_dep_ids,
    load_foundation,
)


# ─── Layer 1: asn_id input validation ──────────────────────────────


def test_validate_asn_id_accepts_positive_int() -> None:
    assert _validate_asn_id(97) == 97
    assert _validate_asn_id(1) == 1


def test_validate_asn_id_rejects_zero() -> None:
    with pytest.raises(FoundationError, match="must be positive"):
        _validate_asn_id(0)


def test_validate_asn_id_rejects_negative() -> None:
    with pytest.raises(FoundationError, match="must be positive"):
        _validate_asn_id(-1)


def test_validate_asn_id_rejects_string() -> None:
    with pytest.raises(FoundationError, match="must be int"):
        _validate_asn_id("97")  # type: ignore[arg-type]


def test_validate_asn_id_rejects_float() -> None:
    with pytest.raises(FoundationError, match="must be int"):
        _validate_asn_id(97.0)  # type: ignore[arg-type]


def test_validate_asn_id_rejects_none() -> None:
    with pytest.raises(FoundationError, match="must be int"):
        _validate_asn_id(None)  # type: ignore[arg-type]


def test_validate_asn_id_rejects_bool() -> None:
    # bool is a subclass of int in Python; we explicitly reject it
    with pytest.raises(FoundationError, match="must be int"):
        _validate_asn_id(True)  # type: ignore[arg-type]


# ─── Layer 2: dep id list validation ───────────────────────────────


def test_validate_dep_ids_accepts_int_list() -> None:
    assert _validate_dep_ids(97, [34, 36, 47]) == [34, 36, 47]


def test_validate_dep_ids_accepts_string_numerals() -> None:
    # YAML may parse "34" as a string in some configurations
    assert _validate_dep_ids(97, ["34", "36"]) == [34, 36]


def test_validate_dep_ids_sorts_and_dedupes() -> None:
    assert _validate_dep_ids(97, [47, 34, 36, 34]) == [34, 36, 47]


def test_validate_dep_ids_accepts_empty_list() -> None:
    # depends: [] — legitimate foundation-ASN case
    assert _validate_dep_ids(34, []) == []


def test_validate_dep_ids_rejects_non_list() -> None:
    with pytest.raises(FoundationError, match="must be a list"):
        _validate_dep_ids(97, "34,36")  # type: ignore[arg-type]


def test_validate_dep_ids_rejects_empty_string_entry() -> None:
    with pytest.raises(FoundationError, match="empty string"):
        _validate_dep_ids(97, [34, ""])


def test_validate_dep_ids_rejects_whitespace_string_entry() -> None:
    with pytest.raises(FoundationError, match="empty string"):
        _validate_dep_ids(97, [34, "   "])


def test_validate_dep_ids_rejects_none_entry() -> None:
    with pytest.raises(FoundationError, match="invalid entry"):
        _validate_dep_ids(97, [34, None])


def test_validate_dep_ids_rejects_bool_entry() -> None:
    with pytest.raises(FoundationError, match="invalid entry"):
        _validate_dep_ids(97, [34, True])


def test_validate_dep_ids_rejects_non_numeric_string() -> None:
    with pytest.raises(FoundationError, match="not numeric"):
        _validate_dep_ids(97, [34, "abc"])


def test_validate_dep_ids_rejects_unsupported_type() -> None:
    with pytest.raises(FoundationError, match="unsupported"):
        _validate_dep_ids(97, [34, 36.5])  # type: ignore[list-item]


def test_validate_dep_ids_rejects_zero() -> None:
    with pytest.raises(FoundationError, match="non-positive"):
        _validate_dep_ids(97, [0])


def test_validate_dep_ids_rejects_negative() -> None:
    with pytest.raises(FoundationError, match="non-positive"):
        _validate_dep_ids(97, [-1])


def test_validate_dep_ids_rejects_self_reference() -> None:
    with pytest.raises(FoundationError, match="self-referential"):
        _validate_dep_ids(97, [34, 97])


# ─── load_foundation orchestrator: input gate ──────────────────────


def test_load_foundation_rejects_invalid_asn_id() -> None:
    # Hits the layer 1 gate before any I/O
    with pytest.raises(FoundationError, match="must be positive"):
        load_foundation(0)
    with pytest.raises(FoundationError, match="must be int"):
        load_foundation("97")  # type: ignore[arg-type]


def test_load_foundation_raises_on_missing_inquiry_and_note() -> None:
    # An ASN id with no inquiry file AND no note in substrate. The new
    # LEGACY fallback handles "no inquiry but note exists"; for an ASN
    # with neither, the loader raises with a clear message.
    with pytest.raises(
        FoundationError,
        match="no inquiry file AND no note in substrate",
    ):
        load_foundation(99999)


def test_load_foundation_legacy_fallback_for_protocol_notes(capsys) -> None:
    """Hand-authored protocol notes (no inquiry file) load via the
    LEGACY note-side substrate fallback. ASN-0086 is a known protocol
    note; expect non-empty content and a stderr fallback log line."""
    result = load_foundation(86)
    assert result, "ASN-0086 should load via LEGACY fallback"
    captured = capsys.readouterr()
    assert "LEGACY" in captured.err
    assert "ASN-0086" in captured.err


# ─── Integration: live substrate ───────────────────────────────────
#
# Walks every active ASN. Each one must either succeed (return
# non-empty content, or "" only when `depends: []`) or raise
# FoundationError with a clear message. Never a silent zero return
# from a non-empty declared dep list.


def _iter_active_asn_ids() -> list[int]:
    """Enumerate active, non-retired ASN ids from the live substrate.

    Filters retired notes (carry `retired` classifier on top of `note`)
    — retired ASNs aren't subject to the loader contract.
    """
    from lib.lattice.labels import label_pattern
    from lib.protocols.febe.session import open_session
    from lib.shared.paths import LATTICE, NOTE_DIR, WORKSPACE
    pattern = label_pattern()
    note_prefix = str(NOTE_DIR.relative_to(WORKSPACE)) + "/"
    found: set[int] = set()
    with open_session(LATTICE) as session:
        for path, addr in session.store.path_to_addr.items():
            if not path.startswith(note_prefix):
                continue
            if path.endswith(".statements.md"):
                continue
            if not session.active_links("note", to_set=[addr]):
                continue
            if session.active_links("retired", to_set=[addr]):
                continue
            m = pattern.search(path)
            if m:
                found.add(int(m.group(1)))
    return sorted(found)


def test_load_foundation_against_live_substrate() -> None:
    """For every active ASN: succeed (with non-empty or empty-ok) OR
    raise FoundationError. Never a silent zero from a declared dep
    list, never a non-FoundationError exception."""
    failures: list[str] = []
    silent_zeros: list[int] = []
    for asn_id in _iter_active_asn_ids():
        try:
            result = load_foundation(asn_id)
        except FoundationError:
            # Expected for ASNs in BROKEN/LEGACY/etc. states pre-cleanup
            continue
        except Exception as e:
            failures.append(
                f"ASN-{asn_id:04d}: non-FoundationError raised: "
                f"{type(e).__name__}: {e}",
            )
            continue
        if not result:
            # Empty return — only acceptable if declared deps is empty.
            # We re-read frontmatter to confirm this is the legitimate case.
            from lib.shared.foundation import _read_inquiry_depends
            try:
                declared = _read_inquiry_depends(asn_id)
            except FoundationError:
                # Shouldn't happen — we just succeeded above
                silent_zeros.append(asn_id)
                continue
            if declared:
                silent_zeros.append(asn_id)

    assert not silent_zeros, (
        f"Silent zero return from declared non-empty deps for: "
        f"{silent_zeros} — this is the regression class the refactor "
        f"is designed to eliminate"
    )
    assert not failures, "Non-FoundationError exceptions:\n" + "\n".join(failures)
