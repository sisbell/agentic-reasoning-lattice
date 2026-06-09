# Channel Assignment — ASN-0116 review-17

**Date:** 2026-06-09 07:40

## Issue 1: P7a proof relies on an unstated precondition
Reason: Internal — ExtendedReachableStateInvariants (ASN-0047) already defines P7a as a composite-boundary property, so the fix is to add "Σ is a composite boundary" to INSERT's precondition (the natural input for a composite). No design intent or implementation evidence is needed.

## Issue 2: P6 range identity omits the cross-subspace contribution
Reason: Internal — F-SUB is already established in the ASN; the fix is purely to cite it in the P6 derivation so the full-range identity is complete.

## Issue 3: Repeated non-inheritance meta-prose (anti-bloat)
Reason: Internal — editorial trimming of redundant why-not-inherit narrative, keeping the direct S3★-by-S3+P2 discharge. No external input required.

## Issue 4: Range identity derived twice (anti-bloat)
Reason: Internal — structural hoisting of a single named range-identity fact cited from both PROV and P6, parallel to the prior block-disjointness hoist. Derivable from the ASN's existing Effect clauses.
