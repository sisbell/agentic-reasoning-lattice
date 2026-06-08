# Review of ASN-0102

This is a careful, mathematically thorough specification. The displacement tiling (X16), the `wp(COPY, S3★)` reduction, the J0/J1★/J1'★ coupling discharges (X14), and the five worked scenarios (cross-origin, self-transclusion, empty-subspace, append, coalescing) are correct and exercise the boundary cases I would otherwise demand. I found no correctness gap. The remaining issues are forward-reference accretion flagged by this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Superfluous V-adjacency argument in X8's within-reference case

**ASN-0102, X8 (RunFragmentation)**: "resolve(d_s, σ) already returns the maximally-merged decomposition (ASN-0058, C1a/M12), so its blocks are pairwise non-I-adjacent, **and on the V-contiguous restriction domain — content-reference well-formedness places every depth-m span position in dom(M(d_s)), C0a confines them to a shared prefix — they are V-adjacent.** No within-reference boundary is a merge candidate"

**Problem**: The conclusion "no within-reference boundary is a merge candidate" follows from non-I-adjacency *alone* — the merge condition M7 requires both V- and I-adjacency, so failing either closes it. The bolded clause establishing V-adjacency is irrelevant to the conclusion. Worse, it argues V-adjacency from the *source* arrangement's contiguity (C0a, well-formedness), but the merge candidacy is evaluated on the *target* block set `B_copy`, where V-adjacency holds by construction (`c_{j+1} = c_j + n_j`), not by any source-side property. The clause is both superfluous and mis-located reasoning the precise reader must work around.

**Required**: Drop the source-contiguity sub-argument; rest the within-reference non-merging conclusion on non-I-adjacency from M12 alone.

### Issue 2: The Σ.R-vs-Contains_C distinction is drawn twice

**ASN-0102, Definition (Provenance)**: "This is a state component distinct from the *derived* containment relation `Contains_C` (which reads off `Σ'.M` automatically): the provenance relation `Σ.R` records the fact persistently."

**ASN-0102, X14**: "the *derived* content-containment relation records `Contains_C(Σ') ⊇ {(a_j + i, d)}`, while COPY's effect writes the corresponding pairs into the persistent provenance relation `Σ.R` (Definition)... This is a state component distinct from the *derived* containment relation `Contains_C`".

**Problem**: Both passages make the same persistent-`Σ.R` versus derived-`Contains_C` distinction in different words. The Definition states the effect (`Σ'.R = Σ.R ∪ …`); the distinction belongs once, at the point of effect. X14 then only needs to invoke it.

**Required**: State the distinction once (in the Definition); in X14, reference it rather than re-explaining it.

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
