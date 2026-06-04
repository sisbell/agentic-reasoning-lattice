# Channel Assignment — ASN-0091 review-66

**Date:** 2026-06-04 01:54

## Issue 1: "K.μ~ is a valid composite" omits the coupling constraints
Reason: The fix is to cite J3 (ReorderingIsolation) from ASN-0047 to discharge the J0/J1★/J1'★ coupling clauses — the constraint and its discharge are both already named in the ASN's own dependency stack, so no design intent or implementation evidence is required.

## Issue 2: The RA-adm discharge is a three-layer derivation where one layer suffices
Reason: Collapsing the three layers into a single ExtendedReachableStateInvariants step is a proof-structure simplification entirely internal to the ASN's existing reasoning and the per-state invariant list it already cites.

## Issue 3: Defensive prose about a rejected proof path
Reason: Pure editorial removal of defensive justification; no external input needed.

## Issue 4: Use-site inventory in the ChainDisjointAdjacency lemma
Reason: Pure editorial deletion of a forward use-site pointer; the lemma content stands on its own.
