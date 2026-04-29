# Review of ASN-0063

## REVISE

### Issue 1: K.μ~ link-subspace fixity proof — missing subspace exhaustiveness step

**ASN-0063, "Extending the Transition Framework" (S3★ preservation by K.μ~)**: "π must map link-subspace positions to link-subspace positions: if `v ∈ dom_L(M(d))` then `M(d)(v) ∈ dom(L)`, and `M'(d)(π(v)) = M(d)(v) ∈ dom(L)`, so `subspace(π(v)) = s_L` by S3★ for M'(d) (a content-subspace position mapping to dom(L) would violate the content clause)."

**Problem**: The argument eliminates `subspace(π(v)) = s_C` via contradiction (S3★ content clause + L14 disjointness), but concludes `subspace(π(v)) = s_L` without establishing that `{s_C, s_L}` exhausts all possible subspace values. S3★ has only two clauses; a V-position with hypothetical subspace `s₃ ∉ {s_C, s_L}` would satisfy neither antecedent, producing no contradiction. Without subspace exhaustiveness, the injection `π : dom_L(M(d)) → dom_L(M'(d))` is not established — π might map link-subspace positions into a third subspace, breaking the cardinality argument that yields `r = 0`.

The same implicit assumption appears in the P4★ preservation proof for K.μ~, where `dom_C(M(d)) = dom(M(d)) \ dom_L(M(d))` equates the set complement with "content-subspace positions" — valid only if `{s_C, s_L}` is exhaustive.

The property holds by induction on transitions without depending on fixity (avoiding circularity): K.μ⁺ (amended) creates only `s_C` positions; K.μ⁺_L creates only `s_L` positions; K.μ⁻ removes positions without altering subspaces of survivors; K.μ~ decomposes into K.μ⁻ + K.μ⁺, both of which maintain the property. The base case is vacuous (M₀ = ∅).

**Required**: Before the fixity argument, state and prove: "In every reachable state, all V-positions have subspace `s_C` or `s_L`. *Proof.* By induction. Base: `M₀ = ∅`. Step: K.μ⁺ (amended) creates only `s_C` positions; K.μ⁺_L only `s_L`; K.μ⁻ preserves subspaces of surviving positions; K.μ~ decomposes into K.μ⁻ + K.μ⁺, each maintaining the property independently of fixity." Then cite this property at the step concluding `subspace(π(v)) = s_L` and at the `dom_C = dom \ dom_L` identification.

## OUT_OF_SCOPE

### Topic 1: Link-subspace ownership invariant
K.μ⁺_L does not require `origin(ℓ) = d` — it permits placing a link from document X into document Y's arrangement. CREATELINK ensures home-document ownership through K.λ, but K.μ⁺_L as a standalone transition is more permissive. Whether to add an invariant `(A d, v : v ∈ dom(M(d)) ∧ subspace(v) = s_L : origin(M(d)(v)) = d)` depends on whether link transclusion (sharing another document's links) is architecturally desired.

**Why out of scope**: This concerns future usage of K.μ⁺_L beyond CREATELINK — a design question for the operations that would invoke it.

### Topic 2: D-CTG preservation by K.μ⁻
K.μ⁻ (ASN-0047) has no precondition preventing removal of interior link-subspace V-positions, which would violate D-CTG. The ASN correctly identifies this tension in the orphan-link discussion and defers the withdrawal mechanism to open questions.

**Why out of scope**: This is a pre-existing gap in ASN-0047's specification of K.μ⁻, not introduced by this ASN.

VERDICT: REVISE
