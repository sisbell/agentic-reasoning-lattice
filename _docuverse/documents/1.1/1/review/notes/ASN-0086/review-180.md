# Review of ASN-0086

## REVISE

### Issue 1: CoverageEqualityDecidable — soundness of the decision procedure silently depends on tumbler-line density, which the proof both omits and disclaims

**ASN-0086, Lemma — CoverageEqualityDecidable**: "An interval `[s, s ⊕ ℓ)` covers ... the gap `(c_k, c_{k+1})` iff `s ≤ c_k ∧ c_{k+1} ≤ s ⊕ ℓ` — each a finite conjunction of T2 comparisons, requiring no interior witness (so the density of the tumbler line is never consulted). ... Computing each coverage's indicator over the finitely many cells ... and comparing the two indicator vectors decides `coverage(e) = coverage(e')`."

**Problem**: The final step claims "indicator vectors equal ⟺ coverage sets equal." For the forward direction (sets equal ⟹ indicators equal) this is only valid if every gap-cell `(c_k, c_{k+1})` is non-empty *as a set of tumblers*. If a gap-cell contained no tumbler, both coverages would restrict to `∅` there regardless, yet the boolean gap-indicators (`s ≤ c_k ∧ c_{k+1} ≤ s ⊕ ℓ`) could differ — producing a false "unequal" verdict on genuinely-equal coverages. Non-emptiness of every gap is exactly tumbler-line density (between any `c_k < c_{k+1}` there exists `c_k.0` with `c_k < c_k.0 < c_{k+1}`, by T1 case (ii)/(i)). So density *is* load-bearing for the procedure's soundness — directly contradicting the parenthetical "the density of the tumbler line is never consulted." The parenthetical is correct only about the per-point membership test, not about the set-equality conclusion the procedure draws.

**Required**: Either (a) add the explicit step that every gap-cell is non-empty (cite the density witness `c_k.0`), establishing that gap-indicator equality faithfully reflects coverage-set restriction; or (b) restate the proof to draw set-equality only from cells known non-empty. Remove or qualify the "density never consulted" parenthetical, since the soundness of the decision rests on it.

### Issue 2: Defensive "generalizes verbatim" justification is made redundant by the induction it precedes

**ASN-0086, L-ContiguousPrefix, "Extension to substrate-conforming states"**: "The justification is that ChainMembershipForOrigin's per-`→`-step preservation generalizes verbatim to any transition satisfying conformance clauses (a)–(c): clauses (b) and (c) are precisely the per-step properties ... that drive that preservation, so the argument transfers to any (a)–(c)-preserving `↝`-step."

**Problem**: This sentence asserts a transfer-of-argument, then the very next sentences carry out a fully self-contained induction (base via EmptyInitialLinkStore, step via clauses (b)/(c)) that establishes the claim without appeal to any "verbatim generalization" of ChainMembershipForOrigin's internal proof. The defensive sentence neither supplies a step the induction lacks nor is consumed by it — it is meta-justification around a forward/foundation reference, exactly the accretion the anti-bloat mandate targets.

**Required**: Delete the "generalizes verbatim" sentence (and its sub-clause restating what (b)/(c) are) and let the explicit induction stand as the proof.

## OUT_OF_SCOPE

### Topic 1: Whether `#E ≥ 2` should be tightened to `#E = 2` at the substrate source

L-ContiguousPrefix-Cor1 proves `#E(a) = 2` at substrate-conforming states, while L1b admits `#E ≥ 2`; the NestedLinkWitness shows `#E > 2` is state-local-conforming. Reconciling the substrate-level admission is a substrate (ASN-0093/ASN-0043) design question, correctly deferred to the Open Questions, not a defect here.

### Topic 2: Concurrency / atomicity model for Observe vs Emit

Raised in Open Questions; this note's `→`/`↝` machinery is sequential per ASN-0093's SequentialTransitionAxiom, so a concurrency consistency model is genuinely future territory.

VERDICT: REVISE
