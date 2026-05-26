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

## Decomposition

We observe that link creation must accomplish two distinct effects: (i) introduce the link into `dom(L)` with its value recorded, and (ii) make the link visible in the home document's arrangement. The substrate (ASN-0093, ASN-0047) provides exactly two atomic operations matching this division:

- `K.λ` allocates the link in `dom(L)`, binding it to the given endsets.
- `K.μ⁺_L` extends `M(d)` in the link subspace, mapping a fresh V-position to the link.

We therefore identify MAKELINK as the composite `K.λ ⊕ K.μ⁺_L` applied to the same home document. The order is forced: K.μ⁺_L's precondition requires `ℓ ∈ dom(L)`, so K.λ must precede it.

Why must MAKELINK include K.μ⁺_L? The substrate's coupling constraints (J0, J1★, J1'★ from ASN-0047) do not require it — they apply only to content-subspace allocations. But Nelson's design is explicit that a document "consists of its contents and its out-links" — retrieval of the home document's arrangement must yield the link. By L14a's supersession (ASN-0047), the link subspace of the home document's arrangement is where links live in V-space; K.μ⁺_L is what places them there. Without K.μ⁺_L, the link would be allocated but invisible to any retrieval framed against its home document's arrangement.

## Preconditions

The composite is valid when its component preconditions hold. For K.λ at `Σ`:

  d ∈ dom(M)
  ℓ ∉ dom(C) ∪ dom(L)
  zeros(ℓ) = 3 ∧ E(ℓ)₁ = s_L ∧ #E(ℓ) ≥ 2 ∧ origin(ℓ) = d
  ℓ is produced by A_L(d) (first emission if d has no prior links; otherwise inc(ℓ_prev, 0))
  N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅

For K.μ⁺_L at the intermediate state `Σ_mid` after K.λ:

  d ∈ dom(M)             [preserved by K.λ's frame on dom(M)]
  ℓ ∈ dom(L)             [established by K.λ]
  origin(ℓ) = d           [established by K.λ]
  ℓ ∉ ran(M(d))           [from ℓ ∉ dom(L) at Σ and K.λ's frame (A d :: M'(d) = M(d))]
  v_ℓ at the next link-subspace position per D-MIN★ / D-CTG★, depth m_L = 2

The intermediate-state conditions for K.μ⁺_L reduce to original-state conditions, so the caller-visible precondition for MAKELINK is just K.λ's precondition, with `ℓ` supplied by `A_L(d)`'s next emission and `v_ℓ` determined by the link subspace's current cardinality.

## Effect

We summarize the composite state transition. Writing the post-state as `Σ'`:

  Σ'.L  =  Σ.L ∪ {ℓ ↦ (e₁, ..., eₙ)}
  Σ'.M(d)  =  Σ.M(d) ∪ {v_ℓ ↦ ℓ}

Other components are unchanged:

  Σ'.C  =  Σ.C
  Σ'.E  =  Σ.E                                          [no entity allocation]
  Σ'.R  =  Σ.R                                          [provenance applies to content subspace only]
  (A ℓ' ∈ dom(Σ.L) :: Σ'.L(ℓ') = Σ.L(ℓ'))               [L12]
  (A d' ∈ dom(Σ.M), d' ≠ d :: Σ'.M(d') = Σ.M(d'))

## Freshness of the Allocation

The address `ℓ` is genuinely new. The argument proceeds in three layers.

*Within d's link chain.* By ChainEnumerationInjectivity (ASN-0093), the chain `A_L(d) = (t_1, t_2, ...)` is strictly monotone under T1. Each K.λ event on `A_L(d)` consumes the next index in the chain, so `ℓ ≠ t_k` for any `k ≤ n_d` where `n_d` is the current count of links with `origin(·) = d`.

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

## What Does Not Change

The frame `Σ'.C = Σ.C` is total: every `a ∈ dom(Σ.C)` satisfies `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`. The referenced content is byte-identical before and after MAKELINK.

This is not a separate guarantee. It is a direct consequence of the composite's structure: K.λ modifies only `L`, and K.μ⁺_L modifies only `M(d)`. Neither operation touches `C`. The link's endsets *reference* I-addresses in `dom(C)`, but referencing is read-only — the endset stores spans (start, length pairs), not the bytes at those addresses. The bytes remain where they were.

By the same reasoning, no prior link in `dom(L)` is modified (L12), no other document's arrangement is modified (frame on `M`), no entity is allocated, no provenance pair is recorded.

The phenomenology Nelson describes — that creating a link has zero effect on the content it references — falls out of the architecture: ownership of the link belongs to the home document; the link's storage is in the home document's element subspace; writing into the home document's element subspace cannot, by structure, modify content at I-addresses elsewhere. The guarantee is structural, not behavioral.

## Invariant Preservation

We verify the post-state `Σ'` satisfies the substrate invariants. The new entries are `ℓ ∈ dom(L)` and `v_ℓ ∈ dom(M(d))`; prior entries are unchanged by the frame.

For the link itself:

  L0:    E(ℓ)₁ = s_L                          from K.λ precondition
  L1:    zeros(ℓ) = 3                          from K.λ precondition
  L1a:   origin(ℓ) = d ∈ dom(Σ'.M)             from K.λ precondition and M1
  L1b:   #E(ℓ) ≥ 2                             from K.λ precondition
  L1c:   structural inc-chain conformance      from SubAllocatorAxiom.ChainDiscipline
  L3:    N ≥ 3 ∧ e₃ ≠ ∅                       from K.λ precondition
  L12:   immutability                          new entry only; no modification of prior
  L14:   store disjointness                    ℓ ∉ dom(C) from K.λ freshness
  L-fin: link store finiteness                 |dom(L')| = |dom(L)| + 1

For the V-arrangement entry:

  S3★:    image of v_ℓ is ℓ ∈ dom(L')          direct from the effect
  CL-OWN: origin(M'(d)(v_ℓ)) = origin(ℓ) = d  direct from K.λ precondition
  CL-UNIQ: partial injection preserved         K.μ⁺_L first-arrangement guard ℓ ∉ ran(M_mid(d))
  D-MIN★: v_ℓ at minimum if empty              K.μ⁺_L positioning rule
  D-CTG★: extension is contiguous              K.μ⁺_L positioning rule

For state components unchanged by MAKELINK (C, E, R), the invariants P0, P1, P2, P4★, P6, P7, P8 are preserved trivially.

## Atomicity

MAKELINK is a *composite* of two atomic transitions. Each component is atomic by SequentialTransitionAxiom (ASN-0093). The composite is not.

In the intermediate state `Σ_mid` between K.λ and K.μ⁺_L:

- `ℓ ∈ dom(Σ_mid.L)` with value `Σ_mid.L(ℓ) = (e₁, ..., eₙ)` — the link exists, with its endsets recorded.
- `ℓ ∉ ran(Σ_mid.M(d))` — the link is not yet visible in any V-arrangement.
- `discoverable_from(ℓ, d, Σ_mid)` is computable, and may or may not hold depending on the endsets and the pre-MAKELINK arrangements (its value at `Σ_mid` is the same as at the pre-state for every `d`, since `Σ_mid.M = Σ.M`).

The substrate provides no composite-level atomicity. A reader observing `Σ_mid` would see the link in `dom(L)` but not in `M(d)`. If this intermediate visibility is undesirable — if MAKELINK must appear as a single event — the protocol layer above must enforce it, typically by sequencing both atomic transitions within a single request-response cycle.

Nelson's "canonical operating condition" language suggests external atomicity is expected: MAKELINK is presented to the client as one event, and the system must be canonical at the response. This is a *protocol-level* guarantee, not a substrate-level one. The strand model does not, by itself, supply it.

## Permanence

By LP13 (ASN-0098), the link persists unconditionally:

  (A reachable Σ' →* Σ'' :: ℓ ∈ dom(Σ''.L) ∧ Σ''.L(ℓ) = Σ'.L(ℓ))

No transition in the substrate's vocabulary removes `ℓ` from `dom(L)` or modifies `L(ℓ)`. The link is permanent in the strongest sense: its identity, its value, and its home are all immutable for the life of the system.

The link's V-position `v_ℓ` in the home document is less permanent. Subsequent operations may remove it (per the contraction operation's rules) or reassign it (per the reordering operation's rules). What is permanent is the link's I-address and value; what is mutable is the link's V-position in the home document's arrangement. This is S9 (TwoStreamSeparation, ASN-0036) specialized to the link subspace.

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
| M-Comp | MAKELINK is the composite `K.λ ⊕ K.μ⁺_L`, in that order, applied to the same home document `d`. | introduced |
| M-Pre | Caller-visible precondition: `d ∈ dom(M)`, `N ≥ 3`, `(A i : eᵢ ∈ Endset)`, `e₃ ≠ ∅`. System-supplied parameters: `ℓ` from `A_L(d)`'s next emission, `v_ℓ` from K.μ⁺_L's positioning rule. | introduced |
| M-Alloc | MAKELINK allocates a fresh `ℓ ∈ T \ (dom(Σ.L) ∪ dom(Σ.C))` and a fresh `v_ℓ ∈ T \ dom(Σ.M(d))` with `subspace(v_ℓ) = s_L`. | introduced |
| M-Effect | `Σ'.L = Σ.L ∪ {ℓ ↦ (e₁, ..., eₙ)}`; `Σ'.M(d) = Σ.M(d) ∪ {v_ℓ ↦ ℓ}`. | introduced |
| M-Frame | `Σ'.C = Σ.C`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`; existing entries in `L` and in `M(d')` for `d' ≠ d` are unchanged. | introduced |
| M-NoContentEffect | For every `a ∈ dom(Σ.C)`: `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`. The referenced content is byte-identical before and after MAKELINK. | introduced |
| M-Disc | After MAKELINK: `discoverable_from(ℓ, d_target, Σ') ⟺ (E i : coverage(Σ'.L(ℓ).eᵢ) ∩ ran(Σ'.M(d_target)) ≠ ∅)`, by LP12. | introduced |
| M-DiscSymmetry | Discoverability of `ℓ` is symmetric across all documents whose arrangements reach into any endset coverage; the home document has no privileged role in discovery. | introduced |
| M-Perm | After MAKELINK: `(A Σ' →* Σ'' :: ℓ ∈ dom(Σ''.L) ∧ Σ''.L(ℓ) = Σ'.L(ℓ))`, by LP13. | introduced |
| M-NoIndexState | The abstract specification requires no separate index state component. Discoverability is computed from `L` and `M` via the projection function of ASN-0098. | introduced |
| M-CompAtomicity | The composite is not atomic at the substrate level. The intermediate state `Σ_mid` between K.λ and K.μ⁺_L has the link allocated but not placed. Composite-level atomicity, if required, belongs to the protocol layer above the substrate. | introduced |
| M-Inv | The post-state `Σ'` satisfies L0, L1, L1a, L1b, L1c, L3, L12, L14, L-fin, S3★, CL-OWN, CL-UNIQ, D-MIN★, D-CTG★, and all unchanged-component invariants (P0, P1, P2, P4★, P6, P7, P8). | introduced |

## Open Questions

What well-formedness constraints, beyond `e₃ ≠ ∅`, must endsets satisfy when their spans reference I-addresses not currently in `dom(C)` or `dom(L)`?

At what abstraction layer is MAKELINK's composite-level atomicity guaranteed, and what mechanism enforces it?

Must MAKELINK distinguish between two invocations producing links with identical endset values, beyond the necessary distinctness of their I-addresses?

Must MAKELINK's discoverability guarantee hold at the precise post-state of the operation, or is a deferred-consistency model admissible?

When MAKELINK's endsets reference content in documents not yet allocated, what discoverability properties become available once that content is later created?

Under what conditions may a link's V-position move within the home document's link subspace by subsequent operations, and what discoverability properties does such movement preserve?

What abstract guarantee distinguishes a "properly created" link visible in its home document's arrangement from a link allocated but not placed?

What invariants must hold for a link whose type endset references content at an address that will never be allocated, and what does discoverability mean in that limiting case?
