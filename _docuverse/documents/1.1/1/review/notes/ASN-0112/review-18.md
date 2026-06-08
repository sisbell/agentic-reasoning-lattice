# Review of ASN-0112

This note is mathematically sound — I checked V1–V3, V10's count-coincidence, the worked example, and the endpoint-depth-divergent variant, and the tumbler arithmetic holds in every case (including the `#origin_d > #reach_d` round-trip-failure branch of V2, where `r⋆ = reach_d.0…0` is computed correctly). No foundation cross-references are misused; all citations are to foundation ASNs. The findings below are the accreted meta-prose and editing-mechanics drift that the `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: Provenance narration and defenses against non-existent alternatives

**ASN-0112, V2 and V3**:
- V2: "coverage holds *unconditionally* — it does not route through any endpoint depth relation or through WF."
- V3: "The upper bound requires an argument, not an appeal to a 'one step at a time' convention — the tumbler line has no such convention."

**Problem**: Both sentences narrate what the proof does *not* depend on rather than advancing it. "Does not route through WF" is an exhaustiveness claim about proof provenance; "no such convention" defends against an alternative no one proposed. These are the defensive-justification pattern that compounds across cycles. The coverage proof and the `inc(w,0)` tightness argument stand on their own without the disclaimers.

**Required**: Delete the provenance/defense clauses. State the coverage result and the tightness result directly.

### Issue 2: V10/V18 re-derive INSERT and DELETE mechanics

**ASN-0112, V10 and V18**: V10 gives the `n`-step shift arithmetic for content insertion under two subspace-maximal conditions; V18 gives a three-case deletion analysis (content-maximal retreat, link-maximal invariance, full-clearance origin migration) with implementation-consultation citations.

**Problem**: RETRIEVEDOCVSPAN is a pure query. The only query-relevant fact is V16 (`σ_d` is a function of `O(d)`); from it, *any* edit's effect on the span follows mechanically once that edit's effect on `O(d)` is known. The exact reach-arithmetic of insertion and the three deletion cases are INSERT/DELETE behavior re-derived here, not invariants of this operation. This is the heaviest accreted material in the note. V9 (rearrangement invariance) is genuinely a query property and should stay; V10/V18's edit-arithmetic belongs in the INSERT/DELETE ASNs.

**Required**: Reduce V10/V18 to the query-level consequence — that any edit changes the reported span exactly insofar as it changes `O(d)` (via V16), with at most one illustrative line — and move the detailed shift/clearance derivations out of this note. If origin migration on content-clearance is worth recording here, state it as a single bound on V8's hypothesis, not a multi-case deletion walkthrough.

### Issue 3: Repeated deferral to the span-set operation

**ASN-0112, V6/V7 region and Open Questions**: "recovering the per-subspace extents exactly requires a span-*set* — a different operation, out of scope here" (V7), echoed by "no single span can trace it exactly; recovering the per-subspace extents exactly requires a span-set" (V6 paragraph) and again in Open Question 1.

**Problem**: The same downstream operation (RETRIEVEDOCVSPANSET) is deferred to three times in different words. One statement of the structural reason (V7: a single convex region cannot trace a separated series) suffices; the others are restatements.

**Required**: State the single-span-cannot-fragment fact once (V7) and remove the duplicate deferrals in the V6 paragraph and the Open Questions.

## OUT_OF_SCOPE

### Topic 1: Per-subspace exact extents
**Why out of scope**: The note correctly identifies that exact per-subspace tracing needs a span-set (RETRIEVEDOCVSPANSET / ASN-0113), which the scope section already excludes. The V6/V7 bounding-box characterization is the right thing for *this* operation; no coverage gap.

VERDICT: REVISE
