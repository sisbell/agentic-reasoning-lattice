# Channel Assignment — ASN-0125 review-18

**Date:** 2026-06-13 12:43

## Issue 1: The editing-layer discipline commitment contradicts editlink's own `[R]`-emission capability
Reason: Internal consistency repair — the ASN's own EDITop precondition `DC(ℓ')` (retraction clause), EL7(iv), and EL8(d) already commit editlink to producing `[R]`-class successors, and EL-DM/EL7(vi) rely only on `DC` forcing unit-depth shape, not on the commitment's exhaustiveness; widening the `[R]` line to parallel the `[K_sup]` line is the unique fix consistent with what the ASN already decided, with no design-intent or implementation evidence in play.

## Issue 2: Use-site inventory in "K.λ-only composites are valid" (anti-bloat)
Reason: Pure prose trim — the trailing parenthetical roster is redundant with the invariants' actual invocations (R0a in EL4/EL6/EL11, L12 throughout, wp in EL6/EL7), all internal to the ASN, so dropping it is derivable from the ASN's own structure.
