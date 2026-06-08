# Review of ASN-0112

## REVISE

### Issue 1: V3 summary asserts σ_d's reach lies at max O(d)'s depth, contradicting V2's second covering case

**ASN-0112, Claims table (V3) / "The bounding span" section**: "reach_d is the least strict upper bound of `max O(d)` … among tumblers at the depth of `max O(d)` … so `σ_d` is the tightest covering span whose reach is at the depth of `max O(d)`."

**Problem**: The denotational reach of `σ_d` is `reach(σ_d) = origin_d ⊕ extent_d = r⋆`, not `reach_d`. V2's own second case (`#origin_d > #reach_d`) proves `r⋆ ≠ reach_d`, with `r⋆` sitting at depth `#origin_d > #reach_d =` depth of `max O(d)` (the worked variant gives `reach_d = [2,2]` but `r⋆ = [2,2,0]`). So in that case `σ_d`'s reach is *not* at the depth of `max O(d)`, and the final clause of V3 is false. The V3 body in fact concedes this — "Whether `σ_d`'s own reach attains `reach_d` is governed by the V2 reach biconditional" — so the table summary overclaims relative to its own body and to V2.

**Required**: Restate V3's conclusion so it speaks of the constructed endpoint `reach_d` (which is genuinely the least strict upper bound of `max O(d)` at that depth), not of `σ_d`'s denotational reach. Either drop the "so `σ_d` is the tightest covering span whose reach is at the depth of `max O(d)`" clause or qualify it with the V2 reach biconditional (`reach(σ_d) = reach_d` only when `#origin_d ≤ #reach_d`).

### Issue 2: "The extent is a well-formed, non-negative displacement" section restates V2 without adding a claim

**ASN-0112, "The extent is a well-formed, non-negative displacement"**: "The abstract obligation here is V2's alone: V2 established `σ_d`'s T12 legality — `Pos(extent_d)` and `actionPoint(extent_d) ≤ #origin_d` … so the non-degeneracy of the reported extent is already settled."

**Problem**: This section introduces no new claim; its first paragraph reproduces V2's positivity/legality result verbatim (two passages stating the same thing in different words), and explicitly says so. Under the note's anti-bloat classifier this is the duplication pattern — the precise reader must recognize it as a restatement and skip to find the one piece of new content, the Q18 implementation remark on negative intermediate displacements.

**Required**: Fold the Q18 evidence directly under V2 (where its T12-positivity claim lives) and remove the restating section, or reduce the section to the implementation remark alone with a one-line pointer to V2.

## OUT_OF_SCOPE

### Topic 1: Multi-subspace extent-to-cardinality invariant
The first Open Question asks what invariant relates the cross-subspace extent to the count of occupied positions. This is genuinely new territory (and overlaps per-subspace extent reporting reserved for ASN-0113); correctly deferred, not an error here.

### Topic 2: Historical-version and correspondence-run composition reports
The third and fourth Open Questions (version faithfulness, run-to-whole composition) belong to version comparison / per-run reporting, both outside a bare whole-document boundary query.

VERDICT: REVISE
