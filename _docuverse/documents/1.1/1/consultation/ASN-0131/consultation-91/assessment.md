# Channel Assignment — ASN-0131 review-91

**Date:** 2026-06-14 18:41

## Issue 1: Retraction-permanence re-derives ASN-0086's R6a instead of citing it
Reason: Internal fix. R6a (ASN-0086) is an already-cited dependency whose one-step monotonicity is exactly what the frame-by-frame walk-through reconstructs; replacing it with "R6a + induction" is pure redundancy removal, derivable from the citation the ASN already makes.

## Issue 2: Redundant per-transition expansion in the "three further kinds" stability paragraph
Reason: Internal fix. The complete argument (RE-LOC makes `Σ.M(d)` and `Σ.L` the only things `RE` reads, both fixed by the frame) is already stated in the paragraph's opening sentence; dropping the per-transition K.α/K.ρ re-dispatch is derivable from RE-LOC, present in this ASN.

## Issue 3: Belt-and-suspenders citation of the link prefix-antichain
Reason: Internal fix. Citation cleanup only — the reviewer already designates R0a (ASN-0086) as the citation to keep and the redundant alternative groundings to drop; the antichain fact itself is unchanged, so no design intent or implementation evidence is in question.

## Issue 4: Unneeded exhaustiveness claim in the link-subspace-confined paragraph
Reason: Internal fix. The fix deletes a surplus "are exactly" exhaustiveness claim; the two positive results (`K.μ⁺_L` and link-only `K.μ⁻` leave the answer fixed) stand independently of it, so the deletion needs nothing beyond the ASN's own content.
