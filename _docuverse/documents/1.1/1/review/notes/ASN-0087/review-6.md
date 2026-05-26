# Review of ASN-0087

## REVISE

(none)

## OUT_OF_SCOPE

(none)

The ASN is unusually thorough for its size. Specifically:

- **Decomposition argument is sound**: K.λ ; K.μ⁺_L identified, ordering forced by K.μ⁺_L's `ℓ ∈ dom(L)` precondition, and the necessity of the K.μ⁺_L step (against L14a's supersession) is argued from Nelson's design intent rather than coupling J0/J1★/J1'★ (which are vacuous here).
- **Precondition derivations are complete**: The non-trivial reduction of K.μ⁺_L's intermediate-state precondition `ℓ ∉ ran(Σ_mid.M(d))` to original-state conditions via S3★ + S3★-aux + K.λ frame is fully derived.
- **Three-layer freshness argument** (within d's link chain via ChainEnumerationInjectivity; cross-subspace via DisjointSubAllocatorChains; cross-document via T10) discharges K.λ's freshness precondition by construction.
- **L1c chain construction is explicit**: The structurally-forced chain `d → b_C(d) → b_L(d) → t_1^L(d) → … → ℓ` is tabulated with k-values, TA5a admissibility bounds, post-step zero counts, and T4-validity at every intermediate. Verified against TA5(c)/(d) and K.δ-ID.zeros-0/1 / K.δ-ID.zeros-2 from foundation ASN-0047.
- **Worked example** (d = [1,0,1,0,1], d' = [1,0,1,0,2], concrete a₁/a₂/a₃/ℓ tumblers) verifies discoverability checks down to position-by-position prefix testing.
- **Weakest precondition** for `discoverable_from(ℓ, d_target, ·)` is computed for both `d_target = d` and `d_target ≠ d`, including the reflexive-endset branch and the standard-authoring collapse.
- **Reflexive endsets** treated carefully: home-document privilege under reflexive coverage is structural (placement of v_ℓ), not semantic (LP12 remains symmetric), and the case is excluded by K.λ freshness under standard authoring.
- **Side effects on prior links** characterized via LP9 specialization, with the side-effect window correctly confined to the home document (frame on M for d' ≠ d).
- **Invariant preservation** stratified into per-state / composite-boundary / transition classes per ASN-0047's classification, with each invariant discharged by specific premise (precondition, frame, K.δ-ID lemma, or vacuity).
- **Atomicity discussion** acknowledges Σ_mid is a fully reachable state under SequentialTransitionAxiom, S3★ is preserved there, and discoverability values at Σ_mid vs Σ' agree except in the reflexive-endset case from d.

VERDICT: CONVERGED
