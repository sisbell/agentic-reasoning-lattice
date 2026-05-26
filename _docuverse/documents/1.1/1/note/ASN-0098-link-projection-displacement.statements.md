# ASN-0098 Claim Statements

*Source: ASN-0098-link-projection-displacement.md (revised 2026-05-24) — Extracted: 2026-05-26*

## Definition — Coverage

```
coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ})
```

Each span `(s, ℓ)` denotes `{t ∈ T : s ≤ t < s ⊕ ℓ}` by T12 of ASN-0034, where `s ⊕ ℓ ∈ T` exists by TA0 because `Pos(ℓ)` and `actionPoint(ℓ) ≤ #s` are well-formedness conditions of the span. Coverage is a purely combinatorial property of the endset's span representation — it does not consult any state component.

---

## Definition — ProjectFunction

```
project(e, d, Σ)
  defined when  d ∈ dom(Σ.M)
  ≡             {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(e)}
```

For a link `a ∈ dom(Σ.L)` with slot `i ∈ {1, …, |Σ.L(a)|}`, write `project(a, i, d, Σ) ≡ project(Σ.L(a).eᵢ, d, Σ)`, defined when `a ∈ dom(Σ.L) ∧ d ∈ dom(Σ.M)`.

---

## Definition — DiscoverableFrom

```
discoverable_from(a, d, Σ)
  defined when  a ∈ dom(Σ.L) ∧ d ∈ dom(Σ.M)
  ≡             (E i : 1 ≤ i ≤ |Σ.L(a)| : project(a, i, d, Σ) ≠ ∅)
```

The link is *discoverable* at `Σ` iff there exists some document from which it is discoverable.

---

## Definition — SubstrateEmittableAddresses

```
F = {a ∈ T : (E d ∈ T, s ∈ {s_C, s_L}, k ≥ 1 :: zeros(d) = 2 ∧ d satisfies T4 ∧ a = [d, 0, s, k])}
```

Every `a ∈ F` has `#a = #d + 3`, `zeros(a) = 3`, and `#E(a) = 2`. An address outside `F` cannot be the target of any K.α/K.λ emission. The sub-allocator anchors `b_C(d) = [d, 0, s_C]` and `b_L(d) = [d, 0, s_L]` have `#E = 1` and lie outside `F`.

---

## Definition — Tight

```
tight(e, Σ_e) ≡ every span (s, ℓ) ∈ e is canonical (ℓ = δ(n, #s) for some n ≥ 1,
equivalently #ℓ = #s with ℓ an ordinal displacement) and satisfies:
  s ∈ dom(Σ_e.C) ∪ dom(Σ_e.L)
  ∧ (A t ∈ F : s ≤ t < s ⊕ ℓ : t ∈ dom(Σ_e.C) ∪ dom(Σ_e.L))
```

Non-canonical spans are unconditionally non-tight at every state. `Σ_e` is the state-relative evaluation point; in canonical use `Σ_e` is the state at which `e` was incorporated into a link.

---

## LP2 — SlotInvariance (LEMMA, lemma)

For every transition `Σ → Σ'`, every link `a ∈ dom(Σ.L)`, and every slot index `i ∈ {1, …, |Σ.L(a)|}`:
```
a ∈ dom(Σ'.L) ∧ Σ'.L(a).eᵢ = Σ.L(a).eᵢ
```

---

## LP2★ — MultiStepSlotInvariance (LEMMA, lemma)

For every reachable state sequence `Σ →* Σ'`, every link `a ∈ dom(Σ.L)`, and every slot index `i ∈ {1, …, |Σ.L(a)|}`:
```
a ∈ dom(Σ'.L) ∧ Σ'.L(a).eᵢ = Σ.L(a).eᵢ
```

---

## LP3 — CoverageInvariance (LEMMA, lemma)

For every transition `Σ → Σ'`, every link `a ∈ dom(Σ.L)`, and every slot `i`:
```
a ∈ dom(Σ'.L) ∧ coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)
```

---

## LP3★ — MultiStepCoverageInvariance (LEMMA, lemma)

For every reachable state sequence `Σ →* Σ'`, every `a ∈ dom(Σ.L)`, and every slot `i`:
```
a ∈ dom(Σ'.L) ∧ coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)
```

---

## Store Monotonicity★ — StoreMonotonicity (LEMMA, lemma)

For every reachable state sequence `Σ →* Σ'`:
```
dom(Σ.C) ⊆ dom(Σ'.C)  ∧  dom(Σ.L) ⊆ dom(Σ'.L)
```

---

## LP4 — ArrangementSpecificity (LEMMA, lemma)

For every transition `Σ → Σ'`, every endset `e`, and every document `d ∈ dom(Σ.M) ∩ dom(Σ'.M)`:
```
Σ'.M(d) = Σ.M(d) ⟹ project(e, d, Σ') = project(e, d, Σ)
```

*Frame note.* Downstream applications instantiate `d ∈ dom(Σ.M)` and rely on M1 (ASN-0093) — `dom(Σ.M) ⊆ dom(Σ'.M)` for every transition — to lift to `d ∈ dom(Σ.M) ∩ dom(Σ'.M)`.

---

## LP5 — CrossDocumentIndependence (LEMMA, lemma)

Every operation in the K.μ family (K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~) has frame `(A d' : d' ≠ d : M'(d') = M(d'))` — it modifies at most one document's arrangement per transition. By LP4 applied to each unmodified document:
```
(A d' ∈ dom(Σ.M), d' ≠ d : project(e, d', Σ') = project(e, d', Σ))
```

---

## LP6 — ContentAllocationInvariance (LEMMA, lemma)

The K.α operation modifies only `Σ.C` and has frame `(A d :: M'(d) = M(d))`; K.α also preserves `dom(Σ.M)`, so `dom(Σ.M) = dom(Σ'.M)`. By LP4 applied to every `d ∈ dom(Σ.M) = dom(Σ'.M)`:
```
project(e, d, Σ') = project(e, d, Σ)
```
for every endset `e` and every such `d`, whenever `Σ → Σ'` is a K.α transition.

---

## LP7 — LinkAllocationInvariance (LEMMA, lemma)

The K.λ operation modifies only `Σ.L`; its frame is `(A d :: M'(d) = M(d))`, and K.λ preserves `dom(Σ.M)`. By LP4 applied to every `d ∈ dom(Σ.M) = dom(Σ'.M)`:
```
project(e, d, Σ') = project(e, d, Σ)
```
for every endset `e` and every such `d`.

---

## LP8 — DocumentRegistrationInvariance (LEMMA, lemma)

For any document-registration transition `Σ → Σ'` — either K.σ (ASN-0093) or K.δ in the IsDocument case (ASN-0047) — registering a fresh document `d_new` (with `d_new ∉ dom(Σ.M)`, `dom(Σ'.M) = dom(Σ.M) ∪ {d_new}`, `Σ'.M(d_new) = ∅`, and `Σ'.M(d) = Σ.M(d)` for every `d ∈ dom(Σ.M)`) and any endset `e`, both:

(a) Pre-state preservation: `(A d ∈ dom(Σ.M) :: project(e, d, Σ') = project(e, d, Σ))`.

(b) Newly-registered emptiness: `project(e, d_new, Σ') = ∅`.

---

## LP14 — ProvenanceRecordingInvariance (LEMMA, lemma)

The K.ρ operation (ASN-0047), which records provenance by adding a pair to `Σ.R`, has frame `(A d :: M'(d) = M(d))` — it leaves every document's arrangement intact — and preserves `dom(Σ.M)`. By LP4 applied to every `d ∈ dom(Σ.M) = dom(Σ'.M)`:
```
project(e, d, Σ') = project(e, d, Σ)
```
for every endset `e` and every such `d`, whenever `Σ → Σ'` is a K.ρ transition.

---

## LP9 — ExtensionMonotonicity (LEMMA, lemma)

For every extension transition `Σ → Σ'` operating on document `d` — either K.μ⁺ (content-subspace extension) or K.μ⁺_L (link-subspace extension) — and every endset `e`:
```
project(e, d, Σ) ⊆ project(e, d, Σ')
```

The new V-positions that enter the projection are exactly:
```
project(e, d, Σ') ∖ project(e, d, Σ) = {v ∈ dom(Σ'.M(d)) ∖ dom(Σ.M(d)) : Σ'.M(d)(v) ∈ coverage(e)}
```

The proof relies on:
- (E1) *Strict domain extension:* `dom(Σ'.M(d)) ⊃ dom(Σ.M(d))`
- (E2) *Prior-domain agreement:* `(A v : v ∈ dom(Σ.M(d)) : Σ'.M(d)(v) = Σ.M(d)(v))`

---

## LP10 — ContractionMonotonicity (LEMMA, lemma)

For every K.μ⁻ transition `Σ → Σ'` operating on `d`, and every endset `e`:
```
project(e, d, Σ') ⊆ project(e, d, Σ)
```

The V-positions that leave the projection are exactly:
```
project(e, d, Σ) ∖ project(e, d, Σ') = {v ∈ dom(Σ.M(d)) ∖ dom(Σ'.M(d)) : Σ.M(d)(v) ∈ coverage(e)}
```

---

## LP11 — ReorderingRebinding (LEMMA, lemma)

For every K.μ~ transition `Σ → Σ'` operating on `d` via the witnessing bijection `π : dom(Σ.M(d)) → dom(Σ'.M(d))`, and every endset `e`:
```
project(e, d, Σ') = π(project(e, d, Σ))
```
and
```
ran(Σ'.M(d)) = ran(Σ.M(d))
```

---

## LP-Comp — CompositionalCoverage (NOTE, note)

Documentation note, not a load-bearing lemma: per-step lemmas LP4 through LP14 form a covering case-analysis on the operation kinds of the working frame. Every atomic transition `Σ → Σ'` admitted by the ASN-0047 + ASN-0093 vocabulary is governed by exactly one of them: K.σ and K.δ-IsDocument by LP8; K.δ-IsNode and K.δ-IsAccount by LP4 via their `(A d :: M'(d) = M(d))` frames; K.α by LP6; K.λ by LP7; K.ρ by LP14; K.μ⁺ and K.μ⁺_L on document `d` by LP9 (and on `d' ≠ d` by LP5); K.μ⁻ on `d` by LP10 (and on `d' ≠ d` by LP5); K.μ~ on `d` by LP11 (and on `d' ≠ d` by LP5). Since reachable sequences `Σ →* Σ'` decompose into finite chains of atomic transitions, the per-step lemmas jointly characterise the projection's evolution across any such sequence.

---

## LP12 — DiscoverabilityCharacterisation (LEMMA, lemma)

For every link `a ∈ dom(Σ.L)`, document `d ∈ dom(Σ.M)`, and state `Σ`:
```
discoverable_from(a, d, Σ) ⟺ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)
```

Per-slot biconditional: `project(a, i, d, Σ) ≠ ∅ ⟺ coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅`.

---

## LP12a — ContractionDiscoverabilityWP (LEMMA, lemma)

Fix a K.μ⁻ operation on document `d ∈ dom(Σ.M)` with retention parameters `(n'_{s_C}, n'_{s_L})` admissible under K.μ⁻'s precondition, and let
```
R := ⋃ {[S, 1, ..., 1, k] : S ∈ {s_C, s_L} ∧ 1 ≤ k ≤ n'_S}
```
denote the resulting retention set. For every link `a ∈ dom(Σ.L)`, the weakest precondition on the pre-state `Σ` under which `discoverable_from(a, d, Σ')` holds in the post-state `Σ' = K.μ⁻[d, R](Σ)` is:
```
wp(K.μ⁻[d, R], discoverable_from(a, d, ·))
  ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : project(a, i, d, Σ) ∩ R ≠ ∅)
```

*Boundary case — empty retention.* At `R = ∅` the wp specialises:
```
(E i : project(a, i, d, Σ) ∩ ∅ ≠ ∅) ≡ false
```

Per-slot post-state reduction: `project(a, i, d, Σ') = project(a, i, d, Σ) ∩ R`.

Equivalent coverage-range form:
```
discoverable_from(a, d, Σ')
  ⟺ (E i : coverage(Σ.L(a).eᵢ) ∩ ran(Σ'.M(d)) ≠ ∅)
  ⟺ (E i : coverage(Σ.L(a).eᵢ) ∩ {Σ.M(d)(v) : v ∈ R} ≠ ∅)
```

---

## LP12b — ContentCanonicalLinkSubspaceWPFalse (LEMMA, lemma)

Let `a ∈ dom(Σ.L)` be a link such that every span `(s, ℓ) ∈ Σ.L(a).eᵢ` (for every slot `i`) is canonical (`ℓ = δ(n, #s)` for some `n ≥ 1`) with `s = [d_s, 0, s_C, k_s]` for some T4-valid document `d_s` and chain index `k_s ≥ 1`. For any K.μ⁻ retention parameters `n'_{s_C} = 0` and `n'_{s_L} > 0`, the wp evaluates to `false`:
```
(E i : project(a, i, d, Σ) ∩ R ≠ ∅) ≡ false
```
where `R = {[s_L, 1, ..., 1, k] : 1 ≤ k ≤ n'_{s_L}} ⊆ V_{s_L}(d)`.

Derived via: `coverage(Σ.L(a).eᵢ) ∩ dom(Σ.L) = ∅` (from LP-Fin Corollary at `X = s_C`), giving `project(a, i, d, Σ) ⊆ V_{s_C}(d)`, and therefore `project(a, i, d, Σ) ∩ R ⊆ V_{s_C}(d) ∩ V_{s_L}(d) = ∅`.

*OUT_OF_SCOPE:* The symmetric link-canonical class — every span canonical with `s = [d_s, 0, s_L, k_s]` under the same retention pattern — is explicitly out of scope for this ASN.

---

## LP13 — UnconditionalLinkPersistence (LEMMA, lemma)

For every reachable state sequence `Σ →* Σ'` and every link `a ∈ dom(Σ.L)`:
```
a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)
```

The conclusion holds independently of `Σ.M`, `Σ'.M`, `dom(Σ.M)`, `dom(Σ'.M)`, and any document's range.

---

## LP16 — TransclusionDiscoverability (LEMMA, lemma)

For any link `a ∈ dom(Σ.L)`, slot `i ∈ {1, …, |Σ.L(a)|}`, and documents `d_src, d_new ∈ dom(Σ.M)` at state `Σ`:
```
coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d_src)) ∩ ran(Σ.M(d_new)) ≠ ∅
  ⟹  discoverable_from(a, d_src, Σ) ∧ discoverable_from(a, d_new, Σ)
```

---

## LP17 — GhostProjection (LEMMA, lemma)

Suppose at state `Σ` no document's arrangement reaches any I-address in `coverage(Σ.L(a).eᵢ)` for any slot `i`:
```
(A d ∈ dom(Σ.M), i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) = ∅)
```

Then by LP12, `project(a, i, d, Σ) = ∅` for every `d, i`. By L12 (ASN-0043), `a` remains in `dom(Σ.L)` and `Σ.L(a)` is unchanged.

---

## LP18 — Resurrection (LEMMA, lemma)

If `a` is orphaned at `Σ` and a subsequent transition sequence `Σ →* Σ'` introduces an arrangement entry `Σ'.M(d)(v) = a*` for some `d, v, a*` with `a* ∈ coverage(Σ.L(a).eᵢ)`, then `a` is discoverable from `d` at `Σ'`.

By LP3★: `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)`, so `a* ∈ coverage(Σ'.L(a).eᵢ)`. By the definition of `project`, `v ∈ project(a, i, d, Σ')` since `v ∈ dom(Σ'.M(d))` and `Σ'.M(d)(v) = a* ∈ coverage(Σ'.L(a).eᵢ)`.

---

## LP-Fin — IntervalFinitude (LEMMA, lemma)

For every *canonical* span `(s, ℓ)` — meaning `s ∈ F` (so `s = [d_0, 0, s', k_s]` for some T4-valid `d_0` with `zeros(d_0) = 2`, subspace `s' ∈ {s_C, s_L}`, chain index `k_s ≥ 1`) and `ℓ = δ(n, #s)` for some `n ≥ 1` (equivalently `#ℓ = #s` with `ℓ` an ordinal displacement):
```
|F ∩ [s, s ⊕ ℓ)| < ∞
```

Non-canonical spans:
- (i) `#ℓ < #s`: `|F ∩ [s, s ⊕ ℓ)| = ℵ₀` (within-chain construction gives infinite F-candidates)
- (ii) `#ℓ = #s` with `ℓ` non-ordinal (`actionPoint(ℓ) < #s`): `|F ∩ [s, s ⊕ ℓ)| = ℵ₀` (same within-chain construction)
- (iii) `#ℓ > #s`: excluded by the tightness predicate's definitional canonical-form requirement

---

## LP-Fin Corollary — CanonicalIntervalCharacterisation (LEMMA, lemma)

For canonical span `(s, ℓ)` with `s = [d_0, 0, X, k_s]` (where `X ∈ {s_C, s_L}`) and `ℓ = δ(n, #s)`:
```
F ∩ [s, s ⊕ ℓ) = {[d_0, 0, X, k] : k_s ≤ k < k_s + n}
```

Every `t ∈ F ∩ [s, s ⊕ ℓ)` satisfies `subspace_I(t) = X` and `origin(t) = d_0`. The interval contains no F-candidates from any chain other than `A_X(d_0)`.

---

## LP19-Achiev-CrossSub-C — TightAchievCrossSubC (LEMMA, lemma)

For span on `A_C(d_0)` (so `s = [d_0, 0, s_C, k_s]`) with canonical `ℓ = δ(n, #s)`:

For every chain element `b` of `A_L(d_0)` with structural form `[d_0, 0, s_L, k]`:
- Positions `1..#d_0 + 1` agree between `b`, `s`, and `s ⊕ ℓ`
- At position `#d_0 + 2`: `b_{#d_0 + 2} = s_L > s_C = (s ⊕ ℓ)_{#d_0 + 2}`
- By T1 case (i) at position `#d_0 + 2`: `b > s ⊕ ℓ`, hence `b ∉ [s, s ⊕ ℓ)`

Interfering chain elements of `A_L(d_0)` are excluded *above* the interval.

---

## LP19-Achiev-CrossSub-L — TightAchievCrossSubL (LEMMA, lemma)

For span on `A_L(d_0)` (so `s = [d_0, 0, s_L, k_s]`) with canonical `ℓ = δ(n, #s)`:

For every chain element `b` of `A_C(d_0)` with structural form `[d_0, 0, s_C, k]`:
- Positions `1..#d_0 + 1` agree between `b`, `s`, and `s ⊕ ℓ`
- At position `#d_0 + 2`: `b_{#d_0 + 2} = s_C < s_L = s_{#d_0 + 2}`
- By T1 case (i) at position `#d_0 + 2`: `b < s`, hence `b ∉ [s, s ⊕ ℓ)`

Interfering chain elements of `A_C(d_0)` are excluded *below* the interval.

---

## LP19-Achiev-NonNest — TightAchievNonNest (LEMMA, lemma)

For non-nesting `d' ≠ d_0` (neither a prefix of the other), canonical span `(s, ℓ)` with `s` rooted on `d_0`:

By Divergence (ASN-0034) case (i), there exists a position `j ≤ min(#d_0, #d')` with `d_{0,j} ≠ d'_j` and `d_{0,i} = d'_i` for `1 ≤ i < j`. For every chain element `b` of `A_sub'(d')`:
- Positions `1..j-1` agree between `b`, `s`, and `s ⊕ ℓ` (prefix agreement + TumblerAdd prefix-copy since `j ≤ #d_0 < #s = actionPoint(ℓ)`)
- At position `j`: `b_j = d'_j ≠ d_{0,j} = s_j = (s ⊕ ℓ)_j`
- By T1 case (i): if `d'_j < d_{0,j}` then `b < s`; if `d'_j > d_{0,j}` then `b > s ⊕ ℓ`
- Either way `b ∉ [s, s ⊕ ℓ)`

---

## LP19-Achiev-Desc — TightAchievDesc (LEMMA, lemma)

For descendant `d_0 ≺ d'` (so `d' = [d_0, x_1, …, x_q]` with `x_i ≥ 1` by zero-count balance), canonical span `(s, ℓ)` with `s = [d_0, 0, X, k_s]`:

For every chain element `b` of `A_sub'(d')` with prefix `d'`:
- Positions `1..#d_0` agree between `b`, `s`, and `s ⊕ ℓ` (prefix relations + TumblerAdd prefix-copy since `#d_0 < #s = actionPoint(ℓ)`)
- At position `#d_0 + 1`: `b_{#d_0 + 1} = x_1 ≥ 1` while `s_{#d_0 + 1} = 0` and `(s ⊕ ℓ)_{#d_0 + 1} = 0`
- By T1 case (i) at position `#d_0 + 1`: `b > s ⊕ ℓ`, hence `b ∉ [s, s ⊕ ℓ)`

Zero-count balance argument: `zeros(d_0) = 2` and `d_0 ≺ d'` with `zeros(d') = 2` forces `#{i : x_i = 0} = 0`, so every `x_i ≥ 1`.

---

## LP19-Achiev-Anc — TightAchievAnc (LEMMA, lemma)

For ancestor `d' ≺ d_0` (so `d_0 = [d', y_1, …, y_r]` with `y_i ≥ 1` by zero-count balance), canonical span `(s, ℓ)` with `s = [d_0, 0, X, k_s]`:

For every chain element `b` of `A_sub'(d')` with structural form `[d', 0, s'', k]` (so `#b = #d' + 3`):
- Positions `1..#d'` agree between `b` and `s` (prefix derived from `d' ≺ d_0`)
- At position `#d' + 1`: `b_{#d' + 1} = 0` while `s_{#d' + 1} = d_{0, #d' + 1} = y_1 ≥ 1` and `(s ⊕ ℓ)_{#d' + 1} = y_1` (prefix-copy since `#d' + 1 ≤ #d_0 < #s = actionPoint(ℓ)`)
- By T1 case (i) at position `#d' + 1`: `b < s`, hence `b ∉ [s, s ⊕ ℓ)`

Zero-count balance argument: `zeros(d') = 2` and `d' ≺ d_0` with `zeros(d_0) = 2` forces `#{i : y_i = 0} = 0`, so every `y_i ≥ 1`.

---

## LP19a — TightFreshness (LEMMA, lemma)

For any endset `e` tight at `Σ_e`, any reachable state sequence `Σ_e →* Σ`, and any K.α (or K.λ) transition `Σ → Σ'` allocating a fresh address `a_new`:
```
a_new ∉ coverage(e)
```

The K.α step emits `a_new` from sub-allocator `A_C(d_alloc)` for some `d_alloc`, so `a_new ∈ F`. K.α's precondition requires `a_new ∉ dom(Σ.C) ∪ dom(Σ.L)`. By Store Monotonicity★ applied to `Σ_e →* Σ`, `a_new ∉ dom(Σ_e.C) ∪ dom(Σ_e.L)`. The tightness condition at `Σ_e` applied with `a_new ∈ F` would yield `a_new ∈ dom(Σ_e.C) ∪ dom(Σ_e.L)` if `a_new ∈ coverage(e)` — contradiction.

---

## LP19 — TightEndsetBoundaryExclusion (LEMMA, lemma)

Let `e` be an endset tight at `Σ_e`, and let `Σ_e →* Σ_n → Σ_{n+1}` be a reachable transition sequence whose final step is a K.μ⁺ (or K.μ⁺_L) transition operating on document `d`. For every `v_new ∈ dom(Σ_{n+1}.M(d)) ∖ dom(Σ_n.M(d))`, letting `a_new := Σ_{n+1}.M(d)(v_new)`, if `a_new` was freshly allocated by a K.α (or K.λ) step on the prefix `Σ_e →* Σ_n`:
```
v_new ∉ project(e, d, Σ_{n+1})
```

V-positions added at the same K.μ⁺ step whose image is *not* freshly allocated on the prefix — transclusion entries whose image lies in `dom(Σ_n.C) ∪ dom(Σ_n.L)` — fall outside this lemma's hypothesis and are governed by LP9's general growth characterisation.

---

## LP20 — RangeConfinement (LEMMA, lemma)

For every endset `e`, document `d`, state `Σ`:
```
{Σ.M(d)(v) : v ∈ project(e, d, Σ)} = coverage(e) ∩ ran(Σ.M(d))
```

*Corollary (store-confinement form)* via S3★:
```
{Σ.M(d)(v) : v ∈ project(e, d, Σ)} ⊆ coverage(e) ∩ (dom(Σ.C) ∪ dom(Σ.L))
```

*Per-subspace refinement* via S3★ and S3★-aux:
```
{Σ.M(d)(v) : v ∈ project(e, d, Σ) ∧ subspace(v) = s_C} ⊆ coverage(e) ∩ dom(Σ.C)
{Σ.M(d)(v) : v ∈ project(e, d, Σ) ∧ subspace(v) = s_L} ⊆ coverage(e) ∩ dom(Σ.L)
```

The two per-subspace components *partition* the full projection range:
```
{Σ.M(d)(v) : v ∈ project(e, d, Σ)} = {Σ.M(d)(v) : v ∈ project(e, d, Σ) ∧ subspace(v) = s_C}
                                   ∪ {Σ.M(d)(v) : v ∈ project(e, d, Σ) ∧ subspace(v) = s_L}
```

---

## LP21 — RepresentationInvariance (LEMMA, lemma)

For any two endsets `e₁, e₂` with `coverage(e₁) = coverage(e₂)`:
```
project(e₁, d, Σ) = project(e₂, d, Σ)
```
