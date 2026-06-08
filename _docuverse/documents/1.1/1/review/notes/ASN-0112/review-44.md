# Review of ASN-0112

This is a careful, technically sound note. The span construction (`origin_d = min O(d)`, `reach_d = shift(max O(d), 1)`, `extent_d = reach_d ⊖ origin_d`) is well-defined; V2's two covering cases correctly handle both the round-trip-closing case (#origin_d ≤ #reach_d, via D1) and the round-trip-failing case (#origin_d > #reach_d, computed directly through TumblerAdd at action point 1); V5/V6 partition exact-cover vs. bounding-box by subspace occupancy exhaustively via S3★-aux; the empty case (V11), origin migration (V18), and the two wp analyses (Exact, Tight) are all genuine and complete. Edge cases — empty, single position, link-only, depth-divergent endpoints — are covered. All cross-references are to foundation ASNs.

The note carries the anti-bloat classifier, and the findings are at the prose/citation level.

## REVISE

### Issue 1: V3 pre-empts its own proof with a defensive caveat
**ASN-0112, "The constructed endpoint is the tightest same-depth covering bound" (V3)**: The paragraph states the same-depth caveat three times. The claim itself carries "among tumblers of its depth." Then sentence 2 asserts defensively: "Dropping the same-depth qualifier makes the claim false, since the deeper zero-extension `max O(d).0` is a smaller upper bound." The proof's closing sentence then *establishes* exactly this with the actual derivation: "`w < w.0 < inc(w, 0) = reach_d`. So `reach_d` is *not* the least admissible reach over all of `T` (a span with reach `w.0` already covers `O(d)`), but it is the least strict upper bound of `w` at `w`'s depth."
**Problem**: Sentence 2 is a defensive justification placed before the argument that the proof's conclusion derives properly. The counterexample `max O(d).0` and the conclusion `w.0` are the same witness stated twice. This is the meta-prose-around-a-caveat pattern the anti-bloat classifier targets.
**Required**: Delete sentence 2 ("Dropping the same-depth qualifier makes the claim false, since…"). The proof's closing sentence already carries the caveat with the witness derived in place.

### Issue 2: V9 cites the content-only D-SEQ for a generic-subspace claim
**ASN-0112, V9**: "the occupied positions remain the dense set `{[s,1,…,1,k]}` by D-SEQ; only the values `M(d)(v)` are permuted."
**Problem**: The note's own convention fixes "D-SEQ" as the content instance (`S = s_C`) and uses "D-SEQ★"/"the link instance" for the per-subspace shape. V9's set is written with a free subspace variable `s`, so a rearrangement touching link positions needs the per-subspace D-SEQ★, not D-SEQ. The dense-run citation is also not load-bearing for V9 — the conclusion needs only that `O(d) = dom(M(d))` is preserved and that `origin_d`, `extent_d` depend on `O(d)` alone.
**Required**: Either cite D-SEQ★ (or drop the dense-set parenthetical, since V9's conclusion rests only on `O(d)`-invariance, which the sentence already states).

## OUT_OF_SCOPE

None. The note correctly defers per-subspace extent (RETRIEVEDOCVSPANSET), version comparison, link counting, and content delivery to its Open Questions and the stated scope boundary, without making claims about them.

VERDICT: REVISE
