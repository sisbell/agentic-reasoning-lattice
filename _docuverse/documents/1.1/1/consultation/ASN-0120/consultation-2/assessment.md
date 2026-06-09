# Channel Assignment — ASN-0120 review-2

**Date:** 2026-06-08 22:57

## Issue 1: `ρ(R, Σ) ⊆ dom(Σ.C)` is justified by the wrong referential-integrity invariant
Reason: Internal fix. The correction is to cite S3★ (already in the ASN-0047 substrate the ASN builds on) and either add a content-subspace precondition or widen the containment to `dom(Σ.C) ∪ dom(Σ.L)` — a formal bookkeeping choice fully determined by the cited foundation invariants and the ASN's own framing of endsets as content-region specs.

## Issue 2: Fact (a) of the ML9 derivation asserts a false universal about arrangement ranges
Reason: Internal fix. Replacing the S3 citation with S3★ and inserting the subspace-disjointness step (`s_C ≠ s_L`, already fixed in the substrate) is mechanical; both the corrected invariant and the disjointness fact are present in the ASN's cited material.

## Issue 3: The ML9 weakest precondition omits the operation's enabledness conjunct
Reason: Internal fix. The needed `enabled` conjunct unfolds to conditions already established in the ASN (ML6's `ρ(R₃,Σ) ≠ ∅`, ML0's `d ∈ dom(Σ.M)`), and the pattern is given by the cited ASN-0098 LP12a; no design intent or implementation evidence is required.
