# ASN-0043 Formal Statements

*Source: ASN-0043-link-ontology.md (revised 2026-03-16) — Extracted: 2026-03-22*

## Definition — LinkStore

`Σ.L : T ⇀ Link` is the *link store*, a partial function mapping tumbler addresses to link values. The domain `dom(Σ.L)` is the set of addresses at which links have been created.

The full system state: `Σ = (Σ.C, Σ.M, Σ.L)`

## Definition — Endset

`Endset = 𝒫_fin(Span)`

where `Span` is the set of well-formed span pairs `(s, ℓ)` satisfying T12 (SpanWellDefined): `ℓ > 0` and the action point `k` of `ℓ` satisfies `k ≤ #s`. The empty set `∅` is a valid endset.

## Definition — Link

`Link = {(e₁, e₂, ..., eₙ) : N ≥ 2, each eᵢ ∈ Endset}`

`|L|` denotes the *arity* of a link — the number of endsets in the sequence.

**Convention — StandardTriple.** The standard link form has arity 3, with slot 1 as the *from-endset*, slot 2 as the *to-endset*, and slot 3 as the *type-endset*. Written `(F, G, Θ)`.

## Definition — Coverage

For an endset `e`, the *coverage* is:

`coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ})`

## Definition — LinkHome

For a link at address `a ∈ dom(Σ.L)`, its *home document* is:

`home(a) = origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

## Definition — TypeByAddress (L8, DEF)

For links following the standard triple convention (`|Σ.L(a)| ≥ 3`), type matching is by *address identity*, not by content at the address:

`same_type(a₁, a₂) ⟺ Σ.L(a₁).type = Σ.L(a₂).type`

where endset equality is set equality of spans.

---

## L0 — SubspacePartition (INV, predicate)

The system designates subspace identifiers `s_C ≠ s_L` for content and links respectively.

`(A a ∈ dom(Σ.L) :: fields(a).E₁ = s_L)`

`(A a ∈ dom(Σ.C) :: fields(a).E₁ = s_C)`

Derived by T7 (SubspaceDisjoint):

`dom(Σ.L) ∩ dom(Σ.C) = ∅`

## L1 — LinkElementLevel (INV, predicate)

`(A a ∈ dom(Σ.L) :: zeros(a) = 3)`

## L1a — LinkScopedAllocation (INV, predicate)

`(A a ∈ dom(Σ.L) :: origin(a) identifies the allocating document)`

## L2 — OwnershipEndsetIndependence (LEMMA, lemma)

`(A a ∈ dom(Σ.L) :: home(a) depends only on a)`

## L3 — NEndsetStructure (INV, predicate)

`(A a ∈ dom(Σ.L) :: |Σ.L(a)| ≥ 2 ∧ (A i : 1 ≤ i ≤ |Σ.L(a)| : Σ.L(a).eᵢ ∈ Endset))`

## L4 — EndsetGenerality (LEMMA, lemma)

`(A a ∈ dom(Σ.L), i : 1 ≤ i ≤ |Σ.L(a)|, (s, ℓ) ∈ Σ.L(a).eᵢ :: s ∈ T ∧ (s, ℓ) satisfies T12)`

The substantive content is the *absence* of additional constraints beyond T12:

(a) *Cross-document endsets.* A single endset may contain spans whose start addresses fall under different document-level prefixes. No constraint prevents this.

(b) *Intra-document links.* Nothing prevents a link's endsets from referencing content within the link's own home document.

(c) *Cross-subspace endsets.* Endset spans may reference addresses in the link subspace — addresses of other links.

## L5 — EndsetSetSemantics (INV, predicate)

`(A a ∈ dom(Σ.L), e :: Σ.L(a).e is characterized by {(s, ℓ) : (s, ℓ) ∈ Σ.L(a).e})`

An endset is an *unordered* set; the ordering of spans within an endset carries no semantic meaning. Only membership matters.

## L6 — SlotDistinction (INV, predicate)

A link is a sequence — permuting endset slots produces a different link value when the permuted entries differ. For the standard triple:

`(A F, G, Θ :: F ≠ G ⟹ (F, G, Θ) ≠ (G, F, Θ))`

## L7 — DirectionalFlexibility (META)

The invariants L0–L14 impose no constraint on which of the from/to slots carries directional significance; any directional interpretation is determined by the link type, outside the link structure.

## L9 — TypeGhostPermission (LEMMA, lemma)

For links following the standard triple convention: for any conforming state `Σ` satisfying L0–L14 and S0–S3, there exists a conforming state `Σ'` extending `Σ` with a standard-triple link whose type endset references an address outside `dom(Σ'.C) ∪ dom(Σ'.L)`:

`(A Σ : Σ satisfies L0–L14 ∧ S0–S3 : (E Σ' extending Σ, a ∈ dom(Σ'.L), (s, ℓ) ∈ Σ'.L(a).type :: coverage({(s, ℓ)}) ⊄ dom(Σ'.C) ∪ dom(Σ'.L)))`

## PrefixSpanCoverage — PrefixSpanCoverage (LEMMA, lemma)

For any tumbler `x` with `#x ≥ 1`:

`coverage({(x, δ(1, #x))}) = {t ∈ T : x ≼ t}`

where `δ(1, #x)` is the displacement `[0, ..., 0, 1]` of length `#x` with action point `k = #x`, and `x ⊕ δ(1, #x) = shift(x, 1) = [x₁, ..., x_{#x-1}, x_{#x} + 1]`.

*Inclusion* (`{t : x ≼ t} ⊆ coverage`): let `c` extend `x`, so `x ≼ c`. By T1(ii), `c ≥ x`. Since `c` agrees with `x` at all positions `1` through `#x`, we have `c_{#x} = x_{#x} < x_{#x} + 1 = shift(x, 1)_{#x}`, giving `c < shift(x, 1)` by T1(i). Therefore `c ∈ [x, shift(x, 1))`.

*Exclusion* (`coverage ⊆ {t : x ≼ t}`): every `t ∈ [x, shift(x, 1))` with `t ≠ x` must extend `x`, by case analysis on depth:

- *Same depth* (`#t = #x`): since `t ≠ x`, let `j = divergence(t, x)`. As `t > x`, T1(i) gives `t_j > x_j`. If `j < #x`: `t_j > shift(x, 1)_j`, giving `t > shift(x, 1)`. If `j = #x`: `t_{#x} ≥ shift(x, 1)_{#x}`. Only `x` itself survives, and `x ≼ x` holds trivially.
- *Greater depth* (`#t > #x`): if `t` does not extend `x`, let `j = divergence(t, x)`. If `j < #x`: `t_j > shift(x, 1)_j`, giving `t > shift(x, 1)`. If `j = #x`: `t_{#x} ≥ shift(x, 1)_{#x}` — either `t > shift(x, 1)` or `shift(x, 1)` is a proper prefix of `t`, giving `shift(x, 1) < t`. Either way `t ≥ shift(x, 1)` — outside the interval.
- *Shorter depth* (`#t < #x`): if `t` agrees with `x` at all positions `1..#t`, then `x` extends `t`, so `t < x` — contradiction. Otherwise `t > shift(x, 1)`.

## L10 — TypeHierarchyByContainment (LEMMA, lemma)

For type addresses `p, c ∈ T` where `p ≼ c`, define `subtypes(p) = {c ∈ T : p ≼ c}`. By T5 (ContiguousSubtrees), `subtypes(p)` is a contiguous interval under T1. By PrefixSpanCoverage:

`coverage({(p, δ(1, #p))}) = {t ∈ T : p ≼ t} = subtypes(p)`

A single span query rooted at `p` matches all and only subtypes of `p`.

## GlobalUniqueness — GlobalUniqueness (LEMMA, lemma)

No two allocation events anywhere in the system, at any time, produce the same address.

*Proof sketch.* For any two allocation events producing addresses `a` and `b` with respective allocator prefixes `p_a` and `p_b`:

(i) *Same allocator* (`p_a = p_b`): by T9 (ForwardAllocation), allocation within each allocator is strictly increasing — if `a` is allocated before `b`, then `a < b`, hence `a ≠ b`.

(ii) *Incomparable prefixes* (`p_a ⋠ p_b ∧ p_b ⋠ p_a`): by T10 (PartitionIndependence), `a ≠ b`.

(iii) *Comparable prefixes* (`p_a ≼ p_b` or `p_b ≼ p_a`, with `p_a ≠ p_b`): WLOG suppose `p_a ≼ p_b`. By T10a (AllocatorDiscipline), each allocator produces sibling outputs exclusively via `inc(·, 0)`, which by TA5(c) preserves tumbler length: `#t' = #t`. Child spawning via `inc(·, k')` with `k' > 0` increases depth by TA5(d): `#t' = #t + k'`. Since `p_a` is a proper prefix of `p_b`, the child allocator operates at strictly greater depth. Its outputs therefore have strictly greater tumbler length. By T3 (CanonicalRepresentation), tumblers of different lengths are unequal, so `a ≠ b`.

## L11a — LinkUniqueness (LEMMA, lemma)

Link addresses are produced by forward allocation (T9) within the link subspace. By GlobalUniqueness, no two allocation events anywhere in the system, at any time, produce the same address. Therefore every link has a globally unique, permanent identity, and the question "are these the same link?" reduces to tumbler comparison (T2, IntrinsicComparison).

## L11b — NonInjectivity (LEMMA, lemma)

The link store imposes no injectivity constraint — multiple addresses may store the same endset sequence:

`(A Σ satisfying L0–L14, a ∈ dom(Σ.L) :: (E Σ' extending Σ, a' ∈ dom(Σ'.L) :: a' ≠ a ∧ Σ'.L(a') = Σ.L(a) ∧ Σ' satisfies L0–L14))`

The invariants *permit* non-injectivity — every state with a link can be extended to a non-injective state — but they do not *require* it.

## L12 — LinkImmutability (INV, predicate)

For every state transition `Σ → Σ'`:

`(A Σ, Σ' : Σ → Σ' : (A a : a ∈ dom(Σ.L) : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)))`

## L12a — LinkStoreMonotonicity (LEMMA, lemma)

Corollary of L12. For every state transition `Σ → Σ'`:

`dom(Σ.L) ⊆ dom(Σ'.L)`

## L13 — ReflexiveAddressing (LEMMA, lemma)

Link addresses are valid targets for endset spans. For any link at address `b ∈ dom(Σ.L)`, `b` is an element-level tumbler by L1, so `#b ≥ 1` and PrefixSpanCoverage applies. The unit-depth span `(b, δ(1, #b))` is well-formed, and:

`coverage({(b, δ(1, #b))}) = {t ∈ T : b ≼ t}`

An endset *references* an entity at address `a` when `a ∈ coverage(e)`, and `(b, δ(1, #b))` is the canonical span for referencing the entity at `b`.

## L14 — DualPrimitive (INV, predicate)

The set of addresses at which entity values reside is `dom(Σ.C) ∪ dom(Σ.L)`. No state component maps an address outside this union to an entity value. The two domains are disjoint:

`dom(Σ.C) ∩ dom(Σ.L) = ∅`

Arrangements `Σ.M(d)` are mappings *between* addresses — they relate V-positions to I-addresses — but V-positions are not entities in their own right.
