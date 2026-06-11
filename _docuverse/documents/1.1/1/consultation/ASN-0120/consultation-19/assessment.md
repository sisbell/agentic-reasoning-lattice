# Channel Assignment — ASN-0120 review-19

**Date:** 2026-06-11 04:49

## Issue 1: `shift(·, 0)` is used without being defined, and the merge induction's base case invokes TS3 outside its precondition
Reason: The fix is purely formal bookkeeping internal to the ASN — adopt the `shift(t, 0) := t` convention already used by ASN-0036/ASN-0058 and split out the trivial `k = 1` base case so TS3 is only invoked for `k ≥ 2`. Neither design intent nor implementation behavior bears on a notational convention and an induction restructuring.

## Issue 2: the store-trace consequence of the recovery equation is established in ML1 and then re-derived or restated twice in ML9
Reason: This is an accretion/deduplication issue — the derivations are correct and already present in ML1; the fix is editorial, replacing the repeated derivations in ML9 Fact (a) and the closing paragraph with citations to ML1's established results. No external consultation can change how internal cross-referencing is organized.
