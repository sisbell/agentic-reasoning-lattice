# ASN-0043 Formal Statements

*Source: ASN-0043-link-ontology.md (revised 2026-03-16) — Extracted: 2026-03-23*

## Definition — LinkStore

`Σ.L : T ⇀ Link` is the *link store*, a partial function mapping tumbler addresses to link values. The domain `dom(Σ.L)` is the set of addresses at which links have been created.

The full system state is: `Σ = (Σ.C, Σ.M, Σ.L)`

## Definition — Endset

`Endset = 𝒫_fin(Span)`

where `Span` is the set of well-formed span pairs `(s, ℓ)` satisfying T12 (SpanWellDefinedness, ASN-0034): `ℓ > 0` and the action point `k` of `ℓ` satisfies `k ≤ #s`. The empty set `∅` is a valid endset.

## Definition — Link

`Link = {(e₁, e₂, ..., eₙ) : N ≥ 2, each eᵢ ∈ Endset}`

`|L|` denotes the *arity* of a link — the number of endsets in the sequence.

## Definition — StandardTriple (Convention)

The standard link form has arity 3, with slot 1 as the *from-endset*, slot 2 as the *to-endset*, and slot 3 as the *type-endset*. Written `(F, G, Θ)`.

## Definition — Coverage

For an endset `e`:

`coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ})`

## Definition — LinkHome

For a link at address `a ∈ dom(Σ.L)`, its *home document* is:

`home(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

Precondition: `a ∈ dom(Σ.L)` implies `zeros(a) = 3` (by L1) and T4 (HierarchicalParsing, ASN-0034) constrains `a` to satisfy its format requirements, so `fields` is well-defined.

## Definition — Subtypes

For type address `p ∈ T`:

`subtypes(p) = {c ∈ T : p ≼ c}`

## Definition — SameType

For standard-triple links (`|Σ.L(a)| ≥ 3`):

`same_type(a₁, a₂) ⟺ Σ.L(a₁).type = Σ.L(a₂).type`

where endset equality is set equality of spans.

---

## L0 — SubspacePartition (INV, predicate)

Let `s_C` and `s_L` be the subspace identifiers for content and links respectively, with `s_C ≠ s_L`.

`(A a ∈ dom(Σ.L) :: fields(a).E₁ = s_L)`

`(A a ∈ dom(Σ.C) :: fields(a).E₁ = s_C)`

By T7 (SubspaceDisjointness, ASN-0034):

`dom(Σ.L) ∩ dom(Σ.C) = ∅`

## L1 — LinkElementLevel (INV, predicate)

`(A a ∈ dom(Σ.L) :: zeros(a) = 3)`

## L1a — LinkScopedAllocation (INV, predicate)

`(A a ∈ dom(Σ.L) :: (fields(a).node).0.(fields(a).user).0.(fields(a).document) identifies the allocating document)`

Precondition: L1 establishes `zeros(a) = 3`; T4 (HierarchicalParsing, ASN-0034) applies to link addresses as keys in `Σ.L`, making `fields` well-defined.

## L2 — OwnershipEndsetIndependence (LEMMA, lemma)

`(A a ∈ dom(Σ.L) :: home(a) depends only on a)`

`home(a)` uniquely identifies the creating document across the system (by T9, T10, T10a + TA5(d) + T3, ASN-0034), and this identification is structural — embedded in the address, not attached as metadata.

## L3 — NEndsetStructure (INV, predicate)

`(A a ∈ dom(Σ.L) :: |Σ.L(a)| ≥ 2 ∧ (A i : 1 ≤ i ≤ |Σ.L(a)| : Σ.L(a).eᵢ ∈ Endset))`

## L4 — EndsetGenerality (LEMMA, lemma)

Formal content (from L3 and T12):

`(A a ∈ dom(Σ.L), i : 1 ≤ i ≤ |Σ.L(a)|, (s, ℓ) ∈ Σ.L(a).eᵢ :: s ∈ T ∧ (s, ℓ) satisfies T12)`

Sub-properties (absence of additional constraints):

(a) *Cross-document endsets.* A single endset may contain spans whose start addresses fall under different document-level prefixes.

(b) *Intra-document links.* Nothing prevents a link's endsets from referencing content within the link's own home document.

(c) *Cross-subspace endsets.* Endset spans may reference addresses in the link subspace — that is, addresses of other links.

## L5 — EndsetSetSemantics (INV, predicate)

`(A a ∈ dom(Σ.L), e :: Σ.L(a).e is characterized by {(s, ℓ) : (s, ℓ) ∈ Σ.L(a).e})`

Only membership matters; insertion order is not preserved or recoverable.

## L6 — SlotDistinction (INV, predicate)

A link is a sequence — permuting endset slots produces a different link value when the permuted entries differ. For the standard triple:

`(A F, G, Θ :: F ≠ G ⟹ (F, G, Θ) ≠ (G, F, Θ))`

## L7 — DirectionalFlexibility (META)

The invariants L0–L14 impose no constraint on which of the from/to slots carries directional significance; any directional interpretation is determined by the link type, outside the link structure.

## L8 — TypeByAddress (DEF, function)

For links following the standard triple convention (`|Σ.L(a)| ≥ 3`), type matching is by *address identity*:

`same_type(a₁, a₂) ⟺ Σ.L(a₁).type = Σ.L(a₂).type`

where endset equality is set equality of spans. The search mechanism does not dereference the type address; it only matches the address.

## L9 — TypeGhostPermission (LEMMA, lemma)

For links following the standard triple convention: ghost types are permitted.

`(A Σ : Σ satisfies L0–L14 ∧ S0–S3 : (E Σ' extending Σ, a ∈ dom(Σ'.L), (s, ℓ) ∈ Σ'.L(a).type :: coverage({(s, ℓ)}) ⊄ dom(Σ'.C) ∪ dom(Σ'.L)))`

No property of L0–L14 constrains `coverage(Σ'.L(a).type) ⊆ dom(Σ'.C)`.

## PrefixSpanCoverage — PrefixSpanCoverage (LEMMA, lemma)

For any tumbler `x` with `#x ≥ 1`:

`coverage({(x, δ(1, #x))}) = {t ∈ T : x ≼ t}`

Equivalently: `x ⊕ δ(1, #x) = shift(x, 1) = [x₁, ..., x_{#x-1}, x_{#x} + 1]`

Precondition: `δ(1, #x)` is the displacement `[0, ..., 0, 1]` of length `#x`, with action point `k = #x`. The span `(x, δ(1, #x))` is well-formed by T12: `δ(1, #x) > 0` and `k ≤ #x`.

## L10 — TypeHierarchyByContainment (LEMMA, lemma)

For type addresses `p, c ∈ T` where `p ≼ c`:

`subtypes(p) = {c ∈ T : p ≼ c}`

By T5 (ContiguousSubtrees, ASN-0034), `subtypes(p)` is a contiguous interval under T1. By PrefixSpanCoverage:

`coverage({(p, δ(1, #p))}) = {t ∈ T : p ≼ t} = subtypes(p)`

A single span query rooted at `p` matches all and only subtypes of `p`.

## GlobalUniqueness — GlobalUniqueness (LEMMA, lemma)

No two allocation events anywhere in the system produce the same address.

The three foundation axioms underlying S4's derivation apply without subspace restriction: T9 (ForwardAllocation), T10 (PartitionIndependence), and T10a (AllocatorDiscipline) (all ASN-0034) carry no subspace restriction in their quantifiers. The same three cases apply to link-subspace allocations:
- same-allocator distinctness via T9
- non-nesting cross-allocator distinctness via T10
- nesting-prefix cross-allocator distinctness via T10a + TA5(d) + T3

## L11a — LinkUniqueness (LEMMA, lemma)

Link addresses are produced by forward allocation (T9, ASN-0034) within the link subspace. By GlobalUniqueness, no two allocation events anywhere in the system produce the same address. Therefore every link has a globally unique, permanent identity, and the question "are these the same link?" reduces to tumbler comparison (T2, IntrinsicComparison).

## L11b — NonInjectivity (LEMMA, lemma)

`(A Σ satisfying L0–L14, a ∈ dom(Σ.L) :: (E Σ' extending Σ, a' ∈ dom(Σ'.L) :: a' ≠ a ∧ Σ'.L(a') = Σ.L(a) ∧ Σ' satisfies L0–L14))`

The invariants *permit* non-injectivity but do not *require* it.

## L12 — LinkImmutability (INV, predicate)

`(A Σ, Σ' : Σ → Σ' : (A a : a ∈ dom(Σ.L) : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)))`

for every state transition `Σ → Σ'`.

## L12a — LinkStoreMonotonicity (LEMMA, lemma)

`dom(Σ.L) ⊆ dom(Σ'.L)`

for every state transition `Σ → Σ'`. Direct corollary of L12.

## L13 — ReflexiveAddressing (LEMMA, lemma)

Link addresses are valid targets for endset spans. For any link at address `b ∈ dom(Σ.L)`, `b` is an element-level tumbler by L1, so `#b ≥ 1` and PrefixSpanCoverage applies. The unit-depth span `(b, δ(1, #b))` is well-formed, and:

`coverage({(b, δ(1, #b))}) = {t ∈ T : b ≼ t}`

An endset *references* an entity at address `a` when `a ∈ coverage(e)`. The canonical span for referencing the entity at `b` is `(b, δ(1, #b))`.

By L4(c), endset spans may reference addresses in the link subspace — no code path at any layer distinguishes "addressable" from "non-addressable" objects.

## L14 — DualPrimitive (INV, predicate)

The set of addresses at which entity values reside is `dom(Σ.C) ∪ dom(Σ.L)`. No state component maps an address outside this union to an entity value.

`dom(Σ.C) ∩ dom(Σ.L) = ∅`

Arrangements `Σ.M(d)` are mappings *between* addresses — V-positions are not entities in their own right. Documents, accounts, servers, and nodes are organizational concepts with no stored representation.
