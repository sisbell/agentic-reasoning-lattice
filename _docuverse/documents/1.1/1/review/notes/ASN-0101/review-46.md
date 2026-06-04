# Review of ASN-0101

I checked the operation specification (D0), the gap-closure and shift mechanics (D1), the seven preservation claims (D2–D8), the projection characterisation (D9), the ValidComposite★ extension (D10), and the weakest-precondition calculations (D11), including the worked examples and boundary-case traces.

The formal content is sound. D8's three-group discharge covers every per-state invariant of ASN-0047's ExtendedReachableStateInvariants theorem, the composite-boundary properties are correctly separated and handled as neutral-to-helpful, the wp algebra (including the partial-command negation and the cardinality collapse via the Λ⊎X⊎Π partition) checks out, and the boundary traces exercise the genuinely distinct discharge routes. I found no correctness errors. The findings below are bloat/meta-prose, which this note's `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: "Closing observations" is essay that advances no reasoning and duplicates earlier content
**ASN-0101, "Closing observations"**: "It is not destruction; it is not bytewise erasure; it is not a forking event that produces a new document." and "The breadth of the frame is the design choice. Any one of the preservation claims could have been negotiated away..."
**Problem**: The section restates the content-vs-destruction contrast already made fully in D2 ("In Xanadu, the bytes are not gone") and the cross-document/identity guarantees already established in D4/D5, then editorialises about negotiable design philosophy. No claim is stated, derived, or sharpened. This is essay content in a structural slot, and the destruction-contrast is now said three times (opening "The setting," D2, and here).
**Required**: Remove the section, or reduce it to a one-line pointer to the Claims-Introduced table. Delete the duplicated destruction-contrast prose.

### Issue 2: First atomicity reason is removable rationale; the second reason carries the argument alone
**ASN-0101, "The operation"**: "First, where the composite is well-formed it produces a strictly longer elementary-transition history than DEL: K.μ~ decomposes into K.μ⁻ + K.μ⁺ (ASN-0047), so the substitute runs three elementary steps where DEL runs one, and SequentialAtomicTransitions (ASN-0093) makes that history-length difference an intrinsic distinction between the two scenarios."
**Problem**: "History length" of an elementary decomposition is a modeling artifact, not an observable system guarantee — both scenarios reach the same final state where the composite is well-formed, so the only distinction is decomposition granularity. This is "why the axiom is needed" rationale. The *second* reason (link-subspace interior deletion has no admissible π under K.μ~ clause (v), so no composite substitute exists) is the load-bearing justification and suffices by itself.
**Required**: Drop the first reason; let the second reason justify DEL as a new transition kind.

### Issue 3: Boundary-cases closing summary re-narrates D8's discharge routes
**ASN-0101, "Boundary cases" (final paragraph)**: "the *route* by which each clause is discharged varies: when `V_S(M'(d)) = ∅` ... discharge vacuously ...; when `Λ = ∅` but `Q ≠ ∅` D-MIN★ requires a non-vacuous `σ_d`-witness ...; when `Π = ∅` ... inherit ... pointwise ..."
**Problem**: This paragraph re-states D8's Group (i) justification and the per-case bullets immediately above it, in different words. The same routing (vacuous / σ_d-witness / inheritance / two-summand) is already given in both places.
**Required**: Delete the summary paragraph; the per-case bullets already carry the content.

### Issue 4: D5 and D6 carry counterfactual/editorial prose that does not advance the claim
**ASN-0101, D5**: "Without D5, a deletion in `d` would have to either: propagate ... or prevent ... or somehow allow ..."
**ASN-0101, D6**: "This is a happy accident at the implementation level ..." and "Two unrelated mechanisms ... converge on the same abstract guarantee."
**Problem**: D5's three-way counterfactual imagines design alternatives the claim already excludes by frame condition — it argues significance rather than advancing the proof. D6's "happy accident" framing editorialises about implementation coincidence; the concrete implementation evidence (exponent guard, positional ordering) is fine, but the convergence essay around it is not.
**Required**: Trim D5's counterfactual to at most one sentence; keep D6's implementation evidence but drop the "happy accident / convergence" editorial framing.

## OUT_OF_SCOPE

### Topic 1: Full historical reconstruction of arbitrary prior states
**Why out of scope**: The "A note on recoverability" section correctly confines DELETE to supplying the *substrate* (D2 + D5) and defers the *mechanism* (versioning) to a future ASN. This is properly scoped; the open questions already flag the residual obligations. No revision needed — noted only to confirm the deferral is legitimate, not a gap in this ASN.

VERDICT: REVISE
