# ASN-0036 Formal Statements

*Source: ASN-0036-streams.md (revised 2026-03-22) — Extracted: 2026-03-22*

## Definition — ContentStore

`Σ.C : T ⇀ Val` — a partial function mapping Istream addresses to content values. `T` is the set of tumblers (ASN-0034); `Val` is an unspecified set of content values, opaque at this level of abstraction. `dom(Σ.C)` is the set of I-addresses at which content has been stored.

## Definition — Arrangement

`Σ.M(d) : T ⇀ T` — a partial function mapping Vstream positions to Istream addresses for document `d`. `dom(Σ.M(d))` is the set of V-positions currently active in `d`; `ran(Σ.M(d))` is the set of I-addresses that `d` currently references.

## Definition — SubspaceOf

`subspace(v) = v₁` — the subspace identifier: the first component of the element-field V-position `v`.

## Definition — SubspacePositions

`V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}` — the set of V-positions in subspace `S` of document `d`.

## Definition — CorrespondenceRun

A *correspondence run* is a triple `(v, a, n)` — a V-position, an I-address, and a natural number `n ≥ 1` — such that:

`(A k : 0 ≤ k < n : Σ.M(d)(v + k) = a + k)`

At `k = 0` this is the base case `M(d)(v) = a`. Each subsequent `k` increments both the V-ordinal and the I-ordinal by the same amount.

## Definition — Origin

For every `a ∈ dom(Σ.C)`, the *origin* is the document-level prefix obtained by truncating the element field:

`origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

This is the full document tumbler `N.0.U.0.D`.

---

## Σ.C — ContentStoreType (DEF, type)

`Σ.C : T ⇀ Val`, mapping I-addresses to content values. `dom(Σ.C)` is the set of I-addresses at which content has been stored.

## Σ.M(d) — ArrangementType (DEF, type)

`Σ.M(d) : T ⇀ T`, mapping V-positions to I-addresses for document `d`. `dom(Σ.M(d))` is the set of V-positions currently active in `d`; `ran(Σ.M(d))` is the set of I-addresses that `d` currently references.

## S0 — ContentImmutability (INV, predicate)

For every state transition `Σ → Σ'`:

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)]`

In weakest-precondition terms, for any operation producing successor state `Σ'`:

`wp(op, (A a : a ∈ dom(C) : a ∈ dom(C') ∧ C'(a) = C(a)))`

must hold in every reachable state.

## S1 — StoreMonotonicity (LEMMA, predicate)

`[dom(Σ.C) ⊆ dom(Σ'.C)]`

for all state transitions `Σ → Σ'`. Corollary of S0.

## S2 — ArrangementFunctionality (INV, predicate)

For each document `d`, `Σ.M(d)` is a function — each V-position maps to exactly one I-address:

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) is uniquely determined)`

## S3 — ReferentialIntegrity (INV, predicate)

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`

The weakest precondition for S3 under an operation that adds a V-mapping `M(d)(v) = a` is:

`wp(add-mapping, S3) ⟹ a ∈ dom(Σ.C)`

## S4 — OriginBasedIdentity (LEMMA, predicate)

For I-addresses `a₁`, `a₂` produced by distinct allocation events:

`a₁ ≠ a₂`

regardless of whether `Σ.C(a₁) = Σ.C(a₂)`. From GlobalUniqueness (ASN-0034).

## S5 — UnrestrictedSharing (LEMMA, predicate)

S0–S3 do not entail any finite bound on sharing multiplicity:

`(A N ∈ ℕ :: (E Σ :: Σ satisfies S0–S3 ∧ (E a ∈ dom(Σ.C) :: |{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N)))`

Witness for cross-document sharing: fix any `N`. Construct state `Σ_N` with one I-address `a` where `C(a) = w` for some value `w`, and `N + 1` documents `d₁, ..., d_{N+1}`, each with `M(dᵢ) = {vᵢ ↦ a}` for distinct V-positions `vᵢ`. Sharing multiplicity of `a` is `N + 1 > N`.

Witness for within-document sharing: construct `Σ'_N` with one I-address `a` where `C(a) = w`, and one document `d` with `M(d) = {v₁ ↦ a, v₂ ↦ a, ..., v_{N+1} ↦ a}` for `N + 1` distinct V-positions. Within-document sharing multiplicity is `N + 1 > N`.

## S6 — PersistenceIndependence (LEMMA, predicate)

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)]`

regardless of any changes to any `Σ.M(d)`. Corollary of S0.

## S7a — DocumentScopedAllocation (INV, predicate)

Every Istream address is allocated under the tumbler prefix of the document that created it. For every `a ∈ dom(Σ.C)`, the document-level prefix of `a` — the tumbler `N.0.U.0.D` obtained by truncating the element field — identifies the document whose owner performed the allocation that placed `a` into `dom(C)`.

## S7b — ElementLevelAddresses (INV, predicate)

`(A a ∈ dom(Σ.C) :: zeros(a) = 3)`

Every address in `dom(Σ.C)` is an element-level tumbler: all four identifying fields — node, user, document, element — are present.

## S7 — StructuralAttribution (LEMMA, predicate)

Preconditions: S7a, S7b, T4 (ASN-0034), GlobalUniqueness (ASN-0034).

For every `a ∈ dom(Σ.C)`:

`origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

This is the full document tumbler `N.0.U.0.D` — uniquely identifying the allocating document across the system. Since I-addresses are permanent (S0) and unique (S4), this attribution is permanent and unseverable.

## S8-fin — FiniteArrangement (INV, predicate)

For each document `d`, `dom(Σ.M(d))` is finite.

## S8a — VPositionWellFormedness (INV, predicate)

`(A v ∈ dom(Σ.M(d)) : v₁ ≥ 1 : zeros(v) = 0 ∧ v > 0)`

The range guard `v₁ ≥ 1` captures both text-subspace (`v₁ = 1`) and link-subspace (`v₁ = 2`) V-positions. Link subspace semantics deferred to a future ASN.

## S8-depth — FixedDepthVPositions (INV, predicate)

`(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`

Within a given subspace of document `d`, all V-positions share the same tumbler depth.

## S8 — SpanDecomposition (THEOREM, lemma)

Preconditions: S8-fin, S8a, S2, S8-depth, T5, PrefixOrderingExtension, TA5(c), TA7a (ASN-0034).

For each document `d`, the text-subspace portion of the arrangement — `{(v, Σ.M(d)(v)) : v ∈ dom(Σ.M(d)) ∧ v₁ ≥ 1}` — can be decomposed into a finite set of correspondence runs `{(vⱼ, aⱼ, nⱼ)}` such that:

(a) The runs partition the text-subspace V-positions:

`(A v ∈ dom(Σ.M(d)) : v₁ ≥ 1 : (E! j :: vⱼ ≤ v < vⱼ + nⱼ))`

(b) Within each run:

`Σ.M(d)(vⱼ + k) = aⱼ + k` for all `k` with `0 ≤ k < nⱼ`

## D-CTG — VContiguity (INV, predicate)

**Design constraint.** For each document `d` and subspace `S`, `V_S(d)` is either empty or occupies every intermediate position between its extremes:

`(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`

Within each subspace, V-positions form a contiguous ordinal range with no gaps.

## D-MIN — VMinimumPosition (INV, predicate)

**Design constraint.** For each document `d` and subspace `S` with `V_S(d)` non-empty:

`min(V_S(d)) = [S, 1, ..., 1]`

where the tuple has length `m` (the common depth of V-positions in subspace `S` per S8-depth), and every component after the first is 1.

## D-CTG-depth — SharedPrefixReduction (LEMMA, lemma)

Preconditions: D-CTG, S8-fin, S8-depth.

For depth `m ≥ 3`, all positions in a non-empty `V_S(d)` share components 2 through `m − 1`. Contiguity reduces to contiguity of the last component alone — structurally identical to the depth 2 case.

*Proof sketch.* Suppose for contradiction that `V_S(d)` contains two positions `v₁ < v₂` (both depth `m` by S8-depth) whose first point of disagreement is at component `j` with `2 ≤ j ≤ m − 1` — that is, `(v₁)ᵢ = (v₂)ᵢ` for all `i < j`, and `(v₁)ⱼ < (v₂)ⱼ`. For any natural number `n > (v₁)ⱼ₊₁`, define `w` of length `m` by:

- `wᵢ = (v₁)ᵢ` for `1 ≤ i ≤ j`
- `wⱼ₊₁ = n`
- `wᵢ = 1` for `j + 2 ≤ i ≤ m`

Then `w` has subspace `S` and depth `m`, and `v₁ < w < v₂`. By D-CTG, every such `w` belongs to `V_S(d)`. By T0(a), unboundedly many values of `n` exist, yielding infinitely many distinct positions in `V_S(d)` — contradicting S8-fin. ∎

## D-SEQ — SequentialPositions (LEMMA, lemma)

Preconditions: D-CTG, D-MIN, S8-fin, S8-depth.

For each document `d` and subspace `S`, if `V_S(d)` is non-empty then there exists `n ≥ 1` such that:

`V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}`

where the tuple has length `m` (the common V-position depth in subspace `S`). At depth 2 this gives `V_S(d) = {[S, k] : 1 ≤ k ≤ n}`.

## ValidInsertionPosition — ValidInsertionPosition (DEF, predicate)

A V-position `v` is a *valid insertion position* in subspace `S` of document `d` satisfying D-CTG when one of two cases holds:

**Non-empty subspace.** `V_S(d) ≠ ∅` with `|V_S(d)| = N`. Write `m` for the common V-position depth in subspace `S` (S8-depth); `m ≥ 2`. Then either:
- `v = min(V_S(d))` (the `j = 0` case), or
- `v = shift(min(V_S(d)), j)` for some `j` with `1 ≤ j ≤ N`

In both cases, `#v = m`. This gives exactly `N + 1` valid insertion positions. The explicit form: `shift(min(V_S(d)), j) = [S, 1, ..., 1 + j]`.

**Empty subspace.** `V_S(d) = ∅`. Then `v = [S, 1, ..., 1]` of depth `m ≥ 2`, establishing the subspace's V-position depth at `m`. The lower bound `m ≥ 2` is required: at `m = 1`, `shift([S], 1) = [S] ⊕ [1]` produces `[S + 1]` — a position in subspace `S + 1`, not `S`. For `m ≥ 2`, OrdinalShift preserves the subspace identifier.

In both cases, `S = v₁` is the subspace identifier.

Structural properties of valid positions:
- *Depth preservation*: `#shift(v, j) = #v = m` for all `j ≥ 0` (OrdinalShift result-length identity, ASN-0034).
- *Subspace identity*: `shift(min, j)₁ = min₁ = S` for all `j` (since `δ(j, m)` has action point `m ≥ 2`, TumblerAdd copies component 1 unchanged).
- *Distinctness*: the `N + 1` positions have last components `1, 2, ..., N + 1` — pairwise distinct by T3 (ASN-0034).
- *S8a consistency*: every valid position `[S, 1, ..., 1 + j]` has all components strictly positive, so `zeros(v) = 0` and `v > 0`.

## S9 — TwoStreamSeparation (THEOREM, lemma)

Precondition: S0.

No modification to any arrangement `Σ.M(d)` can alter the content store `Σ.C`:

`[Σ'.M(d) ≠ Σ.M(d) ⟹ (A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))]`

*Proof.* S0 guarantees that `a ∈ dom(Σ.C)` implies `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)` for every state transition `Σ → Σ'`, unconditionally. The consequent of S9 is a special case of S0's universal guarantee, restricted to transitions that modify some arrangement. ∎
