# Review of ASN-0112

## REVISE

### Issue 1: V3's tightness conclusion is unsound in the depth-divergent case it elsewhere admits
**ASN-0112, "The bounding span and its two endpoints" (V3)**: "so `σ_d` is the tightest covering span whose reach is at the depth of `max O(d)`."
**Problem**: V3 correctly proves that *`reach_d`* (the tumbler `shift(max O(d), 1)`) is the least strict upper bound of `max O(d)` among depth-`#reach_d` tumblers. But the conclusion is about *`σ_d`*, whose actual reach is `reach(σ_d) = r⋆ = origin_d ⊕ extent_d`. By V2 itself, `r⋆ = reach_d` **only** when `#origin_d ≤ #reach_d`; when `#origin_d > #reach_d` the round-trip fails (D0) and `r⋆` overshoots to depth `#origin_d ≠ #reach_d`. In that case `σ_d` is not "a covering span whose reach is at the depth of `max O(d)`" at all, so the tightness statement is inapplicable to `σ_d` rather than true of it. The worked-example variant concedes exactly this ("only the V3 same-depth tightness lapses"), yet the claim as written carries no condition tying the conclusion to `reach(σ_d) = reach_d`.
**Required**: Condition the `σ_d`-tightness conclusion on `#origin_d ≤ #reach_d` (i.e. `reach(σ_d) = reach_d`), or restate V3 purely about the witness `reach_d` and drop the unqualified leap to `σ_d`. Note this validity domain (`m_C ≤ m_L`) is the *opposite* of the level-uniformity aside V3 appends (`m_C ≥ m_L`), so the two must not be conflated.

### Issue 2: Reach-biconditional / endpoint-depth fact accreted across four sections
**ASN-0112, V2 / V3 / V6 / "Preconditions and well-definedness"**: the condition `#origin_d ≤ #reach_d` and its consequence `reach(σ_d) = reach_d` are stated and re-stated in V2 ("the reach biconditional `reach(σ_d) = reach_d ⟺ #origin_d ≤ #reach_d`"), revisited in V3 (level-uniformity aside), re-derived in V6 ("The V2 reach biconditional already disposes of this... coverage was proved without any endpoint depth relation and so holds regardless"), and stated a fourth time in the wp section (`wp(..., "reach(σ_d) = reach_d") = (#origin_d ≤ #reach_d)`).
**Problem**: V6's "subtlety of depth" paragraph adds no object-level content beyond deferring back to V2 and appending one implementation fact (`m_C = m_L`); it is the "two paragraphs say the same thing in different words" / repeated-deferral accretion pattern this note is classified to surface.
**Required**: Consolidate the reach-biconditional into a single carrier (V2) and let V6/wp cite it in one clause each, deleting the restatement of the coverage-holds-regardless argument in V6.

### Issue 3: Defensive meta-prose in V2
**ASN-0112, V2**: "*We do not assume level-uniformity here.*"
**Problem**: This italicized aside advances no reasoning — it preempts an anticipated objection rather than establishing a claim. The covering proof already makes the absence of a level-uniformity assumption evident from its case split.
**Required**: Delete the defensive sentence; the case structure speaks for itself.

## OUT_OF_SCOPE

### Topic 1: Origin-vs-identity coincidence, version faithfulness, run composition, out-of-range arithmetic
The four trailing Open Questions (permanent-identity vs min-occupied origin, historical-version faithfulness, whole-vs-run extent composition, out-of-range editing artifacts) are correctly posed as future work, not gaps in this ASN. No action needed; flagged only to confirm they are out of scope here.

META: (none — the ASN remains squarely about query value-semantics and invariants.)

VERDICT: REVISE
