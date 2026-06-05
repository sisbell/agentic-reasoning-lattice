# Review of ASN-0112

## REVISE

### Issue 1: The empty-document result is not a well-formed span, and its origin is undefined
**ASN-0112, V11 / V0**: "When `O(d) = ∅`, the result is the *zero-extent span* — an origin with `extent_d = 0` (the zero tumbler) — a degenerate but perfectly well-defined span." vs. V0: "returns one well-formed span."
**Problem**: A well-formed span requires `Pos(ℓ)` (Span/T12, ASN-0034). The zero tumbler fails `Pos` (and by TA6 is not even a valid address), so the "zero-extent span" is *not* a T12 span — it contradicts V0's blanket "well-formed span" guarantee, and V17 silently concedes positivity only "for non-empty `d`." Worse, `origin_d` is left undefined when `O(d) = ∅`: V1 defines `origin_d = min O(d)` only for `O(d) ≠ ∅`, and `min ∅` does not exist. The Gregory evidence ("returns zeros for both displacement and width") shows the implementation returns a zero *tumbler* for the origin, which TA6 excludes from valid addresses. The empty case — the boundary case the ASN claims to handle — is the one left unspecified.
**Required**: Define the empty-document result precisely as a distinguished value (a sentinel, an empty span-set, or an explicitly-carved-out non-T12 result) and reconcile it with V0/V17. State what `origin_d` is when `O(d) = ∅` and whether it is a legal tumbler.

### Issue 2: Span well-formedness and reach are proven only for level-uniform spans, but the cross-subspace case need not be level-uniform
**ASN-0112, V2 / V6 / V17**: "the span `(origin_d, extent_d)` is well-formed with reach `reach_d` (WF, ASN-0053, **in the level-uniform case where `#origin_d = #reach_d`**)."
**Problem**: S8-depth explicitly permits distinct subspaces to have distinct depths. In the cross-subspace case (V6), `origin_d` is a content position (depth `m_C`) and `max O(d)` — hence `reach_d = shift(max O(d), 1)` — is a link position (depth `m_L`). When `m_C ≠ m_L` the span is *not* level-uniform, so WF does not apply, and the parenthetical restriction in V2 quietly excludes exactly the case V6 analyzes. Concretely, when `m_C > m_L` (`#origin_d > #reach_d`), D0 guarantees the round-trip *fails*: `origin_d ⊕ (reach_d ⊖ origin_d) ≠ reach_d`. So the span's actual reach is not `reach_d`, and the V2 covering claim and V17 well-formedness claim are unestablished. The worked example uses depth 2 throughout and never exercises differing subspace depths, so it does not test this.
**Required**: Either prove `origin_d ⊕ extent_d = reach_d` and `Pos(extent_d)`, `actionPoint(extent_d) ≤ #origin_d` for the cross-subspace case with `m_C ≠ m_L` (handling `#origin_d > #reach_d` via D0), or restrict the well-formedness/reach claims and show coverage by a separate argument that does not route through WF. Add a worked example with `m_C ≠ m_L`.

### Issue 3: `reach_d` is not the least admissible upper bound — V3 overclaims tightness
**ASN-0112, V3**: "reach `reach_d` the least admissible upper bound of the occupied set ... `reach(σ') ≥ reach_d` under the convention that ordinal positions advance one step at a time."
**Problem**: The "convention that ordinal positions advance one step at a time" contradicts the tumbler foundation. ASN-0034 (T0 note) states the true immediate T1-successor of `t` is the zero-extension `t.0`, and `t < t.0 < shift(t, 1)`. A covering span needs only `reach > max O(d)`; taking `reach' = max O(d).0` gives `O(d) ⊆ ⟦(origin_d, reach'⊖origin_d)⟧` with `reach' < reach_d`. So `reach_d` is strictly not the least admissible reach, and V3's "tightest bounding span" claim is false as stated. The hand-wave "ordinal positions advance one step at a time" is doing illegitimate work.
**Required**: Either weaken V3 to the *canonical* (same-depth/level-uniform) upper bound — and prove `reach_d` is least *among same-depth tumblers* — or justify rigorously why the zero-extension successor is disallowed as a reach. Replace the "convention" with an explicit argument grounded in T1 and the immediate-successor structure.

### Issue 4: Insertion monotonicity (V10) fails for multi-subspace documents
**ASN-0112, V10**: "an insertion of `n` content positions increases the extent by exactly `n` and leaves the origin fixed."
**Problem**: This is stated unconditionally but holds only for single-subspace (content-only) documents. When the link subspace is occupied, `max O(d)` is a *link* position (`s_C < s_L`), so inserting `n` content positions extends the content run but does not move `max O(d)` — therefore `reach_d` and `extent_d` are unchanged, not "increased by `n`." The supporting derivation ("inserting `n` positions ... growing `max O(d)` by `n` ordinal steps") tacitly assumes the inserted positions are the maximum, which is only true in the content-only case.
**Required**: Add the single-subspace (or "content is the maximal subspace occupied") precondition to V10, or state the multi-subspace behavior explicitly (extent invariant under content insertion when links occupy the maximum).

## OUT_OF_SCOPE

### Topic 1: Recovering per-subspace extents exactly (first Open Question)
**Why out of scope**: Exact per-subspace decomposition requires a span-set (RETRIEVEDOCVSPANSET / ASN-0113), which the scope note excludes. The Open Question correctly defers it.

### Topic 2: Historical-version reporting faithfulness (fourth Open Question)
**Why out of scope**: Version comparison/selection is deferred (SHOWRELATIONOF2VERSIONS is out of scope); reporting on a designated version is future territory, not an error here.

VERDICT: REVISE
