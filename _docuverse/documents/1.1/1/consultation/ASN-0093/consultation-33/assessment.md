# Channel Assignment — ASN-0093 review-33

**Date:** 2026-05-31 06:43

## Issue 1: "Forward allocation, derivable" derives an unconsumed property and defends its non-inclusion
Reason: Internal — the fix is deletion of a property the review already established is consumed by no invariant or discharge within the substrate; no design-intent or implementation evidence bears on whether to remove unconsumed prose.

## Issue 2: "(cited downstream)" forward-pointer annotation
Reason: Internal — dropping a meta-prose annotation while keeping the admissibility statement is a pure editorial fix with no dependence on design intent or implementation.

## Issue 3: Defensive "not parallel chains" paragraph
Reason: Internal — the two chains are exhibited in full immediately above; removing the defensive disclaimer is derivable from the ASN's own content.

## Issue 4: K.σ "anchor-disjointness" discharges an excluded non-case
Reason: Internal — whether `d ∉ dom(C) ∪ dom(L)` or `d ≠ anchor` is consumed by any discharge is answerable from the ASN's own invariants (the `zeros = 2` vs `zeros = 3` gap and the carrier-set status of anchors are both stated in-note).

## Issue 5: Discharge matrix attributes derived facts to "precondition"
Reason: Internal — the deriving disciplines for the subsequent-emit branch (B5a / ChainUniformZeroCount for `zeros`, TA5(c) length preservation for `#E`) are already present in the ASN; the fix only relabels the matrix to match the existing proof.
