# Review of ASN-0042

## REVISE

### Issue 1: "all eight conditions" contradicts the six-condition delegation predicate
**ASN-0042, O3 (OwnershipRefinement) proof**: "The remaining clause of O15 supplies an existing principal `π_d ∈ Π_Σ` for which the full delegation predicate `delegated_Σ(π_d, π')` — all eight conditions, freshness and next-reachability included — held at `π'`'s introducing event."
**Problem**: The delegation predicate has **six** conditions — O15 itself says "subject to six structural conditions," and `Definition (delegated)` lists exactly `(i), (ii), (iii), (iv), (vi), (viii)`. "All eight conditions" is leftover from the pre-collapse formulation in which (v) and (vii) still existed. This is a direct internal contradiction.
**Required**: Change "all eight conditions" to "all six conditions" (or just "the full delegation predicate").

### Issue 2: Gap-numbered conditions plus meta-prose explaining the gaps
**ASN-0042, O15**: "The condition labels (i)–(iv), (vi), (viii) are preserved from an earlier formulation in which the now-removed (v) and (vii) appeared; the gaps are intentional, since downstream proofs cite these labels."
**Problem**: This is meta-prose about the document's edit history, and the gapped numbering (skipping v and vii) forces every reader to track phantom labels. The justification ("downstream proofs cite these labels") is precisely the downstream-consumer rationale the anti-bloat pass exists to remove. Issue 1 above is the direct cost of carrying stale labels.
**Required**: Renumber the surviving conditions consecutively `(i)–(vi)`, update the citing proofs, and delete the historical explanation.

### Issue 3: "Why the axiom is needed" prose around condition (iv)
**ASN-0042, O15**: "Condition (iv) (`zeros(pfx(π')) ≤ 1`) is genuinely needed and is *not* implied by (viii) — B6(iii) bounds only `zeros(p) + (d − 1) ≤ 3`."
**Problem**: This explains *why* condition (iv) is present rather than what it states — the flagged "new prose around an axiom explains why the axiom is needed" pattern. The same pattern recurs in the Delegation section: "T4 is not implied by condition (iv): a prefix such as `[1, 2, 0]` satisfies `zeros ≤ 1` but violates T4..." (the `[1,2,0]` example is legitimate content, but its framing as a necessity-defense is the bloat).
**Required**: Drop the "genuinely needed / not implied by" framing; keep condition (iv) stated plainly. If the independence of (iv) from (viii) is load-bearing, it belongs as a one-line lemma, not an inline defense.

### Issue 4: Gregory's `tumbleraccounteq` lockstep walk described three times
**ASN-0042, O1 / O1a / O6**: O1 — "compares two tumbler mantissa arrays digit by digit"; O1a — "walks the mantissa of both tumblers in lockstep"; O6 — "read directly by `tumbleraccounteq` (the lockstep mantissa walk described under O1a)."
**Problem**: The same implementation fact is restated in three sections, and O6 explicitly back-references O1a — the "two paragraphs say the same thing" / deferral pattern. The repetition adds no reasoning.
**Required**: State the lockstep-walk evidence once (at O1a, where the account boundary is the point), and at O1/O6 cite the structural conclusion without re-narrating the implementation.

### Issue 5: Forward-reference deferral and triple-stated unilateral witness
**ASN-0042, OwnershipDomainPermanence proof / O10 Formal Contract**: The single-transition proof says "Multi-step closure ... is extended to `→⁺` in Corollary OwnershipDomainPermanence★ below"; separately, O10's unilateral single-baptism witness is asserted in the *Unilateral postcondition*, restated in the *Invariant* line, and narrated again in body prose ("The single-baptism witness is thus unconditional...").
**Problem**: The deferral pointer and the triple restatement are forward-reference accretion — prose that points elsewhere or repeats a settled claim without advancing it.
**Required**: Let the corollary stand on its own without the forward pointer; state the unilateral witness once in O10's contract and remove the duplicated body narration.

### Issue 6: Condition (iii) restates its own binder
**ASN-0042, O15 / Definition (delegated)**: condition "(iii) `π' ∈ Π_{Σ'} ∖ Π_Σ`" is listed as a condition on the existential witness `π`, but it merely repeats the outer binder `(A π' ∈ Π_{Σ'} ∖ Π_Σ : ...)`.
**Problem**: A condition that duplicates the quantifier it sits under carries no content; it inflates the count and the citations.
**Required**: Fold (iii) into the binder and renumber (subsumed by the Issue 2 renumbering).

## OUT_OF_SCOPE

### Topic 1: Next-reachability as a restriction on which prefixes are delegable
Condition (viii) forces a delegate prefix to be the *next* unallocated stream element `c_{hwm+1}`, so a principal cannot delegate `[1,0,5]` until `[1,0,2..4]` are baptized. Whether delegation should be free to target any fresh valid descendant is a model-design question, not an error in this ASN — the note is internally consistent under the chosen gate.
**Why out of scope**: This is a deliberate coupling of delegation to baptism order; revisiting it is new design territory, and the Open Questions section already gestures at related concerns.

### Topic 2: Ownership transfer and provenance/owner divergence
The note repeatedly observes Nelson permits "bought document rights" but the model has no transfer. The invariants such transfer must preserve are correctly deferred.
**Why out of scope**: Already listed under Open Questions; introducing transfer would be a future ASN.

VERDICT: REVISE
