# ASN-0047 Formal Statements

*Source: ASN-0047-state-transitions.md (revised 2026-03-22) — Extracted: 2026-03-22*

## Definition — EntitySet

**Σ.E ⊆ T** — the set of allocated entity addresses. Every e ∈ E satisfies ValidAddress(e) (T4, ASN-0034). Entities are organisational — nodes, accounts, documents — not content; element-level addresses live in dom(C), not E:

`(A e ∈ E :: ¬IsElement(e))`

Equivalently, E ⊆ {t : ValidAddress(t) ∧ zeros(t) ≤ 2}. Given this exclusion, the level predicates of ASN-0045 partition E into exactly three strata:

- E_node = {e ∈ E : IsNode(e)} — server nodes
- E_account = {e ∈ E : IsAccount(e)} — user accounts
- E_doc = {e ∈ E : IsDocument(e)} — documents and links

## Definition — ProvenanceRelation

**Σ.R ⊆ T_elem × E_doc** — where T_elem = {a ∈ T : IsElement(a)} (ASN-0045). The pair (a, d) ∈ R records that document d has, at some point in the system's history, contained I-address a in its arrangement.

## Definition — ParentEntity

For a non-node entity e (where ¬IsNode(e)), define **parent(e)** as the tumbler obtained by truncating the last field and its preceding zero separator. If IsAccount(e) with form N.0.U, then parent(e) = N. If IsDocument(e) with form N.0.U.0.D, then parent(e) = N.0.U. In each case parent(e) is a valid address at the next higher level: zeros(parent(e)) = zeros(e) − 1.

## Definition — InitialState

The initial state Σ₀ = (C₀, E₀, M₀, R₀) is:

- C₀ = ∅ (no content allocated)
- E₀ = {n₀} for a designated bootstrap node n₀ with IsNode(n₀)
- M₀(d) = ∅ for all d — (E₀)_doc = ∅, so every arrangement is the empty partial function
- R₀ = ∅ (no provenance recorded)

## Definition — Endset

An *endset* is a finite set of well-formed spans: `Endset = 𝒫_fin(Span)`, where `Span` is the set of well-formed span pairs `(s, ℓ)` satisfying T12 (ASN-0034). The empty set ∅ is a valid endset.

## Definition — LinkValue

A *link value* is a triple `(F, G, Θ)` where `F, G, Θ ∈ Endset` — the *from-endset*, *to-endset*, and *type-endset* respectively.

## Definition — SubspaceIdentifiers

`s_C` for the content subspace identifier and `s_L` for the link subspace identifier. These are the first components of the element field for content and link addresses respectively: `fields(a).E₁ = s_C` for content addresses, `fields(ℓ).E₁ = s_L` for link addresses. The same identifiers serve for V-positions: `subspace(v) = v₁`.

## Definition — CurrentContainment

`Contains(Σ) = {(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))}`

## Definition — ContentContainment

`Contains_C(Σ) = {(a, d) : d ∈ E_doc ∧ (E v : v ∈ dom(M(d)) ∧ subspace(v) = s_C : M(d)(v) = a)}`

## Definition — ValidComposite

A composite transition Σ → Σ' is *valid* iff it is a finite sequence of elementary transitions Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ' satisfying two conditions:

(1) *Elementary preconditions:* each step Σᵢ → Σᵢ₊₁ satisfies the precondition of its elementary transition kind, evaluated at the intermediate state Σᵢ.

(2) *Coupling constraints:* J0, J1, and J1' hold for the composite — evaluated between the initial state Σ and the final state Σ'.

## Definition — ValidCompositeExtended

A composite transition Σ → Σ' in the extended state Σ = (C, L, E, M, R) is *valid* iff it is a finite sequence of transitions `Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ'` — drawn from K.α (amended), K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻ (amended), K.μ~, and K.ρ — satisfying:

1. *Transition preconditions:* each step `Σᵢ → Σᵢ₊₁` satisfies the precondition of its transition kind, evaluated at the intermediate state `Σᵢ`. K.μ~ appearing in the sequence is shorthand for its K.μ⁻ + K.μ⁺ decomposition — it expands into two consecutive elementary steps, each satisfying its own precondition at the respective intermediate state.
2. *Coupling constraints:* J0, J1★, and J1'★ hold for the composite — evaluated between the initial state Σ and the final state Σ'.

## Definition — Fork

A *fork* of d_src to d_new is a composite transition Σ → Σ', with *precondition* d_src ∈ E_doc ∧ M(d_src) ≠ ∅, consisting of:

(i) K.δ creating d_new with d_new ∉ E_doc,

(ii) K.μ⁺ populating M'(d_new) with ran(M'(d_new)) ⊆ ran(M(d_src)),

(iii) K.ρ recording provenance for each a ∈ ran(M'(d_new)),

and no other elementary steps.

---

## Σ.E — EntitySet (DEF, predicate)

`Σ.E ⊆ T`, partitioned by:

- E_node = {e ∈ E : IsNode(e)}
- E_account = {e ∈ E : IsAccount(e)}
- E_doc = {e ∈ E : IsDocument(e)}

with `(A e ∈ E :: ¬IsElement(e))`.

Equivalently: `E ⊆ {t : ValidAddress(t) ∧ zeros(t) ≤ 2}`.

## Σ.R — ProvenanceRelation (DEF, predicate)

`Σ.R ⊆ T_elem × E_doc`

where `T_elem = {a ∈ T : IsElement(a)}`.

## Σ₀ — InitialState (DEF, function)

- `C₀ = ∅`
- `E₀ = {n₀}` where `IsNode(n₀)`
- `M₀(d) = ∅` for all d
- `R₀ = ∅`

## parent(e) — ParentEntity (DEF, function)

For `¬IsNode(e)`: tumbler obtained by truncating the last field and its preceding zero separator.

- If `IsAccount(e)` with form N.0.U: `parent(e) = N`
- If `IsDocument(e)` with form N.0.U.0.D: `parent(e) = N.0.U`

In each case: `zeros(parent(e)) = zeros(e) − 1`.

## Contains(Σ) — CurrentContainment (DEF, function)

`Contains(Σ) = {(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))}`

## ValidComposite — ValidComposite (DEF, predicate)

A composite transition Σ → Σ' is valid iff it is a finite sequence Σ = Σ₀ → ... → Σₙ = Σ' satisfying:

(1) Each step Σᵢ → Σᵢ₊₁ satisfies its elementary precondition at Σᵢ.

(2) J0, J1, and J1' hold for the composite, evaluated between Σ and Σ'.

## ArrangementInvariantsLemma — ArrangementInvariantsLemma (LEMMA, lemma)

Every valid composite transition preserves S2, S3, S8a, S8-depth, and S8-fin. Each elementary transition preserves these per-state properties: K.μ⁺ establishes them via its preconditions (disjoint extension for S2, referential integrity for S3, explicit S8a/S8-depth/S8-fin requirements); K.μ⁻ preserves them by restriction of M(d); K.δ for documents produces the empty arrangement (vacuously satisfying all five); all other transitions hold M in frame. Since each step of a valid composite preserves these per-state properties, they hold at every intermediate and final state.

## ReachableStateInvariants — ReachableStateInvariants (THEOREM, lemma)

Every state reachable from Σ₀ by a finite sequence of valid composite transitions satisfies P4 (Contains(Σ) ⊆ R), P6, P7, P7a, P8, S2, S3, S8a, S8-depth, and S8-fin.

## P0 — ContentPermanence (INV, predicate)

`(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ (A a : a ∈ dom(C) : C'(a) = C(a)))`

## P1 — EntityPermanence (INV, predicate)

`(A Σ → Σ' :: E ⊆ E')`

Specialised to levels:

`[e ∈ E ∧ IsNode(e) ⟹ e ∈ E']`
`[e ∈ E ∧ IsAccount(e) ⟹ e ∈ E']`
`[e ∈ E ∧ IsDocument(e) ⟹ e ∈ E']`

## P2 — ProvenancePermanence (INV, predicate)

`(A Σ → Σ' :: R ⊆ R')`

## P3 — ArrangementMutabilityOnly (INV, predicate)

Arrangements admit three modes of change:

(a) *Extension*: new V→I mappings may be added to M(d).

(b) *Contraction*: existing V→I mappings may be removed from M(d).

(c) *Reordering*: V-positions of existing mappings may change while the multiset of referenced I-addresses is preserved.

No other component admits contraction or reordering.

## P3★ — ArrangementMutabilityOnlyExtended (INV, predicate)

`(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ dom(L) ⊆ dom(L') ∧ E ⊆ E' ∧ R ⊆ R')`

L admits only extension, by L12: `dom(L) ⊆ dom(L') ∧ (A ℓ ∈ dom(L) : L'(ℓ) = L(ℓ))`.

## P4 — ProvenanceBounds (INV, predicate)

`Contains(Σ) ⊆ R`

## P4★ — ProvenanceBoundsContent (INV, predicate)

`Contains_C(Σ) ⊆ R`

## P4a — HistoricalFidelity (INV, predicate)

`(A (a, d) ∈ R :: (E Σ_k in the transition history : a ∈ ran(M_k(d))))`

## P5 — DestructionConfinement (THEOREM, lemma)

For every state transition Σ → Σ':

(a) `dom(C') ⊇ dom(C) ∧ (A a : a ∈ dom(C) : C'(a) = C(a))`

(b) `E' ⊇ E`

(c) `R' ⊇ R`

The only component that can lose information is M.

## P5★ — DestructionConfinementExtended (THEOREM, lemma)

For every state transition Σ → Σ':

(a) `dom(C') ⊇ dom(C) ∧ (A a : a ∈ dom(C) : C'(a) = C(a))`

(b) `dom(L') ⊇ dom(L) ∧ (A ℓ : ℓ ∈ dom(L) : L'(ℓ) = L(ℓ))`

(c) `E' ⊇ E`

(d) `R' ⊇ R`

The only component that can lose information is M.

## P6 — ExistentialCoherence (INV, predicate)

`(A a ∈ dom(C) :: origin(a) ∈ E_doc)`

## P7 — ProvenanceGrounding (INV, predicate)

`(A (a, d) ∈ R :: a ∈ dom(C))`

## P7a — ProvenanceCoverage (INV, predicate)

`(A a ∈ dom(C) :: (E d :: (a, d) ∈ R))`

## P8 — EntityHierarchy (INV, predicate)

`(A e ∈ E : ¬IsNode(e) : parent(e) ∈ E)`

## SC-NEQ — SubspaceDistinctness (INV, predicate)

`s_C ≠ s_L`

## K.α — ContentAllocation (TRANS, predicate)

*Precondition:* `IsElement(a) ∧ origin(a) ∈ E_doc ∧ a ∉ dom(C)`

*Effect:* `C' = C ∪ {a ↦ v}`

*Frame:* `E' = E; (A d :: M'(d) = M(d)); R' = R`

## K.α amendment — ContentAllocationSubspaceRestriction (TRANS, predicate)

Additional precondition on K.α in the extended state:

`fields(a).E₁ = s_C`

## K.δ — EntityCreation (TRANS, predicate)

*Precondition:* `e ∉ E ∧ ValidAddress(e) ∧ ¬IsElement(e)`; when `¬IsNode(e)`: `parent(e) ∈ E`

*Effect:* `E' = E ∪ {e}`

When `IsDocument(e)`: `M'(e) = ∅`

*Frame:* `C' = C; (A d' :: M'(d') = M(d')); R' = R`

## K.μ⁺ — ArrangementExtension (TRANS, predicate)

*Precondition:* `d ∈ E_doc`; for every new mapping `M'(d)(v) = a`: `a ∈ dom(C)`; new V-positions satisfy S8a; `M'(d)` satisfies S8-depth; `dom(M'(d))` is finite (S8-fin).

*Effect:* `dom(M'(d)) ⊃ dom(M(d)) ∧ (A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))`

*Frame:* `C' = C; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R`

## K.μ⁺ amendment — ArrangementExtensionSubspaceRestriction (TRANS, predicate)

Additional precondition on K.μ⁺ in the extended state:

New V-positions must satisfy `subspace(v) = s_C`. Additionally, `M'(d)` must satisfy D-CTG and D-MIN for each subspace.

## K.μ⁻ — ArrangementContraction (TRANS, predicate)

*Precondition:* `d ∈ E_doc`

*Effect:* `dom(M'(d)) ⊂ dom(M(d)) ∧ (A v : v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v))`

*Frame:* `C' = C; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d'))`

## K.μ⁻ amendment — ArrangementContractionPerSubspaceContiguity (TRANS, predicate)

Additional postcondition on K.μ⁻ in the extended state:

`M'(d)` must satisfy D-CTG and D-MIN for each subspace. By D-SEQ at the input state, V_S(d) for each non-empty subspace S is a contiguous ordinal range `{[S, 1, ..., 1, k] : 1 ≤ k ≤ n}`; the postcondition constrains contraction to removal from the maximum end of V_S(d) or removal of all positions in V_S(d).

## K.μ~ — ArrangementReordering (TRANS, predicate)

*Precondition:* `d ∈ E_doc`; π produces V-positions satisfying S8a; the resulting arrangement `M'(d)` satisfies S8-depth.

*Effect:* there exists a bijection `π : dom(M(d)) → dom(M'(d))` such that:

`(A v : v ∈ dom(M(d)) : M'(d)(π(v)) = M(d)(v))`

*Frame (derived):* `C' = C; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d'))`

## K.ρ — ProvenanceRecording (TRANS, predicate)

*Precondition:* `a ∈ dom(C) ∧ d ∈ E_doc`

*Effect:* `R' = R ∪ {(a, d)}`

*Frame:* `C' = C; E' = E; (A d :: M'(d) = M(d))`

## K.λ — LinkAllocation (TRANS, predicate)

*Precondition:*
- `d ∈ E_doc`
- `ℓ ∉ dom(L) ∪ dom(C)`
- `zeros(ℓ) = 3 ∧ fields(ℓ).E₁ = s_L`
- `origin(ℓ) = d`
- `(A ℓ' : ℓ' ∈ dom(L) ∧ origin(ℓ') = d : ℓ' < ℓ)`
- `(F, G, Θ) ∈ Link`

*Effect:* `L' = L ∪ {ℓ ↦ (F, G, Θ)}`

*Frame:* `C' = C; E' = E; (A d' :: M'(d') = M(d')); R' = R`

## K.μ⁺_L — LinkSubspaceExtension (TRANS, predicate)

*Precondition:*
- `d ∈ E_doc`
- `ℓ ∈ dom(L)`
- `origin(ℓ) = d`
- `subspace(v_ℓ) = s_L`
- If `V_{s_L}(d) ≠ ∅`: `m_L` is the common depth of existing link-subspace V-positions (determined by S8-depth)
- If `V_{s_L}(d) = ∅`: `m_L` is a parameter of the transition, subject only to `m_L ≥ 2`
- If `V_{s_L}(d) = ∅`: `v_ℓ` is the minimum position `[s_L, 1, ..., 1]` of depth m_L (D-MIN)
- If `V_{s_L}(d) ≠ ∅`: `v_ℓ = shift(max(V_{s_L}(d)), 1)` (D-CTG)
- `#v_ℓ = m_L` (S8-depth within the link subspace)

*Effect:* `M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}`

*Frame:* `C' = C; L' = L; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R`

## J0 — AllocationRequiresPlacement (INV, predicate)

`(A Σ → Σ', a : a ∈ dom(C') \ dom(C) : (E d, v : d ∈ E'_doc ∧ v ∈ dom(M'(d)) : M'(d)(v) = a))`

## J1 — ExtensionRecordsProvenance (INV, predicate)

`(A Σ → Σ', d ∈ E'_doc, a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R')`

## J1★ — ExtensionRecordsProvenanceScoped (INV, predicate)

`(A Σ → Σ', d ∈ E'_doc, a : (E v ∈ dom(M'(d)) : subspace(v) = s_C ∧ M'(d)(v) = a) ∧ ¬(E v ∈ dom(M(d)) : subspace(v) = s_C ∧ M(d)(v) = a) : (a, d) ∈ R')`

## J1' — ProvenanceRequiresExtension (INV, predicate)

`(A Σ → Σ', a, d ∈ E'_doc : (a, d) ∈ R' \ R : a ∈ ran(M'(d)) \ ran(M(d)))`

## J1'★ — ProvenanceRequiresExtensionScoped (INV, predicate)

`(A Σ → Σ', a, d : (a, d) ∈ R' \ R : (E v ∈ dom(M'(d)) : subspace(v) = s_C ∧ M'(d)(v) = a) ∧ ¬(E v ∈ dom(M(d)) : subspace(v) = s_C ∧ M(d)(v) = a))`

## J2 — ContractionIsolation (INV, predicate)

K.μ⁻ as an elementary transition satisfies:

`C' = C ∧ E' = E ∧ R' = R`

No co-occurring transition is needed to maintain any system invariant.

## J3 — ReorderingIsolation (INV, predicate)

K.μ~ as a distinguished composite satisfies:

`C' = C ∧ E' = E ∧ R' = R`

No co-occurring transition is needed to maintain any system invariant.

## J4 — Fork (DEF, predicate)

*Precondition:* `d_src ∈ E_doc ∧ M(d_src) ≠ ∅`

A *fork* of d_src to d_new consists of exactly:

(i) K.δ creating d_new with `d_new ∉ E_doc`,

(ii) K.μ⁺ populating M'(d_new) with `ran(M'(d_new)) ⊆ ran(M(d_src))`,

(iii) K.ρ recording provenance for each `a ∈ ran(M'(d_new))`,

and no other elementary steps.

Since none of K.δ, K.μ⁺, K.ρ modify C: `dom(C') = dom(C)`.

## S3★ — GeneralizedReferentialIntegrity (INV, predicate)

`(A d, v : v ∈ dom(Σ.M(d)) : (subspace(v) = s_C ⟹ Σ.M(d)(v) ∈ dom(Σ.C)) ∧ (subspace(v) = s_L ⟹ Σ.M(d)(v) ∈ dom(Σ.L)))`

where `subspace(v)` denotes the first component of the V-position.

## S3★-aux — SubspaceExhaustiveness (INV, predicate)

`(A d, v : v ∈ dom(M(d)) : subspace(v) = s_C ∨ subspace(v) = s_L)`

## Contains_C(Σ) — ContentContainment (DEF, function)

`Contains_C(Σ) = {(a, d) : d ∈ E_doc ∧ (E v : v ∈ dom(M(d)) ∧ subspace(v) = s_C : M(d)(v) = a)}`

## ValidComposite★ — ValidCompositeExtended (DEF, predicate)

A composite transition Σ → Σ' in the extended state Σ = (C, L, E, M, R) is *valid* iff it is a finite sequence `Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ'` drawn from K.α (amended), K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻ (amended), K.μ~, and K.ρ, satisfying:

1. Each step `Σᵢ → Σᵢ₊₁` satisfies the precondition of its transition kind at `Σᵢ`. K.μ~ is shorthand for its K.μ⁻ + K.μ⁺ decomposition.
2. J0, J1★, and J1'★ hold for the composite, evaluated between Σ and Σ'.

## P4★ — ProvenanceBoundsContent (INV, predicate)

`Contains_C(Σ) ⊆ R`

## P3★ — ArrangementMutabilityOnlyExtended (INV, predicate)

`(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ dom(L) ⊆ dom(L') ∧ E ⊆ E' ∧ R ⊆ R')`

L admits only extension (L12): `dom(L) ⊆ dom(L') ∧ (A ℓ ∈ dom(L) : L'(ℓ) = L(ℓ))`.

## P5★ — DestructionConfinementExtended (THEOREM, lemma)

For every state transition Σ → Σ':

(a) `dom(C') ⊇ dom(C) ∧ (A a : a ∈ dom(C) : C'(a) = C(a))`

(b) `dom(L') ⊇ dom(L) ∧ (A ℓ : ℓ ∈ dom(L) : L'(ℓ) = L(ℓ))`

(c) `E' ⊇ E`

(d) `R' ⊇ R`

The only component that can lose information is M.

## CL-OWN — LinkSubspaceOwnership (INV, predicate)

`(A d, v : v ∈ dom(M(d)) ∧ subspace(v) = s_L : origin(M(d)(v)) = d)`

## ExtendedReachableStateInvariants — ExtendedReachableStateInvariants (THEOREM, lemma)

Every state reachable from Σ₀ = (C₀, L₀, E₀, M₀, R₀) by a finite sequence of valid composite transitions — composed from K.α (amended), K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻ (amended), K.μ~ (shorthand for K.μ⁻ + K.μ⁺ decomposition), and K.ρ — satisfies:

`S0 ∧ S1 ∧ S2 ∧ S3★ ∧ S3★-aux ∧ S8a ∧ S8-fin ∧ S8-depth ∧ S8 ∧ D-CTG ∧ D-MIN ∧ P0 ∧ P1 ∧ P2 ∧ P3★ ∧ P4★ ∧ P5★ ∧ P6 ∧ P7 ∧ P7a ∧ P8 ∧ L0 ∧ L1 ∧ L1a ∧ L3 ∧ L12 ∧ L14 ∧ CL-OWN`
