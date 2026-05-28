# Review of ASN-0101

I worked through the ASN carefully, checking each claim's proof, the boundary-case taxonomy, the worked examples, and the cross-references against the foundation vocabulary.

**D0** introduces DEL as a new atomic transition with precise preconditions, effect, and frame. The containment-precondition reduction is proved for m_S = 2 (vacuous middle range) and m_S ≥ 3 (minimality argument on j₀ with T0/T1 ruling out v_{j₀} = 0 and v_{j₀} ≥ 2). **D1** uses TS1/TS2 (ASN-0034) to establish σ_d as an order-preserving bijection from Π to Q with the precise structural form [S, 1, ..., 1, k − n].

**D2-D7** are derived from D0's frame plus foundation invariants. D7's attribution survival relies on origin being a tumbler projection (state-independent) plus D2/D3/L0/L14; the "Equivalently, restricted by subspace" clause partitions the store membership cleanly.

**D8** organizes invariant preservation into three groups. Group (i) uses source correspondence — each post-state v ∈ dom(M'(d)) has M'(d)(v) = M(d)(u) for a unique u with subspace preserved — to discharge S2, S3★, S3★-aux, S8★, CL-OWN, CL-UNIQ. The CL-UNIQ argument for S = s_L correctly exploits Λ ∩ Π = ∅ (last-component ranges) plus σ_d's bijectivity to combine the two-summand injectivity. Groups (ii) and (iii) reduce to frame arguments, with P4★ given explicit lift-back via case analysis on v ∈ Λ ⊎ Q ⊎ V_{S'}(d) under both S = s_C and S = s_L. S9's antecedent firing for non-vacuous DEL is correctly discharged via D2.

**D9** covers all (d'', subspace) combinations; its third bullet's union of (project ∩ Λ) and {σ_d(v) : v ∈ project ∩ Π} is verified concretely in both single-document examples.

**D10** honestly identifies composite-level limits with the explicit K.α → K.μ⁺ → DEL counterexample: composite-level J0 fails when DEL removes the witness that an earlier allocation requires. The vacuity arguments for the one-step composite are correct.

**D11** derives wps with explicit justifications: the discoverability wp reduces (project ⊄ X) via the chain Λ ∪ Π ∪ V_{S'}(d) = dom(M(d)) \ X; the cardinality wp uses |project ∩ (Λ ∪ Π)| = |project ∩ V_S(d)| − |project ∩ X|.

The boundary-case taxonomy (empty post-state, deletion at start/end, singleton subspace, singleton interior, non-singleton interior) enumerates per-case discharge routes: D-MIN★ receives a non-vacuous σ_d-witness only in the "deletion at the start" case; other cases use vacuous discharge or pre-state inheritance.

The atomicity argument is sound: SequentialAtomicTransitions makes history sequence length observable (composite produces Σ_pre → Σ_mid → Σ_post, atomic produces Σ_pre → Σ_post), and the killer case (link-subspace interior with |V_{s_C}(d)| < 2) shows K.μ~ + K.μ⁻ is structurally unavailable.

VERDICT: CONVERGED
