# ASN-0036 Formal Statements

*Source: ASN-0036-two-space.md (revised 2026-03-14) — Index: 2026-03-14 — Extracted: 2026-03-14*

## Definition — ContentStore

**Σ.C : T ⇀ Val** — the *content store*. A partial function mapping I-space addresses to content values. `T` is the set of tumblers (ASN-0034); `Val` is an unspecified set of content values, opaque at this level of abstraction. The domain `dom(Σ.C)` is the set of I-addresses at which content has been stored.

## Definition — Arrangement

**Σ.M(d) : T ⇀ T** — the *arrangement* of document `d`. A partial function mapping V-space positions to I-space addresses. The domain `dom(Σ.M(d))` is the set of V-positions currently active in `d`; the range `ran(Σ.M(d))` is the set of I-addresses that `d` currently references.

## Definition — CorrespondenceRun

A *correspondence run* is a triple `(v, a, n)` — a V-position, an I-address, and a natural number `n ≥ 1` — such that the arrangement preserves ordinal displacement within the run:

`(A k : 0 ≤ k < n : Σ.M(d)(v + k) = a + k)`

At `k = 0` this is the base case `M(d)(v) = a` — no displacement, no arithmetic. Each subsequent `k` increments both the V-ordinal and the I-ordinal by the same amount.

## Definition — Origin

For every `a ∈ dom(Σ.C)`, define the *origin* as the document-level prefix obtained by truncating the element field:

`origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

This is the full document tumbler `N.0.U.0.D`.

---

## S0 — ContentImmutability (INV, predicate(State, State))

For every state transition `Σ → Σ'`:

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)]`

In weakest-precondition terms, for any operation producing successor state `Σ'`:

`wp(op, (A a : a ∈ dom(C) : a ∈ dom(C') ∧ C'(a) = C(a)))`

must hold in every reachable state.

## S1 — StoreMonotonicity (LEMMA, lemma)

`[dom(Σ.C) ⊆ dom(Σ'.C)]`

Corollary of S0, for every state transition `Σ → Σ'`.

## S2 — ArrangementFunctional (INV, predicate(State))

For each document `d`, `Σ.M(d)` is a function — each V-position maps to exactly one I-address:

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) is uniquely determined)`

## S3 — ReferentialIntegrity (INV, predicate(State))

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`

The weakest precondition for S3 under an operation that adds a V-mapping `M(d)(v) = a` is:

`wp(add-mapping, S3) ⟹ a ∈ dom(Σ.C)`

## S4 — OriginBasedIdentity (LEMMA, lemma)

For I-addresses `a₁`, `a₂` produced by distinct allocation events:

`a₁ ≠ a₂`

regardless of whether `Σ.C(a₁) = Σ.C(a₂)`.

## S5 — UnrestrictedSharing (LEMMA, lemma)

The same I-address may appear in the ranges of multiple arrangements, and at multiple V-positions within a single arrangement. S0–S3 are consistent with any finite sharing multiplicity — they place no constraint on `|{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}|`:

`(A N ∈ ℕ :: (E Σ :: Σ satisfies S0–S3 ∧ (E a ∈ dom(Σ.C) :: |{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N)))`

Within-document witness: for any `N`, construct `Σ'_N` with one I-address `a` where `C(a) = w`, and one document `d` with `M(d) = {v₁ ↦ a, v₂ ↦ a, ..., v_{N+1} ↦ a}` for `N + 1` distinct V-positions. The within-document sharing multiplicity is `N + 1 > N`.

## S6 — PersistenceIndependence (LEMMA, lemma)

The membership of `a` in `dom(Σ.C)` is independent of all arrangements:

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)]`

regardless of any changes to any `Σ.M(d)`.

## S7a — DocumentScopedAllocation (INV, predicate(State))

Every I-space address is allocated under the tumbler prefix of the document that created it. That is, for every `a ∈ dom(Σ.C)`, the document-level prefix of `a` — the tumbler `N.0.U.0.D` obtained by truncating the element field — identifies the document whose owner performed the allocation that placed `a` into `dom(C)`.

## S7b — ElementLevelAddresses (INV, predicate(State))

Every address in `dom(Σ.C)` is an element-level tumbler:

`(A a ∈ dom(Σ.C) :: zeros(a) = 3)`

## S7 — StructuralAttribution (LEMMA, lemma)

For every `a ∈ dom(Σ.C)`:

`origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

This uniquely identifies the allocating document across the system (by GlobalUniqueness, ASN-0034). It is not metadata that can be stripped or forged — it IS the address.

Derived from S7a (document-scoped allocation ensures the document-level prefix identifies the allocating document), S7b (element-level restriction ensures all three identifying fields are present), and T4 (field parsing, ASN-0034).

## S8-fin — FiniteArrangement (INV, predicate(State))

For each document `d`, `dom(Σ.M(d))` is finite.

## S8a — VPositionWellFormed (INV, predicate(State))

Every text-subspace V-position is an element-field tumbler with all components strictly positive:

`(A v ∈ dom(Σ.M(d)) : v₁ ≥ 1 : zeros(v) = 0 ∧ v > 0)`

where `v₁` is the first component of `v` (the subspace identifier), and this ASN treats only the text subspace where `v₁ ≥ 1`.

## S8-depth — FixedDepthPositions (INV, predicate(State))

Within a given subspace `s` of document `d`, all V-positions share the same tumbler depth:

`(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`

where `(vᵢ)₁` denotes the first component (subspace identifier) of `vᵢ`, and `#v` denotes the tumbler depth.

## S8 — SpanDecomposition (LEMMA, lemma)

For each document `d`, the text-subspace portion of the arrangement — `{(v, Σ.M(d)(v)) : v ∈ dom(Σ.M(d)) ∧ v₁ ≥ 1}` — can be decomposed into a finite set of correspondence runs `{(vⱼ, aⱼ, nⱼ)}` such that:

(a) The runs partition the text-subspace V-positions: every text-subspace V-position in `dom(Σ.M(d))` falls in exactly one run:

`(A v ∈ dom(Σ.M(d)) : v₁ ≥ 1 : (E! j :: vⱼ ≤ v < vⱼ + nⱼ))`

(b) Within each run:

`Σ.M(d)(vⱼ + k) = aⱼ + k` for all `k` with `0 ≤ k < nⱼ`

Derived from S8-fin (finiteness of `dom(M(d))`), S8a, S2, S8-depth, T5 (ContiguousSubtrees), PrefixOrderingExtension, TA5(c), and TA7a (ASN-0034).

Degenerate decomposition: each V-position `v` with `M(d)(v) = a` forms a singleton run `(v, a, 1)`. At `k = 0`: `M(d)(v + 0) = M(d)(v) = a = a + 0`.

## S9 — TwoSpaceSeparation (LEMMA, lemma)

No modification to any arrangement `Σ.M(d)` can alter the content store `Σ.C`:

`[Σ'.M(d) ≠ Σ.M(d) ⟹ (A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))]`

*Proof.* S0 guarantees that `a ∈ dom(Σ.C)` implies `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)` for every state transition `Σ → Σ'`, unconditionally. The consequent of S9 is a special case of S0's universal guarantee, restricted to transitions that modify some arrangement. ∎
