# ASN-0047 Formal Statements

*Source: ASN-0047-state-transitions.md (revised 2026-03-22) — Extracted: 2026-03-22*

## Definition — EntitySet

**Σ.E ⊆ T** — the set of allocated entity addresses. Every e ∈ E satisfies ValidAddress(e). Membership constraint: `(A e ∈ E :: ¬IsElement(e))`. Equivalently, E ⊆ {t : ValidAddress(t) ∧ zeros(t) ≤ 2}.

Partition:
- E_node = {e ∈ E : IsNode(e)}
- E_account = {e ∈ E : IsAccount(e)}
- E_doc = {e ∈ E : IsDocument(e)}

---

## Definition — ProvenanceRelation

**Σ.R ⊆ T_elem × E_doc** where T_elem = {a ∈ T : IsElement(a)}. The pair (a, d) ∈ R records that document d has, at some point in the system's history, contained I-address a in its arrangement.

---

## Definition — LinkStore

**Σ.L : T ⇀ Link** — link store, partial function from link addresses to link values.

Extended system state: **Σ = (C, L, E, M, R)**, where L : T ⇀ Link is the link store.

---

## Definition — Endset

An *endset* is a finite set of well-formed spans: `Endset = 𝒫_fin(Span)`, where `Span` is the set of well-formed span pairs `(s, ℓ)` satisfying T12 (ASN-0034). The empty set ∅ is a valid endset.

---

## Definition — LinkValue

A *link value* is a triple `(F, G, Θ)` where `F, G, Θ ∈ Endset` — the *from-endset*, *to-endset*, and *type-endset* respectively.

---

## Definition — SubspaceIdentifiers

We write `s_C` for the content subspace identifier and `s_L` for the link subspace identifier. These are the first components of the element field for content and link addresses respectively: `fields(a).E₁ = s_C` for content addresses, `fields(ℓ).E₁ = s_L` for link addresses. The same identifiers serve for V-positions: `subspace(v) = v₁`.

Derived: `s_C ≥ 1` and `s_L ≥ 1` (from L1, T4, S7b).

---

## Definition — ParentFunction

For non-node entity e (where ¬IsNode(e)): tumbler obtained by truncating the last field and its preceding zero separator. If IsAccount(e) with form N.0.U, then parent(e) = N. If IsDocument(e) with form N.0.U.0.D, then parent(e) = N.0.U. In each case parent(e) is a valid address at the next higher level: zeros(parent(e)) = zeros(e) − 1.

---

## Definition — InitialState

The initial state Σ₀ = (C₀, L₀, E₀, M₀, R₀) is:
- C₀ = ∅
- L₀ = ∅
- E₀ = {n₀} for a designated bootstrap node n₀ with IsNode(n₀)
- M₀(d) = ∅ for all d
- R₀ = ∅

---

## Definition — CurrentContainment

`Contains(Σ) = {(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))}`

---

## Definition — ContentContainment

`Contains_C(Σ) = {(a, d) : d ∈ E_doc ∧ (E v : v ∈ dom(M(d)) ∧ subspace(v) = s_C : M(d)(v) = a)}`

---

## Definition — ValidComposite

A composite transition Σ → Σ' is *valid* iff it is a finite sequence of elementary transitions Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ' satisfying two conditions:

(1) *Elementary preconditions:* each step Σᵢ → Σᵢ₊₁ satisfies the precondition of its elementary transition kind, evaluated at the intermediate state Σᵢ.

(2) *Coupling constraints:* J0, J1, and J1' hold for the composite — evaluated between the initial state Σ and the final state Σ'.

---

## Definition — ValidCompositeExtended (ValidComposite★)

A composite transition Σ → Σ' in the extended state Σ = (C, L, E, M, R) is *valid* iff it is a finite sequence of transitions `Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ'` — drawn from K.α (amended), K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻ (amended), K.μ~, and K.ρ — satisfying:

1. *Transition preconditions:* each step `Σᵢ → Σᵢ₊₁` satisfies the precondition of its transition kind, evaluated at the intermediate state `Σᵢ`. K.μ~ appearing in the sequence is shorthand for its decomposition — when dom_C(M(d)) ≠ ∅ it expands into two consecutive elementary steps (K.μ⁻ + K.μ⁺), each satisfying its own precondition at the respective intermediate state; when dom_C(M(d)) = ∅, link-subspace fixity forces π = id and K.μ~ expands into zero elementary steps (M'(d) = M(d)).
2. *Coupling constraints:* J0, J1★, and J1'★ hold for the composite — evaluated between the initial state Σ and the final state Σ'.

---

## Definition — ForkComposite (J4)

A *fork* of d_src to d_new is a composite transition Σ → Σ', with *precondition* d_src ∈ E_doc ∧ V_{s_C}(d_src) ≠ ∅, consisting of:

(i) K.δ creating d_new with d_new ∉ E_doc,

(ii) K.μ⁺ populating M'(d_new) with ran(M'(d_new)) ⊆ ran(M(d_src)),

(iii) K.ρ recording provenance for each a ∈ ran(M'(d_new)),

and no other elementary steps.

Consequence: dom(C') = dom(C).

---

## SC-NEQ — SubspaceDistinctness (AX, axiom)

`s_C ≠ s_L`

---

## L0 — SubspacePartition (INV, predicate)

`(A a ∈ dom(Σ.L) :: fields(a).E₁ = s_L)`

`(A a ∈ dom(Σ.C) :: fields(a).E₁ = s_C)`

---

## L1 — LinkElementLevel (INV, predicate)

`(A a ∈ dom(Σ.L) :: zeros(a) = 3)`

---

## L1a — LinkScopedAllocation (INV, predicate)

`(A a ∈ dom(Σ.L) :: origin(a) ∈ E_doc)`

---

## L3 — TripleEndsetStructure (INV, predicate)

`(A a ∈ dom(Σ.L) :: Σ.L(a) = (F, G, Θ) where F, G, Θ ∈ Endset)`

---

## L12 — LinkImmutability (INV, predicate)

`(A Σ → Σ' : (A a : a ∈ dom(Σ.L) : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)))`

---

## L14 — StoreDisjointness (LEMMA, lemma)

`dom(Σ.C) ∩ dom(Σ.L) = ∅`

Derived from L0 and SC-NEQ via T7 (SubspaceDisjointness, ASN-0034).

---

## P0 — ContentPermanence (INV, predicate)

`(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ (A a : a ∈ dom(C) : C'(a) = C(a)))`

---

## P1 — EntityPermanence (INV, predicate)

`(A Σ → Σ' :: E ⊆ E')`

Per-level forms:
- `[e ∈ E ∧ IsNode(e) ⟹ e ∈ E']`
- `[e ∈ E ∧ IsAccount(e) ⟹ e ∈ E']`
- `[e ∈ E ∧ IsDocument(e) ⟹ e ∈ E']`

---

## P2 — ProvenancePermanence (INV, predicate)

`(A Σ → Σ' :: R ⊆ R')`

---

## P3 — ArrangementMutability (INV, predicate)

Arrangements admit three modes of change:

(a) *Extension*: new V→I mappings may be added to M(d).

(b) *Contraction*: existing V→I mappings may be removed from M(d).

(c) *Reordering*: V-positions of existing mappings may change while the multiset of referenced I-addresses is preserved.

No other component admits contraction or reordering. C, E, and R are all monotonic; only M can shrink.

---

## P3★ — ArrangementMutabilityOnlyExtended (INV, predicate)

`(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ dom(L) ⊆ dom(L') ∧ E ⊆ E' ∧ R ⊆ R')`

Including L12: `dom(L) ⊆ dom(L') ∧ (A ℓ ∈ dom(L) : L'(ℓ) = L(ℓ))`.

---

## P4 — ProvenanceBounds (INV, predicate)

`Contains(Σ) ⊆ R`

---

## P4★ — ProvenanceBoundsContent (INV, predicate)

`Contains_C(Σ) ⊆ R`

---

## P4a — HistoricalFidelity (INV, predicate)

`(A (a, d) ∈ R :: (E Σ_k in the transition history : a ∈ ran(M_k(d))))`

---

## P5 — DestructionConfinement (LEMMA, lemma)

For every state transition Σ → Σ':

(a) `dom(C') ⊇ dom(C) ∧ (A a : a ∈ dom(C) : C'(a) = C(a))`

(b) `E' ⊇ E`

(c) `R' ⊇ R`

---

## P5★ — DestructionConfinementExtended (LEMMA, lemma)

For every state transition Σ → Σ':

(a) `dom(C') ⊇ dom(C) ∧ (A a : a ∈ dom(C) : C'(a) = C(a))`

(b) `dom(L') ⊇ dom(L) ∧ (A ℓ : ℓ ∈ dom(L) : L'(ℓ) = L(ℓ))`

(c) `E' ⊇ E`

(d) `R' ⊇ R`

---

## P6 — ExistentialCoherence (INV, predicate)

`(A a ∈ dom(C) :: origin(a) ∈ E_doc)`

---

## P7 — ProvenanceGrounding (INV, predicate)

`(A (a, d) ∈ R :: a ∈ dom(C))`

---

## P7a — ProvenanceCoverage (INV, predicate)

`(A a ∈ dom(C) :: (E d :: (a, d) ∈ R))`

---

## P8 — EntityHierarchy (INV, predicate)

`(A e ∈ E : ¬IsNode(e) : parent(e) ∈ E)`

---

## S3★ — GeneralizedReferentialIntegrity (INV, predicate)

`(A d, v : v ∈ dom(Σ.M(d)) : (subspace(v) = s_C ⟹ Σ.M(d)(v) ∈ dom(Σ.C)) ∧ (subspace(v) = s_L ⟹ Σ.M(d)(v) ∈ dom(Σ.L)))`

where `subspace(v)` denotes the first component of the V-position.

---

## S3★-aux — SubspaceExhaustiveness (INV, predicate)

`(A d, v : v ∈ dom(M(d)) : subspace(v) = s_C ∨ subspace(v) = s_L)`

---

## CL-OWN — LinkSubspaceOwnership (INV, predicate)

`(A d, v : v ∈ dom(M(d)) ∧ subspace(v) = s_L : origin(M(d)(v)) = d)`

---

## K.α — ContentAllocation (TRANSITION, method)

*Effect:* `C' = C ∪ {a ↦ v}` where `a ∉ dom(C)`

*Precondition:* `IsElement(a) ∧ origin(a) ∈ E_doc`

*Frame:* `E' = E; (A d :: M'(d) = M(d)); R' = R`

---

## K.α amendment — ContentSubspaceRestriction (PRE, requires)

In the extended state, the allocated address must satisfy `fields(a).E₁ = s_C`.

---

## K.δ — EntityCreation (TRANSITION, method)

*Effect:* `E' = E ∪ {e}` where `e ∉ E ∧ ValidAddress(e) ∧ ¬IsElement(e)`

*Precondition:* when `¬IsNode(e)`, `parent(e) ∈ E`; for root nodes (`IsNode(e)`), no parent required.

When `IsDocument(e)`: `M'(e) = ∅` (empty arrangement).

*Frame:* `C' = C; (A d' :: M'(d') = M(d')); R' = R`

---

## K.μ⁺ — ArrangementExtension (TRANSITION, method)

*Effect:* `dom(M'(d)) ⊃ dom(M(d)) ∧ (A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))`

*Precondition:* `d ∈ E_doc`; for every new mapping `M'(d)(v) = a`, `a ∈ dom(C)`; new V-positions satisfy S8a; M'(d) satisfies S8-depth; `dom(M'(d))` is finite (S8-fin); M'(d) satisfies D-CTG and D-MIN.

*Frame:* `C' = C; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R`

---

## K.μ⁺ amendment — ContentSubspaceRestrictionOnExtension (PRE, requires)

New V-positions must satisfy `subspace(v) = s_C`.

---

## K.μ⁻ — ArrangementContraction (TRANSITION, method)

*Effect:* `dom(M'(d)) ⊂ dom(M(d)) ∧ (A v : v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v))`

*Precondition:* `d ∈ E_doc`.

*Postcondition:* M'(d) satisfies D-CTG and D-MIN. By D-SEQ, valid contractions are constrained to removal from the maximum end of V_S(d) or removal of all positions in V_S(d), for each subspace S.

*Frame:* `C' = C; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d'))`

---

## K.μ⁻ amendment — PerSubspaceContiguity (PRE, requires)

D-CTG and D-MIN postconditions extend to the two-subspace case: contraction must satisfy D-CTG and D-MIN for each subspace independently.

---

## K.μ~ — ArrangementReordering (TRANSITION, method)

*Effect:* For some `d ∈ E_doc`, there exists a bijection `π : dom(M(d)) → dom(M'(d))` such that:

`(A v : v ∈ dom(M(d)) : M'(d)(π(v)) = M(d)(v))`

Corollary: `ran(M'(d)) = ran(M(d))`.

*Precondition:* `d ∈ E_doc`; π produces V-positions satisfying S8a; M'(d) satisfies S8-depth, D-CTG, D-MIN.

*Frame (derived):* `C' = C; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d'))`

Distinguished composite: decomposes into K.μ⁻ followed by K.μ⁺ when `dom_C(M(d)) ≠ ∅`; zero elementary steps (π = id, M'(d) = M(d)) when `dom_C(M(d)) = ∅`.

---

## K.μ~-FIX — DomainFixityUnderReorder (LEMMA, lemma)

`dom(M'(d)) = dom(M(d))` — the bijection π is a permutation of a fixed domain.

Derived from D-SEQ + bijection cardinality + subspace preservation (link-subspace fixity): `|dom(M'(d))| = |dom(M(d))|`, and D-SEQ at both states yields `V_S(d') = V_S(d)` for each subspace S.

---

## K.ρ — ProvenanceRecording (TRANSITION, method)

*Effect:* `R' = R ∪ {(a, d)}` where `a ∈ dom(C) ∧ d ∈ E_doc`

*Precondition:* `a ∈ dom(C) ∧ d ∈ E_doc`. The level constraint `IsElement(a)` follows from S7b.

*Frame:* `C' = C; E' = E; (A d :: M'(d) = M(d))`

---

## K.λ — LinkAllocation (TRANSITION, method)

*Precondition:*
- `d ∈ E_doc`
- `ℓ ∉ dom(L) ∪ dom(C)`
- `zeros(ℓ) = 3 ∧ fields(ℓ).E₁ = s_L`
- `origin(ℓ) = d`
- `(A ℓ' : ℓ' ∈ dom(L) ∧ origin(ℓ') = d : ℓ' < ℓ)`
- `(F, G, Θ) ∈ Link`

*Effect:* `L' = L ∪ {ℓ ↦ (F, G, Θ)}`

*Frame:* `C' = C; E' = E; (A d' :: M'(d') = M(d')); R' = R`

---

## K.μ⁺_L — LinkSubspaceExtension (TRANSITION, method)

*Precondition:*
- `d ∈ E_doc`
- `ℓ ∈ dom(L)`
- `origin(ℓ) = d`
- V-position `v_ℓ` satisfies:
  - `subspace(v_ℓ) = s_L`
  - `m_L ≥ 2`, where: if `V_{s_L}(d) ≠ ∅`, `m_L` is the common depth of existing link-subspace V-positions (by S8-depth); if `V_{s_L}(d) = ∅`, `m_L` is a parameter subject only to `m_L ≥ 2`
  - If `V_{s_L}(d) = ∅`: `v_ℓ` is the minimum position `[s_L, 1, ..., 1]` of depth `m_L` (D-MIN)
  - If `V_{s_L}(d) ≠ ∅`: `v_ℓ = shift(max(V_{s_L}(d)), 1)` (D-CTG)
  - `#v_ℓ = m_L` (S8-depth)

*Effect:* `M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}`

*Frame:* `C' = C; L' = L; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R`

---

## J0 — AllocationRequiresPlacement (COUPLING, predicate)

`(A Σ → Σ', a : a ∈ dom(C') \ dom(C) : (E d, v : d ∈ E'_doc ∧ v ∈ dom(M'(d)) : M'(d)(v) = a))`

---

## J1 — ExtensionRecordsProvenance (COUPLING, predicate)

`(A Σ → Σ', d ∈ E'_doc, a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R')`

---

## J1' — ProvenanceRequiresExtension (COUPLING, predicate)

`(A Σ → Σ', a, d ∈ E'_doc : (a, d) ∈ R' \ R : a ∈ ran(M'(d)) \ ran(M(d)))`

---

## J1★ — ExtensionRecordsProvenanceContent (COUPLING, predicate)

`(A Σ → Σ', d ∈ E'_doc, a : (E v ∈ dom(M'(d)) : subspace(v) = s_C ∧ M'(d)(v) = a) ∧ ¬(E v ∈ dom(M(d)) : subspace(v) = s_C ∧ M(d)(v) = a) : (a, d) ∈ R')`

---

## J1'★ — ProvenanceRequiresExtensionContent (COUPLING, predicate)

`(A Σ → Σ', a, d : (a, d) ∈ R' \ R : (E v ∈ dom(M'(d)) : subspace(v) = s_C ∧ M'(d)(v) = a) ∧ ¬(E v ∈ dom(M(d)) : subspace(v) = s_C ∧ M(d)(v) = a))`

---

## J2 — ContractionIsolation (LEMMA, lemma)

K.μ⁻ as an elementary transition requires no coupling:

`C' = C ∧ E' = E ∧ R' = R`

Consequence: `Contains(Σ') ⊆ Contains(Σ) ⊆ R = R'`.

---

## J3 — ReorderingIsolation (LEMMA, lemma)

K.μ~ as a distinguished composite requires no coupling:

`C' = C ∧ E' = E ∧ R' = R`

Consequence: `ran(M'(d)) = ran(M(d))`, so `Contains(Σ') = Contains(Σ)`.

---

## ArrangementInvariantsLemma — ArrangementInvariantsLemma (LEMMA, lemma)

Every valid composite transition preserves S2, S3, S8a, S8-depth, S8-fin, D-CTG, and D-MIN.

Each elementary transition preserves these per-state properties: K.μ⁺ establishes them via its preconditions; K.μ⁻ preserves them by restriction and D-CTG/D-MIN postcondition; K.δ for documents produces the empty arrangement (vacuously satisfying all seven); all other transitions hold M in frame.

---

## ReachableStateInvariants — ReachableStateInvariants (THEOREM, lemma)

Every state reachable from Σ₀ by a finite sequence of valid composite transitions satisfies:

`P0 ∧ P1 ∧ P2 ∧ P4 ∧ P6 ∧ P7 ∧ P7a ∧ P8 ∧ S2 ∧ S3 ∧ S8a ∧ S8-depth ∧ S8-fin ∧ D-CTG ∧ D-MIN`

where P4 is `Contains(Σ) ⊆ R`.

---

## ExtendedReachableStateInvariants — ExtendedReachableStateInvariants (THEOREM, lemma)

Every state reachable from Σ₀ = (C₀, L₀, E₀, M₀, R₀) by a finite sequence of valid composite transitions — composed from K.α (amended), K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻ (amended), K.μ~ (shorthand for K.μ⁻ + K.μ⁺), and K.ρ — satisfies:

`S0 ∧ S1 ∧ S2 ∧ S3★ ∧ S3★-aux ∧ S8a ∧ S8-fin ∧ S8-depth ∧ S8 ∧ D-CTG ∧ D-MIN ∧ P0 ∧ P1 ∧ P2 ∧ P3★ ∧ P4★ ∧ P5★ ∧ P6 ∧ P7 ∧ P7a ∧ P8 ∧ L0 ∧ L1 ∧ L1a ∧ L3 ∧ L12 ∧ L14 ∧ CL-OWN`
