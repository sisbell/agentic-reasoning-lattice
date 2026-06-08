# Review of ASN-0102

I checked the COPY definition, the wp(COPY, S3★) reduction, every X-claim derivation, the coupling/invariant discharge in X14, and all five worked examples (cross-origin fragmented, self-transclusion-over-displacement, empty-subspace first insert, append, coalescing). The state/operation/invariant content is sound: the three-class effect partition is single-valued and total (X16 tiling), S3★ reduces correctly to C1, pre-state pinning (X10(b)/X15) forecloses self-transclusion circularity, and the composite-boundary discharge of J1★/J1'★/P4★/P4a via the BD dichotomy is coherent. I found no correctness gap.

The findings below are anti-bloat (this note carries `review-mode.anti-bloat`): forward-reference accretion and frame restatement that a precise reader must skip past.

## REVISE

### Issue 1: Source-designation section previews X8's merge result
**ASN-0102, "The source designation and its resolution"**: "The concatenated list of `k` blocks is not in general M7-maximal as a whole — an inter-reference boundary may itself satisfy the merge condition, so canonicalising the laid-down region can yield strictly fewer than `k` blocks (X8)."
**Problem**: This sentence states X8's within-region merge result (inter-reference boundary may coalesce → fewer than `k` blocks) and tags `(X8)`, where X8 then develops and proves the same point in full. The effect clause needs only `k`, `n_j`, `c_j` from this section — it does not need the merge behavior, which is purely a forward-reference preview of X8. This is the forward-reference accretion pattern: the preview advances no reasoning the section requires.
**Required**: Drop the merge-preview sentence here; let the section define `k = Σ k_i` (which the effect clause consumes) and leave the canonicalisation/merge claim to X8 where it is proved.

### Issue 2: X10(a) restates frame clauses already fixed in the COPY definition
**ASN-0102, X10(a)**: "No source document *other than the target* is altered: `(A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))`, and `Σ'.C = Σ.C`."
**Problem**: Both conjuncts are verbatim the COPY definition's frame ("Other documents — untouched" gives `(A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))`; "Content store — untouched" gives `Σ'.C = Σ.C`). X10(a) re-asserts the frame under a new name. The genuinely new content of X10 is (b), the snapshot-resolution guarantee for `d_s = d`, and the "in particular" specialization to source documents.
**Required**: Trim X10(a) to its specialization (the consequence for a source `d_s ≠ d`, with the X6 origin clause) rather than re-stating the frame the definition already pins.

## OUT_OF_SCOPE

### Topic 1: Re-displacement of copied content and continued discoverability
**Why out of scope**: The first Open Question (origin vs. discoverability under later displacement) is link-projection territory (the LP-series), not COPY mechanics. Correctly deferred.

### Topic 2: Reference-of-a-reference containment obligations
**Why out of scope**: The second Open Question concerns containment-record propagation when a referencing document is itself a source — a transition-model/provenance composition question for a later ASN, not a COPY revision.

VERDICT: REVISE
