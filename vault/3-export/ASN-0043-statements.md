# ASN-0043 Formal Statements

*Source: ASN-0043-link-ontology.md (revised 2026-03-16) — Extracted: 2026-03-20*

## Definition — LinkStore

`Σ.L : T ⇀ Link` is the *link store*, a partial function mapping tumbler addresses to link values. The domain `dom(Σ.L)` is the set of addresses at which links have been created.

## Definition — Endset

An *endset* is a finite set of well-formed spans:

`Endset = 𝒫_fin(Span)`

where `Span` is the set of well-formed span pairs `(s, ℓ)` satisfying T12 (SpanWellDefined): `ℓ > 0` and the action point `k` of `ℓ` satisfies `k ≤ #s`. The empty set `∅` is a valid endset.

## Definition — Link

A *link value* is a triple of endsets:

`Link = (from : Endset, to : Endset, type : Endset)`

The three components are called the *from-endset*, the *to-endset*, and the *type-endset* respectively.

## Definition — Coverage

For an endset `e`, define the *coverage* as the union of the sets denoted by its spans:

`coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ})`

## Definition — LinkHome

For a link at address `a ∈ dom(Σ.L)`, its *home document* is:

`home(a) = origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

## Definition — UnitDepthDisplacement

For any tumbler `x` with `#x ≥ 1`, define the *unit-depth displacement* `ℓ_x` with `#ℓ_x = #x`, zero at positions `1` through `#x - 1`, and value 1 at position `#x`. The action point of `ℓ_x` is `k = #x`.

---

## L0 — SubspacePartition (INV, predicate)

Let `s_C` and `s_L` be the subspace identifiers for content and links respectively, with `s_C ≠ s_L`.

```
(A a ∈ dom(Σ.L) :: fields(a).E₁ = s_L)

(A a ∈ dom(Σ.C) :: fields(a).E₁ = s_C)
```

Derived:

```
dom(Σ.L) ∩ dom(Σ.C) = ∅
```

## L1 — LinkElementLevel (INV, predicate)

```
(A a ∈ dom(Σ.L) :: zeros(a) = 3)
```

## L1a — LinkScopedAllocation (INV, predicate)

```
(A a ∈ dom(Σ.L) :: origin(a) identifies the allocating document)
```

## L2 — OwnershipEndsetIndependence (LEMMA, lemma)

```
(A a ∈ dom(Σ.L) :: home(a) depends only on a)
```

Derived from L1, L1a, and T4 (FieldParsing): `home(a) = origin(a)`, computed from the field structure of `a` alone, with `Σ.L(a)` not consulted.

## L3 — TripleEndsetStructure (INV, predicate)

```
(A a ∈ dom(Σ.L) :: Σ.L(a) = (F, G, Θ) where F, G, Θ ∈ Endset)
```

## L4 — EndsetGenerality (LEMMA, lemma)

Type-level statement (from L3 and T12):

```
(A a ∈ dom(Σ.L), e ∈ {from, to, type}, (s, ℓ) ∈ Σ.L(a).e :: s ∈ T ∧ (s, ℓ) satisfies T12)
```

Sub-properties (absences of additional constraints):

(a) *Cross-document endsets.* A single endset may contain spans whose start addresses fall under different document-level prefixes.

(b) *Intra-document links.* Nothing prevents a link's endsets from referencing content within the link's own home document.

(c) *Cross-subspace endsets.* Endset spans may reference addresses in the link subspace — that is, addresses of other links.

## L5 — EndsetSetSemantics (INV, predicate)

```
(A a ∈ dom(Σ.L), e :: Σ.L(a).e is characterized by {(s, ℓ) : (s, ℓ) ∈ Σ.L(a).e})
```

Only span membership matters; ordering carries no semantic meaning.

## L6 — SlotDistinction (INV, predicate)

```
(A F, G, Θ :: F ≠ G ⟹ (F, G, Θ) ≠ (G, F, Θ))
```

## L7 — DirectionalFlexibility (META)

The invariants L0–L14 impose no constraint on which of the from/to slots carries directional significance; any directional interpretation is determined by the link type, outside the link structure.

## L8 — TypeByAddress (INV, predicate)

```
same_type(a₁, a₂) ⟺ Σ.L(a₁).type = Σ.L(a₂).type
```

where endset equality is set equality of spans.

## L9 — TypeGhostPermission (LEMMA, lemma)

```
(A Σ : Σ satisfies L0–L14 ∧ S0–S3 :
  (E Σ' extending Σ, a ∈ dom(Σ'.L), (s, ℓ) ∈ Σ'.L(a).type ::
    coverage({(s, ℓ)}) ⊄ dom(Σ'.C) ∪ dom(Σ'.L)))
```

## PrefixSpanCoverage — PrefixSpanCoverage (LEMMA, lemma)

Precondition: `x ∈ T`, `#x ≥ 1`. Let `ℓ_x` be the unit-depth displacement at `x` (see Definition — UnitDepthDisplacement). Then `(x, ℓ_x)` is well-formed by T12: `ℓ_x > 0` and `k = #x ≤ #x`. By TumblerAdd: `x ⊕ ℓ_x = [x₁, ..., x_{#x-1}, x_{#x} + 1]`.

```
coverage({(x, ℓ_x)}) = {t ∈ T : x ≼ t}
```

## L10 — TypeHierarchyByContainment (LEMMA, lemma)

For type addresses `p, c ∈ T` where `p ≼ c`, define:

```
subtypes(p) = {c ∈ T : p ≼ c}
```

By T5 (ContiguousSubtrees), `subtypes(p)` is a contiguous interval under T1. By PrefixSpanCoverage:

```
coverage({(p, ℓ_p)}) = {t ∈ T : p ≼ t} = subtypes(p)
```

## L11a — LinkUniqueness (LEMMA, lemma)

Link addresses are produced by forward allocation (T9) within the link subspace. By GlobalUniqueness (ASN-0034), no two allocation events anywhere in the system, at any time, produce the same address. Therefore every link has a globally unique, permanent identity, and the question "are these the same link?" reduces to tumbler comparison (T2, IntrinsicComparison).

## L11b — NonInjectivity (LEMMA, lemma)

```
(A Σ satisfying L0–L14, a ∈ dom(Σ.L) ::
  (E Σ' extending Σ, a' ∈ dom(Σ'.L) ::
    a' ≠ a ∧ Σ'.L(a') = Σ.L(a) ∧ Σ' satisfies L0–L14))
```

The invariants *permit* non-injectivity but do not *require* it.

## L12 — LinkImmutability (INV, predicate)

```
(A Σ, Σ' : Σ → Σ' :
  (A a : a ∈ dom(Σ.L) : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)))
```

for every state transition `Σ → Σ'`.

## L12a — LinkStoreMonotonicity (LEMMA, lemma)

```
dom(Σ.L) ⊆ dom(Σ'.L)
```

for every state transition `Σ → Σ'`. Direct corollary of L12.

## L13 — ReflexiveAddressing (LEMMA, lemma)

For any `b ∈ dom(Σ.L)`, `b` is an element-level tumbler by L1, so `#b ≥ 1` and PrefixSpanCoverage applies. The unit-depth span `(b, ℓ_b)` is well-formed by T12, and:

```
coverage({(b, ℓ_b)}) = {t ∈ T : b ≼ t}
```

An endset *references* an entity at address `a` when `a ∈ coverage(e)`. The canonical span `(b, ℓ_b)` is the canonical reference to the entity at `b`.

## L14 — DualPrimitive (INV, predicate)

The set of addresses at which entity values reside is `dom(Σ.C) ∪ dom(Σ.L)`. No state component maps an address outside this union to an entity value. Arrangements `Σ.M(d)` are mappings *between* addresses, not stored entities.

```
dom(Σ.C) ∩ dom(Σ.L) = ∅
```
