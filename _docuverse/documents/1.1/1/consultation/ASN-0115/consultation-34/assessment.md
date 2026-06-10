# Channel Assignment — ASN-0115 review-34

**Date:** 2026-06-10 00:36

## Issue 1: The Confinement lemma imports arrangement/C0a context into a purely geometric claim
Reason: Purely editorial deletion. The lemma and its three-line proof use only TumblerAdd (ASN-0034) and T5 (ASN-0034), both already present; collapsing the provenance sentence to a bare parenthetical citation requires no design intent and no implementation evidence — it is derivable from the ASN's own content.

## Issue 2: The transclusion non-disclosure guarantee is stated three times
Reason: Pure deduplication. The non-disclosure guarantee (fact-of-resolution, byte-indistinguishability from S4) already exists in the R8 box; trimming the "Second" point and the Synthesis back-reference removes restatement without sourcing anything new. Internal.

## Issue 3: R6 proof's `act = ∅` parenthetical over-splits a vacuous case
Reason: Editorial simplification. The replacement (when `act = ∅` the depth-`m_S` slice is disjoint from `V_S(d)`, so no bound position, no interior hole) follows directly from the case definition `act = slice ∩ V_S(d) = ∅` and D-SEQ★ contiguity, both already cited; no design intent or implementation evidence is needed.
