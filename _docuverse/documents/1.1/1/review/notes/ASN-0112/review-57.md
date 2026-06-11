# Review of ASN-0112

I verified the span construction (V1–V3), both covering cases of V2 (including the componentwise TumblerSub/TumblerAdd computation in the depth-divergent case), the V-ReachTight and V-LevelUniform biconditionals, the V5 prefix-pinning/discreteness argument, the V6 witness, the V9a inverse construction with its final-component discriminator, V18's case analysis, both worked examples, and both wp derivations. The mathematics is sound at every labeled claim. Two items remain, both localized.

## REVISE

### Issue 1: Unproven existential in V3's "not least over all of T" remark; natural witness fails at the single-occupied-position boundary

**ASN-0112, "The bounding span and its two endpoints," V3 paragraph**: "So `reach_d` is *not* the least admissible reach over all of `T` (a span with reach `w.0` already covers `O(d)`), but it is the least strict upper bound of `w` at `w`'s depth — V3's claim."

**Problem**: The parenthetical asserts the existence of a well-formed T12 span whose denotational reach is exactly `w.0` and which covers `O(d)`. No construction is given, and the natural witness — `(origin_d, w.0 ⊖ origin_d)` — fails in two reachable configurations:

1. *Single-subspace with `|O(d)| = 1`* (so `origin_d = w`). Padding `w` to length `#w + 1` makes it zero-padded-equal to `w.0`, so `zpd(w.0, w)` is undefined and TumblerSub returns the zero tumbler — not `Pos`, hence no T12 width exists from this start. This is the state every document passes through at first population, so it is not exotic.
2. *Cross-subspace with `m_C > m_L + 1`*. The width `w.0 ⊖ origin_d` is well-formed (divergence at position 1), but `#origin_d > #w.0`, so by D0's round-trip boundary `origin_d ⊕ (w.0 ⊖ origin_d) ≠ w.0` — the span's actual reach overshoots `w.0`. That span does not have reach `w.0`, contrary to what the parenthetical needs.

The claim is in fact true in all cases, but the witnesses are case-dependent and none is in the text: for case 1, start `s' = [s,1,…,1,0]` (origin with final component lowered to 0) gives width `w.0 ⊖ s' = [0,…,0,1,0]` with `actionPoint = m_s ≤ #s'` and round-trip closing exactly at `w.0`; for case 2, truncating `origin_d` to length `m_L + 1` as the start makes D1 applicable (divergence 1, equal lengths) and closes at `w.0`. This is precisely the pattern the standards forbid: a one-line claim that requires a multi-case construction, with the obvious construction failing at a boundary.

**Required**: Either (a) weaken the parenthetical to the order-theoretic fact already proven — `w < w.0 < reach_d` exhibits a strictly smaller strict upper bound of `max O(d)` in `T`, which fully motivates V3's depth-scoping without committing to span attainability — or (b) retain the span-attainability claim and supply the witness construction with its case split (generic case via D1 from `origin_d`; the `min O(d) = max O(d)` boundary and the `m_C > m_L + 1` cross-subspace sub-case via the alternative starts above).

### Issue 2: The wp section derives a post-hoc discriminator for `Tight` but not the parallel — and equally derivable — one for `Exact`

**ASN-0112, "Preconditions and well-definedness"**: "A caller can thus decide *before* querying whether the answer will be exact (check single-subspace occupancy) and whether its reach is the tight `reach_d` (check the endpoint depths), without inspecting the returned span; tightness is also decidable *after* the fact from the returned value alone, the width's final component being positive exactly when the reach is tight (the V9a discriminator)."

**Problem**: The section answers "what kind of answer will I get" for two properties, then supplies an after-the-fact test for only one of them. The after-the-fact test for `Exact` is a one-line corollary of machinery already in the ASN: in the single-subspace case the endpoints agree at position 1 and diverge at `zpd = m_s ≥ 2` (S8a), so `extent_d₁ = 0`; in the cross-subspace case `zpd = 1` (V2's second covering case) and `extent_d₁ = s_L − s_C ≥ 1 > 0`. Hence, for any non-empty result, `extent_d₁ = 0 ⟺ O(d)` occupies a single subspace `⟺ Exact` (by V5/V6 and the wp(`Exact`) characterization). The omission leaves the wp analysis asymmetric exactly where the text invites the comparison, and the consequence is unexplored despite all its premises being established in the document — the "postconditions established but consequences not derived" pattern.

**Required**: State the post-hoc `Exact` discriminator — the returned width's *first* component is zero exactly when the answer is an exact cover (non-empty case; vacuous on `⟨⟩`) — alongside the existing `Tight` discriminator, with the two-line derivation from the `zpd` case split, or record explicitly why it is omitted.

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
