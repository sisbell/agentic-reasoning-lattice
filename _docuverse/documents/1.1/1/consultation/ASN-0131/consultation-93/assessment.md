# Channel Assignment — ASN-0131 review-93

**Date:** 2026-06-14 19:25

## Issue 1: The K.λ stability case-split omits the self-emit Nullify
Reason: Derivable from the ASN alone. Every piece of the benign argument is already in the note: RE-ADDR's excluded branch (a fresh output that retracts its own emitter address is born-nullified, non-addressable — already stated in §"Fresh emissions": "covers `ℓ_new` exactly when `ℓ_new` retracts its own emitter address"), the R-Scope/SingleTupleScope single-target argument already invoked for retraction (applied at target = `b` instead of `ℓ`, and the note already flags R-Scope as arity-independent), and the `K.λ` `M' = M` frame used throughout. The self-emit branch's existence and validity are already imported from ASN-0086 by the review's own citations (P-tgt, R-Scope, wp Case 1); the fix only assembles these into one case.

## Issue 2: anticipatory use-site inventory in §"Fresh emissions"
Reason: Pure editorial deduplication internal to the note — dropping a clause that duplicates §Stability and collapsing `K.ρ`'s double justification. The frames being relocated and the LP14 route are already established in the note; no design intent or implementation evidence bears on the cut.
