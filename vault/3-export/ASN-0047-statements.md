# ASN-0047 Formal Statements

*Source: ASN-0047-state-transitions.md (revised 2026-03-17) — Index: 2026-03-17 — Extracted: 2026-03-17*

## Definition — EntitySet

**Σ.E ⊆ T** — the set of allocated entity addresses. Every e ∈ E satisfies ValidAddress(e). Entities are organisational — nodes, accounts, documents — not content; element-level addresses live in dom(C), not E:

`(A e ∈ E :: ¬IsElement(e))`

Equivalently, E ⊆ {t : ValidAddress(t) ∧ zeros(t) ≤ 2}. Given this exclusion, the level predicates partition E into exactly three strata:

- E_node = {e ∈ E : IsNode(e)}
- E_account = {e ∈ E : IsAccount(e)}
- E_doc = {e ∈ E : IsDocument(e)}

## Definition — ParentEntity

For a non-node entity e (where ¬IsNode(e)), **parent(e)** is the tumbler obtained by truncating the last field and its preceding zero separator. If IsAccount(e) with form N.0.U, then parent(e) = N. If IsDocument(e) with form N.0.U.0.D, then parent(e) = N.0.U. In each case parent(e) is a valid address at the next higher level: zeros(parent(e)) = zeros(e) − 1.

## Definition — CurrentContainment

The *current containment* of state Σ is:

`Contains(Σ) = {(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))}`

## Definition — ValidCompositeTransition

A composite transition Σ → Σ' is *valid* iff it is a finite sequence of elementary transitions Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ' satisfying:

(1) *Elementary preconditions:* each step Σᵢ → Σᵢ₊₁ satisfies the precondition of its elementary transition kind, evaluated at the intermediate state Σᵢ.

(2) *Coupling constraints:* J0, J1, and J1' hold for the composite — evaluated between the initial state Σ and the final state Σ'.

## Definition — Fork

A *fork* of d_src to d_new is a composite transition Σ → Σ', with *precondition* d_src ∈ E_doc ∧ M(d_src) ≠ ∅, consisting of:

(i) K.δ creating d_new with d_new ∉ E_doc,

(ii) K.μ⁺ populating M'(d_new) with ran(M'(d_new)) ⊆ ran(M(d_src)),

(iii) K.ρ recording provenance for each a ∈ ran(M'(d_new)),

and no other elementary steps.

---

## Σ.E — EntitySetValid (INV, predicate(State))

E ⊆ {t : ValidAddress(t) ∧ zeros(t) ≤ 2}

`(A e ∈ E :: ¬IsElement(e))`

Level partition:
- E_node = {e ∈ E : IsNode(e)}
- E_account = {e ∈ E : IsAccount(e)}
- E_doc = {e ∈ E : IsDocument(e)}

## Σ.R — ProvenanceWellTyped (INV, predicate(State))

**Σ.R ⊆ T_elem × E_doc** where T_elem = {a ∈ T : IsElement(a)}. The pair (a, d) ∈ R records that document d has, at some point in the system's history, contained I-address a in its arrangement.

## Σ₀ — IsInitialState (INV, predicate(State))

The initial state Σ₀ = (C₀, E₀, M₀, R₀) is:

- C₀ = ∅
- E₀ = {n₀} for a designated bootstrap node n₀ with IsNode(n₀)
- M₀(d) = ∅ for all d — (E₀)_doc = ∅, so every arrangement is the empty partial function
- R₀ = ∅

## P0 — ContentPermanence (INV, predicate(State, State))

`(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ (A a : a ∈ dom(C) : C'(a) = C(a)))`

## P1 — EntityPermanence (INV, predicate(State, State))

`(A Σ → Σ' :: E ⊆ E')`

Sub-properties:

`[e ∈ E ∧ IsNode(e) ⟹ e ∈ E']`
`[e ∈ E ∧ IsAccount(e) ⟹ e ∈ E']`
`[e ∈ E ∧ IsDocument(e) ⟹ e ∈ E']`

## P8 — EntityHierarchy (LEMMA, lemma)

`(A e ∈ E : ¬IsNode(e) : parent(e) ∈ E)`

*Derivation:* K.δ for non-root entities requires parent(e) ∈ E as a precondition. P1 preserves the parent's membership across subsequent transitions. Base case: E₀ = {n₀} with IsNode(n₀), so the quantifier is vacuously satisfied. Inductive step: K.δ adds e with parent(e) ∈ E ⊆ E' (by precondition and P1); all other transitions have E' ⊇ E. ∎

## P2 — ProvenancePermanence (INV, predicate(State, State))

`(A Σ → Σ' :: R ⊆ R')`

## P3 — ArrangementMutability (LEMMA, lemma)

Arrangements admit three modes of change:

(a) *Extension*: new V→I mappings may be added to M(d).

(b) *Contraction*: existing V→I mappings may be removed from M(d).

(c) *Reordering*: V-positions of existing mappings may change while the multiset of referenced I-addresses is preserved.

No other component admits contraction or reordering. C, E, and R are all monotonic; only M can shrink.

## K.α (pre) — ContentAllocatable (PRE, requires)

`IsElement(a) ∧ origin(a) ∈ E_doc`

## K.α — ContentAllocation (POST, ensures)

`C' = C ∪ {a ↦ v}` where `a ∉ dom(C)`

*Frame:* E' = E; (A d :: M'(d) = M(d)); R' = R.

## K.δ (pre) — EntityCreatable (PRE, requires)

When ¬IsNode(e): `parent(e) ∈ E`. For root nodes (IsNode(e)), no parent is required.

## K.δ — EntityCreation (POST, ensures)

`E' = E ∪ {e}` where `e ∉ E ∧ ValidAddress(e) ∧ ¬IsElement(e)`

When IsDocument(e): M'(e) = ∅.

*Frame:* C' = C; (A d' :: M'(d') = M(d')); R' = R.

## K.μ⁺ — ArrangementExtension (POST, ensures)

`dom(M'(d)) ⊃ dom(M(d)) ∧ (A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))`

*Precondition:* d ∈ E_doc; for every new mapping M'(d)(v) = a, `a ∈ dom(C)`; new V-positions satisfy S8a; the resulting arrangement M'(d) satisfies S8-depth; dom(M'(d)) is finite (S8-fin).

*Frame:* C' = C; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R.

## K.μ⁻ — ArrangementContraction (POST, ensures)

`dom(M'(d)) ⊂ dom(M(d)) ∧ (A v : v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v))`

*Precondition:* d ∈ E_doc.

*Frame:* C' = C; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d')).

## K.μ~ — ArrangementReordering (POST, ensures)

For some d ∈ E_doc, there exists a bijection π : dom(M(d)) → dom(M'(d)) such that:

`(A v : v ∈ dom(M(d)) : M'(d)(π(v)) = M(d)(v))`

As a corollary: ran(M'(d)) = ran(M(d)).

*Precondition:* d ∈ E_doc; π produces V-positions satisfying S8a; the resulting arrangement M'(d) satisfies S8-depth.

*Frame (derived):* C' = C; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d')).

## K.ρ (pre) — ProvenanceRecordable (PRE, requires)

`a ∈ dom(C) ∧ d ∈ E_doc`

## K.ρ — ProvenanceRecording (POST, ensures)

`R' = R ∪ {(a, d)}` where `a ∈ dom(C) ∧ d ∈ E_doc`

*Frame:* C' = C; E' = E; (A d :: M'(d) = M(d)).

## Arrangement invariants lemma — ArrangementInvariantsPreserved (LEMMA, lemma)

Every valid composite transition preserves S2, S3, S8a, S8-depth, and S8-fin. Each elementary transition preserves these per-state properties: K.μ⁺ establishes them via its preconditions (disjoint extension for S2, referential integrity for S3, explicit S8a/S8-depth/S8-fin requirements); K.μ⁻ preserves them by restriction of M(d); K.δ for documents produces the empty arrangement (vacuously satisfying all five); all other transitions hold M in frame. Since each step of a valid composite preserves these per-state properties, they hold at every intermediate and final state.

## Valid composite — ValidComposite (INV, predicate(State, State))

A composite transition Σ → Σ' satisfies:

(1) Each step Σᵢ → Σᵢ₊₁ satisfies the precondition of its elementary transition kind, evaluated at Σᵢ.

(2) J0, J1, and J1' hold for the composite, evaluated between Σ and Σ'.

## Permanence lemma — PermanenceFromFrames (LEMMA, lemma)

Every valid composite transition satisfies P0, P1, and P2. Each elementary transition's frame ensures: K.α extends dom(C) preserving existing entries (all others hold C' = C), giving P0; K.δ extends E (all others hold E' = E), giving P1; K.ρ extends R (all others hold R' = R), giving P2. By transitivity over any finite sequence satisfying (1), the composite inherits all three permanence properties.

## Reachable-state invariants — ReachableStateInvariants (LEMMA, lemma)

Every state reachable from Σ₀ by a finite sequence of valid composite transitions satisfies P4 (Contains(Σ) ⊆ R), P6, P7, P7a, P8, S2, S3, S8a, S8-depth, and S8-fin.

*Base case.* At Σ₀: dom(C₀) = ∅ makes P6 vacuous; R₀ = ∅ makes P7 vacuous; dom(C₀) = ∅ makes P7a vacuous; (E₀)_doc = ∅ makes P4 vacuous (Contains(Σ₀) = ∅ ⊆ R₀); E₀ = {n₀} with IsNode(n₀) makes P8 vacuous; (E₀)_doc = ∅ makes S2–S8-fin vacuous.

*Inductive step.* For any reachable state Σ satisfying the above, every valid composite Σ → Σ' produces Σ' satisfying the same — P0/P1/P2 by the permanence lemma; S2/S3/S8a/S8-depth/S8-fin by the arrangement invariants lemma; P8 as derived above; P4, P6, P7, and P7a as derived below.

## J0 — AllocationRequiresPlacement (INV, predicate(State, State))

`(A Σ → Σ', a : a ∈ dom(C') \ dom(C) : (E d, v : d ∈ E'_doc ∧ v ∈ dom(M'(d)) : M'(d)(v) = a))`

Every freshly allocated I-address appears in some arrangement in the post-state — the containing document may itself have been freshly created by K.δ in the same composite transition.

## J1 — ExtensionRecordsProvenance (INV, predicate(State, State))

`(A Σ → Σ', d ∈ E'_doc, a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R')`

For a freshly created document d ∈ E'_doc \ E_doc, M(d) = ∅ by totality, so ran(M(d)) = ∅, so ran(M'(d)) \ ran(M(d)) = ran(M'(d)): every I-address placed in a new document triggers provenance recording.

## J1' — ProvenanceRequiresExtension (INV, predicate(State, State))

`(A Σ → Σ', a, d ∈ E'_doc : (a, d) ∈ R' \ R : a ∈ ran(M'(d)) \ ran(M(d)))`

When (a, d) ∈ R already — from a prior insertion-deletion cycle — K.μ⁺ re-introducing a into d's arrangement requires no new K.ρ, because J1's requirement (a, d) ∈ R' is satisfied by existing membership (P2 ensures prior entries persist).

## P4a — HistoricalFidelity (LEMMA, lemma)

`(A (a, d) ∈ R :: (E Σ_k in the transition history : a ∈ ran(M_k(d))))`

*Derivation.* By induction on the transition sequence. *Base:* R₀ = ∅; the quantifier is vacuously satisfied. *Inductive step:* for (a, d) ∈ R' \ R, J1' gives a ∈ ran(M'(d)) \ ran(M(d)) — the post-state Σ' is a witnessing state. For (a, d) ∈ R, the inductive hypothesis provides a prior witnessing state; P2 ensures the entry persists in R'. ∎

## J2 — ContractionIsolation (LEMMA, lemma)

K.μ⁻ as an elementary transition satisfies:

`C' = C ∧ E' = E ∧ R' = R`

Additionally: Contains(Σ') ⊆ Contains(Σ) ⊆ R = R'. No co-occurring transition is needed to maintain any system invariant.

## J3 — ReorderingIsolation (LEMMA, lemma)

K.μ~ as a distinguished composite satisfies:

`C' = C ∧ E' = E ∧ R' = R`

Reordering preserves ran(M(d)), so Contains(Σ') = Contains(Σ). All invariants are trivially maintained; no co-occurring transition is needed.

## J4 — ForkComposite (POST, ensures)

A *fork* of d_src to d_new with precondition d_src ∈ E_doc ∧ M(d_src) ≠ ∅ consists of:

(i) K.δ creating d_new with d_new ∉ E_doc,

(ii) K.μ⁺ populating M'(d_new) with ran(M'(d_new)) ⊆ ran(M(d_src)),

(iii) K.ρ recording provenance for each a ∈ ran(M'(d_new)),

and no other elementary steps.

`dom(C') = dom(C)` — since none of K.δ, K.μ⁺, K.ρ modify C.

`(A a ∈ ran(M'(d_new)) :: (a, d_new) ∈ R')` — follows from J1 applied to the fresh-document case: ran(M'(d_new)) \ ran(M(d_new)) = ran(M'(d_new)), and J1 directly requires provenance recording for each such address.

## P4 — ProvenanceBounds (LEMMA, lemma)

`Contains(Σ) ⊆ R`

*Base case.* In Σ₀, (E₀)_doc = ∅, so Contains(Σ₀) = ∅ ⊆ ∅ = R₀.

*Inductive step.* Assume Contains(Σ) ⊆ R. For every (a, d) ∈ Contains(Σ'):

(i) *Pre-existing containment:* a ∈ ran(M(d)), requiring d ∈ E_doc. Then (a, d) ∈ Contains(Σ) ⊆ R, and P2 gives R ⊆ R', so (a, d) ∈ R'.

(ii) *Newly introduced containment:* a ∈ ran(M'(d)) \ ran(M(d)). J1 requires (a, d) ∈ R'.

In both cases (a, d) ∈ R', so Contains(Σ') ⊆ R'. ∎

## P5 — DestructionConfinement (LEMMA, lemma)

For every state transition Σ → Σ':

(a) `dom(C') ⊇ dom(C) ∧ (A a : a ∈ dom(C) : C'(a) = C(a))`

(b) `E' ⊇ E`

(c) `R' ⊇ R`

The only component that can lose information is M.

*Proof.* By case analysis on the five elementary transitions. K.α extends dom(C) preserving existing entries, with E and R in its frame. K.δ extends E, with C and R in its frame. K.μ⁺ and K.μ⁻ have C, E, and R in their frames. K.ρ extends R, with C and E in its frame. Each preserves (a) through (c). K.μ~ decomposes into K.μ⁻ followed by K.μ⁺, both of which preserve (a)–(c). General composite transitions, being finite sequences of elementary ones, preserve (a)–(c) by transitivity of ⊇ and ∧. ∎

## P6 — ExistentialCoherence (LEMMA, lemma)

`(A a ∈ dom(C) :: origin(a) ∈ E_doc)`

*Derivation.* K.α allocates a under origin(a)'s prefix and requires origin(a) ∈ E_doc as a precondition. P1 preserves entity membership across subsequent transitions; P0 preserves a ∈ dom(C). Initial state: dom(C₀) = ∅, so the quantifier is vacuously satisfied. ∎

## P7 — ProvenanceGrounding (LEMMA, lemma)

`(A (a, d) ∈ R :: a ∈ dom(C))`

*Derivation.* K.ρ requires a ∈ dom(C) as a precondition. P0 preserves dom(C). By induction: initially R₀ = ∅ (vacuous). Each K.ρ adds (a, d) with a ∈ dom(C); P0 ensures a remains in dom(C') for all subsequent states; P2 ensures (a, d) remains in R'. ∎

## P7a — ProvenanceCoverage (LEMMA, lemma)

`(A a ∈ dom(C) :: (E d :: (a, d) ∈ R))`

*Derivation.* By induction. *Base:* dom(C₀) = ∅; vacuous. *Inductive step:* for a ∈ dom(C) (pre-existing), the inductive hypothesis gives (a, d) ∈ R for some d, and P2 preserves it. For a ∈ dom(C') \ dom(C) (freshly allocated), J0 gives a ∈ ran(M'(d)) for some d; since a is fresh, S3 gives a ∉ ran(M(d)) for all d, so a ∈ ran(M'(d)) \ ran(M(d)); J1 gives (a, d) ∈ R'. ∎
