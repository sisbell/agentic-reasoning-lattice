# Review of ASN-0131

This is a careful, largely sound note. The core definition (RE-DEF), the soundness/completeness biconditional (RE-SND/RE-CMP), the union law (RE-UDIST), the one-sided intersection law with its non-injectivity counterexample (RE-UDIST-∩), the contraction weakest-precondition (RE-CWP), and the worked example all check out under scrutiny. The stability analysis is exhaustive over the ASN-0047 transition vocabulary. The issues below are a load-bearing-lemma misattribution, one conditional guarantee resting on unestablished behavior, and forward-reference accretion the anti-bloat classifier directs me to surface.

## REVISE

### Issue 1: RE-ADDR leans on `wp` Case 2, which governs only triple (`Emit_K`) emissions

**ASN-0131, "The unit of the answer" (RE-ADDR paragraph)**: "whether that fresh output is *addressable* in its post-state (`ℓ_new ∉ nullified(Σ')`) is settled by `wp` Case 2 (ASN-0086)." RE-ADDR itself: "a fresh `K.λ` output that does not retract its own emitter address is addressable in its post-state … in particular every non-retraction emission (`K ≁ Θ`) is addressable."

**Problem**: `wp` Case 2 (EmitKWeakestPrecondition, ASN-0086) is `wp(Emit_K(Σ, d, F, G), (a, F, G) ∈ A_K^{Σ'})`, and `Emit_K` emits a **standard triple** `(F, G, K)`; `A_K`/`L_K` are the arity-3 slice. RE-ADDR is stated and used over *all* `K.λ` outputs (links are arity `≥ 3`, e.g. the general `ℓ_new` in the "under link emission" paragraph), including arity `> 3`. For a non-triple raw `K.λ` output, `wp` Case 2 does not typecheck (there is no `A_K` membership to compute), so it cannot "settle" `ℓ_new ∉ nullified(Σ')` for those outputs. The genuine, arity-independent justification is the one the note gives for the *third* conjunct — the standing unit-depth discipline plus R0a/FlatLinkDomain: every retraction to-set is unit-depth at an existing link `t`, `dom(Σ'.L)` is a prefix-antichain, so `t ⋠ ℓ_new` and no retraction to-set covers `ℓ_new`. That argument needs neither `wp` Case 2 nor arity 3. As written, the load-bearing lemma is mis-identified for the general case.

**Required**: State the arity-independent argument (discipline + R0a give `ℓ_new ∉ nullified(Σ')` directly) as the primary justification for RE-ADDR, and reserve `wp` Case 2 for the triple sub-case where its *second* conjunct (the non-self-targeting `a_emit ∉ coverage(G)`) is the operative one — i.e. the retraction emitter `b` in RE-RET, which is genuinely an `Emit_R`/`Emit_K` triple.

### Issue 2: RE-EDIT's shift-based insert/delete coverage rests on the unestablished natural-lift assumption

**ASN-0131, "Stability" (insert/delete paragraph)**: "What the lift does to `Σ.L`, `Σ.E`, `Σ.R` is not something ASN-0082 establishes; this note adopts it as an **assumption** (the *natural-lift assumption*): the lift of ASN-0082's `(C, M)` insert/delete to the full `(C, L, E, M, R)` state writes only `Σ.M(d)` and frames the rest …" RE-EDIT: "Extension to ASN-0082's shift-based insert/delete holds only **conditionally on the natural-lift assumption** … with delete scoped to text depth `#p = 2`."

**Problem**: The operation is motivated throughout by the user-facing edits (insert/delete that shift content), yet RE's stability under exactly those edits is delivered only *conditionally*, on behavior ASN-0082 does not establish, and the subsection then spends substantial prose managing that assumption (the `#p = 2` delete scoping, the discussion of a higher-depth interior-span delete the foundation "supplies no" primitive for, the unbackfilled-gap caveat). A guarantee resting on an unproven assumption is not a derived guarantee. Note that ASN-0082's I3/D-SHIFT primitives provably write only `Σ.M(d)` and frame `Σ.C` in their own model, so the only `L/E/R`-respecting lift is the framing one — there is nothing else such a lift *could* do.

**Required**: Either (a) discharge the lift — observe that the `(C,M)` insert/delete touch only `Σ.M(d)`, so the lift framing `L/E/R` is the unique extension, promoting "assumption" to a one-line convention and making RE-EDIT's coverage unconditional; or (b) confine RE-EDIT to ASN-0047's atomic movers (already covered unconditionally) and defer shift-based insert/delete to the ASN that establishes the displacement model on the full state. Either choice removes the conditional hedge and the assumption-management prose it drags in.

### Issue 3: Forward-reference accretion around the ASN-0086 bridge

**ASN-0131, "The unit of the answer" (standing-assumption paragraph)**: "Two ASN-0086 lemmas we invoke below — R-Scope (SingleTupleScope) and `wp` Case 2 (EmitKWeakestPrecondition) — reach just past '`Σ.L` alone': their `Σ.L`/`nullified` conclusions carry hypotheses over `dom(Σ.M)` and a derived emitter `a_emit(Σ, d)` … The bridge carries these too, because `dom(Σ.M)` is the *same* ASN-0093 document substrate …"

**Problem**: This is a use-site inventory — the paragraph names the two downstream consumers in advance and pre-justifies their hypothesis-transfer before either is used. The bridge *principle* (ASN-0086 lemmas constraining `Σ.L` transfer to ASN-0047 states because `Σ.L` evolves only via the shared `K.λ`) is legitimate and necessary; the accretion is the up-front per-lemma roadmap. Per the anti-bloat directive this is a flag at source: the inventory degrades the argument because a reader must hold "two lemmas below" in mind through several intervening sections before the payoff.

**Required**: State the bridge principle once as a general fact about `Σ.L`-only lemmas, and attach the lemma-specific hypothesis-transfer note (`dom(Σ.M)`/`a_emit` carry) at each use site — R-Scope in RE-RET, `wp` Case 2 in RE-ADDR — rather than inventorying them up front.

### Issue 4: Repeated content and defensive asides (anti-bloat)

**ASN-0131, "Anchoring reached through borrowed content"**: the point that anchoring is keyed to content identity is made at least three times — "anchoring is keyed to *content identity*, and our query is keyed to *content identity*"; the LP16 home-blindness restatement; and "Endset spans name content identity … not the borrowing V-position … so one endset is the same anchoring through every co-transcluder." **"Composing regions"**: "This is a genuine counterexample to `⊇`, not an unresolved question" — a defensive aside preempting an objection, immediately before Open Question 4 covers the same ground. **RE-ADDR paragraph**: "we settle it once"; **RE-CWP**: "a set of V-positions, distinct from the provenance relation `Σ.R` of the same ASN, which `RE` never reads (RE-LOC)" — meta-narration and parenthetical disambiguation that do not advance the surrounding claim.

**Problem**: These are repetition-for-emphasis and defensive justifications the reader must skip past. The content-identity point in particular is one idea stated three ways across one section.

**Required**: Collapse the transclusion section to one statement of the content-identity keying (it is the substance of RE-TRANS); drop the "not an unresolved question" aside (the negative settlement is already carried by RE-UDIST-∩ and OQ4); trim the meta-narration.

## OUT_OF_SCOPE

### The seven Open Questions are correctly deferred
RE-WHOLE-vs-touching-spans (OQ1), multiplicity preservation (OQ2), rendered-into-V-order answers (OQ3, RETRIEVEV territory), the intersection-equality refinement under arrangement restriction (OQ4), cross-store completeness (OQ5), type-slot-against-content matching (OQ6), and link-subspace region queries (OQ7) are all genuine future territory, not defects in this note. In particular OQ4 (whether injectivity recovers `RE(W₁ ∩ W₂) = RE(W₁) ∩ RE(W₂)`) and OQ6 (the lone exception to the `coverage(Θ) ∩ dom(Σ.C) = ∅` hypothesis in RE-RET) are the right things to leave open, given the counterexample and hypothesis are stated precisely. The note also correctly stays out of identity enumeration, counting, and pagination (RE-UNIT withholds identities and multiplicity by design).

VERDICT: REVISE
