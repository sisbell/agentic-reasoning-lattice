# Review of ASN-0100

This is a mature, heavily-worked specification. The forward proofs are sound: the seven worked examples each exercise a genuinely distinct path (interior/append/prepend/empty-doc/cleared-subspace/deep-subspace), the disjointness and closed-interval reductions are carried with their off-prefix cases live, and the invariant coverage matches ExtendedReachableStateInvariants + ExtendedTransitionInvariants without an obvious gap. I found no rigor defect. The findings are anti-bloat, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: L0's content conjunct deferred to one downstream location from two sections
**ASN-0100, §Atomicity (link-store bullet) and §Link store unchanged (L0)**: both say the second conjunct of L0 is "discharged ... in the per-address paragraph of §Post-state V-position well-formedness (S7 bullet)." The same per-address discharge is also pointed at from §Atomicity's "K.α and K.ρ frame M" paragraph, which adds "we do not repeat that discharge here."
**Problem**: This is the flagged pattern — multiple paragraphs in different sections deferring to the same downstream location. The reader must hold three pointers to one site to confirm a single fact (L0's content clause / per-address content invariants for `a_k`). The "we do not repeat that discharge here" sentence is pure cross-reference bookkeeping that does not advance the argument.
**Required**: Discharge L0's content conjunct once at its canonical site and let the other sites cite it by name without restating that the discharge happens elsewhere; drop the "we do not repeat ... here" meta-sentence.

### Issue 2: Document-organization narration around I3-coincide
**ASN-0100, §Effect Three**: "We record the consequence once, here, and cite it directly in the verification sections below without rebuilding the premise: on Left ∪ Shifted-right, M'(d) inherits I3-S2 ... I3-fin ..."
**Problem**: The inherited-lemma list is substantive content, but the framing clause "We record the consequence once, here, and cite it directly in the verification sections below without rebuilding the premise" narrates the document's citation strategy rather than the reasoning. It is meta-prose justifying the (correct) consolidation, not part of it. The same flavor appears in the INS.proj label "(INS.proj — canonical statement and proof)," where "canonical statement" implies non-canonical statements elsewhere and adds nothing.
**Required**: State the inheritance directly ("On Left ∪ Shifted-right, M'(d) inherits I3-S2, I3-S3, I3-VP, I3-VD, I3-fin from ASN-0082; the Insertion region is discharged separately wherever it bears"). Drop the citation-strategy narration and the "canonical statement" qualifier.

## OUT_OF_SCOPE

(none — the ASN correctly bounds DELETE/COPY/REARRANGE, link-subspace insertion, versioning, and BEBE in §Bounding the Scope without specifying them.)

VERDICT: REVISE
