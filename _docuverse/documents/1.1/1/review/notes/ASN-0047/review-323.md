# Review of ASN-0047

## REVISE

### Issue 1: Foundation property S8 mislabeled

**ASN-0047, *Amendments to existing transitions*, S8★ definition**: "S8★ states the per-subspace analogue of ASN-0036's S8 (SpanDecomposition)"

**Problem**: Foundation ASN-0036 names S8 *CorrespondenceRunPartition*, and ASN-0047 itself uses that correct name elsewhere (e.g., J4 step (ii): "S8★ follows from ASN-0036's S8 (CorrespondenceRunPartition)"). The S8★ definition is the lone site calling it "SpanDecomposition." A reader cross-checking the foundation will find no property by that name. Either the foundation reinvents a name it already has, or the citation is simply wrong.

**Required**: Replace "(SpanDecomposition)" with "(CorrespondenceRunPartition)" so the S8 citation is consistent throughout and matches the foundation.

### Issue 2: Invariant-preservation arguments duplicated between definition sections and the Class (a) matrix

**ASN-0047, S3★ / S3★-aux / D-CTG★ / D-MIN★ / S8★ (definitions vs. *Class (a)* matrix and its prose)**: The per-transition preservation of S3★ is stated in full three times — in the *Generalized referential integrity* section ("Existing transitions preserve S3★: K.α, K.δ, K.ρ hold M in frame; K.μ⁺ creates only content-subspace positions…"), in the matrix S3★ row, and again in the matrix's accompanying S3★ prose ("Established and preserved as per the dedicated paragraphs…"). S3★-aux carries a full inductive proof in its definition box *and* a matrix cell *and* matrix prose; D-CTG★/D-MIN★ and S8★ are likewise discharged twice.

**Problem**: This note carries the `review-mode.anti-bloat` classifier and asks specifically for "two paragraphs in the same document say the same thing in different words." The triple statement of the same case-by-case preservation argument is exactly that — the reader must reconcile three renderings to confirm they agree, which is work that does not advance the proof.

**Required**: Keep one authoritative discharge per invariant. Either the matrix cell *or* the prose paragraph should carry the load-bearing argument, with the other reduced to a pointer. The definition box should state the invariant, not re-prove preservation that the matrix already owns.

### Issue 3: The "content-scoped so it coexists with P7" and "composite-boundary (Class b)" classifications are restated past the point of navigation

**ASN-0047, P4★ definition + Properties Introduced (P4★ row) + *Extended reachable-state invariants* preamble**: "scoped to the content subspace so it coexists with P7" appears in the P4★ definition and verbatim-in-substance in the P4★ Properties row. Separately, the per-state/composite-boundary dichotomy is defined in the section preamble, restated in the ExtendedReachableStateInvariants definition, and restated a third time immediately after it ("P4★ and P7a are composite-boundary state-predicates — state-predicates guaranteed only at composite boundaries, not at every reachable state").

**Problem**: These are classification restatements, not reasoning. The third rendering of the dichotomy adds nothing the preamble and the definition did not already fix.

**Required**: State each classification once (preamble for the dichotomy; P4★ definition for the P7-coexistence rationale) and let the later mentions be bare references.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link/content withdrawal
The ASN's K.μ⁻ contracts by suffix removal only; interior withdrawal with compaction (the implementation's `DELETEVSPAN` renumbering) is correctly deferred to a future ASN and already listed as an open question. No revision needed here — modeling that operation is new territory, not an error in this transition set.

### Topic 2: Transitive-transclusion provenance guarantees
Provenance behavior across chains of transclusion (open question 1) is genuinely future work; the present R/K.ρ machinery is self-consistent without it.

VERDICT: REVISE
