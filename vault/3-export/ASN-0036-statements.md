# ASN-0036 Formal Statements

*Source: ASN-0036-streams.md (revised 2026-03-22) — Extracted: 2026-03-23*

## Definition — ContentStore

`Σ.C : T ⇀ Val` — a partial function mapping Istream addresses to content values. `T` is the set of tumblers (ASN-0034); `Val` is an unspecified set of content values, opaque at this level of abstraction. The domain `dom(Σ.C)` is the set of I-addresses at which content has been stored.

## Definition — Arrangement

`Σ.M(d) : T ⇀ T` — the arrangement of document `d`. A partial function mapping Vstream positions to Istream addresses. The domain `dom(Σ.M(d))` is the set of V-positions currently active in `d`; the range `ran(Σ.M(d))` is the set of I-addresses that `d` currently references.

## Definition — Subspace

`subspace(v) = v₁` — the subspace identifier, the first component of the element-field V-position `v`.

## Definition — SubspaceVPositions

`V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}` — the set of V-positions in subspace `S` of document `d`.

## Definition — CorrespondenceRun

A *correspondence run* is a triple `(v, a, n)` — a V-position, an I-address, and a natural number `n ≥ 1` — such that the arrangement preserves ordinal displacement within the run:

`(A k : 0 ≤ k < n : Σ.M(d)(v + k) = a + k)`

At `k = 0` this is the base case `M(d)(v) = a` — no displacement, no arithmetic. Each subsequent `k` increments both the V-ordinal and the I-ordinal by the same amount.

## Definition — Origin

For every `a ∈ dom(Σ.C)`, the *origin* is the document-level prefix obtained by truncating the element field:

`origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

This is the full document tumbler `N.0.U.0.D`.

---

## S0 — ContentImmutability (INV, predicate)

For every state transition `Σ → Σ'`:

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)]`

In weakest-precondition terms, for any operation producing successor state `Σ'`:

`wp(op, (A a : a ∈ dom(C) : a ∈ dom(C') ∧ C'(a) = C(a)))`

must hold in every reachable state.

## S1 — StoreMonotonicity (INV, corollary of S0)

`[dom(Σ.C) ⊆ dom(Σ'.C)]`

## S2 — ArrangementFunctionality (INV, predicate)

For each document `d`, `Σ.M(d)` is a function — each V-position maps to exactly one I-address:

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) is uniquely determined)`

## S3 — ReferentialIntegrity (INV, predicate)

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`

The weakest precondition for S3 under an operation that adds a V-mapping `M(d)(v) = a` is:

`wp(add-mapping, S3) ⟹ a ∈ dom(Σ.C)`

## S4 — OriginBasedIdentity (LEMMA, lemma)

For I-addresses `a₁`, `a₂` produced by distinct allocation events:

`a₁ ≠ a₂`

regardless of whether `Σ.C(a₁) = Σ.C(a₂)`.

Follows from T9 (same-allocator distinctness), T10 (non-nesting cross-allocator distinctness), and T10a + TA5(d) + T3 (nesting-prefix cross-allocator distinctness) (ASN-0034).

## S5 — UnrestrictedSharing (LEMMA, lemma)

S0–S3 do not entail any finite bound on sharing multiplicity:

`(A N ∈ ℕ :: (E Σ :: Σ satisfies S0–S3 ∧ (E a ∈ dom(Σ.C) :: |{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N)))`

Within a single document: for any `N`, there exists `Σ'_N` with one I-address `a` where `C(a) = w`, and one document `d` with `M(d) = {v₁ ↦ a, v₂ ↦ a, ..., v_{N+1} ↦ a}` for `N + 1` distinct V-positions. S2 holds — each `vᵢ` maps to exactly one I-address. S3 holds — `a ∈ dom(C)`. The within-document sharing multiplicity is `N + 1 > N`.

## S6 — PersistenceIndependence (LEMMA, corollary of S0)

The membership of `a` in `dom(Σ.C)` is independent of all arrangements:

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)]`

regardless of any changes to any `Σ.M(d)`.

## S7a — DocumentScopedAllocation (INV, predicate)

Every Istream address is allocated under the tumbler prefix of the document that created it. That is, for every `a ∈ dom(Σ.C)`, the document-level prefix of `a` — the tumbler `N.0.U.0.D` obtained by truncating the element field — identifies the document whose owner performed the allocation that placed `a` into `dom(C)`.

## S7b — ElementLevelAddresses (INV, predicate)

`(A a ∈ dom(Σ.C) :: zeros(a) = 3)`

## S7 — StructuralAttribution (LEMMA, lemma)

For every `a ∈ dom(Σ.C)`:

`origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

uniquely identifies the allocating document across the system. Three cases establish that distinct documents produce distinct prefixes:
- T9 (ForwardAllocation): distinct documents within an allocator have distinct prefixes (later allocations strictly greater)
- T10 (PartitionIndependence): documents from non-nesting independent allocators cannot share a prefix
- T10a + TA5(d) + T3: for nesting-prefix allocators, child outputs are deeper than parent's (`#inc(t, k') = #t + k'`), so document prefixes are distinct by T3

Since I-addresses are permanent (S0) and unique (S4), attribution is permanent and unseverable.

Follows from S7a, S7b, T4, T9, T10, T10a, TA5, T3 (ASN-0034).

## S8-fin — FiniteArrangement (INV, predicate)

For each document `d`, `dom(Σ.M(d))` is finite.

## S8a — VPositionWellFormedness (INV, predicate)

Every text-subspace V-position is an element-field tumbler with all components strictly positive:

`(A v ∈ dom(Σ.M(d)) : v₁ ≥ 1 : zeros(v) = 0 ∧ v > 0)`

A V-position represents the element field of a full document-scoped address — the fourth field in the T4 field structure. Its first component `v₁` is the subspace identifier; this ASN treats only the text subspace, where `v₁ ≥ 1`. The range guard `v₁ ≥ 1` captures both text-subspace (v₁ = 1) and link-subspace (v₁ = 2) V-positions.

The domain and range of `M(d)` live in structurally different tumbler subsets: within the text subspace, `{v ∈ dom(M(d)) : v₁ ≥ 1} ⊆ {t ∈ T : zeros(t) = 0 ∧ t > 0}` (element-field tumblers), while `ran(M(d)) ⊆ {t ∈ T : zeros(t) = 3}` (full element-level addresses, per S7b).

## S8-depth — FixedDepthVPositions (INV, predicate)

Within a given subspace `s` of document `d`, all V-positions share the same tumbler depth:

`(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`

## S8 — SpanDecomposition (THEOREM, lemma)

For each document `d`, the text-subspace portion of the arrangement — `{(v, Σ.M(d)(v)) : v ∈ dom(Σ.M(d)) ∧ v₁ ≥ 1}` — can be decomposed into a finite set of correspondence runs `{(vⱼ, aⱼ, nⱼ)}` such that:

(a) The runs partition the text-subspace V-positions: every text-subspace V-position in `dom(Σ.M(d))` falls in exactly one run —
`(A v ∈ dom(Σ.M(d)) : v₁ ≥ 1 : (E! j :: vⱼ ≤ v < vⱼ + nⱼ))`

(b) Within each run: `Σ.M(d)(vⱼ + k) = aⱼ + k` for all `k` with `0 ≤ k < nⱼ`

*Singleton decomposition existence.* By S8-fin, `dom(M(d))` is finite, hence so is `{v ∈ dom(M(d)) : v₁ ≥ 1}`. Each V-position `v` with `M(d)(v) = a` forms a singleton run `(v, a, 1)`. At `k = 0`: `M(d)(v + 0) = M(d)(v) = a = a + 0`.

*Uniqueness within a subspace.* A singleton `(v, a, 1)` claims the interval `[v, v + 1)`. By S8-depth, all V-positions in a subspace share depth `d`. For depth-`d` V-position `v` with `zeros(v) = 0` (S8a): `sig(v) = d` and TA5(c) gives `#(v+1) = #v = d`. For any `t` with `#t = d` and `v ≤ t < v + 1`: if `t ≠ v`, divergence at component `j < d` gives `t_j > v_j = (v+1)_j`, so `t > v + 1` — contradiction; divergence only at component `d` gives `t_d = v_d` by combining `t_d ≥ v_d` (from `v ≤ t`) and `t_d < v_d + 1` (from `t < v + 1`) — contradiction. Hence `t = v`.

*Cross-subspace separation.* By S8a, V-positions in subspace `s` share prefix `[s]`. By T5 (ContiguousSubtrees), tumblers extending `[s]` form a contiguous interval. By T10 (PartitionIndependence), for `s₁ ≠ s₂`, prefixes `[s₁]` and `[s₂]` are non-nesting, and their extensions are disjoint. No singleton interval in one subspace contains any tumbler from another.

Follows from S8-fin, S8a, S2, S8-depth, T1, T5, T10, TA5(c), TA7a (ASN-0034).

## D-CTG — VContiguity (DESIGN, predicate)

For each document d and subspace S, V_S(d) is either empty or occupies every intermediate position between its extremes:

`(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`

For the standard text subspace at depth m = 2: the intermediates between `[S, a]` and `[S, b]` are the finitely many `[S, i]` with `a < i < b`. Combined with S8-fin, contiguity at depth 2 says V_S(d) occupies a single unbroken block of ordinals.

## D-MIN — VMinimumPosition (DESIGN, predicate)

For each document d and subspace S with V_S(d) non-empty:

`min(V_S(d)) = [S, 1, ..., 1]`

where the tuple has length m (the common depth of V-positions in subspace S per S8-depth), and every component after the first is 1.

## D-CTG-depth — SharedPrefixReduction (COROLLARY, lemma)

For depth m ≥ 3, all positions in a non-empty V_S(d) share components 2 through m − 1.

*Proof sketch.* Suppose for contradiction that V_S(d) contains two positions v₁ < v₂ (both depth m by S8-depth) whose first point of disagreement is at component j with 2 ≤ j ≤ m − 1 — that is, (v₁)ᵢ = (v₂)ᵢ for all i < j, and (v₁)ⱼ < (v₂)ⱼ (since v₁ < v₂ by T1(i)). For any natural number n > (v₁)ⱼ₊₁, define w of length m by:
- wᵢ = (v₁)ᵢ for 1 ≤ i ≤ j
- wⱼ₊₁ = n
- wᵢ = 1 for j + 2 ≤ i ≤ m

Then w has subspace S and depth m. By T1(i): w > v₁ (since w agrees with v₁ on 1..j and n > (v₁)ⱼ₊₁), and w < v₂ (since w agrees with v₂ on 1..j−1 and wⱼ = (v₁)ⱼ < (v₂)ⱼ). By D-CTG, every such w belongs to V_S(d). By T0(a), unboundedly many values of n exist, yielding infinitely many distinct positions — contradicting S8-fin. ∎

Follows from D-CTG, S8-fin, S8-depth, T0(a), T1 (ASN-0034).

## D-SEQ — SequentialPositions (COROLLARY, lemma)

For each document d and subspace S, if V_S(d) is non-empty then there exists n ≥ 1 such that:

`V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}`

where the tuple has length m (the common V-position depth in subspace S). At depth 2 this gives `V_S(d) = {[S, k] : 1 ≤ k ≤ n}`.

*Derivation.* By D-CTG-depth (m ≥ 3) or trivially (m = 2), all positions in V_S(d) share components 2 through m − 1. By D-MIN, min(V_S(d)) = [S, 1, …, 1], so those shared components have value 1. Every position is therefore [S, 1, …, 1, k] for varying k. D-CTG restricted to the last component forbids gaps among the k values; D-MIN gives minimum k = 1; S8-fin bounds the maximum at some finite n.

Follows from D-CTG, D-CTG-depth, D-MIN, S8-fin, S8-depth.

## ValidInsertionPosition — ValidInsertionPosition (DEF, predicate)

A V-position v is a *valid insertion position* in subspace S of document d satisfying D-CTG when one of two cases holds:

- *Non-empty subspace.* V_S(d) ≠ ∅ with |V_S(d)| = N. Write m for the common V-position depth in subspace S (S8-depth); m ≥ 2. Then either v = min(V_S(d)) (the j = 0 case) or v = shift(min(V_S(d)), j) for some j with 1 ≤ j ≤ N. In both cases, #v = m.

- *Empty subspace.* V_S(d) = ∅. Then v = [S, 1, ..., 1] of depth m ≥ 2, establishing the subspace's V-position depth at m. The lower bound m ≥ 2 is necessary: at m = 1, v = [S] and shift([S], 1) = [S] ⊕ δ(1, 1) = [S] ⊕ [1]; the action point of [1] is k = 1, so TumblerAdd gives r₁ = S + 1, producing [S + 1] — a position in subspace S + 1, not S. For m ≥ 2, δ(n, m) has action point m, and since m > 1, TumblerAdd copies component 1 unchanged — OrdinalShift preserves the subspace identifier.

In both cases, S = v₁ is the subspace identifier. In the non-empty case, there are exactly N + 1 valid insertion positions. The explicit form: by D-MIN, min(V_S(d)) = [S, 1, ..., 1] of depth m, and `shift(min(V_S(d)), j) = [S, 1, ..., 1 + j]`.

*Distinctness.* The N + 1 positions have last components 1, 2, ..., N + 1 — pairwise distinct, so by T3 (CanonicalRepresentation, ASN-0034) the tumblers are pairwise distinct.

*Depth preservation.* For j ≥ 1, `#shift(v, j) = #v = m` by the result-length identity of OrdinalShift (ASN-0034). For j = 0, `#v = #min(V_S(d)) = m` by D-MIN.

*Subspace identity.* Since δ(j, m) has action point m ≥ 2, TumblerAdd copies component 1 unchanged: `shift(min, j)₁ = min₁ = S` for all j ≥ 1.

*S8a consistency.* For text-subspace positions (S ≥ 1), every valid position [S, 1, ..., 1 + j] has all components strictly positive, so `zeros(v) = 0` and `v > 0` — satisfying S8a.

## S9 — TwoStreamSeparation (THEOREM, lemma)

No modification to any arrangement `Σ.M(d)` can alter the content store `Σ.C`:

`[Σ'.M(d) ≠ Σ.M(d) ⟹ (A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))]`

*Proof.* S0 guarantees that `a ∈ dom(Σ.C)` implies `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)` for every state transition `Σ → Σ'`, unconditionally. The consequent of S9 is a special case of S0's universal guarantee, restricted to transitions that modify some arrangement. ∎

Follows from S0.
