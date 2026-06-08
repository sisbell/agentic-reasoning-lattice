# ASN-0107 Claim Statements

*Source: ASN-0107-findnumoflinksfromtothree-operation.md (revised 2026-06-04) — Extracted: 2026-06-07*

## Definition — Sat

`sat(a, Q, Σ) ≡ (A i : 1 ≤ i ≤ 3 : coverage(Σ.L(a).eᵢ) ∩ Qᵢ ≠ ∅)` — conjunctive across slots, disjunctive within

**Variables:** `a ∈ dom(Σ.L)` is a link address; `Q = (Q₁, Q₂, Q₃)` is a counting request with each `Qᵢ ⊆ T`; `Σ.L : T ⇀ Link` is the link store; `coverage(e)` is the combinatorial projection of endset spans that consults no state component; `Σ.L(a).eᵢ` is the `i`-th endset of the link at `a`.

---

## Definition — MatchingSet

`match(Q, Σ) = {a ∈ dom(Σ.L) : sat(a, Q, Σ)}` — the matching set

---

## Definition — Count

`num(Q, Σ) = |match(Q, Σ)|` — the count; total and finite (L-fin)

---

## Definition — DiscoveryCount

Given querying document `d_q ∈ dom(Σ.M)` and query V-regions `W = (W₁, W₂, W₃)`:

> `Qᵢ(Σ) = {Σ.M(d_q)(v) : v ∈ Wᵢ ∩ dom(Σ.M(d_q))}`
>
> `num_disc(d_q, W, Σ) = num(Q(Σ), Σ)`

---

## P0 — CountIsCardinality (PROP, predicate)

`num(Q, Σ) = |match(Q, Σ)|`, a natural number whose unit is the link address `a ∈ dom(Σ.L)`. Neither endpoints, nor documents touched, nor the index entries by which a link is found, are the unit of the count.

---

## P1 — LinkAtomicity (PROP, predicate)

For each `a ∈ dom(Σ.L)`, the contribution of `a` to `num(Q, Σ)` is `[sat(a, Q, Σ)] ∈ {0, 1}`. The breadth of an endset — the number of spans, endpoints, or documents its coverage touches — enlarges `coverage(Σ.L(a).eᵢ)` and so can only make the intersection test *easier to pass*; it never multiplies the contribution. A link with a multi-span endset that meets the request in several places is counted once.

---

## P2 — IdentityIndividuation (PROP, predicate)

For distinct addresses `a ≠ a'` with `Σ.L(a) = Σ.L(a')`, both satisfy `Q` or both fail, and if both satisfy they contribute `2` to the count. Distinct allocation events produce distinct link addresses (GlobalUniqueness, ASN-0034; L11a), and the store imposes no value-injectivity (L11b permits equal-valued links at distinct addresses). The count therefore individuates by address; identical descriptions are never merged.

---

## P3 — StoreResidence (PROP, predicate)

`match(Q, Σ) ⊆ dom(Σ.L)`. The count ranges over the links the store holds at `Σ`, never over a hypothetical or historical population outside it.

---

## E1 — CoveragePermanence (LEMMA, lemma)

For fixed `Q` and any `Σ →* Σ'`, every `a ∈ dom(Σ.L)` satisfies `sat(a, Q, Σ') ⟺ sat(a, Q, Σ)`. Satisfaction against permanent address sets is decided by the link's stored value, which is itself permanent (L12).

---

## E2 — ExistenceMonotonicity (LEMMA, lemma)

For fixed `Q`, `Σ →* Σ' ⟹ num(Q, Σ) ≤ num(Q, Σ')`. The store grows (L12a), coverage is invariant (E1), so `match(Q, Σ) ⊆ match(Q, Σ')`: the matching set only gains members. The existence count never falls.

---

## E3 — ContentInvariance (LEMMA, lemma)

For fixed `Q`, the transitions that allocate content (K.α), extend, contract, or reorder an arrangement (K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~), register a document (K.σ/K.δ), or record provenance (K.ρ) all leave `num(Q, Σ)` unchanged. By E1, `sat` depends on neither `Σ.C` nor `Σ.M`; only a link-creation transition (K.λ) touches `dom(Σ.L)`.

---

## E4 — CreationConservation (LEMMA, lemma)

For fixed `Q`, `num(Q, Σ') − num(Q, Σ)` over `Σ →* Σ'` equals the number of links created on that path whose stored value satisfies `Q`. Creation is the sole source of change, and each matching creation adds exactly one (P0, P2); the substrate provides no link-removal transition (L12), so no term subtracts.

---

## D1 — PresentTenseResolution (LEMMA, lemma)

`Qᵢ(Σ)` is a live reading of `d_q`'s arrangement. Editing `d_q` moves content into or out of the queried V-region without any link being created or retracted, so the resolved request — and hence `num_disc` — can change while `dom(Σ.L)` is fixed.

---

## D2 — DiscoveryNonMonotonicity (LEMMA, lemma)

`num_disc` is not monotone across `Σ →* Σ'`, because the resolved request `Qᵢ(Σ)` — the *forward image* of the **fixed** V-region `Wᵢ` under `d_q`'s arrangement — moves with the arrangement.

- *Extension (K.μ⁺ or K.μ⁺_L).* For every `v ∈ Wᵢ ∩ dom(Σ.M(d_q))` the image `Σ'.M(d_q)(v) = Σ.M(d_q)(v)` survives, and new positions falling in `Wᵢ` may add images. Hence `Qᵢ(Σ) ⊆ Qᵢ(Σ')` — the resolved request can only grow.
- *Contraction (K.μ⁻).* The contracted arrangement agrees with the prior one on its retained, smaller domain. So `Qᵢ(Σ') ⊆ Qᵢ(Σ)` — the resolved request can only shrink.
- *Reordering (K.μ~).* The witnessing bijection `π` carries `Σ'.M(d_q)(v) = Σ.M(d_q)(π⁻¹(v))`, so `Qᵢ(Σ') = {Σ.M(d_q)(u) : u ∈ π⁻¹(Wᵢ) ∩ dom(Σ.M(d_q))}`. This need **not** equal `Qᵢ(Σ)`. The forward image of the fixed sub-region `Wᵢ` is preserved exactly when the two image sets agree: `Qᵢ(Σ') = Qᵢ(Σ) ⟺ {Σ.M(d_q)(u) : u ∈ π⁻¹(Wᵢ) ∩ dom} = {Σ.M(d_q)(u) : u ∈ Wᵢ ∩ dom}`. A *sufficient* condition is that `π` fix `Wᵢ` setwise (`π⁻¹(Wᵢ) ∩ dom = Wᵢ ∩ dom`). It is *not necessary*: content sharing (M13/S5) means a non-trivial reorder that does not fix `Wᵢ` setwise can still leave the image set unchanged — it suffices that `π` permute positions within each shared-image class without carrying a distinctly-imaged position across the `Wᵢ` boundary.

Because the resolved request itself rises and falls, the composite count rises and falls.

---

## D3 — ZeroIsPresentNotHistorical (LEMMA, lemma)

`num(Q, Σ) = 0` asserts that no link in `dom(Σ.L)` satisfies `Q` *at `Σ`*. It does not assert that no such link ever existed, nor that none is discoverable from another document or another arrangement. Absence from the present count is non-existence *in the view*, not non-existence *in the archive*.

---

## A1 — FreshContentNeutrality (LEMMA, lemma)

Inserting freshly-allocated content — new I-addresses carrying no incoming links — into any arrangement leaves the count unchanged for a request whose parts denote unchanged content. For the existence count the neutrality is *unconditional*: K.α changes neither `dom(Σ.L)` nor any `coverage` nor the fixed `Q` (E3), so `match(Q, ·)` is invariant regardless of where — or whether — the new address `a_new` sits in `Q`. The membership `a_new ∈ Q` does not move the existence count: if some stored link `ℓ` already covers `a_new` (a ghost reference, LP17), then `coverage(Σ.L(ℓ).eᵢ) ∩ Qᵢ ∋ a_new` holds identically before and after the K.α step that materialises content at `a_new` — `ℓ` matched before allocation and matches after — so the count does not move; and if no stored link covers `a_new`, there is nothing to add. For the existence count this is a special case of E3; for the discovery count it holds directly from the no-incoming-links premise — no stored link has `a_new ∈ coverage(Σ.L(a).eᵢ)`, so even arranging `a_new` into a queried V-region (a K.μ⁺ step that places it in some `Qᵢ(Σ')`) creates no new match.

---

## A2 — TransclusionDiscoverability (LEMMA, lemma)

Transcluding existing content into a new document `d_new` — installing arrangement entries in `d_new` that map V-positions to the *same* shared I-addresses — makes every link whose coverage includes those I-addresses *discoverable* from `d_new` (LP16, ASN-0098). `discoverable_from` is an *existential* over slots, so a single transcluded slot suffices to make a link reachable, whereas `sat` — and hence the count — is *conjunctive* across all three slots. A link made discoverable through one transcluded slot is therefore counted against `d_new` only when its other two slots are also met by the corresponding query parts. The discovery count of a query against `d_new` thus rises by exactly those shared links that satisfy all three slots.

The maximally-wide discovery analogue takes `W₂` and `W₃` to be the maximal query V-regions over `d_new`'s own positions — every V-position in `dom(Σ.M(d_new))`, drawn from `d_new`'s content and link subspaces alike — so that `Q₂(Σ) = Q₃(Σ) = ran(Σ.M(d_new))`, the full set of I-addresses `d_new` currently arranges. A shared link discoverable through the from-slot is then counted exactly when its to- and type-coverage also meet those two resolved sets — which holds precisely for the from-discoverable shared links whose other endpoints `d_new` likewise references; the count rises by exactly that subset, and equals all from-discoverable shared links only when every one of them has its to/type endpoints arranged in `d_new` too. The existence count is unchanged regardless: those links already resided in the store and already satisfied a permanent-address request; transclusion shares I-addresses rather than minting them.

---

## R1 — MinimalDecrementNoStoreRetraction (LEMMA, lemma)

No transition removes a link from `dom(Σ.L)`, so `num` registers no "retraction" or "nullification" as such — the existence count never falls, and the discovery count falls only through arrangement contraction of consulted content. Consider the *minimal contraction*: a `K.μ⁻` step removing a single consulted entry, under three preconditions:

- **(P-last)** *Last position.* The removed V-position is the last consulted one mapping to its resolved I-address `a`, so `a` leaves `Qᵢ(Σ')`.
- **(P-slot)** *Single-slot consultation.* The removed V-position lies in exactly one query region — `(E! i : 1 ≤ i ≤ 3 : v ∈ Wᵢ)` — so `a` is consulted in only slot `i`.
- **(P-sole)** *Sole matching link.* `a` is reached, in the relevant slot `i`, by exactly one matching link `ℓ`.

Under (P-last), (P-slot), and (P-sole), the change splits on a single further condition:

- `coverage(Σ.L(ℓ).eᵢ) ∩ Qᵢ(Σ) = {a}` (the sole matching link's slot-`i` reach is exactly `{a}` — no alternate reach into the region) ⟹ `Δnum_disc = −1`;
- otherwise `ℓ` still meets `Qᵢ(Σ')` at some surviving `a' ≠ a` (precisely the R3 situation) ⟹ `Δnum_disc = 0`.

So the minimal contraction gives `Δnum_disc ∈ {−1, 0}` — the `k = 1` specialisation of R2's `Δ ∈ {−k, …, 0}`, with `−1` attained exactly when the sole matching link's slot-`i` reach is `{a}`.

---

## R2 — ContentDeletionUnbounded (LEMMA, lemma)

Let `k` be the number of matching links that reach a deleted endpoint in the consulted slot. Contracting an arrangement so as to remove that endpoint can drop up to `k` links from the discovery count in one operation: `Δnum ∈ {−k, …, 0}`. The per-operation bound is *not* one; it scales with `k`, the sharing multiplicity of the deleted endpoint. The drop attains its full magnitude `−k` exactly when *none* of those `k` reaching links has an alternate surviving reach into the resolved request; a reaching link that still meets the request at a surviving address (the R3 situation) does not drop, so the actual decrement is the number of the `k` reaching links whose only consulted reach ran through the deleted entry.

---

## R3 — PartialSurvival (LEMMA, lemma)

A link with a partially-deleted endpoint remains counted while at least one address of the relevant endset's coverage still lies in the resolved request part: `coverage(Σ.L(a).eᵢ) ∩ Qᵢ(Σ) ≠ ∅` persists if any covered address survives in the region. The link drops from the count only when *all* of its slot-`i` coverage has left every consulted arrangement — the empty-intersection boundary.

---

## R4 — SupersessionStability (LEMMA, lemma)

Publishing a newer version does not decrement the count of links to the superseded content. The old version's I-addresses persist (content is immutable and append-only, S0/P0), coverage is permanent (E1), and an arrangement that re-references those addresses keeps them reachable. Supersession adds arrangement; it removes no link from the count. A link drops only if all of its endpoint addresses leave every consulted arrangement, which supersession by itself does not cause.

---

## R5 — ConservationConditional (LEMMA, lemma)

For the existence count against a fixed permanent request, `num(Q, Σ₂) − num(Q, Σ₁) = (matching links created on the path)` holds exactly between any two states `Σ₁ →* Σ₂`. There is *no subtractive term*: the store never loses an address (L12) and no nullification is visible to `num`, so the identity is exactly E4. For the discovery count the identity fails: by D1, arrangement edits move membership into or out of the resolved request without any link being created, so the net change need not equal the number of matching creations.

---

## R6 — CountedLinkPreservationWP (LEMMA, lemma)

**Context:** Fix a querying document `d_q`, a query triple `W = (W₁, W₂, W₃)`, and a `K.μ⁻` contraction on `d_q` with retention set `R ⊆ dom(Σ.M(d_q))`, so the post-state `Σ' = K.μ⁻[d_q, R](Σ)` satisfies `Σ'.M(d_q) = Σ.M(d_q) ↾ R` and hence resolves to `Qᵢ(Σ') = {Σ.M(d_q)(v) : v ∈ Wᵢ ∩ R}`. Let `ℓ ∈ dom(Σ.L)` be a link counted at `Σ` — `sat(ℓ, Q(Σ), Σ)`.

The weakest precondition on `Σ` under which `ℓ` remains counted in `Σ' = K.μ⁻[d_q, R](Σ)` is:

```
wp(K.μ⁻[d_q, R], sat(ℓ, Q(·), ·))
  ≡  enabled(K.μ⁻[d_q, R]) ∧ (A i : 1 ≤ i ≤ 3 : coverage(Σ.L(ℓ).eᵢ) ∩ {Σ.M(d_q)(v) : v ∈ Wᵢ ∩ R} ≠ ∅)
```

where `enabled(K.μ⁻[d_q, R])` is the operation's applicability predicate (ASN-0047).

*Monotone specialisation.* Since `R ⊆ dom(Σ.M(d_q))`, the pulled-back part `{Σ.M(d_q)(v) : v ∈ Wᵢ ∩ R}` is a subset of `Qᵢ(Σ)`; the wp is therefore *stronger* than the pre-state count condition `sat(ℓ, Q(Σ), Σ)` — exactly the asymmetry that makes contraction able to drop a counted link but never add one (D2).

*Specialisation to R1.* Under (P-last)/(P-slot)/(P-sole) the sole link `ℓ` whose slot-`i` reach is `{a}` is precisely the one whose wp fails (its only retained witness `a` is evicted), yielding `Δnum_disc = −1`; when `ℓ` retains an alternate witness `a' ∈ Wᵢ ∩ R`, its wp holds and `Δnum_disc = 0` — recovering R1's split as the two truth-values of R6 at `ℓ`.

---

## W1 — CardinalAbstraction (LEMMA, lemma)

`num(Q, Σ)` is determined by `match(Q, Σ)` only through its cardinality. It identifies no link's address, owner, endsets, type, or order of arrival. Any two states whose matching sets are equinumerous are indistinguishable by the count. Identity and permanence of the individual links live in their tumbler addresses; the count lives one level above them and is silent about both.

---

## W2 — NonReconstructibility (LEMMA, lemma)

Equality of counts does not entail equality of matching sets: the same numeral may denote wholly different sets at two states or under two requests. Between two states, an arrangement withdrawal (which removes a link from the discovery view) paired with a matching creation can hold the discovery count fixed while every member of the matching set changes. The count sizes the answer; it never names it, and it cannot be inverted to the set it summarises.
