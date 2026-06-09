# ASN-0118 Claim Statements

*Source: ASN-0118-copy-operation.md (revised 2026-06-08) — Extracted: 2026-06-09*

## Definition — ActivePositions

```
act(ρ, Σ) = dom(Σ.M(d_s)) ∩ ⟦σ⟧
```

Where `ρ = (d_s, σ)` is a V-spec, `σ = (s, ℓ)` a span, and `⟦σ⟧ = {t ∈ T : s ≤ t < s ⊕ ℓ}`. The set is finite (subset of the finite `dom(Σ.M(d_s))`, S8-fin) and totally ordered (subset of the totally ordered carrier `T`, T1), hence has a unique ascending enumeration `v₁ < … < v_k`.

---

## Definition — ResolutionExpansion

```
resolve(R, Σ) = expand(resolve(R)),  where
expand(⟨(aⱼ, nⱼ)⟩ⱼ) = ⟨a₁, a₁+1, …, a₁+(n₁−1), …, aₖ, …, aₖ+(nₖ−1)⟩
```

Where `resolve(R)` is ASN-0058's run-pair resolution `⟨(a₁, n₁), …, (aₖ, nₖ)⟩` and a content-reference sequence resolves by concatenation, `resolve(R) = resolve(ρ₁) ⌢ … ⌢ resolve(ρ_q)`. Write `resolve(R, Σ) = ⟨c₀, c₁, …, c_{W−1}⟩`, with `W = |resolve(R,Σ)|` the total count of resolved addresses (the sum of the run widths `nⱼ`).

---

## Definition — ContentResidence (COPY precondition)

```
(A ρ ∈ R, v ∈ act(ρ, Σ) : subspace(v) = s_C)
```

Every active position of every V-spec in `R` lies in the text subspace.

---

## Definition — WpDiscoverability

```
wp(COPY, "a discoverable from d") = (E j : coverage(Σ.L(a).eⱼ) ∩ {c₀, …, c_{W−1}} ≠ ∅)
```

Obtained by pulling the post-state criterion back through the operation via `Σ'.L = Σ.L` (CP7a) and `ran(Σ'.M(d)) = ran(Σ.M(d)) ∪ {c₀, …, c_{W−1}}`.

---

## CP0 — ResolutionIntegrity (CLAIM, lemma)

`resolve(R, Σ)` reads each active source position through its arrangement, in spec-set order, yielding `⟨c₀,…,c_{W−1}⟩` with:

**(a)** Every resolved address already exists:
```
cᵢ ∈ dom(Σ.C)  for  0 ≤ i < W
```
Each `cᵢ` — run-leading or run-interior alike — is `Σ.M(d_s)(v)` for some active position `v ∈ act(ρ, Σ) ⊆ dom(Σ.M(d_s))` with `subspace(v) = s_C` (content-residence); referential integrity S3★ gives `Σ.M(d_s)(v) ∈ dom(Σ.C)`.

**(b)** Resolution is a pure read:
`resolve` is a function of `Σ`; it modifies no component — not `Σ.C`, not any `Σ.M(d)`, not `Σ.L`, not `Σ.R`.

**(c)** Non-contiguity survives resolution:
ASN-0058's C1a (RestrictionDecomposition) supplies the unique maximal-run decomposition of any restriction `M(d_s)|⟦σ⟧` whose domain lies in a single subspace (precondition met by content-residence, `act(ρ, Σ) ⊆ V_{s_C}(d_s)`). When a single V-span covers content the source itself assembled from several disjoint I-regions, the decomposition returns several run-pairs in V-start order (C1b, ResolutionSequenceOrder), so the expanded sequence records as many distinct origins as the source content had homes.

---

## CP1 — TransclusionFrame (FRAME, ensures)

```
dom(Σ'.C) = dom(Σ.C) ∧ (A a : a ∈ dom(Σ.C) : Σ'.C(a) = Σ.C(a))
```

COPY allocates no content; the placed material refers to existing I-addresses. The boundary distinguishing transclusion from replication.

---

## CP2 — Placement (POST, ensures)

```
(A i : 0 ≤ i < W : Σ'.M(d)(p + i) = cᵢ)
```

`W` fresh destination V-positions bind the resolved (pre-existing) I-addresses; the placed material shares the source's content identity.

---

## CP3 — PriorArrangementPreservation (POST, ensures)

Three sub-claims:

**(CP3a)** Trailing text content shifted forward by `W` with bindings intact:
```
(A v : v ∈ V_{s_C}(d) ∧ v ≥ p : Σ'.M(d)(v + W) = Σ.M(d)(v))
```

**(CP3b)** Left content unchanged:
```
(A v : v ∈ V_{s_C}(d) ∧ v < p : Σ'.M(d)(v) = Σ.M(d)(v))
```

**(CP3c)** Text-subspace domain closed to left ∪ placement ∪ shifted, with pre-shift positions vacated:
```
{v ∈ dom(Σ'.M(d)) : subspace(v) = s_C} =
  {v ∈ V_{s_C}(d) : v < p} ∪ {p + i : 0 ≤ i < W} ∪ {v + W : v ∈ V_{s_C}(d) ∧ v ≥ p}
```

So S2 functionality is dischargeable from the postconditions; order-preserving, injective, non-destructive.

---

## CP4 — MultiplicityIncrease (LEMMA, lemma)

Total references into the placed set increase by exactly `W`; each placed `cᵢ`'s own reference count increases by its occurrence count in `resolve(R, Σ)` (≥ 1); distinct V-positions binding one address are permanently independent occurrences (S5, M14).

Formally: COPY adds `W` new `(document, V-position)` references (one per placement, CP2), so the total number of references into the placed set `{c₀, …, c_{W−1}}` increases by exactly `W`. For a fixed placed address `cᵢ`, its reference count increases by the number of times `cᵢ` occurs in `resolve(R, Σ)` — at least one, more only when a single source address is resolved at several positions.

Two distinct V-positions `v, v'` with `Σ'.M(d)(v) = Σ'.M(d)(v') = cᵢ` cannot be merged or identified — they are permanently independent occurrences of one shared identity (ASN-0058, M14 IndependentOccurrences, M14a).

---

## CP5 — OriginInvariance (LEMMA, lemma)

`origin(cᵢ)` is unchanged by COPY and equals the source document that allocated `cᵢ`, never `d`; attribution and ownership remain the source's.

Formally: for every placed address `cᵢ`, CP1 keeps `cᵢ` in the store, and S7(d) makes `origin` constant while it is stored, so `origin(cᵢ)` is invariant across the transition and equals the document that allocated `cᵢ` — a source, never `d` (unless `d` was itself that allocator).

---

## CP6 — SourceIsolation (FRAME, ensures)

```
(A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))
```

And the cross-subspace frame, closing `d`'s non-`s_C` domain to its pre-state value:

```
{v ∈ dom(Σ'.M(d)) : subspace(v) ≠ s_C} = {v ∈ dom(Σ.M(d)) : subspace(v) ≠ s_C}
  ∧ (A v : v ∈ dom(Σ.M(d)) ∧ subspace(v) ≠ s_C : Σ'.M(d)(v) = Σ.M(d)(v))
```

Every source and every other document is unmodified; the source's connectedness nonetheless grows (shared identity + provenance).

---

## CP7 — Links (POST, ensures)

**(CP7a)**
```
Σ'.L = Σ.L
```

**(CP7b) LinkSurvivalUnderReuse:** Any link whose endset coverage meets `{c₀,…,c_{W−1}}` becomes discoverable from `d` in `Σ'`:

Let `a` be a link with `coverage(Σ.L(a).eⱼ) ∩ {c₀, …, c_{W−1}} ≠ ∅` for some endset `j`. After COPY the placed addresses are in `ran(Σ'.M(d))` (CP2), so `coverage(Σ.L(a).eⱼ) ∩ ran(Σ'.M(d)) ≠ ∅`. The discoverability characterisation at the post-state:
```
discoverable_from(a, d, Σ') ⟺ (E i : coverage(Σ'.L(a).eᵢ) ∩ ran(Σ'.M(d)) ≠ ∅)
```
with `Σ'.L = Σ.L` by CP7a (coverage unchanged) yields `a` discoverable from `d`.

Links to the destination's prior content survive untouched, because that content's I-addresses are unchanged by the displacement (CP3).

---

## CP8 — ProvenanceRecording (POST, ensures)

```
(A i : 0 ≤ i < W : (cᵢ, d) ∈ Σ'.R)
```

J1★ demands the membership in `Σ'.R`, satisfied by:
- A fresh K.ρ step for range-new addresses not already in `Σ.R` (J1'★-admissible);
- Permanence P2 for range-new addresses already in `Σ.R` (re-COPY of deleted content, K.ρ optional);
- P4★ + P2 for addresses already in `d`'s current content-subspace range (not range-new; P4★ licensed at composite boundary).

---

## CP9 — SelfTransclusionAdmissibility (LEMMA, lemma)

When `d_s = d`, resolution reads the pre-state arrangement `Σ.M(d)`, so the addresses `cᵢ` are fixed before any displacement; the effect then adds new V-positions, in the same document, referring to the same I-addresses. The result is a document with two (or more) V-positions mapping to one address — admitted by S5 and permanently independent by M14. No content is duplicated; the arrangement simply references the same identity twice.

---

## CP10 — ImmutabilityPreservation (LEMMA, lemma)

S0 (ContentImmutability) is preserved across COPY (corollary of CP1): because `Σ.C` is untouched (CP1), every previously stored address keeps its value. In particular the reused `cᵢ` carry into the destination the same bytes they hold at the source, because they are the same bytes.

---

## CP11 — OriginMultisetPreservation (LEMMA, lemma)

```
{ origin(cᵢ) : 0 ≤ i < W }
```

is preserved verbatim into the destination's arrangement: each fragment retains its distinct home, and each home remains queryable from the destination address that binds it.

Within a block, all addresses share an origin (`origin(cᵢ + 1) = origin(cᵢ)` for contiguous addresses, ASN-0058 M16a); across a block boundary where the origins differ, the blocks cannot be merged (ASN-0058, M16 CrossOriginMergeImpossibility).

Contrast with replication: REPLICATE would allocate `W` fresh contiguous addresses under the destination with `origin = d`, collapsing the multiset to `{d, d, …, d}` and erasing the seams between source regions.
