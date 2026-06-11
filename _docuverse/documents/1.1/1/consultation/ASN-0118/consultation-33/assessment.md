# Channel Assignment — ASN-0118 review-33

**Date:** 2026-06-11 00:16

## Issue 1: V-spec definition paragraph has accreted genealogy, defense, example, and implementation evidence into one block
Reason: The restructuring (definition first, relaxation in one clause, example moved out) is internal — all content is already present in the ASN. But the reconciliation of "matches the relaxed admissibility at every stage" with the recorded clipping divergence requires knowing precisely which pipeline stage the divergence lives in, so the compressed sentence scopes "matches" accurately; that is implementation evidence.
Gregory question: In udanax-green's spec-set processing, at which stage does the integer-offset clipping arithmetic that discards sub-depth structure occur — admissibility validation (`acceptablevsa`/`specset2ispanset`), the tumbler-order span classification, or content retrieval after classification — so that we can state which stages match the relaxed admissibility and which diverge?

## Issue 2: Repeated forward deferrals to the composite section
Reason: Pure editorial consolidation — removing two of three redundant forward references and letting CP8's clauses stand without the parenthetical. No design intent or implementation evidence is involved; the fix is derivable from the ASN's own structure.

## Issue 3: The link-discoverability wp omits the enabledness conjunct that the foundation's own wp convention includes
Reason: The fix is internal — the review identifies the in-house precedent (ASN-0098 LP12a's `enabled(...) ∧ ⟨pullback⟩` form) and the ASN already defines COPY's enabledness conditions (`W ≥ 1`, content residence, valid insertion position), so conjoining `enabled(COPY(Σ, d, p, R))` or scoping the wp to the enabled domain requires no external consultation.
