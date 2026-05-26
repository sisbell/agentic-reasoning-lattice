# Review of ASN-0076

## REVISE

### Issue 1: Foundation Recap overstates its completeness
**ASN-0076, "Foundation Recap" section**: The section closes with "We will need nothing else."
**Problem**: The proofs throughout the body cite numerous foundation items not listed in the recap — including T0, T1, TA5, TA5-SigValid, T4, T4b, T10a.7, T12, OrdinalDisplacement, L0, L1, L1b, L14, L-fin, SC-NEQ, SubAllocatorAxiom, SubspaceConventionAxiom, SequentialTransitionAxiom, ExtendedReachableStateInvariants, ExtendedTransitionInvariants, ValidComposite★, J0/J1★/J1'★, P0/P1/P2/P3/P4★/P4a/P7a. The "nothing else" claim is contradicted by the body.
**Required**: Either expand the recap to enumerate the additional foundation items the proofs draw on, or soften the closing sentence to acknowledge that further foundation items are cited at points of use.

### Issue 2: Step 2's discharge of `d_new ∈ E_doc` is implicit
**ASN-0076, E0 discharge of the supersession step**: The text discharges K.λ's clauses (i)–(iii) for Step 2 "by the same argument structure as sub-case (b) of the successor step, now applied at Σ_1," then enumerates the work for ℓ_sup ∉ dom(L), ℓ_sup ∉ dom(C), zeros, subspace, origin, and #E — but never explicitly states why `d_new ∈ Σ_1.E_doc` holds.
**Problem**: Clause (i) of K.λ's precondition is `d ∈ E_doc`. The composite precondition gives `d_new ∈ Σ.E_doc`; the lift to Σ_1 follows from K.λ's frame `E' = E` on Step 1, but this single line is omitted from the discharge.
**Required**: Add the one-line discharge: "d_new ∈ Σ_1.E_doc by K.λ's frame E' = E on Step 1, applied to the composite precondition d_new ∈ Σ.E_doc."

### Issue 3: E5's precondition phrasing weaker than what the proof requires
**ASN-0076, E5**: "For any state Σ satisfying all per-state invariants of ASN-0047's extended reachable state..."
**Problem**: The inductive step cites ExtendedReachableStateInvariants to claim "per-state invariants ... are preserved at every intermediate state." Strictly, ExtendedReachableStateInvariants is a theorem about states *reachable from Σ₀*; preservation by individual valid composites is a lemma in its proof, not the theorem itself. If Σ is merely a state satisfying the invariants (not necessarily reachable from Σ₀), the citation does not directly give preservation.
**Required**: Either strengthen E5's precondition to "for any reachable state Σ," or explicitly invoke the preservation-by-valid-composites lemma underlying ExtendedReachableStateInvariants rather than the theorem itself.

## OUT_OF_SCOPE

### Topic 1: Convention pinning τ_sup as the supersession-type address
**Why out of scope**: The ASN explicitly notes that "The semantics of distinguishing 'supersession-type addresses' from other type addresses — and any registry convention that pins τ_sup to a particular tumbler — are deferred to a future ASN on type-endset conventions." This deferral is appropriate; the link model alone cannot fix such conventions.

### Topic 2: Authorization model for who may invoke EDITLINK on which document
**Why out of scope**: E6's prose explicitly defers authorization to "a future ASN on authorization and capabilities." The abstract specification's K.λ has no executor field, so this belongs elsewhere.

### Topic 3: Termination and uniqueness of supersession-chain traversal
**Why out of scope**: The Appendix labels the reader procedure as illustrative and names this gap explicitly. The Open Questions section asks "under what conditions can such chains contain cycles?" — appropriate future work.

VERDICT: REVISE
