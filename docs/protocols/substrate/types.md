# Typed Relations on Address Sets

*Drawing the link model forward into a relational vocabulary*

ASN-0043 establishes the link as a primitive: an addressed, owned, typed connection between spans of content. We now adopt a different vocabulary for the same structure. Where ASN-0043 speaks of *links* and *endsets*, we speak of *tuples* and *typed relations*. The two vocabularies describe one object — a standard-triple link `(F, G, Θ)` at address `a ∈ dom(Σ.L)` is a tuple in a typed relation indexed by `Θ` — but predicates compose more cleanly over relations than over endsets, and several substrate-level guarantees become easier to state in this form.

We are looking for what a relation algebra over the link store affords. The answer is six structural properties, of which five (R0–R5) are derivable from ASN-0043 and one (R6, the active subset) is the substrate's own contribution — made possible by R5 (the existence of a self-referential retraction relation) and R3 (the audit trail it is computed against). The six properties suffice to define three operations under which all visible substrate change reduces to a single primitive: Emit.


## The Two Foundational Sets

**Definition — AddressUniverse.** The substrate's address universe is

`A = dom(Σ.C) ∪ dom(Σ.L)`

By L14 (DualPrimitive, ASN-0043), `A` is the entirety of stored-entity addresses; no third category exists.

**Definition — Partition.** Define:

`A_doc = dom(Σ.C)` &nbsp; — content addresses
`A_rel = dom(Σ.L)` &nbsp; — relation-tuple addresses

We claim `A = A_doc ⊔ A_rel` (disjoint union). The disjointness is R4 below.

**Definition — TypeCatalog.** The *type catalog* is the set of type-endsets actually in use:

`T_cat = {Θ ∈ Endset : (E a ∈ dom(Σ.L) :: |Σ.L(a)| ≥ 3 ∧ Σ.L(a).type = Θ)}`

By L4 (EndsetGenerality, ASN-0043) and L9 (TypeGhostPermission, ASN-0043), `T_cat` is unconstrained by content existence: type endsets may reference any tumbler addresses, including ghosts. We require only that type-equality is decidable by endset comparison — which it is, by L8 (TypeByAddress).

For the rest of this development we restrict attention to standard-triple links — those with `|Σ.L(a)| ≥ 3`. Higher-arity links (L3, NEndsetStructure) admit the same construction with additional slot positions; nothing in what follows depends on arity = 3 except the projection to a single (from, to) pair.


## The Typed Relation

**Definition — TypedRelation.** For each `K ∈ T_cat`, the *typed relation of type K* is

`L_K = {(a, F, G) : a ∈ dom(Σ.L) ∧ Σ.L(a) = (F, G, K) ∧ |Σ.L(a)| ≥ 3}`

Each member is a triple of (tuple-address, from-endset, to-endset). The pair `(F, G)` is the *relational content* of the tuple; `a` is the *tuple address*. The substrate as a whole is the disjoint union over types:

`L = ⨆_{K ∈ T_cat} L_K`

We will show (R1) that this disjoint union is well-defined: each tuple address belongs to exactly one type-slice.

**Definition — TupleAddress.** Define `addr : L → A_rel` by `addr(a, F, G) = a`.

*Remark — relation to ℘(A) × ℘(A).* A generic mathematical typed relation is a subset of `℘(A) × ℘(A)` — a set of address-pair-pairs distinguished only by content. Our typed relation is richer: each tuple carries an address that participates in the relation's identity. The projection `(a, F, G) ↦ (coverage(F), coverage(G))` recovers the address-pair view, but it loses information that the substrate retains (R0, R1).


## Tuple Identity (R0, R1, R2)

A generic mathematical relation distinguishes its members only by content: two tuples with identical (F, G) are the same tuple. The substrate's relations do not work that way. Each tuple emission allocates a fresh address (R0), the address-to-pair binding is a function (R1), and the binding is permanent (R2).

**R0 — TupleAddressFreshness.** For any state Σ and any (F, G, K), there exists a state Σ' with Σ → Σ' that emits a tuple with content (F, G) of type K at a fresh address:

`(A Σ, F, G ∈ Endset, K ∈ T_cat :: (E Σ' extending Σ, a : a ∉ dom(Σ.L) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = (F, G, K)))`

*Proof.* By L1c (LinkAllocatorConformance, ASN-0043), link allocation conforms to T10a (AllocatorDiscipline, ASN-0034). By GlobalUniqueness (UniqueAddressAllocation, ASN-0034), addresses produced by T10a-conforming allocators are globally unique — no allocation event in the system produces an address that has been allocated before. By L-fin (LinkStoreFiniteness, ASN-0043), `|dom(Σ.L)| < ∞`, so only finitely many addresses are occupied at any state. By L1b (LinkElementFieldDepth) and T0(a) (UnboundedComponentValues, ASN-0034), the set of valid link addresses within any document's link subspace is countably infinite. Therefore an unoccupied valid link address `a` exists; the witness construction in L11b (NonInjectivity, ASN-0043) shows that `Σ'` extending `Σ` with `Σ'.L(a) = (F, G, K)` preserves all invariants of ASN-0043 and ASN-0036. ∎

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

**R4 — TupleAddressDisjointness.** Tuple addresses and document addresses are disjoint:

`A_doc ∩ A_rel = ∅`

*Proof.* By Definition, `A_doc = dom(Σ.C)` and `A_rel = dom(Σ.L)`. By L14 (DualPrimitive, ASN-0043), `dom(Σ.C) ∩ dom(Σ.L) = ∅`. ∎

A stronger structural form follows from L0 (SubspacePartition, ASN-0043): not merely empty intersection, but residence in disjoint subspaces (`s_C` and `s_L`). By T7 (SubspaceDisjointness, ASN-0034), addresses in different subspaces are permanently distinct as tumblers — the disjointness is a structural property of address composition, not a coincidence of which addresses happen to be currently occupied.

*Consequences (S4).*

(a) *Predicates are typeable.* A predicate like `is_classified(d, K)` has signature `A_doc × T_cat → Bool`; a predicate like `is_active(τ)` (R6) has signature `A_rel → Bool`. No predicate has an ambiguous signature; categorical confusion at the address level is impossible.

(b) *Retraction is well-typed.* Only `A_rel` addresses are valid arguments to Nullify (R6). "Retracting a document" is not directly expressible — the to-set of an `L_R` tuple must contain a tuple address, not a document address. Document removal from active consideration is done via classifier tuples (e.g., `L_retired`) targeting the document; the document's `A_doc` address is never disturbed.

(c) *Lifecycle separation.* Documents have mutable bodies (arrangements `Σ.M` change per ASN-0036); tuples never mutate (R2). The address-level structure permits these to diverge without interference.


## Self-Reference (R5)

**R5 — TupleSelfTargeting.** A tuple's from-set or to-set may reference tuple addresses:

`(A Σ, a ∈ dom(Σ.L), (F, G, K) = Σ.L(a) :: nothing in L0–L14, L-fin, S0–S3 forbids coverage(F) ∩ A_rel ≠ ∅ or coverage(G) ∩ A_rel ≠ ∅)`

That is: the substrate model imposes no constraint forbidding endsets from referencing other tuple addresses.

*Justification.* L4 (EndsetGenerality, ASN-0043) imposes no constraint on endset span targets beyond well-formedness (T12). L4(c) explicitly notes that endset spans may reference addresses in the link subspace — that is, addresses of other links. L13 (ReflexiveAddressing, ASN-0043) establishes that link addresses are valid span targets and exhibits the canonical unit-depth span `(b, δ(1, #b))` whose coverage equals `{t : b ≼ t}` — exactly the entity at `b` and its extensions. Therefore tuples can target tuples by ordinary endset construction; no special machinery is required. The worked example in ASN-0043 explicitly constructs such a meta-link in its Step 2 verification. ∎

*Consequences (S5).* Several constructs that would otherwise require out-of-band machinery collapse into the relational primitive:

(a) *Retraction.* A tuple in a designated relation `L_R` whose to-set contains the address of the tuple being nullified. Mutation becomes Emit; `L_K` is never modified (R3).

(b) *Resolution.* A tuple in `L_resolution` whose to-set contains a comment-tuple's address. Comment lifecycle is uniformly substrate-tracked; "this comment is closed" is an ordinary observation, not a flag stored elsewhere.

(c) *Agent provenance.* A tuple whose from-set contains an agent's address and whose to-set contains the emitted tuple. Every emission has an attributable emitter as a substrate fact, with no separate metadata channel.

(d) *Higher-order predicates.* "Has τ been retracted?", "who emitted τ?", "what tuples target τ?" — all are ordinary observations over `L_K`, evaluated by the same machinery as predicates over documents.

Without R5, each construct would require its own layer that predicates could not see and that the audit trail (R3) would not preserve. R5 collapses such layers into the relational structure.


## The Active Subset (R6)

R0–R5 are derivable from ASN-0043. The active subset is the substrate's own contribution — added here, not present in Nelson's link model. It is made possible by R5 (a self-referential retraction relation can exist) and R3 (the retraction relation accumulates monotonically, providing the audit trail against which the active subset is computed).

**Definition — RetractionType.** Fix a designated type `R ∈ T_cat` reserved for retraction. The corresponding typed relation `L_R` is the *retraction relation*. By L9 (TypeGhostPermission), `R` need not refer to anything stored — it is a name chosen by convention.

**Definition — Nullified.** The set of *nullified* tuple addresses at state `Σ` is

`nullified(Σ) = {a ∈ A_rel : (E (b, F', G') ∈ L_R^Σ :: a ∈ coverage(G'))}`

By R5, `coverage(G')` may include `A_rel` addresses, so `nullified(Σ)` is well-defined as a subset of `A_rel`.

**Definition — ActiveSubset.** For each `K ∈ T_cat`, the *active subset of type K* at state Σ is

`A_K^Σ = {(a, F, G) ∈ L_K^Σ : a ∉ nullified(Σ)}`

**R6 — ActiveSubsetWellDefinedness.** For every state `Σ` and every type `K ∈ T_cat`, `A_K^Σ` is well-defined and computable from `Σ.L` alone, with no auxiliary state.

*Proof.* `nullified(Σ)` is determined entirely by `L_R^Σ`, which by Definition of TypedRelation is determined by `Σ.L`. `A_K^Σ` is a set-difference between `L_K^Σ` and tuples whose addresses lie in `nullified(Σ)`; both inputs are determined by `Σ.L`. No flag, no version field, no separate snapshot is consulted. ∎

**R6a — RetractionStability.** Once a tuple's address is nullified, it stays nullified across all future state transitions:

`(A Σ → Σ', a ∈ A_rel : a ∈ nullified(Σ) :: a ∈ nullified(Σ'))`

*Proof.* Suppose `a ∈ nullified(Σ)`. By Definition, there exists `(b, F', G') ∈ L_R^Σ` with `a ∈ coverage(G')`. By R3, `(b, F', G') ∈ L_R^{Σ'}`. By R2, `coverage(G')` evaluated at `Σ'` equals `coverage(G')` evaluated at `Σ` (the endset value is preserved). So `a ∈ coverage(G')` at `Σ'` as well, and `a ∈ nullified(Σ')`. ∎

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

**Definition — Emit_K.** For `K ∈ T_cat` and finite endsets `F, G`:

`Emit_K(F, G) → A_rel`

allocates a fresh address `a ∉ dom(Σ.L)` (R0), extends `Σ.L` to `Σ'.L` with `Σ'.L(a) = (F, G, K)` while holding all other state in frame, and returns `a`. By R2, the binding is permanent.

**Definition — Observe_K.** For `K ∈ T_cat`, a pattern `(F̂, Ĝ) ∈ ℘_fin(A) × ℘_fin(A)`, and a view selector:

`Observe_K(F̂, Ĝ, view) → ℘_fin(L_K)`

returns

`{(a, F, G) ∈ view : F̂ ⊆ coverage(F) ∧ Ĝ ⊆ coverage(G)}`

with `view ∈ {L_K^Σ, A_K^Σ}`. The audit query uses `L_K`; the operational query uses `A_K`. Matching is set-inclusion of pattern within coverage.

**Definition — Nullify.** For `a ∈ A_rel`:

`Nullify(a) ≡ Emit_R(∅, {(a, δ(1, #a))})`

That is, emit a tuple into the retraction relation with empty from-set and a unit-depth to-span targeting `a`. By PrefixSpanCoverage (ASN-0043), `coverage({(a, δ(1, #a))}) = {t : a ≼ t}`, which contains `a`. By Definition of `nullified`, `a ∈ nullified(Σ')` after the emission. By R6a, `a` remains nullified thereafter.

**R7 — NullifyIsEmit.** Nullify is not a separate primitive; it is `Emit_R` with a designated argument shape.

*Proof.* By Definition. The substrate has exactly two visible-operation primitives at the relational level: Emit (which writes) and Observe (which reads). Nullify is a Composition of Emit, not an additional primitive. There is no Update primitive at all; change is nullify-then-emit, both expressed via Emit. ∎


## Worked Sketch

We illustrate the structure of a retraction cycle in the relational vocabulary, building on the ASN-0043 worked example.

*Setup.* Let `K ∈ T_cat` be any content-classifying type. Suppose at state `Σ_0` the substrate contains:

`L_K^{Σ_0} = {(a₁, F₁, G₁)}` &nbsp; — one classification tuple
`L_R^{Σ_0} = ∅` &nbsp; — no retractions yet

By Definition, `A_K^{Σ_0} = L_K^{Σ_0} = {(a₁, F₁, G₁)}` and `nullified(Σ_0) = ∅`.

*Step 1: Nullify a₁.* `Σ_0 → Σ_1` via `Nullify(a₁) = Emit_R(∅, {(a₁, δ(1, #a₁))})`. This allocates a fresh `b₁ ∉ dom(Σ_0.L)` (R0) and sets `Σ_1.L(b₁) = (∅, {(a₁, δ(1, #a₁))}, R)`. Now:

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
| A | DEF | Address universe `dom(Σ.C) ∪ dom(Σ.L)` | introduced |
| A_doc, A_rel | DEF | Partition of `A` into content addresses (`dom(Σ.C)`) and tuple addresses (`dom(Σ.L)`) | introduced |
| T_cat | DEF | Type catalog — type-endsets actually in use | introduced |
| L_K | DEF | Typed relation: `{(a, F, G) : Σ.L(a) = (F, G, K)}` | introduced |
| L | DEF | Substrate relation: `⨆_{K ∈ T_cat} L_K` | introduced |
| addr | DEF | Map `(a, F, G) ↦ a : L → A_rel` | introduced |
| nullified(Σ) | DEF | Tuple addresses targeted by some `L_R` to-set at Σ | introduced |
| A_K^Σ | DEF | Active subset: `{(a, F, G) ∈ L_K^Σ : a ∉ nullified(Σ)}` | introduced |
| R0 | LEMMA | TupleAddressFreshness — every emission allocates a fresh address (= L1c + GlobalUniqueness + L-fin + L11b witness) | introduced |
| R1 | LEMMA | AddressInjectivity — `addr` is an injection (= function property of `Σ.L`) | introduced |
| R2 | LEMMA | TupleAddressPermanence — addresses persist with values intact (= L12) | introduced |
| R3 | LEMMA | TypedSliceMonotonicity — each `L_K` is monotone (= L12a + R2) | introduced |
| R4 | LEMMA | TupleAddressDisjointness — `A_doc ∩ A_rel = ∅` (= L14) | introduced |
| R5 | META | TupleSelfTargeting — endsets may reference `A_rel` addresses (= L4(c) + L13) | introduced |
| R6 | LEMMA | ActiveSubsetWellDefinedness — `A_K^Σ` is determined by `Σ.L` | introduced |
| R6a | LEMMA | RetractionStability — once nullified, always nullified | introduced |
| R6b | LEMMA | SingleDepthRetraction — `nullified` checks only direct targeting | introduced |
| R6c | LEMMA | RestorationByReemission — restoration is fresh emission, never retraction-of-retraction | introduced |
| R7 | LEMMA | NullifyIsEmit — Nullify is `Emit_R` with designated argument shape, not a separate primitive | introduced |
| Emit_K | OP | Allocate fresh address; extend `Σ.L` with `(F, G, K)` | introduced |
| Observe_K | OP | Return matching `(a, F, G)` triples in selected view | introduced |
| Nullify | OP | `Nullify(a) ≡ Emit_R(∅, {(a, δ(1, #a))})` | introduced |


## Open Questions

- What invariants must hold between `L_K` and the arrangements `Σ.M` when relational predicates depend on whether the from-set or to-set content is currently visible in some document?
- Should multi-arity links (`|Σ.L(a)| > 3`) define multiple binary projections, or be regarded directly as elements of higher-arity typed relations `L_K^{(n)} ⊆ A_rel × ℘(A)^n`?
- Under what conditions is `Nullify(b)` for `b ∈ L_R` operationally meaningful, given that R6b makes single-depth checking ignore the second-order retraction?
- What ordering, if any, must the substrate guarantee on Observe results — by emission cycle, by tuple address, or unordered as set semantics suggest?
- Must Emit be atomic with respect to concurrent Observe, and if so, what is the consistency model under which `A_K` transitions are observed?
- What guarantees does the substrate provide about the cardinality bound of `nullified(Σ)` relative to `dom(Σ.L)` — is unbounded retraction permitted, or must some structural ratio hold?
- Can higher layers extend the type catalog `T_cat` dynamically without coordination, given L9 (TypeGhostPermission), and what happens when two layers independently choose colliding type addresses?