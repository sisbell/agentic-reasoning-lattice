# Review of ASN-0047

This note is squarely in specification territory — it defines state (Σ = C, L, E, M, R), elementary operations, and their invariants. I checked the operation discharges, the K.δ case split, the K.μ~ decomposition, the allocator arithmetic, and the cross-layer invariants; the core logic holds up. The findings below are the `review-mode.anti-bloat` patterns the note flags, plus one depth gap in the worked examples.

## REVISE

### Issue 1: Three-part freshness argument stated three times
**ASN-0047, K.α / K.λ / SubAllocatorFreshness**: K.α states "Freshness `a ∉ dom(C) ∪ dom(L)` is discharged in three parts, self-contained at this point of statement: *seed* ... *frontier* ... *cross-subspace* ... These three parts are collected ... as SubAllocFresh at `x = C`." K.λ states the identical three-part decomposition verbatim at `x = L`. The SubAllocatorFreshness lemma then states the *same* seed/frontier/cross-subspace argument a third time, explicitly "parametric in `x ∈ {C, L}`."
**Problem**: The parametric lemma (SubAllocFresh) exists precisely to be the single home for this argument; the two inline restatements at K.α and K.λ defer to the very lemma that subsumes them while reproducing its content. This is the "two paragraphs say the same thing" + "defer to the same downstream location" accretion pattern. The "self-contained at this point of statement" clause is defensive ordering meta-prose — it justifies the redundancy rather than advancing the claim.
**Required**: State the three-part decomposition once, in SubAllocFresh. At K.α and K.λ, cite `SubAllocFresh at x = C` (resp. `x = L`) by name without reproducing seed/frontier/cross-subspace. Drop "self-contained at this point of statement."

### Issue 2: Road-not-taken essay in the entity-distinctness prose
**ASN-0047, Class (a) verification, *Entity distinctness***: "Applying the Cross-document disjointness chain lemma at `e₁ = A₁, e₂ = A₂, s = 1` would deliver distinctness only for addresses extending `[A₁.0.1]` and `[A₂.0.1]`, excluding sibling documents `[Aᵢ.0.k]` for `k ≥ 2` (same length, prefix-incomparable to `[Aᵢ.0.1]`); direct application of T10 at the account level covers every sibling."
**Problem**: This is essay content explaining why one available tool is *not* used in favor of another. The discharge that is actually used (direct T10 at the account level) stands on its own; the paragraph contrasting it against the rejected alternative does not advance the proof, it defends a method choice. This is the "defensive justification" pattern.
**Required**: State the direct-T10 discharge and delete the contrastive explanation of why the chain lemma is inadequate. If the distinction must be preserved, a single clause ("via T10 at the account level, covering all sibling positions `k ≥ 1`") suffices.

### Issue 3: ParentAllocatorDispatch division-of-labor meta-prose
**ASN-0047, ParentAllocatorDispatch proof, document-level case**: "This identification is all ParentAllocatorDispatch supplies: the unique owning allocator of `t`, and (for the document level) the parent allocator of the version sub-allocator `A_v(t)`. The k = 1 child-spawn that activates `A_v(t)` consumes the case hypothesis ... as its spawnPt premise; that consumption — including the T10a allocator-monotonicity that carries the membership to the spawn event — is part of the K.δ operation's own case-(ii) discharge, which this lemma feeds rather than re-derives."
**Problem**: The closing sentences describe the boundary between what the lemma proves and what the K.δ operation proves — a division-of-labor narration that explains the document structure rather than the mathematics. "This identification is all X supplies" and "feeds rather than re-derives" are scope-drawing meta-prose.
**Required**: End the case at the identification conclusion. The spawnPt premise's provenance belongs in (and is already covered by) the K.δ case-(ii) discharge section; no boundary-narration is needed here.

### Issue 4: P4a is never exercised in any worked example
**ASN-0047, ExtendedReachableStateInvariants Class (b)**: P4a (Trace witnessing) is named as one of the three composite-boundary properties, with an abstract "induction along the witnessing trace" discharge. The five worked examples explicitly verify P4★, P6, P7, and P7a (e.g. the fork trace checks "P4★: Contains_C(Σ₂) ... ⊆ R₂" and "P7a: ... Every a ∈ dom(C₃) has at least one provenance entry"), but none checks P4a.
**Problem**: P4a is the most error-prone of the boundary properties — it is the only *trace* property, quantifying over historical states rather than the current one, and its discharge depends on the subtle K.ρ/K.μ⁺ ordering robustness. The standards require key postconditions verified against at least one concrete scenario; P4a is verified only abstractly. The fork example already produces a witnessing state (Σ₂ after K.μ⁺ witnesses `(a₁, d₂)`, `(a₂, d₂)`), so a concrete check is one line away and would exercise exactly the trace-witnessing mechanism the abstract discharge relies on.
**Required**: Add a P4a check to at least one worked example — e.g., in the fork trace, name the witnessing trace state for each new R-entry `(aⱼ, d₂)`.

## OUT_OF_SCOPE

### Topic 1: Forked arrangement / source-arrangement relationship, link discoverability under contraction, version-lineage/arrangement coupling
**Why out of scope**: These are already listed by the ASN as Open Questions and are genuinely new territory (relations between documents' arrangements, transitive transclusion provenance), not errors in the present transition model.

VERDICT: REVISE
