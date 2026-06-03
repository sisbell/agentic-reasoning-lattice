# Channel Assignment — ASN-0101 review-27

**Date:** 2026-06-03 16:18

## Issue 1: History-length argument mixes atomic and named-operation counting conventions
Reason: The fix is a consistency repair derivable from the ASN itself: the review already quotes ASN-0047's definition of K.μ~ as a non-atomic named composite (K.μ⁻ + K.μ⁺), so choosing a single counting convention and revising the "differ by one" claims requires no design-intent or implementation evidence.

## Issue 2: D8 discharge of S8★ does not establish condition (c) on the content subspace
Reason: The fix is internal — the ASN already establishes S2 (functionality) and S8-fin (finiteness) for the post-state, and M12 (CanonicalUniqueness, already in the foundation) yields the unique maximal-run decomposition; the proof need only invoke it explicitly.
