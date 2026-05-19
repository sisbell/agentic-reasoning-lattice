# Channel Assignment — ASN-0093 review-14

**Date:** 2026-05-18 21:12

## Issue 1: FirstEmissionFreshness proof cites L0 for E(a)₁ = s_C
Reason: The correct source (SubAllocatorAxiom.FirstEmission's structural form `a = [d.0.s_C.1]`) is already established within the ASN; the fix is a citation split between the new key (FirstEmission) and the pre-existing peer (L0 at Σ). No design intent or implementation evidence is required.

## Issue 2: K.α/K.λ subsequent-emit cross-subspace freshness has the same citation issue
Reason: The fix substitutes DisjointSubAllocatorChains + ChainMembershipForOrigin + ChainDiscipline (all established in the ASN) for the new key's subspace identifier, while retaining L0 at Σ for the pre-existing peer. The substitution machinery is entirely internal to the ASN.

## Issue 3: L14 invariant declaration omits StoreT4Validity from the derivation list
Reason: StoreT4Validity is already a derived lemma in the ASN and the discharge matrix's L14 entry already invokes it correctly; the fix is a textual amendment to align the invariant declaration with the matrix.

## Issue 4: Cross-document disjointness Case B sub-case relationship description is incorrect
Reason: The fix is a logical exposition correction grounded in NAT-order's trichotomy (≤ and > partition ℕ², with equality falling into B.i alone). The trichotomy is foundation-level (already cited via NAT-order in ASN-0034) and the proof structure is internal.

## Issue 5: Chain Definition's infinity commitment does not explicitly cite its foundation dependency
Reason: TA5's postcondition `t' ∈ T` is foundation content from ASN-0034, already cited extensively throughout the ASN; the fix is a brief citation addition at the Definition to make the well-formedness warrant explicit.
