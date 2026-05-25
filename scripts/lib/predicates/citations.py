"""Citation-graph predicates.

Outgoing/incoming citation traversal over `citation.<direction>`
links. Retracted citations drop from the graph automatically.

Generated from `lib/predicates/factory.py`'s `citation_outgoing` /
`citation_incoming` templates parameterized by direction.

**Convention notice — `depends(session, X)` semantics depend on X:**
  - X is a review_addr → returns cascade-anchor targets the review
    emitted (canonical use; see is_note_cascade_fresh)
  - X is a claim_addr (or version_head(claim_addr)) → returns claim's
    own cross-ASN citations (claim-side cascade-fresh)
  - X is a note_addr → returns ONLY note-side citation.depends, which
    is empty for HEALTHY ASNs under the post-2026-05-24 convention.
    For "what are this ASN's foundation deps?" use
    `lib.shared.foundation.foundation_dep_ids` /
    `foundation_dep_addrs` instead — they route through the canonical
    inquiry-primary + LEGACY-fallback resolution path.

See `docs/design-notes/asn-dep-lookup-convention.md`.
"""

from __future__ import annotations

from .factory import citation_incoming, citation_outgoing


depends = citation_outgoing("depends")
dependents = citation_incoming("depends")
