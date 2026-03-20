# ASN-0036 Formal Statements

*Source: ASN-0036-two-space.md (revised 2026-03-14) — Extracted: 2026-03-20*

## Definition — ContentStore

**Σ.C : T ⇀ Val** — the *content store*. A partial function mapping Istream addresses to content values. `T` is the set of tumblers (ASN-0034); `Val` is an unspecified set of content values, opaque at this level of abstraction. The domain `dom(Σ.C)` is the set of I-addresses at which content has been stored.

## Definition — Arrangement

**Σ.M(d) : T ⇀ T** — the *arrangement* of document `d`. A partial function mapping Vstream positions to Istream addresses. The domain `dom(Σ.M(d))` is the set of V-positions currently active in `d`; the range `ran(Σ.M(d))` is the set of I-addresses that `d` currently references.

## Definition — CorrespondenceRun

A *correspondence run* is a triple `(v, a, n)` — a V-position, an I-address, and a natural number `n ≥ 1` — such that the arrangement preserves ordinal displacement within the run:

`(A k : 0 ≤ k < n : Σ.M(d)(v + k) = a + k)`

At `k = 0` this is the base case `M(d)(v) = a` — no displacement, no arithmetic. Each subsequent `k` increments both the V-ordinal and the I-ordinal by the same amount.

## Definition — Origin

For every `a ∈ dom(Σ.C)`, the *origin* is the document-level prefix obtained by truncating the element field:

`origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

This is the full document tumbler `N.0.U.0.D` — uniquely identifying the allocating document across the system (by GlobalUniqueness, ASN-0034).

---

## S0 — ContentImmutability (INV, predicate)

For every state transition `Σ → Σ'`:

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)]`

Weakest-precondition form: for any operation producing successor state `Σ'`:

`wp(op, (A a : a ∈ dom(C) : a ∈ dom(C') ∧ C'(a) = C(a)))`

must hold in every reachable state.

## S1 — StoreMonotonicity (INV, predicate; corollary of S0)

`[dom(Σ.C) ⊆ dom(Σ'.C)]`

for every state transition `Σ → Σ'`.

## S2 — ArrangementFunctionality (INV, predicate)

For each document `d`, `Σ.M(d)` is a function — each V-position maps to exactly one I-address:

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) is uniquely determined)`

## S3 — ReferentialIntegrity (INV, predicate)

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`

Weakest-precondition form for an operation that adds a V-mapping `M(d)(v) = a`:

`wp(add-mapping, S3) ⟹ a ∈ dom(Σ.C)`

## S4 — OriginBasedIdentity (INV, predicate; from GlobalUniqueness ASN-0034)

For I-addresses `a₁`, `a₂` produced by distinct allocation events:

`a₁ ≠ a₂`

regardless of whether `Σ.C(a₁) = Σ.C(a₂)`.

## S5 — UnrestrictedSharing (LEMMA, lemma; consistent with S0–S3)

`(A N ∈ ℕ :: (E Σ :: Σ satisfies S0–S3 ∧ (E a ∈ dom(Σ.C) :: |{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N)))`

Within-document form: for any `N`, there exists a state `Σ'_N` with one I-address `a` where `C(a) = w`, and one document `d` with `M(d) = {v₁ ↦ a, v₂ ↦ a, ..., v_{N+1} ↦ a}` for `N + 1` distinct V-positions. S0–S3 are satisfied and within-document sharing multiplicity is `N + 1 > N`.

## S6 — PersistenceIndependence (INV, predicate; corollary of S0)

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)]`

regardless of any changes to any `Σ.M(d)`.

## S7a — DocumentScopedAllocation (INV, predicate; design requirement)

Every Istream address is allocated under the tumbler prefix of the document that created it. For every `a ∈ dom(Σ.C)`, the document-level prefix of `a` — the tumbler `N.0.U.0.D` obtained by truncating the element field — identifies the document whose owner performed the allocation that placed `a` into `dom(C)`.

## S7b — ElementLevelIAddresses (INV, predicate; design requirement)

`(A a ∈ dom(Σ.C) :: zeros(a) = 3)`

Every address in `dom(Σ.C)` is an element-level tumbler. Precondition: `zeros(a) = 3` means all four identifying fields — node, user, document, element — are present, per T4's field correspondence (ASN-0034).

## S7 — StructuralAttribution (LEMMA, lemma; from S7a, S7b, T4, GlobalUniqueness ASN-0034)

For every `a ∈ dom(Σ.C)`:

`origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

where `origin(a)` is the full document tumbler `N.0.U.0.D` uniquely identifying the allocating document. Since I-addresses are permanent (S0) and unique (S4), this attribution is permanent and unseverable.

Preconditions: S7a (document-scoped allocation), S7b (element-level restriction, `zeros(a) = 3`), T4 field parsing (ASN-0034).

## S8-fin — FiniteArrangement (INV, predicate)

For each document `d`, `dom(Σ.M(d))` is finite. A document contains finitely many V-positions at any given state.

## S8a — VPositionWellFormedness (INV, predicate)

Every text-subspace V-position is an element-field tumbler with all components strictly positive:

`(A v ∈ dom(Σ.M(d)) : v₁ ≥ 1 : zeros(v) = 0 ∧ v > 0)`

Within the text subspace: `{v ∈ dom(M(d)) : v₁ ≥ 1} ⊆ {t ∈ T : zeros(t) = 0 ∧ t > 0}`.

The range guard `v₁ ≥ 1` excludes link-subspace V-positions (where `v₁ = 0`).

## S8-depth — FixedDepthVPositions (INV, predicate; design requirement)

Within a given subspace `s` of document `d`, all V-positions share the same tumbler depth:

`(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`

Note: `(v₁)₁` denotes the first component of V-position `v₁` (the subspace identifier).

## S8 — SpanDecomposition (LEMMA, lemma; theorem from S8-fin, S8a, S2, S8-depth, T5, PrefixOrderingExtension, TA5(c), TA7a ASN-0034)

For each document `d`, the text-subspace portion of the arrangement — `{(v, Σ.M(d)(v)) : v ∈ dom(Σ.M(d)) ∧ v₁ ≥ 1}` — can be decomposed into a finite set of correspondence runs `{(vⱼ, aⱼ, nⱼ)}` such that:

(a) The runs partition the text-subspace V-positions: every text-subspace V-position in `dom(Σ.M(d))` falls in exactly one run:

`(A v ∈ dom(Σ.M(d)) : v₁ ≥ 1 : (E! j :: vⱼ ≤ v < vⱼ + nⱼ))`

(b) Within each run:

`Σ.M(d)(vⱼ + k) = aⱼ + k` for all `k` with `0 ≤ k < nⱼ`

## S9 — TwoStreamSeparation (LEMMA, lemma; theorem from S0)

`[Σ'.M(d) ≠ Σ.M(d) ⟹ (A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))]`

*Proof sketch.* S0 guarantees `a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)` for every state transition `Σ → Σ'`, unconditionally. The consequent of S9 is a special case of S0's universal guarantee, restricted to transitions that modify some arrangement. ∎
