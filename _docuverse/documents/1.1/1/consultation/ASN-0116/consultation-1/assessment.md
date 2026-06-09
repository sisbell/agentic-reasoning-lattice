# Channel Assignment — ASN-0116 review-1

**Date:** 2026-06-08 17:03

## Issue 1: Insertion depth `m` is undefined when the target subspace is empty
Reason: Derivable internally — the fix (`m := #p`, require `#p ≥ 2`, match existing common depth when non-empty) follows from the already-cited foundation ValidFirstInsertionPosition and S8a, plus the ASN's own notation. No external intent or evidence is needed; the depth is pinned by the supplied position.

## Issue 2: P4 (LinkSurvival) rests on a false premise and omits resurrection
Reason: Derivable internally — the review already cites the governing foundation claims (L4 EndsetGenerality, L9 TypeGhostPermission, ASN-0098 LP18 resurrection, and endset immutability). Re-deriving coverage-invariance from immutability and extending P4 for `coverage(e) ∩ A_new ≠ ∅` is a composition of those cited results.

## Issue 3: Arrangement-layer effects and allocation reinvent foundation claims
Reason: Derivable internally — the review identifies the exact foundation transitions to compose (K.α, the I3 family, ValidInsertionPosition). The fix is citation and composition, not new intent or evidence.

## Issue 4: No concrete worked example
Reason: Derivable internally — the worked example only instantiates the ASN's own definitions (P0, P1, I-DOM, I-NEW) against a chosen state; no external input required.

## Issue 5: No weakest-precondition / derived-consequence analysis
Reason: Derivable internally — the wp computation (e.g. discoverability preservation requiring `coverage(e) ∩ A_new = ∅`) follows mechanically from the operation's own postconditions and the foundation claims already in scope from Issue 2.
