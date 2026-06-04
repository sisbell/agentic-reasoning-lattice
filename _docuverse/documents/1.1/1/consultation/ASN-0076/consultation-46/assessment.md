# Channel Assignment — ASN-0076 review-46

**Date:** 2026-06-03 23:48

## Issue 1: E11 depends on E10 but is stated before it
Reason: Pure document-ordering fix — reorder the E8/E9/E10 block ahead of E11, or inline E10's frame fact at point of use. This is structural editing derivable from the ASN's own content; no design intent or implementation evidence is at stake.

## Issue 2: E2 carries defensive prose justifying machinery the proof does not use
Reason: Pure deletion of meta-commentary; the member/non-member argument already present in E2 stands alone. No external channel needed.

## Issue 3: E11's `ℓ_new`-branch vacuity is asserted with an informal "unspawned frontier" notion, not derived
Reason: The replacement derivation is to be assembled from foundation results the review already names — SubAllocatorBundle's `#E = 2` uniformity (ASN-0047) and LP-Sub / `F`-structure (ASN-0098), both already in the spec. The conclusion that no element of `dom(Σ.L)` properly extends `ℓ_new` follows from these cited invariants, so the fix is internal to the existing foundation.
