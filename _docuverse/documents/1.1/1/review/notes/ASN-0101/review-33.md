# Review of ASN-0101

I checked the operation specification (D0), the gap-closure bijection (D1), all seven preservation claims (D2–D8), the link-projection characterisation (D9), the ValidComposite★/LP-family extension (D10), and the weakest-precondition analysis (D11), against the three worked examples and the boundary-case enumeration.

## Verification performed

**D0/D1 — shift mechanism.** The shift-inverse `σ_d` is correctly shown well-defined (length forced by OrdinalShift length-preservation, uniqueness by TS2, existence by explicit construction `[S,1,...,1,k−n]`). Order-preservation routed through T1 trichotomy + TS1 is complete, not hand-waved. The post-state form `{[S,1,...,1,k] : 1 ≤ k ≤ n_S−n}` is contiguous in the depth-`m_S` subspace-`S` slice (any tuple with a middle/leading component ≥2 exceeds the max under T1, so no interleaving), so D-CTG★/D-MIN★/D-SEQ★ follow.

**Containment reduction.** The `m_S = 2` vacuous base and the `m_S ≥ 3` least-divergence argument (ruling out `v_{j₀}=0` via `v < s` and `v_{j₀}≥2` via `v > r`) are both rigorous and correctly avoid invoking S8a on the candidate tumbler.

**D8 — invariant preservation.** Group (i) source-correspondence handling of the `Q ∩ X ≠ ∅` re-mapping case (S3★, S3★-aux, CL-OWN, CL-UNIQ) is sound; the S8★ condition (c) discharge correctly separates the existential (a)/(b) singleton-witness from the M12-uniqueness obligation and restricts (c) to the content subspace per ASN-0047. Group (ii)/(iii) frame discharges (including the P4★ `Contains_C(Σ') ⊆ Contains_C(Σ) ⊆ R = R'` chain) check out.

**D10 — composite honesty.** The ASN correctly refuses to claim DEL automatically discharges composite-level J0/J1★/J1'★, exhibiting the K.α→K.μ⁺→DEL counterexample. The LP-family catalogue correctly skips the nonexistent LP15 and dispatches each lemma through D2/D3/D5/D6/D9/D11.

**Numerical spot-checks.** All three worked examples (content depth-3, link depth-2, cross-document transclusion) verified element-by-element — regions, `σ_d` images, post-state values, D9 third-bullet LHS=RHS, and the four D11 wps all compute as stated.

**Edge cases.** Empty post-state, deletion-at-start (the sole non-vacuous D-MIN★ `σ_d`-witness case), deletion-at-end (`Π=∅`), singleton subspace, singleton interior, and non-singleton interior are each traced with the correct discharge route. Zero-width is excluded by `Pos(ℓ_σ)`; empty-arrangement non-applicability is stated explicitly.

No proof-by-"similarly", no bare checkmarks standing in for multi-case arguments, no skipped invariant conjuncts, and no cross-ASN references outside the foundation set. The depth requirements (derived consequences, concrete examples, non-trivial wp) are met.

I found no REVISE items.

VERDICT: CONVERGED
