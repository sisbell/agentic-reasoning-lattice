# Review of ASN-0112

## REVISE

### Issue 1: "Level-uniform" is conflated with the distinct condition #origin_d = #reach_d, producing a false claim in the non-level-uniform worked example

**ASN-0112, V2 well-formedness/coverage paragraph**: "What level-uniformity buys is only that the span's reach *equals* `reach_d` exactly: `reach(σ_d) = reach_d ⟺ #origin_d ≤ #reach_d`, which holds whenever the occupied subspaces share a common depth."

**ASN-0112, "A non-level-uniform variant" (worked report)**: "Here `#origin_d = 3 > 2 = #reach_d`, so the span is *not* level-uniform."

**Problem**: ASN-0053 (S6, foundation) defines a span `(s, ℓ)` as *level-uniform* iff `#s = #ℓ`. The ASN repeatedly uses "level-uniform" to mean instead `#origin_d = #reach_d` (level-compatibility of the two *endpoints*). These are not the same condition, and the construction makes them diverge.

Because `extent_d = reach_d ⊖ origin_d` has length `#extent_d = max(#origin_d, #reach_d)` (TumblerSub/TA2), the reported span `(origin_d, extent_d)` is level-uniform iff `#origin_d = #extent_d`, i.e. iff `#origin_d ≥ #reach_d` — the *opposite* inequality from the one the ASN ties to `reach(σ_d) = reach_d` (which is `#origin_d ≤ #reach_d`). Two concrete consequences:

1. The worked "non-level-uniform" span is actually level-uniform. With `origin_d = [1,1,1]` and `extent_d = [1,2,0]`, we have `#s = #ℓ = 3`, so by S6 the span **is** level-uniform, with actual reach `r⋆ = [1,1,1] ⊕ [1,2,0] = [2,2,0]` (depth 3, as S6's `#reach = #s` requires). The ASN's statement "the span is *not* level-uniform" contradicts the foundation definition it cites.

2. "Level-uniformity buys `reach(σ_d) = reach_d`" is false. That same span is level-uniform yet has `reach(σ_d) = [2,2,0] ≠ [2,2] = reach_d` (the ASN itself proves the inequality via D0). So a level-uniform span does **not** guarantee `reach = reach_d`; the genuine condition for `reach(σ_d) = reach_d` is `#origin_d ≤ #reach_d`, an endpoint condition unrelated to span level-uniformity.

The same conflation recurs in the V2 parenthetical ("in particular the level-uniform case `#origin_d = #reach_d`"), in V6 ("the span is level-uniform whenever the subspaces share a depth") — which is true but wrongly implies non-level-uniformity when `m_C ≠ m_L`, even though the `m_C > m_L` span is level-uniform — and in V17 ("level-uniformity is needed only for `reach(σ_d) = reach_d`").

**Required**: Separate the two notions. Reserve "level-uniform" for ASN-0053's `#s = #ℓ`, and introduce a distinct name (e.g. "endpoint-level-compatible," `#origin_d = #reach_d`, via S6's `level_compat`) for the same-depth-endpoint condition. Restate the boundary facts correctly:
- `reach(σ_d) = reach_d ⟺ #origin_d ≤ #reach_d` (D1/D0);
- the span is level-uniform `⟺ #origin_d ≥ #reach_d`;
- both, plus `reach(σ_d) = reach_d` *and* tightness (V3), hold exactly when `#origin_d = #reach_d` (the uniform-depth case the implementation realizes).

Correct the worked variant: the span `([1,1,1],[1,2,0])` **is** level-uniform; what fails there is `reach(σ_d) = reach_d` (the reach overshoots to `[2,2,0]`) and the V3 tightness claim, not level-uniformity.

## OUT_OF_SCOPE

(none — the ASN correctly defers per-subspace extent recovery, version reporting, and cardinality relationships to its Open Questions rather than specifying them here.)

VERDICT: REVISE
