# Review of ASN-0084

## REVISE

### Issue 1: ASN-0036's S8 is miscited as "SpanDecomposition"

**ASN-0084, R-SP, R-BLK, and throughout**: "S8 (SpanDecomposition)" / "S8's uniqueness of the maximal-run decomposition (ASN-0036)"

**Problem**: ASN-0036's S8 is titled **CorrespondenceRunPartition**, not "SpanDecomposition." The ASN consistently invents a different name for a foundation property. Per standard #7, an ASN must use the foundation's own notation rather than reinventing it.

**Required**: Replace every "S8 (SpanDecomposition)" with "S8 (CorrespondenceRunPartition)".

### Issue 2: Dangling foundation citations

**ASN-0084, State and Vocabulary**: "stripping the subspace identifier (per OrdinalExtraction, ASN-0036)"
**ASN-0084, R-NS / R-SP**: "ShiftPreservation (ASN-0036) gives the corresponding shift identities"; "The S8 corollary (preservation of subspace_I, zeros, and #E across runs)"

**Problem**: ASN-0036 (as extracted) exports no property named **OrdinalExtraction**, no **ShiftPreservation**, and S8 carries no stated corollary about `subspace_I`, `zeros`, `#E`. The ordinal-stripping operation corresponds to nothing in the foundation; the closest is `SubspaceProjection` (which extracts `v₁`, not the tail). These citations reference content the foundation does not establish, so the proofs that lean on them (notably the S8-corollary discharge in R-SP) are not grounded.

**Required**: Either cite the correct foundation property names, or — if these results genuinely don't exist in ASN-0036 — establish them in-ASN rather than citing them. Likewise reconcile "NAT-sub" (used in PermutationDisplacement/R-DISP) with the locally-defined "truncated subtraction"; "NAT-sub" reads as a foundation export but ASN-0034 has no such axiom.

### Issue 3: Use-site inventory — "OrdinalShift consumers under the identity extension"

**ASN-0084, after the `c₀ + 0 = c₀` convention**: "Each ASN-0034 consumer of OrdinalShift used below has a stated domain restriction. We record here, once, which extend uniformly to n = 0 … Subsequent invocations cite these consumers without re-deriving …" and "every 'by associativity' invocation in this ASN cites it"; "we do not repeat the case analysis at each consumer."

**Problem**: This is a downstream-consumer inventory plus citation-convention bookkeeping, not reasoning that advances the argument. The substantive content (n=0 extends for TS2/TS5/OrdShiftHom; TS4 does not) is one or two sentences; the rest is meta-prose telling the reader how citations will work later.

**Required**: Reduce to the load-bearing facts (the identity convention extends TS2, TS5, OrdShiftHom to n=0; TS4 requires n≥1). Delete the "we record here once / we do not repeat / every invocation cites" framing.

### Issue 4: R-NS "Dependencies and direction" and "Citation convention" are pure meta-prose

**ASN-0084, R-NS**: "We collect the consequences of this structural fact into one lemma, cited by R-PPERM, R-SPERM, R-COMM, R-BLK, and R-SP." … "R-NS is therefore upstream of the bijection lemmas: R-PPERM and R-SPERM cite R-NS(NS-π) … R-NS does *not* depend on the bijectivity …" … "Citation convention. Throughout the remainder of this ASN … the non-S case is dispatched by citing R-NS … without re-derivation."

**Problem**: These paragraphs enumerate consumers, justify document ordering and non-circularity, and announce a citation convention — exactly the forward-reference accretion patterns flagged for this note. None of it advances the lemma's content.

**Required**: Delete the consumer enumeration, the "upstream of / does not depend on" ordering essay, and the standalone "Citation convention" paragraph. The lemma statement and proof stand on their own.

### Issue 5: Reviser drift — prose imagining cases the preconditions exclude

**ASN-0084, Reduction of compound shifts**: "The identity convention extends each step to the j = 0, w_μ = 0, or w_β = 0 corner cases (although Width positivity … excludes the latter two from this ASN's scope)."
**PermutationDisplacement**: "The spurious carrier values (+, 0), (−, 0), and (0, n) with n ≥ 1 are never produced."
**PermutationDisplacement, non-S convention**: "the non-S clause is not needed for soundness but is stated separately to make explicit that …"

**Problem**: Each passage develops machinery for a case its own precondition rules out (w_μ=0, w_β=0 are excluded by Width positivity; "spurious" carrier values are never produced; a clause "not needed for soundness"). This is reviser drift — handling phantom cases — and should be removed at source rather than annotated as excluded.

**Required**: State the convention only over the cases that occur. Drop the parenthetical excursions into excluded/never-produced/not-needed material.

### Issue 6: Duplicated prose

**ASN-0084**:
- The two-stream / S0 argument — "The two-stream separation of the ASN-0036 state model — Σ.C and Σ.M(d) are distinct … makes 'Σ.C is unchanged' immediate" — appears in the *Invariant preservation* paragraph and again, nearly verbatim, in R-SP's S0 discharge.
- The S8a/S8(a) disambiguation note ("*S8a* without parenthesized clause … *S8(a)* with parenthesized clause …") appears in the *Invariant preservation* paragraph and again in R-SP.
- R-PPERM and R-SPERM each give the surjectivity argument twice: "on a finite set, every self-injection is a bijection" followed by "Equivalently — and exhibited explicitly for the reader —" a second ordinal-extent proof.

**Problem**: Two paragraphs saying the same thing in different words, repeated across sections; the "exhibited explicitly for the reader" second proof is redundant with the finite-self-injection argument.

**Required**: State each once. Keep one surjectivity proof per permutation lemma.

### Issue 7: Repeated deferrals to the same downstream locations / forward-reference justification

**ASN-0084, R-SP**: "The proof below invokes two results proved later in the ASN … R-BLK … and R-COMM …"; "computing the weakest precondition … is beyond the scope of this ASN"; "is left as the open question recorded above"; "the closing remark of R-BLK identifies this gap"; and in the Necessity sketches, repeated "necessity not claimed," "beyond the scope," "left as the open question."

**Problem**: Multiple paragraphs defer to the same downstream/forward locations and re-announce the sufficiency-only framing several times — accretion that compounds across cycles.

**Required**: Announce "this lemma establishes sufficiency, not the weakest precondition" once. Consolidate the deferrals; cite R-BLK/R-COMM where used without the preamble that they appear "later."

### Issue 8: "Width positivity" use-site inventory

**ASN-0084, Consequences of R-PRE**: "This consequence is used uniformly by R-PIV, R-SWP, R-DISP, and R-BLK without re-derivation; downstream invocations cite 'Width positivity' rather than a dropped precondition clause."

**Problem**: Consumer enumeration plus a defensive note about a "dropped precondition clause" — meta-prose, not derivation.

**Required**: End the consequence at the derived fact (w_α, w_β ≥ 1; w_μ ≥ 1 for n=4). Delete the consumer list and the dropped-clause justification.

## OUT_OF_SCOPE

### Topic 1: Composition of multiple rearrangements / k-cut generalization

**Why out of scope**: The Open Questions (k>4 cuts, closure under composition, run-count growth bounds, cut-vs-run-boundary constraints) are genuinely new territory and correctly deferred — they are not defects in this ASN's single-operation scope.

VERDICT: REVISE
