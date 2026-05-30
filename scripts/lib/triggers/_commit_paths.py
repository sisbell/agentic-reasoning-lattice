"""Shared `commit_paths` helpers for triggers.

Each trigger declares which paths its fire owns so the runner's
auto-commit stages only those (plus substrate metadata) instead of
sweeping all of _docuverse/. These helpers cover the recurring
patterns; rarer cases can declare commit_paths inline.

All helpers return paths relative to WORKSPACE (repo root), suitable
for passing to `git add`.
"""

from __future__ import annotations

import re

from lib.backend.addressing import Address
from lib.backend.store import _parse_node_user_from_path
from lib.lattice.labels import label_pattern
from lib.protocols.febe.protocol import Session
from lib.shared.paths import (
    CLAIM_DIR, CLAIM_FINDINGS_DIR, CLAIM_REVIEWS_DIR,
    NOTE_FINDINGS_DIR, NOTE_REVIEWS_DIR, RATIONALE_DIR, WORKSPACE,
)


def _asn_label_from_path(path: str) -> str | None:
    """Extract the ASN-NNNN label from a substrate path. None if absent."""
    if not path:
        return None
    m = label_pattern().search(path)
    return m.group(0) if m else None


def _claim_subdir_rel(path: str, kind: str, asn_label: str) -> str:
    """Build the WORKSPACE-relative claim/review/finding subdir for `path`'s
    (node, user) region.

    `kind` ∈ {"claim", "review/claims", "finding/claims"}. The (node, user)
    prefix is parsed from the substrate path so commit paths track the
    actual region the addr lives in (e.g., 1.3/1 for claim-derivation
    work), not the lattice default.
    """
    nu = _parse_node_user_from_path(path) if path else None
    if nu is None:
        # Fall back to lattice defaults for non-prefixed paths.
        defaults = {
            "claim": CLAIM_DIR,
            "review/claims": CLAIM_REVIEWS_DIR,
            "finding/claims": CLAIM_FINDINGS_DIR,
            "finding/notes": NOTE_FINDINGS_DIR,
        }
        return str((defaults[kind] / asn_label).relative_to(WORKSPACE))
    node, user = nu
    return f"_docuverse/documents/{node}/{user}/{kind}/{asn_label}"


def per_claim_commit_paths(
    session: Session, claim_addr: Address,
) -> list[str]:
    """Per-claim file family — main claim doc + all known sidecars.

    Many claim-side triggers fire on a single claim and write to that
    claim's main file or one of its sidecar attributes (description,
    signature, references, label, name, contract). Returning the full
    sidecar family keeps the commit accurate even when the agent edits
    one sidecar and the next fire's check picks up another.

    Non-existent paths in the returned list are silently skipped by
    `_stage_dirty`; we list the full family so any subset emitted by
    the fire lands in the commit.
    """
    claim_path = session.get_path_for_addr(claim_addr)
    if not claim_path:
        return []
    asn_label = _asn_label_from_path(claim_path)
    if asn_label is None:
        return []
    # Derive claim label from the filename stem. Main claim path is
    # `<asn>/<label>.md`; sidecars are `<asn>/<label>.<attr>.md`.
    from pathlib import Path
    p = Path(claim_path)
    stem = p.name
    # Strip trailing .md
    if stem.endswith(".md"):
        stem = stem[:-3]
    # If this is a sidecar (label.attr), take just the label part
    label = stem.split(".", 1)[0]
    asn_dir_rel = _claim_subdir_rel(claim_path, "claim", asn_label)
    return [
        f"{asn_dir_rel}/{label}.md",
        f"{asn_dir_rel}/{label}.description.md",
        f"{asn_dir_rel}/{label}.signature.md",
        f"{asn_dir_rel}/{label}.references.md",
        f"{asn_dir_rel}/{label}.label.md",
        f"{asn_dir_rel}/{label}.name.md",
        f"{asn_dir_rel}/{label}.contract.md",
    ]


def per_asn_claim_review_paths(
    session: Session, addr: Address,
) -> list[str]:
    """Claim-side review + finding subtrees for the addr's ASN.

    Triggers like cone_review / full_review / claim_structural_audit
    emit review docs about an ASN's claims, plus per-issue finding
    decompositions. Both live under the ASN's review and finding
    subtrees.
    """
    path = session.get_path_for_addr(addr)
    asn_label = _asn_label_from_path(path) if path else None
    if asn_label is None:
        return []
    return [
        _claim_subdir_rel(path, "review/claims", asn_label),
        _claim_subdir_rel(path, "finding/claims", asn_label),
    ]


def per_review_finding_paths(
    session: Session, review_addr: Address,
) -> list[str]:
    """Finding-decomposition paths for a single review.

    claim_findings fires on a review doc and emits finding docs into
    a review-N/ subdirectory under the ASN's finding tree (claim-side
    or note-side, depending on which family the review covered).

    Returns both possible subtrees keyed by ASN, plus the review doc
    itself (the fire may also write provenance.derivation that links
    to the review).
    """
    path = session.get_path_for_addr(review_addr)
    asn_label = _asn_label_from_path(path) if path else None
    if asn_label is None:
        return []
    return [
        path,  # the review doc itself (in case its body gets touched)
        _claim_subdir_rel(path, "finding/claims", asn_label),
        _claim_subdir_rel(path, "finding/notes", asn_label),
    ]


def claims_aggregate_paths(
    session: Session, note_addr: Address,
) -> list[str]:
    """The `_statements.md` aggregate for the target ASN's claims.

    claims_statements_refresh emits/updates a single aggregate doc
    under `claim/<ASN>/_statements.md`. Per-claim files are NOT
    touched by this trigger (the aggregate is a roll-up read).
    """
    path = session.get_path_for_addr(note_addr)
    asn_label = _asn_label_from_path(path) if path else None
    if asn_label is None:
        return []
    # claims-statements-refresh writes the aggregate into the agent's
    # region (claim_dir), not the note's region. Use the agent's class
    # attrs to derive the aggregate's location.
    from lib.agents.producers.claims_statements_refresh import (
        ClaimsStatementsRefreshAgent,
    )
    agg_kind_dir = ClaimsStatementsRefreshAgent().claim_dir / asn_label
    asn_dir_rel = str(agg_kind_dir.relative_to(WORKSPACE))
    return [f"{asn_dir_rel}/_statements.md"]


def rationale_dir_for_asn(
    path: str | None, asn_label: str | None,
) -> str | None:
    """Per-ASN rationale subdir for revise fires that may call
    `resolution.py reject`.

    Each rejected finding writes a rationale doc to
    `<region>/rationale/<asn_label>/<comment_addr>.md`. The substrate's
    `resolution.reject` link lands in `links.jsonl` automatically, but
    the rationale FILE belongs to the fire and must be in commit_paths
    or it accumulates as untracked dirt.

    Returns the WORKSPACE-relative dir path, or None when `asn_label`
    is missing. Non-existent dirs are skipped by `_stage_dirty`.
    """
    if asn_label is None:
        return None
    nu = _parse_node_user_from_path(path) if path else None
    if nu is None:
        return str((RATIONALE_DIR / asn_label).relative_to(WORKSPACE))
    node, user = nu
    return f"_docuverse/documents/{node}/{user}/rationale/{asn_label}"


def single_path(session: Session, addr: Address) -> list[str]:
    """Return the addr's registered path as the single owned path.

    For fires that write only to the doc address they fire on (e.g.,
    note_revise editing the note body, note_statements writing a
    sidecar). The trigger module that uses this helper supplies its
    own context.
    """
    p = session.get_path_for_addr(addr)
    return [p] if p else []
