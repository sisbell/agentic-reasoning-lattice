# Review of ASN-0086

This note carries the `review-mode.anti-bloat` classifier. The mathematical core (R0–R6, the wp analysis, the worked sketch) checks out: R0a's two-case antichain argument is sound, R-Scope's reliance on the antichain at Σ′ is correct, both wp derivations are genuinely weakest (the self-emit disjunct in Case 1 is correctly identified as the slack past `P0 ∧ P1`), CoverageEqualityDecidable's cell argument is complete, and the worked-sketch tumbler arithmetic is internally consistent. The findings below are accreted meta-prose, which the classifier asks me to surface.

## REVISE

### Issue 1: wp Case 2 restates "disciplinedness is derived and cited, not assumed" three times
**ASN-0086, Weakest-Precondition Analysis, Case 2**: the same claim appears in three adjacent locations:
- "Every layer-reachable state is unit-depth-disciplined — a *derived* invariant, established once by the Definition — relational layer discharge — so disciplinedness is not an independent domain hypothesis on the wp; we cite that discharge rather than re-assume it."
- "*Disciplinedness is what the formula leans on.* ... the Definition — relational layer discharge establishes it for every layer-reachable state, so we cite it rather than re-argue it here."
- (in the derivation) "By unit-depth-disciplinedness of Σ — the derived invariant cited above — ..."

**Problem**: Three sentences carry the identical content (disciplinedness holds on layer-reachable states, is established by the relational-layer discharge, and is cited rather than re-assumed) and all three defer to the same upstream location. This is meta-prose about wp bookkeeping, not the derivation. The "non-vacuous because a direct K.λ caller outside the layer could emit a crafted non-unit-depth retraction span" point is itself a fourth restatement of the same dependency.
**Required**: State the dependency once, at the point of use in the derivation ("disciplinedness — derived for layer-reachable states by the relational-layer discharge — gives that no pre-existing retraction covers the fresh `a`"), and delete the two standalone framing paragraphs.

### Issue 2: wp methodology framing prose does not advance either derivation
**ASN-0086, Case 1**: "The `→*`-reachability of Σ is the ambient domain assumption — it supplies R0a's antichain — not a separately droppable conjunct." **Case 2**: "...so disciplinedness is not an independent domain hypothesis on the wp..."
**Problem**: These sentences explain *why a conjunct is or isn't in the wp expression* rather than computing the wp. They are defensive annotations about the methodology ("not droppable," "not independent"). A reader following the backward substitution does not need them; they are arguing with a hypothetical objection.
**Required**: Drop the "not a separately droppable conjunct" / "not an independent domain hypothesis" asides. The domain over which each wp is stated is already named in the Result line.

### Issue 3: Observe_K "Pattern domain" justifies a design choice by counterfactual
**ASN-0086, Definition — Observe_K**: "Patterns range over the full tumbler space `T`, not the state-dependent address universe `A^Σ = dom(Σ.C) ∪ dom(Σ.L)`, so they can express ghost-targeting queries — by L9 (TypeGhostPermission) and L4 (EndsetGenerality), endset spans may target ghost tumblers, so a pattern restricted to `A^Σ` could not express the canonical 'does this tuple's from-endset cover ghost address `g`?' query."
**Problem**: The bulk of this is a defense of the choice against a rejected alternative (`A^Σ`-restricted patterns) — a counterfactual ("could not express...") rather than a statement of what the signature does. The operative content is one clause.
**Required**: Reduce to: "Patterns range over `T` (not `A^Σ`) so a pattern may target ghost addresses (L9, L4)."

### Issue 4: R1 back-defers to a proof embedded in a definition
**ASN-0086, R1**: "(Slice well-definedness — that `a` indexes exactly one coverage-class slice — was discharged in place at the *Definition — TypedRelation* union above.)"
**Problem**: The disjoint-union well-definedness proof sits inside *Definition — TypedRelation*, and R1 points back to it. A definition carrying a proof that a downstream lemma must reach back to is the forward-reference accretion pattern. The single-value/single-slice fact is one line; it belongs at R1's point of need or as a named one-line lemma, not buried in the definition with a cross-pointer.
**Required**: Either move the slice-uniqueness step into R1, or pull it out as a named lemma both the definition and R1 cite — not a "discharged in place above" parenthetical.

## OUT_OF_SCOPE

### Topic 1: Substrate-level enforcement of the unit-depth target-residency constraint
The Nullify contract makes `P1` (`a ∈ A_rel^Σ`) condition only the *postcondition* R-Scope, not execution; an undisciplined caller can emit a unit-depth retraction rooted at a non-link prefix `a` and, via R0a, nullify every link extending `a`. The note already raises this as an open question (elevating the unit-depth discipline to a substrate guarantee). It is correctly a layer convention here, not a defect in this ASN.

VERDICT: REVISE
