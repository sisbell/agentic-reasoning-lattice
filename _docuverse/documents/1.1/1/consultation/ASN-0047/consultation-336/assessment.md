# Channel Assignment — ASN-0047 review-336

**Date:** 2026-06-02 06:09

## Issue 1: S8★ for K.μ~ is deferred to a section that does not establish it
Reason: The fix is purely internal — redirect the two S8★ deferral pointers to the inherited K.μ⁺/K.μ⁻ matrix columns (where the s_C-via-ASN-0036-S8 and s_L-via-length-1 arguments actually live), or add an explicit step; no design intent or implementation evidence bears on where a proof result is located.

## Issue 2: Meta-labeling and "needs no proof" prose in the K.μ~ realisation steps
Reason: Pure prose restructuring — collapse the "claim/half" scaffolding into the two-direction case split already present and drop the disclaimer; the underlying argument is unchanged and entirely internal.

## Issue 3: Use-site inventory prose at ChildSpawnFreshness and FrontierEquivalence
Reason: Editorial removal of a consumer-inventory sentence from a lemma's intro; the lemma statement and proof are self-contained and the cleanup needs no external input.
