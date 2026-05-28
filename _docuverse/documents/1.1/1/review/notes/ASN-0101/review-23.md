# Review of ASN-0101

I've worked through D0-D11 against the foundation claims, traced the worked examples, verified each boundary case, and checked the proofs of the well-formedness preservation (D8) and the wp derivations (D11) line by line.

## REVISE

None.

The ASN is unusually thorough. Specifically:

**D0's containment reduction** — the "Justification of the reduction" sub-section walks through both the `m_S = 2` (vacuous middle-range) and `m_S ≥ 3` (contradiction at the least non-`1` middle position) cases, using T0/T1 against the structural forms of `s` and `r` without slipping in S8a where it isn't yet established.

**D1's gap closure** — order preservation is derived through TS1, injectivity through TS2 (not collapsed to "by similar reasoning"), and surjectivity by construction. The vacuous-when-empty case is explicitly traced.

**D8's well-formedness** — invariants are partitioned into three groups by discharge mechanism. Each Group (i) invariant routes through either inheritance (Λ), `σ_d`-witness (Q), or D6-inheritance (V_{S'}). The CL-UNIQ proof is the only non-trivial route — disjoint pre-state images (Λ vs Π) are carefully transferred through the bijection. Group (ii) and (iii) are catalogued exhaustively with the frame fact discharging each. P4★'s lift `Contains_C(Σ') ⊆ Contains_C(Σ)` traces every case-by-region.

**D11's wp derivations** — the discoverability wp's set-algebra step `(V_S(d) \ X) ∪ V_{S'}(d) = dom(M(d)) \ X` is computed explicitly. The cardinality wp uses inclusion-exclusion on the disjoint partition `V_S(d) = Λ ⊎ X ⊎ Π` and combines with the D6-preserved cross-subspace term. Determinism is justified (frame components plus `σ_d^{-1}` well-defined by D1) before negation-symmetry of wp is used.

**Boundary cases** — six configurations (empty post-state, deletion at start/end, singleton subspace, singleton interior, non-singleton interior) plus cross-subspace independence. Each case explicitly identifies which D8 clauses discharge vacuously (empty-set vs empty-conditional), which require non-vacuous `σ_d`-witnesses (D-MIN★ at deletion-at-start), and which combine inheritance with shift-witness.

**Worked examples** — three: content-subspace at depth 3, link-subspace at depth 2 (exercising CL-OWN, CL-UNIQ, the `dom(L)` clause of S3★), and cross-document transclusion (exercising D5, cross-document D9, and both cross-document wps of D11). Each example traces D9's third-bullet equation explicitly with concrete LHS/RHS values.

**D10's composite-validity scope** — correctly distinguishes one-step DEL vacuity from multi-step composite validity. The K.α + K.μ⁺ + DEL counterexample concretely shows composite-level J0 failure even though each step's elementary precondition holds. The LP-family dispatch catalogues LP2★-LP14 exhaustively across the extended vocabulary.

**Operation-as-atomic-primitive justification** — the formal argument that DEL is not a derived K.μ~ + K.μ⁻ composite is anchored to two distinct obstacles: (i) sequence-length difference under SequentialAtomicTransitions, which holds unconditionally regardless of whether intermediate states are observationally distinct, and (ii) genuine unavailability of K.μ~ for link-subspace interior deletions when `|V_{s_C}(d)| < 2`, with the killer-case analysis ruling out spurious alternatives.

VERDICT: CONVERGED
