# ASN-0047 Formal Statements

*Source: ASN-0047-state-transitions.md (revised 2026-03-17) — Extracted: 2026-03-20*

## Definition — EntitySet

**Σ.E ⊆ T** — the set of allocated entity addresses.

`(A e ∈ E :: ¬IsElement(e))`

Equivalently: `E ⊆ {t : ValidAddress(t) ∧ zeros(t) ≤ 2}`

Partition by level predicates (ASN-0045):
- `E_node = {e ∈ E : IsNode(e)}`
- `E_account = {e ∈ E : IsAccount(e)}`
- `E_doc = {e ∈ E : IsDocument(e)}`

M is total with `M(d) = ∅` for `d ∉ E_doc`.

---

## Definition — ProvenanceRelation

**Σ.R ⊆ T_elem × E_doc** — where `T_elem = {a ∈ T : IsElement(a)}`.

The pair `(a, d) ∈ R` records that document d has, at some point in the system's history, contained I-address a in its arrangement.

---

## Definition — InitialState

The initial state `Σ₀ = (C₀, E₀, M₀, R₀)`:

- `C₀ = ∅`
- `E₀ = {n₀}` for a designated bootstrap node n₀ with `IsNode(n₀)`
- `M₀(d) = ∅` for all d — `(E₀)_doc = ∅`
- `R₀ = ∅`

---

## Definition — ParentEntity

For a non-node entity e where `¬IsNode(e)`: **parent(e)** is the tumbler obtained by truncating the last field and its preceding zero separator.

- If `IsAccount(e)` with form N.0.U, then `parent(e) = N`
- If `IsDocument(e)` with form N.0.U.0.D, then `parent(e) = N.0.U`

In each case: `zeros(parent(e)) = zeros(e) − 1`

---

## Definition — SystemState

**Σ = (C, E, M, R)**

where `C : T ⇀ Val`, and `M : T → (T ⇀ T)` is total, satisfying `M(d) = ∅` for `d ∉ E_doc`.

---

## Definition — CurrentContainment

`Contains(Σ) = {(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))}`

---

## Definition — ValidComposite

A composite transition Σ → Σ' is *valid* iff it is a finite sequence of elementary transitions `Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ'` satisfying:

1. *Elementary preconditions:* each step `Σᵢ → Σᵢ₊₁` satisfies the precondition of its elementary transition kind, evaluated at the intermediate state `Σᵢ`.
2. *Coupling constraints:* J0, J1, and J1' hold for the composite — evaluated between the initial state Σ and the final state Σ'.

---

## Definition — ForkComposite

A *fork* of `d_src` to `d_new` is a composite transition Σ → Σ', with precondition `d_src ∈ E_doc ∧ M(d_src) ≠ ∅`, consisting of:

(i) K.δ creating `d_new` with `d_new ∉ E_doc`,
(ii) K.μ⁺ populating `M'(d_new)` with `ran(M'(d_new)) ⊆ ran(M(d_src))`,
(iii) K.ρ recording provenance for each `a ∈ ran(M'(d_new))`,

and no other elementary steps.

Consequence: `dom(C') = dom(C)` (none of K.δ, K.μ⁺, K.ρ modify C).

---

## Σ.E — EntitySet (DEF, definition)

`E ⊆ {t : ValidAddress(t) ∧ zeros(t) ≤ 2}`

`(A e ∈ E :: ¬IsElement(e))`

---

## Σ.R — ProvenanceRelation (DEF, definition)

`R ⊆ T_elem × E_doc`

where `T_elem = {a ∈ T : IsElement(a)}`

---

## Σ₀ — InitialState (DEF, definition)

- `C₀ = ∅`
- `E₀ = {n₀}` with `IsNode(n₀)`
- `M₀(d) = ∅` for all d
- `R₀ = ∅`

---

## parent(e) — ParentEntity (DEF, function)

For `¬IsNode(e)`: tumbler obtained by truncating last field and preceding zero separator.

`zeros(parent(e)) = zeros(e) − 1`

---

## Contains(Σ) — CurrentContainment (DEF, function)

`Contains(Σ) = {(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))}`

---

## Valid composite — ValidComposite (DEF, predicate)

Σ → Σ' valid iff finite sequence `Σ = Σ₀ → ... → Σₙ = Σ'` satisfying:
1. Elementary preconditions at each intermediate state Σᵢ.
2. J0, J1, J1' hold for the composite (evaluated Σ to Σ').

---

## Arrangement invariants lemma — ArrangementInvariantsLemma (LEMMA, lemma)

Every valid composite transition preserves S2, S3, S8a, S8-depth, and S8-fin.

Elementary cases:
- K.μ⁺: establishes via preconditions (disjoint extension for S2, referential integrity for S3, explicit S8a/S8-depth/S8-fin requirements)
- K.μ⁻: preserves by restriction of M(d)
- K.δ for documents: produces empty arrangement (vacuously satisfying all five)
- all other transitions: hold M in frame

---

## Reachable-state invariants — ReachableStateInvariants (THEOREM, theorem)

Every state reachable from Σ₀ by a finite sequence of valid composite transitions satisfies:

`P4 ∧ P6 ∧ P7 ∧ P7a ∧ P8 ∧ S2 ∧ S3 ∧ S8a ∧ S8-depth ∧ S8-fin`

i.e., `Contains(Σ) ⊆ R`, existential coherence, provenance grounding, provenance coverage, entity hierarchy, and all arrangement well-formedness properties.

---

## P0 — ContentPermanence (INV, predicate)

`(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ (A a : a ∈ dom(C) : C'(a) = C(a)))`

---

## P1 — EntityPermanence (INV, predicate)

`(A Σ → Σ' :: E ⊆ E')`

Sub-properties:
- `[e ∈ E ∧ IsNode(e) ⟹ e ∈ E']`
- `[e ∈ E ∧ IsAccount(e) ⟹ e ∈ E']`
- `[e ∈ E ∧ IsDocument(e) ⟹ e ∈ E']`

---

## P8 — EntityHierarchy (INV, predicate)

`(A e ∈ E : ¬IsNode(e) : parent(e) ∈ E)`

---

## P2 — ProvenancePermanence (INV, predicate)

`(A Σ → Σ' :: R ⊆ R')`

---

## P3 — ArrangementMutabilityOnly (INV, predicate)

Arrangements admit three modes of change:

(a) *Extension*: new V→I mappings may be added to M(d).
(b) *Contraction*: existing V→I mappings may be removed from M(d).
(c) *Reordering*: V-positions of existing mappings may change while the multiset of referenced I-addresses is preserved.

No other component (C, E, R) admits contraction or reordering.

---

## P4 — ProvenanceBounds (INV, predicate)

`Contains(Σ) ⊆ R`

(Stale entries `(a, d) ∈ R \ Contains(Σ)` are possible from prior insertion-deletion cycles.)

---

## P4a — HistoricalFidelity (INV, predicate)

`(A (a, d) ∈ R :: (E Σ_k in the transition history : a ∈ ran(M_k(d))))`

---

## P5 — DestructionConfinement (INV, predicate)

For every state transition Σ → Σ':

(a) `dom(C') ⊇ dom(C) ∧ (A a : a ∈ dom(C) : C'(a) = C(a))`
(b) `E' ⊇ E`
(c) `R' ⊇ R`

The only component that can lose information is M.

---

## K.α — ContentAllocation (TRANS, definition)

Effect: `C' = C ∪ {a ↦ v}` where `a ∉ dom(C)`

*Precondition:* `IsElement(a) ∧ origin(a) ∈ E_doc`

*Frame:* `E' = E; (A d :: M'(d) = M(d)); R' = R`

---

## K.δ — EntityCreation (TRANS, definition)

Effect: `E' = E ∪ {e}` where `e ∉ E ∧ ValidAddress(e) ∧ ¬IsElement(e)`

*Precondition:* when `¬IsNode(e)`, `parent(e) ∈ E`; for `IsNode(e)`, no parent required.

When `IsDocument(e)`: `M'(e) = ∅`

*Frame:* `C' = C; (A d' :: M'(d') = M(d')); R' = R`

---

## K.μ⁺ — ArrangementExtension (TRANS, definition)

Effect: `dom(M'(d)) ⊃ dom(M(d)) ∧ (A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))`

*Precondition:* `d ∈ E_doc`; for every new mapping `M'(d)(v) = a`, `a ∈ dom(C)`; new V-positions satisfy S8a; `M'(d)` satisfies S8-depth; `dom(M'(d))` is finite (S8-fin).

*Frame:* `C' = C; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R`

---

## K.μ⁻ — ArrangementContraction (TRANS, definition)

Effect: `dom(M'(d)) ⊂ dom(M(d)) ∧ (A v : v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v))`

*Precondition:* `d ∈ E_doc`

*Frame:* `C' = C; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d'))`

---

## K.μ~ — ArrangementReordering (TRANS, definition)

Distinguished composite (K.μ⁻ + K.μ⁺). There exists a bijection `π : dom(M(d)) → dom(M'(d))` such that:

`(A v : v ∈ dom(M(d)) : M'(d)(π(v)) = M(d)(v))`

*Precondition:* `d ∈ E_doc`; π produces V-positions satisfying S8a; `M'(d)` satisfies S8-depth.

*Corollary:* `ran(M'(d)) = ran(M(d))`

*Frame (derived):* `C' = C; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d'))`

---

## K.ρ — ProvenanceRecording (TRANS, definition)

Effect: `R' = R ∪ {(a, d)}` where `a ∈ dom(C) ∧ d ∈ E_doc`

*Precondition:* `a ∈ dom(C) ∧ d ∈ E_doc`

*Frame:* `C' = C; E' = E; (A d :: M'(d) = M(d))`

---

## J0 — AllocationRequiresPlacement (AX, predicate)

`(A Σ → Σ', a : a ∈ dom(C') \ dom(C) : (E d, v : d ∈ E'_doc ∧ v ∈ dom(M'(d)) : M'(d)(v) = a))`

---

## J1 — ExtensionRecordsProvenance (AX, predicate)

`(A Σ → Σ', d ∈ E'_doc, a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R')`

For freshly created `d ∈ E'_doc \ E_doc`: `M(d) = ∅` by totality, so `ran(M'(d)) \ ran(M(d)) = ran(M'(d))`.

---

## J1' — ProvenanceRequiresExtension (AX, predicate)

`(A Σ → Σ', a, d ∈ E'_doc : (a, d) ∈ R' \ R : a ∈ ran(M'(d)) \ ran(M(d)))`

---

## J2 — ContractionIsolation (AX, predicate)

K.μ⁻ as elementary transition requires no coupling:

`C' = C ∧ E' = E ∧ R' = R`

Consequence: `Contains(Σ') ⊆ Contains(Σ) ⊆ R = R'`

---

## J3 — ReorderingIsolation (AX, predicate)

K.μ~ as distinguished composite requires no coupling:

`C' = C ∧ E' = E ∧ R' = R`

Consequence: `Contains(Σ') = Contains(Σ)`

---

## J4 — Fork (DEF, definition)

*Precondition:* `d_src ∈ E_doc ∧ M(d_src) ≠ ∅`

Steps (exactly):
(i) K.δ: `d_new ∉ E_doc`, `E' = E ∪ {d_new}`, `M'(d_new) = ∅`
(ii) K.μ⁺: `ran(M'(d_new)) ⊆ ran(M(d_src))`
(iii) K.ρ: `(a, d_new) ∈ R'` for each `a ∈ ran(M'(d_new))`

Consequence: `dom(C') = dom(C)` (no new content allocated).

When `M(d_src) = ∅`: fork does not apply; creation is K.δ alone (ex nihilo).

---

## P6 — ExistentialCoherence (INV, predicate)

`(A a ∈ dom(C) :: origin(a) ∈ E_doc)`

---

## P7 — ProvenanceGrounding (INV, predicate)

`(A (a, d) ∈ R :: a ∈ dom(C))`

---

## P7a — ProvenanceCoverage (INV, predicate)

`(A a ∈ dom(C) :: (E d :: (a, d) ∈ R))`
