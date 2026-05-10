# Review of ASN-0047

## REVISE

### Issue 1: J4 formal statement is universally quantified but false as stated

**ASN-0047, Coupling and isolation, J4**: The formal claim:

`(A Σ → Σ', d_new, d_src : d_new ∈ E'_doc \ E_doc ∧ ran(M'(d_new)) ⊆ ran(M(d_src)) : dom(C') = dom(C))`

**Problem**: This quantifies over *all* valid composite transitions. A composite can create d_new as a fork of d_src (satisfying the antecedent) while *also* allocating fresh content for an unrelated document d_old via K.α + K.μ⁺ + K.ρ. The antecedent holds for the (d_new, d_src) pair, but dom(C') ≠ dom(C) because of the content allocated for d_old. The composite is valid (J0, J1, J1' all satisfied), yet J4's consequent is violated.

The prose correctly describes J4 as characterising "Nelson's forking creation mode... a composite of K.δ + K.μ⁺ + K.ρ" — a *specific kind* of composite. The formal statement says something broader and false.

**Required**: Rephrase J4 as a definition or characterisation of fork composites, not a universal constraint. For example: "A fork from d_src to d_new is a composite consisting of K.δ (creating d_new) + K.μ⁺ (populating d_new with I-addresses from ran(M(d_src))) + K.ρ. Since none of K.δ, K.μ⁺, K.ρ modify C, dom(C') = dom(C)." Alternatively, restrict the quantifier to composites whose only elementary steps serve the fork.

### Issue 2: K.μ~ decomposition argument applies J1 at wrong level

**ASN-0047, Elementary transitions, K.μ~**: "J1 requires (a, d) ∈ R' for each a ∈ ran(M'(d)) \ ran(M_inter(d)) = ran(M(d)), and these pairs are already in R from prior containment (P2 preserves them)."

**Problem**: The valid composite definition states that coupling constraints J0, J1, J1' are "evaluated between the initial state Σ and the final state Σ'." At the composite level for K.μ~ decomposed as K.μ⁻ + K.μ⁺: ran(M'(d)) = ran(M(d)) (reordering preserves range), so ran(M'(d)) \ ran(M(d)) = ∅, and J1 is vacuously satisfied. No provenance analysis is needed.

The text instead applies J1's formula using M_inter(d) = ∅ (the intermediate state after K.μ⁻) as the pre-state — this is the wrong pair of states. The conclusion is correct (no K.ρ needed), but the reasoning contradicts the ASN's own definition of where coupling constraints are evaluated, and may mislead readers about the composite-vs-step distinction.

**Required**: Replace the intermediate-state J1 analysis with the simpler composite-level argument: since K.μ~ preserves ran(M(d)), the set difference ran(M'(d)) \ ran(M(d)) is empty, and J1 is vacuously satisfied.

### Issue 3: K.μ~ called "elementary" despite acknowledged decomposability

**ASN-0047, Elementary transitions**: "We seek the elementary modifications — the minimal state changes from which all system operations compose." Then: "K.μ~ likewise decomposes into K.μ⁻ (removing all mappings) followed by K.μ⁺ (re-adding them at new positions)."

**Problem**: The word "minimal" implies primitive, non-decomposable transitions. K.μ~ demonstrably decomposes into K.μ⁻ + K.μ⁺. The completeness argument derives five primitive kinds from the state structure (one growth mode each for C, E, R; two mutation modes for M) and then adds K.μ~ as a sixth with acknowledged redundancy. Claiming "these six kinds are complete" conflates covering (true of six) with minimality (true of five). The retention justification — "isolation property (J3) and semantic clarity" — is sound, but the terminology obscures the actual structure.

**Required**: Either (a) drop "minimal" from the characterisation and explicitly note that five kinds are primitive while K.μ~ is a derived convenience transition, or (b) define "elementary" in a way that accommodates semantic convenience without implying minimality. The completeness argument should state that {K.α, K.δ, K.μ⁺, K.μ⁻, K.ρ} are the primitive transitions and K.μ~ is retained as a distinguished composite for isolation analysis.

## OUT_OF_SCOPE

### Topic 1: Fork arrangement constraints
**Why out of scope**: J4 allows ran(M'(d_new)) to be any subset of ran(M(d_src)) — whether a fork must copy the full arrangement or may take a proper subset is a version-semantics question. The ASN correctly lists this in Open Questions.

### Topic 2: Provenance under transitive transclusion
**Why out of scope**: When content is shared through chains of transclusion (d₁ → d₂ → d₃), the current model records direct containment only. Whether transitive provenance guarantees are needed is a future-ASN question about link and sharing semantics. Correctly identified in Open Questions.

VERDICT: REVISE
