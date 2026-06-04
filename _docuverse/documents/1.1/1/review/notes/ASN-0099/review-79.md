# Review of ASN-0099

I checked the proofs and the math is sound: F1–F20a, the meta-lemma chain (ComprehensionInvariantUnderΣL / PerLinkInvarianceUnderValuePreservation), F9-λ's disjoint-union characterization, and the six-query worked example all hold, and the witnesses in F4 are valid (verified α.0 ∈ coverage but ∉ I, etc.). All cross-references are to foundation ASNs (0034, 0036, 0043, 0047, 0058, 0093, 0098), so no self-containment violation. The ASN defines an operation, its conformance obligation, and its preservation invariants at the abstract-state level — it has not drifted.

The findings below are the anti-bloat / meta-prose items the review mode asks me to surface.

## REVISE

### Issue 1: Completeness section closes by restating F2 ∧ F3
**ASN-0099, "Completeness"**: "Completeness must hold *unconditionally* with respect to `dom(Σ.L)`: any implementation whose `result(I, Σ)` differs from the comprehension is non-conforming."
**Problem**: Two sentences earlier the section already states "Together F2 ∧ F3 force `result(I, Σ) = findlinks(I, Σ)`." The closing sentence adds no new obligation — "differs from the comprehension ⇒ non-conforming" is exactly the contrapositive of the forced equality. It is skippable prose restating a theorem already on the page.
**Required**: Delete the closing sentence (the F2 ∧ F3 forcing already carries the unconditionality).

### Issue 2: F7 (EndsetSymmetry) restates the quantifier structure of the definitions
**ASN-0099, "Endset Filtering"**: "F7 ... (a) Slot symmetry: matches(a, I, Σ) consults all slots uniformly. (b) Filter conjunction: findlinks_filtered(C, Σ) intersects per-slot constraints ... Both halves follow from the quantifier structure of the definitions: existential ⇒ slot-symmetric; universal ⇒ conjunctive."
**Problem**: F7(a) is F1's existential `(E i …)` reread, and F7(b) is the universal `(A (i,J) ∈ C …)` of `findlinks_filtered` reread. The stated "derivation" concedes this — it is a tautology over definitions already given. A labeled claim whose entire content is "the definition quantifies the way it quantifies" does not advance the argument; the worked-example citations of F7(a)/F7(b) could point at F1 and the filtered definition directly.
**Required**: Remove F7 as a standalone claim, or fold the slot-symmetry / conjunction observations into the definitions of `matches` and `findlinks_filtered` as one-line remarks.

### Issue 3: F1's project-form/coverage-form reconciliation establishes an unused identity
**ASN-0099, "The Match Predicate"**: "F1 generalizes ASN-0098's `discoverable_from` ... The two coincide by LP12 ..., whose per-slot biconditional ... gives `discoverable_from(a, d, Σ) = matches(a, ran(Σ.M(d)), Σ)`."
**Problem**: F1 is self-standing as a definition; the LP12-derivation paragraph reconciling it with the foundation predicate produces the identity `discoverable_from = matches(a, ran(Σ.M(d)), Σ)`, but that identity is not consumed by any downstream claim. F11's contrast with `discoverable_from` ("distinct from ASN-0098's V-side ... not persistent") uses only the *concept*, not this equation. This is accretion around the foundation reference — derivation prose for a fact the rest of the ASN never uses.
**Required**: Reduce to a one-line orientation note ("F1's `matches` is the coverage-form generalization of ASN-0098's `discoverable_from`") and drop the LP12 derivation of the unused identity, or use the identity somewhere if it is meant to be load-bearing.

## OUT_OF_SCOPE

### Topic 1: Necessity (vs sufficiency) of the link-store-inert frame commitment
The third Open Question ("minimum structural commitment any conforming substrate must make...") asks a necessity question. A1a/F9 establish sufficiency (the current frames suffice for invariance); deriving the *minimal* commitment is a distinct investigation belonging to a future ASN, not a gap in this one.

### Topic 2: Audit witnesses, latency bounds, FOLLOWLINK inverse
The first two Open Questions and the "What We Have Not Specified" items (procedure, replication, caching, the V→endset inverse) are correctly deferred.

VERDICT: REVISE
