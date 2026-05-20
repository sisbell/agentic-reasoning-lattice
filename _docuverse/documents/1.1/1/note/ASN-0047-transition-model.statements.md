# ASN-0047 Claim Statements

*Source: ASN-0047-transition-model.md (revised 2026-03-22) — Extracted: 2026-05-20*

## Σ.E — EntitySet (DEF, definition)

`Σ.E ⊆ T` — the set of allocated entity addresses. Every e ∈ E satisfies ValidAddress(e). `(A e ∈ E :: ¬IsElement(e))`. Equivalently, `E ⊆ {t : ValidAddress(t) ∧ zeros(t) ≤ 2}`.

Partitioned into:
- `E_node = {e ∈ E : IsNode(e)}`
- `E_account = {e ∈ E : IsAccount(e)}`
- `E_doc = {e ∈ E : IsDocument(e)}`

---

## Σ.R — ProvenanceRelation (DEF, definition)

`Σ.R ⊆ T_elem × E_doc` — where `T_elem = {a ∈ T : IsElement(a)}` (ASN-0045). The pair `(a, d) ∈ R` records that document d has, at some point in the system's history, contained I-address a in its arrangement.

---

## Σ₀ — InitialState (DEF, definition)

The initial state Σ₀ = (C₀, L₀, E₀, M₀, R₀) is:
- `C₀ = ∅`
- `L₀ = ∅`
- `E₀ = {n₀}` where `n₀ = [1]` — the canonical single-component bootstrap node
- `M₀(d) = ∅` for all d — `(E₀)_doc = ∅`, so every arrangement is the empty partial function
- `R₀ = ∅`

**Structural form of n₀:** `zeros(n₀) = 0`, satisfying `IsNode(n₀)` and `ValidAddress(n₀)`.

---

## parent(e) — ParentProjection (DEF, definition)

For `¬IsNode(e)`:
- *Account case* (`IsAccount(e)`): `parent(e) = N(e)` — the node-prefix projection. Since `IsAccount(e)` requires `zeros(e) = 1`, T4b's parse `e = N(e).0.U(e)` is defined with `zeros(N(e)) = 0`, giving `zeros(parent(e)) = 0 = zeros(e) − 1`.
- *Document case* (`IsDocument(e)`): `parent(e) = N(e).0.U(e)` — the account-prefix projection. Since `IsDocument(e)` requires `zeros(e) = 2`, T4b's parse `e = N(e).0.U(e).0.D(e)` is defined with `zeros(N(e).0.U(e)) = 1`, giving `zeros(parent(e)) = 1 = zeros(e) − 1`.

In each case: `zeros(parent(e)) = zeros(e) − 1`.

---

## Contains(Σ) — CurrentContainment (DEF, definition)

`Contains(Σ) = {(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))}`

---

## Contains_C(Σ) — ContentContainment (DEF, definition)

`Contains_C(Σ) = {(a, d) : d ∈ E_doc ∧ (E v : v ∈ dom(M(d)) ∧ subspace(v) = s_C : M(d)(v) = a)}`

---

## Valid composite — ValidComposite (DEF, definition)

A composite transition `Σ →* Σ'` is *valid* iff it is a finite sequence of atomic transitions `Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ'` satisfying two conditions:

(1) *Elementary preconditions:* each step Σᵢ → Σᵢ₊₁ satisfies the precondition of its elementary transition kind, evaluated at the intermediate state Σᵢ.

(2) *Coupling constraints:* J0, J1, and J1' hold for the composite — evaluated between the initial state Σ and the final state Σ'.

---

## K.α — ContentAllocation (TRANSITION, definition)

*First emission* (predicate: `{a' ∈ dom(C) : origin(a') = d} = ∅`): `a = [d.0.s_C.1]`, the determinate first emission of `A_C(d)`.

*Subsequent emission* (predicate: `{a' ∈ dom(C) : origin(a') = d} ≠ ∅`): `a = inc(max{a' ∈ dom(C) : origin(a') = d}, 0)` (TA5(c)).

*Preconditions:* `d ∈ E_doc`; `a ∉ dom(C) ∪ dom(L)`; `zeros(a) = 3 ∧ E(a)₁ = s_C`; `#E(a) ≥ 2`; `origin(a) = d`; `v ∈ Val`.

*Effect:* `C' = C ∪ {a ↦ v}`.

*Frame:* `L' = L; E' = E; (A d :: M'(d) = M(d)); R' = R`.

---

## K.δ — EntityCreation (TRANSITION, definition)

`E' = E ∪ {e}` where `e ∉ E ∧ ValidAddress(e) ∧ ¬IsElement(e)`.

*Case (i) IsNode(e):* Required: `ValidAddress(e) ∧ IsNode(e) ∧ e ∉ E ∧ n₀ ≼ e`. Discharged by NodeUniqueAllocation.

*Case (ii) ¬IsNode(e):* `e = inc(t, k)` for some operand `t` and `k ∈ {0, 1, 2}`. Required uniformly: `parent(e) ∈ E`. Per-sub-case:
- *k = 0 (sibling):* `t ∈ E ∧ ¬IsNode(t) ∧ inc(t, 0) ∉ E`.
- *k = 1 (version):* `t ∈ E_doc`.
- *k = 2 (descent):* `t ∈ E ∧ zeros(t) ≤ 1`.

*Effect on M, per case.* When `IsDocument(e)`: `M'(e) = ∅`, and `M'(d') = M(d')` for every `d' ≠ e`. When `IsAccount(e)` or `IsNode(e)`: `M'(d') = M(d')` for every `d'`.

*Frame:* `C' = C; L' = L; R' = R`.

---

## K.μ⁺ — ArrangementExtension (TRANSITION, definition)

`dom(M'(d)) ⊃ dom(M(d)) ∧ (A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))`

*Precondition:* `d ∈ E_doc`; for every new mapping `M'(d)(v) = a`, `a ∈ dom(C)` (S3, since K.μ⁺'s frame holds `C' = C`); new V-positions satisfy S8a and S8-depth; `dom(M'(d))` is finite (S8-fin); M'(d) satisfies D-CTG and D-MIN; newly added V-positions `{v_1, …, v_k} := dom(M'(d)) ∖ dom(M(d))` are pairwise distinct.

*Frame:* `C' = C; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R`.

---

## K.μ⁻ — ArrangementContraction (TRANSITION, definition)

`dom(M'(d)) ⊂ dom(M(d)) ∧ (A v : v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v))`

*Precondition:* `d ∈ E_doc`; `dom(M(d)) ≠ ∅`; per-subspace suffix-prefix retention: for each `S ∈ {s_C, s_L}`, caller selects retention count `n'_S ∈ {0, 1, ..., n_S}` with `(E S :: n'_S < n_S)`. The contracted arrangement: `M'(d) = M(d) ↾ R` where `R := ∪_{S ∈ {s_C, s_L}} {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}`.

*Frame:* `C' = C; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d'))`.

---

## K.μ~ — ArrangementReordering (TRANSITION, definition)

For `d ∈ E_doc` with `|dom_C(M(d))| ≥ 2`, K.μ~ realises the *bijection equation*:

`(E π : π is a bijection dom(M(d)) → dom(M'(d)) : (A v ∈ dom(M(d)) :: M'(d)(π(v)) = M(d)(v)))`

π is admissible iff (i) the induced post-state M'(d) satisfies S8a, S8-depth, D-CTG★, D-MIN★, and S3★, and (ii) `π ≠ id`.

*Preconditions:* `d ∈ E_doc`; `|dom_C(M(d))| ≥ 2`.

*Frame (derived):* `C' = C; E' = E; R' = R; L' = L; (A d' : d' ≠ d : M'(d') = M(d'))`.

---

## K.λ — LinkAllocation (TRANSITION, definition)

*First emission* (predicate: `{ℓ' ∈ dom(L) : origin(ℓ') = d} = ∅`): `ℓ = [d.0.s_L.1]`, the determinate first emission of `A_L(d)`.

*Subsequent emission* (predicate: `{ℓ' ∈ dom(L) : origin(ℓ') = d} ≠ ∅`): `ℓ = inc(max{ℓ' ∈ dom(L) : origin(ℓ') = d}, 0)` (TA5(c)).

*Preconditions:* `d ∈ E_doc`; `ℓ ∉ dom(L) ∪ dom(C)`; `zeros(ℓ) = 3 ∧ E(ℓ)₁ = s_L`; `#E(ℓ) ≥ 2`; `origin(ℓ) = d`; `N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅`.

*Effect:* `L' = L ∪ {ℓ ↦ (e₁, …, eₙ)}`.

*Frame:* `C' = C; E' = E; (A d' :: M'(d') = M(d')); R' = R`.

---

## K.ρ — ProvenanceRecording (TRANSITION, definition)

`R' = R ∪ {(a, d)}` where `a ∈ dom(C) ∧ d ∈ E_doc`.

*Precondition:* `a ∈ dom(C)` ∧ `d ∈ E_doc`.

*Frame:* `C' = C; E' = E; (A d :: M'(d) = M(d))`.

---

## K.μ⁺_L — LinkSubspaceExtension (TRANSITION, definition)

*Precondition:*
- `d ∈ E_doc`
- `ℓ ∈ dom(L)` (the target link must already exist in dom(L) — placed there by some prior K.λ)
- `origin(ℓ) = d` (only home-document links may be arranged)
- `ℓ ∉ ran(M(d))` (the link is not already arranged at any V-position in d's arrangement — first-arrangement constraint)
- V-position `v_ℓ` satisfies: `subspace(v_ℓ) = s_L`; `m_L = 2` (supplied by LinkVPositionDepthAxiom); if `V_{s_L}(d) = ∅`: `v_ℓ` is the minimum position `[s_L, 1, ..., 1]` of depth `m_L` (D-MIN★); if `V_{s_L}(d) ≠ ∅`: `v_ℓ = shift(max(V_{s_L}(d)), 1)` (D-CTG★); `#v_ℓ = m_L`.

*Effect:* `M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}`, with `dom(M'(d)) = dom(M(d)) ∪ {v_ℓ} ⊃ dom(M(d))`.

*Frame:* `C' = C; L' = L; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R`.

---

## K.μ~-FIX — DomainFixity (LEMMA, lemma)

`dom(M'(d)) = dom(M(d))`.

D-SEQ★ at the pre- and post-states gives `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` and `V_S(d') = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}` for each subspace S; since π is a bijection and (by subspace preservation) bijects `V_S(d)` onto `V_S(d')`, `n'_S = n_S` and `V_S(d') = V_S(d)`. So π is a permutation of `dom(M(d))`.

---

## J0 — AllocationRequiresPlacement (COUPLING, predicate)

`(A Σ →* Σ', a : a ∈ dom(C') \ dom(C) : (E d, v : d ∈ E'_doc ∧ v ∈ dom(M'(d)) : M'(d)(v) = a))`

---

## J1 — ExtensionRecordsProvenance (COUPLING, predicate)

`(A Σ →* Σ', d ∈ E'_doc, a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R')`

---

## J1' — ProvenanceRequiresExtension (COUPLING, predicate)

`(A Σ →* Σ', a, d ∈ E'_doc : (a, d) ∈ R' \ R : a ∈ ran(M'(d)) \ ran(M(d)))`

---

## J2 — ContractionIsolation (COUPLING, predicate)

`C' = C ∧ L' = L ∧ E' = E ∧ R' = R`

(K.μ⁻ as elementary transition requires no coupling with respect to P0–P2, L12, and `Contains(Σ) ⊆ R`.)

---

## J3 — ReorderingIsolation (COUPLING, predicate)

`C' = C ∧ L' = L ∧ E' = E ∧ R' = R`

(K.μ~ as named composite requires no coupling; reordering preserves `ran(M(d))`, so `Contains(Σ') = Contains(Σ)`.)

---

## J4 — ForkComposite (DEF, definition)

A *fork* of `d_src` to `d_new` is a composite transition `Σ →* Σ'`, with *precondition* `d_src ∈ E_doc ∧ V_{s_C}(d_src) ≠ ∅`, consisting of:

(i) K.δ case (ii) with k = 1 and t = d_src, producing `d_new = inc(d_src, 1)` with `d_new ∉ E_doc`,

(ii) K.μ⁺ populating `M'(d_new)` from `d_src`'s content subspace under transclusion: `ran(M'(d_new)) ⊆ ran(M(d_src)|_{V_{s_C}(d_src)})` — no new content addresses are introduced, every target lies in the pre-existing content store,

(iii) K.ρ recording provenance for each `a ∈ ran(M'(d_new))`,

and no other elementary steps.

---

## P1 — EntityPermanence (INV, predicate)

`(A Σ → Σ' :: E ⊆ E')`

Uniformly across levels:
- `[e ∈ E ∧ IsNode(e) ⟹ e ∈ E']`
- `[e ∈ E ∧ IsAccount(e) ⟹ e ∈ E']`
- `[e ∈ E ∧ IsDocument(e) ⟹ e ∈ E']`

---

## P2 — ProvenancePermanence (INV, predicate)

`(A Σ → Σ' :: R ⊆ R')`

---

## P4 — ProvenanceBounds (INV, predicate)

`Contains(Σ) ⊆ R`

---

## P4a — HistoricalFidelity (INV, predicate)

`(A (a, d) ∈ R :: (E Σ_k in the transition history : (E v ∈ dom(M_k(d)) : subspace(v) = s_C ∧ M_k(d)(v) = a)))`

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

## LinkVPositionDepthAxiom — FixedLinkVPositionDepth (AXIOM, axiom)

`(A d ∈ E_doc :: m_L = 2)` — every link-subspace V-position has depth 2.

---

## NodeUniqueAllocation — FreshNodeAddress (AXIOM, axiom)

Every K.δ node-allocation event — every elementary transition of K.δ whose effect places an entity `e` with `IsNode(e)` into E — produces an address satisfying three conditions:

(a) *Freshness:* `e ∉ Σ.E` at the state Σ of allocation;

(b) *Bootstrap lineage:* `n₀ ≼ e` under the tumbler-prefix order;

(c) *Registry tracking:* for every reachable state Σ and every `t ∈ Σ.E_node`, `t` inhabits the external node-allocation registry's tracked domain.

---

## NodeRegistryBootstrap — BootstrapRegistrySeeding (AXIOM, axiom)

At the initial state `Σ₀`, `n₀` is committed to the node-allocation protocol's tracked domain.

---

## FrontierEquivalence — FrontierEquivalence (LEMMA, lemma)

For every reachable state `Σ` and every operand `t ∈ Σ.E` with `¬IsNode(t)`:

`inc(t, 0) ∉ Σ.E ⟺ t is the frontier of its sub-allocator's (t, 0)-branch`

Three load-bearing premises:
(i) T10a chain-advancement uniqueness at `(t, 0)` (derived from TA5(c) functional determinism + P1 + operational precondition; T10a.7 plays only a framing role);
(ii) P1 (E-monotonicity): any prior firing of `(t, 0)` would have placed its output permanently in E;
(iii) T10a GlobalUniqueness (via T10a.6 cross-allocator domain-disjointness): no allocator other than t's own sub-allocator can produce `inc(t, 0)`.

---

## NodeLineage — NodeDescentFromBootstrap (INV, predicate)

`(A e ∈ E : IsNode(e) : n₀ ≼ e)`

where `≼` is the prefix order on tumblers (ASN-0034).

---

## GlobalLineage — GlobalDescentFromBootstrap (COROLLARY, lemma)

`(A x ∈ E ∪ dom(C) ∪ dom(L) :: n₀ ≼ x)`

---

## b_C(d), b_L(d) — SubAllocatorAnchors (DEF, definition)

`b_C(d) := [d.0.s_C]` (single-component element field with E₁ = s_C; zeros = 3, #E = 1) — the **content sub-allocator anchor**.

`b_L(d) := [d.0.s_L]` (single-component element field with E₁ = s_L; zeros = 3, #E = 1) — the **link sub-allocator anchor**.

Under SubspaceConventionAxiom (`s_C = 1`, `s_L = 2`): `b_C(d) = inc(d, 2) = [d.0.1]` and `b_L(d) = inc(b_C(d), 0) = [d.0.2]`. The anchors are not in `dom(C) ∪ dom(L)` — content addresses have `#E ≥ 2` (S7c), link addresses have `#E ≥ 2` (L1b), and the anchors have `#E = 1`.

---

## Allocator hierarchy — AllocatorHierarchy (DEF, definition)

For each `d ∈ E_doc`:

- `A_C(d)` — d's **content sub-allocator**, anchor `b_C(d) = [d.0.s_C]`, first emission `[d.0.s_C.1]`. Outputs `a` satisfy `a ∈ dom(C)`, `subspace_I(a) = s_C`, `origin(a) = d`, `zeros(a) = 3`.
- `A_L(d)` — d's **link sub-allocator**, anchor `b_L(d) = [d.0.s_L]`, first emission `[d.0.s_L.1]`. Outputs `ℓ` satisfy `ℓ ∈ dom(L)`, `subspace_I(ℓ) = s_L`, `origin(ℓ) = d`, `zeros(ℓ) = 3`.
- `A_v(d)` — d's **version sub-allocator**; first emission `inc(d, 1)`, subsequent emissions `inc(prev_version, 0)`. Outputs inhabit `E_doc`.
- `A_doc(A)` — account A's **document sub-allocator**; first emission `inc(A, 2)`. Outputs inhabit `E_doc`.
- `A_account(N)` — node N's **account sub-allocator**; first emission `inc(N, 2)`. Outputs inhabit `E_account`.

T10a-conformance applies to each frontier separately; cross-document collisions prevented by T10; cross-subspace by L14.

---

## S3★-aux — SubspaceExhaustiveness (INV, predicate)

`(A d, v : v ∈ dom(M(d)) : subspace(v) = s_C ∨ subspace(v) = s_L)`

---

## CL-OWN — LinkSubspaceOwnership (INV, predicate)

`(A d, v : v ∈ dom(M(d)) ∧ subspace(v) = s_L : origin(M(d)(v)) = d)`

---

## CL-UNIQ — LinkSubspacePositionUniqueness (INV, predicate)

`(A d, v₁, v₂ : v₁ ∈ dom(M(d)) ∧ v₂ ∈ dom(M(d)) ∧ subspace(v₁) = s_L ∧ subspace(v₂) = s_L ∧ M(d)(v₁) = M(d)(v₂) : v₁ = v₂)`

Equivalently, `M(d)|_{dom_L}` is a partial injection from V-positions to link addresses.

---

## K.δ-ID.zeros-0/1 — KDeltaZerosK01 (LEMMA, lemma)

`zeros(e) = zeros(t)` for k ∈ {0, 1} on `e = inc(t, k)`.

*Derivation:* TA5(c) preserves zeros for k = 0; TA5(d) at k = 1 appends a final `1` with no new zero, so zeros is preserved.

---

## K.δ-ID.zeros-2 — KDeltaZerosK2 (LEMMA, lemma)

`zeros(e) = zeros(t) + 1` for k = 2 on `e = inc(t, 2)`.

*Derivation:* TA5(d) at k = 2 appends one zero separator and a final `1`.

---

## K.δ-ID.parent-0/1 — KDeltaParentK01 (LEMMA, lemma)

`parent(e) = parent(t)` for k ∈ {0, 1} on `e = inc(t, k)`.

*Derivation:* k = 0 leaves the trailing-component position unchanged; k = 1 extends by one non-zero component without crossing a zero separator; in either case T4b's truncation past the last separator yields the same prefix.

---

## K.δ-ID.parent-2 — KDeltaParentK2 (LEMMA, lemma)

`parent(e) = t` for k = 2 on `e = inc(t, 2)`.

*Derivation:* k = 2 introduces a new zero separator immediately after t, making t itself the parent prefix under T4b.

---

## SequentialTransitionAxiom — SequentialAtomicTransitions (AXIOM, axiom)

The transition relation `Σ → Σ'` is single-event sequential: each transition is an atomic, uninterruptible event in which the elementary precondition is evaluated against `Σ` and the elementary effect is committed to `Σ'` in one indivisible step, and transitions are totally ordered (no two transitions overlap in time). The system admits no intermediate state in which a transition has begun but not yet committed.

---

## SubspaceConventionAxiom — FixedSubspaceIdentifiers (AXIOM, axiom)

`s_C = 1 ∧ s_L = 2`.

The distinctness consequence `s_C ≠ s_L` is abbreviated **SC-NEQ**.

---

## SubAllocatorAxiom — ContentLinkSubAllocatorExistence (AXIOM, axiom)

For each `d ∈ E_doc`, the entity-allocation event placing d into E_doc activates a content sub-allocator `A_C(d)` with anchor `b_C(d) = [d.0.s_C]` and a link sub-allocator `A_L(d)` with anchor `b_L(d) = [d.0.s_L]`. Five sub-clauses:

**(a) SubAllocatorAxiom.Subspace.** Every `a` emitted by `A_C(d)` has `subspace_I(a) = s_C`; every `ℓ` emitted by `A_L(d)` has `subspace_I(ℓ) = s_L`.

**(b) SubAllocatorAxiom.FirstEmission.** The first emission of each is the determinate tumbler `[d.0.s_C.1]` (resp. `[d.0.s_L.1]`), satisfying `a ∉ dom(Σ.C) ∪ dom(Σ.L)` at the state of allocation with `origin(a) = d` and `#E(a) = 2`.

**(c) SubAllocatorAxiom.Namespace.** Every output of d's sub-allocators is T4-valid with `zeros(·) = 3`.

**(d) SubAllocatorAxiom.T10aConformance.** `A_C(d)` and `A_L(d)` are T10a-conforming allocators within d's allocator subtree, activated by the K.δ event for `d` as the joint T2-spawn step.

**(e) SubAllocatorAxiom.Disjointness.** `dom(A_C(d)) ∩ dom(A_L(d)) = ∅`, and for any `d ≠ d'`: `dom(A_C(d)) ∩ dom(A_C(d')) = ∅`, `dom(A_L(d)) ∩ dom(A_L(d')) = ∅`, `dom(A_C(d)) ∩ dom(A_L(d')) = ∅`.

---

## L0 — SubspacePartition (INV, predicate)

Both clauses are foundation invariants:

`(A a ∈ dom(Σ.L) :: subspace_I(a) = s_L)`

`(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)`

---

## L3 — NEndsetStructure (INV, predicate)

`(A a ∈ dom(Σ.L) :: |Σ.L(a)| ≥ 3 ∧ (A i : 1 ≤ i ≤ |Σ.L(a)| : Σ.L(a).eᵢ ∈ Endset) ∧ Σ.L(a).e₃ ≠ ∅)`

---

## C-fin — ContentStoreFiniteness (INV, predicate)

`|dom(Σ.C)| < ∞`

---

## L1c — LinkAllocatorConformance (INV, predicate)

Every `ℓ ∈ dom(L)` is reachable from a T4-valid document-level seed `s` (`zeros(s) = 2`) by a finite sequence `(t₀, …, tₙ)` with `t₀ = origin(ℓ)`, `tₙ = ℓ`, each step `tᵢ = inc(tᵢ₋₁, kᵢ)` with `kᵢ ∈ {0, 1, 2}` satisfying T10a's per-step admissibility (T4-validity preservation, zeros bound at `kᵢ = 2`), `k₁ = 2`, and `#tᵢ > #origin(ℓ)` at every step `i ≥ 1`.

---

## P0 — ContentPermanence (INV, predicate)

`(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ (A a : a ∈ dom(C) : C'(a) = C(a)))`

C is *append-only with immutable values*. (Subsumes ASN-0036's S0 and S1.)

---

## L14 — StoreDisjointness (INV, predicate)

`dom(Σ.C) ∩ dom(Σ.L) = ∅`

Derived from L0 and SC-NEQ: if `a ∈ dom(C)` then `subspace_I(a) = s_C`, and if `a ∈ dom(L)` then `subspace_I(a) = s_L`; since `s_C ≠ s_L`, no single tumbler can inhabit both domains.

---

## L14a — L14aSuperseded (NOTE, note)

ASN-0043's L14a (`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∉ dom(Σ.L))`) is *superseded by* S3★ + CL-OWN in the extended state. S3★ permits link-subspace V→I mappings by routing them into `dom(L)`, and CL-OWN constrains such mappings to the home document. In the link-subspace-permitting state, `S3★ + CL-OWN ⟹ ¬L14a`.

---

## S3★ — GeneralizedReferentialIntegrity (INV, predicate)

`(A d, v : v ∈ dom(Σ.M(d)) : (subspace(v) = s_C ⟹ Σ.M(d)(v) ∈ dom(Σ.C)) ∧ (subspace(v) = s_L ⟹ Σ.M(d)(v) ∈ dom(Σ.L)))`

where `subspace(v)` denotes the first component of the V-position. Supersedes S3 (ASN-0036).

---

## D-CTG★ — PerSubspaceContiguity (INV, predicate)

`(A d, S : V_S(d) ≠ ∅ : V_S(d) is contiguous under the V-ordering on subspace S)`

where *contiguous* unpacks as: for every `v_lo, v_hi ∈ V_S(d)` and every depth-m_S positive tuple `z` with subspace identifier S and `v_lo ≤ z ≤ v_hi` under the V-ordering, `z ∈ V_S(d)`.

The *V-ordering on subspace S* is the restriction of T1 (LexicographicOrder, ASN-0034) to the depth-m_S positive-component tuples whose first component is S.

---

## D-MIN★ — PerSubspaceMinimumPosition (INV, predicate)

`(A d, S : V_S(d) ≠ ∅ : min(V_S(d)) = [S, 1, ..., 1] of depth m_S)`

---

## D-SEQ★ — PerSubspaceSequentialPositions (INV, predicate)

For each non-empty subspace S in M(d):

`V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` for some `n_S ≥ 1`,

where the inner positions are of uniform depth m_S (the common depth within subspace S, by S8-depth), and `n_S = |V_S(d)|`.

Derived from D-CTG★ + D-MIN★ + S8-depth + S8-fin + S8a.

---

## P3 — ArrangementMutabilityOnly (INV, predicate)

`(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ dom(L) ⊆ dom(L') ∧ E ⊆ E' ∧ R ⊆ R' ∧ (A a ∈ dom(C) :: C'(a) = C(a)) ∧ (A ℓ ∈ dom(L) :: L'(ℓ) = L(ℓ)))`

Synthesises P0 ∧ P1 ∧ P2 ∧ L12. The only component that can lose information is M.

---

## P4★ — ProvenanceBoundsContentSubspace (INV, predicate)

`Contains_C(Σ) ⊆ R`

Supersedes P4 for the extended state. In pre-extension states (no link-subspace mappings), `Contains_C(Σ) = Contains(Σ)`, so P4★ reduces to P4.

---

## J1★ — ExtensionRecordsProvenanceContentSubspace (COUPLING, predicate)

`(A Σ →* Σ', d ∈ E'_doc, a : (E v ∈ dom(M'(d)) : subspace(v) = s_C ∧ M'(d)(v) = a) ∧ ¬(E v ∈ dom(M(d)) : subspace(v) = s_C ∧ M(d)(v) = a) : (a, d) ∈ R')`

Supersedes J1 in the extended state; range-based content-subspace scoping.

---

## J1'★ — ProvenanceRequiresExtensionContentSubspace (COUPLING, predicate)

`(A Σ →* Σ', a, d : (a, d) ∈ R' \ R : (E v ∈ dom(M'(d)) : subspace(v) = s_C ∧ M'(d)(v) = a) ∧ ¬(E v ∈ dom(M(d)) : subspace(v) = s_C ∧ M(d)(v) = a))`

Supersedes J1' in the extended state; range-based content-subspace scoping.

---

## ValidComposite★ — ValidCompositeAmended (DEF, definition)

A composite transition `Σ →* Σ'` in the extended state `Σ = (C, L, E, M, R)` is *valid* iff it is a finite sequence of atomic transitions `Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ'` — drawn from K.α (amended), K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻ (amended), K.μ~, and K.ρ — satisfying:

1. *Transition preconditions.* Each step `Σᵢ → Σᵢ₊₁` satisfies the elementary precondition of its transition kind, evaluated at the intermediate state `Σᵢ`. K.μ~ appearing in the sequence is shorthand for its K.μ⁻ + K.μ⁺ decomposition; its existence condition `|dom_C(M(d))| ≥ 2` is necessary and sufficient for admissibility clause (ii).

2. *Coupling constraints.* J0, J1★, and J1'★ hold for the composite as a whole — evaluated only between the initial state Σ and the final state Σ'.

Supersedes ValidComposite.

---

## S8★ — PerSubspaceSpanDecomposition (INV, predicate)

For each `d ∈ E_doc` and each subspace `S ∈ {s_C, s_L}`, the per-subspace arrangement `M(d)|_{V_S(d)}` decomposes into a finite set of correspondence runs `{(v_j, a_j, n_j)}` satisfying ASN-0036's S8 conditions (a) and (b) applied to the projected arrangement:

- *Content subspace.* `M(d)|_{V_{s_C}(d)} : V_{s_C}(d) → dom(C)` is a direct application of ASN-0036's S8 (S3★ restricted to `V_{s_C}(d)` is exactly S3 with target `dom(C)`).
- *Link subspace.* `M(d)|_{V_{s_L}(d)} : V_{s_L}(d) → dom(L)` is discharged by the *trivial length-1 decomposition* `{(v, M(d)(v), 1) : v ∈ V_{s_L}(d)}` — every link-subspace V-position constitutes its own length-1 correspondence run. S8's condition (a) holds by construction; condition (b) at `k = 0` reduces to `M(d)(v) = M(d)(v)` under the convention `shift(t, 0) := t`.

---

## ExtendedReachableStateInvariants — ExtendedReachableStateInvariants (THEOREM, lemma)

Every state reachable from Σ₀ by a finite sequence of valid composite transitions satisfies the *per-state invariants* (Class (a) — preserved by each elementary transition):

S2 ∧ S3★ ∧ S3★-aux ∧ S4 ∧ S7a ∧ S7b ∧ S7c ∧ S7d ∧ S8a ∧ S8-fin ∧ S8-depth ∧ S8★ ∧ C-fin ∧ D-CTG★ ∧ D-MIN★ ∧ D-SEQ★ ∧ P6 ∧ P7 ∧ P8 ∧ NodeLineage ∧ L0 ∧ L1 ∧ L1a ∧ L1b ∧ L1c ∧ L3 ∧ L14 ∧ L-fin ∧ CL-OWN ∧ CL-UNIQ

Every state at a composite boundary additionally satisfies the *composite-boundary properties* (Class (b) — discharged at boundaries by J0/J1★/J1'★):

P4★ ∧ P4a ∧ P7a

---

## ExtendedTransitionInvariants — ExtendedTransitionInvariants (THEOREM, lemma)

Every valid composite transition `Σ →* Σ'` satisfies:

P3

where P3 is the conjunction `P0 ∧ P1 ∧ P2 ∧ L12` (which subsumes ASN-0036's S0 and S1 via P0 and extends ASN-0043's L12). S9 (TwoStreamSeparation, ASN-0036) follows from P0 unconditionally.

---

## K.α's `E(a)₁ = s_C` precondition — KAlphaContentSubspacePrecondition (PRE, requires)

The precondition `E(a)₁ = s_C` (equivalently `subspace_I(a) = s_C`) is inherited from ASN-0093's K.α directly — not a local amendment. It pins every newly allocated content address to the content subspace, preserving L0's C-clause and L14 in the extended state.

---

## K.μ⁺ amendment — KMuPlusContentSubspaceRestriction (DEF, definition)

K.μ⁺ is amended with a content-subspace restriction: new V-positions must satisfy `subspace(v) = s_C`.

This partitions arrangement extensions by subspace with K.μ⁺_L. Without this restriction, K.μ⁺ could create a link-subspace V-position mapping to `dom(C)`, violating S3★. Existing D-CTG and D-MIN postconditions carry forward, now strengthened to D-CTG★ / D-MIN★.

---

## K.μ⁻ (per-subspace scope) — KMuMinusPerSubspaceScope (DEF, definition)

In the extended state, K.μ⁻'s D-CTG / D-MIN postconditions read as D-CTG★ / D-MIN★ (the per-subspace forms), and the constructive per-subspace retention precondition applies independently to each subspace under the D-SEQ★ enumeration `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}`.

Per-subspace consequence of the strict-contraction clause: `(E S ∈ {s_C, s_L} : V_S(d) ≠ ∅ : n'_S < n_S)` — at least one subspace shrinks strictly.
