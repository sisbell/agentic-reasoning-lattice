# Review of ASN-0086

## REVISE

### Issue 1: R0 subsequent-emission freshness argument is incomplete
**ASN-0086, R0 proof, "Subsequent emission" branch**: "By ChainEnumerationInjectivity (ASN-0093) and ChainMembershipForOrigin (ASN-0093), `ℓ_prev` is the maximum index of the contiguous prefix of `A_L(d)`'s realized chain, and `inc(ℓ_prev, 0)` is the next chain index — which by ChainEnumerationInjectivity is distinct from every element of `dom(Σ.L)`..."
**Problem**: K.λ's contract requires `ℓ ∉ dom(L) ∪ dom(C)` as a precondition. The first-emission branch correctly discharges this via FirstEmissionFreshness. The subsequent-emission branch only addresses one of three potential collision sources:
- (a) inc(ℓ_prev, 0) ≠ chain elements of A_L(d) already in dom(L) — handled by ChainEnumerationInjectivity + ChainMembershipForOrigin's contiguous prefix
- (b) inc(ℓ_prev, 0) ≠ dom(L) elements at homes d' ≠ d — NOT addressed; requires DisjointSubAllocatorChains or CrossDocDisjointness from ASN-0093
- (c) inc(ℓ_prev, 0) ∉ dom(C) — NOT addressed; requires E(inc(ℓ_prev, 0))₁ = s_L vs ASN-0093 L0 + SC-NEQ

ChainEnumerationInjectivity establishes distinctness *within* the chain enumeration, not against dom(L) elements outside A_L(d), nor against dom(C). The claim "distinct from every element of `dom(Σ.L)`" goes beyond what ChainEnumerationInjectivity delivers.
**Required**: Either explicitly cite (b) cross-allocator/cross-doc disjointness and (c) SC-NEQ + L0 in the subsequent-emission freshness argument, or appeal to K.λ's contract holistically (rather than naming only one source lemma).

### Issue 2: R7a iteration ordering argument is under-elaborated
**ASN-0086, R7a proof**: "Re-ordering the Δ-enumeration so that fresh addresses homed at the same `d_k` are listed in chain-order from least to greatest index (a permissible re-enumeration since Δ is finite and we are free to choose the iteration order), each `a_k` is the chain element at the next available index after the prior iteration completed; K.λ's first/subsequent rule produces exactly this element."
**Problem**: Two sub-claims are asserted without explicit derivation:
- (i) That chain-order is well-defined within each home — presumably via R0a-Cor1's contiguous-prefix structure, but not cited
- (ii) That interleaving across distinct homes doesn't affect K.λ's deterministic outcome at any home — presumably because K.λ's first/subsequent predicate at d_k depends only on `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d_k}`, but this scope-restriction isn't pointed out

Without these, the iteration argument reads as "we can pick the right order" rather than "any valid order works because K.λ's determinism is per-home."
**Required**: Cite R0a-Cor1 to establish chain-order existence within each home, and explicitly note that K.λ's per-home determinism (origin-scoped homed-set predicate) makes the cross-home iteration order immaterial.

### Issue 3: R0a-Cor2 zero-position stability not fully derived
**ASN-0086, R0a-Cor2 proof**: "ChainUniformLength (ASN-0093) gives `#t_n = #t_1` for every `n ≥ 1`; ChainUniformZeroCount (ASN-0093) gives `zeros(t_n) = zeros(t_1) = 3`. Together, these fix the zero-index partition of every `t_n` identically: positions are the same and zero positions are the same."
**Problem**: ChainUniformLength + ChainUniformZeroCount give same length and same *count* of zeros. They do not, by themselves, force the zero *positions* to be identical — different length-L tumblers can carry the same number of zeros at different positions. The bridge to "the partition is identical" requires either ChainPrefixExtension (every t_n extends b_L(d), which has all 3 zeros within positions 1..#b_L(d); ChainUniformZeroCount then forces the trailing position #b_L(d)+1 to be non-zero) or TA5(c) + TA5-SigValid (inc(·, 0) modifies only sig(t_n) = #t_n, which is and stays non-zero).
**Required**: Cite ChainPrefixExtension (or TA5(c) + TA5-SigValid) alongside the count and length lemmas so that position-stability — the load-bearing fact for #E(t_n) = #E(t_1) — is explicitly derived.

### Issue 4: Worked sketch's invocation of R6c-Corollary overreaches the corollary's stated conclusion
**ASN-0086, Worked Sketch, end of Step 2**: "by *R6c-Corollary*, the established `A_K^{Σ_2} = {(a₂, F₁, G₁)}` persists across any subsequent arrangement-modifying step `Σ_2 ↦ Σ_arr`..."
**Problem**: R6c-Corollary's *stated conclusion* concerns retracted tuples staying out of A_K under `⊑̂`. The Worked Sketch claims something stronger — that `A_K` is *fully preserved* (including the non-retracted active member (a₂, F₁, G₁)) across arrangement-modifying steps. This broader fact is established within R6c-Corollary's *proof* (as the intermediate `A_K^{Σ_arr} = A_K^Σ pointwise` step), but it is not what the corollary's headline claim says.
**Required**: Either cite L12 + L12a directly (which yield `Σ_arr.L = Σ.L`, hence pointwise A_K preservation), or split R6c-Corollary into its narrow conclusion (retracted-stays-out on `⊑̂`) and the underlying broader claim (full A_K stability across arrangement modifications), and let the Worked Sketch cite the broader one explicitly.

## OUT_OF_SCOPE

The Open Questions list captures the substantial deferrals appropriately (higher-arity links, concurrency model, observation ordering, atomicity of Emit vs Observe, cardinality bounds on `nullified`, tightening L1b, elevating unit-depth retraction discipline to substrate, dynamic type-catalog extension). No additional out-of-scope topics flagged.

META: not applicable — the ASN stays in spec territory (state properties, operation contracts, invariant preservation), without drifting into implementation mechanics.

VERDICT: REVISE
