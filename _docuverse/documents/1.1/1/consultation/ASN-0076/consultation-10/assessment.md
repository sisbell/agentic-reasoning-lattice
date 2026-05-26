# Channel Assignment — ASN-0076 review-10

**Date:** 2026-05-25 21:23

## Issue 1: L12 mis-classified as per-state invariant
Reason: Fix is internal — the review identifies the exact correction (cite L12 via ExtendedTransitionInvariants/P3 rather than ExtendedReachableStateInvariants), and the classification is established by reading ASN-0047's invariant taxonomy directly.

## Issue 2: S0/S1 mis-classified in "S-invariants S0–S3★"
Reason: Fix is internal — the review specifies both correction options (narrow the range to S2 onward, or split S0/S1 into P0 inheritance), and the classification is settled by ASN-0036 and ASN-0047's existing invariant placements.

## Issue 3: Implicit step in content-disjointness discharge
Reason: Fix is internal — the review provides two complete alternative proof chains using only foundation already cited in this ASN (L0, L14, SC-NEQ, SubAllocatorAxiom.Subspace, K.α/P6). Option (b) is the cleaner subspace argument and is fully derivable from the existing foundation.
