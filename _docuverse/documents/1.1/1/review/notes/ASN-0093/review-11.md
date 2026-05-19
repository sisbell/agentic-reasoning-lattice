# Review of ASN-0093

## REVISE

### Issue 1: L14 discharge matrix entries for K.α and K.λ elide per-transition specifics

**ASN-0093, "Discharge of stated invariants" matrix, L14 row**: "Holds at Σ' by direct derivation: L0(Σ') + SC-NEQ + StoreT4Validity(Σ') + T7. [...] All four premises hold at Σ' | Holds at Σ': same derivation | Holds at Σ': same derivation"

**Problem**: All three transition columns read "same derivation," but the substantive content differs. At K.σ, `dom(C)` and `dom(L)` are unchanged, so L14 transfers from IH on L14 at Σ via frame preservation — the direct-derivation route is unnecessary. At K.α, the new key `a` requires L0's C-clause discharged from precondition `E(a)₁ = s_C` and StoreT4Validity for `a` discharged from ChainElementT4Validity applied to A_C(d). At K.λ, symmetric. The matrix conflates frame preservation (K.σ) with new-key direct derivation (K.α, K.λ).

**Required**: Distinguish the K.σ entry (frame preservation alone suffices) from the K.α/K.λ entries (direct derivation needed for the new key, with explicit citation of which premise is discharged at the new key vs. inherited at prior keys).

### Issue 2: Cross-document disjointness Case A overstates witness route for `p₂ ⋠ p₁`

**ASN-0093, Cross-document disjointness chain (Case A)**: "Thus `p₁[k] = 0 ≠ p₂[k]` at an index within both anchors, witnessing `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` via the position-divergence clause of Prefix (ASN-0034)."

**Problem**: In Case A, `p₂ ⋠ p₁` has a more direct witness via length divergence (`#p₂ = #d₂ + 2 > #d₁ + 2 = #p₁`, which fails Prefix's length conjunct). The position-divergence route also works (since `k ≤ #p₁ ≤ #p₂`), but the proof's framing — citing only "position-divergence clause" without acknowledging the simpler length-divergence route — obscures that Case A admits two independent witnesses for `p₂ ⋠ p₁`. Additionally, Prefix (ASN-0034) does not define a named "position-divergence clause"; the term is informal shorthand for negation of the component conjunct.

**Required**: Either name the clause precisely ("the component-disagreement direction of Prefix's negation") or note that `p₂ ⋠ p₁` in Case A follows by length divergence directly, with position-divergence as an alternative.

### Issue 3: Inductive ordering of ChainPrefixExtension and ChainElementT4Validity needs an explicit dependency note

**ASN-0093, ChainPrefixExtension proof, step**: "By ChainElementT4Validity (corollary on sub-allocator chains), `t_n` is T4-valid — supplied as a standalone fact established by a prior chain induction, not by a nested induction inside the present proof."

**Problem**: The parenthetical "not by a nested induction" is the right disclaimer, but the proof does not explicitly state that ChainElementT4Validity must be proved *before* ChainPrefixExtension in the lemma ordering — the inductions are over the same index variable `n`, and a reader could plausibly worry about mutual dependency. The chain lemmas section presents the six lemmas in an order that happens to discharge dependencies correctly, but the ordering is not commented on as load-bearing.

**Required**: State explicitly that the chain lemmas are proved in dependency order (ChainElementT4Validity, ChainUniformLength, ChainEnumerationInjectivity, ChainUniformZeroCount, DisjointSubAllocatorChains, ChainPrefixExtension), so that each lemma's proof may cite the conclusions of all earlier lemmas as fully established at every chain index.

## OUT_OF_SCOPE

### Topic 1: Operations beyond K.σ/K.α/K.λ
**Why out of scope**: Arrangement mutation (K.μ family), link withdrawal/tombstoning, entity stratification (E_doc), provenance recording (K.ρ, Σ.R), and coupling constraints (J-family) are explicitly deferred to higher-layer ASNs per the Scope section.

### Topic 2: Hierarchical baptism discipline for K.σ
**Why out of scope**: K.σ admits address-space configurations broader than Nelson's hierarchical baptism; node-account-document chain enforcement is deferred to a higher-layer document-introduction primitive (per Open Questions).

### Topic 3: Concurrent operation discipline
**Why out of scope**: SequentialTransitionAxiom commits transitions to atomic and sequential ordering; concurrent emission across allocators is deferred (per Open Questions).

### Topic 4: Sub-allocator stratification beyond s_C and s_L
**Why out of scope**: SubspaceConventionAxiom commits to exactly two subspaces; future subspace identifiers `s ≥ 3` are noted in Open Questions for higher-layer extension.

VERDICT: REVISE
