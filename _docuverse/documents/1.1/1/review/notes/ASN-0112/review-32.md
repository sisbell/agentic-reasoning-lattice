# Review of ASN-0112

## REVISE

### Issue 1: Worked-example variant mislabels which claim lapses

**ASN-0112, "A worked report" (depth-divergent variant)**: "the actual reach `r⋆ = [2,2,0]` overshoots `reach_d` exactly as V2's second covering case predicts (coverage and T12 legality survive; only the V3 same-depth tightness lapses)."

**Problem**: This contradicts V3's own statement. V3 has two separated parts: (A) `reach_d` is the least strict upper bound of `max O(d)` *among tumblers at the depth of `max O(d)`*, and (B) whether `σ_d`'s denotational reach `r⋆` attains `reach_d`, which V3 explicitly assigns to "the separate question governed by the V2 reach biconditional." In the variant, `max O(d) = [2,1]` (depth 2) and `reach_d = [2,2]` (depth 2) — so `reach_d` *is* the least strict same-depth upper bound of `max O(d)`, and V3's claim (A) **holds**. What fails is `r⋆ = reach_d` (claim B / `ReachTight`), which V3 routes to the V2 biconditional, not to itself. So "the V3 same-depth tightness lapses" names the wrong claim.

**Required**: State that what lapses in the `#origin_d > #reach_d` variant is the V2 reach biconditional (`reach(σ_d) = reach_d`, i.e. `ReachTight`), and that V3's same-depth tightness of `reach_d` relative to `max O(d)` is intact.

### Issue 2: "Implementation evidence" section is self-justifying meta-prose

**ASN-0112, "Implementation evidence: the extent stays non-negative"**: "The non-degeneracy of the reported extent is settled by V2 alone... What this section adds is implementation evidence for that positivity, nothing more." / "This confirms V2 in the concrete implementation; it introduces no further guarantee, since an alternative implementation need reproduce neither the negative intermediate entries nor the max-minus-min recomputation — only V2's positive extent."

**Problem**: The substantive content is a single sentence (deletions can drive intermediate displacements negative, but the root width is a max-minus-min reach and stays non-negative). Surrounding it are framing sentences whose only job is to announce that the section adds "nothing more" and "no further guarantee" — defensive essay content in a structural slot, the `review-mode.anti-bloat` pattern. A reader must skip past the self-justification to reach the one load-bearing observation.

**Required**: Reduce to the single implementation remark (negative intermediates, non-negative root reach, evidence for V2's positivity) and drop the "nothing more / no further guarantee / an alternative implementation need reproduce neither..." framing.

## OUT_OF_SCOPE

### Topic 1: Extent-to-occupancy-count invariant in the multi-subspace case
The first Open Question (relating reported extent to `|O(d)|` when an inter-subspace void intervenes) is genuinely new territory — a future invariant, not a defect here. Correctly parked.

### Topic 2: Historical-version reporting and per-run composition
The third and fourth Open Questions (faithfulness of a version-designated report; composing the whole-document extent from per-run bounding spans) belong to version comparison and per-subspace/run reporting (ASN-0113 territory), not this query.

VERDICT: REVISE
