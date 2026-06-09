# ASN-0121 Claim Statements

*Source: ASN-0121-findlinksfromtothree-operation.md (revised 2026-06-08) — Extracted: 2026-06-09*

## Definition — Touch

`touch(e, r) ≡ coverage(e) ∩ coverage(r) ≠ ∅`

Where `e, r ∈ Endset`, `Endset = 𝒫_fin(Span)`, and `coverage` maps an endset to the union of its constituent spans' address ranges.

---

## Definition — AtHome

`athome(a, H) ≡ home(a) ∈ coverage(H)`

Where `a` is a link address, `home(a)` is the document-level prefix `N(a).0.U(a).0.D(a)`, and `H ∈ Endset ∪ {∗}`.

---

## Definition — Lift

```
lift(e, ∗) ≡ true,    lift(e, r) ≡ touch(e, r)   for r ≠ ∗
liftH(a, ∗) ≡ true,   liftH(a, H) ≡ athome(a, H)  for H ≠ ∗
```

---

## Definition — Sat

`sat(a, q, Σ) ≡ liftH(a, H) ∧ lift(Σ.L(a).e₁, F) ∧ lift(Σ.L(a).e₂, G) ∧ lift(Σ.L(a).e₃, Θ)`

Where `q = (H, F, G, Θ) ∈ (Endset ∪ {∗})⁴`, `Σ.L(a) = (e₁, e₂, …)` with `N ≥ 3` endsets, and only slots `e₁, e₂, e₃` are tested; slots `e₄ … eₙ` are unconstrained.

---

## Definition — Addressable

`addressable(Σ) = dom(Σ.L) \ nullified(Σ)`

Where `nullified(Σ) = { a ∈ dom(Σ.L) : (E (b, F', G') ∈ L_R^Σ :: a ∈ coverage(G')) }` (ASN-0086), and `L_R^Σ` is the retraction relation — the subset of link triples `(a, F, G) ∈ dom(Σ.L) × Endset × Endset` with `|Σ.L(a)| = 3` and slot-3 coverage equal to `coverage(R)` for the designated retraction-type representative `R`.

---

## Definition — LiftHD

`liftH_d(q.H) ≡ (q.H = ∗) ∨ (d ∈ coverage(q.H))`

Where `d = home(ℓ)` for a fresh link address `ℓ`. Used in FL-WP as the residence conjunct specialised to a fixed home `d`.

---

## FL-DEF — FindLinksDefinition (DEF, definition)

`findlinks(q, Σ) = { a ∈ addressable(Σ) : sat(a, q, Σ) }`

With `sat` the conjunction of the four lifted slot-criteria (AND of the ORs); `addressable(Σ) = dom(Σ.L) \ nullified(Σ)` (ASN-0086, monotone by R6a); the operation has frame `Σ` (reads only, writes nothing).

---

## FL-DEC — FindLinksDecidability (LEMMA, lemma)

For any two endsets `e, r ∈ Endset`, `touch(e, r)` is decidable using only T2 comparisons and TumblerAdd; consequently `sat(a, q, Σ)` is decidable per link, and `findlinks(q, Σ) ⊆ dom(Σ.L)` is a finite, computable set (L-fin, ASN-0093).

*Proof sketch.* By `Endset = 𝒫_fin(Span)` (ASN-0043), `e ∪ r` is finite, so `coverage(e)` and `coverage(r)` are each a finite union of half-open T1-intervals `[s, s ⊕ ℓ)` (T12, ASN-0034). Sort the finite endpoint set `{s : (s, ℓ) ∈ e ∪ r} ∪ {s ⊕ ℓ : (s, ℓ) ∈ e ∪ r}` under T1 into distinct values `c₁ < … < c_m`; each coverage is constant (in or out) on every cell between consecutive endpoints, so `coverage(e) ∩ coverage(r) ≠ ∅` iff some cell with a representative is in both — a cell-wise membership comparison, finitely many T2 tests. The home test `athome(a, H) ≡ home(a) ∈ coverage(H)` is decidable by the same finite cell membership. Hence `sat` — a conjunction of four decidable tests — is decidable. `nullified(Σ)`-membership is decidable by CoverageEqualityDecidable (ASN-0086), so `addressable(Σ) = dom(Σ.L) \ nullified(Σ)` is enumerable, and `findlinks(q, Σ) ⊆ dom(Σ.L)` is finite and computable.

---

## FL-SND — FindLinksSoundness (LEMMA, lemma)

`(A a : a ∈ findlinks(q, Σ) : sat(a, q, Σ))`

No returned link fails any of the four criteria. Equivalently, in contrapositive form: if any constrained slot is *wholly disjoint* from the request — `coverage(Σ.L(a).eᵢ) ∩ coverage(Rᵢ) = ∅` for a constrained `Rᵢ`, or `home(a) ∉ coverage(H)` for a constrained `H` — then `a` is not returned. There are no false positives.

---

## FL-CMP — FindLinksCompleteness (LEMMA, lemma)

`(A a : a ∈ addressable(Σ) ∧ sat(a, q, Σ) : a ∈ findlinks(q, Σ))`

Every currently addressable link meeting all four criteria is returned; none is silently omitted. The result is *exactly* the satisfying subset of `addressable(Σ)`.

---

## FL-JUNK — FindLinksNonImpedance (LEMMA, lemma)

Let `Σ → Σ'` be a transition that adds links but matches none of them and retracts none — `dom(Σ.L) ⊆ dom(Σ'.L)`, `nullified(Σ') = nullified(Σ)`, and `(A a : a ∈ dom(Σ'.L) \ dom(Σ.L) : ¬ sat(a, q, Σ'))` — and that preserves the values and home-projections of existing links. Then `findlinks(q, Σ') = findlinks(q, Σ)`. The body of irrelevant links, however vast, neither enlarges the answer nor displaces a qualifying link from it.

---

## FL-RES — FindLinksResidenceEndpointIndependence (LEMMA, lemma)

The home criterion is a function of the link address alone; the from/to/type criteria are functions of the link value alone. The four constraints are therefore *independent* slots of the request: residence may be constrained without constraining endpoints, and conversely. In particular, with `F = G = Θ = ∗` the result is every addressable link residing in `H`, irrespective of what it connects; with `H = ∗` the result is every addressable link whose endpoints match, irrespective of where it lives.

---

## FL-DIR — FindLinksPositionalDirectionality (LEMMA, lemma)

The from-criterion tests `Σ.L(a).e₁` and the to-criterion tests `Σ.L(a).e₂`; the slots are matched by position, not symmetrically. The asymmetry is observable, and we exhibit an explicit witness. Take two distinct content I-addresses `x = [1,0,1,0,1,0,1,5]` and `y = [1,0,1,0,1,0,1,9]` (both element-level, `zeros = 3`, text subspace `s_C = 1`, differing only in the last component), and the unit-depth request endsets `X = {(x, δ(1,#x))}` and `Y = {(y, δ(1,#y))}`. By PrefixSpanCoverage (ASN-0043), `coverage(X) = {t : x ≼ t}` and `coverage(Y) = {t : y ≼ t}`; since `x` and `y` are equal-length and non-nesting (T1, ASN-0034), these subtrees are disjoint, so `coverage(X) ∩ coverage(Y) = ∅`. Now let `a` be a link with from-endset `e₁ = X` and to-endset `e₂ = Y`. Then for `q = (∗, X, Y, ∗)`, `lift(e₁, X) = true` and `lift(e₂, Y) = true`, so `sat(a, q, Σ)` holds and `a ∈ findlinks((∗, X, Y, ∗), Σ)`; for the reversed `q' = (∗, Y, X, ∗)`, `lift(e₁, Y) ≡ touch(e₁, Y) = (coverage(X) ∩ coverage(Y) ≠ ∅) = false`, so `sat(a, q', Σ)` fails and `a ∉ findlinks((∗, Y, X, ∗), Σ)`. Reversing the two endpoint constraints is therefore not a no-op.

---

## FL-TYP — FindLinksTypeByAddress (LEMMA, lemma)

The type criterion tests `touch(Σ.L(a).e₃, Θ)`, an overlap of address coverages, and never reads content stored at any type address. Three consequences follow.

*(a) Ghost types.* A type address need not lie in `dom(Σ.C)`; an endset whose coverage includes addresses with no stored content is a valid, matchable type — "Link types may be ghost elements" (4/45).

*(b) Independent constraint.* Because the type participates in `sat` on equal footing with from and to, a request may constrain type alone — `findlinks((∗, ∗, ∗, Θ), Σ)` returns every addressable link of a kind touching `Θ`, leaving from and to open.

*(c) Hierarchy by containment.* A type request whose span is rooted at a supertype address `p` covers the whole subtree `{t : p ≼ t}` (PrefixSpanCoverage, ASN-0043), so a single type span matches all subtypes of `p`; the type slot is searchable for super- and sub-types without any registry.

---

## FL-WILD — FindLinksWildcardSemantics (LEMMA, lemma)

A wildcard slot imposes no constraint: `findlinks` with a wildcard component returns exactly the links the *remaining* constrained slots admit. In the limit `findlinks((∗, ∗, ∗, ∗), Σ) = addressable(Σ)` — all currently addressable links — and a single constrained slot yields precisely the links matching that slot alone. This is the formal reading of Nelson's "If the home-set is the whole docuverse, all links between these two elements are returned" (4/63): an unconstrained axis widens, never empties, the result. `addressable(Σ)` here ranges over links of *every* arity `N ≥ 3`; a higher-arity link is admitted by the all-wildcard request like any other, and under a constrained request is matched on its first three endsets alone (its slots `e₄ … eₙ` never enter `sat`).

---

## FL-EMP — FindLinksEmptyConstraintZero (LEMMA, lemma)

For a constrained slot whose endset has empty coverage, `lift(e, ∅) ≡ touch(e, ∅) ≡ coverage(e) ∩ ∅ ≠ ∅` is `false` for every link `a` (and likewise `liftH(a, H) ≡ home(a) ∈ ∅` is `false` when `H` has empty coverage). Hence if *any* constrained component of `q` has empty coverage, `findlinks(q, Σ) = ∅` regardless of the store's contents.

By the symmetry of `touch`, the same zero applies to a *link's* own empty endset (L3 permits `e₁ = ∅` or `e₂ = ∅`): for any constrained `F ≠ ∗`,

`lift(∅, F) ≡ touch(∅, F) ≡ coverage(∅) ∩ coverage(F) = ∅ ∩ coverage(F) = ∅`

so `lift(∅, F) = false` and the link is excluded from every constrained from-slot. Under the from-wildcard `F = ∗`, `lift(∅, ∗) = true` drops the slot from the conjunction. The to-side is identical with `e₂` and the to-request `G`.

---

## FL-CUR — FindLinksCurrency (LEMMA, lemma)

`a ∈ findlinks(q, Σ) ⟺ a ∈ addressable(Σ) ∧ sat(a, q, Σ)`

The result is the faithful, exhaustive satisfying subset of the currently addressable links. *Forward* (`a ∈ findlinks(q, Σ) ⟹ a ∈ addressable(Σ) ∧ sat(a, q, Σ)`): FL-DEF's set-builder `{ a ∈ addressable(Σ) : sat(a, q, Σ) }` supplies *both* conjuncts. *Backward* (`a ∈ addressable(Σ) ∧ sat(a, q, Σ) ⟹ a ∈ findlinks(q, Σ)`): this is FL-CMP.

---

## FL-MON — FindLinksMonotoneAccumulation (LEMMA, lemma)

For any reachable `Σ →* Σ'` with `a ∉ nullified(Σ')`: if `a ∈ findlinks(q, Σ)` then `a ∈ findlinks(q, Σ')`. A matching link, once found and not withdrawn, stays found as the store grows.

(By LP13 (ASN-0098, UnconditionalLinkPersistence) `Σ'.L(a) = Σ.L(a)` across the reachability closure `Σ →* Σ'`, and `home(a)` is a projection of the fixed address `a`, so `sat(a, q, Σ') = sat(a, q, Σ)`; and `a ∈ addressable(Σ')` because `a ∈ dom(Σ'.L)` by link-store monotonicity across `Σ →* Σ'` (ASN-0098 StoreMonotonicity★) and `a ∉ nullified(Σ')` by hypothesis.)

---

## FL-WP — FindLinksWeakestPrecondition (LEMMA, lemma)

*Scope.* Each case presupposes `enabled(K.λ)` — K.λ's freshness `ℓ ∉ dom(Σ.L)`, L3 well-formedness (arity `≥ 3`, slot-3 type endset non-empty), and `home(ℓ) ∈ dom(Σ.M)` (ASN-0093 K.λ). The displayed conjunctions are the weakest *additional* precondition; the full wp is `enabled(K.λ) ∧ ⟨displayed conjunction⟩`.

*(a) Entry of a fresh ordinary link.* Let `Σ → Σ'` be a K.λ step allocating a fresh address `ℓ ∉ dom(Σ.L)` with value `Σ'.L(ℓ) = (F, G, Θ)` of arity `N ≥ 3`, homed at `d = home(ℓ)`, where `ℓ ∉ L_R^{Σ'}` (ordinary: either `coverage(Θ) ≠ coverage(R)` of any arity, or `coverage(Θ) = coverage(R)` with `N > 3`). Then:

`wp(K.λ, ℓ ∈ findlinks(q, ·)) ≡ ℓ ∉ nullified(Σ') ∧ liftH_d(q.H) ∧ lift(F, q.F) ∧ lift(G, q.G) ∧ lift(Θ, q.Θ)`

where `liftH_d(q.H) ≡ (q.H = ∗) ∨ (d ∈ coverage(q.H))`, and the addressability conjunct unfolds as `ℓ ∉ nullified(Σ') ≡ ¬(E (b, F', G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))`. This conjunct is not discharged by freshness alone — a pre-existing retraction tuple may cover the ghost-allocated `ℓ`.

*(c) Entry of a fresh retraction link.* Let `Σ → Σ'` be a K.λ step allocating a fresh address `b ∉ dom(Σ.L)` with value `Σ'.L(b) = (F_b, G', Θ_b)` of *arity exactly 3* with `coverage(Θ_b) = coverage(R)`, so `b ∈ L_R^{Σ'}` and `L_R^{Σ'} = L_R^Σ ∪ {(b, F_b, G')}`, with `d = home(b)`. Then:

`wp(K.λ, b ∈ findlinks(q, ·)) ≡ ¬(E (c, F'', G'') ∈ L_R^Σ :: b ∈ coverage(G'')) ∧ b ∉ coverage(G') ∧ liftH_d(q.H) ∧ lift(F_b, q.F) ∧ lift(G', q.G) ∧ lift(Θ_b, q.Θ)`

Cases (a) and (c) are complementary and exhaustive over the fresh-link space (partitioned by `ℓ ∉ L_R^{Σ'}` vs. `b ∈ L_R^{Σ'}`).

*(b) Survival of an existing match under retraction.* Let `Σ → Σ'` be a K.λ step committing a retraction tuple with to-coverage `coverage(G')`. For an existing link `a ∈ dom(Σ.L)`:

`wp(K.λ_retract, a ∈ findlinks(q, ·)) ≡ a ∈ findlinks(q, Σ) ∧ a ∉ coverage(G')`

---

## FL-STB — FindLinksStabilityUnderEditing (LEMMA, lemma)

For a transition `Σ → Σ'` that preserves the link store — `Σ'.L = Σ.L` — and any request `q` (necessarily an I-address request, the grammar's only kind), `findlinks(q, Σ') = findlinks(q, Σ)`. The single hypothesis `Σ'.L = Σ.L` suffices: because `nullified` is a function of `Σ.L` alone (it is defined through the retraction relation `L_R^Σ ⊆ Σ.L`), `Σ'.L = Σ.L` already entails `nullified(Σ') = nullified(Σ)`, so retraction-set preservation is a consequence of the link-store hypothesis rather than an independent assumption. Pure-arrangement edits (insertion, deletion, rearrangement) and content appends, which preserve `Σ.L`, leave the answer invariant.

---

## FL-RET — FindLinksRetractionAbsence (LEMMA, lemma)

If `a ∈ nullified(Σ)`, then for every reachable `Σ →* Σ'` and every request `q`, `a ∉ findlinks(q, Σ')`. The exclusion is total: even if `a`'s endsets would still satisfy every endpoint criterion, `a ∉ addressable(Σ')` removes it from FL-DEF, and the non-decrease of `nullified` across the full transition vocabulary — R6a (ASN-0086) across K.λ, and constancy of `nullified` across every other operation in `→` (all of which leave `Σ.L`, hence `L_R^Σ`, untouched) — keeps it out forever.

---

## FL-REACH — FindLinksCrossDocumentReach (LEMMA, lemma)

For any request `q` (an I-address request, the grammar's only kind), `findlinks(q, Σ)` is independent of `Σ.M`. Four consequences follow.

*(a) Every home is reached.* The store is searched whole; a link is eligible regardless of which document homes it, so in-links — stored in documents other than the one being read — are found on equal footing with out-links.

*(b) Transclusion is found once.* When the same endpoint content is shared across documents, the link is indexed by that content's I-addresses and is found exactly once by content identity, however many documents surface it.

*(c) Whole-docuverse residence.* Setting `H = ∗` imposes no residence bound, returning all matching links wherever homed.

*(d) Superset of the satisfying discoverable links.* The formal containment is:

`findlinks(q, Σ) ⊇ ⋃_d { a : a ∈ addressable(Σ) ∧ sat(a, q, Σ) ∧ discoverable_from(a, d, Σ) }`

Every satisfying, addressable link that some document `d` surfaces is in the result. The inclusion is *strict* whenever a satisfying, addressable *orphan* exists — an addressable `a` with `sat(a, q, Σ)` whose endset I-addresses lie in no arrangement range, so `discoverable_from(a, d, Σ)` fails for every `d` yet `a ∈ findlinks(q, Σ)`. (Note: `findlinks(q, Σ)` is *not* in general a superset of the bare, request-independent discoverable union `⋃_d { a : discoverable_from(a, d, Σ) }`; only the satisfying restriction holds.)
