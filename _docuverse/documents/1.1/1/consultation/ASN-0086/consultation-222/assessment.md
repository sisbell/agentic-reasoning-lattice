# Channel Assignment — ASN-0086 review-222

**Date:** 2026-06-01 18:19

## Issue 1: R0 first-emission branch mislabels the chain's first emission as its "anchor"
Reason: The fix is purely terminological and derivable from the note's own "Allocator Structure" section, which already states the chain is anchored at `b_L(d) := [d.0.s_L]` with first emission `[d.0.s_L.1]`. The corrected wording the review prescribes is internally consistent with that section; no design intent or implementation evidence is required.

## Issue 2: Leftover defensive meta-prose around R0's precondition
Reason: This is a pure editorial deletion — removing two self-justifying sentences and reducing the Emit_K precondition to its statement. The vacuity of the universal over `d ∈ dom(Σ.M)` is already carried by the note's own quantifier structure; no external channel is needed.
