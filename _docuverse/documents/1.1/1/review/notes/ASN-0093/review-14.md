# Review of ASN-0093

## REVISE

### Issue 1: FirstEmissionFreshness proof cites L0 for E(a)₁ = s_C
**ASN-0093, FirstEmissionFreshness lemma proof, "Against dom(L)" paragraph**: "By L0, E(ℓ)₁ = s_L and E(a)₁ = s_C"
**Problem**: L0 at the pre-state Σ supplies E(ℓ)₁ = s_L for ℓ ∈ dom(L(Σ)) via its L-clause. It cannot supply E(a)₁ = s_C because a is not in dom(C(Σ)) at the K.α event firing the first-emit predicate — the K.α event is about to commit a but has not yet done so. Using L0 at Σ' would be circular (L0 at Σ' is itself proved in the discharge matrix using FirstEmissionFreshness to discharge the K.α precondition). The conclusion E(a)₁ = s_C is sound, but its source is the structural form a = [d.0.s_C.1] (SubAllocatorAxiom.FirstEmission), not L0.
**Required**: Split the citation: "by L0 at Σ, E(ℓ)₁ = s_L; by SubAllocatorAxiom.FirstEmission's structural form a = [d.0.s_C.1], E(a)₁ = s_C by inspection".

### Issue 2: K.α/K.λ subsequent-emit cross-subspace freshness has the same citation issue
**ASN-0093, K.α subsequent-emit precondition discharge "Freshness against dom(L)" paragraph (and symmetrically in K.λ)**: "L0 supplies E(a)₁ = s_C ≠ s_L = E(ℓ)₁ (SC-NEQ)"
**Problem**: Parallel to Issue 1, but in the subsequent-emit context. For the new key a (resp. ℓ in the K.λ case), L0 at Σ does not apply because the address is not yet committed to its store. The correct source for the new key's subspace identifier is DisjointSubAllocatorChains: a = inc(a_prev, 0) ∈ A_C(d) by ChainDiscipline's closure (with a_prev ∈ A_C(d) by ChainMembershipForOrigin at Σ), and every element of A_C(d) has E(·)₁ = s_C by DisjointSubAllocatorChains. The pre-existing peer's subspace identifier remains L0 at Σ.
**Required**: In both subsequent-emit derivations, split the citation to distinguish the new key (whose subspace identifier comes from DisjointSubAllocatorChains applied to the relevant sub-allocator chain) from the pre-existing peer (whose subspace identifier comes from L0 at Σ).

### Issue 3: L14 invariant declaration omits StoreT4Validity from the derivation list
**ASN-0093, L14 (StoreDisjointness) invariant declaration**: "Derived from L0 + SC-NEQ + T7 (FirstElementFieldDistinction, ASN-0034)"
**Problem**: T7's preconditions (per ASN-0034) require T4-validity of both compared addresses. The substrate's L14 derivation chain therefore depends on StoreT4Validity (a derived lemma stated later in the ASN) to discharge T7's T4-validity preconditions for the pair (a ∈ dom(C), ℓ ∈ dom(L)). The discharge matrix's L14 entry under K.α correctly invokes StoreT4Validity, but the invariant declaration's brief derivation list omits this dependency.
**Required**: Amend the derivation list to read "Derived from L0 + SC-NEQ + StoreT4Validity + T7 (FirstElementFieldDistinction, ASN-0034)".

### Issue 4: Cross-document disjointness Case B sub-case relationship description is incorrect
**ASN-0093, Cross-document disjointness chain Case B paragraph**: "Sub-cases B.i and B.ii are *exhaustive but not mutually exclusive*: B.i covers #d_1 < #d_2 and #d_1 = #d_2, B.ii covers #d_2 < #d_1, and at equality both B.i and the mirror reading of B.ii fire symmetrically"
**Problem**: B.i (hypothesis #d_1 ≤ #d_2) and B.ii (hypothesis #d_2 < #d_1) are mutually exclusive (≤ and > are disjoint relations on ℕ) and exhaustive (their union covers NAT-order's trichotomy). At equality, only B.i fires; B.ii's strict #d_2 < #d_1 fails. The reference to "the mirror reading of B.ii fire[ing] symmetrically" at equality is misleading: the mirror reading is an alternative proof structure (extracting the witness from d_2 ⋠ d_1 instead of d_1 ⋠ d_2), not a separate sub-case being triggered.
**Required**: Rephrase to: "Sub-cases B.i and B.ii are exhaustive and mutually exclusive, partitioning NAT-order's trichotomy. At equality, only B.i fires; the proof's witness extraction may equivalently proceed from d_2 ⋠ d_1 (a mirror argument) rather than d_1 ⋠ d_2, since at equality both ⋠ conjuncts admit component witnesses at indices within min(#d_1, #d_2)."

### Issue 5: Chain Definition's infinity commitment does not explicitly cite its foundation dependency
**ASN-0093, Definition (T10a-discipline-satisfying chain)**: "A *T10a-discipline-satisfying chain* is an *infinite* sequence (t_1, t_2, t_3, …) of tumblers — indexed by every n ∈ ℕ with n ≥ 1 — satisfying two structural conditions"
**Problem**: The Definition asserts the existence of an infinite sequence in T. The well-formedness of this assertion requires inc(t, 0) ∈ T whenever t ∈ T — i.e., TA5's "Postconditions: t' ∈ T" applied at k = 0, which is a load-bearing foundation fact for the recurrence to be well-defined for every n ≥ 1. The Definition does not cite TA5 (or any other foundation claim) as the warrant for this well-formedness, leaving the reader to infer it. The substrate elsewhere cites TA5 thoroughly, so the gap is recoverable, but a brief justification at the Definition itself would close the inferential step.
**Required**: Add a short clause to the Definition citing TA5 (HierarchicalIncrement, ASN-0034) — specifically that TA5's postcondition `t' ∈ T` at every step k = 0 underwrites the well-formedness of the infinite recurrence.

VERDICT: REVISE
