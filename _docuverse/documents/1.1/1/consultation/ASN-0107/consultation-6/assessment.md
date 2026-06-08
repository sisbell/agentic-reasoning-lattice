# Channel Assignment — ASN-0107 review-6

**Date:** 2026-06-07 22:14

## Issue 1: Worked-example R2 attribution contradicts the link table
Reason: Internal. The contradiction is between the prose and the example's own table (`ℓ₃.e₁ = {a₁, a₂}`); the fix is restating "exactly `ℓ₁` and `ℓ₂`" as "`ℓ₁`, `ℓ₂`, `ℓ₃` reach `a₁`, but only `ℓ₁`, `ℓ₂` exclusively," which follows directly from the ASN's `sat` and coverage definitions.

## Issue 2: R2 defines `k` two incompatible ways
Reason: Internal. Reconciling the bound-vs-exact-drop readings of `k` is a definitional consistency fix derivable from R1–R3 and the worked instance already in the ASN; no external evidence or design intent is needed to pick one definition.

## Issue 3: A2 conflates discoverability (one-slot) with the count (three-slot conjunction)
Reason: Internal. The slippage is between the ASN's own conjunctive `sat`/P1 and the existential `discoverable_from` of LP16 (already cited from ASN-0098); the corrected claim — discoverability per slot vs. count requiring all three slots satisfied — is derivable from definitions present in or cited by the ASN.
