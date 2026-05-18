# ASN-0093: Allocation Substrate

A Xanadu-style substrate maintains three address-keyed stores: the content store, the link store, and the document-arrangement function. Each store is grown by an allocation primitive that extends the store's domain at a fresh key with structural invariants on the new entry. ASN-0043 introduced the link store and its structural invariants (L0/L1/L1a/L1b/L1c/L3/L12/L14); ASN-0036 introduced the content store and arrangement function. ASN-0047 (Transition Model) folded both into a larger state model that also tracks entity allocation and arrangement provenance — `Σ = (C, L, E, M, R)` — and supplied the operational primitives for the full state.

This note extracts the *allocation-substrate* layer: the three allocation primitives (K.σ, K.α, K.λ) and the structural invariants on `(Σ.C, Σ.L, Σ.M)` they preserve. The substrate requires no commitment to `Σ.E` (the entity set) or `Σ.R` (the provenance relation). Downstream ASNs that reason about address allocation into the three stores without lifting the entity/provenance layer can depend on this note directly, without inheriting the additional state components or their associated invariants. Higher-layer concerns — arrangement mutation, entity stratification, provenance recording — are deferred to ASN-0047, which composes this substrate's primitives with its additional disciplines.

The factoring is downward from ASN-0047: every operation and invariant here is identical to its counterpart in ASN-0047 except for one notational substitution — `E_doc` (the set of entities classified `IsDocument`) is replaced by `dom(M)` (the set of allocated documents in the arrangement function), so the substrate-layer claims can be stated without reference to the entity set.


## Scope

Downstream ASNs that operate on the link store without needing arrangement mutation, entity stratification, or provenance recording can cite this substrate directly. Downstream ASNs that need any of the deferred machinery cite ASN-0047 (which itself depends on this substrate).

**Provided.** Three primitive operations and the structural invariants on `(C, L, M)` they preserve:

- **Operations:** `K.σ` (document registration), `K.α` (content allocation), `K.λ` (link allocation)
- **Invariants:** M0–M1 (arrangement-function shape), C0–C1c + C2 (content store), L0–L14 + L-fin (link store)
- **Lemma:** Cross-document disjointness (T10a.{2,5} → T10)
- **Axiom:** SubAllocatorAxiom (four clauses: Exists, Disjoint, FirstEmission, T10aConformance)

**Substrate axioms:** SubspaceConventionAxiom pinning `s_C = 1 ∧ s_L = 2`; SequentialTransitionAxiom committing transitions to atomic and sequential.

**Deferred to higher-layer ASNs:**

- **Arrangement mutation.** `K.μ⁺`, `K.μ⁻`, `K.μ~`, `K.μ⁺_L` — operations that modify `M(d)` for an existing `d ∈ dom(M)`. The substrate fixes `M(d)` at `∅` on registration and leaves it unmodified thereafter. Consequently, arrangement-side invariants from ASN-0036 (S2, S3, S8a, S8-depth, S8-fin, D-CTG, D-MIN) hold vacuously here since `M(d) = ∅` for every `d ∈ dom(M)`; arrangement-extension primitives that would make them non-trivial are deferred to ASN-0047.
- **Entity allocation.** The substrate's `K.σ` is the document-registration primitive without the entity-hierarchy machinery. ASN-0047's `K.δ` rebuilds itself as `K.σ` plus entity-set tracking, lineage discipline (`NodeLineage`), and version-allocator activation.
- **Provenance recording.** `K.ρ` and the provenance relation `R`. The substrate has no `R` component.
- **Coupling constraints.** ASN-0047's J-family (J0, J1, J1', J2, J3, J4) coupling K.α to K.μ⁺ etc. is out of scope; the substrate's `K.α` and `K.λ` stand independently.
- **Link withdrawal.** Nelson's tombstone-style withdrawal (LM 4/9) is not expressible at this layer. Closing the gap is deferred to a higher-layer ASN that may extend the substrate with an explicit retraction mechanism (per ASN-0086's `Nullify` or a future tombstoning ASN).


## State model

The substrate-level state is

> **Σ = (C, L, M)**

where

- `C : T ⇀ Val` is the content store (per ASN-0036): a partial function from element-level tumblers to content values. `Val` is the content value type defined in ASN-0036.
- `L : T ⇀ Link` is the link store (per ASN-0043): a partial function from element-level tumblers to triples `(F, G, Θ) ∈ Endset × Endset × Endset`. `Link` and `Endset` are defined in ASN-0043.
- `M : T ⇀ (T ⇀ T)` is the arrangement function (per ASN-0036): a partial function whose domain `dom(M)` is the set of allocated document addresses, mapping each to its V-position-to-I-address arrangement

`dom(M)` is the set of tumblers committed by `K.σ` events (defined below). A document is *allocated* iff `d ∈ dom(M)`; content addresses with `origin(a) = d` and link addresses with `origin(ℓ) = d` may be emitted only when `d ∈ dom(M)`. The `origin(·)` function is the tumbler-projection defined in ASN-0036 (truncation to the `zeros = 2` prefix); it is a pure structural projection on tumblers and depends on no state component.

**Note on `M`'s shape.** In ASN-0047, `M` is total with the convention `M(e) = ∅` for `e ∉ E_doc`, and "allocated document" means `e ∈ E_doc`. In this substrate, `M` is partial: `dom(M)` is precisely the set of allocated documents, and the convention "`M(d) = ∅` outside the domain" is replaced by `M(d)` being undefined outside `dom(M)`. This is a semantic shift, not a notational one — the substrate's vocabulary for "document allocated" runs through `dom(M)` rather than through `E_doc`.

**Design rationale for retaining `M`.** The substrate could replace `M` with a set `D ⊆ T` (since `M(d) = ∅` throughout this layer). `M` is retained as a partial function for *downward compatibility*: ASN-0047 and other higher-layer ASNs that compose this substrate with arrangement mutation extend `M(d)` from `∅` rather than re-introducing a new state component. Keeping `M` here makes the substrate→ASN-0047 lift trivial: `K.μ⁺` unfreezes what `K.σ` registers at `M(d) = ∅`.

**Terminology.** "Document" in this substrate means "element of `dom(M)`" — a purely structural notion (a T4-valid tumbler with `zeros = 2` registered into the arrangement function's domain). ASN-0047's `IsDocument(e) ∧ e ∈ E` is a strict refinement: every Layer-2 document is a substrate document, but the substrate admits documents that may not pass Layer 2's entity-hierarchy discipline.

The initial state is `Σ₀ = (∅, ∅, ∅)` — no content, no links, no documents.

**Subspace identifiers.** As in ASN-0043, `s_C` and `s_L` denote the content-subspace and link-subspace first-element-field values. This substrate commits to two axioms governing them:

- **SubspaceConventionAxiom (FixedSubspaceIdentifiers).** `s_C = 1 ∧ s_L = 2`. The distinctness `s_C ≠ s_L` (abbreviated **SC-NEQ**) and the sibling relation `s_L = s_C + 1` are immediate consequences. Pinned by Nelson's design (LM 4/30–4/31) and Gregory's `xanadu.h:144–146` / `granf2.c:162` / `do2.c:94`. SC-NEQ underwrites L14 (StoreDisjointness) and the L0 partition; the sibling relation underwrites the L1c chain exhibition's step `inc(b_C(d), 0) = b_L(d)`.

- **SequentialTransitionAxiom (SequentialAtomicTransitions).** Transitions `Σ → Σ'` are atomic, uninterruptible, and totally ordered: each transition evaluates its precondition against `Σ` and commits its effect to `Σ'` in one indivisible step, with no intermediate state in which a transition has begun but not committed.


## Arrangement-function invariants

**M0 (DocumentTumblerWellFormed).**

  `(A d ∈ dom(M) :: ValidAddress(d) ∧ zeros(d) = 2)`

Every allocated document address is a T4-valid tumbler with exactly two zero components (i.e., a document-level address per S7d of ASN-0036). Discharged from `K.σ`'s precondition (below) and inductively across transitions.

**M1 (ArrangementMonotonicity).**

  `(A Σ → Σ' :: dom(M) ⊆ dom(M'))`

`dom(M)` is non-decreasing across all transitions. The substrate admits no transition that removes a document from `dom(M)`. Discharged from the frame conditions of every transition kind: `K.σ` extends `dom(M)` by one element; `K.α` and `K.λ` hold `M` in frame.

`M1` underwrites every "remains in dom(M)" claim used downstream and is what allows SubAllocatorAxiom.Exists's "remain active at every reachable state in which `d ∈ dom(M)`" to be read as a permanent activation once `d` enters `dom(M)`.


## Content store invariants

**C0 (ContentImmutability).**

  `(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ (A a : a ∈ dom(C) : C'(a) = C(a)))`

Append-only with immutable values: `dom(C)` is non-decreasing, and no transition alters the value bound to an existing key. This is ASN-0036's S0/S1 restated for the substrate. Restated here (rather than inherited silently) so the substrate is self-contained — symmetric to L12 on the link side.

**C1 (ContentElementLevel).**

  `(A a ∈ dom(C) :: zeros(a) = 3)`

Every content address is an element-level tumbler. This is ASN-0036's S7b restated for the substrate. Discharged from `K.α`'s precondition.

**C1b (ContentElementFieldDepth).**

  `(A a ∈ dom(C) :: #E(a) ≥ 2)`

Every content address has at least two element-field components — the content-side analog of L1b. This is ASN-0036's S7c restated for the substrate. Discharged from `K.α`'s precondition.

**C1c (ContentAllocatorConformance).** Every content address `a ∈ dom(C)` has a structural inc-chain from its home document to `a`: a finite sequence `(t₀, t₁, …, tₙ)` with `t₀ = origin(a)` and `tₙ = a`, where each step `tᵢ = inc(tᵢ₋₁, kᵢ)` with `kᵢ ∈ {0, 1, 2}` satisfies T10a's per-step admissibility constraints. The chain witnesses `a`'s structural producibility from its home document via the content sub-allocator. This is the content-side analog of L1c. The bootstrap gap (no T10a-tracked allocator domain for the anchor traversal and first emission) is closed by SubAllocatorAxiom.FirstEmission for the content sub-allocator; subsequent emissions inherit T10a's GlobalUniqueness via SubAllocatorAxiom.T10aConformance.

**C2 (ContentScopedAllocation).**

  `(A a ∈ dom(C) :: origin(a) ∈ dom(M))`

Every content address has its home document allocated — the content-side analog of L1a. Discharged from `K.α`'s precondition and M1.


## Link store invariants

All invariants below are stated against the reachable-state quantifier — they hold at every `Σ` reachable from `Σ₀` via the transitions defined later in this note.

**L0 (SubspacePartition).**

  `(A a ∈ dom(L) :: E(a)₁ = s_L)`
  `(A a ∈ dom(C) :: E(a)₁ = s_C)`

Every link address has subspace identifier `s_L`; every content address has subspace identifier `s_C`. The L-clause is from ASN-0043; the C-clause is added here as a substrate-level commitment — ASN-0043 carries only the L-clause, and the substrate pins both as joint preconditions of its sub-allocator discipline.

**L1 (LinkElementLevel).**

  `(A a ∈ dom(L) :: zeros(a) = 3)`

Every link address is an element-level tumbler.

**L1a (LinkScopedAllocation).**

  `(A a ∈ dom(L) :: origin(a) ∈ dom(M))`

Every link address has its home document allocated. (Replaces `origin(a) ∈ E_doc` from ASN-0047 — at the substrate layer, the relevant predicate is "the document exists in the arrangement function's domain.")

**L1b (LinkElementFieldDepth).**

  `(A a ∈ dom(L) :: #E(a) ≥ 2)`

Every link address has at least two element-field components.

**L1c (LinkAllocatorConformance).** Every link address `a ∈ dom(L)` has a *structural inc-chain* from its home document to `a`: a finite sequence `(t₀, t₁, …, tₙ)` with `t₀ = origin(a)` and `tₙ = a`, where each step `tᵢ = inc(tᵢ₋₁, kᵢ)` with `kᵢ ∈ {0, 1, 2}` satisfies T10a's per-step admissibility constraints (T4-validity preservation, zero-count side conditions). The chain witnesses `a`'s structural producibility from its home document via the link sub-allocator.

The substrate states L1c in its per-step inc-rule form — not as the stronger "every intermediate `tᵢ` inhabits a T10a-tracked allocator's domain at the state of emission." The strong form fails for the anchor traversal and the first emission, which inhabit no T10a-tracked allocator domain at the moment of allocation; SubAllocatorAxiom.FirstEmission (below) closes the bootstrap gap by licensing the first emission directly, and SubAllocatorAxiom.T10aConformance carries subsequent emissions onto T10a's per-allocator inc chain. ASN-0047's L1c takes the same per-step inc-rule form.

**L3 (TripleEndsetStructure, narrowed form).**

  `(A a ∈ dom(L) :: L(a) = (F, G, Θ) where F, G, Θ ∈ Endset ∧ Θ ≠ ∅)`

Every link in the link store has exactly three endsets, with the type endset non-empty. This is a substrate-level *narrowing* of ASN-0043's L3 (`|L(a)| ≥ 3 ∧ L(a).e₃ ≠ ∅`): the substrate pins fixed-three-arity, matching ASN-0047's narrowing rather than ASN-0043's foundation form. ASN-0043's `N ≥ 3` generality is preserved in principle for foundation-level extensions, but the substrate's transition model is closed under fixed-three arity.

**L12 (LinkImmutability).**

  `(A Σ → Σ' : (A a : a ∈ dom(L) : a ∈ dom(L') ∧ L'(a) = L(a)))`

Once allocated, a link's address persists in `dom(L)` and its value is permanently fixed across all transitions.

**L14 (StoreDisjointness).**

  `dom(C) ∩ dom(L) = ∅`

Derived from L0 + SC-NEQ + T7 (SubspaceDisjointness, ASN-0034): every content address has `E(·)₁ = s_C`, every link address has `E(·)₁ = s_L`, and `s_C ≠ s_L`, so the domains are disjoint.

**L-fin (LinkStoreFiniteness).**

  `|dom(L)| < ∞`

The link store is finite at every reachable state. Discharged inductively from `Σ₀.L = ∅` and `K.λ`'s singleton extension.


## Address sub-allocators under documents

The content and link subspaces are organised as sibling element-field sub-allocators rooted at each document. For each `d ∈ dom(M)`, two element-field anchors sit immediately under `d`:

- `b_C(d) := [d.0.s_C]` — the **content sub-allocator anchor** (one-component element field with `E₁ = s_C`, `zeros = 3`, `#E = 1`)
- `b_L(d) := [d.0.s_L]` — the **link sub-allocator anchor** (one-component element field with `E₁ = s_L`, `zeros = 3`, `#E = 1`)

These anchors are *structurally producible* by T10a `inc` steps from `d`: `b_C(d) = inc(d, 2)` (TA5(d), `k = 2`) and `b_L(d) = inc(b_C(d), 0)` (TA5(c)). The anchors themselves are *not* in `dom(C) ∪ dom(L)` — content and link addresses have `#E ≥ 2` (C1; L1b above), and the anchors have `#E = 1` — so they inhabit the foundation carrier set `T` as structural witnesses without occupying any state component.

**SubAllocatorAxiom (Axiom, ContentLinkSubAllocatorExistence).** For each `d ∈ dom(M)`, two sub-allocators are simultaneously activated under `d` at the moment of `d`'s registration into `dom(M)` (by `K.σ`). Three clauses, independently citable as discharge premises:

- *Existence (SubAllocatorAxiom.Exists).* For every `d ∈ dom(M)`, the content sub-allocator `A_C(d)` (anchored at `b_C(d)`) and the link sub-allocator `A_L(d)` (anchored at `b_L(d)`) are active. By M1 (ArrangementMonotonicity), once `d ∈ dom(M)` it remains so at every successor state, and the sub-allocators correspondingly remain active permanently.

- *Disjointness (SubAllocatorAxiom.Disjoint).* Addresses produced by `A_C(d)` satisfy `E(·)₁ = s_C`; addresses produced by `A_L(d)` satisfy `E(·)₁ = s_L`. No address is produced by both sub-allocators.

- *First-emission namespace property (SubAllocatorAxiom.FirstEmission).* The first emission of each sub-allocator carries a freshness commitment evaluated at the K.α (resp. K.λ) event that commits the address as the sub-allocator's first emission (not at the earlier K.σ event that activated the sub-allocator; in general the K.σ event and the first-emission K.α/K.λ event are distinct, separated by zero or more intervening transitions):
  - *Content sub-allocator first-emit:* the first address `a` produced by `A_C(d)` satisfies `a ∉ dom(C) ∪ dom(L)` at the K.α event that emits `a`, with `E(a)₁ = s_C`, `origin(a) = d`, `#E(a) = 2`. Concretely: `a = [d.0.s_C.1]`.
  - *Link sub-allocator first-emit:* the first address `ℓ` produced by `A_L(d)` satisfies `ℓ ∉ dom(L) ∪ dom(C)` at the K.λ event that emits `ℓ`, with `E(ℓ)₁ = s_L`, `origin(ℓ) = d`, `#E(ℓ) = 2`. Concretely: `ℓ = [d.0.s_L.1]`.

- *T10a-conformance from the second emission onward (SubAllocatorAxiom.T10aConformance).* From the second emission onward, `A_C(d)` and `A_L(d)` are T10a-conforming sub-allocators, each treating the first emission committed by SubAllocatorAxiom.FirstEmission as the base address of its `inc(·, 0)` sibling chain. T10a's GlobalUniqueness on that chain discharges freshness for every emission past the first. This clause underwrites the freshness obligations cited in K.α's and K.λ's subsequent-emission preconditions; without it, those preconditions' appeals to "T10a's GlobalUniqueness on the inc chain" would have no axiomatic basis at the substrate layer. M1's monotonicity carries the "remain active" property forward across all subsequent transitions.

SubAllocatorAxiom.FirstEmission underwrites the bootstrap (where T10a alone cannot, since no prior `inc`-history exists in the sub-allocator's frontier); SubAllocatorAxiom.T10aConformance + T10a underwrites every subsequent emission. Together the four clauses cover the full sub-allocator lifecycle from activation through arbitrary emission.


## Cross-document disjointness chain

**Lemma (Cross-document disjointness; T10a.{2,5} → T10).** For any two distinct documents `d₁, d₂ ∈ dom(M)` with `d₁ ≠ d₂`, the link sub-allocator anchors `p₁ := b_L(d₁) = [d₁.0.s_L]` and `p₂ := b_L(d₂) = [d₂.0.s_L]` satisfy

  `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`

so by T10 (PartitionIndependence, ASN-0034), every address extending `p₁` differs from every address extending `p₂`. The same lemma holds with `b_C` in place of `b_L` for content allocations.

*Proof.* By M0, both `d₁, d₂ ∈ dom(M)` are T4-valid tumblers with `zeros(d_i) = 2`. Case-split on the document-level prefix relationship: prefix-comparable or prefix-incomparable.

*Case A — Prefix-comparable.* WLOG `d₁ ≼ d₂` and `d₁ ≠ d₂`, so `#d₁ < #d₂` and the component `d₂[#d₁+1]` is well-defined. The prefix relation gives `d₂[k] = d₁[k]` for `1 ≤ k ≤ #d₁`, so `d₂`'s first `#d₁` positions contain `d₁`'s two zero components; for `zeros(d₂) = 2` to hold (M0 at `d₂`), `d₂[#d₁+1] ≠ 0`.

The anchors are length-`+2` extensions of their respective document addresses: `#p_i = #d_i + 2`, with `p_i[k] = d_i[k]` for `1 ≤ k ≤ #d_i`, `p_i[#d_i + 1] = 0`, and `p_i[#d_i + 2] = s_L`. From `#d₁ < #d₂` we obtain `#p₁ ≤ #p₂` (in fact `#p₁ < #p₂`).

At position `k = #d₁ + 1`:
- `k ≤ #p₁` since `k = #d₁ + 1 ≤ #d₁ + 2 = #p₁`
- `k ≤ #p₂` since `k = #d₁ + 1 < #d₂ + 2 = #p₂` (using `#d₁ < #d₂`)

So `k ≤ min(#p₁, #p₂)`. The values:
- `p₁[k] = p₁[#d₁ + 1] = 0` (the zero separator inserted by the `b_L` construction)
- `p₂[k] = p₂[#d₁ + 1] = d₂[#d₁ + 1] ≠ 0` (by the T4 zero-count argument above; `#d₁ + 1 ≤ #d₂` since `#d₁ < #d₂`)

Thus `p₁[k] = 0 ≠ p₂[k]` at an index within both anchors, witnessing `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` via the position-divergence clause of Prefix (ASN-0034).

*Case B — Prefix-incomparable.* `d₁ ⋠ d₂ ∧ d₂ ⋠ d₁` at the document level. By Prefix (ASN-0034), the joint conjunction forces a position divergence: some `k ≤ min(#d₁, #d₂)` with `d₁[k] ≠ d₂[k]`. The anchors are length-`+2` extensions agreeing with `d_i` at positions `1..#d_i`, so the same index `k ≤ min(#d₁, #d₂) ≤ min(#p₁, #p₂)` satisfies `p₁[k] = d₁[k] ≠ d₂[k] = p₂[k]`, witnessing `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`.

*Closure.* T10 (PartitionIndependence, ASN-0034) applies uniformly: for any `a, b ∈ T` with `p₁ ≼ a` and `p₂ ≼ b`, we have `a ≠ b`. Every link address allocated under `d₁` extends `p₁ = b_L(d₁)`; every link address allocated under `d₂` extends `p₂ = b_L(d₂)`. Therefore no link allocated under `d₁` can coincide with any link allocated under `d₂`. The same argument with `b_C(d_i)` in place of `b_L(d_i)` gives cross-document content disjointness. ∎

Cross-subspace collisions between `dom(C)` and `dom(L)` are prevented by L14 (StoreDisjointness, above), itself derived from L0 + SC-NEQ + T7.


## Substrate primitive operations

The substrate admits three primitive transitions, one per state component. Each is atomic — its precondition is evaluated against `Σ` and its effect committed to `Σ'` in a single indivisible step; no intermediate state with the transition partially applied is admitted.

### K.σ (DocumentRegistration)

Extends `dom(M)` by registering a new document address with an empty arrangement.

*Precondition:*
- `d ∉ dom(M)` (fresh document address)
- `ValidAddress(d) ∧ zeros(d) = 2` (T4-valid, document-level — discharges M0 at the new key)

*Effect:* `dom(M') = dom(M) ∪ {d}`, with `M'(d) = ∅` and `M'(d') = M(d')` for every `d' ∈ dom(M)`.

*Frame:* `C' = C; L' = L`

*Cross-store freshness.* K.σ has no explicit `d ∉ dom(C) ∪ dom(L)` clause because cross-store freshness is automatic from the substrate's invariants: C1 forces `zeros(a) = 3` for every `a ∈ dom(C)`, L1 forces `zeros(ℓ) = 3` for every `ℓ ∈ dom(L)`, and K.σ's precondition pins `zeros(d) = 2`. Since no address can simultaneously satisfy `zeros = 2` and `zeros = 3`, `d ∉ dom(C) ∪ dom(L)` is forced by the precondition list together with C1/L1.

K.σ activates `A_C(d)` and `A_L(d)` per SubAllocatorAxiom.Exists, opening the content and link sub-allocator frontiers under `d` for subsequent K.α and K.λ emissions. K.σ is the substrate-level document-introduction primitive; higher-layer ASNs that need entity stratification, lineage discipline, or version-allocator activation compose K.σ with their own additional preconditions (e.g., ASN-0047's K.δ rebuilds itself as K.σ-plus-entity-set-tracking-plus-NodeLineage-plus-version-allocator-activation).

This substrate makes no commitment about *which* document addresses are admissible at K.σ beyond T4-validity and `zeros(d) = 2`. The discipline that constrains which tumblers are introduced (Nelson's hierarchical baptism, T10a allocator conformance for the document allocator, etc.) is a higher-layer commitment; the substrate's only commitment is that whatever `d` is introduced satisfies M0 going forward. In particular, K.σ admits address-space configurations broader than Nelson's hierarchical baptism — a tumbler `d` with `zeros(d) = 2` whose prefix corresponds to no allocated node or account is structurally admissible at this layer. Downstream ASNs that lift entity hierarchy discipline (notably ASN-0047) tighten K.σ's precondition accordingly.

### K.α (ContentAllocation)

Extends `dom(C)` with a fresh content address scoped to an allocated document.

*Precondition:*
- `d ∈ dom(M)` (home document exists)
- `a ∉ dom(C) ∪ dom(L)` (fresh address — L14)
- `zeros(a) = 3 ∧ E(a)₁ = s_C` (element-level, content subspace — C1, L0)
- `#E(a) ≥ 2` (C1b)
- `origin(a) = d` (scoped to home document — C2)
- `a` is produced by `d`'s content sub-allocator `A_C(d)`:
  - *First emission* (predicate: `{a' ∈ dom(C) : origin(a') = d} = ∅`): `a = [d.0.s_C.1]`. Freshness against `dom(C) ∪ dom(L)` is pinned by SubAllocatorAxiom.FirstEmission directly.
  - *Subsequent emission* (predicate: `{a' ∈ dom(C) : origin(a') = d} ≠ ∅`): `a = inc(max{a' ∈ dom(C) : origin(a') = d}, 0)` (TA5(c)), the next sibling on `A_C(d)`'s `inc` chain. Freshness against `dom(C)` is discharged by T10a's GlobalUniqueness on the `A_C(d)` `inc` chain; freshness against `dom(L)` is discharged by SC-NEQ + T7 (equivalently L14 at the pre-state).
- `v ∈ Val` (well-formed content value)

*Effect:* `C' = C ∪ {a ↦ v}`

*Frame:* `L' = L; (A d' :: M'(d') = M(d'))`

Cross-document disjointness for content allocations is supplied by the Cross-document disjointness chain lemma (above), applied with `p₁ := b_C(d)` and `p₂ := b_C(d')`.

### K.λ (LinkAllocation)

Extends `dom(L)` with a fresh link address scoped to an allocated document.

*Precondition:*
- `d ∈ dom(M)` (home document exists)
- `ℓ ∉ dom(L) ∪ dom(C)` (fresh address — L14)
- `zeros(ℓ) = 3 ∧ E(ℓ)₁ = s_L` (element-level, link subspace — L0, L1)
- `#E(ℓ) ≥ 2` (L1b)
- `origin(ℓ) = d` (scoped to home document — L1a)
- `ℓ` is produced by `d`'s link sub-allocator `A_L(d)`:
  - *First emission* (predicate: `{ℓ' ∈ dom(L) : origin(ℓ') = d} = ∅`): `ℓ = [d.0.s_L.1]`, the determinate first emission of `A_L(d)`. Freshness against `dom(L) ∪ dom(C)` is pinned by SubAllocatorAxiom.FirstEmission directly.
  - *Subsequent emission* (predicate: `{ℓ' ∈ dom(L) : origin(ℓ') = d} ≠ ∅`): `ℓ = inc(max{ℓ' ∈ dom(L) : origin(ℓ') = d}, 0)` (TA5(c)), the next sibling on `A_L(d)`'s `inc` chain. Freshness against `dom(L)` is discharged by T10a's GlobalUniqueness on the `A_L(d)` `inc` chain; freshness against `dom(C)` is discharged by SC-NEQ + T7 (equivalently L14 at the pre-state).
- `(A ℓ' : ℓ' ∈ dom(L) ∧ origin(ℓ') = d : ℓ' < ℓ)` (forward allocation — T9, ASN-0034; consequence of `inc(·, 0)` on the frontier in the subsequent case, and of the first-emit position being greater than any pre-existing `d`-scoped link in the first case, vacuous antecedent)
- `(F, G, Θ) ∈ Endset × Endset × Endset ∧ Θ ≠ ∅` (well-formed link value with mandatory non-empty type endset — L3)

*Effect:* `L' = L ∪ {ℓ ↦ (F, G, Θ)}`

*Frame:* `C' = C; (A d' :: M'(d') = M(d'))`

Cross-document disjointness for link allocations is supplied by the Cross-document disjointness chain lemma (above), applied with `p₁ := b_L(d)` and `p₂ := b_L(d')`.


## Discharge of stated invariants

Each invariant is discharged by induction on transition sequences from `Σ₀`. The inductive step is recorded as a per-(invariant, transition) matrix; entries describe how each transition kind preserves or discharges each invariant.

**Base case verification (at `Σ₀ = (∅, ∅, ∅)`).** Most invariants are vacuously satisfied: M0/M1/C1/C1b/C1c/C2/L0/L1/L1a/L1b/L1c/L3 quantify over `dom(C)`, `dom(L)`, or `dom(M)`, all empty at `Σ₀`. C0 and L12 quantify over transitions `Σ → Σ'`, vacuous at `Σ₀` until the first transition fires. Two invariants are non-vacuous but trivially satisfied at `Σ₀`:

- **L14** (`dom(C) ∩ dom(L) = ∅`): at `Σ₀`, both stores empty, so `∅ ∩ ∅ = ∅` — trivially true.
- **L-fin** (`|dom(L)| < ∞`): `|∅| = 0 < ∞` — trivially true.

The base case holds.

**Inductive step.** Per (invariant, transition):

| Invariant | K.σ | K.α | K.λ |
|---|---|---|---|
| **M0** (DocumentTumblerWellFormed) | Discharged at new key: precondition pins `ValidAddress(d) ∧ zeros(d) = 2` | Preserved: `M` in frame | Preserved: `M` in frame |
| **M1** (ArrangementMonotonicity) | Discharged: effect extends `dom(M)` by union | Preserved: `M` in frame | Preserved: `M` in frame |
| **C0** (ContentImmutability) | Preserved: `C` in frame | Discharged: effect extends `dom(C)` at fresh `a` with value `v`; value at existing keys unaltered (definitional in effect clause) | Preserved: `C` in frame |
| **C1** (ContentElementLevel) | Preserved: `C` in frame | Discharged at new key: precondition pins `zeros(a) = 3` | Preserved: `C` in frame |
| **C1b** (ContentElementFieldDepth) | Preserved: `C` in frame | Discharged at new key: precondition pins `#E(a) ≥ 2` | Preserved: `C` in frame |
| **C1c** (ContentAllocatorConformance) | Preserved: `C` in frame | Discharged at new key via the structural inc-chain (parallel to L1c chain exhibition below; first-emit case substitutes `s_C` for `s_L` in the final step) | Preserved: `C` in frame |
| **C2** (ContentScopedAllocation) | Preserved: vacuously (no new content); for prior keys `a ∈ dom(C)`, `origin(a) ∈ dom(M) ⊆ dom(M')` (`C` in frame, M1 extends `dom(M)`) | Discharged at new key: precondition pins `origin(a) = d ∧ d ∈ dom(M)`; preserved at prior keys (`origin(·)` is structural, M1 extends `dom(M)`) | Preserved: `C` in frame; prior keys preserved by M1 |
| **L0** (SubspacePartition) | Preserved: `L`, `C` in frame | Preserved on L-clause (`L` in frame); discharged at new key on C-clause via `E(a)₁ = s_C` precondition | Discharged at new key on L-clause via `E(ℓ)₁ = s_L` precondition; preserved on C-clause (`C` in frame) |
| **L1** (LinkElementLevel) | Preserved: `L` in frame | Preserved: `L` in frame | Discharged at new key: precondition pins `zeros(ℓ) = 3` |
| **L1a** (LinkScopedAllocation) | Preserved: vacuously (no new link); for prior keys `ℓ ∈ dom(L)`, `origin(ℓ) ∈ dom(M) ⊆ dom(M')` (M1 extends `dom(M)`) | Preserved: `L` in frame; prior keys preserved by M1 | Discharged at new key: precondition pins `origin(ℓ) = d ∧ d ∈ dom(M)`; prior keys preserved by M1 |
| **L1b** (LinkElementFieldDepth) | Preserved: `L` in frame | Preserved: `L` in frame | Discharged at new key: precondition pins `#E(ℓ) ≥ 2` |
| **L1c** (LinkAllocatorConformance) | Preserved: `L` in frame | Preserved: `L` in frame | Discharged at new key via the structural inc-chain (see *L1c chain exhibition* below — first-emit and subsequent-emit cases) |
| **L3** (TripleEndsetStructure, narrowed) | Preserved: `L` in frame | Preserved: `L` in frame | Discharged at new key: precondition pins `(F, G, Θ) ∈ Endset × Endset × Endset ∧ Θ ≠ ∅` |
| **L12** (LinkImmutability) | Preserved: `L` in frame | Preserved: `L` in frame | Discharged: effect extends `dom(L)` at fresh `ℓ`; value at existing keys unaltered (definitional) |
| **L14** (StoreDisjointness) | Holds at Σ' by direct derivation: L0(Σ') + SC-NEQ + T7 — all hold at Σ' | Holds at Σ': same derivation | Holds at Σ': same derivation |
| **L-fin** (LinkStoreFiniteness) | Preserved: `L` in frame | Preserved: `L` in frame | Discharged: `|dom(L')| = |dom(L)| + 1`; finiteness closed under +1 |

*L1c chain exhibition.* The substrate's L1c is "every link address has a structural inc-chain from its home document." For `K.λ`'s discharge, two sub-cases:

**First-emit case** (`ℓ = [d.0.s_L.1]`, predicate `{ℓ' ∈ dom(L) : origin(ℓ') = d} = ∅`). The structural inc-chain witnessing L1c is:

  `(t₀, t₁, t₂, t₃)` where `t₀ = d`, `t₁ = inc(d, 2) = b_C(d)`, `t₂ = inc(b_C(d), 0) = b_L(d)`, `t₃ = inc(b_L(d), 1) = [d.0.s_L.1] = ℓ`

Per-step admissibility:

- `t₁ = inc(d, 2)`: T10a admits `k = 2` when `zeros(spawnPt) ≤ 2`; by M0, `zeros(d) = 2`, satisfied. TA5(d) at `k = 2` yields `zeros(t₁) = 2 + (2 − 1) = 3`, T4-valid.
- `t₂ = inc(b_C(d), 0)`: TA5(c) at `k = 0` is unconditionally T4-preserving and length-preserving, with the sibling component advanced from `s_C` to `s_L`. By SubspaceConventionAxiom, `s_C = 1` and `s_L = 2`, so `inc([d.0.1], 0) = [d.0.2] = b_L(d)`. This step's correctness depends substantively on `s_L = s_C + 1`; the SubspaceConventionAxiom underwrites it.
- `t₃ = inc(b_L(d), 1)`: TA5(d) at `k = 1` has no zero-count side condition; `zeros(t₃) = 3 + 0 = 3` (k = 1 introduces no new zero), T4-valid, with `#E(t₃) = 2`.

**Subsequent-emit case** (`ℓ = inc(max{ℓ' ∈ dom(L) : origin(ℓ') = d}, 0)`, predicate `{ℓ' ∈ dom(L) : origin(ℓ') = d} ≠ ∅`). Let `ℓ_prev = max{ℓ' ∈ dom(L) : origin(ℓ') = d}`. By the inductive hypothesis on L1c, `ℓ_prev` has a structural inc-chain `(t₀, …, t_n)` with `t₀ = d` and `t_n = ℓ_prev`. The chain for `ℓ` extends this by one step: `(t₀, …, t_n, t_{n+1})` with `t_{n+1} = inc(t_n, 0) = inc(ℓ_prev, 0) = ℓ`. Per-step admissibility of the new step `t_{n+1} = inc(ℓ_prev, 0)`: TA5(c) at `k = 0` is unconditionally T4-preserving; freshness against `dom(L)` is discharged by SubAllocatorAxiom.T10aConformance applied to `A_L(d)`'s inc chain (T10a's GlobalUniqueness on the chain).


## Properties Introduced

| ID | Name | Status | Source |
|---|---|---|---|
| M0 | DocumentTumblerWellFormed | INV | Substrate, derived from K.σ precondition |
| M1 | ArrangementMonotonicity | INV | Substrate, frame of all transitions |
| C0 | ContentImmutability | INV | Substrate, ASN-0036's S0/S1 restated |
| C1 | ContentElementLevel | INV | Substrate, ASN-0036's S7b restated |
| C1b | ContentElementFieldDepth | INV | Substrate, ASN-0036's S7c restated; content-side analog of L1b |
| C1c | ContentAllocatorConformance | INV | Substrate, content-side analog of L1c; first-emit gap closed by SubAllocatorAxiom.FirstEmission, subsequent-emit by SubAllocatorAxiom.T10aConformance |
| C2 | ContentScopedAllocation | INV | Substrate, content-side analog of L1a |
| L0 | SubspacePartition | INV | L-clause from ASN-0043; C-clause added here |
| L1 | LinkElementLevel | INV | ASN-0043 |
| L1a | LinkScopedAllocation | INV | ASN-0043 (refactored: `E_doc` → `dom(M)`) |
| L1b | LinkElementFieldDepth | INV | ASN-0043 |
| L1c | LinkAllocatorConformance | INV | Substrate commitment: per-step inc-rule conformance (matching ASN-0047's L1c form). First-emit gap closed by SubAllocatorAxiom.FirstEmission, subsequent-emit by SubAllocatorAxiom.T10aConformance |
| L3 | TripleEndsetStructure | INV | Narrowed form of ASN-0043's L3 (fixed-three-arity, matching ASN-0047) |
| L12 | LinkImmutability | INV | ASN-0043 |
| L14 | StoreDisjointness | INV (derived) | L0 + SC-NEQ + T7 |
| L-fin | LinkStoreFiniteness | INV (derived) | Inductively from `Σ₀.L = ∅` + K.λ |
| SubAllocatorAxiom | ContentLinkSubAllocatorExistence | AXIOM | Four clauses: Exists, Disjoint, FirstEmission, T10aConformance |
| Cross-doc disjointness | T10a.{2,5} → T10 lemma | LEMMA | Derived from M0 + T4 + T10 + Prefix (ASN-0034); T4's zero-count argument underwrites the Case A divergence step |
| SubspaceConventionAxiom | FixedSubspaceIdentifiers | AXIOM | Substrate commitment: `s_C = 1 ∧ s_L = 2`; pinned by Nelson (LM 4/30–4/31) and Gregory (`xanadu.h:144–146`, `granf2.c:162`, `do2.c:94`). Underwrites L14 derivation and the L1c chain exhibition. |
| SequentialTransitionAxiom | SequentialAtomicTransitions | AXIOM | Substrate commitment: `Σ → Σ'` is atomic, uninterruptible, totally ordered. |
| K.σ | DocumentRegistration | OP | Substrate-level document introduction into `dom(M)` |
| K.α | ContentAllocation | OP | Substrate-level content emission |
| K.λ | LinkAllocation | OP | Substrate-level link emission |


## Open Questions

- *Link withdrawal.* The substrate admits no withdrawal of `dom(L)` entries (L12 enforces immutability). Nelson's tombstone-style withdrawal (LM 4/9) is not expressible at this layer. Closing the gap is deferred to a higher-layer ASN that may extend the substrate with an explicit retraction mechanism (per ASN-0086's `Nullify` or a future tombstoning ASN).

- *Higher-arity links.* L3 here pins three-arity, matching ASN-0047's narrowing. ASN-0043's general `N ≥ 3` form is preserved in principle for foundation-level extensions; this substrate is closed under fixed-three arity.

- *Document address discipline.* K.σ's precondition is structural-only (`ValidAddress(d) ∧ zeros(d) = 2 ∧ d ∉ dom(M)`). The substrate admits any T4-valid document-level tumbler. Nelson's hierarchical baptism (where node-account-document chains are enforced) is a higher-layer commitment; ASN-0047's K.δ tightens K.σ's precondition with the additional discipline.

- *Concurrency.* `K.σ`, `K.α`, and `K.λ` are stated as atomic transitions; the discipline for concurrent emission across multiple allocators is not addressed at this layer.

- *Sub-allocator stratification beyond `A_C(d)` and `A_L(d)`.* Future subspace identifiers `s ≥ 3` would require parallel sub-allocators; the present axiom commits to exactly two (content and link).

- *Arrangement extension primitives.* The substrate fixes `M(d) = ∅` at K.σ-time and never re-modifies. ASN-0047's K.μ-family extends arrangements; downstream ASNs needing arrangement mutation depend on ASN-0047.
