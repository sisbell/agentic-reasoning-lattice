# Channel Assignment — ASN-0047 review-335

**Date:** 2026-06-02 05:47

## Issue 1: Bridging lemma (†) is load-bearing but asserted, not proved
Reason: The fix is internal — all needed facts (K.δ Document-case effect growing both sets; K.μ⁺/K.μ⁺_L/K.μ⁻ frames on the document set; the default-value convention) are already stated in the ASN. Writing the explicit base/step induction is a restructuring of present content, not a design-intent or implementation question.

## Issue 2: Child-spawn freshness discharge is triple-deferred (reviser drift)
Reason: The fix is internal — ChildSpawnFreshness is already a full lemma in the ASN; collapsing the three-hop relay into a direct citation from each sub-case is pure cross-reference cleanup requiring no external input.

## Issue 3: K.μ~ — "S3★ discharged separately, outside clause (i)" restated three times (reviser drift)
Reason: The fix is internal — Step (B) already carries the S3★ discharge; removing the two redundant scope-caveat restatements is deduplication derivable from the ASN's own structure.

## Issue 4: K.μ⁻ effect satisfiability argument duplicated across precondition and amendment
Reason: The fix is internal — the equivalence lemma already proves the strict-subset ⟺ strict-contraction correspondence; replacing the inline precondition re-derivation with a citation to that lemma is a self-contained editorial change.
