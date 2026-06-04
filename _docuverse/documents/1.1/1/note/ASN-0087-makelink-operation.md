# ASN-0087: MAKELINK Operation
*2026-05-26*

## The Problem

We are looking for the precise meaning of *creating a link*. The system already maintains a content store, a family of arrangements, and a link store with prior entries. Some event introduces a new link. What does that event do?

A link, in this design, is a stored connective unit — a first-class entity binding together fragments of content. By L3 (ASN-0043) every link has at least three endsets, the third designated as type, the type slot non-empty. Beyond this, link creation must produce three things unconditionally: an *identity* (the link's address), a *value* (the endsets), and a *home* (the document under whose authority the link is allocated). It must also establish the *discoverability property* — the LP12 (ASN-0098) mechanism by which a query of the content reached by the link's endsets can surface the link.

## Inputs

What must the caller supply?

- A *home document* `d ∈ dom(Σ.M)` — the document under whose authority the link is allocated. (By L1a, ASN-0043, every link's home document must be allocated.)
- A *sequence of endsets* `(e₁, ..., eₙ)` with `N ≥ 3`, each `eᵢ ∈ Endset`, and `e₃ ≠ ∅`. (By L3, ASN-0043.)

The caller does *not* specify the link's address or its V-position in the home document — neither is an operation *parameter*. The address `ℓ` is *derived* by the system from the current state (the next emission of `A_L(d)`); the V-position `v_ℓ` is likewise system-derived, not a parameter.

*Canonical link-subspace depth (M-DepthConv).* When `V_{s_L}(d) = ∅`, the substrate operation K.μ⁺_L (ASN-0047) admits *any* `m ≥ 2` for the first link's V-position via `ValidFirstLinkPosition(d, v_ℓ, m)`. MAKELINK commits to the *minimal admissible* depth `m = 2` for every first link *it* places. Once it has done so, S8-depth (ASN-0047) pins `m_L(d) = 2` for all later link V-positions of that document.

We write `dom(M)` throughout for the set of allocated documents (`dom(M) = E_doc` by M1, ArrangementMonotonicity, ASN-0047).

*Endsets and emptiness.* L3 (ASN-0043) requires the third slot `e₃` to be non-empty but imposes no non-emptiness constraint on the other slots. The empty endset `eᵢ = ∅` is a permitted boundary case for `i ≠ 3`: by the coverage definition, `coverage(∅) = ⋃_{(s,ℓ) ∈ ∅} … = ∅`, so an empty slot contributes nothing to any `project(ℓ, i, ·, ·)` and nothing to any LP12-based discoverability disjunct.

*Standard authoring.* An endset `e` is *standardly authored at state `Σ`* iff every *substrate-emittable* address it covers already resides in the substrate — coverage intersected with `F`, ASN-0098's set of substrate-emittable addresses (the only set K.α and K.λ allocate from, with `dom(Σ.C) ∪ dom(Σ.L) ⊆ F` by LP-Sub):

  StandardAuthoring(e, Σ)  ≡  coverage(e) ∩ F  ⊆  dom(Σ.C) ∪ dom(Σ.L)

A link's input endset sequence `(e₁, ..., eₙ)` is standardly authored at `Σ` iff `StandardAuthoring(eᵢ, Σ)` holds for every `i ∈ {1, ..., N}`. The discipline rules out forward-reaching endsets that pre-emptively cover not-yet-allocated substrate addresses.

*Fresh-address exclusion (M-FreshExcl).* For any `x ∈ F` with `x ∉ dom(Σ.C) ∪ dom(Σ.L)` and any endset `e` satisfying `StandardAuthoring(e, Σ)`:

  x ∉ coverage(e)

The derivation is immediate — were `x ∈ coverage(e)`, then `x ∈ coverage(e) ∩ F ⊆ dom(Σ.C) ∪ dom(Σ.L)` by standard authoring, contradicting `x ∉ dom(Σ.C) ∪ dom(Σ.L)`.

## Decomposition

We observe that link creation must accomplish two distinct effects: (i) introduce the link into `dom(L)` with its value recorded, and (ii) make the link visible in the home document's arrangement. The substrate (ASN-0093, ASN-0047) provides exactly two atomic operations matching this division:

- `K.λ` allocates the link in `dom(L)`, binding it to the given endsets.
- `K.μ⁺_L` extends `M(d)` in the link subspace — where links live in V-space (L14a's supersession, ASN-0047) — mapping a fresh V-position to the link.

We therefore identify MAKELINK as the composite `K.λ ; K.μ⁺_L` — K.λ followed by K.μ⁺_L — applied to the same home document. The semicolon denotes sequential composition of atomic transitions. The order is forced: K.μ⁺_L's precondition requires `ℓ ∈ dom(L)`, so K.λ must precede it.

## Preconditions

The composite is valid when its component preconditions hold. ASN-0093's K.λ has exactly the following binding precondition at `Σ`:

  d ∈ dom(M)
  ℓ is produced by A_L(d) (first emission if d has no prior links; otherwise inc(ℓ_prev, 0))
  N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅

The emission clause `ℓ is produced by A_L(d)` is the caller-discharged obligation on `ℓ`. The freshness and structural shape of `ℓ` are derived — ASN-0093 facts that hold automatically for any `A_L(d)` emission:

  ℓ ∉ dom(C) ∪ dom(L)                                   [FirstEmissionFreshness, SubsequentEmissionFreshness, ASN-0093: every A_L(d) emission is fresh against dom(C) ∪ dom(L)]
  zeros(ℓ) = 3 ∧ E(ℓ)₁ = s_L ∧ #E(ℓ) ≥ 2 ∧ origin(ℓ) = d   [FirstEmission, ChainDiscipline]

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

The derived freshness of `ℓ` (FirstEmissionFreshness, SubsequentEmissionFreshness, ASN-0093) gives `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)`. In either subspace case, `Σ.M(d)(v) ∈ dom(Σ.C) ∪ dom(Σ.L)`, so `Σ.M(d)(v) ≠ ℓ`. Hence `ℓ ∉ ran(Σ.M(d)) = ran(Σ_mid.M(d))`.

The intermediate-state conditions for K.μ⁺_L reduce to original-state conditions, so the caller-visible precondition for MAKELINK is just K.λ's precondition, with `ℓ` supplied by `A_L(d)`'s next emission and `v_ℓ` system-derived.

## Effect

We summarize the composite state transition. Writing the post-state as `Σ'`:

  Σ'.L  =  Σ.L ∪ {ℓ ↦ (e₁, ..., eₙ)}
  Σ'.M(d)  =  Σ.M(d) ∪ {v_ℓ ↦ ℓ}

where `v_ℓ` is determined by `Σ.M(d)`'s link subspace, via K.μ⁺_L's positioning rule (ASN-0047):

  v_ℓ  =  [s_L, 1]                             if V_{s_L}(d) = ∅ at Σ  (depth per M-DepthConv)
  v_ℓ  =  shift(max(V_{s_L}(d)), 1)             otherwise  (depth m_L(d), the existing link-subspace depth)

The depth follows M-DepthConv throughout. By D-SEQ★ (ASN-0047), `V_{s_L}(d) = {[s_L, 1, ..., 1, k] : 1 ≤ k ≤ n_L}` of common depth `m_L(d)` when non-empty (with `n_L = |V_{s_L}(d)|`), so the non-empty case yields `v_ℓ = shift(max(V_{s_L}(d)), 1) = [s_L, 1, ..., 1, n_L + 1]` at that same depth `m_L(d)`.

Other components are unchanged:

  Σ'.C  =  Σ.C
  Σ'.E  =  Σ.E                                          [K.λ, K.μ⁺_L hold E fixed]
  Σ'.R  =  Σ.R                                          [K.λ, K.μ⁺_L hold R fixed]
  (A ℓ' ∈ dom(Σ.L) :: Σ'.L(ℓ') = Σ.L(ℓ'))               [L12]
  (A d' ∈ dom(Σ.M), d' ≠ d :: Σ'.M(d') = Σ.M(d'))

## Permanence of the Recording

The endset sequence `Σ'.L(ℓ) = (e₁, ..., eₙ)` is permanently fixed. By LP13 (ASN-0098), for every reachable state sequence `Σ' →* Σ''`: `ℓ ∈ dom(Σ''.L) ∧ Σ''.L(ℓ) = Σ'.L(ℓ)`, hence in particular `Σ''.L(ℓ).eᵢ = Σ'.L(ℓ).eᵢ` for every slot `i`. Coverage equality is then immediate, since `coverage` is a deterministic function of the endset: `coverage(Σ''.L(ℓ).eᵢ) = coverage(Σ'.L(ℓ).eᵢ)` — the link names the same set of I-addresses across every reachable state.

## What Is Indexed?

We are looking for the discovery guarantee — the property that a future query "what links touch this content?" surfaces `ℓ` whenever the query's content lies in any of `ℓ`'s endset coverages. The query is answered by ASN-0098's `project(ℓ, i, d, Σ')` and `discoverable_from(ℓ, d, Σ')`, which we apply here at the post-state `Σ'`. By LP12 (ASN-0098):

  discoverable_from(ℓ, d, Σ')  ⟺  (E i : coverage(Σ'.L(ℓ).eᵢ) ∩ ran(Σ'.M(d)) ≠ ∅)

LP12 computes discoverability from `Σ'.L(ℓ)` and `Σ'.M(d)` alone — no separate state component participates. Discoverability is therefore a derived function of `L` and `M`, so the abstract specification requires no separate index state component (M-NoIndexState). The discoverability *mechanism* and *actual* discoverability are thus distinct: MAKELINK establishes the LP12 mechanism unconditionally, but whether `ℓ` is actually discoverable from a given document is arrangement-conditional — it turns on whether that document's arrangement reaches into an endset coverage.

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

*Reflexive variant.* We instantiate M-Reflexive concretely. Replace `e₁` with `e₁' = {(ℓ, δ(1, #ℓ))}`, keeping `e₂` and `e₃` (the caller predicts `ℓ = [d, 0, 2, 1]` per the predictability principle of wp Case 2). By PrefixSpanCoverage (ASN-0043), `coverage(e₁') = {t ∈ T : ℓ ≼ t}`, which contains `ℓ`. The M-Reflexive hypothesis `ℓ ∈ coverage(e₁')` is thus met, so wp Case 2's reflexive disjunct fires: `discoverable_from(ℓ, d, Σ')` holds with witness `v_ℓ ∈ project(ℓ, 1, d, Σ')`, regardless of `d`'s prior arrangement. Note that `e₁'` is *not* standardly authored at `Σ`: it pre-emptively covers the fresh `ℓ` (`ℓ ∈ F` but `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)`), so `coverage(e₁') ∩ F ⊄ dom(Σ.C) ∪ dom(Σ.L)`.

## Weakest Precondition for Discoverability

We compute `wp(MAKELINK, discoverable_from(ℓ, d_target, ·))` — the predicate on the pre-state `Σ` (parametrized by the input endsets `(e₁, ..., eₙ)` and the choice of `d_target`) that ensures the post-state satisfies `discoverable_from(ℓ, d_target, Σ')`.

*Operation enabledness.* Following the foundation's wp convention (LP12a, ASN-0098), wp is written `enabled(op) ∧ …` for total correctness. For MAKELINK the applicability predicate is the caller-visible precondition M-Pre:

  enabled(MAKELINK)  ≡  d ∈ dom(Σ.M)  ∧  N ≥ 3  ∧  (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset)  ∧  e₃ ≠ ∅

The predicate concerns the *home* document `d` and the endset inputs, and is logically independent of the target document `d_target`.

*Membership precondition.* `discoverable_from(a, d, Σ)` is defined in ASN-0098 only when `a ∈ dom(Σ.L) ∧ d ∈ dom(Σ.M)`. At the post-state, `ℓ ∈ dom(Σ'.L)` by K.λ's effect, so the left conjunct is automatic. The right conjunct `d_target ∈ dom(Σ'.M)` requires that the target document was already registered at the pre-state. MAKELINK leaves the document set fixed:

  dom(Σ'.M) = dom(Σ.M)                                    (M-DocFixity)

M1 supplies only the inclusion `dom(Σ.M) ⊆ dom(Σ'.M)`; the reverse inclusion at MAKELINK comes from the K.λ frame and K.μ⁺_L's effect, neither of which extends `dom(M)` (K.λ's frame holds `M` entirely fixed; K.μ⁺_L extends `dom(M(d))` for an already-registered `d` without adding any new document). Combining the M1 inclusion with these two frame consequences gives M-DocFixity, so `d_target ∈ dom(Σ'.M) ⟺ d_target ∈ dom(Σ.M)`. For `d_target = d` the membership clause is subsumed by `enabled(MAKELINK)`'s `d ∈ dom(Σ.M)` conjunct; for `d_target ≠ d` it is an independent obligation.

*Case 1: d_target ≠ d.* K.μ⁺_L's frame gives `Σ'.M(d_target) = Σ.M(d_target)` for every `d_target ≠ d` in `dom(Σ'.M)`. By LP12 at `Σ'`:

  discoverable_from(ℓ, d_target, Σ')
    ⟺  (E i :: coverage(Σ'.L(ℓ).eᵢ) ∩ ran(Σ'.M(d_target)) ≠ ∅)
    ⟺  (E i :: coverage(eᵢ) ∩ ran(Σ.M(d_target)) ≠ ∅)

The wp reduces to a predicate on the pre-state alone, conjoined with MAKELINK's enabledness and the membership clause that keeps `discoverable_from` defined at the post-state:

  wp(MAKELINK, discoverable_from(ℓ, d_target, ·))
    ≡  enabled(MAKELINK)  ∧  d_target ∈ dom(Σ.M)  ∧  (E i :: coverage(eᵢ) ∩ ran(Σ.M(d_target)) ≠ ∅)

*Case 2: d_target = d.* The post-state arrangement gains `ℓ`: `ran(Σ'.M(d)) = ran(Σ.M(d)) ∪ {ℓ}`. By LP12:

  discoverable_from(ℓ, d, Σ')
    ⟺  (E i :: coverage(eᵢ) ∩ (ran(Σ.M(d)) ∪ {ℓ}) ≠ ∅)
    ⟺  (E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)  ∨  (E i :: ℓ ∈ coverage(eᵢ))

The disjunction isolates two routes to home-document discoverability:

- (i) *Arrangement-reach route:* some endset's coverage intersects `d`'s pre-existing arrangement range.
- (ii) *Reflexive route:* some endset's coverage contains `ℓ` itself.

L13 (ReflexiveAddressing, ASN-0043) permits a link's endsets to cover link addresses, including the link's own address, so route (ii) is admissible. Although `ℓ` is not a parameter, it is state-derivable — a caller predicts it by evaluating `A_L(d)`'s emission rule against the observed state (`[d, 0, s_L, 1]` when `d` has no prior links, else `inc(ℓ_prev, 0)`) — so the reflexive disjunct is non-vacuous. When its disjunct holds it is forced by the post-state witness `v_ℓ ↦ ℓ`: if `ℓ ∈ coverage(eᵢ)` for some `i`, then since `Σ'.L(ℓ).eᵢ = eᵢ` (K.λ's effect, K.μ⁺_L's frame on `L`) and `Σ'.M(d)(v_ℓ) = ℓ`, we have `v_ℓ ∈ project(ℓ, i, d, Σ')`, so `discoverable_from(ℓ, d, Σ')` holds regardless of `Σ.M(d)`'s pre-existing arrangement (M-Reflexive). Because `ℓ` enters only `d`'s arrangement, this route is available to the home document alone — Case 1 already shows other documents gain nothing from the allocation of `ℓ`.

As a wp (the membership clause subsumed by `enabled(MAKELINK)` here, since `d_target = d`):

  wp(MAKELINK, discoverable_from(ℓ, d, ·))
    ≡  enabled(MAKELINK)  ∧  [(E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅) ∨ (E i :: ℓ ∈ coverage(eᵢ))]

*Reduction under standard authoring.* We first establish `ℓ ∈ F` structurally: `ℓ` is an `A_L(d)` emission, so FirstEmission and ChainDiscipline (ASN-0093) fix its form `[d, 0, s_L, k]` with `k ≥ 1`; `origin(ℓ) = d` with `d` T4-valid and `zeros(d) = 2` by M0 (ASN-0093); F's definition then yields `ℓ ∈ F`. When every input endset satisfies `StandardAuthoring(eᵢ, Σ)`, K.λ's freshness gives `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)`, so M-FreshExcl (*Inputs*) instantiated at `x = ℓ` yields `ℓ ∉ coverage(eᵢ)` for every `i` — the reflexive route's disjunct `(E i :: ℓ ∈ coverage(eᵢ))` is unreachable (M-Reflexive). The wp collapses:

  wp(MAKELINK, discoverable_from(ℓ, d, ·))
    ≡  enabled(MAKELINK)  ∧  (E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)

— the same shape as Case 1 (with `d_target := d`; the two enabledness-and-membership conjuncts coincide there into `enabled(MAKELINK)`, since the home and target documents are one). Under standard authoring, home-document discoverability requires `d`'s arrangement to reach into some endset's coverage; there is no automatic "self-discovery" of `ℓ` from `d` (M-DiscSymmetry).

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

The side effect can only occur when `ℓ'` was authored with an endset whose span coverage extends to addresses not yet allocated at authoring time. Such forward-reaching endsets are permitted by L4 (EndsetGenerality, ASN-0043) — endset spans may reference any addresses in the tumbler space, including those not currently in `dom(C) ∪ dom(L)`. MAKELINK's allocation of `ℓ` "fills in" a previously-uncovered region of the address space, retroactively activating any prior endset that had pre-emptively claimed it. When `ℓ'` was authored under standard authoring at its own authoring state — `StandardAuthoring(Σ.L(ℓ').eᵢ, Σ_{ℓ'})` holds at the state `Σ_{ℓ'}` at which `ℓ'` was incorporated — no such endset can cover the future fresh `ℓ`, and the side effect is vacuous. The freshness of `ℓ` transfers backward from the K.λ allocation state `Σ_ℓ` to the earlier authoring state `Σ_{ℓ'}` (where `Σ_{ℓ'} →* Σ_ℓ`): by Store Monotonicity★ (ASN-0098), `dom(Σ_{ℓ'}.C) ∪ dom(Σ_{ℓ'}.L) ⊆ dom(Σ_ℓ.C) ∪ dom(Σ_ℓ.L)`, so K.λ's freshness `ℓ ∉ dom(Σ_ℓ.C) ∪ dom(Σ_ℓ.L)` yields `ℓ ∉ dom(Σ_{ℓ'}.C) ∪ dom(Σ_{ℓ'}.L)`. M-FreshExcl (*Inputs*) — instantiated at `x = ℓ` (with `ℓ ∈ F` established in *Weakest Precondition for Discoverability*, "Reduction under standard authoring") and `e = Σ.L(ℓ').eᵢ` at state `Σ_{ℓ'}`, using this transferred freshness — then gives `ℓ ∉ coverage(Σ.L(ℓ').eᵢ)`.

For `d_target ≠ d`, `Σ'.M(d_target) = Σ.M(d_target)`, so prior-link discoverability is unchanged; the side-effect window is the home document `d` (M-PriorLinkDisc).

## Invariant Preservation

We verify the substrate invariants in three classes, following ASN-0047's stratification: (a) *per-state invariants* holding at the post-state `Σ'`; (b) *composite-boundary properties* (P4★, P4a, P7a) evaluated at composite boundaries; (c) *transition invariants* governing the pair `Σ → Σ'`. The new entries are `ℓ ∈ dom(L)` and `v_ℓ ∈ dom(M(d))`; prior entries are unchanged by the frame.

### Per-State Invariants at Σ'

For the link itself:

  L0:    E(ℓ)₁ = s_L                          derived from A_L(d) emission (FirstEmission, ChainDiscipline)
  L1:    zeros(ℓ) = 3                          derived from A_L(d) emission (FirstEmission, ChainDiscipline)
  L1a:   origin(ℓ) = d ∈ dom(Σ'.M)             derived from A_L(d) emission and M1
  L1b:   #E(ℓ) ≥ 2                             derived from A_L(d) emission (FirstEmission, ChainDiscipline)
  L3:    N ≥ 3 ∧ e₃ ≠ ∅                       from K.λ precondition
  L12:   immutability                          new entry only; no modification of prior
  L14:   store disjointness                    ℓ ∉ dom(C) from derived freshness
  L-fin: link store finiteness                 |dom(L')| = |dom(L)| + 1

L1c (structural inc-chain conformance) requires a T10a-conforming inc-chain seeded at `origin(ℓ) = d` with `k₁ = 2` and `#tᵢ > #origin(ℓ)` at every step. We discharge L1c directly: `ℓ` enters `dom(L)` solely via K.λ, and ASN-0093 establishes L1c as an invariant maintained over all of `dom(L)` under K.λ allocation. Hence L1c holds at `ℓ` in `Σ'`. ✓

For the V-arrangement entry `v_ℓ ↦ ℓ`:

  S2:       M'(d) remains a partial function                      v_ℓ ∉ dom(Σ.M(d)) by the two-part argument below; v_ℓ enters dom(M'(d)) fresh, preserving functionality of M'(d)
  S3★:      image of v_ℓ is ℓ ∈ dom(L'), subspace(v_ℓ) = s_L     direct from the effect
  S3★-aux:  subspace(v_ℓ) = s_L ∈ {s_C, s_L}                      direct from the effect
  S8a:      zeros(v_ℓ) = 0, #v_ℓ = m_L^{Σ'}(d) ≥ 2, components all > 0  v_ℓ = [s_L, 1, ..., 1, k]; post-state link depth m_L^{Σ'}(d) = 2 when V_{s_L}(d) = ∅ (pinned by M-DepthConv), else m_L^{Σ'}(d) = m_L(d) (existing depth); s_L = 2 > 0, all components ≥ 1
  S8-depth: depth uniformity in subspace s_L at d                 common depth m_L(d) for all V-positions in V_{s_L}(d); v_ℓ's depth per M-DepthConv
  S8-fin:   |dom(M'(d))| = |dom(M(d))| + 1                       S8-fin at Σ gives finiteness of the predecessor
  S8★:      per-subspace span decomposition                       content subspace frame-fixed (inheritance); link subspace admits trivial length-1 decomposition (see below)
  CL-OWN:   origin(M'(d)(v_ℓ)) = origin(ℓ) = d                   origin(ℓ) = d derived from A_L(d) emission
  CL-UNIQ:  partial injection preserved                           K.μ⁺_L first-arrangement guard ℓ ∉ ran(M_mid(d))
  D-MIN★:   min(V_{s_L}^{Σ'}(d)) = [s_L, 1, ..., 1]               both cases below
  D-CTG★:   extension is contiguous                               discharged below: the post-state set is an initial segment of the depth-m_L^{Σ'}(d), subspace-s_L slice, contiguous at every depth m ≥ 2
  D-SEQ★:   V_{s_L}^{Σ'}(d) is contiguous initial segment           see below

*Scope of the arrangement-indexed obligations.* The invariants S2, S8a, D-CTG★, D-MIN★, and D-SEQ★ are universally quantified over documents (and, for the D-invariants, over subspaces `S` with `V_S(d') ≠ ∅`, ASN-0047), so each is a conjunction of per-document/per-subspace conjuncts. Every conjunct at a document `d' ≠ d` is preserved by frame: `M'(d') = M(d')` leaves `dom(M'(d'))`, `V_{s_C}(d')`, and `V_{s_L}(d')` all unchanged. At the home document `d` the content-subspace conjunct is likewise frame-preserved: K.μ⁺_L touches only the link subspace, so `V_{s_C}^{Σ'}(d) = V_{s_C}(d)` and `M'(d)|_{V_{s_C}(d)}` is unchanged (S3★-aux, K.μ⁺_L effect). Only the link-subspace conjunct at `d` — carrying the newly entered V-position `v_ℓ ∈ V_{s_L}(d)` — requires argument; the discharges below address exactly that conjunct.

For S2: we must show `v_ℓ ∉ dom(Σ.M(d))`, not merely `v_ℓ ∉ V_{s_L}(d)`. By S3★-aux at `Σ`, `dom(Σ.M(d)) = V_{s_C}(d) ∪ V_{s_L}(d)`, so the obligation splits into two exclusions:
- *Within-subspace exclusion:* `v_ℓ ∉ V_{s_L}(d)`. By D-SEQ★ at `Σ`, `V_{s_L}(d) = {[s_L, 1, ..., 1, k] : 1 ≤ k ≤ n_L}` at the common depth `m_L(d)`; K.μ⁺_L's positioning rule sets `v_ℓ = [s_L, 1, ..., 1, n_L + 1]` (or, when `n_L = 0`, the chosen first position `[s_L, 1, ..., 1]`), which lies outside this set by the strict inequality `n_L + 1 > n_L` (resp. by the emptiness of the set when `n_L = 0`).
- *Cross-subspace exclusion:* `v_ℓ ∉ V_{s_C}(d)`. By construction `(v_ℓ)₁ = s_L`, while every `v ∈ V_{s_C}(d)` has `(v)₁ = s_C` by the definition `V_{s_C}(d) = {v ∈ dom(M(d)) : subspace(v) = s_C}` together with `subspace(v) = v₁` (SubspaceProjection, ASN-0036). By SC-NEQ (ASN-0093), `s_L ≠ s_C`, so `v_ℓ ≠ v` for every `v ∈ V_{s_C}(d)`.

Combining the two exclusions, `v_ℓ ∉ V_{s_C}(d) ∪ V_{s_L}(d) = dom(Σ.M(d))`, discharging S2. ✓

For D-MIN★: we must show `min(V_{s_L}^{Σ'}(d)) = [s_L, 1, ..., 1]`. Two cases on whether the link subspace was empty at `Σ`:
- *Empty case* (`V_{s_L}(d) = ∅`): K.μ⁺_L's positioning rule places `v_ℓ = [s_L, 1]` at depth 2 (M-DepthConv), so `V_{s_L}^{Σ'}(d) = {v_ℓ}` and `min(V_{s_L}^{Σ'}(d)) = v_ℓ = [s_L, 1]`, the singleton minimum.
- *Non-empty case* (`V_{s_L}(d) ≠ ∅`): the pre-state minimum is `[s_L, 1, ..., 1]` by D-MIN★ at `Σ`. K.μ⁺_L adds `v_ℓ = [s_L, 1, ..., 1, n_L + 1]` *above* the existing positions: since `n_L ≥ 1`, the last component `n_L + 1 > 1` makes `v_ℓ` strictly exceed `[s_L, 1, ..., 1]` under T1, so `v_ℓ` does not undercut the existing minimum. The minimum is retained: `min(V_{s_L}^{Σ'}(d)) = min(V_{s_L}(d)) = [s_L, 1, ..., 1]`. ✓

For D-SEQ★: by D-SEQ★ at `Σ`, `V_{s_L}(d) = {[s_L, 1, ..., 1, k] : 1 ≤ k ≤ n_L}` of common depth `m_L(d)` for some `n_L ≥ 0` (with `n_L = 0` meaning the link subspace at `d` is empty). If `n_L = 0`, MAKELINK commits the minimal depth per M-DepthConv: the K.μ⁺_L positioning rule gives `v_ℓ = [s_L, 1]` at depth 2, so `V_{s_L}^{Σ'}(d) = {v_ℓ}` — a contiguous initial segment of cardinality 1, fixing `m_L^{Σ'}(d) = 2`. If `n_L ≥ 1`, the rule gives `v_ℓ = shift(max(V_{s_L}(d)), 1) = [s_L, 1, ..., 1, n_L + 1]` at depth `m_L(d)`, so `V_{s_L}^{Σ'}(d) = {[s_L, 1, ..., 1, k] : 1 ≤ k ≤ n_L + 1}` — a contiguous initial segment of cardinality `n_L + 1`. Either way, the post-state set conforms to D-SEQ★. ✓

For D-CTG★: D-CTG★ (ASN-0047) quantifies over the *full* depth-`m_L^{Σ'}(d)`, subspace-`s_L` slice — every positive-component tuple `z` with `v_lo ≤ z ≤ v_hi` (extremes drawn from `V_{s_L}^{Σ'}(d)`) must be a member. We prove this directly at the arbitrary post-state depth `m := m_L^{Σ'}(d) ≥ 2`, without assuming `m = 2`. By D-SEQ★ (discharged above), the post-state set is the initial segment `V_{s_L}^{Σ'}(d) = {[s_L, 1, ..., 1, k] : 1 ≤ k ≤ K}` of length-`m` tuples, with `K = 1` (empty case) or `K = n_L + 1` (non-empty case); its extremes are `v_lo = [s_L, 1, ..., 1]` and `v_hi = [s_L, 1, ..., 1, K]`. Let `z = [s_L, z_2, ..., z_m]` be any slice tuple (depth `m`, first component `s_L`, all components `≥ 1`) with `v_lo ≤ z ≤ v_hi` under T1. From `z ≤ v_hi`: were `z_j > 1` at any interior position `2 ≤ j ≤ m − 1`, then at the least such `j` the tuples `z` and `v_hi` agree on positions `1..j−1` (component `s_L` at position 1, component `1` at positions `2..j−1`) while `z_j > 1 = (v_hi)_j`, giving `z > v_hi` by T1 case (i) — contradicting `z ≤ v_hi`. Hence `z_j = 1` for every `2 ≤ j ≤ m − 1`, so `z = [s_L, 1, ..., 1, z_m]`. Then `v_lo ≤ z` forces `z_m ≥ 1` and `z ≤ v_hi` forces `z_m ≤ K`, so `z = [s_L, 1, ..., 1, k]` with `1 ≤ k ≤ K`, i.e. `z ∈ V_{s_L}^{Σ'}(d)`. The extension-by-one-at-the-top of a D-SEQ★ initial segment is thus contiguous at every depth `m ≥ 2`, discharging the D-CTG★ contiguity conjunct over the full slice. ✓

For S8★: ASN-0047's S8★ is a conjunction over both subspaces `S ∈ {s_C, s_L}`, retaining S8's conditions (a), (b) on each and the uniqueness condition (c) on the content subspace. We discharge both halves at the home document `d`.

- *Content subspace.* K.μ⁺_L touches only the link subspace: by its effect `dom(Σ'.M(d)) = dom(Σ.M(d)) ∪ {v_ℓ}` with `subspace(v_ℓ) = s_L`, and by S3★-aux the content-subspace V-positions are unchanged, so `V_{s_C}^{Σ'}(d) = V_{s_C}(d)` and `M'(d)|_{V_{s_C}^{Σ'}(d)} = M(d)|_{V_{s_C}(d)}` is frame-fixed. The pre-state content-subspace decomposition — including its uniqueness condition (c) — holds at `Σ` by the reachability hypothesis and carries to `Σ'` unchanged by inheritance.
- *Link subspace.* Per ASN-0047's S8★, the link-subspace projected arrangement `M'(d)|_{V_{s_L}^{Σ'}(d)} : V_{s_L}^{Σ'}(d) → dom(L')` admits the trivial length-1 decomposition `{(v, M'(d)(v), 1) : v ∈ V_{s_L}^{Σ'}(d)}`. The new entry `(v_ℓ, ℓ, 1)` joins this decomposition; S8's conditions (a) and (b) hold trivially at length 1. ✓

Every invariant quantifying solely over `C`, `E`, `R`, or the document set `dom(M)` — all frame-fixed at MAKELINK (`Σ'.C = Σ.C`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`, and `dom(Σ'.M) = dom(Σ.M)` by M-DocFixity) — is preserved by inheritance: S4, S7a, S7b, C1b, C1c, C-fin, P6, P7, P8, M0, NodeLineage, ActivatedEmission.

- S7d (DocumentAllocationDiscipline, ASN-0036): document set unchanged by M-DocFixity; preserved by inheritance.
- L11a (link uniqueness, ASN-0043): `ℓ` is fresh against `dom(Σ.L)` (FirstEmissionFreshness, SubsequentEmissionFreshness, ASN-0093), so its allocation event is distinct from every prior link allocation event, and L11a's distinctness conclusion holds at `Σ'`.

### Composite-Boundary Properties

ASN-0047 classifies P4★, P4a, and P7a as Class (b) — properties discharged at composite boundaries by the coupling constraints J0, J1★, J1'★. MAKELINK introduces a single link-subspace V-arrangement entry, and all three coupling constraints are vacuously satisfied. J0 (AllocationPlacementCoupling) and J1'★ (ProvenanceRequiresExtension) hold by an empty quantification universe: the frame fixes `C` and `R`, so `dom(Σ'.C) ∖ dom(Σ.C) = ∅` and `R' ∖ R = ∅`. J1★ (ExtensionRecordsProvenance) holds because the sole new V-position `v_ℓ` has `subspace(v_ℓ) = s_L ≠ s_C` (SC-NEQ, ASN-0093) — and every prior V-position's image is frame-fixed (`Σ'.M(d)(v) = Σ.M(d)(v)`) — so no content-subspace witness arises.

- P4★ (ProvenanceBounds): `Contains_C(Σ') ⊆ R'`. The new V-arrangement entry `v_ℓ ↦ ℓ` has `subspace(v_ℓ) = s_L`, so it does not contribute to `Contains_C(Σ')`. Hence `Contains_C(Σ') = Contains_C(Σ) ⊆ R = R'`.
- P4a (TraceWitnessing): for every `(a, d') ∈ R'`, some prior state `Σ_k` in the transition history had `M_k(d')(v) = a` with `subspace(v) = s_C`. Since `R' = R`, the obligation is identical to P4a at `Σ`, which holds by the reachability hypothesis on `Σ`.
- P7a (ProvenanceCoverage): for every `a ∈ dom(Σ'.C)`, some `d'` satisfies `(a, d') ∈ R'`. Since `dom(Σ'.C) = dom(Σ.C)` and `R' = R`, the obligation is identical to P7a at `Σ`, which holds by reachability.

### Transition Invariants for Σ → Σ'

- M1 (ArrangementMonotonicity, inclusion clause): `dom(Σ.M) ⊆ dom(Σ'.M)`. Holds with equality by M-DocFixity.
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

By SequentialTransitionAxiom (ASN-0093), K.λ commits to `Σ_mid` before K.μ⁺_L's precondition is evaluated. K.λ is an atomic substrate operation that ASN-0093/ASN-0047 establish to preserve the per-state invariants on reachable states, so `Σ_mid` inherits them.

Because K.λ's frame fixes `M`, `Σ_mid.M = Σ.M`, so the discoverability difference between `Σ_mid` and `Σ'` is exactly the `Σ → Σ'` delta already computed: it agrees for every `d_target ≠ d` (M-WP, Case 1), and for `d_target = d` the two values agree unless some endset reflexively covers `ℓ` (M-Reflexive).

## Permanence of the Binding

The V-position binding `v_ℓ ↦ ℓ` in the home document is less permanent than the link's identity and value — but the *only* mutation available to it is removal. K.μ~ (reordering) cannot rebind it: by K.μ~'s admissibility clause (v), *link-subspace fixing* (ASN-0047), the witnessing bijection satisfies `π(v) = v` for every link-subspace V-position `v ∈ dom_L(M(d))`. Since `v_ℓ` is a link V-position, `π(v_ℓ) = v_ℓ`, and the bijection equation gives `M'(d)(v_ℓ) = M(d)(v_ℓ) = ℓ`; the binding `v_ℓ ↦ ℓ` is therefore *invariant* under every K.μ~ transition. The link subspace is fixed pointwise by reordering. The sole operation that can alter the binding is K.μ⁻ (contraction), which may drop `v_ℓ` from `dom(M(d))` entirely. Thus the binding is mutable only by removal, never by re-binding: whether `v_ℓ ↦ ℓ` remains present in the home document's link-subspace arrangement is the one impermanent aspect of the recording.

Even if `v_ℓ` is later removed from `dom(M(d))`, the link is still in `dom(L)` and still discoverable when conditions warrant. By LP17 (ASN-0098), a link orphaned from all V-arrangements remains in the store; by LP18, it becomes discoverable again when any document later transcludes content covered by its endsets.

## No Permission Check

MAKELINK performs *no permission check on referenced content*. It does not verify ownership of the documents whose content the endsets reach; no precondition consults any ownership or permission state, and the substrate exposes no such state to consult.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| M-Comp | MAKELINK is the composite `K.λ ; K.μ⁺_L` — K.λ followed by K.μ⁺_L — applied to the same home document `d`. | introduced |
| M-DepthConv | MAKELINK fixes every first link's V-position depth at the canonical minimal `m = 2`; thereafter S8-depth pins `m_L(d) = 2`. Stated and scoped in *Inputs*. | introduced |
| M-Pre | Caller-visible precondition: `d ∈ dom(M)`, `N ≥ 3`, `(A i : eᵢ ∈ Endset)`, `e₃ ≠ ∅`. The caller supplies neither the link address nor its V-position. | introduced |
| M-Alloc | MAKELINK derives and allocates a fresh `ℓ ∈ T \ (dom(Σ.L) ∪ dom(Σ.C))` from `A_L(d)`'s next emission, and a fresh `v_ℓ ∈ T \ dom(Σ.M(d))` from K.μ⁺_L's positioning rule (serial component `n_L + 1` computed from `Σ`), with `subspace(v_ℓ) = s_L` and `#v_ℓ` per M-DepthConv. | introduced |
| M-Effect | `Σ'.L = Σ.L ∪ {ℓ ↦ (e₁, ..., eₙ)}`; `Σ'.M(d) = Σ.M(d) ∪ {v_ℓ ↦ ℓ}` (the empty/non-empty positioning case split stated once in *Effect*). | introduced |
| M-Frame | `Σ'.C = Σ.C`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`; existing entries in `L` and in `M(d')` for `d' ≠ d` are unchanged. Content is byte-identical before and after MAKELINK (referencing is read-only). | introduced |
| M-DiscSymmetry | For the standard content-reach route, discoverability of `ℓ` is symmetric across all documents whose arrangements reach into an endset coverage — LP12 grants the home document no privileged status. The reflexive route is the home document's alone, since MAKELINK places `ℓ` into its arrangement and no other. | introduced |
| StandardAuthoring | `StandardAuthoring(e, Σ) ≡ coverage(e) ∩ F ⊆ dom(Σ.C) ∪ dom(Σ.L)`, where `F` is ASN-0098's set of substrate-emittable addresses. A link's endset sequence is standardly authored at `Σ` iff every constituent endset satisfies the predicate. | introduced |
| M-Reflexive | If `ℓ ∈ coverage(eᵢ)` for some `i` (the reflexive endset case), then `v_ℓ ∈ project(ℓ, i, d, Σ')` and `discoverable_from(ℓ, d, Σ')` is forced true regardless of `Σ.M(d)`'s pre-existing arrangement. Under `(A i : StandardAuthoring(eᵢ, Σ))` the reflexive case is structurally excluded. | introduced |
| M-PriorLinkDisc | For every prior link `ℓ' ∈ dom(Σ.L)`: from the home document `d`, `discoverable_from(ℓ', d, Σ') ⟺ discoverable_from(ℓ', d, Σ) ∨ (E i :: ℓ ∈ coverage(Σ.L(ℓ').eᵢ))` — newly discoverable precisely when some endset of `ℓ'` covers `ℓ`; from any `d_target ≠ d`, `discoverable_from(ℓ', d_target, Σ') = discoverable_from(ℓ', d_target, Σ)`. The side-effect window is confined to the home document. | introduced |
| M-WP | Post-MAKELINK discoverability has explicit weakest preconditions (total correctness): for `d_target ≠ d`, `wp ≡ enabled(MAKELINK) ∧ d_target ∈ dom(Σ.M) ∧ (E i :: coverage(eᵢ) ∩ ran(Σ.M(d_target)) ≠ ∅)`; for `d_target = d`, `wp ≡ enabled(MAKELINK) ∧ [(E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅) ∨ (E i :: ℓ ∈ coverage(eᵢ))]`. Under `(A i : StandardAuthoring(eᵢ, Σ))` the reflexive disjunct collapses and the two shapes coincide. | introduced |
| M-Perm | After MAKELINK: `(A Σ' →* Σ'' :: ℓ ∈ dom(Σ''.L) ∧ Σ''.L(ℓ) = Σ'.L(ℓ))`, by LP13. | introduced |
| M-NoIndexState | The abstract specification requires no separate index state component. Discoverability is computed from `L` and `M` via the projection function of ASN-0098. | introduced |
| M-CompAtomicity | The composite is not atomic at the substrate level. The intermediate state `Σ_mid` between K.λ and K.μ⁺_L has the link allocated but not placed. `discoverable_from(ℓ, d_target, ·)` agrees at `Σ_mid` and `Σ'` for every `d_target ≠ d`; for `d_target = d` the two values agree unless some endset reflexively covers `ℓ`. Composite-level atomicity, if required, belongs to the protocol layer above the substrate. | introduced |
| M-Inv-State | *Per-state invariants at `Σ'`.* The post-state satisfies the link-store invariants (L0, L1, L1a, L1b, L1c, L3, L14, L-fin), the arrangement invariants (S2, S3★, S3★-aux, S8a, S8-depth, S8-fin, S8★, CL-OWN, CL-UNIQ, D-MIN★, D-CTG★, D-SEQ★), and the frame-inherited invariants over unchanged domains (S4, S7a, S7b, S7d, C1b, C1c, C-fin, P6, P7, P8, M0, NodeLineage, ActivatedEmission). Discharged in *Invariant Preservation*. | introduced |
| M-Inv-Bdry | *Composite-boundary properties at `Σ'`.* P4★, P4a, P7a hold at `Σ'`, and the coupling constraints J0, J1★, J1'★ are satisfied across the composite. Discharged in *Invariant Preservation*. | introduced |
| M-Inv-Trans | *Transition invariants for `Σ → Σ'`.* M1, L12, P0, P1, P2 hold, and P3 (= P0 ∧ P1 ∧ P2 ∧ L12) holds as their conjunction. Discharged in *Invariant Preservation*. | introduced |

## Open Questions

What well-formedness constraints, beyond `e₃ ≠ ∅`, must endsets satisfy when their spans reference I-addresses not currently in `dom(C)` or `dom(L)`?

Must MAKELINK distinguish between two invocations producing links with identical endset values, beyond the necessary distinctness of their I-addresses?

Must MAKELINK's discoverability guarantee hold at the precise post-state of the operation, or is a deferred-consistency model admissible?

When MAKELINK's endsets reference content in documents not yet allocated, what discoverability properties become available once that content is later created?

What protocol-level guarantee should bound the visibility of the intermediate state `Σ_mid`, in which a link is allocated but not yet placed?

What invariants must hold for a link whose type endset references content at an address that will never be allocated, and what does discoverability mean in that limiting case?
