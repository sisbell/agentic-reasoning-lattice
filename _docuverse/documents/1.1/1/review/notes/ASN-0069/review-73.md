# Review of ASN-0069

## REVISE

### Issue 1: V5a duplicates the K.μ~ "not elementary" explanation
**ASN-0069, V5a**: The statement opens with a parenthetical — *"(The named composite K.μ~ is not elementary: ASN-0047 defines it as a K.μ⁻ + K.μ⁺ decomposition ... We therefore exclude K.μ~ from K_M and treat it through its two constituent elementary steps, both M-targeted at the same d_target — see the note in clause (a).)"* — and then clause (a)'s derivation restates it: *"The composite K.μ~ is handled by decomposition rather than as a single elementary step: it expands into a K.μ⁻ + K.μ⁺ pair, both M-targeted at the same d_target. If d_target ≠ d*, each constituent step preserves M(d*)..."*
**Problem**: The same fact (K.μ~ is non-elementary, treat via its two constituent steps both targeting d_target) is asserted twice in the same property — once in the statement, once in the derivation. The statement's "see the note in clause (a)" is a self-pointer to a paragraph that repeats it. This is the "two paragraphs say the same thing in different words" accretion pattern.
**Required**: Keep the decomposition fact in exactly one place (the derivation, where it is consumed). Reduce the statement-level parenthetical to "K_M lists only the three elementary kinds; K.μ~ is handled by decomposition in clause (a)."

### Issue 2: V8b's "Non-monotonicity" disclaimer is defensive meta-prose, and the property's machinery is unused
**ASN-0069, V8b**: The "Non-monotonicity" paragraph — *"Π_g is not monotone — later arrangement edits ... may remove or restore witnesses; by V5a(a), every step not M-targeted ... frames M ..."* — together with the table note *"(no monotonic-decay claim)"*.
**Problem**: This prose exists to explain what V8b does *not* establish (it is not the monotone-decay property a prior cycle apparently asked for). It advances no reasoning. Compounding this, V8b's apparatus (`Corr_g`, `F`, `Π_g`) is referenced nowhere downstream — V12, V10, V11, and the worked example never consume it — and its two postconditions reduce to trivial set facts (`F ∩ Corr_g ⊆ F`; `Π_{Σ'} = F` by V8). A property that proves intersection-is-a-subset and carries a paragraph disclaiming a stronger reading is accretion, not a load-bearing claim.
**Required**: Either delete V8b (its conceptual point — correspondence is fork-time-bounded — is already implied by V8 + V5a) or, if retained, drop the "Non-monotonicity" disclaimer and the "(no monotonic-decay claim)" table note. State only what is proved.

### Issue 3: V8 paragraph justifies *not* promoting a claim and defers to the worked example
**ASN-0069, §"Structural Correspondence", the paragraph beginning "V8 alone establishes correspondence..."**: *"The transitive d_src ↔ d_new correspondence for the subsequent-fork case ... is not a first-fork deepening chain and therefore lies outside V11's scope ... The transitive correspondence in that configuration is instead obtained by composing V8 ... the §"Subsequent fork of d_src" vignette of the worked example carries out exactly this composition. We do not promote it to a named claim."*
**Problem**: This is essay content explaining why a result is *not* a named claim and pointing forward to where it is informally exercised. It justifies a structural decision (non-promotion) and defers downstream rather than advancing the argument — the "prose justifies document ordering / defers to a downstream location" pattern. The reader must work past a meta-discussion of V11's scope to follow V8.
**Required**: Cut to the substantive content: either promote the transitive subsequent-fork correspondence to a (sub-)claim with its derivation, or state in one sentence that subsequent-fork transitivity follows by composing V8 at consecutive forks, without the scope-comparison and the "we do not promote it" justification.

### Issue 4: Dependency Audit carries justification prose beyond its accounting role
**ASN-0069, §"Dependency Audit"**: *"the freshness lemmas (ChildSpawnFreshness, FrontierEquivalence) consume the T10a.6/T10a.7 guarantees on our behalf rather than our re-deriving them."*
**Problem**: The audit's job is to record which dependencies are used and which are not. This trailing clause justifies *how* the foundation guarantees are reached — a use-site rationale that belongs in the discharge sites (which already cite T10a.6/T10a.7), not the audit.
**Required**: End the sentence at the enumeration of consumed lemmas; drop the "on our behalf rather than re-deriving" justification.

## OUT_OF_SCOPE

### Topic 1: Concurrent-modification guarantees during a fork
**Why out of scope**: The first Open Question (fork invoked while source is concurrently modified, beyond SequentialTransitionAxiom) is genuinely new territory — a concurrency model the present transition system does not provide. Correctly deferred.

### Topic 2: Snapshot vs. living forks
**Why out of scope**: Distinguishing frozen-at-fork-time from source-tracking forks (Open Question 3) introduces a new arrangement-coupling discipline not part of this operation's derivation.

META: not applicable — the ASN remains squarely about state, the fork operation on it, and its invariants; the findings are local accretion, not drift.

VERDICT: REVISE
