# Channel Assignment — ASN-0116 review-5

**Date:** 2026-06-08 20:55

## Issue 1: I-NEW gap-attribution case split is per-`J` but the obligation is per-block-position
Reason: The fix is internal — it reworks how the absence of block positions is attributed between two already-cited foundation lemmas (I3-V's `v ∈ dom(M(d))` quantifier vs I3-CS domain closure), and the review itself supplies the corrected per-block-position split and its soundness argument. No design intent or implementation evidence is in question; everything needed is in the ASN's own Effect clause and ASN-0082's lemma statements.
