# Review of ASN-0099

I checked every claim's derivation, the operation-vocabulary coverage (F9 over V∖{K.λ}, F9-λ for K.λ), the wp analyses (F21/F22/F23), the worked example's six queries, and the boundary cases (empty query, empty link store, ℛ=∅, partial run-cut in the image).

The math holds. Spot-checks I verified: F21's `project ∩ R ∩ ℛ` reduction (ℛ ⊆ dom(M(d)) makes the project-membership clause sound); F23's demonic wp weakening (LP9 gives project-monotonicity under K.μ⁺, so Q⟹wp(K.μ⁺,Q) at every successor, and wp postcondition-monotonicity closes it); F22's π-independence via LP11 range invariance; the `findlinks = ⋃ findlinks_filtered` arity-guard collapse; F13's existential-over-disjunction lift. Edge cases mandated by the rubric (empty document, full-document delete via ℛ=∅, cross-subspace image picking up link addresses) are all handled.

The two previously-declined findings (Coverage restatement, F4 Strengthening-1 witness) are correctly resolved in the current text — the Coverage block is absent, and F4 now carries the explicit "non-empty slots are load-bearing because coverage⊆I is vacuously satisfied by an empty slot" justification.

Anti-bloat pass: I looked for accreted meta-prose, forward-reference deferrals, axiom-rationale sub-paragraphs, and duplicated paragraphs. The factoring (ComprehensionInvariantUnderΣL stated once, reused by PerLinkInvariance and F8/F9/F15) is anti-duplication, not accretion. The dense nested-em-dash sentence in "The Image Set" is hard to parse but advances reasoning (run-intersections vs. full V-extents) — content, not noise. No flaggable accretion found.

## REVISE

None.

## OUT_OF_SCOPE

### Topic 1: Partial-region discoverability under reordering
F22 establishes reordering-invariance only for the full-document query (R = T). For a proper sub-region R, K.μ~'s bijection π can move the relevant V-positions in or out of R even though the global range is invariant, so a per-region wp would be needed. This is natural future territory, not a defect — the ASN scopes F22 to R = T explicitly.

**Why out of scope**: A new claim (per-region reordering wp), not a gap in F22's stated guarantee.

### Topic 2: Combined filtered-and-scoped operation
The ASN itself lists `findlinks_filtered_scoped(C, S, Σ)` under "What We Have Not Specified." Agreeing with that scoping.

**Why out of scope**: New operation definition, correctly deferred.

VERDICT: CONVERGED
