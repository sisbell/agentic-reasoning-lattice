# Review of ASN-0047

This ASN carries the `review-mode.anti-bloat` classifier. The transition model is structurally sound — I checked the elementary transitions, the K.μ~ decomposition (Steps A/B, FIX, RANGE), the coupling discharges (J0/J1★/J1'★, P4★/P4a/P7a), the Class (a) matrix coverage, and the boundary cases (empty document, full clearance, interior-vs-suffix contraction, first-vs-subsequent emission). The verification carries. My findings are accretion/meta-prose at source, plus one structural redundancy.

## REVISE

### Issue 1: Use-site inventory appended to the Freshness-discharge note
**ASN-0047, *FrontierEquivalence → Freshness discharge (scope note)***: "The K.δ bullets, the S7d discharge, and the worked examples below invoke this note by name rather than re-deriving the contrast."
**Problem**: This is a use-site inventory — it enumerates downstream consumers of the note without advancing the note's content. It matches the named accretion pattern ("a definition's introduction enumerates downstream consumers... rather than advancing the definition's meaning"). The note's content stands on its own; the sentence is bookkeeping about how other sites cite it.
**Required**: Delete the sentence. The note's claim is self-contained; sites that cite it need no roster here.

### Issue 2: The "GlobalUniqueness gives cross-event distinctness, not freshness" contrast is restated at every K.δ site
**ASN-0047, multiple sites**: The scope note establishes the contrast once: "GlobalUniqueness (ASN-0034) establishes distinctness only *across distinct allocation events* ... never freshness itself." It is then re-derived, not merely cited by name, at: the K.δ k=1 bullet ("with GlobalUniqueness (ASN-0034) supplying only cross-event distinctness rather than freshness"), the k=2 routing, and worked-example Steps 2, 3, and 4 ("with GlobalUniqueness (ASN-0034) ... supplying only cross-event distinctness once freshness is granted").
**Problem**: The note exists precisely so these sites can invoke it by name (Issue 1's deleted sentence even promises this), yet each site re-states the same logical contrast. This is "two paragraphs say the same thing in different words," compounded across five sites.
**Required**: State the contrast once (the scope note), and at each use-site reduce to a bare citation ("freshness per the *Freshness discharge* note; cross-event distinctness by GlobalUniqueness") without re-deriving.

### Issue 3: TrackedEmission's "discharged separately" routing is repeated across five locations
**ASN-0047, *Extended reachable-state invariants***: The fact that TrackedEmission is discharged in its own definition box rather than the matrix is asserted in: the ExtendedReachableStateInvariants definition ("All per-state invariants except TrackedEmission are discharged cell-by-cell ... TrackedEmission is the one ... discharged separately"), the per-state-list note, the Class (a) proof intro, the standalone line "*TrackedEmission:* see its definition-box induction," and the Properties Introduced table.
**Problem**: Multiple paragraphs defer to the same downstream location (the TrackedEmission definition box). The routing is load-bearing once; four restatements are accretion.
**Required**: Keep one routing pointer (the ExtendedReachableStateInvariants definition), drop the others.

### Issue 4: K.μ~ column duplicates the elementary K.μ⁻ + K.μ⁺ cells in an induction declared over elementary transitions
**ASN-0047, *Class (a) verification matrix***: The proof states "Class (a) per-state invariants are proved by induction over *elementary* transitions," and K.μ~ is defined as a *named composite* (not elementary), expanding to K.μ⁻ + K.μ⁺. Yet the matrix carries a dedicated K.μ~ column whose cells restate the K.μ⁻ and K.μ⁺ cells (e.g., S8a/S8-depth: "K.μ⁻ restricts + K.μ⁺ finite-extends"; D-SEQ★: "derived from ... all discharged in their own K.μ~ cells").
**Problem**: For the *per-state* induction the two elementary columns already discharge every intermediate state of a K.μ~ instance; the K.μ~ column adds no per-state obligation and duplicates reasoning. The genuinely composite-specific results (LRP, K.μ~-S3★, K.μ~-FIX) are composite-boundary facts, not per-elementary-step facts, and already live in the K.μ~ decomposition section.
**Required**: Either drop the K.μ~ column from the elementary per-state matrix (its steps are covered by K.μ⁻/K.μ⁺), or relabel it explicitly as a composite-boundary summary distinct from the elementary induction so a reader does not double-count it as an inductive step.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link/content contraction
**Why out of scope**: K.μ⁻ models suffix-only contraction; interior `DELETEVSPAN` compaction-and-renumbering is a named-operation concern (DELETE/DELETEVSPAN), already correctly deferred to the Open Questions and excluded by the scope list. No action needed.

### Topic 2: Concurrent allocation under a shared home document
**Why out of scope**: SequentialTransitionAxiom assumes totally-ordered atomic transitions; concurrency/serialization of link allocation is operation-atomicity territory, correctly raised as an Open Question rather than resolved here.

VERDICT: REVISE
