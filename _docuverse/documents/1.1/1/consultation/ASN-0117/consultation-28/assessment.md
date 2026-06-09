# Channel Assignment — ASN-0117 review-28

**Date:** 2026-06-09 11:04

## Issue 1: P4a (a composite-boundary invariant) is never addressed
Reason: The fix is internal — the review itself supplies both remedies (cite the composite-boundary half of ExtendedReachableStateInvariants, or derive P4a from `R' = R` and the trace-prefix relation, both already in the ASN's reasoning). No design intent or implementation evidence is needed.

## Issue 2: Duplicated "blanket `ran ⊆ dom(C)` would be false" argument
Reason: Purely editorial — state the per-subspace S3★ split once and have the later section cite it. No channel needed.

## Issue 3: Defensive comparative prose in DEL-LIMM and boundary examples
Reason: Purely editorial — drop the L12 counterfactual and collapse the two `R = ∅` boundary examples. Derivable from the ASN alone; no channel needed.
