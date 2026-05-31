# Review of ASN-0093

The structural mathematics here is sound. I worked the chain disciplines, the FirstEmissionFreshness and Cross-document disjointness proofs, the C1c/L1c exhibitions, and the discharge matrix; the T10/T7 freshness arguments, the contiguous-prefix induction in ChainMembershipForOrigin, and the anchor-construction admissibility all check out, and the worked example correctly exercises both emission branches and both cross-document cases. The findings below are the residual meta-prose the `review-mode.anti-bloat` classifier asks to surface.

## REVISE

### Issue 1: Atomicity restated verbatim outside its axiom
**ASN-0093, "Substrate primitive operations" preamble**: "Each is atomic — its precondition is evaluated against `Σ` and its effect committed to `Σ'` in a single indivisible step; no intermediate state with the transition partially applied is admitted."
**Problem**: This is a near-verbatim repetition of SequentialTransitionAxiom ("each transition evaluates its precondition against `Σ` and commits its effect to `Σ'` in one indivisible step, with no intermediate state in which a transition has begun but not committed"). Two passages stating the same fact in different words — the named "same thing in different words" pattern.
**Required**: Delete the preamble restatement; cite SequentialTransitionAxiom if a pointer is wanted.

### Issue 2: Subsequent-emit freshness deferred forward from multiple sites
**ASN-0093, K.α and K.λ binding preconditions (subsequent-emit bullets)**: "Freshness of `a` against `dom(C) ∪ dom(L)` is discharged in the inductive step (see the C1c subsequent-emit exhibition and the L14 / ChainMembershipForOrigin rows of the discharge matrix)."
**Problem**: Both operations carry the same forward-deferral, and the matrix rows they point to in turn defer onward (to the chain exhibitions and DisjointSubAllocatorChains). This is the "multiple paragraphs in different sections defer to the same downstream location" pattern; a reader chasing freshness bounces through three sites before reaching the argument.
**Required**: State the freshness discharge once (the within-document / cross-document / cross-subspace split) and reference that single site from both ops, rather than threading deferrals.

### Issue 3: Citation bookkeeping in the Cross-document disjointness lemma
**ASN-0093, Cross-document disjointness lemma**: "The chain-level corollary — `A_L(d₁) ∩ A_L(d₂) = ∅` and `A_C(d₁) ∩ A_C(d₂) = ∅` — is ASN-0040's B7 (NamespaceDisjointness) directly, cited once here; the T10 any-extension claim above is the strictly stronger form."
**Problem**: "cited once here" and the corollary-vs-stronger-form comparison are bookkeeping about how the citation relates to the lemma, not reasoning that advances the lemma. The lemma's postcondition already states the T10 any-extension form.
**Required**: Drop the bookkeeping sentence; if the weaker B7 corollary is needed downstream, cite it at the use site.

## OUT_OF_SCOPE

(none — the deferred-topic enumerations in Scope are correctly scoped.)

VERDICT: REVISE
