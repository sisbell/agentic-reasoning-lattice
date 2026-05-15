# ASN-0043 Claim Statements

*Source: ASN-0043-link-model.md (revised 2026-04-09) — Extracted: 2026-05-14*

## Definition — LinkStore

`Σ.L : T ⇀ Link` is the *link store*, a partial function mapping tumbler addresses to link values. The domain `dom(Σ.L)` is the set of addresses at which links have been created.

The full system state is:

`Σ = (Σ.C, Σ.M, Σ.L)`

where `Σ.C` is the content store (ASN-0036), `Σ.M` is the family of arrangements (ASN-0036), and `Σ.L` is the link store.

---

## Definition — Endset

An *endset* is a finite set of well-formed spans:

`Endset = 𝒫_fin(Span)`

where `Span` is the set of well-formed span pairs `(s, ℓ)` satisfying T12 (SpanWellDefinedness, ASN-0034): `ℓ > 0` and the action point `k` of `ℓ` satisfies `k ≤ #s`. The empty set `∅` is a valid endset.

---

## Definition — Link

A *link value* is a finite sequence of N ≥ 3 endsets, with the third slot designated as the type endset by the StandardTriple convention:

`Link = {(e₁, e₂, ..., eₙ) : N ≥ 3, each eᵢ ∈ Endset}`

`|L|` denotes the *arity* of a link — the number of endsets in the sequence.

**Convention — StandardTriple.** The standard link form has arity 3, with slot 1 as the *from-endset*, slot 2 as the *to-endset*, and slot 3 as the *type-endset*. Written `(F, G, Θ)`.

*Named accessor.* `Σ.L(a).type ≡ Σ.L(a).e₃` — the two forms are interchangeable; `.type` preferred when the role is salient, `.e₃` when the position is load-bearing.

---

## Definition — Coverage

For an endset `e`, define the *coverage* as the union of the sets denoted by its spans:

`coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ})`

Coverage is a lossy projection: two endsets with different span decompositions may have identical coverage.

---

## Definition — LinkHome

For a link at address `a ∈ dom(Σ.L)`, its *home document* is:

`home(a) = N(a).0.U(a).0.D(a)`

Preconditions: `a` is T4-valid (derived via L1c + T10a.4); `zeros(a) = 3` (L1), placing it at element level with all four fields present; therefore T4b's projections `N`, `U`, `D` are well-defined.

---

## L-fin — LinkStoreFiniteness (INV, predicate)

For each reachable system state, `dom(Σ.L)` is finite:

`|dom(Σ.L)| < ∞`

---

## L0 — SubspacePartition (INV, predicate)

Every link address has subspace identifier `s_L`:

`(A a ∈ dom(Σ.L) :: subspace_I(a) = s_L)`

`s_L` is the link subspace identifier. Together with L0a, yields the scoped disjointness `dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅` via T7.

---

## L0a — ContentSubspaceScope (DEF, function)

Define:

`dom(Σ.C)|_{s_C} = {a ∈ dom(Σ.C) : subspace_I(a) = s_C}`

— the slice of `dom(Σ.C)` whose addresses occupy subspace `s_C`. The disjointness this ASN derives is:

`dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅`

Conforming systems whose content stores are entirely `s_C`-resident enjoy the global disjointness `dom(Σ.L) ∩ dom(Σ.C) = ∅` as a corollary.

---

## L1 — LinkElementLevel (INV, predicate)

Every link address is an element-level tumbler:

`(A a ∈ dom(Σ.L) :: zeros(a) = 3)`

---

## L1a — LinkScopedAllocation (INV, predicate)

Every link address is allocated under the tumbler prefix of the document whose owner created it. With L1 and L1c's T4-validity postcondition, T4b's projections `N(a)`, `U(a)`, `D(a)` are well-defined on every `a ∈ dom(Σ.L)`. The invariant:

`(A a ∈ dom(Σ.L) :: N(a).0.U(a).0.D(a) ∈ dom(Σ.M))`

The membership clause is the substantive constraint: the document-level prefix `N(a).0.U(a).0.D(a)` must be an allocated, owned document in the current state. Once `home(a)` is defined, the invariant reads `home(a) ∈ dom(Σ.M)`.

---

## L1b — LinkElementFieldDepth (INV, predicate)

Every link address has element field depth at least 2:

`(A a ∈ dom(Σ.L) :: #E(a) ≥ 2)`

---

## L1c — LinkAllocatorConformance (AXIOM, axiom)

Link allocation operates within a system conforming to T10a (AllocatorDiscipline, ASN-0034). Single chain-existential clause:

*Chain.* There exists a T4-valid document-level seed `s` and a T10a-conforming step sequence terminating at `a`:

`(A a ∈ dom(Σ.L) :: (E s ∈ T, n ≥ 1, t₀, t₁, ..., tₙ, k₁, ..., kₙ :: T4-valid(s) ∧ zeros(s) = 2 ∧ t₀ = s ∧ tₙ = a ∧ (A i : 1 ≤ i ≤ n : tᵢ = inc(tᵢ₋₁, kᵢ) ∧ kᵢ ∈ {0, 1, 2} ∧ (kᵢ = 2 ⟹ zeros(tᵢ₋₁) ≤ 2)) ∧ k₁ = 2 ∧ (A i : 1 ≤ i ≤ n : #tᵢ > #s)))`

*Postcondition: T4-validity of `a`.* By T10a.4, every link address is T4-valid.

*Postcondition: `s = h(a)`.* Chain-prefix-preservation gives `a` agreeing with `s` on positions `1..#s`; the third zero of `a` first appears at position `#s + 1`; the prefix of `a` ending just before the third zero is exactly `s`, which by definition is `h(a)`. Hence `s = h(a)`.

---

## L2 — OwnershipEndsetIndependence (LEMMA, lemma)

The home document of a link is determined entirely by the link's address and is independent of the link's endsets:

`(A a ∈ dom(Σ.L) :: home(a) depends only on a)`

---

## L3 — NEndsetStructure (INV, predicate)

Every link in the link store is a sequence of at least three endsets, each in `Endset`, with slot 3 a non-empty type endset:

`(A a ∈ dom(Σ.L) :: |Σ.L(a)| ≥ 3 ∧ (A i : 1 ≤ i ≤ |Σ.L(a)| : Σ.L(a).eᵢ ∈ Endset) ∧ Σ.L(a).e₃ ≠ ∅)`

---

## L4 — EndsetGenerality (META, meta)

The spans within an endset may reference any addresses in the tumbler space. The formal content follows from definitions:

`(A a ∈ dom(Σ.L), i : 1 ≤ i ≤ |Σ.L(a)|, (s, ℓ) ∈ Σ.L(a).eᵢ :: s ∈ T ∧ (s, ℓ) satisfies T12)`

Sub-items (absent constraints):

(a) *Cross-document endsets.* A single endset may contain spans whose start addresses fall under different document-level prefixes.

(b) *Intra-document links.* Nothing prevents a link's endsets from referencing content within the link's own home document.

(c) *Cross-subspace endsets.* Endset spans may reference addresses in the link subspace — addresses of other links.

---

## L5 — EndsetSetSemantics (INV, predicate)

An endset is an *unordered* set; the ordering of spans within an endset carries no semantic meaning:

`(A a, a' ∈ dom(Σ.L), i ∈ {1, ..., |Σ.L(a)|}, j ∈ {1, ..., |Σ.L(a')|} :: Σ.L(a).eᵢ = Σ.L(a').eⱼ ⟺ (A (s, ℓ) :: (s, ℓ) ∈ Σ.L(a).eᵢ ⟺ (s, ℓ) ∈ Σ.L(a').eⱼ))`

---

## L6 — SlotDistinction (INV, predicate)

The endsets within a link are addressable by slot position. The link model provides a positional accessor `Σ.L(a).eᵢ` returning the i-th endset, defined for every `a ∈ dom(Σ.L)` and every `i ∈ {1, ..., |Σ.L(a)|}`. Slot index is a primitive of the model, not a derived label over an unordered collection. Link equality is component-wise tuple equality, by the `Link = {(e₁, ..., eₙ) : N ≥ 3, each eᵢ ∈ Endset}` definition.

Standard-triple consequence: when `F ≠ G`, `(F, G, Θ) ≠ (G, F, Θ)`; more generally, any slot-permutation that swaps differing entries produces a distinct link value by component-wise tuple inequality.

---

## L7 — DirectionalFlexibility (META, meta)

The invariants L0–L14 and L-fin impose no constraint on which of the from/to slots carries directional significance; any directional interpretation is determined by the link type, outside the link structure.

---

## L8 — TypeByAddress (DEF, function)

Type matching is by *address identity*, not by content at the address:

`same_type(a₁, a₂) ⟺ coverage(Σ.L(a₁).type) = coverage(Σ.L(a₂).type)`

where `Σ.L(a).type` denotes slot 3 — well-defined for every `a ∈ dom(Σ.L)` by L3's `|Σ.L(a)| ≥ 3` — and `coverage(·)` is the address-set projection. The relation is on coverage (the address set referenced by the endset), not on span-set identity.

`same_type` is an equivalence relation on `dom(Σ.L)`:

- *Reflexive.* `(A a ∈ dom(Σ.L) :: same_type(a, a))`
- *Symmetric.* `(A a₁, a₂ ∈ dom(Σ.L) :: same_type(a₁, a₂) ⟹ same_type(a₂, a₁))`
- *Transitive.* `(A a₁, a₂, a₃ ∈ dom(Σ.L) :: same_type(a₁, a₂) ∧ same_type(a₂, a₃) ⟹ same_type(a₁, a₃))`

---

## L9 — TypeGhostPermission (LEMMA, lemma)

For any state `Σ` satisfying all invariants of this ASN (L0–L14, L-fin) together with all ASN-0036 invariants (S0–S3, S7a, S7b, S7c, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ), with `dom(Σ.M) ≠ ∅`, and with `s_C`-resident content (`(A b ∈ dom(Σ.C) :: subspace_I(b) = s_C)`), there exists for every arity `N ≥ 3` a conforming state `Σ'` extending `Σ` with a link of arity `N` whose type endset references an address outside `dom(Σ'.C) ∪ dom(Σ'.L)`:

`(A Σ : Σ satisfies all L- and S-invariants ∧ dom(Σ.M) ≠ ∅ ∧ (A b ∈ dom(Σ.C) :: subspace_I(b) = s_C) : (A N ≥ 3 :: (E Σ' extending Σ, a ∈ dom(Σ'.L), (s, ℓ) ∈ Σ'.L(a).type :: |Σ'.L(a)| = N ∧ coverage({(s, ℓ)}) ⊄ dom(Σ'.C) ∪ dom(Σ'.L))))`

---

## PrefixSpanCoverage — PrefixSpanCoverage (AXIOM, axiom)

For any tumbler `x` with `#x ≥ 1`, the unit-depth displacement `δ(1, #x)` (OrdinalDisplacement, ASN-0034) is `[0, ..., 0, 1]` of length `#x`, with action point `k = #x`; the span `(x, δ(1, #x))` is well-formed by T12; and:

`coverage({(x, δ(1, #x))}) = {t ∈ T : x ≼ t}`

equivalently `x ⊕ δ(1, #x) = shift(x, 1)`.

---

## L10 — TypeHierarchyByContainment (LEMMA, lemma)

For type addresses `p, c ∈ T` where `p ≼ c`, define `subtypes(p) = {c ∈ T : p ≼ c}`. By T5 (ContiguousSubtrees, ASN-0034), `subtypes(p)` is a contiguous interval under T1. By PrefixSpanCoverage:

`coverage({(p, δ(1, #p))}) = {t ∈ T : p ≼ t} = subtypes(p)`

*Hierarchy inclusion.*

`(A p₁, p₂ ∈ T :: p₁ ≼ p₂ ⟹ subtypes(p₂) ⊆ subtypes(p₁))`

---

## L11a — LinkUniqueness (LEMMA, lemma)

Distinct T10a-conforming allocation events produce distinct link addresses. Formally, for any pair of allocation events producing link addresses `a₁` and `a₂` in the system, if the events are distinct then `a₁ ≠ a₂` as tumblers — and equivalently, every `a ∈ dom(Σ.L)` corresponds to a single allocation event.

This is a corollary of L1c (LinkAllocatorConformance) combined with T10a's GlobalUniqueness (ASN-0034). Two cases in the derivation:

(i) `home(a₁) ≠ home(a₂) ⟹ a₁ ≠ a₂` — `home(·)` is a deterministic projection of a T4-valid address, so equal arguments force equal outputs; contrapositive yields the result.

(ii) `home(a₁) = home(a₂)` — T10a's per-`(t, k')` discipline (GlobalUniqueness) forces any two chains terminating at a common point to coincide on the entire shared tail, contradicting the assumed distinctness of allocation events.

---

## L11b — NonInjectivity (LEMMA, lemma)

The link store imposes no injectivity constraint — multiple addresses may store the same endset sequence:

`(A Σ satisfying all L- and S-invariants, a ∈ dom(Σ.L) :: (E Σ' extending Σ, a' ∈ dom(Σ'.L) :: a' ≠ a ∧ Σ'.L(a') = Σ.L(a) ∧ Σ' satisfies all L- and S-invariants))`

where "all L- and S-invariants" denotes L0–L14, L-fin, and ASN-0036's S0–S3, S7a, S7b, S7c, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ.

---

## L12 — LinkImmutability (INV, predicate)

Once created, a link's address persists and its value is permanently fixed:

`(A Σ, Σ' : Σ → Σ' : (A a : a ∈ dom(Σ.L) : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)))`

for every state transition `Σ → Σ'`.

---

## L12a — LinkStoreMonotonicity (LEMMA, lemma)

The domain of the link store is monotonically non-decreasing:

`[dom(Σ.L) ⊆ dom(Σ'.L)]`

for every state transition `Σ → Σ'`.

---

## L12b — HomeDocumentPersistence (LEMMA, lemma)

The home documents of all existing links remain allocated across every state transition:

`(A Σ, Σ' : Σ → Σ' :: {home(a) : a ∈ dom(Σ.L)} ⊆ dom(Σ'.M))`

---

## L13 — ReflexiveAddressing (LEMMA, lemma)

Link addresses are valid targets for endset spans. For any link at address `b ∈ dom(Σ.L)`, `b` is an element-level tumbler by L1, so `#b ≥ 1` and PrefixSpanCoverage applies. The unit-depth span `(b, δ(1, #b))` is well-formed, and:

`coverage({(b, δ(1, #b))}) = {t ∈ T : b ≼ t}`

The canonical span contains exactly the target entity and its extensions, with no extraneous tumblers. An endset *references* an entity at address `a` when `a ∈ coverage(e)`, and `(b, δ(1, #b))` is the canonical span for referencing the entity at `b`.

---

## L14 — DualPrimitive (INV, predicate)

The set of addresses at which entity values reside is `dom(Σ.C) ∪ dom(Σ.L)`. No state component maps an address outside this union to an entity value. The two domains are disjoint over the `s_C`-resident slice of content (L0a):

`dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅`

Global disjointness `dom(Σ.L) ∩ dom(Σ.C) = ∅` follows whenever every content address is `s_C`-resident.

---

## L14a — NonTranscludability (INV, predicate)

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∉ dom(Σ.L))`
