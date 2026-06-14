# Review of ASN-0131

I checked the mathematical content closely — RE-DEF and its derived guarantees (RE-ADDR, RE-SEL, RE-UDIST, RE-UDIST-∩, RE-RET, RE-CWP), the worked instance, and the stability sweep across the ASN-0047 vocabulary. The reasoning is sound: the antichain argument, the single-tuple-scope confinement of retraction, the wp derivations, and both intersection counterexamples (including the *injective* one) all check out, and the foundation citations are used correctly. I found no correctness or completeness gap. The findings below are prose-scoped — this note carries the `review-mode.anti-bloat` classifier, and the "Fresh emissions" section is where residual meta-prose has settled.

## REVISE

### Issue 1: Cross-model-transport defense accretes around a load-bearing derivation
**ASN-0131, "Fresh emissions and the addressable population"**: three sites carry the same defensive theme —
- "This is the content of ASN-0086's R0a/FlatLinkDomain, obtained here from ASN-0093's model-agnostic discipline directly — no cross-model transport."
- "We *posit* the commitment of ASN-0047's own system rather than transport it across reachable-state models: it is the regime under which we study addressability, and ASN-0086 — where the commitment holds at every layer-reachable state — is its source and consistency witness."
- "Two further facts feed the addressability argument, and neither needs ASN-0086's reachable states."

**Problem**: The antichain re-derivation from ASN-0093 is genuinely load-bearing (an ASN-0047 state with a populated arrangement is not reachable under ASN-0086's `→ = K.σ ∪ K.α ∪ K.λ`, so R0a as stated does not directly transfer — the derivation is correct to go through ASN-0093). But the prose wrapped around it is not reasoning; it is a defense of *why R0a isn't cited* and *why the discipline is posited rather than imported*. A precise reader must skip past "no cross-model transport," "rather than transport it across reachable-state models," "source and consistency witness," and "neither needs ASN-0086's reachable states" to reach the actual claims (dom(Σ.L) is an antichain; the discipline's unit-depth to-sets; `nullified` is a Σ.L-function). This is the "new prose around an axiom explains why the axiom is needed rather than what it says" pattern, repeated.

**Required**: State the standing assumption flatly ("We assume the relational-layer discipline of ASN-0086: every store transition that grows the retraction slice `L_Θ` is a `Nullify`; consequences used — every `L_Θ` to-set is unit-depth at a link target, and `nullified` is a function of `Σ.L` alone"), keep the ASN-0093 antichain derivation, and strip the methodology-defense sentences. The argument survives intact; only the anticipated-objection prose goes.

### Issue 2 (minor): Parenthetical imagines a precondition-excluded case, then defers it
**ASN-0131, "Under retraction"**: "(This content-disjointness is exactly what the standing `W ⊆ s_C` obligation buys; the link-subspace case `W ⊆ s_L` lies outside this note's content-region scope and is reopened as Open Question 7.)"

**Problem**: The first clause is useful (it ties the disjointness to the obligation). The tail invokes `W ⊆ s_L`, a case the operation's own precondition (`W ⊆ s_C`) excludes, only to defer it to OQ7 — an imagine-and-defer that OQ7 already records.

**Required**: Keep the disjointness-to-obligation connection; drop the `W ⊆ s_L` clause (OQ7 carries it).

## OUT_OF_SCOPE

### The note's seven Open Questions are correctly future territory
OQ1 (whole-endset vs. touching-spans return value — the operation is fully specified under the adopted RE-WHOLE reading, with `RE_clip` defined as the alternative), OQ4 (a *structurally-restricted sufficient* condition for intersection-equality — the note already supplies the exact necessary-and-sufficient touch-implication and proves no injectivity-style restriction discharges it), OQ5 (cross-store completeness), OQ6 (semantics of a type-slot match against content), and OQ7 (link-subspace regions) are genuinely new territory, not gaps in this note.
**Why out of scope**: Each defers a question the present operation neither needs nor under-specifies; RETRIEVEENDSETS over a content region is completely determined without them.

### The conservative-lift modelling assumption for ASN-0082 insert/delete
The note assumes shift-based insert/delete frame `Σ.L, Σ.E, Σ.R` (since ASN-0082 models only `(C, M)`). Re-deriving the displacement primitives in the full `Σ = (C, L, E, M, R)` state is a separate concern.
**Why out of scope**: ASN-0082 cannot prove a frame over components it does not model; the lift is appropriately flagged as an assumption, and discharging it belongs to whichever note re-homes insert/delete in the full state.

VERDICT: REVISE
