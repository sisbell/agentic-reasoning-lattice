# Channel Assignment — ASN-0069 review-94

**Date:** 2026-06-03 02:04

## Issue 1: Internal inconsistency about when the version sub-allocator activates
Reason: The fix is internal — the ASN already establishes (via SubAllocatorBundle and the fork-composite sub-case A discharge) that `A_v(d_src)`'s base `inc(d_src, 1)` is emitted only by the first fork, so the §"Independence Among Forks" prose is simply the inconsistent statement to correct. No design intent or implementation evidence is needed.

## Issue 2: Forward use-site inventory of the B-Seq bridge discharge
Reason: Pure editorial deletion of a forward-reference clause; derivable from the ASN alone.

## Issue 3: Duplicate B-Seq bridge citation within §"Independence Among Forks"
Reason: Pure editorial de-duplication, retaining V10(a) as the sole carrier; derivable from the ASN alone.
