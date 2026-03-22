# ASN-0036 Formal Statements

*Source: ASN-0036-streams.md (revised 2026-03-21) — Extracted: 2026-03-22*

## Definition — State

`Σ = (Σ.C, Σ.M)` where `Σ.C : T ⇀ Val` and `Σ.M(d) : T ⇀ T` for each document `d`. A state transition is written `Σ → Σ'`.

## Definition — Subspace

`subspace(v) = v₁` — the first component of V-position `v`.

## Definition — VSubspace

`V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}` — the set of V-positions in subspace `S` of document `d`.

## Definition — Origin

For `a ∈ dom(Σ.C)` with `zeros(a) = 3`:

`origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

This is the full document tumbler `N.0.U.0.D` — the document-level prefix obtained by truncating the element field.

## Definition — CorrespondenceRun

A *correspondence run* is a triple `(v, a, n)` — a V-position, an I-address, and a natural number `n ≥ 1` — such that:

`(A k : 0 ≤ k < n : Σ.M(d)(v + k) = a + k)`

where `v + k` denotes ordinal displacement applied to V-positions and `a + k` denotes ordinal displacement applied to the element ordinal of I-addresses (TA7a, ASN-0034).

---

## Σ.C — ContentStore (DEF, type)

`Σ.C : T ⇀ Val` — a partial function mapping Istream addresses to content values. `T` is the set of tumblers (ASN-0034); `Val` is an unspecified set of content values. `dom(Σ.C)` is the set of I-addresses at which content has been stored.

## Σ.M(d) — Arrangement (DEF, type)

`Σ.M(d) : T ⇀ T` — a partial function mapping Vstream positions to Istream addresses for document `d`. `dom(Σ.M(d))` is the set of V-positions currently active in `d`; `ran(Σ.M(d))` is the set of I-addresses that `d` currently references.

---

## S0 — ContentImmutability (INV, predicate)

For every state transition `Σ → Σ'`:

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)]`

Equivalently, for any operation producing successor state `Σ'`:

`wp(op, (A a : a ∈ dom(C) : a ∈ dom(C') ∧ C'(a) = C(a)))`

must hold in every reachable state.

## S1 — StoreMonotonicity (LEMMA, lemma)

`[dom(Σ.C) ⊆ dom(Σ'.C)]`

for every state transition `Σ → Σ'`. Corollary of S0.

## S2 — ArrangementFunctionality (INV, predicate)

For each document `d`, `Σ.M(d)` is a function — each V-position maps to exactly one I-address:

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) is uniquely determined)`

## S3 — ReferentialIntegrity (INV, predicate)

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`

Precondition for adding a V-mapping `M(d)(v) = a` without simultaneously creating content:

`wp(add-mapping, S3) ⟹ a ∈ dom(Σ.C)`

## S4 — OriginBasedIdentity (LEMMA, lemma)

For I-addresses `a₁`, `a₂` produced by distinct allocation events:

`a₁ ≠ a₂`

regardless of whether `Σ.C(a₁) = Σ.C(a₂)`. From GlobalUniqueness (ASN-0034).

## S5 — UnrestrictedSharing (LEMMA, lemma)

S0–S3 place no constraint on `|{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}|`:

`(A N ∈ ℕ :: (E Σ :: Σ satisfies S0–S3 ∧ (E a ∈ dom(Σ.C) :: |{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N)))`

## S6 — PersistenceIndependence (LEMMA, lemma)

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)]`

for every state transition `Σ → Σ'`, regardless of any changes to any `Σ.M(d)`. Corollary of S0.

## S7a — DocumentScopedAllocation (INV, predicate)

For every `a ∈ dom(Σ.C)`, the document-level prefix of `a` — the tumbler `N.0.U.0.D` obtained by truncating the element field — identifies the document whose owner performed the allocation that placed `a` into `dom(C)`.

## S7b — ElementLevelAddresses (INV, predicate)

`(A a ∈ dom(Σ.C) :: zeros(a) = 3)`

Every address in `dom(Σ.C)` is an element-level tumbler: all four identifying fields (node, user, document, element) are present.

## S7 — StructuralAttribution (LEMMA, lemma)

For every `a ∈ dom(Σ.C)`:

`origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

This is the full document tumbler `N.0.U.0.D`, uniquely identifying the allocating document across the system (by GlobalUniqueness, ASN-0034). From S7a, S7b, T4, GlobalUniqueness (ASN-0034).

## S8-fin — FiniteArrangement (INV, predicate)

For each document `d`, `dom(Σ.M(d))` is finite.

## S8a — VPositionWellFormedness (INV, predicate)

`(A v ∈ dom(Σ.M(d)) : v₁ ≥ 1 : zeros(v) = 0 ∧ v > 0)`

The range guard `v₁ ≥ 1` captures both text-subspace (`v₁ = 1`) and link-subspace (`v₁ = 2`) V-positions. Within the text subspace: `{v ∈ dom(M(d)) : v₁ ≥ 1} ⊆ {t ∈ T : zeros(t) = 0 ∧ t > 0}`.

## S8-depth — FixedDepthVPositions (INV, predicate)

Within a given subspace of document `d`, all V-positions share the same tumbler depth:

`(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`

## S8 — SpanDecomposition (LEMMA, lemma)

For each document `d`, the text-subspace portion of the arrangement — `{(v, Σ.M(d)(v)) : v ∈ dom(Σ.M(d)) ∧ v₁ ≥ 1}` — can be decomposed into a finite set of correspondence runs `{(vⱼ, aⱼ, nⱼ)}` such that:

(a) The runs partition the text-subspace V-positions: every text-subspace V-position in `dom(Σ.M(d))` falls in exactly one run:

`(A v ∈ dom(Σ.M(d)) : v₁ ≥ 1 : (E! j :: vⱼ ≤ v < vⱼ + nⱼ))`

(b) Within each run:

`Σ.M(d)(vⱼ + k) = aⱼ + k` for all `k` with `0 ≤ k < nⱼ`

From S8-fin, S8a, S2, S8-depth, T5, PrefixOrderingExtension, TA5(c), TA7a (ASN-0034).

---

## D-CTG — VContiguity (INV, predicate)

For each document `d` and subspace `S`, `V_S(d)` is either empty or occupies every intermediate position between its extremes:

`(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`

Design constraint on well-formed document states.

## D-MIN — VMinimumPosition (INV, predicate)

For each document `d` and subspace `S` with `V_S(d)` non-empty:

`min(V_S(d)) = [S, 1, ..., 1]`

where the tuple has length `m` (the common depth of V-positions in subspace `S` per S8-depth), and every component after the first is 1. At depth 2: `min(V_S(d)) = [S, 1]`.

## D-CTG-depth — SharedPrefixReduction (LEMMA, lemma)

For depth `m ≥ 3`, all positions in a non-empty `V_S(d)` share components 2 through `m − 1`. Contiguity reduces to contiguity of the last component alone — structurally identical to the depth 2 case.

From D-CTG, S8-fin, S8-depth.

*Proof sketch.* If `V_S(d)` contains two positions `v₁ < v₂` (both depth `m`) whose first point of disagreement is at component `j` with `2 ≤ j ≤ m − 1`, then for any `n > (v₁)ⱼ₊₁`, the position `w` defined by `wᵢ = (v₁)ᵢ` for `1 ≤ i ≤ j`, `wⱼ₊₁ = n`, `wᵢ = 1` for `j + 2 ≤ i ≤ m` satisfies `v₁ < w < v₂` with `subspace(w) = S` and `#w = m`. By D-CTG, `w ∈ V_S(d)` for all such `n` — infinitely many, contradicting S8-fin.

## D-SEQ — SequentialPositions (LEMMA, lemma)

For each document `d` and subspace `S`, if `V_S(d)` is non-empty then there exists `n ≥ 1` such that:

`V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}`

where the tuple has length `m` (the common V-position depth in subspace `S`). At depth 2: `V_S(d) = {[S, k] : 1 ≤ k ≤ n}`.

From D-CTG, D-MIN, S8-fin, S8-depth.

---

## S9 — TwoStreamSeparation (LEMMA, lemma)

No modification to any arrangement `Σ.M(d)` can alter the content store `Σ.C`:

`[Σ'.M(d) ≠ Σ.M(d) ⟹ (A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))]`

From S0. The consequent is a special case of S0's universal guarantee restricted to transitions that modify some arrangement.
