# Review of ASN-0086

The mathematical core is sound — R0 through R7a discharge their obligations, the four-way conformance containment is carefully maintained, the worked sketch is internally consistent, and the antichain/contiguity machinery (R0a, L-ContiguousPrefix) is correctly layered. My findings are accretion-pattern and framing issues; this note carries the `review-mode.anti-bloat` classifier, and several meta-prose instances obstruct the argument.

## REVISE

### Issue 1: R0 postcondition prose enumerates downstream consumers
**ASN-0086, R0 (TupleAddressFreshness)**: "It is exposed here as a stated postcondition because downstream consumers (R5, Steps 3–4) cite the conforming post-state directly."

**Problem**: This justifies *why* the postcondition is exposed by inventorying its use sites, rather than advancing R0's meaning. A postcondition stands on its own; "R5 and Steps 3–4 use it" is PR-description content, not specification content, and it rots as consumers change. Matches the anti-bloat pattern "a definition's introduction enumerates downstream consumers."

**Required**: State the postcondition; delete the use-site justification.

### Issue 2: NestedLinkWitness separating-witness deferral repeated across three sites
**ASN-0086, Remark — NestedLinkWitness**: "The two conformance definitions below cite this construction as their separating witness." Then *Definition — state-local-conforming state*: "The separation is witnessed by the NestedLinkWitness construction above." Then *Definition — substrate-conforming state*: "The NestedLinkWitness construction above satisfies (b) yet is not the frontier successor…"

**Problem**: Three paragraphs in different sections point at the same construction to do the same separating-witness job — "multiple paragraphs in different sections defer to the same location." The Remark's forward pointer ("below cite this") is pure routing prose; the two definitions can each invoke the construction inline without the Remark pre-announcing that they will.

**Required**: Drop the Remark's closing forward-pointer sentence; let each definition cite the construction once where it needs it.

### Issue 3: wp Case 1 contains forward-deferral and essay content in a structural slot
**ASN-0086, WP Case 1**: "(Case 2 below discharges the section's non-trivial-wp obligation in full.)" and the trailing "*Non-weakestness.*" paragraph: "`P0 ∧ P1 ∧ PC` is sufficient but not weakest: PC's global antichain strictly over-constrains a postcondition local to `a`'s prefix-subtree."

**Problem**: The parenthetical defers the section's stated obligation to a downstream location — the standard "deferred to Y" pattern. The "Non-weakestness" paragraph then explains *why this case doesn't satisfy the section's purpose*, which is meta-commentary about document structure, not a result. Case 1 is a sufficient-precondition analysis; that is its content. Whether it also discharges the non-trivial-wp obligation is the reader's bookkeeping, not the proof's.

**Required**: State Case 1 as a sufficient precondition with its load-bearingness argument; remove the cross-deferral and the structural self-commentary.

### Issue 4: R7a Corollary re-derives the substrate-conforming-layer definition
**ASN-0086, Corollary (reduction to Emit_K), proof**: "Each state-affecting relational-layer operation is a single K.λ `→`-step … which satisfies clauses (a)–(c) by its ASN-0093 contract; the layer's only other operation, the read-only `Observe_K`, takes no transition and so trivially preserves conformance. Therefore the layer carries substrate-conforming states to substrate-conforming states."

**Problem**: This restates the *Definition — substrate-conforming layer* almost verbatim and then concludes the layer satisfies it — "two paragraphs say the same thing in different words." The definition already says "every operation it publishes … carries substrate-conforming states to substrate-conforming states." The corollary's proof should *check* the relational layer against that definition (one sentence: each op is K.λ or read-only), not re-narrate the definition.

**Required**: Compress to the membership check; do not reproduce the definition's body.

### Issue 5: wp Case 2 conjunct `K ∈ T_admissible` conflates operation-indexing with state-precondition
**ASN-0086, WP Case 2 Result and Derivation**: "`d ∈ dom(Σ.M) ∧ K ∈ T_admissible ∧ (…)`" with "dropping the second admits `K = ∅` … violating K.λ's `e₃ ≠ ∅` precondition (L3), so again no Σ' exists."

**Problem**: By *Definition — Emit_K*, the operation is *indexed by* `K ∈ T_admissible` — there is no operation `Emit_∅`. So `K ∈ T_admissible` is a well-formedness condition on which operation is named, presupposed before any state is examined, not a predicate over the pre-state Σ that a wp ranges over. Presenting it as a load-bearing wp conjunct ("dropping the second admits `K = ∅`") treats a non-existent operation instantiation as an admitted call. The wp's genuine free variables are `(Σ, d, F, G)`.

**Required**: Either move `K ∈ T_admissible` out of the wp body into the operation's standing index condition, or justify treating K as a quantified call-argument rather than a fixed index.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity of Emit vs. Observe and the consistency model for `A_K` transitions
**Why out of scope**: The note's Open Questions already flag this. A serialized single-authority model is assumed throughout (inherited via ASN-0093's SequentialTransitionAxiom); a concurrent observation model is new territory for a future ASN, not a gap in this one.

### Topic 2: Cardinality bound of `nullified(Σ)` relative to `dom(Σ.L)`
**Why out of scope**: Whether unbounded retraction is permitted or a structural ratio must hold is a substrate-policy question the note correctly defers; it does not undermine any claim made here.

VERDICT: REVISE
