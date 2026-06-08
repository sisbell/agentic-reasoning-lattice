# Review of ASN-0102

I checked the displacement/tiling arithmetic, the wp computation for S3★, the per-state and transition invariant discharge in X14, and all five worked examples. The core mathematics is sound: the three-class tiling in X16 closes (unmoved `[1,p)` ∪ copied `[p,p+W)` ∪ displaced `[p+W,n_S+W]` with `1 ≤ p ≤ n_S+1`), the boundary cases (empty subspace `n_S=0`, append `p=n_S+1`, self-transclusion overlap, coalescing) are each instantiated and verified, and the invariant discharge covers every conjunct of ExtendedReachableStateInvariants. The findings below are accretion/clarity issues, consistent with this note's anti-bloat classifier.

## REVISE

### Issue 1: Stale "three" count heading a six-claim section
**ASN-0102, "What invariants the completed operation must maintain"**: "Three further obligations bind the post-state."
**Problem**: The section that follows contains six claims — X10 (SourceHandling), X11 (CrossOriginSeparation), X12 (BoundaryAbsorption), X13 (Multiplicity), X14 (ContainmentRecording), X15 (Atomicity). The count "three" is a stale artifact from an earlier version with fewer claims; a precise reader counts to six and stops to reconcile.
**Required**: Drop the numeral (e.g., "Further obligations bind the post-state.") or correct it.

### Issue 2: X14 residual meta-prose referencing a stripped apparatus
**ASN-0102, X14**: "...they are that composite's obligation, not the elementary step's, and we do not re-prove them here **with a private boundary apparatus**." and "COPY's contribution to the composite couplings is therefore (SL) together with X1, **requiring no boundary reconstruction**."
**Problem**: Both phrases describe what the ASN is *not* doing and point at a "boundary apparatus" / "boundary reconstruction" that no longer exists in the note (it was removed in a prior cycle). This is reviser-drift scar tissue: it justifies an absence rather than advancing the claim, and the reader must skip it.
**Required**: Delete the trailing clauses. "...not the elementary step's." and "...is therefore (SL) together with X1." carry the full content.

### Issue 3: Composite-boundary deferral (P4★/P4a/P7a) stated three times
**ASN-0102, X14** (paragraph 1): "...the composite-boundary properties (P4★, P4a, P7a) are evaluated by ValidComposite★ only between an embedding composite's initial and final states; they are that composite's obligation..."
**ASN-0102, X14** (final paragraph): "The composite-boundary properties P4★, P4a, P7a are not in this list: they are evaluated only at composite boundaries, so an embedding composite discharges them..."
**ASN-0102, Claims table, X14 row**: "...boundary properties P4★/P4a/P7a follow from (SL) + ValidComposite★ boundary checks, not re-proved here."
**Problem**: The same deferral assertion appears in three places. This matches the flagged pattern "multiple paragraphs defer to the same downstream location." The first statement establishes the principle and the couplings paragraph does the substantive J0/J1★/J1'★ work; the final paragraph and the table row restate the deferral without adding reasoning.
**Required**: State the deferral once (paragraph 1 is sufficient, since it already names all six items). Collapse the final paragraph to whatever residue is genuinely new (the per-state-list exclusion can be a half-sentence) and strip the restatement from the table row.

## OUT_OF_SCOPE

None beyond the Open Questions, which are already correctly framed as forward work (re-displacement of copied content, transitive containment when a reference-holder is itself referenced, time-varying views, reachability of the allocating document).

META: The ASN remains properly abstract — it specifies state changes, an operation, and invariants, using Gregory's trace only as confirmation; no termination warranted.

VERDICT: REVISE
