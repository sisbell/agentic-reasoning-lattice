# ASN-0113 Claim Statements

*Source: ASN-0113-retrievedocvspanset-operation-per-subspace-document-extent-query.md (revised 2026-06-04) — Extracted: 2026-06-05*

## Definition — OccupiedPositions

`O(d) = dom(M(d))`

The set of *occupied V-positions* of `d`, well-defined under W-pre.

---

## Definition — ActivePositions

`V_S(d) = {v ∈ O(d) : subspace(v) = S}`

The *active V-positions of `d` in subspace `S`*. `subspace(v) = v₁` (ASN-0036). Convention: `s_C = 1`, `s_L = 2` (SubspaceConventionAxiom).

---

## Definition — VSlice

`VSlice(S, m) = {t ∈ T : t₁ = S ∧ #t = m ∧ zeros(t) = 0}`

The depth-`m`, zero-free tumblers of subspace `S`; the population from which active V-positions are drawn (S8a).

---

## Definition — OrdinalDisplacement

`δ(n, m) = [0,…,0,n]` of length `m`

The canonical pure depth-`m` shift.

---

## Definition — Shift

`shift(t, n) = t ⊕ δ(n, #t)`

Advances `t`'s last component by `n`.

---

## Definition — SpanReach

For span `σ = (s, ℓ)`:

`reach(σ) = s ⊕ ℓ`

---

## Definition — ExtentSpan

`ext(d, S) = (start_S, δ(n_S, m_S))`, where `start_S = [S,1,…,1]` of depth `m_S`.

The **extent span** of subspace `S` in document `d`, where `n_S = |V_S(d)|` and `m_S` is the common depth of all `v ∈ V_S(d)` (S8-depth).

---

## Definition — OccupiedSubspaces

`occupied(d) = {S ∈ {s_C, s_L} : V_S(d) ≠ ∅}`

---

## W-pre — OperationPrecondition (PRE, requires)

`RETRIEVEDOCVSPANSET(d)` requires `d ∈ dom(M)` (equivalently, by M0/M1 of ASN-0093, `Document(d) ∧ d ∈ dom(M)`: a T4-valid document-level tumbler that some K.δ event has placed into `dom(M)`).

---

## W0 — SpanSetValuedResult (SPEC, ensures)

For an *allocated* document `d` (W-pre), `RETRIEVEDOCVSPANSET(d)` returns a normalized span-set, never a content sequence and never a cardinality; for an allocated document that is *empty in both counted subspaces* (`d ∈ dom(M)` with `V_{s_C}(d) = V_{s_L}(d) = ∅`) it returns `⟨⟩`, the distinguished value denoting `∅` (which is not a T12 span, since every well-formed span is non-empty — S2, ASN-0053).

---

## W1 — SubspaceExtent (DEF, function)

`n_S(d) = |V_S(d)|` is the extent of subspace `S` in `d`.

---

## W2 — ExtentSpanEncoding (DEF, function)

`ext(d, S) = ([S,1,…,1], δ(n_S, m_S))` is the extent span encoding `n_S`, where `start_S = [S,1,…,1]` of depth `m_S`.

---

## W3 — ExtentSpanWellFormed (LEMMA, lemma)

`ext(d, S)` satisfies T12. The width `δ(n_S, m_S)` is positive because `n_S ≥ 1` (the run is non-empty), and its action point is its last position `m_S`, which equals `#start_S = m_S`, so `actionPoint(δ(n_S, m_S)) ≤ #start_S`. T12's two preconditions hold, so the span is well-formed; moreover it is level-uniform, `#δ(n_S, m_S) = m_S = #start_S`. Its reach is

`reach(ext(d, S)) = start_S ⊕ δ(n_S, m_S) = shift(start_S, n_S) = [S,1,…,1,1+n_S]`

one ordinal step past the last active position `[S,1,…,1,n_S]`, realizing the half-open convention under which the last occupied position is included and the next is excluded.

---

## W4 — ExactCoverage (LEMMA, lemma)

`⟦ext(d, S)⟧ ∩ VSlice(S, m_S) = V_S(d)`

(complete and exclusive).

Sub-claim: `⟦ext(d, S)⟧ = {t : start_S ≤ t < [S,1,…,1,1+n_S]}`. Take any `t ∈ VSlice(S, m_S)`. Such a `t` has the form `[S, t_2, …, t_{m_S}]` with all components positive. The bounds `start_S = [S,1,…,1]` and `reach = [S,1,…,1,1+n_S]` share the common prefix `[S,1,…,1]` of length `m_S − 1`, so by T5 (ContiguousSubtrees), applied with `start_S ≤ t < reach`, every interior `t` extends that prefix — its first `m_S − 1` components are pinned to `[S,1,…,1]`. The only remaining freedom is in the last component, which the half-open bounds pin to `1 ≤ t_{m_S} ≤ n_S`. These are exactly the elements `[S,1,…,1,k]` with `1 ≤ k ≤ n_S` — which is `V_S(d)` by D-SEQ★.

---

## W5 — ExactnessRequiresContiguity (LEMMA, lemma)

*Under the hypothesis `V_S(d) ≠ ∅`:* there exists a single level-uniform span `σ` of subspace `S` at depth `m` satisfying `⟦σ⟧ ∩ VSlice(S, m) = V_S(d)` *if and only if* `V_S(d)` is contiguous in `VSlice(S, m)` — i.e. `V_S(d)` contains every V-slice tumbler lying (under T1) between its own minimum and maximum.

Sub-claims:

(a) *Forward* (contiguous ⟹ a single exact span exists): Let `V_S(d)` be contiguous and non-empty, and put `a = min(V_S(d))`, `b = max(V_S(d))` under T1. Every element lies in `VSlice(S, m)`, so all share depth `m`, first component `S`, and are zero-free; write `a = [S, a_2, …, a_m]`. The whole run shares the prefix `[S, a_2, …, a_{m−1}]` and varies only in the last component; with `n_S = |V_S(d)|`, that block is `a_m, a_m+1, …, a_m + n_S − 1`, and `b = [S, a_2, …, a_{m−1}, a_m + n_S − 1]`. Define `σ = (a, δ(n_S, m))` — level-uniform and T12-well-formed, with `reach(σ) = shift(a, n_S) = [S, a_2, …, a_{m−1}, a_m + n_S]`. By T5 on the prefix `[S, a_2, …, a_{m−1}]` (length `m − 1`) shared by `a` and `reach(σ)`, every interior tumbler extends that prefix, and the half-open bounds pin its last component to `a_m ≤ t_m ≤ a_m + n_S − 1` — exactly the run. Hence `⟦σ⟧ ∩ VSlice(S, m) = V_S(d)`.

(b) *Converse* (non-contiguous ⟹ no single span is exact): Suppose `V_S(d)` is *not* contiguous: there exist `p, q ∈ V_S(d)` and `r ∈ VSlice(S, m)` with `p < r < q` and `r ∉ V_S(d)`. Let `σ` be any level-uniform span with `⟦σ⟧ ∩ VSlice(S, m) ⊇ V_S(d)`. Then `p, q ∈ ⟦σ⟧`, and since a span's denotation is order-convex (T12; S0 of ASN-0053), `p < r < q` forces `r ∈ ⟦σ⟧`. As `r ∈ VSlice(S, m)`, we get `r ∈ ⟦σ⟧ ∩ VSlice(S, m)` while `r ∉ V_S(d)`, so the intersection strictly exceeds `V_S(d)`.

(c) *Empty exclusion*: For empty `V_S(d)` the biconditional fails outright: its right-hand side is ill-defined, while its left-hand side is *false* — any level-uniform span `σ` of subspace `S` at depth `m` contains its own start `start(σ)`, so `start(σ) ∈ ⟦σ⟧ ∩ VSlice(S, m)`, making the intersection non-empty; equivalently, no span denotes `∅` (S2, ASN-0053). Handled separately by W0.

---

## W6 — OccupiedSubspacesDefinition (DEF, function)

`occupied(d) = {S ∈ {s_C, s_L} : V_S(d) ≠ ∅}`

---

## W7 — OneSpanPerOccupiedSubspace (SPEC, ensures)

`RETRIEVEDOCVSPANSET(d) = ⟨ ext(d, S) : S ∈ occupied(d), in increasing S ⟩`, the empty span-set `⟨⟩` when `occupied(d) = ∅`.

The result has exactly `|occupied(d)|` members — one per occupied subspace, *never one per contiguous fragment and never one per individual item*.

---

## W8 — PureQuery (INV, predicate)

`Σ' = Σ`. The operation reads `C`, `L`, `M`, and the document identity, and writes nothing — no allocation, no arrangement change, no provenance. It is a function of the present state alone.

---

## W9 — TwoKindsOnly (LEMMA, lemma)

`O(d) = V_{s_C}(d) ⊔ V_{s_L}(d)`

Derived from S3★-aux (SubspaceExhaustiveness, ASN-0047): `(A d, v : v ∈ dom(M(d)) : subspace(v) = s_C ∨ subspace(v) = s_L)`. The union is disjoint because `s_C ≠ s_L` (SC-NEQ). No third subspace holds content, so no third member can arise.

---

## W10 — SubspaceConfinement (LEMMA, lemma)

`(A t : t ∈ ⟦ext(d, S)⟧ : t₁ = S)`

The bounds are `start_S = [S,1,…,1]` and `reach = [S,1,…,1,1+n_S]`, both with first component `S`. Take any `t ∈ ⟦ext(d, S)⟧`, so `start_S ≤ t < reach`. If `t₁ < S`, then by T1 the first divergence is at position `1` and `t < start_S` — contradicting `start_S ≤ t`. If `t₁ > S`, then by T1 `t > reach` — contradicting `t < reach`. Hence `t₁ = S`, for `t` of any depth.

---

## W11 — Disjointness (LEMMA, lemma)

`⟦ext(d, s_C)⟧ ∩ ⟦ext(d, s_L)⟧ = ∅`

For any `t` in the intersection we would need `t₁ = s_C` and `t₁ = s_L` at once (W10), impossible since `s_C ≠ s_L` (SC-NEQ).

---

## W12 — ProfileIrreducibility (LEMMA, lemma)

The map `d ↦ (n_{s_C}(d), n_{s_L}(d))` is determined by neither coordinate alone. Formally, neither projection is injective on the profile: for any value of one coordinate there exist states realizing distinct values of the other —

`(A c, k₁, k₂ ∈ ℕ : k₁ ≠ k₂ : (E d₁, d₂ : n_{s_C}(d₁) = n_{s_C}(d₂) = c : n_{s_L}(d₁) = k₁ ∧ n_{s_L}(d₂) = k₂))`

and symmetrically with the roles of the subspaces exchanged.

---

## W13 — UniformShape (INV, predicate)

The result is a normalized span-set whose members occupy positions drawn from the fixed, ordered kind-list `(s_C, s_L)`. The shape of the report is invariant across the docuverse; only the magnitudes `n_S` differ.

Sub-claim (normalization): The result is already normalized — sorted and separated (ASN-0053) — because the two members are disjoint and ordered `s_C < s_L`, with `reach(ext(d, s_C)) < start_{s_L}` by T1, so no merging is possible and the sequence is in normal form (W11).

---

## W14 — Comparability (LEMMA, lemma)

For any two allocated documents `d₁, d₂`, the per-kind comparison `n_S(d₁)` versus `n_S(d₂)` is well-defined for each `S ∈ {s_C, s_L}`.

The comparison is total because `n_S(d) = |V_S(d)|` is a *total function* (W1), defined for every allocated `d` and every `S ∈ {s_C, s_L}` independently of whether the operation emits a member for that subspace; an empty subspace has `n_S(d) = 0` as a fact about `V_S(d)`, regardless of the report's membership.

---

## W15 — Independence (LEMMA, lemma)

`n_{s_C}(d)` is a function of `V_{s_C}(d)` alone, and `n_{s_L}(d)` of `V_{s_L}(d)` alone; consequently an edit confined to one subspace leaves the other subspace's reported extent unchanged.

Each count is read off a *disjoint* position set: `V_S(d) = {v ∈ O(d) : v₁ = S}` is selected by the predicate `v₁ = S`, and `s_C ≠ s_L` (SC-NEQ) makes `V_{s_C}(d)` and `V_{s_L}(d)` disjoint, so `n_{s_C} = |V_{s_C}(d)|` and `n_{s_L} = |V_{s_L}(d)|` are computed from non-overlapping data (W1). As a conditional: an edit confined to one subspace leaves the other's count untouched — a content edit cannot alter `V_{s_L}(d)` and a link edit cannot alter `V_{s_C}(d)`.

---

## W16 — Partition (LEMMA, lemma)

`(⊔ S : S ∈ occupied(d) : ⟦ext(d, S)⟧ ∩ VSlice(S, m_S)) = {v ∈ O(d) : v₁ ∈ {s_C, s_L}}`

a *disjoint* union (W11 gives disjointness; W4 gives that each part is exactly `V_S(d)`; and `O(d)` restricted to the counted subspaces is `V_{s_C}(d) ⊔ V_{s_L}(d)` by definition). No counted position is orphaned and no member claims a position that is not active.

---

## W17 — ExtentDeterminesPopulation (LEMMA, lemma)

For each occupied `S`, the active positions of `S` are exactly those V-slice tumblers lying within `ext(d, S)` (W4 restated as a fidelity claim), and each such position carries content — `M(d)(v) ∈ dom(C)` for `S = s_C`, `M(d)(v) ∈ dom(L)` for `S = s_L` (S3★).

---

## W18 — DerivedReport (INV, predicate)

`RETRIEVEDOCVSPANSET(d)` is a pure function of the current state `Σ` (by W8), so any two queries against the *same* `Σ` return identical span-sets, and any query against a *changed* `Σ` may legitimately differ.

---

## W19 — StateStability (INV, predicate)

Against an unchanged state `Σ`, repeated queries return identical span-sets; a later report contradicts an earlier one only if `M(d)` changed in between. The link count is specifically the count of *home* links — links the document owns (CL-OWN) — so a third party linking *into* the document, owning its link at another address, cannot perturb the document's reported link extent.

---

## W20 — ResultCardinalityWP (LEMMA, lemma)

The empty result:

`wp(RETRIEVEDOCVSPANSET(d), "result = ⟨⟩") ≡ d ∈ dom(M) ∧ V_{s_C}(d) = ∅ ∧ V_{s_L}(d) = ∅`

The two-member result:

`wp(RETRIEVEDOCVSPANSET(d), "|result| = 2") ≡ d ∈ dom(M) ∧ V_{s_C}(d) ≠ ∅ ∧ V_{s_L}(d) ≠ ∅`

The one-member result:

`wp(RETRIEVEDOCVSPANSET(d), "|result| = 1") ≡ d ∈ dom(M) ∧ (V_{s_C}(d) = ∅ ⊻ V_{s_L}(d) = ∅)`

The three preconditions partition the allocated states (`d ∈ dom(M)`) by the pair of emptiness bits — `(∅, ∅)`, exactly one empty, neither empty — exhausting the result's three possible cardinalities.
