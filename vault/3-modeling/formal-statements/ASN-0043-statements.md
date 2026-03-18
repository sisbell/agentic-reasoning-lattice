# ASN-0043 Formal Statements

*Source: ASN-0043-link-ontology.md (revised 2026-03-16) — Index: 2026-03-17 — Extracted: 2026-03-17*

## Definition — LinkStore

`Σ.L : T ⇀ Link` is the link store, a partial function mapping tumbler addresses to link values. The domain `dom(Σ.L)` is the set of addresses at which links have been created.

## Definition — Endset

An *endset* is a finite set of well-formed spans:

`Endset = 𝒫_fin(Span)`

where `Span` is the set of well-formed span pairs `(s, ℓ)` satisfying T12 (SpanWellDefined): `ℓ > 0` and the action point `k` of `ℓ` satisfies `k ≤ #s`. The empty set `∅` is a valid endset.

## Definition — Link

A *link value* is a triple of endsets:

`Link = (from : Endset, to : Endset, type : Endset)`

The three components are called the *from-endset*, the *to-endset*, and the *type-endset* respectively.

## Definition — Home

For a link at address `a ∈ dom(Σ.L)`, its *home document* is:

`home(a) = origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

## Definition — Coverage

For an endset `e`, define the *coverage* as the union of the sets denoted by its spans:

`coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ})`

---

## L0 — SubspacePartition (INV, predicate(State))

Every link address has subspace identifier `s_L`, and every content address has subspace identifier `s_C`:

`(A a ∈ dom(Σ.L) :: fields(a).E₁ = s_L)`

`(A a ∈ dom(Σ.C) :: fields(a).E₁ = s_C)`

with `s_C ≠ s_L`, yielding:

`dom(Σ.L) ∩ dom(Σ.C) = ∅`

## L1 — LinkElementLevel (INV, predicate(State))

Every link address is an element-level tumbler:

`(A a ∈ dom(Σ.L) :: zeros(a) = 3)`

## L1a — LinkScopedAllocation (INV, predicate(State))

Every link address is allocated under the tumbler prefix of the document whose owner created it:

`(A a ∈ dom(Σ.L) :: origin(a) identifies the allocating document)`

## L2 — OwnershipEndsetIndependence (LEMMA, lemma)

The home document of a link is determined entirely by the link's address and is independent of the link's endsets:

`(A a ∈ dom(Σ.L) :: home(a) depends only on a)`

*Derived from L1, L1a, T4 (FieldParsing).*

## L3 — TripleEndsetStructure (INV, datatype Link)

Every link in the link store has exactly three endsets:

`(A a ∈ dom(Σ.L) :: Σ.L(a) = (F, G, Θ) where F, G, Θ ∈ Endset)`

*Encoded in the type definition of Link.*

## L4 — EndsetGenerality (INV, predicate(State))

The spans within an endset may reference any addresses in the tumbler space. There is no constraint confining spans to a single document, to content addresses only, or to addresses at which content currently exists:

`(A a ∈ dom(Σ.L), e ∈ {from, to, type}, (s, ℓ) ∈ Σ.L(a).e :: s ∈ T ∧ (s, ℓ) satisfies T12)`

Sub-properties:

(a) *Cross-document endsets.* A single endset may contain spans whose start addresses fall under different document-level prefixes.

(b) *Intra-document links.* Nothing prevents a link's endsets from referencing content within the link's own home document.

(c) *Cross-subspace endsets.* Endset spans may reference addresses in the link subspace — that is, addresses of other links.

## L5 — EndsetSetSemantics (INV, type Endset)

An endset is an *unordered* set; the ordering of spans within an endset carries no semantic meaning. Only membership matters:

`(A a ∈ dom(Σ.L), e :: Σ.L(a).e is characterized by {(s, ℓ) : (s, ℓ) ∈ Σ.L(a).e})`

*Encoded in the set type.*

## L6 — SlotDistinction (INV, predicate(Link))

The three endsets occupy structurally distinguished positions within the link. A link `(F, G, Θ)` is a different value from `(G, F, Θ)` when `F ≠ G`:

`(A F, G, Θ :: F ≠ G ⟹ (F, G, Θ) ≠ (G, F, Θ))`

*Follows from datatype equality.*

## L7 — DirectionalFlexibility (META, —)

The invariants L0–L14 impose no constraint on which of the from/to slots carries directional significance; any directional interpretation is determined by the link type, outside the link structure.

*Meta-property of L0–L14; not directly encodable as a Dafny predicate.*

## L8 — TypeByAddress (INV, predicate(State))

Type matching is by *address identity*, not by content at the address. Whether two links share the same type is determined by whether their type endsets reference the same addresses, not by what is stored at those addresses:

`same_type(a₁, a₂) ⟺ Σ.L(a₁).type = Σ.L(a₂).type`

where endset equality is set equality of spans.

## L9 — TypeGhostPermission (LEMMA, lemma)

Ghost types are permitted: for any conforming state `Σ` satisfying L0–L14 and S0–S3, there exists a conforming state `Σ'` extending `Σ` with a link whose type endset references an address outside `dom(Σ'.C) ∪ dom(Σ'.L)`:

`(A Σ : Σ satisfies L0–L14 ∧ S0–S3 : (E Σ' extending Σ, a ∈ dom(Σ'.L), (s, ℓ) ∈ Σ'.L(a).type :: coverage({(s, ℓ)}) ⊄ dom(Σ'.C) ∪ dom(Σ'.L)))`

*Witness construction:* Take any conforming `Σ`. Let `d` be a document with an allocator for subspace `s_L`. Choose a fresh ghost address `g ∈ T` with `g ∉ dom(Σ.C) ∪ dom(Σ.L)` (exists by T0(b)). Allocate a new link address `a` via forward allocation (T9) within `d`'s link subspace. Define `Σ'` as `Σ` extended with `Σ'.L(a) = (∅, ∅, {(g, ℓ_g)})` where `ℓ_g` is the unit-width displacement at depth `#g`, and `Σ'.C = Σ.C`, `Σ'.M = Σ.M`.

## L10 — TypeHierarchyByContainment (LEMMA, lemma)

For type addresses `p, c ∈ T` where `p ≼ c` (p is a prefix of c), define `subtypes(p) = {c ∈ T : p ≼ c}`. By T5 (ContiguousSubtrees), `subtypes(p)` is a contiguous interval under T1.

Define `ℓ_p` with `#ℓ_p = #p`, zero at positions `1` through `#p - 1`, and value 1 at position `#p`. The action point is `k = #p`. The span `(p, ℓ_p)` is well-formed by T12: `ℓ_p > 0` and `k ≤ #p`. By TumblerAdd, `p ⊕ ℓ_p = [p₁, ..., p_{#p-1}, p_{#p} + 1]`.

`(A c : p ≼ c : c ∈ coverage({(p, ℓ_p)}))`

A single span query rooted at `p` matches every subtype of `p`.

*Derived from T1, T5.*

## L11 — IdentityByAddress (INV, predicate(State))

Link identity is address identity. For link addresses `a₁, a₂ ∈ dom(Σ.L)` produced by distinct allocation events, `a₁ ≠ a₂` regardless of whether `Σ.L(a₁) = Σ.L(a₂)`:

`(A a₁, a₂ ∈ dom(Σ.L) :: a₁ ≠ a₂ ⟹ a₁ and a₂ designate separate link entities, even when Σ.L(a₁) = Σ.L(a₂))`

The link store is not necessarily injective.

## L12 — LinkImmutability (INV, predicate(State, State))

Once created, a link's address persists and its value is permanently fixed:

`(A Σ, Σ' : Σ → Σ' : (A a : a ∈ dom(Σ.L) : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)))`

for every state transition `Σ → Σ'`.

## L12a — LinkStoreMonotonicity (LEMMA, lemma)

The domain of the link store is monotonically non-decreasing:

`[dom(Σ.L) ⊆ dom(Σ'.L)]`

for every state transition `Σ → Σ'`.

*Derived from L12.*

## L13 — ReflexiveAddressing (LEMMA, lemma)

Link addresses are valid targets for endset spans. For any link at address `b ∈ dom(Σ.L)`, define the displacement `ℓ_b` with `#ℓ_b = #b`, zero at positions `1` through `#b - 1`, and value 1 at position `#b`. The action point of `ℓ_b` is `k = #b`. Since `b` is an element-level tumbler, `k ≤ #b` holds and the span `(b, ℓ_b)` is well-formed by T12.

`coverage({(b, ℓ_b)}) = {t ∈ T : b ≼ t}`

Proof of both directions:

*Inclusion* (`{t : b ≼ t} ⊆ coverage`): let `c` be an extension of `b`, so `b ≼ c`. By T1(ii), `c ≥ b`. Since `c` agrees with `b` at all positions `1` through `#b`, `c_{#b} = b_{#b} < b_{#b} + 1 = (b ⊕ ℓ_b)_{#b}`. By T1(i), `c < b ⊕ ℓ_b`.

*Exclusion* (`coverage ⊆ {t : b ≼ t}`): by case analysis on depth of `t ∈ [b, b ⊕ ℓ_b)`:

- *Same depth* (`#t = #b`): since `t ≠ b`, some `k ≤ #b` has `t_k ≠ b_k`; as `t > b`, `t_k > b_k`; if `k < #b` then `t > b ⊕ ℓ_b`; if `k = #b` then `t_{#b} ≥ b_{#b} + 1`, giving `t ≥ b ⊕ ℓ_b`. Only `b` survives.
- *Greater depth* (`#t > #b`): if `t` does not extend `b`, there exists `k ≤ #b` with `t_k > b_k = (b ⊕ ℓ_b)_k`, giving `t > b ⊕ ℓ_b`.
- *Shorter depth* (`#t < #b`): if `t` agrees with `b` at all positions `1..#t`, then `b` extends `t`, so `t < b` — contradiction. Otherwise `t > b ⊕ ℓ_b`.

*Derived from L1, T1, T12.*

## L14 — DualPrimitive (INV, predicate(State))

The set of addresses at which entity values reside is `dom(Σ.C) ∪ dom(Σ.L)`. No state component maps an address outside this union to an entity value. Arrangements `Σ.M(d)` are mappings *between* addresses. The two domains are disjoint:

`dom(Σ.C) ∩ dom(Σ.L) = ∅`
