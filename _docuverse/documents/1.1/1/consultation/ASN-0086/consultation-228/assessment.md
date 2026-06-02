# Channel Assignment — ASN-0086 review-228

**Date:** 2026-06-01 19:21

## Issue 1: The "post-state membership" clarification of the unit-depth discipline is stated three times
Reason: Pure editorial deduplication — state the post-state-evaluation convention once in the discipline definition and cite it elsewhere. Both sites already exist in the ASN; no design intent or implementation evidence is needed.

## Issue 2: "Definition — relational layer" carries defensive meta-prose and conflates the operation with its wp-cases
Reason: Internal restructuring — the operation/wp-case distinction and the "would be stronger" aside are both already grounded in the ASN's own Nullify definition and wp Case 1. Tightening the prose requires nothing external.

## Issue 3: Worked Sketch Step 4's parenthetical re-derives the entire layer-commitment apparatus
Reason: The parenthetical restates material already established in Definition — Nullify, Definition — relational layer, and the wp section; reducing it to a pointer is purely internal cross-referencing.

## Issue 4: "The layer satisfies the unit-depth retraction discipline" is asserted without the base+step induction
Reason: The induction's ingredients — empty seed `Σ_init.L = ∅`, the `K ≁ R` / `Nullify` case split, and L12a target persistence — are all already present in the ASN, so the proof is derivable from its own content.
