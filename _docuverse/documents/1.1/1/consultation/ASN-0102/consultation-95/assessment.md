# Channel Assignment — ASN-0102 review-95

**Date:** 2026-06-08 04:42

## Issue 1: X2 recites K.α's allocation mechanism instead of advancing the corollary
Reason: Internal — the fix only trims prose to the load-bearing step (`D_d` unchanged via X1+X6 ⟹ same K.α handle), both already present in the ASN. No design intent or implementation evidence is needed to drop the per-case emission recitation.

## Issue 2: X14's mid-composite coupling prose explains the composite framework rather than COPY's effect
Reason: Internal — (SL) and the `Σ_0`-residency split are already stated in X14; the fix removes narration about hypothetical enclosing-composite steps. The boundary between COPY's effect and ValidComposite★'s obligation is fixed by ASN-0047, already cited.

## Issue 3: the `Σ_0`-residency / A-membership split is re-stated three times
Reason: Internal — pure deduplication. The range partition (post-state `s_C`-range = pre-state range ∪ `A`) and its two discharge mechanisms (SL, P4★+P2) are all present; factoring into one lemma and citing it requires no external input.
