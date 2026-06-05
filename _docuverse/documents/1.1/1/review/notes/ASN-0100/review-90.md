# Review of ASN-0100

This is a substantively strong ASN: the three-region decomposition is sound, the disjointness/functionality arguments are correct, the closed-interval reduction for D-CTG★ is rigorous, every conjunct of ExtendedReachableStateInvariants is addressed, and both wp analyses are non-trivial. The findings below are forward-reference accretion and meta-prose (this note carries `review-mode.anti-bloat`), not correctness defects.

## REVISE

### Issue 1: Use-site inventory in the I3-identification paragraph
**ASN-0100, §Effect Three ("Identification with the foundation's post-insertion shift")**: "The invariant sections below invoke these directly for the Left and Shifted-right regions, supplying independent arguments only where I3 cannot reach: the INSERT-specific Insertion region (fresh content, §Effect Two), the cross-region disjointness that combines Insertion with Left ∪ Shifted-right, and the intermediate contraction state (§Atomicity), which has no I3 counterpart."
**Problem**: This sentence enumerates downstream consumers of the I3 inheritance rather than advancing Effect Three's reasoning. It is a roadmap of where later proof labor lives — exactly the "definition's introduction enumerates downstream consumers" pattern. The same I3-inheritance is then re-invoked at each use site (§Arrangement functionality, §Referential integrity, §Post-state V-position well-formedness), so the pre-announcement is redundant.
**Required**: Delete the inventory sentence. The core identification (INS.M-shift = I3 at S = s_C, and that INSERT fills the gap I3 vacates) advances reasoning and should stay; the catalog of which sections invoke what should not.

### Issue 2: Defensive justification of proof structure in §Atomicity
**ASN-0100, §Atomicity and Canonical Order**: "The I3-* family (ASN-0082) characterises only this *final* arrangement M'(d) — it is a single-step post-insertion postcondition, not a statement about substrate intermediates. ... requires the independent argument given below; this is the scope within which the substrate-composite realization genuinely cannot use I3."
**Problem**: The trailing clause justifies why the proof is structured as it is rather than proving anything; "genuinely cannot use I3" is reviser drift. The single-step-vs-intermediate observation also duplicates the point already made in §Effect Three.
**Required**: Keep the one fact that is load-bearing (the post-K.μ⁻ contraction state has no I3 counterpart and needs the argument that follows). Drop the meta-justification clause and the duplicated single-step framing.

### Issue 3: Repeated deferral to INS.proj with deferral prose
**ASN-0100, §A Worked Example**: "...is deferred to INS.proj (§Coverage and link discoverability), where the projection-shift correspondence is stated and derived in general."
**ASN-0100, §Cross-document independence (Q3)**: "This is the d' ≠ d case of INS.proj (§Coverage and link discoverability), the canonical home for the projection-shift correspondence across all d'; we cite it here rather than re-run the LP4-composition argument it already carries."
**Problem**: Multiple paragraphs in different sections defer to the same downstream location, and the second adds explicit deferral-justification prose ("we cite it here rather than re-run..."). This is the "multiple paragraphs defer to the same downstream location" pattern compounded with document-ordering justification.
**Required**: Cite INS.proj once where the result is actually used (the cross-document frame is established by INS.frame.doc independently; the projection extension only needs a bare cross-reference). Remove the "we cite it here rather than re-run" justification.

## OUT_OF_SCOPE

(none — the ASN respects its declared scope boundaries; the INSERT-vs-COPY section fixes only INSERT's identity character and defines no COPY claims, and the empty-document/re-insertion worked examples are legitimate boundary cases, not drift.)

VERDICT: REVISE
