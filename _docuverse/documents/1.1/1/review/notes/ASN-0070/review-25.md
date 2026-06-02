# Review of ASN-0070

I checked the core inverse-image definition (F0), the operation postcondition (F1), the large CanonicalUniqueness theorem (F-canonical), the derived lemmas, the weakest-precondition analysis, and all seven worked configurations.

## Verification notes

**F-canonical proof.** The case split on `k = actionPoint(ℓ)` is exhaustive (`k ∈ {1,...,m}` since `#ℓ = m_S(d)`): `k < m` yields infinite `⟦σ⟧_V` (via T0(a) unboundedness) and is excluded by finiteness; `k = m` is proved by mutual inclusion. The consecutive-tumbler characterisation (forward + the induction in the reverse direction) is complete, including the `q=p ∧ q'=p` contradiction against ℕ-irreflexivity and the position-`m` discreteness step. The maximal-run partition is justified (single-valued successor/predecessor + acyclicity from T1). Step 2a (existence) and the right/left-closure inter-component gap arguments correctly use N1/N2 and handle the `s_j.m = 1` zero-component sub-case separately.

**Edge cases covered.** Empty subspace (`m_S(d)` undefined → `⟨⟩` convention), empty resolution (F-empty, with representational uniqueness derived via T12(b)), within-document multiplicity (F-multi, with the implication and the K.μ⁺ non-injectivity reachability argument kept distinct from the S5 cardinality point), fragmentation (Config 6, instantiating F-contig at `j>0, c<n`), cross-subspace straddle (Config 7, both components non-empty), and state-dependence (Config 4).

**Examples.** All seven configurations check out arithmetically (shift/δ computations, retention-set form for K.μ⁻, separation `reach(σ₁) < start(σ₂)` in the fragmentation case).

**Self-containment.** Every external reference is to a listed foundation (ASN-0034/0036/0043/0047/0053/0058); no non-foundation ASN is cited. F-subspace's reverse direction correctly uses ASN-0047's unscoped L14, not ASN-0043's scoped variant.

**Soundness/completeness** are correctly framed as the two inclusions of the postcondition's set equality rather than independent obligations. The wp analysis is non-trivial (unpacking definedness of `L(ℓ).eᵢ`, `M(d)`, and the subspace projection) and the operation defines an abstract state query, not implementation mechanics — no drift.

## OUT_OF_SCOPE

### Topic 1: Partial-reach reporting, transclusion-lineage relationships, concurrency semantics, unbounded-coverage compactness
**Why out of scope**: These are the ASN's own Open Questions and concern downstream system-level contracts (citation artifacts, content-retrieval coupling, concurrent modification) that build on `follow` rather than defining it. Correctly deferred.

VERDICT: CONVERGED
