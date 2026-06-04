# ASN-0087: MAKELINK Operation
*2026-05-26*

## The Problem

We are looking for the precise meaning of *creating a link*. The system already maintains a content store, a family of arrangements, and a link store with prior entries. Some event introduces a new link. What does that event do?

A link, in this design, is a stored connective unit — a first-class entity binding together fragments of content. By L3 (ASN-0043) every link has at least three endsets, the third designated as type, the type slot non-empty. Beyond this, link creation must produce three things unconditionally: an *identity* (the link's address), a *value* (the endsets), and a *home* (the document under whose authority the link is allocated). It must also establish the *discoverability property* — the LP12 (ASN-0098) mechanism by which a query of the content reached by the link's endsets can surface the link.

We are careful to distinguish the property from its realization. MAKELINK brings identity, value, and home into being unconditionally, and it establishes the LP12 discoverability mechanism. Whether the link is *actually* discoverable from a given document is a separate, arrangement-conditional matter that the body characterizes. We ask: what is allocated, what is recorded, what discoverability mechanism is established, and what remains untouched?

## Inputs

What must the caller supply?

- A *home document* `d ∈ dom(Σ.M)` — the document under whose authority the link is allocated. (By L1a, ASN-0043, every link's home document must be allocated.)
- A *sequence of endsets* `(e₁, ..., eₙ)` with `N ≥ 3`, each `eᵢ ∈ Endset`, and `e₃ ≠ ∅`. (By L3, ASN-0043.)

The caller does *not* specify the link's address or its V-position in the home document — neither is an operation *parameter*. The address `ℓ` is *derived* by the system from the current state (the next emission of `A_L(d)`); the V-position `v_ℓ` is derived from the current state together with the canonical-depth convention M-DepthConv below — its serial component fixed by the link subspace's current cardinality, its depth fixed per M-DepthConv.

*Reflexive authoring and prediction.* Although `ℓ` is not a parameter, it is deterministically derivable from `Σ`: a caller authoring a *reflexive* endset (one whose coverage is to contain `ℓ` itself, per L13 and M-Reflexive) may *predict* `ℓ` by evaluating `A_L(d)`'s emission rule against the state it observes — first emission `[d, 0, s_L, 1]` when `d` has no prior links, else `inc(ℓ_prev, 0)`.

*Canonical link-subspace depth (M-DepthConv).* When `V_{s_L}(d) = ∅`, the substrate operation K.μ⁺_L (ASN-0047) admits *any* `m ≥ 2` for the first link's V-position via `ValidFirstLinkPosition(d, v_ℓ, m)`. MAKELINK commits to the *minimal admissible* depth `m = 2` for every first link *it* places. Once it has done so, S8-depth (ASN-0047) pins `m_L(d) = 2` for all later link V-positions of that document, so every subsequent `v_ℓ` MAKELINK places *is* fully state-determined. This is a scoped, normative commitment — for any document `d` whose every link V-position was placed by MAKELINK, `m_L(d) = 2` — not a system-wide invariant.

We write `dom(M)` throughout for the set of allocated documents (`dom(M) = E_doc` by M1, ArrangementMonotonicity, ASN-0047).

*Endsets and emptiness.* L3 (ASN-0043) requires the third slot `e₃` to be non-empty but imposes no non-emptiness constraint on the other slots. The empty endset `eᵢ = ∅` is a permitted boundary case for `i ≠ 3`: by the coverage definition, `coverage(∅) = ⋃_{(s,ℓ) ∈ ∅} … = ∅`, so an empty slot contributes nothing to any `project(ℓ, i, ·, ·)` and nothing to any LP12-based discoverability disjunct.

*Standard authoring.* An endset `e` is *standardly authored at state `Σ`* iff every span in `e` references addresses already in the substrate:

  StandardAuthoring(e, Σ)  ≡  coverage(e) ⊆ dom(Σ.C) ∪ dom(Σ.L)

A link's input endset sequence `(e₁, ..., eₙ)` is standardly authored at `Σ` iff `StandardAuthoring(eᵢ, Σ)` holds for every `i ∈ {1, ..., N}`. The discipline rules out forward-reaching endsets that pre-emptively cover not-yet-allocated addresses.

## Decomposition

We observe that link creation must accomplish two distinct effects: (i) introduce the link into `dom(L)` with its value recorded, and (ii) make the link visible in the home document's arrangement. The substrate (ASN-0093, ASN-0047) provides exactly two atomic operations matching this division:

- `K.λ` allocates the link in `dom(L)`, binding it to the given endsets.
- `K.μ⁺_L` extends `M(d)` in the link subspace — where links live in V-space (L14a's supersession, ASN-0047) — mapping a fresh V-position to the link.

We therefore identify MAKELINK as the composite `K.λ ; K.μ⁺_L` — K.λ followed by K.μ⁺_L — applied to the same home document. The semicolon denotes sequential composition of atomic transitions. The order is forced: K.μ⁺_L's precondition requires `ℓ ∈ dom(L)`, so K.λ must precede it.

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
  subspace(v_ℓ) = s_L          [by construction: (v_ℓ)₁ = s_L]
  #v_ℓ per M-DepthConv        [depth fixed per M-DepthConv: m = 2 when V_{s_L}(d) = ∅, else the existing m_L(d)]
  v_ℓ at the next link-subspace position per D-MIN★ / D-CTG★

The condition `ℓ ∉ ran(Σ_mid.M(d))` requires more than `ℓ ∉ dom(Σ.L)`; it must be derived through the S3★ + S3★-aux + K.λ freshness chain. K.λ's frame preserves `M`, so `Σ_mid.M(d) = Σ.M(d)` and `ran(Σ_mid.M(d)) = ran(Σ.M(d))`. By S3★-aux (ASN-0047), every `v ∈ dom(Σ.M(d))` has `subspace(v) ∈ {s_C, s_L}`. By S3★:

- If `subspace(v) = s_C`, then `Σ.M(d)(v) ∈ dom(Σ.C)`.
- If `subspace(v) = s_L`, then `Σ.M(d)(v) ∈ dom(Σ.L)`.

K.λ's freshness precondition gives `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)`. In either subspace case, `Σ.M(d)(v) ∈ dom(Σ.C) ∪ dom(Σ.L)`, so `Σ.M(d)(v) ≠ ℓ`. Hence `ℓ ∉ ran(Σ.M(d)) = ran(Σ_mid.M(d))`.

The intermediate-state conditions for K.μ⁺_L reduce to original-state conditions, so the caller-visible precondition for MAKELINK is just K.λ's precondition, with `ℓ` supplied by `A_L(d)`'s next emission and `v_ℓ` determined by the link subspace's current cardinality (serial component `n_L + 1`, where `n_L = |V_{s_L}(d)|`) together with its depth per M-DepthConv.

## Effect

We summarize the composite state transition. Writing the post-state as `Σ'`:

  Σ'.L  =  Σ.L ∪ {ℓ ↦ (e₁, ..., eₙ)}
  Σ'.M(d)  =  Σ.M(d) ∪ {v_ℓ ↦ ℓ}

where `v_ℓ` is determined by `Σ.M(d)`'s link subspace, via K.μ⁺_L's positioning rule (ASN-0047):

  v_ℓ  =  [s_L, 1]                             if V_{s_L}(d) = ∅ at Σ  (depth per M-DepthConv)
  v_ℓ  =  shift(max(V_{s_L}(d)), 1)             otherwise  (depth m_L(d), the existing link-subspace depth)

The depth follows M-DepthConv throughout. By D-SEQ★ (ASN-0047), `V_{s_L}(d) = {[s_L, 1, ..., 1, k] : 1 ≤ k ≤ n_L}` of common depth `m_L(d)` when non-empty (with `n_L = |V_{s_L}(d)|`), so the non-empty case yields `v_ℓ = shift(max(V_{s_L}(d)), 1) = [s_L, 1, ..., 1, n_L + 1]` at that same depth `m_L(d)`.

Whenever MAKELINK is the placing operation the caller never supplies `v_ℓ`: in the non-empty case it is computed from `Σ` (the link subspace's current cardinality at the recorded depth `m_L(d)`), and in the empty (first-link) case its serial component is computed from `Σ` (cardinality 0, giving serial 1) while its depth is supplied by M-DepthConv.

Other components are unchanged:

  Σ'.C  =  Σ.C
  Σ'.E  =  Σ.E                                          [no entity allocation]
  Σ'.R  =  Σ.R                                          [provenance applies to content subspace only]
  (A ℓ' ∈ dom(Σ.L) :: Σ'.L(ℓ') = Σ.L(ℓ'))               [L12]
  (A d' ∈ dom(Σ.M), d' ≠ d :: Σ'.M(d') = Σ.M(d'))

## Freshness of the Allocation

The address `ℓ` is genuinely new — `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)` at `Σ` — so K.λ's freshness precondition is met by construction. By FirstEmissionFreshness and SubsequentEmissionFreshness (ASN-0093), every emission of `A_L(d)` is fresh against `dom(Σ.C) ∪ dom(Σ.L)`:

- *First-emission case* (`{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d} = ∅`): FirstEmissionFreshness (ASN-0093) gives `ℓ = [d, 0, s_L, 1] ∉ dom(Σ.L) ∪ dom(Σ.C)`.
- *Subsequent-emission case* (`ℓ = inc(ℓ_prev, 0)`): SubsequentEmissionFreshness (ASN-0093) gives `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)`. That lemma's own three-way split discharges within-document freshness (via ChainEnumerationInjectivity), cross-subspace freshness (via DisjointSubAllocatorChains and SC-NEQ), and cross-document freshness (via Cross-doc disjointness composed with T10, PartitionIndependence, ASN-0034).

The freshness of the V-position `v_ℓ` in `dom(M(d))` is established where it is consumed, in the S2 verification of the post-state invariants.

## Permanence of the Recording

The endset sequence `Σ'.L(ℓ) = (e₁, ..., eₙ)` is permanently fixed. We assemble three guarantees:

- By L12 (ASN-0093/ASN-0043), no transition modifies `L(ℓ)` once set.
- By LP13 (ASN-0098), for every reachable state sequence `Σ' →* Σ''`: `ℓ ∈ dom(Σ''.L) ∧ Σ''.L(ℓ) = Σ'.L(ℓ)`, hence in particular `Σ''.L(ℓ).eᵢ = Σ'.L(ℓ).eᵢ` for every slot `i`.
- By LP3★ (ASN-0098), for every such sequence and every slot: `coverage(Σ''.L(ℓ).eᵢ) = coverage(Σ'.L(ℓ).eᵢ)`.

The implication is that once recorded, the endsets' *addressing intent* is permanent. The link forever names the same set of I-addresses — even as those I-addresses' V-arrangements change, even if all V-arrangements lose them entirely, even if new documents transclude content sharing those I-addresses (in which case LP18 makes the link rediscoverable from those new documents).

## What Is Indexed?

We are looking for the discovery guarantee — the property that a future query "what links touch this content?" surfaces `ℓ` whenever the query's content lies in any of `ℓ`'s endset coverages.

The discovery function `discoverable_from(ℓ, d, Σ')` is defined in ASN-0098:

  project(ℓ, i, d, Σ')  =  {v ∈ dom(Σ'.M(d)) : Σ'.M(d)(v) ∈ coverage(Σ'.L(ℓ).eᵢ)}
  discoverable_from(ℓ, d, Σ')  ≡  (E i :: project(ℓ, i, d, Σ') ≠ ∅)

The function is *computed* from `Σ'.L(ℓ)` and `Σ'.M(d)` — no separate state component is required. By LP12 (ASN-0098):

  discoverable_from(ℓ, d, Σ')  ⟺  (E i : coverage(Σ'.L(ℓ).eᵢ) ∩ ran(Σ'.M(d)) ≠ ∅)

After MAKELINK, this biconditional holds at the post-state for every `d ∈ dom(Σ'.M)`. We state the resulting symmetry property once here (M-DiscSymmetry). LP12's definition treats every document uniformly — the home document has no privileged status *in the discovery function itself*. For the *standard content-reach route* (an endset coverage meeting a document's arrangement range), discoverability is therefore symmetric: `ℓ` is discoverable from every document whose arrangement reaches into any of its endset coverages, realizing Nelson's intent that all parties reaching a link's endpoints discover it by querying their own content. (The home document alone gains an additional, arrangement-independent reflexive route; we derive it once, in *Weakest Precondition for Discoverability*, Case 2.)

The abstract specification requires no auxiliary index state (M-NoIndexState). An implementation may maintain an auxiliary structure — a reverse lookup from I-addresses to link addresses, the *spanfilade* in Gregory's implementation — for efficient computation. Such structures are caches: any state where they are consistent with `L` and `M` produces the same `project` and `discoverable_from` results. The abstract claim is the discovery *property*; the index is a performance choice.

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
- `v_ℓ = [s_L, 1] = [2, 1]`, the first link V-position (`V_{s_L}(d) = ∅` at `Σ`), depth per M-DepthConv.

Post-state `Σ'`:

- `dom(Σ'.L) = {ℓ}` with `Σ'.L(ℓ) = (e₁, e₂, e₃)`.
- `Σ'.M(d) = {[1, 1] ↦ a₁, [1, 2] ↦ a₂, [2, 1] ↦ ℓ}`.
- `Σ'.M(d') = {[1, 1] ↦ a₃}` (unchanged by frame).
- `Σ'.C = Σ.C`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`.

Discoverability checks via LP12:

- `discoverable_from(ℓ, d, Σ')`: `ran(Σ'.M(d)) = {a₁, a₂, ℓ}`. We compute `coverage(e₁) ∩ ran(Σ'.M(d)) = {t : a₁ ≼ t} ∩ {a₁, a₂, ℓ}` by prefix-testing each element of `ran(Σ'.M(d))` against `a₁`. With `a₁ = [1, 0, 1, 0, 1, 0, 1, 1]`, `a₂ = [1, 0, 1, 0, 1, 0, 1, 2]`, and `ℓ = [1, 0, 1, 0, 1, 0, 2, 1]` (all of length 8): `a₁ ≼ a₁` trivially; `a₁ ⋠ a₂` since the two have equal length and disagree at position 8 (`1 ≠ 2`); `a₁ ⋠ ℓ` since the two have equal length and disagree at position 7 (`1 ≠ 2`). The intersection is `{a₁} ≠ ∅`. Hence `ℓ` is discoverable from its home document `d` via slot 1 — `d`'s arrangement reaches `a₁`, which `e₁` covers.

- `discoverable_from(ℓ, d', Σ')`: `ran(Σ'.M(d')) = {a₃}`. Prefix-testing `a₃ ≼ a₃` holds trivially, so `coverage(e₂) ∩ ran(Σ'.M(d')) = {t : a₃ ≼ t} ∩ {a₃} = {a₃} ≠ ∅`. Hence `ℓ` is discoverable from `d'` via slot 2 — and discovery from `d'` does not consult `Σ'.M(d)`.

The type-endset coverage `coverage(e₃) = {t : τ ≼ t}` does not contribute to discoverability from either `d` or `d'` in this state: by the setup's constraint that `τ ⋠ x` for every `x ∈ {a₁, a₂, a₃, ℓ}`, prefix-testing each element of `ran(Σ'.M(d)) = {a₁, a₂, ℓ}` and `ran(Σ'.M(d')) = {a₃}` against `τ` yields no matches. Hence `coverage(e₃) ∩ ran(Σ'.M(d)) = ∅` and `coverage(e₃) ∩ ran(Σ'.M(d')) = ∅`. This is consistent with the type endset's role: it carries the link's classification, not its content connections.

*Reflexive variant.* We instantiate M-Reflexive concretely. Replace `e₁` with `e₁' = {(ℓ, δ(1, #ℓ))}`, keeping `e₂` and `e₃` (the caller must *predict* `ℓ = [d, 0, 2, 1]` from `Σ` via `A_L(d)`'s deterministic first-emission rule — see the note on reflexive authoring in *Inputs*). By PrefixSpanCoverage (ASN-0043), `coverage(e₁') = {t ∈ T : ℓ ≼ t}`, which contains `ℓ`. The M-Reflexive hypothesis `ℓ ∈ coverage(e₁')` is thus met, so wp Case 2's reflexive disjunct fires: `discoverable_from(ℓ, d, Σ')` holds with witness `v_ℓ ∈ project(ℓ, 1, d, Σ')`, regardless of `d`'s prior arrangement.

## Weakest Precondition for Discoverability

We compute `wp(MAKELINK, discoverable_from(ℓ, d_target, ·))` — the predicate on the pre-state `Σ` (parametrized by the input endsets `(e₁, ..., eₙ)` and the choice of `d_target`) that ensures the post-state satisfies `discoverable_from(ℓ, d_target, Σ')`.

*Operation enabledness.* Following the foundation's wp convention (LP12a, ASN-0098), wp is written `enabled(op) ∧ …` for total correctness. For MAKELINK the applicability predicate is the caller-visible precondition M-Pre:

  enabled(MAKELINK)  ≡  d ∈ dom(Σ.M)  ∧  N ≥ 3  ∧  (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset)  ∧  e₃ ≠ ∅

The predicate concerns the *home* document `d` and the endset inputs, and is logically independent of the target document `d_target`.

*Membership precondition.* `discoverable_from(a, d, Σ)` is defined in ASN-0098 only when `a ∈ dom(Σ.L) ∧ d ∈ dom(Σ.M)`. At the post-state, `ℓ ∈ dom(Σ'.L)` by K.λ's effect, so the left conjunct is automatic. The right conjunct `d_target ∈ dom(Σ'.M)` requires that the target document was already registered at the pre-state. M1 (ASN-0093) supplies only the inclusion `dom(Σ.M) ⊆ dom(Σ'.M)`; equality `dom(Σ'.M) = dom(Σ.M)` at MAKELINK comes from the K.λ frame and K.μ⁺_L's effect, neither of which extends `dom(M)` (K.λ's frame holds `M` entirely fixed; K.μ⁺_L extends `dom(M(d))` for an already-registered `d` without adding any new document). Combining the M1 inclusion with these two frame consequences gives the equality, so `d_target ∈ dom(Σ'.M) ⟺ d_target ∈ dom(Σ.M)`. This membership clause keeps `discoverable_from` *defined* at the post-state; it is distinct from `enabled(MAKELINK)`, which keeps the post-state from existing at all. For `d_target = d` the membership clause is subsumed by `enabled(MAKELINK)`'s `d ∈ dom(Σ.M)` conjunct; for `d_target ≠ d` it is an independent obligation.

*Case 1: d_target ≠ d.* K.μ⁺_L's frame gives `Σ'.M(d_target) = Σ.M(d_target)` for every `d_target ≠ d` in `dom(Σ'.M)`. By LP12 at `Σ'`:

  discoverable_from(ℓ, d_target, Σ')
    ⟺  (E i :: coverage(Σ'.L(ℓ).eᵢ) ∩ ran(Σ'.M(d_target)) ≠ ∅)
    ⟺  (E i :: coverage(eᵢ) ∩ ran(Σ.M(d_target)) ≠ ∅)

The wp reduces to a predicate on the pre-state alone, conjoined with MAKELINK's enabledness and the membership clause that keeps `discoverable_from` defined at the post-state:

  wp(MAKELINK, discoverable_from(ℓ, d_target, ·))
    ≡  enabled(MAKELINK)  ∧  d_target ∈ dom(Σ.M)  ∧  (E i :: coverage(eᵢ) ∩ ran(Σ.M(d_target)) ≠ ∅)

The allocation of `ℓ` contributes nothing to discoverability from documents other than `d`; the predicate this case adds is the independent membership obligation `d_target ∈ dom(Σ.M)` that keeps `discoverable_from` defined at the post-state.

*Case 2: d_target = d.* The post-state arrangement gains `ℓ`: `ran(Σ'.M(d)) = ran(Σ.M(d)) ∪ {ℓ}`. By LP12:

  discoverable_from(ℓ, d, Σ')
    ⟺  (E i :: coverage(eᵢ) ∩ (ran(Σ.M(d)) ∪ {ℓ}) ≠ ∅)
    ⟺  (E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)  ∨  (E i :: ℓ ∈ coverage(eᵢ))

The disjunction isolates two routes to home-document discoverability:

- (i) *Arrangement-reach route:* some endset's coverage intersects `d`'s pre-existing arrangement range.
- (ii) *Reflexive route:* some endset's coverage contains `ℓ` itself.

L13 (ReflexiveAddressing, ASN-0043) permits a link's endsets to cover link addresses, including the link's own address, so route (ii) is admissible. When its disjunct holds it is forced by the post-state witness `v_ℓ ↦ ℓ`: if `ℓ ∈ coverage(eᵢ)` for some `i`, then since `Σ'.L(ℓ).eᵢ = eᵢ` (K.λ's effect, K.μ⁺_L's frame on `L`) and `Σ'.M(d)(v_ℓ) = ℓ`, we have `v_ℓ ∈ project(ℓ, i, d, Σ')`, so `discoverable_from(ℓ, d, Σ')` holds regardless of `Σ.M(d)`'s pre-existing arrangement (M-Reflexive). Because `ℓ` enters only `d`'s arrangement, this route is available to the home document alone — Case 1 already shows other documents gain nothing from the allocation of `ℓ`.

As a wp (the membership clause subsumed by `enabled(MAKELINK)` here, since `d_target = d`):

  wp(MAKELINK, discoverable_from(ℓ, d, ·))
    ≡  enabled(MAKELINK)  ∧  [(E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅) ∨ (E i :: ℓ ∈ coverage(eᵢ))]

*Reduction under standard authoring.* When every input endset satisfies `StandardAuthoring(eᵢ, Σ)`, K.λ's freshness gives `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)` while standard authoring confines every `coverage(eᵢ)` to `dom(Σ.C) ∪ dom(Σ.L)`, so `ℓ ∉ coverage(eᵢ)` for every `i` — the reflexive route's disjunct `(E i :: ℓ ∈ coverage(eᵢ))` is unreachable (M-Reflexive). The wp collapses:

  wp(MAKELINK, discoverable_from(ℓ, d, ·))
    ≡  enabled(MAKELINK)  ∧  (E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)

— the same shape as Case 1 (with `d_target := d`; the two enabledness-and-membership conjuncts coincide there into `enabled(MAKELINK)`, since the home and target documents are one). Under standard authoring, home-document discoverability requires `d`'s arrangement to reach into some endset's coverage; there is no automatic "self-discovery" of `ℓ` from `d` (M-DiscSymmetry).

## What Does Not Change

The frame `Σ'.C = Σ.C` is total: every `a ∈ dom(Σ.C)` satisfies `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`. The referenced content is byte-identical before and after MAKELINK.

This is not a separate guarantee. It is a direct consequence of the composite's structure: K.λ modifies only `L`, and K.μ⁺_L modifies only `M(d)`. Neither operation touches `C`. The link's endsets *reference* I-addresses in `dom(C)`, but referencing is read-only — the endset stores spans (start, length pairs), not the bytes at those addresses. The bytes remain where they were.

By the same reasoning, no prior link in `dom(L)` is modified (L12), no other document's arrangement is modified (frame on `M`), no entity is allocated, no provenance pair is recorded.

That creating a link has zero effect on referenced content — Nelson's phenomenology — is structural, not behavioral: the link's storage lies in the home document's element subspace, which by construction cannot modify content at I-addresses elsewhere.

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

The side effect can only occur when `ℓ'` was authored with an endset whose span coverage extends to addresses not yet allocated at authoring time. Such forward-reaching endsets are permitted by L4 (EndsetGenerality, ASN-0043) — endset spans may reference any addresses in the tumbler space, including those not currently in `dom(C) ∪ dom(L)`. MAKELINK's allocation of `ℓ` "fills in" a previously-uncovered region of the address space, retroactively activating any prior endset that had pre-emptively claimed it. When `ℓ'` was authored under standard authoring at its own authoring state — `StandardAuthoring(Σ.L(ℓ').eᵢ, Σ_{ℓ'})` holds at the state `Σ_{ℓ'}` at which `ℓ'` was incorporated, so `coverage(Σ.L(ℓ').eᵢ) ⊆ dom(Σ_{ℓ'}.C) ∪ dom(Σ_{ℓ'}.L)` — no such endset can cover the future fresh `ℓ`, and the side effect is vacuous. The transfer of `ℓ`'s freshness backward from the K.λ allocation state `Σ_ℓ` to the authoring state `Σ_{ℓ'}` (where `Σ_{ℓ'} →* Σ_ℓ`) uses Store Monotonicity★ (ASN-0098): `dom(Σ_{ℓ'}.C) ∪ dom(Σ_{ℓ'}.L) ⊆ dom(Σ_ℓ.C) ∪ dom(Σ_ℓ.L)`, so K.λ's freshness `ℓ ∉ dom(Σ_ℓ.C) ∪ dom(Σ_ℓ.L)` yields `ℓ ∉ dom(Σ_{ℓ'}.C) ∪ dom(Σ_{ℓ'}.L)`; chaining with the standard-authoring inclusion at `Σ_{ℓ'}` gives `ℓ ∉ coverage(Σ.L(ℓ').eᵢ)`.

The biconditional above is stated for `d` because, by M-PriorLinkDisc, `d` is the only document whose prior-link discoverability MAKELINK can change; for any `d_target ≠ d` the arrangement is frame-preserved and prior-link discoverability is unchanged, so the side-effect window is confined to the home document.

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

L1c (structural inc-chain conformance) requires an inc-chain from `origin(ℓ) = d` to `ℓ`. K.λ's precondition supplies it directly: `ℓ` is produced by `A_L(d)`, so by ChainDiscipline (ASN-0093) `ℓ` lies on `d`'s link sub-allocator chain `A_L(d) = S(b_L(d), 1)`, whose elements are exactly the inc-chain emissions; ChainElementT4Validity carries T4-validity along it, and the `k₁ = 2`, `#tᵢ > #origin(ℓ)` clauses are part of ASN-0093's L1c statement. ✓

For the V-arrangement entry `v_ℓ ↦ ℓ`:

  S2:       M'(d) remains a partial function                      v_ℓ ∉ dom(Σ.M(d)) by the two-part argument below; v_ℓ enters dom(M'(d)) fresh, preserving functionality of M'(d)
  S3★:      image of v_ℓ is ℓ ∈ dom(L'), subspace(v_ℓ) = s_L     direct from the effect
  S3★-aux:  subspace(v_ℓ) = s_L ∈ {s_C, s_L}                      direct from the effect
  S8a:      zeros(v_ℓ) = 0, #v_ℓ = m_L(d) ≥ 2, components all > 0  v_ℓ = [s_L, 1, ..., 1, k] with s_L = 2 > 0, all components ≥ 1
  S8-depth: depth uniformity in subspace s_L at d                 common depth m_L(d) for all V-positions in V_{s_L}(d); v_ℓ's depth per M-DepthConv
  S8-fin:   |dom(M'(d))| = |dom(M(d))| + 1                       S8-fin at Σ gives finiteness of the predecessor
  S8★:      per-subspace span decomposition                       link subspace admits trivial length-1 decomposition (see below)
  CL-OWN:   origin(M'(d)(v_ℓ)) = origin(ℓ) = d                   direct from K.λ precondition
  CL-UNIQ:  partial injection preserved                           K.μ⁺_L first-arrangement guard ℓ ∉ ran(M_mid(d))
  D-MIN★:   v_ℓ at minimum if empty                               K.μ⁺_L positioning rule (depth m_L(d))
  D-CTG★:   extension is contiguous                               K.μ⁺_L positioning rule
  D-SEQ★:   V_{s_L}(d') is contiguous initial segment             see below

For S2: we must show `v_ℓ ∉ dom(Σ.M(d))`, not merely `v_ℓ ∉ V_{s_L}(d)`. By S3★-aux at `Σ`, `dom(Σ.M(d)) = V_{s_C}(d) ∪ V_{s_L}(d)`, so the obligation splits into two exclusions:
- *Within-subspace exclusion:* `v_ℓ ∉ V_{s_L}(d)`. By D-SEQ★ at `Σ`, `V_{s_L}(d) = {[s_L, 1, ..., 1, k] : 1 ≤ k ≤ n_L}` at the common depth `m_L(d)`; K.μ⁺_L's positioning rule sets `v_ℓ = [s_L, 1, ..., 1, n_L + 1]` (or, when `n_L = 0`, the chosen first position `[s_L, 1, ..., 1]`), which lies outside this set by the strict inequality `n_L + 1 > n_L` (resp. by the emptiness of the set when `n_L = 0`).
- *Cross-subspace exclusion:* `v_ℓ ∉ V_{s_C}(d)`. By construction `(v_ℓ)₁ = s_L`, while by S8a every `v ∈ V_{s_C}(d)` has `(v)₁ = s_C`. By SC-NEQ (ASN-0093), `s_L ≠ s_C`, so `v_ℓ ≠ v` for every `v ∈ V_{s_C}(d)`.

Combining the two exclusions, `v_ℓ ∉ V_{s_C}(d) ∪ V_{s_L}(d) = dom(Σ.M(d))`, discharging S2. ✓

For D-SEQ★: by D-SEQ★ at `Σ`, `V_{s_L}(d) = {[s_L, 1, ..., 1, k] : 1 ≤ k ≤ n_L}` of common depth `m_L(d)` for some `n_L ≥ 0` (with `n_L = 0` meaning the link subspace at `d` is empty). If `n_L = 0`, MAKELINK commits the minimal depth per M-DepthConv: the K.μ⁺_L positioning rule gives `v_ℓ = [s_L, 1]` at depth 2, so `V_{s_L}(d') = {v_ℓ}` — a contiguous initial segment of cardinality 1, fixing `m_L(d') = 2`. If `n_L ≥ 1`, the rule gives `v_ℓ = shift(max(V_{s_L}(d)), 1) = [s_L, 1, ..., 1, n_L + 1]` at depth `m_L(d)`, so `V_{s_L}(d') = {[s_L, 1, ..., 1, k] : 1 ≤ k ≤ n_L + 1}` — a contiguous initial segment of cardinality `n_L + 1`. Either way, the post-state set conforms to D-SEQ★. ✓

For S8★: per ASN-0047's S8★, the link-subspace projected arrangement `M'(d)|_{V_{s_L}(d')} : V_{s_L}(d') → dom(L')` admits the trivial length-1 decomposition `{(v, M'(d)(v), 1) : v ∈ V_{s_L}(d')}`. The new entry `(v_ℓ, ℓ, 1)` joins this decomposition; S8's conditions (a) and (b) hold trivially at length 1. ✓

Every invariant quantifying solely over `C`, `E`, `R`, or the document set `dom(M)` — all frame-fixed at MAKELINK (`Σ'.C = Σ.C`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`, `dom(Σ'.M) = dom(Σ.M)`, since MAKELINK allocates no new document and only adds a V-position within an already-allocated one) — is preserved by inheritance: S4, S7a, S7b, C1b, C1c, C-fin, P6, P7, P8, M0, NodeLineage, ActivatedEmission.

- S7d (DocumentAllocationDiscipline, ASN-0036): document set unchanged (`dom(Σ'.M) = dom(Σ.M)`); preserved by inheritance.
- L11a (link uniqueness, ASN-0043): the new allocation event for `ℓ` is distinct from every prior link allocation event (by ChainEnumerationInjectivity, DisjointSubAllocatorChains, and Cross-doc disjointness — see "Freshness of the Allocation"), so L11a's distinctness conclusion holds at `Σ'`.

### Composite-Boundary Properties

ASN-0047 classifies P4★, P4a, and P7a as Class (b) — properties discharged at composite boundaries by the coupling constraints J0, J1★, J1'★. MAKELINK introduces a single link-subspace V-arrangement entry. The three coupling constraints are vacuously satisfied — but for *structurally distinct* reasons, which we discharge separately:

- *J0 (AllocationPlacementCoupling):* J0 quantifies over `dom(Σ'.C) ∖ dom(Σ.C)` — content addresses freshly allocated across the composite. MAKELINK's frame `Σ'.C = Σ.C` gives `dom(Σ'.C) ∖ dom(Σ.C) = ∅`. J0 holds by emptiness of the quantification universe.
- *J1★ (ExtensionRecordsProvenance):* J1★ quantifies over content-subspace V-positions whose image changes across the composite. The only new V-position is `v_ℓ` with `subspace(v_ℓ) = s_L`, and `s_L ≠ s_C` (SC-NEQ, ASN-0093). For every `v ∈ dom(Σ.M(d))`, `Σ'.M(d)(v) = Σ.M(d)(v)` by K.μ⁺_L's effect, so no prior V-position's image changed. The quantification `(E v ∈ dom(Σ'.M(d)) : subspace(v) = s_C ∧ Σ'.M(d)(v) = a) ∧ ¬(E v ∈ dom(Σ.M(d)) : subspace(v) = s_C ∧ Σ.M(d)(v) = a)` requires a *new* content-subspace witness; none exists, since `v_ℓ`'s subspace is `s_L`. J1★ holds by absence of content-subspace witnesses.
- *J1'★ (ProvenanceRequiresExtension):* J1'★ quantifies over `R' ∖ R`. MAKELINK's frame `Σ'.R = Σ.R` gives `R' ∖ R = ∅`. J1'★ holds by emptiness of the quantification universe.

- P4★ (ProvenanceBounds): `Contains_C(Σ') ⊆ R'`. The new V-arrangement entry `v_ℓ ↦ ℓ` has `subspace(v_ℓ) = s_L`, so it does not contribute to `Contains_C(Σ')`. Hence `Contains_C(Σ') = Contains_C(Σ) ⊆ R = R'`.
- P4a (TraceWitnessing): for every `(a, d') ∈ R'`, some prior state `Σ_k` in the transition history had `M_k(d')(v) = a` with `subspace(v) = s_C`. Since `R' = R`, the obligation is identical to P4a at `Σ`, which holds by the reachability hypothesis on `Σ`.
- P7a (ProvenanceCoverage): for every `a ∈ dom(Σ'.C)`, some `d'` satisfies `(a, d') ∈ R'`. Since `dom(Σ'.C) = dom(Σ.C)` and `R' = R`, the obligation is identical to P7a at `Σ`, which holds by reachability.

### Transition Invariants for Σ → Σ'

- M1 (ArrangementMonotonicity, ASN-0093): `dom(Σ.M) ⊆ dom(Σ'.M)`. Trivially holds with equality — MAKELINK does not extend `dom(M)`.
- L12 (LinkImmutability): `(A ℓ' ∈ dom(Σ.L) :: ℓ' ∈ dom(Σ'.L) ∧ Σ'.L(ℓ') = Σ.L(ℓ'))`. K.λ adds only the fresh `ℓ`; no prior entry is modified.
- P0 (ContentPermanence): trivially via the frame `Σ'.C = Σ.C`.
- P1 (EntityPermanence): trivially via the frame `Σ'.E = Σ.E`.
- P2 (ProvenancePermanence): trivially via the frame `Σ'.R = Σ.R`.
- P3 (ArrangementMutabilityOnly): the conjunction P0 ∧ P1 ∧ P2 ∧ L12, already discharged above clause-by-clause. P3 holds at MAKELINK.

## Atomicity

MAKELINK is a *composite* of two atomic transitions. Each component is atomic by SequentialTransitionAxiom (ASN-0093). The composite is not.

In the intermediate state `Σ_mid` between K.λ and K.μ⁺_L:

- `ℓ ∈ dom(Σ_mid.L)` with value `Σ_mid.L(ℓ) = (e₁, ..., eₙ)` — the link exists, with its endsets recorded.
- `ℓ ∉ ran(Σ_mid.M(d))` — the link is not yet visible in any V-arrangement (derived in Preconditions).
- `discoverable_from(ℓ, d_target, Σ_mid)` is well-defined for every `d_target ∈ dom(Σ_mid.M) = dom(Σ.M)` since `ℓ ∈ dom(Σ_mid.L)` and `Σ_mid.L(ℓ) = (e₁, ..., eₙ)`.

`Σ_mid` is a fully reachable state, not a transitional artifact: by SequentialTransitionAxiom (ASN-0093), K.λ commits before K.μ⁺_L begins, so K.λ on `Σ` yields a complete state `Σ_mid` against which K.μ⁺_L's precondition is evaluated. K.λ is an atomic substrate operation that ASN-0093/ASN-0047 establish to preserve the per-state invariants on reachable states, so `Σ_mid` inherits them.

Because K.λ's frame fixes `M`, `Σ_mid.M = Σ.M`, so the discoverability difference between `Σ_mid` and `Σ'` is exactly the `Σ → Σ'` delta already computed: it agrees for every `d_target ≠ d` (M-WP, Case 1), and for `d_target = d` the two values agree unless some endset reflexively covers `ℓ` (M-Reflexive).

The substrate provides no composite-level atomicity. A reader observing `Σ_mid` would see the link in `dom(L)` but not in `M(d)`. If this intermediate visibility is undesirable — if MAKELINK must appear as a single event — the protocol layer above must enforce it, typically by sequencing both atomic transitions within a single request-response cycle. Composite-level atomicity is thus a protocol-layer guarantee, not a substrate-level one.

## Permanence

*Permanence of the Recording* established that the link's identity and value are permanent. What remains to characterize is the V-position binding `v_ℓ ↦ ℓ` in the home document, which is less permanent — but the *only* mutation available to it is removal. K.μ~ (reordering) cannot rebind it: by K.μ~'s admissibility clause (v), *link-subspace fixing* (ASN-0047), the witnessing bijection satisfies `π(v) = v` for every link-subspace V-position `v ∈ dom_L(M(d))`. Since `v_ℓ` is a link V-position, `π(v_ℓ) = v_ℓ`, and the bijection equation gives `M'(d)(v_ℓ) = M(d)(v_ℓ) = ℓ`; the binding `v_ℓ ↦ ℓ` is therefore *invariant* under every K.μ~ transition. The link subspace is fixed pointwise by reordering. The sole operation that can alter the binding is K.μ⁻ (contraction), which may drop `v_ℓ` from `dom(M(d))` entirely. Thus what is permanent is the link's I-address and value; what is mutable — and only by removal, never by re-binding — is whether `v_ℓ ↦ ℓ` remains present in the home document's link-subspace arrangement.

Even if `v_ℓ` is later removed from `dom(M(d))`, the link is still in `dom(L)` and still discoverable when conditions warrant. By LP17 (ASN-0098), a link orphaned from all V-arrangements remains in the store; by LP18, it becomes discoverable again when any document later transcludes content covered by its endsets.

## No Permission Check

MAKELINK performs *no permission check on referenced content*. It does not verify ownership of the documents whose content the endsets reach; no precondition consults any ownership or permission state, and the substrate exposes no such state to consult.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| M-Comp | MAKELINK is the composite `K.λ ; K.μ⁺_L` — K.λ followed by K.μ⁺_L — applied to the same home document `d`. The semicolon denotes sequential composition of atomic transitions. | introduced |
| M-DepthConv | MAKELINK fixes every first link's V-position depth at the canonical minimal `m = 2`; thereafter S8-depth pins `m_L(d) = 2`. Stated and scoped in *Inputs*. | introduced |
| M-Pre | Caller-visible precondition: `d ∈ dom(M)`, `N ≥ 3`, `(A i : eᵢ ∈ Endset)`, `e₃ ≠ ∅`. System-supplied parameters: `ℓ` from `A_L(d)`'s next emission; `v_ℓ` from K.μ⁺_L's positioning rule, serial component `n_L + 1` computed from `Σ`, depth per M-DepthConv. | introduced |
| M-Alloc | MAKELINK allocates a fresh `ℓ ∈ T \ (dom(Σ.L) ∪ dom(Σ.C))` and a fresh `v_ℓ ∈ T \ dom(Σ.M(d))` with `subspace(v_ℓ) = s_L` and `#v_ℓ` per M-DepthConv. | introduced |
| M-Effect | `Σ'.L = Σ.L ∪ {ℓ ↦ (e₁, ..., eₙ)}`; `Σ'.M(d) = Σ.M(d) ∪ {v_ℓ ↦ ℓ}` where `v_ℓ = [s_L, 1]` if `V_{s_L}(d) = ∅` at `Σ`, else `v_ℓ = shift(max(V_{s_L}(d)), 1)` (with `n_L = |V_{s_L}(d)|`); depth per M-DepthConv. | introduced |
| M-Frame | `Σ'.C = Σ.C`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`; existing entries in `L` and in `M(d')` for `d' ≠ d` are unchanged. | introduced |
| M-NoContentEffect | For every `a ∈ dom(Σ.C)`: `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`. The referenced content is byte-identical before and after MAKELINK. | introduced |
| M-DiscSymmetry | For the standard content-reach route, discoverability of `ℓ` is symmetric across all documents whose arrangements reach into an endset coverage — LP12 grants the home document no privileged status. The reflexive route is the home document's alone, since MAKELINK places `ℓ` into its arrangement and no other. Stated and reconciled in *What Is Indexed?*. | introduced |
| StandardAuthoring | `StandardAuthoring(e, Σ) ≡ coverage(e) ⊆ dom(Σ.C) ∪ dom(Σ.L)` — a structural predicate on endset values at a state. A link's endset sequence is standardly authored at `Σ` iff every constituent endset satisfies the predicate. | introduced |
| M-Reflexive | If `ℓ ∈ coverage(eᵢ)` for some `i` (the reflexive endset case), then `v_ℓ ∈ project(ℓ, i, d, Σ')` and `discoverable_from(ℓ, d, Σ')` is forced true regardless of `Σ.M(d)`'s pre-existing arrangement. Under `(A i : StandardAuthoring(eᵢ, Σ))` the reflexive case is structurally excluded (derivation in *Weakest Precondition for Discoverability*, Case 2). | introduced |
| M-PriorLinkDisc | For every prior link `ℓ' ∈ dom(Σ.L)`: from the home document `d`, `discoverable_from(ℓ', d, Σ') ⟺ discoverable_from(ℓ', d, Σ) ∨ (E i :: ℓ ∈ coverage(Σ.L(ℓ').eᵢ))` — newly discoverable precisely when some endset of `ℓ'` covers `ℓ`; from any `d_target ≠ d`, `discoverable_from(ℓ', d_target, Σ') = discoverable_from(ℓ', d_target, Σ)`. The side-effect window is confined to the home document. | introduced |
| M-WP | Post-MAKELINK discoverability has explicit weakest preconditions (total correctness): for `d_target ≠ d`, `wp ≡ enabled(MAKELINK) ∧ d_target ∈ dom(Σ.M) ∧ (E i :: coverage(eᵢ) ∩ ran(Σ.M(d_target)) ≠ ∅)`; for `d_target = d`, `wp ≡ enabled(MAKELINK) ∧ [(E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅) ∨ (E i :: ℓ ∈ coverage(eᵢ))]`. Under `(A i : StandardAuthoring(eᵢ, Σ))` the reflexive disjunct collapses and the two shapes coincide. | introduced |
| M-Perm | After MAKELINK: `(A Σ' →* Σ'' :: ℓ ∈ dom(Σ''.L) ∧ Σ''.L(ℓ) = Σ'.L(ℓ))`, by LP13. | introduced |
| M-NoIndexState | The abstract specification requires no separate index state component. Discoverability is computed from `L` and `M` via the projection function of ASN-0098. | introduced |
| M-CompAtomicity | The composite is not atomic at the substrate level. The intermediate state `Σ_mid` between K.λ and K.μ⁺_L has the link allocated but not placed. `discoverable_from(ℓ, d_target, ·)` agrees at `Σ_mid` and `Σ'` for every `d_target ≠ d`; for `d_target = d` the two values agree unless some endset reflexively covers `ℓ`. Composite-level atomicity, if required, belongs to the protocol layer above the substrate. | introduced |
| M-Inv-State | *Per-state invariants at `Σ'`.* The post-state satisfies the link-store invariants (L0, L1, L1a, L1b, L1c, L3, L14, L-fin), the arrangement invariants (S2, S3★, S3★-aux, S8a, S8-depth, S8-fin, S8★, CL-OWN, CL-UNIQ, D-MIN★, D-CTG★, D-SEQ★), and the frame-inherited invariants over unchanged domains (S4, S7a, S7b, S7d, C1b, C1c, C-fin, P6, P7, P8, M0, NodeLineage, ActivatedEmission). The grouping by frame is given in *Invariant Preservation*. | introduced |
| M-Inv-Bdry | *Composite-boundary properties at `Σ'`.* P4★, P4a, P7a hold at `Σ'` — all preserved because `R' = R`, `dom(Σ'.C) = dom(Σ.C)`, and the new V-arrangement entry is link-subspace (so it does not enter `Contains_C(Σ')`). The three coupling constraints are discharged separately: J0 by `dom(Σ'.C) ∖ dom(Σ.C) = ∅` (frame on `C`); J1★ by `subspace(v_ℓ) = s_L ≠ s_C` (structural, the new V-position fails J1★'s content-subspace filter); J1'★ by `R' ∖ R = ∅` (frame on `R`). | introduced |
| M-Inv-Trans | *Transition invariants for `Σ → Σ'`.* M1, L12, P0, P1, P2 hold, and P3 (= P0 ∧ P1 ∧ P2 ∧ L12) holds as their conjunction. Each conjunct is discharged trivially by the frames `Σ'.C = Σ.C`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`, and L12 by K.λ adding only the fresh `ℓ`. | introduced |

## Open Questions

What well-formedness constraints, beyond `e₃ ≠ ∅`, must endsets satisfy when their spans reference I-addresses not currently in `dom(C)` or `dom(L)`?

Must MAKELINK distinguish between two invocations producing links with identical endset values, beyond the necessary distinctness of their I-addresses?

Must MAKELINK's discoverability guarantee hold at the precise post-state of the operation, or is a deferred-consistency model admissible?

When MAKELINK's endsets reference content in documents not yet allocated, what discoverability properties become available once that content is later created?

What protocol-level guarantee should bound the visibility of the intermediate state `Σ_mid`, in which a link is allocated but not yet placed?

What invariants must hold for a link whose type endset references content at an address that will never be allocated, and what does discoverability mean in that limiting case?
