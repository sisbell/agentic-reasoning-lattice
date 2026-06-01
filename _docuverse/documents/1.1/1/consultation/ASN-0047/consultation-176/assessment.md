# Channel Assignment — ASN-0047 review-176

**Date:** 2026-05-31 22:03

## Issue 1: S8★ silently weakens foundation S8 — "substitutes for" overstates what it guarantees
Reason: The fix is to acknowledge that ASN-0036's S8 condition (c) (uniqueness of the maximal-run decomposition) is not carried into S8★ and to confirm no downstream property depends on it. Both the foundation S8 structure and the internal dependency check (D-SEQ★ derives from D-CTG★+D-MIN★+S8-depth+S8-fin+S8a, not S8★) are settled by the cited foundation and this ASN's own derivations — no design-intent or implementation evidence is required.

## Issue 2: Rationale prose in the K.δ operational slot (forward-reference accretion)
Reason: This is a pure placement/concision edit — reduce the subsumption note to the load-bearing claim and let S7d own the three-route enumeration. Fully derivable from the ASN's own structure; no channel needed.
