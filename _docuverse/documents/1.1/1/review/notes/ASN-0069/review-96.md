# Review of ASN-0069

This ASN is mathematically sound. I checked the V4/V4b inheritance derivation, the V11 chain induction (base, inductive step, the two-stage inclusion transport, and the closing equality chain), the V6a discoverability lemma (all three parts and both set inclusions), the K.δ + K.μ⁺ + K.ρ×n composite verification against ValidComposite★, and the empty-source K.δ-alone branch. The proofs hold and edge cases (empty source, first vs. subsequent fork, sibling vs. chain forks, post-fork deletion) are covered. The findings below are anti-bloat trims, per the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: V6a(iii) ⊆-direction carries a use-site meta-note
**ASN-0069, §"Subspace Selectivity", V6a clause (iii) ⊆-direction**: "(V4's universal supplies both conjuncts directly given `v ∈ V_{s_C}(d_op)` in the premise; V4b — the domain-equality commitment — is not consulted in this direction)."
**Problem**: The clause "V4b ... is not consulted in this direction" advances no reasoning — it is a use-site annotation about which lemma is/isn't invoked, exactly the meta-prose the anti-bloat pass targets. The ⊆ derivation already cites V4 for both conjuncts; the reader does not need to be told what was *not* used.
**Required**: Delete the "V4b ... is not consulted in this direction" aside. The ⊇ direction legitimately cites V4b where it is actually used; the contrast note adds nothing.

### Issue 2: K.δ precondition enumeration restated in both sub-cases after promising to state it once
**ASN-0069, §"The Fork Composite", K.δ sub-cases A and B**: intro states "Four preconditions are discharged identically in both sub-cases ... we state them once," then sub-case A reads "The K.δ outer preconditions are `e ∉ E ∧ T4-valid(e) ∧ ¬Element(e)`; the uniform Case (ii) precondition is `parent(e) ∈ E`" and sub-case B repeats the identical enumeration verbatim.
**Problem**: The shared precondition list is enumerated three times (intro plus both sub-cases), contradicting the "we state them once" factoring. Each sub-case then closes with "the remaining K.δ preconditions are the four shared discharges above" — so the re-listing is pure restatement that the reader must skip past to reach the sub-case-specific discharge.
**Required**: In sub-cases A and B, list only the per-sub-case precondition (k = 1: `t ∈ E_doc`; k = 0: `t ∈ E ∧ ¬Node(t) ∧ inc(t, 0) ∉ E`) and reference the shared four by the intro, rather than re-enumerating `e ∉ E ∧ T4-valid(e) ∧ ¬Element(e) ∧ parent(e) ∈ E` in each.

### Issue 3: NodeBaptism exclusion parenthetical explains why an axiom does not fire
**ASN-0069, §"The Fork Composite"**: "(NodeBaptism does not apply in either sub-case — it governs only K.δ events with `Node(e)`, while `d_new` satisfies `Document(d_new)`.)"
**Problem**: K.δ is invoked under Case (ii), whose contract already excludes `Node(e)`; the parenthetical re-derives this exclusion to preempt a question the contract structure already answers. This is the "new prose around an axiom explains why it doesn't apply" pattern.
**Required**: Drop the parenthetical; the Case (ii) routing already establishes `¬Node(d_new)` (stated as a discharge in the shared block).

## OUT_OF_SCOPE

### Topic 1: Concurrent fork while source is edited
**Why out of scope**: Raised as an Open Question; concurrency semantics beyond SequentialTransitionAxiom are new territory, not a defect here.

### Topic 2: Snapshot vs. living fork distinction
**Why out of scope**: The ASN commits to snapshot semantics (V10a, time-sensitivity); admitting living forks is a future design axis.

VERDICT: REVISE
