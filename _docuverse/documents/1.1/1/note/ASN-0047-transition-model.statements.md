# ASN-0047 Claim Statements

*Source: ASN-0047-transition-model.md (revised 2026-03-22) — Extracted: 2026-05-19*

## Definition — EntitySet

**Σ.E ⊆ T** — the set of allocated entity addresses. Every e ∈ E satisfies ValidAddress(e). Entities are organisational — not content; element-level addresses live in dom(C), not E:

`(A e ∈ E :: ¬IsElement(e))`

Equivalently, E ⊆ {t : ValidAddress(t) ∧ zeros(t) ≤ 2}.

*Stratification:* Σ.E partitions into:
- E_node = {e ∈ E : IsNode(e)}
- E_account = {e ∈ E : IsAccount(e)}
- E_doc = {e ∈ E : IsDocument(e)} — zeros = 2

## Definition — ProvenanceRelation

**Σ.R ⊆ T_elem × E_doc** — where T_elem = {a ∈ T : IsElement(a)}. The pair (a, d) ∈ R records that document d has, at some point in the system's history, contained I-address a in its arrangement.

## Definition — InitialState

Σ₀ = (C₀, L₀, E₀, M₀, R₀):
- C₀ = ∅
- L₀ = ∅
- E₀ = {n₀} where n₀ = `[1]` — canonical single-component bootstrap node; `zeros(n₀) = 0`, `IsNode(n₀)`, `ValidAddress(n₀)`
- M₀(d) = ∅ for all d
- R₀ = ∅

## Definition — ParentOf

For ¬IsNode(e), **parent(e)** using T4b's partial projections N, U, D, E:

- *Account case (IsAccount(e)):* `parent(e) = N(e)`. T4b parse: `e = N(e).0.U(e)`, `zeros(N(e)) = 0`, so `zeros(parent(e)) = 0 = zeros(e) − 1`.
- *Document case (IsDocument(e)):* `parent(e) = N(e).0.U(e)`. T4b parse: `e = N(e).0.U(e).0.D(e)`, `zeros(N(e).0.U(e)) = 1`, so `zeros(parent(e)) = 1 = zeros(e) − 1`.

In each case: `zeros(parent(e)) = zeros(e) − 1`.

## Definition — Endset

An *endset* is a finite set of well-formed spans: `Endset = 𝒫_fin(Span)`, where Span is the set of well-formed span pairs `(s, ℓ)` satisfying T12. The empty set ∅ ∈ Endset.

## Definition — LinkValue

A *link value* is a triple `(F, G, Θ)` where `F, G, Θ ∈ Endset` — the *from-endset*, *to-endset*, and *type-endset* respectively.

## Definition — SubAllocatorAnchors

For each `d ∈ E_doc`:
- `b_C(d) := [d.0.s_C]` — content sub-allocator anchor; `zeros = 3`, `#E = 1`; not in dom(C) ∪ dom(L)
- `b_L(d) := [d.0.s_L]` — link sub-allocator anchor; `zeros = 3`, `#E = 1`; not in dom(C) ∪ dom(L)

Under SubspaceConventionAxiom: `b_C(d) = inc(d, 2) = [d.0.1]`; `b_L(d) = inc(b_C(d), 0) = [d.0.2]`.

## Definition — CurrentContainment

`Contains(Σ) = {(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))}`

Derived quantity of state capturing what each document currently displays.

## Definition — ContentContainment

`Contains_C(Σ) = {(a, d) : d ∈ E_doc ∧ (E v : v ∈ dom(M(d)) ∧ subspace(v) = s_C : M(d)(v) = a)}`

## Definition — VOrderingOnSubspace

The *V-ordering on subspace S* is the restriction of T1 (LexicographicOrder) to the depth-m_S positive-component tuples whose first component is S — the standard lexicographic order on ℕ⁺-valued tuples of length m_S, scoped to the slice with `v_1 = S`.

## Definition — DomainProjections

`dom_C(M(d)) := V_{s_C}(d) := {v ∈ dom(M(d)) : subspace(v) = s_C}`

`dom_L(M(d)) := V_{s_L}(d) := {v ∈ dom(M(d)) : subspace(v) = s_L}`

---

## Σ.E — EntitySet (DEF, predicate)

`(A e ∈ E :: ¬IsElement(e))`

Equivalently, E ⊆ {t : ValidAddress(t) ∧ zeros(t) ≤ 2}.

## Σ.R — ProvenanceRelation (DEF, predicate)

**Σ.R ⊆ T_elem × E_doc** — where T_elem = {a ∈ T : IsElement(a)}. The pair (a, d) ∈ R records that document d has, at some point in the system's history, contained I-address a in its arrangement.

## Σ₀ — InitialState (DEF, function)

The initial state Σ₀ = (C₀, L₀, E₀, M₀, R₀):
- C₀ = ∅; L₀ = ∅; E₀ = {n₀} where n₀ = `[1]`; M₀(d) = ∅ for all d; R₀ = ∅

## parent(e) — ParentOf (DEF, function)

For ¬IsNode(e):
- IsAccount(e): `parent(e) = N(e)`
- IsDocument(e): `parent(e) = N(e).0.U(e)`

In each case `zeros(parent(e)) = zeros(e) − 1`.

## Contains(Σ) — CurrentContainment (DEF, function)

`Contains(Σ) = {(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))}`

## Contains_C(Σ) — ContentContainment (DEF, function)

`Contains_C(Σ) = {(a, d) : d ∈ E_doc ∧ (E v : v ∈ dom(M(d)) ∧ subspace(v) = s_C : M(d)(v) = a)}`

## Valid composite — ValidComposite (DEF, predicate)

A composite transition `Σ →* Σ'` is *valid* iff it is a finite sequence of atomic transitions Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ' satisfying two conditions:

(1) *Elementary preconditions:* each step Σᵢ → Σᵢ₊₁ satisfies the precondition of its elementary transition kind, evaluated at the intermediate state Σᵢ.

(2) *Coupling constraints:* J0, J1, and J1' hold for the composite — evaluated between the initial state Σ and the final state Σ'.

## K.α — ContentAllocation (TRANS, function)

*Precondition:* `d ∈ E_doc`; `a ∉ dom(C) ∪ dom(L)`; `zeros(a) = 3 ∧ E(a)₁ = s_C`; `#E(a) ≥ 2`; `origin(a) = d`.

- *First emission* (`{a' ∈ dom(C) : origin(a') = d} = ∅`): `a = [d.0.s_C.1]`
- *Subsequent emission* (`{a' ∈ dom(C) : origin(a') = d} ≠ ∅`): `a = inc(max{a' ∈ dom(C) : origin(a') = d}, 0)`

*Effect:* `C' = C ∪ {a ↦ v}`

*Frame:* `L' = L; E' = E; (A d :: M'(d) = M(d)); R' = R`

## K.δ — EntityCreation (TRANS, function)

*Effect:* `E' = E ∪ {e}` where `e ∉ E ∧ ValidAddress(e) ∧ ¬IsElement(e)`

*Precondition* splits on IsNode(e):

- **Case (i) IsNode(e):** `ValidAddress(e) ∧ IsNode(e) ∧ e ∉ E ∧ n₀ ≼ e` (discharged by NodeUniqueAllocation)
- **Case (ii) ¬IsNode(e):** `e = inc(t, k)` for `k ∈ {0, 1, 2}`; required uniformly: `parent(e) ∈ E`
  - *k = 0 (sibling):* `t ∈ E ∧ ¬IsNode(t) ∧ parent(t) = parent(e) ∧ zeros(t) = zeros(e) ∧ inc(t, 0) ∉ E`
  - *k = 1 (version):* `t ∈ E_doc`
  - *k = 2 (descent):* `t ∈ E ∧ parent(e) = t ∧ zeros(t) ≤ 1`

*Structural identities (consequences of TA5 + T4b):*
- `zeros(e) = zeros(t)` for k ∈ {0, 1}
- `zeros(e) = zeros(t) + 1` for k = 2
- `parent(e) = parent(t)` for k ∈ {0, 1}
- `parent(e) = t` for k = 2

*Effect on M (IsDocument case):* `M'(e) = ∅`; `(A d' : d' ≠ e : M'(d') = M(d'))`

*Frame:* `C' = C; L' = L; R' = R`

## K.μ⁺ — ArrangementExtension (TRANS, function)

*Effect:* `dom(M'(d)) ⊃ dom(M(d)) ∧ (A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))`

*Precondition:* `d ∈ E_doc`; for every new mapping M'(d)(v) = a, `a ∈ dom(C)` (S3); new V-positions satisfy S8a (all components strictly positive); resulting M'(d) satisfies S8-depth (uniform depth within each subspace); dom(M'(d)) finite (S8-fin); M'(d) satisfies D-CTG (contiguity) and D-MIN (minimum position).

*Amendment (ContentSubspaceRestriction):* new V-positions must satisfy `subspace(v) = s_C`.

*Frame:* `C' = C; L' = L; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R`

## K.μ⁻ — ArrangementContraction (TRANS, function)

*Effect:* `dom(M'(d)) ⊂ dom(M(d)) ∧ (A v : v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v))`

*Precondition:* `d ∈ E_doc`; contracted arrangement M'(d) satisfies S2, S3★, S8a, S8-depth, S8-fin, D-CTG★, D-MIN★ at the post-state.

*Per-subspace consequence:* `(E S ∈ {s_C, s_L} : V_S(d) ≠ ∅ : n'_S < n_S)` — at least one subspace shrinks strictly.

*Admissible contraction shape (derived):* For each subspace S with D-SEQ★-shaped pre-state `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}`, the post-state takes: `V_S(d') = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}` for some `0 ≤ n'_S ≤ n_S`.

*Frame:* `C' = C; L' = L; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d'))`

## K.μ~ — ArrangementReordering (TRANS, function)

Named composite K.μ⁻ + K.μ⁺ (not a primitive transition). *Precondition:* `d ∈ E_doc`; `|dom_C(M(d))| ≥ 2`.

*Bijection equation:* `(E π : π is a bijection dom(M(d)) → dom(M'(d)) : (A v ∈ dom(M(d)) :: M'(d)(π(v)) = M(d)(v)))`

π is admissible iff: (i) every `π(v)` satisfies S8a; (ii) induced M'(d) satisfies S8-depth, D-CTG★, D-MIN★, S3★; (iii) `π ≠ id`.

*Subspace preservation (derived):* `(A v ∈ dom(M(d)) :: subspace(π(v)) = subspace(v))`

*Link-subspace fixity (derived):* `π(v) = v` for every `v ∈ dom_L(M(d))`

*Frame (derived):* `C' = C; L' = L; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d'))`

## K.λ — LinkAllocation (TRANS, function)

*Precondition:* `d ∈ E_doc`; `ℓ ∉ dom(L) ∪ dom(C)`; `zeros(ℓ) = 3 ∧ E(ℓ)₁ = s_L`; `#E(ℓ) ≥ 2`; `origin(ℓ) = d`; `(F, G, Θ) ∈ Link ∧ Θ ≠ ∅`.

- *First emission* (`{ℓ' ∈ dom(L) : origin(ℓ') = d} = ∅`): `ℓ = [d.0.s_L.1]`
- *Subsequent emission:* `ℓ = inc(max{ℓ' ∈ dom(L) : origin(ℓ') = d}, 0)`

*Effect:* `L' = L ∪ {ℓ ↦ (F, G, Θ)}`

*Frame:* `C' = C; E' = E; (A d' :: M'(d') = M(d')); R' = R`

## K.ρ — ProvenanceRecording (TRANS, function)

*Effect:* `R' = R ∪ {(a, d)}` where `a ∈ dom(C) ∧ d ∈ E_doc`

*Precondition:* `a ∈ dom(C)` ∧ `d ∈ E_doc`. The level constraint IsElement(a) follows from S7b.

*Frame:* `C' = C; L' = L; E' = E; (A d :: M'(d) = M(d))`

## K.μ⁺_L — LinkSubspaceExtension (TRANS, function)

*Precondition:*
- `d ∈ E_doc`
- `ℓ ∈ dom(L)`
- `origin(ℓ) = d`
- `ℓ ∉ ran(M(d))`
- V-position v_ℓ satisfies: `subspace(v_ℓ) = s_L`; `#v_ℓ = m_L = 2`
  - If `V_{s_L}(d) = ∅`: `v_ℓ = [s_L, 1, ..., 1]` of depth m_L (D-MIN★)
  - If `V_{s_L}(d) ≠ ∅`: `v_ℓ = shift(max(V_{s_L}(d)), 1)` (D-CTG★)

*Effect:* `M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}`

*Frame:* `C' = C; L' = L; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R`

## K.μ~-FIX — DomainFixity (LEMMA, predicate)

`dom(M'(d)) = dom(M(d))`

D-SEQ★ at pre- and post-states gives `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` and `V_S(d') = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}`; since π is a bijection preserving subspaces, `n'_S = n_S` and `V_S(d') = V_S(d)`.

## J0 — AllocationRequiresPlacement (COUPLING, predicate)

`(A Σ →* Σ', a : a ∈ dom(C') \ dom(C) : (E d, v : d ∈ E'_doc ∧ v ∈ dom(M'(d)) : M'(d)(v) = a))`

Every freshly allocated I-address appears in some arrangement in the post-state.

## J1 — ExtensionRecordsProvenance (COUPLING, predicate)

`(A Σ →* Σ', d ∈ E'_doc, a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R')`

When (a, d) ∈ R already — from a prior insertion-deletion cycle — K.μ⁺ re-introducing a into d's arrangement requires no new K.ρ, because J1's requirement (a, d) ∈ R' is satisfied by existing membership.

## J1' — ProvenanceRequiresExtension (COUPLING, predicate)

`(A Σ →* Σ', a, d ∈ E'_doc : (a, d) ∈ R' \ R : a ∈ ran(M'(d)) \ ran(M(d)))`

Every new provenance entry corresponds to an actual containment event.

## J2 — ContractionIsolation (INV, predicate)

`C' = C ∧ L' = L ∧ E' = E ∧ R' = R`

K.μ⁻ requires no coupling. The L' = L conjunct extends the original J2 frame with the link store.

## J3 — ReorderingIsolation (INV, predicate)

`C' = C ∧ L' = L ∧ E' = E ∧ R' = R`

K.μ~ requires no coupling. Reordering preserves ran(M(d)), so Contains(Σ') = Contains(Σ). The L' = L conjunct extends the original J3 frame.

## J4 — ForkComposite (DEF, function)

A *fork* of d_src to d_new is a composite transition `Σ →* Σ'`, with *precondition* `d_src ∈ E_doc ∧ V_{s_C}(d_src) ≠ ∅`, consisting of:

(i) K.δ case (ii) with k = 1 and t = d_src, producing `d_new = inc(d_src, 1)` with `d_new ∉ E_doc`

(ii) K.μ⁺ populating M'(d_new) from d_src's content subspace under transclusion: `ran(M'(d_new)) ⊆ ran(M(d_src)|_{V_{s_C}(d_src)})`

(iii) K.ρ recording provenance for each `a ∈ ran(M'(d_new))`

and no other elementary steps.

Since none of K.δ, K.μ⁺, K.ρ modify C: `dom(C') = dom(C)`.

## P1 — EntityPermanence (INV, predicate)

`(A Σ → Σ' :: E ⊆ E')`

Uniform across levels:
- `[e ∈ E ∧ IsNode(e) ⟹ e ∈ E']`
- `[e ∈ E ∧ IsAccount(e) ⟹ e ∈ E']`
- `[e ∈ E ∧ IsDocument(e) ⟹ e ∈ E']`

## P2 — ProvenancePermanence (INV, predicate)

`(A Σ → Σ' :: R ⊆ R')`

Once the system records that d referenced a, that record persists.

## P4 — ProvenanceBounds (INV, predicate)

`Contains(Σ) ⊆ R`

In any reachable state where J1 has been satisfied for all prior transitions.

## P4a — HistoricalFidelity (INV, predicate)

`(A (a, d) ∈ R :: (E Σ_k in the transition history : (E v ∈ dom(M_k(d)) : subspace(v) = s_C ∧ M_k(d)(v) = a)))`

Every entry in R reflects an actual past content-subspace containment event.

## P6 — ExistentialCoherence (INV, predicate)

`(A a ∈ dom(C) :: origin(a) ∈ E_doc)`

## P7 — ProvenanceGrounding (INV, predicate)

`(A (a, d) ∈ R :: a ∈ dom(C))`

## P7a — ProvenanceCoverage (INV, predicate)

`(A a ∈ dom(C) :: (E d :: (a, d) ∈ R))`

## P8 — EntityHierarchy (INV, predicate)

`(A e ∈ E : ¬IsNode(e) : parent(e) ∈ E)`

## LinkVPositionDepthAxiom — LinkVPositionDepth (AX, axiom)

`(A d ∈ E_doc :: m_L = 2)`

Every link-subspace V-position has depth 2.

## NodeUniqueAllocation — NodeUniqueAllocation (AX, axiom)

Every K.δ node-allocation event — every elementary transition of K.δ whose effect places an entity `e` with `IsNode(e)` into E — produces an address satisfying three conditions:

(a) *Freshness:* `e ∉ Σ.E` at the state Σ of allocation

(b) *Bootstrap lineage:* `n₀ ≼ e` under the tumbler-prefix order

(c) *Registry tracking:* for every reachable state Σ and every `t ∈ Σ.E_node`, `t` inhabits the external node-allocation registry's tracked domain

## NodeRegistryBootstrap — NodeRegistryBootstrap (AX, axiom)

At the initial state `Σ₀`, `n₀` is committed to the node-allocation protocol's tracked domain. The node-allocation registry is external to Σ; `n₀` enters at `Σ₀` rather than via a prior K.δ event.

## NodeLineage — NodeLineage (INV, predicate)

`(A e ∈ E : IsNode(e) : n₀ ≼ e)`

where `≼` is the prefix order on tumblers.

## GlobalLineage — GlobalLineage (LEMMA, predicate)

`(A x ∈ E ∪ dom(C) ∪ dom(L) :: n₀ ≼ x)`

Every entity, content address, and link address descends structurally from the bootstrap node n₀. Derived via:
- Entities: NodeLineage + P8 + transitivity of ≼ (parent chain terminates at a node in at most 2 steps)
- Content addresses: P6 gives `origin(a) ∈ E_doc ⊆ E`; S7a gives `origin(a) ≼ a`; transitivity
- Link addresses: L1a gives `origin(ℓ) ∈ E_doc ⊆ E`; L1c gives `origin(ℓ) ≼ ℓ` via structural inc-chain; transitivity

## b_C(d), b_L(d) — SubAllocatorAnchors (DEF, function)

Virtual sub-allocator anchors under d:
- `b_C(d) = [d.0.s_C]` — single-component element-field base, not in dom(C) ∪ dom(L)
- `b_L(d) = [d.0.s_L]` — single-component element-field base, not in dom(C) ∪ dom(L)

## Allocator hierarchy — AllocatorHierarchy (DEF, predicate)

For each `d ∈ E_doc`, three T10a sub-allocators:
- `A_C(d)` — content sub-allocator, anchor `b_C(d) = [d.0.s_C]`; outputs satisfy `a ∈ dom(C)`, `subspace_I(a) = s_C`, `origin(a) = d`, `zeros(a) = 3`
- `A_L(d)` — link sub-allocator, anchor `b_L(d) = [d.0.s_L]`; outputs satisfy `ℓ ∈ dom(L)`, `subspace_I(ℓ) = s_L`, `origin(ℓ) = d`, `zeros(ℓ) = 3`
- `A_v(d)` — version sub-allocator; outputs enter E_doc at zeros = 2

Cross-document disjointness by T10a.{2,5} → T10 applied at anchor pairs; cross-subspace disjointness by L14 + SC-NEQ + T7.

## S3★-aux — SubspaceExhaustiveness (INV, predicate)

`(A d, v : v ∈ dom(M(d)) : subspace(v) = s_C ∨ subspace(v) = s_L)`

In every reachable state, all V-positions have subspace s_C or s_L.

## CL-OWN — LinkSubspaceOwnership (INV, predicate)

`(A d, v : v ∈ dom(M(d)) ∧ subspace(v) = s_L : origin(M(d)(v)) = d)`

Every document's link-subspace arrangement contains only its own links.

## CL-UNIQ — LinkSubspacePositionUniqueness (INV, predicate)

`(A d, v₁, v₂ : v₁ ∈ dom(M(d)) ∧ v₂ ∈ dom(M(d)) ∧ subspace(v₁) = s_L ∧ subspace(v₂) = s_L ∧ M(d)(v₁) = M(d)(v₂) : v₁ = v₂)`

Equivalently, `M(d)|_{dom_L}` is a partial injection from V-positions to link addresses.

## SequentialTransitionAxiom — SequentialAtomicTransitions (AX, axiom)

The transition relation `Σ → Σ'` is single-event sequential: each transition is an atomic, uninterruptible event in which the elementary precondition is evaluated against `Σ` and the elementary effect is committed to `Σ'` in one indivisible step, and transitions are totally ordered (no two transitions overlap in time). Equivalently, the system admits no intermediate state in which a transition has begun but not yet committed.

## SubspaceConventionAxiom — FixedSubspaceIdentifiers (AX, axiom)

`s_C = 1 ∧ s_L = 2`

The distinctness consequence `s_C ≠ s_L` is abbreviated **SC-NEQ**.

## SubAllocatorAxiom — ContentLinkSubAllocatorExistence (AX, axiom)

For each `d ∈ E_doc`, the entity-allocation event placing d into E_doc activates a content sub-allocator `A_C(d)` with anchor `b_C(d) = [d.0.s_C]` and a link sub-allocator `A_L(d)` with anchor `b_L(d) = [d.0.s_L]`.

Five sub-clauses:
- **SubAllocatorAxiom.Subspace:** Every `a` emitted by `A_C(d)` has `subspace_I(a) = s_C`; every `ℓ` emitted by `A_L(d)` has `subspace_I(ℓ) = s_L`.
- **SubAllocatorAxiom.FirstEmission:** First emission of each is `[d.0.s_C.1]` resp. `[d.0.s_L.1]`, satisfying `a ∉ dom(Σ.C) ∪ dom(Σ.L)` at the state of allocation, with `origin(a) = d` and `#E(a) = 2`.
- **SubAllocatorAxiom.Namespace:** Every output is T4-valid with `zeros(·) = 3`.
- **SubAllocatorAxiom.T10aConformance:** `A_C(d)` and `A_L(d)` are T10a-conforming allocators within d's allocator subtree; the K.δ event for d is the joint T2-spawn step activating both sub-allocators.
- **SubAllocatorAxiom.Disjointness:** `dom(A_C(d)) ∩ dom(A_L(d)) = ∅`; for d ≠ d', `dom(A_C(d)) ∩ dom(A_C(d')) = ∅`, `dom(A_L(d)) ∩ dom(A_L(d')) = ∅`, `dom(A_C(d)) ∩ dom(A_L(d')) = ∅`.

## L0 — SubspacePartition (INV, predicate)

`(A a ∈ dom(Σ.L) :: subspace_I(a) = s_L)`

`(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)`

## P0 — ContentPermanence (INV, predicate)

`(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ (A a : a ∈ dom(C) : C'(a) = C(a)))`

C is *append-only with immutable values*. Subsumes ASN-0036's S0 and S1.

## L3 — TripleEndsetStructure (INV, predicate)

`(A a ∈ dom(Σ.L) :: Σ.L(a) = (F, G, Θ) where F, G, Θ ∈ Endset ∧ Θ ≠ ∅)`

Every link has exactly three endsets, with the type endset non-empty. (L3 admits `F = ∅` and `G = ∅` independently — only Θ is required non-empty.)

## L14 — StoreDisjointness (INV, predicate)

`dom(Σ.C) ∩ dom(Σ.L) = ∅`

Derived from L0 and SC-NEQ via T7: if `a ∈ dom(C)` then `subspace_I(a) = s_C`, and if `a ∈ dom(L)` then `subspace_I(a) = s_L`; since `s_C ≠ s_L`, no address inhabits both domains.

## L14a — NonTranscludability (INV, predicate)

Superseded by S3★ + CL-OWN in the extended state: S3★ routes every link-subspace V→I mapping to dom(L), and CL-OWN forces home-document ownership at each such mapping.

## L1c — LinkAllocatorConformance (INV, predicate)

Every `ℓ ∈ dom(L)` is reachable from a T4-valid document-level seed `s` (`zeros(s) = 2`) by a *structural inc-chain* satisfying:
- Each step `tᵢ = inc(tᵢ₋₁, kᵢ)` with `kᵢ ∈ {0, 1, 2}` satisfying TA5's structural preconditions (operand T4-validity, zeros bound at k = 2)
- Length monotonicity: `#tᵢ > #s`

(Per-step inc-rule conformance only — *not* full T10a discipline including allocator-frontier domain tracking.)

## S3★ — GeneralizedReferentialIntegrity (INV, predicate)

`(A d, v : v ∈ dom(Σ.M(d)) : (subspace(v) = s_C ⟹ Σ.M(d)(v) ∈ dom(Σ.C)) ∧ (subspace(v) = s_L ⟹ Σ.M(d)(v) ∈ dom(Σ.L)))`

where `subspace(v)` denotes the first component of the V-position. Supersedes S3 (ASN-0036) for the extended state.

## D-CTG★ — PerSubspaceContiguity (INV, predicate)

`(A d, S : V_S(d) ≠ ∅ : V_S(d) is contiguous under the V-ordering on subspace S)`

where *contiguous* unpacks as: for every `v_lo, v_hi ∈ V_S(d)` and every depth-m_S positive tuple `z` with subspace identifier S and `v_lo ≤ z ≤ v_hi` under the V-ordering, `z ∈ V_S(d)`.

## D-MIN★ — PerSubspaceMinimumPosition (INV, predicate)

`(A d, S : V_S(d) ≠ ∅ : min(V_S(d)) = [S, 1, ..., 1] of depth m_S)`

## D-SEQ★ — PerSubspaceSequentialPositions (LEMMA, predicate)

For each non-empty subspace S in M(d):

`V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` for some `n_S ≥ 1`

where the inner positions are of uniform depth m_S (common depth within subspace S, by S8-depth), and `n_S = |V_S(d)|`. Derived from D-CTG★ + D-MIN★ + S8-depth + S8-fin + S8a.

## P3 — ArrangementMutabilityOnly (INV, predicate)

`(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ dom(L) ⊆ dom(L') ∧ E ⊆ E' ∧ R ⊆ R' ∧ (A a ∈ dom(C) :: C'(a) = C(a)) ∧ (A ℓ ∈ dom(L) :: L'(ℓ) = L(ℓ)))`

The only component that can lose information is M.

## P4★ — ProvenanceBoundsContentSubspace (INV, predicate)

`Contains_C(Σ) ⊆ R`

Supersedes P4 for the extended state. In pre-extension states (no link-subspace mappings), `Contains_C(Σ) = Contains(Σ)`, so P4★ reduces to P4.

## J1★ — ExtensionRecordsProvenanceContentSubspace (COUPLING, predicate)

`(A Σ →* Σ', d ∈ E'_doc, a : (E v ∈ dom(M'(d)) : subspace(v) = s_C ∧ M'(d)(v) = a) ∧ ¬(E v ∈ dom(M(d)) : subspace(v) = s_C ∧ M(d)(v) = a) : (a, d) ∈ R')`

Range-based: triggers whenever an I-address `a` is new to the content-subspace range of M'(d). Supersedes J1 in the extended state.

## J1'★ — ProvenanceRequiresExtensionContentSubspace (COUPLING, predicate)

`(A Σ →* Σ', a, d : (a, d) ∈ R' \ R : (E v ∈ dom(M'(d)) : subspace(v) = s_C ∧ M'(d)(v) = a) ∧ ¬(E v ∈ dom(M(d)) : subspace(v) = s_C ∧ M(d)(v) = a))`

Supersedes J1' in the extended state.

## ValidComposite★ — ValidCompositeExtended (DEF, predicate)

A composite transition `Σ →* Σ'` in the extended state Σ = (C, L, E, M, R) is *valid* iff it is a finite sequence of atomic transitions `Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ'` — drawn from K.α (amended), K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻ (amended), K.μ~, and K.ρ — satisfying:

1. *Transition preconditions (intra-composite sequencing):* Each step `Σᵢ → Σᵢ₊₁` satisfies the elementary precondition of its transition kind, evaluated at the intermediate state `Σᵢ`. K.μ~ is shorthand for its K.μ⁻ + K.μ⁺ decomposition; `|dom_C(M(d))| ≥ 2` is its necessary-and-sufficient existence condition for clause `π ≠ id`.

2. *Coupling constraints (initial-to-final):* J0, J1★, and J1'★ hold for the composite as a whole — evaluated *only* between the initial state Σ and the final state Σ'.

## S8★ — PerSubspaceSpanDecomposition (INV, predicate)

For each `d ∈ E_doc` and each subspace `S ∈ {s_C, s_L}`, the per-subspace arrangement `M(d)|_{V_S(d)}` decomposes into a finite set of correspondence runs `{(v_j, a_j, n_j)}` satisfying ASN-0036's S8 conditions (a) and (b) applied to the projected arrangement:

- *Content subspace:* `M(d)|_{V_{s_C}(d)} : V_{s_C}(d) → dom(C)` — direct application of ASN-0036's S8.
- *Link subspace:* `M(d)|_{V_{s_L}(d)} : V_{s_L}(d) → dom(L)` — by the trivial length-1 decomposition `{(v, M(d)(v), 1) : v ∈ V_{s_L}(d)}`: every link-subspace V-position constitutes its own length-1 correspondence run.

## ExtendedReachableStateInvariants — ExtendedReachableStateInvariants (INV, predicate)

Every state reachable from Σ₀ by a finite sequence of valid composite transitions satisfies the *per-state invariants* (preserved by each elementary transition):

S2 ∧ S3★ ∧ S3★-aux ∧ S4 ∧ S7a ∧ S7b ∧ S7c ∧ S7d ∧ S8a ∧ S8-fin ∧ S8-depth ∧ S8★ ∧ D-CTG★ ∧ D-MIN★ ∧ D-SEQ★ ∧ P6 ∧ P7 ∧ P8 ∧ NodeLineage ∧ L0 ∧ L1 ∧ L1a ∧ L1b ∧ L1c ∧ L3 ∧ L14 ∧ L-fin ∧ CL-OWN ∧ CL-UNIQ

Every state at a composite boundary additionally satisfies the *composite-boundary properties* (discharged at boundaries by J0/J1★/J1'★, may transiently fail at intermediate states):

P4★ ∧ P4a ∧ P7a

## ExtendedTransitionInvariants — ExtendedTransitionInvariants (INV, predicate)

Every valid composite transition Σ →* Σ' satisfies P3, the conjunction:

P0 ∧ P1 ∧ P2 ∧ L12

(which subsumes ASN-0036's S0 and S1 via P0 and extends ASN-0043's L12). S9 follows from P0.

## K.α's E(a)₁ = s_C precondition — ContentSubspacePrecondition (INV, requires)

Inherited from ASN-0093's K.α directly. The precondition `E(a)₁ = s_C` (equivalently `subspace_I(a) = s_C`) is part of ASN-0093's K.α precondition; downstream sites in this ASN cite it as **K.α's content-subspace precondition**, explicitly attributing it to ASN-0093.

## K.μ⁺ amendment — ContentSubspaceRestriction (INV, requires)

K.μ⁺ is amended with a content-subspace restriction: new V-positions must satisfy `subspace(v) = s_C`.

This complements K.μ⁺_L (which handles link-subspace extensions exclusively). Without it, K.μ⁺ could create a link-subspace V-position mapping to dom(C), violating S3★.

*Frame (extended state):* `C' = C; L' = L; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R`

## K.μ⁻ (per-subspace scope) — PerSubspaceScope (INV, requires)

K.μ⁻'s D-CTG★/D-MIN★ postconditions apply *per-subspace* under the D-SEQ★ enumeration `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}`. Valid contractions per-subspace are suffix removals (empty, proper, or full), forced by D-CTG★ + D-MIN★ + D-SEQ★ at the post-state.

*Per-subspace consequence:* `(E S ∈ {s_C, s_L} : V_S(d) ≠ ∅ : n'_S < n_S)` — at least one subspace shrinks strictly.

*Frame (extended state):* `C' = C; L' = L; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d'))`
