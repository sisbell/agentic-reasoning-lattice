# Review of ASN-0112

This note carries the `review-mode.anti-bloat` classifier. The mathematics is sound — I checked the V2 coverage split (D0/D1 round-trip in both depth cases), the V3 tightness argument through TA5, the divergence bounds, and the wp/Exact derivation, and found no correctness gaps. My findings are confined to accreted meta-prose around the endpoint-depth corner case.

## REVISE

### Issue 1: Defensive don't-conflate note in V3
**ASN-0112, "The bounding span and its two endpoints"**: "Note the tightness validity domain `m_C ≤ m_L` is the *opposite* inequality to the level-uniformity condition `m_C ≥ m_L`; the two must not be conflated."
**Problem**: This is a warning to the reader, not a step in the argument. Both conditions are stated precisely two sentences earlier in the same paragraph; a reader following the math does not need to be told not to conflate two clearly distinct inequalities. Pure meta-prose.
**Required**: Delete the sentence.

### Issue 2: V6 restates V2's reach biconditional
**ASN-0112, "Exact cover within a subspace; a bounding box across subspaces"**: "In the cross-subspace case the endpoints need not be level-compatible (`#origin_d ≠ #reach_d` when `m_C ≠ m_L`...), but the bounding-box reading of V6 is independent of the depth relation by the V2 reach biconditional."
**Problem**: V2's two-case coverage proof already establishes `O(d) ⊊ ⟦σ_d⟧` regardless of the endpoint depth relation, and V2 already names the reach biconditional. This sentence re-derives nothing — it defers back to V2 to assert depth-independence that V2 already proved. The level-compatibility hedge appears here, in V2, and again in V3, scattering one point across three sections.
**Required**: Drop the level-compatibility hedge from V6; if a pointer is wanted, reduce to one clause referencing V2.

### Issue 3: Redundant "function of `O(d)` alone" kernel across V9, V13, V16
**ASN-0112, claims V9/V13/V16**: V9 "σ_d is a function of O(d) alone"; V13 "σ_d depends only on O(d)"; V16 "σ_d is a pure function of O(d)".
**Problem**: The same kernel is asserted three times. V9's rearrangement-invariance is a direct corollary of V16's purity: a pure rearrangement preserves `O(d) = dom(M(d))`, so by V16 the span is unchanged — V9 adds no independent content beyond the Nelson framing. V13's cross-document consequence is genuinely distinct and should stay.
**Required**: State purity once (V16), derive V9's rearrangement-invariance as its corollary, and keep V13 for its distinct cross-document independence consequence.

## OUT_OF_SCOPE

None. The four Open Questions correctly defer per-subspace counting, version faithfulness, run composition, and out-of-range arithmetic to future ASNs; the scope fence is respected in the body.

VERDICT: REVISE
