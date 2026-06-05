# Review of ASN-0113

I read this as a pure-query specification: state observed, span-set returned, nothing written. The core obligations — what the returned value is (W0–W2), that each member is a well-formed span (W3), that it covers its subspace exactly (W4), that the members partition the counted positions (W16), and the boundary behavior (empty/allocated-empty/unallocated, one-member, degenerate depth, non-contiguous) — are all discharged with explicit derivations and two worked instances.

I checked the load-bearing proofs:

- **W4 (ExactCoverage)** — the T5 application is sound: `[S,1,…,1]` of length `m_S−1` is a prefix of both `start_S` and `reach`, so every `t` in the closed interval shares it; with `#t = m_S` and the half-open upper bound, the last component is pinned to `1..n_S`, matching D-SEQ★. Completeness and (VSlice-restricted) exclusivity both hold.
- **W5 (ExactnessRequiresContiguity)** — order-convexity (S0/T12) genuinely forces the gap point into any covering span; the `{[S,1],[S,3]}` counterexample is concrete and correct (`σ* = ([S,1],δ(3,2))`, reach `[S,4]`, intersection admits `[S,2]`).
- **W9/W11/W16** — `O(d) = V_{s_C}(d) ⊔ V_{s_L}(d)` rests on S3★-aux (not merely the definitional `occupied ⊆ {s_C,s_L}`), and disjointness is correctly grounded in SC-NEQ on `t₁`, with the deliberate non-invocation of T7 (wrong preconditions — these are zero-free V-positions, not `zeros=3` I-addresses) explicitly justified.
- **W12 (ProfileIrreducibility)** — the reachability witness is discharged over valid composites satisfying the full J0 ∧ J1★ ∧ J1'★ discipline (not J0 alone), with the content composite (K.α+K.μ⁺+K.ρ) and link composite (K.λ+K.μ⁺_L, couplings vacuous) correctly analyzed, and J4 named as the bundled alternative.
- **W15 (Independence)** — correctly resists the tempting overclaim: it notes K.μ⁻ can contract both subspaces jointly and re-derives independence from the disjoint position sets rather than from a false single-subspace-transition premise.

The precondition discipline (W-pre) sharply separates allocated-empty (`⟨⟩`, defined) from unallocated (outside domain, failure), and never collapses `⟨⟩` into the failure case. Boundaries — empty document, single-occupied-subspace, degenerate `m_S = 2`, non-contiguous — are each instantiated against specific tumblers. No proof-by-"similarly," no checkmark substituting for a case analysis.

The ASN stays in specification territory: abstract state, a pure operation on it, and cross-member invariants (partition, disjointness, independence, comparability) that any alternative implementation would have to satisfy. Implementation traces appear only as corroborating evidence. No drift; no META. Out-of-scope siblings (content delivery, overall extent, link counting/discovery, version/transclusion permanence) are correctly deferred to Open Questions rather than claimed.

I found no REVISE-level defect: no incomplete case, no undischarged conjunct, no foundation misuse, no hand-waved derivation, and the required concrete-example and boundary coverage are present.

VERDICT: CONVERGED
