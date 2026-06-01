# Review of ASN-0047

## REVISE

### Issue 1: K.μ~ realisation keyed to `|dom_C(M(d))| ≥ 2`, contradicting its own sufficiency condition
**ASN-0047, *Decomposition of K.μ~* (Decomposition paragraph)**: "Here we give the realisation of K.μ~ when the existence condition holds. *Realisation of K.μ~ when the existence condition holds.* When `|dom_C(M(d))| ≥ 2`, K.μ~ is realised as *any* valid K.μ⁻ + K.μ⁺ pair…"

**Problem**: The operation's stated precondition is "`M(d)|_{dom_C(M(d))}` takes at least two distinct values," and the necessity/sufficiency analysis explicitly establishes that bare cardinality is *not* sufficient: "a constant-valued `M(d)|_{dom_C}` of cardinality ≥ 2 admits only net-identity permutations" and "this entails `|dom_C(M(d))| ≥ 2` but is strictly stronger." The closing caller-checked-precondition paragraph likewise excludes "any state in which every content V-position shares a single I-address by transclusion." Yet the Realisation paragraph asserts K.μ~ *is realised* whenever `|dom_C(M(d))| ≥ 2`. In a transclusion state (cardinality ≥ 2, all values equal), the precondition fails, clause (ii) has no witness, and no admissible π exists — but this paragraph claims realisation. The "existence condition" referenced in the header is the non-constant condition, but the realisation paragraph operationalises it as the wrong (cardinality) condition.

**Required**: Restate the realisation existence condition as "`M(d)|_{dom_C(M(d))}` takes at least two distinct values," matching the precondition and the sufficiency proof. Do not key realisation off `|dom_C(M(d))| ≥ 2`.

### Issue 2: P4a's trace-property status and design rationale restated across three+ locations
**ASN-0047, P4a definition box, ExtendedReachableStateInvariants intro, and Class (b) discharge**: The definition box says "This trace-existential reading is the design-correct one: provenance rides on the permanent I-address and survives deletion…"; the ExtendedReachableStateInvariants intro repeats "P4a is the lone *trace property* in this set (its witness need not inhabit the boundary state's arrangement — see its definition box)… Its discharge is read against the witnessing trace reaching the boundary, not against the boundary state alone"; the Class (b) discharge repeats again "P4a is a trace property, so its discharge is an induction along the witnessing trace, not a per-state check… Restoration at the composite boundary is *not* by re-deriving from history but by the post-state itself."

**Problem**: This is the same conceptual content (witness-need-not-be-current, restoration-by-post-state) stated three times in different words, with the definition box carrying pure rationale ("the design-correct one") rather than advancing the claim. The `review-mode.anti-bloat` classifier flags exactly this: "two paragraphs in the same document say the same thing" and "multiple paragraphs defer to the same downstream location (see its definition box)." A related smaller instance: the K.δ IsDocument case states "K.δ subsumes ASN-0093's K.σ" in the *Subsumption* paragraph and again as "This is exactly ASN-0093 K.σ's effect" in the Frame bullet.

**Required**: State the trace-property definition and its discharge mechanism once (at the definition box). At the discharge sites, cite it without re-explaining what a trace property is or why the reading is design-correct.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
The fork composite (J4) leaves the forked document's link subspace empty and explicitly defers a link-inheritance mechanism. This is correctly scoped out (and noted in Open Questions); no action needed.

META: not applicable — the ASN defines abstract state, transitions, and invariants that an alternative implementation would have to satisfy.

VERDICT: REVISE
