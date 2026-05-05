# ASN-0036 Claim Statements

*Source: ASN-0036-streams.md (revised 2026-04-09) — Extracted: 2026-04-09*

## Definition — ContentStore

`Σ.C : T ⇀ Val` — the content store is a partial function from tumblers to content values.

`dom(Σ.C) = {a ∈ T : Σ.C(a) is defined}` — the set of I-addresses at which content has been stored.

## Definition — Arrangement

`Σ.M(d) : T ⇀ T` — the arrangement of document `d` is a partial function from V-position tumblers to I-address tumblers.

`dom(Σ.M(d)) = {v ∈ T : Σ.M(d)(v) is defined}` — the set of V-positions currently active in `d`.

`ran(Σ.M(d)) = {Σ.M(d)(v) : v ∈ dom(Σ.M(d))}` — the set of I-addresses that `d` currently references.

## Definition — Subspace

`subspace(v) = v₁` — the subspace identifier is the first component of the element-field V-position.

`V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}` — the set of V-positions in subspace S of document d.

## Definition — CorrespondenceRun

A *correspondence run* is a triple `(v, a, n)` — a V-position, an I-address, and a natural number `n ≥ 1` — such that the arrangement preserves ordinal displacement within the run:

`(A k : 0 ≤ k < n : Σ.M(d)(v + k) = a + k)`

where `v + 0 = v` (identity) and `v + k = shift(v, k)` for `k ≥ 1`, and `a + 0 = a` and `a + k = shift(a, k) = a ⊕ δ(k, #a)` for `k ≥ 1`.

## Definition — Origin

For every `a ∈ dom(Σ.C)`:

`origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

This is the full document tumbler `N.0.U.0.D` — the document-level prefix obtained by truncating the element field.

---

## Σ.C — ContentStore (DEF, axiom)

- *Axiom:* `Σ.C : T ⇀ Val` — the content store is a partial function from tumblers to content values.
- *Definition:* `dom(Σ.C) = {a ∈ T : Σ.C(a) is defined}` — the set of I-addresses at which content has been stored.

## Σ.M(d) — Arrangement (DEF, axiom)

- *Axiom:* `Σ.M(d) : T ⇀ T` — the arrangement of document `d` is a partial function from V-position tumblers to I-address tumblers.
- *Definition:* `dom(Σ.M(d)) = {v ∈ T : Σ.M(d)(v) is defined}` — the set of V-positions currently active in `d`.
- *Definition:* `ran(Σ.M(d)) = {Σ.M(d)(v) : v ∈ dom(Σ.M(d))}` — the set of I-addresses that `d` currently references.

## S0 — ContentImmutability (INV, predicate)

For every state transition `Σ → Σ'`:

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)]`

## S1 — StoreMonotonicity (LEMMA, lemma)

`[dom(Σ.C) ⊆ dom(Σ'.C)]`

- *Preconditions:* State transition `Σ → Σ'` in a system satisfying S0 (content immutability).
- *Postconditions:* `dom(Σ.C) ⊆ dom(Σ'.C)`.

## S2 — ArrangementFunctionality (INV, axiom)

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) is uniquely determined)`

## S3 — ReferentialIntegrity (INV, predicate)

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`

## S4 — OriginBasedIdentity (LEMMA, lemma)

For I-addresses `a₁`, `a₂` produced by distinct allocation events:

`a₁ ≠ a₂`

regardless of whether `Σ.C(a₁) = Σ.C(a₂)`.

- *Preconditions:* `a₁, a₂ ∈ dom(Σ.C)` produced by distinct allocation events within a system conforming to T10a (allocator discipline, ASN-0034).
- *Postconditions:* `a₁ ≠ a₂`, regardless of whether `Σ.C(a₁) = Σ.C(a₂)`.
- *Frame:* The content store `C` and value domain `Val` play no role in the proof — distinctness is a property of the addressing scheme alone.

## S5 — UnrestrictedSharing (LEMMA, lemma)

`(A N ∈ ℕ :: (E Σ :: Σ satisfies S0–S3 ∧ (E a ∈ dom(Σ.C) :: |{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N)))`

- *Preconditions:* `N ∈ ℕ` arbitrary.
- *Postconditions:* There exists a state `Σ` satisfying S0 (content immutability), S1 (store monotonicity), S2 (arrangement functionality), and S3 (referential integrity) such that for some `a ∈ dom(Σ.C)`, `|{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N`. The construction works both across documents (multiplicity `N + 1` over `N + 1` documents) and within a single document (multiplicity `N + 1` at `N + 1` distinct V-positions).
- *Frame:* S0–S3 are the only invariants checked.

## S6 — PersistenceIndependence (LEMMA, lemma)

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)]`

regardless of any changes to any `Σ.M(d)`.

- *Preconditions:* `a ∈ dom(Σ.C)` and state transition `Σ → Σ'` in a system satisfying S0 (content immutability).
- *Postconditions:* `a ∈ dom(Σ'.C)`, with no condition on the arrangement functions `Σ.M(d)` or `Σ'.M(d)` for any document `d`.
- *Frame:* The arrangement functions `M(d)` are unconstrained — S6 holds for all possible values of `Σ'.M(d)`, including `Σ'.M(d) = ∅`.

## S7a — DocumentScopedAllocation (INV, predicate)

Every Istream address is allocated under the tumbler prefix of the document that created it. That is, for every `a ∈ dom(Σ.C)`, the document-level prefix of `a` — the tumbler `N.0.U.0.D` obtained by truncating the element field — identifies the document whose owner performed the allocation that placed `a` into `dom(C)`.

## S7b — ElementLevelIAddresses (INV, predicate)

`(A a ∈ dom(Σ.C) :: zeros(a) = 3)`

## S7c — ElementFieldDepth (INV, predicate)

`(A a ∈ dom(Σ.C) :: #fields(a).element ≥ 2)`

## S7 — StructuralAttribution (LEMMA, lemma)

For every `a ∈ dom(Σ.C)`:

`origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

- *Preconditions:* `a ∈ dom(Σ.C)` in a system conforming to S7a (document-scoped allocation), S7b (element-level I-addresses), T4 (FieldSeparatorConstraint, ASN-0034), and T10a (allocator discipline, ASN-0034).
- *Postconditions:*
  - (a) `origin(a)` is well-defined and is a document-level tumbler with `zeros(origin(a)) = 2`.
  - (b) `origin(a)` is the tumbler of the document that allocated `a`.
  - (c) For `a₁, a₂` allocated under distinct documents, `origin(a₁) ≠ origin(a₂)`.
  - (d) `origin(a)` is invariant across all states in which `a ∈ dom(Σ.C)`.
- *Frame:* The content values `Σ.C(a)` and arrangement functions `Σ.M(d)` play no role — attribution is a property of the addressing scheme alone.

## S8-fin — FiniteArrangement (INV, predicate)

For each document `d`, `dom(Σ.M(d))` is finite.

## S8a — VPositionWellFormedness (INV, axiom)

`(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0)`

- *Axiom:* V-positions are element-field tumblers — the fourth field in T4's decomposition of element-level addresses.
- *Preconditions:* T4 (FieldSeparatorConstraint, ASN-0034) — every non-separator component is strictly positive, every present field has at least one component; S7b — addresses in `dom(Σ.C)` are element-level tumblers with `zeros(a) = 3`.
- *Postconditions:* `(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0)`.

## S8-depth — FixedDepthVPositions (INV, predicate)

`(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`

## S8 — FiniteSpanDecomposition (LEMMA, lemma)

For each document `d`, the arrangement `{(v, Σ.M(d)(v)) : v ∈ dom(Σ.M(d))}` can be decomposed into a finite set of correspondence runs `{(vⱼ, aⱼ, nⱼ)}` such that:

(a) `(A v ∈ dom(Σ.M(d)) :: (E! j :: vⱼ ≤ v < vⱼ + nⱼ))`

(b) `Σ.M(d)(vⱼ + k) = aⱼ + k` for all `k` with `0 ≤ k < nⱼ`

- *Preconditions:* `dom(M(d))` finite (S8-fin); `M(d)` a function (S2); `(A v ∈ dom(M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1)` (S8a); within each subspace, all V-positions share a common depth (S8-depth).
- *Postconditions:* There exists a finite set of correspondence runs `{(vⱼ, aⱼ, nⱼ)}` satisfying (a) `(A v ∈ dom(M(d)) :: (E! j :: vⱼ ≤ v < vⱼ + nⱼ))` and (b) `(A j, k : 0 ≤ k < nⱼ : M(d)(vⱼ + k) = aⱼ + k)`.

## D-CTG — VContiguity (INV, predicate)

`(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`

where `V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}` and `subspace(v) = v₁`.

## D-MIN — VMinimumPosition (INV, predicate)

For each document d and subspace S with V_S(d) non-empty:

`min(V_S(d)) = [S, 1, ..., 1]`

where the tuple has length m (the common depth of V-positions in subspace S per S8-depth), and every component after the first is 1.

## D-CTG-depth — SharedPrefixReduction (LEMMA, lemma)

`(A v₁, v₂ ∈ V_S(d), j : 2 ≤ j ≤ m − 1 : (v₁)ⱼ = (v₂)ⱼ)`

Contiguity of V_S(d) reduces to contiguity of the m-th (last) component.

- *Preconditions:* V_S(d) non-empty; common depth m ≥ 3 (S8-depth).
- *Postconditions:* `(A v₁, v₂ ∈ V_S(d), j : 2 ≤ j ≤ m − 1 : (v₁)ⱼ = (v₂)ⱼ)`. Contiguity of V_S(d) reduces to contiguity of the m-th (last) component.

## D-SEQ — SequentialPositions (LEMMA, lemma)

For each document d and subspace S, if V_S(d) is non-empty and the common V-position depth m ≥ 2 (S8-depth), then there exists n ≥ 1 such that:

`V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}`

where the tuple has length m.

- *Preconditions:* V_S(d) non-empty; common V-position depth m ≥ 2 (S8-depth).
- *Postconditions:* `(E n : n ≥ 1 : V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n})` where each tuple has length m.

## ValidInsertionPosition — ValidInsertionPosition (DEF, predicate)

A V-position v is a *valid insertion position* in subspace S of document d satisfying D-CTG when one of two cases holds:

- *Non-empty subspace.* V_S(d) ≠ ∅ with |V_S(d)| = N. Write m for the common V-position depth in subspace S (S8-depth); m ≥ 2. Then either v = min(V_S(d)) (the j = 0 case) or v = shift(min(V_S(d)), j) for some j with 1 ≤ j ≤ N. In both cases, #v = m.

- *Empty subspace.* V_S(d) = ∅. Then v = [S, 1, ..., 1] of depth m ≥ 2, establishing the subspace's V-position depth at m. The lower bound m ≥ 2 is necessary: at m = 1, v = [S] and shift([S], 1) = [S] ⊕ δ(1, 1) = [S] ⊕ [1]; the action point of [1] is k = 1, so TumblerAdd gives r₁ = S + 1, producing [S + 1] — a position in subspace S + 1, not S. For m ≥ 2, δ(n, m) has action point m, and since m > 1, TumblerAdd copies component 1 unchanged — OrdinalShift preserves the subspace identifier.

In both cases, S = v₁ is the subspace identifier.

The explicit form of valid positions: `shift(min(V_S(d)), j) = [S, 1, ..., 1 + j]` (last component is 1 + j, all preceding post-subspace components are 1).

## S9 — TwoStreamSeparation (LEMMA, lemma)

`[Σ'.M(d) ≠ Σ.M(d) ⟹ (A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))]`
