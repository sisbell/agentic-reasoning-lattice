# Review of ASN-0131

This is a mature, carefully constructed note. I verified the core machinery in full: RE-DEF and its locality/determinism (RE-LOC), the overlap-vs-containment argument (RE-OVL), the boundary cases (RE-BND), the worked instance (the `[a₂, a₄)` coverage, the `e₃` field-agreement disjointness, the dedup to `{(1, e₁)}` — all check out), union-distributivity and the non-injective intersection counterexample (RE-UDIST / RE-UDIST-∩), the discovery-side selection identity (RE-SEL), the contraction weakest precondition (RE-CWP, including the `R = ∅` boundary and the "strictly finer than D-CWP" claim), and the retraction iff (RE-RET, both directions, via R-Scope and R6a). RE-ADDR's self-emit caveat is non-vacuous and correctly not invoked in the withdrawal scenario. No correctness errors in the operation, its claims, the wp analysis, or the stability catalogue.

Two issues remain.

## REVISE

### Issue 1: The Σ.L-evolution bridge over-generalizes and elides its load-bearing step

**ASN-0131, "The region, and what it resolves to" → "The unit of the answer" (the bridge paragraph)**: "the link store evolves identically under ASN-0086's transition relation and under ASN-0047's, and every ASN-0086 lemma whose conclusion constrains Σ.L or nullified holds at every ASN-0047-reachable state."

**Problem**: This bridge is not optional decoration — it is what licenses importing ASN-0086 lemmas (R0a, R-Scope, R6a, computability of `nullified`) whose own quantifiers range over *ASN-0086*'s `→*`-reachable states, into a note that operates in ASN-0047's transition vocabulary. So getting it tight matters; RE-ADDR rests on R0a, and RE-ADDR in turn underwrites both the RE-UDIST-∩ counterexample and RE-RET.

Two defects:

1. **The justification skips the step that actually makes it true.** "Σ.L evolves only through K.λ" establishes that the *transition steps* on Σ.L coincide, but transferring a lemma quantified over *all* `→*`-reachable states requires that every ASN-0047-reachable Σ.L-configuration is also ASN-0086-reachable. That is non-obvious precisely because ASN-0086 grows `dom(Σ.M)` via K.σ while ASN-0047 grows it via K.δ — and K.λ's home-document precondition is evaluated against those differently-built document sets. The missing observation is that every K.δ-created document is T4-valid with `zeros = 2` (M0, ASN-0093), hence K.σ-registrable, so ASN-0086 can stage the identical homes and replay the identical K.λ sequence; therefore ASN-0047 Σ.L-reachable ⊆ ASN-0086 Σ.L-reachable, and only *then* does a `∀`-quantified ASN-0086 Σ.L-lemma carry over. The note asserts the conclusion ("evolves identically") without this inclusion step.

2. **"every ASN-0086 lemma" is broader than anything used or justified.** Only R0a/FlatLinkDomain, R-Scope, R6a, and the computability of `nullified` are imported. A blanket universal over all Σ.L/nullified-conclusion lemmas is a defensive over-claim.

**Required**: Either supply the reachability-inclusion step (K.σ registers every document K.δ can create ⟹ ASN-0047 Σ.L-reachable ⊆ ASN-0086 Σ.L-reachable), which makes the transfer sound, or narrow the bridge to the specific lemmas the note actually imports.

### Issue 2: Open Question 7 carries embedded analysis rather than posing a question

**ASN-0131, "Open Questions", item 7**: "What must a region query guarantee when its V-positions are drawn from the link subspace (`subspace(v) = s_L`) … — resolving, by S3★ (ASN-0047), to an image inside `dom(Σ.L)` (link addresses, not content), so that the touch test surfaces anchoring aimed at links (the to-endsets of retraction emitters, type endsets) and the exactness of retraction stability acquires an extra term for the retraction emitter `b`, whose to-set then meets the image?"

**Problem**: OQ1–OQ6 are crisp single questions; OQ7 is a multi-clause mini-analysis that pre-answers itself (it derives `image ⊆ dom(Σ.L)`, identifies which anchoring would surface, and concludes retraction stability "acquires an extra term"). The content is correct — for `W ⊆ s_L`, S3★ does place the image in `dom(Σ.L)`, and the Nullify emitter `b`'s to-set targets `ℓ ∈ dom(Σ.L)`, so it would meet the link-image — but that is essay content in a structural slot. A question slot should state the open question; the partial resolution belongs in the stability section (as a noted exclusion) or in the future ASN, not folded into the question.

**Required**: Reduce OQ7 to the question it poses (region queries over the link subspace), moving the `image ⊆ dom(Σ.L)` / extra-emitter-term observation into the stability narrative as an explicit scope exclusion, or drop it.

## OUT_OF_SCOPE

None beyond what the note already scopes. The open questions (entirety-vs-touching-spans extent, multiplicity preservation, rendered-into-V-order answers, intersection-equality under injectivity, non-co-resident link stores, type-slot meaningfulness, link-subspace regions) are correctly held as future work rather than smuggled in as claims, and RE-WHOLE is honestly marked provisional pending OQ1.

VERDICT: REVISE
