# Channel Assignment — ASN-0086 review-242

**Date:** 2026-06-01 21:42

## Issue 1: Nullify Rationale carries an implementation-mechanics walkthrough in a spec-rationale slot
Reason: The abstract authority argument (Nelson's ownership scoping, ownership-at-Σ vs. ownership-at-commit) is already fully written into the Rationale, and the review explicitly states it suffices to justify both P-tgt branches. The fix is to retain that existing argument and relocate the udanax-green prose; no new design-intent or implementation evidence is required.

## Issue 2: R0 proof narrates the foundation lemma's internal proof structure
Reason: Purely editorial — drop the description of FirstEmissionFreshness/SubsequentEmissionFreshness's internal case split and cite only their conclusions. The conclusions are already invoked in the R0 proof; nothing external is needed.

## Issue 3: WP Case 1 re-derives R-Scope's scope conclusion rather than citing it
Reason: R-Scope (SingleTupleScope) is established within the ASN for exactly the P1 and self-emit branches, so the fix is to cite it and keep only the non-redundancy/weakestness argument. Fully derivable from the note's own content.
