# Review of ASN-0100

This is a careful, well-instrumented note: it discharges the post-state invariants directly, verifies intermediate states, gives three worked examples (interior, append, empty), supplies two non-trivial wp computations, and derives the identity corollaries. Edge cases (position 0, append, empty document, m ≥ 3 depth, all-1 leading components) are genuinely covered. The findings below are residual-redundancy and one placement contradiction in the atomicity section, consistent with the anti-bloat classifier on this cycle.

## REVISE

### Issue 1: A bullet labeled "not admissible" concludes the opposite
**ASN-0100, §Atomicity and Canonical Order**: The header reads "The composite is *not* admissible in alternative decompositions that would break a per-state invariant at an intermediate:" and lists three bullets. The third bullet ("K.μ⁻ retaining strictly less than the Left prefix") concludes: "Such alternative decompositions are admissible and reach the same Σ'."
**Problem**: The third bullet contradicts its own section header. The first two bullets are genuine inadmissibility arguments (K.μ⁺-before-K.α breaks a precondition; K.μ⁺-without-K.μ⁻ breaks S2). The third is the opposite claim — an *admissible* alternative establishing post-state uniqueness — yet sits under the "not admissible" header.
**Required**: Move the `n'_{s_C} = 0` discussion to the uniqueness paragraph (where "Two representative comparisons confirm..." already lives), or relabel the header to cover both admissible and inadmissible alternatives. As written, the reader must reconcile a direct contradiction.

### Issue 2: Inter-step ordering constraints stated twice in the same section
**ASN-0100, §Atomicity and Canonical Order**: The constraint "K.μ⁺ requires its image in dom(C)" appears as non-admissible bullet 1 ("K.μ⁺ before K.α") and again as forced ordering 2 ("K.α(a_k) before K.μ⁺ placing a_k"). The constraint "K.μ⁻ must precede K.μ⁺ to avoid an S2/functional-extension violation" appears as non-admissible bullet 2 and again as forced ordering 4.
**Problem**: Two passages in one section say the same thing in different words — each ordering constraint is argued once as an inadmissible decomposition and again as a forced ordering, with the same supporting precondition.
**Required**: State each ordering constraint once. The "forced orderings" enumeration subsumes the inadmissible-decomposition bullets; fold the latter into the former (or vice versa) rather than carrying both.

### Issue 3: Cross-document projection invariance derived twice
**ASN-0100, §Cross-document independence (Q3) and §Coverage and link discoverability (INS.proj, d' ≠ d bullet)**: The Q3 section states "the projection from d' is unchanged, project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ) (LP4, ArrangementSpecificity, composed stepwise; ASN-0098)." The INS.proj d' ≠ d bullet re-derives the identical conclusion with the full stepwise-LP4 chaining argument.
**Problem**: The same result (cross-document projection invariance via per-step LP4 composition) is established in two sections with the same citation.
**Required**: Keep the derivation in one place (INS.proj, where the chaining detail belongs) and have the Q3 sentence point to it rather than restate the conclusion-plus-citation.

### Issue 4: The `#p = m_C` precondition is self-referential in the empty case
**ASN-0100, §The Operation: Formal Contract, State Preconditions**: "`#p = m_C` (the common depth of `V_{s_C}(d)` if non-empty per S8-depth; if empty, `m_C := #p` with `#p ≥ 2` ...)"
**Problem**: In the empty case `m_C := #p`, so the precondition `#p = m_C` reduces to `#p = #p` — vacuous — and the genuine constraint `#p ≥ 2` is carried only by the separate `ValidFirstInsertionPosition` precondition. A reader inspecting precondition 3 alone cannot tell what constrains `#p` in the empty case.
**Required**: Split the depth precondition into its two cases explicitly, or move the `#p ≥ 2` lower bound out of the parenthetical so the empty-case constraint is stated as a real obligation rather than buried as a definitional binding.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion, concurrent INSERTs, composition closure
**Why out of scope**: The Open Questions and §Bounding the Scope correctly defer link-subspace insertion (K.μ⁺_L semantics), concurrent-insert serialization, INSERT-with-INSERT composition closure, and derived document properties to future ASNs. These are new territory, not errors here.

VERDICT: REVISE
