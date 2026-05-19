# ASN-0093 Claim Statements

*Source: ASN-0093-allocation-substrate.md (revised unknown) — Extracted: 2026-05-18*

## Definition — SubAllocatorAnchor

For each `d ∈ dom(M)`, two element-field anchors sit immediately under `d`:

- `b_C(d) := [d.0.s_C]` — the **content sub-allocator anchor** (one-component element field with `E₁ = s_C`, `zeros = 3`, `#E = 1`)
- `b_L(d) := [d.0.s_L]` — the **link sub-allocator anchor** (one-component element field with `E₁ = s_L`, `zeros = 3`, `#E = 1`)

These anchors are *structurally producible* by T10a `inc` steps from `d`: `b_C(d) = inc(d, 2)` (TA5(d), `k = 2`) and `b_L(d) = inc(b_C(d), 0)` (TA5(c)). The anchors themselves are *not* in `dom(C) ∪ dom(L)` — content and link addresses have `#E ≥ 2` (C1; L1b above), and the anchors have `#E = 1`.

## Definition — ActiveSubAllocatorChain

A sub-allocator chain `A_C(d)` (resp. `A_L(d)`) is *active at state* `Σ` iff `d ∈ dom(M)` at `Σ`. Concretely, "active" is the predicate under which K.α (resp. K.λ) admits the chain as the emission source for an address with `origin(·) = d`: the operation's precondition requires `d ∈ dom(M)`, which is exactly the activation condition.

## T10a-discipline-satisfying chain — T10aDisciplineSatisfyingChain (DEF, definition)

A *T10a-discipline-satisfying chain* is an *infinite* sequence `(t_1, t_2, t_3, …)` of tumblers — indexed by every `n ∈ ℕ` with `n ≥ 1` — satisfying two structural conditions, both stated without reference to allocator-tree membership or spawning triples:

  (i) *FirstElementValidity:* `t_1` is T4-valid.
  (ii) *SiblingRecurrence:* `t_{n+1} = inc(t_n, 0)` for every `n ≥ 1`.

## SubspaceConventionAxiom — FixedSubspaceIdentifiers (AXIOM, axiom)

`s_C = 1 ∧ s_L = 2`

Consequences: distinctness `s_C ≠ s_L` (abbreviated **SC-NEQ**) and sibling relation `s_L = s_C + 1`.

## SequentialTransitionAxiom — SequentialAtomicTransitions (AXIOM, axiom)

Transitions `Σ → Σ'` are atomic, uninterruptible, and totally ordered: each transition evaluates its precondition against `Σ` and commits its effect to `Σ'` in one indivisible step, with no intermediate state in which a transition has begun but not committed.

## M0 — DocumentTumblerWellFormed (INV, predicate)

`(A d ∈ dom(M) :: ValidAddress(d) ∧ zeros(d) = 2)`

Every allocated document address is a T4-valid tumbler with exactly two zero components (i.e., a document-level address per S7d of ASN-0036).

**Definitional identification.** Throughout this substrate, `ValidAddress(d) ≡ d satisfies T4 (HierarchicalParsing, ASN-0034)`. T4's four conjuncts are: `zeros(d) ≤ 3`, no adjacent zero components, `d[1] ≠ 0`, and `d[#d] ≠ 0`.

## M1 — ArrangementMonotonicity (INV, predicate)

`(A Σ → Σ' :: dom(M) ⊆ dom(M'))`

`dom(M)` is non-decreasing across all transitions. The substrate admits no transition that removes a document from `dom(M)`.

## C0 — ContentImmutability (INV, predicate)

`(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ (A a : a ∈ dom(C) : C'(a) = C(a)))`

Append-only with immutable values: `dom(C)` is non-decreasing, and no transition alters the value bound to an existing key.

## C1 — ContentElementLevel (INV, predicate)

`(A a ∈ dom(C) :: zeros(a) = 3)`

Every content address is an element-level tumbler.

## C1b — ContentElementFieldDepth (INV, predicate)

`(A a ∈ dom(C) :: #E(a) ≥ 2)`

Every content address has at least two element-field components.

## C1c — ContentAllocatorConformance (INV, predicate)

Every content address `a ∈ dom(C)` has a structural inc-chain from its home document to `a`: a finite sequence `(t₀, t₁, …, tₙ)` with `n ≥ 1`, `t₀ = origin(a)`, and `tₙ = a`, where each step `tᵢ = inc(tᵢ₋₁, kᵢ)` with `kᵢ ∈ {0, 1, 2}` satisfies T10a's per-step admissibility constraints (T4-validity preservation, including the `kᵢ = 2 ⟹ zeros(tᵢ₋₁) ≤ 2` zero-count side condition); additionally, `k₁ = 2` (the first step is a depth-2 increment off the document seed) and `(A i : 1 ≤ i ≤ n : #tᵢ > #origin(a))` (every intermediate length strictly exceeds the seed's).

## C2 — ContentScopedAllocation (INV, predicate)

`(A a ∈ dom(C) :: origin(a) ∈ dom(M))`

Every content address has its home document allocated.

## C-fin — ContentStoreFiniteness (INV, predicate)

`|dom(C)| < ∞`

The content store is finite at every reachable state.

## L0 — SubspacePartition (INV, predicate)

`(A a ∈ dom(L) :: E(a)₁ = s_L)`
`(A a ∈ dom(C) :: E(a)₁ = s_C)`

Every link address has subspace identifier `s_L`; every content address has subspace identifier `s_C`.

## L1 — LinkElementLevel (INV, predicate)

`(A a ∈ dom(L) :: zeros(a) = 3)`

Every link address is an element-level tumbler.

## L1a — LinkScopedAllocation (INV, predicate)

`(A a ∈ dom(L) :: origin(a) ∈ dom(M))`

Every link address has its home document allocated.

## L1b — LinkElementFieldDepth (INV, predicate)

`(A a ∈ dom(L) :: #E(a) ≥ 2)`

Every link address has at least two element-field components.

## L1c — LinkAllocatorConformance (INV, predicate)

Every link address `ℓ ∈ dom(L)` has a *structural inc-chain* from its home document to `ℓ`: a finite sequence `(t₀, t₁, …, tₙ)` with `n ≥ 1`, `t₀ = origin(ℓ)`, and `tₙ = ℓ`, where each step `tᵢ = inc(tᵢ₋₁, kᵢ)` with `kᵢ ∈ {0, 1, 2}` satisfies T10a's per-step admissibility constraints (T4-validity preservation, including the `kᵢ = 2 ⟹ zeros(tᵢ₋₁) ≤ 2` zero-count side condition); additionally, `k₁ = 2` (the first step is a depth-2 increment off the document seed) and `(A i : 1 ≤ i ≤ n : #tᵢ > #origin(ℓ))` (every intermediate length strictly exceeds the seed's).

## L3 — NEndsetStructure (INV, predicate)

`(A a ∈ dom(L) :: |L(a)| ≥ 3 ∧ (A i : 1 ≤ i ≤ |L(a)| : L(a).eᵢ ∈ Endset) ∧ L(a).e₃ ≠ ∅)`

Every link is a sequence of at least three endsets, with the type endset (slot 3) non-empty.

## L12 — LinkImmutability (INV, predicate)

`(A Σ → Σ' : (A a : a ∈ dom(L) : a ∈ dom(L') ∧ L'(a) = L(a)))`

Once allocated, a link's address persists in `dom(L)` and its value is permanently fixed across all transitions.

## L14 — StoreDisjointness (INV, predicate)

`dom(C) ∩ dom(L) = ∅`

Derived from L0 + SC-NEQ + StoreT4Validity + T7 (FirstElementFieldDistinction, ASN-0034): every content address has `E(·)₁ = s_C`, every link address has `E(·)₁ = s_L`, and `s_C ≠ s_L`, so the domains are disjoint.

## L-fin — LinkStoreFiniteness (INV, predicate)

`|dom(L)| < ∞`

The link store is finite at every reachable state.

## SubAllocatorAxiom — ContentLinkSubAllocatorExistence (AXIOM, axiom)

For each `d ∈ dom(M)`, two sub-allocator chains are simultaneously activated under `d` at the moment of `d`'s registration into `dom(M)` (by `K.σ`). Three clauses, independently citable as discharge premises:

- *Existence (SubAllocatorAxiom.Exists).* For every `d ∈ dom(M)`, the content sub-allocator chain `A_C(d)` (anchored at `b_C(d)`) and the link sub-allocator chain `A_L(d)` (anchored at `b_L(d)`) are active (per the *Active sub-allocator chains* definition above).

- *First emission structural form (SubAllocatorAxiom.FirstEmission).* The first emission of each chain has a concrete structural form:
  - *Content chain first-emit:* the first address produced by `A_C(d)` is `t_1^C(d) := [d.0.s_C.1]` — `E(·)₁ = s_C`, `origin(·) = d`, `#E(·) = 2`, `zeros(·) = 3`, and T4-valid by direct inspection given M0's T4-valid `d`.
  - *Link chain first-emit:* the first address produced by `A_L(d)` is `t_1^L(d) := [d.0.s_L.1]` — structurally analogous (with `s_L` in place of `s_C`); T4-valid by the same inspection.

  This clause carries only the structural form of the first emission. The freshness commitment `a ∉ dom(C) ∪ dom(L)` (resp. `ℓ ∉ dom(L) ∪ dom(C)`) at the K.α (resp. K.λ) event is *not* axiom content; it is restated as the derived lemma FirstEmissionFreshness.

- *Chain discipline (SubAllocatorAxiom.ChainDiscipline).* Each chain `A_C(d)` (resp. `A_L(d)`) is a T10a-discipline-satisfying chain (per the Definition above), rooted at FirstEmission's `t_1^C(d)` (resp. `t_1^L(d)`). The two structural conditions are discharged thus: FirstElementValidity by FirstEmission (T4-validity established above by inspection); SiblingRecurrence by axiom (`t_{n+1} = inc(t_n, 0)`).

## ChainElementT4Validity — ChainElementT4Validity (LEMMA, lemma)

`(A chain (t_1, t_2, t_3, …) satisfying FirstElementValidity ∧ SiblingRecurrence : (A n ≥ 1 :: t_n is T4-valid))`

*Corollary (sub-allocator chains).* By SubAllocatorAxiom.ChainDiscipline, `A_C(d)` and `A_L(d)` are T10a-discipline-satisfying chains; hence every element of `A_C(d)` (resp. `A_L(d)`) is T4-valid.

## ChainUniformLength — ChainUniformLength (LEMMA, lemma)

`(A chain (t_1, t_2, t_3, …) satisfying FirstElementValidity ∧ SiblingRecurrence : (A n ≥ 1 :: #t_n = #t_1))`

*Corollary (sub-allocator chains).* For each `d ∈ dom(M)`, all elements of `A_C(d)` (resp. `A_L(d)`) have length `#d + 3`.

## ChainEnumerationInjectivity — ChainEnumerationInjectivity (LEMMA, lemma)

`(A chain (t_1, t_2, t_3, …) satisfying FirstElementValidity ∧ SiblingRecurrence : (A m, n ≥ 1 : m < n : t_m < t_n))`

In particular, `n ↦ t_n` is injective on chain indices: distinct chain indices map to distinct chain elements.

*Corollary (within-chain freshness).* For each `d ∈ dom(M)` and each pair of distinct chain indices `m ≠ n` on `A_C(d)` (resp. `A_L(d)`), the two chain elements are distinct as tumblers; moreover the chain enumeration is order-preserving in both directions (`m < n ⟺ t_m < t_n`).

## ChainUniformZeroCount — ChainUniformZeroCount (LEMMA, lemma)

`(A chain (t_1, t_2, t_3, …) satisfying FirstElementValidity ∧ SiblingRecurrence : (A n ≥ 1 :: zeros(t_n) = zeros(t_1)))`

*Corollary (sub-allocator chains).* For each `d ∈ dom(M)`, every element of `A_C(d)` (resp. `A_L(d)`) has `zeros = 3`.

## DisjointSubAllocatorChains — DisjointSubAllocatorChains (LEMMA, lemma)

Addresses produced by `A_C(d)` satisfy `E(·)₁ = s_C`; addresses produced by `A_L(d)` satisfy `E(·)₁ = s_L`. Hence by SC-NEQ (`s_C ≠ s_L`), no address is produced by both chains.

## ChainPrefixExtension — ChainPrefixExtension (LEMMA, lemma)

At every reachable state `Σ`, every element of an active sub-allocator chain extends its anchor under the prefix relation:

`(A d ∈ dom(M), t ∈ A_C(d) :: b_C(d) ≼ t)`
`(A d ∈ dom(M), t ∈ A_L(d) :: b_L(d) ≼ t)`

*Quantifier scope.* `A_C(d)` and `A_L(d)` here denote the *conceptual* chains supplied by SubAllocatorAxiom.ChainDiscipline — the full `inc(·, 0)`-extension sequences `(t_1, t_2, t_3, …)` anchored at FirstEmission's first element — not the (proper) subsets of these chains realised in `dom(C)` (resp. `dom(L)`) at `Σ`.

## ChainMembershipForOrigin — ChainMembershipForOrigin (LEMMA, lemma)

At every reachable state `Σ`, every entry of `dom(C)` (resp. `dom(L)`) inhabits the content (resp. link) sub-allocator chain of its origin, and forms a *contiguous initial segment* of that chain. Letting `A_C(d) = (t_1, t_2, t_3, …)` denote the enumeration of `d`'s content sub-allocator chain (with `t_1` the first emission and `t_{n + 1} = inc(t_n, 0)`), and `A_L(d) = (s_1, s_2, s_3, …)` the analogous link chain:

- `(A d ∈ dom(M) :: (E m_d ≥ 0 :: dom(C) ∩ {a' ∈ T : origin(a') = d} = {t_1, …, t_{m_d}}))` (content contiguous prefix; `{t_1, …, t_0} = ∅` by convention)
- `(A d ∈ dom(M) :: (E n_d ≥ 0 :: dom(L) ∩ {ℓ' ∈ T : origin(ℓ') = d} = {s_1, …, s_{n_d}}))` (link contiguous prefix)

## StoreT4Validity — StoreT4Validity (LEMMA, lemma)

At every reachable state `Σ`, every entry of `dom(C) ∪ dom(L)` is a T4-valid tumbler:

`(A a ∈ dom(C) :: ValidAddress(a))`
`(A ℓ ∈ dom(L) :: ValidAddress(ℓ))`

## FirstEmissionFreshness — FirstEmissionFreshness (LEMMA, lemma)

At every reachable state `Σ`, the first emission of an active sub-allocator chain — the address that K.α (resp. K.λ) commits when the corresponding first-emit predicate fires — is fresh against `dom(C) ∪ dom(L)`:

- *Content first-emit:* Under the K.α first-emit predicate `{a' ∈ dom(C) : origin(a') = d} = ∅`, the first emission `a = [d.0.s_C.1]` of `A_C(d)` satisfies `a ∉ dom(C) ∪ dom(L)` at the K.α event that commits `a`.
- *Link first-emit:* Under the K.λ first-emit predicate `{ℓ' ∈ dom(L) : origin(ℓ') = d} = ∅`, the first emission `ℓ = [d.0.s_L.1]` of `A_L(d)` satisfies `ℓ ∉ dom(L) ∪ dom(C)` at the K.λ event that commits `ℓ`.

## Cross-doc disjointness — CrossDocDisjointness (LEMMA, lemma)

For any two distinct documents `d₁, d₂ ∈ dom(M)` with `d₁ ≠ d₂`, the link sub-allocator anchors `p₁ := b_L(d₁) = [d₁.0.s_L]` and `p₂ := b_L(d₂) = [d₂.0.s_L]` satisfy

`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`

so by T10 (PartitionIndependence, ASN-0034), every address extending `p₁` differs from every address extending `p₂`. The same lemma holds with `b_C` in place of `b_L` for content allocations.

## K.σ — DocumentRegistration (OP, operation)

Extends `dom(M)` by registering a new document address with an empty arrangement.

*Precondition:*
- `d ∉ dom(M)` (fresh document address)
- `ValidAddress(d) ∧ zeros(d) = 2` (T4-valid, document-level — discharges M0 at the new key)

*Effect:* `dom(M') = dom(M) ∪ {d}`, with `M'(d) = ∅` and `M'(d') = M(d')` for every `d' ∈ dom(M)`.

*Frame:* `C' = C; L' = L`

## K.α — ContentAllocation (OP, operation)

Extends `dom(C)` with a fresh content address scoped to an allocated document.

*Precondition:*
- `d ∈ dom(M)` (home document exists)
- `a ∉ dom(C) ∪ dom(L)` (fresh address — L14)
- `zeros(a) = 3 ∧ E(a)₁ = s_C` (element-level, content subspace — C1, L0)
- `#E(a) ≥ 2` (C1b)
- `origin(a) = d` (scoped to home document — C2)
- `a` is produced by `d`'s content sub-allocator `A_C(d)`:
  - *First emission* (predicate: `{a' ∈ dom(C) : origin(a') = d} = ∅`): `a = [d.0.s_C.1]`
  - *Subsequent emission* (predicate: `{a' ∈ dom(C) : origin(a') = d} ≠ ∅`): `a = inc(a_prev, 0)` where `a_prev := max{a' ∈ dom(C) : origin(a') = d}`
- `v ∈ Val` (well-formed content value)

*Effect:* `C' = C ∪ {a ↦ v}`

*Frame:* `L' = L; dom(M') = dom(M); (A d' ∈ dom(M) :: M'(d') = M(d'))`

## K.λ — LinkAllocation (OP, operation)

Extends `dom(L)` with a fresh link address scoped to an allocated document.

*Precondition:*
- `d ∈ dom(M)` (home document exists)
- `ℓ ∉ dom(L) ∪ dom(C)` (fresh address — L14)
- `zeros(ℓ) = 3 ∧ E(ℓ)₁ = s_L` (element-level, link subspace — L0, L1)
- `#E(ℓ) ≥ 2` (L1b)
- `origin(ℓ) = d` (scoped to home document — L1a)
- `ℓ` is produced by `d`'s link sub-allocator `A_L(d)`:
  - *First emission* (predicate: `{ℓ' ∈ dom(L) : origin(ℓ') = d} = ∅`): `ℓ = [d.0.s_L.1]`
  - *Subsequent emission* (predicate: `{ℓ' ∈ dom(L) : origin(ℓ') = d} ≠ ∅`): `ℓ = inc(ℓ_prev, 0)` where `ℓ_prev := max{ℓ' ∈ dom(L) : origin(ℓ') = d}`
- `N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅` (well-formed link value with mandatory non-empty type endset at slot 3 — L3)

*Effect:* `L' = L ∪ {ℓ ↦ (e₁, …, eₙ)}`

*Frame:* `C' = C; dom(M') = dom(M); (A d' ∈ dom(M) :: M'(d') = M(d'))`
