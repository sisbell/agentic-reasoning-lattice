# ASN-0091 Claim Statements

*Source: ASN-0091-rearrange-operation.md (revised 2026-05-26) — Extracted: 2026-05-27*

## Definition — PerAddressMultiplicity

For each I-address `a` and each registered document `d'`, define `μ_a(M(d')) = |{v : v ∈ dom(M(d')) ∧ M(d')(v) = a}|`.

## Definition — ProjectionSet

`project(e, d, Σ) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}`

## Definition — ProjectionTransport

Define the *projection transport* `π̂_d`: `π̂_d := π` when `d = d_tgt` and `π̂_d := id_{dom(Σ.M(d))}` when `d ≠ d_tgt`. The identity case is well-typed because RE-other forces `dom(Σ'.M(d)) = dom(Σ.M(d))` for `d ≠ d_tgt`, so `π̂_d` is in every case a bijection between `dom(Σ.M(d))` and `dom(Σ'.M(d))`.

## Definition — MultiStepProjectionTransport

For a finite sequence of REARRANGE-only transitions `Σ_0 →_R Σ_1 →_R ⋯ →_R Σ_n`: for each step `Σ_{i−1} →_R Σ_i` targeting document `dᵢ` with rearrangement permutation `π_i` on `dom(Σ_{i−1}.M(dᵢ))`, `π̂_i := π_i` when `dᵢ = d` and `π̂_i := id_{dom(Σ_{i−1}.M(d))}` otherwise (in which case RE-other applied at step i gives `Σ_i.M(d) = Σ_{i−1}.M(d)`, so the identity is well-typed and the projection is unchanged).

## Definition — ChainDisjointAdjacency

**Inline lemma (ChainDisjointAdjacency).** For chain elements `x ∈ A_{s_X}(d_X)` and `y ∈ A_{s_Y}(d_Y)` with `(d_X, s_X) ≠ (d_Y, s_Y)` — i.e., the two sub-allocator chains differ in either their home document or their subspace — neither `x + 1 = y` nor `y + 1 = x` can hold under TA5(c).

*Justification.* Each chain element of `A_{s_X}(d_X)` has the structural form `[d_X, 0, s_X, k]` for some chain index `k ≥ 1`; the chain-adjacency operator `inc(·, 0)` from TA5(c) preserves length and modifies only the rightmost (significant) position, so the chain successor of `x = [d_X, 0, s_X, k_x]` is exactly `x + 1 = [d_X, 0, s_X, k_x + 1]` — still in `A_{s_X}(d_X)`. Symmetrically, if `y ∈ A_{s_Y}(d_Y)` then `y = [d_Y, 0, s_Y, k_y]` for some `k_y ≥ 1`. For `x + 1 = y` to hold, the structural equality `[d_X, 0, s_X, k_x + 1] = [d_Y, 0, s_Y, k_y]` would be required; by T3 (CanonicalRepresentation, ASN-0034), tumbler equality is component-wise sequence equality, so this demands `(d_X, s_X, k_x + 1) = (d_Y, s_Y, k_y)` as triples — in particular `d_X = d_Y` and `s_X = s_Y`, contradicting the hypothesis `(d_X, s_X) ≠ (d_Y, s_Y)`. The symmetric direction `y + 1 = x` demands `(d_Y, s_Y, k_y + 1) = (d_X, s_X, k_x)` — again forcing `d_Y = d_X` and `s_Y = s_X`, contradicting `(d_X, s_X) ≠ (d_Y, s_Y)`.

---

## RA-reg — RearrangeRegistration (DEF, PRE)

```
d ∈ dom(Σ.M)                                                                            (RA-reg)
```

Precondition that makes every subsequent appearance of `Σ.M(d)`, `dom(Σ.M(d))`, and the bijection's domain type-correct.

## RA-dom — RearrangeDomainStability (DEF, DEF)

```
dom(Σ'.M(d)) = dom(Σ.M(d))                                                              (RA-dom)
```

## RA-π — RearrangePermutation (DEF, DEF)

There exists a bijection
```
π : dom(Σ.M(d)) → dom(Σ'.M(d))
```
satisfying
```
(A v : v ∈ dom(Σ.M(d)) : Σ'.M(d)(π(v)) = Σ.M(d)(v))                                    (RA-π)
```

## RA-frame — RearrangeFrame (DEF, DEF)

```
Σ'.C = Σ.C  ∧  Σ'.L = Σ.L  ∧  Σ'.E = Σ.E  ∧  Σ'.R = Σ.R                                 (RA-frame)
  ∧  dom(Σ'.M) = dom(Σ.M)
  ∧  (A d' ∈ dom(Σ.M) : d' ≠ d : Σ'.M(d') = Σ.M(d'))
```

## RA-adm — RearrangeAdmissibility (DEF, INV)

```
every foundation invariant satisfied by Σ is satisfied by Σ'                            (RA-adm)
```

---

## RE-C — ContentStoreInvariance (LEMMA, LEMMA)

```
Σ'.C = Σ.C                                                                              (RE-C)
```

## RE-dom — DomainStability (LEMMA, LEMMA)

```
dom(Σ'.M(d)) = dom(Σ.M(d))                                                              (RE-dom)
```

## RE-ran — RangeInvariance (LEMMA, LEMMA)

```
(A d' ∈ dom(Σ.M) :: ran(Σ'.M(d')) = ran(Σ.M(d')))                                      (RE-ran)
```

Derived via two-case argument for the target document `d`:
```
ran(Σ'.M(d)) = {Σ'.M(d)(v') : v' ∈ dom(Σ'.M(d))}
             = {Σ'.M(d)(π(v)) : v ∈ dom(Σ.M(d))}        [π bijects dom onto itself]
             = {Σ.M(d)(v) : v ∈ dom(Σ.M(d))}             [RA-π]
             = ran(Σ.M(d))
```
and for every other registered document `d' ∈ dom(Σ.M)` with `d' ≠ d`, RA-frame's other-document clause `Σ'.M(d') = Σ.M(d')` forces `ran(Σ'.M(d')) = ran(Σ.M(d'))` trivially.

## RE-μ — PerAddressMultiplicityInvariance (LEMMA, LEMMA)

```
(A a ∈ T, d' ∈ dom(Σ.M) :: μ_a(Σ'.M(d')) = μ_a(Σ.M(d')))                              (RE-μ)
```

For the target document `d`, by injectivity of π on a finite set (dom(M(d)) is finite by S8-fin):
```
μ_a(Σ'.M(d)) = |{v' : v' ∈ dom(Σ'.M(d)) ∧ Σ'.M(d)(v') = a}|
             = |{π(v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}|       [substitute v' = π(v)]
             = |{v : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}|           [π injective]
             = μ_a(Σ.M(d))
```

## RE-L — LinkStoreInvariance (LEMMA, LEMMA)

```
dom(Σ'.L) = dom(Σ.L)  ∧  (A a ∈ dom(Σ.L) :: Σ'.L(a) = Σ.L(a))                          (RE-L)
```

## RE-cov — CoverageInvariance (LEMMA, LEMMA)

```
(A a ∈ dom(Σ.L), i : 1 ≤ i ≤ |Σ.L(a)| :: coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ))   (RE-cov)
```

## RE-disc — DiscoverabilityInvariance (LEMMA, LEMMA)

```
(A a ∈ dom(Σ.L), d ∈ dom(Σ.M) :: discoverable_from(a, d, Σ') ⟺ discoverable_from(a, d, Σ))    (RE-disc)
```

Derived via LP12 (ASN-0098) characterisation `discoverable_from(a, d, Σ) ⟺ (E i :: coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)`:
```
discoverable_from(a, d, Σ')
  ⟺ (E i :: coverage(Σ'.L(a).eᵢ) ∩ ran(Σ'.M(d)) ≠ ∅)
  ⟺ (E i :: coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)
  ⟺ discoverable_from(a, d, Σ)
```

## RE-proj — ProjectionTransport (LEMMA, LEMMA)

```
project(e, d, Σ') = π̂_d(project(e, d, Σ))      for every d ∈ dom(Σ.M)                  (RE-proj)
```

Where `π̂_d := π` when `d = d_tgt` and `π̂_d := id_{dom(Σ.M(d))}` when `d ≠ d_tgt`.

Equivalently at `d_tgt`: `project(e, d_tgt, Σ') = π(project(e, d_tgt, Σ))`.

Sub-claims:

*Target case.* For each `v ∈ project(e, d_tgt, Σ)`, `π(v) ∈ project(e, d_tgt, Σ')`. For the reverse inclusion, take any `v' ∈ project(e, d_tgt, Σ')`: by RA-dom, `v' ∈ dom(Σ.M(d_tgt))`; let `v := π⁻¹(v')`; then `Σ.M(d_tgt)(v) = Σ'.M(d_tgt)(π(v)) = Σ'.M(d_tgt)(v') ∈ coverage(e)`, so `v ∈ project(e, d_tgt, Σ)` and `v' = π(v) ∈ π(project(e, d_tgt, Σ))`.

*Non-target case.* For any `d ≠ d_tgt`, RE-other gives `Σ'.M(d) = Σ.M(d)` entirely, so `project(e, d, Σ') = project(e, d, Σ)`.

## RE-frag — FragmentationPossibility (LEMMA, LEMMA)

> **Fragmentation Possibility.** There exist rearrangements `Σ → Σ'` such that the cardinality of the canonical maximal-run decomposition of `Σ'.M(d)` is strictly greater than that of `Σ.M(d)`. (RE-frag)

## RE-coal — CoalescencePossibility (LEMMA, LEMMA)

> **Coalescence Possibility.** There exist rearrangements `Σ → Σ'` such that the cardinality of the canonical maximal-run decomposition of `Σ'.M(d)` is strictly less than that of `Σ.M(d)`. (RE-coal)

## RE-eq — CardinalityInvariancePossibility (LEMMA, LEMMA)

> **Cardinality Invariance Possibility.** There exist rearrangements `Σ → Σ'` such that the cardinality of the canonical maximal-run decomposition of `Σ'.M(d)` equals that of `Σ.M(d)`. (RE-eq)

## RE-other — OtherDocumentInvariance (LEMMA, LEMMA)

```
(A d' ∈ dom(Σ.M) : d' ≠ d :: Σ'.M(d') = Σ.M(d'))                                       (RE-other)
```

## RE-trans — TransclusionPreservation (LEMMA, LEMMA)

> **Transclusion Preservation.** For every transclusion relationship at Σ — every pair (a, d) with `a ∈ ran(Σ.M(d))` and `origin(a) ≠ d` — the foreign relationship at d is preserved: (i) `a ∈ ran(Σ'.M(d))` and (ii) the multiplicity of `a` at d is unchanged — both unconditional in `d`. Additionally (iii) `origin(a)`'s arrangement is unchanged when `origin(a) ≠ d_tgt` (the rearrangement target). (RE-trans)

Sub-claims:
- (i) `a ∈ ran(Σ'.M(d))` — unconditional in d
- (ii) `μ_a(Σ'.M(d)) = μ_a(Σ.M(d))` — unconditional in d
- (iii) `Σ'.M(origin(a)) = Σ.M(origin(a))` when `origin(a) ≠ d_tgt`

Note: a foreign address `a` with `origin(a) ≠ d` cannot arise at a link-subspace V-position (by CL-OWN); by S3★-aux V-positions are exhaustively content-subspace or link-subspace, so the witnessing V-position is content-subspace; S3★ then gives `a ∈ dom(Σ.C)`. By C2 (ASN-0093), `origin(a) ∈ dom(Σ.M)`.

## RE-subpres — AbstractSubspacePreservation (LEMMA, LEMMA)

```
(A v : v ∈ dom(Σ.M(d)) :: subspace(π(v)) = subspace(v))                                (RE-subpres)
```

Two-stage derivation:

*Stage 1 — binary constraint.* RA-frame's `dom(Σ'.M) = dom(Σ.M)` together with RA-dom gives `π(v) ∈ dom(Σ'.M(d))`. RA-adm preserves S3★-aux at Σ': `(A d, v' : v' ∈ dom(Σ'.M(d)) : subspace(v') = s_C ∨ subspace(v') = s_L)`. Applied at `v' = π(v)`, this gives `subspace(π(v)) ∈ {s_C, s_L}`.

*Stage 2 — cross-direction exclusion.*

- *Content-to-link direction:* Let `v ∈ dom(Σ.M(d))` with `subspace(v) = s_C`. Pre-state S3★ gives `Σ.M(d)(v) ∈ dom(Σ.C)`. Suppose `subspace(π(v)) = s_L`. RA-π gives `Σ'.M(d)(π(v)) = Σ.M(d)(v) ∈ dom(Σ.C)`, and RA-frame's `Σ'.C = Σ.C` gives `dom(Σ'.C) = dom(Σ.C)`, so `Σ'.M(d)(π(v)) ∈ dom(Σ'.C)`. But RA-adm requires post-state S3★'s link-subspace clause: `Σ'.M(d)(π(v)) ∈ dom(Σ'.L)`. L14 (`dom(Σ'.C) ∩ dom(Σ'.L) = ∅`) yields the contradiction.
- *Link-to-content direction:* Let `v ∈ dom(Σ.M(d))` with `subspace(v) = s_L`. Pre-state S3★ gives `Σ.M(d)(v) ∈ dom(Σ.L)`. Suppose `subspace(π(v)) = s_C`. RA-π combined with RA-frame's `Σ'.L = Σ.L` gives `Σ'.M(d)(π(v)) = Σ.M(d)(v) ∈ dom(Σ.L) = dom(Σ'.L)`. But post-state S3★'s content-subspace clause demands `Σ'.M(d)(π(v)) ∈ dom(Σ'.C)`. L14 again yields the contradiction.

## RE-sub — SubspaceFrame (LEMMA, LEMMA)

```
(A v : v ∈ dom(Σ.M(d)) ∧ subspace(v) ≠ S :: π(v) = v ∧ Σ'.M(d)(v) = Σ.M(d)(v))           (RE-sub)
```

Two conjuncts:
- `π(v) = v` — sourced from R-PPERM/R-SPERM non-S branch
- `Σ'.M(d)(v) = Σ.M(d)(v)` — sourced from R-FRAME-P/S(a); also follows from the first conjunct via RA-π

## RE-ext — InSubspaceExteriorFrame (LEMMA, LEMMA)

```
(A v : v ∈ V_S(d) ∧ (v < c₀ ∨ v ≥ c_{n−1}) :: π(v) = v ∧ Σ'.M(d)(v) = Σ.M(d)(v))    (RE-ext)
```

Two conjuncts:
- `π(v) = v` — sourced from R-PPERM/R-SPERM exterior branch
- `Σ'.M(d)(v) = Σ.M(d)(v)` — sourced from R-EXT; also follows from the first conjunct via RA-π

## RE-origin — OriginInvariance (LEMMA, LEMMA)

```
(A a ∈ T :: origin(a) at Σ' = origin(a) at Σ)                                           (RE-origin)
```

Origin is a function on tumblers, not state: `origin(a) = N(a).0.U(a).0.D(a)` (S7 of ASN-0036), a structural projection on T independent of any state component.

## RE-R — ProvenanceInvariance (LEMMA, LEMMA)

```
Σ'.R = Σ.R                                                                              (RE-R)
```

---

## RE-C★ — MultiStepContentStoreInvariance (LEMMA, LEMMA)

Multi-step content-store invariance:
```
Σ_n.C = Σ_0.C
```
No composition conditions. Follows from chaining RE-C across n steps.

## RE-L★ — MultiStepLinkStoreInvariance (LEMMA, LEMMA)

Multi-step link-store invariance:
```
dom(Σ_n.L) = dom(Σ_0.L)  ∧  (A a ∈ dom(Σ_0.L) :: Σ_n.L(a) = Σ_0.L(a))
```
No composition conditions.

## RE-R★ — MultiStepProvenanceInvariance (LEMMA, LEMMA)

Multi-step provenance invariance:
```
Σ_n.R = Σ_0.R
```
No composition conditions.

## RE-dom★ — MultiStepDomainStability (LEMMA, LEMMA)

Multi-step domain stability at fixed d:
```
dom(Σ_n.M(d)) = dom(Σ_0.M(d))
```
No composition conditions. At each step `Σᵢ₋₁ →_R Σᵢ` targeting `dᵢ`: either `dᵢ = d` (RE-dom) or `dᵢ ≠ d` (RE-other forces `Σᵢ.M(d) = Σᵢ₋₁.M(d)`).

## RE-ran★ — MultiStepRangeInvariance (LEMMA, LEMMA)

Multi-step range invariance at fixed d:
```
ran(Σ_n.M(d)) = ran(Σ_0.M(d))
```
No composition conditions.

## RE-μ★ — MultiStepPerAddressMultiplicityInvariance (LEMMA, LEMMA)

Multi-step per-address multiplicity invariance:
```
(A a ∈ T, d ∈ dom(Σ_0.M) :: μ_a(Σ_n.M(d)) = μ_a(Σ_0.M(d)))
```
No composition conditions.

## RE-cov★ — MultiStepCoverageInvariance (LEMMA, LEMMA)

Multi-step coverage invariance:
```
(A a ∈ dom(Σ_0.L), i :: coverage(Σ_n.L(a).eᵢ) = coverage(Σ_0.L(a).eᵢ))
```
No composition conditions.

## RE-disc★ — MultiStepDiscoverabilityInvariance (LEMMA, LEMMA)

Multi-step discoverability invariance:
```
(A a ∈ dom(Σ_0.L), d ∈ dom(Σ_0.M) :: discoverable_from(a, d, Σ_n) ⟺ discoverable_from(a, d, Σ_0))
```
No composition conditions.

## RE-proj★ — MultiStepProjectionTransport (LEMMA, LEMMA)

Multi-step projection transport:
```
project(e, d, Σ_n) = (π̂_n ∘ ⋯ ∘ π̂_1)(project(e, d, Σ_0))
```
where for each step `Σ_{i−1} →_R Σ_i` targeting document `dᵢ` with rearrangement permutation `π_i` on `dom(Σ_{i−1}.M(dᵢ))`, `π̂_i := π_i` when `dᵢ = d` and `π̂_i := id_{dom(Σ_{i−1}.M(d))}` otherwise.

For sequences where every step targets the same document `d`, reduces to:
```
project(e, d, Σ_n) = (π_n ∘ ⋯ ∘ π_1)(project(e, d, Σ_0))
```
No composition conditions.

## RE-other★ — MultiStepOtherDocumentInvariance (LEMMA, LEMMA)

Multi-step other-document invariance at fixed `d'`:
```
Σ_n.M(d') = Σ_0.M(d')
```
Composition condition: no step in the sequence targets `d'`.

## RE-sub★ — MultiStepSubspaceFrame (LEMMA, LEMMA)

Multi-step subspace frame at fixed d: for every `v ∈ dom(Σ_0.M(d))` with `subspace(v) ≠ S`, the V-position remains pointwise fixed and its image is preserved across all steps targeting d.

Formally: `(A v : v ∈ dom(Σ_0.M(d)) ∧ subspace(v) ≠ S :: (A i : dᵢ = d :: π_i(v) = v ∧ Σᵢ.M(d)(v) = Σᵢ₋₁.M(d)(v)))` and thus `Σ_n.M(d)(v) = Σ_0.M(d)(v)`.

No composition conditions (per-step RE-sub chains through identity on non-targeting steps).

## RE-ext★ — MultiStepInSubspaceExteriorFrame (LEMMA, LEMMA)

Multi-step in-subspace exterior frame at fixed d: for every `v` that lies in the in-S exterior of every targeted step — i.e., for every step `Σᵢ₋₁ →_R Σᵢ` targeting d with cut sequence `Kᵢ` and cut subspace `Sᵢ`, either the step does not target d, or `v ∈ V_{Sᵢ}(Σᵢ₋₁.M(d)) ∧ (v < c₀,ᵢ ∨ v ≥ c_{n−1},ᵢ)` — the V-position remains pointwise fixed and its image is preserved across all such steps.

Composition condition: the `v` in question must lie in the in-S exterior of every step in the sequence that targets d; for steps not targeting d, RE-other applies and `v` is fixed unconditionally.

## RE-trans★ — MultiStepTransclusionPreservation (LEMMA, LEMMA)

Multi-step transclusion preservation: for every pair (a, d) with `a ∈ ran(Σ_0.M(d))` and `origin(a) ≠ d`:
- (i) `a ∈ ran(Σ_n.M(d))` — no composition conditions
- (ii) `μ_a(Σ_n.M(d)) = μ_a(Σ_0.M(d))` — no composition conditions
- (iii) `Σ_n.M(origin(a)) = Σ_0.M(origin(a))` — composition condition: no step in the sequence targets `origin(a)`

Conclusions (i) and (ii) follow from per-step preservation of `ran(M(d))` and `μ_a(M(d))` with the same two-case split as RE-other★ applied at d. Conclusion (iii) requires the restriction, since if some intermediate step targets `origin(a)`, that step reorders `origin(a)`'s arrangement.

## RE-frag★ / RE-coal★ / RE-eq★ — MultiStepRunDecompositionArbitrary (LEMMA, LEMMA)

Arbitrary per-step direction: for every `n ≥ 1` and every finite direction sequence `(s_1, ..., s_n) ∈ {+, −, =}^n`, there exists a multi-step REARRANGE sequence `Σ_0 →_R Σ_1 →_R ⋯ →_R Σ_n` targeting a single document `d` such that step `i` (`Σ_{i−1} →_R Σ_i`) realises direction `s_i`, where:
- `+` = strict increase of canonical maximal-run-decomposition cardinality of `M(d)`
- `−` = strict decrease of canonical maximal-run-decomposition cardinality of `M(d)`
- `=` = exact preservation of canonical maximal-run-decomposition cardinality of `M(d)`

No composition conditions (existential; concatenation construction proves it). No uniform per-step monotonicity is asserted, and no claim is made about the net cardinality change `|runs(Σ_n.M(d))| − |runs(Σ_0.M(d))|` across the full sequence.

## RE-origin★ — MultiStepOriginInvariance (LEMMA, LEMMA)

Multi-step origin invariance:
```
(A a ∈ T :: origin(a) at Σ_n = origin(a) at Σ_0)
```
No composition conditions. Structural (state-independent).
