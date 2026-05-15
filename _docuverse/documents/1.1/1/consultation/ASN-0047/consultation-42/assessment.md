# Channel Assignment — ASN-0047 review-42

**Date:** 2026-05-15 16:28

## Issue 1: L3 conflicts with ASN-0043
Reason: Resolving the N≥3 vs exactly-3 conflict and the empty-Θ question requires both design intent (was a link defined as a fixed triple or extensible n-tuple, and is type-endset semantically required?) and implementation evidence (what arity does the allocator actually support?).
Nelson question: In Literary Machines, is a link defined as exactly three endsets (from, to, type) with a required non-empty type-endset, or is it an n-ary structure with N ≥ 3 endsets and an optional type?
Gregory question: Does udanax-green's link allocation (docreatelink and the link-orgl structure) fix the endset count at three, or does it support N ≥ 3, and does it require the type-endset to be non-empty?

## Issue 2: D-CTG/D-MIN applied to link subspace conflicts with ASN-0036
Reason: Whether link arrangements must be contiguous or admit tombstones is a design-intent question (Nelson's withdrawal mechanism) and an implementation question (does the allocator/arrangement code permit gaps in the link subspace?).
Nelson question: When a link is withdrawn (made "not currently addressable"), does its V-position in the home document's link subspace remain occupied as a tombstone, or is the position freed and the surrounding range compacted?
Gregory question: Does udanax-green's link-subspace arrangement enforce contiguous V-positions, or does it permit sparse arrangements with gaps (e.g., from withdrawn or deleted links)?

## Issue 3: Per-subspace D-SEQ used without foundation
Reason: This is a purely internal derivation — per-subspace D-SEQ follows from per-subspace D-CTG + D-MIN + S8a + S8-fin + S8-depth, mirroring the ASN-0036 derivation. No external evidence needed; the fix is to either prove it locally or restate ASN-0036's per-subspace forms in the amendments.

## Issue 4: K.δ and K.λ allocator discipline weakened by "typically"
Reason: Tightening "typically" to a structural requirement requires implementation evidence about how entity and link addresses are actually produced (always via inc(·, k)? always under parent ownership?). Nelson's design is silent on the allocator-level mechanism.
Gregory question: In udanax-green, are all entity addresses (nodes, accounts, documents) produced exclusively via inc(·, k) within the parent's ownership domain, and are all link addresses produced via inc(·, 0) on the link allocator's frontier under the home document's link prefix — or are non-conforming allocation paths possible?

## Issue 5: P3★ formal statement weaker than verbal claim
Reason: Internal formalism fix — strengthen P3★'s formal statement to add value-preservation clauses for C and L, matching P0 and L12 which are already established in this ASN. No external input needed.

## Issue 6: K.μ⁻ valid-contractions constraint stated as postcondition, not precondition
Reason: Presentation symmetry with K.μ⁺_L — restate the per-subspace suffix-removal constraint as an explicit precondition with D-CTG/D-MIN as consequences. Purely internal restructuring.

## Issue 7: Π = id case in K.μ~ — "vacuous round-trip" wording unclear
Reason: Internal clarification of an existing decomposition argument. Pick one of the two phrasings (zero elementary steps vs. n'=0 remove-and-re-add) consistently with the ExtendedReachableStateInvariants proof. No external input needed.
