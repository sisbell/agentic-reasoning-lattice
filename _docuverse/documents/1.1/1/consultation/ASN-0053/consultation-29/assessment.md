# Channel Assignment — ASN-0053 review-29

**Date:** 2026-05-28 19:27

## Issue 1: S9 case analysis drops the (start=, reach=) residual
Reason: Internal fix. The required closure uses TA-LC (left cancellation), already cited in this ASN, to show shared start and reach force equal width — so the residual case is vacuous. No external evidence or design intent needed.

## Issue 2: S8 construction references the current interval before it is initialized
Reason: Internal fix. Moving the initialization `[s, r) = [start(σ₁), reach(σ₁))` from the invariant clause into the construction body is a structural edit using only material already present in the proof.

## Issue 3: Use-site inventory of D1 (forward-reference accretion)
Reason: Internal fix. The required action is simply deleting a redundant pre-announcement sentence; the point is already established by the surrounding D1/D2 discussion. No channel input needed.

## Issue 4: D1 round-trip and the #a>#b failure each stated twice (redundancy)
Reason: Internal fix. Consolidating duplicated statements of the D0/D1 dichotomy is an editorial dedup using only facts already cited from ASN-0034. No channel input needed.
