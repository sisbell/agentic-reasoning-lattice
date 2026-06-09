# Channel Assignment — ASN-0116 review-43

**Date:** 2026-06-09 11:45

## Issue 1: Post-state well-formedness is established twice — once as K.μ⁺ preconditions, once as a standalone walk-through — and several invariants delivered free by the cited theorem are re-derived anyway
Reason: The fix is purely structural — deciding which clauses are genuine K.μ⁺ precondition-inputs to validity versus corollaries of ExtendedReachableStateInvariants (ASN-0047), then deleting or marking the duplicates. Both theorems and the dependency structure are already present in the ASN; no design intent or implementation evidence is required.
