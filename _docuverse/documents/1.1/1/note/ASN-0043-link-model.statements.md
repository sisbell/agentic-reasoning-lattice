# ASN-0043 Claim Statements

*Source: ASN-0043-link-model.md (revised 2026-04-09) — Extracted: 2026-05-13*

## Definition — LinkStore

`Σ.L : T ⇀ Link` is the *link store*, a partial function mapping tumbler addresses to link values. The domain `dom(Σ.L)` is the set of addresses at which links have been created.

The full system state is:

`Σ = (Σ.C, Σ.M, Σ.L)`

where `Σ.C` is the content store (ASN-0036), `Σ.M` is the family of arrangements (ASN-0036), and `Σ.L` is the link store (this ASN).

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

*Convention — StandardTriple.* The standard link form has arity 3, with slot 1 as the *from-endset*, slot 2 as the *to-endset*, and slot 3 as the *type-endset*. Written `(F, G, Θ)`.

*Named accessor.* `Σ.L(a).type ≡ Σ.L(a).e₃` — interchangeable with the indexed form in all formal statements.

---

## Definition — Coverage

For an endset `e`, the *coverage* is the union of the sets denoted by its spans:

`coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ})`

---

## Definition — LinkHome

For a link at address `a ∈ dom(Σ.L)`, its *home document* is:

`home(a) = N(a).0.U(a).0.D(a)`

Preconditions: by L1c (LinkAllocatorConformance) and T10a.4 (T4PreservationUnderDiscipline, ASN-0034), link addresses are T4-valid; L1 establishes `zeros(a) = 3`, placing them at element level with all four fields present; therefore T4b's projections `N`, `U`, `D` are well-defined and the formula computes correctly.

---

## Definition — SameType (L8 — TypeByAddress)

`same_type(a₁, a₂) ⟺ coverage(Σ.L(a₁).type) = coverage(Σ.L(a₂).type)`

where `Σ.L(a).type` denotes slot 3 — well-defined for every `a ∈ dom(Σ.L)` by L3's `|Σ.L(a)| ≥ 3` — and `coverage(·)` is the address-set projection defined above. The relation is on coverage (the address set referenced by the endset), not on span-set identity.

*Closure properties:*
- *Reflexive.* `(A a ∈ dom(Σ.L) :: same_type(a, a))`
- *Symmetric.* `(A a₁, a₂ ∈ dom(Σ.L) :: same_type(a₁, a₂) ⟹ same_type(a₂, a₁))`
- *Transitive.* `(A a₁, a₂, a₃ ∈ dom(Σ.L) :: same_type(a₁, a₂) ∧ same_type(a₂, a₃) ⟹ same_type(a₁, a₃))`

---

## L-fin — LinkStoreFiniteness (INV, predicate)

For each reachable system state, `dom(Σ.L)` is finite:

`|dom(Σ.L)| < ∞`

---

## L0 — SubspacePartition (INV, predicate)

Every link address has subspace identifier `s_L`, and every content address has subspace identifier `s_C`, where `s_C ≠ s_L`:

`(A a ∈ dom(Σ.L) :: subspace_I(a) = s_L)`

`(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)`

Derived consequence (by T7, with T4-validity discharged via L1c+T10a.4 for link addresses and S7b+T4b for content addresses, and `zeros(a) = zeros(b) = 3` on each side):

`dom(Σ.L) ∩ dom(Σ.C) = ∅`

---

## L1 — LinkElementLevel (INV, predicate)

Every link address is an element-level tumbler:

`(A a ∈ dom(Σ.L) :: zeros(a) = 3)`

---

## L1a — LinkScopedAllocation (INV, predicate)

Every link address is allocated under the tumbler prefix of the document whose owner created it. By L1, `zeros(a) = 3` for every `a ∈ dom(Σ.L)`. By L1c and T10a.4, every link address is T4-valid, so T4b's projections `N(a)`, `U(a)`, `D(a)` are well-defined on every `a ∈ dom(Σ.L)`. The document-level prefix is extractable as `N(a).0.U(a).0.D(a)`, and the invariant is:

`(A a ∈ dom(Σ.L) :: N(a).0.U(a).0.D(a) ∈ dom(Σ.M))`

Once `home(a)` is defined, equivalently: `home(a) ∈ dom(Σ.M)`.

---

## L1b — LinkElementFieldDepth (INV, predicate)

Every link address has element field depth at least 2:

`(A a ∈ dom(Σ.L) :: #E(a) ≥ 2)`

---

## L1c — LinkAllocatorConformance (AXIOM, axiom)

Link allocation operates within a system conforming to T10a (AllocatorDiscipline, ASN-0034): link addresses are produced by allocators that use `inc(·, 0)` for sibling allocation and `inc(·, k')` with `k' ∈ {1, 2}` (within the TA5a bounds) for child-spawning.

Chain-origin clause: writing `h(a) = N(a).0.U(a).0.D(a)` for the document-level prefix of `a`:

`(A a ∈ dom(Σ.L) :: (E n ≥ 1, t₀, t₁, ..., tₙ :: t₀ = h(a) ∧ tₙ = a ∧ (A i : 1 ≤ i ≤ n : tᵢ = inc(tᵢ₋₁, kᵢ) ∧ the step at i is T10a-admissible at tᵢ₋₁) ∧ k₁ ∈ {1, 2} ∧ (A i : 1 ≤ i ≤ n : #tᵢ > #h(a))))`

The seed `t₀` is `h(a)` itself — not an arbitrary tumbler that contains `h(a)` as a prefix; the first step is a child-spawn that lifts depth from `#h(a)` to `#h(a) + 1`; every subsequent intermediate state has length strictly greater than `#h(a)`.

Consequence: GlobalUniqueness (ASN-0034) applies to link addresses, since its sole precondition is T10a conformance.

---

## L2 — OwnershipEndsetIndependence (LEMMA, lemma)

The home document of a link is determined entirely by the link's address and is independent of the link's endsets:

`(A a ∈ dom(Σ.L) :: home(a) depends only on a)`

---

## L3 — NEndsetStructure (INV, predicate)

Every link in the link store is a sequence of at least three endsets, with slot 3 reserved as the type endset:

`(A a ∈ dom(Σ.L) :: |Σ.L(a)| ≥ 3 ∧ (A i : 1 ≤ i ≤ |Σ.L(a)| : Σ.L(a).eᵢ ∈ Endset))`

---

## L4 — EndsetGenerality (META, meta)

The spans within an endset may reference any addresses in the tumbler space. There is no constraint confining spans to a single document, to content addresses only, or to addresses at which content currently exists.

Formal content (from definitions): by L3, every link value is a sequence of endsets of type `Endset = 𝒫_fin(Span)`:

`(A a ∈ dom(Σ.L), i : 1 ≤ i ≤ |Σ.L(a)|, (s, ℓ) ∈ Σ.L(a).eᵢ :: s ∈ T ∧ (s, ℓ) satisfies T12)`

Sub-items (explicit absences of additional constraints):

(a) *Cross-document endsets.* A single endset may contain spans whose start addresses fall under different document-level prefixes.

(b) *Intra-document links.* Nothing prevents a link's endsets from referencing content within the link's own home document.

(c) *Cross-subspace endsets.* Endset spans may reference addresses in the link subspace — that is, addresses of other links.

---

## L5 — EndsetSetSemantics (INV, predicate)

An endset is an *unordered* set; the ordering of spans within an endset carries no semantic meaning. Two endsets are equal iff they have the same span members:

`(A a, a' ∈ dom(Σ.L), i ∈ {1, ..., |Σ.L(a)|}, j ∈ {1, ..., |Σ.L(a')|} :: Σ.L(a).eᵢ = Σ.L(a').eⱼ ⟺ (A (s, ℓ) :: (s, ℓ) ∈ Σ.L(a).eᵢ ⟺ (s, ℓ) ∈ Σ.L(a').eⱼ))`

The substantive content: (i) endset equality reduces to extensional set equality over `Span`, and (ii) no operator in the model selects a span by position within an endset.

---

## L6 — SlotDistinction (INV, predicate)

The endsets within a link are addressable by slot position. The link model provides a positional accessor `Σ.L(a).eᵢ` returning the i-th endset, defined for every `a ∈ dom(Σ.L)` and every `i ∈ {1, ..., |Σ.L(a)|}`. Slot index is a primitive of the model, not a derived label over an unordered collection. Link equality is component-wise tuple equality, by the `Link = {(e₁, ..., eₙ) : N ≥ 3, each eᵢ ∈ Endset}` definition.

Standard-triple consequence: when `F ≠ G`, `(F, G, Θ) ≠ (G, F, Θ)`; more generally, any slot-permutation that swaps differing entries produces a distinct link value by component-wise tuple inequality.

---

## L7 — DirectionalFlexibility (META, meta)

The invariants L0–L14 and L-fin impose no constraint on which of the from/to slots carries directional significance; any directional interpretation is determined by the link type, outside the link structure.

No invariant uses the words "from," "to," "source," "target," "origin," or "destination" in any structural role; the F/G labels in the standard triple `(F, G, Θ)` are nominal conveniences for prose, not constraints carried by the invariants.

---

## L9 — TypeGhostPermission (LEMMA, lemma)

For any state `Σ` satisfying all invariants of this ASN (L0–L14, L-fin) together with all ASN-0036 invariants (S0–S3, S7a, S7b, S7c, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ), and with `dom(Σ.M) ≠ ∅`, there exists a conforming state `Σ'` extending `Σ` with a standard-triple link whose type endset references an address outside `dom(Σ'.C) ∪ dom(Σ'.L)`:

`(A Σ : Σ satisfies all L- and S-invariants ∧ dom(Σ.M) ≠ ∅ : (E Σ' extending Σ, a ∈ dom(Σ'.L), (s, ℓ) ∈ Σ'.L(a).type :: coverage({(s, ℓ)}) ⊄ dom(Σ'.C) ∪ dom(Σ'.L)))`

---

## PrefixSpanCoverage — PrefixSpanCoverage (LEMMA, lemma)

For any tumbler `x` with `#x ≥ 1`, `δ(1, #x)` (OrdinalDisplacement, ASN-0034) is the displacement `[0, ..., 0, 1]` of length `#x`, with action point `k = #x`. The span `(x, δ(1, #x))` is well-formed by T12: `δ(1, #x) > 0` and `k ≤ #x`. By OrdinalShift (ASN-0034), `x ⊕ δ(1, #x) = shift(x, 1) = [x₁, ..., x_{#x-1}, x_{#x} + 1]`. By StrictIncrease (TA-strict, ASN-0034) applied at `k ≥ 1`, `x < shift(x, 1)`. Then:

`coverage({(x, δ(1, #x))}) = {t ∈ T : x ≼ t}`

---

## L10 — TypeHierarchyByContainment (LEMMA, lemma)

For type addresses `p, c ∈ T` where `p ≼ c`, define `subtypes(p) = {c ∈ T : p ≼ c}`. By T5 (ContiguousSubtrees, ASN-0034), `subtypes(p)` is a contiguous interval under T1. By PrefixSpanCoverage:

`coverage({(p, δ(1, #p))}) = {t ∈ T : p ≼ t} = subtypes(p)`

*Hierarchy inclusion.* The map `p ↦ subtypes(p)` reverses prefix order:

`(A p₁, p₂ ∈ T :: p₁ ≼ p₂ ⟹ subtypes(p₂) ⊆ subtypes(p₁))`

---

## L11a — LinkUniqueness (LEMMA, lemma)

Link addresses are produced by forward allocation (T9, ASN-0034) within the link subspace, by allocators conforming to T10a (L1c, LinkAllocatorConformance). T10a conformance is the precondition of GlobalUniqueness (ASN-0034), so distinct allocation events anywhere in the system produce distinct link addresses:

`(A a₁, a₂ ∈ dom(Σ.L) : a₁, a₂ produced by distinct allocation events : a₁ ≠ a₂)`

Equivalently, the question "are these the same link?" reduces to tumbler comparison (T2, IntrinsicComparison, ASN-0034).

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

## L13 — ReflexiveAddressing (LEMMA, lemma)

Link addresses are valid targets for endset spans. For any link at address `b ∈ dom(Σ.L)`, `b` is an element-level tumbler by L1, so `#b ≥ 1` and PrefixSpanCoverage applies. The unit-depth span `(b, δ(1, #b))` is well-formed, and:

`coverage({(b, δ(1, #b))}) = {t ∈ T : b ≼ t}`

An endset *references* an entity at address `a` when `a ∈ coverage(e)`, and `(b, δ(1, #b))` is the canonical span for referencing the entity at `b`.

---

## L14 — DualPrimitive (INV, predicate)

The set of addresses at which entity values reside is `dom(Σ.C) ∪ dom(Σ.L)`. No state component maps an address outside this union to an entity value. The two domains are disjoint:

`dom(Σ.C) ∩ dom(Σ.L) = ∅`

---

## L14a — NonTranscludability (INV, predicate)

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∉ dom(Σ.L))`

Note: under the current model, S3 and L0 jointly satisfy L14a — S3 (ReferentialIntegrity, ASN-0036) requires `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`, and L0 establishes `dom(Σ.L) ∩ dom(Σ.C) = ∅`. L14a stands as an independent design requirement.
