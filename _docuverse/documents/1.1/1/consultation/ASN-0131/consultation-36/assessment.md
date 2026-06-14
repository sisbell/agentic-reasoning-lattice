# Channel Assignment — ASN-0131 review-36

**Date:** 2026-06-13 22:07

## Issue 1: "both gains and loses" overstates the image's response to a shift
Reason: Neither channel — the fix re-characterizes how ASN-0082's displacement primitives move the forward image using I3/I3-V (PostInsertionShift) and D-SHIFT semantics the ASN already cites and restates (including its own note that the insert gap is vacated under the primitive, a separate content-placing step). Correcting the monotonicity granularity (shift family non-monotone as a class), the insert mechanism (vacated gap vs. above-gap recipients), and the optional LP19a gloss is mathematical reasoning over material already in hand.

## Issue 2: defensive meta-prose around the `Θ` disjointness hypothesis (anti-bloat)
Reason: Neither channel — the operative fact (`coverage(Θ) ∩ dom(Σ.C) = ∅` is a construction hypothesis, not a theorem, since `Θ`'s spans may be wide and a wide span's coverage can reach content past its start) is already correct in the text, so the fix is editorial: strip the reviser-drift framing and the rebuttal of an absent prior phrasing, and drop the redundant R0a citation since R-Scope's `{t : ℓ ≼ t} ∩ A_rel^{Σ'} = {ℓ}` alone confines the nullification.
