# Channel Assignment — ASN-0043 review-58

**Date:** 2026-05-14 14:17

## Issue 1: L1a + L12 jointly require home documents to persist; consequence not derived
Reason: Pure derivation from existing invariants (L1a instantiated at Σ' plus L12). No design intent or implementation evidence required — the consequence falls out of two ASN-internal properties.

## Issue 2: L1c formal statement leaves k_i as unbound free variables
Reason: Notational fix — extend the existential binder to include `k₁, ..., kₙ`. Purely a formal-logic correction internal to the ASN.

## Issue 3: L1c uses "T10a-admissible at tᵢ₋₁" without formal definition
Reason: Definition derives from ASN-0034's T10a/TA5a contract (cases on `kᵢ ∈ {0, 1, 2}`, TA5a zeros bound, per-parent uniqueness). All ingredients already exist in the foundation ASN; no external input needed.

## Issue 4: L9 proof attributes S2 preservation to wrong invariant component
Reason: Attribution slip — S2 is an arrangement invariant, preserved by `Σ'.M = Σ.M`. Internal correction; the right reason is already cited elsewhere in the same proof for S8a/D-CTG.

## Issue 5: L10 cites "transitivity of ≼" from PrefixRelation, but PrefixRelation does not export transitivity
Reason: Citation precision — transitivity of `≼` is derivable from PrefixRelation's definition plus NAT-order's `≤`-transitivity (both in ASN-0034). Fix is a one-line inline derivation; no channel needed.
