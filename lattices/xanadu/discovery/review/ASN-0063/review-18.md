# Review of ASN-0063

## REVISE

### Issue 1: K.α needs a content-subspace amendment for the extended state

**ASN-0063, Extending the Transition Framework / ExtendedReachableStateInvariants**: "All existing elementary transitions from ASN-0047 hold L in their frame: L' = L." and "For K.α, K.δ, K.ρ: hold both M and L in frame; ... link invariants preserved since L is unchanged."

**Problem**: K.α (ContentAllocation, ASN-0047) has precondition `IsElement(a) ∧ origin(a) ∈ E_doc` — no subspace constraint. In the extended state, L0 (SubspacePartition) requires `(A a ∈ dom(Σ.C) :: fields(a).E₁ = s_C)`. K.α adds `a` to `dom(C')`, so L0 clause 2 requires `fields(a).E₁ = s_C`. This is not in K.α's precondition and is not verified in the proof.

The downstream consequence: without `fields(a).E₁ = s_C`, K.α could allocate an address with subspace `s_L`, placing it in `dom(C')`. This violates L0 (clause 2: content addresses must have content subspace) and L14 (disjointness: `dom(C') ∩ dom(L')` could become non-empty, since the address might also appear in `dom(L)` or future link allocations share the same subspace prefix).

The proof says "link invariants preserved since L is unchanged," but L0 clause 2 constrains `dom(C)`, not `dom(L)`. K.α modifies `dom(C)`. "L unchanged" handles L0 clause 1 and L12 but not L0 clause 2 or the derived disjointness.

K.λ already has `fields(ℓ).E₁ = s_L` in its precondition. The parallel constraint is missing from K.α.

**Required**: Amend K.α for the extended state with `fields(a).E₁ = s_C`, parallel to K.λ's `fields(ℓ).E₁ = s_L`. Add it to the Properties Introduced table as an amendment. In the ExtendedReachableStateInvariants proof, verify L0 clause 2 and L14 explicitly for K.α: `fields(a).E₁ = s_C` gives `a ∉ dom(L)` (since L0 clause 1 at the pre-state ensures all `dom(L)` addresses have subspace `s_L ≠ s_C`), so `dom(C') ∩ dom(L') = ∅`.

## OUT_OF_SCOPE

### Topic 1: Link withdrawal invariants
**Why out of scope**: The ASN identifies the tension between K.μ⁻ on link-subspace positions and D-CTG (only the maximum can be removed), and notes that Nelson's design suggests an inactive-status mechanism rather than arrangement removal. This is a new operation definition, not an error in CREATELINK.

### Topic 2: Link inheritance under forking
**Why out of scope**: The ASN explicitly notes that copying link-subspace mappings during fork "would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope." This is a design decision for a future ASN on version semantics.

### Topic 3: Discovery function efficiency and index structure
**Why out of scope**: The ASN correctly separates the abstract specification (disc is a derived function on L) from the implementation concern (maintaining an index for sub-linear evaluation). The abstract properties CL7–CL9 are stated and proven.

### Topic 4: Concurrency of link allocation
**Why out of scope**: Listed in open questions. The current framework is sequential; concurrent allocation semantics belong to a replication or concurrency ASN.

VERDICT: REVISE
