# Review of ASN-0047

## REVISE

### Issue 1: Full-clearance decomposition mechanism stated near-verbatim in three places
**ASN-0047, *Decomposition of K.μ~* (Step (A), the sufficiency construction, and the trailing *Decomposition.* paragraph)**:

- Step (A): "The full-clearance decomposition clears the content subspace with K.μ⁻ (content-only removal) and rebuilds it with K.μ⁺, while every link-subspace position is retained by K.μ⁻ and framed by K.μ⁺."
- Sufficiency: "the full-clearance form ... is admissible for *every* admissible π without per-π precondition checks, since K.μ⁻'s suffix-removal precondition holds vacuously at the full-subspace suffix and K.μ⁺ writes at fresh positions."
- *Decomposition.* bullet: "This form works for *every* admissible π without per-π precondition checks: K.μ⁻'s suffix-removal precondition holds vacuously at the full-subspace suffix, and K.μ⁺ writes at fresh positions."

**Problem**: The last two are the same sentence reworded; the first is a third statement of the identical mechanism. Per the note's anti-bloat classifier, "two paragraphs in the same document say the same thing in different words" is a finding, and these patterns compound across cycles if left at source. The justification (vacuous suffix-removal precondition + fresh writes) belongs in exactly one location.

**Required**: State the full-clearance mechanism and its no-per-π-check property once (the sufficiency construction is the natural home, since that is where realisability of an arbitrary admissible π is discharged), and have Step (A) and the trailing *Decomposition.* paragraph reference it rather than restate it.

### Issue 2: Base-case uses unstarred D-CTG / D-MIN where the starred forms are meant
**ASN-0047, *Extended reachable-state invariants*, "Base" paragraph**: "S3★ and P4★ reduce to S3 and P4; S3★-aux holds vacuously since M₀(d) = ∅ for all d; D-CTG and D-MIN hold vacuously since V_S(d) = ∅ for every subspace S."

**Problem**: The invariant list of ExtendedReachableStateInvariants names D-CTG★ / D-MIN★ / D-SEQ★ (the per-subspace strengthenings); the unstarred D-CTG / D-MIN are the ASN-0036 forms with the link-subspace exemption, which this ASN explicitly supersedes. The base case must discharge the starred forms it claims to carry. The dedicated *Initial state invariant verification* block correctly names D-CTG★ / D-MIN★ / D-SEQ★, so the "Base" paragraph is internally inconsistent with it.

**Required**: Replace "D-CTG and D-MIN" with "D-CTG★, D-MIN★ (and the derived D-SEQ★)" in the proof's Base paragraph, matching the invariant list and the initial-state verification block.

## OUT_OF_SCOPE

### Topic 1: One-sided / type-only links (K.λ with empty from/to endsets)
**Why out of scope**: Whether K.λ should require `e₁ ∪ e₂ ≠ ∅`, and the semantics of one-sided vs. type-only markers in `same_type` and discovery unions, is genuinely new territory. The ASN already flags it in Open Questions; it is not an error in the present transition taxonomy, which correctly admits the orphan-link and `e₃ ≠ ∅`-only cases.

### Topic 2: Concurrent allocation against a shared home document
**Why out of scope**: Serialization vs. coordination-free distinct allocation under concurrency is a separate concern; SequentialTransitionAxiom (inherited) makes transitions atomic and totally ordered, so the question is deferred correctly and noted in Open Questions.

VERDICT: REVISE
