# Review of ASN-0047

This ASN is technically dense and, on the mathematics, sound: the D-SEQ★ derivation (both `m=2` and `m≥3` branches), the K.μ⁻ constructive/post-state equivalence, the K.μ~ necessity/sufficiency argument, the φ-bijection multiplicity preservation, and the per-elementary invariant matrix all check out against the foundations. The worked-example tumbler arithmetic is consistent throughout. My findings are confined to forward-reference accretion and meta-prose, which the `review-mode.anti-bloat` classifier directs me to surface at source, plus one defensive paragraph.

## REVISE

### Issue 1: Triplicated "scope GlobalUniqueness to the node-rooted subtree" argument
**ASN-0047, FrontierEquivalence (reverse), ChildSpawnFreshness (reverse), CrossDocEntityDisjoint (*Same-parent pairs*)**: The same scoping argument is restated three times in near-identical form, e.g. ChildSpawnFreshness: "Because the inc-allocator structure is a forest and not a single tree, GlobalUniqueness cannot be applied unscoped: cross-node distinctness (T10, ASN-0034) first excludes any event under a distinct baptised node ... Scoped to the single node-rooted subtree at N, GlobalUniqueness ... applies"; CrossDocEntityDisjoint: "discharged by GlobalUniqueness ... scoped, per NodeRootedForest, to the single node-rooted subtree"; FrontierEquivalence: "GlobalUniqueness ... applies and the address inc(t, 0) can be produced by exactly one allocator's tracked chain."
**Problem**: This matches the listed accretion pattern "two paragraphs in the same document say the same thing in different words." The forest-scoping caveat is a single reusable fact (it lives in NodeRootedForest), yet each lemma reconstructs it inline.
**Required**: State the subtree-scoping discharge once (NodeRootedForest already exists as the home for it) and have the three lemmas cite it by name rather than re-derive it.

### Issue 2: K.δ case (ii) k=1 and k=2 restate the at-most-once discharge verbatim
**ASN-0047, K.δ case (ii)**: The `k = 1` and `k = 2` sub-cases carry parallel sentences: "Here the case-level `e ∉ E` (with `e = inc(t, 1)`) *is* the enforcement of T10a's at-most-once-per-`(t, k')` discipline ... discharged by ChildSpawnFreshness at `k' = 1`, whose biconditional gives `inc(t, 1) ∉ Σ.E ⟺ the (t, 1) child-spawn has not yet been performed`" — and the same sentence again with `2` substituted for `1`.
**Problem**: The two sub-cases differ only in the substituted parameter; the prose is otherwise identical, so the reader parses the same argument twice.
**Required**: Collapse to one statement parameterised over `k' ∈ {1, 2}` ("the case-level `e ∉ E` enforces T10a's at-most-once discipline, discharged by ChildSpawnFreshness at `k' = k`"), retaining only the genuinely k-specific conjuncts (the `Document(t)` requirement at `k=1`, the `zeros(t) ≤ 1` bound at `k=2`).

### Issue 3: Defensive "robustness" paragraph imagining an internal step ordering
**ASN-0047, Class (b) P4a discharge**: "Because J1'★ constrains only the endpoint and not the moment of recording, the discharge is robust to the internal ordering of K.ρ and K.μ⁺: an ordering such as K.α → K.ρ → K.μ⁺ (each step satisfying its elementary precondition, since K.ρ requires only `a∈dom(C)∧d∈E_doc`) passes through an intermediate state with no live witnessing V-position, yet Σ' carries the witness J1'★ forces."
**Problem**: This is meta-prose justifying robustness against a hypothetical step ordering that the J1'★ endpoint formulation already renders irrelevant. The substantive claim — "for a fresh entry the witnessing trace state is Σ', supplied by J1'★'s post-state conjunct" — is complete one sentence earlier. The ordering excursion adds no reasoning the J1'★ definition does not already carry.
**Required**: Delete the robustness sentence; the preceding J1'★ appeal discharges P4a on its own.

### Issue 4: Default-value convention stated twice
**ASN-0047, *The state model***: The default-value rule appears first inline ("By the default-value convention (Bridging lemma (M–E_doc)), `M(d) = ∅` when `d ∉ dom(M) = E_doc`...") and again in full as the "*Notational convention (default value)*" paragraph.
**Problem**: Minor duplication; the inline mention pre-states the convention before its formal definition a few lines later.
**Required**: Drop the inline restatement and let the formal "Notational convention" paragraph be the single site.

## OUT_OF_SCOPE

### Topic 1: Interior-link renumbering contraction and transitive-transclusion provenance
**Why out of scope**: Both are correctly deferred as Open Questions (renumbering-aware `DELETEVSPAN`-style interior contraction; provenance under transclusion chains). The ASN's K.μ⁻ models only suffix/full contraction, which is the right elementary primitive here; the compacting interior delete belongs to a later operation-level ASN, not a revision of this one.

VERDICT: REVISE
