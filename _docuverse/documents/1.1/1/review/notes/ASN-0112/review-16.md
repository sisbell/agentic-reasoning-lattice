# Review of ASN-0112

## REVISE

### Issue 1: "level-uniform" conflated with "endpoint-level-compatible" in V3 and V6

**ASN-0112, V3 (bounding) / "The bounding span and its two endpoints"**: "So σ_d is the tightest *level-uniform* covering span of O(d)."

**Problem**: The note's own definitions (V2 / S6) separate two notions: *level-uniform* (`#s = #ℓ`, i.e. `#origin_d = #extent_d`) and *endpoint-level-compatible* (`#start = #reach`). V3's universal claim does not track either cleanly.

- S8-depth permits `m_C ≠ m_L`. When `m_C < m_L` (content shallower than the maximal link position), `#origin_d = m_C` and `#extent_d = max(m_C, m_L) = m_L ≠ m_C`, so σ_d is **not** level-uniform — yet V3 asserts it is "the tightest level-uniform covering span" unconditionally. This is exactly the cross-subspace case V2 (case 2) and V6 elsewhere admit.
- The V6 table entry compounds the confusion: "the endpoints are level-compatible **and the span level-uniform** whenever the subspaces share a depth (m_C = m_L)." But the note's *own* divergent worked variant (`m_C = 3 > m_L = 2`) gives `extent_d = [1,2,0]` of depth 3 `= #origin_d`, so σ_d **is** level-uniform there (`#s = #ℓ = 3`) even though `m_C ≠ m_L` and the endpoints are not level-compatible (`#start = 3 ≠ 2 = #reach`). So "span level-uniform ⟺ m_C = m_L" is false.

The actual situation: σ_d is level-uniform iff `m_C ≥ m_L` (`#origin_d ≥ #reach_d`); endpoints are level-compatible iff `m_C = m_L`. These are distinct conditions, and the note uses one word for both.

**Required**: Scope V3 to what the reach argument actually proves — `reach_d` is the least strict upper bound of `max O(d)` *among tumblers at the depth of `max O(d)`* — and drop or correct the "σ_d is level-uniform" conclusion (it holds only when `m_C ≥ m_L`). Correct the V6 table to separate "span level-uniform" (`m_C ≥ m_L`) from "endpoints level-compatible" (`m_C = m_L`).

### Issue 2: single-span structural impossibility stated twice (anti-bloat)

**ASN-0112, V6 closing paragraph and V7**: V6 closes with "A document occupying two disjoint subspaces is a *separated series*; no single span can trace it exactly… Any implementation that answers with one origin-and-extent pair must, of necessity, bridge the gap." V7 then records the same: "the result is always one convex region; fragmentation is unrepresentable in a single span, so a multi-subspace document is reported by enclosure rather than by exact decomposition," prefaced by the essay "This is not a defect peculiar to one engine. It is a *theorem about single spans*."

**Problem**: The "one span cannot exactly trace a separated series" point is argued in full prose at the end of the V6 section and then re-recorded as V7. The intervening essay ("not a defect peculiar to one engine…") restates V7's content before V7 is stated. This is the kind of meta-prose restatement the anti-bloat classifier targets.

**Required**: State the structural impossibility once. Let V6 carry the empirical claim (`O(d) ⊊ ⟦σ_d⟧`) and V7 carry the structural reason (single convex region) without the connecting essay restating both.

## OUT_OF_SCOPE

(none — the note's Open Questions correctly defer span-set per-subspace recovery, version reporting, and out-of-range arithmetic to future ASNs rather than claiming them.)

VERDICT: REVISE
