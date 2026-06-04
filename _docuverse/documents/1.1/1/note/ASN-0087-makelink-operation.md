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

The caller does *not* — and cannot — specify the link's address or its V-position in the home document. The address `ℓ` is determined by the system from the current state (the next emission of `A_L(d)`). The V-position `v_ℓ` is determined from the current state together with the canonical-depth convention M-DepthConv below — its serial component fixed by the link subspace's current cardinality, its depth fixed per M-DepthConv. We make the convention explicit precisely because the depth is *not* recoverable from `Σ` in the boundary case where the link subspace is empty.

*Canonical link-subspace depth (M-DepthConv).* When `V_{s_L}(d) = ∅`, the substrate operation K.μ⁺_L (ASN-0047) admits *any* `m ≥ 2` for the first link's V-position via `ValidFirstLinkPosition(d, v_ℓ, m)`; the state `Σ` does not determine `m` (`m_L(d)`, ASN-0047, is well-defined only while `V_{s_L}(d) ≠ ∅`). MAKELINK therefore commits to the *minimal admissible* depth `m = 2` for every first link *it* places. Once it has done so, S8-depth (ASN-0047) pins `m_L(d) = 2` for all later link V-positions of that document, so every subsequent `v_ℓ` MAKELINK places *is* fully state-determined. As a scoped universal: for any document `d` whose every link V-position was placed by MAKELINK, `m_L(d) = 2`. This is MAKELINK's normative commitment, not a system-wide invariant; the general `m_L(d)` reading is retained downstream, since K.μ⁺_L is a standalone substrate primitive that may be invoked outside MAKELINK.

We write `dom(M)` throughout for the set of allocated documents (`dom(M) = E_doc` by M1, ArrangementMonotonicity, ASN-0047; ASN-0047 states some preconditions against `E_doc`).

*Endsets and emptiness.* L3 (ASN-0043) requires the third slot `e₃` to be non-empty but imposes no non-emptiness constraint on the other slots. The empty endset `eᵢ = ∅` is a permitted boundary case for `i ≠ 3`: by the coverage definition, `coverage(∅) = ⋃_{(s,ℓ) ∈ ∅} … = ∅`, so an empty slot contributes nothing to any `project(ℓ, i, ·, ·)` and nothing to any LP12-based discoverability disjunct. The analysis below covers this case implicitly through the existential `(E i :: …)` in LP12: empty slots simply fail to witness, leaving the disjunction's truth value determined by the non-empty slots.

*Standard authoring.* We name the discipline under which several later reductions hold. An endset `e` is *standardly authored at state `Σ`* iff every span in `e` references addresses already in the substrate:

  StandardAuthoring(e, Σ)  ≡  coverage(e) ⊆ dom(Σ.C) ∪ dom(Σ.L)

A link's input endset sequence `(e₁, ..., eₙ)` is standardly authored at `Σ` iff `StandardAuthoring(eᵢ, Σ)` holds for every `i ∈ {1, ..., N}`. This is a *structural* constraint on the endset value at the time MAKELINK is invoked — it is not an epistemic constraint on the caller's knowledge. The discipline rules out forward-reaching endsets that pre-emptively cover not-yet-allocated addresses.

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
  subspace(v_ℓ) = s_L          [by construction: (v_ℓ)₁ = s_L]
  #v_ℓ per M-DepthConv        [depth fixed per M-DepthConv: m = 2 when V_{s_L}(d) = ∅, else the existing m_L(d)]
  v_ℓ at the next link-subspace position per D-MIN★ / D-CTG★

The condition `ℓ ∉ ran(Σ_mid.M(d))` requires more than `ℓ ∉ dom(Σ.L)`; it must be derived through the S3★ + S3★-aux + L14 chain. K.λ's frame preserves `M`, so `Σ_mid.M(d) = Σ.M(d)` and `ran(Σ_mid.M(d)) = ran(Σ.M(d))`. By S3★-aux (ASN-0047), every `v ∈ dom(Σ.M(d))` has `subspace(v) ∈ {s_C, s_L}`. By S3★:

- If `subspace(v) = s_C`, then `Σ.M(d)(v) ∈ dom(Σ.C)`.
- If `subspace(v) = s_L`, then `Σ.M(d)(v) ∈ dom(Σ.L)`.

K.λ's freshness precondition gives `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)`. In either subspace case, `Σ.M(d)(v) ∈ dom(Σ.C) ∪ dom(Σ.L)`, so `Σ.M(d)(v) ≠ ℓ`. Hence `ℓ ∉ ran(Σ.M(d)) = ran(Σ_mid.M(d))`. L14 (StoreDisjointness, ASN-0093) confirms internal consistency at `Σ_mid`: `dom(Σ_mid.L) = dom(Σ.L) ∪ {ℓ}` and `dom(Σ_mid.C) = dom(Σ.C)`, so `ℓ ∈ dom(Σ_mid.L)` combined with `dom(Σ_mid.C) ∩ dom(Σ_mid.L) = ∅` gives `ℓ ∉ dom(Σ_mid.C)` — so no `s_C`-subspace V-position at `Σ_mid` can image to `ℓ` either, matching the conclusion derived above.

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

The address `ℓ` is genuinely new — `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)` at `Σ` — so K.λ's freshness precondition is met by construction rather than by faith. We do not re-derive this from the underlying chain lemmas; ASN-0093 already packages the guarantee for every emission of `A_L(d)`, and MAKELINK introduces no allocation step beyond the K.λ it composes, so the result transfers verbatim:

- *First-emission case* (`{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d} = ∅`): FirstEmissionFreshness (ASN-0093) gives `ℓ = [d, 0, s_L, 1] ∉ dom(Σ.L) ∪ dom(Σ.C)`.
- *Subsequent-emission case* (`ℓ = inc(ℓ_prev, 0)`): SubsequentEmissionFreshness (ASN-0093) gives `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)`. That lemma's own three-way split discharges within-document freshness (via ChainEnumerationInjectivity), cross-subspace freshness (via DisjointSubAllocatorChains and SC-NEQ), and cross-document freshness (via Cross-doc disjointness composed with T10, PartitionIndependence, ASN-0034) — so the layered argument lives in the foundation, not here.

The V-position `v_ℓ` is fresh in `dom(M(d))`. K.μ⁺_L's positioning rule combined with D-SEQ★ (ASN-0047) supplies the within-subspace half: the link subspace V-positions form a contiguous sequence `{[s_L, 1, ..., 1, k] : 1 ≤ k ≤ n_L}`, and `v_ℓ` extends it by one, so `v_ℓ ∉ V_{s_L}(d)`. But `dom(M(d)) = V_{s_C}(d) ∪ V_{s_L}(d)` (S3★-aux, ASN-0047), so full freshness additionally requires the cross-subspace exclusion `v_ℓ ∉ V_{s_C}(d)`, which holds at position 1: `(v_ℓ)₁ = s_L`, while every `v ∈ V_{s_C}(d)` has `(v)₁ = s_C` (S8a), and `s_L ≠ s_C` (SC-NEQ, ASN-0093). Both halves are discharged in full in the S2 verification of the post-state invariants below.

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

After MAKELINK, this biconditional holds at the post-state for every `d ∈ dom(Σ'.M)`. The link is discoverable from every document whose arrangement reaches into any of its endset coverages.

The abstract specification requires no auxiliary index state. The implementation may maintain an auxiliary structure — a reverse lookup from I-addresses to link addresses, the *spanfilade* in Gregory's implementation — for efficient computation. Such structures are caches: any state where they are consistent with `L` and `M` produces the same `project` and `discoverable_from` results. The abstract claim is the discovery *property*; the index is a performance choice.

This is the abstract content of what Nelson calls the system's "inter-indexing mechanisms": the mechanisms exist for performance; the discoverability is mathematical.

## Discoverability Is Symmetric

A consequence worth recording: the home document has no privileged position in discovery. By LP12, any document whose arrangement reaches `coverage(eᵢ)` for any `i` becomes a source from which `ℓ` is discoverable. The home document is one such document only if its own arrangement happens to reach into the endsets' coverages.

This realizes Nelson's intent that all parties reaching a link's endpoints — including any third document transcluding either endpoint's content — discover it by querying their own content; the home document holds the link for ownership and naming only.

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

*Reflexive variant.* We exhibit M-Reflexive concretely. Replace `e₁` with `e₁' = {(ℓ, δ(1, #ℓ))}`, keeping `e₂` and `e₃` (the caller computes `ℓ = [d, 0, 2, 1]` from `Σ` via `A_L(d)`'s deterministic first-emission rule). By PrefixSpanCoverage (ASN-0043), `coverage(e₁') = {t ∈ T : ℓ ≼ t}`, which contains `ℓ`. After MAKELINK, `Σ'.M(d) = {[1, 1] ↦ a₁, [1, 2] ↦ a₂, [2, 1] ↦ ℓ}` and `Σ'.L(ℓ).e₁ = e₁'`. Prefix-testing each image of `dom(Σ'.M(d))` against `ℓ`: `ℓ ⋠ a₁` and `ℓ ⋠ a₂` (different position-7 component), `ℓ ≼ ℓ` trivially. Hence `project(ℓ, 1, d, Σ') = {v_ℓ}` and `discoverable_from(ℓ, d, Σ')` holds (M-Reflexive).

## Weakest Precondition for Discoverability

We compute `wp(MAKELINK, discoverable_from(ℓ, d_target, ·))` — the predicate on the pre-state `Σ` (parametrized by the input endsets `(e₁, ..., eₙ)` and the choice of `d_target`) that ensures the post-state satisfies `discoverable_from(ℓ, d_target, Σ')`.

*Operation enabledness.* We follow the foundation's wp convention (LP12a, ASN-0098), which writes wp as `enabled(op) ∧ …` — conjoining the operation's applicability predicate so that the result is the weakest precondition for *total* correctness (a post-state must exist for the postcondition to be assertable). For MAKELINK the applicability predicate is exactly the caller-visible precondition M-Pre, namely the conjunction of home-document allocation and endset validity:

  enabled(MAKELINK)  ≡  d ∈ dom(Σ.M)  ∧  N ≥ 3  ∧  (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset)  ∧  e₃ ≠ ∅

Unless `enabled(MAKELINK)` holds at `Σ`, no post-state `Σ'` exists (K.λ's precondition fails), and `discoverable_from(ℓ, d_target, Σ')` is not assertable. The predicate concerns the *home* document `d` and the endset inputs, and is logically independent of the target document `d_target`.

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

As a wp (the membership clause subsumed by `enabled(MAKELINK)` here, since `d_target = d`):

  wp(MAKELINK, discoverable_from(ℓ, d, ·))
    ≡  enabled(MAKELINK)  ∧  [(E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅) ∨ (E i :: ℓ ∈ coverage(eᵢ))]

*Reduction under standard authoring.* When every input endset satisfies `StandardAuthoring(eᵢ, Σ)`, the reflexive route's disjunct `(E i :: ℓ ∈ coverage(eᵢ))` is unreachable (M-Reflexive). The wp collapses:

  wp(MAKELINK, discoverable_from(ℓ, d, ·))
    ≡  enabled(MAKELINK)  ∧  (E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)

— the same shape as Case 1 (with `d_target := d`; the two enabledness-and-membership conjuncts coincide there into `enabled(MAKELINK)`, since the home and target documents are one). Under standard authoring, home-document discoverability requires `d`'s arrangement to reach into some endset's coverage; there is no automatic "self-discovery" of `ℓ` from `d` (M-DiscSymmetry).

## Reflexive Endsets

L13 (ReflexiveAddressing, ASN-0043) permits link addresses as valid endset targets — a link's endsets may cover other link addresses, or even cover the link's own address. We consider the case where one of MAKELINK's input endsets has coverage containing `ℓ` itself.

*Reflexive coverage is structurally excluded under standard authoring.* When every input endset satisfies `StandardAuthoring(eᵢ, Σ)`, K.λ's freshness gives `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)`, and standard authoring confines every `coverage(eᵢ)` to `dom(Σ.C) ∪ dom(Σ.L)`, so `ℓ ∉ coverage(eᵢ)` for every `i`. The exclusion is structural, not epistemic (see StandardAuthoring): `A_L(d)`'s next emission is fully deterministic from the current state (`[d, 0, s_L, 1]` for the first emission, `inc(max{ℓ' : origin(ℓ') = d}, 0)` otherwise), so a client with state access can compute `ℓ` in advance, and the substrate provides no architectural barrier against deliberately constructed reflexive coverage. The structural defense above is the only substrate-level guarantee.

*A reflexive endset yields guaranteed home-document discovery at the post-state.* Suppose `ℓ ∈ coverage(eᵢ)` for some `i ∈ {1, ..., N}`. After MAKELINK, `Σ'.M(d)(v_ℓ) = ℓ ∈ coverage(Σ'.L(ℓ).eᵢ)` (by K.λ's effect `Σ_mid.L(ℓ) = (e₁, ..., eₙ)` and K.μ⁺_L's frame `Σ'.L = Σ_mid.L`, so `Σ'.L(ℓ).eᵢ = eᵢ` and `coverage(Σ'.L(ℓ).eᵢ) = coverage(eᵢ)`). Hence `v_ℓ ∈ project(ℓ, i, d, Σ')`, giving `discoverable_from(ℓ, d, Σ')`. The home document's reflexive discovery is forced regardless of `Σ.M(d)`'s pre-existing arrangement.

*No reflexive discovery from other documents.* For `d_target ≠ d`, K.μ⁺_L's frame leaves `Σ.M(d_target)` unchanged: `ran(Σ'.M(d_target)) = ran(Σ.M(d_target))`. The address `ℓ` enters only `d`'s arrangement, so only `d`'s `discoverable_from` query benefits from the reflexive endset. Other documents must rely on their own arrangement-reach into `coverage(eᵢ)` to discover `ℓ`. LP12 covers the reflexive case uniformly via the witness `v_ℓ ↦ ℓ ∈ ran(Σ'.M(d))`, with no special-case rule (M-DiscSymmetry).

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

The side effect can only occur when `ℓ'` was authored with an endset whose span coverage extends to addresses not yet allocated at authoring time. Such forward-reaching endsets are permitted by L4 (EndsetGenerality, ASN-0043) — endset spans may reference any addresses in the tumbler space, including those not currently in `dom(C) ∪ dom(L)`. MAKELINK's allocation of `ℓ` "fills in" a previously-uncovered region of the address space, retroactively activating any prior endset that had pre-emptively claimed it. When `ℓ'` was authored under standard authoring at its own authoring state — `StandardAuthoring(Σ.L(ℓ').eᵢ, Σ_{ℓ'})` holds at the state `Σ_{ℓ'}` at which `ℓ'` was incorporated, so `coverage(Σ.L(ℓ').eᵢ) ⊆ dom(Σ_{ℓ'}.C) ∪ dom(Σ_{ℓ'}.L)` — no such endset can cover the future fresh `ℓ`, and the side effect is vacuous. The transfer of `ℓ`'s freshness backward from the K.λ allocation state `Σ_ℓ` to the authoring state `Σ_{ℓ'}` (where `Σ_{ℓ'} →* Σ_ℓ`) uses Store Monotonicity★ (ASN-0098): `dom(Σ_{ℓ'}.C) ∪ dom(Σ_{ℓ'}.L) ⊆ dom(Σ_ℓ.C) ∪ dom(Σ_ℓ.L)`, so K.λ's freshness `ℓ ∉ dom(Σ_ℓ.C) ∪ dom(Σ_ℓ.L)` yields `ℓ ∉ dom(Σ_{ℓ'}.C) ∪ dom(Σ_{ℓ'}.L)`; chaining with the standard-authoring inclusion at `Σ_{ℓ'}` gives `ℓ ∉ coverage(Σ.L(ℓ').eᵢ)`. The temporal direction of the inclusion is load-bearing — freshness at `Σ_ℓ` is propagated *backward* to `Σ_{ℓ'}`, which is precisely what Store Monotonicity★ supplies.

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

L1c (structural inc-chain conformance) requires an inc-chain from `origin(ℓ) = d` to `ℓ`. We discharge it by the same transfer discipline used for freshness above, and for the same reason: ASN-0093 already establishes a T10a-conforming chain for *every* emission of `A_L(d)` (ChainMembershipForOrigin and ChainDiscipline place `ℓ` on `d`'s link sub-allocator chain `A_L(d) = S(b_L(d), 1)`, ChainElementT4Validity carries T4-validity along it, and the `k₁ = 2`, `#tᵢ > #origin(ℓ)` clauses are part of ASN-0093's own L1c statement). MAKELINK introduces no allocation step beyond the K.λ it composes, so the conformance result transfers verbatim — no re-derivation of the chain is needed. ✓

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

For D-SEQ★: by D-SEQ★ at `Σ`, `V_{s_L}(d) = {[s_L, 1, ..., 1, k] : 1 ≤ k ≤ n_L}` of common depth `m_L(d)` for some `n_L ≥ 0` (with `n_L = 0` meaning the link subspace at `d` is empty). If `n_L = 0`, the K.μ⁺_L positioning rule gives `v_ℓ = [s_L, 1, ..., 1]` of the chosen depth `m ≥ 2`, so `V_{s_L}(d') = {v_ℓ}` — a contiguous initial segment of cardinality 1, fixing `m_L(d') = m`. If `n_L ≥ 1`, the rule gives `v_ℓ = shift(max(V_{s_L}(d)), 1) = [s_L, 1, ..., 1, n_L + 1]` at depth `m_L(d)`, so `V_{s_L}(d') = {[s_L, 1, ..., 1, k] : 1 ≤ k ≤ n_L + 1}` — a contiguous initial segment of cardinality `n_L + 1`. Either way, the post-state set conforms to D-SEQ★. ✓

For S8★: per ASN-0047's S8★, the link-subspace projected arrangement `M'(d)|_{V_{s_L}(d')} : V_{s_L}(d') → dom(L')` admits the trivial length-1 decomposition `{(v, M'(d)(v), 1) : v ∈ V_{s_L}(d')}`. The new entry `(v_ℓ, ℓ, 1)` joins this decomposition; S8's conditions (a) and (b) hold trivially at length 1. ✓

For state components unchanged by MAKELINK (`C`, `E`, `R`) and for the document-set `dom(M)`, the remaining per-state invariants are preserved:

- M0 (DocumentTumblerWellFormed, ASN-0093): preserved because the document set is unchanged — `dom(Σ'.M) = dom(Σ.M)` (MAKELINK allocates no new document, only a new V-position within an already-allocated document); every `d ∈ dom(Σ'.M)` satisfies M0 by inheritance from `Σ`.
- S4 (origin-based identity for content addresses, ASN-0036): preserved by inheritance (no new `dom(C)` entries) since `Σ'.C = Σ.C`; the lemma's content is fixed by the existing content-allocation events, and MAKELINK introduces none.
- L11a (link uniqueness, ASN-0043): the new allocation event for `ℓ` is distinct from every prior link allocation event (by ChainEnumerationInjectivity, DisjointSubAllocatorChains, and Cross-doc disjointness — see "Freshness of the Allocation"), so L11a's distinctness conclusion holds at `Σ'`.
- S7a, S7b (origin and structural attribution for content addresses): preserved by inheritance (no new `dom(C)` entries) since `Σ'.C = Σ.C`; the predicates quantify over `dom(C)`, which is unchanged, so every existing content address retains its attribution and no new content address arises to verify.
- S7d (DocumentAllocationDiscipline, ASN-0036): preserved because the document set is unchanged. S7d quantifies over *document tumblers* (each `d` has `zeros(d) = 2`, arises from a distinct allocation event, and distinct documents have distinct tumblers) — *not* over `dom(C)`. MAKELINK registers no new document (`dom(Σ'.M) = dom(Σ.M)` under K.λ and K.μ⁺_L), so the predicate carries over from `Σ` unchanged.
- C1b (content element-field depth), C1c (content allocator conformance): preserved by inheritance (no new `dom(C)` entries) since `Σ'.C = Σ.C`; both quantify over `dom(C)`, which is unchanged, so MAKELINK introduces no content address against which to verify them.
- C-fin (content store finiteness): preserved since `dom(Σ'.C) = dom(Σ.C)` is finite at `Σ`.
- P6 (existential coherence), P7 (provenance grounding): preserved by inheritance since `dom(C)`, `dom(M)`, and `R` are unchanged in the relevant respects (`dom(M)` grows only by new V-positions within an already-allocated document, not by new documents; `R` is unchanged), so every existing content/provenance instance is carried over and no new instance arises.
- P8 (entity hierarchy): preserved by inheritance (no new `E` entries) since `E` is unchanged.
- NodeLineage (descent from bootstrap), ActivatedEmission (every non-node entity emitted by an activated sub-allocator): preserved by inheritance (no new `E` entries) since `Σ'.E = Σ.E`; both quantify over `E`, which MAKELINK leaves unchanged.

### Composite-Boundary Properties

ASN-0047 classifies P4★, P4a, and P7a as Class (b) — properties discharged at composite boundaries by the coupling constraints J0, J1★, J1'★. MAKELINK introduces a single link-subspace V-arrangement entry. The three coupling constraints are vacuously satisfied — but for *structurally distinct* reasons, which we discharge separately:

- *J0 (AllocationRequiresPlacement):* J0 quantifies over `dom(Σ'.C) ∖ dom(Σ.C)` — content addresses freshly allocated across the composite. MAKELINK's frame `Σ'.C = Σ.C` gives `dom(Σ'.C) ∖ dom(Σ.C) = ∅`. J0 holds by emptiness of the quantification universe.
- *J1★ (ExtensionRecordsProvenanceContentSubspace):* J1★ quantifies over content-subspace V-positions whose image changes across the composite. The only new V-position is `v_ℓ` with `subspace(v_ℓ) = s_L`, and `s_L ≠ s_C` (SC-NEQ, ASN-0093). For every `v ∈ dom(Σ.M(d))`, `Σ'.M(d)(v) = Σ.M(d)(v)` by K.μ⁺_L's effect, so no prior V-position's image changed. The quantification `(E v ∈ dom(Σ'.M(d)) : subspace(v) = s_C ∧ Σ'.M(d)(v) = a) ∧ ¬(E v ∈ dom(Σ.M(d)) : subspace(v) = s_C ∧ Σ.M(d)(v) = a)` requires a *new* content-subspace witness; none exists, since `v_ℓ`'s subspace is `s_L`. J1★ holds by absence of content-subspace witnesses.
- *J1'★ (ProvenanceRequiresExtensionContentSubspace):* J1'★ quantifies over `R' ∖ R`. MAKELINK's frame `Σ'.R = Σ.R` gives `R' ∖ R = ∅`. J1'★ holds by emptiness of the quantification universe.

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

## Atomicity

MAKELINK is a *composite* of two atomic transitions. Each component is atomic by SequentialTransitionAxiom (ASN-0093). The composite is not.

In the intermediate state `Σ_mid` between K.λ and K.μ⁺_L:

- `ℓ ∈ dom(Σ_mid.L)` with value `Σ_mid.L(ℓ) = (e₁, ..., eₙ)` — the link exists, with its endsets recorded.
- `ℓ ∉ ran(Σ_mid.M(d))` — the link is not yet visible in any V-arrangement (derived in Preconditions).
- `discoverable_from(ℓ, d_target, Σ_mid)` is well-defined for every `d_target ∈ dom(Σ_mid.M) = dom(Σ.M)` since `ℓ ∈ dom(Σ_mid.L)` and `Σ_mid.L(ℓ) = (e₁, ..., eₙ)`.

`Σ_mid` is a fully reachable state, not a transitional artifact: by SequentialTransitionAxiom (ASN-0093), K.λ commits before K.μ⁺_L begins, so K.λ on `Σ` yields a complete state `Σ_mid` against which K.μ⁺_L's precondition is evaluated. K.λ is an atomic substrate operation that ASN-0093/ASN-0047 establish to preserve the per-state invariants on reachable states, so `Σ_mid` inherits them — the link exists in `dom(L)` with its endsets recorded but is unplaced in `M(d)`. The only content new at `Σ_mid` relative to `Σ` is this unplaced link.

We compare discoverability at `Σ_mid` and `Σ'`. By LP12:

  Σ_mid:  discoverable_from(ℓ, d_target, Σ_mid)  ⟺  (E i :: coverage(eᵢ) ∩ ran(Σ_mid.M(d_target)) ≠ ∅)
  Σ':     discoverable_from(ℓ, d_target, Σ')     ⟺  (E i :: coverage(eᵢ) ∩ ran(Σ'.M(d_target)) ≠ ∅)

For `d_target ≠ d`, K.μ⁺_L's frame gives `Σ'.M(d_target) = Σ_mid.M(d_target)`, so the two values coincide. For `d_target = d`, the post-state arrangement gains `ℓ`: `ran(Σ'.M(d)) = ran(Σ_mid.M(d)) ∪ {ℓ}`. The two values differ precisely when some endset `eᵢ` *reflexively* covers `ℓ`: if `ℓ ∈ coverage(eᵢ)` for some `i`, then `discoverable_from(ℓ, d, Σ')` is forced true via `v_ℓ` while `discoverable_from(ℓ, d, Σ_mid)` may be false (M-Reflexive). Outside the reflexive case, the value of `discoverable_from(ℓ, d, ·)` agrees at `Σ_mid` and `Σ'`.

The substrate provides no composite-level atomicity. A reader observing `Σ_mid` would see the link in `dom(L)` but not in `M(d)`. If this intermediate visibility is undesirable — if MAKELINK must appear as a single event — the protocol layer above must enforce it, typically by sequencing both atomic transitions within a single request-response cycle.

Nelson's "canonical operating condition" language suggests external atomicity is expected: MAKELINK is presented to the client as one event, and the system must be canonical at the response. This is a *protocol-level* guarantee, not a substrate-level one. The strand model does not, by itself, supply it.

## Permanence

The link's identity and value are permanent (L12, LP13, LP3★) — established in *Permanence of the Recording*. What remains to characterize is the V-position binding `v_ℓ ↦ ℓ` in the home document, which is less permanent — but the *only* mutation available to it is removal. K.μ~ (reordering) cannot rebind it: by K.μ~'s admissibility clause (v), *link-subspace fixing* (ASN-0047), the witnessing bijection satisfies `π(v) = v` for every link-subspace V-position `v ∈ dom_L(M(d))`. Since `v_ℓ` is a link V-position, `π(v_ℓ) = v_ℓ`, and the bijection equation gives `M'(d)(v_ℓ) = M(d)(v_ℓ) = ℓ`; the binding `v_ℓ ↦ ℓ` is therefore *invariant* under every K.μ~ transition. The link subspace is fixed pointwise by reordering. The sole operation that can alter the binding is K.μ⁻ (contraction), which may drop `v_ℓ` from `dom(M(d))` entirely. Thus what is permanent is the link's I-address and value; what is mutable — and only by removal, never by re-binding — is whether `v_ℓ ↦ ℓ` remains present in the home document's link-subspace arrangement. This separation of permanent I-stream content (the link's identity and value, L12) from mutable V-stream arrangement (the placement of `v_ℓ`, which only K.μ⁻ can withdraw) is the content/arrangement split that P3 (ArrangementMutabilityOnly, ASN-0047) names: arrangement `M` is the only state component that can lose information, while `L` is immutable.

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
| M-DepthConv | MAKELINK fixes the V-position depth of every first link it places at the canonical minimal `m = 2` (`Σ` leaves `m` free, since K.μ⁺_L admits any `m ≥ 2`); thereafter S8-depth pins `m_L(d) = 2`. Scoped universal: for any `d` whose every link V-position was placed by MAKELINK, `m_L(d) = 2`. Not a system-wide invariant. | introduced |
| M-Pre | Caller-visible precondition: `d ∈ dom(M)`, `N ≥ 3`, `(A i : eᵢ ∈ Endset)`, `e₃ ≠ ∅`. System-supplied parameters: `ℓ` from `A_L(d)`'s next emission; `v_ℓ` from K.μ⁺_L's positioning rule, serial component `n_L + 1` computed from `Σ`, depth per M-DepthConv. | introduced |
| M-Alloc | MAKELINK allocates a fresh `ℓ ∈ T \ (dom(Σ.L) ∪ dom(Σ.C))` and a fresh `v_ℓ ∈ T \ dom(Σ.M(d))` with `subspace(v_ℓ) = s_L` and `#v_ℓ` per M-DepthConv. | introduced |
| M-Effect | `Σ'.L = Σ.L ∪ {ℓ ↦ (e₁, ..., eₙ)}`; `Σ'.M(d) = Σ.M(d) ∪ {v_ℓ ↦ ℓ}` where `v_ℓ = [s_L, 1]` if `V_{s_L}(d) = ∅` at `Σ`, else `v_ℓ = shift(max(V_{s_L}(d)), 1)` (with `n_L = |V_{s_L}(d)|`); depth per M-DepthConv. | introduced |
| M-Frame | `Σ'.C = Σ.C`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`; existing entries in `L` and in `M(d')` for `d' ≠ d` are unchanged. | introduced |
| M-NoContentEffect | For every `a ∈ dom(Σ.C)`: `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`. The referenced content is byte-identical before and after MAKELINK. | introduced |
| M-DiscSymmetry | Discoverability of `ℓ` is symmetric across all documents whose arrangements reach into any endset coverage; the home document has no privileged role in LP12's definition. Any asymmetry of outcome reflects asymmetry of arrangement-reach, not a privileged status. | introduced |
| StandardAuthoring | `StandardAuthoring(e, Σ) ≡ coverage(e) ⊆ dom(Σ.C) ∪ dom(Σ.L)` — a structural predicate on endset values at a state. A link's endset sequence is standardly authored at `Σ` iff every constituent endset satisfies the predicate. This is the named discipline cited by M-Reflexive, M-WP, and the cascade-vacuity discussion. | introduced |
| M-Reflexive | If `ℓ ∈ coverage(eᵢ)` for some `i` (the reflexive endset case), then `v_ℓ ∈ project(ℓ, i, d, Σ')` and `discoverable_from(ℓ, d, Σ')` is forced true regardless of `Σ.M(d)`'s pre-existing arrangement. Under `(A i : StandardAuthoring(eᵢ, Σ))` the reflexive case is structurally excluded (derivation in *Reflexive Endsets*). | introduced |
| M-PriorLinkDisc | For every prior link `ℓ' ∈ dom(Σ.L)`: from the home document `d`, `discoverable_from(ℓ', d, Σ') ⟺ discoverable_from(ℓ', d, Σ) ∨ (E i :: ℓ ∈ coverage(Σ.L(ℓ').eᵢ))` — newly discoverable precisely when some endset of `ℓ'` covers `ℓ`; from any `d_target ≠ d`, `discoverable_from(ℓ', d_target, Σ') = discoverable_from(ℓ', d_target, Σ)`. The side-effect window is confined to the home document. Composition across MAKELINK sequences preserves all per-state invariants (LP9, LP13, L12). | introduced |
| M-WP | Post-MAKELINK discoverability has explicit weakest preconditions (total correctness): for `d_target ≠ d`, `wp ≡ enabled(MAKELINK) ∧ d_target ∈ dom(Σ.M) ∧ (E i :: coverage(eᵢ) ∩ ran(Σ.M(d_target)) ≠ ∅)`; for `d_target = d`, `wp ≡ enabled(MAKELINK) ∧ [(E i :: coverage(eᵢ) ∩ ran(Σ.M(d)) ≠ ∅) ∨ (E i :: ℓ ∈ coverage(eᵢ))]`. Under `(A i : StandardAuthoring(eᵢ, Σ))` the reflexive disjunct collapses and the two shapes coincide. | introduced |
| M-Perm | After MAKELINK: `(A Σ' →* Σ'' :: ℓ ∈ dom(Σ''.L) ∧ Σ''.L(ℓ) = Σ'.L(ℓ))`, by LP13. | introduced |
| M-NoIndexState | The abstract specification requires no separate index state component. Discoverability is computed from `L` and `M` via the projection function of ASN-0098. | introduced |
| M-CompAtomicity | The composite is not atomic at the substrate level. The intermediate state `Σ_mid` between K.λ and K.μ⁺_L has the link allocated but not placed. `discoverable_from(ℓ, d_target, ·)` agrees at `Σ_mid` and `Σ'` for every `d_target ≠ d`; for `d_target = d` the two values agree unless some endset reflexively covers `ℓ`. Composite-level atomicity, if required, belongs to the protocol layer above the substrate. | introduced |
| M-Inv-State | *Per-state invariants at `Σ'`.* The post-state satisfies the link-store invariants (L0, L1, L1a, L1b, L1c, L3, L14, L-fin), the arrangement invariants (S2, S3★, S3★-aux, S8a, S8-depth, S8-fin, S8★, CL-OWN, CL-UNIQ, D-MIN★, D-CTG★, D-SEQ★), and the frame-inherited invariants over unchanged domains (S4, S7a, S7b, S7d, C1b, C1c, C-fin, P6, P7, P8, M0, NodeLineage, ActivatedEmission). The grouping by frame is given in *Invariant Preservation*. | introduced |
| M-Inv-Bdry | *Composite-boundary properties at `Σ'`.* P4★, P4a, P7a hold at `Σ'` — all preserved because `R' = R`, `dom(Σ'.C) = dom(Σ.C)`, and the new V-arrangement entry is link-subspace (so it does not enter `Contains_C(Σ')`). The three coupling constraints are discharged separately: J0 by `dom(Σ'.C) ∖ dom(Σ.C) = ∅` (frame on `C`); J1★ by `subspace(v_ℓ) = s_L ≠ s_C` (structural, the new V-position fails J1★'s content-subspace filter); J1'★ by `R' ∖ R = ∅` (frame on `R`). | introduced |
| M-Inv-Trans | *Transition invariants for `Σ → Σ'`.* M1, L12, P0, P1, P2 hold, and P3 (= P0 ∧ P1 ∧ P2 ∧ L12) holds as their conjunction. Each conjunct is discharged trivially by the frames `Σ'.C = Σ.C`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`, and L12 by K.λ adding only the fresh `ℓ`. | introduced |

## Open Questions

What well-formedness constraints, beyond `e₃ ≠ ∅`, must endsets satisfy when their spans reference I-addresses not currently in `dom(C)` or `dom(L)`?

At what abstraction layer is MAKELINK's composite-level atomicity guaranteed, and what mechanism enforces it?

Must MAKELINK distinguish between two invocations producing links with identical endset values, beyond the necessary distinctness of their I-addresses?

Must MAKELINK's discoverability guarantee hold at the precise post-state of the operation, or is a deferred-consistency model admissible?

When MAKELINK's endsets reference content in documents not yet allocated, what discoverability properties become available once that content is later created?

Under what conditions may a link's V-position move within the home document's link subspace by subsequent operations, and what discoverability properties does such movement preserve?

What abstract guarantee distinguishes a "properly created" link visible in its home document's arrangement from a link allocated but not placed?

What invariants must hold for a link whose type endset references content at an address that will never be allocated, and what does discoverability mean in that limiting case?
