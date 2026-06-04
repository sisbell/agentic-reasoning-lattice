# Review of ASN-0076

The core construction is technically sound: EDITLINK as a two-K.λ composite is correctly discharged against ValidComposite★, the precondition discharges in E0 are complete (both first- and subsequent-emission sub-cases, freshness against both `dom(C)` and `dom(L)`, the `#E ≥ 2` induction), and the worked example exercises the key postconditions concretely. No correctness defect found in E0–E10. The findings below are accumulated meta-prose and duplicated argument — the patterns this cycle's classifier targets.

## REVISE

### Issue 1: E2 carries two independent proofs of the same conclusion
**ASN-0076, E2**: The first proof establishes `ℓ_new ≠ ℓ_old ∧ ℓ_sup ≠ ℓ_old ∧ ℓ_sup ≠ ℓ_new` fully via SequentialTransitionAxiom + L11a ("The conclusion does not depend on any property of EDITLINK beyond its consisting of two K.λ steps"). The following paragraph ("As a per-step confirmation that K.λ's freshness precondition... we discharge the two steps separately") re-derives the identical conclusion from the per-step freshness preconditions.
**Problem**: The L11a argument is complete on its own; the per-step re-derivation adds no new conclusion. A reader must work through two proofs to confirm one fact.
**Required**: Keep one. Drop the redundant per-step discharge (or demote to a one-line aside if it is needed to confirm the precondition is *enforced* at each site).

### Issue 2: The `τ_sup` supersession-type convention is deferred in four places
**ASN-0076, "The Supersession Relationship" / E4 caveat / Appendix Step 2 / Open Questions**: each separately states that no convention designates `τ_sup` as "the" supersession type and defers it downstream ("defers to a future ASN on type-endset conventions (see Open Questions)"; E4's "we do not — and cannot... claim... that ℓ_sup is *the* supersession"; Appendix "Step 2 — the supersession-type designation"; first Open Question).
**Problem**: Multiple paragraphs in different sections defer to the same downstream location — the forward-reference accretion pattern. The point is made once in "The Supersession Relationship"; the other three are restatements.
**Required**: State the `τ_sup`-convention deferral once (in "The Supersession Relationship") and let E4/Appendix/Open-Questions reference it without re-arguing it.

### Issue 3: E6's "Informal motivation" is an essay on an unformalized authorization model
**ASN-0076, E6**: The formal claim and its proof occupy two sentences (K.λ constrains only `d_new ∈ E_doc`). They are followed by ~three paragraphs introducing Alice/Bob/Carol, "trust models that weight claims," and "Nelson's broader posture" — all premised on "an unstated authorization model... not part of the abstract specification."
**Problem**: Essay content built on machinery the ASN explicitly states it does not formalize. It does not advance the formal claim; the precise reader skips it to reach the next claim.
**Required**: Compress to one sentence noting that selection/authorization of `d_new` is an application-layer concern deferred to a future authorization ASN. Drop the Alice/Bob/Carol trust discussion.

### Issue 4: E10 trailing paragraph restates its own proof
**ASN-0076, E10**: After the proof ("Each K.λ step... has frame `(A d :: M'(d) = M(d)) ∧ R' = R`"), the closing paragraph "The non-notification property is structural: K.λ's frame does not admit modifications to home(ℓ_old)'s arrangement, so EDITLINK performs no notification" says the same thing in different words.
**Problem**: Two passages in the same claim assert the identical fact.
**Required**: Delete the trailing restatement.

### Issue 5: "Why Editing Cannot Be Otherwise" and "On Identity" are motivational essay
**ASN-0076, §"Why Editing Cannot Be Otherwise" / §"On Identity"**: The load-bearing content of the former is a one-line contradiction (a mutating transition violates L12); the rest ("The dilemma is stark... There is no third path") is rhetorical padding. "On Identity" restates E1/E2/E9 and closes with a slogan ("links are immutable; relationships between links are claims; claims are themselves links") introducing no claim.
**Problem**: Essay content that does not advance reasoning beyond claims already proved.
**Required**: Reduce "Why Editing Cannot Be Otherwise" to the L12-contradiction observation. Cut "On Identity" to the one substantive point (address identity `ℓ_old ≠ ℓ_new` is settled by E2; the semantic relation lives in `ℓ_sup`, not in either link) or remove it.

## OUT_OF_SCOPE

None. The ASN correctly confines itself to link-edit semantics and explicitly defers INSERT/DELETE/COPY, forking, and authorization to other ASNs rather than defining claims for them.

VERDICT: REVISE
