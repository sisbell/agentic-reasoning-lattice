# ASN-0091 Claim Statements

*Source: ASN-0091-rearrange-operation.md (revised 2026-05-26) — Extracted: 2026-06-03*

## Definition — PerAddressMultiplicity

For each I-address `a` and registered document `d'`:
```
μ_a(M(d')) = |{v : v ∈ dom(M(d')) ∧ M(d')(v) = a}|
```

## Definition — DiscoverableFrom

A link `a` is *discoverable from* document `d` at state `Σ` when:
```
discoverable_from(a, d, Σ) ⟺ (E i :: coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)
```
(characterisation supplied by foundation lemma LP12 of ASN-0098)

## Definition — ProjectionSet

```
project(e, d, Σ) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}
```

## Definition — ProjectionTransportMap

Define the *projection transport* `π̂_d`:
```
π̂_d := π                       when d = d_tgt
π̂_d := id_{dom(Σ.M(d))}        when d ≠ d_tgt
```
`π̂_d` is in every case a bijection between `dom(Σ.M(d))` and `dom(Σ'.M(d))`.

## Definition — VstreamOnly

A transition `Σ → Σ'` is *Vstream-only on `d`* when:

```
d ∈ dom(Σ.M)                                                                            (RA-reg)
```
and
```
dom(Σ'.M(d)) = dom(Σ.M(d))                                                              (RA-dom)
```
and there exists a bijection
```
π : dom(Σ.M(d)) → dom(Σ'.M(d))
```
satisfying
```
(A v : v ∈ dom(Σ.M(d)) : Σ'.M(d)(π(v)) = Σ.M(d)(v))                                    (RA-π)
```
together with
```
Σ'.C = Σ.C  ∧  Σ'.L = Σ.L  ∧  Σ'.E = Σ.E  ∧  Σ'.R = Σ.R                                 (RA-frame)
  ∧  dom(Σ'.M) = dom(Σ.M)
  ∧  (A d' ∈ dom(Σ.M) : d' ≠ d : Σ'.M(d') = Σ.M(d'))
```
and
```
every per-state foundation invariant satisfied by Σ is satisfied by Σ'                  (RA-adm)
```

---

## RA-reg — RearrangeReg (PRE, precondition)

```
d ∈ dom(Σ.M)
```

## RA-dom — RearrangeDom (DEF, definition)

```
dom(Σ'.M(d)) = dom(Σ.M(d))
```

## RA-π — RearrangePi (DEF, definition)

```
π : dom(Σ.M(d)) → dom(Σ'.M(d)) is a bijection with
(A v : v ∈ dom(Σ.M(d)) : Σ'.M(d)(π(v)) = Σ.M(d)(v))
```

## RA-frame — RearrangeFrame (DEF, definition)

```
Σ'.C = Σ.C  ∧  Σ'.L = Σ.L  ∧  Σ'.E = Σ.E  ∧  Σ'.R = Σ.R
  ∧  dom(Σ'.M) = dom(Σ.M)
  ∧  (A d' ∈ dom(Σ.M) : d' ≠ d : Σ'.M(d') = Σ.M(d'))
```

## RA-adm — RearrangeAdm (DEF, definition)

```
every per-state foundation invariant satisfied by Σ is satisfied by Σ'
```
Composite-boundary properties P4★/P4a/P7a and state-independent theorems S5, T0(a/b) lie outside its scope, discharged by their own arguments.

---

## RE-C — ContentStoreInvariance (LEMMA, lemma)

```
Σ'.C = Σ.C
```

## RE-dom — DomainStability (LEMMA, lemma)

```
dom(Σ'.M(d)) = dom(Σ.M(d))
```

## RE-ran — RangeInvariance (LEMMA, lemma)

```
(A d' ∈ dom(Σ.M) :: ran(Σ'.M(d')) = ran(Σ.M(d')))
```

## RE-μ — MultiplicityInvariance (LEMMA, lemma)

```
(A a ∈ T, d' ∈ dom(Σ.M) :: μ_a(Σ'.M(d')) = μ_a(Σ.M(d')))
```

where `μ_a(M(d')) = |{v : v ∈ dom(M(d')) ∧ M(d')(v) = a}|`.

## RE-L — LinkStoreInvariance (LEMMA, lemma)

```
dom(Σ'.L) = dom(Σ.L)  ∧  (A a ∈ dom(Σ.L) :: Σ'.L(a) = Σ.L(a))
```

## RE-cov — CoverageInvariance (LEMMA, lemma)

```
(A a ∈ dom(Σ.L), i : 1 ≤ i ≤ |Σ.L(a)| :: coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ))
```

## RE-disc — DiscoverabilityInvariance (LEMMA, lemma)

```
(A a ∈ dom(Σ.L), d ∈ dom(Σ.M) :: discoverable_from(a, d, Σ') ⟺ discoverable_from(a, d, Σ))
```

Expanded:
```
discoverable_from(a, d, Σ')
  ⟺ (E i :: coverage(Σ'.L(a).eᵢ) ∩ ran(Σ'.M(d)) ≠ ∅)
  ⟺ (E i :: coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)
  ⟺ discoverable_from(a, d, Σ)
```

## RE-proj — ProjectionTransport (LEMMA, lemma)

```
project(e, d, Σ') = π̂_d(project(e, d, Σ))      for every d ∈ dom(Σ.M)
```

where `π̂_d := π` when `d = d_tgt` and `π̂_d := id_{dom(Σ.M(d))}` for `d ≠ d_tgt`.

Equivalently at `d_tgt`:
```
project(e, d_tgt, Σ') = π(project(e, d_tgt, Σ))
```

## RE-frag — FragmentationPossibility (LEMMA, lemma)

There exist rearrangements `Σ → Σ'` such that the cardinality of the canonical maximal-run decomposition of `Σ'.M(d)` is strictly greater than that of `Σ.M(d)`.

## RE-coal — CoalescencePossibility (LEMMA, lemma)

There exist rearrangements `Σ → Σ'` such that the cardinality of the canonical maximal-run decomposition of `Σ'.M(d)` is strictly less than that of `Σ.M(d)`.

## RE-eq — CardinalityInvariancePossibility (LEMMA, lemma)

There exist rearrangements `Σ → Σ'` such that the cardinality of the canonical maximal-run decomposition of `Σ'.M(d)` equals that of `Σ.M(d)`.

## RE-other — OtherDocumentInvariance (LEMMA, lemma)

```
(A d' ∈ dom(Σ.M) : d' ≠ d :: Σ'.M(d') = Σ.M(d'))
```

## RE-trans — TransclusionPreservation (LEMMA, lemma)

For every transclusion relationship at Σ — every pair `(a, d)` with `a ∈ ran(Σ.M(d))` and `origin(a) ≠ d`:

- (i) `a ∈ ran(Σ'.M(d))` — unconditional in `d`
- (ii) the multiplicity of `a` at `d` is unchanged (`μ_a(Σ'.M(d)) = μ_a(Σ.M(d))`) — unconditional in `d`
- (iii) `Σ'.M(origin(a)) = Σ.M(origin(a))` — conditional on `origin(a) ≠ d_tgt` (the rearrangement target)

## RE-subpres — SubspacePreservation (LEMMA, lemma)

```
(A v : v ∈ dom(Σ.M(d)) :: subspace(π(v)) = subspace(v))
```

No V-position crosses from the content subspace to the link subspace or vice versa under any admissible `π`.

## RE-sub — SubspaceFrame (LEMMA, lemma)

```
(A v : v ∈ dom(Σ.M(d)) ∧ subspace(v) ≠ S :: π(v) = v ∧ Σ'.M(d)(v) = Σ.M(d)(v))
```

## RE-ext — InSubspaceExteriorFrame (LEMMA, lemma)

```
(A v : v ∈ V_S(d) ∧ (v < c₀ ∨ v ≥ c_{n−1}) :: π(v) = v ∧ Σ'.M(d)(v) = Σ.M(d)(v))
```

## RE-origin — OriginInvariance (LEMMA, lemma)

```
(A a ∈ T :: origin(a) at Σ' = origin(a) at Σ)
```

origin is a function on tumblers, not state; it has no temporal dimension.

## RE-R — ProvenanceInvariance (LEMMA, lemma)

```
Σ'.R = Σ.R
```

---

## RE-C★ — ContentStoreInvarianceMulti (LEMMA, lemma)

For a finite sequence `Σ_0 →_R Σ_1 →_R ⋯ →_R Σ_n`:
```
Σ_n.C = Σ_0.C
```
Composition conditions: none.

## RE-L★ — LinkStoreInvarianceMulti (LEMMA, lemma)

```
dom(Σ_n.L) = dom(Σ_0.L)  ∧  (A a ∈ dom(Σ_0.L) :: Σ_n.L(a) = Σ_0.L(a))
```
Composition conditions: none.

## RE-R★ — ProvenanceInvarianceMulti (LEMMA, lemma)

```
Σ_n.R = Σ_0.R
```
Composition conditions: none.

## RE-dom★ — DomainStabilityMulti (LEMMA, lemma)

For fixed `d`:
```
dom(Σ_n.M(d)) = dom(Σ_0.M(d))
```
Composition conditions: none.

## RE-ran★ — RangeInvarianceMulti (LEMMA, lemma)

For fixed `d`:
```
ran(Σ_n.M(d)) = ran(Σ_0.M(d))
```
Composition conditions: none.

## RE-μ★ — MultiplicityInvarianceMulti (LEMMA, lemma)

```
(A a ∈ T, d ∈ dom(Σ_0.M) :: μ_a(Σ_n.M(d)) = μ_a(Σ_0.M(d)))
```
Composition conditions: none.

## RE-cov★ — CoverageInvarianceMulti (LEMMA, lemma)

```
(A a ∈ dom(Σ_0.L), i :: coverage(Σ_n.L(a).eᵢ) = coverage(Σ_0.L(a).eᵢ))
```
Composition conditions: none.

## RE-disc★ — DiscoverabilityInvarianceMulti (LEMMA, lemma)

```
(A a ∈ dom(Σ_0.L), d ∈ dom(Σ_0.M) :: discoverable_from(a, d, Σ_n) ⟺ discoverable_from(a, d, Σ_0))
```
Composition conditions: none.

## RE-proj★ — ProjectionTransportMulti (LEMMA, lemma)

```
project(e, d, Σ_n) = (π̂_n ∘ ⋯ ∘ π̂_1)(project(e, d, Σ_0))
```

where for each step `Σ_{i−1} →_R Σ_i` targeting document `dᵢ` with rearrangement permutation `π_i` on `dom(Σ_{i−1}.M(dᵢ))`:
```
π̂_i := π_i                             when dᵢ = d
π̂_i := id_{dom(Σ_{i−1}.M(d))}          otherwise
```

For sequences in which every step targets the same document `d`:
```
project(e, d, Σ_n) = (π_n ∘ ⋯ ∘ π_1)(project(e, d, Σ_0))
```
Composition conditions: none.

## RE-other★ — OtherDocumentInvarianceMulti (LEMMA, lemma)

For fixed `d'`:
```
Σ_n.M(d') = Σ_0.M(d')
```
Composition conditions: no step in the sequence targets `d'`.

## RE-sub★ — SubspaceFrameMulti (LEMMA, lemma)

For fixed `d`: for every `v ∈ dom(Σ_0.M(d))` with `subspace(v) ≠ S`, the V-position remains pointwise fixed and its image is preserved across all steps targeting `d`:
```
(A i : step Σ_{i−1} →_R Σ_i targets d :: π_i(v) = v ∧ Σ_i.M(d)(v) = Σ_{i−1}.M(d)(v))
```
Composition conditions: none (per-step RE-sub chains through identity on non-targeting steps).

## RE-ext★ — InSubspaceExteriorFrameMulti (LEMMA, lemma)

For fixed `d` and V-position `v`: for every step `Σ_{i−1} →_R Σ_i` targeting `d` with cut sequence `Kᵢ` of cut subspace `Sᵢ`, if
```
(v ∈ V_{Sᵢ}(Σ_{i−1}.M(d)) ∧ (v < c₀,ᵢ ∨ v ≥ c_{n−1},ᵢ))  ∨  dᵢ ≠ d
```
holds at every step, then:
```
π_n(...π_1(v)...) = v  ∧  Σ_n.M(d)(v) = Σ_0.M(d)(v)
```
Composition conditions: `v` must lie in the in-S exterior of every step in the sequence that targets `d`.

## RE-trans★ — TransclusionPreservationMulti (LEMMA, lemma)

For a finite sequence `Σ_0 →_R Σ_1 →_R ⋯ →_R Σ_n`, for every `(a, d)` with `a ∈ ran(Σ_0.M(d))` and `origin(a) ≠ d`:

- (i) `a ∈ ran(Σ_n.M(d))` — unconditional
- (ii) `μ_a(Σ_n.M(d)) = μ_a(Σ_0.M(d))` — unconditional
- (iii) `Σ_n.M(origin(a)) = Σ_0.M(origin(a))` — conditional on no step in the sequence targeting `origin(a)`

Composition conditions: (iii) requires no step targets `origin(a)`; (i)+(ii) require no restriction.

## RE-frag★/RE-coal★/RE-eq★ — ArbitraryDirectionMulti (LEMMA, lemma)

For every `n ≥ 1` and every finite direction sequence `(s_1, ..., s_n) ∈ {+, −, =}^n`, there exists a multi-step REARRANGE sequence `Σ_0 →_R Σ_1 →_R ⋯ →_R Σ_n` targeting a single document `d` such that step `i` (`Σ_{i−1} →_R Σ_i`) realises direction `s_i`, where:
```
+ : |runs(Σ_i.M(d))| > |runs(Σ_{i−1}.M(d))|   (strict increase)
− : |runs(Σ_i.M(d))| < |runs(Σ_{i−1}.M(d))|   (strict decrease)
= : |runs(Σ_i.M(d))| = |runs(Σ_{i−1}.M(d))|   (exact preservation)
```

Composition conditions: none (existential; concatenation construction via spatial partitioning with RE-ext bridging between steps).

## RE-origin★ — OriginInvarianceMulti (LEMMA, lemma)

```
(A a ∈ T :: origin(a) is unchanged across Σ_0 →_R ⋯ →_R Σ_n)
```
Composition conditions: none (state-independent).

---

## Definition — ChainDisjointAdjacency

**Inline lemma.** For chain elements `x ∈ A_{s_X}(d_X)` and `y ∈ A_{s_Y}(d_Y)` with `(d_X, s_X) ≠ (d_Y, s_Y)`:
```
¬(x + 1 = y)  ∧  ¬(y + 1 = x)
```

Justification: each chain element of `A_{s_X}(d_X)` has the structural form `[d_X, 0, s_X, k]` for some `k ≥ 1`; the chain-adjacency operator `inc(·, 0)` from TA5(c) preserves length and modifies only the rightmost position, so:
```
x + 1 = [d_X, 0, s_X, k_x + 1]
```
For `x + 1 = y` to hold, T3 (CanonicalRepresentation) requires component-wise equality `(d_X, s_X, k_x + 1) = (d_Y, s_Y, k_y)`, which forces `d_X = d_Y` and `s_X = s_Y`, contradicting `(d_X, s_X) ≠ (d_Y, s_Y)`. Symmetric argument applies to `y + 1 = x`.
