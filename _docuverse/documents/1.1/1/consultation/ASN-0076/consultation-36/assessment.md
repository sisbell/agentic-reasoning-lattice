# Channel Assignment — ASN-0076 review-36

**Date:** 2026-06-03 22:38

## Issue 1: E0's composite precondition omits the reachability hypothesis the proof depends on
Reason: Derivable from the ASN alone — E5 already carries the exact "outer hypothesis" (Σ reachable in ASN-0047's extended reachable state) that E0 must adopt, and ExtendedReachableStateInvariants is already cited in-text. The fix is to import E5's existing hypothesis into E0's precondition; no external evidence or intent needed.

## Issue 2: τ_sup paragraph is deferral meta-prose
Reason: Internal editorial reduction. The single operative fact (`τ_sup ∈ T` ⇒ span well-formed by T12 via T0) is already stated and re-proved within the ASN, and the deferred convention is already listed in Open Questions, so the cut requires no channel.

## Issue 3: E7's discoverability caveat is stated three times
Reason: Internal de-duplication. The substantive LP17/LP18 + E10 orphaning/resurrection derivation is already present in the ASN; collapsing the repeated "structural-witness, not discoverability" framing to one location is a prose edit derivable from the ASN's own content.

## Issue 4: E0's "First" ordering observation is design rationale, not reasoning
Reason: Derivable from the ASN alone — L4 (endset spans may reference any tumbler, including unallocated ones) is already a cited foundation item, which directly establishes that the "First" point is non-load-bearing convention while the "Second" adjacency point is what the `ℓ_sup = inc(ℓ_new, 0)` identification consumes.
