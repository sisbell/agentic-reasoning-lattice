# Integration Review of ASN-0047

## REVISE

(none)

The integrated material — SC-NEQ, K.α/K.μ⁺/K.μ⁻ amendments, K.λ, K.μ⁺_L, S3★, S3★-aux, Contains_C, P4★, J1★, J1'★, ValidComposite★, P3★, P5★, CL-OWN, and ExtendedReachableStateInvariants — is correct and cleanly integrated.

Key points verified:

**Link-subspace fixity under K.μ~.** The chain S3★ + S3★-aux → π maps dom_L injectively into dom_L(M'(d)) → K.μ⁺ can't create link-subspace positions → r = 0 is tight. No circularity: S3★ and S3★-aux are established independently by decomposition (K.μ⁻ preserves, K.μ⁺ preserves), then fixity follows. The K.μ⁺ frame at the intermediate state gives the stronger result M'(d)|_{dom_L} = M(d)|_{dom_L} directly.

**Two-class proof structure in ExtendedReachableStateInvariants.** The partition into elementary invariants (preserved per-step) and composite invariants (P4★, P7a — violated at intermediate states, restored at composite boundaries via J1★/J0) is sound. P7 is correctly classified as elementary: K.ρ's precondition a ∈ dom(C) plus P0 ensures grounding persists.

**K.μ~ decomposition existence.** The n' = 0 construction (remove all content-subspace positions, re-add at new positions) always satisfies D-CTG/D-MIN at the intermediate state vacuously. The K.μ⁺ frame preserves link-subspace values, establishing fixity without requiring π|_{dom_L} = identity explicitly.

**P4★ necessity.** The argument that unscoped Contains is unsatisfiable with P7 once link-subspace mappings exist (ℓ ∈ dom(L), dom(L) ∩ dom(C) = ∅ by L14, so (ℓ,d) ∉ R) correctly motivates the content-subspace scoping. J1★/J1'★ are range-based, matching J1/J1' structure while avoiding the K.μ⁺/P7 conflict.

**Registry.** All 17 integrated properties listed with correct labels and descriptions.

VERDICT: CONVERGED
