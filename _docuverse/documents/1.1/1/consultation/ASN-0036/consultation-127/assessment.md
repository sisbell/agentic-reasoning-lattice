# Channel Assignment — ASN-0036 review-127

**Date:** 2026-05-28 23:01

## Issue 1: Two separate slots defer the same coalescing question downstream
Reason: Pure editorial deduplication — remove the redundant deferral pointer from the postcondition. The fix touches only this ASN's own prose; no design intent or implementation evidence is at stake.

## Issue 2: The depth-locking transition is stated three times
Reason: Editorial deduplication — keep the normative statement in contract postcondition (d), remove the two restatements. Derivable from the ASN's own structure; no external channel needed.

## Issue 3: Over-elaborated length bound in ShiftPreservation
Reason: Internal proof simplification — the step only needs `#a > 1`, which follows from S7c's `#E(a) ≥ 2` already present in the ASN. No design or implementation input required.

## Issue 4: Spurious S0 dependency on S7b
Reason: The fix is a precise restatement of what S0/S1 guarantee (address-persistence) versus the intrinsic, state-independent nature of `zeros(a) = 3` — both already defined within this ASN and ASN-0034's tumbler model. Derivable internally.

## Issue 5: Use-site inventory phrasing on Nat-pos
Reason: Editorial deletion of a meta-prose clause; the Nat-pos naming and its NAT-discrete derivation remain intact. No external channel needed.
