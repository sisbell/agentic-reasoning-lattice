# Channel Assignment — ASN-0113 review-9

**Date:** 2026-06-05 00:55

## Issue 1: J4 (ForkComposite) mischaracterized in the W12 reachability construction
Reason: Internal fix. The discrepancy is purely formal — J4's semantics (fork creating `d_new`, K.μ⁺ reusing source range via `φ`, no K.α) versus the `K.α+K.μ⁺+K.ρ` composite are both already specified in ASN-0047, which this ASN cites. The standalone composites already discharge W12; deleting the false equivalence requires no design intent or implementation evidence.

## Issue 2: W4 main-text justification attributes confinement to the wrong bound
Reason: Internal fix. The correction is a property of lexicographic order under T1/T5 — already invoked in the parenthetical and the depth-3 worked instance within this ASN. Reassigning the load-bearing step from the lower bound to the upper bound + T5 is derivable entirely from content already present.
