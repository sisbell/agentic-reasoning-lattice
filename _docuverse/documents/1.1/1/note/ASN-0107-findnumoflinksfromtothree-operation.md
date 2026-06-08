# ASN-0107: FINDNUMOFLINKSFROMTOTHREE Operation

*2026-06-04*

## The Question

A caller hands the system three address descriptions — a *from* part, a *to* part, a *type* part — and asks a single question: **how many?** Not *which* links connect across these regions, but how many there are. The answer is one natural number. Our task is to say, with precision, what that number means: what it counts, what it asserts about the link store, what it deliberately withholds from the caller, and what laws govern its rise and fall as content is added and links are withdrawn.

The temptation is to treat the count as obvious — surely it is "the number of links matching the description." But three words in that phrase each conceal a decision. *Number* forces a choice between set and multiset semantics. *Links* forces a choice of counting unit: whole links, or endpoints, or documents touched. *Matching* forces a choice of tense: links that exist now, or links that ever existed; links the request can presently reach, or links whose stored endsets merely overlap the request in the permanent address space. The count is simple to compute and subtle to specify, and the subtlety is exactly where an implementation can go wrong while still returning a plausible integer.

We are looking for the abstract guarantees — the claims any correct implementation must honour, independent of how it walks its indices. We develop the count as the cardinality of a precisely-defined matching set, then ask under which anchoring that set is stable and under which it breathes.

## State and the Counting Request

We work over the link store `Σ.L : T ⇀ Link` of ASN-0043: a partial function from tumbler addresses to link values, where each value `Σ.L(a)` is a sequence of `N ≥ 3` endsets (L3, ASN-0043), and `dom(Σ.L)` is the set of addresses at which links presently reside. The store is finite at every reachable state (L-fin), monotone non-decreasing across transitions (L12a), and its entries are immutable once written (L12). Endsets denote address sets through `coverage(e)` (ASN-0043, ASN-0098), a purely combinatorial projection of the endset's spans that consults no state component.

A **counting request** is a triple of address sets `Q = (Q₁, Q₂, Q₃)` with each `Qᵢ ⊆ T`. The three components are Nelson's *from set*, *to set*, and *type set* (the "three set"). A component may be the whole space `T` (the corresponding slot is unconstrained) or `∅` (the slot is constrained to match nothing). Although Nelson admits `n`-part requests for `n > 3` (LM 4/79), we fix the standard triple here; the development generalises slot-by-slot without change.

A second decision concerns the *link* side rather than the request side. The substrate (L3, ASN-0043; ASN-0093) admits link values of any arity `N ≥ 3`, so a three-part request meets only the first three endsets of a longer link, leaving slots `4, …, N` unconsulted. We must say whether such a link is eligible to be counted at all. We restrict the operation to **standard-triple links** — those with exactly three endsets:

> **EL (StandardTripleEligibility).** Only links of arity `|Σ.L(a)| = 3` are eligible for FROMTOTHREE counting; a link of arity `N > 3` is never counted, regardless of how its first three endsets meet the request.

This is the design intent, not a convenience. Nelson's link *is* the three endsets — from-set, to-set, type-set — and richer relations are built not by enlarging a link but by linking links ("complex relational structures … may be constructed with links to links … much like the CONS cell in LISP", LM 4/51). His satisfaction rule — "one span of each endset satisfies a corresponding part" (LM 4/58) — is written for that three-endset object, with no notion of "first three of `N`"; three-part search and three-endset links were meant to be coextensive. udanax-green realises this literally: a link is physically capped at three endset subspaces (`LINKFROMSPAN`, `LINKTOSPAN`, `LINKTHREESPAN`), and no fourth is representable, so arity `> 3` cannot arise. We therefore decline to assign FROMTOTHREE meaning to surplus slots a correct link never has, and adopt ASN-0086's choice — its typed relations likewise restrict to `|Σ.L(a)| = 3`.

We must say when a link *satisfies* a request. Nelson's rule is exact (LM 4/58): "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." Reading "one span of each endset satisfies a corresponding part" as *the endset's coverage meets that part*, and "each endset" as a conjunction across the three slots, we define:

> `sat(a, Q, Σ)  ≡  (A i : 1 ≤ i ≤ 3 : coverage(Σ.L(a).eᵢ) ∩ Qᵢ ≠ ∅)`

The structure is conjunctive across slots, disjunctive within: *every* part must be hit, but a part is hit by *any* overlapping span of the corresponding endset ("all or any part of <from set>", LM 4/69). Each part may independently be `T` or `∅`: an unconstrained part `Qᵢ = T` is satisfied by any link with a non-empty `i`-th endset; an empty part `Qᵢ = ∅` is satisfied by no link, since `coverage(e) ∩ ∅ = ∅`. The fully-unconstrained request `Q = (T, T, T)` counts every eligible (standard-triple, EL) stored link whose from- and to-endsets are non-empty — L3 guarantees only that the *type* endset is non-empty (`e₃ ≠ ∅`), and `Endset = 𝒫_fin(Span)` admits `∅`, so a link with an empty from- or to-endset fails `sat` on that slot. This matches Nelson's design, where "any" is expressed not by *omitting* a part but by *widening* it to the universal span (a single "1" digit "may be used to designate ... the entire docuverse", LM 4/38).

The **matching set** and the **count** follow:

> `match(Q, Σ)  =  {a ∈ dom(Σ.L) : |Σ.L(a)| = 3 ∧ sat(a, Q, Σ)}`
>
> `num(Q, Σ)    =  |match(Q, Σ)|`

The arity conjunct `|Σ.L(a)| = 3` is the EL eligibility restriction; `sat` then evaluates the three slots every eligible link carries.

`num` is the operation's whole output. The matching set is a mathematical object internal to its definition — we use it only to size it; returning the matched links is the separate FINDLINKS retrieval operation, out of scope here.

**Well-definedness.** `match(Q, Σ) ⊆ dom(Σ.L)`, and `dom(Σ.L)` is finite (L-fin), so `match(Q, Σ)` is finite and `num(Q, Σ) ∈ ℕ` is total — defined for every request and every reachable state, with no partiality and no error condition. The degenerate requests are clean: if any `Qᵢ = ∅` then `sat` fails universally and `num = 0`; if no stored link overlaps the constrained parts then `match = ∅` and again `num = 0`. A zero is a legitimate answer, not a fault.

`sat` consults each request part only set-wise, which fixes how the count responds to the way a request is presented.

> **Q0 (RequestRepresentationInvariance).** If `Q` and `Q'` have `Qᵢ = Q'ᵢ` as address sets for every `i` — in particular if their parts are presented as spans and re-decomposed into different spans of the same coverage (equal by the `coverage` definition, ASN-0043; PrefixSpanCoverage, ASN-0043) — then `match(Q, Σ) = match(Q', Σ)` and `num(Q, Σ) = num(Q', Σ)`. Equal-coverage requests yield equal counts; this is immediate from `sat`, which consults `Qᵢ` only set-wise.

## What Is Counted

The counting unit is the **distinct link address**, and nothing else. This is forced by the definition: `match` is a subset of `dom(Σ.L)`, and `num` is its cardinality. A link `a` whose from-set spans ten documents, whose to-set is a broken set of discontiguous spans, and whose type-set names a fourth document is still one element of `dom(Σ.L)` — one address — and contributes exactly one to the count.

We record this as our first claim.

> **P0 (CountIsCardinality).** `num(Q, Σ) = |match(Q, Σ)|`, a natural number whose unit is the link address `a ∈ dom(Σ.L)`. Neither endpoints, nor documents touched, nor the index entries by which a link is found, are the unit of the count.

The contribution of any single link to the count is the indicator of its satisfaction — a value in `{0, 1}`, never larger:

> **P1 (LinkAtomicity).** For each `a ∈ dom(Σ.L)`, the contribution of `a` to `num(Q, Σ)` is `[sat(a, Q, Σ)] ∈ {0, 1}`. The breadth of an endset — the number of spans, endpoints, or documents its coverage touches — enlarges `coverage(Σ.L(a).eᵢ)` and so can only make the intersection test *easier to pass*; it never multiplies the contribution. A link with a multi-span endset that meets the request in several places is counted once.

Identity, not description, individuates the links being counted. Two links authored separately are two objects at two addresses, even if their from, to, and type endsets are value-identical.

> **P2 (IdentityIndividuation).** For distinct addresses `a ≠ a'` with `Σ.L(a) = Σ.L(a')`, both satisfy `Q` or both fail, and if both satisfy they contribute `2` to the count. Distinct allocation events produce distinct link addresses (GlobalUniqueness, ASN-0034; L11a), and the store imposes no value-injectivity (L11b permits equal-valued links at distinct addresses). The count therefore individuates by address; identical descriptions are never merged.

P2 is the converse face of P1: one link is never counted twice, and two links are never counted once. If two authors independently assert the same connection, the docuverse holds two links and the count reports two — to collapse them would erase one author's owned object.

Finally, only links *present* in the store at the queried state are eligible:

> **P3 (StoreResidence).** `match(Q, Σ) ⊆ dom(Σ.L)`. The count ranges over the links the store holds at `Σ`, never over a hypothetical or historical population outside it.

## Two Anchorings, and the Tense of the Count

Everything so far is parametric in the request `Q`. The crux of the operation's meaning is *how the three address sets are obtained*, because that choice fixes whether the count is a stable property of the permanent store or a live reading of the current arrangement. Two anchorings present themselves.

**Existence anchoring.** The request is given directly as fixed address sets `Q` in the permanent address space. A link's eligibility then turns only on `coverage(Σ.L(a).eᵢ) ∩ Qᵢ`, and coverage is invariant across all transitions (LP3★, ASN-0098): once a link is written, what its endsets denote never changes. Hence `sat(a, Q, ·)` for a fixed `Q` is a function of `a ∈ dom(Σ.L)` alone — independent of the content store `Σ.C` and the arrangements `Σ.M`.

> **E1 (CoveragePermanence).** For fixed `Q` and any `Σ →* Σ'`, every `a ∈ dom(Σ.L)` satisfies `sat(a, Q, Σ') ⟺ sat(a, Q, Σ)`. Satisfaction against permanent address sets is decided by the link's stored value, which is itself permanent (L12).

> **E2 (ExistenceMonotonicity).** For fixed `Q`, `Σ →* Σ' ⟹ num(Q, Σ) ≤ num(Q, Σ')`. The store grows across the transitive closure (Store Monotonicity★, ASN-0098), coverage is invariant (E1), so `match(Q, Σ) ⊆ match(Q, Σ')`: the matching set only gains members. The existence count never falls.

> **E3 (ContentInvariance).** For fixed `Q`, the transitions that allocate content (K.α), extend, contract, or reorder an arrangement (K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~), register a document (K.σ/K.δ), or record provenance (K.ρ) all leave `num(Q, Σ)` unchanged. By E1, `sat` depends on neither `Σ.C` nor `Σ.M`; only a link-creation transition (K.λ) touches `dom(Σ.L)`.

> **E4 (CreationConservation).** For fixed `Q`, `num(Q, Σ') − num(Q, Σ)` over `Σ →* Σ'` equals the number of links created on that path whose stored value satisfies `Q`. Creation is the sole source of change, and each matching creation adds exactly one (P0, P2); no term subtracts, since no link is ever removed (R0).

**Discovery anchoring.** The request is instead resolved through a querying document's current arrangement. Given a querying document `d_q ∈ dom(Σ.M)` and a triple of query V-regions `W = (W₁, W₂, W₃)`, the address parts are the I-images of those regions under `d_q`'s present arrangement:

> `Qᵢ(Σ)  =  {Σ.M(d_q)(v) : v ∈ Wᵢ ∩ dom(Σ.M(d_q))}`
>
> `num_disc(d_q, W, Σ)  =  num(Q(Σ), Σ)`

This is the count a caller obtains who knows only arranged positions, not permanent addresses. The set `Qᵢ(Σ)` is exactly the I-addresses that `d_q`'s arrangement currently assigns to the queried V-positions — and it tracks the arrangement, not the positions.

> **D1 (PresentTenseResolution).** `Qᵢ(Σ)` is a live reading of `d_q`'s arrangement. Editing `d_q` moves content into or out of the queried V-region without any link being created or retracted, so the resolved request — and hence `num_disc` — can change while `dom(Σ.L)` is fixed.

> **D2 (DiscoveryNonMonotonicity).** `num_disc` is not monotone across `Σ →* Σ'`, because the resolved request `Qᵢ(Σ)` — the *forward image* of the **fixed** V-region `Wᵢ` under `d_q`'s arrangement — moves with the arrangement.
> - *Extension (K.μ⁺ or K.μ⁺_L).* An extension step strictly extends the prior domain and agrees with it on every prior position — K.μ⁺ adding content-subspace positions, K.μ⁺_L adding link-subspace positions (a query part may resolve to link-subspace addresses, since `Wᵢ` may contain link-subspace V-positions whose images are link addresses; link-to-link references, L4(c); S3★ maps such positions into `dom(Σ.L)`). So for every `v ∈ Wᵢ ∩ dom(Σ.M(d_q))` the image `Σ'.M(d_q)(v) = Σ.M(d_q)(v)` survives, and new positions falling in `Wᵢ` may add images. Hence `Qᵢ(Σ) ⊆ Qᵢ(Σ')` — the resolved request can only grow.
> - *Contraction (K.μ⁻).* The contracted arrangement agrees with the prior one on its retained, smaller domain. So `Qᵢ(Σ') ⊆ Qᵢ(Σ)` — the resolved request can only shrink.
> - *Reordering (K.μ~).* The witnessing bijection `π` carries `Σ'.M(d_q)(v) = Σ.M(d_q)(π⁻¹(v))` (the K.μ~ bijection equation, ASN-0047), so `Qᵢ(Σ') = {Σ.M(d_q)(u) : u ∈ π⁻¹(Wᵢ) ∩ dom(Σ.M(d_q))}`. This need **not** equal `Qᵢ(Σ)`: although LP11 preserves the *total* range (`ran(Σ'.M(d_q)) = ran(Σ.M(d_q))`), the forward image of a *fixed sub-region* `Wᵢ` can move. When a reorder moves a position with an otherwise-unshared image across the `Wᵢ` boundary, `Qᵢ(Σ)` changes, so for a positionally-anchored query `num_disc` can rise or fall under K.μ~ with no link created or retracted.
>
> Because the resolved request itself rises and falls, the composite count rises and falls.

The two counts agree exactly when the queried content has not been edited between readings.

This also fixes the tense of the empty answer.

> **D3 (ZeroIsPresentNotHistorical).** The present-tense disclaimer is a property of the *discovery* count alone. A zero discovery count `num_disc(d_q, W, Σ) = 0` — equivalently `num(Q(Σ), Σ) = 0` against the state-resolved request `Q(Σ)` — asserts that no link in `dom(Σ.L)` is presently discoverable from `d_q`'s arrangement at `Σ`. It does *not* assert that no such link ever existed, nor that none is discoverable from another document or another arrangement: a link whose endpoints have left the consulted arrangement merely ceases to be reachable through it (its resolved reach drops by D2), so it leaves the discovery count while remaining a permanent member of the store (R0, L12). Absence from the discovery count is non-existence *in the view*, not non-existence *in the archive*.
>
> The existence count, by contrast, *does* certify historical absence. Against a fixed permanent request `Q`, `num(Q, Σ) = 0` implies `num(Q, Σ₀) ≤ num(Q, Σ) = 0` along every path `Σ₀ →* Σ` — by E1 satisfaction against fixed `Q` is per-link time-invariant, and by E2 the count is monotone non-decreasing — so no link satisfying `Q` was *ever* created. For the existence anchoring a zero certifies absence in the store across all of history, and the "discoverable from another arrangement" disclaimer is meaningless, since existence satisfaction consults no arrangement at all.

## How the Count Changes: Content Added

The caller's natural expectation is that adding content somewhere should not silently change the count of links elsewhere. For a request anchored to *unchanged* content, this expectation is met.

> **A1a (FreshContentNeutrality, existence).** For a fixed permanent request `Q`, inserting freshly-allocated content leaves the existence count unchanged — *unconditionally*. This is a corollary of E3: K.α changes neither `dom(Σ.L)` nor any `coverage` nor the fixed `Q`, so `match(Q, ·)` is invariant regardless of where — or whether — the new address `a_new` sits in `Q`.
>
> **A1b (FreshContentNeutrality, discovery).** For a discovery query, inserting freshly-allocated content *not referenced by any stored link in any slot* leaves the discovery count unchanged. The neutrality is conditioned on that unreferenced premise: no stored link has `a_new ∈ coverage(Σ.L(a).eᵢ)` for *any* slot `i` (from, to, or type) — not merely no *incoming* link pointing at `a_new` in its to-slot — so even arranging `a_new` into a queried V-region (a K.μ⁺ step that places it in some `Qᵢ(Σ')`) creates no new match.

Stability is a guarantee about content identity, not about positional notation: a content-anchored count is stable across arrangement edits, but a positionally-anchored query must be re-anchored after a reordering (K.μ~), since a reorder can move the image of a fixed V-position across a query-region boundary (D2's reordering clause).

Transclusion is the case where content addition genuinely *increases* a count — but on the query side, not in the store.

> **A2 (TransclusionDiscoverability).** Transcluding existing content into a new document `d_new` — installing arrangement entries in `d_new` that map V-positions to the *same* shared I-addresses — makes every link whose coverage includes those I-addresses *discoverable* from `d_new` (LP16, ASN-0098). Discoverability and counting must not be conflated here: `discoverable_from` is an *existential* over slots, so a single transcluded slot suffices to make a link reachable, whereas `sat` — and hence the count — is *conjunctive* across all three slots. The discovery count of a query against `d_new` thus rises by exactly those shared links that satisfy all three slots — a number bounded above by the from-discoverable shared links and below by `0`, with the gap determined by how many of them fail their to/type slots. To count the broadest such population, take `W₂` and `W₃` to be the maximal query V-regions over `d_new`'s own positions — every V-position in `dom(Σ.M(d_new))` — so that `Q₂(Σ) = Q₃(Σ) = ran(Σ.M(d_new))`, the full set of I-addresses `d_new` currently arranges. A from-discoverable shared link is then counted exactly when its to- and type-coverage also meet those two resolved sets — i.e. when `d_new` likewise references its other endpoints. The existence count is unchanged regardless: those links already resided in the store and already satisfied a permanent-address request; transclusion shares I-addresses rather than minting them.

Copying content adds no entry to the link store. The link population does not grow; what grows is the set of documents from which the unchanged population is reachable. The increase lives in `Σ.M`, not `Σ.L` — realising Nelson's "a link to one version is a link to all versions" (LM 2/26).

## How the Count Changes: Links Retracted

> **R0 (NoStoreRetraction).** The substrate provides no link-removal transition: once a link enters `dom(Σ.L)` it is never removed and its value never changes (L12). udanax-green confirms the design literally — there is no DELETELINK in the FEBE protocol, no nullify or retract operation, and the `typelink` record carries no status field ("once created, a link exists forever"). Consequently `num`'s existence reading is *blind* to any notion of link nullification or retraction and cannot fall (E2); every "withdrawal" removes a link from the *view*, never from the store.

Only the discovery count moves under withdrawal, and it moves through one mechanism alone: arrangement contraction that severs a link's endpoints from every consulted document — the abstract analogue of a link becoming "not currently addressable" (LM 4/9). The governing laws distinguish sharply between severing the reach of *one* link and deleting *content* that many links share.

Every such contraction runs through one structural constraint on `K.μ⁻`. By PerSubspaceContractionScope (ASN-0047), a contraction retains a canonical prefix `R = ⋃{[S,1,…,1,k] : 1 ≤ k ≤ n'_S}` per subspace, so it can only drop a *trailing suffix* of consulted positions: removing the endpoint at a non-maximal position `[S, j]` forces `n'_S < j` and hence drops every later endpoint `[S, j], [S, j+1], …, [S, n_S]` as well. Surgical removal of a single interior endpoint is impossible — dropping an interior position while keeping a later one would violate D-MIN★/D-CTG★ — and a contraction touches exactly one endpoint only when that endpoint is the arrangement-maximal consulted position. We call this the **trailing-suffix property** of `K.μ⁻`.

> **R1 (MinimalDecrement).** With no store retraction available (R0), the discovery count moves only through arrangement contraction. Consider the *minimal contraction*: a `K.μ⁻` step removing a single consulted entry `v ↦ a`, under these preconditions:
>
> - **(P-max)** *Arrangement-maximal removal.* By the trailing-suffix property, dropping exactly one entry forces the removed `v` to be the arrangement-maximal position `[S, n_S]` in its subspace.
> - **(P-uniq)** *Unique consulted reach.* `v` is the *only* consulted V-position mapping to its resolved I-address `a` — no other position in `Wᵢ ∩ R` maps to `a` — so removing `v` makes `a` leave `Qᵢ(Σ')`.
> - **(P-slot)** *Single-slot consultation.* The removed V-position lies in exactly one query region — `(E! i : 1 ≤ i ≤ 3 : v ∈ Wᵢ)` — so `a` is consulted in only slot `i`.
> - **(P-sole)** *Sole matching link.* `a` is reached, in the relevant slot `i`, by exactly one matching link `ℓ`.
>
> Under (P-max), (P-uniq), (P-slot), and (P-sole), the change splits on a single further condition:
>
> - `coverage(Σ.L(ℓ).eᵢ) ∩ Qᵢ(Σ) = {a}` (the sole matching link's slot-`i` reach is exactly `{a}` — no alternate reach into the region) ⟹ `Δnum_disc = −1`;
> - otherwise `ℓ` still meets `Qᵢ(Σ')` at some surviving `a' ≠ a` — the reaching link is retained — ⟹ `Δnum_disc = 0`.
>
> So the minimal contraction gives `Δnum_disc ∈ {−1, 0}`, with `−1` attained exactly when the sole matching link's slot-`i` reach is `{a}`. Severing one link does not cascade: a distinct link whose endset merely *references* `a` by coverage (a link-to-link reference, ASN-0043 L4(c)) is a separate object, untouched.

R1 is the minimal case; the general case is where the decrement *exceeds* one, because the contracted endpoint may be shared by many links.

> **R2 (ContentDeletionUnbounded).** Consider a `K.μ⁻` step under a *single-consulted-slot* restriction paralleling R1's (P-slot):
> - **(P-slot₂)** *Single consulted slot.* Every dropped consulted V-position lies in one and the same query region — `(E! i : 1 ≤ i ≤ 3 : every dropped consulted v has v ∈ Wᵢ)` — so the contraction alters only the resolved part `Qᵢ`, leaving the other two parts fixed.
>
> By the trailing-suffix property, the step can only drop a trailing suffix of consulted positions in slot `i`. Let `D` be the set of I-addresses that leave the resolved part `Qᵢ` through the contraction — the dropped-position images in slot `i` that retain *no* surviving consulted preimage, i.e. every consulted position mapping to the address was dropped (R1's (P-uniq) condition, lifted to the whole removed suffix; a dropped position whose image is also the image of a *retained* consulted position does not contribute to `D`, since that address survives in `Qᵢ`) — and let `k` be the number of matching links reaching *some* `a ∈ D` in slot `i`. The contraction can drop up to `k` links from the discovery count in one operation: `Δnum_disc ∈ {−k, …, 0}`. The per-operation bound is *not* one; it scales with `k`, the aggregate sharing multiplicity over the whole removed suffix `D`. The drop attains its full magnitude `−k` exactly when *none* of those `k` reaching links has an alternate surviving reach into `Qᵢ(Σ')`; a reaching link that still meets the request at a surviving address does not drop, so the actual decrement is the number of the `k` reaching links whose only slot-`i` reach ran through some removed endpoint. The decrement is therefore always governed by how many links reached the removed suffix and how many retained an alternate reach — never a fixed unit independent of sharing.

A link survives partial damage to its endpoints, and is counted as long as *any* of its reach remains.

> **R3 (PartialSurvival).** Slot `i`'s contribution to satisfaction — the conjunct `coverage(Σ.L(a).eᵢ) ∩ Qᵢ(Σ) ≠ ∅` — survives partial deletion of the endpoint while at least one address of that endset's coverage still lies in the resolved request part. The conjunct fails only at the empty-intersection boundary `coverage(Σ.L(a).eᵢ) ∩ Qᵢ(Σ) = ∅`, i.e. when slot-`i` coverage no longer meets the single resolved part `Qᵢ(Σ)`. Whether the *link* remains counted is a separate question: since `sat` is conjunctive across the three slots, slot-`i` survival keeps `a` counted only if the other two conjuncts also hold, and `a` can drop through a slot `j ≠ i` even while slot `i` stays fully intact.

Supersession — replacing a document with a newer version — must not be mistaken for deletion.

> **R4 (SupersessionStability).** Publishing a newer version does not decrement the count of links to the superseded content. The old version's I-addresses persist (content is immutable and append-only, S0/P0), coverage is permanent (E1), and an arrangement that re-references those addresses keeps them reachable. Supersession adds arrangement; it removes no link from the count. A link drops only if some slot's coverage leaves the resolved request part — `coverage(Σ.L(a).eᵢ) ∩ Qᵢ(Σ) = ∅` for some `i` — which supersession by itself does not cause.

The R-laws above give *sufficient* conditions for the discovery count to fall. We now sharpen one of them into a *weakest* precondition, so that the boundary between "still counted" and "dropped" is characterised exactly rather than by a one-sided implication. The non-trivial postcondition we anchor to is the survival of a single counted link across an arrangement contraction — the per-link event whose aggregate over `match` *is* `Δnum_disc`.

Fix a querying document `d_q`, a query triple `W = (W₁, W₂, W₃)`, and a `K.μ⁻` contraction on `d_q` with admissible per-subspace retention counts `(n'_{s_C}, n'_{s_L})`, whose retained domain is the canonical prefix set `R := ⋃ {[S, 1, …, 1, k] : S ∈ {s_C, s_L} ∧ 1 ≤ k ≤ n'_S}` (PerSubspaceContractionScope, ASN-0047; this is exactly LP12a's retention set, ASN-0098 — the trailing-suffix property forbids any other retained domain). The post-state `Σ' = K.μ⁻[d_q, R](Σ)` satisfies `Σ'.M(d_q) = Σ.M(d_q) ↾ R` and hence resolves to `Qᵢ(Σ') = {Σ.M(d_q)(v) : v ∈ Wᵢ ∩ R}`. Let `ℓ ∈ dom(Σ.L)` be a link counted at `Σ` — `sat(ℓ, Q(Σ), Σ)`. We seek `wp(K.μ⁻[d_q, R], "ℓ is counted at the post-state")`.

> **R6 (CountedLinkPreservationWP).** The weakest precondition on `Σ` under which `ℓ` remains counted in `Σ' = K.μ⁻[d_q, R](Σ)` is
> ```
> wp(K.μ⁻[d_q, R], sat(ℓ, Q(·), ·))
>   ≡  enabled(K.μ⁻[d_q, R]) ∧ (A i : 1 ≤ i ≤ 3 : coverage(Σ.L(ℓ).eᵢ) ∩ {Σ.M(d_q)(v) : v ∈ Wᵢ ∩ R} ≠ ∅)
> ```
> where `enabled(K.μ⁻[d_q, R])` is the operation's applicability predicate (ASN-0047). *Derivation.* `K.μ⁻[d_q, R]` is deterministic, so the weakest precondition is the postcondition mechanically pulled back through its effect. The post-state condition is `sat(ℓ, Q(Σ'), Σ') ≡ (A i : coverage(Σ'.L(ℓ).eᵢ) ∩ Qᵢ(Σ') ≠ ∅)`. Two substitutions reduce every post-state term to a pre-state term: `ℓ ∈ dom(Σ'.L)` with `Σ'.L(ℓ) = Σ.L(ℓ)` (L12a, L12) gives `coverage(Σ'.L(ℓ).eᵢ) = coverage(Σ.L(ℓ).eᵢ)` (equivalently E1); and `Σ'.M(d_q) = Σ.M(d_q) ↾ R` gives `Qᵢ(Σ') = {Σ.M(d_q)(v) : v ∈ Wᵢ ∩ R}`. The conjunction of `enabled` with the substituted body is the displayed predicate. It is *weakest*, not merely sufficient: because the transition is deterministic and the substituted body is logically equivalent to the post-state condition (no implication is one-sided — each step is an identity of coverage or of the resolved part), any pre-state satisfying it reaches a post-state satisfying the postcondition, and any pre-state violating some slot `i` reaches a post-state where slot `i` fails `sat`, so the postcondition fails. No weaker condition can imply the postcondition. *Monotone specialisation.* Since `R ⊆ dom(Σ.M(d_q))`, the pulled-back part `{Σ.M(d_q)(v) : v ∈ Wᵢ ∩ R}` is a subset of `Qᵢ(Σ)`; the wp is therefore *stronger* than the pre-state count condition `sat(ℓ, Q(Σ), Σ)` — exactly the asymmetry that makes contraction able to drop a counted link but never add one (D2). *Specialisation to R1.* R1's minimal-contraction split is the `k = 1` case of this wp: under (P-max)/(P-uniq)/(P-slot)/(P-sole) the wp's failure at the sole matching link `ℓ` is R1's `Δnum_disc = −1` branch and its holding is R1's `Δnum_disc = 0` branch.

## A Worked Instance

To exercise the load-bearing claims against something concrete, fix a single document `d = 1.0.1.0.1` (a document-level tumbler, `zeros = 2`). Under it sit content addresses in the text subspace (`s_C = 1`) and link addresses in the link subspace (`s_L = 2`):

- content: `a₁ = 1.0.1.0.1.0.1.1` and `a₂ = 1.0.1.0.1.0.1.2`, both in `dom(Σ.C)`;
- links: `ℓ₁ = 1.0.1.0.1.0.2.1`, `ℓ₂ = …0.2.2`, `ℓ₃ = …0.2.3`, all in `dom(Σ.L)`;
- a type address `τ = 1.0.1.0.1.0.1.3` in the text subspace, `τ ∈ dom(Σ.C)` — the content address the three type endsets name (an endset may reference content addresses freely, L4, ASN-0043; here `subspace_I(τ) = E(τ)₁ = s_C` and `origin(τ) = d`).

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

**Discovery change under contraction and extension.** Returning to the original three-link store, read `Q` through `d`'s own arrangement. Every queried position is a *content-subspace* V-position (`s_C = 1`): let `M(d)` map the contiguous run `v_τ = [1,1] ↦ τ`, `v₂ = [1,2] ↦ a₂`, `v₁ = [1,3] ↦ a₁` (D-SEQ), with the type position `v_τ` placed first so the content contraction below retains it. Each image lies in `dom(Σ.C)` — `τ, a₂, a₁` are all content addresses — which discharges S3★ (GeneralizedReferentialIntegrity) for the content subspace. With query regions `W₁ = {v₁, v₂}`, `W₂ = {v₂}`, `W₃ = {v_τ}` these resolve to exactly the `Q` above, so `num_disc(d, W, Σ) = 3`.

Contract `M(d)` by `K.μ⁻`, retaining the content-subspace prefix `{[1,1], [1,2]}` (content retention count `n'_{s_C} = 2`) and so dropping the *trailing* entry `v₁ = [1,3] ↦ a₁`; the type entry `v_τ = [1,1] ↦ τ` sits inside the retained prefix and survives. The resolved from-part becomes `Q₁' = {a₂}`. Re-evaluate: `ℓ₁` and `ℓ₂` now fail (`{a₁} ∩ {a₂} = ∅`), while `ℓ₃` survives (`{a₁, a₂} ∩ {a₂} = {a₂} ≠ ∅`). So `num_disc` drops `3 → 1`. No link was created and none left `dom(Σ.L)`: the two-unit drop is R2 with `k = 3` — the I-address `a₁` was reached in the from-slot by `ℓ₁`, `ℓ₂`, and `ℓ₃`, but only `ℓ₁` and `ℓ₂` reach it *exclusively*, while `ℓ₃` clung to the surviving `a₂` (R3). So of the three reaching links, two had their only consulted reach severed and dropped, giving `Δnum_disc = −2` within R2's `{−3, …, 0}` band. Now re-extend by `K.μ⁺`, reinstating `v₁ = [1,3] ↦ a₁`: `Q₁` returns to `{a₁, a₂}` and `num_disc` rises `1 → 3` (D2, extension). Throughout, the existence count stayed at `3` (E3): arrangement edits never touch `dom(Σ.L)`.

**Reordering is not count-preserving for a positional sub-region.** Sharpen the from-region to `W₁ = {v₁}` while retaining `W₂ = {v₂}` and `W₃ = {v_τ}`. Pre-swap the regions resolve to `Q₁(Σ) = {a₁}`, `Q₂(Σ) = {a₂}`, `Q₃(Σ) = {τ}`, and all of `ℓ₁, ℓ₂, ℓ₃` match (each meets `{a₁}` on from, `{a₂}` on to, `{τ}` on type), so `num_disc = 3`. Reorder `M(d)` by `K.μ~`, swapping the images of `v₁` and `v₂` (`π` transposes the two content positions `v₁` and `v₂` and fixes every other position, so `v_τ` is untouched; it is length-preserving, subspace-preserving, and — with no link-subspace position in play — link-subspace-fixing vacuously). Now `M'(d)(v₁) = a₂` and `M'(d)(v₂) = a₁`, so `Q₁(Σ') = {a₂}`, `Q₂(Σ') = {a₁}`, `Q₃(Σ') = {τ}`. Re-evaluate all three slots: `ℓ₁` and `ℓ₂` fail on slot 1 (`{a₁} ∩ {a₂} = ∅`); `ℓ₃` passes slot 1 (`{a₁, a₂} ∩ {a₂} = {a₂} ≠ ∅`) but now fails slot 2 (`{a₂} ∩ {a₁} = ∅`). All three drop, so `num_disc` moves `3 → 0` — with no link created or retracted and the total range `ran(M(d)) = {a₁, a₂, τ}` unchanged. This exhibits D2's reordering clause: `π` carries the *distinctly-imaged* positions `v₁ ↦ a₁` and `v₂ ↦ a₂` across the `W₁` and `W₂` boundaries, so the image sets disagree (`Q₁` moves `{a₁} → {a₂}`, `Q₂` moves `{a₂} → {a₁}`) and the count moves.

## What the Count Does Not Say

> **W1 (CardinalAbstraction).** `num(Q, Σ)` is determined by `match(Q, Σ)` only through its cardinality. It identifies no link's address, owner, endsets, type, or order of arrival. Any two states whose matching sets are equinumerous are indistinguishable by the count. Identity and permanence of the individual links live in their tumbler addresses; the count lives one level above them and is silent about both.

The corollary is that equal counts carry no promise of equal answers, and a steady count carries no promise of a steady population.

> **W2 (NonReconstructibility).** Equality of counts does not entail equality of matching sets: the same numeral may denote different sets at two states or under two requests. The witness is a single-member swap, which already establishes that equal counts need not denote equal matching sets. Take a discovery query with at least one matching link, and a link `ℓ` in `match` whose sole consulted reach runs through one arrangement-maximal endpoint — R1's `(P-max)/(P-uniq)/(P-slot)/(P-sole)`. A first step, a `K.μ⁻` contraction severing that endpoint, drops `ℓ` from the view: `Δnum_disc = −1` (R1's `−1` branch). A second composite — `K.α` allocating fresh content, `K.μ⁺` arranging it into the queried region, and `K.λ` creating a link whose reach meets that region — adds one new matching link distinct from `ℓ` (it sits at a fresh address, P2): `Δnum_disc = +1` (D2, extension). The discovery count returns to its starting value while the matching set has exchanged `ℓ` for a distinct member, so the two equinumerous states have different matching sets. The count sizes the answer; it never names it, and it cannot be inverted to the set it summarises.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| `sat` | `sat(a, Q, Σ) ≡ (A i : 1 ≤ i ≤ 3 : coverage(Σ.L(a).eᵢ) ∩ Qᵢ ≠ ∅)` — conjunctive across slots, disjunctive within | introduced |
| `match` | `match(Q, Σ) = {a ∈ dom(Σ.L) : |Σ.L(a)| = 3 ∧ sat(a, Q, Σ)}` — the matching set | introduced |
| `num` | `num(Q, Σ) = |match(Q, Σ)|` — the count; total and finite (L-fin) | introduced |
| EL | Only standard-triple links (`|Σ.L(a)| = 3`) are eligible; arity `N > 3` links are never counted | introduced |
| P0 | The counted unit is the distinct link address; `num` is set cardinality | introduced |
| Q0 | Equal-coverage requests yield equal counts; `num` reads request parts only set-wise | introduced |
| P1 | A link contributes `[sat(a,Q,Σ)] ∈ {0,1}`; endset breadth never multiplies the count (set, not multiset) | introduced |
| P2 | Distinct addresses with equal values count separately; the count individuates by identity, not description | introduced |
| P3 | `match(Q, Σ) ⊆ dom(Σ.L)` — only resident links are eligible | introduced |
| E1 | Against fixed permanent `Q`, satisfaction is invariant across transitions (coverage is permanent) | introduced |
| E2 | The existence count is monotone non-decreasing across `Σ →* Σ'` | introduced |
| E3 | The existence count is invariant under all non-link-creating transitions | introduced |
| E4 | Existence-count change equals the number of matching link creations on the path | introduced |
| D1 | A request resolved through an arrangement is present-tense; edits move the count with no link created or retracted | introduced |
| D2 | The discovery count is non-monotone: extension raises `Qᵢ`, contraction lowers it, reordering may move it | introduced |
| D3 | A zero *discovery* count asserts absence in the present view, not the archive; a zero *existence* count, by contrast, certifies historical absence in the store (E1+E2) | introduced |
| A1a | Fresh content addition is *unconditionally* neutral for the existence count (corollary of E3) | introduced |
| A1b | Fresh content unreferenced by any stored link in any slot is neutral for the discovery count (conditioned on the unreferenced premise) | introduced |
| A2 | Transclusion makes shared links discoverable from `d_new`; the discovery count rises only by shared links satisfying all three slots, not the existence count | introduced |
| R0 | The substrate provides no link-removal transition (L12); a link, once stored, is permanent — every withdrawal is from the view, not the store | introduced |
| R1 | Under (P-max)/(P-uniq)/(P-slot)/(P-sole), minimal contraction gives `Δnum_disc ∈ {−1,0}` | introduced |
| R2 | Single-consulted-slot (P-slot₂) canonical-prefix contraction drops a trailing suffix of endpoints; the discovery count can fall by up to `k`, the matching links reaching any removed endpoint in that slot | introduced |
| R3 | Slot `i`'s satisfaction conjunct survives partial endpoint loss while any covered address remains; whole-link counting still requires the other two slots | introduced |
| R4 | Supersession does not decrement the count of links to the superseded content | introduced |
| R6 | Weakest precondition for a counted link `ℓ` to survive `K.μ⁻[d_q, R]`: `enabled ∧ (A i : coverage(Σ.L(ℓ).eᵢ) ∩ {Σ.M(d_q)(v) : v ∈ Wᵢ ∩ R} ≠ ∅)`; specialises to R1's split | introduced |
| W1 | The count reveals only cardinality — no address, owner, endset, type, or arrival order | introduced |
| W2 | Equal counts need not denote equal matching sets; the count cannot be inverted | introduced |

## Open Questions

What invariants must the count guarantee when the three request parts are independently anchored to different documents' arrangements that evolve separately?

Under what conditions must the discovery count coincide with the existence count — that is, when is every resident matching link also currently discoverable?

What guarantee, if any, must hold between the count at a state and the cardinality of the set the corresponding retrieval operation would return at the same state, and under what staleness may the two diverge?
