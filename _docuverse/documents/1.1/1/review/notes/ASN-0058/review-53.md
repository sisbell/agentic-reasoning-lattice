# Review of ASN-0058

The mathematical core is rigorous: M-int, M12a/b, M16a, C0, and C2 carry their case splits and boundary cases (empty arrangement, `n=1`, `k=0`) explicitly, and the two worked examples discharge the concrete-verification requirement. The findings below are confined to forward-reference accretion flagged by the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: M16 trailing paragraph is defensive meta-prose after a completed proof
**ASN-0058, M16 (CrossOriginMergeImpossibility), paragraph following the proof**: "The cross-origin merge impossibility above is not an additional constraint imposed on the merge — it is a consequence of I-adjacency and the invariance of document origin under ordinal increment. ... At the abstract level, the guard is redundant: the contrapositive of origin equality already prevents cross-origin I-adjacency. But its presence in the implementation reflects the abstract property and provides an efficient short-circuit."
**Problem**: The proof ends at `∎`. The "is not an additional constraint — it is a consequence" sentence restates what was just proven as a defensive reassurance, and the "the guard is redundant ... But its presence reflects the abstract property" sentences are essay-style justification of an implementation redundancy. A reader following the result skips past all of it. The only non-meta content is the single statement of what `isanextensionnd`'s `homedoc` check does.
**Required**: Delete the framing and redundancy commentary. Keep at most the one-sentence statement of what the implementation guard does, if implementation evidence is wanted.

### Issue 2: ContentReference precondition-necessity prose explains *why* a precondition is needed rather than deriving the fact it supports
**ASN-0058, Definition (ContentReference), the `m ≥ 2` paragraph**: "Precondition (i) is what makes m well-defined at all — S8-depth (ASN-0036) is vacuously true for an empty subspace and determines no common depth."
**Problem**: This is the named drift pattern — prose around a precondition explaining why the precondition is needed rather than advancing the claim. The load-bearing content is only the next sentence ("Given (i), some `v ∈ V_{u₁}(d_s)` exists, so S8a gives `#v ≥ 2` and S8-depth gives `m = #v ≥ 2`"), which establishes `m ≥ 2` on its own.
**Required**: Drop the "Precondition (i) is what makes m well-defined at all — ..." sentence; let the `m ≥ 2` derivation stand alone.

## OUT_OF_SCOPE

None. The mapping-block canonical decomposition (M11/M12) is this ASN's own contribution — distinct from ASN-0036's arrangement-level contiguity invariants (D-CTG, D-SEQ) named in the scope exclusion — so it is correctly in scope here.

VERDICT: REVISE
