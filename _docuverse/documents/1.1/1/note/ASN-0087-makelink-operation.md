# ASN-0087: MAKELINK Operation
*2026-05-26*

## The Problem

We are looking for the precise meaning of *creating a link*. The system already maintains a content store, a family of arrangements, and a link store with prior entries. Some event introduces a new link. What does that event do?

A link, in this design, is a stored connective unit — a first-class entity binding together fragments of content. By L3 (ASN-0043) every link has at least three endsets, the third designated as type, the type slot non-empty. Beyond this, link creation must produce four things: an *identity* (the link's address), a *value* (the endsets), a *home* (the document under whose authority the link is allocated), and *discoverability* (the property that a query of the content reached by the link's endsets surfaces the link).

The MAKELINK operation is the event by which all four come into being. We ask: what is allocated, what is recorded, what is rendered discoverable, and what remains untouched?

## Inputs

What must the caller supply?

- A *home document* `d ∈ dom(Σ.M)` — the document under whose authority the link is allocated. (By L1a, ASN-0043, every link's home document must be allocated.)
- A *sequence of endsets* `(e₁, ..., eₙ)` with `N ≥ 3`, each `eᵢ ∈ Endset`, and `e₃ ≠ ∅`. (By L3, ASN-0043.)

The caller does *not* — and cannot — specify the link's address or its V-position in the home document. Both are determined by the system from the current state.

*Notation convention — `dom(M)` and `E_doc`.* ASN-0093 uses `dom(M)` for the set of allocated documents; ASN-0047 uses `E_doc` for the same set. In the combined substrate (ASN-0093 + ASN-0047), the two are identical at every reachable state: document registration occurs by K.σ (ASN-0093) or by K.δ in the IsDocument case (ASN-0047), each of which simultaneously enters `d` into both `dom(M)` and `E_doc`; and no transition removes a document from either set. Hence `d ∈ dom(M) ⟺ d ∈ E_doc` is a preserved invariant of the combined model. We use `dom(M)` throughout this ASN; ASN-0047 preconditions stated against `E_doc` — notably K.μ⁺_L's `d ∈ E_doc` — are discharged equivalently by membership in `dom(M)`.

*Endsets and emptiness.* L3 (ASN-0043) requires the third slot `e₃` to be non-empty but imposes no non-emptiness constraint on the other slots. The empty endset `eᵢ = ∅` is a permitted boundary case for `i ≠ 3`: by the coverage definition, `coverage(∅) = ⋃_{(s,ℓ) ∈ ∅} … = ∅`, so an empty slot contributes nothing to any `project(ℓ, i, ·, ·)` and nothing to any LP12-based discoverability disjunct. The analysis below covers this case implicitly through the existential `(E i :: …)` in LP12: empty slots simply fail to witness, leaving the disjunction's truth value determined by the non-empty slots.

## Decomposition

We observe that link creation must accomplish two distinct effects: (i) introduce the link into `dom(L)` with its value recorded, and (ii) make the link visible in the home document's arrangement. The substrate (ASN-0093, ASN-0047) provides exactly two atomic operations matching this division:

- `K.λ` allocates the link in `dom(L)`, binding it to the given endsets.
- `K.μ⁺_L` extends `M(d)` in the link subspace, mapping a fresh V-position to the link.

We therefore identify MAKELINK as the composite `K.λ ; K.μ⁺_L` — K.λ followed by K.μ⁺_L — applied to the same home document. The semicolon denotes sequential composition of atomic transitions, distinct from the tumbler addition operator `⊕` of ASN-0034. The order is forced: K.μ⁺_L's precondition requires `ℓ ∈ dom(L)`, so K.λ must precede it.

Why must MAKELINK include K.μ⁺_L? The substrate's coupling constraints (J0, J1★, J1'★ from ASN-0047) do not require it — they apply only to content-subspace allocations. But Nelson's design is explicit that a document "consists of its contents and its out-links" — retrieval of the home document's arrangement must yield the link. By L14a's supersession (ASN-0047), the link subspace of the home document's arrangement is where links live in V-space; K.μ⁺_L is what places them there. Without K.μ⁺_L, the link would be allocated but invisible to any retrieval framed against its home document's arrangement.

## Preconditions

The composite is valid when its component preconditions hold. For K.λ at `Σ`:

  d ∈ dom(M)
  ℓ ∉ dom(C) ∪ dom(L)
  zeros(ℓ) = 3 ∧ E(ℓ)₁ = s_L ∧ #E(ℓ) ≥ 2 ∧ origin(ℓ) = d
  ℓ is produced by A_L(d) (first emission if d has no prior links; otherwise inc(ℓ_prev, 0))
  N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅

For K.μ⁺_L at the intermediate state `Σ_mid` after K.λ:

  d ∈ dom(M)                  [preserved by K.λ's frame on dom(M)]
  ℓ ∈ dom(L)                  [established by K.λ]
  origin(ℓ) = d                [established by K.λ]
  ℓ ∉ ran(M(d))                [derived below]
  subspace(v_ℓ) = s_L          [by construction: v_ℓ = [s_L, k], so (v_ℓ)₁ = s_L]
  #v_ℓ = m_L = 2              [by LinkVPositionDepthAxiom (ASN-0047)]
  v_ℓ at the next link-subspace position per D-MIN★ / D-CTG★ at depth 2

The condition `ℓ ∉ ran(Σ_mid.M(d))` requires more than `ℓ ∉ dom(Σ.L)`; it must be derived through the S3★ + S3★-aux + L14 chain. K.λ's frame preserves `M`, so `Σ_mid.M(d) = Σ.M(d)` and `ran(Σ_mid.M(d)) = ran(Σ.M(d))`. By S3★-aux (ASN-0047), every `v ∈ dom(Σ.M(d))` has `subspace(v) ∈ {s_C, s_L}`. By S3★:

- If `subspace(v) = s_C`, then `Σ.M(d)(v) ∈ dom(Σ.C)`.
- If `subspace(v) = s_L`, then `Σ.M(d)(v) ∈ dom(Σ.L)`.

K.λ's freshness precondition gives `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)`. In either subspace case, `Σ.M(d)(v) ∈ dom(Σ.C) ∪ dom(Σ.L)`, so `Σ.M(d)(v) ≠ ℓ`. Hence `ℓ ∉ ran(Σ.M(d)) = ran(Σ_mid.M(d))`. L14 (StoreDisjointness, ASN-0093) confirms internal consistency at `Σ_mid`: `dom(Σ_mid.L) = dom(Σ.L) ∪ {ℓ}` and `dom(Σ_mid.C) = dom(Σ.C)`, so `ℓ ∈ dom(Σ_mid.L)` combined with `dom(Σ_mid.C) ∩ dom(Σ_mid.L) = ∅` gives `ℓ ∉ dom(Σ_mid.C)` — so no `s_C`-subspace V-position at `Σ_mid` can image to `ℓ` either, matching the conclusion derived above.

The intermediate-state conditions for K.μ⁺_L reduce to original-state conditions, so the caller-visible precondition for MAKELINK is just K.λ's precondition, with `ℓ` supplied by `A_L(d)`'s next emission and `v_ℓ` determined by the link subspace's current cardinality.

## Effect

We summarize the composite state transition. Writing the post-state as `Σ'`:

  Σ'.L  =  Σ.L ∪ {ℓ ↦ (e₁, ..., eₙ)}
  Σ'.M(d)  =  Σ.M(d) ∪ {v_ℓ ↦ ℓ}

where `v_ℓ` is determined by `Σ.M(d)`'s link subspace at depth `m_L = 2` (LinkVPositionDepthAxiom, ASN-0047):

  v_ℓ  =  [s_L, 1]                       if V_{s_L}(d) = ∅ at Σ
  v_ℓ  =  shift(max(V_{s_L}(d)), 1)        otherwise

By D-SEQ★ (ASN-0047), `V_{s_L}(d) = {[s_L, k] : 1 ≤ k ≤ n_L}` when non-empty (with `n_L = |V_{s_L}(d)|`), so `v_ℓ = [s_L, n_L + 1]` of depth `m_L = 2`. The caller does not supply `v_ℓ`; the substrate computes it from the link subspace's current cardinality.

Other components are unchanged:

  Σ'.C  =  Σ.C
  Σ'.E  =  Σ.E                                          [no entity allocation]
  Σ'.R  =  Σ.R                                          [provenance applies to content subspace only]
  (A ℓ' ∈ dom(Σ.L) :: Σ'.L(ℓ') = Σ.L(ℓ'))               [L12]
  (A d' ∈ dom(Σ.M), d' ≠ d :: Σ'.M(d') = Σ.M(d'))

## Freshness of the Allocation

The address `ℓ` is genuinely new. The argument proceeds in three layers.

*Within d's link chain.* By ChainMembershipForOrigin (ASN-0093), the set `dom(Σ.L) ∩ {ℓ' : origin(ℓ') = d}` is a contiguous initial segment `{s_1, …, s_{n_d}}` of `A_L(d)`'s enumeration, where `n_d` is the current count of links with `origin(·) = d`. Hence `max{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d} = s_{n_d}` (when `n_d ≥ 1`). K.λ's subsequent-emission rule selects `ℓ = inc(s_{n_d}, 0) = s_{n_d + 1}`. By ChainEnumerationInjectivity (ASN-0093), the chain `A_L(d) = (t_1, t_2, …)` is strictly monotone under T1, so `s_{n_d + 1} ≠ s_k` for every `k ≤ n_d` — i.e., `ℓ ∉ {s_1, …, s_{n_d}} = dom(Σ.L) ∩ {ℓ' : origin(ℓ') = d}`. In the first-emission case (`n_d = 0`), `ℓ = s_1` is the first chain element and `dom(Σ.L) ∩ {ℓ' : origin(ℓ') = d} = ∅`, so the conclusion holds trivially.

*Cross-subspace, within d.* By DisjointSubAllocatorChains (ASN-0093), `A_C(d)` and `A_L(d)` are disjoint — outputs differ in their element-field subspace identifier (`s_C` vs `s_L`), forced apart by SC-NEQ.

*Cross-document.* By Cross-doc disjointness (ASN-0093), for `d ≠ d'` the link-anchor prefixes `b_L(d)` and `b_L(d')` are non-nesting; T10 (PartitionIndependence, ASN-0034) then guarantees that every address extending `b_L(d)` differs from every address extending `b_L(d')`.

Hence `ℓ ∉ dom(C) ∪ dom(L)` at `Σ`, satisfying K.λ's freshness precondition by construction rather than by faith.

The V-position `v_ℓ` is fresh in `dom(M(d))` by K.μ⁺_L's positioning rule combined with D-SEQ★ (ASN-0047): the link subspace V-positions form a contiguous sequence `{[s_L, 1, ..., 1, k] : 1 ≤ k ≤ n_L}`, and `v_ℓ` extends it by one.

## Permanence of the Recording

The endset sequence `Σ'.L(ℓ) = (e₁, ..., eₙ)` is permanently fixed. We assemble three guarantees:

- By L12 (ASN-0093/ASN-0043), no transition modifies `L(ℓ)` once set.
- By LP2★ (ASN-0098), for every reachable state sequence `Σ' →* Σ''` and every slot `i`: `Σ''.L(ℓ).eᵢ = Σ'.L(ℓ).eᵢ`.
- By LP3★ (ASN-0098), for every such sequence and every slot: `coverage(Σ''.L(ℓ).eᵢ) = coverage(Σ'.L(ℓ).eᵢ)`.

The implication is that once recorded, the endsets' *addressing intent* is permanent. The link forever names the same set of I-addresses — even as those I-addresses' V-arrangements change, even if all V-arrangements lose them entirely, even if new documents transclude content sharing those I-addresses (in which case LP18 makes the link rediscoverable from those new documents).

## What Is Indexed?

We are looking for the discovery guarantee — the property that a future query "what links touch this content?" surfaces `ℓ` whenever the query's content lies in any of `ℓ`'s endset coverages.

The discovery function `discoverable_from(ℓ, d, Σ')` is defined in ASN-0098:

  project(ℓ, i, d, Σ')  =  {v ∈ dom(Σ'.M(d)) : Σ'.M(d)(v) ∈ coverage(Σ'.L(ℓ).eᵢ)}
  discoverable_from(ℓ, d, Σ')  ≡  (E i :: project(ℓ, i, d, Σ') ≠ ∅)

The function is *computed* from `Σ'.L(ℓ)` and `Σ'.M(d)` — no separate state component is required. By LP12 (ASN-0098):

  discoverable_from(ℓ, d, Σ')  ⟺  (E i : coverage(Σ'.L(ℓ).eᵢ) ∩ ran(Σ'.M(d)) ≠ ∅)

After MAKELINK, this biconditional holds at the post-state for every `d ∈ dom(Σ'.M)`. The link is discoverable from every document whose arrangement reaches into any of its endset coverages.

The abstract specification requires no auxiliary index state. The implementation may maintain an auxiliary structure — a reverse lookup from I-addresses to link addresses, the *spanfilade* in Gregory's implementation — for efficient computation. Such structures are caches: any state where they are consistent with `L` and `M` produces the same `project` and `discoverable_from` results. The abstract claim is the discovery *property*; the index is a performance choice.

This is the abstract content of what Nelson calls the system's "inter-indexing mechanisms": the mechanisms exist for performance; the discoverability is mathematical.

## Discoverability Is Symmetric

A consequence worth recording: the home document has no privileged position in discovery. By LP12, any document whose arrangement reaches `coverage(eᵢ)` for any `i` becomes a source from which `ℓ` is discoverable. The home document is one such document only if its own arrangement happens to reach into the endsets' coverages.

This matches Nelson's design intent: when a link's endsets reach into different documents owned by different users, all parties — and any third document transcluding either endpoint's content — can discover the link by querying their own content. The link belongs to its home document for ownership and naming; discovery is a property of content identity.

The MAKELINK operation respects this symmetry by treating all `N ≥ 3` endsets uniformly in storage. No endset is given special treatment beyond the type-endset's non-empty requirement (L3) and the from/to/type role convention (StandardTriple, ASN-0043).

## A Worked Example

We illustrate MAKELINK on a concrete state. Suppose at `Σ`:

- `dom(Σ.M) = {d, d'}` with `d = [1, 0, 1, 0, 1]` and `d' = [1, 0, 1, 0, 2]` — sibling documents under the same account.
- `dom(Σ.C) = {a₁, a₂, a₃}` with `a₁ = [d, 0, 1, 1]`, `a₂ = [d, 0, 1, 2]` (allocated by `A_C(d)`) and `a₃ = [d', 0, 1, 1]` (allocated by `A_C(d')`).
- `dom(Σ.L) = ∅` — no prior links.
- `Σ.M(d)` maps `[1, 1] ↦ a₁` and `[1, 2] ↦ a₂` (content-subspace positions at depth 2).
- `Σ.M(d')` maps `[1, 1] ↦ a₃`.

A caller invokes MAKELINK with home document `d` and endsets:

- `e₁ = {(a₁, δ(1, #a₁))}` — by PrefixSpanCoverage (ASN-0043), `coverage(e₁) = {t ∈ T : a₁ ≼ t}`.
- `e₂ = {(a₃, δ(1, #a₃))}` — `coverage(e₂) = {t ∈ T : a₃ ≼ t}`.
- `e₃ = {(τ, δ(1, #τ))}` for some type-tumbler `τ ∈ T` chosen so that `τ ⋠ x` for every `x ∈ {a₁, a₂, a₃, ℓ}` — `coverage(e₃) = {t ∈ T : τ ≼ t}`; non-empty as required by L3.

System-determined parameters:

- `ℓ = [d, 0, 2, 1]`, the first emission of `A_L(d)` (since `{ℓ' ∈ dom(L) : origin(ℓ') = d} = ∅`).
- `v_ℓ = [s_L, 1] = [2, 1]`, by D-MIN★ at depth `m_L = 2` (link subspace `V_{s_L}(d) = ∅` at `Σ`).

Post-state `Σ'`:

- `dom(Σ'.L) = {ℓ}` with `Σ'.L(ℓ) = (e₁, e₂, e₃)`.
- `Σ'.M(d) = {[1, 1] ↦ a₁, [1, 2] ↦ a₂, [2, 1] ↦ ℓ}`.
- `Σ'.M(d') = {[1, 1] ↦ a₃}` (unchanged by frame).
- `Σ'.C = Σ.C`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`.

Discoverability checks via LP12:

- `discoverable_from(ℓ, d, Σ')`: `ran(Σ'.M(d)) = {a₁, a₂, ℓ}`. We compute `coverage(e₁) ∩ ran(Σ'.M(d)) = {t : a₁ ≼ t} ∩ {a₁, a₂, ℓ}` by prefix-testing each element of `ran(Σ'.M(d))` against `a₁`. With `a₁ = [1, 0, 1, 0, 1, 0, 1, 1]`, `a₂ = [1, 0, 1, 0, 1, 0, 1, 2]`, and `ℓ = [1, 0, 1, 0, 1, 0, 2, 1]` (all of length 8): `a₁ ≼ a₁` trivially; `a₁ ⋠ a₂` since the two have equal length and disagree at position 8 (`1 ≠ 2`); `a₁ ⋠ ℓ` since the two have equal length and disagree at position 7 (`1 ≠ 2`). The intersection is `{a₁} ≠ ∅`. Hence `ℓ` is discoverable from its home document `d` via slot 1 — `d`'s arrangement reaches `a₁`, which `e₁` covers.

- `discoverable_from(ℓ, d', Σ')`: `ran(Σ'.M(d')) = {a₃}`. Prefix-testing `a₃ ≼ a₃` holds trivially, so `coverage(e₂) ∩ ran(Σ'.M(d')) = {t : a₃ ≼ t} ∩ {a₃} = {a₃} ≠ ∅`. Hence `ℓ` is discoverable from `d'` via slot 2.

The cross-document case `d' ≠ d` exhibits M-DiscSymmetry: discovery from `d'` does not consult `Σ'.M(d)`. The link's home document plays no privileged role in `d'`'s discovery; the relevant relation is `coverage(e₂) ∩ ran(Σ'.M(d'))`.

The type-endset coverage `coverage(e₃) = {t : τ ≼ t}` does not contribute to discoverability from either `d` or `d'` in this state: by the setup's constraint that `τ ⋠ x` for every `x ∈ {a₁, a₂, a₃, ℓ}`, prefix-testing each element of `ran(Σ'.M(d)) = {a₁, a₂, ℓ}` and `ran(Σ'.M(d')) = {a₃}` against `τ` yields no matches. Hence `coverage(e₃) ∩ ran(Σ'.M(d)) = ∅` and `coverage(e₃) ∩ ran(Σ'.M(d')) = ∅`. This is consistent with the type endset's role: it carries the link's classification, not its content connections.

## Weakest Precondition for Discoverability

We compute `wp(MAKELINK, discoverable_from(ℓ, d_target, ·))` — the predicate on the pre-state `Σ` (parametrized by the input endsets `(e₁, ..., eₙ)` and the choice of `d_target`) that ensures the post-state satisfies `discoverable_from(ℓ, d_target, Σ')`.

*Case 1: d_target ≠ d.* K.μ⁺_L's frame gives `Σ'.M(d_target) = Σ.M(d_target)`. By LP12 at `Σ'`:

  discoverable_from(ℓ, d_target, Σ')
    ⟺  (E i :: coverage(Σ'.L(ℓ).eᵢ) ∩ ran(Σ'.M(d_target)) ≠ ∅)
    ⟺  (E i :: coverage(eᵢ) ∩ ran(Σ.M(d_target)) ≠ ∅)

The wp reduces to a predicate on the pre-state alone:

  wp(MAKELINK, discoverable_from(ℓ, d_target, ·))
    ≡  (E i :: coverage(eᵢ) ∩ ran(Σ.M(d_target)) ≠ ∅)

The allocation of `ℓ` contributes nothing to discoverability from documents other than `d`. The wp depends only on the chosen endsets and `d_target`'s pre-existing arrangement.

*Case 2: d_target = d.* The post-state arrangement gains `ℓ`: `ran(Σ'.M(d)) = ran(Σ.M(d)) ∪ {ℓ}`. By LP12:

  discoverable_from(ℓ, d, Σ')
    ⟺  (E i :: coverage(eᵢ) ∩ (ran(Σ.M(d)) ∪ {ℓ}) ≠ ∅)
    ⟺  (E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)  ∨  (E i :: ℓ ∈ coverage(eᵢ))

The disjunction isolates two routes to home-document discoverability:

- (i) *Arrangement-reach route:* some endset's coverage intersects `d`'s pre-existing arrangement range.
- (ii) *Reflexive route:* some endset's coverage contains `ℓ` itself.

*Reduction under standard authoring.* The caller does not know `ℓ` at endset-formation time — the substrate determines `A_L(d)`'s next emission only when K.λ fires. Under the discipline that endsets reference *already-existing* substrate addresses (`coverage(eᵢ) ⊆ dom(Σ.C) ∪ dom(Σ.L)` at `Σ`), the reflexive route's disjunct is unreachable: by K.λ's freshness, `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)`, so `ℓ ∉ coverage(eᵢ)` for any `i`. The wp collapses:

  wp(MAKELINK, discoverable_from(ℓ, d, ·))
    ≡  (E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)

— the same shape as Case 1. Under standard authoring, home-document discoverability requires `d`'s arrangement to reach into some endset's coverage; there is no automatic "self-discovery" of `ℓ` from `d`. The home-document privilege of MAKELINK is structural (placement of `v_ℓ`), not semantic (privileged discoverability).

## Reflexive Endsets

L13 (ReflexiveAddressing, ASN-0043) permits link addresses as valid endset targets — a link's endsets may cover other link addresses, or even cover the link's own address. We consider the case where one of MAKELINK's input endsets has coverage containing `ℓ` itself.

*The caller cannot construct a reflexive endset deliberately.* The substrate does not expose `A_L(d)`'s next emission to the caller. Endsets are chosen without knowledge of `ℓ`. Reflexive coverage arises only by accident — when an endset span chosen for other reasons happens to contain the address `ℓ` that `A_L(d)` will emit. Under standard authoring (endsets that reference *already-existing* addresses), the reflexive case is excluded by K.λ's freshness, since `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)`.

*A reflexive endset yields guaranteed home-document discovery at the post-state.* Suppose `ℓ ∈ coverage(eᵢ)` for some `i ∈ {1, ..., N}`. After MAKELINK, `Σ'.M(d)(v_ℓ) = ℓ ∈ coverage(Σ'.L(ℓ).eᵢ)` (by K.λ's effect `Σ_mid.L(ℓ) = (e₁, ..., eₙ)` and K.μ⁺_L's frame `Σ'.L = Σ_mid.L`, so `Σ'.L(ℓ).eᵢ = eᵢ` and `coverage(Σ'.L(ℓ).eᵢ) = coverage(eᵢ)`). Hence `v_ℓ ∈ project(ℓ, i, d, Σ')`, giving `discoverable_from(ℓ, d, Σ')`. The home document's reflexive discovery is forced regardless of `Σ.M(d)`'s pre-existing arrangement.

*No reflexive discovery from other documents.* For `d_target ≠ d`, K.μ⁺_L's frame leaves `Σ.M(d_target)` unchanged: `ran(Σ'.M(d_target)) = ran(Σ.M(d_target))`. The address `ℓ` enters only `d`'s arrangement, so only `d`'s `discoverable_from` query benefits from the reflexive endset. Other documents must rely on their own arrangement-reach into `coverage(eᵢ)` to discover `ℓ`.

*Consistency with M-DiscSymmetry.* The home-document privilege under reflexive endsets is structural, not semantic. M-DiscSymmetry asserts that LP12's definition of `discoverable_from` treats every document uniformly — it does not distinguish home from non-home. The asymmetry of outcome under reflexive endsets reflects the asymmetry of arrangement-reach: MAKELINK places `v_ℓ` in `d`'s arrangement only, not in any other document's. The discovery protocol is symmetric; the substrate state change is localised to `d`.

*Boundary case for LP12.* LP12's biconditional `discoverable_from(ℓ, d_target, Σ') ⟺ (E i :: coverage(Σ'.L(ℓ).eᵢ) ∩ ran(Σ'.M(d_target)) ≠ ∅)` holds in the reflexive case via the witness `ℓ ∈ coverage(eᵢ) ∩ {ℓ} ⊆ coverage(eᵢ) ∩ ran(Σ'.M(d))` (using `v_ℓ ↦ ℓ ∈ ran(Σ'.M(d))`). No special-case rule is needed; LP12 covers the reflexive case uniformly.

## What Does Not Change

The frame `Σ'.C = Σ.C` is total: every `a ∈ dom(Σ.C)` satisfies `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`. The referenced content is byte-identical before and after MAKELINK.

This is not a separate guarantee. It is a direct consequence of the composite's structure: K.λ modifies only `L`, and K.μ⁺_L modifies only `M(d)`. Neither operation touches `C`. The link's endsets *reference* I-addresses in `dom(C)`, but referencing is read-only — the endset stores spans (start, length pairs), not the bytes at those addresses. The bytes remain where they were.

By the same reasoning, no prior link in `dom(L)` is modified (L12), no other document's arrangement is modified (frame on `M`), no entity is allocated, no provenance pair is recorded.

The phenomenology Nelson describes — that creating a link has zero effect on the content it references — falls out of the architecture: ownership of the link belongs to the home document; the link's storage is in the home document's element subspace; writing into the home document's element subspace cannot, by structure, modify content at I-addresses elsewhere. The guarantee is structural, not behavioral.

## Side Effects on Prior Links' Discoverability

Although the frame `(A ℓ' ∈ dom(Σ.L) :: Σ'.L(ℓ') = Σ.L(ℓ'))` preserves every prior link's value, `ran(Σ'.M(d)) = ran(Σ.M(d)) ∪ {ℓ}` gains the new address. Discoverability is a derived property of `(L, M)`, not a state component the frame can directly assert about — so the frame does not, by itself, exclude a change in `discoverable_from(ℓ', ·, ·)` for prior links `ℓ'`.

We characterize the change. For a prior link `ℓ' ∈ dom(Σ.L)`, by L12 and LP3★ the coverage of every endset of `ℓ'` is preserved across MAKELINK: `coverage(Σ'.L(ℓ').eᵢ) = coverage(Σ.L(ℓ').eᵢ)`. The only post-state change relevant to `discoverable_from(ℓ', d, ·)` is the addition of `ℓ` to `ran(M(d))`. By LP12 at `Σ` and `Σ'`:

  discoverable_from(ℓ', d, Σ')
    ⟺  (E i :: coverage(Σ'.L(ℓ').eᵢ) ∩ ran(Σ'.M(d)) ≠ ∅)
    ⟺  (E i :: coverage(Σ.L(ℓ').eᵢ) ∩ (ran(Σ.M(d)) ∪ {ℓ}) ≠ ∅)
    ⟺  discoverable_from(ℓ', d, Σ)  ∨  (E i :: ℓ ∈ coverage(Σ.L(ℓ').eᵢ))

Hence `ℓ'` is *newly* discoverable from `d` (discoverable at `Σ'` but not at `Σ`) precisely when some endset of `ℓ'` covers `ℓ`:

  ¬discoverable_from(ℓ', d, Σ)  ∧  discoverable_from(ℓ', d, Σ')
    ⟺  ¬(E i :: coverage(Σ.L(ℓ').eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)
       ∧ (E i :: ℓ ∈ coverage(Σ.L(ℓ').eᵢ))

This is the LP9 (ExtensionMonotonicity, ASN-0098) growth characterization specialized to MAKELINK's single new V-position `v_ℓ ↦ ℓ`: the set of new projection witnesses is `{v_ℓ}` if `ℓ ∈ coverage(Σ.L(ℓ').eᵢ)`, otherwise `∅`. When `ℓ'` was orphaned at `Σ` (`¬discoverable_from(ℓ', d', Σ)` for every `d'`), this is exactly the LP18 (Resurrection, ASN-0098) pattern with `a* = ℓ` and `d` as the resurrection target.

The side effect is bounded: it can only occur when `ℓ'` was authored with an endset whose span coverage extends to addresses not yet allocated at authoring time. Such forward-reaching endsets are permitted by L4 (EndsetGenerality, ASN-0043) — endset spans may reference any addresses in the tumbler space, including those not currently in `dom(C) ∪ dom(L)`. MAKELINK's allocation of `ℓ` "fills in" a previously-uncovered region of the address space, retroactively activating any prior endset that had pre-emptively claimed it. Under standard authoring (every endset's coverage is a subset of `dom(C) ∪ dom(L)` at authoring time), no prior link can cover the fresh `ℓ`, so the side effect is vacuous.

*Restriction to the home document.* The biconditional above is stated for `d` — MAKELINK's home document — because `d` is the only document whose arrangement K.μ⁺_L modifies. For any other document `d_target ≠ d`, K.μ⁺_L's frame `(A d' ≠ d :: Σ'.M(d') = Σ.M(d'))` preserves the arrangement, and K.λ leaves `M` entirely unchanged, so `ran(Σ'.M(d_target)) = ran(Σ.M(d_target))`. By LP12, prior-link discoverability from `d_target` is unchanged: `discoverable_from(ℓ', d_target, Σ') = discoverable_from(ℓ', d_target, Σ)`. The side-effect window is confined to the home document.

## Invariant Preservation

We verify the substrate invariants in three classes, following ASN-0047's stratification: (a) *per-state invariants* holding at the post-state `Σ'`; (b) *composite-boundary properties* (P4★, P4a, P7a) evaluated at composite boundaries; (c) *transition invariants* governing the pair `Σ → Σ'`. The new entries are `ℓ ∈ dom(L)` and `v_ℓ ∈ dom(M(d))`; prior entries are unchanged by the frame.

### Per-State Invariants at Σ'

For the link itself:

  L0:    E(ℓ)₁ = s_L                          from K.λ precondition
  L1:    zeros(ℓ) = 3                          from K.λ precondition
  L1a:   origin(ℓ) = d ∈ dom(Σ'.M)             from K.λ precondition and M1
  L1b:   #E(ℓ) ≥ 2                             from K.λ precondition
  L3:    N ≥ 3 ∧ e₃ ≠ ∅                       from K.λ precondition
  L12:   immutability                          new entry only; no modification of prior
  L14:   store disjointness                    ℓ ∉ dom(C) from K.λ freshness
  L-fin: link store finiteness                 |dom(L')| = |dom(L)| + 1

L1c (structural inc-chain conformance) requires an explicit chain from `origin(ℓ) = d` to `ℓ`. Writing `ℓ = [d, 0, s_L, k_s]` for the chain index `k_s ≥ 1` of `ℓ` in `A_L(d)`, we construct the chain `(t₀, t₁, ..., t_n)` with explicit zero counts:

  i   tᵢ                                                kᵢ   zeros(tᵢ₋₁) bound  zeros(tᵢ)
  0   d                                                  —    —                  2          (M0)
  1   inc(d, 2)      = [d, 0, 1]      = b_C(d)           2    zeros(d) = 2 ≤ 2   3
  2   inc(b_C(d),0)  = [d, 0, 2]      = b_L(d)           0    n/a                3
  3   inc(b_L(d),1)  = [d, 0, 2, 1]   = t_1^L(d)         1    zeros(b_L(d))=3≤3  3
  3+j inc(t_{2+j},0) = [d, 0, 2, 1+j]                    0    n/a                3
                                                                                  (1 ≤ j ≤ k_s − 1)

so `n = k_s + 2`. The "bound" column records TA5a's preservation precondition: at `k = 2`, `zeros(t) ≤ 2`; at `k = 1`, `zeros(t) ≤ 3`; at `k = 0`, no bound applies. The `zeros(tᵢ)` column records the post-step value, derived from K.δ-ID.zeros-0/1 and K.δ-ID.zeros-2 (ASN-0047): `k ∈ {0, 1}` preserves zeros; `k = 2` adds one. Step-by-step verification:

- *t₁ = inc(d, 2) = b_C(d):* By TA5(d) (ASN-0034) at `k = 2`, `inc(d, 2)` appends positions `#d + 1` (value 0) and `#d + 2` (value 1), giving `[d, 0, 1]`. Under SubspaceConventionAxiom (ASN-0093), `s_C = 1`, so `[d, 0, 1] = [d, 0, s_C] = b_C(d)`. TA5a's `k = 2` admissibility requires `zeros(t₀) ≤ 2`; by M0 (ASN-0093), `zeros(d) = 2`, so the bound holds with equality. T4-validity is preserved by TA5a. `zeros(t₁) = zeros(d) + 1 = 3`. `#t₁ = #d + 2 > #d`. The L1c clause `k₁ = 2` is satisfied. ✓

- *t₂ = inc(b_C(d), 0) = b_L(d):* By TA5(c) at `k = 0`, `inc(b_C(d), 0)` increments the rightmost nonzero component (position `#d + 2`, value 1) to 2, giving `[d, 0, 2] = b_L(d)` (since `s_L = 2` by SubspaceConventionAxiom). No zero-count side condition applies at `k = 0`. T4-validity preserved by TA5a (sibling step). `zeros(t₂) = zeros(b_C(d)) = 3`. `#t₂ = #d + 2 > #d`. ✓

- *t₃ = inc(b_L(d), 1) = t_1^L(d):* By TA5(d) at `k = 1`, `inc(b_L(d), 1)` appends a single component of value 1 at position `#d + 3`, giving `[d, 0, 2, 1]`. By SubAllocatorAxiom.FirstEmission (ASN-0093), this is exactly `t_1^L(d)`. TA5a's `k = 1` admissibility requires `zeros(b_L(d)) ≤ 3`; from step t₂ we have `zeros(b_L(d)) = 3`, so the bound holds with equality. T4-validity preserved by TA5a. `zeros(t₃) = zeros(b_L(d)) = 3`. `#t₃ = #d + 3 > #d`. ✓

- *t_{3+j} = inc(t_{2+j}, 0) for j ≥ 1:* These are A_L(d)'s SiblingRecurrence steps (SubAllocatorAxiom.ChainDiscipline). Each `k_{3+j} = 0` increments the rightmost nonzero position (the element-field counter). No zero-count bound applies at `k = 0`. T4-validity preserved by TA5a. `zeros(t_{3+j}) = zeros(t_{2+j}) = 3`. Length unchanged at `#d + 3 > #d`. ✓

The chain satisfies every L1c clause: every `kᵢ ∈ {0, 1, 2}`, `k₁ = 2`, every `#tᵢ > #d`, and TA5a's per-step admissibility holds throughout — the `k = 2` step at position 1 against `zeros(d) = 2`, and the `k = 1` step at position 3 against `zeros(b_L(d)) = 3`. Zero counts saturate at 3 from t₁ onward, consistent with L1's `zeros(ℓ) = 3`.

Both admissibility bounds *saturate exactly* — the `k = 2` step at position 1 with `zeros(d) = 2 = 2` (TA5a's `k = 2` limit) and the `k = 1` step at position 3 with `zeros(b_L(d)) = 3 = 3` (TA5a's `k = 1` limit) — leaving no slack in either direction. From the post-t₁ state with `zeros = 3`, no further `k = 2` step is admissible (would require `zeros ≤ 2`); from the post-t₃ state with `zeros = 3`, no further `k = 1` step is admissible (would require `zeros ≤ 3` — this bound is also at saturation but additional `k = 1` steps would drive `#E` and length beyond the structural target). Combined with TA5a's branching constraint (each step fixes one of `k ∈ {0, 1, 2}` with the precondition-permitted values determined by the current zero count), the chain `(d, b_C(d), b_L(d), t_1^L(d), …, ℓ)` is the *unique* structural inc-derivation of any `ℓ ∈ dom(L)` from its home document. L1c's existential conclusion ("there exists a chain") therefore tightens, for link addresses, to a canonical witness — every `ℓ ∈ dom(L)` has exactly one structural inc-derivation from `origin(ℓ)`.

For the V-arrangement entry `v_ℓ ↦ ℓ`:

  S2:       M'(d) remains a partial function                      v_ℓ ∉ dom(Σ.M(d)) by the two-part argument below; v_ℓ enters dom(M'(d)) fresh, preserving functionality of M'(d)
  S3★:      image of v_ℓ is ℓ ∈ dom(L'), subspace(v_ℓ) = s_L     direct from the effect
  S3★-aux:  subspace(v_ℓ) = s_L ∈ {s_C, s_L}                      direct from the effect
  S8a:      zeros(v_ℓ) = 0, #v_ℓ = 2 ≥ 2, components all > 0      v_ℓ = [s_L, k] with s_L = 2 > 0, k ≥ 1
  S8-depth: depth uniformity in subspace s_L at d                 m_L = 2 for all V-positions in V_{s_L}(d'), by LinkVPositionDepthAxiom
  S8-fin:   |dom(M'(d))| = |dom(M(d))| + 1                       S8-fin at Σ gives finiteness of the predecessor
  S8★:      per-subspace span decomposition                       link subspace admits trivial length-1 decomposition (see below)
  CL-OWN:   origin(M'(d)(v_ℓ)) = origin(ℓ) = d                   direct from K.λ precondition
  CL-UNIQ:  partial injection preserved                           K.μ⁺_L first-arrangement guard ℓ ∉ ran(M_mid(d))
  D-MIN★:   v_ℓ at minimum if empty                               K.μ⁺_L positioning rule (depth 2)
  D-CTG★:   extension is contiguous                               K.μ⁺_L positioning rule
  D-SEQ★:   V_{s_L}(d') is contiguous initial segment             see below

For S2: we must show `v_ℓ ∉ dom(Σ.M(d))`, not merely `v_ℓ ∉ V_{s_L}(d)`. By S3★-aux at `Σ`, `dom(Σ.M(d)) = V_{s_C}(d) ∪ V_{s_L}(d)`, so the obligation splits into two exclusions:
- *Within-subspace exclusion:* `v_ℓ ∉ V_{s_L}(d)`. By D-SEQ★ at `Σ`, `V_{s_L}(d) = {[s_L, k] : 1 ≤ k ≤ n_L}`; K.μ⁺_L's positioning rule sets `v_ℓ = [s_L, n_L + 1]` (or `[s_L, 1]` when `n_L = 0`), which lies outside this set by the strict inequality `n_L + 1 > n_L` (resp. by the emptiness of the set when `n_L = 0`).
- *Cross-subspace exclusion:* `v_ℓ ∉ V_{s_C}(d)`. By construction `(v_ℓ)₁ = s_L`, while by S8a every `v ∈ V_{s_C}(d)` has `(v)₁ = s_C`. By SC-NEQ (ASN-0093), `s_L ≠ s_C`, so `v_ℓ ≠ v` for every `v ∈ V_{s_C}(d)`.

Combining the two exclusions, `v_ℓ ∉ V_{s_C}(d) ∪ V_{s_L}(d) = dom(Σ.M(d))`, discharging S2. ✓

For D-SEQ★: by D-SEQ★ at `Σ`, `V_{s_L}(d) = {[s_L, k] : 1 ≤ k ≤ n_L}` for some `n_L ≥ 0` (with `n_L = 0` meaning the link subspace at `d` is empty). If `n_L = 0`, the K.μ⁺_L positioning rule gives `v_ℓ = [s_L, 1]`, so `V_{s_L}(d') = {[s_L, 1]}` — a contiguous initial segment of length 1. If `n_L ≥ 1`, the rule gives `v_ℓ = shift([s_L, n_L], 1) = [s_L, n_L + 1]`, so `V_{s_L}(d') = {[s_L, k] : 1 ≤ k ≤ n_L + 1}` — a contiguous initial segment of length `n_L + 1`. Either way, the post-state set conforms to D-SEQ★. ✓

For S8★: per ASN-0047's S8★, the link-subspace projected arrangement `M'(d)|_{V_{s_L}(d')} : V_{s_L}(d') → dom(L')` admits the trivial length-1 decomposition `{(v, M'(d)(v), 1) : v ∈ V_{s_L}(d')}`. The new entry `(v_ℓ, ℓ, 1)` joins this decomposition; S8's conditions (a) and (b) hold trivially at length 1. ✓

For state components unchanged by MAKELINK (`C`, `E`, `R`) and for the document-set `dom(M)`, the remaining per-state invariants are preserved:

- M0 (DocumentTumblerWellFormed, ASN-0093): vacuous since `dom(Σ'.M) = dom(Σ.M)` (MAKELINK allocates no new document); every `d ∈ dom(Σ'.M)` satisfies M0 by inheritance from `Σ`.
- S4 (origin-based identity for content addresses, ASN-0036): vacuous since `Σ'.C = Σ.C`; the lemma quantifies over `dom(C)` allocation events, of which MAKELINK introduces none.
- L11a (link uniqueness, ASN-0043): the new allocation event for `ℓ` is distinct from every prior link allocation event (by ChainEnumerationInjectivity, DisjointSubAllocatorChains, and Cross-doc disjointness — see "Freshness of the Allocation"), so L11a's distinctness conclusion holds at `Σ'`.
- S7a, S7b, S7c, S7d (origin and structural attribution for content addresses): vacuous since `Σ'.C = Σ.C`; the predicates quantify over `dom(C)`, which is unchanged.
- C-fin (content store finiteness): vacuous since `dom(Σ'.C) = dom(Σ.C)` is finite at `Σ`.
- P6 (existential coherence), P7 (provenance grounding): vacuous since `dom(C)`, `dom(M)`, and `R` are unchanged in the relevant respects (`dom(M)` grows only by new V-positions within an already-allocated document, not by new documents; `R` is unchanged).
- P8 (entity hierarchy): vacuous since `E` is unchanged.
- NodeLineage (descent from bootstrap): vacuous since `E` is unchanged.

### Composite-Boundary Properties

ASN-0047 classifies P4★, P4a, and P7a as Class (b) — properties discharged at composite boundaries by the coupling constraints J0, J1★, J1'★. MAKELINK introduces a single link-subspace V-arrangement entry; J-coupling is vacuous (J0, J1★, J1'★ all quantify over content-subspace effects on `dom(C) \ pre-state` or `ran(M(d)) \ pre-state` restricted to `subspace = s_C`, none of which are produced by MAKELINK).

- P4★ (ProvenanceBoundsContentSubspace): `Contains_C(Σ') ⊆ R'`. The new V-arrangement entry `v_ℓ ↦ ℓ` has `subspace(v_ℓ) = s_L`, so it does not contribute to `Contains_C(Σ')`. Hence `Contains_C(Σ') = Contains_C(Σ) ⊆ R = R'`.
- P4a (HistoricalFidelity): for every `(a, d') ∈ R'`, some prior state `Σ_k` in the transition history had `M_k(d')(v) = a` with `subspace(v) = s_C`. Since `R' = R`, the obligation is identical to P4a at `Σ`, which holds by the reachability hypothesis on `Σ`.
- P7a (ProvenanceCoverage): for every `a ∈ dom(Σ'.C)`, some `d'` satisfies `(a, d') ∈ R'`. Since `dom(Σ'.C) = dom(Σ.C)` and `R' = R`, the obligation is identical to P7a at `Σ`, which holds by reachability.

### Transition Invariants for Σ → Σ'

- M1 (ArrangementMonotonicity, ASN-0093): `dom(Σ.M) ⊆ dom(Σ'.M)`. Trivially holds with equality — MAKELINK does not extend `dom(M)`.
- L12 (LinkImmutability): `(A ℓ' ∈ dom(Σ.L) :: ℓ' ∈ dom(Σ'.L) ∧ Σ'.L(ℓ') = Σ.L(ℓ'))`. K.λ adds only the fresh `ℓ`; no prior entry is modified.
- P0 (ContentPermanence): trivially via the frame `Σ'.C = Σ.C`.
- P1 (EntityPermanence): trivially via the frame `Σ'.E = Σ.E`.
- P2 (ProvenancePermanence): trivially via the frame `Σ'.R = Σ.R`.
- P3 (ArrangementMutabilityOnly): the conjunction P0 ∧ P1 ∧ P2 ∧ L12, already discharged above clause-by-clause. P3 holds at MAKELINK.
- S9 (TwoStreamSeparation, ASN-0036): `S9` follows from P0 alone — since `Σ'.C = Σ.C`, the antecedent's consequent (preservation of every content entry) is satisfied by the identity, regardless of which arrangement modifications occurred. P0 is discharged trivially.

## Atomicity

MAKELINK is a *composite* of two atomic transitions. Each component is atomic by SequentialTransitionAxiom (ASN-0093). The composite is not.

In the intermediate state `Σ_mid` between K.λ and K.μ⁺_L:

- `ℓ ∈ dom(Σ_mid.L)` with value `Σ_mid.L(ℓ) = (e₁, ..., eₙ)` — the link exists, with its endsets recorded.
- `ℓ ∉ ran(Σ_mid.M(d))` — the link is not yet visible in any V-arrangement (derived in Preconditions).
- `discoverable_from(ℓ, d_target, Σ_mid)` is well-defined for every `d_target ∈ dom(Σ_mid.M) = dom(Σ.M)` since `ℓ ∈ dom(Σ_mid.L)` and `Σ_mid.L(ℓ) = (e₁, ..., eₙ)`.

`Σ_mid` is a fully reachable state, not a transitional artifact: by SequentialTransitionAxiom (ASN-0093), every atomic step commits before the next begins, so K.λ on `Σ` yields a complete state `Σ_mid` against which K.μ⁺_L's precondition is evaluated. The per-state invariants hold at `Σ_mid` — in particular, S3★ (referential integrity) is preserved because K.λ extends `dom(L)` from `dom(Σ.L)` to `dom(Σ.L) ∪ {ℓ}` while preserving `M` entirely (K.λ frame: `Σ_mid.M = Σ.M`), so every `v ∈ dom(Σ_mid.M(d'))` images consistently — content-subspace V-positions still point into the unchanged `dom(Σ_mid.C) = dom(Σ.C)`, and link-subspace V-positions still point into `dom(Σ_mid.L) ⊇ dom(Σ.L)` (referential integrity cannot break under growth). The same reasoning preserves all link-store invariants (L0, L1, L1a, L1b, L1c, L3, L14, L-fin) at `Σ_mid` via K.λ's precondition discharge.

We compare discoverability at `Σ_mid` and `Σ'`. By LP12:

  Σ_mid:  discoverable_from(ℓ, d_target, Σ_mid)  ⟺  (E i :: coverage(eᵢ) ∩ ran(Σ_mid.M(d_target)) ≠ ∅)
  Σ':     discoverable_from(ℓ, d_target, Σ')     ⟺  (E i :: coverage(eᵢ) ∩ ran(Σ'.M(d_target)) ≠ ∅)

For `d_target ≠ d`, K.μ⁺_L's frame gives `Σ'.M(d_target) = Σ_mid.M(d_target)`, so the two values coincide. For `d_target = d`, the post-state arrangement gains `ℓ`: `ran(Σ'.M(d)) = ran(Σ_mid.M(d)) ∪ {ℓ}`. The two values differ precisely when some endset `eᵢ` *reflexively* covers `ℓ`: if `ℓ ∈ coverage(eᵢ)` for some `i`, then `discoverable_from(ℓ, d, Σ')` is forced true via `v_ℓ` while `discoverable_from(ℓ, d, Σ_mid)` may be false. The reflexive case is treated in the "Reflexive Endsets" section. Outside the reflexive case, the value of `discoverable_from(ℓ, d, ·)` agrees at `Σ_mid` and `Σ'`.

The substrate provides no composite-level atomicity. A reader observing `Σ_mid` would see the link in `dom(L)` but not in `M(d)`. If this intermediate visibility is undesirable — if MAKELINK must appear as a single event — the protocol layer above must enforce it, typically by sequencing both atomic transitions within a single request-response cycle.

Nelson's "canonical operating condition" language suggests external atomicity is expected: MAKELINK is presented to the client as one event, and the system must be canonical at the response. This is a *protocol-level* guarantee, not a substrate-level one. The strand model does not, by itself, supply it.

## Permanence

By LP13 (ASN-0098), the link persists unconditionally:

  (A reachable Σ' →* Σ'' :: ℓ ∈ dom(Σ''.L) ∧ Σ''.L(ℓ) = Σ'.L(ℓ))

No transition in the substrate's vocabulary removes `ℓ` from `dom(L)` or modifies `L(ℓ)`. The link is permanent in the strongest sense: its identity, its value, and its home are all immutable for the life of the system.

The link's V-position `v_ℓ` in the home document is less permanent. Subsequent operations may remove it (per the contraction operation's rules) or rebind its image (per the reordering operation's rules — K.μ~ does not reassign V-positions themselves but applies a bijection `π : dom(M(d)) → dom(M'(d))` to the mapping graph, and by K.μ~-FIX `dom(M'(d)) = dom(M(d))`, so `v_ℓ` itself persists in the domain; what changes is which value `M(d)(v_ℓ)` maps to, and where `ℓ` re-appears as the image of some other V-position). What is permanent is the link's I-address and value; what is mutable is the V-position-to-link binding within the home document's arrangement graph. This is S9 (TwoStreamSeparation, ASN-0036) specialized to the link subspace.

Even if `v_ℓ` is later removed from `dom(M(d))`, the link is still in `dom(L)` and still discoverable when conditions warrant. By LP17 (ASN-0098), a link orphaned from all V-arrangements remains in the store; by LP18, it becomes discoverable again when any document later transcludes content covered by its endsets. The two-stream architecture makes link permanence cleanly separable from link visibility.

## What MAKELINK Does Not Do

For clarity, we enumerate what MAKELINK does not perform:

- *No content allocation.* `dom(Σ'.C) = dom(Σ.C)`. The link's endsets may reference I-addresses not currently in `dom(C)`; this is permitted by the endset definition and does not trigger any content allocation.
- *No content modification.* `Σ'.C = Σ.C`, including at I-addresses referenced by the endsets.
- *No modification of prior links.* L12.
- *No modification of other documents' arrangements.* `(A d' ≠ d :: Σ'.M(d') = Σ.M(d'))`.
- *No entity allocation.* `Σ'.E = Σ.E`.
- *No provenance recording.* `Σ'.R = Σ.R`. Provenance, per P2/P4★, tracks content-subspace arrangement history; link placement in the link subspace is outside its scope.
- *No permission check on referenced content.* Per Nelson's publication contract, publication grants linking rights to all parties; MAKELINK does not verify ownership of the documents whose content the endsets reach. The substrate has no such mechanism, and the design intent rules it out.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| M-Comp | MAKELINK is the composite `K.λ ; K.μ⁺_L` — K.λ followed by K.μ⁺_L — applied to the same home document `d`. The semicolon denotes sequential composition, distinct from the tumbler addition `⊕` of ASN-0034. | introduced |
| M-Pre | Caller-visible precondition: `d ∈ dom(M)`, `N ≥ 3`, `(A i : eᵢ ∈ Endset)`, `e₃ ≠ ∅`. System-supplied parameters: `ℓ` from `A_L(d)`'s next emission, `v_ℓ` from K.μ⁺_L's positioning rule at depth `m_L = 2`. | introduced |
| M-Alloc | MAKELINK allocates a fresh `ℓ ∈ T \ (dom(Σ.L) ∪ dom(Σ.C))` and a fresh `v_ℓ ∈ T \ dom(Σ.M(d))` with `subspace(v_ℓ) = s_L` and `#v_ℓ = 2`. | introduced |
| M-Effect | `Σ'.L = Σ.L ∪ {ℓ ↦ (e₁, ..., eₙ)}`; `Σ'.M(d) = Σ.M(d) ∪ {v_ℓ ↦ ℓ}` where `v_ℓ = [s_L, 1]` if `V_{s_L}(d) = ∅` at `Σ`, else `v_ℓ = shift(max(V_{s_L}(d)), 1) = [s_L, n_L + 1]` (with `n_L = |V_{s_L}(d)|`). | introduced |
| M-Frame | `Σ'.C = Σ.C`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`; existing entries in `L` and in `M(d')` for `d' ≠ d` are unchanged. | introduced |
| M-NoContentEffect | For every `a ∈ dom(Σ.C)`: `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`. The referenced content is byte-identical before and after MAKELINK. | introduced |
| M-DiscSymmetry | Discoverability of `ℓ` is symmetric across all documents whose arrangements reach into any endset coverage; the home document has no privileged role in LP12's definition. Any asymmetry of outcome reflects asymmetry of arrangement-reach, not a privileged status. | introduced |
| M-Reflexive | If `ℓ ∈ coverage(eᵢ)` for some `i` (the reflexive endset case), then `v_ℓ ∈ project(ℓ, i, d, Σ')` and `discoverable_from(ℓ, d, Σ')` is forced true regardless of `Σ.M(d)`'s pre-existing arrangement. Under standard authoring (`coverage(eᵢ) ⊆ dom(Σ.C) ∪ dom(Σ.L)` for every `i`), the reflexive case is excluded by K.λ's freshness. | introduced |
| M-PriorLinkDisc | For every prior link `ℓ' ∈ dom(Σ.L)` and every document `d_target ∈ dom(Σ.M)`: if `d_target = d` (the home document of the new link `ℓ`), then `discoverable_from(ℓ', d, Σ') ⟺ discoverable_from(ℓ', d, Σ) ∨ (E i :: ℓ ∈ coverage(Σ.L(ℓ').eᵢ))` — a prior link is newly discoverable from `d` precisely when some endset of `ℓ'` covers `ℓ`; if `d_target ≠ d`, then `discoverable_from(ℓ', d_target, Σ') = discoverable_from(ℓ', d_target, Σ)` by K.μ⁺_L's frame on `M` (and K.λ's frame on `M`), so prior-link discoverability is unchanged. The discoverability relation is derived from `(L, M)` and is not preserved by the frame on `L` alone; the side-effect window is confined to the home document. | introduced |
| M-WP | Post-MAKELINK discoverability has explicit weakest preconditions on `Σ`: for `d_target ≠ d`, `wp ≡ (E i :: coverage(eᵢ) ∩ ran(Σ.M(d_target)) ≠ ∅)`; for `d_target = d`, `wp ≡ (E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅) ∨ (E i :: ℓ ∈ coverage(eᵢ))`. Under standard authoring, the home and non-home wp shapes coincide. | introduced |
| M-Perm | After MAKELINK: `(A Σ' →* Σ'' :: ℓ ∈ dom(Σ''.L) ∧ Σ''.L(ℓ) = Σ'.L(ℓ))`, by LP13. | introduced |
| M-NoIndexState | The abstract specification requires no separate index state component. Discoverability is computed from `L` and `M` via the projection function of ASN-0098. | introduced |
| M-CompAtomicity | The composite is not atomic at the substrate level. The intermediate state `Σ_mid` between K.λ and K.μ⁺_L has the link allocated but not placed. `discoverable_from(ℓ, d_target, ·)` agrees at `Σ_mid` and `Σ'` for every `d_target ≠ d`; for `d_target = d` the two values agree unless some endset reflexively covers `ℓ`. Composite-level atomicity, if required, belongs to the protocol layer above the substrate. | introduced |
| M-Inv-State | *Per-state invariants at `Σ'`.* The post-state satisfies: link-store invariants (L0, L1, L1a, L1b, L1c, L3, L14, L-fin); arrangement invariants (S2, S3★, S3★-aux, S8a, S8-depth, S8-fin, S8★, CL-OWN, CL-UNIQ, D-MIN★, D-CTG★, D-SEQ★); and vacuous-by-frame invariants (M0, S4, S7a, S7b, S7c, S7d, C-fin, P6, P7, P8, NodeLineage). | introduced |
| M-Inv-Bdry | *Composite-boundary properties at `Σ'`.* P4★, P4a, P7a hold at `Σ'` — all preserved because `R' = R`, `dom(Σ'.C) = dom(Σ.C)`, and the new V-arrangement entry is link-subspace (so it does not enter `Contains_C(Σ')`). J0, J1★, J1'★ are vacuously satisfied (no content-subspace allocation, no content-subspace range growth). | introduced |
| M-Inv-Trans | *Transition invariants for `Σ → Σ'`.* M1, L12, P0, P1, P2, and P3 hold; S9 follows from P0. Each is discharged trivially by the frames `Σ'.C = Σ.C`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`, and L12 by K.λ adding only the fresh `ℓ`. P3 is the conjunction `P0 ∧ P1 ∧ P2 ∧ L12`. | introduced |

## Open Questions

What well-formedness constraints, beyond `e₃ ≠ ∅`, must endsets satisfy when their spans reference I-addresses not currently in `dom(C)` or `dom(L)`?

At what abstraction layer is MAKELINK's composite-level atomicity guaranteed, and what mechanism enforces it?

Must MAKELINK distinguish between two invocations producing links with identical endset values, beyond the necessary distinctness of their I-addresses?

Must MAKELINK's discoverability guarantee hold at the precise post-state of the operation, or is a deferred-consistency model admissible?

When MAKELINK's endsets reference content in documents not yet allocated, what discoverability properties become available once that content is later created?

Under what conditions may a link's V-position move within the home document's link subspace by subsequent operations, and what discoverability properties does such movement preserve?

What abstract guarantee distinguishes a "properly created" link visible in its home document's arrangement from a link allocated but not placed?

What invariants must hold for a link whose type endset references content at an address that will never be allocated, and what does discoverability mean in that limiting case?
