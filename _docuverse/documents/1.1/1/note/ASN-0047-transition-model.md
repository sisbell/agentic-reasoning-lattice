# ASN-0047: Transition Model

*2026-03-17, revised 2026-03-22*

ASN-0036 established two components of system state — a permanent content store C and mutable document arrangements M(d) — and proved their separation: content, once stored, is immutable (S0); arrangement mutations cannot alter the content store (S9). These are properties of the invariants. We have not yet classified the transitions. In what primitive ways can the state change, and what must each change preserve?

The consultation answers reveal a state model richer than the two-space analysis captured. Nelson enumerates the ways the docuverse changes — new documents created, new content inserted, new links established, views rearranged — and is equally precise about what cannot happen: content is never destroyed, addresses are never reassigned, history is never erased. Gregory reduces eight protocol commands to six kinds of persistent modification, distributed across three storage layers with distinct permanence contracts.

We seek the abstract taxonomy. Not the protocol commands, which are interface design, but the primitive modifications and their invariants. The central result is a *mutability hierarchy*: the state components arrange into three temporal layers, each with its own permanence contract. Destructive change — removal and reordering — is confined entirely to the most mutable layer.


## Notation

This ASN draws on projection functions and predicates established in the foundation ASNs (ASN-0034 Tumbler Algebra, ASN-0036 Strand Model, ASN-0043 Link Model, ASN-0045 Tumbler Fields). For reader convenience we list them here, fixing one notation per concept and pointing to the defining ASN. Notation introduced for the first time in this ASN is marked "introduced here."

*I-address (element-level) projections.* For each `a ∈ T_elem`:

- `E(a)` (ASN-0034, T4b): the element-field projection — the sequence of components after the last zero separator. `E(a)` is itself a positive-component tumbler with `#E(a) ≥ 1`.
- `subspace_I(a)` (ASN-0036): the I-address subspace identifier, equal to `E(a)₁`.
- `origin(a)` (ASN-0036, S7a): the document address `d ∈ E_doc` under whose allocator a was minted. For each `a ∈ dom(C)`, `origin(a) ∈ E_doc`; for each `ℓ ∈ dom(L)`, `origin(ℓ) ∈ E_doc` (L1a). origin is recovered by truncating a to the document prefix (zeros = 2).
- `IsElement(a)`, `IsNode(a)`, `IsAccount(a)`, `IsDocument(a)` (ASN-0045): level predicates parameterised by `zeros(a)` ∈ {0, 1, 2, 3}.
- `#E(a)` (ASN-0034): the depth (component count) of `E(a)` — equivalently `#a − zeros(a) − 1` if a has zero separators, or `#a` if a has no zero separators.

*V-position (arrangement-domain) projections.* For each `v ∈ dom(M(d))`:

- `subspace(v)` (ASN-0036): the first component `v₁` of the V-position tumbler — the subspace identifier at the V-position level. By S8a, every `v ∈ dom(M(d))` satisfies `v₁ ≥ 1`, so `subspace(v) ∈ ℕ⁺`. In this ASN the two subspaces are `s_C` (content/text) and `s_L` (link), with `s_C ≠ s_L` (SC-NEQ axiom, introduced here).
- `#v` (ASN-0034): the depth of v. By S8-depth, V-positions within a fixed subspace under a fixed document share a common depth `m_S`.

*Entity-hierarchy projections.* For each non-node entity `e ∈ E`:

- `parent(e)` (introduced here, §The state model): the tumbler obtained by truncating e's last field together with its preceding zero separator. `parent(e)` is the entity-hierarchy spine — defined only for non-node entities (`¬IsNode(e)`), and producing a valid address at the next-higher level: `zeros(parent(e)) = zeros(e) − 1`.

*Subspace-position correspondence.* For `v ∈ dom(M(d))` with `M(d)(v) = a`, `subspace(v) = subspace_I(a)` (S3★). The two projections apply at different state-component levels — `subspace(v)` projects V-positions, `subspace_I(a)` projects I-addresses.

*Content/link domain notation.* `dom_C(M(d)) := V_{s_C}(d) := {v ∈ dom(M(d)) : subspace(v) = s_C}`; symmetrically `dom_L(M(d)) := V_{s_L}(d) := {v ∈ dom(M(d)) : subspace(v) = s_L}`. The `V_S(d)` form generalises to any subspace S; both spellings appear in this ASN denotationally identically.

*Entity-level allocator.* A T10a-tracked sub-allocator whose output addresses satisfy `zeros(·) ≤ 2`: node, account, document, and version sub-allocators. The content and link sub-allocators `A_C(d), A_L(d)` introduced under SubAllocatorAxiom are *not* entity-level — their outputs inhabit `dom(C) ∪ dom(L)` at zeros = 3.


## The state model

ASN-0036 gave us C and M(d). Two phenomena require additional state components.

First, entities come into existence. Nelson describes exactly two document creation modes: ex nihilo (a fresh empty document) and forking (a new document derived from an existing one). Gregory confirms both use the same allocation mechanism, differing only in whether the new arrangement starts empty or populated. We need an explicit record of which entities exist.

**Definition (Entity set).** **Σ.E ⊆ T** — the set of allocated entity addresses. Every e ∈ E satisfies ValidAddress(e) (T4, ASN-0034). Entities are organisational — nodes, accounts, documents — not content; element-level addresses live in dom(C), not E:

`(A e ∈ E :: ¬IsElement(e))`

Equivalently, E ⊆ {t : ValidAddress(t) ∧ zeros(t) ≤ 2}.

*Consequence (Stratification).* By T4c (ASN-0045) and the exclusion clause above, Σ.E partitions into exactly three strata:

- E_node = {e ∈ E : IsNode(e)} — server nodes
- E_account = {e ∈ E : IsAccount(e)} — user accounts
- E_doc = {e ∈ E : IsDocument(e)} — documents (zeros = 2)

For a non-node entity e (where ¬IsNode(e)), define **parent(e)** using T4b's (UniqueParse, ASN-0034) partial projections N, U, D, E:

- *Account case (IsAccount(e)).* `parent(e) = N(e)` — the node-prefix projection. Since `IsAccount(e)` requires `zeros(e) = 1`, T4b's parse `e = N(e).0.U(e)` is defined with `zeros(N(e)) = 0`, giving `zeros(parent(e)) = 0 = zeros(e) − 1`.
- *Document case (IsDocument(e)).* `parent(e) = N(e).0.U(e)` — the account-prefix projection. Since `IsDocument(e)` requires `zeros(e) = 2`, T4b's parse `e = N(e).0.U(e).0.D(e)` is defined with `zeros(N(e).0.U(e)) = 1`, giving `zeros(parent(e)) = 1 = zeros(e) − 1`.

In each case parent(e) is a valid address at the next higher level: `zeros(parent(e)) = zeros(e) − 1` is a derivable property of T4b's projections, not a stipulation. The two cases together define parent uniformly on non-node entities (the IsNode case is excluded by the precondition `¬IsNode(e)`, since nodes have no parent in the entity-hierarchy spine).

M is a total function with M(d) = ∅ (the empty partial function) when d ∉ E_doc; non-empty arrangements arise only for document entities. Links are owned by documents (`origin(ℓ) ∈ E_doc`, by L1a) but inhabit a separate state component L, not E_doc: L1 (ASN-0043) requires `zeros(ℓ) = 3` for every link address, and IsDocument (ASN-0045) requires `zeros(t) = 2`, so `IsDocument(ℓ)` is false and `ℓ ∉ E`. Nelson describes links as owned entities with internal structure ("a package of connecting or marking information... owned by a user... thereafter maintained by the back end"); the link store L gives them their own first-class state component, distinct from the entity set E.

Second, removal of content from an arrangement does not erase the historical fact of prior containment. Gregory: the reverse index "accumulates entries from every content addition but is never trimmed." Nelson: "every previous arrangement remains reconstructable." The system must answer "which documents have ever contained content with origin *a*?" — a question about history, not about current state.

**Definition (Provenance relation).** **Σ.R ⊆ T_elem × E_doc** — where T_elem = {a ∈ T : IsElement(a)} (ASN-0045). The pair (a, d) ∈ R records that document d has, at some point in the system's history, contained I-address a in its arrangement. This historical fidelity — that every entry reflects an actual past containment event, not merely eligibility — is not assumed by the definition alone; it is established as P4a below, by induction over J1', P2, and P0.

The full system state is:

> **Σ = (C, E, M, R)**

where C : T ⇀ Val is as defined in ASN-0036, and M : T → (T ⇀ T) is total, satisfying M(d) = ∅ for d ∉ E_doc.

**Definition (Initial state).** The initial state Σ₀ = (C₀, E₀, M₀, R₀) is:

- C₀ = ∅ (no content allocated)
- E₀ = {n₀} where n₀ = `[1]` — the canonical single-component bootstrap node
- M₀(d) = ∅ for all d — (E₀)_doc = ∅, so every arrangement is the empty partial function
- R₀ = ∅ (no provenance recorded)

**Structural form of n₀.** The bootstrap node is fixed as `[1]` — a one-element tumbler with `zeros(n₀) = 0`, satisfying `IsNode(n₀)` and `ValidAddress(n₀)`. The NodeLineage invariant (`n₀ ≼ e`) constrains every node address to extend `[1]` by prefix, ruling out disconnected-forest allocations.

At Σ₀, (E₀)_doc = ∅, so arrangement invariants hold vacuously.

**SequentialTransitionAxiom (Axiom, SequentialAtomicTransitions).** The transition relation `Σ → Σ'` is single-event sequential: each transition is an atomic, uninterruptible event in which the elementary precondition is evaluated against `Σ` and the elementary effect is committed to `Σ'` in one indivisible step, and transitions are totally ordered (no two transitions overlap in time). Equivalently, the system admits no intermediate state in which a transition has begun but not yet committed.


## Link store and extended system state

This ASN uses properties of the link store. For self-containment, we restate the definitions and invariants needed.

**Definition (Endset).** An *endset* is a finite set of well-formed spans: `Endset = 𝒫_fin(Span)`, where `Span` is the set of well-formed span pairs `(s, ℓ)` satisfying T12 (ASN-0034). The empty set ∅ is a valid endset — `∅ ∈ 𝒫_fin(Span)` trivially — matching ASN-0043's `Endset` definition.

**Definition (Link).** A *link value* is a triple `(F, G, Θ)` where `F, G, Θ ∈ Endset` — the *from-endset*, *to-endset*, and *type-endset* respectively.

**Definition (Subspace identifiers).** We write `s_C` for the content subspace identifier and `s_L` for the link subspace identifier. These are the first components of the element field for content and link addresses respectively: `subspace_I(a) = s_C` for content addresses, `subspace_I(ℓ) = s_L` for link addresses. The same identifiers serve for V-positions: `subspace(v) = v₁`.

**SubspaceConventionAxiom (Axiom, FixedSubspaceIdentifiers).** `s_C = 1 ∧ s_L = 2`. The distinctness consequence `s_C ≠ s_L` is abbreviated **SC-NEQ**.

The derivation of L14 (StoreDisjointness, dom(C) ∩ dom(L) = ∅) is a three-premise chain:

  - **L0 (SubspacePartition, this ASN, below).** Every a ∈ dom(C) has subspace_I(a) = s_C; every a ∈ dom(L) has subspace_I(a) = s_L. (L0's C-clause is added in this ASN; the L-clause is from ASN-0043.)
  - **SC-NEQ (consequence of SubspaceConventionAxiom).** s_C ≠ s_L.
  - **T7 (FirstElementFieldDistinction, ASN-0034).** Two tumblers with distinct first element-field components are themselves distinct addresses; equivalently, the value of subspace_I(a) partitions tumblers into disjoint subspaces.

  Chaining: suppose a ∈ dom(C) ∩ dom(L). By L0's C-clause, subspace_I(a) = s_C; by L0's L-clause, subspace_I(a) = s_L. Since subspace_I(a) is a single value for a single tumbler, s_C = s_L, contradicting SC-NEQ. Therefore dom(C) ∩ dom(L) = ∅, i.e., L14 holds.

We note that `s_C ≥ 1` follows from S7b and T4: content I-addresses are element-level by S7b (`zeros(a) = 3`), and T4 requires every element-field component to be strictly positive, so `subspace_I(a) = s_C > 0`. The same derivation gives `s_L ≥ 1`: link I-addresses are element-level by L1 below (`zeros(ℓ) = 3`), so by T4, `subspace_I(ℓ) = s_L > 0`.

**L0 (SubspacePartition).**

  `(A a ∈ dom(Σ.L) :: subspace_I(a) = s_L)`

  `(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)`

The L-clause is from ASN-0043; the C-clause is introduced here, supplied by the K.α amendment below.

**L1 (LinkElementLevel).**

  `(A a ∈ dom(Σ.L) :: zeros(a) = 3)`

Every link address is an element-level tumbler.

**L1a (LinkScopedAllocation).**

  `(A a ∈ dom(Σ.L) :: origin(a) ∈ E_doc)`

Every link address is allocated under the tumbler prefix of a document in E_doc.

**L3 (TripleEndsetStructure).**

  `(A a ∈ dom(Σ.L) :: Σ.L(a) = (F, G, Θ) where F, G, Θ ∈ Endset ∧ Θ ≠ ∅)`

Every link has exactly three endsets, with the type endset non-empty. This narrows ASN-0043's `N ≥ 3` arity to fixed three. The `Θ ≠ ∅` conjunct is *not* part of ASN-0043's `Link` definition (which posits only `(e₁, ..., eₙ) : N ≥ 3, each eᵢ ∈ Endset`); it is introduced here as a separate conjunct of L3. Accordingly K.λ's precondition states `(F, G, Θ) ∈ Link ∧ Θ ≠ ∅` explicitly, with the second conjunct cited to L3 — the `Θ ≠ ∅` requirement is *explicit* at every site, not implicit in `Link`.

*Relationship to ASN-0043's foundation L3.* The narrowing from `N ≥ 3` to exactly three is a *local strengthening* applied to states reachable from Σ₀ via this ASN's transition vocabulary, not a re-statement of the foundation invariant. ASN-0043's L3 admits arity ≥ 3 as a general structural envelope. This ASN's L3 reads: every `a ∈ dom(Σ.L)` in a state reachable from Σ₀ by valid composite transitions has `Σ.L(a)` of arity exactly three with `Θ ≠ ∅`. Two complementary facts close out the relationship:

  - (i) *Reachability closure.* The only transition that extends `dom(L)` is K.λ, whose precondition fixes the new entry as a triple `(F, G, Θ) ∈ Link` with `Θ ≠ ∅`; L12 then preserves every entry's value pointwise. Σ₀ has `dom(L₀) = ∅`, so every link populated along any sequence of valid composite transitions from Σ₀ inhabits this ASN's L3 — every reachable state satisfies the strengthened invariant by construction.
  - (ii) *Higher-arity exclusion.* Foundation-conforming states with `N > 3` links are *out of scope* of this ASN's transition model: K.λ does not produce them, and no transition admits a link-value rewrite that could introduce higher arity (L12 is per-entry-immutable). Whether such states could arise outside this ASN — e.g., from a future operations ASN's vocabulary, or from a system bootstrapped with a non-empty `L₀` containing higher-arity entries — is left open. Within the present ASN, the only states under consideration are those reachable from Σ₀, all of which satisfy `N = 3`.

  This local-strengthening framing is consistent with Nelson's design intent — the triple `(F, G, Θ)` is invariant in the design ("This is symmetrical with the other endsets," LM 4/44; richer structures arise through *composition* via link-to-link, LM 4/51) — and with Gregory's implementation, which fixes arity at exactly three throughout (`LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3` in `xanadu.h`; explicit triadic dispatch in `setlinkvsas`, `insertendsetsinspanf`, `intersectlinksets`). The Properties Introduced table records this as a strengthening of foundation L3 to exactly three, matching the framing here.

*Semantics of empty F or G.* L3 admits `F = ∅` and `G = ∅` independently — only Θ is required non-empty. Exactly one of F, G empty is Nelson's one-sided link case (LM 4/48); both empty is admissible as a type-only marker. Whether to narrow K.λ with a stricter `F ∪ G ≠ ∅` precondition is recorded as *design-uncertain* and left to a future operations ASN. Endset-iterating consumers (L8's `same_type`, discovery-set unions) treat an empty endset as contributing ∅ by the natural inductive form.

**L12 (LinkImmutability).**

  `(A Σ → Σ' : (A a : a ∈ dom(Σ.L) : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)))`

Once created, a link's address persists in dom(L) and its value is permanently fixed.

**L14 (StoreDisjointness).**

  `dom(Σ.C) ∩ dom(Σ.L) = ∅`

Derived from L0 and SC-NEQ via T7: if `a ∈ dom(C)` then `subspace_I(a) = s_C`, and if `a ∈ dom(L)` then `subspace_I(a) = s_L`; since `s_C ≠ s_L`, no address inhabits both domains.

**L-fin (LinkStoreFiniteness).** `|dom(Σ.L)| < ∞`. Holds at Σ₀ (|∅| = 0); preserved by K.λ (single-element extension) and by L-frame in all other transitions.

**Extended system state.** The extended system state is **Σ = (C, L, E, M, R)**, where L : T ⇀ Link is the link store.

**Extended initial state.** Σ₀ = (C₀, L₀, E₀, M₀, R₀) with L₀ = ∅. The extended invariants hold vacuously at Σ₀: L0, L1, L1a, L3, L12, L14, L-fin are satisfied by empty L (L-fin: `|∅| = 0 < ∞`); S3★'s link-subspace clause is vacuous (no link-subspace V-positions exist in M₀); P4★ reduces to P4 (which holds at Σ₀ per ASN-0047); D-CTG and D-MIN hold vacuously since M₀(d) = ∅ for all d, so V_S(d) = ∅ for every subspace S. This closes the inductive base for the ExtendedReachableStateInvariants theorem.

All existing elementary transitions from ASN-0047 — K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.ρ — hold L in their extended-state frame: `L' = L`. Only K.λ (introduced below) extends L. L12 (LinkImmutability) follows trivially from this split: `L' = L` preserves dom(L) and values pointwise, and K.λ appends a fresh entry without altering existing ones.


## Permanence

We classify each component by the transitions it admits. Four components, three distinct permanence contracts.

**P0 (Content permanence).** The content store admits only extensions, and existing entries are immutable:

`(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ (A a : a ∈ dom(C) : C'(a) = C(a)))`

This is S0 of ASN-0036, restated for the full state model. C is *append-only with immutable values*. Nelson: "Instead, suppose we create an append-only storage system." Gregory confirms: no deletion or update operation exists for the content store.

**P1 (Entity permanence).** The entity set admits only extensions:

`(A Σ → Σ' :: E ⊆ E')`

No transition removes an entity. This specialises T8 (AllocationPermanence, ASN-0034) to the entity set. P1 holds uniformly across levels:

`[e ∈ E ∧ IsNode(e) ⟹ e ∈ E']`
`[e ∈ E ∧ IsAccount(e) ⟹ e ∈ E']`
`[e ∈ E ∧ IsDocument(e) ⟹ e ∈ E']`

Nelson: "New items may be continually inserted in tumbler-space while the other addresses remain valid." The address space is a growing tree; entities are born but never die.

**P8 (Entity hierarchy).** Every non-node entity has its parent in E:

`(A e ∈ E : ¬IsNode(e) : parent(e) ∈ E)`

This ensures the entity set is hierarchically well-formed: every account has its node in E, every document has its account in E. Combined with P1, the hierarchy only grows — once an entity's parent chain is established, it persists.

*Derivation.* K.δ for non-root entities requires parent(e) ∈ E as a precondition (below). P1 preserves the parent's membership across subsequent transitions. Base case: E₀ = {n₀} with IsNode(n₀), so the quantifier is vacuously satisfied. Inductive step: K.δ adds e with parent(e) ∈ E ⊆ E' (by precondition and P1); all other transitions have E' ⊇ E, preserving existing parent relationships. ∎

**P2 (Provenance permanence).** The provenance relation admits only extensions:

`(A Σ → Σ' :: R ⊆ R')`

Once the system records that d referenced a, that record persists. Gregory: the provenance structure is "a permanently-growing reverse index that accumulates entries from every content addition but is never trimmed."

Arrangements admit three modes of change — extension (new V→I mappings added), contraction (existing V→I mappings removed), and reordering (V-positions of existing mappings change while the multiset of referenced I-addresses is preserved); no other component admits contraction or reordering. Gregory: the arrangement layer is "the sole locus of destructive mutation."


## Elementary transitions

We seek the elementary modifications — the state changes from which all system operations compose. Each is defined by its effect and its frame: what changes and what does not.

**Convention.** A transition with unsatisfied preconditions does not fire.

**K.α (Content allocation).** A fresh I-address is bound to a value in the content store:

`C' = C ∪ {a ↦ v}` where `a ∉ dom(C)`

*Precondition:* `IsElement(a)` (S7b, ASN-0036) ∧ `origin(a) ∈ E_doc` ∧ `a ∉ dom(C)` ∧ `a ∉ dom(L)` ∧ `a` is produced by origin(a)'s content sub-allocator. Freshness against dom(C) is discharged by SubAllocatorAxiom.FirstEmission at the first emission `[d.0.s_C.1]` (which alone is committed outside `dom(C) ∪ dom(L)` by that clause) and by T10a's GlobalUniqueness at every subsequent inc-produced sibling on A_C(d)'s frontier. Disjointness from dom(L) follows from SC-NEQ + T7 + L14.

*Frame:* E' = E; (A d :: M'(d) = M(d)); R' = R.

**NodeLineage (Derived invariant, NodeDescentFromBootstrap).** `(A e ∈ E : IsNode(e) : n₀ ≼ e)`, where `≼` is the prefix order on tumblers (ASN-0034). Proved as part of ExtendedReachableStateInvariants below.

**NodeUniqueAllocation (Axiom, FreshNodeAddress).** Every K.δ node-allocation event — every elementary transition of K.δ whose effect places an entity `e` with `IsNode(e)` into E — produces an address satisfying two conditions: (a) *Freshness:* `e ∉ Σ.E` at the state Σ of allocation; (b) *Bootstrap lineage:* `n₀ ≼ e` under the tumbler-prefix order. These are the conditions the node-allocation registry must satisfy; details of the registry mechanism (issuing protocol, persistence model, concurrency discipline) lie outside this ASN's discharge layer.

**K.δ (Entity creation).** A fresh entity address enters E with initial state:

`E' = E ∪ {e}` where `e ∉ E ∧ ValidAddress(e) ∧ ¬IsElement(e)`

*Precondition.* The precondition splits on `IsNode(e)`, reflecting two distinct allocation disciplines — protocol-established node baptism versus T10a-conforming inc-allocation under a parent entity.

- **Case (i) IsNode(e).** No operand `t` is consumed (`e` is supplied by the node-allocation protocol, not by inc). Required: `ValidAddress(e) ∧ IsNode(e) ∧ e ∉ E ∧ n₀ ≼ e`. Both the freshness conjunct `e ∉ E` and the bootstrap-lineage conjunct `n₀ ≼ e` are discharged by NodeUniqueAllocation — the protocol-established axiom — directly. The operational allocator is Nelson's hierarchical baptism / Gregory's single global granfilade with query-and-increment dispatch, outside T10a's standard discharge layer.
- **Case (ii) ¬IsNode(e).** `e = inc(t, k)` for some operand `t` and `k ∈ {0, 1, 2}`. Required uniformly: `parent(e) ∈ E`. Per-sub-case additional requirements:
  - *k = 0 (sibling):* `t ∈ E ∧ ¬IsNode(t) ∧ parent(t) = parent(e) ∧ zeros(t) = zeros(e)`. The `¬IsNode(t)` conjunct is implied by the structural identity `zeros(t) = zeros(e)` together with the case-level `¬IsNode(e)` (which gives `zeros(e) ≥ 1`), and is required for `parent(t)` to be defined (T4b's parent projection is partial on T and undefined when `IsNode(t)`); it is stated explicitly so the operand admissibility is visible at the definition site rather than left as a consequence of partial-function evaluation.
  - *k = 1 (version):* `t ∈ E_doc`. The operand must be an allocated document — only an existing document can be versioned. Nelson's CREATENEWVERSION operates on `<doc id>`, an allocated document (LM 4/66); Gregory's `docreatenewversion` retrieves the source's vspan via `doretrievedocvspanfoo`, which fails on a source not present in the granfilade. (`IsDocument(t)` follows from `t ∈ E_doc` by the definition of E_doc.)
  - *k = 2 (descent):* `t ∈ E ∧ parent(e) = t ∧ zeros(t) ≤ 1` (equivalently, `IsNode(t) ∨ IsAccount(t)`). The operand-level constraint follows from the case-level precondition `¬IsElement(e)` (`zeros(e) ≤ 2`) combined with the consequence `zeros(e) = zeros(t) + 1` recorded below; stated explicitly here so the operand admissibility is visible at the definition site rather than left as a derivation.
  - Structural identities (consequences of TA5 + T4b's parent projection on `e = inc(t, k)`, not independent preconditions): `zeros(e) = zeros(t)` for k ∈ {0, 1} (TA5(c) preserves zeros for k = 0; TA5(d) at k = 1 appends a final 1 with no new zero, so zeros is preserved); `zeros(e) = zeros(t) + 1` for k = 2 (TA5(d) at k = 2 appends one zero separator and a final 1); `parent(e) = parent(t)` for k ∈ {0, 1} (k = 0 leaves the trailing-component position unchanged, k = 1 extends by one non-zero component without crossing a zero separator, so T4b's truncation past the last separator yields the same prefix); `parent(e) = t` for k = 2 (k = 2 introduces a new zero separator immediately after t, making t itself the parent prefix under T4b).

*Freshness discharge.* The `e ∉ E` precondition is discharged by case on the K.δ form: case (i) is closed by NodeUniqueAllocation (the node-allocation protocol's axiomatic uniqueness clause); case (ii) is closed by T10a's GlobalUniqueness on the parent allocator's tracked domain. Every K.δ case (ii) event has its operand `t ∈ E` (sub-cases k = 0 and k = 2 require this directly; sub-case k = 1 requires `t ∈ E_doc ⊆ E`), placed there by a prior K.δ event whose allocator chain is T10a-tracked from activation onward.

*Effect on M, per case.* When IsDocument(e): M'(e) = ∅ (empty arrangement), and M'(d') = M(d') for every d' ≠ e. When IsAccount(e) or IsNode(e): M'(d') = M(d') for every d' (by the totality convention M(e) = ∅ for e ∉ E_doc). The collective effect on M is therefore `(A d' : d' ≠ e : M'(d') = M(d'))` ∧ `M'(e) = ∅`.

Nelson identifies two document-creation modes — ex nihilo and forking. At the elementary level, both begin with K.δ producing an empty document. When the source's content subspace is non-empty, forking is compound: K.δ followed by arrangement extension and provenance recording (J4 below). When the source's content subspace is empty, fork reduces to K.δ alone.

*Frame:* C' = C; L' = L; R' = R; M is per-case (above). The IsDocument case's `M'(e) = ∅` matches `M(e)` in value by the totality convention but enters e into E_doc, changing M's typing.

**K.μ⁺ (Arrangement extension).** New V→I mappings are added to some d ∈ E_doc, with existing mappings unchanged:

`dom(M'(d)) ⊃ dom(M(d)) ∧ (A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))`

Extension is pure addition — the domain grows, and no existing value is altered. Without the value-preservation clause, K.μ⁺ could silently replace values at existing positions, conflating extension with replacement. The decomposition of replacement into K.μ⁻ followed by K.μ⁺ depends on each being a pure operation.

The two conjuncts together force new mappings at positions disjoint from dom(M(d)). For any v ∈ dom(M'(d)) \ dom(M(d)), v is a new position by construction. For any v ∈ dom(M(d)), the value-preservation clause pins M'(d)(v) = M(d)(v), so that position cannot be the site of a "new" mapping carrying a different value. Hence dom(M'(d)) \ dom(M(d)) — the set of newly-mapped positions — is exactly the set of positions disjoint from dom(M(d)) that K.μ⁺ adds. The K.μ~ decomposition (replacement as K.μ⁻ then K.μ⁺) relies on this disjointness: the K.μ⁻ step empties the affected positions from dom, and the subsequent K.μ⁺ step adds mappings at positions that — having been removed — are now disjoint from the intermediate domain.

*Precondition:* `d ∈ E_doc`; for every new mapping M'(d)(v) = a, `a ∈ dom(C)` (S3, ASN-0036 — since K.μ⁺'s frame holds C' = C, referential integrity reduces to membership in the pre-state content store); new V-positions satisfy S8a (all components strictly positive), and the resulting arrangement M'(d) satisfies S8-depth (uniform depth within each subspace); dom(M'(d)) is finite (S8-fin); the resulting arrangement satisfies D-CTG (contiguity within each subspace, ASN-0036) and D-MIN (minimum position in each non-empty subspace, ASN-0036). Functionality (S2) is preserved: dom(M'(d)) ⊃ dom(M(d)) with value preservation at existing positions means new entries are assigned at positions outside dom(M(d)), so M'(d) remains a function — extending a partial function at disjoint domain elements cannot introduce ambiguity.

In a composite transition, K.α may precede K.μ⁺, extending dom(C) before K.μ⁺ executes. At that intermediate state the freshly allocated address is already in the content store, satisfying the precondition. From the composite perspective, the I-address in a new mapping falls into one of two cases:

(i) Freshly allocated — co-occurring K.α places a into dom(C) before K.μ⁺ maps to it. Nelson: "new content enters Istream permanently."

(ii) Previously existing — a ∈ dom(C) at the composite's initial state. This is transclusion: "the copy shares I-addresses with the source. No new content is created in Istream."

*Frame:* C' = C; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R.

**K.μ⁻ (Arrangement contraction).** Existing V→I mappings are removed from some d ∈ E_doc, with surviving mappings unchanged:

`dom(M'(d)) ⊂ dom(M(d)) ∧ (A v : v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v))`

*Precondition:*
- `d ∈ E_doc`.
- `dom(M(d)) ≠ ∅` — the pre-state arrangement must be non-empty (the strict-subset clause `dom(M'(d)) ⊂ dom(M(d))` has no witness when `dom(M(d)) = ∅`).
- The contracted arrangement `M'(d)` must satisfy the per-state arrangement invariants S2, S3 (extended later to S3★), S8a, S8-depth, S8-fin, D-CTG (extended later to D-CTG★), and D-MIN (extended later to D-MIN★).

Contraction preserves S2, S3 (since C' = C), S8a, S8-depth, and S8-fin by restriction of M(d). Under D-CTG / D-MIN, valid contractions are restricted to suffix-removal patterns on the lex-sequential range of the arrangement.

The per-subspace refinement of K.μ⁻'s contraction pattern in the extended state — including the explicit suffix shape, the strict-contraction clause, and the K.μ⁻ exhaustiveness lemma partitioning per-subspace contractions into cases (a) suffix removal, (b) interior hole, (c) minimum hole — is given in the K.μ⁻ amendment paragraph in *Amendments to existing transitions* below, once D-CTG★ / D-MIN★ / D-SEQ★ have been introduced. The value-preservation clause additionally pins K.μ⁻ as removal-only, ruling out modification of surviving values.

*Frame:* C' = C; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d')).

**K.ρ (Provenance recording).** A document-content association enters R:

`R' = R ∪ {(a, d)}` where `a ∈ dom(C) ∧ d ∈ E_doc`

*Precondition:* `a ∈ dom(C)` ∧ `d ∈ E_doc`. The level constraint IsElement(a) follows from S7b (every a ∈ dom(C) satisfies IsElement(a)).

*Frame:* C' = C; E' = E; (A d :: M'(d) = M(d)).

The seven elementary kinds — K.α, K.δ, K.λ (introduced later under *Link allocation*), K.μ⁺, K.μ⁺_L (introduced later under *Link-subspace extension*), K.μ⁻, K.ρ — plus the named composite K.μ~ are *structurally sufficient* for the *catalogued* modification modes of this ASN, enumerated per component as follows. (i) *Existential components C, L, E and historical component R* admit only extension (P3): the elementary set covers each via K.α, K.λ, K.δ, K.ρ respectively, with no contraction or value rewriting on any of them. (ii) *Presentational component M* admits three modes — *extension* (K.μ⁺ for content-subspace, K.μ⁺_L for link-subspace), *contraction* (K.μ⁻, with per-subspace suffix-removal patterns spelled out in K.μ⁻'s definition and exhaustiveness lemma), and *bijection-preserving reordering* (K.μ~, the named composite of K.μ⁻ + K.μ⁺ with subspace preservation and link-subspace fixity). (iii) *Replacement* — changing which I-address a V-position maps to — is the named compound K.μ⁻ + K.μ⁺ (decomposition below): K.μ⁻ removes a suffix of `V_S(d)` ending at the replaced position, K.μ⁺ re-adds the suffix with the new value installed and any displaced positions carrying their previously mapped values. When the new value is freshly allocated content, the full composite extends to K.α + K.μ⁻ + K.μ⁺ + K.ρ. See *Worked example: interior content replacement* for the concrete trace; the formal decomposition is stated in *Decomposition of K.μ~* below (interior replacement is the same shape with `n'_S = k₀ − 1` rather than `n'_S = 0`).

K.μ~ — *arrangement reordering* — is a named composite of K.μ⁻ + K.μ⁺ (analogous to J4), not a primitive transition. Its bijection equation, admissibility constraints, and derived frame are stated in §*Decomposition of K.μ~* below.

We observe that neither split nor merge appears as an elementary transition. Nelson addresses this explicitly: the effect of splitting a document is achieved by creating two new documents and transcluding different portions of the original into each. Merging is creating a new document and transcluding from multiple sources. Both compose from K.δ, K.μ⁺, and K.ρ — the elementary transitions suffice.


## Amendments to existing transitions

**K.α amendment (ContentSubspaceRestriction).** In the extended state, K.α is amended with a content-subspace restriction: the allocated address must satisfy `subspace_I(a) = s_C`. This parallels K.λ's `subspace_I(ℓ) = s_L` and is required by L0 clause 2 — without it, K.α could allocate an address with subspace s_L, placing it in dom(C') and violating the partition. The amendment also preserves L14: since `subspace_I(a) = s_C` and `s_C ≠ s_L` (SC-NEQ), the address `a` cannot appear in dom(L) — L0 clause 1 at the pre-state ensures all dom(L) addresses have subspace s_L — so `dom(C') ∩ dom(L') = ∅`.

**K.μ⁺ amendment (ContentSubspaceRestriction).** K.μ⁺ is amended with a content-subspace restriction: new V-positions must satisfy `subspace(v) = s_C`. This complements K.μ⁺_L (defined below), which handles link-subspace extensions exclusively. The restriction is necessary — without it, K.μ⁺ could create a link-subspace V-position mapping to dom(C), violating S3★. With this amendment, the two transitions partition arrangement extensions by subspace. The existing D-CTG and D-MIN postconditions carry forward, now complemented by K.μ⁺_L's parallel contiguity and minimum-position preconditions in the link subspace.

**K.μ⁻ amendment (PerSubspaceScope).** In the extended state, K.μ⁻'s D-CTG / D-MIN postconditions read as D-CTG★ / D-MIN★ (per-subspace forms introduced immediately below) and the admissible removal pattern applies *per-subspace* under the D-SEQ★ enumeration `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}`. The full per-subspace precondition is:

  (1) *Per-subspace suffix pattern.* For each subspace `S ∈ {s_C, s_L}` with `V_S(d) ≠ ∅`, there exists `0 ≤ n'_S ≤ n_S` such that the post-state subspace satisfies `V_S(d') = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}` — partial suffix removal when `1 ≤ n'_S < n_S`, full clearance when `n'_S = 0`, no change when `n'_S = n_S`. The per-subspace patterns are independent across `s_C` and `s_L`.

  (2) *Strict contraction (delivers the whole-arrangement effect clause `dom(M'(d)) ⊂ dom(M(d))`).* `(E S ∈ {s_C, s_L} : V_S(d) ≠ ∅ : n'_S < n_S)` — at least one subspace shrinks strictly. The per-subspace patterns of (1) supply `V_S(d') ⊆ V_S(d)` for each S, and this strict-contraction conjunct supplies at least one strict inclusion `V_S(d') ⊊ V_S(d)`, so `dom(M'(d)) = V_{s_C}(d') ∪ V_{s_L}(d')` is a proper subset of `dom(M(d))`.

**Exhaustiveness lemma (K.μ⁻ per-subspace partition).** Fix a subspace S with D-SEQ★-shaped pre-state `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` and post-state `V_S(d') ⊆ V_S(d)`. Let `K := {k : [S, 1, ..., 1, k] ∈ V_S(d)} = {1, ..., n_S}` and `K' := {k : [S, 1, ..., 1, k] ∈ V_S(d')} ⊆ K`. Exactly one of (a), (b), (c) holds for the per-subspace contraction `K → K'`:

- (a) *Suffix removal.* `K' = {1, ..., n'_S}` for some `0 ≤ n'_S ≤ n_S` (full-clearance when n'_S = 0; no-change when n'_S = n_S).
- (b) *Hole at an interior index.* There exist `k_lo < k_hi` in K' with some `k₀ ∈ K \ K'` satisfying `k_lo < k₀ < k_hi`.
- (c) *Hole at the minimum.* `K'` is contiguous, `1 ∈ K \ K'`, and `K' ≠ ∅` (the minimum is removed and the surviving indices form a contiguous block strictly above it; subspace is not fully cleared). The contiguity clause is what disambiguates routing: any post-state with both a missing minimum and an interior hole falls into (b), not (c).

*Proof of partition.* If `K' = ∅`, then (a) holds with n'_S = 0. Otherwise let `k_min := min K'` and `k_max := max K'`; both exist because K' is non-empty and finite. The remaining configuration splits on whether K' is contiguous over `[k_min, k_max]`:

- *K' contiguous over `[k_min, k_max]`.* Then `K' = {k : k_min ≤ k ≤ k_max}`. If `k_min = 1`, `K' = {1, ..., k_max}` is a downward-closed initial segment — (a) with `n'_S = k_max`. If `k_min ≥ 2`, then `1 ∈ K \ K'` (since `1 ∈ K = {1, ..., n_S}` whenever K is non-empty and `1 < k_min`), `K' ≠ ∅`, and the contiguity clause of (c) is satisfied — (c).
- *K' not contiguous over `[k_min, k_max]`.* Then some `k₀` satisfies `k_min < k₀ < k_max` with `k₀ ∉ K'`; since `k₀ ∈ (k_min, k_max) ⊆ [1, n_S] = K`, we have `k₀ ∈ K \ K'`. Witness (b) at `k_lo := k_min`, `k_hi := k_max`. This branch absorbs every non-contiguous K' regardless of whether the minimum is present (`1 ∈ K'`) or absent (`1 ∉ K'`): in either configuration the routing is via (b)'s interior hole at `k₀`, not via (c) — (c)'s contiguity clause excludes any K' carrying an interior hole.

Mutual exclusion and exhaustiveness follow by construction of the case-analysis tree above. ∎

Only case (a) is admissible under D-CTG★ / D-MIN★: (b) violates D-CTG★ (interior `[S, 1, ..., 1, k₀]` lex-between two surviving members but absent from V_S(d')); (c) violates D-MIN★ (`min(V_S(d'))` not at `[S, 1, ..., 1, 1]`).

**L14a amendment.** In the extended state, S3★ + CL-OWN supersede ASN-0043's L14a.

**D-CTG★ / D-MIN★.** ASN-0036's D-CTG and D-MIN have a link-subspace exemption accommodating Nelson's tombstoning design (LM 4/9). This ASN introduces strengthened forms D-CTG★ and D-MIN★ that apply uniformly across both subspaces:

  **D-CTG★ (per-subspace contiguity).** `(A d, S : V_S(d) ≠ ∅ : V_S(d) is contiguous under the V-ordering on subspace S)`, where *contiguous* unpacks as closed-interval membership: for every `v_lo, v_hi ∈ V_S(d)` and every depth-m_S positive tuple `z` with subspace identifier S and `v_lo ≤ z ≤ v_hi` under the V-ordering, `z ∈ V_S(d)` — with `m_S` fixed by S8-depth (ASN-0036) and "positive tuple" denoting the S8a-compatible domain (components in ℕ⁺), so the closed-interval form is well-defined whenever S8-depth and S8a hold at the state under consideration. The closed-interval formulation is what D-CTG★ unpacks to in the derivations below — appeals to D-CTG★ discharge to "every depth-m_S positive tuple lex-between two named members of V_S(d) is itself in V_S(d)" without further unpacking.

  **D-MIN★ (per-subspace minimum position).** `(A d, S : V_S(d) ≠ ∅ : min(V_S(d)) = [S, 1, ..., 1] of depth m_S)`

All subsequent references to D-CTG and D-MIN in this ASN denote the amended (per-subspace) forms D-CTG★ and D-MIN★ — including the K.μ⁺, K.μ⁻, K.μ⁺_L, and K.μ~ postconditions and the per-subspace arrangement invariants below.

  **V-ordering on subspace S (definition).** The *V-ordering on subspace S* is the restriction of T1 (LexicographicOrder, ASN-0034) to the depth-m_S positive-component tuples whose first component is S — equivalently, the standard lexicographic order on ℕ⁺-valued tuples of length m_S, scoped to the slice with `v_1 = S`. (The depth m_S is the common depth of V_S(d) under S8-depth on each non-empty subspace; on an empty subspace the V-ordering's domain is empty, consistent with the vacuous form of the per-subspace clauses at empty subspaces.)

**S8★ (per-subspace span decomposition).** ASN-0036's S8 (SpanDecomposition) is stated for the full arrangement under S3 (single content store target). In the extended state, S3 fails on the unprojected M(d) because link-subspace V-positions target dom(L) rather than dom(C), so ASN-0036's S8 cannot be applied to M(d) directly. S8★ states the corresponding decomposition per-subspace:

For each `d ∈ E_doc` and each subspace `S ∈ {s_C, s_L}`, the per-subspace arrangement `M(d)|_{V_S(d)}` decomposes into a finite set of correspondence runs `{(v_j, a_j, n_j)}` satisfying ASN-0036's S8 conditions (a) and (b) applied to the projected arrangement: every `v ∈ V_S(d)` lies in exactly one run, and within each run the V-positions and I-addresses advance by shift in lockstep. The decomposition is established by direct application of ASN-0036's S8 to the per-subspace projection — `M(d)|_{V_{s_C}(d)} : V_{s_C}(d) → dom(C)` discharges S3's content clause (since S3★ restricted to V_{s_C}(d) is exactly S3, and S2/S8a/S8-depth/S8-fin are elementary-preserved); `M(d)|_{V_{s_L}(d)} : V_{s_L}(d) → dom(L)` discharges S3-style range containment in dom(L) via S3★'s link clause. The trivial length-1 decomposition `{(v, M(d)(v), 1) : v ∈ V_S(d)}` suffices for S8★'s existence postcondition on either projection; richer decompositions arise naturally for arrangements built via shift-aligned K.μ⁺/K.μ⁺_L sequences.

S8★ substitutes for ASN-0036's S8 in ExtendedReachableStateInvariants, applied per-subspace to each projection. The S8 conjunct of ExtendedReachableStateInvariants is the conjunction of S8★(s_C) and S8★(s_L), each of which is established by direct application of the corresponding projection-restricted form.

**D-SEQ★ (per-subspace sequential positions, derived).** For each non-empty subspace S in M(d):

  `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` for some `n_S ≥ 1`,

where the inner positions are of uniform depth m_S (the common depth within subspace S, by S8-depth), and `n_S = |V_S(d)|`.

D-SEQ★ is re-established in full detail here from the amended D-CTG★ + D-MIN★ + S8-depth + S8-fin + S8a. The derivation is a single-state implication consuming the per-state invariants on its left and producing the per-state shape on its right; it is reusable at every reachable state without re-invoking the outer induction.

*Derivation.* Fix d and a non-empty subspace S, and abbreviate `m := m_S`, `n := n_S`. By D-MIN★, V_S(d) contains the minimum position `v_min = [S, 1, ..., 1]` of depth m. By S8-depth, every v ∈ V_S(d) has #v = m. By S8a, every component of every v ∈ V_S(d) is strictly positive (in ℕ⁺). By S8-fin, V_S(d) is finite; let n := |V_S(d)|. The V-ordering on a fixed subspace at a fixed depth is the standard lexicographic order on ℕ⁺-valued tuples; we show that under this ordering, D-CTG★ + S8-fin force every element of V_S(d) into the all-1-inner form `[S, 1, ..., 1, k]`.

*Step 1: inner positions are fixed at 1.* We show that every v ∈ V_S(d) satisfies `v_j = 1` for `2 ≤ j ≤ m - 1` (when m = 2 there are no inner positions and the claim is vacuous).

*Base case (m = 2).* The inner-position range `2 ≤ j ≤ m - 1 = 1` is empty, so the inner-positions-fixed claim is vacuously satisfied. Every v ∈ V_S(d) has the form `[S, v_2]` with v_1 = S (by definition of V_S(d), which projects M(d) onto positions with subspace(v) = S = v_1) and v_2 ∈ ℕ⁺ (from S8a); Step 2 below then directly identifies V_S(d) with `{[S, k] : 1 ≤ k ≤ n_S}`, the m = 2 specialisation of D-SEQ★.

*Inductive case (m ≥ 3).* The argument below addresses this case. The inner range `2 ≤ j ≤ m - 1` is non-empty (containing at least j = 2 = m - 1 when m = 3, the smallest case where the u_M construction places M at the terminal position j + 1 = m, with the trailing range j + 2..m empty as noted). Suppose for contradiction that some v ∈ V_S(d) has v_j ≥ 2 at the *minimal* inner position j with `2 ≤ j ≤ m - 1`. By minimality, `v_l = 1` for `2 ≤ l < j`; combined with v_1 = S, v agrees with v_min on positions 1..j - 1, and `v_j > v_min[j] = 1`, so `v_min < v` in lex order. For each integer `M ≥ 2`, define the depth-m tuple
  `u_M := [S, 1, ..., 1, 1, M, 1, ..., 1]`
with `S` at position 1, `1` at every position from 2 through j, `M` at position j + 1, and `1` at every remaining position from j + 2 through m. (When j = m - 1, the trailing range j + 2..m is empty; the tuple becomes `[S, 1, ..., 1, 1, M]` with M at the terminal — the construction's placement of M coincides with the terminal position whenever the minimal inner position is the rightmost-but-one.) Each u_M has all positive components, so it inhabits the V-ordering's domain at depth m.

We verify `v_min < u_M < v` for each M ≥ 2:
  - `v_min < u_M`: v_min and u_M agree on positions 1..j (both have `S` at 1 and `1` everywhere through position j); they first differ at position j + 1, where `v_min[j+1] = 1 < M = u_M[j+1]`.
  - `u_M < v`: u_M and v agree on positions 1..j - 1 (both have `S` at 1 and `1` at positions 2..j - 1); they first differ at position j, where `u_M[j] = 1 < v_j` (since v_j ≥ 2 by hypothesis).
Each u_M is a depth-m positive tuple with subspace identifier S satisfying `v_min < u_M < v`, so by D-CTG★'s closed-interval membership (v_min, v ∈ V_S(d) bracket a closed interval), u_M ∈ V_S(d). The map `M ↦ u_M` is injective (u_M and u_{M'} disagree at position j+1 whenever M ≠ M'), so `{u_M : M ≥ 2}` is a countably infinite subset of V_S(d). This contradicts S8-fin's finiteness of `dom(M(d))`, discharging the hypothesis that some `v ∈ V_S(d)` has an inner position ≥ 2.

Therefore no v ∈ V_S(d) has an inner position ≥ 2: every v has `v_j = 1` for `2 ≤ j ≤ m - 1`, and the only remaining freedom is in the terminal position v_m. So every v ∈ V_S(d) has the form `[S, 1, ..., 1, k]` for some `k ∈ ℕ⁺`.

*Step 2: terminal contiguity.* Restricted to terminal-varying tuples `[S, 1, ..., 1, k]`, the V-ordering coincides with the natural order on `k`. By S8-fin, n < ∞; let `v_max = max(V_S(d)) = [S, 1, ..., 1, k_max]` for some k_max ∈ ℕ⁺ (well-defined since V_S(d) is finite and non-empty). By D-CTG★'s closed-interval-membership content, every depth-m positive tuple z with subspace identifier S satisfying `v_min ≤ z ≤ v_max` is in V_S(d) (v_min and v_max are both in V_S(d), bracketing a closed interval admissible to the D-CTG★ premise); restricted to terminal-varying tuples `[S, 1, ..., 1, k]`, this gives `{[S, 1, ..., 1, k] : 1 ≤ k ≤ k_max} ⊆ V_S(d)`. The reverse inclusion follows from v_max being the maximum: any `[S, 1, ..., 1, k]` with `k > k_max` would exceed v_max in lex order. Hence `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ k_max}`, and counting gives `k_max = n`.

The infinite-cardinality contradiction in Step 1 supplies, for an arbitrary subspace S, the per-subspace analogue of the D-CTG-depth property that ASN-0036 states specifically for the text subspace V_1(d). Here it is derived directly from D-CTG★ + S8-fin + S8a, so D-SEQ★ does not require a separate D-CTG-depth axiom for non-text subspaces. ∎

The discharge of J4 (Fork) under the amended K.μ⁺ is given in *Coupling and isolation* below alongside J4's definition.


## Allocator hierarchy under documents

The content- and link-subspace allocators are organized as sibling element-field sub-allocators rooted at each document. We formalise the sub-allocator structure under each document — anchors, frontier discipline, and emission ordering.

For each `d ∈ E_doc`, the document-level address `d` (zeros = 2) is the root of d's allocator subtree. Two element-field bases sit immediately under d:

- `b_C(d) := [d.0.s_C]` (single-component element field with E₁ = s_C; zeros = 3, #E = 1) — the **content sub-allocator anchor**.
- `b_L(d) := [d.0.s_L]` (single-component element field with E₁ = s_L; zeros = 3, #E = 1) — the **link sub-allocator anchor**.

These anchors are structurally producible via T10a inc steps from `d`. Under SubspaceConventionAxiom (defined at the head of the *Link store and extended system state* section, fixing `s_C = 1` and `s_L = 2`), `b_C(d) = inc(d, 2) = [d.0.1]` (TA5(d) with k = 2), and `b_L(d) = inc(b_C(d), 0) = inc([d.0.1], 0) = [d.0.2]` (TA5(c)): the rightmost nonzero component of `b_C(d)` is `s_C = 1` and incrementing yields `s_L = 2`. The anchors are not themselves in `dom(C) ∪ dom(L)` — content addresses have `#E ≥ 2` (S7c), link addresses have `#E ≥ 2` (L1b), and the anchors have `#E = 1` — so they inhabit the foundation carrier set `T` but no state component of Σ.

**Definition (Sub-allocator names).** For each `d ∈ E_doc`, three T10a sub-allocators are associated with d:

- `A_C(d)` — d's **content sub-allocator**, with anchor `b_C(d) = [d.0.s_C]`. Its outputs `a` satisfy `a ∈ dom(C)`, `subspace_I(a) = s_C`, `origin(a) = d`, and `zeros(a) = 3` (element-level).
- `A_L(d)` — d's **link sub-allocator**, with anchor `b_L(d) = [d.0.s_L]`. Its outputs `ℓ` satisfy `ℓ ∈ dom(L)`, `subspace_I(ℓ) = s_L`, `origin(ℓ) = d`, and `zeros(ℓ) = 3` (element-level).
- `A_v(d)` — d's **version sub-allocator**, with no element-field anchor (it emits at the entity-hierarchy level, not the element-field level). Its outputs are k = 1 children of d under T10a's discipline: the first emission is `inc(d, 1)` (a new IsDocument tumbler with `zeros = 2`), and subsequent emissions chain as k = 0 siblings on the same frontier. Activation requires d's spawning point to inhabit d's parent allocator's tracked domain at the K.δ event (T10a's T2 spawnPt premise); this is satisfied whenever `d ∈ E_doc`, which K.δ k = 1's precondition `t ∈ E_doc` requires of the version-creation operand.

Outputs of `A_C(d)` and `A_L(d)` are *not* entity-level (their outputs inhabit `dom(C) ∪ dom(L)` at `zeros = 3`); outputs of `A_v(d)` *are* entity-level (they enter `E_doc` at `zeros = 2`). All three are T10a-conforming sub-allocators within d's allocator subtree.

Once each element-field anchor heads a frontier (not derivable from T10a alone — admitted as SubAllocatorAxiom below), the sub-allocator behaves as a T10a-conforming `inc(·, 0)` chain: the first content address under d is `[d.0.s_C.1]`, subsequent siblings advance by `inc([d.0.s_C.k], 0)` (TA5(c)); the first link address is `[d.0.s_L.1]`, subsequent siblings by `inc(ℓ_prev, 0)`. The two frontiers advance independently — each inc step operates locally under its subspace prefix.

**SubAllocatorAxiom (Axiom, ContentLinkSubAllocatorExistence).** For each `d ∈ E_doc`, the entity-allocation event placing d into E_doc activates a content sub-allocator `A_C(d)` with anchor `b_C(d) = [d.0.s_C]` and a link sub-allocator `A_L(d)` with anchor `b_L(d) = [d.0.s_L]`. The axiom comprises three sub-clauses:

- **SubAllocatorAxiom.Subspace.** Outputs of the two sub-allocators inhabit `s_C` and `s_L` respectively: every `a` emitted by `A_C(d)` has `subspace_I(a) = s_C`, every `ℓ` emitted by `A_L(d)` has `subspace_I(ℓ) = s_L`.
- **SubAllocatorAxiom.FirstEmission.** The first emission of each is the determinate tumbler `[d.0.s_C.1]` (resp. `[d.0.s_L.1]`), satisfying `a ∉ dom(Σ.C) ∪ dom(Σ.L)` at the state of allocation with `origin(a) = d` and `#E(a) = 2`.
- **SubAllocatorAxiom.Namespace.** Every output of d's sub-allocators is T4-valid with `zeros(·) = 3`. The first emission `[d.0.s_C.1]` (resp. `[d.0.s_L.1]`) is T4-valid by construction: the document `d` is T4-valid with `zeros(d) = 2` (every `d ∈ E_doc` is T4-valid by P1's preservation of K.δ's T4-validity precondition), and appending one zero separator and the two-component element field `[s_C, 1]` (resp. `[s_L, 1]`) — both `s_C ≥ 1` and `s_L ≥ 1` by SubspaceConventionAxiom — yields a T4-valid tumbler with `zeros = 3`; subsequent `inc(·, 0)` emissions preserve T4-validity by TA5a (ASN-0034).

*T10a.6 (DomainDisjointness) non-violation.* The activation cannot be derived from T10a's T2 spawning rule because `b_C(d), b_L(d)` inhabit no predecessor's tracked domain. Disjointness between `A_C(d)`'s and `A_L(d)`'s outputs is structural — `subspace_I(b_C(d)) = s_C ≠ s_L = subspace_I(b_L(d))` (SubspaceConventionAxiom + T7) — not derived from T10a.6's domain-tracking argument.

**Lemma (Cross-document disjointness chain).** *Derivation chain: T10a.{2,5} → T10.*

*Statement.* For any two distinct entities `e₁, e₂` with `e₁ ≠ e₂` of the same allocator-hierarchy level (both with `zeros(eᵢ) = z` for some fixed `z`), and for any T10a-conforming sub-allocator with prefix `[e₁.0.s]` and `[e₂.0.s]` for some component `s ≥ 1`, the prefixes `p₁ := [e₁.0.s]` and `p₂ := [e₂.0.s]` satisfy `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`. By T10 (PartitionIndependence, ASN-0034), every address extending `p₁` differs from every address extending `p₂`. The statement instantiates at the document level with `e₁ = d₁, e₂ = d₂ ∈ E_doc` and `s ∈ {s_C, s_L}` (yielding anchors `b_C(d), b_L(d)`), and at the account level with `e₁ = A₁, e₂ = A₂ ∈ E_account` (where the sub-allocator under each account is the account's document sub-allocator, with first emission `inc(A, 2) = [A.0.1]`).

*Proof.* Case-split on the prefix relationship between `e₁` and `e₂`, which is exhaustive: every distinct pair is either prefix-comparable or prefix-incomparable.

*Case A — Prefix-comparable* (WLOG `e₁ ≺ e₂`, so `#e₁ < #e₂`). Both entities satisfy `zeros = z` (their common level by T4). Since e₂'s first `#e₁` positions reproduce e₁ exactly — including all of e₁'s zero separators — the remaining positions `#e₁+1, ..., #e₂` of e₂ carry no zeros, so `e₂[#e₁+1] ≠ 0`. The prefix `p₁ = [e₁.0.s]` places its own zero separator at position `#e₁+1` (`p₁[#e₁+1] = 0`), while `p₂[#e₁+1] = e₂[#e₁+1] ≠ 0`. Position-divergence at index `#e₁+1 ≤ min(#p₁, #p₂)` witnesses `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` by Prefix.

*Case B — Prefix-incomparable* (`e₁ ⋠ e₂ ∧ e₂ ⋠ e₁`). The hypothesis supplies a divergence position `k ≤ min(#e₁, #e₂)` with `e₁[k] ≠ e₂[k]`. Since each prefix `pᵢ = [eᵢ.0.s]` agrees with `eᵢ` on positions `1..#eᵢ`, `p₁[k] = e₁[k] ≠ e₂[k] = p₂[k]`, witnessing prefix-incomparability by Prefix.

T10 (PartitionIndependence) then closes the lemma in both cases: every `a` extending `p₁` differs from every `b` extending `p₂`. ∎

Downstream sites cite this lemma as **CrossDocDisjoint** (or "the Cross-document disjointness chain lemma"). Note that the lemma is stated for any sub-allocator prefix of the form `[e.0.s]` with `e` an entity and `s ≥ 1`. At the document level this includes the content and link anchors `b_C(d) = [d.0.s_C]` and `b_L(d) = [d.0.s_L]`; at the account level the document sub-allocator's first emission `inc(A, 2) = [A.0.1]` is a similar prefix (the difference between minted-direct and minted-via-anchor is in the activation discharge, not in the cross-entity disjointness analysis).

Cross-subspace collisions are further prevented by L14 (StoreDisjointness), itself derived from L0 and SC-NEQ via T7 (SubspaceDisjointness, ASN-0034): every content address has `subspace_I(a) = s_C`, every link address has `subspace_I(ℓ) = s_L`, and `s_C ≠ s_L`, so no allocation in one subspace can produce an address inhabiting the other.


## Link allocation

**K.λ (LinkAllocation).** Creates a new entry in the link store.

*Precondition:*
- d ∈ E_doc  (home document exists)
- ℓ ∉ dom(L) ∪ dom(C)  (fresh address — L14)
- zeros(ℓ) = 3 ∧ subspace_I(ℓ) = s_L  (element-level, link subspace — L0, L1)
- #E(ℓ) ≥ 2  (link element field has at least two components — L1b, ASN-0043; established by the inc(t, 1) descent in the first-link case and preserved by the inc(t, 0) sibling step in subsequent cases)
- origin(ℓ) = d  (scoped to home document — L1a)
- ℓ is produced by d's link sub-allocator. The first-emission and subsequent-emission cases have structurally distinct discharge routes and must be stated separately; SubAllocatorAxiom.FirstEmission does not commit "every emission" outside `dom(L) ∪ dom(C)`, only the first.
  - *First emission* (predicate: `{ℓ' ∈ dom(L) : origin(ℓ') = d} = ∅`): `ℓ = [d.0.s_L.1]`, the determinate first emission of A_L(d). Freshness against `dom(L) ∪ dom(C)` is pinned by SubAllocatorAxiom.FirstEmission directly — that clause alone commits the first emission outside both stores.
  - *Subsequent emission* (predicate: `{ℓ' ∈ dom(L) : origin(ℓ') = d} ≠ ∅`): `ℓ = inc(max{ℓ' ∈ dom(L) : origin(ℓ') = d}, 0)` (TA5(c)), the next sibling on A_L(d)'s inc chain. Freshness against `dom(L)` is discharged by T10a's GlobalUniqueness on the A_L(d) inc chain; freshness against `dom(C)` is discharged by SC-NEQ + T7 (and equivalently by L14 at the pre-state).
- `(A ℓ' : ℓ' ∈ dom(L) ∧ origin(ℓ') = d : ℓ' < ℓ)`  (forward allocation — T9; consequence of inc(·, 0) on the frontier in the subsequent case, and of the first-emit position [d.0.s_L.1] being greater than any pre-existing d-scoped link in the first-link case, where the antecedent is vacuous)
- (F, G, Θ) ∈ Link ∧ Θ ≠ ∅  (well-formed link value with mandatory non-empty type endset — L3)

*Effect:* `L' = L ∪ {ℓ ↦ (F, G, Θ)}`

*Frame:* `C' = C; E' = E; (A d' :: M'(d') = M(d')); R' = R`

Cross-document disjointness is supplied by the Cross-document disjointness chain lemma (T10a.{2,5} → T10) above, applied with `p₁ := b_L(d)` and `p₂ := b_L(d')`.


## K.δ case (ii) discharge and parent-allocator activation

Each non-node K.δ event closes its `e ∉ E` freshness obligation by interpreting the step as a T10a transition on the parent's entity-level sub-allocator. The discharge applies uniformly across k ∈ {0, 1, 2}, but the parent-allocator regime differs by k:

- *k = 0 (sibling under existing allocator):* operand `t ∈ E` already inhabits the parent's tracked domain by K.δ's `parent(t) = parent(e)` precondition; the step `e = inc(t, 0)` is a T10a T1 sibling-increment on the activated parent allocator. T10a GlobalUniqueness on the inc-chain delivers `e ∉ E` directly.

- *k = 1 (version under existing document allocator):* operand `t ∈ E_doc` was placed in E_doc by a prior K.δ event whose effect activated t's version sub-allocator `A_v(t)` (per the Sub-allocator-names definition's clause: "Activation requires t's spawning point to inhabit t's parent allocator's tracked domain at the K.δ event"). The step `e = inc(t, 1)` is a T10a T1 sibling-increment (after the first version) or T2 spawn step (for the first version) on `A_v(t)`. T10a GlobalUniqueness delivers `e ∉ E`.

- *k = 2 (descent producing the first child under a node or account):* this is the activation case, and care is required to identify *which* allocator is being spawned and *which* allocator is its parent in T10a's allocator tree. We name the participants explicitly. Let `t` be the K.δ operand (a node when creating an account; an account when creating a document) and `e = inc(t, 2)` the spawn output. The K.δ event itself spawns a *new entity-level sub-allocator* under `t` — call it `A_↓(t)`: when t is a node, `A_↓(t)` is "t's account sub-allocator" emitting account-level children of t; when t is an account, `A_↓(t)` is "t's document sub-allocator" emitting document-level children of t. The K.δ event is the T10a T2 spawn step that *creates* `A_↓(t)`, with `t` as spawnPt and `e` as the first emission.

  T10a T2 admissibility requires the spawnPt `t` to inhabit `dom(parent_allocator(A_↓(t)))` at the spawn event — i.e., t must already lie in the tracked domain of whatever allocator sits *above* the newly-spawned `A_↓(t)` in the allocator tree. The parent allocator above `A_↓(t)` is identified by `t`'s own provenance: it is precisely the allocator that minted `t`. When t is a node, that minting allocator is the *node-allocation registry* (Nelson's hierarchical baptism / Gregory's granfilade; see NodeUniqueAllocation above), which we model as an external T10a-conforming allocator whose tracked domain contains every baptised node — so `n₀ ≼ t` (NodeLineage) places `t` in that domain by construction, and NodeUniqueAllocation's freshness clause `t ∉ E` at the prior K.δ event for `t` itself is the T10a discipline that placed `t` there. When t is an account, the minting allocator is `A_↓(parent(t))` — the account sub-allocator under t's node — which was itself activated by an earlier K.δ event of this same k = 2 form; `t ∈ dom(A_↓(parent(t)))` follows from that earlier event by induction.

  In either case the same K.δ precondition `t = parent(e) ∈ E` discharges the T2 spawnPt requirement: every entity in E has been baptised by a prior K.δ event, and that prior K.δ placed t into the tracked domain of t's minting allocator (which is precisely the parent allocator of `A_↓(t)`). The spawn step's `k' = 2 ∈ {1, 2}` is admissible by T10a; K.δ's case-level zeros bound `zeros(t) ≤ 1` discharges T10a's zero-count side condition (T10a admits k' = 2 when `zeros(spawnPt) ≤ 2`, satisfied a fortiori). T10a GlobalUniqueness on the parent allocator's tracked domain — now extended to include `e` as `A_↓(t)`'s first emission — then delivers `e ∉ E`.

In all three K.δ case (ii) sub-cases, the row's "parent allocator's tracked domain" denotes the parent allocator at the moment of the K.δ event — which is either pre-activated (k = 0; k = 1 after first version) or activated by the K.δ event itself (k = 2; first k = 1 emission), with the parent allocator named explicitly above for each sub-case. T10a GlobalUniqueness then closes the freshness obligation directly.


## Generalized referential integrity

**S3★ (GeneralizedReferentialIntegrity).** The arrangement maps V-positions to addresses in the store appropriate to their subspace:

  `(A d, v : v ∈ dom(Σ.M(d)) : (subspace(v) = s_C ⟹ Σ.M(d)(v) ∈ dom(Σ.C)) ∧ (subspace(v) = s_L ⟹ Σ.M(d)(v) ∈ dom(Σ.L)))`

where `subspace(v)` denotes the first component of the V-position. S3★ supersedes S3 (ASN-0036) for the extended state Σ = (C, L, E, M, R): S3 requires every V-position to map into dom(C), which is violated by link-subspace mappings targeting dom(L). S3 remains valid when restricted to states with no link-subspace mappings — the four-component model of the prior sections has only content-subspace V-positions, for which S3★ reduces to S3.

Existing transitions preserve S3★: K.α, K.δ, K.ρ hold M in frame; K.μ⁺ creates only content-subspace V-positions (by its amended precondition `subspace(v) = s_C`), so new mappings target dom(C) and the link-subspace clause is unaffected; K.μ⁻ contracts dom(M(d)), preserving both clauses; K.μ~ is a distinguished composite K.μ⁻ + K.μ⁺ (per its definition above) with a bijection `π : dom(M(d)) → dom(M'(d))` satisfying `M'(d)(π(v)) = M(d)(v)`. K.μ~ preserves S3★ by direct decomposition: K.μ⁻ restricts dom(M(d)) with values unchanged — content-subspace mappings still target dom(C), link-subspace mappings still target dom(L) — so S3★ holds for the intermediate state; K.μ⁺ (amended) adds only content-subspace V-positions targeting dom(C) by precondition, preserving existing mappings by frame — S3★ holds for M'(d). The stronger derived property — that link-subspace mappings under K.μ~ are pointwise fixed — is established in *Decomposition of K.μ~* below.

**S3★-aux (SubspaceExhaustiveness).** In every reachable state, all V-positions have subspace s_C or s_L:

  `(A d, v : v ∈ dom(M(d)) : subspace(v) = s_C ∨ subspace(v) = s_L)`

*Proof.* By induction on transition sequences from Σ₀. Base: M₀ = ∅, the property holds vacuously. Step: K.μ⁺ (amended) creates only s_C positions; K.μ⁺_L creates only s_L positions; K.μ⁻ removes positions without altering subspaces of survivors; K.μ~ decomposes into K.μ⁻ + K.μ⁺, each maintaining the property independently of fixity; K.α, K.δ, K.λ, K.ρ hold M in frame. ∎


## Link-subspace extension

**LinkVPositionDepthAxiom (Axiom, FixedLinkVPositionDepth).** `(A d ∈ E_doc :: m_L = 2)` — every link-subspace V-position has depth 2. The lower bound `m_L ≥ 2` is structural (ordinal shift at depth 1 alters the subspace identifier, violating TA7a); LinkVPositionDepthAxiom instantiates it at 2.

**K.μ⁺_L (LinkSubspaceExtension).** Extends a document's arrangement in the link subspace.

*Precondition:*
- d ∈ E_doc
- ℓ ∈ dom(L)  (the target link must already exist in dom(L) — placed there by some prior K.λ)
- origin(ℓ) = d  (only home-document links may be arranged)
- ℓ ∉ ran(M(d))  (the link is not already arranged at any V-position in d's arrangement — first-arrangement constraint). This guarantees CL-UNIQ at the post-state: were `ℓ ∈ ran(M(d))` already, there would exist some `v' ∈ dom(M(d))` with `M(d)(v') = ℓ`, and adding `(v_ℓ, ℓ)` with `v_ℓ ∉ dom(M(d))` (verified below) would produce two distinct V-positions both mapping to `ℓ`, violating CL-UNIQ. Combined with CL-OWN (which restricts the link-subspace range of M(d) to links with `origin(·) = d`), the freshness condition `ℓ ∉ ran(M(d))` is equivalent — under the precondition `origin(ℓ) = d` — to `ℓ ∉ ran(M(d)|_{dom_L})`: a link can appear in M(d)'s range only as the value of a link-subspace V-position (by S3★, since `ℓ ∈ dom(L)` and `dom(L) ∩ dom(C) = ∅` by L14), so the unrestricted `ℓ ∉ ran(M(d))` clause suffices.
- V-position v_ℓ satisfies:
  - subspace(v_ℓ) = s_L
  - m_L = 2, supplied by **LinkVPositionDepthAxiom** (FixedLinkVPositionDepth, stated above at the head of this section). When V_{s_L}(d) ≠ ∅, m_L = 2 is consistent with S8-depth on existing link-subspace positions; when V_{s_L}(d) = ∅, S8-depth is vacuous and the axiom supplies the depth directly.
  - If V_{s_L}(d) = ∅: v_ℓ is the minimum position `[s_L, 1, ..., 1]` of depth m_L (D-MIN)
  - If V_{s_L}(d) ≠ ∅: v_ℓ = shift(max(V_{s_L}(d)), 1), extending the contiguous range (D-CTG). OrdShiftHom (ASN-0036, clauses (b) and (c)) and OrdAddS8a (ASN-0036) are subspace-parametric in v₁, so they apply to v_ℓ at v₁ = s_L exactly as at v₁ = s_C; they jointly supply subspace(v_ℓ) = s_L, S8a preservation, and S8-depth preservation.
  - #v_ℓ = m_L (S8-depth within the link subspace)

*Effect:* `M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}`

*Frame:* `C' = C; L' = L; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R`

We verify `v_ℓ ∉ dom(M(d))`, as required for M'(d) to be a proper extension preserving S2 (ArrangementFunctionality). When `V_{s_L}(d) = ∅`: no link-subspace V-position exists in dom(M(d)), and `subspace(v_ℓ) = s_L`, so `v_ℓ ∉ dom(M(d))`. When `V_{s_L}(d) ≠ ∅`: `v_ℓ = shift(max(V_{s_L}(d)), 1) > max(V_{s_L}(d))` by TS4 (ShiftStrictIncrease, ASN-0034), placing v_ℓ beyond all existing link-subspace positions. In both cases, `subspace(v_ℓ) = s_L` and `s_L ≠ s_C` (SC-NEQ) ensures no collision with text-subspace positions (T3, CanonicalRepresentation, ASN-0034: tumblers are extensionally identified by their component sequence, so two tumblers differing in their first component are distinct). T7 (FirstElementFieldDistinction, ASN-0034) does not apply at V-positions because T7's hypothesis is element-level (zeros = 3) while V-positions have zeros = 0; the structural fact required here — that distinct first components yield distinct tumblers — is supplied by T3, which holds at every depth. Therefore `v_ℓ ∉ dom(M(d))`.

The preconditions ensure that after the extension, D-CTG (contiguity), D-MIN (minimum position), and S8-depth (uniform depth) hold for the link subspace of d. S3★ is satisfied: `subspace(v_ℓ) = s_L` and `M'(d)(v_ℓ) = ℓ ∈ dom(L')`.

The origin restriction `origin(ℓ) = d` distinguishes link-subspace extension from content-subspace extension, where K.μ⁺ intentionally permits `origin(a) ≠ d` — that is content transclusion, an established architectural feature. Link transclusion — arranging a foreign-origin link in a document's link subspace — is excluded by design. Nelson: "A document includes only the links of which it is the home document" (LM 4/31). The byte stream admits transclusion ("The virtual byte stream of a document may include bytes from any other document," LM 4/10); links do not. Links maintain "permanent order of arrival" in their home document, and home document determines ownership ("A link need not point anywhere in its home document. Its home document indicates who owns it," LM 4/12). Arranging a link with `origin(ℓ) ≠ d` would place an out-link in a document that does not own it — violating the ownership semantics that home-document identity is meant to carry. The architecture provides alternatives: bidirectional link search discovers all links attached to transcluded content regardless of which document houses them; creating a new link in one's own document is the natural analog of annotation. Gregory confirms that the implementation achieves origin matching by procedural atomicity — `docreatelink` both allocates the link ISA under the document's address and places it in the document's arrangement in a single operation — but no runtime guard exists; `acceptablevsa` unconditionally returns TRUE and `docopy` performs no origin check. The origin restriction in K.μ⁺_L formalizes the structural guarantee that the implementation achieves by construction.


## Link-subspace ownership

**CL-OWN (LinkSubspaceOwnership).** In every reachable state:

  `(A d, v : v ∈ dom(M(d)) ∧ subspace(v) = s_L : origin(M(d)(v)) = d)`

Every document's link-subspace arrangement contains only its own links. K.μ⁺_L's precondition `origin(ℓ) = d` ensures ownership at creation; link-subspace fixity under K.μ~ ensures preservation through reordering. Proved as part of ExtendedReachableStateInvariants below.

**CL-UNIQ (LinkSubspacePositionUniqueness).** Within each document's link-subspace arrangement, each link occupies exactly one V-position — the restriction of M(d) to dom_L is injective:

  `(A d, v₁, v₂ : v₁ ∈ dom(M(d)) ∧ v₂ ∈ dom(M(d)) ∧ subspace(v₁) = s_L ∧ subspace(v₂) = s_L ∧ M(d)(v₁) = M(d)(v₂) : v₁ = v₂)`

Equivalently, `M(d)|_{dom_L}` is a partial injection from V-positions to link addresses. Proved as part of ExtendedReachableStateInvariants below.


## Decomposition of K.μ~

For `d ∈ E_doc`, K.μ~ realises the *bijection equation*:

  `(E π : π is a bijection dom(M(d)) → dom(M'(d)) : (A v ∈ dom(M(d)) :: M'(d)(π(v)) = M(d)(v)))`

π is admissible iff (i) every `π(v)` satisfies S8a, (ii) the induced post-state `M'(d)` would satisfy S8-depth, D-CTG★, D-MIN★, and S3★, and (iii) `π ≠ id`. Clause (iii) makes K.μ~ a real reordering: a permutation whose net effect is the identity is not a K.μ~ transition (the system simply does not change). Subspace preservation — `(A v ∈ dom(M(d)) :: subspace(π(v)) = subspace(v))` — follows from S3★(Σ') + L14 + the bijection equation: were π to map a content-subspace v to s_L, the post-state would have `M'(d)(π(v)) ∈ dom(C) ∩ dom(L) = ∅`, contradicting L14; the link-subspace case is symmetric.

*Frame (derived).* C' = C; E' = E; R' = R; L' = L; (A d' : d' ≠ d : M'(d') = M(d')) — by composition of K.μ⁻ and K.μ⁺ frames.

**K.μ~-FIX (Domain fixity).** `dom(M'(d)) = dom(M(d))`. D-SEQ★ at the pre- and post-states gives `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` and `V_S(d') = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}` for each subspace S; since π is a bijection and (by subspace preservation) bijects V_S(d) onto V_S(d'), `n'_S = n_S` and `V_S(d') = V_S(d)`. So π is a permutation of dom(M(d)).

**Link-subspace fixity.** `π(v) = v` for every `v ∈ dom_L(M(d))`. Proof:

(1) *Subspace-preserving bijection preserves per-subspace cardinality.* π is a bijection `dom(M(d)) → dom(M'(d))` (from the bijection equation) with `(A v ∈ dom(M(d)) :: subspace(π(v)) = subspace(v))` (subspace preservation). The restriction `π|_{dom_L(M(d))}` therefore maps dom_L(M(d)) bijectively into dom_L(M'(d)); symmetrically, `π⁻¹|_{dom_L(M'(d))}` maps dom_L(M'(d)) bijectively into dom_L(M(d)). Bijection between subsets of a finite set forces equal cardinality: `|dom_L(M'(d))| = |dom_L(M(d))|`. Combined with K.μ~-FIX's per-subspace decomposition (n'_S = n_S for every S), this gives `dom_L(M'(d)) = dom_L(M(d))` as sets.

(2) *K.μ⁻'s removal set lies in dom_C.* K.μ⁺ (amended) cannot create link-subspace V-positions, so any link-subspace V-position present in dom_L(M'(d)) must have been present in dom_L(M(d)) — the K.μ⁻ + K.μ⁺ pipeline through K.μ~'s decomposition cannot introduce new link-subspace positions. Combined with the cardinality equality from (1), K.μ⁻'s removal set X = dom(M(d)) \ dom(M_int(d)) must satisfy `X ∩ dom_L(M(d)) = ∅` — every removed position is content-subspace. (Were a link-subspace position removed by K.μ⁻, the subsequent K.μ⁺ could not restore it, leaving `|dom_L(M'(d))| < |dom_L(M(d))|` and contradicting (1).)

(3) *Pointwise preservation on dom_L.* For each `v ∈ dom_L(M(d))`: v survives K.μ⁻ (by (2), X ∩ dom_L = ∅), so `v ∈ dom(M_int(d))` and K.μ⁻'s value-preservation clause gives `M_int(d)(v) = M(d)(v) = ℓ`. K.μ⁺ then frames existing positions: `v ∈ dom(M_int(d)) ⊆ dom(M'(d))` and `M'(d)(v) = M_int(d)(v) = ℓ`. Therefore `M'(d)|_{dom_L} = M(d)|_{dom_L}` as functions.

(4) *Identity via CL-UNIQ at the pre-state.* From (3), `M'(d)|_{dom_L} = M(d)|_{dom_L}`, so for the V-position `v ∈ dom_L(M(d))` under consideration, `M(d)(v) = ℓ`. Subspace preservation places `π(v) ∈ dom_L(M(d))` (using (1)'s cardinality equality `dom_L(M'(d)) = dom_L(M(d))`), and the bijection equation gives `M(d)(π(v)) = M'(d)(π(v)) = M(d)(v) = ℓ` (the first equality by (3) applied at `π(v) ∈ dom_L`). Both `v` and `π(v)` are link-subspace V-positions in `dom(M(d))` mapping to the same link `ℓ`. CL-UNIQ at Σ — the inductive hypothesis, link-subspace injectivity of `M(d)|_{dom_L}` — forces `π(v) = v`. ∎

**Decomposition.** Admissibility clause (iii) requires `π ≠ id`, which (combined with link-subspace fixity, which forces π = id when `dom_C(M(d)) = ∅`) in turn requires `dom_C(M(d)) ≠ ∅`. K.μ~ is realised as *any* valid K.μ⁻ + K.μ⁺ pair on `V_{s_C}(d)` whose net effect achieves the bijection equation for π, subject to K.μ⁻'s admissibility (per-subspace suffix removal under D-CTG★/D-MIN★) and K.μ⁺'s preconditions at the intermediate state. The cardinality of the K.μ⁻ removal — equivalently, the choice of `n'_{s_C} ∈ {0, 1, ..., n_{s_C} − 1}` — depends on which content-subspace positions π actually moves:

- If π's action on `V_{s_C}(d)` affects only a suffix `{[s_C, 1, ..., 1, k] : k₀ ≤ k ≤ n_{s_C}}` for some `k₀ ≥ 1`, then a *partial-suffix expansion* at `n'_{s_C} = k₀ − 1` suffices: K.μ⁻ removes only the affected suffix, K.μ⁺ rebuilds it with π applied. Positions below `k₀`, where π acts as identity, pass through unchanged.
- The maximum case is *full content-subspace clearance and rebuild*: at `n'_{s_C} = 0`, K.μ⁻ removes V_{s_C}(d) entirely (case-(a) maximal-suffix removal, with link-subspace retained) and K.μ⁺ then adds `{π(v) ↦ M(d)(v) : v ∈ V_{s_C}(d)}` in one step. This expansion works for *every* admissible π — it is the universal default and the form referenced in the K.μ~ verification arguments below.

We refer to the full-clearance form as the *canonical* expansion in the sense of universal applicability, not exclusivity: every partial-suffix expansion that matches π's action is equally valid, and a non-identity permutation that fixes the suffix above some `k₀` admits the partial-suffix form as well. K.μ⁻ must retain link-subspace mappings under every expansion — K.μ⁺ (amended) is content-only and K.μ⁺_L only places at the contiguous min or max, so any removed link-subspace position could not be restored.

*Intermediate-state admissibility.* At Σ_int (post-K.μ⁻, pre-K.μ⁺): C_int = C, M_int(d) = M(d) ↾ V_{s_L}(d). K.μ⁺'s preconditions at Σ_int discharge: `d ∈ E_doc` (frame); referential integrity from `M(d)(v) ∈ dom(C)` for `v ∈ V_{s_C}(d)` at pre-state; content-subspace restriction from K.μ~'s subspace-preserving precondition; S8a/S8-depth/S8-fin/D-CTG★/D-MIN★ on M'(d) from K.μ~'s postcondition. S2 holds because π is a bijection.

Since K.μ~ preserves ran(M(d)), ran(M'(d)) \ ran(M(d)) is empty, and the J1 coupling has no new containment pairs to record.


## Coupling and isolation

The elementary transitions do not all occur independently. Some must co-occur to maintain invariants (coupling); some must leave other components unchanged (isolation). The weakest-precondition calculus makes the coupling constraints visible.

A clarification on scope. The frame conditions stated above describe individual elementary transitions: K.μ⁺ alone does not modify R, K.α alone does not modify M, and so on. Coupling constraints describe required co-occurrence — when K.μ⁺ occurs, K.ρ must also occur in the same composite transition.

**Definition (Current containment).** The *current containment* of state Σ is the set of all document-content pairs where the content is presently in the document's arrangement:

`Contains(Σ) = {(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))}`

This is a derived quantity of the state — it captures what each document currently displays. We will need it both in the valid composite definition (as a state invariant) and in the coupling derivations that follow.

**Definition (Valid composite transition).** A composite transition Σ → Σ' is *valid* iff it is a finite sequence of elementary transitions Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ' satisfying two conditions:

(1) *Elementary preconditions:* each step Σᵢ → Σᵢ₊₁ satisfies the precondition of its elementary transition kind, evaluated at the intermediate state Σᵢ.

(2) *Coupling constraints:* J0, J1, and J1' hold for the composite — evaluated between the initial state Σ and the final state Σ'.

Intermediate states need not satisfy all system invariants; only the final state is required to. The ordering matters: J0 couples K.α with K.μ⁺, and S3 requires the I-address to exist before the V→I mapping is created, so K.α precedes K.μ⁺. Similarly, J4's fork compounds K.δ + K.μ⁺ + K.ρ, and K.μ⁺ requires d ∈ E_doc, which K.δ establishes — so K.δ precedes K.μ⁺. The net effect of a composite transition is the composition of its elementary effects.

For freshly created documents d ∈ E'_doc \ E_doc, the pre-state has d ∉ E_doc, so M(d) = ∅ by the totality of M. Consequently ran(M(d)) = ∅, and the set difference ran(M'(d)) \ ran(M(d)) reduces to ran(M'(d)): all content placed in a new document counts as newly introduced. The coupling constraints below quantify over E'_doc, not E_doc, making them applicable to freshly created documents without special cases.

**J0 (Allocation requires placement).** Content allocation K.α always co-occurs with arrangement extension K.μ⁺:

`(A Σ → Σ', a : a ∈ dom(C') \ dom(C) : (E d, v : d ∈ E'_doc ∧ v ∈ dom(M'(d)) : M'(d)(v) = a))`

Every freshly allocated I-address appears in some arrangement in the post-state — the containing document may itself have been freshly created by K.δ in the same composite transition. This is an axiom of the state transition model, not a theorem of ASN-0036. S7a tells us that the prefix of a identifies the creating document, but it does not tell us that the creating document's arrangement must contain a — an address could be allocated into dom(C) with the correct prefix while appearing in no arrangement. The justification for J0 is design intent: in Nelson's model, content enters the docuverse by being placed in a document. There is no mechanism for creating "orphan" content that exists in Istream without any document displaying it. Gregory confirms: allocation always occurs in the context of a document operation that inserts the new content.

**J1 (Extension records provenance).** Arrangement extension K.μ⁺ must co-occur with provenance recording K.ρ:

`(A Σ → Σ', d ∈ E'_doc, a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R')`

J1 does not fall out of the calculus alone; the wp computation reveals what coupling is needed *to preserve a design choice* — namely the invariant `Contains(Σ) ⊆ R` (P4 below), which declares that every current containment is recorded in R. The design choice is P4 itself: Nelson's docuverse commits to recording every document-content association into a permanent reverse index, and Gregory confirms the implementation accumulates entries "from every content addition." The wp computation then asks: given that K.μ⁺ frames R, can K.μ⁺ alone preserve P4 across `Σ → Σ'`?

Computing wp backward from `Contains(Σ') ⊆ R'`: after K.μ⁺, `Contains(Σ') ⊇ Contains(Σ)`, so new pairs appear. Since K.μ⁺ frames R (`R' = R`), evaluating `Contains(Σ') ⊆ R'` collapses the R' on the right-hand side to R:

`wp(K.μ⁺, Contains(Σ') ⊆ R') = (A a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R)`

This requires every new containment pair to already be in R — not generally true for fresh content. K.μ⁺ in isolation cannot maintain P4. Therefore, to maintain P4, K.ρ must co-occur, extending R so that the composite post-state satisfies `(A a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R')`. J1 is the coupling constraint that the design choice P4 forces upon the elementary transition set.

Gregory identifies one implementation anomaly where provenance recording is skipped for a particular command, "making content invisible to find_documents." The abstract specification treats this as a defect: the coupling is required.

For a freshly created document d ∈ E'_doc \ E_doc, M(d) = ∅ by totality, so ran(M(d)) = ∅, so ran(M'(d)) \ ran(M(d)) = ran(M'(d)): every I-address placed in a new document triggers provenance recording.

**J1' (Provenance requires extension).** Conversely, provenance recording K.ρ for (a, d) occurs only within a composite transition where K.μ⁺ introduces a into ran(M'(d)):

`(A Σ → Σ', a, d ∈ E'_doc : (a, d) ∈ R' \ R : a ∈ ran(M'(d)) \ ran(M(d)))`

J1 ensures every new containment pair is recorded; J1' ensures every new provenance entry corresponds to an actual containment event. Together they characterise new provenance entries: (a, d) ∈ R' \ R if and only if K.μ⁺ introduces a into ran(M'(d)) and (a, d) ∉ R. When (a, d) ∈ R already — from a prior insertion-deletion cycle — K.μ⁺ re-introducing a into d's arrangement requires no new K.ρ, because J1's requirement (a, d) ∈ R' is satisfied by existing membership (P2 ensures prior entries persist). The totality of M ensures J1' is well-defined for freshly created documents: M(d) = ∅ for d ∉ E_doc gives ran(M'(d)) \ ran(M(d)) = ran(M'(d)). Gregory confirms this tight coupling — the provenance structure "accumulates entries from every content addition" and no mechanism exists to record provenance outside of content placement.

**P4a (Historical fidelity).** Every entry in R reflects an actual past *content-subspace* containment event:

`(A (a, d) ∈ R :: (E Σ_k in the transition history : (E v ∈ dom(M_k(d)) : subspace(v) = s_C ∧ M_k(d)(v) = a)))`

*Derivation (four-component state).* By induction on the transition sequence. *Base:* R₀ = ∅; the quantifier is vacuously satisfied. *Inductive step:* for (a, d) ∈ R' \ R, J1' gives a ∈ ran(M'(d)) \ ran(M(d)) — the post-state Σ' is a witnessing state where d's arrangement contains a (in the four-component state every V-position has subspace s_C, so the content-subspace qualifier is automatic). For (a, d) ∈ R, the inductive hypothesis provides a prior witnessing state; P2 ensures the entry persists in R'.

*Derivation (extended state, with J1'★).* The same induction discharges P4a in the extended state, with J1'★ replacing J1' as the coupling. *Base:* R₀ = ∅; vacuous. *Inductive step:* for `(a, d) ∈ R' \ R`, J1'★ gives that some content-subspace V-position in M'(d) maps to `a` while no content-subspace V-position in M(d) does — i.e., there exists `v ∈ dom(M'(d))` with `subspace(v) = s_C ∧ M'(d)(v) = a`. The post-state Σ' is therefore a witnessing state whose arrangement contains `a` at a content-subspace V-position, matching the strengthened P4a quantifier. For `(a, d) ∈ R`, the inductive hypothesis provides a prior content-subspace witnessing state; P2 carries the entry into R'. The content-subspace qualification is essential here: J1'★ scopes provenance recording to content-subspace range changes (link-subspace mappings target `dom(L)`, which is disjoint from `dom(C)` by L14, so no link-subspace V-position can witness provenance under P7's `a ∈ dom(C)` requirement). P4a in the extended state therefore reads as "every provenance entry corresponds to a past content-subspace arrangement," consistent with both P7's grounding in `dom(C)` and J1'★'s content-scoped coupling. ∎

**J2 (Contraction isolation).** The elementary transition K.μ⁻ requires no coupling — it is self-sufficient with respect to P0–P2, L12, and Contains(Σ) ⊆ R. As an elementary transition, K.μ⁻ satisfies:

`C' = C ∧ L' = L ∧ E' = E ∧ R' = R`

(The `L' = L` conjunct is the link-store extension contributed by the *Extended system state* paragraph above; the original J2 predated the link store and is superseded by this extended form in the extended state.) The wp analysis confirms this. For P0: K.μ⁻ does not touch C. For P1: does not touch E. For P2: does not touch R. For L12: does not touch L. For the provenance bound Contains(Σ) ⊆ R: contraction can only remove pairs from Contains, so Contains(Σ') ⊆ Contains(Σ) ⊆ R = R'. No co-occurring transition is needed to maintain any system invariant.

This is the deepest consequence of the design. Deletion is purely presentational — it changes what appears, not what exists or what has been. Gregory confirms: contraction "never triggers" provenance recording, and the provenance structure "is never pruned."

**J3 (Reordering isolation).** The named composite K.μ~ is likewise self-sufficient:

`C' = C ∧ L' = L ∧ E' = E ∧ R' = R`

(As with J2, the `L' = L` conjunct is the link-store extension contributed by the *Extended system state* paragraph; the original J3 predated the link store and is superseded by this extended form in the extended state.) Reordering preserves ran(M(d)), so Contains(Σ') = Contains(Σ). All invariants are trivially maintained; no co-occurring transition is needed.

**J4 (Fork composite).** Nelson's forking creation mode — version creation with ancestry indication (LM 4/66, CREATENEWVERSION) — is a composite whose elementary steps are exactly K.δ + K.μ⁺ + K.ρ, all serving the new document d_new. *Fork is strictly the k = 1 version-creation case:* d_new = inc(d_src, 1), a child of d_src in the address space (zeros(d_new) = 2 = zeros(d_src), parent(d_new) = parent(d_src)). The k = 0 sibling allocation under the source's account (`docreatenewdocument` in Gregory's implementation) and the k = 2 hierarchical descent are *not* forks under this definition; they are independent K.δ + K.μ⁺ + K.ρ composites without the ancestry-by-address indication. This restriction matches Nelson's specific "fork" terminology and Gregory's `docreatenewversion` (which dispatches `makehint(DOCUMENT, DOCUMENT, depth=1)` to obtain the k = 1 child address).

**Definition (Fork).** A *fork* of d_src to d_new is a composite transition Σ → Σ', with *precondition* d_src ∈ E_doc ∧ V_{s_C}(d_src) ≠ ∅, consisting of:

(i) K.δ case (ii) with k = 1 and t = d_src, producing d_new = inc(d_src, 1) with d_new ∉ E_doc,

(ii) K.μ⁺ populating M'(d_new) from d_src's content subspace under transclusion: `ran(M'(d_new)) ⊆ ran(M(d_src)|_{V_{s_C}(d_src)})` — no new content addresses are introduced, every target lies in the pre-existing content store,

(iii) K.ρ recording provenance for each a ∈ ran(M'(d_new)),

and no other elementary steps. Step (ii) must produce a content-subspace arrangement on d_new whose range is contained in d_src's content-subspace range and discharges the per-state arrangement invariants (S2, S3★, S8a, S8-depth, S8-fin, D-CTG★, D-MIN★) at the post-state.

*Discharge of arrangement-side invariants.* Step (ii)'s K.μ⁺ creates only content-subspace V-positions (by the K.μ⁺ amendment) targeting addresses in `ran(M(d_src)|_{V_{s_C}(d_src)}) ⊆ dom(C)` (by S3★'s content clause at the pre-state, which is the only S3★ clause supplying a dom(C) containment — the unrestricted `ran(M(d_src))` includes link-subspace targets in dom(L), which are excluded from dom(C) by L14); C is frame-preserved across the composite (none of K.δ, K.μ⁺, K.ρ modify C), so S3★'s content clause holds at the post-state. The link subspace `V_{s_L}(d_new)` is empty (step (ii) creates only content-subspace V-positions; step (i) initialised `M(d_new) = ∅`), so D-CTG★, D-MIN★, S8-depth, S8-fin, and S8a hold vacuously on d_new's link subspace. Step (ii)'s K.μ⁺ must establish D-CTG★, D-MIN★, S8a, S8-depth, S8-fin on `V_{s_C}(d_new)` by its postconditions — the choice of V-positions in step (ii) must be invariant-discharging, but the specific V-positions are operation-specific. By choosing V-positions contiguously from the minimum `[s_C, 1, ..., 1]`, D-CTG★ and D-MIN★ hold for the content subspace of d_new.

*Discharge of coupling constraints under the amended K.μ⁺.* J1★ is satisfied because step (ii)'s K.μ⁺ creates only content-subspace V-positions (by the amendment) and step (iii)'s K.ρ records provenance for each `a ∈ ran(M'(d_new))`, covering every content-subspace extension. J1'★ is satisfied because each new `(a, d_new) ∈ R' \ R` has `a ∈ ran(M'(d_new))` from a content-subspace extension — S3★'s content clause gives `M'(d_new)(v) ∈ dom(C)` for each such v, so `ran(M'(d_new)) ⊆ dom(C)` and P7 compatibility is maintained. Link-subspace mappings from the source document are not copied — the forked document's link subspace starts empty. This is consistent with Nelson's design: each document owns only its home links, and links from the source remain discoverable through the shared I-addresses via refractive following — "a link to one version of a Prismatic Document is a link to all versions" (Nelson). A mechanism for link inheritance under forking, if desired, would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope.

Since none of K.δ, K.μ⁺, K.ρ modify C (each has C' = C in its frame), a fork satisfies dom(C') = dom(C) — no new content is created. The provenance conclusion — that (a, d_new) ∈ R' for every a ∈ ran(M'(d_new)) — follows from J1 applied to the fresh-document case: the convention M(d_new) = ∅ gives ran(M'(d_new)) \ ran(M(d_new)) = ran(M'(d_new)), and J1 directly requires provenance recording for each such address. No additional constraint beyond J1 is needed.

The new document d_new is created empty (K.δ), its arrangement extended with mappings to the source's I-addresses (K.μ⁺, with `ran(M'(d_new)) ⊆ ran(M(d_src)|_{V_{s_C}(d_src)})`), and the new associations recorded (K.ρ). The precondition V_{s_C}(d_src) ≠ ∅ ensures K.μ⁺ is well-formed. Since K.μ⁺ (amended) creates only content-subspace V-positions, the I-addresses it maps to must lie in dom(C) (by S3★'s content clause). Only content-subspace V-positions in d_src have I-addresses in dom(C) — link-subspace V-positions map to dom(L), and dom(L) ∩ dom(C) = ∅ (L14). With V_{s_C}(d_src) ≠ ∅, there is at least one content I-address to transclude, so the strict domain extension dom(M'(d_new)) ⊃ dom(M(d_new)) = ∅ is satisfiable. The weaker condition M(d_src) ≠ ∅ is insufficient: a document with only link-subspace positions (reachable via K.δ + K.λ + K.μ⁺_L with no intervening K.μ⁺) has ran(M(d_src)) ⊆ dom(L), and no address in dom(L) can serve as the target of a content-subspace V-position. When the source's content subspace is empty — whether because M(d_src) = ∅ or because dom_C(M(d_src)) = ∅ — the fork definition does not apply; creation from such a source is ex nihilo (K.δ alone), not a fork. Nelson: "the new document's id will indicate its ancestry."

An immediate consequence of J1 and J2 is that the provenance relation diverges from current containment over time.

**P4 (Provenance bounds).** In any reachable state where J1 has been satisfied for all prior transitions:

`Contains(Σ) ⊆ R`

*Base case.* In Σ₀, (E₀)_doc = ∅ (E₀ contains only the bootstrap node), so Contains(Σ₀) = ∅ ⊆ ∅ = R₀. The bound holds vacuously.

*Inductive step.* Assume Contains(Σ) ⊆ R at a reachable state Σ, and let Σ → Σ' be a valid composite transition. Every (a, d) ∈ Contains(Σ') falls into exactly one of two cases:

(i) *Pre-existing containment:* a ∈ ran(M(d)), which requires d ∈ E_doc (since d ∈ E'_doc \ E_doc would give M(d) = ∅ by totality, contradicting a ∈ ran(M(d))). Then (a, d) ∈ Contains(Σ) ⊆ R (inductive hypothesis), and P2 gives R ⊆ R', so (a, d) ∈ R'.

(ii) *Newly introduced containment:* a ∈ ran(M'(d)) \ ran(M(d)). J1 requires (a, d) ∈ R'. (When (a, d) ∈ R already — from a prior insertion-deletion cycle — the requirement is satisfied by P2 without fresh K.ρ.)

In both cases (a, d) ∈ R', so Contains(Σ') ⊆ R'. ∎

The per-elementary analysis confirms *why* only K.μ⁺ introduces new containment and why other transitions are harmless:

- K.α: Does not modify M or R. Contains(Σ') = Contains(Σ). Preserved.
- K.δ: Creates entity e with empty arrangement M'(e) = ∅, contributing no new pairs to Contains. Preserved.
- K.μ⁺: The sole source of new containment pairs — case (ii) above. J1 couples it with K.ρ.
- K.μ⁻: Can only remove pairs from Contains — ran(M'(d)) ⊆ ran(M(d)). Preserved by monotonicity.
- K.μ~ (composite): Preserves ran(M(d)), so Contains(Σ') = Contains(Σ). Preserved.
- K.ρ: Does not modify M, so Contains(Σ') = Contains(Σ). Extends R. Preserved. (By J1', K.ρ occurs only when K.μ⁺ introduces new containment — a constraint on historical fidelity (P4a), not on the provenance bound itself.)

Every I-address currently in some arrangement is recorded in R. But the converse does not hold: (a, d) ∈ R does not imply a ∈ ran(M(d)). Stale entries persist from earlier states where d contained a before contraction removed it. These entries are not errors — they are the system's historical memory of content associations, monotonically truthful, never retracting a claim once made. Gregory: "find_documents returns historically accurate results, not current state."


## Content-scoped containment and provenance

The containment relation `Contains(Σ)` (defined earlier in this ASN) is `{(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))}` — unscoped across all subspaces. With link-subspace mappings, `Contains(Σ')` includes `(ℓ, d)` for every link ℓ mapped in d's arrangement. P4 requires `Contains(Σ) ⊆ R`, but provenance entries satisfy P7: `(A (a, d) ∈ R :: a ∈ dom(C))`. Since `ℓ ∈ dom(L)` and `dom(L) ∩ dom(C) = ∅` (L14), `(ℓ, d) ∉ R` — P4 is unsatisfiable for the unscoped relation once link-subspace mappings exist.

**Contains_C(Σ) (ContentContainment).**

  `Contains_C(Σ) = {(a, d) : d ∈ E_doc ∧ (E v : v ∈ dom(M(d)) ∧ subspace(v) = s_C : M(d)(v) = a)}`

**P4★ (ProvenanceBounds, content-subspace).**

  `Contains_C(Σ) ⊆ R`

P4★ supersedes P4 for the extended state. In pre-extension states (no link-subspace mappings), `Contains_C(Σ) = Contains(Σ)`, so P4★ reduces to P4. Existing transitions preserve P4★: K.α, K.δ, K.ρ hold M in frame; K.μ⁻ contracts dom(M(d)), which can only shrink Contains_C; K.μ~ preserves P4★ by the link-subspace fixity established in the S3★ analysis above. Since π bijects dom(M(d)) onto dom(M'(d)) and maps dom_L bijectively onto dom_L (by fixity), it maps the complement dom_C(M(d)) = dom(M(d)) \ dom_L(M(d)) bijectively onto dom_C(M'(d)) = dom(M'(d)) \ dom_L(M'(d)). These complements are exactly the content-subspace positions by S3★-aux: every V-position has subspace s_C or s_L, so `dom(M(d)) \ dom_L(M(d)) = {v ∈ dom(M(d)) : subspace(v) = s_C}`. With `M'(d)(π(v)) = M(d)(v)` for each such v, the set `{a : (E v ∈ dom_C(M(d)) : M(d)(v) = a)} = {a : (E u ∈ dom_C(M'(d)) : M'(d)(u) = a)}`, so `Contains_C(Σ') = Contains_C(Σ) ⊆ R = R'`. K.μ⁺ alone may transiently violate P4★ (it adds to Contains_C but does not extend R); restoration at the composite boundary is governed by J1★ and proved in ExtendedReachableStateInvariants.


## Scoped coupling constraints

The coupling constraints J1, J1' (defined earlier in this ASN) were formulated before link-subspace mappings existed. They must be scoped to content-subspace arrangement extensions; otherwise J1 and P7 are mutually unsatisfiable — J1 would require provenance recording for the link address ℓ entering ran(M'(d)), but P7 requires every provenance entry to reference dom(C), and ℓ ∈ dom(L) with dom(L) ∩ dom(C) = ∅ (L14).

**J1★ (ExtensionRecordsProvenance, content-subspace).**

  `(A Σ → Σ', d ∈ E'_doc, a : (E v ∈ dom(M'(d)) : subspace(v) = s_C ∧ M'(d)(v) = a) ∧ ¬(E v ∈ dom(M(d)) : subspace(v) = s_C ∧ M(d)(v) = a) : (a, d) ∈ R')`

J1★ is range-based: it triggers whenever an I-address `a` is new to the content-subspace range of M'(d), regardless of whether the V-position carrying it existed in dom(M(d)). This matches J1's range-based structure (`a ∈ ran(M'(d)) \ ran(M(d))`), scoped to the content subspace. A domain-based formulation — `v ∈ dom(M'(d)) \ dom(M(d))` — would fail for value replacement at a reused position: K.μ⁻ removing `[1,2]` followed by K.μ⁺ re-adding `[1,2] ↦ a₃` leaves the V-position in both domains, making `dom(M'(d)) \ dom(M(d))` empty at that position, while `a₃` is genuinely new to the content-subspace range and requires provenance recording.

**J1'★ (ProvenanceRequiresExtension, content-subspace).**

  `(A Σ → Σ', a, d : (a, d) ∈ R' \ R : (E v ∈ dom(M'(d)) : subspace(v) = s_C ∧ M'(d)(v) = a) ∧ ¬(E v ∈ dom(M(d)) : subspace(v) = s_C ∧ M(d)(v) = a))`

J1'★ is likewise range-based, matching J1': every new provenance entry `(a, d) ∈ R' \ R` must correspond to an I-address `a` that is new to the content-subspace range — present in the content-subspace range of M'(d) but absent from the content-subspace range of M(d).

Link-subspace extensions (K.μ⁺_L) do not trigger provenance recording: the link address ℓ enters ran(M'(d)), but no content-subspace V-position maps to ℓ — `subspace(v_ℓ) = s_L ≠ s_C` (SC-NEQ) — so ℓ is not in the content-subspace range of M'(d), and J1★ is vacuous. P7 (ProvenanceGrounding) — `(A (a, d) ∈ R :: a ∈ dom(C))` — is preserved because R is unchanged (K.μ⁺_L holds R in frame).

**ValidComposite★ (ValidComposite, amended).** A composite transition Σ → Σ' in the extended state Σ = (C, L, E, M, R) is *valid* iff it is a finite sequence of transitions `Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ'` — drawn from K.α (amended), K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻ (amended), K.μ~, and K.ρ — satisfying:

1. *Transition preconditions (intra-composite sequencing).* Each step `Σᵢ → Σᵢ₊₁` satisfies the *elementary* precondition of its transition kind, evaluated at the *intermediate* state `Σᵢ`. K.μ~ appearing in the sequence is shorthand for its K.μ⁻ + K.μ⁺ decomposition (per its definition above): admissibility clause (iii) requires `π ≠ id` (and hence `dom_C(M(d)) ≠ ∅`), so K.μ~ always expands into two consecutive elementary steps, each satisfying its own precondition at the respective intermediate state. This clause is what enforces intra-composite ordering — e.g., that K.α precedes K.μ⁺ when the latter places a freshly allocated I-address `a`, since K.μ⁺'s referential-integrity precondition `a ∈ dom(C)` would fail at the pre-K.α intermediate state otherwise. Step preconditions are *local* to the elementary transition; they say nothing about the composite's endpoints.
2. *Coupling constraints (initial-to-final).* J0, J1★, and J1'★ hold for the composite as a whole — evaluated *only* between the initial state Σ and the final state Σ'. The coupling predicates quantify over the *net* change between Σ and Σ' (e.g., `a ∈ dom(C') \ dom(C)`); they do not constrain the order or shape of intermediate steps, only that the *aggregate* effect of the composite must satisfy them. A composite that satisfies clause (1) but violates clause (2) — for instance, K.α alone without an accompanying K.μ⁺ and K.ρ — is not a valid composite even though every elementary precondition holds at every intermediate state.

This supersedes the earlier ValidComposite definition by extending the elementary transition set with K.λ and K.μ⁺_L, and replacing J1/J1' with J1★/J1'★ — scoping provenance coupling to content-subspace arrangement changes. J0 (AllocationRequiresPlacement) is unchanged — it constrains content allocation (K.α), which remains content-subspace only.

**Notation disambiguation: atomic vs. composite `Σ → Σ'`.** `Σ → Σ'` denotes the boundary of a finite sequence of elementary transitions when used in coupling/composite contexts (J0, J1, J1★, J1'★, P3, ExtendedReachableStateInvariants, ExtendedTransitionInvariants), and a single atomic step elsewhere (elementary transition specifications, SequentialTransitionAxiom).

## Orphan links and coupling flexibility

The coupling constraints do not require K.λ to be paired with K.μ⁺_L. A composite consisting of K.λ alone is valid: J0 is vacuous (no content allocated), J1★ is vacuous (no content-subspace extension), and J1'★ is vacuous (no provenance change). The result is a link in dom(L) with no placement in any document's arrangement — an *orphan link*. This is a valid system state, not an error condition. State invariants are preserved: M, C, E, R are all in K.λ's frame (unchanged), so all arrangement, content, entity, and provenance invariants hold identically. L grows by one entry: dom(L') = dom(L) ∪ {ℓ}. K.λ's preconditions guarantee L0 (ℓ has subspace s_L, and ℓ ∉ dom(C) ensures dom(L') ∩ dom(C) = ∅), L1 (zeros(ℓ) = 3), L1a (origin(ℓ) ∈ E_doc), L3 (K.λ requires (F, G, Θ) ∈ Link, so L3 is established for the new entry; L12 preserves all existing entries), L12 (existing entries unchanged: L'(ℓ') = L(ℓ') for all ℓ' ∈ dom(L)), and L14 (disjointness: ℓ ∉ dom(C), so dom(L') ∩ dom(C') = ∅). Nelson explicitly diagrams "deleted links" as a category of document content (LM 4/9): links that exist in permanent storage but are "not currently addressable, awaiting historical backtrack functions."

Link withdrawal via K.μ⁻ applied to the link subspace would in principle produce the same orphan-link state but is constrained to suffix truncations under D-CTG★ (per K.μ⁻'s case analysis).

We do not add a J0 analog for links — the orphan state is architecturally intentional, satisfying both the permanence guarantee (L12: links are immutable once created) and the owner's right to withdraw (Nelson, LM 2/29). The wp analysis above shows the *form* of this design choice: it consists of *not* asserting a link-coverage invariant, rather than asserting an "orphan-permitting" rule. The decision-point lives at the invariant set, not at the transition set.


## Destruction confinement

We now state the central structural theorem — a generalisation of S9 (ASN-0036) to the extended state.

**P3 (ArrangementMutabilityOnly).** No component other than M admits contraction or value rewriting:

  `(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ dom(L) ⊆ dom(L') ∧ E ⊆ E' ∧ R ⊆ R' ∧ (A a ∈ dom(C) :: C'(a) = C(a)) ∧ (A ℓ ∈ dom(L) :: L'(ℓ) = L(ℓ)))`

The only component that can lose information is M.

*Proof.* By case analysis on the seven elementary transitions. K.α extends dom(C) preserving existing entries, with L, E, and R in its frame. K.δ extends E, with C, L, and R in its frame. K.λ extends dom(L) preserving existing entries, with C, E, and R in its frame. K.μ⁺ (amended), K.μ⁺_L, and K.μ⁻ have C, L, E, and R in their frames. K.ρ extends R, with C, L, and E in its frame. Each preserves every conjunct. The named composite K.μ~ decomposes into K.μ⁻ followed by K.μ⁺, both of which preserve the conjuncts, so K.μ~ does as well. General composite transitions, being finite sequences of elementary ones, preserve the conjuncts by transitivity of ⊆ and equality. ∎

P3 is the synthesis of P0 ∧ L12 ∧ P1 ∧ P2 — one named per-transition predicate over `Σ → Σ'` covering every component except M. The label carries no "★" because there is no four-component predecessor to amend: P0, P1, and P2 retain their identities under both the four-component and extended states, and P3 packages them together with the link-store clause L12.

P3 makes the confinement vivid. Every destructive state change — every removal, every reordering — is confined to the presentational layer. The permanent record (what content exists, what links exist, which entities have been created, what provenance has been recorded) can only grow.


## Worked example: entity hierarchy by K.δ

We exercise the three K.δ patterns — case (i) node baptism, case (ii) k = 2 account descent, case (ii) k = 2 document descent — by building the chain `n₀ = 1 → 1.2 → 1.2.0.1 → 1.2.0.1.0.1` from Σ₀ (with E₀ = {1}).

**Step 1: K.δ case (i) — baptise node `1.2`.** Address `1.2` is supplied by the node-allocation protocol, not by inc. Preconditions: `ValidAddress(1.2)`, `IsNode(1.2)` (zeros = 0), `1.2 ∉ E₀` (discharged by NodeUniqueAllocation clause (a)), `n₀ ≼ 1.2` (`[1] ≼ [1, 2]`, discharged by NodeUniqueAllocation clause (b)). Effect: `E₁ = {1, 1.2}`, all other components frame.

**Step 2: K.δ case (ii) k = 2 — allocate account `1.2.0.1 = inc(1.2, 2)`.** TA5(d) gives `zeros = 1`, `parent = 1.2`. Preconditions: `parent(e) = 1.2 ∈ E₁`; `zeros(1.2) = 0 ≤ 2`; `1.2.0.1 ∉ E₁` discharged by T10a's GlobalUniqueness at the account sub-allocator under node `1.2` (T2-spawning at the live operand `t = 1.2`). Effect: `E₂ = E₁ ∪ {1.2.0.1}`.

**Step 3: K.δ case (ii) k = 2 — allocate document `1.2.0.1.0.1 = inc(1.2.0.1, 2)`.** TA5(d) gives `zeros = 2`, `parent = 1.2.0.1`. Preconditions analogous to Step 2; T10a's GlobalUniqueness at the document sub-allocator `A_doc(1.2.0.1)` discharges `d ∉ E₂`. Effect: `E₃ = E₂ ∪ {1.2.0.1.0.1}`, with `M₃(1.2.0.1.0.1) = ∅` and SubAllocatorAxiom activating the content and link sub-allocators (anchors `b_C(d) = [d.0.1]`, `b_L(d) = [d.0.2]`).

The zero-count progression `0 → 1 → 2` exhausts the entity stratum at the document level: a hypothetical fourth k = 2 descent would produce `zeros = 3`, which is the IsElement stratum and falls outside E.

A second K.δ case (i) attempting to re-baptise `1.2` is excluded by `e ∉ E`; a K.δ case (i) attempting to baptise a disconnected node `2.1` is excluded by `n₀ ≼ e`.


## Worked example: fork with subsequent insertion

We trace a concrete scenario to ground the abstract definitions. Let the starting state Σ₁ contain node 1, account 1.0.1, and document d₁ = 1.0.1.0.1 with two characters:

> C₁ = {1.0.1.0.1.0.1.1 ↦ 'H', 1.0.1.0.1.0.1.2 ↦ 'i'}
> E₁ = {1, 1.0.1, 1.0.1.0.1}
> M₁(d₁) = {[1,1] ↦ 1.0.1.0.1.0.1.1, [1,2] ↦ 1.0.1.0.1.0.1.2}
> R₁ = {(1.0.1.0.1.0.1.1, d₁), (1.0.1.0.1.0.1.2, d₁)}

We write a₁ = 1.0.1.0.1.0.1.1 and a₂ = 1.0.1.0.1.0.1.2 for brevity.

**Fork d₁ to d₂ = 1.0.1.0.1.1.** This is J4's compound K.δ + K.μ⁺ + K.ρ — the k = 1 version-creation case.

*K.δ:* E₂ = E₁ ∪ {1.0.1.0.1.1}. The address 1.0.1.0.1.1 = inc(1.0.1.0.1, 1) is obtained from d₁ = 1.0.1.0.1 by TA5's k = 1 child-allocation rule — a version of d₁ at the next address-space level. M₂(d₂) = ∅.

*K.μ⁺:* M₂(d₂) = {[1,1] ↦ a₁, [1,2] ↦ a₂}. The same I-addresses as d₁ — transclusion, case (ii). No new content enters C. The V-positions [1,1] and [1,2] satisfy S8a (all components strictly positive, zeros = 0) and S8-depth (uniform depth 2 within subspace s_C, matching the pre-existing arrangement of d₁); the shared first component 1 — identifying subspace s_C — is a subspace-identity fact via `subspace(v)` (ASN-0036) rather than a clause of S8-depth itself.

*K.ρ:* R₂ = R₁ ∪ {(a₁, d₂), (a₂, d₂)}.

Verification against the resulting state Σ₂:

- *J0:* No fresh content (dom(C₂) = dom(C₁)), so vacuously satisfied.
- *J1★:* ran(M₂(d₂)|_{s_C}) \ ran(M₁(d₂)|_{s_C}) = {a₁, a₂} \ ∅ = {a₁, a₂} (M₁(d₂) = ∅ since d₂ ∉ (E₁)_doc). Both (a₁, d₂) and (a₂, d₂) are in R₂. ✓
- *J1'★:* `R₂ \ R₁ = {(a₁, d₂), (a₂, d₂)}` — both are new provenance entries from the K.ρ step. For each, the address must be new to d₂'s content-subspace range: `a₁ ∈ ran(M₂(d₂)|_{s_C}) = {a₁, a₂}` and `a₁ ∉ ran(M₁(d₂)|_{s_C}) = ∅` (M₁(d₂) = ∅), and symmetrically for a₂. Both entries are anchored in content-subspace range extensions introduced by the K.μ⁺ step of this composite. ✓
- *J4:* d₂ ∈ E₂_doc \ E₁_doc, ran(M₂(d₂)) = {a₁, a₂} ⊆ ran(M₁(d₁)). ✓
- *P4★:* Contains_C(Σ₂) = {(a₁, d₁), (a₂, d₁), (a₁, d₂), (a₂, d₂)} ⊆ R₂. ✓
- *P7a:* dom(C₂) = dom(C₁) = {a₁, a₂}; both a₁ and a₂ have provenance entries (a₁, d₁), (a₂, d₁) ∈ R₁ ⊆ R₂. ✓
- *P8:* parent(d₂) = parent(1.0.1.0.1.1) = 1.0.1 ∈ E₁ ⊆ E₂ (k = 1 preserves parent(d_new) = parent(d_src), so parent(d₂) = parent(d₁) = 1.0.1). The existing non-node entity 1.0.1 (account) retains parent(1.0.1) = 1 ∈ E₂. ✓

**Insert new content into d₂.** Compound K.α + K.μ⁺ + K.ρ.

*K.α:* Allocate a₃ = 1.0.1.0.1.1.0.1.1 with C₃(a₃) = '!'. The address falls under d₂'s prefix (S7a): origin(a₃) = 1.0.1.0.1.1 = d₂. The freshness of a₃ — i.e., `a₃ ∉ dom(C₂)` — is discharged by two complementary premises. *(i) Distinctness from addresses under d₁ (cross-document).* The pre-state content store dom(C₂) = dom(C₁) = {a₁, a₂} contains only addresses with origin d₁ (≠ d₂), so the Cross-document disjointness lemma — the consequence of T10a.{2,5} → T10 applied at the namespace level, with d₁'s and d₂'s content sub-allocators occupying disjoint prefix subtrees by S7a — yields a₃ ∉ {a₁, a₂}. *(ii) First-emission discharge at d₂'s content sub-allocator.* This K.α event is the first emission of d₂'s content sub-allocator A_C(d₂) — d₂ was created at the immediately preceding K.δ step with the convention dom_s(A_C(d₂)) = ∅ at activation. SubAllocatorAxiom.FirstEmission directly supplies `[d₂.0.s_C.1] ∉ dom(Σ.C) ∪ dom(Σ.L)` at the state of allocation, discharging `a₃ ∉ dom(C₂)`; the FirstEmission clause commits *only* the first emission of the activated sub-allocator, not every output, so subsequent emissions of A_C(d₂) would discharge freshness via T10a's GlobalUniqueness on its inc chain instead. Freshness against A_C(d₂)'s own prior emissions is vacuous at the empty initial domain. The two premises together close the obligation.

*K.μ⁺:* M₃(d₂) = M₂(d₂) ∪ {[1,3] ↦ a₃}. V-position [1,3] has first component 1 and depth 2, matching [1,1] and [1,2] (S8-depth, non-vacuously: shared first component). Referential integrity: a₃ ∈ dom(C₃) (S3). ✓

*K.ρ:* R₃ = R₂ ∪ {(a₃, d₂)}.

Verification:

- *J0:* a₃ ∈ dom(C₃) \ dom(C₂), and d₂ ∈ E₃_doc with M₃(d₂)([1,3]) = a₃. ✓
- *J1★:* ran(M₃(d₂)|_{s_C}) \ ran(M₂(d₂)|_{s_C}) = {a₃}, and (a₃, d₂) ∈ R₃. ✓
- *J1'★:* `R₃ \ R₂ = {(a₃, d₂)}` — the K.ρ step adds exactly this entry. The address `a₃` is new to d₂'s content-subspace range: `a₃ ∈ ran(M₃(d₂)|_{s_C}) = {a₁, a₂, a₃}` and `a₃ ∉ ran(M₂(d₂)|_{s_C}) = {a₁, a₂}`. The new provenance is anchored in the K.μ⁺ step's content-subspace range extension. ✓
- *P4★:* Contains_C(Σ₃) adds (a₃, d₂); this pair is in R₃. ✓
- *P6:* origin(a₃) = d₂ = 1.0.1.0.1.1 ∈ E₃_doc. ✓
- *P7:* (a₃, d₂) ∈ R₃ and a₃ ∈ dom(C₃). ✓
- *P7a:* dom(C₃) = {a₁, a₂, a₃}; a₁ and a₂ retain provenance from R₂ ⊆ R₃, and a₃ has new provenance (a₃, d₂) ∈ R₃. Every a ∈ dom(C₃) has at least one provenance entry. ✓

**Delete a₃ from d₂'s arrangement (K.μ⁻).** Remove the mapping at V-position [1,3] — the maximum end of V_{s_C}(d₂), satisfying the K.μ⁻ amendment's D-CTG/D-MIN postcondition.

*K.μ⁻:* dom(M₄(d₂)) = {[1,1], [1,2]} ⊂ dom(M₃(d₂)) = {[1,1], [1,2], [1,3]}. The surviving mappings are unchanged: M₄(d₂)([1,1]) = a₁, M₄(d₂)([1,2]) = a₂. D-MIN: min(V_1(d₂)) = [1,1] = [s_C, 1]. D-CTG: {[1,1], [1,2]} is contiguous.

Verification:

- *J2:* C₄ = C₃; E₄ = E₃; R₄ = R₃. All permanent and historical state unchanged. ✓
- *J1'★ (vacuous):* `R₄ \ R₃ = ∅` since K.μ⁻ holds R in frame. There are no new provenance entries to check; J1'★ is vacuously satisfied. ✓
- *P4★:* Contains_C(Σ₄) = {(a₁, d₁), (a₂, d₁), (a₁, d₂), (a₂, d₂)}. The pair (a₃, d₂) is no longer in Contains_C — d₂ no longer displays a₃. Yet (a₃, d₂) ∈ R₄: the stale entry persists. Contains_C(Σ₄) ⊂ Contains_C(Σ₃), while R₄ = R₃. ✓
- *P7a:* dom(C₄) = dom(C₃) and R₄ = R₃ (frame); every a ∈ dom(C₄) retains its provenance entry from R₃. ✓

The divergence is now concrete: R₄ records that d₂ once contained a₃, while the current arrangement does not. This is the historical memory that J2 preserves — deletion is purely presentational.

**Reorder d₂'s arrangement (K.μ~).** Swap V-positions [1,1] and [1,2].

*K.μ~:* The bijection π : {[1,1], [1,2]} → {[1,1], [1,2]} with π([1,1]) = [1,2] and π([1,2]) = [1,1]. The definition requires M₅(d₂)(π(v)) = M₄(d₂)(v) for all v ∈ dom(M₄(d₂)), giving M₅(d₂) = {[1,1] ↦ a₂, [1,2] ↦ a₁}. Both target V-positions satisfy S8a (all components strictly positive) and S8-depth (uniform depth 2, shared first component 1).

Verification:

- *J3:* C₅ = C₄; E₅ = E₄; R₅ = R₄. All permanent and historical state unchanged. ✓
- *J1'★ (vacuous):* `R₅ \ R₄ = ∅` since K.μ~ holds R in frame. There are no new provenance entries to check; J1'★ is vacuously satisfied. ✓
- *ran preservation:* ran(M₅(d₂)) = {a₁, a₂} = ran(M₄(d₂)). The multiset of referenced I-addresses is identical; only V-positions changed. ✓
- *P4★:* Contains_C(Σ₅) = Contains_C(Σ₄) ⊆ R₄ = R₅. Since ran is preserved for d₂ and no other arrangement changed, the current containment set is unchanged. ✓
- *P7a:* dom(C₅) = dom(C₄) and R₅ = R₄ (frame); every a ∈ dom(C₅) retains its provenance entry. ✓

Reordering is the simplest transition to verify: it touches nothing beyond the V-position mapping, and all invariants hold by the frame conditions alone.


## Worked example: interior content replacement

We trace the interior-position case of the content-replacement decomposition (K.μ⁻ + K.μ⁺ with `n'_{s_C} = k₀ − 1` rather than the single-position pair at `k₀ = n_{s_C}`) introduced in the *Elementary transitions* section.

*Initial state.* Let document `d = 1.0.1.0.1` have four content-subspace mappings, with `aₖ := 1.0.1.0.1.0.1.k` for `k ∈ {1, 2, 3, 4}`:

> C ⊇ {a₁ ↦ char₁, a₂ ↦ char₂, a₃ ↦ char₃, a₄ ↦ char₄}
> M(d) = {[1,1] ↦ a₁, [1,2] ↦ a₂, [1,3] ↦ a₃, [1,4] ↦ a₄}
> R ⊇ {(a₁, d), (a₂, d), (a₃, d), (a₄, d)}

Content-subspace V-positions: `V_{s_C}(d) = {[1,1], [1,2], [1,3], [1,4]}` — contiguous (D-CTG★), minimum `[1,1] = [s_C, 1]` (D-MIN★), uniform depth 2 (S8-depth), structural form `{[s_C, k] : 1 ≤ k ≤ 4}` (D-SEQ★ at `n_{s_C} = 4`, `m_{s_C} = 2`; the general D-SEQ★ form `{[s_C, 1, ..., 1, k]}` has no intermediate 1s since the inner range from position 2 to position `m_{s_C} − 1 = 1` is empty). Link subspace: `V_{s_L}(d) = ∅`. The four pre-state provenance entries are assumed established by prior J0/J1★ couplings at d's initial population (the details are not material here).

**Goal.** Replace the I-address at the interior V-position `[1,2]` with a freshly allocated `a₂' ≠ a₂` of new content value. Positions `[1,3]` and `[1,4]` lie strictly above `[1,2]` under the V-ordering on `s_C` (T1 of ASN-0034 restricted to depth-2 positive tuples with first component 1), so a single-position K.μ⁻ + K.μ⁺ pair at `[1,2]` alone would leave `V_{s_C}(d)` with a gap at `[1,2]` between `[1,1]` and `[1,3]` at the intermediate state — case (b) of the K.μ⁻ admissibility analysis, forbidden by D-CTG★. The replacement therefore decomposes as a multi-position K.μ⁻ removing the suffix from `[1,2]` upward, followed by K.α allocating `a₂'`, then a multi-position K.μ⁺ rebuilding the suffix with `a₂'` at `[1,2]` and the previously-mapped `a₃, a₄` at `[1,3], [1,4]`, and finally K.ρ recording the new provenance — four elementary steps in this order. (An alternative valid ordering, K.α before K.μ⁻, produces the same composite endpoints; the order chosen here keeps the K.μ⁻ removal at the head of the trace, matching the narrative of "interior replacement = remove suffix, then rebuild.")

**Step 1: K.μ⁻ — remove the interior suffix `{[1,2], [1,3], [1,4]}`.** Effect: `M_int(d) = {[1,1] ↦ a₁}`. Frame: `C_int = C`, `L_int = L`, `E_int = E`, `R_int = R`.

*Admissibility (per-subspace).*
- *Content subspace.* `V_{s_C}(d) = {[1,1], [1,2], [1,3], [1,4]}` shrinks to `V_{s_C}(d_int) = {[1,1]}` — case-(a) partial suffix removal with `n'_{s_C} = 1`; the removed set `{[s_C, k] : 1 < k ≤ 4}` is exactly the n'_{s_C} = 1 suffix in the D-SEQ★-shaped pre-state.
- *Link subspace.* `V_{s_L}(d) = V_{s_L}(d_int) = ∅` — vacuous (case-(a) zero-suffix at `n'_{s_L} = n_{s_L} = 0`).

At least one subspace contracts strictly (content: 4 → 1), so the effect clause `dom(M_int(d)) ⊂ dom(M(d))` is satisfied at the whole-arrangement level. K.μ⁻ commits.

*Intermediate-state verification at M_int.* Two classes of invariant must be distinguished. The *elementary per-state* invariants (D-CTG★, D-MIN★, D-SEQ★, S2, S3★, S8a, S8-depth, S8-fin, P6, P7, P8, and others enumerated in ExtendedReachableStateInvariants Class (a)) hold at every intermediate state — including M_int — by elementary preservation, since K.μ⁻'s postconditions discharge them. The *composite-boundary* invariants (P4★, P4a, P7a — Class (b)) need *not* hold at M_int as a precondition: ValidComposite★ scopes the J0/J1★/J1'★ couplings (and hence Class (b)'s discharge) between Σ and Σ', not at each intermediate state. We verify the Class (a) invariants at M_int below; P4★ at M_int is a *consequence* of K.μ⁻'s contractive action on Contains_C, not a requirement we must establish to take the step.

- *D-CTG★ at M_int:* `V_{s_C}(d_int) = {[1,1]}` is a singleton — vacuously contiguous under the V-ordering on `s_C` (no two distinct members bracket an interval). ✓
- *D-MIN★ at M_int:* `min(V_{s_C}(d_int)) = [1,1] = [s_C, 1]` of depth `m_{s_C} = 2`. ✓
- *D-SEQ★ at M_int:* `V_{s_C}(d_int) = {[s_C, 1]}` matches `{[s_C, k] : 1 ≤ k ≤ 1}` at `n_{s_C} = 1` (`m_{s_C} = 2`, so the general form has zero intermediate 1s). ✓
- *S2, S3★, S8a, S8-depth, S8-fin at M_int:* the surviving mapping `[1,1] ↦ a₁` is functional, has all-positive components and uniform depth 2 in `s_C`, with `a₁ ∈ dom(C_int) = dom(C)`. ✓
- *Per-state invariants at M_int:* P6/P7/P8 preserved by K.μ⁻'s frame on C, E, R. ✓
- *P4★ at M_int (consequence, not requirement).* `Contains_C(M_int) = {(a₁, d)} ⊆ Contains_C(Σ) ⊆ R = R_int`. P4★ happens to hold at M_int as an incidental consequence of K.μ⁻'s monotonicity: K.μ⁻ can only shrink Contains_C (its frame on the V-position domain is contractive) and R is unchanged (J2). The pairs `(a₂, d), (a₃, d), (a₄, d)` exit Contains_C at this step but remain in R as stale entries. P4★ at M_int is not load-bearing — ValidComposite★ does not require it; the next intermediate state M_post (after K.μ⁺ but before K.ρ) genuinely violates P4★ at the pair `(a₂', d)`, and restoration to Class (b) compliance occurs only after the trailing K.ρ. The check is recorded here for clarity, not because the composite would fail if it did not hold.

**Step 2: K.α — allocate the replacement address `a₂'`.** Allocate `a₂' = 1.0.1.0.1.0.1.5 = inc(a₄, 0)` (the next sibling on d's content sub-allocator's frontier under TA5(c)) with `C'(a₂') = char₂'` for some new content value. Effect: `C' = C ∪ {a₂' ↦ char₂'}`. Frame: L, E, M (= M_int), R unchanged.

Preconditions: IsElement(a₂') (zeros = 3, element-field `[1, 5]`); origin(a₂') = `1.0.1.0.1` = d ∈ E_doc; `subspace_I(a₂') = 1 = s_C`; `a₂' ∉ dom(C)` by GlobalUniqueness (T10a) on the content sub-allocator's inc chain; `a₂' ∉ dom(L) = ∅` vacuously. ✓

**Step 3: K.μ⁺ — rebuild the suffix `{[1,2] ↦ a₂', [1,3] ↦ a₃, [1,4] ↦ a₄}`.** Effect: `M_post(d) = {[1,1] ↦ a₁, [1,2] ↦ a₂', [1,3] ↦ a₃, [1,4] ↦ a₄}`. Frame: C', L, E, R unchanged.

Preconditions at the post-K.α intermediate state:
- *d ∈ E_doc; disjoint extension; value preservation.* New positions `{[1,2], [1,3], [1,4]}` are disjoint from `dom(M_int(d)) = {[1,1]}`; the existing mapping at `[1,1]` retains its value `a₁`. ✓
- *K.μ⁺ amendment (content-subspace restriction).* Each new V-position has `subspace(v) = s_C` — first components of `[1,2], [1,3], [1,4]` are all `1 = s_C`. ✓ The amendment scopes the rebuild to the content subspace; on a state with a non-empty link subspace, the same K.μ⁻ + K.μ⁺ replacement pair would re-add only content-subspace positions, leaving the link subspace untouched.
- *Referential integrity (S3 content clause).* `a₂' ∈ dom(C')` (post-K.α); `a₃, a₄ ∈ dom(C) ⊆ dom(C')` by P0 frame on the prior content addresses. ✓
- *S8a, S8-depth, S8-fin on M_post.* New positions have all strictly positive components; `V_{s_C}(d_post) = {[1,1], [1,2], [1,3], [1,4]}` of uniform depth 2; cardinality 4 < ∞. ✓
- *D-CTG★, D-MIN★ on M_post.* `V_{s_C}(d_post)` is contiguous under the V-ordering on `s_C` (every depth-2 positive tuple with first component 1 lex-between `[1,1]` and `[1,4]` — i.e., `[1,2]` and `[1,3]` — is present), with `min = [1, 1] = [s_C, 1]`. ✓

*P4★ status at M_post.* `Contains_C(M_post) = {(a₁, d), (a₂', d), (a₃, d), (a₄, d)}`. K.μ⁺ holds R in frame (R = R_int), so `(a₂', d) ∉ R` at M_post — `Contains_C(M_post) ⊄ R`. Restoration occurs at the K.ρ step.

**Step 4: K.ρ — record provenance for the new address.** Effect: `R' = R ∪ {(a₂', d)}`. Preconditions: `a₂' ∈ dom(C')` (post-K.α); `d ∈ E_doc`. ✓ **P4★ restored**: `(a₂', d) ∈ R'`, so `Contains_C(M_post) ⊆ R'`.

**Composite verification at Σ → Σ'.**

Net change across the composite:
- `dom(C') \ dom(C) = {a₂'}` — one new content address.
- `dom(M'(d)) = dom(M(d)) = {[1,1], [1,2], [1,3], [1,4]}` — the V-position domain returns to its pre-state shape after the K.μ⁻ + K.μ⁺ round-trip.
- `ran(M'(d)|_{s_C}) \ ran(M(d)|_{s_C}) = {a₁, a₂', a₃, a₄} \ {a₁, a₂, a₃, a₄} = {a₂'}` — only `a₂'` is new to d's content-subspace range; `a₃` and `a₄` are re-added but were already in the pre-state range.
- `R' \ R = {(a₂', d)}` — one new provenance entry.

Coupling verification:
- *J0.* `a₂' ∈ dom(C') \ dom(C)`, and the placement clause is witnessed by `M'(d)([1,2]) = a₂'` at d ∈ E'_doc. ✓
- *J1★ (new-address coupling).* Computing the content-subspace ranges at the composite endpoints:
  - *Pre-composite (Σ):* `ran(M(d)|_{s_C}) = {M(d)(v) : v ∈ V_{s_C}(d)} = {M(d)([1,1]), M(d)([1,2]), M(d)([1,3]), M(d)([1,4])} = {a₁, a₂, a₃, a₄}`.
  - *Post-composite (Σ'):* `ran(M'(d)|_{s_C}) = {M'(d)(v) : v ∈ V_{s_C}(d')} = {M'(d)([1,1]), M'(d)([1,2]), M'(d)([1,3]), M'(d)([1,4])} = {a₁, a₂', a₃, a₄}`.
  - *Difference:* `ran(M'(d)|_{s_C}) \ ran(M(d)|_{s_C}) = {a₁, a₂', a₃, a₄} \ {a₁, a₂, a₃, a₄} = {a₂'}`.
  J1★ requires `(a₂', d) ∈ R'`, which K.ρ supplied at Step 4. ✓ The re-added addresses `a₃` and `a₄` are *not* new to d's content-subspace range — they appear in both the pre-state range `{a₁, a₂, a₃, a₄}` and the post-state range `{a₁, a₂', a₃, a₄}` — so J1★ does not require fresh provenance for them, even though they pass through the K.μ⁻ + K.μ⁺ cycle internally. J1★ is range-based and evaluated only between Σ and Σ', so the intermediate dispossession at M_int (where the ranges transit through `ran(M_int(d)|_{s_C}) = {a₁}` and `ran(M_post(d)|_{s_C}) = {a₁, a₂', a₃, a₄}` before reaching `ran(M'(d)|_{s_C})`) is invisible to the coupling.
- *J1'★ (new-provenance check; vacuity on re-added addresses).* The single new provenance entry `(a₂', d) ∈ R' \ R` corresponds to `a₂'` being new to d's content-subspace range, witnessed by the explicit set computation above: `a₂' ∈ ran(M'(d)|_{s_C}) = {a₁, a₂', a₃, a₄}` and `a₂' ∉ ran(M(d)|_{s_C}) = {a₁, a₂, a₃, a₄}`. *Vacuity on re-added addresses:* `a₃` and `a₄` pass through the K.μ⁻ + K.μ⁺ cycle but generate no entries in `R' \ R` — the pre-existing `(a₃, d), (a₄, d) ∈ R` carry through by P2, no fresh K.ρ is invoked for them, and J1'★ therefore has nothing to check for them at the composite boundary; equivalently, neither `a₃` nor `a₄` lies in `ran(M'(d)|_{s_C}) \ ran(M(d)|_{s_C}) = {a₂'}`. ✓

Post-state invariant verification:
- *P4 (Contains ⊆ R).* `Contains(Σ') ⊇ {(a₁, d), (a₂', d), (a₃, d), (a₄, d)}`; each pair is in R' — `(a₁, d), (a₃, d), (a₄, d) ∈ R ⊆ R'` by P2, and `(a₂', d) ∈ R'` by K.ρ. The stale pair `(a₂, d) ∈ R' \ Contains(Σ')` records that d once contained `a₂`, the historical fact that survives the replacement. ✓
- *P6 (Existential coherence).* `origin(a₂') = d ∈ E_doc`; pre-existing content addresses retain their origin entities by frame. ✓
- *P7 (Provenance grounding).* `(a₂', d) ∈ R'` has `a₂' ∈ dom(C')`; pre-existing R entries retain their grounding by P0. ✓
- *P7a (Provenance coverage).* every `a ∈ dom(C')` has at least one provenance entry — `a₁, a₂, a₃, a₄` retain their pre-state entries (R ⊆ R' by P2), and `a₂'` has the freshly added `(a₂', d)`. ✓
- *D-CTG, D-MIN at Σ'.* `V_{s_C}(d') = {[1,1], [1,2], [1,3], [1,4]}` contiguous, minimum `[1,1] = [s_C, 1]`. ✓


## Worked example: link allocation and arrangement

We verify the central postconditions on concrete tumbler values. By SubspaceConventionAxiom (FixedSubspaceIdentifiers), `s_C = 1` and `s_L = 2` throughout (and SC-NEQ `1 ≠ 2` is satisfied automatically). Consider document `d` at address `1.0.1.0.1` with two text content addresses allocated and arranged.

*Initial state.* `dom(C) = {1.0.1.0.1.0.1.1, 1.0.1.0.1.0.1.2}`, `dom(L) = ∅`, `E_doc = {1.0.1.0.1}`, `R = {(1.0.1.0.1.0.1.1, d), (1.0.1.0.1.0.1.2, d)}` (implicit from prior J0/J1 of allocation).

Arrangement: `M(d) = {[1,1] ↦ 1.0.1.0.1.0.1.1, [1,2] ↦ 1.0.1.0.1.0.1.2}`.

Text-subspace V-positions: `V_1(d) = {[1,1], [1,2]}` — contiguous (D-CTG), minimum at `[1,1]` (D-MIN), depth 2 (S8-depth). Link subspace: `V_2(d) = ∅`.

**Step 1: K.λ — allocate link.** Create link `ℓ = 1.0.1.0.1.0.2.1` with value `(F, G, Θ)`.

Precondition verification:
- `d = 1.0.1.0.1 ∈ E_doc`
- `ℓ ∉ dom(L) ∪ dom(C)`: `dom(L) = ∅`; content addresses have element field `1.1` and `1.2` (subspace 1), while ℓ has element field `2.1` (subspace 2) — by T7 and SC-NEQ, disjoint
- `zeros(ℓ) = 3`: zeros at positions 2, 4, 6 in the tumbler `1.0.1.0.1.0.2.1`
- `subspace_I(ℓ) = 2 = s_L`
- `origin(ℓ) = 1.0.1.0.1 = d`
- Forward allocation: no prior links in dom(L) with origin d, so vacuously satisfied
- `(F, G, Θ) ∈ Link` by assumption (L3)

Effect: `L' = {1.0.1.0.1.0.2.1 ↦ (F, G, Θ)}`. Frame: C, E, M, R unchanged.

Post-state verification:
- L14: `dom(C) ∩ dom(L') = ∅` — content addresses have `subspace_I(a) = 1`, link has `subspace_I(ℓ) = 2`, and `1 ≠ 2`
- L0: all dom(L') addresses have subspace s_L = 2; all dom(C) addresses have subspace s_C = 1
- L3: `L'(ℓ) = (F, G, Θ)` with `F, G, Θ ∈ Endset`
- L-fin: `dom(L') = {ℓ}` is a singleton, hence finite. ✓
- S3★, CL-OWN: M unchanged, hold from pre-state
- *P7a:* dom(C) is unchanged; every a ∈ dom(C) retains its provenance entry from R. ✓
- *J1'★ (vacuous):* K.λ holds R in frame, so `R' \ R = ∅`. No new provenance entries to check; J1'★ is vacuously satisfied. ✓

**Step 2: K.μ⁺_L — arrange the link in d.** Map the newly allocated `ℓ` into d's link subspace at the minimum link V-position.

Precondition verification:
- `d ∈ E_doc`
- `ℓ = 1.0.1.0.1.0.2.1 ∈ dom(L')`
- `origin(ℓ) = 1.0.1.0.1 = d`
- `ℓ ∉ ran(M(d))`: pre-state `M(d) = {[1,1] ↦ a₁, [1,2] ↦ a₂}` has range `{a₁, a₂} ⊆ dom(C)`; since `ℓ ∈ dom(L)` and `dom(L) ∩ dom(C) = ∅` (L14), `ℓ ∉ ran(M(d))`
- `subspace(v_ℓ) = 2 = s_L`
- `V_{s_L}(d) = ∅`, so `v_ℓ = [s_L, 1] = [2, 1]` with `m_L = 2 ≥ 2` (D-MIN for empty link subspace)
- `#v_ℓ = 2 = m_L` (S8-depth)

Effect: `M'(d) = {[1,1] ↦ 1.0.1.0.1.0.1.1, [1,2] ↦ 1.0.1.0.1.0.1.2, [2,1] ↦ 1.0.1.0.1.0.2.1}`.

Post-state verification:
- S3★: `subspace([1,1]) = 1 = s_C` and `M'(d)([1,1]) = 1.0.1.0.1.0.1.1 ∈ dom(C)`; `subspace([1,2]) = 1 = s_C` and `M'(d)([1,2]) = 1.0.1.0.1.0.1.2 ∈ dom(C)`; `subspace([2,1]) = 2 = s_L` and `M'(d)([2,1]) = 1.0.1.0.1.0.2.1 ∈ dom(L')`
- CL-OWN: the only link-subspace position is `[2,1]` with `origin(M'(d)([2,1])) = origin(1.0.1.0.1.0.2.1) = 1.0.1.0.1 = d`
- D-CTG: `V_1(d) = {[1,1], [1,2]}` contiguous; `V_2(d) = {[2,1]}` singleton, trivially contiguous
- D-MIN: `min(V_1(d)) = [1,1] = [s_C, 1]`; `min(V_2(d)) = [2,1] = [s_L, 1]`
- L14: subspace identifiers 1 and 2 are distinct (SC-NEQ), so dom(C) ∩ dom(L') = ∅
- L-fin: dom(L') = {ℓ} is unchanged from Step 1; still finite. ✓
- *P7a:* dom(C) is unchanged; every a ∈ dom(C) retains its provenance entry from R. ✓
- *J1'★ (vacuous):* K.μ⁺_L holds R in frame, so `R' \ R = ∅`. The new M extension is link-subspace only (`subspace(v_ℓ) = s_L`), so the content-subspace range `ran(M'(d)|_{s_C})` is unchanged — no provenance coupling is triggered, consistent with J1'★'s content-subspace scoping. ✓

**Step 3: K.μ~ — reorder text, verify link fixity.** Swap text: `π([1,1]) = [1,2]`, `π([1,2]) = [1,1]`. Link-subspace fixity (proved in the K.μ~ section above) forces `π([2,1]) = [2,1]`.

Let `a₁ = 1.0.1.0.1.0.1.1` and `a₂ = 1.0.1.0.1.0.1.2`. Pre-state: `M'(d) = {[1,1] ↦ a₁, [1,2] ↦ a₂, [2,1] ↦ ℓ}`. K.μ~ decomposes as K.μ⁻ (full content-subspace clearance, retaining `[2,1]`) followed by K.μ⁺ (re-adding `{[1,1] ↦ a₂, [1,2] ↦ a₁}`). Intermediate-state admissibility discharges from the K.μ~ Decomposition section's checks.

Post-state: `M''(d) = {[1,1] ↦ a₂, [1,2] ↦ a₁, [2,1] ↦ ℓ}`.

Post-state verification:
- *S3★:* `subspace([1,1]) = 1 = s_C` and `M''(d)([1,1]) = a₂ ∈ dom(C)`; `subspace([1,2]) = 1 = s_C` and `M''(d)([1,2]) = a₁ ∈ dom(C)`; `subspace([2,1]) = s_L` and `M''(d)([2,1]) = ℓ ∈ dom(L')`. ✓
- *L14:* dom(C) ∩ dom(L') = ∅ unchanged from Step 2. ✓
- *L-fin:* dom(L') = {ℓ} unchanged; still finite. ✓
- *D-CTG★/D-MIN★:* V_{s_C}(d) = {[1,1], [1,2]} and V_{s_L}(d) = {[2,1]} are both unchanged from Step 2 (K.μ~ preserves dom by K.μ~-FIX); contiguity and minima are inherited.
- *CL-OWN:* the link-subspace mapping is fixed pointwise, so origin(M''(d)([2,1])) = origin(ℓ) = d remains satisfied. ✓
- *P7a:* dom(C) is unchanged and R is unchanged; every a ∈ dom(C) retains its provenance entry. ✓
- *J1'★ (vacuous):* K.μ~ holds R in frame, so `R' \ R = ∅`. No new provenance entries to check; J1'★ is vacuously satisfied. (Note: K.μ~ also preserves the content-subspace range `ran(M'(d)|_{s_C}) = ran(M(d)|_{s_C})` exactly — π is a bijection on dom(M(d)) and the multiset of values is preserved — so even if a provenance entry were added it would have no new content-subspace range entry to anchor against.) ✓

**Step 4: K.λ + K.μ⁺_L — allocate and arrange a second link.** To exercise link-subspace contraction below we need a non-singleton link subspace. Allocate `ℓ₂ = 1.0.1.0.1.0.2.2 = inc(ℓ, 0)` (the next sibling on d's link frontier under TA5(c), per K.λ's subsequent-link case) with some value `(F', G', Θ')`; then arrange `ℓ₂` at `v_{ℓ₂} = shift(max(V_{s_L}(d)), 1) = shift([2,1], 1) = [2,2]` (D-CTG case of K.μ⁺_L).

Effect after both transitions: `L = {ℓ ↦ (F, G, Θ), ℓ₂ ↦ (F', G', Θ')}`, `M''(d) = {[1,1] ↦ a₂, [1,2] ↦ a₁, [2,1] ↦ ℓ, [2,2] ↦ ℓ₂}`. Link-subspace V-positions: `V_{s_L}(d) = {[2,1], [2,2]}` — contiguous (D-CTG★), minimum at `[2,1] = [s_L, 1]` (D-MIN★), depth 2 (S8-depth), structural form `{[s_L, k] : 1 ≤ k ≤ 2}` (D-SEQ★ with `n_{s_L} = 2`, `m_{s_L} = 2`; the general form `{[s_L, 1, ..., 1, k]}` has zero intermediate 1s). *J1'★ (vacuous):* both K.λ and K.μ⁺_L hold R in frame, so `R' \ R = ∅` for the composite — no new provenance entries are introduced, and J1'★ is vacuously satisfied. The K.μ⁺_L step adds only link-subspace V-positions, so the content-subspace range of M''(d) is unchanged across the composite, consistent with J1'★'s content-subspace scoping. ✓

Post-state verification (for the K.λ + K.μ⁺_L composite):
- *S3★:* the new link-subspace position `[2,2]` has `subspace([2,2]) = s_L` and maps to `ℓ₂ ∈ dom(L')`; existing positions retain their pre-state values. ✓
- *CL-OWN:* `origin(M''(d)([2,2])) = origin(ℓ₂) = d` (K.λ's `origin(ℓ₂) = d` precondition combined with the K.μ⁺_L placement). ✓
- *CL-UNIQ:* `ℓ₂` is fresh to `dom(L)` (K.λ's allocation precondition), so no prior V-position references it; the new V-position `[2,2]` is therefore the unique link-subspace V-position mapping to `ℓ₂`. ✓
- *L0/L1/L1a/L3/L-fin:* each established for `ℓ₂` by K.λ's preconditions and inherited at the post-state.
- *L14:* `dom(C) ∩ dom(L') = ∅` — the new link `ℓ₂` has `subspace_I(ℓ₂) = s_L = 2`, distinct from `s_C = 1`. ✓

**Step 5: K.μ⁻ — admissible suffix removal of links.** Remove the mapping at `[2,2]` — the maximum end of `V_{s_L}(d)`, a 1-element suffix of the link-subspace range.

*K.μ⁻:* `dom(M'''(d)) = {[1,1], [1,2], [2,1]} ⊂ dom(M''(d))`. Surviving mappings unchanged: `M'''(d)([1,1]) = a₂`, `M'''(d)([1,2]) = a₁`, `M'''(d)([2,1]) = ℓ`. The content subspace is unchanged: `V_{s_C}(d') = {[1,1], [1,2]}`. The link subspace contracts to a 1-element suffix prefix: `V_{s_L}(d') = {[2,1]}`.

Admissibility verification (per K.μ⁻'s per-subspace precondition):
- *Content-subspace pattern.* `V_{s_C}(d') = V_{s_C}(d)` — empty removal, `n'_{s_C} = n_{s_C} = 2`. This is the case-(a) zero-suffix admissible pattern.
- *Link-subspace pattern.* `V_{s_L}(d) = {[2,1], [2,2]}`, `V_{s_L}(d') = {[2,1]}` — a 1-element suffix removal with `n'_{s_L} = 1` (case (a) admissible).

Post-state invariant verification:
- *S3★:* surviving mappings retain their pre-state values; `[2,1] ↦ ℓ ∈ dom(L)` satisfies the link clause. ✓
- *D-CTG★:* `V_{s_C}(d') = {[1,1], [1,2]}` and `V_{s_L}(d') = {[2,1]}` are each contiguous. ✓
- *D-MIN★:* `min(V_{s_C}(d')) = [1,1] = [s_C, 1]`; `min(V_{s_L}(d')) = [2,1] = [s_L, 1]`. ✓
- *D-SEQ★:* `V_{s_L}(d') = {[s_L, 1]}` matches `{[s_L, k] : 1 ≤ k ≤ 1}` at `n_{s_L} = 1` (`m_{s_L} = 2`, so the general D-SEQ★ form has zero intermediate 1s). ✓
- *CL-OWN:* `origin(M'''(d)([2,1])) = origin(ℓ) = d` (preserved from pre-state by frame on the surviving mapping). ✓
- *CL-UNIQ:* the surviving link-subspace mapping is the singleton `{[2,1] ↦ ℓ}`; vacuously injective. ✓
- *L12:* `dom(L)` unchanged — `ℓ₂` remains in `dom(L)` despite no longer being arranged. ✓ This is the *orphan link* state Nelson identifies (LM 4/9): `ℓ₂ ∈ dom(L)` but `ℓ₂ ∉ ran(M'''(d))` for any d.
- *J1'★ (vacuous):* K.μ⁻ holds R in frame, so `R' \ R = ∅`. No new provenance entries to check; J1'★ is vacuously satisfied. (J1'★ is range-based: the content-subspace range `ran(M'''(d)|_{s_C}) = ran(M''(d)|_{s_C}) = {a₁, a₂}` is unchanged across this link-subspace contraction — the link-subspace range loses ℓ₂, but the link subspace is outside J1'★'s scope.) ✓

An attempt to remove `[2,1]` while retaining `[2,2]` is excluded by D-MIN★ (case (c) of the K.μ⁻ exhaustiveness lemma); an attempt to remove an interior position while retaining both endpoints is excluded by D-CTG★ (case (b)).


## Cross-layer invariants

**P6 (Existential coherence).** For every I-address in the content store, its origin document exists as an entity:

`(A a ∈ dom(C) :: origin(a) ∈ E_doc)`

*Derivation.* K.α allocates a under origin(a)'s prefix (S7a, ASN-0036), and requires origin(a) ∈ E_doc as a precondition — the allocation mechanism inc(·, k) operates on an existing tumbler within the ownership domain. P1 preserves entity membership across subsequent transitions; P0 preserves a ∈ dom(C). Initial state: dom(C₀) = ∅, so the quantifier is vacuously satisfied. Inductive step: each K.α has origin(a) ∈ E_doc by precondition; P0 preserves a; P1 preserves origin(a). ∎

**P7 (Provenance grounding).** Every provenance entry references allocated content:

`(A (a, d) ∈ R :: a ∈ dom(C))`

*Derivation.* K.ρ requires a ∈ dom(C) as a precondition. P0 preserves dom(C). By induction: initially R₀ = ∅ (vacuous). Each K.ρ adds (a, d) with a ∈ dom(C); P0 ensures a remains in dom(C') for all subsequent states; P2 ensures (a, d) remains in R'. ∎

**P7a (Provenance coverage).** Every I-address in the content store has at least one provenance record:

`(A a ∈ dom(C) :: (E d :: (a, d) ∈ R))`

*Derivation.* By induction. *Base:* dom(C₀) = ∅; vacuous. *Inductive step:* for a ∈ dom(C) (pre-existing), the inductive hypothesis gives (a, d) ∈ R for some d, and P2 preserves it. For a ∈ dom(C') \ dom(C) (freshly allocated), J0 gives a ∈ ran(M'(d)) for some d; J1 then gives (a, d) ∈ R'. ∎

**GlobalLineage (Derived corollary, GlobalDescentFromBootstrap).** Every entity, content address, and link address descends structurally from the bootstrap node n₀:

`(A x ∈ E ∪ dom(C) ∪ dom(L) :: n₀ ≼ x)`

*Derivation.* The three components are discharged separately.

*(i) Entities.* `(A e ∈ E :: n₀ ≼ e)`. For `IsNode(e)`, NodeLineage gives `n₀ ≼ e` directly. For `¬IsNode(e)`, P8 supplies `parent(e) ∈ E` with `zeros(parent(e)) = zeros(e) − 1` (T4b's parent projection). By the parent definition — `parent(e)` is obtained by truncating e's last field and the preceding zero separator — we have `parent(e) ≼ e` under the tumbler-prefix order (ASN-0034). Recursive descent through parent chains terminates at a node (since each step strictly decreases `zeros`, and entities satisfy `zeros ∈ {0, 1, 2}` by the entity-set definition, the chain reaches `zeros = 0` in at most two steps — the longest case being a document with `zeros = 2`, whose parent is an account with `zeros = 1`, whose parent is a node with `zeros = 0`), where NodeLineage applies. Transitivity of ≼ over the parent chain `e ≽ parent(e) ≽ parent(parent(e)) ≽ ... ≽ node` together with NodeLineage at the node gives `n₀ ≼ e`.

*(ii) Content addresses.* `(A a ∈ dom(C) :: n₀ ≼ a)`. By P6, `origin(a) ∈ E_doc ⊆ E`, so (i) gives `n₀ ≼ origin(a)`. By S7a, `a` is allocated under `origin(a)`'s prefix — formally, `origin(a) ≼ a` (origin recovers the document-level prefix of a by truncating to `zeros = 2`). Transitivity of ≼ closes: `n₀ ≼ origin(a) ≼ a`.

*(iii) Link addresses.* `(A ℓ ∈ dom(L) :: n₀ ≼ ℓ)`. By L1a, `origin(ℓ) ∈ E_doc ⊆ E`, so (i) gives `n₀ ≼ origin(ℓ)`. By L1c, ℓ is reachable from `origin(ℓ)` by a structural inc-chain (per-step inc-rule conformance, not full T10a discipline; see L1c discharge), and every step in such a chain preserves the operand's prefix (TA5(b) for k > 0, TA5(c) for k = 0), so `origin(ℓ) ≼ ℓ`. Transitivity closes: `n₀ ≼ origin(ℓ) ≼ ℓ`. ∎

GlobalLineage promotes NodeLineage from a node-restricted invariant to a docuverse-wide rooted-tree property: the entity hierarchy, content store, and link store all descend from the single bootstrap address n₀.


## Extended reachable-state invariants

**ExtendedReachableStateInvariants.** Every state reachable from Σ₀ by a finite sequence of valid composite transitions satisfies the conjunction of two clauses, partitioned by *temporal scope* (i.e., which states the invariant holds at along a composite). *Elementary per-state* invariants hold at **every** state reachable from Σ₀ — including every intermediate state within a composite — because each elementary transition preserves them individually. *Composite-boundary* invariants hold at every state reachable from Σ₀ when measured at *composite boundaries* (the initial Σ and final Σ' of any valid composite), but may transiently fail at intermediate states *within* a composite (e.g., after K.α before its companion K.μ⁺/K.ρ); they are restored by the close of each valid composite via the J0/J1★/J1'★ couplings.

  *Elementary per-state* (Class (a) of the proof below — preserved step-by-step):

  S2 ∧ S3★ ∧ S3★-aux ∧ S4 ∧ S7a ∧ S7b ∧ S7c ∧ S7d ∧ S8a ∧ S8-fin ∧ S8-depth ∧ S8★ ∧ D-CTG★ ∧ D-MIN★ ∧ D-SEQ★ ∧ P6 ∧ P7 ∧ P8 ∧ NodeLineage ∧ L0 ∧ L1 ∧ L1a ∧ L1b ∧ L1c ∧ L3 ∧ L14 ∧ L-fin ∧ CL-OWN ∧ CL-UNIQ

  *Composite-boundary* (Class (b) of the proof below — discharged at boundaries by J0/J1★/J1'★):

  P4★ ∧ P4a ∧ P7a

  The Class (b) invariants may transiently fail at intermediate states; in particular, a composite that allocates fresh content (K.α) violates P7a at the post-K.α intermediate state (the new I-address is in dom(C') but no (·, d) entry yet sits in R'), with restoration by the composite-trailing K.ρ. The reader should consult ValidComposite★'s notation-disambiguation block (clauses (a)–(d) of the *Notation disambiguation: atomic vs. composite `Σ → Σ'`* paragraph) for the precise reading of `Σ → Σ'` at each clause site.

ASN-0036's S7d (document allocation discipline) is preserved unchanged: every `d ∈ E_doc` is T4-valid with `zeros(d) = 2`, placed in E_doc by a K.δ event satisfying `e ∉ E` discharged by T10a's GlobalUniqueness on the parent allocator's tracked domain.

**ExtendedTransitionInvariants (per-transition).** Every valid composite transition `Σ → Σ'` satisfies:

  P3

P3 is the conjunction P0 ∧ P1 ∧ P2 ∧ L12 (extending ASN-0043's L12 with the four-component monotonicity predicates of this ASN), so naming P3 alone covers every per-transition monotonicity obligation. P0 subsumes ASN-0036's S0 (ContentImmutability) and S1 (StoreMonotonicity); ASN-0036's S9 (TwoStreamSeparation) follows from P0 unconditionally.

*S4 scope.* The S4 conjunct of ExtendedReachableStateInvariants holds for every K.δ transition: NodeUniqueAllocation closes the IsNode case, and T10a GlobalUniqueness on the parent allocator's tracked domain closes the ¬IsNode case.

*Proof.* The proof proceeds by induction on the number of valid composite transitions from Σ₀. The per-state invariant set partitions into two classes: *elementary invariants* preserved by each elementary transition individually, and *composite invariants* that may be violated at intermediate states within a composite but hold at every composite boundary. The per-transition invariants are addressed last, in a single elementary-case check.

**Base.** The extended initial state Σ₀ satisfies every per-state invariant (verified in the Link store and extended system state section — L₀ = ∅ satisfies link invariants vacuously, including L3; S3★ and P4★ reduce to S3 and P4; S3★-aux holds vacuously since M₀(d) = ∅ for all d; D-CTG and D-MIN hold vacuously since V_S(d) = ∅ for every subspace S). The per-transition invariants have no base case — they are vacuous before any transition has occurred — and enter the induction at the first step.

**Class (a): Elementary per-state invariants** — preserved by each elementary transition individually. These are all per-state invariants except P4★ and P7a: S2, S3★, S3★-aux, S4, S7a, S7b, S7c, S7d, S8a, S8-fin, S8-depth, S8★, D-CTG★, D-MIN★, D-SEQ★, P6, P7, P8, NodeLineage, L0, L1, L1a, L1b, L3, L14, L-fin, CL-OWN, CL-UNIQ.

S8 (the S8★ conjunct of ExtendedReachableStateInvariants) is established per-subspace by direct application of S8★(s_C) and S8★(s_L), each defined in the Amendments to existing transitions section. *Content subspace:* S8★(s_C) follows from ASN-0036's S8 applied to the projection `M(d')|_{V_{s_C}(d')} : V_{s_C}(d') → dom(C')` (S3★'s content clause is exactly S3 restricted to V_{s_C}(d'), and S2/S7b/S7c/S8a/S8-depth/S8-fin are elementary-preserved). *Link subspace:* S8★(s_L) is established by direct application of ASN-0036's S8 to the projection `M(d')|_{V_{s_L}(d')}`, using the same half-open range `0 ≤ k < n_j` convention that ASN-0036's S8 itself employs in condition (b). The shape of the decomposition is depth-2-specific by LinkVPositionDepthAxiom (`m_L = 2`): every `v ∈ V_{s_L}(d')` has the form `[s_L, k]`, and a sequence of link-subspace V-positions `{[s_L, k], [s_L, k+1], …, [s_L, k+n-1]}` mapping shift-aligned to `{M(d')([s_L, k+i]) : 0 ≤ i < n}` constitutes an n-element correspondence run. ASN-0036's S8 then delivers a finite decomposition (S8-fin gives finiteness of dom(M(d'))).

For K.α (amended): holds M and L in frame; S3★, S3★-aux preserved (M unchanged); content, entity, and provenance invariants preserved; P8 preserved since E is unchanged. L0 clause 2: `subspace_I(a) = s_C` by the K.α amendment, so the new content address satisfies `(A a ∈ dom(C') :: subspace_I(a) = s_C)`. L14: `subspace_I(a) = s_C` and `s_C ≠ s_L` (SC-NEQ), and L0 clause 1 at the pre-state gives `(A ℓ ∈ dom(L) :: subspace_I(ℓ) = s_L)`, so `a ∉ dom(L)` and `dom(C') ∩ dom(L') = ∅`. L1, L1a, L3, L12 preserved (L unchanged). For K.δ: holds both M and L in frame; S3★, S3★-aux preserved; link invariants preserved. *P8 (entity-hierarchy spine).* K.δ adds one entity `e` to E. (i) `IsNode(e)`: the universal quantifies over non-node entities, so `e` is outside its scope; existing non-nodes retain `parent(e') ∈ E ⊆ E'` by inductive hypothesis. (ii) `¬IsNode(e)`: K.δ's case-(ii) precondition requires `parent(e) ∈ E ⊆ E'`; existing non-nodes carry forward by inductive hypothesis. For K.ρ: holds both M and L in frame; S3★, S3★-aux preserved; P8 preserved. P7 is elementary: K.ρ adds (a, d) with `a ∈ dom(C)` (precondition), and P0 carries `a ∈ dom(C')` to subsequent states; all other transitions hold R in frame. For K.μ⁺ (amended): holds L in frame; S3★ preserved (analyses above); S3★-aux preserved (new positions have subspace s_C); D-CTG, D-MIN preserved by postcondition; S8★ at Σ' by the per-subspace decomposition above; link invariants preserved. For K.μ⁻: holds L in frame; S3★ preserved (restriction of M(d)); S3★-aux preserved; D-CTG, D-MIN preserved by the K.μ⁻ amendment postcondition (D-SEQ at the input gives V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}, so valid contractions remove a suffix or all positions); S8★ at Σ' by the per-subspace decomposition; link invariants preserved. For K.μ~ (named composite via K.μ⁻ + K.μ⁺ realisation): holds L in frame. Admissibility clause (iii) ensures π ≠ id (and hence `dom_C(M(d)) ≠ ∅`); the K.μ⁻ + K.μ⁺ decomposition preserves each invariant through the underlying elementary steps; link-subspace fixity (established separately at *Link-subspace fixity under K.μ~*) forces π to biject dom_C(M(d)) onto dom_C(M'(d)) with the link subspace unchanged, and D-SEQ at both input and output yields V_S(d') = V_S(d) for each content subspace. S8★ at Σ' by the per-subspace decomposition; CL-OWN preserved by link-subspace fixity. *CL-UNIQ preservation (dependency chain made explicit).* Steps 1–3 of the link-subspace fixity proof (in the *Decomposition of K.μ~* section above) establish `M'(d)|_{dom_L} = M(d)|_{dom_L}` as functions, *without* invoking CL-UNIQ — they appeal only to the bijection equation, subspace preservation, K.μ⁺'s amendment (no link-subspace V-positions created), and the K.μ⁻ value-preservation clause. Step 4 then uses CL-UNIQ *at the pre-state* Σ — the inductive hypothesis — to conclude `π(v) = v` pointwise on `dom_L`; that *pointwise* identity is not what discharges post-state CL-UNIQ. Post-state CL-UNIQ follows directly from the *functional* identity established by Steps 1–3: `M'(d)|_{dom_L} = M(d)|_{dom_L}` as functions means their injectivity profiles are identical, so the inductive hypothesis (CL-UNIQ at Σ — `M(d)|_{dom_L}` is injective) carries through to CL-UNIQ at Σ' (`M'(d)|_{dom_L}` is injective) without further argument. The dependency chain is therefore "pre-state CL-UNIQ + link-subspace functional fixity (Steps 1–3) → post-state CL-UNIQ"; Step 4's pointwise identity is needed to discharge the K.μ~ link-subspace fixity *postcondition* (`π(v) = v` on `dom_L`), not to discharge CL-UNIQ preservation. Other link invariants preserved. For K.λ: holds M, C, E, R in frame; S3★, S3★-aux preserved; L3 established for the new entry and preserved for existing entries (L12); L-fin preserved (`|dom(L')| = |dom(L)| + 1`); L1c preserved by K.λ's allocation discipline (SubAllocatorAxiom for the first emission, TA5(c) inc(·, 0) chain for subsequent emissions — full chain witnessed in the Foundation invariants block below). For K.μ⁺_L: holds C, L, E, R in frame; S3★-aux preserved (new position has subspace s_L); per-subspace arrangement invariants verified in *Link-subspace extension* (S8a, S8-fin, S8-depth(s_L), D-CTG★(s_L), D-MIN★(s_L), D-SEQ★(s_L) all hold at the post-state); S3★ satisfied by precondition. S8★ at Σ' by the per-subspace decomposition above (content subspace frame-preserved, link subspace by the trivial length-1 decomposition over the extended `V_{s_L}(d')`). CL-OWN preserved (`origin(ℓ) = d` by precondition); CL-UNIQ preserved by the first-arrangement precondition `ℓ ∉ ran(M(d))`; L3 and L-fin preserved (L unchanged).

**Foundation invariants.** The remaining invariants — S4, S7a–d, L1b, L-fin, D-SEQ★, NodeLineage — are preserved as follows.

- *S4 (Origin-based identity)* — distinct allocation events produce distinct addresses. Each K.α produces `a` via the T10a allocator under origin(a) (S7a, ASN-0036), so GlobalUniqueness (T10a) gives `a ∉ dom(C)`; cross-document distinctness for two K.α events under distinct documents d₁, d₂ follows from the *Cross-document disjointness chain* lemma (T10a.{2,5} → T10) applied at `b_C(d₁)` and `b_C(d₂)`. For K.δ on non-node entities, the same allocator discipline applies via T10a GlobalUniqueness on the parent allocator's tracked domain; for K.δ on nodes, NodeUniqueAllocation (the axiom introduced above) supplies `e ∉ E` directly. *Cross-document distinctness for K.δ:* for two K.δ events allocating documents d₁, d₂ under distinct accounts A₁ ≠ A₂ (i.e., parent(d₁) ≠ parent(d₂)), the *Cross-document disjointness chain* lemma applies at the account level — instantiated at `e₁ = A₁, e₂ = A₂` with `s = 1` (the document sub-allocator's first emission `inc(A, 2) = [A.0.1]`). The lemma's prefix-incomparability conclusion `[A₁.0.1] ⋠ [A₂.0.1] ∧ [A₂.0.1] ⋠ [A₁.0.1]` together with T10 (PartitionIndependence) gives `d₁ ≠ d₂` for any document minted under each account. Within a single account (parent(d₁) = parent(d₂)), the same K.δ event admits T10a GlobalUniqueness on the account's document sub-allocator chain directly. *K.λ — first-link case:* The first-link case is identified by `dom(L) ∩ {a : origin(a) = d} = ∅` — no link has yet been allocated under d. In this case K.λ emits `ℓ = [d.0.s_L.1]` via SubAllocatorAxiom (the sub-allocator construction yields the link-allocator base address `[d.0.s_L.1]` under origin(ℓ) = d, where d is a document address `[N, 0, U, 1]`). SubAllocatorAxiom.FirstEmission supplies `ℓ ∉ dom(Σ.L) ∪ dom(Σ.C)` for this first-emission address `[d.0.s_L.1]` directly; the FirstEmission clause commits *only* the first emission, not "every address produced by d's link sub-allocator", so it cannot be cited to discharge freshness for subsequent emissions. T10a's GlobalUniqueness is not invoked in the first-link case for an independent structural reason: the first emission is not an inc-step from a previously inc-produced address within the sub-allocator's frontier, and T10a's per-owner inc-chain discipline does not span the bootstrap from `d` to the sub-allocator's first output (the document `d` cannot mint `[d.0.s_L.1]` directly under T10a's at-most-once spawning constraint — see the Allocator hierarchy under documents section). T10a's discipline takes over from the sub-allocator's second emission onward, as governed in the subsequent-link case immediately below. *K.λ — subsequent-link case:* K.λ emits `ℓ = inc(prev, 0)` via TA5(c) on the prior emission's frontier; T10a's GlobalUniqueness on the A_L(d) inc chain gives uniqueness against every prior `ℓ' ∈ dom(L)` sharing origin(ℓ) = d. The two routes — SubAllocatorAxiom.FirstEmission for the first emission, GlobalUniqueness for every subsequent emission — partition the freshness obligation cleanly along the first-vs-subsequent boundary; neither subsumes the other. *Cross-document distinctness:* for two K.λ events under distinct documents d₁, d₂ producing ℓ₁, ℓ₂, the *Cross-document disjointness chain* lemma (T10a.{2,5} → T10) — derived in the Allocator hierarchy under documents section — gives `ℓ₁ ≠ ℓ₂` because the link-allocator prefixes `[d₁.0.s_L]` and `[d₂.0.s_L]` differ at depth ≤ 4 (d₁ ≠ d₂ at depth ≤ 4 by S7d, whose cross-document distinctness consequence follows from K.δ's `e ∉ E` precondition discharged by T10a GlobalUniqueness on the parent allocator's tracked domain), and every inc-chain emission preserves the prefix. *Cross-store distinctness:* `ℓ ∉ dom(C)` follows from L14 (subspace_I(ℓ) = s_L, subspace_I(a) = s_C for every `a ∈ dom(C)`, and SC-NEQ gives s_L ≠ s_C). Combined: `ℓ ∉ dom(L) ∪ dom(C)`. All other transitions hold C, L, E in frame and add no addresses.
- *S7a (Document-scoped allocation)* — established by K.α's precondition that allocation uses origin(a)'s content-allocator prefix; preserved by P0 thereafter. For pre-existing addresses, S7a is inherited from the inductive hypothesis and P0.
- *S7b (Element-level I-addresses)* — `zeros(a) = 3`: K.α's amendment fixes `subspace_I(a) = s_C` and inc chains under a document-level prefix give `zeros(a) = 3`. Preserved by P0 thereafter.
- *S7c (Element-field depth)* — `#E(a) ≥ 2`: enforced by K.α's allocator chain (`E(a) = [s_C, k]` with `k ≥ 1` at minimum, i.e., depth ≥ 2). Preserved by P0 thereafter.
- *S7d (Document allocation discipline).* Every `d ∈ E_doc` is T4-valid with `zeros(d) = 2`, and was placed in E_doc by a K.δ event satisfying K.δ's `e ∉ E` precondition — discharged by T10a GlobalUniqueness on the parent allocator's tracked domain. Distinct K.δ events on documents produce distinct addresses by T10a's per-`(t, k')` discipline. Preserved by P1 thereafter.
- *L1b (Link element-field depth)* — `#E(ℓ) ≥ 2`: in K.λ's *first-link case*, SubAllocatorAxiom emits `ℓ = [d.0.s_L.1]`. The address `d` is a document tumbler with `zeros(d) = 2`, and the emission appends one zero separator and then the two-component suffix `[s_L, 1]`, so `ℓ` has `zeros(ℓ) = 3` and is T4-valid by SubAllocatorAxiom.Namespace's structural commitment. Applying T4b (UniqueParse, ASN-0034) to `ℓ` at `zeros = 3` makes all four projections — N, U, D, E — well-defined, with `E(ℓ) = [s_L, 1]` (the suffix following the third zero separator). T4b's projection therefore gives `#E(ℓ) = 2` directly, not "by construction" but as a citable consequence of T4b applied to the first-emission address. In the *subsequent-link case*, K.λ produces `ℓ = inc(prev, 0)` (TA5(c)), a sibling extension preserving both tumbler length and zero count: TA5(c) gives `#ℓ = #prev`, and T10a.8 (UniformSiblingZeroCount, ASN-0034) gives `zeros(ℓ) = zeros(prev) = 3` (every sibling on an `inc(·, 0)` chain shares the base's zero count, and `prev` is T4-valid by T10a.4). Same total length and same zero count force same element-field length: `#E(ℓ) = #ℓ − zeros(ℓ) − 1 = #prev − zeros(prev) − 1 = #E(prev) ≥ 2` inductively (the first link emitted under d has `#E = 2` by T4b applied to `[d.0.s_L.1]`; every subsequent sibling preserves this depth). Hence `#E(ℓ) ≥ 2` for every link emission. Preserved by L12 thereafter.
- *L1c (Link allocator conformance)* — every `ℓ ∈ dom(L)` must be reachable from a T4-valid document-level seed `s` (zeros(s) = 2) by a *structural inc-chain* with `k₁ = 2`. The chain property captured here is the per-step inc-rule conformance — each step `tᵢ = inc(tᵢ₋₁, kᵢ)` with `kᵢ ∈ {0, 1, 2}` satisfying TA5's structural preconditions (operand T4-validity, zeros bound at k = 2), plus length monotonicity `#tᵢ > #s` — *not* T10a's full discipline including allocator-frontier domain tracking. The distinction matters at the anchors `b_C(d)`, `b_L(d)` and at the first emission `[d.0.s_L.1]`: these inhabit no T10a-tracked allocator domain (b_C(d) and b_L(d) are virtual anchors outside `dom(C) ∪ dom(L)`; the first emission is committed outside both stores by SubAllocatorAxiom.FirstEmission, not by a T10a T2 spawn step from a prior tracked operand). Allocator-activation discharge for the anchor traversal and first emission goes through SubAllocatorAxiom; T10a's full discipline applies only to subsequent emissions on the activated A_L(d) frontier. Base: dom(L₀) = ∅, vacuous. Inductive step: only K.λ extends dom(L). For the *first-link case*, K.λ emits `ℓ = [d.0.s_L.1]` (SubAllocatorAxiom) under `d ∈ E_doc`. Under SubspaceConventionAxiom (`s_C = 1`, `s_L = 2`), the structural inc-chain `t₀ = d, t₁ = inc(d, 2) = b_C(d) = [d.0.1], t₂ = inc(t₁, 0) = [d.0.2] = b_L(d), t₃ = inc(t₂, 1) = ℓ = [d.0.2.1]` satisfies the per-step inc-rule: `s = d` is T4-valid with `zeros(s) = 2`; `k₁ = 2`, `k₂ = 0`, `k₃ = 1`, each in `{0, 1, 2}`; the only `k = 2` step is `k₁` whose operand `t₀ = d` has `zeros(d) = 2 ≤ 2`; and `#tᵢ > #d` at every step by TA5(d)'s length-extension and TA5(c)'s length-preservation. The step `t₂ = inc(t₁, 0) = b_L(d)` rests on SubspaceConventionAxiom's `s_L = s_C + 1 = 2`, which the present ASN fixes globally. For the *subsequent-link case*, K.λ emits `ℓ = inc(prev, 0)` (TA5(c)) under the same `d`, extending the inductive chain of `prev` by one additional step `kₙ₊₁ = 0`; the structural inc-chain property is preserved. All other transitions hold L in frame, so existing entries' chains persist. ∎
- *L-fin (Link store finiteness)* — `|dom(L)| < ∞`: base `|dom(L₀)| = 0 < ∞`. K.λ extends dom(L) by exactly one address (a finite extension preserves finiteness); all other transitions hold L in frame (`L' = L` preserves `|dom(L')| = |dom(L)| < ∞`). Composing over a finite sequence of valid composites yields `|dom(L)| < ∞` at every reachable state.
- *D-SEQ★ (Per-subspace lex-sequential range)* — derived above in the Per-subspace amendment to D-SEQ section from D-CTG★, D-MIN★, S8-depth, S8-fin, and S8a, all of which are elementary-preserved. D-SEQ★ at each reachable state follows by the same derivation applied at that state.
- *NodeLineage* `(A e ∈ E : IsNode(e) : n₀ ≼ e)` — base case: `E₀ = {n₀}` with `n₀ ≼ n₀` by reflexivity of the tumbler-prefix order. Inductive step: only K.δ extends E. K.δ case (i) — `IsNode(e)` — has `n₀ ≼ e` as an explicit precondition, discharged by NodeUniqueAllocation clause (b) (the registry's bootstrap-lineage condition supplies `n₀ ≼ e` directly at every node-allocation event), and the inductive hypothesis carries `n₀ ≼ e'` for every prior node `e' ∈ E ⊆ E'`. K.δ case (ii) — `¬IsNode(e)` — adds a non-node entity, leaving the universal quantification over nodes unchanged: existing nodes retain their lineage by inductive hypothesis, and the freshly added non-node falls outside the quantifier scope. All other elementary transitions hold E in frame, so the node set is unchanged and the quantifier ranges over the same nodes with the same prefix relationships. NodeLineage therefore holds at every reachable state.

**Class (b): Composite invariants** — discharged at composite boundaries by the J0/J1★/J1'★ couplings of ValidComposite★. These are: P4★, P4a, and P7a.

P4★ (`Contains_C(Σ) ⊆ R`): For each `(a, d) ∈ Contains_C(Σ') \ Contains_C(Σ)`, J1★ at the composite boundary requires `(a, d) ∈ R'`. K.μ⁺_L adds only link-subspace V-positions (excluded from Contains_C); K.μ⁻ can only shrink Contains_C; K.μ~ preserves Contains_C exactly; all other transitions hold M in frame.

P4a (`(A (a, d) ∈ R :: (E Σ_k in the transition history : (E v ∈ dom(M_k(d)) : subspace(v) = s_C ∧ M_k(d)(v) = a)))`): For `(a, d) ∈ R' \ R`, J1'★ supplies `v ∈ dom(M'(d))` with `subspace(v) = s_C ∧ M'(d)(v) = a`, so Σ' itself witnesses; for `(a, d) ∈ R`, the inductive hypothesis supplies a prior witnessing state Σ_k and P2 carries the entry into R'. All other transitions hold R in frame.

P7a (`(A a ∈ dom(C) :: (E d :: (a, d) ∈ R))`): For `a ∈ dom(C') \ dom(C)`, J0 supplies `d` with `a ∈ ran(M'(d))` at a content-subspace V-position (forced by the K.μ⁺ amendment, with K.μ⁺ following K.α in the elementary sequence by referential integrity); J1★ then supplies `(a, d) ∈ R'`. No transition removes from dom(C) (P0) or from R (P2), so P7a, once established, persists.

Coupling constraints J0, J1★, J1'★ hold for all valid composites by the analysis in the Scoped coupling constraints section.

**Per-transition invariant** (ExtendedTransitionInvariants: P3). P3 is the conjunction P0 ∧ P1 ∧ P2 ∧ L12; discharging each conjunct discharges P3.

- *P0.* K.α extends dom(C) at `a ∉ dom(C)` without modifying existing entries; all other elementary transitions hold C in frame.
- *P1.* K.δ extends E; all others hold E in frame.
- *P2.* K.ρ extends R; all others hold R in frame.
- *L12.* K.λ extends dom(L) at `ℓ ∉ dom(L)` without modifying existing entries; all other elementary transitions hold L in frame.

Each conjunct therefore holds across every elementary step; transitivity of inclusion and equality over a finite composite sequence gives P3 at the composite boundary. ∎


## Temporal decomposition

The state Σ = (C, L, E, M, R) decomposes into three temporal layers: an *existential* layer (C, L, E) that admits only growth and per-entry immutability; a *historical* layer (R) that admits only growth and may become stale relative to current arrangements; and a *presentational* layer (M) that is freely mutable. Cross-layer bridges (defined in *Cross-layer invariants* above): P6 and L1a tie C and L to E; S3★ bridges M to {C, L}; P7/P7a bridge C and R; CL-OWN constrains the M→L bridge to a document's own links; P4★ bridges presentational and historical layers via Contains_C(Σ) ⊆ R.

| Layer | Components | Mutability | Transitions modifying this component |
|-------|-----------|------------|----------------------|
| Existential (functional) | C, L | Append-only domain; values immutable | K.α, K.λ |
| Existential (set) | E | Append-only membership; no value structure | K.δ |
| Historical | R | Append-only, entries may stale | K.ρ |
| Presentational | M | Fully mutable | K.μ⁺, K.μ⁺_L, K.μ⁻ (elementary); K.μ~ (named composite, K.μ⁻ + K.μ⁺) |


## Properties Introduced

### New properties introduced by this ASN

| Label | Statement |
|-------|-----------|
| Σ.E | E ⊆ {t : ValidAddress(t) ∧ zeros(t) ≤ 2} — entity addresses, partitioned by IsNode / IsAccount / IsDocument |
| Σ.R | R ⊆ T_elem × E_doc — provenance relation recording historical content associations |
| Σ₀ | Initial state: C₀ = ∅, E₀ = {n₀} (bootstrap node), M₀(d) = ∅ for all d, R₀ = ∅ |
| parent(e) | For ¬IsNode(e): tumbler obtained by truncating last field and preceding separator |
| Contains(Σ) | {(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))} — current containment, derived quantity of state |
| Contains_C(Σ) | `{(a, d) : d ∈ E_doc ∧ (E v : v ∈ dom(M(d)) ∧ subspace(v) = s_C : M(d)(v) = a)}` — content-scoped containment |
| Valid composite | Σ → Σ' valid iff: (1) elementary preconditions at each intermediate state, (2) J0/J1/J1' for the composite; P0/P1/P2 derived as lemma |
| K.α | Content allocation — extend dom(C) with fresh address a at value v; precondition: IsElement(a), origin(a) ∈ E_doc, a ∉ dom(C), a ∉ dom(L), a produced by origin(a)'s content sub-allocator; effect C' = C ∪ {a ↦ v}; frame holds E, M, R |
| K.δ | Entity creation — extend E with fresh entity; precondition: parent(e) ∈ E when ¬IsNode(e); empty arrangement if IsDocument |
| K.μ⁺ | Arrangement extension — extend dom(M(d)) for d ∈ E_doc with new V→I mappings, preserving existing values; co-amended with content-subspace partitioning at the extended-state introduction (see Local extensions block) |
| K.μ⁻ | Arrangement contraction — remove existing V→I mappings from some d ∈ E_doc, with surviving mappings unchanged: dom(M'(d)) ⊂ dom(M(d)) ∧ (A v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v)); per-subspace admissible removal pattern is suffix truncation (empty, proper, or full), with at least one subspace contracting strictly; frame holds C, L, E, R, other documents |
| K.μ~ | Arrangement reordering — named composite K.μ⁻ + K.μ⁺ (not a primitive transition) realising a bijection π : dom(M(d)) → dom(M'(d)) with M'(d)(π(v)) = M(d)(v); subspace-preserving with link-subspace fixity (π(v) = v for v ∈ dom_L); derived frame holds C, L, E, R, other documents |
| K.λ | Link allocation — extend dom(L) with fresh address ℓ at value (F, G, Θ); precondition: d ∈ E_doc, ℓ ∉ dom(L) ∪ dom(C), zeros(ℓ) = 3, subspace_I(ℓ) = s_L, #E(ℓ) ≥ 2, origin(ℓ) = d, ℓ is produced by d's link sub-allocator (first emission [d.0.s_L.1] via SubAllocatorAxiom; subsequent inc(·, 0) on the frontier via TA5(c)), (F, G, Θ) ∈ Link with Θ ≠ ∅; effect L' = L ∪ {ℓ ↦ (F, G, Θ)}; frame holds C, E, M, R |
| K.ρ | Provenance recording — extend R with (a, d) pair where IsElement(a) ∧ a ∈ dom(C) |
| K.μ⁺_L | Elementary transition: link-subspace arrangement extension, M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}, origin(ℓ) = d, ℓ ∉ ran(M(d)) (first-arrangement) |
| K.μ~-FIX | Domain fixity under K.μ~: dom(M'(d)) = dom(M(d)), making π a permutation of a fixed domain — from D-SEQ + bijection cardinality + subspace preservation |
| J0 | **Axiomatic** (alongside SubspaceConventionAxiom, NodeUniqueAllocation, SubAllocatorAxiom, NoDeallocation, S0): content allocation (K.α) always co-occurs with arrangement extension (K.μ⁺); not derived from foundation. P7a depends on it. J0 and J1 are independent couplings — J0 couples K.α with K.μ⁺ (placement requirement); J1 is *derived* by wp from the requirement to preserve P4 (`Contains(Σ) ⊆ R`), not from J0 |
| J1 | Arrangement extension (K.μ⁺) must co-occur with provenance recording (K.ρ), derived by wp |
| J1' | (a, d) ∈ R' \ R only when a ∈ ran(M'(d)) \ ran(M(d)) — new provenance requires new containment |
| J2 | K.μ⁻ as elementary transition requires no coupling: C' = C ∧ E' = E ∧ R' = R |
| J3 | K.μ~ as named composite requires no coupling: C' = C ∧ E' = E ∧ R' = R |
| J4 | Fork composite: K.δ + K.μ⁺ + K.ρ (no other steps); precondition V_{s_C}(d_src) ≠ ∅; dom(C') = dom(C) follows from frames; provenance from J1; content-subspace-empty source is ex nihilo (K.δ), not fork |
| P1 | Entity set is monotonically growing: E ⊆ E' for every transition, uniformly across levels |
| P2 | Provenance relation is monotonically growing: R ⊆ R' for every transition |
| P4 | Provenance bounds: Contains(Σ) ⊆ R, with stale entries possible from prior states |
| P4a | Historical fidelity: every (a, d) ∈ R has a witnessing state where a ∈ ran(M(d)) |
| P6 | Existential coherence: origin(a) ∈ E_doc for all a ∈ dom(C) |
| P7 | Provenance grounding: a ∈ dom(C) for all (a, d) ∈ R |
| P7a | Provenance coverage: (E d :: (a, d) ∈ R) for all a ∈ dom(C) — every I-address has provenance |
| P8 | Entity hierarchy: (A e ∈ E : ¬IsNode(e) : parent(e) ∈ E) — no orphan accounts or documents |
| SequentialTransitionAxiom | Axiom (SequentialAtomicTransitions): the transition relation `Σ → Σ'` is single-event sequential — each transition is an atomic, uninterruptible event in which the elementary precondition is evaluated against `Σ` and the elementary effect is committed to `Σ'` in one indivisible step, and transitions are totally ordered. Equivalently, the system admits no intermediate state in which a transition has begun but not yet committed |
| SubspaceConventionAxiom | Axiom (FixedSubspaceIdentifiers): `s_C = 1 ∧ s_L = 2`. Pins the subspace identifier values used by Nelson (LM 4/30–4/31) and reproduced in udanax-green (xanadu.h:144–146; granf2.c:162; do2.c:94). The consequence `SC-NEQ ≡ s_C ≠ s_L` (1 ≠ 2) is the structural precondition for every disjointness argument in this ASN |
| LinkVPositionDepthAxiom | Axiom (FixedLinkVPositionDepth): `(A d ∈ E_doc :: m_L = 2)` — every link-subspace V-position has depth 2. Pins the link-subspace V-position depth to the value used by Nelson (LM 4/31) and reproduced in udanax-green (do2.c:151–167) |
| NodeUniqueAllocation | Axiom: every K.δ node-allocation event produces (a) e ∉ E (freshness, closing the GlobalUniqueness chain for nodes where T10a does not apply) and (b) n₀ ≼ e (bootstrap lineage, supplying K.δ case (i)'s lineage precondition and inductively preserving NodeLineage). The two conditions the node-allocation registry must satisfy |
| NodeLineage | Derived per-state invariant: `(A e ∈ E : IsNode(e) : n₀ ≼ e)` — every node in E descends structurally from the bootstrap node n₀ by tumbler-prefix relation. Discharged inductively from the base case `E₀ = {n₀}` (reflexivity) and the K.δ case (i) precondition `n₀ ≼ e` |
| GlobalLineage | Derived corollary: `(A x ∈ E ∪ dom(C) ∪ dom(L) :: n₀ ≼ x)` — every entity, content address, and link address descends from n₀ under tumbler-prefix order. Promotes NodeLineage to the full docuverse via P8 + P6 + L1a + L1c + transitivity of ≼ |
| SubAllocatorAxiom | Axiom (ContentLinkSubAllocatorExistence): for each d ∈ E_doc, the entity-allocation event placing d into E_doc simultaneously establishes two disjoint sub-allocators under d — a content sub-allocator with anchor `b_C(d) = [d.0.s_C]` and a link sub-allocator with anchor `b_L(d) = [d.0.s_L]` — each providing a forward-allocation frontier whose namespace property closes the uniqueness chain for K.α (content first-emit) and K.λ (link first-emit) |
| b_C(d), b_L(d) | Virtual sub-allocator anchors under d: `b_C(d) = [d.0.s_C]`, `b_L(d) = [d.0.s_L]` — single-component element-field bases, not in dom(C) ∪ dom(L), serving as formal starting points for the content and link allocator chains under d |
| Allocator hierarchy | Content and link sub-allocators are sibling element-field allocators under d, sharing prefix `[d.0]`; T10a-conformance applies to each frontier separately; cross-document collisions prevented by T10, cross-subspace by L14 + SC-NEQ + T7 |
| S3★-aux | Subspace exhaustiveness: `(A d, v : v ∈ dom(M(d)) : subspace(v) = s_C ∨ subspace(v) = s_L)` in every reachable state |
| CL-OWN | LinkSubspaceOwnership: `(A d, v : v ∈ dom(M(d)) ∧ subspace(v) = s_L : origin(M(d)(v)) = d)` — every document's link subspace contains only its own links |
| CL-UNIQ | LinkSubspacePositionUniqueness: `(A d, v₁, v₂ ∈ dom(M(d)) : subspace(v₁) = subspace(v₂) = s_L ∧ M(d)(v₁) = M(d)(v₂) : v₁ = v₂)` — each link occupies exactly one V-position in its home document's link subspace; injectivity of M(d)\|_{dom_L}. Closes the K.μ~ link-subspace identity precondition derivation |

### Local extensions and strengthenings of foundation properties

| Label | Statement | Foundation source |
|-------|-----------|--------------------|
| P0 | Content store is append-only with immutable values: dom(C) ⊆ dom(C') ∧ C'(a) = C(a) for a ∈ dom(C) | Subsumes ASN-0036's S0 (ContentImmutability) and S1 (StoreMonotonicity) into a single unified statement |
| L0 | SubspacePartition: `dom(L)` addresses have `subspace_I(a) = s_L`; `dom(C)` addresses have `subspace_I(a) = s_C` | L-clause from ASN-0043's L0 (SubspacePartition); the C-clause is the new content-side companion required by the extended state |
| L3 | TripleEndsetStructure: `(A a ∈ dom(L) :: L(a) = (F, G, Θ) where F, G, Θ ∈ Endset ∧ Θ ≠ ∅)` — local extension of ASN-0043's L3 fixing arity at exactly three; non-empty type endset preserved from foundation | ASN-0043's L3 (NEndsetStructure) admits arity ≥ 3; this ASN fixes arity at exactly three |
| L14 | StoreDisjointness: `dom(C) ∩ dom(L) = ∅` — unscoped store disjointness derived from L0 (with the C-clause introduced here) and SC-NEQ via T7 | Strengthens ASN-0043's L14 (DualPrimitive, scoped under `s_C`-resident content as `dom(L) ∩ dom(C)\|_{s_C} = ∅`) to the unscoped form, made available by this ASN's K.α amendment which forces every `a ∈ dom(C)` to be `s_C`-resident |
| L14a | Superseded by S3★ + CL-OWN in the extended state: S3★ routes every link-subspace V→I mapping to dom(L), and CL-OWN forces home-document ownership at each such mapping | ASN-0043's L14a (NonTranscludability) is implied by S3★ + CL-OWN and not separately stated in the extended state |
| L1c (structural inc-chain) | Local weakening of ASN-0043's L1c: every `ℓ ∈ dom(L)` is reachable from a T4-valid document-level seed `s` (zeros(s) = 2) by a *structural inc-chain* — per-step inc-rule conformance (each step `tᵢ = inc(tᵢ₋₁, kᵢ)` with `kᵢ ∈ {0, 1, 2}` satisfying TA5's structural preconditions; length monotonicity `#tᵢ > #s`) — *not* full T10a discipline including allocator-frontier domain tracking. The anchor traversal `d → b_C(d) → b_L(d) → [d.0.s_L.1]` and the first link emission inhabit no T10a-tracked allocator domain; their activation discharge goes through SubAllocatorAxiom rather than T10a's T2 spawning rule. T10a's full discipline applies only to subsequent emissions on the activated A_L(d) frontier. | Weakens ASN-0043's L1c (LinkAllocatorConformance, "operates within a system conforming to T10a") to per-step inc-rule conformance, with the activation-discharge gap bridged by SubAllocatorAxiom |
| S3★ | Subspace-conditional referential integrity: text → dom(C), link → dom(L); supersedes S3 | ASN-0036's S3 (ReferentialIntegrity) is single-store; this ASN partitions the target by subspace |
| D-CTG★ | Per-subspace contiguity: `(A d, S : V_S(d) ≠ ∅ : V_S(d) is contiguous under the V-ordering on subspace S)` — local strengthening of ASN-0036's D-CTG dropping the link-subspace exemption; supersedes D-CTG within the extended state | ASN-0036's D-CTG (Contiguity) had a link-subspace exemption |
| D-MIN★ | Per-subspace minimum position: `(A d, S : V_S(d) ≠ ∅ : min(V_S(d)) = [S, 1, ..., 1] of depth m_S)` — local strengthening of ASN-0036's D-MIN dropping the link-subspace exemption; supersedes D-MIN within the extended state | ASN-0036's D-MIN (MinimumPosition) had a link-subspace exemption |
| D-SEQ★ | Per-subspace lex-sequential range: for each non-empty subspace S in M(d), `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` of uniform depth m_S — derived from D-CTG★ + D-MIN★ + S8-depth + S8-fin + S8a, per-subspace promotion of ASN-0036's D-SEQ to a system-wide invariant of the extended state | ASN-0036's D-SEQ (LexSequential) was per-document; this ASN promotes per-subspace and elevates to system-wide invariant |
| P3 | No component other than M — specifically C, L, E, R — admits contraction or reordering; quantitative monotonicity formalised as `dom(C) ⊆ dom(C') ∧ dom(L) ⊆ dom(L') ∧ E ⊆ E' ∧ R ⊆ R' ∧ (A a ∈ dom(C) :: C'(a) = C(a)) ∧ (A ℓ ∈ dom(L) :: L'(ℓ) = L(ℓ))` | Synthesises this ASN's P0 (subsuming ASN-0036's S0/S1), P1 (specialising ASN-0034's T8), and P2 with ASN-0043's L12 — combined with the qualitative mode-enumeration "no contraction or reordering on C, L, E, R" |
| P4★ | `Contains_C(Σ) ⊆ R` — provenance bounds scoped to content subspace; supersedes P4 | This ASN's own P4 with subspace scoping |
| J1★ | Range-based content-subspace scoping of J1: provenance recording for I-addresses new to content-subspace range | This ASN's own J1 with subspace scoping |
| J1'★ | Range-based content-subspace scoping of J1': provenance entries only from content-subspace range changes | This ASN's own J1' with subspace scoping |
| ValidComposite★ | Valid composite in extended state: transition preconditions at each step (K.μ~ as shorthand for K.μ⁻ + K.μ⁺) + J0, J1★, J1'★ at composite boundary; supersedes ValidComposite | This ASN's own Valid composite definition extended for the two-subspace state |
| S8★ | Per-subspace span decomposition: for each d ∈ E_doc and each subspace S ∈ {s_C, s_L}, M(d)\|_{V_S(d)} decomposes into a finite set of correspondence runs satisfying ASN-0036's S8 conditions (a) and (b) on the per-subspace projection — content-subspace projection by ASN-0036's S8 directly, link-subspace projection by trivial length-1 decomposition | ASN-0036's S8 is stated under S3 (single store), failing on the unprojected M(d) once link-subspace V-positions target dom(L); S8★ restores S8 per-subspace using S3★'s per-subspace clauses |
| ExtendedReachableStateInvariants | Every reachable state satisfies S2 ∧ S3★ ∧ S3★-aux ∧ S4 ∧ S7a–S7d ∧ S8a ∧ S8-fin ∧ S8-depth ∧ S8★ ∧ D-CTG★ ∧ D-MIN★ ∧ D-SEQ★ ∧ P4★ ∧ P6–P8 ∧ L0 ∧ L1 ∧ L1a ∧ L1b ∧ L1c ∧ L3 ∧ L14 ∧ L-fin ∧ CL-OWN ∧ CL-UNIQ (per-state). P3 (which packages P0, P1, P2, L12) and S9 are *per-transition*: see ExtendedTransitionInvariants. Together supersedes ReachableStateInvariants | This ASN's own Reachable-state invariants synthesis extended to the two-subspace state |
| ExtendedTransitionInvariants | Every valid composite transition Σ → Σ' satisfies P3, the conjunction P0 ∧ P1 ∧ P2 ∧ L12 (which subsumes ASN-0036's S0 and S1 via P0 and extends ASN-0043's L12). S9 follows from P0 | This ASN's own per-transition synthesis |
| K.α amendment | Content-subspace restriction (`subspace_I(a) = s_C`); preserves L0 clause 2 and L14 in the extended state | Strengthening of this ASN's K.α (defined in *Elementary transitions* above) at the extended-state introduction |
| K.μ⁺ amendment | Content-subspace restriction (`subspace(v) = s_C`); existing D-CTG/D-MIN postconditions carry forward; partitions arrangement extension by subspace with K.μ⁺_L | Strengthening of this ASN's K.μ⁺ (defined in *Elementary transitions* above) at the extended-state introduction |
| K.μ⁻ (per-subspace scope) | The per-subspace D-CTG★/D-MIN★ postconditions stated at K.μ⁻'s definition apply to each subspace independently; valid contractions per-subspace are per-subspace suffix removals or full clearances (per the K.μ⁻ exhaustiveness lemma) | ASN-0036's K.μ⁻ stated D-CTG/D-MIN with a link-subspace exemption; the per-subspace amendments D-CTG★/D-MIN★ above carry through K.μ⁻'s postconditions to two subspaces |

## Open Questions

- What invariants must a forked document's initial arrangement satisfy with respect to its source's current arrangement — must it be identical, or may it be a proper subset?
- What guarantees must the system provide about provenance when content is transitively shared through chains of transclusion?
- Can arrangement contraction on one document affect the discoverability of links attached to the same I-addresses from another document?
- What relationship must hold between a document's version lineage and its sequence of arrangement transitions?
- What additional permanence properties must the provenance relation satisfy for content that participates in link endsets?
- What invariants must the link subspace satisfy beyond those inherited from D-CTG, D-MIN, and S8-depth — are there link-specific ordering constraints, capacity bounds, or structural properties that D-SEQ does not capture?
- Must the system guarantee that a fresh link address is always available within a document's link subspace, or can link allocation fail due to address space exhaustion?
- What must the system guarantee when concurrent operations target the same home document — must link address allocation be serialized, or can concurrent allocations produce distinct addresses without coordination?
- What is the minimal protocol that a node-allocation registry must implement to satisfy NodeUniqueAllocation? Nelson's design specifies a contractual single root authority (LM 4/17–4/22) delegating recursively under the owned-numbers principle; Gregory's implementation realises this as a single global granfilade with query-and-increment dispatch (the granfilade tree serving as the registry, append-only by L1c/T10a discipline, with single-threaded sequential execution eliminating races). Whether a future ASN should specify the registry mechanism in abstract form (issuing protocol, persistence model, concurrency discipline) or whether NodeUniqueAllocation is the right abstraction boundary for the docuverse layer is left open.
- What invariants must a separate link-withdrawal mechanism (status flag, tombstone marker, or explicit retraction link) maintain in order to reconcile Nelson's tombstoning design (LM 4/9) with D-CTG★ / D-MIN★? Under D-CTG★/D-MIN★ this ASN's K.μ⁻ admits only link-subspace suffix truncations, so withdrawing an interior link requires withdrawing every link allocated after it; tombstoning would require a mechanism outside K.μ⁻'s presentational-removal contract.
- Should the entity-allocation discipline admit account-level depth-1 tumbler extension (K.δ with `k = 1` and `IsAccount(t)`), producing an account-shaped sibling at the same hierarchy level as t? The present ASN excludes this at the precondition, citing the consultation evidence that versioning is reserved to documents (Nelson, LM 4/29; Gregory, `docreatenewversion` for DOCUMENT→DOCUMENT only). The structural form `[N, 0, U, 1]` is itself well-typed (still `IsAccount`) under T4b, and admitting it would not violate any per-state invariant of the present model (the k = 1 harmlessness verification for documents would carry across); but no role for such an entity is documented in the design or implementation. The question is whether a future extension (e.g., account renaming, multi-account user identity) would require admitting account-level depth-1 extension; if so, the precondition restriction here can be relaxed without further structural reorganisation.
