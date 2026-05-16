# ASN-0086: Typed Relations on Address Sets

*Drawing the link model forward into a relational vocabulary*

ASN-0043 establishes the link as a primitive: an addressed, owned, typed connection between spans of content. We now adopt a different vocabulary for the same structure. Where ASN-0043 speaks of *links* and *endsets*, we speak of *tuples* and *typed relations*. The two vocabularies describe one object — a standard-triple link `(F, G, Θ)` at address `a ∈ dom(Σ.L)` is a tuple in a typed relation indexed by `Θ` — but predicates compose more cleanly over relations than over endsets, and several substrate-level guarantees become easier to state in this form.

We are looking for what a relation algebra over the link store affords. The answer is six structural properties, of which five (R0–R5) are derivable from ASN-0043 and one (R6, the active subset) is the substrate's own contribution — made possible by R5 (the existence of a self-referential retraction relation) and R3 (the audit trail it is computed against). The six properties suffice to define three operations under which all *relational-layer* state change reduces to a single primitive: `Emit_K`. (Document allocation and content emission, the other two primitive transitions in `→`, are inherited from ASN-0036 and are not reductions of `Emit_K`; the scope of the reduction is the link store `Σ.L` and the typed relations indexed over it.)


## The Two Foundational Sets

**Setup hypothesis.** We work in systems satisfying ASN-0043 (and therefore ASN-0036 and ASN-0034). We additionally assume globally `s_C`-resident content:

`(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)`

Under this hypothesis the disjointness between content and tuple addresses (R4 below) holds substrate-wide as a structural property, not merely within the slice scoped to `s_C` that L14 (DualPrimitive, ASN-0043) supplies in its stated form.

**State transition relation.** We write `Σ → Σ'` for the substrate's one-step transition relation. The primitive transitions are exactly the substrate-level emissions inherited from the underlying ASNs and lifted here: (i) document allocation (ASN-0036, S7a, S7d) extends `dom(Σ.M)` with a new document address; (ii) content emission (ASN-0036, S0–S3) extends `dom(Σ.C)`; (iii) `Emit_K` as defined later in this note (which composes the underlying ASN-0043 link-store extension) extends `dom(Σ.L)` by one address. Every transition in `→` is one of (i)–(iii); the substrate exposes no removal, replacement, or in-place mutation transition (consistent with S0, L12, and T8 across the underlying ASNs). The operations defined later in this note (Observe, Nullify) either compose `Emit_K` (Nullify is `Emit_R` with a designated argument shape, per R7) or leave Σ unchanged (Observe). R0 through R7 are claims about `→` so defined; in particular, R0's existential `(E Σ' extending Σ, …)` is discharged by exhibiting an `Emit_K` transition.

**Definition — Extension.** `Σ' extends Σ`, written `Σ ⊑ Σ'`, is the reflexive-transitive closure of `→`:

`Σ ⊑ Σ' ≡ Σ →* Σ'`

By the frame conditions of (i)–(iii) — each primitive transition extends exactly one of `Σ.C`, `Σ.M`, `Σ.L` at a fresh key and leaves the other two components unchanged — `Σ ⊑ Σ'` entails `dom(Σ.C) ⊆ dom(Σ'.C)`, `dom(Σ.M) ⊆ dom(Σ'.M)`, `dom(Σ.L) ⊆ dom(Σ'.L)`, with `Σ'.C|_{dom(Σ.C)} = Σ.C`, `Σ'.M|_{dom(Σ.M)} = Σ.M`, `Σ'.L|_{dom(Σ.L)} = Σ.L`. The phrase "Σ' extending Σ" used throughout this note (and lifted from ASN-0043 invariant restatements such as L9, L11b) is this relation.

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

**Definition — TypeEquivalence.** Two admissible types are *type-equivalent* iff they cover the same address set:

`K ~ K' ≡ coverage(K) = coverage(K')`

This is L8's (TypeByAddress, ASN-0043) notion of `same_type`, lifted from links to type endsets themselves. The quotient `T_admissible / ~` is the set of *coverage classes*; the equivalence class of `K` is written `[K]`.

**Definition — TypedRelation.** For each `K ∈ T_admissible` and state Σ, the *typed relation of type K at Σ* is

`L_K^Σ = {(a, F, G) : a ∈ dom(Σ.L) ∧ |Σ.L(a)| = 3 ∧ Σ.L(a).e₁ = F ∧ Σ.L(a).e₂ = G ∧ coverage(Σ.L(a).e₃) = coverage(K)}`

Each member is a triple of (tuple-address, from-endset, to-endset). The pair `(F, G)` is the *relational content* of the tuple; `a` is the *tuple address*. Membership at the type slot is by coverage-equivalence, not by literal endset value: a tuple stored with third endset `K'` belongs to `L_K^Σ` whenever `K' ~ K`, so `L_K^Σ = L_{K'}^Σ` whenever `K ~ K'`. The substrate's standard-triple link store at state Σ is therefore the disjoint union over coverage classes:

`L^Σ = ⨆_{[K] ∈ T_admissible / ~} L_K^Σ`

We will show (R1) that this disjoint union is well-defined: each tuple address belongs to exactly one coverage-class slice. Note that `L^Σ` collects only the arity-3 links; higher-arity links in `dom(Σ.L)` are outside its scope, as noted above. Where ambient state is clear we drop the superscript and write `L_K`, `L`.

*Rationale for coverage-equivalence.* L8 (TypeByAddress, ASN-0043) defines link type-equality through coverage of the third endset, not through endset-value identity. Taking `L_K^Σ` to use literal endset equality at the type slot would make `L_K` a strict refinement of L8's equivalence: two tuples whose type endsets cover the same address set via differently structured spans would lie in distinct `L_K`'s here yet be "same type" under L8 — and the active-subset machinery would silently miss retractions whose type endset was coverage-equivalent to `R` but not literally equal. The coverage-equivalence definition aligns `L_K` with L8 and renders all coverage-equivalent type endsets interchangeable for retraction-relation membership and active-subset computation. (This matches the convention of every endset-comparison primitive in the substrate stack, which projects through `coverage(·)` rather than comparing raw endset values.)

**Definition — TupleAddress.** Define `addr : L^Σ → A_rel^Σ` by `addr(a, F, G) = a`.

*Remark — relation to ℘(A) × ℘(A).* A generic mathematical typed relation is a subset of `℘(A) × ℘(A)` — a set of address-pair-pairs distinguished only by content. Our typed relation is richer: each tuple carries an address that participates in the relation's identity. The projection `(a, F, G) ↦ (coverage(F), coverage(G))` recovers the address-pair view, but it loses information that the substrate retains (R0, R1).


## Tuple Identity (R0, R1, R2)

A generic mathematical relation distinguishes its members only by content: two tuples with identical (F, G) are the same tuple. The substrate's relations do not work that way. Each tuple emission allocates a fresh address (R0), the address-to-pair binding is a function (R1), and the binding is permanent (R2).

**R0 — TupleAddressFreshness.** For any state Σ with `dom(Σ.M) ≠ ∅` and any `(F, G, K) ∈ Endset × Endset × T_admissible`, there exists a state Σ' with Σ → Σ' that emits a tuple with content (F, G) of type K at a fresh address:

`(A Σ : dom(Σ.M) ≠ ∅ :: (A F, G ∈ Endset, K ∈ T_admissible :: (E Σ' extending Σ, a : a ∉ dom(Σ.L) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = (F, G, K))))`

*Proof.* We construct the witness in four steps. Let `LS(d) = {a ∈ T : d ≼ a ∧ T4-valid(a) ∧ zeros(a) = 3 ∧ a.E₁ = s_L ∧ #E(a) ≥ 2}` denote the well-formed link-subspace addresses sited under document `d` (combining the T4 element-level constraint, the L0 first-element-field marker `s_L`, and the L1b depth requirement).

(Step 1 — locate a home document.) By precondition, `dom(Σ.M) ≠ ∅`; pick any `d ∈ dom(Σ.M)`. By L1a (LinkScopedAllocation, ASN-0043), every link address `a'' ∈ dom(Σ.L)` satisfies `home(a'') = N(a'').0.U(a'').0.D(a'') ∈ dom(Σ.M)` — its document-level prefix is an allocated document. We will exhibit a fresh link address with `home = d`.

(Step 2 — constructively exhibit a reachable fresh address sited under `d`, with its T10a-conforming chain.) We case-split on whether `d` already has any link allocations under `Σ`. Both cases produce a concrete `a ∈ LS(d) \ dom(Σ.L)` together with its T10a-conforming chain from `d` (seed `s = d` is T4-valid by S7d, ASN-0036, which fixes `zeros(d) = 2` for every document tumbler). The construction mirrors the L1c-conformance argument used by L9 (TypeGhostPermission, ASN-0043) in its own emission proof, narrowed here to the link store and ground sequentially in the allocator's actual history at `Σ`.

*Case A — `d` has no prior link allocations under `Σ`* (`{a' ∈ dom(Σ.L) : home(a') = d} = ∅`). Set `a = d.0.s_L.1`. The L1c chain from `d` to `a` describes a walk through the depth-1 element-field allocator `A_d` (which is a single shared allocator across all subspaces under `d`, not one allocator per subspace): (i) `t₁ = inc(d, 2)` → `d.0.1` — at element-field depth 1, subspace 1; the underlying spawn pair is `(d, 2)`, admissible because `zeros(d) = 2 ≤ 2`. If `A_d` has not yet emitted any address under `Σ` (e.g., `d` has no content allocations either), this is the spawn event that creates `A_d`; if `A_d` already exists under `Σ` from prior content emissions, the chain navigates to its already-emitted base. L1c asserts the existence of a conforming chain to `a`, not the re-issuance of every spawn that chain traverses. (ii) Sibling sweep `inc(·, 0)` from subspace 1 across to subspace `s_L` at element-field depth 1, applied `s_L − 1` times — each step is a `k = 0` sibling advance within `A_d`, unconditionally T4-preserving (TA5a, ASN-0034) and consistent with T10a's at-most-once discipline because sibling enumeration is the allocator's own monotone advance, not a fresh spawn. (iii) `inc(d.0.s_L, 1)` → `d.0.s_L.1 = a` — child-spawn `(d.0.s_L, 1)` to element-field depth 2 (`k' = 1`, with TA5a unconditional for `k' = 1`, giving `zeros(a) = 3`). The at-most-once constraint binds the step-(iii) spawn pair `(d.0.s_L, 1)`; Case A's hypothesis — no prior link allocations under `d` — precludes any prior spawn at `(d.0.s_L, 1)`, since any such spawn would have produced an address in `LS(d) ∩ dom(Σ.L)`. Freshness: every step from `t₁` onward operates at length `> #d`, so by chain-prefix-preservation (TA5(b) for `k' ≥ 1` and TA5(c) for `k = 0`) every intermediate tumbler agrees with `d` on positions `1..#d`; therefore `home(a) = d`, and Case A's hypothesis directly yields `a ∉ dom(Σ.L)`. The membership conditions for `a ∈ LS(d)` are immediate by construction: `d ≼ a`, `T4-valid(a)` by T10a.4 (T4PreservationUnderDiscipline, ASN-0034), `zeros(a) = 3`, `a.E₁ = s_L`, `#E(a) = 2 ≥ 2`.

*Case B — `d` has prior link allocations under `Σ`* (`{a' ∈ dom(Σ.L) : home(a') = d} ≠ ∅`). Pick any existing link `b ∈ dom(Σ.L)` with `home(b) = d`. By L1c (LinkAllocatorConformance, ASN-0043) on `Σ`, `b` has a T10a-conforming chain `c_b` from `d`. Consider the sibling stream `b, inc(b, 0), inc²(b, 0), …`, which by T10a.7 (EnumerationInjectivity, ASN-0034) is injective and hence infinite. By L-fin (LinkStoreFiniteness, ASN-0043), `dom(Σ.L)` is finite, so the least `i ≥ 1` with `incⁱ(b, 0) ∉ dom(Σ.L)` exists; set `a = incⁱ(b, 0)`. Freshness is immediate from the least-`i` choice. The T10a-conforming chain from `d` to `a` is `c_b` extended by `i` sibling advances `inc(·, 0)`, each unconditionally T4-preserving (TA5a is unconditional for `k = 0`); each new `(parent, k)` pair along the extension is `(incʲ(b, 0), 0)` for `0 ≤ j < i`, which the original allocator producing `b` has not yet committed (precisely because `incⁱ(b, 0) ∉ dom(Σ.L)` and the prior occupied prefix `b, inc(b, 0), …, incⁱ⁻¹(b, 0) ∈ dom(Σ.L)` together fix the next available enumeration index as `i`), so T10a's at-most-once discipline is satisfied. By T10a.8 (UniformSiblingZeroCount, ASN-0034), `zeros(a) = zeros(b) = 3`; by chain-prefix-preservation (TA5(c) for `k = 0` preserves all positions but the rightmost, applied `i` times), `home(a) = home(b) = d`, `a.E₁ = b.E₁ = s_L`, and `#E(a) = #E(b) ≥ 2` (by L1b on `Σ` for `b`). The membership conditions for `a ∈ LS(d)` are immediate: `d ≼ a` (since `d ≼ b ≼ a` by transitivity of `≼`), `T4-valid(a)` by T10a.4, and the element-field constraints just discharged.

(Step 3 — collect the chain.) Step 2 has, in each case, exhibited a concrete `a ∈ LS(d) \ dom(Σ.L)` together with its T10a-conforming chain from `d` (seed `s = d`, length `≥ 1`, monotone in length by TA5; final step satisfying its `k' ⟹ zeros` precondition). This discharges L1c for `a`: the producer chain is `c_b` extended by sibling steps (Case B) or the fresh three-stage chain (i)–(iii) above (Case A).

(Step 4 — confirm freshness, exhibit Σ', verify invariants.) The T10a axiom's at-most-once child-spawning constraint, combined with T10a.7 (EnumerationInjectivity, ASN-0034), ensures each allocator's enumeration produces each address at most once. T10a.6 (DomainDisjointness, ASN-0034) ensures distinct allocators have disjoint domains. The chain of Step 3 is therefore the unique chain (up to allocator identity) producing `a`, and `a ∉ dom(Σ.L)` by Step 2 — so the emission of `a` is fresh. Define `Σ'` by extending `Σ.L` with `Σ'.L(a) = (F, G, K)`, leaving `Σ.C` and `Σ.M` unchanged. Each invariant is verified directly:

- `Σ'.L` remains a partial function: extension at a fresh key.
- L3 (NEndsetStructure, ASN-0043): `(F, G, K)` has `|·| = 3 ≥ 3`, with `F, G ∈ Endset` and `K ∈ T_admissible` non-empty, so the slot-3 type-endset constraint holds.
- L0 (SubspacePartition, ASN-0043): `a.E₁ = s_L` by Step 2's choice, so `subspace_I(a) = s_L`.
- L1 (LinkElementLevel, ASN-0043): `zeros(a) = 3` by Step 2's choice.
- L1a (LinkScopedAllocation, ASN-0043): `home(a) = d ∈ dom(Σ.M)` by Step 2 and Step 1.
- L1b (LinkElementFieldDepth, ASN-0043): `#E(a) ≥ 2` by Step 2's choice.
- L1c (LinkAllocatorConformance, ASN-0043): the chain of Step 3.
- L12 (LinkImmutability, ASN-0043): no existing entry was modified.
- L12a (LinkStoreMonotonicity, ASN-0043): `dom(Σ.L) ⊆ dom(Σ'.L)` by construction.
- L-fin (LinkStoreFiniteness, ASN-0043): finite plus one is finite.
- L11a (LinkUniqueness, ASN-0043): L11a's antecedent (distinct allocation events) is discharged by Step 4's freshness argument; L11a's conclusion then gives that `a` is distinct from every prior link address.
- L11b (NonInjectivity, ASN-0043): permits, does not require, value-level coincidence — the new entry is consistent whether or not `(F, G, K)` already appears at another address.
- Remaining L-invariants (L2, L4–L10, L13, L14, L14a): all are properties of `Σ.L`'s value structure or its targets that are either orthogonal to extension at a fresh key (L2, L4, L5, L6, L7, L8, L10, L13, L14a) or preservation lemmas under monotone extension (L14, L9 — and L14's scoped form is preserved when the new address is link-subspace by Step 2). The ASN-0036 S-invariants and `Σ.M` operate on `Σ.C, Σ.M`, both unchanged. ∎

*Remark on the precondition.* The hypothesis `dom(Σ.M) ≠ ∅` is necessary: by L1a (LinkScopedAllocation), every link address lives under some allocated document, so before any document exists, no link can be allocated. Once at least one document is present, R0 supplies a fresh link address; in particular, R0 may be invoked recursively to add links into the same document or into any subsequently emitted one.

**R1 — AddressInjectivity.** The map `addr : L → A_rel` is an injection:

`(A (a, F, G), (a', F', G') ∈ L : a = a' :: F = F' ∧ G = G' ∧ both belong to the same coverage-class slice L_{[K]})`

*Proof.* `Σ.L` is a partial function `T ⇀ Link` (ASN-0043, Definition of LinkStore). Function-ness gives uniqueness of value: if `a = a'`, then `Σ.L(a) = Σ.L(a')`, and that single value determines the triple `(F, G, K'')` stored at `a`. Therefore `F = F'`, `G = G'`, and the third endset `K''` is unique. Since `coverage(·)` is a pure function on endset values, `coverage(K'')` is a single fixed address set, so the coverage class `[K'']` is unique — whence both members of `L` lie in the same `L_{[K'']}`. ∎

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

`(A Σ → Σ', K ∈ T_admissible :: L_K^Σ ⊆ L_K^{Σ'})`

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

*Proof.* By the setup hypothesis, every content address is `s_C`-resident, so the slice `dom(Σ.C)|_{s_C}` (L0a, ContentSubspaceScope, ASN-0043) coincides with `dom(Σ.C)`. L14 (DualPrimitive, ASN-0043) asserts `dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅`. Substituting, `dom(Σ.L) ∩ dom(Σ.C) = ∅`, i.e., `A_doc^Σ ∩ A_rel^Σ = ∅`. ∎

*Remark on the underlying structural mechanism.* L14's derivation in ASN-0043 rests on three facts: link addresses have `subspace_I = s_L` (L0, SubspacePartition), the `s_C`-resident content slice has `subspace_I = s_C` (L0a, ContentSubspaceScope), and the substrate convention fixes `s_C ≠ s_L` as distinct first-element-field subspace identifiers. T3 (CanonicalRepresentation, ASN-0034) makes tumblers that disagree in any component distinct as values, so addresses with distinct first-element-field components are distinct tumblers. T7 (SubspaceDisjointness, ASN-0034) packages this for element-level addresses, but its applicability requires `zeros(a) = zeros(a') = 3` on both addresses — which L1 (LinkElementLevel, ASN-0043) supplies for link addresses and the analogous ASN-0036 element-level constraint supplies for `s_C`-resident content. R4 invokes only the consolidated L14, deferring this chain to ASN-0043's derivation.

*Remark on L14's scoped form.* L14 supplies disjointness scoped to its hypothesis on which subspace each content address inhabits; here the setup hypothesis is what discharges that scoping globally. Where future work admits `s_L`-resident content, R4 would be replaced by L14 in its native scoped form, and the consequences below would apply slice by slice rather than substrate-wide.

*Consequences (S4).*

(a) *Predicates are typeable.* A predicate like `is_classified(d, K)` has signature `A_doc × T_cat → Bool`; a predicate like `is_active(τ)` (R6) has signature `A_rel → Bool`. No predicate has an ambiguous signature; categorical confusion at the address level is impossible.

(b) *Retraction is well-typed.* Only `A_rel` addresses are valid arguments to Nullify (R6). "Retracting a document" is not directly expressible — the to-set of an `L_R` tuple must contain a tuple address, not a document address. Document removal from active consideration is done via classifier tuples (e.g., `L_retired`) targeting the document; the document's `A_doc` address is never disturbed.

(c) *Lifecycle separation.* Documents have mutable bodies (arrangements `Σ.M` change per ASN-0036); tuples never mutate (R2). The address-level structure permits these to diverge without interference.


## Self-Reference (R5)

**R5 — TupleSelfTargeting.** A tuple's from-set or to-set may reference tuple addresses. Specifically, for any state Σ and any `a ∈ A_rel^Σ`, the unit-depth span `(a, δ(1, #a))` is well-formed and may appear in the from-set or to-set of an emitted tuple, with `a` in its coverage.

*Justification (positive permission).* We argue in two stages.

(Stage 1 — the construct is permitted.) L4(c) (EndsetGenerality, ASN-0043) explicitly states that endset spans may reference addresses in the link subspace `s_L` — i.e., addresses of other links. L13 (ReflexiveAddressing, ASN-0043) establishes that for any address `b`, the unit-depth span `(b, δ(1, #b))` is well-formed with coverage `{t : b ≼ t}` ⊇ `{b}`. Specializing to `b = a` with `a ∈ A_rel^Σ`, the span `(a, δ(1, #a))` is well-formed by L13 and is span-target-admissible by L4(c). R0's construction discharges invariant-preservation for an emission carrying such a span as an endset component: R0 Step 4 verifies each L-invariant against an arbitrary well-formed triple `(F, G, K)`, and the verification chain does not condition on what addresses appear inside `F` or `G` — so taking `F` or `G` to contain `(a, δ(1, #a))` with `a ∈ A_rel^Σ` is admissible by the same step-by-step check.

(Stage 2 — no invariant opposes the construct.) An exhaustive check of the ASN-0043 invariants confirms none is in opposition to the construction in Stage 1. We list each and identify why:

- L-fin (LinkStoreFiniteness): bounds `|dom(Σ.L)|`; orthogonal to span targets.
- L0 (SubspacePartition): constrains link-address residence (`s_L`), is silent on endset-target subspace.
- L0a (ContentSubspaceScope): defines the `s_C`-resident content slice; orthogonal to span targets.
- L1 (LinkElementLevel), L1a (LinkScopedAllocation), L1b (LinkElementFieldDepth), L1c (LinkAllocatorConformance): constrain `Σ.L`'s domain — what addresses may be in `dom(Σ.L)` — not what values may appear within their endsets.
- L2 (OwnershipEndsetIndependence): asserts `home(a)` depends only on `a`, not on endset content; adding new endset content (including self-targeting spans) leaves `home(·)` undisturbed.
- L3 (NEndsetStructure): requires `|Σ.L(a)| ≥ 3` and the type endset non-empty; agnostic to span targets within endsets.
- L4 (EndsetGenerality), L4(c): the positive permission used in Stage 1.
- L5 (EndsetSetSemantics): treats endsets as unordered sets; orthogonal to target subspace.
- L6 (SlotDistinction): positional accessor `Σ.L(a).eᵢ`; orthogonal to span targets.
- L7 (DirectionalFlexibility): silent on directional interpretation; orthogonal.
- L8 (TypeByAddress): operates on type slot via address-identity comparison; orthogonal to span targets in from/to slots.
- L9 (TypeGhostPermission): permits non-content type endsets; if anything, broadens what can be referenced.
- L10 (TypeHierarchyByContainment): operates on coverage of type endsets; orthogonal to span targets in from/to slots.
- L11a (LinkUniqueness): distinct allocation events produce distinct addresses; compatible with emissions whose endsets self-target.
- L11b (NonInjectivity): permits value-level coincidence; compatible.
- L12 (LinkImmutability), L12a (LinkStoreMonotonicity), L12b (HomeDocumentPersistence): forbid mutation and assert persistence; do not forbid new emissions with self-targeting endsets.
- L13 (ReflexiveAddressing): the constructive lemma used in Stage 1.
- L14 (DualPrimitive): asserts content/link residence disjointness; does not restrict span-target subspace within endsets.
- L14a (NonTranscludability): forbids tumblers occurring in arrangements from being link addresses; orthogonal to span targets within link endsets.

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

**Definition — RetractionType.** Fix a designated coverage class `[R]` reserved for retraction, represented by any `R ∈ T_admissible` whose coverage selects the conventional retraction address set. The corresponding typed relation `L_R^Σ` is the *retraction relation at state Σ*. By L9 (TypeGhostPermission, ASN-0043), `R` need not refer to anything stored — its coverage is an address set, chosen by convention — and `L_R^Σ` is well-defined as a coverage-class slice regardless of whether any literal representative is in `T_cat^Σ`. Before the first retraction emission, `L_R^Σ = ∅` and no representative of `[R]` lies in `T_cat^Σ`; after the first such emission, at least one representative does. The definition of `L_R^Σ` does not depend on which case applies. By coverage-equivalence (Definition of TypedRelation), any emission with a type endset `R'` satisfying `coverage(R') = coverage(R)` contributes to `L_R^Σ` and to `nullified(Σ)` — callers are not required to use a canonical span structure for `R`, only its canonical coverage.

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

`(A Σ, K, (a, F, G) ∈ L_K^Σ : a ∈ nullified(Σ) : (A Σ' : Σ ⊑ Σ' :: (a, F, G) ∉ A_K^{Σ'}))`

To "restore" content, emit a fresh tuple with the desired value (R0). The new tuple receives a fresh address; the retracted tuple keeps its address (R2) and stays out of `A_K` (R6a).

*Proof.* We first show `a ∈ nullified(Σ')` by induction on the length `n` of the `→`-chain `Σ = Σ_0 → Σ_1 → … → Σ_n = Σ'` witnessing `Σ ⊑ Σ'` (Definition of Extension). *Base* (`n = 0`): `Σ' = Σ` and `a ∈ nullified(Σ)` by hypothesis. *Step* (`n = k+1`): assume `a ∈ nullified(Σ_k)`. Apply R6a to the single step `Σ_k → Σ_{k+1}` to obtain `a ∈ nullified(Σ_{k+1}) = nullified(Σ')`. By Definition of `A_K`, since `a ∈ nullified(Σ')`, `(a, F, G) ∉ A_K^{Σ'}`. ∎

*Consequences (S6).*

(a) *Operational vs. historical views.* `A_K` is the operational view ("what is currently in effect"); `L_K` is the audit view ("what has ever existed"). Both are computed from `Σ.L` by the same observation machinery, differing only in whether `nullified(Σ)` is excluded. Operational and historical queries use the same observation primitive but specify different views.

(b) *Mutation as set-difference.* `A_K^Σ = L_K^Σ \ {(a, F, G) : a ∈ nullified(Σ)}`. Computed live; no flag, no cache, no version field anywhere in the architecture.

(c) *Quiescence is operational, not historical.* "Every public predicate over `A_K` holds" is the convergence condition. It does not require historical agreement; it requires the current substrate to satisfy every public check.

(d) *All visible relational-layer operations reduce to `Emit_K`.* File a comment, close it, retract a citation, retire a document (by classifier tuple), revive it — each is one or two `Emit_K` calls (varying `K`). The substrate's response (`A_K` shifts, predicates flip) is uniform across the lot. Document allocation and content emission remain separate primitive transitions in `→`; the reduction here is scoped to the relational layer, not to the substrate as a whole.


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

*Rationale for the match relation.* `F̂ ⊆ coverage(F)` is the *minimal* substrate-level match relation, in two senses. First, every substrate computes `coverage(·)` (ASN-0043, Definition of coverage) as the canonical endset-to-address projection, and subset-containment of finite address sets is universally available — no auxiliary primitive is required. Second, the relation answers the canonical substrate-level question: "does this tuple's from-endset cover every address in the requested pattern?" This is exactly the question for which subset-on-coverage is the affirmative answer; richer queries (span-prefix containment, regex over a content projection, type-equality at the address level via L8) post-compose with Observe rather than parameterizing it. Observe is therefore fixed as the substrate-level primitive that returns "tuples whose endsets cover the requested address sets"; layered query languages obtain other relations by filtering Observe's output.

**Definition — Nullify.** For input state Σ and `a ∈ A_rel^Σ` with `|Σ.L(a)| = 3` (i.e., `a` is the address of a standard-triple link), Nullify is the composition

`Nullify(Σ, a) ≡ Emit_R(Σ, ∅, {(a, δ(1, #a))})`

That is, emit a tuple into the retraction relation with empty from-set and a unit-depth to-span targeting `a`. By PrefixSpanCoverage (ASN-0043), `coverage({(a, δ(1, #a))}) = {t : a ≼ t}`, which contains `a`. Let `(Σ', _) = Nullify(Σ, a)`. By Definition of `nullified`, `a ∈ nullified(Σ')`. By R6a, `a` remains nullified thereafter.

The arity-3 restriction matches this note's scope. `A_K^Σ` is defined only over standard-triple links (Definition of `L_K^Σ`), so the active-subset effect of Nullify is meaningful only on arity-3 addresses. Nullifying a higher-arity address (`|Σ.L(a)| > 3`) would be a well-formed Emit_R, and would deposit `a` into `nullified(Σ')`, but no `A_K^{Σ'}` would feel the effect under the present definitions; extending the active-subset machinery to multi-arity relations `A_K^{(n),Σ}` is left to the open question on higher-arity links.

**R7 — NullifyIsEmit.** Nullify is not a separate primitive at the relational layer; it is `Emit_R` with a designated argument shape.

*Proof.* By Definition. At the relational layer, the substrate exposes exactly two visible-operation primitives: `Emit_K` (which writes) and Observe (which reads). Nullify is a composition of `Emit_R`, not an additional primitive. There is no Update primitive at the relational layer at all; change is nullify-then-emit, both expressed via `Emit_K`. (Document allocation and content emission, the other two transitions in `→`, sit at the substrate layers below — ASN-0036 — and remain primitive there; this lemma scopes the reduction to the relational layer.) ∎


## Worked Sketch

We illustrate the structure of a retraction cycle in the relational vocabulary, building on the ASN-0043 worked example.

*Setup.* Let `K ∈ T_admissible` be any content-classifying type with `K ∈ T_cat^{Σ_0}`. Suppose at state `Σ_0` the substrate contains:

`L_K^{Σ_0} = {(a₁, F₁, G₁)}` &nbsp; — one classification tuple
`L_R^{Σ_0} = ∅` &nbsp; — no retractions yet

By Definition, `A_K^{Σ_0} = L_K^{Σ_0} = {(a₁, F₁, G₁)}` and `nullified(Σ_0) = ∅`. Let `d = home(a₁) ∈ dom(Σ_0.M)`, so `a₁ ∈ LS(d)` (recall `LS(d) = {a ∈ T : d ≼ a ∧ T4-valid(a) ∧ zeros(a) = 3 ∧ a.E₁ = s_L ∧ #E(a) ≥ 2}` from R0's proof). We further note that, by L1c (LinkAllocatorConformance, ASN-0043) and the T10a-chain construction in R0 Step 2 (Case B), subsequent allocations within `LS(d)` need not nest under `a₁` — the typical configuration, since allocator outputs within a document's link subtree are siblings or successors of existing link addresses under the discipline, not unconditional prefix-extensions.

*Step 1: Nullify a₁.* `Σ_0 → Σ_1` via `Nullify(Σ_0, a₁) = Emit_R(Σ_0, ∅, {(a₁, δ(1, #a₁))})`. We invoke not R0's bare existential — which would expose neither the home choice nor any prefix-relation constraint at its interface — but R0's *Step 2 Case B construction*, whose preconditions are met since `a₁ ∈ dom(Σ_0.L)` with `home(a₁) = d`. The construction (taking `b = a₁`) yields `b₁ = incⁱ(a₁, 0)` for the least `i ≥ 1` with `incⁱ(a₁, 0) ∉ dom(Σ_0.L)`. By Case B's chain extension, `home(b₁) = home(a₁) = d`, so `b₁ ∈ LS(d)`. By T10a.2 (NonNestingSiblingPrefixes, ASN-0034), `b₁` and `a₁` are distinct siblings of the allocator producing `a₁` and are therefore prefix-incomparable; in particular `a₁ ⊀ b₁`. The to-set `{(a₁, δ(1, #a₁))}` then covers `{t : a₁ ≼ t}` (by PrefixSpanCoverage, ASN-0043), which contains `a₁` and its tumbler-prefix extensions but does not contain `b₁`. The post-state has `Σ_1.L(b₁) = (∅, {(a₁, δ(1, #a₁))}, R)`. Now:

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

*Concrete instantiation.* The schematic sketch admits a fully concrete instantiation, with every address resolved to a specific tumbler and every set-theoretic claim verified by direct inspection. Fix:

- `s_L = 2` (link subspace identifier — matching the ASN-0043 worked example).
- `d = 1.0.1.0.1` — document address, `zeros(d) = 2`, length `5`, T4-valid.
- `c₁ = 1.0.1.0.1.0.1.1`, `c₂ = 1.0.1.0.1.0.1.2` — two content addresses in `dom(Σ_0.C)`, both with `subspace_I = 1 = s_C`, `zeros = 3`, depth `8`.
- `k = 3.0.0.0.1` — a ghost address for the classification type `K = {(k, δ(1, 5))}`, with `coverage(K) = {t : k ≼ t}`.
- `r = 4.0.0.0.1` — a ghost address for the retraction coverage class `[R]`, with `R = {(r, δ(1, 5))}` and `coverage(R) = {t : r ≼ t}`. By construction `coverage(K) ∩ coverage(R) = ∅` (different first components in subspaces 3 and 4), so `K` and `R` lie in distinct coverage classes.
- `a₁ = 1.0.1.0.1.0.2.1` — the classification tuple's address. The L1c chain from `d` walks through the existing depth-1 element-field allocator `A_d` (which serves both content and link subspaces under `d`): (i) `inc(d, 2) = 1.0.1.0.1.0.1` — the address produced by the `(d, 2)` spawn that creates `A_d`; this spawn occurred once system-wide and also supports the content emissions `c₁, c₂` (the L1c chain witnesses, does not re-issue, the spawn); (ii) `inc(·, 0) = 1.0.1.0.1.0.2` — sibling sweep within `A_d` from subspace 1 (content) to subspace `s_L = 2` (link); (iii) `inc(·, 1) = 1.0.1.0.1.0.2.1` — child-spawn `(d.0.2, 1)`, the only spawn fresh for the link emission. Verification: `zeros(a₁) = 3`, `E(a₁) = [2, 1]`, `a₁.E₁ = 2 = s_L`, `#E(a₁) = 2`, T4-valid, `home(a₁) = 1.0.1.0.1 = d`. So `a₁ ∈ LS(d)`. ✓
- `F₁ = {(c₁, δ(1, 8))}`, `G₁ = {(c₂, δ(1, 8))}` — singleton-span endsets covering `c₁` and `c₂` respectively (by PrefixSpanCoverage).
- `Σ_0.L = {a₁ ↦ (F₁, G₁, K)}`, `L_K^{Σ_0} = {(a₁, F₁, G₁)}`, `L_R^{Σ_0} = ∅`.

*Step 1 (concrete).* Applying R0 Step 2 Case B with `b = a₁`: the least `i ≥ 1` with `incⁱ(a₁, 0) ∉ dom(Σ_0.L) = {a₁}` is `i = 1`, since `inc¹(a₁, 0) = 1.0.1.0.1.0.2.2 ∉ {a₁}`. Set `b₁ = 1.0.1.0.1.0.2.2`. Verification: `zeros(b₁) = 3`, `E(b₁) = [2, 2]`, `b₁.E₁ = 2 = s_L`, `#E(b₁) = 2`, `home(b₁) = d`, T4-valid; `b₁ ∈ LS(d)`. `b₁` is a sibling of `a₁` in their shared allocator (both are siblings emitted by the allocator at base `1.0.1.0.1.0.2.1` via `inc(·, 0)`); by T10a.2, `a₁` and `b₁` are prefix-incomparable, so `a₁ ⊀ b₁`.

Emit the retraction: `Σ_1.L = Σ_0.L ∪ {b₁ ↦ (∅, {(a₁, δ(1, 8))}, R)}`. Now compute:

- `coverage({(a₁, δ(1, 8))})`: by PrefixSpanCoverage (with `#a₁ = 8`), `= {t ∈ T : a₁ ≼ t} = {t : 1.0.1.0.1.0.2.1 ≼ t}`. Membership check: `a₁ ∈ {t : a₁ ≼ t}` by reflexivity of `≼`. `b₁ = 1.0.1.0.1.0.2.2`: comparing component-wise, `a₁` and `b₁` agree on positions `1..7` (both `1.0.1.0.1.0.2`) and differ at position `8` (`1` vs `2`); since they have equal length but differ in content, neither is a prefix of the other. So `b₁ ∉ coverage({(a₁, δ(1, 8))})`. ✓
- `L_R^{Σ_1}`: `Σ_1.L(b₁).e₃ = R`, and `coverage(R) = coverage(R)` trivially, so `(b₁, ∅, {(a₁, δ(1, 8))}) ∈ L_R^{Σ_1}`. No other tuple in `Σ_1.L` has type slot coverage-equivalent to `R` (the only other tuple, at `a₁`, has type `K` with `coverage(K) ≠ coverage(R)` by the disjointness above). So `L_R^{Σ_1} = {(b₁, ∅, {(a₁, δ(1, 8))})}`. ✓
- `nullified(Σ_1) = {a ∈ A_rel^{Σ_1} : (E (b, F', G') ∈ L_R^{Σ_1} :: a ∈ coverage(G'))} = {a ∈ {a₁, b₁} : a ∈ coverage({(a₁, δ(1, 8))})} = {a₁}`. ✓
- `A_K^{Σ_1} = L_K^{Σ_1} \ {(a, F, G) : a ∈ nullified(Σ_1)} = {(a₁, F₁, G₁)} \ {(a₁, F₁, G₁)} = ∅`. ✓

*Step 2 (concrete).* Re-emit `Emit_K(F₁, G₁)`. R0 Step 2 Case B (`b = a₁` again works; `b = b₁` would also work) seeks the least `i ≥ 1` with `incⁱ(a₁, 0) ∉ dom(Σ_1.L) = {a₁, b₁}`. `inc¹(a₁, 0) = b₁ ∈ dom(Σ_1.L)`; `inc²(a₁, 0) = 1.0.1.0.1.0.2.3 ∉ dom(Σ_1.L)`. Set `a₂ = 1.0.1.0.1.0.2.3`. Then `Σ_2.L = Σ_1.L ∪ {a₂ ↦ (F₁, G₁, K)}` and:

- `L_K^{Σ_2} = {(a₁, F₁, G₁), (a₂, F₁, G₁)}` — two coverage-class members with identical `(F, G)`, distinct addresses.
- `nullified(Σ_2)` is unchanged: the only `L_R` tuple is still the one at `b₁`, with the same `coverage(G')` containing only `a₁` (not `a₂`, since `a₁` and `a₂` are also distinct siblings under the same allocator). So `nullified(Σ_2) = {a₁}`.
- `A_K^{Σ_2} = {(a₂, F₁, G₁)}` — the new tuple is active; the historical tuple at `a₁` remains in `L_K` but excluded from `A_K`. ✓

Every set-theoretic claim of the schematic sketch is discharged here by direct inspection of tumbler values, with the coverage-equivalence definition of `L_R` and the T10a.2-based prefix-incomparability between sibling allocator outputs both exercised concretely.


## Properties Introduced

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| Setup | HYP | Globally `s_C`-resident content: `(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)` | introduced |
| A^Σ | DEF | Address universe at state Σ: `dom(Σ.C) ∪ dom(Σ.L)` | introduced |
| A_doc^Σ, A_rel^Σ | DEF | Partition of `A^Σ` into content addresses (`dom(Σ.C)`) and tuple addresses (`dom(Σ.L)`) | introduced |
| T_admissible | DEF | Admissible types: `{K ∈ Endset : K ≠ ∅}` — the indexing domain for typed relations | introduced |
| T_cat^Σ | DEF | Type catalog at Σ — admissible types actually in use at Σ (descriptive, not constitutive) | introduced |
| ~ | DEF | TypeEquivalence: `K ~ K' ≡ coverage(K) = coverage(K')` — coverage-equivalence on admissible types (= L8 lifted) | introduced |
| L_K^Σ | DEF | Typed relation (coverage-class slice): `{(a, F, G) : a ∈ dom(Σ.L) ∧ |Σ.L(a)| = 3 ∧ Σ.L(a).e₁ = F ∧ Σ.L(a).e₂ = G ∧ coverage(Σ.L(a).e₃) = coverage(K)}` | introduced |
| L^Σ | DEF | Standard-triple link store: `⨆_{[K] ∈ T_admissible / ~} L_K^Σ` | introduced |
| addr | DEF | Map `(a, F, G) ↦ a : L^Σ → A_rel^Σ` | introduced |
| nullified(Σ) | DEF | Tuple addresses targeted by some `L_R^Σ` to-set | introduced |
| A_K^Σ | DEF | Active subset: `{(a, F, G) ∈ L_K^Σ : a ∉ nullified(Σ)}` | introduced |
| R0 | LEMMA | TupleAddressFreshness — under precondition `dom(Σ.M) ≠ ∅`, every emission allocates a fresh address (= L1 + L1a + L1b + L1c + L3 + L0 + L-fin from ASN-0043; T0(a) + T0(b) + T10a axiom + T10a.6 + T10a.7 from ASN-0034; S7d from ASN-0036) | introduced |
| R1 | LEMMA | AddressInjectivity — `addr` is an injection (= function property of `Σ.L`) | introduced |
| R2 | LEMMA | TupleAddressPermanence — addresses persist with values intact (= L12) | introduced |
| R3 | LEMMA | TypedSliceMonotonicity — each `L_K^Σ` is monotone (= L12a + R2) | introduced |
| R4 | LEMMA | TupleAddressDisjointness — `A_doc^Σ ∩ A_rel^Σ = ∅` (= Setup + L14, whose underlying chain is L0 + L0a + T3 + the `s_C ≠ s_L` convention) | introduced |
| R5 | META | TupleSelfTargeting — for any `a ∈ A_rel^Σ`, the span `(a, δ(1, #a))` is admissible as an endset member (= L4(c) + L13, no opposing invariant) | introduced |
| R6 | LEMMA | ActiveSubsetWellDefinedness — `A_K^Σ` is determined by `Σ.L` | introduced |
| R6a | LEMMA | RetractionStability — once nullified, always nullified (= R3 + R2 + purity of coverage) | introduced |
| R6b | LEMMA | SingleDepthRetraction — `nullified` checks only direct targeting | introduced |
| R6c | LEMMA | RestorationByReemission — restoration is fresh emission, never retraction-of-retraction | introduced |
| R7 | LEMMA | NullifyIsEmit — Nullify is `Emit_R` with designated argument shape, not a separate primitive | introduced |
| Emit_K | OP | State-transforming: `Σ × Endset × Endset → Σ' × A_rel^{Σ'}`, with `K ∈ T_admissible` and `dom(Σ.M) ≠ ∅` | introduced |
| Observe_K | OP | Pure read: `Σ × ℘_fin(A) × ℘_fin(A) × View → ℘_fin(L_K^Σ)`, selecting `L_K^Σ` or `A_K^Σ` | introduced |
| Nullify | OP | `Nullify(Σ, a) ≡ Emit_R(Σ, ∅, {(a, δ(1, #a))})` for `a ∈ A_rel^Σ` with `|Σ.L(a)| = 3` | introduced |
| → | DEF | State transition relation: `Σ → Σ'` is one of (i) document allocation, (ii) content emission, (iii) `Emit_K`. No removal/replacement transition exists. | introduced |


## Open Questions

- What invariants must hold between `L_K` and the arrangements `Σ.M` when relational predicates depend on whether the from-set or to-set content is currently visible in some document?
- Should multi-arity links (`|Σ.L(a)| > 3`) define multiple binary projections, or be regarded directly as elements of higher-arity typed relations `L_K^{(n)} ⊆ A_rel × ℘(A)^n`?
- Under what conditions is `Nullify(b)` for `b ∈ L_R` operationally meaningful, given that R6b makes single-depth checking ignore the second-order retraction?
- What ordering, if any, must the substrate guarantee on Observe results — by emission cycle, by tuple address, or unordered as set semantics suggest?
- Must Emit be atomic with respect to concurrent Observe, and if so, what is the consistency model under which `A_K` transitions are observed?
- What guarantees does the substrate provide about the cardinality bound of `nullified(Σ)` relative to `dom(Σ.L)` — is unbounded retraction permitted, or must some structural ratio hold?
- Can higher layers extend the type catalog `T_cat` dynamically without coordination, given L9 (TypeGhostPermission), and what happens when two layers independently choose colliding type addresses?