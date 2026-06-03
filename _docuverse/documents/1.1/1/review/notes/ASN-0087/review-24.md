# Review of ASN-0087

I read the ASN in full and checked the composite decomposition, the precondition derivations, the freshness arguments, the L1c chain construction, the per-state / boundary / transition invariant verifications, the wp analysis, the reflexive and atomicity treatments, and the worked example.

## Verification notes

**Composite structure (M-Comp).** Ordering K.λ ; K.μ⁺_L is correctly forced by K.μ⁺_L's `ℓ ∈ dom(L)` precondition. K.μ⁺_L is in ValidComposite★'s atomic vocabulary; J0/J1★/J1'★ are discharged separately and correctly (J0, J1'★ by empty quantification universes under the `C`/`R` frames; J1★ by the structural `subspace(v_ℓ) = s_L ≠ s_C` filter).

**L1c chain.** Reconstructed the chain `(d, b_C(d), b_L(d), t₁^L(d), …, ℓ)` step-by-step: TA5(d)/TA5(c) component effects, zero-count bookkeeping, and both TA5a admissibility bounds (saturating at `zeros(d)=2≤2` for the `k=2` step and `zeros(b_L(d))=3≤3` for the `k=1` step) all check. `k₁=2` and `#tᵢ > #d` hold throughout. The uniqueness strengthening is correctly flagged non-load-bearing and its exclusion table is sound.

**Freshness.** The three-layer argument (within-chain via ChainEnumerationInjectivity, cross-subspace via DisjointSubAllocatorChains, cross-document via Cross-doc disjointness + T10) is complete. The S2 discharge correctly splits into within-subspace (D-SEQ★) and cross-subspace (`(v_ℓ)₁=s_L≠s_C` by SC-NEQ) exclusions rather than the weaker `v_ℓ ∉ V_{s_L}(d)`.

**Depth convention (M-DepthConv).** Honestly scoped as a normative convention, not a substrate invariant; the general `m_L(d)` reading is correctly retained downstream and the scoped universal avoids overreach.

**Worked example.** Verified tumbler component sequences, prefix tests (`a₁ ⋠ ℓ` at position 7, `a₁ ⋠ a₂` at position 8), and both discoverability/symmetry/reflexive computations independently — all correct.

**wp / boundary cases.** The total-correctness framing matches LP12a's `enabled(op) ∧ …` convention; the membership-clause vs enabledness distinction is handled correctly for both `d_target = d` and `d_target ≠ d`; the standard-authoring collapse is sound. Empty endsets, first-link (`V_{s_L}(d)=∅`), subsequent-link, empty-arrangement, and reflexive cases are all covered.

**Cross-reference check (standard 7).** Every ASN cited (0034, 0036, 0043, 0047, 0093, 0098) is on the foundation list, so the references are permitted. No reinvented notation.

I found no hand-waved proofs, no missing edge cases, no unaddressed invariant conjuncts, and no correctness errors. The non-trivial wp case, concrete example verification, and derived consequences (discoverability symmetry, prior-link side effects, cascade, atomicity intermediate state) are all present and rigorous.

## OUT_OF_SCOPE

### Topic 1: Movement of a link's V-position within the home document's link subspace
**Why out of scope**: The Permanence section establishes K.μ~ fixes link V-positions pointwise and only K.μ⁻ can remove `v_ℓ`; richer movement semantics belong to a future arrangement-operations ASN, as the ASN's own Open Questions note.

### Topic 2: Protocol-layer composite atomicity
**Why out of scope**: M-CompAtomicity correctly localizes the guarantee above the substrate; the enforcing mechanism is a protocol-layer concern, not a strand-model claim.

VERDICT: CONVERGED
