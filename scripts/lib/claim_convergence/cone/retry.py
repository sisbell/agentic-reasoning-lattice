"""Retry helpers — re-feed open revises and surface declined findings."""

import sys
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import LATTICE
from lib.claim_convergence.full_review.review import extract_findings
from lib.claim_convergence.full_review.revise import revise
from lib.backend.addressing import Address
from lib.backend.predicates import unresolved_revise_comments
from lib.backend.store import Store


def _retry_unresolved_revises(
    store: Store, asn_num: int, claim_dir: Path,
    scope_addrs: List[Address],
) -> None:
    """Re-feed open revise comments to the reviser at the top of a cycle.

    For each unresolved comment.revise targeting a scope doc, fetch its
    finding text from the comment's source (the finding document under
    `_docuverse/findings/...`) and call `revise()` again. The reviser closes
    via `convergence-link-resolution.py accept` (with edit) or
    `convergence-link-resolution.py reject` (with rationale).
    """
    for scope_addr in scope_addrs:
        if scope_addr is None:
            continue
        for c in unresolved_revise_comments(store.state, scope_addr):
            if not c.from_set:
                continue
            finding_addr = c.from_set[0]
            finding_rel = store.path_for_addr(finding_addr)
            if not finding_rel:
                continue
            finding_full = LATTICE / finding_rel
            if not finding_full.exists():
                continue
            finding_text = finding_full.read_text()
            findings = extract_findings(finding_text)
            if not findings:
                continue
            title = findings[0][0]
            target_addr = c.to_set[0] if c.to_set else None
            target_path = store.path_for_addr(target_addr) if target_addr else None
            print(f"  [RETRY] re-feeding open comment {c.addr} ({title})",
                  file=sys.stderr)
            revise(asn_num, title, finding_text, claim_dir=claim_dir,
                   comment_id=str(c.addr), claim_path=target_path)


def _declined_findings_for_cone(
    store: Store,
    cone_addrs: List[Address],
    max_rejects: int = 5,
) -> str:
    """Return text of recently-declined findings on this cone.

    A declined finding is a `comment.revise` targeting any cone claim
    that was closed by `resolution.reject` (the reviser refused to act).
    Each block contains the original finding body plus the reviser's
    rationale text. Sorted by recency, capped at `max_rejects`.

    Accepted findings (closed by `resolution.edit`) are NOT included —
    their resolution lives in the prose itself, so re-evaluating the
    current prose is the correct check on whether the issue persists.
    Open findings (no resolution yet) are NOT included either — they're
    handled by the orchestrator's retry pass at cycle entry.
    """
    cone_addr_set = set(a for a in cone_addrs if a is not None)
    rejects = store.find_links(type_="resolution.reject")

    blocks = []
    lattice = Path(LATTICE)
    # Newest-first: LinkStore preserves emission order, so reverse it
    for r in reversed(rejects):
        if len(blocks) >= max_rejects:
            break
        if not r.to_set or len(r.to_set) < 2:
            continue
        # Substrate convention (matches legacy + migrated data):
        # resolution.reject has F=[rationale_doc], G=[comment_addr, ...]
        # — the comment is in to_set; rationale path is the second to_set
        # entry under the legacy convention. Preserve that here.
        comment_addr = r.to_set[0]
        rationale_addr = r.to_set[1]

        try:
            comment = store.state.links.get(comment_addr)
        except KeyError:
            continue
        if not comment.to_set:
            continue
        if comment.to_set[0] not in cone_addr_set:
            continue
        if not comment.from_set:
            continue

        finding_rel = store.path_for_addr(comment.from_set[0])
        if not finding_rel:
            continue
        finding_full = lattice / finding_rel
        finding_body = (finding_full.read_text().strip()
                        if finding_full.exists() else "(finding body missing)")

        rationale_rel = store.path_for_addr(rationale_addr)
        if rationale_rel:
            rationale_full = lattice / rationale_rel
            rationale_text = (rationale_full.read_text().strip()
                              if rationale_full.exists() else "(rationale missing)")
        else:
            rationale_text = "(rationale missing)"

        blocks.append(
            f"### Declined\n\n"
            f"**Finding (rejected as invalid):**\n\n{finding_body}\n\n"
            f"**Reviser's rationale for declining:**\n\n{rationale_text}"
        )

    return "\n\n---\n\n".join(blocks) if blocks else ""
