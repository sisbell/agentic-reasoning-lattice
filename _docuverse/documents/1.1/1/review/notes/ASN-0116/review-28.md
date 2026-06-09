# Review of ASN-0116

The technical core is sound and thorough. I checked the composite decomposition (K.α×n → K.μ⁻ → K.μ⁺ → K.ρ×n), the intermediate-state preconditions, the I3/I3-L/I3-CS transfer to the filled post-state, the block-disjointness arguments, the J0/J1★/J1'★/P7a coupling discharge, and the wp derivation in P6 — all hold, including the front-insert (J=1) full-clear, append (J=N+1), and empty-subspace boundaries. The worked example exercises P0/P1/P2/P4/P5/P6 plus two boundaries. Findings are confined to anti-bloat prose, which this note's `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: Navigational meta-prose in the composite section
**ASN-0116, "INSERT as a valid composite"**: "This section establishes only that the realization is a valid composite; the values themselves are fixed once, in the Effect."
**Problem**: This is an organizational note about where content lives, not a step in the argument. It tells the reader what the section is *not* doing rather than advancing the proof. Paired with the earlier deferral "the coupling constraints (clause 2) are checked only at the composite boundary, discharged in the provenance section below," the section carries navigational scaffolding that the precise reader must skip past.
**Required**: Delete the sentence. The section's role is evident from its content; the coupling deferral is licensed by the composite-validity discipline and needs no announcement.

### Issue 2: Foundation-vocabulary over-restatement
**ASN-0116, "INSERT as a valid composite"**: "applies only to a *valid composite*: a finite sequence of the atomic transitions `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ}` (K.μ~ being itself a named K.μ⁻+K.μ⁺ composite) in which each step's precondition holds at the *intermediate* state..."
**Problem**: This restates ValidComposite★ (ASN-0047, a foundation), and enumerates the full atomic alphabet including K.δ, K.λ, K.μ⁺_L and the K.μ~ parenthetical — none of which INSERT uses. The two clauses (intermediate-precondition, boundary-coupling) are what the argument needs; the alphabet listing is foundation surface the reader must filter.
**Required**: State the two ValidComposite★ clauses and name only the atomics INSERT actually sequences (K.α, K.μ⁻, K.μ⁺, K.ρ); drop the unused-atomic enumeration and the K.μ~ aside.

## OUT_OF_SCOPE

### Topic 1: Insertion at a transcluded / shared position; concurrent insertions; transclusion provenance; post-edit fragmentation
**Why out of scope**: These are exactly the four Open Questions the ASN itself defers, and they belong to ASN-0118 (transclusion), version/replication work, or future composite-concurrency treatment — not to the single-document, single-authority INSERT specified here.

VERDICT: REVISE
