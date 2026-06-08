# Channel Assignment — ASN-0107 review-5

**Date:** 2026-06-07 22:07

## Issue 1: R1's case analysis silently assumes the deleted entry's I-address is consulted in only one slot
Reason: The fix is internal — the ASN already defines `W` as arbitrary subsets of `T` with no disjointness requirement, and the gap (a single `v ∈ Wᵢ ∩ Wⱼ` evicting `a` from two slots) is fully derivable from those definitions and the `sat`/`Qᵢ` machinery already present. Adding a single-slot precondition or extending the case split needs no design intent or implementation evidence.

## Issue 2: No weakest-precondition analysis; the change-laws give sufficient, not weakest, conditions
Reason: The fix is internal — a wp derivation for a postcondition like "a counted link remains discoverable across `K.μ⁻`" follows mechanically from the `sat`, `Qᵢ(Σ)`, and contraction definitions already in the ASN (and the R1/R3 reasoning); minimality is argued within the same algebra, requiring neither design intent nor code evidence.

## Issue 3: R1's "floor" claim contradicts its own bound and R3
Reason: Purely an internal wording inconsistency — R1's own `Δnum_disc ∈ {−1,0}`, R3's `Δ = 0`, and R2's `Δ = −k` are all present in the ASN, so correcting "floor" to "minimal non-trivial single-link decrement" is derivable without any channel.
