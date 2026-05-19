# Review of ASN-0086

I read this ASN end-to-end against the foundation and walked through each proof. Below is a summary of the close-reading.

## What I verified

**Proofs checked in detail:**
- R0 — the K.λ invocation, freshness sub-claims (a)/(b)/(c) for same-home/cross-home/cross-store via ChainEnumerationInjectivity + CrossDocDisjointness + DisjointSubAllocatorChains + SC-NEQ, and the full per-invariant discharge.
- R0a Case 1 — the `zeros(w) = 0 ⟹ home equality` argument is rigorous; the symmetric direction is correctly handled via explicit substitution (not "by symmetry").
- R0a Case 2 — chain-membership + ChainUniformLength + prefix-with-equal-length + T3.
- R0a-Cor2 — both Route A (TA5(c) + TA5-SigValid + ChainElementT4Validity) and Route B (ChainPrefixExtension + ChainUniformZeroCount).
- R5 + R5-Cor — the meta-argument that R0's verification is endset-content-uniform is sound (I verified each invariant L0/L1/L1a/L1b/L1c/L2/L3/L5/L6/L8/L11a/L12-series/L13/L14/L14a/L-fin checks emitter-address properties only, except L3 which is well-formedness-only).
- R6c-Corollary — the reduction from `↦*`-chain to `→*`-subsequence via Σ.L pointwise-constancy under arrangement-modifying steps.
- R7a — the Δ-enumeration, the three-part chain-order argument (i)/(ii)/(iii), the per-step substrate-invariant discharge for both K.σ-prefix and K.λ-emission cases, and both Worked Examples (length-2 and length-4 decompositions).

**Worked Sketch numerics:**
- `a_1 = 1.0.1.0.1.0.2.1` via `d → inc(d, 2) → inc(_, 0) → inc(_, 1)`: lengths, zero positions, E-projections, T4-validity all check.
- Step 1 `b_1 = 1.0.1.0.1.0.2.2`, Step 2 `a_2 = 1.0.1.0.1.0.2.3`, Step 3 `c_1 = 1.0.1.0.1.0.2.4` — all consistent with K.λ subsequent-emission rule.
- Step 3's R6b demonstration: retracting `b_1` does not restore `a_1` because the existential in `nullified` ranges over `L_R^{Σ_3}` (audit slice), not `A_R^{Σ_3}` — the original retraction tuple at `b_1` directly witnesses `a_1 ∈ nullified(Σ_3)` regardless of `b_1`'s own status.

**WP analysis:**
- Case 1: `wp(Nullify) = P0 ∧ P1 ∧ P2` correct (R0a's unconditional antichain discharges the no-strict-prefix-extension condition without an auxiliary conjunct).
- Case 2: the three regimes (unit-depth discipline / crafted-span admitted / self-nullifying R-typed) cover all paths to `a ∈ nullified(Σ')`; the wp formula correctly captures both pre-existing nullification and self-nullification under `K ~ R`.

**Cross-ASN discipline:** Only foundation ASNs (0034, 0036, 0043, 0093) are cited. No reinvented notation — the ASN uses `home`, `origin`, `coverage`, `subspace_I`, `inc`, `δ`, `≼`, `Endset`, `T_admissible`, T-/L-/S-/M-/C-/B-prefixed claim labels, and ASN-0093's K.σ/K.α/K.λ/SubAllocatorAxiom/Chain* lemmas as foundation primitives.

**Edge cases addressed:** empty `dom(Σ.M)` (R0 precondition), empty `dom(Σ.L)` (first-emission branch, Step 0), empty endsets `F = ∅` (Nullify's from-set), self-targeting (R5), single-tuple scope under arbitrary subtree shape (Nullify), retraction-of-retraction (R6b, Step 3), cross-home (R0a Case 1), same-home (R0a Case 2), zero-length chain (R6c base case), length-1 vs length-≥-2 replay (R7a Worked Examples).

VERDICT: CONVERGED
