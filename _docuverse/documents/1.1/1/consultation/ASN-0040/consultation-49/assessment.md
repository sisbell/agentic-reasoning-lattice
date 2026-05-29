# Channel Assignment — ASN-0040 review-49

**Date:** 2026-05-28 21:28

## Issue 1: Stale T10a claim in B8 contradicts the revised B7
Reason: Derivable from the ASN alone — B7's own Depends line already declares independence from T10a.6 and B8's Preconditions omit it, so the correction is internal consistency cleanup requiring no design or implementation evidence.

## Issue 2: Co-reachability rationale stated three times
Reason: Pure editorial deduplication within the ASN's own text; consolidating three statements of the same scope into the contract needs no external channel.

## Issue 3: B8 provenance essay does not advance the proof
Reason: Internal — the Case 1 / Case 2 split already carries the content, so deleting the redundant provenance paragraph is derivable from the ASN itself.

## Issue 4: Prose justifying document ordering in B6 necessity
Reason: Internal — the clause concerns document placement relative to B8, not the necessity argument; the proof stands on S2 and B7's disjointness target without it.

## Issue 5: B4 decentralization essay, duplicated in B8
Reason: Internal — the substantive point (B4's grain is per-namespace via B7) is already in the ASN; stripping the essay and the T10 forward gesture is editorial.

## Issue 6: Meta-citation sentence in Bop
Reason: Internal — reordering the invariants (B1, B10, B_fin) ahead of Bop or inlining each citation at its point of use is a structural edit derivable from the ASN's own proof dependencies.
