# ASN-0086: Typed Relations on Address Sets

*Drawing the link model forward into a relational vocabulary*

ASN-0043 establishes the link as a primitive: an addressed, owned, typed connection between spans of content. We now adopt a different vocabulary for the same structure. Where ASN-0043 speaks of *links* and *endsets*, we speak of *tuples* and *typed relations*. The two vocabularies describe one object — a standard-triple link `(F, G, Θ)` at address `a ∈ dom(Σ.L)` is a tuple in a typed relation indexed by `Θ` — but predicates compose more cleanly over relations than over endsets, and several substrate-level guarantees become easier to state in this form.

We are looking for what a relation algebra over the link store affords. The answer is six structural properties, of which five (R0–R5) are derivable from ASN-0043 and one (R6, the active subset) is the substrate's own contribution — made possible by R5 (the existence of a self-referential retraction relation) and R3 (the audit trail it is computed against). The six properties suffice to define three operations under which all visible substrate change reduces to a single primitive: Emit.


## The Two Foundational Sets

**Setup hypothesis.** We work in systems satisfying ASN-0043 (and therefore ASN-0036 and ASN-0034). We additionally assume globally `s_C`-resident content:

`(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)`

Under this hypothesis the disjointness between content and tuple addresses (R4 below) holds substrate-wide as a structural property, not merely within the slice scoped to `s_C` that L14 (DualPrimitive, ASN-0043) supplies in its stated form.

**Definition — AddressUniverse.** The substrate's address universe at state Σ is

`A^Σ = dom(Σ.C) ∪ dom(Σ.L)`

By L14 (DualPrimitive, ASN-0043) and the setup hypothesis, `A^Σ` is the entirety of stored-entity addresses at Σ; no third category exists.

**Definition — Partition.** Define:

`A_doc^Σ = dom(Σ.C)` &nbsp; — content addresses
`A_rel^Σ = dom(Σ.L)` &nbsp; — relation-tuple addresses

We claim `A^Σ = A_doc^Σ ⊔ A_rel^Σ` (disjoint union). The disjointness is R4 below.

*Notation.* All three sets are state-dependent — they grow as the substrate evolves. Where the ambient state is unambiguous, we drop the superscript and write `A`, `A_doc`, `A_rel`.

**Definition — TypeCatalog.** The set of *admissible types* is

`T_admissible = {K ∈ Endset : K ≠ ∅}`

— non-empty endsets, eligible to serve as a link's type endset by L3 (NEndsetStructure, ASN-0043). For each state Σ, the *type catalog at Σ* is the subset actually in use:

`T_cat^Σ = {Θ ∈ T_admissible : (E a ∈ dom(Σ.L) :: |Σ.L(a)| = 3 ∧ Σ.L(a).e₃ = Θ)}`

By L4 (EndsetGenerality, ASN-0043) and L9 (TypeGhostPermission, ASN-0043), `T_admissible` is unconstrained by content existence: type endsets may reference any tumbler addresses, including ghosts. We require only that type-equality is decidable by endset comparison — which it is, by L8 (TypeByAddress).

Type indices in what follows range over `T_admissible`, not `T_cat^Σ`. `T_cat^Σ` is descriptive — the snapshot of which types are populated at state Σ — but is not constitutive: `L_K^Σ` (below) is well-defined for any `K ∈ T_admissible` and is simply empty when `K ∉ T_cat^Σ`. This avoids the bootstrap circularity that would arise if `K ∈ T_cat^Σ` were required as a precondition for introducing a genuinely new type via emission.

For the rest of this development we restrict attention to standard-triple links — those with `|Σ.L(a)| = 3`. Higher-arity links (L3, NEndsetStructure, ASN-0043) exist in `dom(Σ.L)` but are not members of any `L_K`; they admit an analogous construction with additional slot positions, which we do not pursue here.


## The Typed Relation

**Definition — TypedRelation.** For each `K ∈ T_admissible` and state Σ, the *typed relation of type K at Σ* is

`L_K^Σ = {(a, F, G) : a ∈ dom(Σ.L) ∧ |Σ.L(a)| = 3 ∧ Σ.L(a) = (F, G, K)}`

Each member is a triple of (tuple-address, from-endset, to-endset). The pair `(F, G)` is the *relational content* of the tuple; `a` is the *tuple address*. The substrate's standard-triple link store at state Σ is the disjoint union over admissible types:

`L^Σ = ⨆_{K ∈ T_admissible} L_K^Σ`

We will show (R1) that this disjoint union is well-defined: each tuple address belongs to exactly one type-slice. Note that `L^Σ` collects only the arity-3 links; higher-arity links in `dom(Σ.L)` are outside its scope, as noted above. Where ambient state is clear we drop the superscript and write `L_K`, `L`.

**Definition — TupleAddress.** Define `addr : L^Σ → A_rel^Σ` by `addr(a, F, G) = a`.

*Remark — relation to ℘(A) × ℘(A).* A generic mathematical typed relation is a subset of `℘(A) × ℘(A)` — a set of address-pair-pairs distinguished only by content. Our typed relation is richer: each tuple carries an address that participates in the relation's identity. The projection `(a, F, G) ↦ (coverage(F), coverage(G))` recovers the address-pair view, but it loses information that the substrate retains (R0, R1).


## Tuple Identity (R0, R1, R2)

A generic mathematical relation distinguishes its members only by content: two tuples with identical (F, G) are the same tuple. The substrate's relations do not work that way. Each tuple emission allocates a fresh address (R0), the address-to-pair binding is a function (R1), and the binding is permanent (R2).

**R0 — TupleAddressFreshness.** For any state Σ with `dom(Σ.M) ≠ ∅` and any `(F, G, K) ∈ Endset × Endset × T_admissible`, there exists a state Σ' with Σ → Σ' that emits a tuple with content (F, G) of type K at a fresh address:

`(A Σ : dom(Σ.M) ≠ ∅ :: (A F, G ∈ Endset, K ∈ T_admissible :: (E Σ' extending Σ, a : a ∉ dom(Σ.L) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = (F, G, K))))`

*Proof.* We construct the witness in four steps.

(Step 1 — locate a document subspace.) By precondition, `dom(Σ.M) ≠ ∅`; pick any `d ∈ dom(Σ.M)`. By ASN-0036, `d` is a document address whose link subspace `s_L(d)` is well-defined. By L1a (LinkResidence, ASN-0043), every link address resides in some `s_L(d')`.

(Step 2 — exhibit an unoccupied valid link address.) By L1b (LinkElementFieldDepth, ASN-0043), valid link addresses within `s_L(d)` have a specified depth structure compatible with T1 (TumblerStructure, ASN-0034). By T0(a) (UnboundedComponentValues, ASN-0034), each tumbler component admits unbounded values, so the set of valid link addresses within `s_L(d)` is countably infinite. By L-fin (LinkStoreFiniteness, ASN-0043), `|dom(Σ.L)| < ∞`. The difference between a countably-infinite set and a finite subset is non-empty, so some unoccupied valid link address `a ∈ s_L(d) \ dom(Σ.L)` exists.

(Step 3 — verify allocator admits `a`.) By L1c (LinkAllocatorConformance, ASN-0043), link allocation conforms to T10a (AllocatorDiscipline, ASN-0034). By T10a.4 (NoReuse, ASN-0034), the allocator never returns an address already in `dom(Σ.L)`, so `a` (being unoccupied) is admissible as an allocator output. By T10a.5 (FreshnessGuarantee, ASN-0034), the allocator's output for the current call is permitted to be `a` provided `a` is unallocated, which Step 2 established. By T10a.6 (DeterministicExtension, ASN-0034), the allocator's choice extends to a fresh subspace position without conflict.

(Step 4 — exhibit Σ'.) Define `Σ'` by extending `Σ.L` with `Σ'.L(a) = (F, G, K)`, leaving `Σ.C` and `Σ.M` unchanged. We verify: (i) `Σ'.L` remains a partial function (extension at a fresh key); (ii) `(F, G, K)` is a well-formed standard-triple link by L3 (NEndsetStructure, ASN-0043) since `F, G ∈ Endset` and `K ∈ T_admissible` is non-empty; (iii) L1a–L1c hold (`a ∈ s_L(d)` by construction, allocator-conformant by Step 3); (iv) L11b (NonInjectivity, ASN-0043) is unaffected — value-level coincidence with any pre-existing link is permitted; (v) L12 (LinkImmutability) holds — no existing entry was modified; (vi) L-fin holds — finite plus one is finite. The L11b witness construction confirms that such an extension preserves all invariants of ASN-0043 and ASN-0036. ∎

*Remark on the precondition.* The hypothesis `dom(Σ.M) ≠ ∅` is necessary: by L1a (LinkResidence), every link address lives in some document's link subspace, so before any document exists, no link can be allocated. Once at least one document is present, R0 supplies a fresh link address; in particular, R0 may be invoked recursively to add links into the same document or into any subsequently emitted one.

**R1 — AddressInjectivity.** The map `addr : L → A_rel` is an injection:

`(A (a, F, G), (a', F', G') ∈ L : a = a' :: F = F' ∧ G = G' ∧ both belong to the same L_K)`

*Proof.* `Σ.L` is a partial function `T ⇀ Link` (ASN-0043, Definition of LinkStore). Function-ness gives uniqueness of value: if `a = a'`, then `Σ.L(a) = Σ.L(a')`, and that single value determines the triple `(F, G, K)`. Therefore `F = F'`, `G = G'`, and `K = K'`, whence both members of `L` lie in `L_K`. ∎

**R2 — TupleAddressPermanence.** Once allocated, a tuple address resolves permanently to the same relational content:

`(A Σ → Σ', a ∈ dom(Σ.L), (F, G, K) = Σ.L(a) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = (F, G, K))`

*Proof.* Direct from L12 (LinkImmutability, ASN-0043): for every state transition, every existing link address persists with its value unchanged. ∎

*Consequences (S1, S2 in the original presentation).*

(a) *Distinct emissions are distinguishable even when content matches.* Two agents independently filing tuples with identical `(F, G)` under identical `K` produce distinct addresses (R0 produces a fresh address regardless of value). By L11b (NonInjectivity, ASN-0043), value-level coincidence is permitted; by R1, address-level identity nevertheless distinguishes them. The substrate does not silently merge them.

(b) *Counting is well-defined.* `|{(a, F, G) ∈ L_K : pattern matches (F, G)}|` is a number, not an equivalence-class size, because the elements counted are distinct addresses (R1).

(c) *Audit references are stable forever.* An address written into the to-set of any tuple in cycle 1 still resolves to the same emission in cycle N, after the substrate has grown by orders of magnitude (R2). The reference does not need re-validation.

(d) *Idempotency on emit is policy, not substrate guarantee.* The substrate accepts duplicate emissions — R0 produces a fresh address regardless of whether identical content already exists. Higher layers wishing at-most-once semantics check `(E (a, F, G) ∈ L_K^Σ :: F, G match)` before calling Emit. This is a layer above the substrate's primitive.


## Append-Only Slices (R3)

**R3 — TypedSliceMonotonicity.** Each typed relation grows monotonically:

`(A Σ → Σ', K ∈ T_cat :: L_K^Σ ⊆ L_K^{Σ'})`

where `L_K^Σ` denotes the typed relation evaluated at state `Σ`.

*Proof.* Let `(a, F, G) ∈ L_K^Σ`. Then `a ∈ dom(Σ.L)` with `Σ.L(a) = (F, G, K)`. By L12a (LinkStoreMonotonicity, ASN-0043), `dom(Σ.L) ⊆ dom(Σ'.L)`; by R2, `Σ'.L(a) = (F, G, K)`. Therefore `(a, F, G) ∈ L_K^{Σ'}`. ∎

*Consequences (S3).*

(a) *One-directional audit stability.* "A tuple of type K with this `(F, G)` existed at some point" stays true once true. Histories do not rewrite themselves.

(b) *Retractions are themselves auditable.* When we introduce the retraction type `R` (R6), `L_R` is one of the typed slices and R3 applies to it as well. Every nullification leaves an entry in `L_R` that persists.

(c) *Historical replay is well-defined.* `L_K` at past cycle `n` is a prefix of `L_K` at any cycle `m ≥ n`; "what was the substrate at cycle n?" is computable from the current substrate and a cycle-cutoff predicate. No separate snapshot mechanism is required.

(d) *No information loss.* No compaction, no garbage collection, no archive tier removes tuples from `L_K`. The substrate's reliability for downstream agents — that an emission in cycle 3 is still observable in cycle 30 — is exactly R3.


## Subspace Disjointness (R4)

**R4 — TupleAddressDisjointness.** Under the setup hypothesis, tuple addresses and document-content addresses are disjoint:

`A_doc^Σ ∩ A_rel^Σ = ∅`

*Proof.* Let `a ∈ A_doc^Σ = dom(Σ.C)`. By the setup hypothesis (globally `s_C`-resident content), `subspace_I(a) = s_C`. Now consider any `a' ∈ A_rel^Σ = dom(Σ.L)`. By L0 (SubspacePartition, ASN-0043), every link address resides in the link subspace component: `subspace_I(a') = s_L`. By T7 (FirstElementFieldDistinction, ASN-0034), `s_C ≠ s_L` are distinct tumbler subspaces, and addresses in distinct subspaces are themselves distinct as tumblers. Therefore `a ≠ a'`. Since `a, a'` were arbitrary, `A_doc^Σ ∩ A_rel^Σ = ∅`. ∎

*Remark on L14's scoped form.* L14 (DualPrimitive, ASN-0043) supplies disjointness scoped to its hypothesis on which subspace each content address inhabits; here the setup hypothesis is what discharges that scoping globally. The structural reason — distinct first-component subspaces (T7) — is the same in either form. Where future work admits `s_L`-resident content, R4 would be replaced by L14 in its native scoped form, and the consequences below would apply slice by slice rather than substrate-wide.

*Consequences (S4).*

(a) *Predicates are typeable.* A predicate like `is_classified(d, K)` has signature `A_doc × T_cat → Bool`; a predicate like `is_active(τ)` (R6) has signature `A_rel → Bool`. No predicate has an ambiguous signature; categorical confusion at the address level is impossible.

(b) *Retraction is well-typed.* Only `A_rel` addresses are valid arguments to Nullify (R6). "Retracting a document" is not directly expressible — the to-set of an `L_R` tuple must contain a tuple address, not a document address. Document removal from active consideration is done via classifier tuples (e.g., `L_retired`) targeting the document; the document's `A_doc` address is never disturbed.

(c) *Lifecycle separation.* Documents have mutable bodies (arrangements `Σ.M` change per ASN-0036); tuples never mutate (R2). The address-level structure permits these to diverge without interference.


## Self-Reference (R5)

**R5 — TupleSelfTargeting.** A tuple's from-set or to-set may reference tuple addresses. Specifically, for any state Σ and any `a ∈ A_rel^Σ`, the unit-depth span `(a, δ(1, #a))` is well-formed and may appear in the from-set or to-set of an emitted tuple, with `a` in its coverage.

*Justification (positive permission).* We argue in two stages.

(Stage 1 — the construct is permitted.) L4(c) (EndsetGenerality, ASN-0043) explicitly states that endset spans may reference addresses in the link subspace `s_L` — i.e., addresses of other links. L13 (ReflexiveAddressing, ASN-0043) establishes that for any address `b`, the unit-depth span `(b, δ(1, #b))` is well-formed with coverage `{t : b ≼ t}` ⊇ `{b}`. Specializing to `b = a` with `a ∈ A_rel^Σ`, the span `(a, δ(1, #a))` is well-formed by L13 and is span-target-admissible by L4(c). The L11b (NonInjectivity, ASN-0043) witness shows that an emission carrying such a span as an endset component preserves all L-invariants.

(Stage 2 — no invariant opposes the construct.) An exhaustive check of the ASN-0043 invariants confirms none is in opposition to the construction in Stage 1. We list each and identify why:

- L0 (SubspacePartition): constrains link-address residence (`s_L`), is silent on endset-target subspace.
- L1a–L1c, L-fin (residence, depth, allocator, finiteness): constrain `Σ.L`'s domain, not span values within endsets.
- L2 (ZeroEndsetExclusion): forbids `K = ∅`, not `a ∈ A_rel` as a span target.
- L3 (NEndsetStructure): requires `|Σ.L(a)| ≥ 2`; agnostic to span targets.
- L4 (EndsetGenerality), L4(c): the positive permission used in Stage 1.
- L5 (EndsetSpanWellFormedness): requires only T12 compliance, which `(a, δ(1, #a))` satisfies by L13.
- L6, L7 (OrderingLaws, EndsetEquality): operate on endset values; orthogonal to target subspace.
- L8 (TypeByAddress): operates on type slot; orthogonal.
- L9 (TypeGhostPermission): permits non-content type endsets; if anything, broadens what can be referenced.
- L10 (Owner): identifies emitting agent; orthogonal to span targets.
- L11, L11b (LinkPermanence, NonInjectivity): permanence and value-coincidence allowance; both compatible.
- L12, L12a (LinkImmutability, LinkStoreMonotonicity): forbid mutation, not new emissions with self-targeting endsets.
- L13 (ReflexiveAddressing): the constructive lemma used in Stage 1.
- L14 (DualPrimitive): asserts content/link residence disjointness; does not restrict targets.

The R-properties already derived (R0–R4) similarly impose no restriction on what addresses an emitted endset may contain. Therefore the construct is permitted by some invariant (L4(c) + L13) and contradicted by none — it is admissible. ∎

*Modal note.* R5 differs in modality from R0–R4: those are *positive lemmas* (the substrate exhibits the property); R5 is a *permission claim* (the substrate does not forbid the construction and supplies the means to perform it). The worked example in ASN-0043 Step 2 exhibits a meta-link of exactly this form, confirming the permission is exercised within ASN-0043's own examples.

*Consequences (S5).* Several constructs that would otherwise require out-of-band machinery collapse into the relational primitive:

(a) *Retraction.* A tuple in a designated relation `L_R` whose to-set contains the address of the tuple being nullified. Mutation becomes Emit; `L_K` is never modified (R3).

(b) *Resolution.* A tuple in `L_resolution` whose to-set contains a comment-tuple's address. Comment lifecycle is uniformly substrate-tracked; "this comment is closed" is an ordinary observation, not a flag stored elsewhere.

(c) *Agent provenance.* A tuple whose from-set contains an agent's address and whose to-set contains the emitted tuple. Every emission has an attributable emitter as a substrate fact, with no separate metadata channel.

(d) *Higher-order predicates.* "Has τ been retracted?", "who emitted τ?", "what tuples target τ?" — all are ordinary observations over `L_K`, evaluated by the same machinery as predicates over documents.

Without R5, each construct would require its own layer that predicates could not see and that the audit trail (R3) would not preserve. R5 collapses such layers into the relational structure.


## The Active Subset (R6)

R0–R5 are derivable from ASN-0043. The active subset is the substrate's own contribution — added here, not present in Nelson's link model. It is made possible by R5 (a self-referential retraction relation can exist) and R3 (the retraction relation accumulates monotonically, providing the audit trail against which the active subset is computed).

**Definition — RetractionType.** Fix a designated type endset `R ∈ T_admissible` reserved for retraction. The corresponding typed relation `L_R^Σ` is the *retraction relation at state Σ*. By L9 (TypeGhostPermission, ASN-0043), `R` need not refer to anything stored — it is an admissible endset chosen by convention, and is well-defined as a type index regardless of whether `R ∈ T_cat^Σ` at any particular state. Before the first retraction emission, `L_R^Σ = ∅` and `R ∉ T_cat^Σ`; after the first such emission, `R ∈ T_cat^Σ`. The definition of `L_R^Σ` does not depend on which case applies.

**Definition — Nullified.** The set of *nullified* tuple addresses at state `Σ` is

`nullified(Σ) = {a ∈ A_rel^Σ : (E (b, F', G') ∈ L_R^Σ :: a ∈ coverage(G'))}`

By R5, `coverage(G')` may include `A_rel^Σ` addresses, so `nullified(Σ)` is well-defined as a subset of `A_rel^Σ`.

**Definition — ActiveSubset.** For each `K ∈ T_admissible`, the *active subset of type K at state Σ* is

`A_K^Σ = {(a, F, G) ∈ L_K^Σ : a ∉ nullified(Σ)}`

**R6 — ActiveSubsetWellDefinedness.** For every state `Σ` and every `K ∈ T_admissible`, `A_K^Σ` is well-defined and computable from `Σ.L` alone, with no auxiliary state.

*Proof.* `nullified(Σ)` is determined entirely by `L_R^Σ`, which by Definition of TypedRelation is determined by `Σ.L`. `A_K^Σ` is a set-difference between `L_K^Σ` and tuples whose addresses lie in `nullified(Σ)`; both inputs are determined by `Σ.L`. No flag, no version field, no separate snapshot is consulted. ∎

**R6a — RetractionStability.** Once a tuple's address is nullified, it stays nullified across all future state transitions:

`(A Σ → Σ', a ∈ A_rel^Σ : a ∈ nullified(Σ) :: a ∈ nullified(Σ'))`

*Proof.* Recall that `coverage : Endset → ℘(A)` is a pure function on endset values, fixed by the substrate model (ASN-0043, Definition of coverage): given an endset value `E`, `coverage(E)` is determined entirely by `E` and the tumbler-order relation `≼`, which itself is state-independent (T1, ASN-0034). In particular, `coverage(E)` does not depend on the state Σ in which `E` is evaluated.

Suppose `a ∈ nullified(Σ)`. By Definition, there exist `b ∈ dom(Σ.L)` and `(b, F', G') ∈ L_R^Σ` with `a ∈ coverage(G')`. We exhibit the same witness at Σ': by R3 (applied to the type slice indexed by `R`), `L_R^Σ ⊆ L_R^{Σ'}`, so `(b, F', G') ∈ L_R^{Σ'}`. By R2, `b ∈ dom(Σ'.L)` with `Σ'.L(b) = (F', G', R)` — the same value `G'` appears in both states. Since `coverage` is a pure function on endset values, `coverage(G')` is a single fixed set, and `a ∈ coverage(G')` is a state-independent proposition once `G'` has been fixed. Therefore `a ∈ nullified(Σ')`. ∎

**R6b — SingleDepthRetraction.** The retraction predicate is *single-depth*: `nullified(Σ)` checks only whether some tuple in `L_R` directly targets `a`, regardless of whether that retracting tuple is itself nullified.

*Justification.* Direct from the Definition of `nullified(Σ)`: the existential quantifier ranges over `L_R^Σ`, not `A_R^Σ`. We do not iterate; once retracted, always retracted. ∎

**R6c — RestorationByReemission.** Once retracted, a tuple stays out of every future active subset:

`(A Σ, K, (a, F, G) ∈ L_K^Σ : a ∈ nullified(Σ) : (A Σ → Σ' :: (a, F, G) ∉ A_K^{Σ'}))`

To "restore" content, emit a fresh tuple with the desired value (R0). The new tuple receives a fresh address; the retracted tuple keeps its address (R2) and stays out of `A_K` (R6a).

*Proof.* By R6a, `a ∈ nullified(Σ')`. By Definition of `A_K`, `(a, F, G) ∉ A_K^{Σ'}`. ∎

*Consequences (S6).*

(a) *Operational vs. historical views.* `A_K` is the operational view ("what is currently in effect"); `L_K` is the audit view ("what has ever existed"). Both are computed from `Σ.L` by the same observation machinery, differing only in whether `nullified(Σ)` is excluded. Operational and historical queries use the same observation primitive but specify different views.

(b) *Mutation as set-difference.* `A_K^Σ = L_K^Σ \ {(a, F, G) : a ∈ nullified(Σ)}`. Computed live; no flag, no cache, no version field anywhere in the architecture.

(c) *Quiescence is operational, not historical.* "Every public predicate over `A_K` holds" is the convergence condition. It does not require historical agreement; it requires the current substrate to satisfy every public check.

(d) *All visible operations reduce to Emit.* File a comment, close it, retract a citation, retire a document, revive it — each is one or two emissions. The substrate's response (`A_K` shifts, predicates flip) is uniform across the lot.


## Three Operations

The six properties yield three operations that suffice to span all visible substrate change.

**Definition — Emit_K.** Emit is a state-transforming operation with signature

`Emit_K : Σ × Endset × Endset → Σ' × A_rel^{Σ'}`

The defining precondition is `K ∈ T_admissible` and `dom(Σ.M) ≠ ∅`. Given input state Σ and finite endsets `F, G ∈ Endset`, `Emit_K(Σ, F, G)` returns `(Σ', a)` where, by R0, `a ∉ dom(Σ.L)`, `a ∈ dom(Σ'.L)`, and `Σ'.L(a) = (F, G, K)`. All other components of Σ are held in frame: `Σ'.C = Σ.C` and `Σ'.M = Σ.M`. By R2, the binding `Σ'.L(a) = (F, G, K)` is permanent across all subsequent transitions.

The address-returning convention in the rest of this note — `Emit_K(F, G) → A_rel` — is a metonym: the state is the ambient one, and `Σ'` is the post-emission state in which the returned address resides.

**Definition — Observe_K.** For `K ∈ T_admissible`, a pattern `(F̂, Ĝ) ∈ ℘_fin(A) × ℘_fin(A)`, and a view selector, Observe is a pure read with signature

`Observe_K : Σ × ℘_fin(A) × ℘_fin(A) × View → ℘_fin(L_K^Σ)`

where `View ∈ {hist, oper}` selects between `L_K^Σ` (audit) and `A_K^Σ` (operational). It returns

`{(a, F, G) ∈ view : F̂ ⊆ coverage(F) ∧ Ĝ ⊆ coverage(G)}`

with `view = L_K^Σ` if `View = hist` and `view = A_K^Σ` if `View = oper`. Observe leaves Σ unchanged.

**Definition — Nullify.** For input state Σ and `a ∈ A_rel^Σ`, Nullify is the composition

`Nullify(Σ, a) ≡ Emit_R(Σ, ∅, {(a, δ(1, #a))})`

That is, emit a tuple into the retraction relation with empty from-set and a unit-depth to-span targeting `a`. By PrefixSpanCoverage (ASN-0043), `coverage({(a, δ(1, #a))}) = {t : a ≼ t}`, which contains `a`. Let `(Σ', _) = Nullify(Σ, a)`. By Definition of `nullified`, `a ∈ nullified(Σ')`. By R6a, `a` remains nullified thereafter.

**R7 — NullifyIsEmit.** Nullify is not a separate primitive; it is `Emit_R` with a designated argument shape.

*Proof.* By Definition. The substrate has exactly two visible-operation primitives at the relational level: Emit (which writes) and Observe (which reads). Nullify is a Composition of Emit, not an additional primitive. There is no Update primitive at all; change is nullify-then-emit, both expressed via Emit. ∎


## Worked Sketch

We illustrate the structure of a retraction cycle in the relational vocabulary, building on the ASN-0043 worked example.

*Setup.* Let `K ∈ T_admissible` be any content-classifying type with `K ∈ T_cat^{Σ_0}`. Suppose at state `Σ_0` the substrate contains:

`L_K^{Σ_0} = {(a₁, F₁, G₁)}` &nbsp; — one classification tuple
`L_R^{Σ_0} = ∅` &nbsp; — no retractions yet

By Definition, `A_K^{Σ_0} = L_K^{Σ_0} = {(a₁, F₁, G₁)}` and `nullified(Σ_0) = ∅`. We further assume `a₁` is sited in some document subspace `s_L(d)` whose subsequent allocations need not nest under `a₁` — the typical configuration, since by L1c (LinkAllocatorConformance, ASN-0043) the allocator's outputs within `s_L(d)` are siblings or successors in the document's link subspace, not extensions of an existing link address.

*Step 1: Nullify a₁.* `Σ_0 → Σ_1` via `Nullify(Σ_0, a₁) = Emit_R(Σ_0, ∅, {(a₁, δ(1, #a₁))})`. By R0, this allocates a fresh `b₁ ∉ dom(Σ_0.L)`; we choose `b₁` from the unoccupied link-subspace positions of `s_L(d)`, and by T10a.5 (FreshnessGuarantee, ASN-0034) the allocator's discipline supplies such a position. The witness construction in R0 (Step 3) further confirms that `b₁` and `a₁` are not in a prefix relation: T10a.4 forbids reuse, T10a.5 supplies freshness within the subspace, and T10a.6 extends the allocator's choice deterministically to a sibling position — so `a₁ ⊀ b₁`, and the to-set `{(a₁, δ(1, #a₁))}` covers `a₁` and its tumbler-prefix extensions without unintentionally covering `b₁` itself. The post-state has `Σ_1.L(b₁) = (∅, {(a₁, δ(1, #a₁))}, R)`. Now:

- `L_K^{Σ_1} = {(a₁, F₁, G₁)}` &nbsp; — unchanged (R3 preserves `L_K`; the emission targets `L_R`)
- `L_R^{Σ_1} = {(b₁, ∅, {(a₁, δ(1, #a₁))})}`
- `nullified(Σ_1) = {a₁}` &nbsp; — `a₁` is in the to-set's coverage
- `A_K^{Σ_1} = ∅` &nbsp; — `a₁` is excluded from the active subset

The audit predicate `(a₁, F₁, G₁) ∈ L_K` remains true forever (R3); the operational predicate `(a₁, F₁, G₁) ∈ A_K` flips to false at `Σ_1`.

*Step 2: Restore by re-emission.* To restore the classification, we do *not* attempt to nullify the retraction (which by R6b would be ineffective — single-depth checking ignores it). Instead, `Σ_1 → Σ_2` via `Emit_K(F₁, G₁)`, allocating fresh `a₂ ∉ dom(Σ_1.L)` (R0) and setting `Σ_2.L(a₂) = (F₁, G₁, K)`. Now:

- `L_K^{Σ_2} = {(a₁, F₁, G₁), (a₂, F₁, G₁)}` &nbsp; — two tuples with identical content (L11b, R0)
- `nullified(Σ_2) = {a₁}` &nbsp; — unchanged (R6a; `a₂` is not targeted by any `L_R` tuple)
- `A_K^{Σ_2} = {(a₂, F₁, G₁)}` &nbsp; — the new tuple is active

The relational content `(F₁, G₁)` is again present in `A_K`, but at a different tuple address. Provenance and audit cleanly distinguish the two emissions: `a₁` is the historical record, `a₂` is the current assertion.


## Properties Introduced

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| Setup | HYP | Globally `s_C`-resident content: `(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)` | introduced |
| A^Σ | DEF | Address universe at state Σ: `dom(Σ.C) ∪ dom(Σ.L)` | introduced |
| A_doc^Σ, A_rel^Σ | DEF | Partition of `A^Σ` into content addresses (`dom(Σ.C)`) and tuple addresses (`dom(Σ.L)`) | introduced |
| T_admissible | DEF | Admissible types: `{K ∈ Endset : K ≠ ∅}` — the indexing domain for typed relations | introduced |
| T_cat^Σ | DEF | Type catalog at Σ — admissible types actually in use at Σ (descriptive, not constitutive) | introduced |
| L_K^Σ | DEF | Typed relation: `{(a, F, G) : a ∈ dom(Σ.L) ∧ |Σ.L(a)| = 3 ∧ Σ.L(a) = (F, G, K)}` | introduced |
| L^Σ | DEF | Standard-triple link store: `⨆_{K ∈ T_admissible} L_K^Σ` | introduced |
| addr | DEF | Map `(a, F, G) ↦ a : L^Σ → A_rel^Σ` | introduced |
| nullified(Σ) | DEF | Tuple addresses targeted by some `L_R^Σ` to-set | introduced |
| A_K^Σ | DEF | Active subset: `{(a, F, G) ∈ L_K^Σ : a ∉ nullified(Σ)}` | introduced |
| R0 | LEMMA | TupleAddressFreshness — under precondition `dom(Σ.M) ≠ ∅`, every emission allocates a fresh address (= L1a + L1b + L1c + T0(a) + T10a.4 + T10a.5 + T10a.6 + L-fin + L11b witness) | introduced |
| R1 | LEMMA | AddressInjectivity — `addr` is an injection (= function property of `Σ.L`) | introduced |
| R2 | LEMMA | TupleAddressPermanence — addresses persist with values intact (= L12) | introduced |
| R3 | LEMMA | TypedSliceMonotonicity — each `L_K^Σ` is monotone (= L12a + R2) | introduced |
| R4 | LEMMA | TupleAddressDisjointness — `A_doc^Σ ∩ A_rel^Σ = ∅` (= Setup + L0 + T7) | introduced |
| R5 | META | TupleSelfTargeting — for any `a ∈ A_rel^Σ`, the span `(a, δ(1, #a))` is admissible as an endset member (= L4(c) + L13, no opposing invariant) | introduced |
| R6 | LEMMA | ActiveSubsetWellDefinedness — `A_K^Σ` is determined by `Σ.L` | introduced |
| R6a | LEMMA | RetractionStability — once nullified, always nullified (= R3 + R2 + purity of coverage) | introduced |
| R6b | LEMMA | SingleDepthRetraction — `nullified` checks only direct targeting | introduced |
| R6c | LEMMA | RestorationByReemission — restoration is fresh emission, never retraction-of-retraction | introduced |
| R7 | LEMMA | NullifyIsEmit — Nullify is `Emit_R` with designated argument shape, not a separate primitive | introduced |
| Emit_K | OP | State-transforming: `Σ × Endset × Endset → Σ' × A_rel^{Σ'}`, with `K ∈ T_admissible` and `dom(Σ.M) ≠ ∅` | introduced |
| Observe_K | OP | Pure read: `Σ × ℘_fin(A) × ℘_fin(A) × View → ℘_fin(L_K^Σ)`, selecting `L_K^Σ` or `A_K^Σ` | introduced |
| Nullify | OP | `Nullify(Σ, a) ≡ Emit_R(Σ, ∅, {(a, δ(1, #a))})` | introduced |


## Open Questions

- What invariants must hold between `L_K` and the arrangements `Σ.M` when relational predicates depend on whether the from-set or to-set content is currently visible in some document?
- Should multi-arity links (`|Σ.L(a)| > 3`) define multiple binary projections, or be regarded directly as elements of higher-arity typed relations `L_K^{(n)} ⊆ A_rel × ℘(A)^n`?
- Under what conditions is `Nullify(b)` for `b ∈ L_R` operationally meaningful, given that R6b makes single-depth checking ignore the second-order retraction?
- What ordering, if any, must the substrate guarantee on Observe results — by emission cycle, by tuple address, or unordered as set semantics suggest?
- Must Emit be atomic with respect to concurrent Observe, and if so, what is the consistency model under which `A_K` transitions are observed?
- What guarantees does the substrate provide about the cardinality bound of `nullified(Σ)` relative to `dom(Σ.L)` — is unbounded retraction permitted, or must some structural ratio hold?
- Can higher layers extend the type catalog `T_cat` dynamically without coordination, given L9 (TypeGhostPermission), and what happens when two layers independently choose colliding type addresses?