# Review of ASN-0112

The arithmetic is sound. I checked the covering proof (V2) in both depth regimes, the worked examples (`1.1 for 1.2`, `1.1 for 0.3`, and the depth-divergent `[1,2,0]` variant), the well-formedness derivation via D0, and the wp factorization — all hold. The findings below are the anti-bloat patterns this note's classifier asks for, plus one local rigor gap.

## REVISE

### Issue 1: V2 case 2 asserts "With k = 1" without local justification
**ASN-0112, "The bounding span and its two endpoints," V2 covering proof**: "*`#origin_d > #reach_d` (content deeper than the maximal link position). By D0 the round-trip fails... With `k = 1`, TumblerAdd gives `r⋆`...*"
**Problem**: The branch silently reuses `k = 1`, but `k = 1` is only established for the *cross-subspace* configuration. The reader must independently reconstruct the chain `#origin_d > #reach_d ⟹ single-subspace excluded (equal depths) ⟹ cross-subspace ⟹ divergence at position 1`. That implication is the whole reason `k = 1` is available here, and it is not stated.
**Required**: One clause noting that `#origin_d > #reach_d` forces the cross-subspace case (single-subspace endpoints are equidepth by S8-depth), whence `k = divergence(origin_d, reach_d) = 1`.

### Issue 2: V3 explains the same-depth qualifier twice
**ASN-0112, "The bounding span...," V3**: first "*The same-depth qualifier is load-bearing: dropped, the claim is false, since the deeper `max O(d).0` is a smaller upper bound.*" then later "*The deeper `w.0` is excluded precisely because it sits at a greater depth than `max O(d)`, outside that same-depth comparison class.*"
**Problem**: Two paragraphs in the same claim make the identical point (the deeper zero-extension is a smaller bound, excluded by the depth qualifier). The second statement adds nothing the first did not already say.
**Required**: Keep one statement of the qualifier; delete the duplicate.

### Issue 3: V3 narrates its own proof structure
**ASN-0112, "The bounding span...," V3**: "*So far this is a statement about the witness `reach_d`, not about `σ_d`. The leap to `σ_d` requires `reach(σ_d) = reach_d`, which by the V2 reach biconditional holds exactly when...*"
**Problem**: This is procedural scaffolding describing where the argument stands rather than advancing it — the precise reader has to step past the meta-commentary to reach the actual content (the conditional `reach(σ_d) = reach_d`). The substantive fact is the biconditional dependency; the "so far / the leap" framing is noise.
**Required**: State the dependency directly ("`σ_d`'s reach equals `reach_d` iff `#origin_d ≤ #reach_d` (V2 reach biconditional); under that condition `σ_d` is the tightest covering span at the depth of `max O(d)`") without the narration about witnesses versus the span.

### Issue 4: V17 restates V2's T12 well-formedness
**ASN-0112, V17 vs. V2**: V2 already concludes "*`(origin_d, extent_d)` satisfies T12 and is a well-formed span*" with the inline `Pos`/`actionPoint ≤ #origin_d` derivation; V17 re-asserts "*`extent_d` is a positive tumbler with `actionPoint(extent_d) ≤ #origin_d`, so `σ_d` is a legal T12 span.*"
**Problem**: The same well-formedness conclusion and its two conjuncts appear in both places. The genuinely new content in V17 is the "never negative / no zero-width artifact" framing and the Gregory grounding; the T12 legality is duplicated.
**Required**: Have V17 cite V2 for T12 legality and confine itself to the non-redundant content (strict positivity / non-degeneracy and the implementation evidence), rather than re-deriving the well-formedness.

### Issue 5: V3's closing depth-taxonomy over-elaborates
**ASN-0112, V3 final sentences**: the distinctions among "tightest covering," "level-uniform (`#origin_d ≥ #reach_d`)," and "endpoint-level-compatible (`#origin_d = #reach_d`)," restated again in the V3 table row.
**Problem**: Three depth relations are introduced and ranked ("stricter still") within a claim whose actual content is the GLB/LUB bounding result. The level-uniformity of `σ_d` is never used downstream (V17 needs only `actionPoint ≤ #origin_d`, not `#origin_d = #extent_d`), so the taxonomy is scaffolding that the reader must absorb without payoff.
**Required**: Reduce to the one relation V3 actually needs (same-depth tightness of `reach_d`); drop the level-uniform/endpoint-compatible ranking or move the single load-bearing fact to where it is consumed.

## OUT_OF_SCOPE

### Topic 1: Extent-versus-cardinality invariant in the multi-subspace case (Open Question 1)
**Why out of scope**: This is the correct framing of a real follow-on question, and the note properly defers it. No action needed here.

### Topic 2: Historical-version faithfulness and correspondence-run composition (Open Questions 3–4)
**Why out of scope**: Version comparison and per-run decomposition belong to other operations; correctly left open.

VERDICT: REVISE
