# ASN-0107: FINDNUMOFLINKSFROMTOTHREE Operation

*2026-06-04*

## The Question

A caller hands the system three address descriptions — a *from* part, a *to* part, a *type* part — and asks a single question: **how many?** Not *which* links connect across these regions, but how many there are. The answer is one natural number. Our task is to say, with precision, what that number means: what it counts, what it asserts about the link store, what it deliberately withholds from the caller, and what laws govern its rise and fall as content is added and links are withdrawn.

The temptation is to treat the count as obvious — surely it is "the number of links matching the description." But three words in that phrase each conceal a decision. *Number* forces a choice between set and multiset semantics. *Links* forces a choice of counting unit: whole links, or endpoints, or documents touched. *Matching* forces a choice of tense: links that exist now, or links that ever existed; links the request can presently reach, or links whose stored endsets merely overlap the request in the permanent address space. The count is simple to compute and subtle to specify, and the subtlety is exactly where an implementation can go wrong while still returning a plausible integer.

We are looking for the abstract guarantees — the claims any correct implementation must honour, independent of how it walks its indices. We develop the count as the cardinality of a precisely-defined matching set, then ask under which anchoring that set is stable and under which it breathes.

## State and the Counting Request

We work over the link store `Σ.L : T ⇀ Link` of ASN-0043: a partial function from tumbler addresses to link values, where each value `Σ.L(a)` is a sequence of `N ≥ 3` endsets (L3, ASN-0043), and `dom(Σ.L)` is the set of addresses at which links presently reside. The store is finite at every reachable state (L-fin), monotone non-decreasing across transitions (L12a), and its entries are immutable once written (L12). Endsets denote address sets through `coverage(e)` (ASN-0043, ASN-0098), a purely combinatorial projection of the endset's spans that consults no state component.

A **counting request** is a triple of address sets `Q = (Q₁, Q₂, Q₃)` with each `Qᵢ ⊆ T`. The three components are Nelson's *from set*, *to set*, and *type set* (the "three set"). A component may be the whole space `T` (the corresponding slot is unconstrained) or `∅` (the slot is constrained to match nothing). Although Nelson admits `n`-part requests for `n > 3` (LM 4/79), we fix the standard triple here; the development generalises slot-by-slot without change. Every link carries at least these three slots, since `|Σ.L(a)| ≥ 3`.

We must say when a link *satisfies* a request. Nelson's rule is exact (LM 4/58): "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." Reading "one span of each endset satisfies a corresponding part" as *the endset's coverage meets that part*, and "each endset" as a conjunction across the three slots, we define:

> `sat(a, Q, Σ)  ≡  (A i : 1 ≤ i ≤ 3 : coverage(Σ.L(a).eᵢ) ∩ Qᵢ ≠ ∅)`

The structure is conjunctive across slots, disjunctive within: *every* part must be hit, but a part is hit by *any* overlapping span of the corresponding endset ("all or any part of <from set>", LM 4/69). An unconstrained part `Qᵢ = T` is satisfied by any link with a non-empty `i`-th endset; an empty part `Qᵢ = ∅` is satisfied by no link, since `coverage(e) ∩ ∅ = ∅`. We impose no well-formedness constraint requiring any part to be constrained. The fully-unconstrained request `Q = (T, T, T)` is a legitimate — if maximally broad — query: it counts every stored link, since every link carries three non-empty endsets (L3). This matches Nelson's design, where "any" is expressed not by *omitting* a part but by *widening* it to the universal span — a single "1" digit "may be used to designate ... the entire docuverse" (LM 4/38) — and the architecture is built to *serve* such breadth, not reject it ("the quantity of links not satisfying a request does not in principle impede search on others", LM 4/60). No part need be constrained for `num` to be defined.

The **matching set** and the **count** follow:

> `match(Q, Σ)  =  {a ∈ dom(Σ.L) : sat(a, Q, Σ)}`
>
> `num(Q, Σ)    =  |match(Q, Σ)|`

`num` is the operation's whole output. The matching set is a mathematical object internal to its definition — the operation that *returns* those links is a different operation, out of scope here. We use the set only to size it.

**Well-definedness.** `match(Q, Σ) ⊆ dom(Σ.L)`, and `dom(Σ.L)` is finite (L-fin), so `match(Q, Σ)` is finite and `num(Q, Σ) ∈ ℕ` is total — defined for every request and every reachable state, with no partiality and no error condition. The degenerate requests are clean: if any `Qᵢ = ∅` then `sat` fails universally and `num = 0`; if no stored link overlaps the constrained parts then `match = ∅` and again `num = 0`. A zero is a legitimate answer, not a fault (this discharges the well-formedness concerns of the empty-specset and no-match cases).

## What Is Counted

The counting unit is the **distinct link address**, and nothing else. This is forced by the definition: `match` is a subset of `dom(Σ.L)`, and `num` is its cardinality. A link `a` whose from-set spans ten documents, whose to-set is a broken set of discontiguous spans, and whose type-set names a fourth document is still one element of `dom(Σ.L)` — one address — and contributes exactly one to the count.

We record this as our first claim.

> **P0 (CountIsCardinality).** `num(Q, Σ) = |match(Q, Σ)|`, a natural number whose unit is the link address `a ∈ dom(Σ.L)`. Neither endpoints, nor documents touched, nor the index entries by which a link is found, are the unit of the count.

The point that an implementation is most likely to miss is that this is a *set* cardinality, not a *multiset* tally. The contribution of any single link to the count is the indicator of its satisfaction — a value in `{0, 1}`, never larger:

> **P1 (LinkAtomicity).** For each `a ∈ dom(Σ.L)`, the contribution of `a` to `num(Q, Σ)` is `[sat(a, Q, Σ)] ∈ {0, 1}`. The breadth of an endset — the number of spans, endpoints, or documents its coverage touches — enlarges `coverage(Σ.L(a).eᵢ)` and so can only make the intersection test *easier to pass*; it never multiplies the contribution. A link with a multi-span endset that meets the request in several places is counted once.

P1 is the abstract content of the set-versus-multiset decision. Nelson's satisfaction rule collapses an endset of arbitrary breadth into a single boolean per link, and `num` sizes the set of links that pass. The search-scaling guarantee (LM 4/60, "the quantity of links not satisfying a request does not in principle impede search on others") is the dual observation that non-satisfying links contribute `0`; the count is insensitive to them. We note as an implementation observation that a backend which materialises the matching set as a list and *walks the list* must deduplicate before counting: if a single multi-span link can be appended to that list more than once — as happens when an endpoint's several spans each independently match — then the walk overcounts, and the returned integer is a multiset tally in violation of P1. The abstract claim is that the count is of the *set*; faithfulness to it is a deduplication obligation, not an optional optimisation.

Identity, not description, individuates the links being counted. Two links authored separately are two objects at two addresses, even if their from, to, and type endsets are value-identical.

> **P2 (IdentityIndividuation).** For distinct addresses `a ≠ a'` with `Σ.L(a) = Σ.L(a')`, both satisfy `Q` or both fail, and if both satisfy they contribute `2` to the count. Distinct allocation events produce distinct link addresses (GlobalUniqueness, ASN-0034; L11a), and the store imposes no value-injectivity (L11b permits equal-valued links at distinct addresses). The count therefore individuates by address; identical descriptions are never merged.

P2 is the converse face of P1. P1 says one link is never counted twice; P2 says two links are never counted once. Together they pin the count to set cardinality over addresses: the bijection between counted units and link identities is exact. If two authors independently assert the same connection, the docuverse holds two links and the count reports two — to collapse them would erase one author's owned object.

Finally, only links *present* in the store at the queried state are eligible:

> **P3 (StoreResidence).** `match(Q, Σ) ⊆ dom(Σ.L)`. The count ranges over the links the store holds at `Σ`, never over a hypothetical or historical population outside it.

## Two Anchorings, and the Tense of the Count

Everything so far is parametric in the request `Q`. The crux of the operation's meaning is *how the three address sets are obtained*, because that choice fixes whether the count is a stable property of the permanent store or a live reading of the current arrangement. Two anchorings present themselves, and the consultation evidence is emphatic that they differ precisely in monotonicity.

**Existence anchoring.** The request is given directly as fixed address sets `Q` in the permanent address space. A link's eligibility then turns only on `coverage(Σ.L(a).eᵢ) ∩ Qᵢ`, and coverage is invariant across all transitions (LP3★, ASN-0098): once a link is written, what its endsets denote never changes. Hence `sat(a, Q, ·)` for a fixed `Q` is a function of `a ∈ dom(Σ.L)` alone — independent of the content store `Σ.C` and the arrangements `Σ.M`.

> **E1 (CoveragePermanence).** For fixed `Q` and any `Σ →* Σ'`, every `a ∈ dom(Σ.L)` satisfies `sat(a, Q, Σ') ⟺ sat(a, Q, Σ)`. Satisfaction against permanent address sets is decided by the link's stored value, which is itself permanent (L12).

> **E2 (ExistenceMonotonicity).** For fixed `Q`, `Σ →* Σ' ⟹ num(Q, Σ) ≤ num(Q, Σ')`. The store grows (L12a), coverage is invariant (E1), so `match(Q, Σ) ⊆ match(Q, Σ')`: the matching set only gains members. The existence count never falls.

> **E3 (ContentInvariance).** For fixed `Q`, the transitions that allocate content (K.α), extend, contract, or reorder an arrangement (K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~), register a document (K.σ/K.δ), or record provenance (K.ρ) all leave `num(Q, Σ)` unchanged. By E1, `sat` depends on neither `Σ.C` nor `Σ.M`; only a link-creation transition (K.λ) touches `dom(Σ.L)`.

> **E4 (CreationConservation).** For fixed `Q`, `num(Q, Σ') − num(Q, Σ)` over `Σ →* Σ'` equals the number of links created on that path whose stored value satisfies `Q`. Creation is the sole source of change, and each matching creation adds exactly one (P0, P2); the substrate provides no link-removal transition (L12), so no term subtracts.

**Discovery anchoring.** The request is instead resolved through a querying document's current arrangement. Given a querying document `d_q ∈ dom(Σ.M)` and a triple of query V-regions `W = (W₁, W₂, W₃)`, the address parts are the I-images of those regions under `d_q`'s present arrangement:

> `Qᵢ(Σ)  =  {Σ.M(d_q)(v) : v ∈ Wᵢ ∩ dom(Σ.M(d_q))}`
>
> `num_disc(d_q, W, Σ)  =  num(Q(Σ), Σ)`

This is the count a caller obtains who knows only arranged positions, not permanent addresses. The set `Qᵢ(Σ)` is exactly the I-addresses that `d_q`'s arrangement currently assigns to the queried V-positions — and it tracks the arrangement, not the positions.

> **D1 (PresentTenseResolution).** `Qᵢ(Σ)` is a live reading of `d_q`'s arrangement. Editing `d_q` moves content into or out of the queried V-region without any link being created or retracted, so the resolved request — and hence `num_disc` — can change while `dom(Σ.L)` is fixed.

> **D2 (DiscoveryNonMonotonicity).** `num_disc` is not monotone across `Σ →* Σ'`, because the resolved request `Qᵢ(Σ)` — the *forward image* of the **fixed** V-region `Wᵢ` under `d_q`'s arrangement — moves with the arrangement. We reason about `Qᵢ` directly: it is a forward image of a query region, not the preimage `project(e, d, Σ)` of an endset's coverage that ASN-0098's LP9–LP11 govern, so those lemmas about `project` do not transfer to it.
> - *Extension (K.μ⁺).* The extended arrangement agrees with the prior one on `dom(Σ.M(d_q))` and adds positions. So for every `v ∈ Wᵢ ∩ dom(Σ.M(d_q))` the image `Σ'.M(d_q)(v) = Σ.M(d_q)(v)` survives, and new positions falling in `Wᵢ` may add images. Hence `Qᵢ(Σ) ⊆ Qᵢ(Σ')` — the resolved request can only grow. (The two facts used — strict domain extension and prior-domain agreement — are the structural premises of LP9, applied here to the forward image rather than the preimage.)
> - *Contraction (K.μ⁻).* The contracted arrangement agrees with the prior one on its retained, smaller domain. So `Qᵢ(Σ') ⊆ Qᵢ(Σ)` — the resolved request can only shrink.
> - *Reordering (K.μ~).* The witnessing bijection `π` carries `Σ'.M(d_q)(v) = Σ.M(d_q)(π⁻¹(v))`, so `Qᵢ(Σ') = {Σ.M(d_q)(u) : u ∈ π⁻¹(Wᵢ) ∩ dom(Σ.M(d_q))}`. This need **not** equal `Qᵢ(Σ)`. Although LP11 preserves the *total* range (`ran(Σ'.M(d_q)) = ran(Σ.M(d_q))`), the forward image of a *fixed sub-region* `Wᵢ` is preserved only when `π` fixes `Wᵢ` setwise — `π⁻¹(Wᵢ) ∩ dom = Wᵢ ∩ dom`, as holds when `Wᵢ` is an entire subspace. A reordering that moves content across the `Wᵢ` boundary changes `Qᵢ(Σ)`, so for a positionally-anchored query `num_disc` can rise or fall under K.μ~ with no link created or retracted.
>
> Because the resolved request itself rises and falls, the composite count rises and falls.

The two anchorings reconcile Nelson's design with the implementation evidence. Nelson speaks of the count of links *currently addressable* (deleted links are "not currently addressable", LM 4/9) — a present-tense reading that is the discovery count. The existence count is the same cardinality taken against permanent addresses, where the link store's own monotonicity shows through. An implementation that resolves the query through a document's mapping realises D1–D2; one that queries fixed addresses realises E1–E4. They agree exactly when the queried content has not been edited between readings.

This also fixes the tense of the empty answer.

> **D3 (ZeroIsPresentNotHistorical).** `num(Q, Σ) = 0` asserts that no link in `dom(Σ.L)` satisfies `Q` *at `Σ`*. It does not assert that no such link ever existed, nor that none is discoverable from another document or another arrangement. Absence from the present count is non-existence *in the view*, not non-existence *in the archive*.

A deleted link, in this model, is not removed from `dom(Σ.L)` — the substrate has no such operation (L12) — but ceases to be reachable through the arrangement the request consults, so it falls out of the discovery count while remaining a permanent member of the store. The archive (the store) and the view (the resolved, discoverable population) diverge exactly here.

## How the Count Changes: Content Added

The caller's natural expectation is that adding content somewhere should not silently change the count of links elsewhere. For a request anchored to *unchanged* content, this expectation is met.

> **A1 (FreshContentNeutrality).** Inserting freshly-allocated content — new I-addresses carrying no incoming links — into any arrangement leaves the count unchanged for a request whose parts denote unchanged content. The new addresses are not in the coverage of any existing link's endset (endsets were fixed against earlier addresses), so they introduce no new satisfier; and they are not in the request region, so they perturb no resolved part. For the existence count this is a special case of E3; for the discovery count it holds whenever the inserted content lies outside the resolved region `Qᵢ(Σ)`.

The boundary case is a warning about *positional* requests. If `W` is expressed as raw V-position ranges and an insertion shifts the following positions, then the literally-identical positional query resolves, after the insertion, to *different* I-addresses — a different request in effect, even though it reads the same. Stability is a guarantee about content identity, not about positional notation; a caller who wants a stable count must anchor to content, or re-anchor the positional span after the edit.

Transclusion is the case where content addition genuinely *increases* a count — but on the query side, not in the store.

> **A2 (TransclusionDiscoverability).** Transcluding existing content into a new document `d_new` — installing arrangement entries in `d_new` that map V-positions to the *same* shared I-addresses — makes every link whose coverage includes those I-addresses discoverable from `d_new` (LP16, ASN-0098). The discovery count of a query against `d_new` rises by the links thus shared. The existence count is unchanged: those links already resided in the store and already satisfied a permanent-address request; transclusion shares I-addresses rather than minting them.

A2 is the precise reconciliation of "a link to one version is a link to all versions" (Nelson, LM 2/26) with the fact that copying content adds no entry to the link store. The link population does not grow; what grows is the set of documents from which the unchanged population is reachable. The increase lives in `Σ.M`, not `Σ.L`.

## How the Count Changes: Links Retracted

To withdraw a link from the count, in this model, is to remove it from the *view*, never from the store. The substrate provides no link-removal transition (L12), and udanax-green confirms the design literally: there is no DELETELINK in the FEBE protocol, no nullify or retract operation, and the `typelink` record carries no status field — "once created, a link exists forever." So `num` is *blind* to any notion of link nullification or retraction: no such notion has a count-visible mechanism, because nothing ever leaves `dom(Σ.L)`, and the existence count (E2) therefore cannot fall. Only the discovery count moves under withdrawal, and it moves through one mechanism alone: arrangement contraction that severs a link's endpoints from every consulted document — the abstract analogue of a link becoming "not currently addressable" (LM 4/9). The governing laws distinguish sharply between severing the reach of *one* link and deleting *content* that many links share.

> **R1 (MinimalDecrementNoStoreRetraction).** No transition removes a link from `dom(Σ.L)`, so `num` registers no "retraction" or "nullification" as such — the existence count never falls, and the discovery count falls only through arrangement contraction of consulted content. In the minimal case — contracting away a single consulted entry whose resolved I-address is reached, in the relevant slot, by exactly one matching link — the discovery count drops by exactly one: `Δnum_disc = −1`. A link is a single unit at a single address; its endset breadth does not multiply its identity (P1); and severing it does not cascade — a distinct link whose endset merely *references* `a` by coverage (a link-to-link reference, ASN-0043 L4(c)) is a separate object, untouched. The decrement of one is the *floor* on a contraction's effect, the `k = 1` case of R2 below — not the action of a per-link delete operation, which does not exist.

R1 is the minimal case; the general case is where the decrement *exceeds* one, because the contracted endpoint may be shared by many links.

> **R2 (ContentDeletionUnbounded).** Contracting an arrangement so as to remove an endpoint that `k` distinct links reach can drop up to `k` links from the discovery count in one operation: `Δnum ∈ {−k, …, 0}`. The per-operation bound is *not* one; it is the number of links whose only consulted reach ran through the deleted entry. R1's `Δnum_disc = −1` is the `k = 1` instance: the same contraction mechanism, specialised to an endpoint reached by a single matching link. There is no separate per-link retraction operation that subtracts exactly one independently of sharing — the decrement is always governed by how many links reached the deleted content.

A link survives partial damage to its endpoints, and is counted as long as *any* of its reach remains.

> **R3 (PartialSurvival).** A link with a partially-deleted endpoint remains counted while at least one address of the relevant endset's coverage still lies in the resolved request part: `coverage(Σ.L(a).eᵢ) ∩ Qᵢ(Σ) ≠ ∅` persists if any covered address survives in the region. The link drops from the count only when *all* of its slot-`i` coverage has left every consulted arrangement — the empty-intersection boundary. Survivability is a guarantee that endset breadth is a reserve: a link clings to whatever bytes remain.

Supersession — replacing a document with a newer version — must not be mistaken for deletion.

> **R4 (SupersessionStability).** Publishing a newer version does not decrement the count of links to the superseded content. The old version's I-addresses persist (content is immutable and append-only, S0/P0), coverage is permanent (E1), and an arrangement that re-references those addresses keeps them reachable. Supersession adds arrangement; it removes no link from the count. A link drops only if all of its endpoint addresses leave every consulted arrangement, which supersession by itself does not cause.

These per-operation laws assemble into a conservation statement — but a conditional one, and the condition is exactly the anchoring.

> **R5 (ConservationConditional).** For the existence count against a fixed permanent request, `num(Q, Σ₂) − num(Q, Σ₁) = (matching links created on the path)` holds exactly between any two states `Σ₁ →* Σ₂`. There is *no subtractive term*: the store never loses an address (L12) and no nullification is visible to `num`, so the identity is exactly E4. For the discovery count the identity fails: by D1, arrangement edits move membership into or out of the resolved request without any link being created, so the net change need not equal the number of matching creations. The conservation law is faithful when the count is over currently-resident links against permanent addresses; it breaks the moment the request is pinned to a mutable arrangement.

## A Worked Instance

To exercise the load-bearing claims against something concrete, fix a single document `d = 1.0.1.0.1` (a document-level tumbler, `zeros = 2`). Under it sit content addresses in the text subspace (`s_C = 1`) and link addresses in the link subspace (`s_L = 2`):

- content: `a₁ = 1.0.1.0.1.0.1.1` and `a₂ = 1.0.1.0.1.0.1.2`, both in `dom(Σ.C)`;
- links: `ℓ₁ = 1.0.1.0.1.0.2.1`, `ℓ₂ = …0.2.2`, `ℓ₃ = …0.2.3`, all in `dom(Σ.L)`;
- a type address `τ` (any tumbler the type endsets name).

Each endset below is a set of unit-depth spans; by PrefixSpanCoverage (ASN-0098) the coverage of a unit span at `a` contains `a`, which is all the intersection tests need. The three link values:

| link | from `e₁` | to `e₂` | type `e₃` |
|------|-----------|---------|-----------|
| `ℓ₁` | `{a₁}` | `{a₂}` | `{τ}` |
| `ℓ₂` | `{a₁}` | `{a₂}` | `{τ}` |
| `ℓ₃` | `{a₁, a₂}` (two spans) | `{a₂}` | `{τ}` |

`ℓ₁` and `ℓ₂` are value-identical at distinct addresses (permitted by L11b); `ℓ₃`'s from-endset carries two spans.

**The request and the count.** Take the permanent request `Q = (Q₁, Q₂, Q₃)` with `Q₁ = {a₁, a₂}`, `Q₂ = {a₂}`, `Q₃ = {τ}`. Evaluate `sat`:

- `ℓ₁`: `{a₁} ∩ Q₁ = {a₁} ≠ ∅`, `{a₂} ∩ Q₂ = {a₂} ≠ ∅`, `{τ} ∩ Q₃ ≠ ∅` — matches.
- `ℓ₂`: identical to `ℓ₁` — matches.
- `ℓ₃`: `{a₁, a₂} ∩ Q₁ = {a₁, a₂} ≠ ∅` (the from-endset meets `Q₁` in *two* places), `{a₂} ∩ Q₂ ≠ ∅`, `{τ} ∩ Q₃ ≠ ∅` — matches.

So `match(Q, Σ) = {ℓ₁, ℓ₂, ℓ₃}` and `num(Q, Σ) = 3`.

**P1 (set, not multiset).** `ℓ₃`'s from-endset passes `Q₁` through both of its spans, yet `ℓ₃` contributes `[sat] = 1`, not `2`. A backend that materialised the match list by appending `ℓ₃` once per matching span would report `4` and violate P1; the abstract count is of the *set* `{ℓ₁, ℓ₂, ℓ₃}`.

**P2 (identity, not description).** `ℓ₁` and `ℓ₂` are value-identical but reside at distinct addresses, so they contribute `2`, not `1`. Collapsing them would erase one author's owned object.

**E4 / E2 (creation conservation).** Apply two `K.λ` steps: create `ℓ₄ = …0.2.4` with value `({a₁}, {a₂}, {τ})` (matching), then `ℓ₅ = …0.2.5` with from-endset `{b}` for some `b ∉ Q₁` (non-matching). After `ℓ₄`: `num = 4`. After `ℓ₅`: `num = 4` (the non-matcher adds nothing). Across the two-step path the existence count rose by `1` — exactly the number of *matching* creations (E4) — and never fell (E2). No term subtracts: there is no link-removal step.

**Discovery change under contraction and extension.** Returning to the original three-link store, read `Q` through `d`'s own arrangement. Let `M(d)` map content V-positions `v₁ ↦ a₁`, `v₂ ↦ a₂` and a type position `v_τ ↦ τ`, with query regions `W₁ = {v₁, v₂}`, `W₂ = {v₂}`, `W₃ = {v_τ}`. These resolve to exactly the `Q` above, so `num_disc(d, W, Σ) = 3`.

Contract `M(d)` by `K.μ⁻`, removing `v₁ ↦ a₁`. The resolved from-part becomes `Q₁' = {a₂}`. Re-evaluate: `ℓ₁` and `ℓ₂` now fail (`{a₁} ∩ {a₂} = ∅`), while `ℓ₃` survives (`{a₁, a₂} ∩ {a₂} = {a₂} ≠ ∅`). So `num_disc` drops `3 → 1`. No link was created and none left `dom(Σ.L)`: the two-unit drop is R2 with `k = 2` — the I-address `a₁` was reached in the from-slot by exactly `ℓ₁` and `ℓ₂` (each only through `a₁`), while `ℓ₃` clung to the surviving `a₂` (R3). Now re-extend by `K.μ⁺`, reinstating `v₁ ↦ a₁`: `Q₁` returns to `{a₁, a₂}` and `num_disc` rises `1 → 3` (D2, extension). Throughout, the existence count stayed at `3` (E3): arrangement edits never touch `dom(Σ.L)`.

**Reordering is not count-preserving for a positional sub-region.** Sharpen the query to `W₁ = {v₁}` alone, so `Q₁(Σ) = {a₁}`; all of `ℓ₁, ℓ₂, ℓ₃` (whose from-coverage meets `{a₁}`) match on slot 1. Reorder `M(d)` by `K.μ~`, swapping the images of `v₁` and `v₂` (`π` exchanges the two positions). Now `M'(d)(v₁) = a₂`, so `Q₁(Σ') = {a₂}`: the links whose from-coverage is exactly `{a₁}` — `ℓ₁` and `ℓ₂` — drop on slot 1, with no link created or retracted and the total range `ran(M(d)) = {a₁, a₂, τ}` unchanged. This is the corrected D2: `K.μ~` preserves `num_disc` only when `π` fixes the query region setwise — here `W₁ = {v₁}` is not fixed, so the count moves.

## What the Count Does Not Say

A count is an abstraction in the strict sense: a number standing in for a set, stripped of everything that distinguishes the set's members. The caller who reads `num(Q, Σ) = 47` learns the size of the answer and nothing of its content.

> **W1 (CardinalAbstraction).** `num(Q, Σ)` is determined by `match(Q, Σ)` only through its cardinality. It identifies no link's address, owner, endsets, type, or order of arrival. Any two states whose matching sets are equinumerous are indistinguishable by the count. Identity and permanence of the individual links live in their tumbler addresses; the count lives one level above them and is silent about both. Recovering *which* links matched requires a different operation — one that returns the links — and that operation is out of scope here precisely because it answers a different question.

The corollary is that equal counts carry no promise of equal answers, and a steady count carries no promise of a steady population.

> **W2 (NonReconstructibility).** Equality of counts does not entail equality of matching sets: the same numeral may denote wholly different sets at two states or under two requests. Between two states, an arrangement withdrawal (which removes a link from the discovery view) paired with a matching creation can hold the discovery count fixed while every member of the matching set changes. The count sizes the answer; it never names it, and it cannot be inverted to the set it summarises.

W1 and W2 are the disciplined statement of why the count is *useful* despite being lossy: it lets a caller size a result — gauge the cost of the richer query, decide whether to ask for the links at all — before paying to enumerate them. The loss of identity is the price and the point. A count that revealed identity would not be a count.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| `sat` | `sat(a, Q, Σ) ≡ (A i : 1 ≤ i ≤ 3 : coverage(Σ.L(a).eᵢ) ∩ Qᵢ ≠ ∅)` — conjunctive across slots, disjunctive within | introduced |
| `match` | `match(Q, Σ) = {a ∈ dom(Σ.L) : sat(a, Q, Σ)}` — the matching set | introduced |
| `num` | `num(Q, Σ) = |match(Q, Σ)|` — the count; total and finite (L-fin) | introduced |
| P0 | The counted unit is the distinct link address; `num` is set cardinality | introduced |
| P1 | A link contributes `[sat(a,Q,Σ)] ∈ {0,1}`; endset breadth never multiplies the count (set, not multiset) | introduced |
| P2 | Distinct addresses with equal values count separately; the count individuates by identity, not description | introduced |
| P3 | `match(Q, Σ) ⊆ dom(Σ.L)` — only resident links are eligible | introduced |
| E1 | Against fixed permanent `Q`, satisfaction is invariant across transitions (coverage is permanent) | introduced |
| E2 | The existence count is monotone non-decreasing across `Σ →* Σ'` | introduced |
| E3 | The existence count is invariant under all non-link-creating transitions | introduced |
| E4 | Existence-count change equals the number of matching link creations on the path | introduced |
| D1 | A request resolved through an arrangement is present-tense; edits move the count with no link created or retracted | introduced |
| D2 | The discovery count is non-monotone: extension raises `Qᵢ`, contraction lowers it, reordering preserves it only when `π` fixes the query region `Wᵢ` setwise | introduced |
| D3 | `num = 0` asserts absence in the present view, not in the historical archive | introduced |
| A1 | Fresh content addition is count-neutral for a request anchored to unchanged content | introduced |
| A2 | Transclusion raises the discovery count (query-side reachability), not the existence count (store) | introduced |
| R1 | No store-level link retraction exists, so `num` is blind to nullification; contracting away an entry reached by exactly one matching link drops the discovery count by one (the `k=1` floor of R2); no cascade | introduced |
| R2 | Deleting an endpoint shared by `k` links can drop up to `k` from the discovery count in one operation | introduced |
| R3 | A link survives partial endpoint loss while any covered address remains in the resolved request | introduced |
| R4 | Supersession does not decrement the count of links to the superseded content | introduced |
| R5 | The existence-count change equals matching creations with no subtractive term (= E4); the conservation identity fails for the discovery count | introduced |
| W1 | The count reveals only cardinality — no address, owner, endset, type, or arrival order | introduced |
| W2 | Equal counts need not denote equal matching sets; the count cannot be inverted | introduced |

## Open Questions

What invariants must the count guarantee when the three request parts are independently anchored to different documents' arrangements that evolve separately?

Under what conditions must the discovery count coincide with the existence count — that is, when is every resident matching link also currently discoverable?

What guarantee, if any, must hold between the count at a state and the cardinality of the set the corresponding retrieval operation would return at the same state, and under what staleness may the two diverge?

Must a conformant implementation guarantee set-semantics by deduplicating multi-span matches before sizing, or may idempotence of counting be left as a discipline on the query layer?

What must the count guarantee about its own stability under a request that is logically equivalent but syntactically re-expressed — for instance, a request whose parts are re-decomposed into different spans of the same coverage?
