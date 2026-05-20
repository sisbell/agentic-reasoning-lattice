# Channel Assignment — ASN-0086 review-73

**Date:** 2026-05-19 17:00

## Issue 1: R7a discharge (4)(iii) implicitly assumes all `d_k` are fresh
Reason: The fix is a proof-structure refinement entirely within the ASN — split (4)(iii) into fresh-d_k (first-emission branch) and existing-d_k (subsequent-emission branch) cases, parallel to how the iteration loop already distinguishes them. K.λ's contract from ASN-0093 already covers both branches; no design intent or implementation evidence is needed.

## Issue 2: R6c-Corollary stated conclusion is strictly narrower than the proof's Step 1 establishes
Reason: Step 1 of the existing proof already establishes Σ.L pointwise-constancy across arrangement-modifying steps; the fix is to lift this to the corollary's statement (or extract it as a named lemma). Purely internal restatement.

## Issue 3: R7a's chain-discipline lemmas discharged via "each transfer through the same construction"
Reason: The discharge mechanism for each chain-discipline lemma is fixed by its proof in ASN-0093 (which the chain-discipline extension consumes), and the reviewer's own commentary identifies the TA5/T10a clauses involved. The fix is enumeration parallel to the four preceding mechanism groups; no external channel needed.

## Issue 4: R0 proof, subsequent-emission case — "ℓ_prev is the maximum index"
Reason: A wording fix — K.λ's contract in ASN-0093 already defines `ℓ_prev` as the T1-max tumbler address. Pure rephrasing internal to the ASN.

## Issue 5: Definition of `nullified` scope rationale — overweight for its placement
Reason: Placement/structure issue only; the reviewer accepts the rationale's content and asks to relocate it. The Definition's mathematical extension and the rationale prose both already exist in the ASN — the fix is to move the paragraph to a Design Note section and leave a pointer.
