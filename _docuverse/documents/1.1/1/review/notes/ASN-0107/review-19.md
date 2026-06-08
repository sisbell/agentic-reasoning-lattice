# Review of ASN-0107

This is a strong, deep note: the matching-set/cardinality development is clean, the existence/discovery anchoring split is the right abstraction, and the depth requirements (worked instance, R6 weakest-precondition) are genuinely met. The findings below are predominantly the forward-reference/meta-prose accretion the `review-mode.anti-bloat` classifier asks me to surface, plus one redundant claim.

## REVISE

### Issue 1: A1b imagines a case its own premise excludes
**ASN-0107, A1b (FreshContentNeutrality, discovery)**: "Neutrality is therefore independent of *where* the fresh content is arranged; the operative reason is that nothing covers `a_new`, not its position relative to `Qᵢ(Σ)`."
**Problem**: The "position relative to `Qᵢ(Σ)`" case is exactly what the no-incoming-links premise already neutralises. This is reviser drift — a paragraph contrasting against a case the precondition forecloses, rather than advancing the claim. The preceding sentence ("even arranging `a_new` into a queried V-region … creates no new match") already carries the content.
**Required**: Drop the trailing "Neutrality is therefore independent…" sentence.

### Issue 2: A1a trailing sentence is contrastive meta-prose
**ASN-0107, A1a (FreshContentNeutrality, existence)**: "For existence anchoring `Q` is a fixed permanent address set, so there is no 'content change' for the neutrality to be conditioned on."
**Problem**: This sentence does not advance A1a; it explains why A1a is unconditional *in contrast to A1b*. The claim "corollary of E3, `match(Q,·)` invariant under K.α" is complete without it. Defensive justification of the conditional/unconditional asymmetry between sibling claims.
**Required**: Remove the sentence; the corollary-of-E3 derivation stands alone.

### Issue 3: R5 restates E4 with self-referential framing
**ASN-0107, R5 (ConservationConditional)**: "The affirmative half … is exactly E4. The content R5 adds is the negative result: under discovery anchoring conservation *fails*…"
**Problem**: R5's affirmative half is, by its own admission, identical to E4, and its negative half is D1/D2 restated. The phrase "The content R5 adds is the negative result" is meta-commentary about the claim's marginal value rather than reasoning. The claims-table entry confirms the redundancy ("conservation is exactly E4; conservation fails under discovery anchoring").
**Required**: Either fold R5's negative observation into D2 as a one-line corollary and delete R5, or strip the "The content R5 adds is…" framing and state the conditional directly without re-deriving E4.

### Issue 4: R1↔R6 circular cross-reference prose
**ASN-0107, R6 derivation**: "*Specialisation to R1.* R1's minimal-contraction split is the `k = 1` case of this wp … R1 states the two branches; here they are simply the two truth-values of this wp at `ℓ`."
**Problem**: R1 forward-defers ("the `k = 1` specialisation of R2's `Δ ∈ {−k,…,0}`") and R6 back-references ("specialises to R1's split"), with R6 then restating the relationship a second time in the closing sentence. Two paragraphs describing the same `k=1` correspondence in different words. The single statement "R1's split is the two truth-values of this wp at `ℓ`" suffices.
**Required**: Keep one statement of the R1/R6 correspondence (in R6's derivation), and delete the redundant closing "R1 states the two branches…" sentence.

### Issue 5: The fourth Open Question is already resolved by the definitions
**ASN-0107, Open Questions**: "What must the count guarantee about its own stability under a request … re-decomposed into different spans of the same coverage?"
**Problem**: `sat` is defined as `coverage(Σ.L(a).eᵢ) ∩ Qᵢ`, with `Qᵢ ⊆ T` an address set; the count is manifestly a function of the *sets* `Qᵢ` and the *coverages*, both representation-independent (the latter is the LP21 property). Representation-invariance of the request is therefore immediate from P0/`sat`, not open. Posing it as a future question misrepresents a settled consequence.
**Required**: Either remove the question or convert it to a one-line derived claim (request-side representation invariance: equal-coverage requests yield equal `num`).

## OUT_OF_SCOPE

### Topic 1: Independently-anchored multi-document requests
The first open question (three parts anchored to separately-evolving documents) is legitimately new territory — it requires a cross-document arrangement-coupling account this note does not need. Correctly deferred.

### Topic 2: Discovery/existence coincidence and count/retrieval staleness
Open questions two and three (when discovery = existence; count vs. the cardinality the retrieval operation would return) belong with the retrieval operation (ASN-0099), which is out of scope here. Correctly deferred.

VERDICT: REVISE
