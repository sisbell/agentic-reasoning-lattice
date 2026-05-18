# Review of ASN-0093

## REVISE

### Issue 1: Prefix-extension property of A_C(d) and A_L(d) is load-bearing but never derived
**ASN-0093, Cross-document disjointness chain (Closure paragraph)**: "Every link address allocated under `d₁` extends `p₁ = b_L(d₁)`; every link address allocated under `d₂` extends `p₂ = b_L(d₂)`. Therefore no link allocated under `d₁` can coincide with any link allocated under `d₂`."

**Problem**: The claim "every chain element of A_C(d) (resp. A_L(d)) extends its anchor b_C(d) (resp. b_L(d))" is asserted but never derived. This claim is load-bearing for every cross-document freshness derivation: K.α first-emit (when ruling out a = a' for a' with origin(a') ≠ d), K.α subsequent-emit (same), K.λ first-emit, K.λ subsequent-emit, and the Cross-document disjointness lemma's own closure step. T10 requires `p₁ ≼ a ∧ p₂ ≼ b` as input; without the prefix-extension property, the chain elements are not known to satisfy that hypothesis.

**Required**: State and prove an explicit corollary "ChainPrefixExtension": for every reachable Σ, every d ∈ dom(M), and every t ∈ A_C(d), `b_C(d) ≼ t` (mirror for A_L(d) and b_L(d)). Base case from FirstEmission's concrete form [d.0.s_C.1] = b_C(d) ++ [1]. Inductive step: t' = inc(t, 0) preserves positions 1..#t-1 (TA5(c) plus TA5-SigValid pinning sig(t) = #t > #b_C(d)). Cite this corollary at every freshness derivation.

### Issue 2: T4-validity of dom(C) ∪ dom(L) is needed for T7 but never stated as a derived invariant
**ASN-0093, Discharge matrix entry for L14**: "Holds at Σ' by direct derivation: L0(Σ') + SC-NEQ + T7 — all hold at Σ'"

**Problem**: T7 (FirstElementFieldDistinction, ASN-0034) requires both operands to satisfy the T4 constraints *and* have zeros = 3. The substrate states zeros = 3 (via C1 and L1) and E(·)₁ values (via L0), but it never exports "every a ∈ dom(C) ∪ dom(L) is T4-valid" as a derived consequence. T4-validity is derivable from C1c/L1c chain admissibility (each step satisfies TA5a's T4-preservation conditional on zeros bound, anchored at M0's T4-valid origin) plus induction, but this derivation is nowhere written down. Without it, the L14 invocation of T7 has an unverified precondition.

**Required**: Add a derived invariant "T4-validity of content and link addresses": for every reachable Σ, every a ∈ dom(C) and every ℓ ∈ dom(L) is T4-valid. Discharge by induction over C1c/L1c chain admissibility plus M0's T4-validity of origin. Then expand L14's matrix entry to walk through T7's precondition explicitly: T4-validity (newly stated), zeros = 3 (C1/L1), E(·)₁ values (L0), SC-NEQ → distinct addresses.

### Issue 3: Remark "derivable clauses" omits two premises in the FirstEmission-freshness derivation
**ASN-0093, Remark after SubAllocatorAxiom**: "FirstEmission's freshness conclusion `a ∉ dom(C) ∪ dom(L)` follows from the first-emit predicate + L0 + Cross-document disjointness + SC-NEQ."

**Problem**: The listed premises are insufficient. (a) For a' ∈ dom(C) with origin(a') ≠ d, the derivation invokes Cross-document disjointness with anchors b_C(d) vs b_C(origin(a')), then applies T10 — but T10 needs `b_C(origin(a')) ≼ a'`, which is the ChainPrefixExtension property (Issue 1), not in the listed premises. (b) For ℓ ∈ dom(L), the derivation routes through L0 + SC-NEQ + T7 to conclude ℓ ≠ a, but T7 needs T4-validity of both a and ℓ (Issue 2), also not in the listed premises. The Remark's "leaner axiom" claim correspondingly under-specifies what the leaner axiom must derive.

**Required**: Either (a) keep FirstEmission's freshness as primitive axiom content and drop the "derivable" framing, or (b) fix the Remark by enumerating the full premise set (first-emit predicate + L0 + ChainPrefixExtension + T4-validity-of-stores + Cross-document disjointness + SC-NEQ + T7) and writing out the two derivations (against dom(C), against dom(L)) step-by-step.

### Issue 4: ChainMembershipForOrigin proof and the discharge matrix are mutually dependent; simultaneous induction is not flagged
**ASN-0093, ChainMembershipForOrigin proof (K.σ step)** uses C2/L1a as IH at Σ; **discharge matrix K.α subsequent-emit freshness derivation** uses ChainMembershipForOrigin at Σ.

**Problem**: ChainMembershipForOrigin's K.σ step relies on C2/L1a holding at Σ. The discharge matrix's K.α/K.λ subsequent-emit freshness derivations rely on ChainMembershipForOrigin at Σ. These are mutually entangled and only sound under a *simultaneous* induction over transition sequences from Σ₀ where the entire bundle (matrix invariants + ChainMembershipForOrigin) is preserved jointly at each step. The note presents the two arguments separately and never explicitly says they form one combined induction.

**Required**: State explicitly that the discharge of stated invariants together with the ChainMembershipForOrigin lemma proceeds by *simultaneous induction* over transition sequences from Σ₀, with all invariants and the lemma serving jointly as inductive hypothesis for each step. Verify that no inductive step uses a conclusion derived in the same step.

### Issue 5: K.α / K.λ subsequent-emit cross-document freshness has no derivation depth
**ASN-0093, K.α subsequent-emit precondition**: "Cross-document collisions within `dom(C)` are ruled out by the Cross-document disjointness lemma."

**Problem**: The within-document freshness derivation (the T10a.7 chain-index argument) is given in detail; the cross-document derivation is a single sentence. After fixing Issue 1, the cross-document argument needs three steps explicitly: (a) a = inc(a_prev, 0) extends b_C(d) (via ChainPrefixExtension applied to a_prev plus TA5(b)/(c) preservation under the new step); (b) for every cross-document a', a' extends b_C(origin(a')) (via ChainMembershipForOrigin + ChainPrefixExtension); (c) Cross-document disjointness + T10 closes the case. The symmetric K.λ argument needs the same treatment.

**Required**: After fixing Issue 1, expand the cross-document freshness paragraphs in both K.α and K.λ subsequent-emit preconditions to walk through (a)-(c). The same expansion is needed in the K.α/K.λ *first-emit* freshness derivations referenced in the Remark.

### Issue 6: Worked example does not exercise K.λ subsequent-emit
**ASN-0093, Worked example (Steps 1–7)**: K.σ ×2, K.α first-emit ×2, K.α subsequent-emit ×1, K.λ first-emit ×2 — but no K.λ subsequent-emit.

**Problem**: K.λ subsequent-emit exercises a distinct freshness chain (T10a.7 within A_L(d) + Cross-document disjointness via b_L anchors + L0 partition). The asymmetric counterpart (K.α subsequent-emit at Step 4) is shown; without parity on K.λ, the reader cannot verify the operation against concrete tumblers.

**Required**: Add a step emitting a second link under d (subsequent K.λ), exhibiting ℓ_prev (the prior link emitted in Step 3), the inc(·, 0) extension ℓ_new = inc(ℓ_prev, 0), and verification that ℓ_new ∉ dom(L) ∪ dom(C) via T10a.7 within-chain + Cross-document disjointness + SC-NEQ.

### Issue 7: Worked example does not exercise Case B (prefix-incomparable documents) of Cross-document disjointness
**ASN-0093, Worked example Step 5**: Verifies only Case A (d ≼ d').

**Problem**: The Cross-document disjointness lemma has two cases (A: comparable, B: incomparable) with B further splitting into B.i (#d₁ ≤ #d₂) and B.ii (#d₂ < #d₁). The Case B sub-cases use a different witness-extraction strategy (position divergence within both native domains, rather than the b_L zero separator at position #d₁+1). The worked example exercises only Case A, leaving the more subtle Case B with no concrete instantiation.

**Required**: Add an example with prefix-incomparable documents (e.g., d_alt = [1, 0, 3, 0, 7] versus d = [1, 0, 2, 0, 5]), exhibit the position-3 divergence (d[3] = 2 ≠ 3 = d_alt[3]), verify the witness lies within both anchors' native domains, and confirm p ⋠ p_alt ∧ p_alt ⋠ p with the constructed witness.

### Issue 8: Contiguity of dom(C)_d as a prefix of A_C(d) is implicit
**ASN-0093, ChainMembershipForOrigin lemma and K.α subsequent-emit emission rule**

**Problem**: ChainMembershipForOrigin establishes only the *subset* relation `dom(C) ∩ {a' : origin(a') = d} ⊆ A_C(d)`. The substrate's K.α emission rule (`a = inc(max{...}, 0)` combined with FirstEmission for the first step) actually forces the stronger *contiguous-prefix* property: at every reachable Σ, dom(C)_d = {t_1, ..., t_m} for some m ≥ 0, where t_i is the i-th element of A_C(d)'s chain. The freshness arguments do not strictly require contiguity (they need only max-property + within-chain monotonicity), but contiguity is conceptually load-bearing for downstream reasoning and is a clean consequence of the emission discipline.

**Required**: Strengthen ChainMembershipForOrigin (or add a corollary) to state the contiguous-prefix form. Symmetric statement for dom(L)_d ⊆ A_L(d). Note this aligns the substrate with ASN-0040's B1 (ContiguousPrefix) for the baptismal registry.

## OUT_OF_SCOPE

None — the issues above all concern claims the ASN itself makes (or relies on implicitly), not topics deferred to higher layers.

VERDICT: REVISE
