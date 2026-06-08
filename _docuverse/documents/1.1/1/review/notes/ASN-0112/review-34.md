# Review of ASN-0112

## REVISE

### Issue 1: Reach biconditional restated redundantly across claim slots
**ASN-0112, V2/V3 table rows and §"The bounding span"**: V2's row states "with equality `r⋆ = reach_d` iff `#origin_d ≤ #reach_d`"; the V3 row then restates the entire biconditional — "Whether `σ_d`'s own denotational reach `r⋆` attains `reach_d` is the separate question governed by the V2 reach biconditional (`reach(σ_d) = reach_d` iff `#origin_d ≤ #reach_d`); in the `#origin_d > #reach_d` case `r⋆ = reach_d` fails".
**Problem**: V3's distinct content is endpoint tightness of `reach_d` at `max O(d)`'s depth. A one-clause pointer would disambiguate it from V2's denotational-reach claim; instead the parenthetical re-derives the full biconditional and its failure case, duplicating V2's covering-proof conclusion. Under the active anti-bloat classifier this is accretion that dilutes V3's purpose. The same biconditional recurs in the wp section (`ReachTight`) and the worked variant.
**Required**: In the V3 row, reference the V2 reach biconditional by name only ("attainment of `reach_d` is the separate V2 question"); do not restate `iff #origin_d ≤ #reach_d` or the failure case there.

### Issue 2: V12 section carries motivational essay in a claim slot
**ASN-0112, §"What the caller learns beyond the name"**: "A document's identity is its tumbler `N.0.U.0.D`: a pure locator. It tells you *where* the document sits and *who* owns it — 'you always know where you are' (2/40) — but 'tumblers … impose no categorization …' (4/17–4/18)."
**Problem**: V12 ("information gain") is the one claim in the table that states no state, operation, or invariant property — it is an observation about caller utility. The surrounding paragraph is identity-locator essay content, not a statement of what `RETRIEVEDOCVSPAN` does or guarantees. It does not advance the operation's reasoning.
**Required**: Either reduce V12 to a one-line corollary of V1/V2 (origin = live anchor, extent = current bounds) and drop the identity-locator digression, or remove the claim if it carries no verifiable content beyond V1/V2/V8.

## OUT_OF_SCOPE

### Topic 1: Multi-subspace extent-to-count invariant; version-report faithfulness; run composition
**Why out of scope**: The Open Questions correctly defer these to per-subspace reporting (ASN-0113), version comparison, and run-composition ASNs. They are appropriately placed as future work, not errors here.

Correctness, case coverage (single/dual subspace via S3★-aux, empty via V11), the D0/D1 covering proof, the non-trivial wp analysis, and the worked examples all hold. The findings above are prose/accretion, not proof gaps.

VERDICT: REVISE
