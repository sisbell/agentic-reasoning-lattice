# ASN-0086: Typed Relations on Address Sets

*Drawing the link model forward into a relational vocabulary*

ASN-0043 establishes the link as a primitive: an addressed, owned, typed connection between spans of content. ASN-0093 wraps that primitive (along with content and document allocation) in three K-operations — K.σ, K.α, K.λ — that fix the sibling-frontier emission discipline and the sub-allocator chain structure. This note layers on top of ASN-0093's K-operations, adopting a different vocabulary for the link store: where ASN-0043 speaks of *links* and *endsets*, we speak of *tuples* and *typed relations*. The two vocabularies describe one object — a standard-triple link `(F, G, Θ)` at address `a ∈ dom(Σ.L)` is a tuple in a typed relation indexed by `Θ` — but predicates compose more cleanly over relations than over endsets, and several substrate-level guarantees become easier to state in this form.

We are looking for what a relation algebra over the link store affords. The answer is structural properties on the typed-relation substrate, partitioned by status: R0–R5 are derived lemmas from ASN-0043 + ASN-0093; R6a/R6b/R6c (and R6c-Corollary) are the substantive lemmas carrying the *active/audit distinction* between `L_K` (audit trail) and `A_K` (operational currently-in-effect set). On top of these we define three operations (Emit_K, Observe, Nullify) and prove R7a (no `Σ.L`-affecting transition lies outside class (iii) = K.λ); the relational layer is then *defined* to commit `Emit_K` as its sole state-affecting K.λ-emission, and the immediate corollary is that all relational-layer state change reduces to `Emit_K`. (Document allocation (K.σ) and content emission (K.α), the other two primitive transitions in `→`, are inherited from ASN-0093 and are not reductions of `Emit_K`; the scope of the reduction is the link store `Σ.L` and the typed relations indexed over it.)


## The Two Foundational Sets

**Foundation.** We work in systems satisfying ASN-0093 (and therefore ASN-0043, ASN-0036, ASN-0034). ASN-0093 owns the K-operation contract — the three primitive emissions K.σ (DocumentRegistration), K.α (ContentAllocation), K.λ (LinkAllocation) — together with the SubAllocatorAxiom making T10a's runtime activation chain explicit, and the SubspaceConventionAxiom fixing `s_C = 1 ∧ s_L = 2` with named consequence `SC-NEQ: s_C ≠ s_L`. We consume these directly rather than reinventing them. Citations of S3 refer to S3 (ReferentialIntegrity, ASN-0036).

**Globally `s_C`-resident content (from ASN-0093 L0).** ASN-0093's L0 (SubspacePartition) supplies the substrate-wide disjointness premise that this note needs without an auxiliary hypothesis: `(A a ∈ dom(Σ.C) :: E(a)₁ = s_C)`. Under ASN-0036's `subspace_I(a) = E(a)₁`, this is equivalent to `(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)`. Consequently the disjointness between content and tuple addresses (R4 below) holds substrate-wide as a structural property — L0 supplies what an external `s_C`-residency hypothesis would otherwise have to assume.

**Subspace identifier distinctness (from ASN-0093 SC-NEQ).** ASN-0093's SubspaceConventionAxiom posits `s_C = 1 ∧ s_L = 2`, with named consequence `s_C ≠ s_L` (SC-NEQ). Wherever this note needs distinct content/link subspace identifiers, we cite SC-NEQ rather than re-asserting it.

**Definition — zero-count depth.** The *zero-count depth* of a tumbler `t` relative to its prefix `s ≼ t` is `zeros(t) − zeros(s)`. By T4 (HierarchicalParsing, ASN-0034), each zero is a field separator, so the difference counts the new T4 field separators introduced between `s` and `t`. A child-spawn `(d, k')` with `k' ≥ 1` produces a child whose zero count exceeds `zeros(d)` by `k' − 1` (TA5 postcondition (d)), so the zero-count depth of the spawn relative to `d` is exactly `k' − 1`.

**Definition — allocator-tree depth.** The *allocator-tree depth* of an allocator A relative to a document `d ∈ dom(Σ.M)` is the number of T10a child-spawn pairs `(·, k')` with `k' ∈ {1, 2}` on ASN-0093's structural chain from `d` to A's base address (i.e., to A's first emission). This is *not* the same as zero-count depth: a `(·, 1)` child-spawn opens a new allocator without introducing a new zero (TA5 with `k' = 1` gives `zeros` unchanged), so it advances the allocator hierarchy by one level without advancing zero-count depth. Concretely, the allocator opened by the single child-spawn `(d, 2)` lives at allocator-tree depth 1 and produces outputs at zero-count depth 1 relative to `d`; the link sub-allocator `A_L(d)` opened by `(d.0.s_L, 1)` lives at allocator-tree depth 2 and produces outputs at zero-count depth 1 relative to `d` (its outputs have `#E = 2` rather than `#E = 1`, but the same zero count). ASN-0093's `b_L(d) := [d.0.s_L]` names the link sub-allocator anchor; its first emission is `[d.0.s_L.1]` per SubAllocatorAxiom.FirstEmission.

*Allocator-naming convention.* Throughout this note, `A_x` denotes the allocator whose *first emission* is `x`. In particular, `A_{d.0.s_L.1}` is ASN-0093's link sub-allocator `A_L(d)`.

**State transition relation.** We write `Σ → Σ'` for the substrate's *dom-extending* one-step transition relation, which we identify exactly with the union of ASN-0093's three K-operations: `→ ≡ K.σ ∪ K.α ∪ K.λ`. Concretely, each `→`-step is one of:

- a *K.σ-step* — document registration, extending `dom(Σ.M)` with a fresh document address `d` satisfying `T4-valid(d) ∧ zeros(d) = 2` and registering `M'(d) = ∅`;
- a *K.α-step* — content allocation, extending `dom(Σ.C)` with a fresh content address `a` produced by `d`'s content sub-allocator `A_C(d)` for some `d ∈ dom(Σ.M)` (first-emission `a = [d.0.s_C.1]` or subsequent-emission `a = inc(a_prev, 0)`);
- a *K.λ-step* — link allocation, extending `dom(Σ.L)` with a fresh link address `ℓ` produced by `d`'s link sub-allocator `A_L(d)` for some `d ∈ dom(Σ.M)` (first-emission `ℓ = [d.0.s_L.1]` or subsequent-emission `ℓ = inc(ℓ_prev, 0)`).

In what follows we sometimes refer to the three classes as *class (i)*, *class (ii)*, *class (iii)* respectively (mnemonic for K.σ, K.α, K.λ); the K-operation labels are authoritative. ASN-0093's frame conditions on each K-op ensure that the two non-affected stores are preserved pointwise, and that the affected store is extended by exactly one fresh key per step. Every dom-extending transition in `→` is one of the three K-ops; the substrate exposes no removal, replacement, or in-place mutation transition that touches `(dom(Σ.C), dom(Σ.M), dom(Σ.L))` (consistent with S0, L12, T8, and ASN-0093 M1/C0/L12 across the underlying ASNs). The operations defined later in this note (Observe, Nullify) either compose `Emit_K` (Nullify is `Emit_R` with a designated argument shape) or leave Σ unchanged (Observe).

*Broader transition relation `↦`.* ASN-0036 admits arrangement modifications — extensions of `dom(Σ.M(d))` for existing `d ∈ dom(Σ.M)` — that change `Σ.M`'s pointwise values without extending `dom(Σ.M)`. We write `↦` for the union of `→` with these arrangement-modifying transitions, and `Σ ↦ Σ'` when the distinction matters. Every `→`-step is an `↦`-step. The arrangement-modification frame on `↦`-steps that are not `→`-steps holds `Σ'.C = Σ.C` by ASN-0036's S9 (TwoStreamSeparation), which forbids any `Σ.M`-modification from altering `Σ.C`; holds `dom(Σ'.M) = dom(Σ.M)` by the definitional partition of `↦` (any step extending `dom(Σ.M)` is a K.σ-step, not an arrangement-modifying step); and holds `Σ'.L = Σ.L` because (i) ASN-0043's L12 (LinkImmutability) forbids modification of existing entries — for every `a ∈ dom(Σ.L)`, `Σ'.L(a) = Σ.L(a)`; (ii) ASN-0043's L12a (LinkStoreMonotonicity) forbids removal — `dom(Σ.L) ⊆ dom(Σ'.L)`; and (iii) arrangement-modifying steps are *defined* not to extend `dom(Σ.L)` (they live in `↦ \ →` by the partition definition of `↦`, with link-store extension partitioned into the K.λ-step). Together (i)–(iii) yield `Σ'.L = Σ.L`. R0 through R7a are stated against `→`; R6c's corollary lifts persistence of nullification to `↦`.

*Categorical transition relation `↝`.* We write `↝` for the *categorical* state-transition relation: the union of `→` with every state-transition relation any higher-layer operation may admit over `(Σ.C, Σ.M, Σ.L)`. Every `→`-step and every `↦`-step is an `↝`-step; `Σ ↝ Σ'` holds iff some admissible operation in some layer carries Σ to Σ'. R7a quantifies over `↝` to make its claim categorical across all layers that conform to substrate invariants (the conformance assumption is lifted into R7a's precondition, below).

**Definition — Extension.** `Σ' extends Σ`, written `Σ ⊑ Σ'`, is the reflexive-transitive closure of `→`:

`Σ ⊑ Σ' ≡ Σ →* Σ'`

By the frame conditions of (i)–(iii) — each primitive transition extends exactly one of `Σ.C`, `Σ.M`, `Σ.L` at a fresh key and leaves the other two components unchanged — `Σ ⊑ Σ'` entails `dom(Σ.C) ⊆ dom(Σ'.C)`, `dom(Σ.M) ⊆ dom(Σ'.M)`, `dom(Σ.L) ⊆ dom(Σ'.L)`, with `Σ'.C|_{dom(Σ.C)} = Σ.C`, `Σ'.M|_{dom(Σ.M)} = Σ.M`, `Σ'.L|_{dom(Σ.L)} = Σ.L`.

**Definition — AddressUniverse.** The substrate's address universe at state Σ is

`A^Σ = dom(Σ.C) ∪ dom(Σ.L)`

By ASN-0093 L14 (StoreDisjointness) — equivalently ASN-0043 L14 (DualPrimitive) together with ASN-0093 L0 supplying global `s_C`-residency of content — `A^Σ` is the entirety of stored-entity addresses at Σ; no third category exists.

**Definition — Partition.** Define:

`A_doc^Σ = dom(Σ.C)` &nbsp; — content addresses
`A_rel^Σ = dom(Σ.L)` &nbsp; — relation-tuple addresses

We claim `A^Σ = A_doc^Σ ⊔ A_rel^Σ` (disjoint union). The disjointness is R4 below.

**Definition — GhostAddresses.** The *ghost addresses* at state Σ are the tumblers outside the stored-entity universe:

`T_ghost^Σ = T \ (dom(Σ.C) ∪ dom(Σ.L))`

By L9 (TypeGhostPermission, ASN-0043), ghost addresses may appear in endset spans (including type-endset coverage) without contradiction; they reference tumbler positions that are well-formed under the addressing scheme but carry no stored entity at Σ.

*Notation.* All four sets are state-dependent — `A^Σ`, `A_doc^Σ`, `A_rel^Σ`, and `T_ghost^Σ` grow or shrink as the substrate evolves (the first three monotonically by S1 and L12a; `T_ghost^Σ` shrinks as content and link emissions populate previously-ghost addresses). Where the ambient state is unambiguous, we drop the superscript and write `A`, `A_doc`, `A_rel`, `T_ghost`.

**Definition — TypeCatalog.** The set of *admissible types* is

`T_admissible = {K ∈ Endset : K ≠ ∅}`

— non-empty endsets, eligible to serve as a link's type endset by L3 (NEndsetStructure, ASN-0043). For each state Σ, the *type catalog at Σ* is the subset actually in use:

`T_cat^Σ = {Θ ∈ T_admissible : (E a ∈ dom(Σ.L) :: |Σ.L(a)| = 3 ∧ Σ.L(a).e₃ = Θ)}`

By L4 (EndsetGenerality, ASN-0043) and L9 (TypeGhostPermission, ASN-0043), `T_admissible` is unconstrained by content existence: type endsets may reference any tumbler addresses, including ghosts. We require only that type-equality is decidable by endset comparison — which it is, by L8 (TypeByAddress).

Type indices in what follows range over `T_admissible`, not `T_cat^Σ`. `T_cat^Σ` is descriptive — the snapshot of which type-endset values literally appear at the type slot in state Σ, by literal endset equality (`Σ.L(a).e₃ = Θ`) — but is not constitutive: `L_K^Σ` (below) is well-defined for any `K ∈ T_admissible` and is simply empty when no `a ∈ dom(Σ.L)` has a stored type-slot endset coverage-equivalent to `K`. Statements that need coverage-class semantics use `L_K^Σ`-membership (e.g., `L_R^Σ ≠ ∅`); statements about literally-stored type-slot values use `T_cat^Σ`.

For the rest of this development we restrict attention to standard-triple links — those with `|Σ.L(a)| = 3`. Higher-arity links (L3, NEndsetStructure, ASN-0043) exist in `dom(Σ.L)` but are not members of any `L_K`; they admit an analogous construction with additional slot positions, which we do not pursue here.

## Implementation Notes

*Boundary marker.* The K.λ contract of ASN-0093 already binds every link-store-extending transition to the sibling-frontier emission discipline: K.λ's first-emission predicate fires on `[d.0.s_L.1]` when no link is homed at `d`, and otherwise its subsequent-emission rule deposits at `inc(ℓ_prev, 0)` where `ℓ_prev := max{ℓ' ∈ dom(L) : origin(ℓ') = d}`. There is therefore no separate "sibling-frontier discipline" hypothesis to track in this note — the discipline is built into the substrate's class-(iii) operation. Claims about sibling-frontier structure (R0a, R0a-Cor1, R0a-Cor2) are accordingly unconditional within the substrate.

**Unit-depth retraction discipline.** This appendix retains one genuine layer-level commitment: the *unit-depth retraction discipline* is the relational layer's hypothesis that every retraction emission deposits an `R`-typed tuple whose to-endset is of the form `{(b, δ(1, #b))}` for some target `b ∈ A_rel^Σ` — equivalently, that every `L_R^Σ` tuple was produced by a `Nullify(Σ, d_retr, b)` call. This is a layer convention on the *shape* of retraction to-endsets, not a substrate discipline on emission addresses; it is honored by the relational-layer commitment that `Nullify` is the layer's sole producer of `L_R` tuples. The substrate (K.λ) does not enforce it: a higher layer could in principle emit `R`-typed retraction tuples with broader-coverage to-spans via direct K.λ calls. WP Case 2 (below) makes the consequence of admitting/excluding crafted-span retractions explicit.


## Allocator Structure

ASN-0093's SubAllocatorAxiom directly axiomatizes the sub-allocator structure this note relies on: for each `d ∈ dom(Σ.M)`, two sub-allocator chains `A_C(d)` (content) and `A_L(d)` (link) are simultaneously activated at `d`'s K.σ-step, anchored respectively at `b_C(d) := [d.0.s_C]` and `b_L(d) := [d.0.s_L]`, with first emissions `[d.0.s_C.1]` and `[d.0.s_L.1]`. We use ASN-0093's names directly throughout. The descriptive lemma below is retained because subsequent claims (especially in the Worked Sketch) refer to the *shared depth-one allocator* between content and link sub-allocators, which ASN-0093's chain axioms do not name explicitly.

**Lemma — SharedDepthOneAllocator.** Under each document address `d ∈ dom(Σ.M)`, T10a admits at most one allocator at allocator-tree depth 1 below `d` whose outputs sit at zero-count depth 1 relative to `d` — written `A_{d.0.1}` and opened by the `(d, 2)` child-spawn. When opened, this allocator is shared across all subspaces: its enumeration `d.0.1, d.0.2, d.0.3, …` indexes subspace identifiers, with position `s_C` landing in the content subspace and position `s_L` in the link subspace by ASN-0093 L0 (SubspacePartition). The subspace-specific sub-allocators ASN-0093 names — `A_C(d) = A_{d.0.s_C.1}` (anchored at `b_C(d)`) and `A_L(d) = A_{d.0.s_L.1}` (anchored at `b_L(d)`) — sit at allocator-tree depth 2, opened by `(d.0.s_C, 1)` and `(d.0.s_L, 1)` respectively.

*Proof.* In three steps.

*(a) The only T10a-admissible child-spawns from `d` are `(d, 1)` and `(d, 2)`.* Document addresses have `zeros(d) = 2` by S7d (DocumentAllocationDiscipline, ASN-0036) and ASN-0093's M0 (DocumentTumblerWellFormed). By TA5 postcondition (d), `zeros(inc(d, k')) = 2 + (k' - 1)` for `k' ≥ 1`; T4's cap `zeros ≤ 3` forces `k' ∈ {1, 2}`.

*(b) Only `(d, 2)` opens an allocator at zero-count depth 1.* By TA5(d), `(d, 1)` yields `zeros = 2` — zero-count depth 0 relative to `d` (extending `d`'s D field). `(d, 2)` yields `zeros = 3` — zero-count depth 1, the unique spawn introducing a new zero.

*(c) Uniqueness via T10a at-most-once.* T10a's at-most-once axiom on `(d, 2)` makes the allocator opened by `(d, 2)`, if opened at all, unique under `d`; we name this allocator `A_{d.0.1}`. The downstream subspace-specific allocators are exactly ASN-0093's `A_C(d)` and `A_L(d)`, with respective bases `b_C(d) = [d.0.s_C]` and `b_L(d) = [d.0.s_L]` and first emissions `[d.0.s_C.1]` and `[d.0.s_L.1]` per SubAllocatorAxiom.FirstEmission. ∎


## The Typed Relation

**Definition — TypeEquivalence.** Two admissible types are *type-equivalent* iff they cover the same address set:

`K ~ K' ≡ coverage(K) = coverage(K')`

This is L8's (TypeByAddress, ASN-0043) notion of `same_type`, lifted from links to type endsets themselves. The quotient `T_admissible / ~` is the set of *coverage classes*; the equivalence class of `K` is written `[K]`.

**Definition — TypedRelation.** For each `K ∈ T_admissible` and state Σ, the *typed relation of type K at Σ* is

`L_K^Σ = {(a, F, G) : a ∈ dom(Σ.L) ∧ |Σ.L(a)| = 3 ∧ Σ.L(a).e₁ = F ∧ Σ.L(a).e₂ = G ∧ coverage(Σ.L(a).e₃) = coverage(K)}`

Each member is a triple of (tuple-address, from-endset, to-endset). The pair `(F, G)` is the *relational content* of the tuple; `a` is the *tuple address*. The substrate's standard-triple link store at state Σ is therefore the disjoint union over coverage classes:

`L^Σ = ⨆_{[K] ∈ T_admissible / ~} L_K^Σ`

We will show (R1) that this disjoint union is well-defined: each tuple address belongs to exactly one coverage-class slice. Note that `L^Σ` collects only the arity-3 links; higher-arity links in `dom(Σ.L)` are outside its scope, as noted above. Where ambient state is clear we drop the superscript and write `L_K`, `L`. Coverage-equivalence at the type slot aligns `L_K` with L8's same-type relation, which also projects through coverage.

**Definition — TupleAddress.** Define `addr : L^Σ → A_rel^Σ` by `addr(a, F, G) = a`.

*Remark — relation to ℘(A) × ℘(A).* A generic mathematical typed relation is a subset of `℘(A) × ℘(A)` — a set of address-pair-pairs distinguished only by content. Our typed relation is richer: each tuple carries an address that participates in the relation's identity. The projection `(a, F, G) ↦ (coverage(F), coverage(G))` recovers the address-pair view, but it loses information that the substrate retains (R0, R1).


## Tuple Identity (R0, R1, R2)

A generic mathematical relation distinguishes its members only by content: two tuples with identical (F, G) are the same tuple. The substrate's relations do not work that way. Each tuple emission allocates a fresh address (R0), the address-to-pair binding is a function (R1), and the binding is permanent (R2).

**R0 — TupleAddressFreshness.** For any state Σ with `dom(Σ.M) ≠ ∅` and any `(F, G, K) ∈ Endset × Endset × T_admissible`, there exists a state Σ' with Σ → Σ' that emits a tuple with content (F, G) of type K at a fresh address:

`(A Σ : dom(Σ.M) ≠ ∅ :: (A F, G ∈ Endset, K ∈ T_admissible :: (E Σ' extending Σ, a : a ∉ dom(Σ.L) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = (F, G, K))))`

*Proof.* R0 is a near-direct consequence of ASN-0093's K.λ contract. Pick any `d ∈ dom(Σ.M)` (precondition `dom(Σ.M) ≠ ∅` is given). We invoke K.λ at home `d` with value `(F, G, K)` ∈ Endset × Endset × T_admissible (which satisfies K.λ's L3-discharge precondition by L3-conformance of the triple: `|·| = 3`, `F, G ∈ Endset`, `K ∈ T_admissible` non-empty).

K.λ's contract supplies the fresh address `a` directly via its first/subsequent emission rule:

- *First emission* (predicate `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d} = ∅` fires): `a = [d.0.s_L.1]`. By SubAllocatorAxiom.FirstEmission, this address has `E(a)₁ = s_L`, `origin(a) = d`, `#E(a) = 2`, `zeros(a) = 3`, and is T4-valid by direct inspection. By SubAllocatorAxiom.Exists, the link sub-allocator chain `A_L(d)` is active at every state with `d ∈ dom(Σ.M)`. By FirstEmissionFreshness, `a ∉ dom(Σ.L) ∪ dom(Σ.C)` at the K.λ-event that commits `a`.
- *Subsequent emission* (predicate `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d} ≠ ∅` fires): `a = inc(ℓ_prev, 0)` where `ℓ_prev := max{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d}`. By ChainEnumerationInjectivity (ASN-0093) and ChainMembershipForOrigin (ASN-0093), `ℓ_prev` is the maximum index of the contiguous prefix of `A_L(d)`'s realized chain, and `inc(ℓ_prev, 0)` is the next chain element of `A_L(d)`. By ChainUniformLength and ChainUniformZeroCount, the result has the same length and zero count as `ℓ_prev` (which by the IH for L1 carries `zeros = 3`); by ChainPrefixExtension, `b_L(d) ≼ a`, so `origin(a) = d`. Freshness of `a` against `dom(Σ.L) ∪ dom(Σ.C)` decomposes into three sub-claims:
  - *(a) Distinctness from same-home chain elements.* By ChainEnumerationInjectivity at chain indices of `A_L(d)`, `a = inc(ℓ_prev, 0)` is strictly greater than every chain element of `A_L(d)` at a smaller index; by ChainMembershipForOrigin, the realized homed-set at `d` is exactly the contiguous prefix up to `ℓ_prev`, so `a` is distinct from every element of `{a' ∈ dom(Σ.L) : origin(a') = d}`.
  - *(b) Distinctness from `dom(Σ.L)` elements homed at `d' ≠ d`.* By CrossDocDisjointness (ASN-0093) applied to the pair `(d, d')` with `d ≠ d'`, the link sub-allocator anchors `b_L(d)` and `b_L(d')` are prefix-incomparable, so by T10 (PartitionIndependence, ASN-0034), every address extending `b_L(d)` differs from every address extending `b_L(d')`. Since `b_L(d) ≼ a` (by ChainPrefixExtension above) and `b_L(d') ≼ a'` for every `a' ∈ dom(Σ.L)` with `origin(a') = d'` (by ChainPrefixExtension applied at `d'`), `a` is distinct from every such `a'`.
  - *(c) Distinctness from `dom(Σ.C)`.* By DisjointSubAllocatorChains (ASN-0093), `A_L(d)`'s outputs satisfy `E(·)₁ = s_L`; by ASN-0093 L0 applied to the content store, every `a' ∈ dom(Σ.C)` has `E(a')₁ = s_C`; by SC-NEQ, `s_C ≠ s_L`, so `a ∉ dom(Σ.C)`.
  Together, (a)–(c) discharge K.λ's freshness precondition `a ∉ dom(Σ.L) ∪ dom(Σ.C)` at the K.λ-event committing `a`.

In either branch, K.λ's effect is `Σ'.L = Σ.L ⊕ {a ↦ (F, G, K)}` with `Σ'.C = Σ.C` and `Σ'.M = Σ.M` per K.λ's Frame, witnessing R0's existential conclusion.

*L-invariant preservation across the K.λ-step.* ASN-0093's K.λ is engineered to preserve every substrate invariant by construction; we verify the ASN-0043 L-invariants by reading K.λ's contract together with R2 (TupleAddressPermanence, proved below from L12) and the consultation-derived chain lemmas.

L0/L1/L1a/L1b at `a` are discharged by K.λ's explicit preconditions: `E(a)₁ = s_L` (L0 at link store), `zeros(a) = 3` (L1), `origin(a) = d ∈ dom(Σ'.M)` (L1a), `#E(a) ≥ 2` (L1b — in fact `#E(a) = 2` by the SubAllocatorAxiom chain). L1c is discharged by the structural chain that SubAllocatorAxiom.ChainDiscipline + ChainElementT4Validity supply: `A_L(d)` is a T10a-discipline-satisfying chain, and the chain from `d` through `b_L(d)` to `a` is the L1c witness chain. (ASN-0043's L1c is a structural existential, and ASN-0093's SubAllocatorAxiom satisfies it by axiomatizing the chain's existence directly; no operational re-execution is required at the emission step.)

L3 holds by triple well-formedness: `(F, G, K)` has arity 3, `F, G ∈ Endset`, `K ∈ T_admissible` non-empty. L11a (LinkUniqueness, ASN-0043) at Σ' transfers from L11a at Σ (which holds because Σ is reachable from Σ_init and L11a is a substrate-level invariant preserved at every reachable state by ASN-0043 + ASN-0093's invariant catalog) together with K.λ's freshness postcondition (`a` distinct from every prior address). L12, L12a, L12b, L-fin are preserved by the single-key value-preserving extension form of K.λ's effect: `Σ'.L(a') = Σ.L(a')` for every `a' ∈ dom(Σ.L)` (L12); `dom(Σ'.L) ⊇ dom(Σ.L)` (L12a); `{home(a') : a' ∈ dom(Σ.L)} ⊆ dom(Σ.M) = dom(Σ'.M)` (L12b); finite-cardinality is closed under single-element union (L-fin).

ASN-0036's S-invariants (S0, S1, S2, S3, S7a, S7b, S7c, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ) transfer by input-substitution: each is a predicate over `(Σ.C, Σ.M)`, and K.λ's Frame fixes both components.

Five further L-invariants discharge per-invariant: *L2 (OwnershipEndsetIndependence):* `home(·)` is a pure projection of the address, independent of endsets. *L5 (EndsetSetSemantics):* `(F, G, K)` is built from set-valued components by construction. *L6 (SlotDistinction):* positional slots are fixed by tuple construction. *L8 (TypeByAddress):* `same_type(·, ·)` is a pure function of stored coverage; R2 preserves prior bindings and the fresh `a`'s value `(F, G, K)` extends consistently. *L13 (ReflexiveAddressing):* a structural property of link addresses, inherited at `a`.

*L-permissions (not invariants requiring preservation).* L4(c), L7, L9, L10, and L11b are permissions, not invariants: L4(c) licenses link-subspace targets, L7 licenses slot-directionality flexibility, L9 licenses ghost types, L10 licenses type-hierarchy containment, and L11b licenses distinct addresses to store equal triples. None constrains state-bound values, so none admits a preservation obligation across the emission step.

*L14 and L14a (prior-state invariant + new element).* L14 at Σ' requires `dom(Σ'.L) ∩ dom(Σ'.C)|_{s_C} = ∅`. Splitting on the K.λ Frame: (i) `dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅`, which is L14 at Σ (holding because Σ is reachable from Σ_init and L14 is a substrate-level invariant preserved at every reachable state by ASN-0043 + ASN-0093's invariant catalog); (ii) `{a} ∩ dom(Σ.C)|_{s_C} = ∅`, which holds because K.λ's preconditions give `E(a)₁ = s_L`, ASN-0093 L0 gives `(A a' ∈ dom(Σ.C) :: E(a')₁ = s_C)`, and SC-NEQ (`s_C ≠ s_L`) excludes `a` from the slice. L14a at Σ' requires `ran(Σ'.M) ∩ dom(Σ'.L) = ∅`. Splitting on the Frame: (i) `ran(Σ.M) ∩ dom(Σ.L) = ∅`, which is L14a at Σ (holding by the same substrate-invariant-at-reachable-state argument); (ii) `{a} ∩ ran(Σ.M) = ∅`, which holds because by S3 `ran(Σ.M) ⊆ dom(Σ.C)`, by ASN-0093 L0 every such address has `E(·)₁ = s_C`, and `E(a)₁ = s_L ≠ s_C` by SC-NEQ excludes `a`. ASN-0093's L14 (StoreDisjointness) also delivers this conclusion directly as a substrate-level invariant. ∎

**R0a — FlatLinkDomain.** At every reachable state Σ, `dom(Σ.L)` is a tumbler-prefix antichain:

`(A Σ : Σ reachable from Σ_init :: (A a, a' ∈ dom(Σ.L) :: a ≼ a' ⟹ a = a'))`

Under the K.λ contract of ASN-0093, R0a is unconditional: K.λ's first/subsequent emission rule, together with ASN-0093's sub-allocator chain axioms (SubAllocatorAxiom and its lemmas), enforce the sibling-frontier discipline as part of the substrate's class-(iii) primitive. No external discipline restriction on the reachable trajectory is required.

*Proof.* The argument decomposes into two cases on `home(a)` vs. `home(a')`, both discharged by ASN-0093's chain machinery (or, equivalently, by T10a's allocator-disjointness lemmas):

*Case 1 — Cross-home (`home(a) ≠ home(a')`).* We show this case directly from L1's element-level constraint plus L1a's NUDE-prefix `home` projection — no chain machinery is required. Let `d = home(a)` and `d' = home(a')` with `d ≠ d'`.

*(Forward direction: `¬(a ≼ a')`.)* Suppose, toward contradiction, that `a ≼ a'`. Then `a' = a · w` for some suffix `w` (the digits appended to `a` to obtain `a'`). Zero counts add along concatenation: `zeros(a') = zeros(a) + zeros(w)`. By L1 (LinkElementLevel, ASN-0043), `zeros(a) = zeros(a') = 3`, so `zeros(w) = 0` — `w` contains no zero positions. By L1a (LinkScopedAllocation, ASN-0043), `home(·) = N(·).0.U(·).0.D(·)` — the prefix of the link extending through the document-field `D(·)` and ending *just before* the third zero. Since `a ≼ a'`, the positions `1..#a` of `a'` agree pointwise with all of `a`; the remaining positions `#a + 1 .. #a'` of `a'` are `w`, which contains no zeros. Therefore every zero of `a'` sits at a position `≤ #a`, and the three zeros of `a'` are *exactly* the three zeros of `a`, at the same positions. In particular, `a'`'s third zero sits at the position of `a`'s third zero — call this position `p₃`, with `p₃ ≤ #a`. The `home` prefix has length `p₃ − 1` (the positions up to and including `D(·)`, which immediately precedes the third zero). Since `p₃ − 1 < p₃ ≤ #a`, the prefix of `a'` of length `p₃ − 1` agrees pointwise with the prefix of `a` of length `p₃ − 1` (by `a ≼ a'` applied at positions `1..#a`); equivalently, `N(a') = N(a)`, `U(a') = U(a)`, and `D(a') = D(a)` — the three NUDE field-components delimited by `a'`'s first three zeros coincide with those of `a` position-by-position. Therefore `home(a') = N(a').0.U(a').0.D(a') = N(a).0.U(a).0.D(a) = home(a) = d`, contradicting `d' ≠ d`. Hence `¬(a ≼ a')`.

*(Reverse direction: `¬(a' ≼ a)`, by explicit substitution.)* The forward derivation depends on `a` and `a'` only through the predicates `a ≼ a'`, `home(a)`, `home(a')`, `zeros(a)`, `zeros(a')`, `#a`, and the NUDE-projection of either argument — all of which are symmetric in their argument positions. We instantiate the forward derivation under the variable substitution `(a, a', d, d') := (a', a, d', d)`:
- The hypothesis `home(a) ≠ home(a')` becomes `home(a') ≠ home(a)` (the symmetric original), unchanged in content.
- The supposition `a ≼ a'` becomes `a' ≼ a`.
- L1's `zeros(a) = zeros(a') = 3` becomes `zeros(a') = zeros(a) = 3`, unchanged.
- L1a's `home(·) = N(·).0.U(·).0.D(·)` is a one-variable projection, applied independently at each argument — substituting `a' ↔ a` swaps the two applications.
- The derived equalities `N(a') = N(a)`, `U(a') = U(a)`, `D(a') = D(a)` become `N(a) = N(a')`, `U(a) = U(a')`, `D(a) = D(a')` (the same equalities by symmetry of `=`).
- The contradiction `home(a') = home(a) = d ≠ d'` becomes `home(a) = home(a') = d' ≠ d`, which is also a contradiction under `d ≠ d'`.

Hence `¬(a' ≼ a)`.

Either way, neither `a ≼ a'` nor `a' ≼ a` holds when `home(a) ≠ home(a')`, so the R0a implication `a ≼ a' ⟹ a = a'` holds vacuously in this case.

*Case 2 — Same-home (`home(a) = home(a') = d`).* By ASN-0093's ChainMembershipForOrigin lemma, the set `{a'' ∈ dom(Σ.L) : origin(a'') = d}` is a contiguous initial segment of `A_L(d)`'s chain enumeration `(t_1, t_2, t_3, …)` with `t_1 = [d.0.s_L.1]` and `t_{n+1} = inc(t_n, 0)`. Hence both `a` and `a'` are chain elements: `a = t_i` and `a' = t_j` for some `i, j ≥ 1`. By ChainUniformLength (ASN-0093), `#a = #t_i = #t_1 = #a'` — all chain elements have equal length. If `a ≼ a'`, then by the prefix definition (positions `1..#a` of `a'` agree with `a`) combined with `#a = #a'`, `a` and `a'` coincide pointwise, so `a = a'` by T3 (CanonicalRepresentation, ASN-0034).

(Equivalent argument via T10a.2: same-home chain elements are siblings of the link sub-allocator `A_L(d)` by SubAllocatorAxiom.ChainDiscipline + T10a.7; T10a.2 (NonNestingSiblingPrefixes, ASN-0034) then forces prefix-incomparability for distinct siblings, equivalently `a ≼ a' ⟹ a = a'`.)

Combining Cases 1 and 2, `a ≼ a' ⟹ a = a'` at every reachable Σ. ∎

**R0a-Cor1 — ContiguousPrefix.** At every reachable state Σ, for every `d ∈ dom(Σ.M)` there exists `J_d^Σ ∈ ℤ_{≥-1}` such that

`(A Σ : Σ reachable from Σ_init :: (A d ∈ dom(Σ.M) :: (E J_d^Σ ∈ ℤ_{≥-1} :: {a ∈ dom(Σ.L) : home(a) = d} = {incʲ(d.0.s_L.1, 0) : 0 ≤ j ≤ J_d^Σ})))`

(with `J_d^Σ = -1` denoting the empty set when no link is homed at `d`).

*Proof.* This is a direct re-expression of ASN-0093's ChainMembershipForOrigin lemma applied to the link store. ChainMembershipForOrigin states that `dom(Σ.L) ∩ {a' ∈ T : origin(a') = d}` is a contiguous initial segment `{s_1, …, s_{n_d}}` of `A_L(d)`'s chain enumeration. Setting `J_d^Σ := n_d − 1`, we have `s_k = inc^{k−1}([d.0.s_L.1], 0)` by SubAllocatorAxiom.FirstEmission (`s_1 = t_1^L(d) = [d.0.s_L.1]`) and SiblingRecurrence (`s_{k+1} = inc(s_k, 0)`). Hence

`{a ∈ dom(Σ.L) : home(a) = d} = {s_1, …, s_{n_d}} = {incʲ([d.0.s_L.1], 0) : 0 ≤ j ≤ J_d^Σ}`

with `J_d^Σ = -1` corresponding to `n_d = 0` (empty homed set). Under ASN-0036, `origin(a)` and `home(a)` coincide on every `a ∈ dom(Σ.L)` because L1 + L1a's NUDE-prefix projection is exactly the `origin(·) = N(·).0.U(·).0.D(·)` projection. ∎

**R0a-Cor2 — DepthTwoLinkAddresses.** At every reachable state Σ, every link address in `dom(Σ.L)` has an element field (T4b's `E` projection) of length exactly 2:

`(A Σ : Σ reachable from Σ_init :: (A a ∈ dom(Σ.L) :: #E(a) = 2))`

(Here `#E(a)` is the length of the element-field projection — e.g., `E(a₁) = [2, 1]`, `#E(a₁) = 2` at the concrete instantiation. This narrows L1b's substrate-level admission `#E ≥ 2` (ASN-0043) to the tighter `#E = 2` strictly.)

*Proof.* By R0a-Cor1, every `a ∈ dom(Σ.L)` lies on the form `a = incʲ(d.0.s_L.1, 0)` for `d = home(a)` and some `j ≥ 0`. The chain anchor `t_1 = [d.0.s_L.1]` has length `#t_1 = #d + 3` and three zero positions: the two zero positions of `d` (inherited from the prefix `d`), and a third zero at position `#d + 1` (the appended field separator in `d.0.s_L`). Position `#t_1 = #d + 3` carries the non-zero subspace ordinal `1`. The element field `E(t_1)` is the suffix following the third zero (at position `#d + 1`): `E(t_1) = [s_L, 1]` at positions `#d + 2` and `#d + 3`, so `#E(t_1) = 2`. ChainUniformLength (ASN-0093) gives `#t_n = #t_1` for every `n ≥ 1`. We now establish that the zero *positions* of every `t_n` coincide with those of `t_1`, which fixes `#E(t_n) = #E(t_1) = 2` strictly. Two routes deliver position-stability:
  - *Route A — TA5(c) + TA5-SigValid.* By SubAllocatorAxiom.ChainDiscipline + SiblingRecurrence, each `t_{n+1} = inc(t_n, 0)`. By TA5(c) (HierarchicalIncrement, ASN-0034), `inc(·, 0)` modifies *exactly one* position — `sig(t_n)`, the rightmost non-zero position — and preserves all other positions: `(t_{n+1})_i = (t_n)_i` for every `i ≠ sig(t_n)`, with `(t_{n+1})_{sig(t_n)} = (t_n)_{sig(t_n)} + 1`. By T10a.4 (T4PreservationUnderDiscipline, ASN-0034), every chain element is T4-valid, so by TA5-SigValid (ASN-0034), `sig(t_n) = #t_n` for every chain element. The single modified position is the terminal position `#t_n = #t_1`, which is non-zero in `t_n` (T4 conjunct iv at `t_n`) and remains non-zero in `t_{n+1}` (incrementing a non-zero ℕ-value stays non-zero — established locally by NAT-zero + NAT-discrete + NAT-addcompat strict-successor inequality `n < n + 1` chained with NAT-order's transitivity, identically to the chain in ASN-0034 T10a.8). Therefore the set of zero positions is identical across `t_n` and `t_{n+1}`; by induction, identical across the whole chain.
  - *Route B — ChainPrefixExtension.* Equivalently, ChainPrefixExtension (ASN-0093) gives `b_L(d) ≼ t_n` for every chain element, so the first `#b_L(d) = #d + 2` positions of `t_n` agree pointwise with `b_L(d)`. The three zero positions of `b_L(d)` (the two of `d` plus position `#d + 1`) therefore coincide with three zero positions of `t_n` at the same locations. ChainUniformZeroCount (ASN-0093) gives `zeros(t_n) = 3`, so no fourth zero appears in `t_n`; combined with ChainUniformLength's `#t_n = #t_1`, this forces position `#t_n` to be non-zero.
Either route fixes the zero positions of `t_n` identically with those of `t_1`. T4b's element field `E(·)` is the suffix following the third zero. Since the three zero positions of every `t_n` coincide with those of `t_1`, the third zero sits at position `#d + 1` in every chain element, and the element field's length is `#E(t_n) = #t_n − (#d + 1) = (#d + 3) − (#d + 1) = 2 = #E(t_1)`. Hence `#E(a) = 2`. ∎

R0a-Cor2 tightens L1b's substrate admission `#E ≥ 2` to `#E = 2` — establishing depth-2 strictly as a structural consequence of the K.λ contract and the link sub-allocator chain axioms.

**R1 — AddressInjectivity.** The map `addr : L → A_rel` is an injection:

`(A (a, F, G), (a', F', G') ∈ L : a = a' :: F = F' ∧ G = G' ∧ both belong to the same coverage-class slice L_{[K]})`

*Proof.* `Σ.L` is a partial function `T ⇀ Link` (ASN-0043, Definition of LinkStore). Function-ness gives uniqueness of value: if `a = a'`, then `Σ.L(a) = Σ.L(a')`, and that single value determines the triple `(F, G, K'')` stored at `a`. Therefore `F = F'`, `G = G'`, and the third endset `K''` is unique. Since `coverage(·)` is a pure function on endset values, `coverage(K'')` is a single fixed address set, so the coverage class `[K'']` is unique — whence both members of `L` lie in the same `L_{[K'']}`. ∎

**R2 — TupleAddressPermanence.** Once allocated, a tuple address resolves permanently to the same relational content:

`(A Σ → Σ', a ∈ dom(Σ.L), (F, G, K) = Σ.L(a) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = (F, G, K))`

*Proof.* Direct from L12 (LinkImmutability, ASN-0043): for every state transition, every existing link address persists with its value unchanged. ∎

*Consequences.* Each bullet is tagged by type — [COROLLARY] for a theorem-level implication of the R-claim and prior R-claims/L-invariants; [POLICY] for a higher-layer convention not entailed by the substrate; [ARCHITECTURE] for a structural design observation about the substrate's shape. The typology is fixed once here and applied uniformly in subsequent Consequences sections (R3, R4, R5, R6c).

(a) *[COROLLARY]* *Distinct emissions are distinguishable even when content matches.* Two agents independently filing tuples with identical `(F, G)` under identical `K` produce distinct addresses (R0 produces a fresh address regardless of value). By L11b (NonInjectivity, ASN-0043), value-level coincidence is permitted; by R1, address-level identity nevertheless distinguishes them. The substrate does not silently merge them.

(b) *[COROLLARY]* *Counting is well-defined.* `|{(a, F, G) ∈ L_K : pattern matches (F, G)}|` is a number, not an equivalence-class size, because the elements counted are distinct addresses (R1).

(c) *[COROLLARY]* *Audit references are stable forever.* An address written into the to-set of any tuple in cycle 1 still resolves to the same emission in cycle N, after the substrate has grown by orders of magnitude (R2). The reference does not need re-validation.

(d) *[POLICY]* *Idempotency on emit is policy, not substrate guarantee.* The substrate accepts duplicate emissions — R0 produces a fresh address regardless of whether identical content already exists. Higher layers wishing at-most-once semantics check `(E (a, F, G) ∈ L_K^Σ :: F, G match)` before calling Emit. This is a layer above the substrate's primitive.


## Append-Only Slices (R3)

**R3 — TypedSliceMonotonicity.** Each typed relation grows monotonically:

`(A Σ → Σ', K ∈ T_admissible :: L_K^Σ ⊆ L_K^{Σ'})`

where `L_K^Σ` denotes the typed relation evaluated at state `Σ`.

*Proof.* Let `(a, F, G) ∈ L_K^Σ`. By Definition of `L_K^Σ` (membership at the type slot is by coverage-equivalence, not by literal endset value), `a ∈ dom(Σ.L)` with `Σ.L(a) = (F, G, K'')` for some `K'' ∈ T_admissible` satisfying `coverage(K'') = coverage(K)`. By L12a (LinkStoreMonotonicity, ASN-0043), `dom(Σ.L) ⊆ dom(Σ'.L)`; by R2, `Σ'.L(a) = (F, G, K'')` — the literal value stored at `a` is preserved exactly. The membership test for `L_K^{Σ'}` is `coverage(Σ'.L(a).e₃) = coverage(K)`, i.e., `coverage(K'') = coverage(K)`, which holds by the choice of `K''`. Therefore `(a, F, G) ∈ L_K^{Σ'}`. ∎

*Consequences.* (Typology per R2's Consequences key.)

(a) *[COROLLARY]* *One-directional audit stability.* "A tuple of type K with this `(F, G)` existed at some point" stays true once true. Histories do not rewrite themselves.

(b) *[COROLLARY]* *Retractions are themselves auditable.* When we introduce the retraction type `R` (R6), `L_R` is one of the typed slices and R3 applies to it as well. Every nullification leaves an entry in `L_R` that persists.

(c) *[COROLLARY]* *Historical replay is well-defined.* `L_K` at past cycle `n` is a prefix of `L_K` at any cycle `m ≥ n`; "what was the substrate at cycle n?" is computable from the current substrate and a cycle-cutoff predicate. No separate snapshot mechanism is required.

(d) *[ARCHITECTURE]* *No information loss.* No compaction, no garbage collection, no archive tier removes tuples from `L_K`. The substrate's reliability for downstream agents — that an emission in cycle 3 is still observable in cycle 30 — is exactly R3.


## Subspace Disjointness (R4)

**R4 — TupleAddressDisjointness.** Tuple addresses and document-content addresses are disjoint:

`A_doc^Σ ∩ A_rel^Σ = ∅`

*Proof.* ASN-0093's L14 (StoreDisjointness) asserts `dom(Σ.C) ∩ dom(Σ.L) = ∅` substrate-wide as a direct consequence of L0 (SubspacePartition) together with SC-NEQ (`s_C ≠ s_L`) and T7 (FirstElementFieldDistinction, ASN-0034): every content address has `E(·)₁ = s_C`, every link address has `E(·)₁ = s_L`, and SC-NEQ makes the two disjoint. Substituting, `A_doc^Σ ∩ A_rel^Σ = ∅`. ∎

*Consequences.* (Typology per R2's Consequences key.)

(a) *[ARCHITECTURE]* *Predicates are typeable.* A predicate like `is_classified(d, K)` has signature `A_doc × T_cat → Bool`; a predicate like `is_active(τ)` (R6) has signature `A_rel → Bool`. No predicate has an ambiguous signature; categorical confusion at the address level is impossible.

(b) *[ARCHITECTURE]* *Retraction is well-typed.* Only `A_rel` addresses are valid arguments to Nullify (R6). "Retracting a document" is not directly expressible — the to-set of an `L_R` tuple must contain a tuple address, not a document address. Document removal from active consideration is done via classifier tuples (e.g., `L_retired`) targeting the document; the document's `A_doc` address is never disturbed.

(c) *[ARCHITECTURE]* *Lifecycle separation.* Documents have mutable bodies (arrangements `Σ.M` change per ASN-0036); tuples never mutate (R2). The address-level structure permits these to diverge without interference.


## Self-Reference (R5)

**R5 — TupleSelfTargeting.** A tuple's from-set or to-set may reference tuple addresses. Specifically, for any state Σ and any `a ∈ A_rel^Σ`, the unit-depth span `(a, δ(1, #a))` is well-formed and may appear in the from-set or to-set of an emitted tuple, with `a` in its coverage. (The Worked Sketch below, Step 1, instantiates R5: the retraction tuple's to-set references the link address `a₁` directly.)

*Proof.* We exhibit a concrete self-targeting emission and verify R0's invariant-preservation argument passes for it. Fix any state Σ with `dom(Σ.M) ≠ ∅` and any `a ∈ A_rel^Σ`.

*(Step 1 — Span well-formedness.)* By L1 (ASN-0043), `zeros(a) = 3`; by L1b (ASN-0043), `#E(a) ≥ 2`, so `#a ≥ 1`. By OrdinalDisplacement (ASN-0034), `δ(1, #a) = [0, …, 0, 1]` is a positive tumbler of length `#a` with action point `#a`. The span `(a, δ(1, #a))` satisfies T12 (SpanWellDefinedness, ASN-0034) — its action point `#a` satisfies `actionPoint(δ(1, #a)) = #a ≤ #a`. By PrefixSpanCoverage (ASN-0043), `coverage({(a, δ(1, #a))}) = {t : a ≼ t}`, which contains `a` by reflexivity of `≼`.

*(Step 2 — Endset admissibility.)* By L4(c) (EndsetGenerality, ASN-0043), endset spans may reference link-subspace addresses. By L13 (ReflexiveAddressing, ASN-0043) applied at `b = a`, the unit-depth span `(a, δ(1, #a))` is the canonical reference span for `a`. The singleton endset `G_self = {(a, δ(1, #a))}` is therefore an admissible `Endset` member at any slot of an emitted link.

*(Step 3 — Concrete self-targeting emission.)* Pick any `d ∈ dom(Σ.M)` (R0's `dom(Σ.M) ≠ ∅` precondition is given) and any `K ∈ T_admissible`. Form the triple `(∅, G_self, K)` — empty from-set, self-targeting to-set, and chosen type — the canonical retraction shape used by Nullify and instantiated concretely in the Worked Sketch (Step 1, with `K := R` and `a := 1.0.1.0.1.0.2.1`). Invoke R0 at this triple and home `d`: R0 produces a fresh emitter `a' ∉ dom(Σ.L)` and post-state Σ' with `Σ'.L(a') = (∅, G_self, K)`.

*(Step 4 — R0's invariant verification applied to this triple.)* R0's L-invariant verification proceeds against `(∅, G_self, K)` without modification:

- *L3 (NEndsetStructure):* the triple has arity 3 with `∅, G_self ∈ Endset` (Endset values are finite sets of well-formed spans; ∅ is the empty endset, `G_self` is the singleton built in Step 2) and `K ∈ T_admissible` non-empty by assumption. L3 holds by construction.
- *L0/L1/L1a/L1b at `a'`:* discharged by `a'`'s position in the link allocator hierarchy as determined by K.λ's first/subsequent emission rule at `d` — `E(a')₁ = s_L`, `zeros(a') = 3`, `home(a') = d ∈ dom(Σ'.M)`, `#E(a') = 2`. Wholly independent of endset content.
- *L1c at `a'`:* discharged by the T10a-conforming chain from `d` to `a'` witnessed by ASN-0093's SubAllocatorAxiom. Independent of endset content.
- *L12/L12a/L12b/L-fin:* preserved by the single-key value-preserving extension frame (K.λ Frame at `a'`).
- *L14a (`{a'} ∩ ran(Σ'.M) = ∅`):* the check operates on the *fresh emitter address* `a'`, not on the endset's targeted address `a`. By ASN-0093 L0, every content address has `E(·)₁ = s_C`; by S3 (ASN-0036), `ran(Σ'.M) ⊆ dom(Σ'.C)`, so every element of `ran(Σ'.M)` has `E(·)₁ = s_C` throughout; by SC-NEQ (ASN-0093 SubspaceConventionAxiom), `E(a')₁ = s_L ≠ s_C`, so `a' ∉ ran(Σ'.M)`. The to-endset's reference to `a` does not enter the L14a check.

R0's verification never inspects endset content beyond L3's well-formedness check — no invariant constrains *which* addresses an endset's spans target, only that the spans themselves are well-formed. The self-targeting endset therefore imposes no additional invariant obligation. The post-state Σ' with `Σ'.L(a') = (∅, G_self, K)` exists, is conforming, and records the self-reference at the substrate level: `a ∈ coverage(Σ'.L(a').e₂)` — the to-set case.

*(Step 5 — From-set case by parallel emission.)* The from-set case is symmetric. Form the triple `(G_self, ∅, K)` — self-targeting from-set, empty to-set, and the same chosen type. This triple is L3-conforming (arity 3, `G_self ∈ Endset` by Step 2, `∅ ∈ Endset` trivially, `K ∈ T_admissible` non-empty by assumption); under R0 invoked at home `d`, K.λ deposits at a fresh emitter address `a''` with `Σ''.L(a'') = (G_self, ∅, K)`. Step 4's L-invariant verification — none of which inspects which slot the self-targeting endset occupies — discharges identically (the slot-symmetric checks `E(a'')₁ = s_L`, `zeros(a'') = 3`, `home(a'') = d`, L14a via SC-NEQ, etc., apply by inspection of the emitter address `a''` alone). The conforming post-state Σ'' records the self-reference at slot 1: `a ∈ coverage(Σ''.L(a'').e₁)` — the from-set case.

*Generalization to arbitrary endset contents.* Examining R0's L-invariant verification invariant-by-invariant, the only endset-content-dependent check is L3 (well-formedness of the triple structure: arity 3, with `F, G ∈ Endset` finite sets of well-formed spans and `K ∈ T_admissible` non-empty). The remaining L-invariants discharge independently of endset targets: L0/L1/L1a/L1b/L1c depend on the emitter address `a'` alone, fixed by K.λ's first/subsequent emission rule at `d`; L2 depends on `home(a')` (a projection of `a'`); L11a depends on the freshness of `a'` against `dom(Σ.L)`; L12/L12a/L12b/L-fin are K.λ frame consequences; L5/L6 are construction-time tuple properties; L8/L13 are structural; L14/L14a depend on `a'`'s subspace marker against ASN-0093 L0 + SC-NEQ. None inspects `coverage(F)`, `coverage(G)`, or `coverage(K)`'s actual target addresses. Therefore any endset content `(F, G, K)` satisfying L3 admits the same R0 emission argument — including endsets built from L13-admissible canonical spans (`{(b, δ(1, #b))}` for any `b ∈ dom(Σ.L) ∪ dom(Σ.C) ∪ T_ghost`), L4(c)-licensed cross-subspace spans, and arbitrary mixtures thereof. The specific self-targeting witness `(∅, G_self, K)` constructed above is one instance of this admissibility class; the argument is uniform across the class. ∎

*Self-targeting emission recipe.* R5 admits a self-targeting unit-depth span (L4(c) + L13, applied independently of slot position) as an endset component; R0 at a caller-supplied home `d ∈ dom(Σ.M)` then emits the triple by its invariant-preservation argument, depositing the emission at a fresh `A_rel` address.

*Consequences.* Several constructs that would otherwise require out-of-band machinery collapse into the relational primitive. (Typology per R2's Consequences key.)

(a) *[ARCHITECTURE]* *Retraction.* A tuple in a designated relation `L_R` whose to-set contains the address of the tuple being nullified. By the self-targeting emission recipe, the retraction triple `(∅, {(a, δ(1, #a))}, R)` is emitted at a fresh `A_rel` address homed at a caller-supplied `d_retr ∈ dom(Σ.M)`. Mutation becomes Emit; `L_K` is never modified (R3).

(b) *[ARCHITECTURE]* *Resolution.* A tuple in `L_resolution` whose to-set contains a comment-tuple's address. By the self-targeting emission recipe, the resolution triple is emitted at a fresh `A_rel` address. Comment lifecycle is uniformly substrate-tracked; "this comment is closed" is an ordinary observation, not a flag stored elsewhere.

(c) *[ARCHITECTURE]* *Agent provenance.* A tuple whose from-set contains an agent's address and whose to-set contains the emitted tuple. By the self-targeting emission recipe, the provenance triple is emitted at a fresh `A_rel` address. Every emission has an attributable emitter as a substrate fact, with no separate metadata channel.

(d) *[COROLLARY for substrate-derivable half; POLICY for conventionally-derivable half]* *Higher-order predicates.* The substrate's Observe machinery uniformly answers any predicate expressible as a query over `L_K`, but the questions split by what each requires as input. *Substrate-derivable from Σ alone [COROLLARY]:* "Has τ been retracted?" reduces to `τ ∈ nullified(Σ)` (Definition of `nullified`), and "What tuples target τ?" to Observe filtered for tuples whose endset coverage contains τ — both decided directly against `Σ.L`. *Conventionally derivable [POLICY]:* "Who emitted τ?" is *not* answered by Σ.L alone — `Emit_K` writes `(F, G, K)` to a fresh address with no implicit emitter slot (Definition of `Emit_K`), so provenance has no substrate-level meaning. By consequence (c) above, the emitter includes its own address in the from-set of an `L_provenance` tuple targeting τ; once that convention is in force, "who emitted τ?" reduces to Observe over `L_provenance`. Predicates over documents face the same split (e.g., "who authored d?" is conventional in exactly the same way). The substrate's contribution is uniform evaluation machinery; *which* relations exist to evaluate against is a caller obligation upstream.

Without R5, each construct would require its own layer that predicates could not see and that the audit trail (R3) would not preserve. R5 collapses such layers into the relational structure.


## The Active Subset (R6a, R6b, R6c)

The conceptual contribution of this section is the *active/audit distinction*: two coherent views over the same link store — `L_K` (audit trail, monotone per R3) and `A_K` (operational currently-in-effect set, obtained by excluding `nullified(Σ)`). The construction is made possible by R5 (self-referential retraction) and R3 (monotone audit). R6a, R6b, R6c carry the distinction's substantive properties.

**Definition — RetractionType.** Fix a designated coverage class `[R]` reserved for retraction, represented by any `R ∈ T_admissible` whose coverage selects the conventional retraction address set. The corresponding typed relation `L_R^Σ` is the *retraction relation at state Σ*. By L9 (TypeGhostPermission, ASN-0043), `R` need not refer to anything stored — its coverage is an address set, chosen by convention — and `L_R^Σ` is well-defined as a coverage-class slice regardless of whether any literal representative endset has yet been stored. Before the first retraction emission, `L_R^Σ = ∅`; after the first such emission, `L_R^Σ ≠ ∅`. The "has any retraction been emitted yet?" question is exactly `L_R^Σ ≠ ∅`, decided in coverage-class terms. By coverage-equivalence, any emission with a type endset `R'` satisfying `coverage(R') = coverage(R)` contributes to `L_R^Σ` and to `nullified(Σ)` — callers are not required to use a canonical span structure for `R`, only its canonical coverage.

**Convention — RetractionDirectionality.** For the retraction coverage class `[R]`, the to-set carries the retraction's targets — addresses whose tuples are being withdrawn from the active subset — and the from-set is reserved for attribution-bearing endset content (e.g., the retractor's own address under the agent-provenance pattern of R5 Consequence (c)) or is left empty for unattributed retractions. L7 (DirectionalFlexibility, ASN-0043) permits this layer-level naming choice.

**Definition — Nullified.** The set of *nullified* tuple addresses at state `Σ` is

`nullified(Σ) = {a ∈ A_rel^Σ : (E (b, F', G') ∈ L_R^Σ :: a ∈ coverage(G'))}`

The existential checks `coverage(G')` only — the to-set's coverage — and does not inspect `coverage(F')`. This is the Convention RetractionDirectionality exercised at the substrate-level predicate: retraction targets are in `G'` by the layer's adoption (justified above against L7); an `Emit_R` call whose to-span coverage misses `a` does not nullify `a`, regardless of what its from-set covers. By R5, `coverage(G')` may include `A_rel^Σ` addresses, so `nullified(Σ)` is well-defined as a subset of `A_rel^Σ`.

*Scope rationale.* The set-builder restricts `a ∈ A_rel^Σ`, which the existential's witness does not imply on its own: a retraction's `coverage(G')` may include addresses outside `A_rel^Σ` — documents in `dom(Σ.M)`, content in `dom(Σ.C)`, or ghost tumblers (per L9, TypeGhostPermission, ASN-0043). The restriction reflects the substrate's typing — only tuple addresses are eligible for nullification, since `A_K^Σ` (the consumer of `nullified`) ranges over tuple addresses alone. Retraction-to-document, retraction-to-content, and retraction-to-ghost are excluded by this scope; document removal is performed via classifier tuples (R5 Consequence, retired classification) rather than direct retraction. A broader definition admitting `a` outside `A_rel^Σ` would be syntactically well-formed but would have no semantic effect on `A_K^Σ` membership — the restriction names the operationally meaningful subset of "addresses targeted by `L_R` to-sets."

**Definition — ActiveSubset.** For each `K ∈ T_admissible`, the *active subset of type K at state Σ* is

`A_K^Σ = {(a, F, G) ∈ L_K^Σ : a ∉ nullified(Σ)}`

`A_K^Σ` is computable from `Σ.L` alone: `L_K^Σ` is a slice of `Σ.L`, and `nullified(Σ)` is fixed by `L_R^Σ`, itself a slice of `Σ.L`.

**R6a — RetractionStability.** Once a tuple's address is nullified, it stays nullified across all future state transitions:

`(A Σ → Σ', a ∈ A_rel^Σ : a ∈ nullified(Σ) :: a ∈ nullified(Σ'))`

*Proof.* Recall that `coverage : Endset → ℘(T)` is a pure function on endset values, fixed by the substrate model (ASN-0043, Definition of coverage): given an endset value `E`, `coverage(E)` is determined entirely by `E` and the tumbler-order relation `≼`, which itself is state-independent (T1, ASN-0034). The codomain is `℘(T)` — the full tumbler space — not the state-dependent address universe `A^Σ`; coverage may include addresses outside `dom(Σ.C) ∪ dom(Σ.L)` (L9, TypeGhostPermission, ASN-0043). In particular, `coverage(E)` does not depend on the state Σ in which `E` is evaluated.

Suppose `a ∈ nullified(Σ)`. By Definition of `nullified(Σ)`, this entails `a ∈ A_rel^Σ = dom(Σ.L)`, and there exist `b ∈ dom(Σ.L)` and `(b, F', G') ∈ L_R^Σ` with `a ∈ coverage(G')`. By the coverage-equivalence membership criterion of `L_R^Σ`, the literal value stored at `b` in Σ is `Σ.L(b) = (F', G', R'')` for some `R'' ∈ T_admissible` with `coverage(R'') = coverage(R)` — the third entry need not equal `R` literally; only its coverage must. We exhibit the same witness at Σ': by L12a (LinkStoreMonotonicity, ASN-0043) applied to `a ∈ A_rel^Σ`, `a ∈ dom(Σ.L) ⊆ dom(Σ'.L) = A_rel^{Σ'}`, discharging the `a ∈ A_rel^{Σ'}` predicate required by Definition of `nullified(Σ')`. By R3 (applied to the type slice indexed by `R`), `L_R^Σ ⊆ L_R^{Σ'}`, so `(b, F', G') ∈ L_R^{Σ'}`. By R2, `b ∈ dom(Σ'.L)` with `Σ'.L(b) = (F', G', R'')` — the literal stored value is preserved exactly, so in particular `G'` is preserved. Since `coverage` is a pure function on endset values, `coverage(G')` is a single fixed set, and `a ∈ coverage(G')` is a state-independent proposition once `G'` has been fixed. Therefore `a ∈ nullified(Σ')`. ∎

**R6b — SingleDepthRetraction (Consequence of Definition `nullified`).** Deciding `a ∈ nullified(Σ)` reduces to a single-pass existential check over `L_R^Σ` — whether some tuple in the audit slice directly targets `a` — with no recursive evaluation of `nullified(·)` on the witness, and no requirement that the witness itself be active.

*Justification.* R6b is a direct consequence of how the Definition of `nullified` quantifies its existential (over the audit slice `L_R^Σ`, not the active subset `A_R^Σ`); we name it because the choice of quantification range — rather than being a derived theorem — has substantive consequences for the decision-procedure flatness and the resulting non-fixpoint semantics on retraction-of-retraction. By Definition of `nullified`, `a ∈ nullified(Σ) ⟺ (E (b, F', G') ∈ L_R^Σ :: a ∈ coverage(G'))`. The two possible readings yield substantively different decision procedures:

(i) *Audit-slice reading (this Definition).* The decision procedure is a single set-membership test: enumerate `L_R^Σ` (a slice of the link store), and for each `(b, F', G')`, test `a ∈ coverage(G')`. The witness `b`'s own status — active or nullified — is never consulted. Decidable in time proportional to `|L_R^Σ|`, independent of any retraction-chain depth within `L_R^Σ`.

(ii) *Active-subset reading (an alternative not adopted).* Had the Definition quantified `(b, F', G') ∈ A_R^Σ` instead, deciding `a ∈ nullified(Σ)` would entail first deciding `b ∉ nullified(Σ)` (membership in `A_R^Σ` requires the witness to be active by Definition of `A_R^Σ`), which is itself a recursive `nullified`-query on `b`. The decision procedure would become a fixpoint computation over the retraction-of-retraction graph: `b₁` retracts `a`; `b₂` retracts `b₁`; `b₃` retracts `b₂`; whether `a ∈ nullified(Σ)` would depend on the parity of the retraction-chain depth, with no fixed bound.

The adopted Definition is the audit-slice reading; R6b's content is the resulting decision-procedure flatness — `nullified` is a one-level check, with no fixpoint semantics imposed on retraction-of-retraction. As a consequence, attempting to "un-nullify" `a` by emitting `Nullify(b)` for the retractor `b` has no effect on `a ∈ nullified(Σ')`: the retractor `b` may itself become nullified, but the original retraction tuple `(b, F', G')` remains in `L_R^Σ ⊆ L_R^{Σ'}` (by R3), and `a ∈ coverage(G')` still witnesses `a ∈ nullified(Σ')`. ∎

**R6c — RestorationByReemission.** Once retracted, a tuple stays out of every active subset at any state reachable from Σ:

`(A Σ, K, (a, F, G) ∈ L_K^Σ : a ∈ nullified(Σ) : (A Σ' : Σ ⊑ Σ' :: (a, F, G) ∉ A_K^{Σ'}))`

*Proof.* Induction on the `→`-chain length `n` witnessing `Σ ⊑ Σ'`. *Base* (`n = 0`): `Σ_0 = Σ`, so `(a, F, G) ∈ L_K^{Σ_0}` and `a ∈ nullified(Σ_0)` are the precondition restated at `Σ_0`; by Definition of `A_K`, `a ∈ nullified(Σ_0)` jointly with `(a, F, G) ∈ L_K^{Σ_0}` give `(a, F, G) ∉ A_K^{Σ_0}`. *IH at `Σ_k`:* `(a, F, G) ∈ L_K^{Σ_k}` and `a ∈ nullified(Σ_k)`. *Step:* R6a gives `a ∈ nullified(Σ_{k+1})`; R3 gives `(a, F, G) ∈ L_K^{Σ_{k+1}}`. *Conclusion at `Σ_n = Σ'`:* by Definition of `A_K`, `(a, F, G) ∉ A_K^{Σ'}`. ∎

**Definition — BroadExtension.** In parallel with `⊑`, `Σ ⊑̂ Σ'` is the reflexive-transitive closure of `↦` (the broader transition relation including arrangement modifications):

`Σ ⊑̂ Σ' ≡ Σ ↦* Σ'`

Every `Σ ⊑ Σ'` entails `Σ ⊑̂ Σ'` (since `→ ⊆ ↦`); `⊑̂` additionally collects sequences that include arrangement-modifying steps, which `⊑` excludes. By the arrangement-modification frame (above) — ASN-0036's S9 (TwoStreamSeparation) keeps `Σ.C` identical under any `Σ.M`-modification, ASN-0043's L12 + L12a forbid `Σ.L` modification or removal, and `dom(Σ.M)` extension is partitioned off into class-(i) `→`-steps — every arrangement-modifying step holds `Σ.C` and `Σ.L` identical and changes only `Σ.M`'s pointwise values. Composed with class-(i)/(ii)/(iii) frames, `Σ ⊑̂ Σ'` entails `dom(Σ.C) ⊆ dom(Σ'.C)`, `dom(Σ.M) ⊆ dom(Σ'.M)`, `dom(Σ.L) ⊆ dom(Σ'.L)`, and `Σ'.L|_{dom(Σ.L)} = Σ.L` (link store extension only).

*Corollary (lift to `⊑̂`).* R6c's conclusion extends from `⊑` to `⊑̂`. By the Definitions of TypedRelation, Nullified, and ActiveSubset, `A_K^Σ` depends only on `Σ.L`; arrangement-modifying transitions hold `Σ.L` identical by ASN-0043's L12 + L12a (link store cannot be modified or removed across any transition), so `A_K^{Σ_arr} = A_K^Σ` pointwise.

*Proof.* The argument reduces the `↦*`-chain to its `→*`-subsequence and invokes R6c directly, avoiding any restatement of R6c's induction over `↦`-steps.

*(Step 1 — Σ.L pointwise-constancy under arrangement-modifying steps.)* By the Definitions of TypedRelation (`L_K^Σ` depends only on `Σ.L`), Nullified (`nullified(Σ)` is determined by `L_R^Σ`, itself a slice of `Σ.L`), and ActiveSubset (`A_K^Σ = L_K^Σ \ {(a, F, G) : a ∈ nullified(Σ)}`), the four quantities `L_K^Σ`, `L_R^Σ`, `nullified(Σ)`, `A_K^Σ` depend on `Σ` only through `Σ.L`. By ASN-0043's L12 (LinkImmutability) and L12a (LinkStoreMonotonicity), every arrangement-modifying step `Σ_k ↦ Σ_{k+1}` in `↦ \ →` holds `Σ_{k+1}.L = Σ_k.L` pointwise; consequently `A_K^{Σ_{k+1}} = A_K^{Σ_k}`, and the same equality holds for `L_K`, `L_R`, and `nullified`.

*(Step 2 — Reduction to a `→*`-subsequence.)* Let `Σ = Σ_0 ↦ Σ_1 ↦ ... ↦ Σ_n = Σ''` be an `↦*`-chain witnessing `Σ ⊑̂ Σ''`. Let `i_0 < i_1 < ... < i_m` be the indices at which `→`-steps occur (`i_0 = 0` by convention; if no `→`-step occurs, set `m = 0` and `i_0 = 0`). The subsequence `Σ_{i_0}, Σ_{i_1}, ..., Σ_{i_m}` together with the terminal state `Σ_n` partitions the chain into maximal runs: each `Σ_{i_j} → Σ_{i_j + 1}` is a `→`-step, and the tail `Σ_{i_j + 1} ↦* Σ_{i_{j+1}}` (resp. `Σ_{i_m + 1} ↦* Σ_n` for the final run) consists entirely of arrangement-modifying steps. By Step 1's Σ.L pointwise-constancy across arrangement-modifying runs, `Σ_{i_j + 1}.L = Σ_{i_{j+1}}.L` and `Σ_{i_m + 1}.L = Σ_n.L = Σ''.L`. Restricting to the `→`-steps yields a `→*`-chain `Σ = Σ_{i_0} → Σ_{i_0 + 1} → ... → Σ_{i_m + 1}` (consolidating each `→`-step with the arrangement-modifying tail that follows it into a single jump to the next `→`-step's source) with `Σ_{i_m + 1}.L = Σ''.L`; equivalently, the `Σ.L` footprint of `Σ ↦* Σ''` equals the `Σ.L` footprint of its `→*`-subsequence.

*(Step 3 — Invoke R6c on the `→*`-subsequence.)* R6c's preconditions hold at `Σ_0 = Σ` by the corollary's hypothesis: `(a, F, G) ∈ L_K^Σ` and `a ∈ nullified(Σ)`. R6c applied to the `→*`-chain `Σ →* Σ_{i_m + 1}` delivers `(a, F, G) ∉ A_K^{Σ_{i_m + 1}}`. Since `A_K^{Σ''}` depends only on `Σ''.L = Σ_{i_m + 1}.L`, `A_K^{Σ''} = A_K^{Σ_{i_m + 1}}`, so `(a, F, G) ∉ A_K^{Σ''}` as required.

*(Edge cases.)* If `n = 0`, then `Σ'' = Σ` and the conclusion `(a, F, G) ∉ A_K^Σ` is immediate from the hypothesis `a ∈ nullified(Σ)` and Definition of `A_K`. If `m = 0` (the chain contains no `→`-steps), then `Σ''.L = Σ.L` by Step 1 iterated, so `A_K^{Σ''} = A_K^Σ` and the conclusion transfers directly from R6c at the trivial `n = 0` case. Both edge cases reduce to R6c without further induction. ∎

To "restore" content, emit a fresh tuple with the desired value (R0). The new tuple receives a fresh address; the retracted tuple keeps its address (R2) and stays out of `A_K` (R6a).

*Consequences.* (Typology per R2's Consequences key.)

(a) *[ARCHITECTURE]* *Operational vs. historical views.* `A_K` is the operational view ("what is currently in effect"); `L_K` is the audit view ("what has ever existed"). Both are computed from `Σ.L` by the same observation machinery, differing only in whether `nullified(Σ)` is excluded. Operational and historical queries use the same observation primitive but specify different views.

(b) *[ARCHITECTURE]* *Mutation as set-difference.* `A_K^Σ = L_K^Σ \ {(a, F, G) : a ∈ nullified(Σ)}`. Computed live; no flag, no cache, no version field anywhere in the architecture.

(c) *[ARCHITECTURE]* *Quiescence is operational, not historical.* "Every public predicate over `A_K` holds" is the convergence condition. It does not require historical agreement; it requires the current substrate to satisfy every public check.

(d) *[COROLLARY]* *`A_K` is not monotone; `L_K` is.* R3 (TypedSliceMonotonicity) makes the audit slice monotone — `Σ ⊑̂ Σ' ⟹ L_K^Σ ⊆ L_K^{Σ'}` — but the same is *not* true of the active subset: a single retraction emission strictly shrinks `A_K` at every type whose tuple address it covers (witnessed by R6c's set-difference: `(a, F, G) ∈ A_K^Σ ∩ (L_K^{Σ'} \ A_K^{Σ'})` for the retracted tuple), and a subsequent re-emission of the same `(F, G)` strictly grows `A_K` again at a *different* address (R0's fresh-address guarantee). The Worked Sketch exhibits both directions concretely: `A_K^{Σ_0} = {(a₁, F₁, G₁)}` shrinks to `A_K^{Σ_1} = ∅` under Step 1's Nullify, and grows to `A_K^{Σ_2} = {(a₂, F₁, G₁)}` under Step 2's re-emission. Neither `⊆` nor `⊇` holds in general between `A_K^Σ` and `A_K^{Σ'}` for `Σ ⊑̂ Σ'`; the active subset is therefore *not* a monotone function of `Σ` under either inclusion direction, while the audit slice `L_K` is monotone under `⊆`. Predicates and observation views over `A_K` must accommodate non-monotone evolution as a substrate-level fact, not assume monotonicity inherited from `L_K`'s audit semantics. The regime distinction governing exactly when a class-(iii) `Emit_K` step contributes to `A_K` versus to `L_K \ A_K` — turning on whether a pre-existing retraction's coverage already includes the fresh sibling-frontier address, or (when `K ~ R`) whether the fresh emission's own to-set coverage self-targets — is unpacked in WP Case 2 (Weakest-Precondition Analysis, below).


## Three Operations

The six properties yield three operations that suffice to span all visible substrate change.

**Definition — Emit_K.** `Emit_K` is a family of state-transforming operations indexed by `K ∈ T_admissible`. K is a type-index (subscript), not a value argument; each fixed K gives a distinct operation with the same shape:

`Emit_K : Σ × dom(Σ.M) × Endset × Endset → Σ' × A_rel^{Σ'}`

(Equivalently: writing the family as a single operation, `Emit : T_admissible × Σ × dom(Σ.M) × Endset × Endset → Σ' × A_rel^{Σ'}` with `Emit_K(·) := Emit(K, ·)`. The subscripted form is used throughout this note for parallelism with `L_K`, `A_K`, and `Observe_K`.) Where Σ is the substrate's state space (every state reachable from `Σ_init`); ASN-0093's K.λ contract enforces the sibling-frontier discipline as part of the substrate's primitive emission, so `Emit_K` is a function over the full domain — no auxiliary discipline restriction is required.

`Emit_K` is operationally `K.λ` of ASN-0093, restricted to the standard-triple link value `(F, G, K)`. K.λ accepts a value `(e₁, …, e_N)` with `N ≥ 3` and `e₃ ≠ ∅`; `Emit_K` specializes to `N = 3` and `e₃ = K`, so K.λ's contract carries over directly.

*Precondition.* `K ∈ T_admissible` (discharged at the type-index, not at the value-argument list). The R0 precondition `dom(Σ.M) ≠ ∅` is enforced by parameter typing: a `d ∈ dom(Σ.M)` argument cannot be supplied unless the document-allocation domain is non-empty.

*Effect.* Given input state Σ, caller-supplied home document `d ∈ dom(Σ.M)`, and finite endsets `F, G ∈ Endset`, `Emit_K(Σ, d, F, G)` invokes K.λ at home `d` with value `(F, G, K)`. K.λ's first/subsequent emission rule fixes the fresh address `a`: *first emission* (predicate `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d} = ∅`) gives `a = [d.0.s_L.1]`; *subsequent emission* (predicate negated) gives `a = inc(ℓ_prev, 0)` where `ℓ_prev := max{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d}`. The returned `(Σ', a)` satisfies `a ∉ dom(Σ.L)`, `a ∈ dom(Σ'.L)`, `home(a) = d`, and `Σ'.L(a) = (F, G, K)`. By R2, this binding is permanent across all subsequent transitions.

*Frame.* `Σ'.C = Σ.C` and `Σ'.M = Σ.M` (K.λ's frame).

(The address-returning convention `Emit_K(d, F, G) → A_rel` used in the rest of this note is metonymic: the state is ambient, `d` is the caller-supplied home document, and `Σ'` is the post-emission state in which the returned address resides.)

**Lemma — Emit_K function-ness.** `Emit_K` is a function: given `(Σ, d, F, G, K)`, the output `(Σ', a)` is uniquely determined.

*Proof.* K.λ's first/subsequent emission rule is deterministic in `(Σ, d)`: the first/subsequent predicate is itself a function of `Σ` and `d` (it checks whether `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d}` is empty), and each branch produces a unique `a`. In the first-emission branch, `a = [d.0.s_L.1]` is a deterministic projection of `d`. In the subsequent-emission branch, `ℓ_prev` is `max{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d}` — a unique extremum because, by R0a-Cor1, the homed set is a contiguous prefix of `A_L(d)`'s chain enumeration and so admits a unique maximum under T1 (LexicographicOrder, ASN-0034). The value `Σ'.L(a) = (F, G, K)` is fixed by the caller-supplied arguments, and K.λ's Frame fixes the rest of Σ'. ∎

**Definition — Observe_K.** For `K ∈ T_admissible`, a pattern `(F̂, Ĝ) ∈ ℘_fin(T) × ℘_fin(T)`, and a view selector, Observe is a pure read with signature

`Observe_K : Σ × ℘_fin(T) × ℘_fin(T) × View → ℘_fin(L_K^Σ)`

where `View ∈ {hist, oper}` selects between `L_K^Σ` (audit) and `A_K^Σ` (operational). It returns

`{(a, F, G) ∈ view : F̂ ⊆ coverage(F) ∧ Ĝ ⊆ coverage(G)}`

with `view = L_K^Σ` if `View = hist` and `view = A_K^Σ` if `View = oper`. Observe leaves Σ unchanged.

*Pattern domain — `T`, not `A^Σ`.* Patterns range over the full tumbler space `T`, not the state-dependent address universe `A^Σ = dom(Σ.C) ∪ dom(Σ.L)`. The reason is `coverage(·)`: by L9 (TypeGhostPermission, ASN-0043) and L4 (EndsetGenerality, ASN-0043), endset spans may target ghost tumblers — tumblers in `T_ghost^Σ = T \ A^Σ` — and `coverage(F)` is consequently a subset of `T`, not of `A^Σ`. A pattern `F̂` restricted to `A^Σ` would be unable to express the canonical "does this tuple's from-endset cover ghost address `g`?" query, which is well-defined on `Σ.L` and operationally meaningful (e.g., for typed retraction targeting a not-yet-allocated coverage class representative, per L9 + R6 Definition of `nullified`). The signature's `℘_fin(T)` admits ghost-targeting patterns without restriction; the substrate-level match relation `F̂ ⊆ coverage(F)` remains decidable in `℘_fin(T)` because `coverage(F)` is itself a finite subset of `T` for every finite endset `F` (T12, ASN-0034 + finiteness of `F`).

*Rationale for the match relation.* `F̂ ⊆ coverage(F)` is the *minimal* substrate-level match relation, in two senses. First, every substrate computes `coverage(·)` (ASN-0043, Definition of coverage) as the canonical endset-to-address projection, and subset-containment of finite address sets is universally available — no auxiliary primitive is required. Second, the relation answers the canonical substrate-level question: "does this tuple's from-endset cover every address in the requested pattern?" This is exactly the question for which subset-on-coverage is the affirmative answer; richer queries (span-prefix containment, regex over a content projection, type-equality at the address level via L8) post-compose with Observe rather than parameterizing it. Observe is therefore fixed as the substrate-level primitive that returns "tuples whose endsets cover the requested address sets"; layered query languages obtain other relations by filtering Observe's output.

**Definition — Nullify.** Nullify has three preconditions: (P0) `d_retr ∈ dom(Σ.M)` — the caller-supplied home document for the retraction tuple itself; (P1) `a ∈ A_rel^Σ` — the target tuple's address; (P2) `|Σ.L(a)| = 3` — `a` is the address of a standard-triple link.

Under these preconditions, Nullify is the composition

`Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})`

That is, emit a tuple into the retraction relation with empty from-set and a unit-depth to-span targeting `a`, with the retraction itself homed at the caller-supplied `d_retr ∈ dom(Σ.M)`. By the self-targeting emission recipe (following R5), R0 at `d_retr` emits the retraction triple `(∅, {(a, δ(1, #a))}, R)`, depositing a fresh emitter address `b` with `Σ'.L(b) = (∅, {(a, δ(1, #a))}, R)`. By PrefixSpanCoverage (ASN-0043), `coverage({(a, δ(1, #a))}) = {t : a ≼ t}`, which contains `a`. Let `(Σ', _) = Nullify(Σ, d_retr, a)`. By Definition of `nullified`, `a ∈ nullified(Σ')`. By R6a, `a` remains nullified thereafter.

*Single-tuple scope, absolute under R0a.* The to-span's coverage `{t : a ≼ t}` is in principle the entire prefix-subtree of `a` within `T`; restricted to `A_rel^Σ = dom(Σ.L)`, however, R0a's unconditional antichain gives `{a' ∈ dom(Σ.L) : a ≼ a'} = {a}` directly. The class-(iii) `→` step taken by `Emit_R` adds the fresh emitter address `b` produced by K.λ at `d_retr`: `b ∉ dom(Σ.L)` by K.λ's freshness postcondition; `b ≠ a` because K.λ deposits `b` at `[d_retr.0.s_L.1]` (first-emission case) or at `inc(ℓ_prev, 0)` (subsequent-emission case), neither of which can equal `a` — both are fresh against `dom(Σ.L)`, and `a ∈ dom(Σ.L)` by P1; `a ⊀ b` by R0a applied to `dom(Σ'.L) = dom(Σ.L) ∪ {b}`. Therefore `{a' ∈ dom(Σ'.L) : a ≼ a'} = {a}` after the step, and `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}`: Nullify's `→` step contributes exactly `a` to `nullified(Σ')`, never a sub-tree of `A_rel`. Single-tuple scope is *absolute* — a substrate-level guarantee from R0a (itself unconditional under ASN-0093's K.λ contract).

The arity-3 restriction matches this note's scope. `A_K^Σ` is defined only over standard-triple links (Definition of `L_K^Σ`), so the active-subset effect of Nullify is meaningful only on arity-3 addresses. Nullifying a higher-arity address (`|Σ.L(a)| > 3`) would be a well-formed Emit_R, and would deposit `a` into `nullified(Σ')`, but no `A_K^{Σ'}` would feel the effect under the present definitions; extending the active-subset machinery to multi-arity relations `A_K^{(n),Σ}` is left to the open question on higher-arity links.

**Definition — substrate-conforming layer.** A layer is *substrate-conforming* iff every operation it publishes over `(Σ.C, Σ.M, Σ.L)` preserves every invariant the underlying substrate ASNs posit at each step. Concretely, this is the full invariant catalog of ASN-0043 — L0 (SubspacePartition), L1 (LinkElementLevel), L1a (LinkScopedAllocation), L1b (LinkElementFieldDepth), L1c (LinkAllocatorConformance), L3 (NEndsetStructure), L12 (LinkImmutability), L12a (LinkStoreMonotonicity), L14 (DualPrimitive), L14a (NonTranscludability), L-fin (LinkStoreFiniteness) — together with the ASN-0036 invariants S0 (ContentImmutability), S1 (StoreMonotonicity), S2 (ArrangementFunctionality), S3 (ReferentialIntegrity), S7a–d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ. The proof's directly-cited consumers are L12, L12a, L-fin, L1a, L0, L1, L1b, L1c, L3, S0, S1, and S7d (with the remainder transferring by input-substitution against Frame conditions); the abbreviation "substrate-conforming" stands in for the full conjunction.

**R7a — NoExtraClassAffectsL.** For any state-affecting transition `Σ ↝ Σ'` issued by a substrate-conforming layer (per the Definition above) with `Σ.L ≠ Σ'.L`, the `Σ.L`-affecting effect of the transition decomposes into a finite sequence of class-(iii) `→`-steps (K.λ-steps), possibly interleaved with class-(i) `→`-setup steps (K.σ-steps) required to discharge each class-(iii) step's L1a precondition: there exists a finite sequence `Σ = Σ_0 → Σ_1 → … → Σ_m` (`m ≥ 1`) of `→`-steps, each of class (i) or (iii), with `Σ_m.L = Σ'.L`, `dom(Σ_m.M) ⊆ dom(Σ'.M)`, and `dom(Σ_m.C) = dom(Σ.C) ⊆ dom(Σ'.C)` (no class-(ii) content-emission steps are introduced — L1a constrains only `home(a_k) ∈ dom(·.M)`, not any content address). Equivalently, the substrate exposes no mechanism for affecting `Σ.L` outside class (iii) (K.λ); when an `↝`-step is itself a primitive (Frame conditions hold `Σ'.C = Σ.C` and `Σ'.M = Σ.M`) adding a single fresh key, the step *is* a K.λ-step and the sequence has length 1; when it is a composite that simultaneously adds fresh document and link keys, its `Σ.L`-affecting sub-effect decomposes into a sequence of K.λ-extensions, prefixed by any K.σ-steps required so each link's `home(a_k) ∈ dom(Σ_{k-1}.M)` at the moment of emission.

The substrate-conformance precondition makes the assumption explicit in the claim itself; the proof verifies that no further clause is needed to derive the decomposition.

*Proof.* The substrate-conformance precondition admits every L- and S-invariant at every `↝`-step in scope (per the Definition above). The proof's central monotonicity argument consumes four of these directly — L12 (LinkImmutability, ASN-0043), L12a (LinkStoreMonotonicity, ASN-0043), S0 (ContentImmutability, ASN-0036), and S1 (StoreMonotonicity, ASN-0036) — and the K.λ-replay step consumes L1a (for `home(a_k)` discharge), L1c (for chain admissibility), L3 (for value well-formedness), L0/L1/L1b (for `a_k`'s structural address properties), L-fin (for Δ-finiteness), and S7d (for K.σ-prefix preconditions when needed). Any layer publishing an operation over the substrate's `(Σ.C, Σ.M, Σ.L)` state vector that violated any invariant in the catalog would by definition place the substrate in a state inconsistent with ASN-0036/ASN-0043 — the resulting `Σ'` would not be a conforming substrate state — so non-conforming layers fall outside R7a's scope.

Under this conformance, every `Σ ↝ Σ'` in scope satisfies `dom(Σ.L) ⊆ dom(Σ'.L)` (L12a), `Σ'.L(a) = Σ.L(a)` for every `a ∈ dom(Σ.L)` (L12), `dom(Σ.C) ⊆ dom(Σ'.C)` (S1), and `Σ'.C(a) = Σ.C(a)` for every `a ∈ dom(Σ.C)` (S0). Therefore any `Σ ↝ Σ'` with `Σ.L ≠ Σ'.L` must extend `dom(Σ.L)` by at least one fresh address: modification of existing entries is forbidden by L12, and removal is forbidden by L12a, so the only remaining mechanism for changing `Σ.L` is a strict extension `dom(Σ'.L) ⊋ dom(Σ.L)`. Let `Δ := dom(Σ'.L) \ dom(Σ.L)`; by L-fin (LinkStoreFiniteness, ASN-0043), both `dom(Σ.L)` and `dom(Σ'.L)` are finite, so `Δ` is a finite, non-empty set of fresh addresses. Enumerate `Δ` in any order as `a_1, …, a_n` (`n ≥ 1`).

At the substrate-model interface, the State transition relation paragraph commits K.σ/K.α/K.λ (classes (i)/(ii)/(iii)) as the *complete* primitive vocabulary of `→`. K.λ's admission requires `home(a_k) ∈ dom(·.M)` (L1a), which K.λ itself does not extend. K.σ's admission requires only freshness against `dom(·.M)` plus S7d's structural commitments (`T4-valid(d) ∧ zeros(d) = 2`).

We construct the replay sequence by interleaving: for each `k ∈ {1, …, n}`, set `d_k := home(a_k)` (computed from the fresh address `a_k` alone, by L1a's home-projection) and `(F_k, G_k, K_k) := Σ'.L(a_k)` (the literal value stored at `a_k` in Σ', well-defined since `a_k ∈ dom(Σ'.L)`). At each iteration `k`, if `d_k ∉ dom(Σ_{prev}.M)` for the running predecessor state `Σ_{prev}`, prefix a K.σ-step `Σ_{prev} → Σ_{prev}'` extending `dom(Σ_{prev}.M)` with `d_k` (K.σ's Frame guarantees `Σ_{prev}'.L = Σ_{prev}.L` and `Σ_{prev}'.C = Σ_{prev}.C`, so this prefix step does not advance `Σ.L` or `Σ.C`). The K.σ-step's preconditions discharge as follows: `d_k ∈ dom(Σ'.M)` (by L1a applied to `a_k` at Σ' in the original `↝`-step), so Σ' satisfies S7d at `d_k`, giving `T4-valid(d_k) ∧ zeros(d_k) = 2` — the structural commitments K.σ requires; freshness against `Σ_{prev}.M` is the case hypothesis `d_k ∉ dom(Σ_{prev}.M)`. Then K.λ admits a class-(iii) `→`-step `Σ_{prev}' → Σ_k` emitting `(F_k, G_k, K_k)` at `a_k`. K.λ requires (1) `a_k ∉ dom(Σ_{prev}'.L)`, (2) L0/L1/L1a/L1b at `a_k`, (3) `origin(a_k) = d_k` per K.λ's scoped-allocation precondition, and (4) the first/subsequent emission rule selects `a_k`. We discharge each:

- *(1) Freshness `a_k ∉ dom(Σ_{prev}'.L)`*: the K.σ-prefix held `Σ_{prev}'.L = Σ_{prev}.L`, with `Σ_{prev}.L = Σ.L ∪ {a_1, …, a_{k-1}}` from prior iterations and `a_k` distinct from each by Δ-enumeration and `a_k ∉ dom(Σ.L)` by Δ-membership.
- *(2) L0/L1/L1b at `a_k`*: these are purely structural properties of the address `a_k` itself — `E(a_k)₁ = s_L`, `zeros(a_k) = 3`, `#E(a_k) ≥ 2` — depending only on `a_k`'s tumbler structure, not on any state. The original `↝`-step's post-state Σ' satisfies all three L-invariants at `a_k` (Σ' is a reachable conforming state); since L0/L1/L1b are state-independent predicates over `a_k`, they hold at `a_k` regardless of which state evaluates them. They transfer to `Σ_{prev}'` without further argument.
- *(2/3) L1a at `a_k` (origin/home discharge)*: requires `home(a_k) = origin(a_k) ∈ dom(Σ_{prev}'.M)`. By construction `d_k = home(a_k)` and the K.σ-prefix (if needed) inserted `d_k` into `dom(Σ_{prev}'.M)`; if no prefix was needed, `d_k ∈ dom(Σ_{prev}.M) ⊆ dom(Σ_{prev}'.M)` by the case hypothesis. Either way, `home(a_k) ∈ dom(Σ_{prev}'.M)`.
- *(4) First/subsequent emission rule selects `a_k`*: ASN-0093's K.λ contract deterministically selects the next link address for home `d_k` based on the predicate `{ℓ' ∈ dom(Σ_{prev}'.L) : origin(ℓ') = d_k} = ∅`. We must show that the rule, applied at `Σ_{prev}'`, produces precisely `a_k`. The argument has three parts:
  - *(i) Chain-order existence within each home.* By R0a-Cor1 at Σ', for each `d_k` the homed set `{a ∈ dom(Σ'.L) : home(a) = d_k}` is `{incʲ(d_k.0.s_L.1, 0) : 0 ≤ j ≤ J_{d_k}^{Σ'}}` — a contiguous prefix of `A_L(d_k)`'s chain enumeration. This contiguous-prefix structure pins down a canonical chain-order on the home `d_k`'s realized link addresses: each address has a unique chain index `j`, and chain indices totally order the homed set.
  - *(ii) Cross-home iteration order is immaterial under K.λ's per-home determinism.* K.λ's first/subsequent emission predicate at home `d_k` is `{ℓ' ∈ dom(Σ_{prev}'.L) : origin(ℓ') = d_k} = ∅` — *origin-scoped* to `d_k`, depending only on those elements of `dom(Σ_{prev}'.L)` whose origin equals `d_k` and ignoring all other elements. Consequently, the rule's outcome at iteration `k` is a function of `(d_k, {ℓ' ∈ dom(Σ_{prev}'.L) : origin(ℓ') = d_k})` alone; emissions homed at other documents in earlier iterations contribute to `dom(Σ_{prev}'.L)` but not to the origin-scoped homed-set at `d_k`, so they do not alter K.λ's outcome at `d_k`. Cross-home interleaving in the Δ-enumeration is therefore immaterial — any iteration order produces the same outcome at each home, provided within-home chain-order is respected.
  - *(iii) Iteration in chain-order at each home selects `a_k`.* Re-order the Δ-enumeration so that fresh addresses homed at the same `d_k` appear in chain-order from least to greatest chain index (a permissible re-enumeration by (ii) since Δ is finite and within-home chain-order is well-defined by (i)). Under this ordering, each `a_k` is the chain element at the next available chain index after the prior iteration completed at the same home; K.λ's first/subsequent rule, evaluated against the origin-scoped homed-set at `Σ_{prev}'`, produces exactly this chain element. (Equivalently: ChainMembershipForOrigin (ASN-0093) at Σ' gives a unique chain enumeration; the replay traverses that enumeration in chain-order at each home, with K.λ's deterministic rule selecting the next chain element at each step.)

After all `n` iterations (interleaved with at most `n` K.σ-prefixes when home documents were not already in `dom(Σ.M)`), the running `Σ_m.L = Σ.L ⊕ {a_1 ↦ (F_1, G_1, K_1), …, a_n ↦ (F_n, G_n, K_n)} = Σ'.L`, and `dom(Σ_m.M) ⊆ dom(Σ'.M)` because each K.σ-prefix introduced only a `d_k ∈ dom(Σ'.M)`. The construction introduces no K.α (class-(ii)) content-emission steps: L1a's precondition on each K.λ-emission depends only on `home(a_k) ∈ dom(Σ_{prev}.M)`, not on any content address, so `dom(Σ_m.C) = dom(Σ.C)` throughout, and `dom(Σ.C) ⊆ dom(Σ'.C)` follows from S1 on the original `↝`-step. ∎

*Worked example 1 — composite create-document-with-initial-link (length-2 decomposition).* Consider a higher-layer operation `CreateDocAndLink` that, in a single atomic `↝`-step, allocates a fresh document `d_new` and emits an initial link `a_new` homed at `d_new`. Concretely: suppose `Σ` is a state with `dom(Σ.M) = {d_old}` (some pre-existing document) and `dom(Σ.L) = ∅`. The composite `↝`-step `Σ ↝ Σ'` produces `Σ'` with `dom(Σ'.M) = {d_old, d_new}`, `dom(Σ'.L) = {a_new}` with `home(a_new) = d_new` and `a_new = d_new.0.s_L.1`, and `Σ'.L(a_new) = (F, G, K)` for some L3-conforming triple. This is a single `↝`-step at the higher layer, but `Σ.L ≠ Σ'.L` and `home(a_new) = d_new ∉ dom(Σ.M)` at the moment Σ is evaluated.

R7a's construction decomposes this composite into a length-2 `→`-sequence `Σ → Σ_1 → Σ_2 = Σ_m` with: (i) Step 1 a K.σ-step `Σ → Σ_1` extending `dom(Σ.M)` with `d_new` — the prefix step required to discharge L1a's `home(a_new) = d_new ∈ dom(·.M)` precondition for the link emission to follow; K.σ's Frame fixes `Σ_1.L = Σ.L = ∅` and `Σ_1.C = Σ.C`. (ii) Step 2 a K.λ-step `Σ_1 → Σ_2` emitting `(F, G, K)` at `a_new = d_new.0.s_L.1` (K.λ's first-emission case at `d = d_new` against the empty homed-set at Σ_1). After Step 2, `Σ_2.L = {a_new ↦ (F, G, K)} = Σ'.L` and `dom(Σ_2.M) = {d_old, d_new} = dom(Σ'.M)`. The Δ-enumeration has `n = 1` with `a_1 = a_new`, `d_1 = d_new ∉ dom(Σ.M)` triggering the K.σ-prefix; the iteration count `m = 2` (one K.σ + one K.λ).

*Worked example 2 — composite create-two-fresh-documents-each-with-initial-link (length-4 decomposition).* The decomposition's interleaving structure is exercised non-trivially when a single `↝`-step affects multiple fresh home documents. Consider a higher-layer operation `CreateTwoDocsAndLinks` that, in a single atomic `↝`-step, allocates two fresh documents `d_A`, `d_B` and emits one initial link homed at each. Concretely: `Σ` has `dom(Σ.M) = ∅` and `dom(Σ.L) = ∅`. The composite `↝`-step `Σ ↝ Σ'` produces `Σ'` with `dom(Σ'.M) = {d_A, d_B}` and `dom(Σ'.L) = {a_A, a_B}` where `home(a_A) = d_A`, `home(a_B) = d_B`, `a_A = d_A.0.s_L.1`, `a_B = d_B.0.s_L.1`, and `Σ'.L(a_X) = (F_X, G_X, K_X)` for `X ∈ {A, B}` (each an L3-conforming triple).

R7a's construction decomposes this composite into a length-4 `→`-sequence `Σ → Σ_1 → Σ_2 → Σ_3 → Σ_4 = Σ_m` (so `m = 4`):

- *Step 1 (K.σ at d_A):* `Σ → Σ_1` extending `dom(Σ.M)` from `∅` to `{d_A}`. K.σ's Frame fixes `Σ_1.L = Σ.L = ∅` and `Σ_1.C = Σ.C = ∅`.
- *Step 2 (K.λ at a_A under d_A):* `Σ_1 → Σ_2` emitting `(F_A, G_A, K_A)` at `a_A = d_A.0.s_L.1` (K.λ's first-emission case at `d = d_A` against `{ℓ' ∈ dom(Σ_1.L) : origin(ℓ') = d_A} = ∅`). After Step 2: `dom(Σ_2.M) = {d_A}`, `dom(Σ_2.L) = {a_A}`.
- *Step 3 (K.σ at d_B):* `Σ_2 → Σ_3` extending `dom(Σ_2.M)` to `{d_A, d_B}`. K.σ's Frame fixes `Σ_3.L = Σ_2.L = {a_A}` and `Σ_3.C = Σ_2.C = ∅`.
- *Step 4 (K.λ at a_B under d_B):* `Σ_3 → Σ_4` emitting `(F_B, G_B, K_B)` at `a_B = d_B.0.s_L.1` (K.λ's first-emission case at `d = d_B` against `{ℓ' ∈ dom(Σ_3.L) : origin(ℓ') = d_B} = ∅` — `a_A` is homed at `d_A ≠ d_B`, so the homed-set at `d_B` is empty). After Step 4: `dom(Σ_4.M) = {d_A, d_B} = dom(Σ'.M)`, `dom(Σ_4.L) = {a_A, a_B} = dom(Σ'.L)`.

The Δ-enumeration is `a_1 = a_A, a_2 = a_B` (or, equivalently, `a_1 = a_B, a_2 = a_A` — the algorithm independently triggers a K.σ-prefix per fresh home regardless of the iteration order). The home-precondition discharge fires twice (once per iteration), each time triggering a K.σ-prefix for a distinct fresh document. The class-(iii) emissions are then issued at the new homes in order. This decomposition exhibits the interleaved K.σ–K.λ–K.σ–K.λ structure that R7a's iteration loop produces when multiple fresh home documents are emitted simultaneously — the iteration's home-document precondition discharge fires across distinct fresh home documents, not just at iteration 1.

**Definition — relational layer.** The relational layer's operations are `{Emit_K, Observe_K, Nullify}`, with `Nullify` a definitional alias for `Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` — `Emit_K` instantiated at three argument positions: `K := R`, `F := ∅`, `G := {(a, δ(1, #a))}`. The layer commits to `Emit_K` (operationally K.λ specialized to standard-triple value `(F, G, K)`) as its sole state-affecting class-(iii) emission, and admits no composites that touch `Σ.L` indirectly. *Nullify-as-sole-`R`-producer discipline:* the layer further commits that callers may invoke `Emit_K` only at type indices `K` satisfying `K ≁ R` (i.e., `coverage(K) ≠ coverage(R)`); every `R`-typed emission is routed through the `Nullify` alias, whose argument shape is fixed to the unit-depth retraction form `(∅, {(a, δ(1, #a))})` by Definition of `Nullify`. Together these two commitments make "every `L_R^Σ` tuple was produced by a `Nullify` call" a definitional property of the relational layer rather than a separately-tracked caller obligation — and, in turn, make the unit-depth retraction discipline (Implementation Notes) hold by definition for all layer-initiated state. `Observe_K` is state-preserving, taking no `→`-step.

*Corollary (reduction to Emit_K).* The relational layer's state-affecting operations reduce to `{Emit_K}` (with `Nullify` as alias).

*Proof.* The layer admits no composites that bundle document allocation with link emission, so R7a's multi-step branch with class-(i) prefix never fires for relational-layer-initiated operations. The layer issues `Emit_K` only when its `d ∈ dom(Σ.M)` precondition is already established, so R7a's replay sequence collapses to length 1: each relational-layer state-affecting operation is itself a single-step class-(iii) `→`-step. By the layer's commitment, every such step is an `Emit_K` call.


## Weakest-Precondition Analysis

The operations' postconditions admit explicit weakest-precondition (wp) computations in two operationally-relevant cases — Nullify's single-tuple scope and Emit_K's membership of the fresh tuple in the active subset. Both cases use the standard wp notation `wp(S, R)`: the weakest predicate over the prior state Σ that guarantees the post-state Σ' satisfies R after S executes.

*Case 1 — wp(Nullify(Σ, d_retr, a), "single-tuple scope holds at Σ'").* The "single-tuple scope" postcondition is `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` (the to-span's `A_rel`-intersection at Σ' is exactly `a`, with no other link address falling within the prefix-subtree of `a`). Working backward through Nullify's definition `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})`:

`wp(Nullify(Σ, d_retr, a), single-tuple scope at Σ') ≡ P0(Σ, d_retr) ∧ P1(Σ, a) ∧ P2(Σ, a)`

where the conjuncts are exactly Nullify's stated preconditions: P0: `d_retr ∈ dom(Σ.M)`; P1: `a ∈ A_rel^Σ`; P2: `|Σ.L(a)| = 3`. P1 combined with L12a discharges `a ∈ A_rel^{Σ'}`. R0a's antichain on `dom(Σ.L)` is unconditional under ASN-0093's K.λ contract, so the no-strict-prefix-extension condition is discharged substrate-wide without an auxiliary conjunct: the internal Emit_R's fresh emitter `b` is prefix-incomparable with `a` at Σ' (`b ∉ {t : a ≼ t}`) by R0a applied to `dom(Σ'.L)`. The wp does *not* include any conjunct on whether the internal emitter `b` is itself nullified — that is a property of `A_R^{Σ'}`, not of single-tuple scope on `a`, and is outside this wp's postcondition.

*Case 2 — wp(Emit_K(Σ, d, F, G), "(a, F, G) ∈ A_K^{Σ'}").* The Definition of `Emit_K` guarantees `(a, F, G) ∈ L_K^{Σ'}` for the fresh emission unconditionally (K.λ deposits `(F, G, K)` at the chain-deterministic address `a`, which is then a member of `L_K^{Σ'}` by coverage-equivalence membership), but is silent on `(a, F, G) ∈ A_K^{Σ'}`, which turns on whether `a ∈ nullified(Σ')`. The post-state retraction slice depends on the K-relation: `L_R^{Σ'} = L_R^Σ ∪ {(a, F, G)}` when `K ~ R`, and `L_R^{Σ'} = L_R^Σ` when `K ≁ R`. Three regimes are operationally relevant — two characterize the pre-state retraction landscape, and a third orthogonal one handles self-nullification under `K ~ R`:

(i) *Unit-depth retraction discipline.* If every `L_R^Σ` tuple is the result of a `Nullify` call — i.e., every retraction has a unit-depth to-span of the form `{(b, δ(1, #b))}` for some target `b ∈ A_rel^Σ` — then each retraction's coverage `{t : b ≼ t}` intersected with `A_rel^{Σ'}` reduces to `{b}` by R0a's antichain on `dom(Σ'.L)`. The fresh `a` produced by Emit_K is, by K.λ's first/subsequent emission rule together with R0a, prefix-incomparable with every `b ∈ A_rel^Σ`. Therefore `a` is not in `coverage(G')` for any `(_, _, G') ∈ L_R^Σ`, hence the pre-state retractions do not nullify `a`.

(ii) *Crafted-span retractions admitted.* Although K.λ enforces the sibling-frontier discipline on emission *addresses*, it does not constrain the *shape* of a link's endsets — in particular, a caller may emit an `R`-typed retraction with a broader-coverage to-span via direct K.λ, e.g. `Emit_R(Σ, d_retr, ∅, {(d, δ(1, #d))})`, whose coverage `{t : d ≼ t}` intersected with `A_rel^Σ` covers every link sited under `d` (and propagates to every link subsequently emitted under `d`, since R3 preserves the retraction tuple). If any `L_R^Σ` tuple has such a crafted span, a fresh `a` emitted under a covered home falls within `coverage(L_R^Σ)` immediately upon emission: `a ∈ nullified(Σ')` at the very step that allocates `a`, and `(a, F, G) ∈ L_K^{Σ'} \ A_K^{Σ'}` — the audit slice records the emission, but the active subset excludes it from emission onward.

(iii) *Self-nullifying R-typed emission.* Orthogonal to (i)/(ii): when `K ~ R`, the fresh emission enters `L_R^{Σ'}` and its own to-set coverage participates in the nullification check at Σ'. If `a_emit(Σ, d) ∈ coverage(G)` — the fresh emitter's address lies within its own to-set coverage — then `a ∈ nullified(Σ')` via the just-emitted tuple itself, independent of any pre-existing retractions, and `(a, F, G) ∈ L_K^{Σ'} \ A_K^{Σ'}` at the very step that allocates `a`. When `K ≁ R`, the fresh tuple is not in `L_R^{Σ'}` and contributes nothing to `nullified(Σ')`; this regime is vacuous.

To back the postcondition through Emit_K's behavior we name the fresh address that K.λ will deposit:

*Definition — `a_emit(Σ, d)`.* For `d ∈ dom(Σ.M)`, the *fresh emission address* `a_emit(Σ, d)` is the address K.λ would deposit at home `d` in state Σ, per K.λ's first/subsequent emission rule:

`a_emit(Σ, d) = [d.0.s_L.1]` when `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d} = ∅` (first-emission branch);
`a_emit(Σ, d) = inc(ℓ_prev, 0)` otherwise, where `ℓ_prev := max{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d}` (subsequent-emission branch).

By the Lemma — Emit_K function-ness, the rule's outcome is uniquely determined by `(Σ, d)`, so `a_emit` is a function. The address `a` that `Emit_K(Σ, d, F, G)` deposits is exactly `a_emit(Σ, d)` (the type-index `K` parameterizes the slot-3 value, not the address selection).

*Definition — `NoCraftedSpanReachesD(Σ, d)`.* The predicate "no pre-existing retraction's to-span coverage contains the address Emit_K is about to deposit under `d`" is

`NoCraftedSpanReachesD(Σ, d) ≡ (A (b, F', G') ∈ L_R^Σ :: a_emit(Σ, d) ∉ coverage(G'))`

— a universal over the audit-slice retraction tuples, asserting that none of their to-set coverages contains the fresh sibling-frontier address. With these auxiliaries the wp reads:

`wp(Emit_K(Σ, d, F, G), (a, F, G) ∈ A_K^{Σ'}) ≡ d ∈ dom(Σ.M) ∧ K ∈ T_admissible ∧ NoCraftedSpanReachesD(Σ, d) ∧ (K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))`

The first three conjuncts characterize the pre-state retraction landscape (regimes (i)/(ii) jointly): `d ∈ dom(Σ.M)` and `K ∈ T_admissible` are Emit_K's own preconditions, and `NoCraftedSpanReachesD(Σ, d)` rules out nullification by any pre-existing `L_R^Σ` tuple. The final conjunct excludes regime (iii): either `K ≁ R` (so the fresh tuple is not in `L_R^{Σ'}` and cannot self-nullify) or `a_emit(Σ, d) ∉ coverage(G)` (so the self-targeting precondition for self-nullification fails). Under the unit-depth retraction discipline (regime (i) holds for the pre-state), `NoCraftedSpanReachesD` is automatic — every `L_R^Σ` tuple has to-span coverage `{t : b ≼ t}` for some `b ∈ A_rel^Σ`, and R0a's antichain on `dom(Σ'.L)` puts `a_emit(Σ, d) ∉ {t : b ≼ t} ∩ A_rel^{Σ'}` for every such `b` — and the wp simplifies to `d ∈ dom(Σ.M) ∧ K ∈ T_admissible ∧ (K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))`.

*Relational-layer discharge.* Under the relational layer's committed operations (`Emit_K`, `Observe_K`, `Nullify` — see Three Operations and Definition of relational layer below), both regime (ii) and regime (iii) are structurally impossible. *For regime (ii):* every `L_R^Σ` tuple arises from a `Nullify` call, and `Nullify` by its Definition produces a unit-depth to-span `{(b, δ(1, #b))}` for some target `b ∈ A_rel^Σ`. The unit-depth retraction discipline therefore holds by definitional commitment of the layer rather than as a separately-checked caller obligation; `NoCraftedSpanReachesD` is discharged at every relational-layer call site. *For regime (iii):* the Nullify-as-sole-`R`-producer discipline restricts direct `Emit_K` calls to type indices `K ≁ R`, so the left disjunct `K ≁ R` of the final conjunct holds trivially for direct callers. R-typed emissions go through `Nullify(Σ, d_retr, a)`, which fires `Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})`; the fresh emitter `b = a_emit(Σ, d_retr)` produced by K.λ in this branch satisfies `b ∉ coverage({(a, δ(1, #a))}) = {t : a ≼ t}` because `b` is fresh (so `b ≠ a`) and R0a's antichain on `dom(Σ'.L)` forces `a ⊀ b` — hence the right disjunct `a_emit(Σ, d) ∉ coverage(G)` holds. The wp simplifies definitionally to `d ∈ dom(Σ.M) ∧ K ∈ T_admissible` at every relational-layer call site. The full conjunct form persists only when callers operate against K.λ directly with crafted retraction spans or self-targeting R-typed emissions (which the substrate does not preclude, but which the relational layer forbids by its own discipline).

The Nullify operation scopes its retraction to the unit-depth-span form (regime (i)); whether the wider crafted-span form (regime (ii)) or self-nullifying R-typed emission (regime (iii)) is admitted is a discipline-level property of caller retraction practice, not a K.λ guarantee.

## Worked Sketch

We illustrate the structure of a retraction cycle in the relational vocabulary, building on the ASN-0043 worked example. Concrete tumbler values are fixed up front; the cycle proceeds in three steps: first, a first-emission step establishing the initial state `Σ_0` from a link-empty precursor `Σ_{-1}` (Step 0); then a retraction (Step 1), then a restoration (Step 2). Steps 0 and 2 exercise K.λ's two emission branches respectively — first-emission (predicate `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d} = ∅`) and subsequent-emission (predicate negated).

*Setup.* Fix:

- `s_L = 2` (link subspace identifier — matching ASN-0093 SubspaceConventionAxiom and the ASN-0043 worked example).
- `d = 1.0.1.0.1` — document address, `zeros(d) = 2`, length `5`, T4-valid; `d ∈ dom(Σ_{-1}.M)` (already allocated by some prior K.σ step at or before `Σ_{-1}`).
- `c₁ = 1.0.1.0.1.0.1.1`, `c₂ = 1.0.1.0.1.0.1.2` — two content addresses in `dom(Σ_{-1}.C)`, both with `subspace_I = 1 = s_C`, `zeros = 3`, depth `8`.
- `k = 3`, `r = 4` — single-component ghost addresses for the classification type `K = {(k, δ(1, 1))}` and the retraction coverage class `[R]` with `R = {(r, δ(1, 1))}`. By construction `coverage(K) ∩ coverage(R) = ∅` (first components 3 and 4 differ; no tumbler extends both prefixes); `K` and `R` lie in distinct coverage classes. *T4-validity note.* Type-endset ghost addresses (per L9, TypeGhostPermission, ASN-0043) need not satisfy T4 — `T4-valid(·)` is required only of allocator outputs under T10a (S7d for documents, ASN-0093 L1c for links). We choose single-component tumblers here to keep the worked sketch's ghosts T4-valid by inspection, but deeper non-T4 tumblers (e.g., `3.0.0.0.1`) would also be admissible.
- `F₁ = {(c₁, δ(1, 8))}`, `G₁ = {(c₂, δ(1, 8))}` — singleton-span endsets covering `c₁` and `c₂` respectively (by PrefixSpanCoverage).
- `Σ_{-1}.L = ∅`, so `L_K^{Σ_{-1}} = ∅`, `L_R^{Σ_{-1}} = ∅`, `nullified(Σ_{-1}) = ∅`, `A_K^{Σ_{-1}} = ∅`.

*Step 0 — first-emission case: K.λ at `d` from empty homed-set, exhibiting `a₁`.* `Σ_{-1} → Σ_0` via `K.λ` (equivalently `Emit_K(Σ_{-1}, d, F₁, G₁)`) emitting `(F₁, G₁, K)` at home `d`. ASN-0093's K.λ first-emission predicate `{ℓ' ∈ dom(Σ_{-1}.L) : origin(ℓ') = d} = ∅` fires (`dom(Σ_{-1}.L) = ∅`), so K.λ deposits at `[d.0.s_L.1]`. Computing concretely: `d = 1.0.1.0.1`, so `d.0` extends `d` with a zero at position 6 to give `1.0.1.0.1.0`; `d.0.s_L = 1.0.1.0.1.0.2`; and `d.0.s_L.1 = 1.0.1.0.1.0.2.1`. So `a₁ := [d.0.s_L.1] = 1.0.1.0.1.0.2.1`.

*Structural witness from ASN-0093.* The underlying structural chain (witnessed by SubAllocatorAxiom — not operationally executed by K.λ) realizes `a₁` as a depth-2 link sub-allocator output:
- `(d, 2)`: child-spawn from `d` opens the shared depth-one allocator `A_{d.0.1}` (per SharedDepthOneAllocator). Its first emission is `1.0.1.0.1.0.1` (length `7`, `zeros = 3`, `E = [1]`).
- Sibling step in `A_{d.0.1}` to `1.0.1.0.1.0.2` (the second emission of `A_{d.0.1}`, which is `b_L(d)` — ASN-0093's link sub-allocator anchor; subspace identifier `s_L = 2` lands at this position by ASN-0093 L0).
- `(b_L(d), 1)`: child-spawn opens the link sub-allocator `A_L(d) = A_{d.0.s_L.1}` (ASN-0093 SubAllocatorAxiom.Exists activates this chain at `d`'s K.σ-step). Its first emission is `t_1^L(d) = [d.0.s_L.1] = 1.0.1.0.1.0.2.1 = a₁`, per ASN-0093 SubAllocatorAxiom.FirstEmission.

K.λ's effect at this step deposits `Σ_0.L = {a₁ ↦ (F₁, G₁, K)}` with `Σ_0.M = Σ_{-1}.M` and `Σ_0.C = Σ_{-1}.C` per K.λ's Frame. Verification at `a₁`: `zeros(a₁) = 3`, `E(a₁) = [2, 1]`, `E(a₁)₁ = 2 = s_L`, `#E(a₁) = 2` (witnessing R0a-Cor2), T4-valid, `origin(a₁) = home(a₁) = 1.0.1.0.1 = d`. ✓ FirstEmissionFreshness (ASN-0093) gives `a₁ ∉ dom(Σ_{-1}.L) ∪ dom(Σ_{-1}.C)` at the K.λ-event committing `a₁`. By R0 (TupleAddressFreshness) and R1 (AddressInjectivity), `a₁` is a fresh, distinct tuple address.

After Step 0: `L_K^{Σ_0} = {(a₁, F₁, G₁)}` (witnessing R3 over the empty `L_K^{Σ_{-1}}`); `L_R^{Σ_0} = ∅`; `nullified(Σ_0) = ∅`; `A_K^{Σ_0} = L_K^{Σ_0} = {(a₁, F₁, G₁)}`. By R0a-Cor1 at Σ_0 with `J_d^{Σ_0} = 0`, the homed-link set at `d` is the singleton prefix `{a₁} = {inc⁰(d.0.s_L.1, 0)}` of `A_L(d)`'s chain enumeration. ✓

*Step 1: Nullify a₁.* `Σ_0 → Σ_1` via `Nullify(Σ_0, d, a₁) = Emit_R(Σ_0, d, ∅, {(a₁, δ(1, 8))})` — the retractor here happens to share `a₁`'s home document, so the caller supplies `d_retr = d`; a different caller homed at `d' ∈ dom(Σ_0.M)` with `d' ≠ d` would supply `Nullify(Σ_0, d', a₁)` instead, with identical effect on `nullified(Σ_1)`. This emission's to-set `{(a₁, δ(1, 8))}` references the link address `a₁` — witnessing *R5* (TupleSelfTargeting): the to-set of an `L_R` tuple refers to another link's address.

Emit_R invokes K.λ at home `d`. The first/subsequent emission predicate fires *subsequent* (since `{ℓ' ∈ dom(Σ_0.L) : origin(ℓ') = d} = {a₁} ≠ ∅`); `ℓ_prev := max{ℓ' ∈ dom(Σ_0.L) : origin(ℓ') = d} = a₁`; K.λ deposits at `inc(a₁, 0) = 1.0.1.0.1.0.2.2`. Set `b₁ = 1.0.1.0.1.0.2.2` — by ChainEnumerationInjectivity (ASN-0093), `b₁` is the second chain element of `A_L(d)` (the first being `a₁ = t_1^L(d)`). By T10a.2 (NonNestingSiblingPrefixes, ASN-0034), `a₁` and `b₁` are distinct siblings of `A_L(d)` and are therefore prefix-incomparable; in particular `a₁ ⊀ b₁` — witnessing *R0* (TupleAddressFreshness): `b₁ ∉ dom(Σ_0.L)` is fresh by FirstEmissionFreshness's generalization through subsequent emissions (chain elements are distinct, and the realized prefix is `{a₁}` at Σ_0, so `b₁` is the next chain index not yet realized).

*L-invariant verification at `b₁`.* R0 verifies each L-invariant against an arbitrary K.λ-emitted address; the concrete `b₁ = 1.0.1.0.1.0.2.2` admits the same checks by direct inspection: L0 (`E(b₁)₁ = 2 = s_L`), L1 (`zeros(b₁) = 3` by ChainUniformZeroCount), L1a (`origin(b₁) = home(b₁) = d`), L1b (`#E(b₁) = 2` by ChainUniformLength), L1c (the structural chain from `d` through `b_L(d)` through `a₁` to `b₁` exists by SubAllocatorAxiom). ✓ The remaining L-invariants (L2, L3, L4(c), L11a, L12, L12a, L12b, L14, L14a, L-fin) discharge by R0's generic argument applied with the concrete `b₁`.

Emit the retraction: `Σ_1.L = Σ_0.L ∪ {b₁ ↦ (∅, {(a₁, δ(1, 8))}, R)}`. Now compute:

- `coverage({(a₁, δ(1, 8))})`: by PrefixSpanCoverage with `#a₁ = 8`, `= {t : a₁ ≼ t}`. Membership: `a₁ ∈ coverage` by reflexivity of `≼`; `b₁ ∉ coverage` since `a₁` and `b₁` agree on positions `1..7` (both `1.0.1.0.1.0.2`) but differ at position `8` (`1` vs `2`) at equal length — neither is a prefix of the other. ✓
- `L_K^{Σ_1} = {(a₁, F₁, G₁)}` — unchanged. Witnesses *R3* (TypedSliceMonotonicity): `L_K^{Σ_0} = {(a₁, F₁, G₁)} ⊆ L_K^{Σ_1}` since the emission targets `L_R`, not `L_K`. Also witnesses *R2* (TupleAddressPermanence): `Σ_1.L(a₁) = Σ_0.L(a₁) = (F₁, G₁, K)`. ✓
- `L_R^{Σ_1} = {(b₁, ∅, {(a₁, δ(1, 8))})}` — the only retraction tuple; no other tuple has type slot coverage-equivalent to `R` (the tuple at `a₁` has type `K` with `coverage(K) ≠ coverage(R)`). Also witnesses *R3* applied to the `R` coverage class: `L_R^{Σ_0} = ∅ ⊆ L_R^{Σ_1}`. ✓
- `nullified(Σ_1) = {a ∈ {a₁, b₁} : a ∈ coverage({(a₁, δ(1, 8))})} = {a₁}`. By Definition of `nullified`, the existential ranges over `L_R^{Σ_1}` (audit slice), so the test is whether `(b₁, ∅, {(a₁, δ(1, 8))}) ∈ L_R^{Σ_1}` directly witnesses `a₁ ∈ coverage(G')` — yes — without recursive evaluation of `b₁`'s status. Witnesses *R6b* (SingleDepthRetraction). ✓
- `A_K^{Σ_1} = L_K^{Σ_1} \ {(a, F, G) : a ∈ nullified(Σ_1)} = ∅`. ✓

The audit predicate `(a₁, F₁, G₁) ∈ L_K` remains true forever (witnessing *R3*); the operational predicate `(a₁, F₁, G₁) ∈ A_K` flips to false at `Σ_1`.

*Step 2: Restore by re-emission.* To restore the classification, we do *not* attempt to nullify the retraction (which by R6b would be ineffective — single-depth checking ignores it). Instead, `Σ_1 → Σ_2` via `Emit_K(d, F₁, G₁)`, re-using the same home `d` as `a₁`. K.λ at home `d` evaluates the subsequent-emission predicate: `{ℓ' ∈ dom(Σ_1.L) : origin(ℓ') = d} = {a₁, b₁} ≠ ∅`; `ℓ_prev := max{a₁, b₁} = b₁` (by T1 lexicographic order, `b₁ > a₁` since they share prefix `1.0.1.0.1.0.2` and differ at position 8 by `2 > 1`); K.λ deposits at `inc(b₁, 0) = 1.0.1.0.1.0.2.3`. Set `a₂ = 1.0.1.0.1.0.2.3` — `A_L(d)`'s third chain element. *R0* witness: `a₂ ∉ dom(Σ_1.L)` is fresh; *R1* (AddressInjectivity) witness: the new tuple address `a₂` is distinct from both `a₁` and `b₁`, so the map `addr` remains injective. L-invariants at `a₂` discharge by R0 applied with substitutions of `a₂` for `b₁`; by R0a-Cor1 at Σ_2, `a₂ = inc²(d.0.s_L.1, 0)` and `a₁, b₁, a₂` are `A_L(d)`'s first three chain elements in order.

Then `Σ_2.L = Σ_1.L ∪ {a₂ ↦ (F₁, G₁, K)}` and:

- `L_K^{Σ_2} = {(a₁, F₁, G₁), (a₂, F₁, G₁)}` — two coverage-class members with identical `(F, G)` at distinct addresses. Witnesses *R3* (monotone extension `L_K^{Σ_1} ⊆ L_K^{Σ_2}`), *R1* (distinct addresses for the two tuples), and *L11b/R0 Consequence (a)* (distinct emissions distinguishable even when content matches). ✓
- `nullified(Σ_2) = {a₁}` — unchanged. Witnesses *R6a* (RetractionStability): `a₁ ∈ nullified(Σ_1) ⟹ a₁ ∈ nullified(Σ_2)`. The only `L_R` tuple is still at `b₁`, whose `coverage(G')` contains `a₁` but not `a₂` since `a₁` and `a₂` are distinct siblings in `A_{a₁}`. *R6b* witnessed again: deciding `a₂ ∈ nullified(Σ_2)` requires only the single-pass check over `L_R^{Σ_2}`, which finds no witnessing tuple. ✓
- `A_K^{Σ_2} = {(a₂, F₁, G₁)}` — the new tuple is active; `a₁` remains in `L_K` but excluded from `A_K` by *R6c* (RestorationByReemission: `(a₁, F₁, G₁) ∈ L_K^{Σ_2} \ A_K^{Σ_2}` for the retracted historical record, and the restoration is the fresh `(a₂, F₁, G₁) ∈ A_K^{Σ_2}` at a different address). ✓

The relational content `(F₁, G₁)` is again present in `A_K`, but at a different tuple address. Provenance and audit cleanly distinguish the two emissions: `a₁` is the historical record, `a₂` is the current assertion. The established `A_K^{Σ_2} = {(a₂, F₁, G₁)}` persists across any subsequent arrangement-modifying step `Σ_2 ↦ Σ_arr`: by L12 (LinkImmutability, ASN-0043) and L12a (LinkStoreMonotonicity, ASN-0043), arrangement-modifying transitions hold `Σ.L` identical (`Σ_arr.L = Σ_2.L`); since `A_K^Σ`, `L_K^Σ`, `L_R^Σ`, and `nullified(Σ)` depend only on `Σ.L` by their Definitions, every such `Σ.L`-derived quantity is preserved pointwise — in particular, `A_K^{Σ_arr} = A_K^{Σ_2} = {(a₂, F₁, G₁)}`. (R6c-Corollary's stated conclusion is the narrower fact that the retracted tuple `(a₁, F₁, G₁)` remains outside `A_K^{Σ_arr}`, which is one consequence of this pointwise preservation; the broader full-`A_K` preservation cited here uses the same L12 + L12a underpinning.)

*R0a-Cor1/Cor2 verification at Σ_2.* The set of link addresses homed at `d` is `{a₁, b₁, a₂} = {incʲ(d.0.s_L.1, 0) : 0 ≤ j ≤ 2}` — a contiguous prefix of `A_L(d)`'s chain enumeration (by ASN-0093 ChainMembershipForOrigin) — so R0a-Cor1 holds at Σ_2 with `J_d^{Σ_2} = 2`. ✓ Each of `a₁ = 1.0.1.0.1.0.2.1`, `b₁ = 1.0.1.0.1.0.2.2`, `a₂ = 1.0.1.0.1.0.2.3` has element-field projection of length 2 (E = `[2, 1]`, `[2, 2]`, `[2, 3]` respectively) by ChainUniformLength, so R0a-Cor2 holds at Σ_2. ✓


## Properties Introduced

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| SharedDepthOneAllocator | LEMMA | Under each `d ∈ dom(Σ.M)`, T10a admits at most one allocator at allocator-tree depth 1 and zero-count depth 1 — `A_{d.0.1}`, opened by `(d, 2)`; when opened it is shared across subspaces. The subspace-specific depth-2 allocators `A_C(d) = A_{d.0.s_C.1}` and `A_L(d) = A_{d.0.s_L.1}` are ASN-0093's sub-allocators (= ASN-0093 L0 + T10a + TA5(d) + T4 + S7d/M0) | introduced |
| A^Σ | DEF | Address universe at state Σ: `dom(Σ.C) ∪ dom(Σ.L)` | introduced |
| A_doc^Σ, A_rel^Σ | DEF | Partition of `A^Σ` into content addresses (`dom(Σ.C)`) and tuple addresses (`dom(Σ.L)`) | introduced |
| T_ghost^Σ | DEF | Ghost addresses at Σ: `T \ (dom(Σ.C) ∪ dom(Σ.L))` — tumblers outside the stored-entity universe, admissible in endset spans by L9 | introduced |
| T_admissible | DEF | Admissible types: `{K ∈ Endset : K ≠ ∅}` — the indexing domain for typed relations | introduced |
| T_cat^Σ | DEF | Type catalog at Σ — admissible types actually in use at Σ (descriptive, not constitutive) | introduced |
| ~ | DEF | TypeEquivalence: `K ~ K' ≡ coverage(K) = coverage(K')` — coverage-equivalence on admissible types (= L8 lifted) | introduced |
| L_K^Σ | DEF | Typed relation (coverage-class slice): `{(a, F, G) : a ∈ dom(Σ.L) ∧ |Σ.L(a)| = 3 ∧ Σ.L(a).e₁ = F ∧ Σ.L(a).e₂ = G ∧ coverage(Σ.L(a).e₃) = coverage(K)}` | introduced |
| L^Σ | DEF | Standard-triple link store: `⨆_{[K] ∈ T_admissible / ~} L_K^Σ` | introduced |
| addr | DEF | Map `(a, F, G) ↦ a : L^Σ → A_rel^Σ` | introduced |
| nullified(Σ) | DEF | Tuple addresses targeted by some `L_R^Σ` to-set | introduced |
| A_K^Σ | DEF | Active subset: `{(a, F, G) ∈ L_K^Σ : a ∉ nullified(Σ)}` | introduced |
| → | DEF | Dom-extending state transition relation, identified as `K.σ ∪ K.α ∪ K.λ` from ASN-0093; each class-(iii) step is a K.λ-step with its first/subsequent emission rule and its associated frame conditions. Arrangement modifications live in a parallel transition vocabulary handled in ASN-0036 | introduced |
| Unit-depth retraction discipline | DEF | (Implementation Notes) Relational-layer commitment: every `L_R^Σ` tuple has to-endset of the form `{(b, δ(1, #b))}` for some target `b ∈ A_rel^Σ` — i.e., every retraction came from a `Nullify` call. The substrate (K.λ) does not enforce this; the relational layer does, by definition of Nullify | introduced |
| R0 | LEMMA | TupleAddressFreshness — under precondition `dom(Σ.M) ≠ ∅`, every emission allocates a fresh address. Discharged via ASN-0093 K.λ's first/subsequent emission rule, plus FirstEmissionFreshness (first-emission branch), ChainMembershipForOrigin + ChainEnumerationInjectivity + ChainPrefixExtension + CrossDocDisjointness + DisjointSubAllocatorChains + ASN-0093 L0 + SC-NEQ + T10 (subsequent-emission branch's three-part freshness against same-home chain, cross-home links, and content), L-invariant preservation under K.λ's frame, and ASN-0093 L0 + SC-NEQ for L14/L14a | introduced |
| R0a | LEMMA | FlatLinkDomain — `dom(Σ.L)` is an antichain in `≼`. Unconditional under ASN-0093's K.λ contract (= Case 1 cross-home via L1 + L1a; Case 2 same-home via ASN-0093 ChainMembershipForOrigin + ChainUniformLength + T3, equivalently via T10a.2) | introduced |
| R0a-Cor1 | LEMMA | ContiguousPrefix — `{a ∈ dom(Σ.L) : home(a) = d} = {incʲ(d.0.s_L.1, 0) : 0 ≤ j ≤ J_d^Σ}` for some `J_d^Σ ∈ ℤ_{≥-1}`; direct re-expression of ASN-0093's ChainMembershipForOrigin lemma | introduced |
| R0a-Cor2 | LEMMA | DepthTwoLinkAddresses — `#E(a) = 2` strictly for every `a ∈ dom(Σ.L)`; tightens L1b's `#E ≥ 2` admission to depth-2 strictly (= R0a-Cor1 + ChainUniformLength + ChainUniformZeroCount + zero-position stability via TA5(c) + TA5-SigValid + T10a.4 [equivalently ChainPrefixExtension]) | introduced |
| R1 | LEMMA | AddressInjectivity — `addr` is an injection (= function property of `Σ.L`) | introduced |
| R2 | LEMMA | TupleAddressPermanence — addresses persist with values intact (= L12) | introduced |
| R3 | LEMMA | TypedSliceMonotonicity — each `L_K^Σ` is monotone (= L12a + R2) | introduced |
| R4 | LEMMA | TupleAddressDisjointness — `A_doc^Σ ∩ A_rel^Σ = ∅` (= ASN-0093 L14 (StoreDisjointness), whose underlying derivation is ASN-0093 L0 + SC-NEQ + T7) | introduced |
| R5 | LEMMA | TupleSelfTargeting — for any `a ∈ A_rel^Σ`, the span `(a, δ(1, #a))` is admissible as an endset member (= L4(c) + L13 + R0's invariant-preservation argument, which imposes no restriction on endset target content) | introduced |
| R6a | LEMMA | RetractionStability — once nullified, always nullified (= R3 + R2 + purity of coverage) | introduced |
| R6b | DEF-Consequence | SingleDepthRetraction — `nullified` checks only direct targeting (single-pass existential over `L_R^Σ`); a tautological consequence of the Definition's quantification range over `L_R^Σ` (audit slice) rather than `A_R^Σ` (active subset), named for its substantive decision-procedure-flatness implication on retraction-of-retraction | introduced |
| R6c | LEMMA | RestorationByReemission — formal claim on `⊑` (reflexive-transitive closure of dom-extending `→`): restoration is fresh emission, never retraction-of-retraction (= R6a + Extension definition) | introduced |
| R6c-Corollary | LEMMA | RestorationByReemission on `⊑̂` — the same conclusion lifts to the broader transition relation including arrangement-modifying steps (= R6c + ASN-0043 L12 + L12a (Σ.L invariance under M-modification) + `A_K^Σ` depends only on `Σ.L`) | introduced |
| R7a | LEMMA | NoExtraClassAffectsL — for any state-affecting `Σ ↝ Σ'` issued by a substrate-conforming layer with `Σ.L ≠ Σ'.L`, the `Σ.L`-affecting effect decomposes into K.λ-steps interleaved with K.σ-setup steps for L1a's home-precondition: `Σ = Σ_0 → Σ_1 → … → Σ_m` (`m ≥ 1`) with `Σ_m.L = Σ'.L`, `dom(Σ_m.M) ⊆ dom(Σ'.M)`, `dom(Σ_m.C) = dom(Σ.C) ⊆ dom(Σ'.C)`. Substrate-conformance (L12 + L12a on the link store; S0 + S1 on the content store) is lifted into R7a's claim statement (= L12 + L12a + L-fin + L1a + S7d + ASN-0093 K-op frame conditions + ASN-0093 ChainMembershipForOrigin for replay determinism) | introduced |
| Relational layer | DEF | Operation set `{Emit_K, Observe_K, Nullify}`; `Emit_K` is the layer's sole state-affecting class-(iii) emission (operationally K.λ specialized to standard-triple value `(F, G, K)`); `Nullify` ≡ `Emit_R` with designated argument shape; `Observe_K` is state-preserving. Corollary: by R7a + the commitment, all `Σ.L`-affecting relational-layer state change reduces to `Emit_K` calls. Adopted as the relational layer's charter; the K.λ contract makes the sibling-frontier discipline a substrate-level guarantee, so this commitment only restricts the *value-shape* of relational-layer emissions, not their address pattern | introduced |
| Emit_K | OP | State-transforming: `Σ × dom(Σ.M) × Endset × Endset → Σ' × A_rel^{Σ'}`, operationally K.λ specialized to value `(F, G, K)`. Function-ness over the full state space follows from K.λ's deterministic first/subsequent emission rule (R0a-Cor1 fixes the unique max element under T1). Caller-supplied home document `d ∈ dom(Σ.M)` and `K ∈ T_admissible`; the `dom(Σ.M) ≠ ∅` precondition of R0 is enforced by parameter typing | introduced |
| Observe_K | OP | Pure read: `Σ × ℘_fin(T) × ℘_fin(T) × View → ℘_fin(L_K^Σ)`, selecting `L_K^Σ` or `A_K^Σ`. Patterns range over the full tumbler space `T` (not `A^Σ`) to admit ghost-targeting queries per L9 + L4 | introduced |
| Nullify | OP | `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` for caller-supplied `d_retr ∈ dom(Σ.M)` and `a ∈ A_rel^Σ` with `|Σ.L(a)| = 3`. Single-tuple scope is *absolute* as a substrate-level guarantee from R0a (itself unconditional under K.λ); not a per-call obligation (= R5 + R0 + R0a + R6a + L12) | introduced |

## Open Questions

- What invariants must hold between `L_K` and the arrangements `Σ.M` when relational predicates depend on whether the from-set or to-set content is currently visible in some document?
- Should multi-arity links (`|Σ.L(a)| > 3`) define multiple binary projections, or be regarded directly as elements of higher-arity typed relations `L_K^{(n)} ⊆ A_rel × ℘(A)^n`?
- Under what conditions is `Nullify(b)` for `b ∈ L_R` operationally meaningful, given that R6b makes single-depth checking ignore the second-order retraction?
- What ordering, if any, must the substrate guarantee on Observe results — by emission cycle, by tuple address, or unordered as set semantics suggest?
- Must Emit be atomic with respect to concurrent Observe, and if so, what is the consistency model under which `A_K` transitions are observed?
- What guarantees does the substrate provide about the cardinality bound of `nullified(Σ)` relative to `dom(Σ.L)` — is unbounded retraction permitted, or must some structural ratio hold?
- Should L1b's substrate-level admission `#E ≥ 2` (ASN-0043) be tightened to `#E = 2` to match Nelson's design intent at the substrate layer? R0a-Cor2 establishes `#E = 2` unconditionally within the substrate via ASN-0093's K.λ contract; the question is whether L1b itself should reflect the intent more strictly (closing the substrate-level gap at the source) or whether retaining `#E ≥ 2` in L1b is the right design point — leaving room for higher-arity or future variants while the standard-triple links of this note remain depth-2 by R0a-Cor2.
- Should the relational layer's unit-depth retraction discipline (Implementation Notes) be elevated to a substrate-level guarantee on `L_R` to-spans — e.g., by introducing a designated K-operation for retraction with a unit-depth shape constraint — or is it correctly a layer convention that callers may bypass via direct K.λ with crafted retraction spans? WP Case 2 makes the consequence of the latter explicit; the design tradeoff is whether the substrate should expose any value-shape constraint on retraction tuples.
- Can higher layers extend the type catalog `T_cat` dynamically without coordination, given L9 (TypeGhostPermission), and what happens when two layers independently choose colliding type addresses?