# Channel Assignment — ASN-0091 review-14

**Date:** 2026-05-26 18:00

## Issue 1: Foundation invariant discharge is incomplete in the abstract narrative
Reason: The fix is derivable from the ASN's own framing — RA-frame already fixes Σ.C, Σ.L, Σ.E, Σ.R, and dom(Σ.M) verbatim, and the review explicitly enumerates the missing invariants. Adding the closure statement requires no external evidence about design intent or implementation behavior.

## Issue 2: Worked-example admissibility paragraphs do not enumerate all foundation invariants
Reason: Parallel to Issue 1 at the worked-example level. The review supplies the exact closing sentence; the inheritance argument from RA-frame is already established in the ASN's own structure.

## Issue 3: S2 (functionality) of Σ'.M(d) is verified by concrete inspection but not derived at the abstract level
Reason: The derivation flows directly from RA-π's bijectivity clause — π injective implies unique pre-images, and Σ.M(d) is already a function. The argument uses only definitions already present in the ASN.

## Issue 4: RE-eq witness's "applies symmetrically" wording is misleading
Reason: Pure wording fix. The state-independent character of `c + 1 ≠ a` was already argued in the pre-state portion of the same witness; the review supplies the replacement text.
