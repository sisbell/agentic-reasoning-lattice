# ASN-0091 Claim Statements

*Source: ASN-0091-rearrange-operation.md (revised 2026-05-26) — Extracted: 2026-06-04*

## Definition — PerAddressMultiplicity

For each I-address `a` and each registered document `d'`, define `μ_a(M(d')) = |{v : v ∈ dom(M(d')) ∧ M(d')(v) = a}|`.

## Definition — ProjectionSet

`project(e, b, Σ) = {v ∈ dom(M(b)) : M(b)(v) ∈ coverage(e)}`, taken at an arbitrary document `b ∈ dom(Σ.M)`.

## Definition — ProjectionTransportBijection

Define the *projection transport* `π̂_b`: `π̂_b := π` when `b = d` and `π̂_b := id_{dom(Σ.M(b))}` when `b ≠ d`. The identity case is well-typed because RE-other forces `dom(Σ'.M(b)) = dom(Σ.M(b))` for `b ≠ d`, so `π̂_b` is in every case a bijection between `dom(Σ.M(b))` and `dom(Σ'.M(b))`.

## Definition — DiscoverableFrom

A link is *discoverable from* document `d` at state `Σ` when some endset's coverage intersects the document's I-address range — when there exists a slot `i` with `coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅` (the characterisation supplied by foundation lemma LP12 of ASN-0098).

---

## RA-reg — RearrangementRegistrationPrecond (PRE, requires)

```
d ∈ dom(Σ.M)                                                                            (RA-reg)
```

## RA-dom — RearrangementDomainClause (DEF, clause)

```
dom(Σ'.M(d)) = dom(Σ.M(d))                                                              (RA-dom)
```

## RA-π — RearrangementEquation (DEF, clause)

```
(A v : v ∈ dom(Σ.M(d)) : Σ'.M(d)(π(v)) = Σ.M(d)(v))                                    (RA-π)
```

Where `π : dom(Σ.M(d)) → dom(Σ'.M(d))` is a bijection (the *rearrangement permutation*) carrying each pre-state pair `(v, Σ.M(d)(v))` to the post-state pair `(π(v), Σ.M(d)(v))`, holding the I-address fixed while moving the V-position.

## RA-frame — RearrangementFrame (DEF, clause)

```
Σ'.C = Σ.C  ∧  Σ'.L = Σ.L  ∧  Σ'.E = Σ.E  ∧  Σ'.R = Σ.R                                 (RA-frame)
  ∧  dom(Σ'.M) = dom(Σ.M)
  ∧  (A d' ∈ dom(Σ.M) : d' ≠ d : Σ'.M(d') = Σ.M(d'))
```

## RA-adm — RearrangementAdmissibility (DEF, clause)

```
every per-state foundation invariant satisfied by Σ is satisfied by Σ'                  (RA-adm)
```

## RA-bndy — CompositeBoundaryPrecond (PRE, requires)

Scopes the composite-boundary properties P4★ ∧ P4a ∧ P7a only:

```
Σ is the final state of a trace of valid composites Σ₀ →* Σ                             (RA-bndy)
```

---

## RE-C — ContentStoreInvariance (INV, predicate)

```
Σ'.C = Σ.C                                                                              (RE-C)
```

RA-frame fixes the content store with equality, so no content is allocated, freed, or modified by rearrangement.

## RE-dom — DomainStability (INV, predicate)

```
dom(Σ'.M(d)) = dom(Σ.M(d))                                                              (RE-dom)
```

Every V-position that was populated in d remains populated; every V-position that was unpopulated remains unpopulated.

## RE-ran — RangeInvariance (LEMMA, lemma)

```
(A d' ∈ dom(Σ.M) :: ran(Σ'.M(d')) = ran(Σ.M(d')))                                      (RE-ran)
```

Derived via two-case argument: for target `d`, via the π-bijection; for `d' ≠ d`, via RA-frame's other-document clause `Σ'.M(d') = Σ.M(d')`.

## RE-μ — PerAddressMultiplicityInvariance (LEMMA, lemma)

```
(A a ∈ T, d' ∈ dom(Σ.M) :: μ_a(Σ'.M(d')) = μ_a(Σ.M(d')))                              (RE-μ)
```

Where `μ_a(M(d')) = |{v : v ∈ dom(M(d')) ∧ M(d')(v) = a}|`. For the target document `d`:
```
μ_a(Σ'.M(d)) = |{v' : v' ∈ dom(Σ'.M(d)) ∧ Σ'.M(d)(v') = a}|
             = |{π(v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}|       [substitute v' = π(v)]
             = |{v : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}|           [π injective]
             = μ_a(Σ.M(d))
```

## RE-L — LinkStoreInvariance (INV, predicate)

```
dom(Σ'.L) = dom(Σ.L)  ∧  (A a ∈ dom(Σ.L) :: Σ'.L(a) = Σ.L(a))                          (RE-L)
```

Every link persists across rearrangement with its full endset sequence intact. No link is added, removed, or modified.

## RE-cov — CoverageInvariance (LEMMA, lemma)

```
(A a ∈ dom(Σ.L), i : 1 ≤ i ≤ |Σ.L(a)| :: coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ))   (RE-cov)
```

Coverage of an endset is a function of the endset's span representation alone (ASN-0098). RE-L preserves every endset verbatim, so coverage is preserved.

## RE-disc — DiscoverabilityInvariance (LEMMA, lemma)

```
(A a ∈ dom(Σ.L), d ∈ dom(Σ.M) :: discoverable_from(a, d, Σ') ⟺ discoverable_from(a, d, Σ))    (RE-disc)
```

Derivation:
```
discoverable_from(a, d, Σ')
  ⟺ (E i :: coverage(Σ'.L(a).eᵢ) ∩ ran(Σ'.M(d)) ≠ ∅)
  ⟺ (E i :: coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)
  ⟺ discoverable_from(a, d, Σ)
```

## RE-proj — ProjectionTransport (LEMMA, lemma)

```
project(e, b, Σ') = π̂_b(project(e, b, Σ))      for every b ∈ dom(Σ.M)                  (RE-proj)
```

Where `π̂_b := π` when `b = d` and `π̂_b := id_{dom(Σ.M(b))}` when `b ≠ d`.

Equivalently at the target: `project(e, d, Σ') = π(project(e, d, Σ))`.

Target case derivation: for any `v ∈ dom(Σ.M(d))`:
```
v ∈ project(e, d, Σ)
  ⟺ Σ.M(d)(v) ∈ coverage(e)              [definition of project]
  ⟺ Σ'.M(d)(π(v)) ∈ coverage(e)          [RA-π: Σ'.M(d)(π(v)) = Σ.M(d)(v)]
  ⟺ π(v) ∈ project(e, d, Σ')             [definition; π(v) ∈ dom(Σ'.M(d)) by RA-π's codomain]
```

## RE-frag — FragmentationPossibility (EXISTENCE, lemma)

> **Fragmentation Possibility.** There exist rearrangements `Σ → Σ'` such that the cardinality of the canonical maximal-run decomposition of `Σ'.M(d)` is strictly greater than that of `Σ.M(d)`. (RE-frag)

## RE-coal — CoalescencePossibility (EXISTENCE, lemma)

> **Coalescence Possibility.** There exist rearrangements `Σ → Σ'` such that the cardinality of the canonical maximal-run decomposition of `Σ'.M(d)` is strictly less than that of `Σ.M(d)`. (RE-coal)

## RE-eq — CardinalityInvariancePossibility (EXISTENCE, lemma)

> **Cardinality Invariance Possibility.** There exist rearrangements `Σ → Σ'` such that the cardinality of the canonical maximal-run decomposition of `Σ'.M(d)` equals that of `Σ.M(d)`. (RE-eq)

Together, RE-frag, RE-coal, and RE-eq record that the maximal-run-decomposition cardinality is *neither monotonically non-decreasing nor monotonically non-increasing nor invariant* under REARRANGE.

## RE-other — OtherDocumentInvariance (INV, predicate)

```
(A d' ∈ dom(Σ.M) : d' ≠ d :: Σ'.M(d') = Σ.M(d'))                                       (RE-other)
```

## RE-trans — TransclusionPreservation (LEMMA, lemma)

> **Transclusion Preservation.** For every transclusion relationship at Σ — every pair (a, d_view) with `a ∈ ran(Σ.M(d_view))` and `origin(a) ≠ d_view` — the foreign relationship at d_view is preserved:
> - (i) `a ∈ ran(Σ'.M(d_view))` — unconditional in `d_view`
> - (ii) the multiplicity of `a` at d_view is unchanged — unconditional in `d_view`
> - (iii) `origin(a)`'s arrangement is unchanged when `origin(a) ≠ d` (the rearrangement target)
>
> (RE-trans)

Precondition for (iii): `origin(a) ≠ d`. Conclusions (i) and (ii) at `d_view` remain intact regardless of whether `origin(a) = d`.

## RE-sub — SubspaceFrame (LEMMA, lemma)

```
(A v : v ∈ dom(Σ.M(d)) ∧ subspace(v) ≠ S :: π(v) = v ∧ Σ'.M(d)(v) = Σ.M(d)(v))           (RE-sub)
```

Where `S` is the cut subspace. V-positions in subspaces *other than* the cut subspace S are left wholly unpermuted. π-fixity from R-PPERM/R-SPERM non-S branch; arrangement preservation from R-FRAME-P/S(a).

## RE-ext — InSubspaceExteriorFrame (LEMMA, lemma)

```
(A v : v ∈ V_S(d) ∧ (v < c₀ ∨ v ≥ c_{n−1}) :: π(v) = v ∧ Σ'.M(d)(v) = Σ.M(d)(v))    (RE-ext)
```

V-positions *within* the cut subspace S that lie *outside* the affected range `[c₀, c_{n−1})`. π-fixity from R-PPERM/R-SPERM exterior branch; arrangement preservation from R-EXT.

## L-chain — ChainDisjointAdjacency (LEMMA, lemma)

> **Lemma L-chain (ChainDisjointAdjacency).** For chain elements `x ∈ A_{s_X}(d_X)` and `y ∈ A_{s_Y}(d_Y)` with `(d_X, s_X) ≠ (d_Y, s_Y)` — i.e., the two sub-allocator chains differ in either their home document or their subspace — neither `x + 1 = y` nor `y + 1 = x` can hold.

*Precondition fixing the successor identification.* Sub-allocator chain elements are T4-valid (ChainElementT4Validity, ASN-0093), so for every chain element `x` we have `sig(x) = #x` (TA5-SigValid, ASN-0034), and hence the ordinal successor `x + 1 = shift(x, 1)` (OrdinalShiftBase, ASN-0058) coincides with `inc(x, 0)`.

*Justification.* The chain-adjacency successor `x + 1 = inc(x, 0)` preserves sub-allocator chain membership, since each sub-allocator chain is closed under `inc(·, 0)` by the SiblingStream recurrence `t_{n+1} = inc(t_n, 0)` (ChainDiscipline, ASN-0093) — so `x + 1 ∈ dom(A_{s_X}(d_X))`; symmetrically `y + 1 ∈ dom(A_{s_Y}(d_Y))`. Distinct sub-allocator chains have disjoint domains — cross-subspace by ASN-0093's DisjointSubAllocatorChains and cross-document by its CrossDocumentDisjointness, both instances of T10a.6 (DomainDisjointness, ASN-0034). Hence `x + 1 ∈ dom(A_{s_X}(d_X))` and `y ∈ dom(A_{s_Y}(d_Y))` lie in disjoint domains, forcing `x + 1 ≠ y`; the symmetric placement of `y + 1` and `x` forces `y + 1 ≠ x`.

## RE-origin — OriginInvariance (INV, predicate)

```
(A a ∈ T :: origin(a) at Σ' = origin(a) at Σ)                                           (RE-origin)
```

The function `origin(a) = N(a).0.U(a).0.D(a)` (S7 of ASN-0036) projects an I-address to the document-level prefix encoding its allocator. Origin consults only the address `a` — it is a structural projection on T, independent of any state component.

## RE-R — ProvenanceInvariance (INV, predicate)

```
Σ'.R = Σ.R                                                                              (RE-R)
```

---

## RE-C★ — ContentStoreInvarianceMultiStep (LEMMA, lemma)

For a finite sequence `Σ₀ →_R Σ₁ →_R ⋯ →_R Σ_n` of REARRANGE-only transitions:

```
Σ_n.C = Σ_0.C
```

Composition condition: none.

## RE-L★ — LinkStoreInvarianceMultiStep (LEMMA, lemma)

```
dom(Σ_n.L) = dom(Σ_0.L)  ∧  (A a ∈ dom(Σ_0.L) :: Σ_n.L(a) = Σ_0.L(a))
```

Composition condition: none.

## RE-R★ — ProvenanceInvarianceMultiStep (LEMMA, lemma)

```
Σ_n.R = Σ_0.R
```

Composition condition: none.

## RE-dom★ — DomainStabilityMultiStep (LEMMA, lemma)

At fixed `d`:

```
dom(Σ_n.M(d)) = dom(Σ_0.M(d))
```

Composition condition: none. At each step `Σᵢ₋₁ →_R Σᵢ` targeting `dᵢ`, either `dᵢ = d` (per-step RE-dom preserves) or `dᵢ ≠ d` (RE-other gives `Σᵢ.M(d) = Σᵢ₋₁.M(d)`).

## RE-ran★ — RangeInvarianceMultiStep (LEMMA, lemma)

At fixed `d`:

```
ran(Σ_n.M(d)) = ran(Σ_0.M(d))
```

Composition condition: none.

## RE-μ★ — PerAddressMultiplicityInvarianceMultiStep (LEMMA, lemma)

```
(A a ∈ T, d ∈ dom(Σ_0.M) :: μ_a(Σ_n.M(d)) = μ_a(Σ_0.M(d)))
```

Composition condition: none.

## RE-cov★ — CoverageInvarianceMultiStep (LEMMA, lemma)

```
(A a ∈ dom(Σ_0.L), i :: coverage(Σ_n.L(a).eᵢ) = coverage(Σ_0.L(a).eᵢ))
```

Composition condition: none.

## RE-disc★ — DiscoverabilityInvarianceMultiStep (LEMMA, lemma)

```
(A a ∈ dom(Σ_0.L), d ∈ dom(Σ_0.M) :: discoverable_from(a, d, Σ_n) ⟺ discoverable_from(a, d, Σ_0))
```

Composition condition: none.

## RE-proj★ — ProjectionTransportMultiStep (LEMMA, lemma)

```
project(e, d, Σ_n) = (π̂_n ∘ ⋯ ∘ π̂_1)(project(e, d, Σ_0))
```

Where `π̂_i = π_i` on steps targeting `d` and `π̂_i = id` otherwise.

Composition condition: none.

## RE-other★ — OtherDocumentInvarianceMultiStep (LEMMA, lemma)

At fixed `d'`:

```
Σ_n.M(d') = Σ_0.M(d')
```

Composition condition: no step in the sequence targets `d'`.

## RE-sub★ — SubspaceFrameMultiStep (LEMMA, lemma)

At fixed `d`: for every `v ∈ dom(Σ_0.M(d))` with `subspace(v) ≠ S`, the V-position remains pointwise fixed and its image is preserved across all steps targeting `d`.

Composition condition: none (per-step RE-sub chains through identity on non-targeting steps).

## RE-ext★ — InSubspaceExteriorFrameMultiStep (LEMMA, lemma)

At fixed `d`: for every `v` that lies in the in-S exterior of every targeted step — i.e., for every step `Σᵢ₋₁ →_R Σᵢ` targeting `d` with cut sequence `Kᵢ` and cut subspace `Sᵢ`:
```
v ∈ V_{Sᵢ}(Σᵢ₋₁.M(d)) ∧ (v < c₀,ᵢ ∨ v ≥ c_{n−1},ᵢ)
```
or the step does not target `d` — the V-position remains pointwise fixed and its image is preserved across all such steps.

Composition condition: the `v` in question must lie in the in-S exterior of every step in the sequence that targets `d`; for steps not targeting `d`, RE-other applies and `v` is fixed unconditionally.

## RE-trans★ — TransclusionPreservationMultiStep (LEMMA, lemma)

For every `(a, d_view)` with `a ∈ ran(Σ_0.M(d_view))` and `origin(a) ≠ d_view`:

- (i) `a ∈ ran(Σ_n.M(d_view))` — unconditional
- (ii) multiplicity of `a` at `d_view` is preserved across `Σ_0` to `Σ_n` — unconditional
- (iii) `origin(a)`'s arrangement is unchanged across the sequence

Composition condition: (i)+(ii) require no restriction; (iii) requires no step in the sequence targets `origin(a)`.

## RE-frag★ / RE-coal★ / RE-eq★ — ArbitraryPerStepDirection (EXISTENCE, lemma)

For every `n ≥ 1` and every finite direction sequence `(s_1, …, s_n) ∈ {+, −, =}^n`, there exists a multi-step REARRANGE sequence `Σ_0 →_R ⋯ →_R Σ_n` targeting a single document `d` such that step `i` realises direction `s_i`:
- `+` = strict increase in maximal-run-decomposition cardinality of `M(d)`
- `−` = strict decrease in maximal-run-decomposition cardinality of `M(d)`
- `=` = exact preservation of maximal-run-decomposition cardinality of `M(d)`

No uniform per-step monotonicity, and no claim about net cardinality change, is asserted.

## RE-origin★ — OriginInvarianceMultiStep (INV, predicate)

```
(A a ∈ T :: origin(a) is unchanged across Σ_0 →_R ⋯ →_R Σ_n)
```

Composition condition: none (state-independent).
