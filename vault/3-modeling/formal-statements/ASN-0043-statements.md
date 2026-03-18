# ASN-0043 Formal Statements

*Source: ASN-0043-link-ontology.md (revised 2026-03-16) — Index: 2026-03-18 — Extracted: 2026-03-18*

## Definition — LinkStore

`Σ.L : T ⇀ Link` is the *link store*, a partial function mapping tumbler addresses to link values. The domain `dom(Σ.L)` is the set of addresses at which links have been created.

The full system state is: `Σ = (Σ.C, Σ.M, Σ.L)`

## Definition — Endset

`Endset = 𝒫_fin(Span)`

where `Span` is the set of well-formed span pairs `(s, ℓ)` satisfying T12 (SpanWellDefined): `ℓ > 0` and the action point `k` of `ℓ` satisfies `k ≤ #s`. The empty set `∅` is a valid endset.

## Definition — Link

`Link = (from : Endset, to : Endset, type : Endset)`

The three components are called the *from-endset*, the *to-endset*, and the *type-endset* respectively.

## Definition — LinkHome

For a link at address `a ∈ dom(Σ.L)`, its *home document* is:

`home(a) = origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

## Definition — Coverage

For an endset `e`, define the *coverage* as the union of the sets denoted by its spans:

`coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ})`

## Definition — SameType

`same_type(a₁, a₂) ⟺ Σ.L(a₁).type = Σ.L(a₂).type`

where endset equality is set equality of spans.

---

## L0 — SubspacePartition (INV, predicate(State))

`(A a ∈ dom(Σ.L) :: fields(a).E₁ = s_L)`

`(A a ∈ dom(Σ.C) :: fields(a).E₁ = s_C)`

where `s_C ≠ s_L`. By T7 (SubspaceDisjoint):

`dom(Σ.L) ∩ dom(Σ.C) = ∅`

## L1 — LinkElementLevel (INV, predicate(State))

`(A a ∈ dom(Σ.L) :: zeros(a) = 3)`

## L1a — LinkScopedAllocation (INV, predicate(State))

`(A a ∈ dom(Σ.L) :: origin(a) identifies the allocating document)`

That is, the document-level prefix of `a` is the prefix of the document `d` under which `a` was allocated, and `origin(a) = d`.

## L2 — OwnershipEndsetIndependence (LEMMA, lemma)

Derived from L1, L1a, T4.

`(A a ∈ dom(Σ.L) :: home(a) depends only on a)`

`home(a)` is computed from the field structure of `a` alone; the endsets `(F, G, Θ)` are not consulted.

## L3 — TripleEndsetStructure (INV, datatype Link)

Encoded in the type definition.

`(A a ∈ dom(Σ.L) :: Σ.L(a) = (F, G, Θ) where F, G, Θ ∈ Endset)`

## L4 — EndsetGenerality (LEMMA, lemma)

Derived from L3, T12.

`(A a ∈ dom(Σ.L), e ∈ {from, to, type}, (s, ℓ) ∈ Σ.L(a).e :: s ∈ T ∧ (s, ℓ) satisfies T12)`

The substantive content is the absence of additional constraints beyond T12. Specifically:

(a) *Cross-document endsets.* A single endset may contain spans whose start addresses fall under different document-level prefixes. No constraint confines spans to a single document.

(b) *Intra-document links.* Nothing prevents a link's endsets from referencing content within the link's own home document.

(c) *Cross-subspace endsets.* Endset spans may reference addresses in the link subspace — addresses of other links.

## L5 — EndsetSetSemantics (INV, type Endset)

Encoded in set type.

`(A a ∈ dom(Σ.L), e :: Σ.L(a).e is characterized by {(s, ℓ) : (s, ℓ) ∈ Σ.L(a).e})`

An endset is an *unordered* set; only span membership matters; ordering of spans carries no semantic meaning.

## L6 — SlotDistinction (INV, predicate(Link))

Follows from datatype equality.

`(A F, G, Θ :: F ≠ G ⟹ (F, G, Θ) ≠ (G, F, Θ))`

## L7 — DirectionalFlexibility (META)

Meta-property of L0–L14. No formal statement to encode: L0–L14 impose no constraint on which of the from/to slots carries directional significance; any directional interpretation is determined by the link type, outside the link structure.

## L8 — TypeByAddress (INV, predicate(State))

Type matching is by *address identity*, not by content at the address:

`same_type(a₁, a₂) ⟺ Σ.L(a₁).type = Σ.L(a₂).type`

where endset equality is set equality of spans. The search mechanism does not dereference the type address; it matches only the address itself.

## L9 — TypeGhostPermission (LEMMA, lemma)

Existence proof; witness construction.

`(A Σ : Σ satisfies L0–L14 ∧ S0–S3 : (E Σ' extending Σ, a ∈ dom(Σ'.L), (s, ℓ) ∈ Σ'.L(a).type :: coverage({(s, ℓ)}) ⊄ dom(Σ'.C) ∪ dom(Σ'.L)))`

*Witness.* Take any conforming `Σ`. Let `d` be a document with an allocator for subspace `s_L`. Choose a fresh ghost address `g ∈ T` with `fields(g).E₁ = s_C` and `g ∉ dom(Σ.C)`. Allocate a new link address `a` via forward allocation (T9) within `d`'s link subspace. Define `Σ'` as `Σ` extended with `Σ'.L(a) = (∅, ∅, {(g, ℓ_g)})` where `ℓ_g` is the unit-width displacement at depth `#g`, and `Σ'.C = Σ.C`, `Σ'.M = Σ.M`.

## PrefixSpanCoverage — PrefixSpanCoverage (LEMMA, lemma)

Derived from T1, T5, T12.

For any tumbler `x` with `#x ≥ 1`, define the *unit-depth displacement* `ℓ_x` with:
- `#ℓ_x = #x`
- zero at positions `1` through `#x - 1`
- value 1 at position `#x`

The action point of `ℓ_x` is `k = #x`. The span `(x, ℓ_x)` is well-formed by T12: `ℓ_x > 0` and `k ≤ #x`. By TumblerAdd: `x ⊕ ℓ_x = [x₁, ..., x_{#x-1}, x_{#x} + 1]`. Then:

`coverage({(x, ℓ_x)}) = {t ∈ T : x ≼ t}`

*Inclusion* (`{t : x ≼ t} ⊆ coverage`): let `c` extend `x`, so `x ≼ c`. By T1(ii), `c ≥ x`. Since `c` agrees with `x` at all positions `1` through `#x`, we have `c_{#x} = x_{#x} < x_{#x} + 1 = (x ⊕ ℓ_x)_{#x}`, giving `c < x ⊕ ℓ_x` by T1(i). Therefore `c ∈ [x, x ⊕ ℓ_x)`.

*Exclusion* (`coverage ⊆ {t : x ≼ t}`): every `t ∈ [x, x ⊕ ℓ_x)` with `t ≠ x` must extend `x`, by case analysis on depth:
- *Same depth* (`#t = #x`): since `t ≠ x`, some `j ≤ #x` has `t_j ≠ x_j`. As `t > x`, `t_j > x_j`. If `j < #x` then `t_j > (x ⊕ ℓ_x)_j`, giving `t > x ⊕ ℓ_x`. If `j = #x` then `t_{#x} ≥ x_{#x} + 1 = (x ⊕ ℓ_x)_{#x}`, giving `t ≥ x ⊕ ℓ_x`. Only `x` itself survives, and `x ≼ x` holds trivially.
- *Greater depth* (`#t > #x`): if `t` does not extend `x`, some `j ≤ #x` has `t_j > x_j`. If `j < #x`: `t > x ⊕ ℓ_x`. If `j = #x`: `t_{#x} ≥ x_{#x} + 1`; when strict `t > x ⊕ ℓ_x`; when equal `x ⊕ ℓ_x` is a proper prefix of `t`, giving `x ⊕ ℓ_x < t` by T1(ii).
- *Shorter depth* (`#t < #x`): if `t` agrees with `x` at all `1..#t`, then `x` extends `t` so `t < x` — contradiction. If `t` diverges from `x` at some `j ≤ #t`, then `t_j > x_j = (x ⊕ ℓ_x)_j`, giving `t > x ⊕ ℓ_x`.

## L10 — TypeHierarchyByContainment (LEMMA, lemma)

Derived from PrefixSpanCoverage, T5.

For type addresses `p, c ∈ T` where `p ≼ c`, define:

`subtypes(p) = {c ∈ T : p ≼ c}`

By T5 (ContiguousSubtrees), `subtypes(p)` is a contiguous interval under T1. By PrefixSpanCoverage:

`coverage({(p, ℓ_p)}) = {t ∈ T : p ≼ t} = subtypes(p)`

A single span query rooted at `p` matches all and only subtypes of `p`.

## L11a — LinkUniqueness (LEMMA, lemma)

Derived from T9, GlobalUniqueness.

Link addresses are produced by forward allocation (T9) within the link subspace. By GlobalUniqueness (ASN-0034), no two allocation events anywhere in the system, at any time, produce the same address. Therefore every link has a globally unique, permanent identity, and "are these the same link?" reduces to tumbler comparison (T2, IntrinsicComparison).

## L11b — NonInjectivity (LEMMA, lemma)

Existence proof; witness construction.

`(A Σ satisfying L0–L14, a ∈ dom(Σ.L) :: (E Σ' extending Σ, a' ∈ dom(Σ'.L) :: a' ≠ a ∧ Σ'.L(a') = Σ.L(a) ∧ Σ' satisfies L0–L14))`

*Witness.* For any `a ∈ dom(Σ.L)` with `Σ.L(a) = (F, G, Θ)`: allocate `a'` by forward allocation within the same document's link subspace; set `Σ'.L(a') = (F, G, Θ)` with `Σ'.C = Σ.C` and `Σ'.M = Σ.M`. The invariants do not require injectivity.

## L12 — LinkImmutability (INV, predicate(State, State))

Transition invariant.

`(A Σ, Σ' : Σ → Σ' : (A a : a ∈ dom(Σ.L) : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)))`

for every state transition `Σ → Σ'`.

## L12a — LinkStoreMonotonicity (LEMMA, lemma)

Derived from L12. Transition invariant.

`dom(Σ.L) ⊆ dom(Σ'.L)`

for every state transition `Σ → Σ'`.

## L13 — ReflexiveAddressing (LEMMA, lemma)

Derived from L1, T12, PrefixSpanCoverage.

For any link at address `b ∈ dom(Σ.L)`, `b` is an element-level tumbler by L1, so `#b ≥ 1` and PrefixSpanCoverage applies. The unit-depth span `(b, ℓ_b)` is well-formed by T12, and:

`coverage({(b, ℓ_b)}) = {t ∈ T : b ≼ t}`

An endset *references* an entity at address `a` when `a ∈ coverage(e)`. The span `(b, ℓ_b)` is the canonical span for referencing the entity at `b`: it covers all and only extensions of `b`.

## L14 — DualPrimitive (INV, predicate(State))

The set of addresses at which entity values reside is `dom(Σ.C) ∪ dom(Σ.L)`. No state component maps an address outside this union to an entity value. Arrangements `Σ.M(d)` are mappings *between* addresses; V-positions are not entities in their own right.

`dom(Σ.C) ∩ dom(Σ.L) = ∅`
