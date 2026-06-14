# Review of ASN-0131

I worked the definition, the worked instance, the union/intersection algebra, the wp derivations, and the stability case-split against the foundation contracts. The core operation (RE-DEF, RE-SND, RE-CMP, RE-OVL, RE-BND), the decidability argument, the worked instance's four touch tests and the `coverage(e₃) ∩ dom(Σ.C) = ∅` field-agreement proof, the union-distributivity proof and the intersection counterexample (a valid M13/M14 sharing construction), RE-SEL, RE-CWP, RE-ADDR, and the retraction argument (R-Scope-bounded, hypothesis-gated) all check out. Two issues remain.

## REVISE

### Issue 1: The insert "strip to ∅" describes a state the standing invariants exclude

**ASN-0131, "Stability: the answer as the document is edited"**: "so an insert whose unbackfilled gap falls under `W` can strip the image without replacement — down to `∅` when the gap swallows `W` entirely (`W ∩ dom(Σ'.M(d)) = ∅`)."

**Problem**: The shift primitive (I3) leaves the vacated positions `[p, shift(p, n))` out of the domain (I3-V, ASN-0082) and **does not backfill** them. The resulting `V_{s_C}(d)` then has an interior gap — `{1..j−1} ∪ {j+n..N+n}` in last-component terms — which violates D-CTG★/D-SEQ★, members of `ExtendedReachableStateInvariants` (ASN-0047). Tellingly, ASN-0082's insertion lemmas (I3-VD, I3-VP, I3-S2, I3-S3, I3-fin, I3-S7) include **no** D-CTG preservation lemma (D-CTG-post is established only for the contraction/delete), confirming the shift alone breaks contiguity. So the post-shift state on which "strip to ∅" rests is not a reachable state, and under SequentialTransitionAxiom (transitions atomic, uninterruptible) it is not independently queryable.

This is an internal inconsistency: the note inherits D-CTG★ as a standing invariant yet ranges over a transition ("ASN-0082's displacement primitives, taken in their own right") whose post-state violates it. The *observable* full insert (shift **+** backfill) restores contiguity and does **not** strip the image to ∅ — the gap positions hold the freshly placed content (which, being a new `K.α` allocation, a *tight* endset excludes by LP19a, so tight endsets do not newly touch it). The note's own "the fresh content a full insert places there is a separate content-placing step, not part of the primitive" concedes the gap state is a sub-step, yet the sentence above then asserts RE's value at it as if it were a resting scenario. (The delete side has no analogous problem — D-SHIFT closes its gap and D-CTG-post holds.)

**Required**: Either (a) tie the insert analysis to the full, contiguity-preserving operation (shift then backfill), stating the image's *replacement* (not unconditional stripping) and how tight vs. non-tight endsets respond; or (b) explicitly mark the post-shift gap configuration as a non-queryable intermediate of a non-atomic operation, not a state at which RE is evaluated. The load-bearing conclusion ("RE tracks the image's motion by membership," RE-IDENT) survives either way, but the "strip to ∅" illustration as written claims RE's value at a state D-CTG★ forbids. While here: RE-EDIT's "holds unconditionally" sits in tension with the same entry's "delete scoped to text depth `#p = 2`" — clarify that *unconditional* qualifies the M-only lift, not the delete's existence.

### Issue 2: The `Σ.L`-evolution bridge over-provisions `a_emit` coverage that is never exercised

**ASN-0131, "The unit of the answer: anchoring without names"**: "This identity reaches even past "`Σ.L` alone" — to lemmas whose `Σ.L`/`nullified` conclusions carry hypotheses over `dom(Σ.M)` or the derived emitter `a_emit(Σ, d)` ..." and the restated conclusion "every ASN-0086 lemma whose conclusion constrains `Σ.L` or `nullified` holds at every ASN-0047-reachable state, including the lemmas whose hypotheses name `dom(Σ.M)` or the derived emitter `a_emit(Σ, d)`."

**Problem**: The `dom(Σ.M)` half of this provision is load-bearing — R-Scope (SingleTupleScope) carries the hypothesis `d_retr ∈ dom(Σ.M)`, and the retraction argument needs it. The `a_emit` half is never used. R-Scope is invoked only through its `a ∈ A_rel^Σ` (P1) branch, with `a = ℓ ∈ dom(Σ.L)`; the note never invokes any lemma through an `a_emit`-hypothesis (R-Scope's self-emit branch and ASN-0086's wp Case 1/2 are not cited). RE-ADDR reasons about the fresh output directly via R0a + the discipline, not via an `a_emit`-hypothesis lemma. This is precisely the "definition's introduction enumerates downstream consumers" pattern with one consumer that does not exist. Additionally, the setup clause ("reaches even past `Σ.L` alone — to lemmas whose ... hypotheses over `dom(Σ.M)` or ... `a_emit`") and the conclusion clause ("including the lemmas whose hypotheses name `dom(Σ.M)` or ... `a_emit`") restate the same scope in different words.

**Required**: Drop the `a_emit` provisioning (and its supporting "computes `a_emit(Σ, d)` from the document operand `d` by one formula" clause); state the bridge once as "Σ.L evolves only through K.λ, so every ASN-0086 lemma whose conclusion constrains `Σ.L`/`nullified` — including R-Scope's `dom(Σ.M)` hypothesis — holds at ASN-0047-reachable states," collapsing the setup/conclusion duplication.

## OUT_OF_SCOPE

The seven Open Questions are appropriately scoped — OQ5 (non-co-resident link stores / replication) and OQ7 (link-subspace regions) in particular are genuine future territory, not gaps in this note. The deferral of OQ1 (whole-endset vs. touching-spans) and OQ2 (multiplicity) is acceptable because RE-DEF commits to a definite convention (whole-endset, deduplicated) and notes the alternative; the spec is complete as stated.

VERDICT: REVISE
