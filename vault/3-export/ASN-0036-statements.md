# ASN-0036 Formal Statements

*Source: ASN-0036-streams.md (revised 2026-03-21) — Extracted: 2026-03-21*

## Definition — ContentStore

`Σ.C : T ⇀ Val` — a partial function mapping Istream addresses to content values. `T` is the set of tumblers (ASN-0034); `Val` is an unspecified set of content values, opaque at this level of abstraction. The domain `dom(Σ.C)` is the set of I-addresses at which content has been stored.

## Definition — Arrangement

`Σ.M(d) : T ⇀ T` — the arrangement of document `d`. A partial function mapping Vstream positions to Istream addresses. The domain `dom(Σ.M(d))` is the set of V-positions currently active in `d`; the range `ran(Σ.M(d))` is the set of I-addresses that `d` currently references.

## Definition — CorrespondenceRun

A correspondence run is a triple `(v, a, n)` — a V-position, an I-address, and a natural number `n ≥ 1` — such that the arrangement preserves ordinal displacement within the run:

`(A k : 0 ≤ k < n : Σ.M(d)(v + k) = a + k)`

At `k = 0` this is the base case `M(d)(v) = a`. Each subsequent `k` increments both the V-ordinal and the I-ordinal by the same amount.

## Definition — SubspacePositions

`V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}` — the set of V-positions in subspace `S` of document `d`, where `subspace(v) = v₁` (the first component of the element-field V-position).

## Definition — OriginPrefix

For every `a ∈ dom(Σ.C)`, the origin is the document-level prefix obtained by truncating the element field:

`origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

This is the full document tumbler `N.0.U.0.D`.

---

## Σ.C — ContentStore (DEF, state-component)

`Σ.C : T ⇀ Val`

## Σ.M(d) — Arrangement (DEF, state-component)

`Σ.M(d) : T ⇀ T`

## S0 — ContentImmutability (INV, predicate)

For every state transition `Σ → Σ'`:

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)]`

In weakest-precondition terms, for any operation producing successor state `Σ'`:

`wp(op, (A a : a ∈ dom(C) : a ∈ dom(C') ∧ C'(a) = C(a)))`

must hold in every reachable state.

## S1 — StoreMonotonicity (INV, predicate; corollary of S0)

`[dom(Σ.C) ⊆ dom(Σ'.C)]`

## S2 — ArrangementFunctionality (INV, predicate)

For each document `d`, `Σ.M(d)` is a function — each V-position maps to exactly one I-address:

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) is uniquely determined)`

## S3 — ReferentialIntegrity (INV, predicate)

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`

The weakest precondition for S3 under an operation that adds a V-mapping `M(d)(v) = a` is:

`wp(add-mapping, S3) ⟹ a ∈ dom(Σ.C)`

## S4 — OriginBasedIdentity (INV, predicate; from GlobalUniqueness ASN-0034)

For I-addresses `a₁`, `a₂` produced by distinct allocation events:

`a₁ ≠ a₂`

regardless of whether `Σ.C(a₁) = Σ.C(a₂)`.

## S5 — UnrestrictedSharing (LEMMA, lemma; consistent with S0–S3)

S0–S3 do not entail any finite bound on sharing multiplicity:

`(A N ∈ ℕ :: (E Σ :: Σ satisfies S0–S3 ∧ (E a ∈ dom(Σ.C) :: |{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N)))`

The same holds within a single document: for any `N`, there exists a state with one document `d` where `|{v : v ∈ dom(M(d)) ∧ M(d)(v) = a}| > N`.

## S6 — PersistenceIndependence (INV, predicate; corollary of S0)

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)]`

regardless of any changes to any `Σ.M(d)`.

## S7a — DocumentScopedAllocation (INV, predicate; design requirement)

Every Istream address is allocated under the tumbler prefix of the document that created it. That is, for every `a ∈ dom(Σ.C)`, the document-level prefix of `a` — the tumbler `N.0.U.0.D` obtained by truncating the element field — identifies the document whose owner performed the allocation that placed `a` into `dom(C)`.

## S7b — ElementLevelIAddresses (INV, predicate; design requirement)

`(A a ∈ dom(Σ.C) :: zeros(a) = 3)`

Every address in `dom(Σ.C)` is an element-level tumbler: all four identifying fields — node, user, document, element — are present.

## S7 — StructuralAttribution (INV, predicate; from S7a, S7b, T4, GlobalUniqueness ASN-0034)

For every `a ∈ dom(Σ.C)`:

`origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

This is the full document tumbler `N.0.U.0.D` — uniquely identifying the allocating document across the system (by GlobalUniqueness, ASN-0034). It is not metadata that can be stripped or forged — it IS the address.

## S8-fin — FiniteArrangement (INV, predicate)

For each document `d`, `dom(Σ.M(d))` is finite. A document contains finitely many V-positions at any given state.

## S8a — VPositionWellFormedness (INV, predicate)

Every text-subspace V-position is an element-field tumbler with all components strictly positive:

`(A v ∈ dom(Σ.M(d)) : v₁ ≥ 1 : zeros(v) = 0 ∧ v > 0)`

A V-position represents the element field of a full document-scoped address. Its first component `v₁` is the subspace identifier; this ASN treats only the text subspace, where `v₁ ≥ 1`. The range guard `v₁ ≥ 1` excludes link-subspace V-positions (where `v₁ = 0`).

Within the text subspace: `{v ∈ dom(M(d)) : v₁ ≥ 1} ⊆ {t ∈ T : zeros(t) = 0 ∧ t > 0}` (element-field tumblers), while `ran(M(d)) ⊆ {t ∈ T : zeros(t) = 3}` (full element-level addresses, per S7b).

## S8-depth — FixedDepthVPositions (INV, predicate; design requirement)

Within a given subspace `s` of document `d`, all V-positions share the same tumbler depth:

`(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`

## S8 — SpanDecomposition (LEMMA, lemma; from S8-fin, S8a, S2, S8-depth, T5, PrefixOrderingExtension, TA5(c), TA7a ASN-0034)

For each document `d`, the text-subspace portion of the arrangement — `{(v, Σ.M(d)(v)) : v ∈ dom(Σ.M(d)) ∧ v₁ ≥ 1}` — can be decomposed into a finite set of correspondence runs `{(vⱼ, aⱼ, nⱼ)}` such that:

(a) The runs partition the text-subspace V-positions: every text-subspace V-position in `dom(Σ.M(d))` falls in exactly one run —
`(A v ∈ dom(Σ.M(d)) : v₁ ≥ 1 : (E! j :: vⱼ ≤ v < vⱼ + nⱼ))`

(b) Within each run: `Σ.M(d)(vⱼ + k) = aⱼ + k` for all `k` with `0 ≤ k < nⱼ`

## D-CTG — VContiguity (INV, predicate; design constraint)

For each document `d` and subspace `S`, `V_S(d)` is either empty or occupies every intermediate position between its extremes:

`(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`

Within each subspace, V-positions form a contiguous ordinal range with no gaps.

## D-MIN — VMinimumPosition (INV, predicate; design constraint)

For each document `d` and subspace `S` with `V_S(d)` non-empty:

`min(V_S(d)) = [S, 1, ..., 1]`

where the tuple has length `m` (the common depth of V-positions in subspace `S` per S8-depth), and every component after the first is 1.

## D-CTG-depth — SharedPrefixReduction (LEMMA, lemma; from D-CTG, S8-fin, S8-depth)

For depth `m ≥ 3`, all positions in a non-empty `V_S(d)` share components 2 through `m − 1`. Contiguity reduces to contiguity of the last component alone — structurally identical to the depth 2 case.

*Proof.* Suppose for contradiction that `V_S(d)` contains two positions `v₁ < v₂` (both depth `m` by S8-depth) whose first point of disagreement is at component `j` with `2 ≤ j ≤ m − 1` — that is, `(v₁)ᵢ = (v₂)ᵢ` for all `i < j`, and `(v₁)ⱼ < (v₂)ⱼ` (since `v₁ < v₂` by T1(i)). For any natural number `n > (v₁)ⱼ₊₁`, define `w` of length `m` by:

- `wᵢ = (v₁)ᵢ` for `1 ≤ i ≤ j`
- `wⱼ₊₁ = n`
- `wᵢ = 1` for `j + 2 ≤ i ≤ m` (if any such positions exist)

Then `w` has subspace `S` and depth `m`. We verify `v₁ < w < v₂`:

- **w > v₁**: `w` agrees with `v₁` on components 1 through `j`. At component `j + 1`, `n > (v₁)ⱼ₊₁`. By T1(i), `w > v₁`.
- **w < v₂**: `w` agrees with `v₂` on components 1 through `j − 1`. At component `j`, `wⱼ = (v₁)ⱼ < (v₂)ⱼ`. By T1(i), `w < v₂`.

By D-CTG, every such `w` belongs to `V_S(d)`. By T0(a), unboundedly many values of `n` exist, yielding infinitely many distinct positions in `V_S(d)` — contradicting S8-fin. ∎

This applies uniformly to all depths `m ≥ 3` and all divergence points `j ∈ {2, …, m − 1}`.

## D-SEQ — SequentialPositions (LEMMA, lemma; from D-CTG, D-MIN, S8-fin, S8-depth)

For each document `d` and subspace `S`, if `V_S(d)` is non-empty then there exists `n ≥ 1` such that:

`V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}`

where the tuple has length `m` (the common V-position depth in subspace `S`). At depth 2 this gives `V_S(d) = {[S, k] : 1 ≤ k ≤ n}`.

## S9 — TwoStreamSeparation (LEMMA, lemma; from S0)

No modification to any arrangement `Σ.M(d)` can alter the content store `Σ.C`:

`[Σ'.M(d) ≠ Σ.M(d) ⟹ (A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))]`

*Proof.* S0 guarantees that `a ∈ dom(Σ.C)` implies `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)` for every state transition `Σ → Σ'`, unconditionally. The consequent of S9 is a special case of S0's universal guarantee, restricted to transitions that modify some arrangement. ∎
