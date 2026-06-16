## Review of M1 — Address & Span Algebra: Detailed Design

I checked every owned capability against ASN-0034/0045/0053 (statements included), traced the trickiest algorithms (`sub` zpd-dispatch, `subtree_of`'s `δ(1,#p)` vs `inc(p,0)`, the `merge`/`intersect` min/max guards, `hull`'s `inc(max,0)` bound, the validate-and-classify scan), and cross-checked the data model / interface / invariants / seams for agreement. The module is **buildable and faithful**: the algorithms are described constructively, the signatures typecheck, the allocator/spanfilade/byte-mapping boundaries are correctly pushed to M3/M7/M4-M5, all seven source-note conflicts are resolved soundly, and the level gate is placed correctly (after classify, before construction; absent on `classify_spans`/`union`). The subtle points a builder most often gets wrong — `subtree_of` using `shift(p,1)` not `inc(p,0)` on trailing-zero prefixes, `zeros()` as `usize` to avoid the wrap-to-3 bug, field-absence⇒NO in containment, `displacement` returning `None` outside the round-trip window — are all correct.

I found no material problems. The items below are genuine but non-load-bearing.

### Revision list

1. **[SHARPENING]** Resolve the `is_normalized` vs `normalize` disagreement on a single non-level-uniform span: `is_normalized(⟨σ⟩)` returns `true` (N1/N2 vacuous) while `normalize(⟨σ⟩)`/`canonical_key(⟨σ⟩)` return `Err(LevelMismatch)` because the level gate fires on σ's non-uniformity. Either gate `is_normalized` on level-uniformity too, or have `normalize` short-circuit zero-/single-span sets unchanged (no coalescing ⇒ no level dependence), so the two agree on every constructible input. (Only bites out-of-spec inputs, but it is the design's own predicate contradicting itself.)

2. **[SHARPENING]** Reconcile the decomposition's "coverage-class *computed in M1*" (M7 entry) with this design's mechanism/policy split. Make the M1→M7 contract surface explicit: M1's deliverable is `canonical_key` → `CanonicalForm` (Hash+Eq), M1 owes *no* `coverage_class()`, and M7 keys its dedup on `CanonicalForm`. The design flags the refinement; stating the seam shape outright keeps M7's builder from expecting a function M1 doesn't expose.

3. **[SHARPENING]** Consolidate `split`'s full precondition in its own bullet — *σ level-uniform* **and** `level_compat(start,p)` **and** strictly-interior `p`. It is currently complete only by combining the §6 general-gate sentence, the split bullet (which names only `level_compat(start,p)`), and the Invariants list; a builder reading the split bullet alone could omit the σ-uniformity that keeps the right part `(p, reach⊖p)` level-uniform.

4. **[SHARPENING]** Push raw `shift` toward crate-private behind `shift_ordinal` (or mark it unsafe-by-convention). Public `shift` defeats TA7a's "un-violable by callers" intent — the digest's stated recommendation — and its only cited use, "a caller already holding a verified full element position," is already served by `ElemPos`/`shift_ordinal`.

5. **[SHARPENING]** Sharpen the magnitude-vs-length justification. "Fixed component-magnitude would violate T0 but `usize` length would not" rests on an unstated asymmetry: the admission path can realistically present huge *component values* but not 2⁶⁴-long *sequences*. Say so, so the `BigUint`-magnitude / `usize`-length split reads as principled (and so the length choice is visibly the spec's permitted "discharge the proof the bound is unreachable").

6. **[SHARPENING]** Package the S7 `|Σ|=|P|` unit-span cover as `cover(points: &[Tumbler]) -> SpanSet` beside `hull`, rather than leaving it a prose recipe — "coverage" is a listed owned capability, and the helper (each `t → from_endpoints(t, inc(t,0))`, unioned) closes it unambiguously.

7. **[SHARPENING]** Minor consistency/robustness: (a) align `subspace() -> Option<Nat>` (owned) with the borrowing field projectors or note the deliberate clone; (b) specify `elem_addr`'s behavior if the defensive `validate` fails despite its guards (`expect`/`unreachable!`, since the guards make it impossible — but the error-type mismatch with `ElemError` should be named); (c) consider an opaque `Nat` newtype over the transparent `pub type Nat = BigUint` alias so the public key/endpoint type survives the component-representation Open decision unchanged.

VERDICT: CONVERGED
