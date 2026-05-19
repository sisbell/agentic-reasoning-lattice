# ASN-0093 Claim Statements

*Source: ASN-0093-allocation-substrate.md (revised unknown) — Extracted: 2026-05-18*

## Definition — StateModel

The substrate-level state is **Σ = (C, L, M)** where:
- `C : T ⇀ Val` is the content store: a partial function from element-level tumblers to content values
- `L : T ⇀ Link` is the link store: a partial function from element-level tumblers to triples `(F, G, Θ) ∈ Endset × Endset × Endset`
- `M : T ⇀ (T ⇀ T)` is the arrangement function: a partial function whose domain `dom(M)` is the set of allocated document addresses

The initial state is `Σ₀ = (∅, ∅, ∅)`.

## Definition — ValidAddressIdentification

Throughout this substrate, `ValidAddress(d) ≡ d satisfies T4 (HierarchicalParsing, ASN-0034)`. T4's four conjuncts are: `zeros(d) ≤ 3`, no adjacent zero components, `d[1] ≠ 0`, and `d[#d] ≠ 0`.

## Definition — ContentAnchor

For each `d ∈ dom(M)`:

`b_C(d) := [d.0.s_C]` — the **content sub-allocator anchor** (one-component element field with `E₁ = s_C`, `zeros = 3`, `#E = 1`)

`b_C(d) = inc(d, 2)` (TA5(d), `k = 2`). The anchor is not in `dom(C) ∪ dom(L)` — content addresses have `#E ≥ 2` and the anchor has `#E = 1`.

## Definition — LinkAnchor

For each `d ∈ dom(M)`:

`b_L(d) := [d.0.s_L]` — the **link sub-allocator anchor** (one-component element field with `E₁ = s_L`, `zeros = 3`, `#E = 1`)

`b_L(d) = inc(b_C(d), 0)` (TA5(c)). The anchor is not in `dom(C) ∪ dom(L)` — link addresses have `#E ≥ 2` and the anchor has `#E = 1`.

## Definition — ActiveSubAllocatorChain

A sub-allocator chain `A_C(d)` (resp. `A_L(d)`) is *active at state* `Σ` iff `d ∈ dom(M)` at `Σ`. "Active" is the predicate under which K.α (resp. K.λ) admits the chain as the emission source for an address with `origin(·) = d`: the operation's precondition requires `d ∈ dom(M)`, which is exactly the activation condition.

---

## M0 — DocumentTumblerWellFormed (INV, predicate)

`(A d ∈ dom(M) :: ValidAddress(d) ∧ zeros(d) = 2)`

Every allocated document address is a T4-valid tumbler with exactly two zero components.

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

Every content address `a ∈ dom(C)` has a structural inc-chain from its home document to `a`: a finite sequence `(t₀, t₁, …, tₙ)` with `t₀ = origin(a)` and `tₙ = a`, where each step `tᵢ = inc(tᵢ₋₁, kᵢ)` with `kᵢ ∈ {0, 1, 2}` satisfies T10a's per-step admissibility constraints.

The bootstrap gap (no T10a-tracked allocator domain for the anchor traversal and first emission) is closed by SubAllocatorAxiom.FirstEmission for the content sub-allocator chain; subsequent emissions inherit T10a.7 (EnumerationInjectivity) via SubAllocatorAxiom.ChainDiscipline.

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

Every link address `ℓ ∈ dom(L)` has a *structural inc-chain* from its home document to `ℓ`: a finite sequence `(t₀, t₁, …, tₙ)` with `t₀ = origin(ℓ)` and `tₙ = ℓ`, where each step `tᵢ = inc(tᵢ₋₁, kᵢ)` with `kᵢ ∈ {0, 1, 2}` satisfies T10a's per-step admissibility constraints (T4-validity preservation, zero-count side conditions).

The substrate states L1c in its per-step inc-rule form — not as the stronger "every intermediate `tᵢ` inhabits a T10a-tracked allocator's domain at the state of emission." SubAllocatorAxiom.FirstEmission closes the bootstrap gap by licensing the first emission directly, and SubAllocatorAxiom.ChainDiscipline carries subsequent emissions onto the sub-allocator's `inc(·, 0)` chain.

## L3 — TripleEndsetStructure (INV, predicate)

`(A a ∈ dom(L) :: L(a) = (F, G, Θ) where F, G, Θ ∈ Endset ∧ Θ ≠ ∅)`

Every link in the link store has exactly three endsets, with the type endset non-empty.

## L12 — LinkImmutability (INV, predicate)

`(A Σ → Σ' : (A a : a ∈ dom(L) : a ∈ dom(L') ∧ L'(a) = L(a)))`

Once allocated, a link's address persists in `dom(L)` and its value is permanently fixed across all transitions.

## L14 — StoreDisjointness (INV, predicate)

`dom(C) ∩ dom(L) = ∅`

Derived from L0 + SC-NEQ + T7 (FirstElementFieldDistinction, ASN-0034): every content address has `E(·)₁ = s_C`, every link address has `E(·)₁ = s_L`, and `s_C ≠ s_L`, so the domains are disjoint.

## L-fin — LinkStoreFiniteness (INV, predicate)

`|dom(L)| < ∞`

The link store is finite at every reachable state.

---

## SubspaceConventionAxiom — FixedSubspaceIdentifiers (AXIOM, axiom)

`s_C = 1 ∧ s_L = 2`

The distinctness `s_C ≠ s_L` (abbreviated **SC-NEQ**) and the sibling relation `s_L = s_C + 1` are immediate consequences. SC-NEQ underwrites L14 (StoreDisjointness) and the L0 partition; the sibling relation underwrites the L1c chain exhibition's step `inc(b_C(d), 0) = b_L(d)`.

## SequentialTransitionAxiom — SequentialAtomicTransitions (AXIOM, axiom)

Transitions `Σ → Σ'` are atomic, uninterruptible, and totally ordered: each transition evaluates its precondition against `Σ` and commits its effect to `Σ'` in one indivisible step, with no intermediate state in which a transition has begun but not committed.

## SubAllocatorAxiom — ContentLinkSubAllocatorExistence (AXIOM, axiom)

For each `d ∈ dom(M)`, two sub-allocator chains are simultaneously activated under `d` at the moment of `d`'s registration into `dom(M)` (by `K.σ`). Four clauses, independently citable as discharge premises:

**(a) Existence (SubAllocatorAxiom.Exists).** For every `d ∈ dom(M)`, the content sub-allocator chain `A_C(d)` (anchored at `b_C(d)`) and the link sub-allocator chain `A_L(d)` (anchored at `b_L(d)`) are active. By M1 (ArrangementMonotonicity), once `d ∈ dom(M)` it remains so at every successor state, and the sub-allocator chains correspondingly remain active permanently.

**(b) Disjointness (SubAllocatorAxiom.Disjoint).** Addresses produced by `A_C(d)` satisfy `E(·)₁ = s_C`; addresses produced by `A_L(d)` satisfy `E(·)₁ = s_L`. No address is produced by both sub-allocator chains.

**(c) First-emission namespace property (SubAllocatorAxiom.FirstEmission).** The first emission of each sub-allocator chain carries a freshness commitment evaluated at the K.α (resp. K.λ) event that commits the address as the chain's first emission:
- *Content chain first-emit:* the first address `a` produced by `A_C(d)` satisfies `a ∉ dom(C) ∪ dom(L)` at the K.α event that emits `a`, with `E(a)₁ = s_C`, `origin(a) = d`, `#E(a) = 2`. Concretely: `a = [d.0.s_C.1]`.
- *Link chain first-emit:* the first address `ℓ` produced by `A_L(d)` satisfies `ℓ ∉ dom(L) ∪ dom(C)` at the K.λ event that emits `ℓ`, with `E(ℓ)₁ = s_L`, `origin(ℓ) = d`, `#E(ℓ) = 2`. Concretely: `ℓ = [d.0.s_L.1]`.

**(d) T10a-discipline-satisfying chains (SubAllocatorAxiom.ChainDiscipline).** From the first emission onward, `A_C(d)` and `A_L(d)` are T10a-discipline-satisfying chains: each is the `inc(·, 0)`-extension chain rooted at its first emission, and the elements of each chain inherit T10a.7 (EnumerationInjectivity — distinct chain indices produce distinct addresses), T10a.1 (UniformSiblingLength — all chain elements share the same length), and T10a.8 (UniformSiblingZeroCount — all chain elements share `zeros = 3` since the first emission has `zeros = 3` per FirstEmission). This clause does *not* claim that `A_C(d)` and `A_L(d)` are embedded in T10a's global allocator tree as standalone allocators with `(parent, spawnPt, spawnParam)` triples; it claims only that each chain's emissions satisfy the per-chain disciplines T10a guarantees for sibling streams.

---

## ChainPrefixExtension — ChainPrefixExtension (LEMMA, lemma)

At every reachable state `Σ`, every element of an active sub-allocator chain extends its anchor under the prefix relation:

`(A d ∈ dom(M), t ∈ A_C(d) :: b_C(d) ≼ t)`
`(A d ∈ dom(M), t ∈ A_L(d) :: b_L(d) ≼ t)`

## ChainMembershipForOrigin — ChainMembershipForOrigin (LEMMA, lemma)

At every reachable state `Σ`, every entry of `dom(C)` (resp. `dom(L)`) inhabits the content (resp. link) sub-allocator chain of its origin, and forms a *contiguous initial segment* of that chain. Letting `A_C(d) = (t_1, t_2, t_3, …)` denote the enumeration of `d`'s content sub-allocator chain (with `t_1` the first emission and `t_{n + 1} = inc(t_n, 0)`), and `A_L(d) = (s_1, s_2, s_3, …)` the analogous link chain:

- `(A d ∈ dom(M) :: (E m_d ≥ 0 :: dom(C) ∩ {a' ∈ T : origin(a') = d} = {t_1, …, t_{m_d}}))` (content contiguous prefix; `{t_1, …, t_0} = ∅` by convention)
- `(A d ∈ dom(M) :: (E n_d ≥ 0 :: dom(L) ∩ {ℓ' ∈ T : origin(ℓ') = d} = {s_1, …, s_{n_d}}))` (link contiguous prefix)

The weaker subset inclusion `dom(C) ∩ {a' : origin(a') = d} ⊆ A_C(d)` (and its link analogue) is the immediate corollary of the contiguous-prefix form.

## StoreT4Validity — StoreT4Validity (LEMMA, predicate)

At every reachable state `Σ`, every entry of `dom(C) ∪ dom(L)` is a T4-valid tumbler:

`(A a ∈ dom(C) :: ValidAddress(a))`
`(A ℓ ∈ dom(L) :: ValidAddress(ℓ))`

## Cross-doc disjointness — CrossDocumentDisjointness (LEMMA, lemma)

For any two distinct documents `d₁, d₂ ∈ dom(M)` with `d₁ ≠ d₂`, the link sub-allocator anchors `p₁ := b_L(d₁) = [d₁.0.s_L]` and `p₂ := b_L(d₂) = [d₂.0.s_L]` satisfy

`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`

so by T10 (PartitionIndependence, ASN-0034), every address extending `p₁` differs from every address extending `p₂`. The same lemma holds with `b_C` in place of `b_L` for content allocations.

---

## K.σ — DocumentRegistration (OP, operation)

Extends `dom(M)` by registering a new document address with an empty arrangement.

**Precondition:**
- `d ∉ dom(M)` (fresh document address)
- `ValidAddress(d) ∧ zeros(d) = 2` (T4-valid, document-level)

**Effect:** `dom(M') = dom(M) ∪ {d}`, with `M'(d) = ∅` and `M'(d') = M(d')` for every `d' ∈ dom(M)`.

**Frame:** `C' = C; L' = L`

Cross-store freshness is automatic from the substrate's invariants: C1 forces `zeros(a) = 3` for every `a ∈ dom(C)`, L1 forces `zeros(ℓ) = 3` for every `ℓ ∈ dom(L)`, and K.σ's precondition pins `zeros(d) = 2`. Since no address can simultaneously satisfy `zeros = 2` and `zeros = 3`, `d ∉ dom(C) ∪ dom(L)` is forced by the precondition list together with C1/L1.

## K.α — ContentAllocation (OP, operation)

Extends `dom(C)` with a fresh content address scoped to an allocated document.

**Precondition:**
- `d ∈ dom(M)` (home document exists)
- `a ∉ dom(C) ∪ dom(L)` (fresh address — L14)
- `zeros(a) = 3 ∧ E(a)₁ = s_C` (element-level, content subspace — C1, L0)
- `#E(a) ≥ 2` (C1b)
- `origin(a) = d` (scoped to home document — C2)
- `a` is produced by `d`'s content sub-allocator `A_C(d)`:
  - *First emission* (predicate: `{a' ∈ dom(C) : origin(a') = d} = ∅`): `a = [d.0.s_C.1]`.
  - *Subsequent emission* (predicate: `{a' ∈ dom(C) : origin(a') = d} ≠ ∅`): `a = inc(a_prev, 0)` where `a_prev := max{a' ∈ dom(C) : origin(a') = d}`.
- `v ∈ Val` (well-formed content value)

**Effect:** `C' = C ∪ {a ↦ v}`

**Frame:** `L' = L; (A d' :: M'(d') = M(d'))`

## K.λ — LinkAllocation (OP, operation)

Extends `dom(L)` with a fresh link address scoped to an allocated document.

**Precondition:**
- `d ∈ dom(M)` (home document exists)
- `ℓ ∉ dom(L) ∪ dom(C)` (fresh address — L14)
- `zeros(ℓ) = 3 ∧ E(ℓ)₁ = s_L` (element-level, link subspace — L0, L1)
- `#E(ℓ) ≥ 2` (L1b)
- `origin(ℓ) = d` (scoped to home document — L1a)
- `ℓ` is produced by `d`'s link sub-allocator `A_L(d)`:
  - *First emission* (predicate: `{ℓ' ∈ dom(L) : origin(ℓ') = d} = ∅`): `ℓ = [d.0.s_L.1]`.
  - *Subsequent emission* (predicate: `{ℓ' ∈ dom(L) : origin(ℓ') = d} ≠ ∅`): `ℓ = inc(ℓ_prev, 0)` where `ℓ_prev := max{ℓ' ∈ dom(L) : origin(ℓ') = d}`.
- `(F, G, Θ) ∈ Endset × Endset × Endset ∧ Θ ≠ ∅` (well-formed link value with mandatory non-empty type endset — L3)

**Effect:** `L' = L ∪ {ℓ ↦ (F, G, Θ)}`

**Frame:** `C' = C; (A d' :: M'(d') = M(d'))`
