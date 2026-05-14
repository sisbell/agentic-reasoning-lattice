# Channel Assignment — ASN-0058 review-13

**Date:** 2026-05-13 17:59

## Issue 1: M14's general claim is asserted without proof
Reason: Fix is internal — case-split on overlap forms (a₁ < a₂ < a₁ + n₁ and a₂ < a₁ < a₂ + n₂) and apply M7's I-adjacency requirement a₂ = a₁ + n₁ using TA-strict from ASN-0034. All machinery is already present in the ASN.

## Issue 2: M16's prefix-position bound is implicit
Reason: Fix is internal — derivation uses S7b (zeros(a) = 3) and S7c (#E(a) ≥ 2) from ASN-0036, both already part of the lattice context this ASN builds on. The position calculation #(N.0.U.0.D) = #a − #E(a) ≤ #a − 2 is mechanical from those citations.

## Issue 3: M12 elides subspace/depth reasoning in the contiguity argument
Reason: Fix is internal — subspace inheritance via OrdShiftHom (ASN-0034) and depth-m enumeration via S8-depth (ASN-0036) are already cited in the surrounding proof. Spelling out the three skipped steps is bookkeeping over existing properties.

## Issue 4: M12's elimination of v' < v + n is similarly opaque
Reason: Fix is internal — the missing arithmetic chain v + n = v' + j ⟹ v + n − 1 = v' + (j − 1) ∈ V(β') is a direct application of M-aux, which is defined in this very ASN.

## Issue 5: M5(b)'s "functionality" clause is redundant and misleading
Reason: Fix is internal — purely editorial. V-extent disjointness alone forces pair-set disjointness because pairs differ at the first component; the functionality clause adds nothing and should be deleted.
