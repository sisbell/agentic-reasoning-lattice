"""Retry helpers — re-feed open revises and surface declined findings."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import LATTICE
from lib.claim_convergence.full_review.review import extract_findings
from lib.claim_convergence.full_review.revise import revise
from lib.store.queries import unresolved_revise_comments


def _retry_unresolved_revises(store, asn_num, claim_dir, scope_md_paths):
    """Re-feed open revise comments to the reviser at the top of a cycle.

    For each unresolved comment.revise targeting a scope path, fetch its
    finding text from the comment's source (the finding document under
    `_docuverse/findings/...`) and call `revise()` again. The reviser closes
    via `convergence-link-resolution.py accept` (with edit) or
    `convergence-link-resolution.py reject` (with rationale).
    """
    for scope_path in scope_md_paths:
        if not scope_path:
            continue
        for c in unresolved_revise_comments(store, scope_path):
            if not c["from_set"]:
                continue
            finding_path = LATTICE / c["from_set"][0]
            if not finding_path.exists():
                continue
            finding_text = finding_path.read_text()
            findings = extract_findings(finding_text)
            if not findings:
                continue
            title = findings[0][0]
            target_path = c["to_set"][0] if c["to_set"] else None
            print(f"  [RETRY] re-feeding open comment {c['id']} ({title})",
                  file=sys.stderr)
            revise(asn_num, title, finding_text, claim_dir=claim_dir,
                   comment_id=c["id"], claim_path=target_path)


def _declined_findings_for_cone(store, cone_md_paths, max_rejects=5):
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

    The reviewer is shown only the declined ones to discourage
    re-surfacing findings of the same shape that have already been
    deliberated and refused.
    """
    cone_paths = set(cone_md_paths)
    rejects = store.find_links(type_set=["resolution.reject"])
    rejects.sort(key=lambda r: r.get("ts", ""), reverse=True)

    blocks = []
    lattice = Path(LATTICE)
    for r in rejects:
        if len(blocks) >= max_rejects:
            break
        if not r.get("to_set") or len(r["to_set"]) < 2:
            continue
        comment_id = r["to_set"][0]
        rationale_rel = r["to_set"][1]

        comment = store.get(comment_id)
        if comment is None or not comment.get("to_set"):
            continue
        if comment["to_set"][0] not in cone_paths:
            continue
        if not comment.get("from_set"):
            continue

        finding_full = lattice / comment["from_set"][0]
        finding_body = (finding_full.read_text().strip()
                        if finding_full.exists() else "(finding body missing)")
        rationale_full = lattice / rationale_rel
        rationale_text = (rationale_full.read_text().strip()
                          if rationale_full.exists() else "(rationale missing)")

        ts = r.get("ts", "?")
        blocks.append(
            f"### Declined ({ts})\n\n"
            f"**Finding (rejected as invalid):**\n\n{finding_body}\n\n"
            f"**Reviser's rationale for declining:**\n\n{rationale_text}"
        )

    return "\n\n---\n\n".join(blocks) if blocks else ""
