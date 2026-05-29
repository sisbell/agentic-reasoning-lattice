# ASN-0036 Claim Statements

*Source: ASN-0036-strand-model.md (revised 2026-05-29) — Extracted: 2026-05-29*

## Σ.C — ContentStore (DEF, partial function)

- *Axiom:* `Σ.C : T ⇀ Val` — the content store is a partial function from tumblers to content values.
- *Definition:* `dom(Σ.C) = {a ∈ T : Σ.C(a) is defined}` — the set of I-addresses at which content has been stored.

`T` is the set of tumblers (ASN-0034); `Val` is an unspecified set of content values, opaque at this level of abstraction.

---

## Σ.M(d) — Arrangement (DEF, partial function)

- *Axiom:* `Σ.M(d) : T ⇀ T` — the arrangement of document `d` is a partial function from V-position tumblers to I-address tumblers.
- *Axiom (domain restriction):* `dom(Σ.M(d)) ⊆ {t ∈ T : zeros(t) = 0 ∧ #t ≥ 2}` — arrangements map only V-positions; every active key is a zero-free tumbler of depth at least 2.
- *Definition:* `dom(Σ.M(d)) = {v ∈ T : Σ.M(d)(v) is defined}` — the set of V-positions currently active in `d`.
- *Definition:* `ran(Σ.M(d)) = {Σ.M(d)(v) : v ∈ dom(Σ.M(d))}` — the set of I-addresses that `d` currently references.

---

## S0 — ContentImmutability (INV, axiom)

For every state transition `Σ → Σ'`:

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)]`

- *Axiom (design requirement):* `(A a : a ∈ dom(Σ.C) : a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))`.
- *Postconditions:* (a) Domain persistence — `a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)`. (b) Value preservation — `a ∈ dom(Σ.C) ⟹ Σ'.C(a) = Σ.C(a)`.
- *Frame:* No condition on arrangements — the postcondition holds for arbitrary `Σ'.M(d)` and arbitrary changes to any document's arrangement.

---

## S1 — StoreMonotonicity (LEMMA, from S0)

`[dom(Σ.C) ⊆ dom(Σ'.C)]`

- *Preconditions:* State transition `Σ → Σ'` in a system satisfying S0 (content immutability).
- *Postconditions:* `dom(Σ.C) ⊆ dom(Σ'.C)`.

*Proof sketch:* Let `a ∈ dom(Σ.C)` be arbitrary. By S0, `a ∈ dom(Σ.C)` implies the conjunction `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`. The first conjunct yields `a ∈ dom(Σ'.C)` directly. Since `a` was chosen arbitrarily, `dom(Σ.C) ⊆ dom(Σ'.C)`.

---

## S2 — ArrangementFunctionality (INV, axiom)

Each V-position maps to exactly one I-address, by the `Σ.M(d) : T ⇀ T` partial-function declaration:

`(A d, v, a₁, a₂ : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a₁ ∧ Σ.M(d)(v) = a₂ : a₁ = a₂)`

- *Postconditions:* `ran(Σ.M(d)) = {Σ.M(d)(v) : v ∈ dom(Σ.M(d))}` is a well-defined set.

---

## S3 — ReferentialIntegrity (INV, design)

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`

- *Axiom (well-formedness invariant):* In every state `Σ`, `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))` — equivalently, `ran(Σ.M(d)) ⊆ dom(Σ.C)`.
- *Preservation across transitions:* For an operation that adds a V-mapping `M(d)(v) = a`, the post-state must satisfy `a ∈ dom(Σ'.C)`.
- *Frame:* S3 asserts `ran(M(d)) ⊆ dom(C)` only; the converse `dom(C) ⊆ ⋃_d ran(M(d))` is not asserted.
- *Depends:* S1 (store monotonicity) — once a reference is valid, S1 prevents the target from being removed.

---

## S4 — OriginBasedIdentity (LEMMA, from GlobalUniqueness)

For I-addresses `a₁`, `a₂` produced by distinct allocation events:

`a₁ ≠ a₂`

regardless of whether `Σ.C(a₁) = Σ.C(a₂)`.

- *Preconditions:* `a₁, a₂ ∈ dom(Σ.C)` produced by distinct allocation events within a system conforming to T10a (allocator discipline, ASN-0034).
- *Postconditions:* `a₁ ≠ a₂`, regardless of whether `Σ.C(a₁) = Σ.C(a₂)`.
- *Frame:* The content store `C` and value domain `Val` play no role — distinctness is a property of the addressing scheme alone.

---

## S5 — UnrestrictedSharing (LEMMA, consistent with S0–S3)

The same I-address may appear in the ranges of multiple arrangements, and at multiple V-positions within a single arrangement. S0–S3 are consistent with any finite sharing multiplicity — they place no constraint on `|{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}|`:

`(A N ∈ ℕ :: (E Σ :: Σ satisfies S0–S3 ∧ (E a ∈ dom(Σ.C) :: |{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N)))`

- *Preconditions:* `N ∈ ℕ` arbitrary.
- *Postconditions:* There exists a state `Σ` satisfying S0–S3 such that for some `a ∈ dom(Σ.C)`, `|{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N`. The construction works both across documents (multiplicity `N + 1` over `N + 1` documents) and within a single document (multiplicity `N + 1` at `N + 1` distinct V-positions).
- *Depends:* S0, S1, S2, S3, T3 (ASN-0034).

---

## S7a — DocumentScopedAllocation (INV, design)

Every Istream address is allocated under the tumbler prefix of the document that created it. That is, for every `a ∈ dom(Σ.C)`, the document-level prefix of `a` — the tumbler `N(a).0.U(a).0.D(a)` obtained by truncating the element field, where `N(a)`, `U(a)`, `D(a)` are the partial projections supplied by T4b (UniqueParse, ASN-0034) — identifies the document whose owner performed the allocation that placed `a` into `dom(C)`.

- *Axiom (design requirement):* `(A a : a ∈ dom(Σ.C) :: the document-level prefix N(a).0.U(a).0.D(a) is the tumbler of the document whose owner performed the allocation that placed a into dom(C))`. By S7b, every `a ∈ dom(Σ.C)` satisfies `zeros(a) = 3`, so T4b's projections `N(a)`, `U(a)`, `D(a)` are everywhere defined on the domain over which the axiom quantifies.
- *Depends:* T4 (HierarchicalParsing, ASN-0034); T4b (UniqueParse, ASN-0034); S7b; T10a (AllocatorDiscipline, ASN-0034); T10a.4 (T4PreservationUnderDiscipline, ASN-0034).

---

## S7b — ElementLevelIAddresses (INV, design)

`(A a ∈ dom(Σ.C) :: zeros(a) = 3)`

- *Axiom (design requirement):* `(A a ∈ dom(Σ.C) :: zeros(a) = 3)`.
- *Postconditions:* By T4's field correspondence, all four identifying fields — node, user, document, element — are present and the element field exists. The projections `N(a)`, `U(a)`, `D(a)`, `E(a)` supplied by T4b are all well-defined.
- *Depends:* T4 (HierarchicalParsing, ASN-0034); T4b (UniqueParse, ASN-0034); T10a.4 (T4PreservationUnderDiscipline, ASN-0034).

---

## S7d — DocumentAllocationDiscipline (INV, design)

Every document is addressed by a document-level tumbler (`zeros = 2`) arising from an allocation event under T10a's allocator discipline (ASN-0034). Distinct documents arise from distinct allocation events.

- *Axiom (design requirement):* Every document tumbler `d` satisfies `zeros(d) = 2` and is the result of an allocation event under T10a; distinct documents arise from distinct allocation events.
- *Postconditions:* By GlobalUniqueness (ASN-0034), distinct documents have distinct document-level tumblers.
- *Depends:* T10a (AllocatorDiscipline, ASN-0034); T10a.4 (T4PreservationUnderDiscipline, ASN-0034); T4 (HierarchicalParsing, ASN-0034); GlobalUniqueness (ASN-0034).

---

## S7 — StructuralAttribution (LEMMA, from S7a/S7b/S7d/S0/S4)

For every `a ∈ dom(Σ.C)`, define the *origin* as the document-level prefix obtained by truncating the element field:

`origin(a) = N(a).0.U(a).0.D(a)`

This is the full document tumbler `N.0.U.0.D` — uniquely identifying the allocating document across the system. Since I-addresses are permanent (S0) and unique (S4), this attribution is permanent and unseverable.

- *Preconditions:* `a ∈ dom(Σ.C)` in a system conforming to S7a, S7b, S7d, T4, T4b, T10a, T10a.4 (ASN-0034). The strict equality `zeros(a) = 3` comes from S7b axiomatically.
- *Postconditions:* (a) `origin(a)` is well-defined and is a document-level tumbler with `zeros(origin(a)) = 2`. (b) `origin(a)` is the tumbler of the document that allocated `a`. (c) For `a₁, a₂` allocated under distinct documents, `origin(a₁) ≠ origin(a₂)`. (d) `origin(a)` is invariant across all states in which `a ∈ dom(Σ.C)`.
- *Frame:* The content values `Σ.C(a)` and arrangement functions `Σ.M(d)` play no role — attribution is a property of the addressing scheme alone.

---

## S8-fin — FiniteArrangement (INV, design)

For each document `d`, `dom(Σ.M(d))` is finite.

- *Axiom (design requirement):* For every state `Σ` and document `d`, `dom(Σ.M(d))` is a finite set.
- *Postconditions:* `|dom(Σ.M(d))| < ∞`. Consequently `ran(Σ.M(d))` is finite (image of a finite set under a function).
- *Frame:* No constraint on the unbounded growth of `dom(C)`; only individual arrangements are required to be finite at any given state.

---

## Definition — DomainRestriction

`dom(Σ.M(d)) ⊆ {t ∈ T : zeros(t) = 0 ∧ #t ≥ 2}` — arrangements map only V-positions; every active key is a zero-free tumbler of depth at least 2 (a subspace identifier followed by a within-subspace ordinal).

---

## S8a — VPositionPositivityAndDepth (INV, from domain-restriction axiom)

By T0, `zeros(v) = 0` holds exactly when every component is positive, so the domain-restriction axiom on `Σ.M(d)` yields, for every active V-position:

`(A v ∈ dom(Σ.M(d)) :: #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))`

---

## Definition — Subspace

For any tumbler `v` of depth `#v ≥ 1`, define:

`subspace(v) = v₁`

extracting the subspace identifier as the first component of a V-position.

- *Signature:* `subspace : T → ℕ` — projects the first component of a tumbler.
- *Preconditions:* `v ∈ T`, `#v ≥ 1` (so that `v₁` is well-defined as the first component of a non-empty tumbler).
- *Definition:* `subspace(v) = v₁`.

---

## S8-depth — FixedDepthVPositions (INV, design)

Within a given subspace `s` of document `d`, all V-positions share the same tumbler depth:

`(A d, u, w : u ∈ dom(Σ.M(d)) ∧ w ∈ dom(Σ.M(d)) ∧ subspace(u) = subspace(w) : #u = #w)`

- *Axiom (design requirement):* `(A d, u, w : u ∈ dom(Σ.M(d)) ∧ w ∈ dom(Σ.M(d)) ∧ subspace(u) = subspace(w) : #u = #w)`.
- *Postconditions:* Within a subspace `s` of document `d`, if `V_s(d) ≠ ∅` then there exists a common depth `m_s ≥ 2` (by S8a) such that every V-position with `v₁ = s` has length `m_s`. For empty `V_s(d)` no witness depth is asserted. Distinct subspaces may have distinct depths.
- *Depends:* S8a — for the lower bound `m_s ≥ 2`.

---

## S8 — SingletonSpanPartition (THEOREM, from S2/S3/S8-fin/S8a/S8-depth)

For each document `d`, the singleton intervals `{[vⱼ, shift(vⱼ, 1)) : vⱼ ∈ dom(Σ.M(d))}` — one per V-position — partition the V-positions of `dom(Σ.M(d))`, and each interval carries a well-defined label `aⱼ ∈ dom(Σ.C)` (the *labeled partition*):

(a) Every V-position falls in exactly one singleton interval — `(A v ∈ dom(Σ.M(d)) :: (E! j :: vⱼ ≤ v < shift(vⱼ, 1)))`

(b) The labeling `vⱼ ↦ aⱼ` is well-defined: the label `aⱼ = Σ.M(d)(vⱼ)` exists and is unique because `Σ.M(d)` is a function (S2), and `aⱼ ∈ dom(Σ.C)` by referential integrity (S3).

- *Preconditions:* `dom(M(d))` finite (S8-fin); `M(d)` a function (S2); referential integrity (S3); `(A v ∈ dom(M(d)) :: zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))` (S8a); within each subspace, all V-positions share a common depth (S8-depth).
- *Postconditions:* The finite set of singleton intervals `{[vⱼ, shift(vⱼ, 1)) : vⱼ ∈ dom(M(d))}` partitions the V-positions of `dom(M(d))`: (a) `(A v ∈ dom(M(d)) :: (E! j :: vⱼ ≤ v < shift(vⱼ, 1)))`. (b) The labeling `vⱼ ↦ aⱼ = M(d)(vⱼ)` is well-defined, yielding the labeled partition.
- *Depends:* S2, S3, S8a, S8-depth, S8-fin; T1 (TumblerOrdering), T3 (CanonicalRepresentation), T5 (ContiguousSubtrees), T10, TS4 (ShiftStrictIncrease), TumblerAdd, OrdinalShift, OrdinalDisplacement, NAT-discrete, NAT-closure, NAT-order (ASN-0034).

---

## D-CTG — VContiguity (INV, design)

For each document d, V_1(d) (the text subspace) is either empty or occupies every intermediate position between its extremes:

`(A d, u, q : u ∈ V_1(d) ∧ q ∈ V_1(d) ∧ u < q : (A v : subspace(v) = 1 ∧ #v = #u ∧ zeros(v) = 0 ∧ u < v < q : v ∈ V_1(d)))`

where `V_1(d) = {v ∈ dom(M(d)) : subspace(v) = 1}` and the guard `zeros(v) = 0` restricts the consequent to S8a-conforming tumblers.

- *Axiom (design requirement):* `(A d, u, q : u ∈ V_1(d) ∧ q ∈ V_1(d) ∧ u < q : (A v : subspace(v) = 1 ∧ #v = #u ∧ zeros(v) = 0 ∧ u < v < q : v ∈ V_1(d)))`.
- *Preconditions:* `subspace(v) = 1`; V-positions share a common depth (S8-depth).
- *Postconditions:* V_1(d) is either empty or occupies every position strictly between its extremes (at the fixed depth).
- *Frame:* D-CTG is a constraint on well-formed text-subspace arrangements.
- *Depends:* S8a, S8-depth, T1 (TumblerOrdering, ASN-0034).

---

## D-MIN — VMinimumPosition (INV, design)

For each document d with V_1(d) non-empty:

`min(V_1(d)) = [1, 1, ..., 1]`

where the tuple has length m (the common depth of V-positions in the text subspace per S8-depth), and every component is 1. At depth 2 this gives min(V_1(d)) = [1, 1].

- *Axiom (design requirement):* `V_1(d) ≠ ∅ ⟹ min(V_1(d)) = [1, 1, ..., 1]` of length `m_1` (the common depth per S8-depth).
- *Preconditions:* V_1(d) non-empty; common depth `m_1` (S8-depth) with `m_1 ≥ 2` (S8a).
- *Postconditions:* Every component of `min(V_1(d))` equals 1; in particular the text subspace identifier `min(V_1(d))₁ = 1` and the within-subspace ordinal starts at the minimum positive value.
- *Depends:* S8a, S8-depth, T1 (TumblerOrdering, ASN-0034).

---

## D-CTG-depth — SharedPrefixReduction (LEMMA, corollary of D-CTG)

For depth m ≥ 3, all positions in a non-empty V_1(d) share components 2 through m − 1. Contiguity reduces to contiguity of the last component alone — structurally identical to the depth 2 case.

`(A u, x ∈ V_1(d), j : 2 ≤ j ≤ m − 1 : uⱼ = xⱼ)`

- *Preconditions:* V_1(d) non-empty; common depth `m` (S8-depth); `m ≥ 3`.
- *Postconditions:* `(A u, x ∈ V_1(d), j : 2 ≤ j ≤ m − 1 : uⱼ = xⱼ)`. Contiguity of V_1(d) reduces to contiguity of the m-th (last) component.
- *Depends:* D-CTG (VContiguity); S8a; S8-depth; S8-fin; T0(a) (UnboundedComponentValues), T1 case (i) (TumblerOrdering), T3 (CanonicalRepresentation) (ASN-0034).

---

## D-SEQ — SequentialPositions (LEMMA, from D-CTG/D-CTG-depth/D-MIN)

For each document d, if V_1(d) is non-empty, then there exists n ≥ 1 such that:

`V_1(d) = {[1, 1, ..., 1, k] : 1 ≤ k ≤ n}`

where the tuple has length m, the common V-position depth in the text subspace (S8-depth). By S8a, every V-position has depth `≥ 2`, so `m ≥ 2`; at depth 2 this gives V_1(d) = {[1, k] : 1 ≤ k ≤ n}.

- *Preconditions:* V_1(d) non-empty; common V-position depth m (S8-depth), with `m ≥ 2` inherited from S8a.
- *Postconditions:* `(E n : n ≥ 1 : V_1(d) = {[1, 1, ..., 1, k] : 1 ≤ k ≤ n})` where each tuple has length m.
- *Depends:* D-CTG, D-CTG-depth, D-MIN, S8a, S8-fin, S8-depth; T1 case (i) (TumblerOrdering, ASN-0034).

---

## Definition — ValidInsertionPosition (non-empty case)

For a document `d` with `V_1(d) ≠ ∅`, the *binary* predicate `ValidInsertionPosition(d, v)` is satisfied when:

- The common V-position depth `m` of V_1(d) is fixed by S8-depth. By S8a, `m ≥ 2`.
- Setting `N = |V_1(d)|`, the predicate holds iff `v = min(V_1(d))` or `v = shift(min(V_1(d)), j)` for some `j ∈ {1, ..., N}`.

*Formal Contract:*
- *Signature:* `ValidInsertionPosition(d, v)` — a *binary* predicate on document `d` and V-position `v`. The common V-position depth `m` is determined by `d` via S8-depth and read from state.
- *Preconditions:* Document `d` with `V_1(d) ⊆ dom(M(d))` non-empty; D-CTG holds on V_1(d); D-MIN gives `min(V_1(d)) = [1, ..., 1]` and D-SEQ gives `V_1(d) = {[1, ..., 1, k] : 1 ≤ k ≤ N}`; `m ≥ 2` is the common depth of V_1(d) by S8-depth and S8a.
- *Definition:* `ValidInsertionPosition(d, v)` holds iff, writing `N = |V_1(d)|`, `v = min(V_1(d))` or `v = shift(min(V_1(d)), j)` for some `j ∈ {1, ..., N}`.
- *Postconditions:* (a) `subspace(v) = 1` and `#v = m`. (b) `v` satisfies S8a: `zeros(v) = 0` and all components positive. (c) For fixed `d`, exactly `N + 1` values of `v` satisfy the predicate. (d) The explicit form is `v = [1, 1, ..., 1, 1 + j]` of depth `m`, with last component `1 + j` and all `m − 1` preceding components equal to 1.
- *Depends:* D-MIN, D-CTG, D-CTG-depth, D-SEQ; S8a, S8-fin, S8-depth; OrdinalShift, TumblerAdd, T3 (ASN-0034).

---

## Definition — ValidFirstInsertionPosition (empty case)

For a document `d` with `V_1(d) = ∅`, the *ternary* predicate `ValidFirstInsertionPosition(d, v, m)` is satisfied when `m ∈ ℕ` with `m ≥ 2` and `v = [1, 1, ..., 1]` of depth `m`.

*Formal Contract:*
- *Signature:* `ValidFirstInsertionPosition(d, v, m)` — a *ternary* predicate on document `d`, V-position `v`, and depth `m`.
- *Preconditions:* Document `d` with `V_1(d) = ∅`; `m ∈ ℕ` with `m ≥ 2`.
- *Definition:* `ValidFirstInsertionPosition(d, v, m)` holds iff `v = [1, 1, ..., 1]` of depth `m`.
- *Postconditions:* (a) `subspace(v) = 1` and `#v = m`. (b) `v` satisfies S8a: `zeros(v) = 0` and all components positive. (c) For fixed `d` and `m`, exactly one value of `v` satisfies the predicate.
- *Depends:* D-MIN; S8a, S8-depth; OrdinalShift, TumblerAdd, T3 (ASN-0034).
