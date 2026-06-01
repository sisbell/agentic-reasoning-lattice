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
- `#E(a)` (ASN-0034): the depth (component count) of the element-field projection `E(a)` supplied by T4b — i.e. `#a` minus the length of the node/user/document prefix together with its three zero separators.

*V-position (arrangement-domain) projections.* For each `v ∈ dom(M(d))`:

- `subspace(v)` (ASN-0036): the first component `v₁` of the V-position tumbler — the subspace identifier at the V-position level. By S8a, every `v ∈ dom(M(d))` satisfies `v₁ ≥ 1`, so `subspace(v) ∈ ℕ⁺`. In this ASN the two subspaces are `s_C` (content/text) and `s_L` (link), with `s_C ≠ s_L` (SC-NEQ axiom, introduced here).
- `#v` (ASN-0034): the depth of v. By S8-depth, V-positions within a fixed subspace under a fixed document share a common depth `m_S`.

*Entity-hierarchy projections.* For each non-node entity `e ∈ E`:

- `parent(e)` (introduced here, §The state model): the tumbler obtained by truncating e's last field together with its preceding zero separator. `parent(e)` is the entity-hierarchy spine — defined only for non-node entities (`¬IsNode(e)`), and producing a valid address at the next-higher level: `zeros(parent(e)) = zeros(e) − 1`.

*Subspace-position correspondence.* For `v ∈ dom(M(d))` with `M(d)(v) = a`, `subspace(v) = subspace_I(a)` (S3★). The two projections apply at different state-component levels — `subspace(v)` projects V-positions, `subspace_I(a)` projects I-addresses.

*Content/link domain notation.* `dom_C(M(d)) := V_{s_C}(d) := {v ∈ dom(M(d)) : subspace(v) = s_C}`; symmetrically `dom_L(M(d)) := V_{s_L}(d) := {v ∈ dom(M(d)) : subspace(v) = s_L}`. The `V_S(d)` form generalises to any subspace S; both spellings appear in this ASN denotationally identically.

*Entity-level allocator.* A T10a-tracked sub-allocator whose output addresses satisfy `zeros(·) ≤ 2`: node, account, document, and version sub-allocators.

*Set-inclusion notation.* Throughout this ASN, `⊂` and `⊃` denote *proper* (strict) subset and superset respectively — `A ⊂ B ≡ A ⊆ B ∧ A ≠ B`, and `A ⊃ B ≡ B ⊂ A`. The non-strict relations are written `⊆` and `⊇`.


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

> **Σ = (C, L, E, M, R)**

where C : T ⇀ Val is the content store (per ASN-0036), L : T ⇀ Link is the link store, and M : T → (T ⇀ T) is total, satisfying M(d) = ∅ for d ∉ E_doc.

**Definition (Initial state).** The initial state Σ₀ = (C₀, L₀, E₀, M₀, R₀) is:

- C₀ = ∅ (no content allocated)
- L₀ = ∅ (no links allocated)
- E₀ = {n₀} where n₀ = `[1]` — the canonical single-component bootstrap node
- M₀(d) = ∅ for all d — (E₀)_doc = ∅, so every arrangement is the empty partial function
- R₀ = ∅ (no provenance recorded)

**Structural form of n₀.** The bootstrap node is fixed as `[1]` — a one-element tumbler with `zeros(n₀) = 0`, satisfying `IsNode(n₀)` and `ValidAddress(n₀)`. The NodeLineage invariant (`n₀ ≼ e`) constrains every node address to extend `[1]` by prefix, ruling out disconnected-forest allocations.

**Initial state invariant verification.** Each Class (a) per-state invariant of ExtendedReachableStateInvariants holds at Σ₀, most vacuously. We enumerate the verifications to make the base case of the inductive proof explicit:

- *Entity invariants.* `E₀ = {n₀}` with `IsNode(n₀)`, `ValidAddress(n₀)` (`[1]` is T4-valid), and `zeros(n₀) = 0` (no separators). The exclusion `(A e ∈ E :: ¬IsElement(e))` holds since `zeros(n₀) = 0 ≠ 3`.
- *NodeLineage* `(A e ∈ E₀ : IsNode(e) : n₀ ≼ e)`: instantiates at `e = n₀`, requiring `n₀ ≼ n₀`, which holds by reflexivity of the tumbler-prefix order.
- *P8 (Entity hierarchy)* `(A e ∈ E₀ : ¬IsNode(e) : parent(e) ∈ E₀)`: vacuously satisfied — `n₀` is the only entity in `E₀` and `IsNode(n₀)`, so the quantifier scope is empty.
- *S7d (Document allocation discipline)*: `(E₀)_doc = ∅`, vacuous.
- *S2, S3★, S3★-aux, S8a, S8-depth, S8-fin, S8★, D-CTG★, D-MIN★, D-SEQ★*: `M₀(d) = ∅` for all `d`, so `dom(M₀(d)) = ∅` and `V_S(d) = ∅` for every subspace `S`. Each invariant holds vacuously over the empty arrangement domain.
- *S4, S7a, S7b, C1b (content invariants)*: `dom(C₀) = ∅`, vacuous.
- *C-fin (Content store finiteness)*: `|dom(C₀)| = |∅| = 0 < ∞`. ✓
- *P6 (Existential coherence)*: `dom(C₀) = ∅`, vacuous.
- *L0, L1, L1a, L1b, L1c, L3, L14, L-fin*: `dom(L₀) = ∅`, vacuous. L-fin: `|∅| = 0 < ∞`. L14: `dom(C₀) ∩ dom(L₀) = ∅ ∩ ∅ = ∅`.
- *CL-OWN, CL-UNIQ*: no link-subspace V-positions exist in `M₀` (the arrangements are empty), so both quantifiers have empty scope.
- *P7 (Provenance grounding)*: `R₀ = ∅`, vacuous.

The Class (b) composite-boundary properties at Σ₀:

- *P4★* `Contains_C(Σ₀) ⊆ R₀`: `Contains_C(Σ₀) = ∅ ⊆ ∅ = R₀`. ✓
- *P4a (Historical fidelity)*: `R₀ = ∅`, vacuous.
- *P7a (Provenance coverage)*: `dom(C₀) = ∅`, vacuous.

This closes the inductive base for ExtendedReachableStateInvariants; the inductive step is the per-elementary verification in the proof body.

**SequentialTransitionAxiom (Axiom, SequentialAtomicTransitions; per ASN-0093).** The transition relation `Σ → Σ'` is single-event sequential: each transition is an atomic, uninterruptible event in which the elementary precondition is evaluated against `Σ` and the elementary effect is committed to `Σ'` in one indivisible step, and transitions are totally ordered (no two transitions overlap in time). Equivalently, the system admits no intermediate state in which a transition has begun but not yet committed. The axiom is taken from ASN-0093 directly.

**Notation.** Throughout this ASN, `Σ → Σ'` denotes a single atomic transition (one elementary K.* event). The reflexive-transitive closure `Σ →* Σ'` denotes a finite (possibly empty) sequence of atomic transitions `Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ'`; the valid such sequences are characterised by ValidComposite★ below. Per-transition predicates stated over `Σ → Σ'` (P0, P1, P2, L12, P3) hold at every atomic step and lift to every composite by transitivity of inclusion and equality. Coupling constraints (J0, J1, J1', J1★, J1'★) are stated over composites `Σ →* Σ'`; they bind initial and final states across a valid composite, not individual atomic steps.


## Link store and extended system state

This ASN uses properties of the link store. For self-containment, we restate the definitions and invariants needed.

**Definition (Endset).** An *endset* is a finite set of well-formed spans: `Endset = 𝒫_fin(Span)`, where `Span` is the set of well-formed span pairs `(s, ℓ)` satisfying T12 (ASN-0034). The empty set ∅ is a valid endset — `∅ ∈ 𝒫_fin(Span)` trivially — matching ASN-0043's `Endset` definition.

**Definition (Link).** A *link value* is a finite sequence of N ≥ 3 endsets, with the third slot designated as the type endset: `Link = {(e₁, ..., eₙ) : N ≥ 3, each eᵢ ∈ Endset}`. `|L|` denotes the *arity* — the number of endsets in the sequence. Following the **StandardTriple convention** (ASN-0043), the standard link form has arity 3 and is written `(F, G, Θ)` — slot 1 as the *from-endset* `F`, slot 2 as the *to-endset* `G`, and slot 3 as the *type-endset* `Θ`. The triple convention is applied in worked examples of this ASN for narrative continuity; it is not a structural restriction on the link store.

**Definition (Subspace identifiers).** We write `s_C` for the content subspace identifier and `s_L` for the link subspace identifier. These are the first components of the element field for content and link addresses respectively: `subspace_I(a) = s_C` for content addresses, `subspace_I(ℓ) = s_L` for link addresses. The same identifiers serve for V-positions: `subspace(v) = v₁`.

**SubspaceConventionAxiom (Axiom, FixedSubspaceIdentifiers; per ASN-0093).** `s_C = 1 ∧ s_L = 2`. The distinctness consequence `s_C ≠ s_L` is abbreviated **SC-NEQ**. The axiom is taken from ASN-0093 directly.

The unscoped disjointness `dom(C) ∩ dom(L) = ∅` is established in the foundation as **SD (StoreDisjointness, ASN-0093)**. It is restated as L14 below, with its derivation cited from ASN-0093.

We note that `s_C ≥ 1` follows from S7b and T4: content I-addresses are element-level by S7b (`zeros(a) = 3`), and T4 requires every element-field component to be strictly positive, so `subspace_I(a) = s_C > 0`. The same derivation gives `s_L ≥ 1`: link I-addresses are element-level by L1 below (`zeros(ℓ) = 3`), so by T4, `subspace_I(ℓ) = s_L > 0`.

**L0 (SubspacePartition, per ASN-0093).** Both clauses are foundation invariants:

  `(A a ∈ dom(Σ.L) :: subspace_I(a) = s_L)`

  `(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)`

The L-clause is the original ASN-0043 form; the C-clause was added in ASN-0093 (foundation L0) and is supplied at allocation time by ASN-0093's K.α precondition `E(a)₁ = s_C`. No "introduced here" claim — both clauses are inherited.

**L1 (LinkElementLevel).**

  `(A a ∈ dom(Σ.L) :: zeros(a) = 3)`

Every link address is an element-level tumbler.

**L1a (LinkScopedAllocation).**

  `(A a ∈ dom(Σ.L) :: origin(a) ∈ E_doc)`

Every link address is allocated under the tumbler prefix of a document in E_doc.

**L3 (NEndsetStructure, per ASN-0093).**

  `(A a ∈ dom(Σ.L) :: |Σ.L(a)| ≥ 3 ∧ (A i : 1 ≤ i ≤ |Σ.L(a)| : Σ.L(a).eᵢ ∈ Endset) ∧ Σ.L(a).e₃ ≠ ∅)`

Every link is a sequence of at least three endsets, with the type endset (slot 3) non-empty. This is ASN-0093's L3 (itself inherited from ASN-0043's `Link` definition admitting arity `N ≥ 3`) restated for narrative continuity. Under the StandardTriple convention applied in worked examples, an arity-3 link is written `(F, G, Θ)` with `e₃ = Θ` the type endset.

*Semantics of empty endsets at slots 1 and 2.* L3 admits `e₁ = ∅` and `e₂ = ∅` independently — only `e₃` (the type endset) is required non-empty. Exactly one of `e₁`, `e₂` empty is Nelson's one-sided link case (LM 4/48); both empty is admissible as a type-only marker. Whether to narrow K.λ with a stricter `e₁ ∪ e₂ ≠ ∅` precondition is recorded as *design-uncertain* and left to a future operations ASN. Endset-iterating consumers (L8's `same_type`, discovery-set unions) treat an empty endset as contributing ∅ by the natural inductive form.

**L12 (LinkImmutability).**

  `(A Σ → Σ' : (A a : a ∈ dom(Σ.L) : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)))`

Once created, a link's address persists in dom(L) and its value is permanently fixed.

**L14 (StoreDisjointness).**

  `dom(Σ.C) ∩ dom(Σ.L) = ∅`

This is ASN-0093's SD (StoreDisjointness) restated; its derivation (L0 + SC-NEQ + StoreT4Validity + T7) is cited from ASN-0093, not re-proved here.

**L-fin (LinkStoreFiniteness).** `|dom(Σ.L)| < ∞`. Holds at Σ₀ (|∅| = 0); preserved by K.λ (single-element extension) and by L-frame in all other transitions.

All existing elementary transitions from ASN-0047 — K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.ρ — hold L in their extended-state frame: `L' = L`. Only K.λ extends L. L12 (LinkImmutability) follows trivially from this split: `L' = L` preserves dom(L) and values pointwise, and K.λ appends a fresh entry without altering existing ones.


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

**Frame convention for inherited transitions.** Inherited K.* transitions extend ASN-0093's frame with `E' = E ∧ R' = R`, since ASN-0093 has no E or R components.

**K.α (Content allocation).** Per ASN-0093 (foundation K.α, ContentAllocation): a fresh I-address is bound to a value in the content store. The precondition structure — `d ∈ E_doc` (home document exists; ASN-0093 writes this as `d ∈ dom(M)`, but under ASN-0047's totality framing where `M` is total with `M(d) = ∅` for `d ∉ E_doc`, `dom(M) = T` trivially and `d ∈ E_doc` is the substantive predicate), `a ∉ dom(C) ∪ dom(L)` (fresh address), `zeros(a) = 3 ∧ E(a)₁ = s_C` (element-level, content subspace), `#E(a) ≥ 2`, `origin(a) = d`, the first/subsequent emission cases producing `a` via d's content sub-allocator `A_C(d)`, and `v ∈ Val` — follows ASN-0093's K.α. The emission cases:

- *First emission* (predicate: `{a' ∈ dom(C) : origin(a') = d} = ∅`): `a = [d.0.s_C.1]`, the determinate first emission of `A_C(d)`.
- *Subsequent emission* (predicate: `{a' ∈ dom(C) : origin(a') = d} ≠ ∅`): `a = inc(max{a' ∈ dom(C) : origin(a') = d}, 0)` (TA5(c)), the next sibling on `A_C(d)`'s inc chain.

Freshness `a ∉ dom(C) ∪ dom(L)` in both cases is SubAllocFresh at `x = C` (lemma stated below, at *Allocator hierarchy under documents*).

*Effect:* `C' = C ∪ {a ↦ v}`.

*Frame:* `L' = L; E' = E; (A d :: M'(d) = M(d)); R' = R`.

**NodeLineage (Derived invariant, NodeDescentFromBootstrap).** `(A e ∈ E : IsNode(e) : n₀ ≼ e)`, where `≼` is the prefix order on tumblers (ASN-0034).

**NodeUniqueAllocation (Axiom, FreshNodeAddress).** Every K.δ node-allocation event — every elementary transition of K.δ whose effect places an entity `e` with `IsNode(e)` into E — produces an address satisfying three conditions: (a) *Freshness:* `e ∉ Σ.E` at the state Σ of allocation; (b) *Bootstrap lineage:* `n₀ ≼ e` under the tumbler-prefix order; (c) *Registry tracking:* for every reachable state Σ and every `t ∈ Σ.E_node`, `t` inhabits the external node-allocation registry's tracked domain.

**NodeRegistryBootstrap (Axiom, BootstrapRegistrySeeding).** At the initial state `Σ₀`, `n₀` is committed to the node-allocation protocol's tracked domain — a registry external to `Σ`, so `n₀` enters at `Σ₀` rather than via a prior K.δ event.

**FrontierEquivalence (Lemma).** For every reachable state `Σ` and every operand `t ∈ Σ.E` with `¬IsNode(t)`:

  `inc(t, 0) ∉ Σ.E ⟺ t is the frontier of its sub-allocator's (t, 0)-branch`

— i.e., the operational predicate "the `(t, 0)` increment has not yet been consumed" is logically equivalent to "no prior K.δ event has fired `(t, 0)` on `t`'s own sub-allocator chain." The term "frontier" is well-defined because, by T10a.7 (EnumerationInjectivity, ASN-0034), the chain map `n ↦ tₙ` is injective, so each chain index names a distinct address.

*Proof.* The biconditional decomposes into two implications, each proved separately.

*Forward direction (⟹).* Assume `inc(t, 0) ∉ Σ.E`. We show `t` is the frontier of its sub-allocator's `(t, 0)`-branch — i.e., no prior K.δ event has fired `(t, 0)` on `t`'s own sub-allocator chain. Argue by contrapositive: suppose for contradiction that some prior K.δ event *had* fired `(t, 0)`, producing the address `inc(t, 0)` and placing it into `E` at that earlier state. By TA5(c), `inc(t, 0)` is a single determinate address (functional determinism — the same operand-and-parameter pair always produces the same output). By P1 (E-monotonicity), any address once placed into E persists across every subsequent transition. So `inc(t, 0)` is in E at the present state Σ — contradicting the assumed `inc(t, 0) ∉ Σ.E`. Hence no prior firing of `(t, 0)` occurred on t's sub-allocator chain; t is the frontier.

*Reverse direction (⟸).* Assume `t` is the frontier of its sub-allocator's `(t, 0)`-branch — no prior K.δ event has fired `(t, 0)` on t's own sub-allocator chain. We show `inc(t, 0) ∉ Σ.E`. Suppose for contradiction `inc(t, 0) ∈ Σ.E`. Then some allocation event in the system history placed `inc(t, 0)` into E. By T10a GlobalUniqueness (via T10a.6 cross-allocator domain-disjointness), the address `inc(t, 0)` can be produced by exactly one allocator's tracked chain — namely t's own sub-allocator (since `inc(t, 0)` is, by TA5(c), the sibling-increment of t on its own chain, and T10a.6 forbids any other allocator's tracked domain from containing it). So the placing event was a K.δ event firing `(t, 0)` on t's own sub-allocator chain — contradicting the frontier assumption. Hence `inc(t, 0) ∉ Σ.E`.

Together, the two implications yield the biconditional `inc(t, 0) ∉ Σ.E ⟺ t is the frontier of its sub-allocator's (t, 0)-branch`. ∎

**K.δ (Entity creation).** A fresh entity address enters E with initial state:

`E' = E ∪ {e}` where `e ∉ E ∧ ValidAddress(e) ∧ ¬IsElement(e)`

*Precondition.* The precondition splits on `IsNode(e)`, reflecting two distinct allocation disciplines — protocol-established node baptism versus T10a-conforming inc-allocation under a parent entity.

- **Case (i) IsNode(e).** No operand `t` is consumed (`e` is supplied by the node-allocation protocol, not by inc). Required: `ValidAddress(e) ∧ IsNode(e) ∧ e ∉ E ∧ n₀ ≼ e`. Both the freshness conjunct `e ∉ E` and the bootstrap-lineage conjunct `n₀ ≼ e` are discharged by NodeUniqueAllocation — the protocol-established axiom — directly. The operational allocator is Nelson's hierarchical baptism / Gregory's single global granfilade with query-and-increment dispatch, outside T10a's standard discharge layer.
- **Case (ii) ¬IsNode(e).** `e = inc(t, k)` for some operand `t` and `k ∈ {0, 1, 2}`. The case-level "where"-clause conjuncts `e ∉ E ∧ ValidAddress(e) ∧ ¬IsElement(e)` apply uniformly to all three sub-cases; in particular, the freshness conjunct `e ∉ E` is discharged per sub-case by the discharge route detailed in §*K.δ case (ii) discharge and parent-allocator activation* below: T10a chain-advancement uniqueness at `(t, 0)` (FrontierEquivalence) at k = 0; T10a GlobalUniqueness on the parent allocator's tracked domain at k = 1 and k = 2. Required uniformly: `parent(e) ∈ E`. Per-sub-case additional requirements:
  - *k = 0 (sibling):* `t ∈ E ∧ ¬IsNode(t) ∧ inc(t, 0) ∉ E`. The operand-admissibility conjuncts are `t ∈ E` (the operand must be an allocated entity), `¬IsNode(t)` (so `parent(t)` is well-defined under T4b), and `inc(t, 0) ∉ E` (the operational frontier check, discharged below). The structural identities `parent(t) = parent(e)` and `zeros(t) = zeros(e)` hold by TA5(c) on `e = inc(t, 0)` (K.δ-ID.parent-0/1, K.δ-ID.zeros-0/1).
  - *k = 1 (version):* `t ∈ E_doc`. The operand must be an allocated document — only an existing document can be versioned. Nelson's CREATENEWVERSION operates on `<doc id>`, an allocated document (LM 4/66); Gregory's `docreatenewversion` retrieves the source's vspan via `doretrievedocvspanfoo`, which fails on a source not present in the granfilade. (`IsDocument(t)` follows from `t ∈ E_doc` by the definition of E_doc.) The operation is uniform across operand provenance — only the surface predicate `t ∈ E_doc` is checked at firing time, and the (a')/(b') dispatch on t's parent allocator (*Sub-allocator names* above) surfaces only in the T2-spawn verification, not in the operation itself.
  - *k = 2 (descent):* `t ∈ E ∧ zeros(t) ≤ 1` (equivalently, `IsNode(t) ∨ IsAccount(t)`). The zeros bound follows from the case-level precondition `¬IsElement(e)` (`zeros(e) ≤ 2`) combined with the structural identity `zeros(e) = zeros(t) + 1` (K.δ-ID.zeros-2). The structural identity `parent(e) = t` holds by TA5(d) on `e = inc(t, 2)` together with T4b's parent projection (K.δ-ID.parent-2).
  - Structural identities on `e = inc(t, k)` (consequences of TA5 + T4b's parent projection):
    - **K.δ-ID.zeros-0/1.** `zeros(e) = zeros(t)` for k ∈ {0, 1}. *Derivation:* TA5(c) preserves zeros for k = 0; TA5(d) at k = 1 appends a final `1` with no new zero, so zeros is preserved.
    - **K.δ-ID.zeros-2.** `zeros(e) = zeros(t) + 1` for k = 2. *Derivation:* TA5(d) at k = 2 appends one zero separator and a final `1`.
    - **K.δ-ID.parent-0/1.** `parent(e) = parent(t)` for k ∈ {0, 1}. *Derivation:* k = 0 leaves the trailing-component position unchanged; k = 1 extends by one non-zero component without crossing a zero separator; in either case T4b's truncation past the last separator yields the same prefix.
    - **K.δ-ID.parent-2.** `parent(e) = t` for k = 2. *Derivation:* k = 2 introduces a new zero separator immediately after t, making t itself the parent prefix under T4b.

    These four identities discharge the case-level requirement `parent(e) ∈ E` against the operand's own membership: combined with P8 at `t` for the k ∈ {0, 1} cases (giving `parent(e) = parent(t) ∈ E` by K.δ-ID.parent-0/1), and directly from `t ∈ E` for the k = 2 case (giving `parent(e) = t ∈ E` by K.δ-ID.parent-2).

*Rationale (k = 0 conjuncts).* The `¬IsNode(t)` conjunct is required for `parent(t)` to be defined — T4b's parent projection is partial on T and undefined when `IsNode(t)`. The freshness conjunct `inc(t, 0) ∉ E` is the case-level `e ∉ E` specialised to `e = inc(t, 0)` — stated locally to record that the caller's operand selection must observe it. Operationally, the conjunction `t ∈ E ∧ inc(t, 0) ∉ E` IS the frontier identification, by FrontierEquivalence. The frontier identification is therefore *derived* from the precondition pair, not an independent obligation; T4b's `parent`/`zeros`/length stratification cannot in general identify t as the frontier of its own sub-allocator, so the direct freshness predicate `inc(t, 0) ∉ E` is the load-bearing operand selector.

*Freshness discharge.* The `e ∉ E` precondition is discharged by case on the K.δ form: case (i) is closed by NodeUniqueAllocation (the node-allocation protocol's axiomatic uniqueness clause); case (ii) is closed by the parent-allocator route detailed in §*K.δ case (ii) discharge and parent-allocator activation* below. That section performs the case (ii) discharge once; it is not repeated here.

*Effect on M, per case.* When IsDocument(e): M'(e) = ∅ (empty arrangement), and M'(d') = M(d') for every d' ≠ e. When IsAccount(e) or IsNode(e): M'(d') = M(d') for every d' (by the totality convention M(e) = ∅ for e ∉ E_doc). The collective effect on M is therefore `(A d' : d' ≠ e : M'(d') = M(d'))` ∧ `M'(e) = ∅`.

*Subsumption of ASN-0093's K.σ.* When `IsDocument(e)`, K.δ subsumes ASN-0093's K.σ (DocumentRegistration). ASN-0093's K.σ has effect `dom(M') = dom(M) ∪ {d}` with `M'(d) = ∅`; under ASN-0047's totality framing this maps to placing `d` into `E_doc` (with `M'(d) = ∅` matching the totality convention for previously-empty documents). The K.δ case (ii) k = 2 event with `parent(e) ∈ E_account` (creating a document under an account) and the K.δ case (ii) k = 1 event with `t ∈ E_doc` (creating a version) are both routes by which an entity enters `E_doc`; either is the single atomic event that, under ASN-0093's vocabulary, would be reported as K.σ. Per ASN-0093's SubAllocatorAxiom, the same K.δ event that places `d` into `E_doc` is the *joint T2-spawn step* activating both `A_C(d)` and `A_L(d)` — captured under SubAllocatorAxiom.T10aConformance and elaborated in the *Allocator hierarchy under documents* section below. ASN-0047 therefore has no separate K.σ primitive; K.δ for `IsDocument(e)` is the consolidated entity-allocation, registry, and sub-allocator-activation event.

Nelson identifies two document-creation modes — ex nihilo and forking. At the elementary level, both begin with K.δ producing an empty document. When the source's content subspace is non-empty, forking is compound: K.δ followed by arrangement extension and provenance recording (J4 below). When the source's content subspace is empty, fork reduces to K.δ alone.

*Frame:* C' = C; L' = L; R' = R; M is per-case (above). The IsDocument case's `M'(e) = ∅` matches `M(e)` in value by the totality convention but enters e into E_doc, changing M's typing.

**K.μ⁺ (Arrangement extension).** New V→I mappings are added to some d ∈ E_doc, with existing mappings unchanged:

`dom(M'(d)) ⊃ dom(M(d)) ∧ (A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))`

Extension is pure addition — the domain grows, and no existing value is altered. Without the value-preservation clause, K.μ⁺ could silently replace values at existing positions, conflating extension with replacement. The decomposition of replacement into K.μ⁻ followed by K.μ⁺ depends on each being a pure operation.

The two conjuncts together force new mappings at positions disjoint from dom(M(d)). For any v ∈ dom(M'(d)) \ dom(M(d)), v is a new position by construction. For any v ∈ dom(M(d)), the value-preservation clause pins M'(d)(v) = M(d)(v), so that position cannot be the site of a "new" mapping carrying a different value. Hence dom(M'(d)) \ dom(M(d)) — the set of newly-mapped positions — is exactly the set of positions disjoint from dom(M(d)) that K.μ⁺ adds. The K.μ~ decomposition (replacement as K.μ⁻ then K.μ⁺) relies on this disjointness: the K.μ⁻ step empties the affected positions from dom, and the subsequent K.μ⁺ step adds mappings at positions that — having been removed — are now disjoint from the intermediate domain.

*Precondition:* `d ∈ E_doc`; for every new mapping M'(d)(v) = a, `a ∈ dom(C)` (S3, ASN-0036 — since K.μ⁺'s frame holds C' = C, referential integrity reduces to membership in the pre-state content store); new V-positions satisfy S8a (all components strictly positive), and the resulting arrangement M'(d) satisfies S8-depth (uniform depth within each subspace); dom(M'(d)) is finite (S8-fin); the resulting arrangement satisfies D-CTG (contiguity of the content subspace `V_1(d)`, ASN-0036) and D-MIN (minimum position of the non-empty content subspace, ASN-0036); the per-subspace strengthening to D-CTG★/D-MIN★ is adopted at the K.μ⁺ amendment — see *Amendments to existing transitions*. *First content insertion:* when `V_{s_C}(d) = ∅`, the depth of the first content V-position is pinned by `ValidFirstInsertionPosition(d, v, m)` (ASN-0036), which for any chosen `m ≥ 2` fixes the unique well-formed first content V-position `v` at that depth; K.μ⁺ realises this predicate directly for the content subspace, just as K.μ⁺_L pins the empty-link-subspace depth operationally at first insertion (mirroring this treatment). *Pairwise V-position distinctness on new mappings:* the newly added V-positions `{v_1, …, v_k} := dom(M'(d)) ∖ dom(M(d))` are pairwise distinct — this is S2 (ArrangementFunctionality, ASN-0036) preservation made explicit for K.μ⁺'s multi-position semantics, ensuring each new mapping `(vᵢ ↦ aᵢ)` adds a fresh V-position. Together with the disjointness-from-dom(M(d)) consequence below, this forces every two distinct new mappings to inhabit distinct V-positions, making `M'(d)` a partial function (S2) by construction rather than by accident. Functionality (S2) is preserved: dom(M'(d)) ⊃ dom(M(d)) with value preservation at existing positions means new entries are assigned at positions outside dom(M(d)), so M'(d) remains a function — extending a partial function at disjoint domain elements (themselves pairwise distinct, by the clause just stated) cannot introduce ambiguity.

In a composite transition, K.α may precede K.μ⁺, extending dom(C) before K.μ⁺ executes. At that intermediate state the freshly allocated address is already in the content store, satisfying the precondition. From the composite perspective, the I-address in a new mapping falls into one of two cases:

(i) Freshly allocated — co-occurring K.α places a into dom(C) before K.μ⁺ maps to it. Nelson: "new content enters Istream permanently."

(ii) Previously existing — a ∈ dom(C) at the composite's initial state. This is transclusion: "the copy shares I-addresses with the source. No new content is created in Istream."

*Frame:* C' = C; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R.

**K.μ⁻ (Arrangement contraction).** Existing V→I mappings are removed from some d ∈ E_doc, with surviving mappings unchanged:

`dom(M'(d)) ⊂ dom(M(d)) ∧ (A v : v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v))`

*Precondition:*
- `d ∈ E_doc`.
- `dom(M(d)) ≠ ∅` — required for the effect clause `dom(M'(d)) ⊂ dom(M(d))` to be satisfiable (no proper subset of `∅` exists).
- *Per-subspace suffix-prefix retention (constructive specification, pre-state checkable).* Under D-SEQ★ at Σ, each non-empty `V_S(d)` has canonical shape `{[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` for `S ∈ {s_C, s_L}`. The caller selects, for each S, a *retention count* `n'_S ∈ {0, 1, ..., n_S}` (with `n'_S = 0` when `V_S(d) = ∅`), with at least one S admitting strict contraction `n'_S < n_S`. The contracted arrangement is then determined constructively as the restriction `M'(d) = M(d) ↾ R` to the retained domain `R := ∪_{S ∈ {s_C, s_L}} {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}`. The choice of `(n'_{s_C}, n'_{s_L})` is the operation's degree of freedom, subject to the strict-contraction constraint, and is verifiable at the pre-state without computing M'(d) explicitly: D-SEQ★ at Σ supplies `(n_{s_C}, n_{s_L})`, and the caller commits to a per-subspace retention count.

The per-state arrangement invariants S2, S3★, S8a, S8-depth, S8-fin, D-CTG★, D-MIN★, and D-SEQ★ at M'(d) are *derived consequences* of this constructive form, not separate preconditions: restriction of a function preserves single-valuedness (S2) and referential integrity (S3★); restriction to a subset of the original domain preserves componentwise positivity (S8a), uniform depth per subspace (S8-depth), and finiteness (S8-fin); the suffix-prefix shape on each subspace directly satisfies the canonical D-CTG★, D-MIN★, and D-SEQ★ forms. The strict-contraction constraint `(E S :: n'_S < n_S)` combined with the constructive form yields `dom(M'(d)) ⊂ dom(M(d))` (proper subset at the whole-arrangement level), discharging the effect clause.

The constructive precondition is *equivalent* to "post-state satisfies D-CTG★/D-MIN★/D-SEQ★": the per-subspace suffix-prefix retention shape is the unique contraction pattern admissible under those invariants — D-SEQ★ at the post-state forces each non-empty `V_S(d')` to be the canonical prefix `{[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}`, so any admissible contraction retains a prefix of each subspace and removes the complementary suffix. The value-preservation clause `(A v : v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v))` (effect clause) is satisfied automatically by the restriction definition `M'(d) = M(d) ↾ R`, ruling out modification of surviving values.

*Frame:* C' = C; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d')).

**K.ρ (Provenance recording).** A document-content association enters R:

`R' = R ∪ {(a, d)}` where `a ∈ dom(C) ∧ d ∈ E_doc`

*Precondition:* `a ∈ dom(C)` ∧ `d ∈ E_doc`. The level constraint IsElement(a) follows from S7b (every a ∈ dom(C) satisfies IsElement(a)).

*Frame:* C' = C; E' = E; (A d :: M'(d) = M(d)).

The seven elementary kinds — K.α, K.δ, K.λ (introduced later under *Link allocation*), K.μ⁺, K.μ⁺_L (introduced later under *Link-subspace extension*), K.μ⁻, K.ρ — plus the named composite K.μ~ are *structurally sufficient* for the *catalogued* modification modes of this ASN, enumerated per component as follows. (i) *Existential components C, L, E and historical component R* admit only extension (P3): the elementary set covers each via K.α, K.λ, K.δ, K.ρ respectively, with no contraction or value rewriting on any of them. (ii) *Presentational component M* admits three modes — *extension* (K.μ⁺ for content-subspace, K.μ⁺_L for link-subspace), *contraction* (K.μ⁻, with per-subspace suffix-removal patterns forced by D-CTG★ + D-MIN★ + D-SEQ★ at the post-state), and *bijection-preserving reordering* (K.μ~, the named composite of K.μ⁻ + K.μ⁺ with subspace preservation and link-subspace fixity). (iii) *Replacement* — changing which I-address a V-position maps to — takes three forms by composite shape, partitioned by whether the new I-address is freshly allocated and (for transcluded forms) whether the destination document `d` has prior provenance for it:
- *Prior-provenance transcluded replacement* (two-step, K.μ⁻ + K.μ⁺): the new I-address is already in dom(C) at the composite's initial state, AND `(a, d) ∈ R` already holds for every transcluded address `a ∈ ran(M'(d)|_{s_C}) \ ran(M(d)|_{s_C})` arranged into `d`. K.μ⁻ removes a suffix of `V_S(d)` ending at the replaced position, then K.μ⁺ re-adds the suffix with the existing I-address installed and any displaced positions carrying their previously mapped values. No K.α and no K.ρ are needed: the new I-address is already in dom(C), and J1★'s composite-boundary requirement `(a, d) ∈ R'` is discharged by the pre-state membership `(a, d) ∈ R ⊆ R'` (P2). The precondition `(a, d) ∈ R` is the *substantive* constraint distinguishing this form from the next — it is *not* "recorded" by J1★ at the boundary (J1★ states a requirement, not an effect); when `(a, d) ∉ R`, the two-step composite genuinely violates J1★ at the boundary and is *not* a valid composite.
- *First-time transcluded replacement* (three-step, K.μ⁻ + K.μ⁺ + K.ρ): the new I-address `a` is already in dom(C) at the composite's initial state, but `(a, d) ∉ R` — `d` has never previously contained `a` in any of its prior arrangements. K.μ⁻ and K.μ⁺ are as in the two-step form, and a trailing K.ρ records the freshly introduced provenance pair `(a, d)` so that J1★'s requirement is satisfied at the composite boundary. This form applies in particular to cross-document transclusion of pre-existing content into a document `d` that has never displayed it before.
- *Fresh-content replacement* (four-step, K.μ⁻ + K.α + K.μ⁺ + K.ρ, or equivalently K.α + K.μ⁻ + K.μ⁺ + K.ρ): the new I-address must be freshly allocated. K.α extends dom(C) with the new value, K.μ⁻ and K.μ⁺ are as above (rebuilt around the newly allocated address), and K.ρ records provenance for the fresh content's first arrangement in d.

See *Worked example: interior content replacement* for the concrete fresh-content trace. All three forms share the K.μ⁻ + K.μ⁺ skeleton of K.μ~ (interior replacement is the same shape with `n'_S = k₀ − 1` rather than `n'_S = 0`).

K.μ~ — *arrangement reordering* — is a named composite of K.μ⁻ + K.μ⁺ (analogous to J4), not a primitive transition. Its bijection equation, admissibility constraints, and derived frame are stated in §*Decomposition of K.μ~* below.

We observe that neither split nor merge appears as an elementary transition. Nelson addresses this explicitly: the effect of splitting a document is achieved by creating two new documents and transcluding different portions of the original into each. Merging is creating a new document and transcluding from multiple sources. Both compose from K.δ, K.μ⁺, and K.ρ — the elementary transitions suffice.


## Amendments to existing transitions

**K.α (no local amendment in extended state).** ASN-0093's K.α already encodes the content-subspace restriction `E(a)₁ = s_C` (equivalently `subspace_I(a) = s_C`) in its precondition and includes `L' = L` in its frame, so no local amendment is required in the extended state.

*Frame (extended state).* `C' = C ∪ {a ↦ v}` (effect); `L' = L; E' = E; (A d :: M'(d) = M(d)); R' = R`.

**K.ρ (no precondition amendment in extended state).** K.ρ's precondition `a ∈ dom(C) ∧ d ∈ E_doc` and effect `R' = R ∪ {(a, d)}` are unchanged in the extended state.

*Frame (extended state).* `C' = C; L' = L; E' = E; (A d :: M'(d) = M(d))`.

**K.μ⁺ amendment (ContentSubspaceRestriction).** K.μ⁺ is amended with a content-subspace restriction: new V-positions must satisfy `subspace(v) = s_C`. This complements K.μ⁺_L, which handles link-subspace extensions exclusively. The restriction is necessary — without it, K.μ⁺ could create a link-subspace V-position mapping to dom(C), violating S3★. With this amendment, the two transitions partition arrangement extensions by subspace. The amended K.μ⁺ precondition is correspondingly strengthened: where the elementary definition required the resulting `M'(d)` to satisfy D-CTG and D-MIN on the content subspace `V_1(d)`, the extended-state precondition requires `M'(d)` to satisfy D-CTG★ and D-MIN★ (defined immediately below) restricted to the content subspace `S = s_C` — i.e. `V_{s_C}(d)` is contiguous under the V-ordering with `min(V_{s_C}(d)) = [s_C, 1, ..., 1]` when non-empty. The link subspace is preserved by the frame (`M'(d')` unchanged for `d' ≠ d`, and within `d` the link-subspace V-positions are untouched since K.μ⁺ adds only content-subspace positions), so the D-CTG★/D-MIN★ obligations on `V_{s_L}(d)` carry over from the pre-state unchanged. K.μ⁺_L discharges the parallel contiguity and minimum-position obligations when the link subspace is the one extended.

*Frame (extended state).* `C' = C; L' = L; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R`.

**D-CTG★ / D-MIN★.** ASN-0036's D-CTG and D-MIN have a link-subspace exemption accommodating Nelson's tombstoning design (LM 4/9). This ASN introduces strengthened forms D-CTG★ and D-MIN★ that apply uniformly across both subspaces:

  **D-CTG★ (per-subspace contiguity).** `(A d, S : V_S(d) ≠ ∅ : V_S(d) is contiguous under the V-ordering on subspace S)`, where *contiguous* unpacks as closed-interval membership: for every `v_lo, v_hi ∈ V_S(d)` and every depth-m_S positive tuple `z` with subspace identifier S and `v_lo ≤ z ≤ v_hi` under the V-ordering, `z ∈ V_S(d)` — with `m_S` fixed by S8-depth (ASN-0036) and "positive tuple" denoting the S8a-compatible domain (components in ℕ⁺), so the closed-interval form is well-defined whenever S8-depth and S8a hold at the state under consideration. The closed-interval formulation is what D-CTG★ unpacks to in the derivations below — appeals to D-CTG★ discharge to "every depth-m_S positive tuple lex-between two named members of V_S(d) is itself in V_S(d)" without further unpacking.

  **D-MIN★ (per-subspace minimum position).** `(A d, S : V_S(d) ≠ ∅ : min(V_S(d)) = [S, 1, ..., 1] of depth m_S)`

  **V-ordering on subspace S (definition).** The *V-ordering on subspace S* is the restriction of T1 (LexicographicOrder, ASN-0034) to the depth-m_S positive-component tuples whose first component is S — equivalently, the standard lexicographic order on ℕ⁺-valued tuples of length m_S, scoped to the slice with `v_1 = S`. (The depth m_S is the common depth of V_S(d) under S8-depth on each non-empty subspace; on an empty subspace the V-ordering's domain is empty, consistent with the vacuous form of the per-subspace clauses at empty subspaces.)

*Justification.* D-CTG★/D-MIN★ constrain *arrangement* (which V-positions are populated and how they sit on the V-ordering), not link existence or discoverability — every link persists in dom(L) with fixed endsets (L12) regardless of arrangement state. The strengthening therefore costs suffix-only contraction on each subspace; *interior link withdrawal* (preserving trailing links' V-positions while withdrawing an interior one) is outside K.μ⁻'s presentational-removal contract and would require a separate mechanism, catalogued in Open Questions.

**S8★ (per-subspace span decomposition).** ASN-0036's S8 (SpanDecomposition) is stated for the full arrangement under S3 (single content store target). In the extended state, S3 fails on the unprojected M(d) because link-subspace V-positions target dom(L) rather than dom(C), so ASN-0036's S8 cannot be applied to M(d) directly. S8★ states the corresponding decomposition per-subspace:

For each `d ∈ E_doc` and each subspace `S ∈ {s_C, s_L}`, the per-subspace arrangement `M(d)|_{V_S(d)}` decomposes into a finite set of correspondence runs `{(v_j, a_j, n_j)}` satisfying ASN-0036's S8 conditions (a) and (b) applied to the projected arrangement: every `v ∈ V_S(d)` lies in exactly one run, and within each run the V-positions and I-addresses advance by shift in lockstep. The decomposition is established by two distinct routes, one per subspace:

- *Content subspace.* `M(d)|_{V_{s_C}(d)} : V_{s_C}(d) → dom(C)` is a direct application of ASN-0036's S8: S3★ restricted to V_{s_C}(d) is exactly S3 (with target `dom(C)`), and S2, S7b, C1b (ASN-0093), S8a, S8-depth, S8-fin are elementary-preserved per the verification below.
- *Link subspace.* `M(d)|_{V_{s_L}(d)} : V_{s_L}(d) → dom(L)` cannot use ASN-0036's S8 directly because its range lies in `dom(L)` not `dom(C)`, falsifying S3; S7b/C1b also do not apply (they constrain `dom(C)`-resident addresses). S8★(s_L) is instead discharged by the *trivial length-1 decomposition* `{(v, M(d)(v), 1) : v ∈ V_{s_L}(d)}` — every link-subspace V-position constitutes its own length-1 correspondence run. S8's condition (a) (every `v ∈ V_{s_L}(d)` lies in exactly one run) holds by construction — each `v` is the sole element of its singleton run. S8's condition (b) requires `M(d)(shift(vⱼ, k)) = shift(aⱼ, k)` for `0 ≤ k < nⱼ`; at `nⱼ = 1` the quantifier reduces to the single case `k = 0`. We adopt the convention `shift(t, 0) := t` for any tumbler `t` (extending ASN-0034's OrdShift, which is stated for `n ≥ 1`, to the boundary case `n = 0` as the identity). Under this convention, condition (b) at `k = 0` reduces to `M(d)(v) = M(d)(v)`, which holds trivially. The trivial decomposition invokes no S8 machinery beyond the run-counting structure itself, so the failed S3 (and S7b/C1b) preconditions of ASN-0036's S8 are sidestepped entirely; finiteness of the decomposition follows from S8-fin's finiteness of `dom(M(d))`.

Richer decompositions arise naturally for arrangements built via shift-aligned K.μ⁺/K.μ⁺_L sequences, but the trivial form always suffices for S8★'s existence postcondition on either subspace.

S8★ substitutes for ASN-0036's S8 in ExtendedReachableStateInvariants, applied per-subspace to each projection. The S8 conjunct of ExtendedReachableStateInvariants is the conjunction of S8★(s_C) (via direct application of ASN-0036's S8 on the content-subspace projection) and S8★(s_L) (via the trivial length-1 decomposition on the link-subspace projection).

**D-SEQ★ (per-subspace sequential positions, derived).** For each non-empty subspace S in M(d):

  `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` for some `n_S ≥ 1`,

where the inner positions are of uniform depth m_S (the common depth within subspace S, by S8-depth), and `n_S = |V_S(d)|`.

D-SEQ★ is re-established in full detail here from the amended D-CTG★ + D-MIN★ + S8-depth + S8-fin + S8a. The derivation is a single-state implication consuming the per-state invariants on its left and producing the per-state shape on its right; it is reusable at every reachable state without re-invoking the outer induction.

*Derivation.* Fix d and a non-empty subspace S, and abbreviate `m := m_S`, `n := n_S`. By D-MIN★, V_S(d) contains the minimum position `v_min` (of the form `[S, 1, ..., 1]` of depth m). By S8-depth, every v ∈ V_S(d) has #v = m. By S8a, every component of every v ∈ V_S(d) is strictly positive (in ℕ⁺). By S8-fin, V_S(d) is finite; let n := |V_S(d)|. The V-ordering on a fixed subspace at a fixed depth is the standard lexicographic order on ℕ⁺-valued tuples. We treat the cases `m = 2` (the practical case driving every text-subspace worked example) and `m ≥ 3` separately so the m = 2 derivation is self-contained — no degenerate notation, no deferral.

*Case m = 2.* Every v ∈ V_S(d) has the form `[S, v_2]` with `v_1 = S` (by the definition of V_S(d), which projects M(d) to positions with `subspace(v) = S = v_1`) and `v_2 ∈ ℕ⁺` (by S8a). D-MIN★ gives `v_min = [S, 1] ∈ V_S(d)`. By S8-fin, let `v_max = max(V_S(d)) = [S, k_max]` for some `k_max ∈ ℕ⁺`. For each `k ∈ ℕ⁺` with `1 ≤ k ≤ k_max`, the depth-2 positive tuple `z = [S, k]` satisfies `v_min ≤ z ≤ v_max` under the V-ordering on S (subspace identifier matches; lex order on the terminal component agrees with the natural order on `k`); D-CTG★'s closed-interval membership then places `z ∈ V_S(d)`. Conversely, any v ∈ V_S(d) is `[S, v_2]` with `v_2 ∈ ℕ⁺` and `v_2 ≤ k_max` (since `v ≤ v_max`), so `v` is one of the listed tuples. Therefore `V_S(d) = {[S, k] : 1 ≤ k ≤ k_max}`. Counting gives `k_max = n`, delivering the m = 2 specialisation of D-SEQ★ directly. ∎ (case m = 2)

*Case m ≥ 3.* The depth supports an inner range `2 ≤ j ≤ m - 1` between the subspace position (1) and the terminal position (m), and the derivation proceeds in two steps.

*Step 1 (inner positions fixed at 1).* We show that every v ∈ V_S(d) satisfies `v_j = 1` for `2 ≤ j ≤ m - 1`. The inner range contains at least `j = 2 = m - 1` when m = 3 (the smallest case where the u_M construction below places M at the terminal position `j + 1 = m`, with the trailing range `j + 2..m` empty). Suppose for contradiction that some v ∈ V_S(d) has v_j ≥ 2 at the *minimal* inner position j with `2 ≤ j ≤ m - 1`. By minimality, `v_l = 1` for `2 ≤ l < j`; combined with `v_1 = S`, v agrees with `v_min` on positions 1..j - 1, and `v_j > v_min[j] = 1`, so `v_min < v` in lex order. For each integer `M ≥ 2`, define the depth-m tuple
  `u_M := [S, 1, ..., 1, 1, M, 1, ..., 1]`
with `S` at position 1, `1` at every position from 2 through j, `M` at position j + 1, and `1` at every remaining position from j + 2 through m. (When j = m - 1, the trailing range j + 2..m is empty; the tuple becomes `[S, 1, ..., 1, 1, M]` with M at the terminal — the construction's placement of M coincides with the terminal position whenever the minimal inner position is the rightmost-but-one.) Each u_M has all positive components, so it inhabits the V-ordering's domain at depth m.

We verify `v_min < u_M < v` for each M ≥ 2:
  - `v_min < u_M`: v_min and u_M agree on positions 1..j (both have `S` at 1 and `1` everywhere through position j); they first differ at position j + 1, where `v_min[j+1] = 1 < M = u_M[j+1]`.
  - `u_M < v`: u_M and v agree on positions 1..j - 1 (both have `S` at 1 and `1` at positions 2..j - 1); they first differ at position j, where `u_M[j] = 1 < v_j` (since v_j ≥ 2 by hypothesis).
Each u_M is a depth-m positive tuple with subspace identifier S satisfying `v_min < u_M < v`, so by D-CTG★'s closed-interval membership (v_min, v ∈ V_S(d) bracket a closed interval), u_M ∈ V_S(d). The map `M ↦ u_M` is injective (u_M and u_{M'} disagree at position j+1 whenever M ≠ M'), so `{u_M : M ≥ 2}` is a countably infinite subset of V_S(d). This contradicts S8-fin's finiteness of `dom(M(d))`, discharging the hypothesis that some `v ∈ V_S(d)` has an inner position ≥ 2.

Therefore no v ∈ V_S(d) has an inner position ≥ 2: every v has `v_j = 1` for `2 ≤ j ≤ m - 1`, and the only remaining freedom is in the terminal position v_m. So every v ∈ V_S(d) has the form `[S, 1, ..., 1, k]` for some `k ∈ ℕ⁺`, where the inner "1, ..., 1" segment has length `m - 2 ≥ 1`.

*Step 2 (terminal contiguity).* Restricted to terminal-varying tuples `[S, 1, ..., 1, k]`, the V-ordering coincides with the natural order on `k`. By S8-fin, n < ∞; let `v_max = max(V_S(d)) = [S, 1, ..., 1, k_max]` for some `k_max ∈ ℕ⁺` (well-defined since V_S(d) is finite and non-empty). By D-CTG★'s closed-interval-membership content, every depth-m positive tuple z with subspace identifier S satisfying `v_min ≤ z ≤ v_max` is in V_S(d) (v_min and v_max are both in V_S(d), bracketing a closed interval admissible to the D-CTG★ premise); restricted to terminal-varying tuples `[S, 1, ..., 1, k]`, this gives `{[S, 1, ..., 1, k] : 1 ≤ k ≤ k_max} ⊆ V_S(d)`. The reverse inclusion follows from v_max being the maximum: any `[S, 1, ..., 1, k]` with `k > k_max` would exceed v_max in lex order. Hence `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ k_max}` and counting gives `k_max = n`, the m ≥ 3 form of D-SEQ★. ∎ (case m ≥ 3)

The two cases together cover every reachable state under S8a + S8-depth. The canonical form for D-SEQ★ thus reads `{[S, k] : 1 ≤ k ≤ n_S}` at m = 2 and `{[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` at m ≥ 3 (with the inner "1, ..., 1" segment of length `m - 2`); the consolidated statement at the head of this definition uses the m ≥ 3 spelling and silently degenerates to the m = 2 form when the inner segment has length zero.

**K.μ⁻ amendment (PerSubspaceScope).** In the extended state, K.μ⁻'s D-CTG / D-MIN postconditions read as D-CTG★ / D-MIN★ (the per-subspace forms introduced above), and the constructive per-subspace retention precondition stated at K.μ⁻'s definition applies independently to each subspace under the D-SEQ★ enumeration `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` (also introduced above). The per-subspace shape — `V_S(d') = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}` for the caller-selected retention count `n'_S` — is determined by the constructive precondition directly; the derivation in *K.μ⁻ admissible contraction shape* below shows this is equivalent to the post-state characterization under D-CTG★ + D-MIN★ + D-SEQ★, justifying the precondition's generality.

*Per-subspace consequence of the strict-contraction clause.* `(E S ∈ {s_C, s_L} : V_S(d) ≠ ∅ : n'_S < n_S)` — at least one subspace shrinks strictly.

*Three-case partition by pre-state subspace populations.* The K.μ⁻ precondition `dom(M(d)) ≠ ∅` excludes the fourth case (`V_{s_C}(d) = V_{s_L}(d) = ∅`); the remaining three cases each force the contraction at a determinate subspace:
- *(a) Both V_{s_C}(d) ≠ ∅ and V_{s_L}(d) ≠ ∅.* At least one of `n'_{s_C} < n_{s_C}` or `n'_{s_L} < n_{s_L}` holds — the operation may contract either or both subspaces by any per-subspace admissible suffix removal (empty, partial, or full), subject only to the effect clause's overall strict-subset requirement on `dom(M'(d))`.
- *(b) V_{s_C}(d) ≠ ∅ ∧ V_{s_L}(d) = ∅.* The link subspace is already empty, so the empty subspace admits only the trivial "empty removal" (`V_{s_L}(d') = ∅ = V_{s_L}(d)`); the effect clause's proper-subset requirement then forces `n'_{s_C} < n_{s_C}` — the content subspace is the sole locus of contraction.
- *(c) V_{s_C}(d) = ∅ ∧ V_{s_L}(d) ≠ ∅.* Symmetrically: the content subspace is already empty (`V_{s_C}(d') = ∅`), and the link subspace must contract strictly (`n'_{s_L} < n_{s_L}`).

*Frame (extended state).* `C' = C; L' = L; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d'))`.

**K.μ⁻ admissible contraction shape (equivalence of constructive and post-state characterizations).** K.μ⁻'s precondition specifies the post-state constructively via the per-subspace retention count `n'_S`. We show this is *equivalent* to the post-state characterization "M'(d) satisfies D-CTG★ + D-MIN★ + D-SEQ★ and dom(M'(d)) ⊆ dom(M(d)) with value preservation on survivors," justifying the constructive precondition as fully general — every contraction admissible under the post-state invariants takes the per-subspace suffix-prefix retention form.

*Forward direction (constructive ⟹ post-state invariants).* The constructive form `M'(d) = M(d) ↾ R` with `R = ∪_S {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}` satisfies D-CTG★ at Σ' (each non-empty `V_S(d')` is the contiguous prefix `{[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}`), D-MIN★ at Σ' (when non-empty, `min(V_S(d')) = [S, 1, ..., 1, 1]`), and D-SEQ★ at Σ' (the canonical shape is exhibited by construction). Restriction preserves single-valuedness (S2), referential integrity (S3★), componentwise positivity (S8a), uniform depth (S8-depth), and finiteness (S8-fin) on survivors.

*Reverse direction (post-state invariants ⟹ constructive form).* The post-state invariants are hypothesised on a *candidate* contraction `M_cand(d)`, not on the constructive form being shown equivalent. Concretely: hypothesise that `M_cand(d)` is some candidate post-state with `dom(M_cand(d)) ⊆ dom(M(d))` and value-preservation on survivors (`(A v ∈ dom(M_cand(d)) :: M_cand(d)(v) = M(d)(v))`), and that `M_cand(d)` satisfies D-CTG★ + D-MIN★ + D-SEQ★ at Σ' together with the elementary-preserved invariants (S2, S3★, S8a, S8-depth, S8-fin). We show that `M_cand(d)` equals `M(d) ↾ R` for some per-subspace `R = ∪_S {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}` of the constructive form. Fix a subspace S, and write `V_S(d') := {v ∈ dom(M_cand(d)) : subspace(v) = S}` for the candidate's per-subspace projection. If `V_S(d') = ∅`, the conclusion holds with `n'_S = 0`. Otherwise D-SEQ★ — applied to the candidate `M_cand(d)` at Σ', as hypothesised — gives `V_S(d') = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}` for some `n'_S ≥ 1` directly. D-SEQ★ fires from D-CTG★, D-MIN★, S8-depth, S8-fin, and S8a at Σ', drawn from two distinct sources: S8-depth, S8-fin, and S8a at Σ' are preserved from Σ by restriction (a subset of a finite set is finite; restriction does not alter components or depth of any survivor), while D-CTG★ and D-MIN★ at Σ' are part of the hypothesis being characterized — they are not preserved by arbitrary restriction (removing an interior position would violate D-CTG★, removing the minimum would violate D-MIN★) but are supplied by the candidate-state hypothesis being shown equivalent. S8-depth at Σ' inherits `m_S` from the surviving V-positions of Σ — restriction cannot alter the depth of any survivor — making `V_S(d')` and `V_S(d)` share the same canonical D-SEQ★ shape `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` and `V_S(d') = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}` at the common depth `m_S`. Explicit comparison via the trailing-component bijection: define `φ_S : {1, ..., n_S} → V_S(d)` by `φ_S(k) = [S, 1, ..., 1, k]`, and symmetrically `φ'_S : {1, ..., n'_S} → V_S(d')`. By T3 (CanonicalRepresentation, ASN-0034), distinct values of `k` at a fixed inner-tuple pattern produce distinct tumblers, so `φ_S` and `φ'_S` are both bijections — `φ_S` between `{1, ..., n_S}` and `V_S(d)`, and `φ'_S` between `{1, ..., n'_S}` and `V_S(d')`. Set inclusion `V_S(d') ⊆ V_S(d)` translates pointwise under these bijections: every `[S, 1, ..., 1, k'] ∈ V_S(d')` is also in `V_S(d)`, so `k' ∈ {1, ..., n_S}`, giving `{1, ..., n'_S} ⊆ {1, ..., n_S}`, which forces `n'_S ≤ n_S` by direct inspection of initial-segment containment in ℕ. Taking the union of these per-subspace prefix shapes gives `dom(M_cand(d)) = R := ∪_S {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}`; combined with the hypothesised value-preservation on survivors, `M_cand(d) = M(d) ↾ R`, the constructive form. ∎

*Excluded shapes (side remark).* Configurations with an interior hole — `{[S, 1, ..., 1, k_lo], [S, 1, ..., 1, k_hi]} ⊆ V_S(d')` with some `k_lo < k₀ < k_hi` and `[S, 1, ..., 1, k₀] ∉ V_S(d')` — violate D-CTG★ (the interior tuple lex-between two surviving members but absent). Configurations with a missing minimum — `[S, 1, ..., 1, 1] ∉ V_S(d')` while `V_S(d') ≠ ∅` — violate D-MIN★. Both are therefore excluded by the constructive form and reverse-confirmed by the per-state invariants.

**L14a amendment.** In the extended state, S3★ + CL-OWN supersede ASN-0043's L14a.

The discharge of J4 (Fork) under the amended K.μ⁺ is given in *Coupling and isolation* below alongside J4's definition.


## Allocator hierarchy under documents

The content- and link-subspace allocators are organized as sibling element-field sub-allocators rooted at each document. The anchor and sub-allocator notation used throughout this ASN — `b_C(d)`, `b_L(d)`, `A_C(d)`, `A_L(d)` — is taken from ASN-0093 directly (the SubAllocatorAnchor and ActiveSubAllocatorChain definitions); we summarise it here for reading continuity.

For each `d ∈ E_doc`, the document-level address `d` (zeros = 2) is the root of d's allocator subtree. Per ASN-0093, two element-field bases sit immediately under d:

- `b_C(d) := [d.0.s_C]` (single-component element field with E₁ = s_C; zeros = 3, #E = 1) — the **content sub-allocator anchor**.
- `b_L(d) := [d.0.s_L]` (single-component element field with E₁ = s_L; zeros = 3, #E = 1) — the **link sub-allocator anchor**.

These anchors are structurally producible via T10a inc steps from `d`. Under SubspaceConventionAxiom (`s_C = 1` and `s_L = 2`), `b_C(d) = inc(d, 2) = [d.0.1]` (TA5(d) with k = 2), and `b_L(d) = inc(b_C(d), 0) = inc([d.0.1], 0) = [d.0.2]` (TA5(c)). The anchors are not themselves in `dom(C) ∪ dom(L)` — content addresses have `#E ≥ 2` (C1b, ASN-0093), link addresses have `#E ≥ 2` (L1b), and the anchors have `#E = 1` — so they inhabit the foundation carrier set `T` but no state component of Σ.

**Sub-allocator names** (A_C(d) and A_L(d) per ASN-0093; A_v(d), A_doc(A), A_account(N) introduced here). The naming family `A_·(·)` covers every T10a sub-allocator in the docuverse layer's allocator tree, indexed by the entity at the parent's level. Five members of the family are named in this ASN, three rooted at a document and two rooted at higher entity-hierarchy levels:

- `A_C(d)` — d's **content sub-allocator**, with anchor `b_C(d) = [d.0.s_C]` and first emission `[d.0.s_C.1]`. Its outputs `a` satisfy `a ∈ dom(C)`, `subspace_I(a) = s_C`, `origin(a) = d`, and `zeros(a) = 3` (element-level).
- `A_L(d)` — d's **link sub-allocator**, with anchor `b_L(d) = [d.0.s_L]` and first emission `[d.0.s_L.1]`. Its outputs `ℓ` satisfy `ℓ ∈ dom(L)`, `subspace_I(ℓ) = s_L`, `origin(ℓ) = d`, and `zeros(ℓ) = 3` (element-level).
- `A_v(d)` — d's **version sub-allocator**, with no element-field anchor (it emits at the entity-hierarchy level, not the element-field level). Its first emission is `inc(d, 1)`, an entity-level address with `zeros = 2` (a new document under T4b sharing `parent(·) = parent(d)`); subsequent emissions are T1 sibling-increments `inc(prev_version, 0)` on its frontier. Its outputs are versions of d and inhabit `E_doc`.
- `A_doc(A)` — account `A`'s **document sub-allocator** (introduced here), defined for each `A ∈ E_account`. Its first emission is `inc(A, 2)` — equivalently, the determinate tumbler `[A.0.1]` — an entity-level address with `zeros = 2` and `parent(·) = A` under T4b. Subsequent emissions are T1 sibling-increments `inc(prev_doc, 0)` on its frontier. Its outputs are original (non-version) documents under `A` and inhabit `E_doc`.
- `A_account(N)` — node `N`'s **account sub-allocator** (introduced here), defined for each `N ∈ E_node`. Its first emission is `inc(N, 2)` — equivalently, the determinate tumbler `[N.0.1]` — an entity-level address with `zeros = 1` and `parent(·) = N` under T4b. Subsequent emissions are T1 sibling-increments `inc(prev_account, 0)` on its frontier. Its outputs are accounts under `N` and inhabit `E_account`.

The three d-rooted sub-allocators (`A_C(d), A_L(d), A_v(d)`) share the document `d` as their common root; the two entity-hierarchy generalisations (`A_doc(A), A_account(N)`) sit one level higher (rooted at an account or node respectively). Across the family, the first-emission rule is uniform — the first output of each non-version sub-allocator is the determinate tumbler `[root.0.first_component]` where the first component is `s_C, s_L`, or `1` depending on the family member — and the subsequent-emission rule is uniformly `inc(prev, 0)`. *Parent allocator in T10a's tree, case-split by d's owning allocator:* version sub-allocators nest along the version chain rather than all rooting in the same account-level document sub-allocator. The split is based on which allocator's tracked domain `d` inhabits (a structural fact at the present state), not on which K.δ event minted `d` (a fact about history) — and these two framings differ: K.δ k = 0 events also place documents into `dom(A_doc(parent(d)))` or `dom(A_v(d'))`, in addition to the K.δ k ∈ {1, 2} events that first activated those allocators. (a') If `d ∈ dom(A_doc(parent(d)))` — d inhabits the document sub-allocator under its account — then `A_v(d)` is a child of `A_doc(parent(d))`, with spawnPt `d` and spawnParam `1`. This covers two minting histories: d minted by a prior K.δ case (ii) k = 2 step (the first document under `parent(d) ∈ E_account`, the T2 spawn step that activated `A_doc(parent(d))` with d as its first emission), and d minted by a prior K.δ case (ii) k = 0 step from another document on the same account chain (a T1 sibling-increment on `A_doc(parent(d))`'s frontier — a second, third, … document allocated under the same account). (b') If `d ∈ dom(A_v(d'))` for some `d' ∈ E_doc` — d inhabits a version sub-allocator — then `A_v(d)` is a child of `A_v(d')`, with spawnPt `d` and spawnParam `1`. This covers two minting histories: d minted by a prior K.δ case (ii) k = 1 step (the first version under d', the T2 spawn step that activated `A_v(d')` with d as its first emission), and d minted by a prior K.δ case (ii) k = 0 step from another version on the same `A_v(d')` chain (a T1 sibling-increment on `A_v(d')`'s frontier — a `v_{i+1} = inc(v_i, 0)` version on the chain headed by d's predecessor `d'`'s first version emission). T10a.6 (DomainDisjointness, ASN-0034) makes (a') and (b') mutually exclusive and exhaustive over `E_doc`: every `d ∈ E_doc` inhabits exactly one allocator's tracked domain, and that allocator is the unique parent allocator of `A_v(d)` in T10a's tree. In case (b') specifically, T10a.6 forbids `d ∈ dom(A_doc(parent(d)))`: d inhabits `dom(A_v(d'))`, and the cross-allocator disjointness `dom(A_v(d')) ∩ dom(A_doc(parent(d))) = ∅` rules out the case-(a') parent. Its outputs are versions of d under T10a's discipline: the first emission is `inc(d, 1)` (a new IsDocument tumbler with `zeros = 2`), produced by the K.δ k = 1 step whose operand is d itself — that step IS the T10a T2 spawn step that activates `A_v(d)`. Subsequent emissions are T1 sibling-increments on `A_v(d)`'s frontier, produced by K.δ k = 0 steps whose operand is a prior version of d (`inc(prev_version, 0)`); the k = 1 case fires at most once per d under T10a's per-`(t, k')` uniqueness. T2 admissibility requires the spawnPt `d` to inhabit the parent allocator's tracked domain at the spawn event: in case (a') this is the case hypothesis itself — `d ∈ dom(A_doc(parent(d)))` is the defining membership; in case (b') likewise `d ∈ dom(A_v(d'))` is the defining membership. The minting K.δ event (k = 2 or k = 0 in case (a'); k = 1 or k = 0 in case (b')) placed d into the appropriate allocator, and T10a allocator-monotonicity preserves that membership across every subsequent transition until the current K.δ k = 1 event reads it.

Outputs of `A_C(d)` and `A_L(d)` are *not* entity-level (their outputs inhabit `dom(C) ∪ dom(L)` at `zeros = 3`); outputs of `A_v(d)` *are* entity-level (they enter `E_doc` at `zeros = 2`). All three are T10a-conforming sub-allocators within d's allocator subtree.

Once each element-field anchor heads a frontier (not derivable from T10a alone — admitted as SubAllocatorAxiom below), the sub-allocator behaves as a T10a-conforming `inc(·, 0)` chain: the first content address under d is `[d.0.s_C.1]`, subsequent siblings advance by `inc([d.0.s_C.k], 0)` (TA5(c)); the first link address is `[d.0.s_L.1]`, subsequent siblings by `inc(ℓ_prev, 0)`. The two frontiers advance independently — each inc step operates locally under its subspace prefix.

**SubAllocatorAxiom (per ASN-0093, ContentLinkSubAllocatorExistence).** The axiom is taken from ASN-0093 directly. For each `d ∈ E_doc`, the entity-allocation event placing d into E_doc activates a content sub-allocator `A_C(d)` with anchor `b_C(d) = [d.0.s_C]` and a link sub-allocator `A_L(d)` with anchor `b_L(d) = [d.0.s_L]`. The five sub-clauses are inherited from ASN-0093 without modification:

- **SubAllocatorAxiom.Subspace.** Outputs of the two sub-allocators inhabit `s_C` and `s_L` respectively: every `a` emitted by `A_C(d)` has `subspace_I(a) = s_C`, every `ℓ` emitted by `A_L(d)` has `subspace_I(ℓ) = s_L`.
- **SubAllocatorAxiom.FirstEmission.** The first emission of each is the determinate tumbler `[d.0.s_C.1]` (resp. `[d.0.s_L.1]`), satisfying `a ∉ dom(Σ.C) ∪ dom(Σ.L)` at the state of allocation with `origin(a) = d` and `#E(a) = 2`.
- **SubAllocatorAxiom.Namespace.** Every output of d's sub-allocators is T4-valid with `zeros(·) = 3`. (Inherited from ASN-0093 ContentLinkSubAllocatorExistence; the T4-validity construction for the first emission and its preservation under subsequent `inc(·, 0)` steps are established there.)
- **SubAllocatorAxiom.T10aConformance.** `A_C(d)` and `A_L(d)` are T10a-conforming allocators within d's allocator subtree, each activated by the entity-allocation event placing d into E_doc. (Inherited from ASN-0093; the T2-spawn activation, the anchors-as-virtual-roots structure, and the GlobalUniqueness/frontier mechanics governing subsequent emissions are established there.)
- **SubAllocatorAxiom.Disjointness.** `dom(A_C(d)) ∩ dom(A_L(d)) = ∅`, and for any d ≠ d', `dom(A_C(d)) ∩ dom(A_C(d')) = ∅`, `dom(A_L(d)) ∩ dom(A_L(d')) = ∅`, `dom(A_C(d)) ∩ dom(A_L(d')) = ∅`. *Within-document discharge:* every output of `A_C(d)` has `E(·)₁ = s_C` by SubAllocatorAxiom.Subspace, and every output of `A_L(d)` has `E(·)₁ = s_L` by SubAllocatorAxiom.Subspace; SC-NEQ (SubspaceConventionAxiom) gives `s_C ≠ s_L`; T7 (FirstElementFieldDistinction, ASN-0034) — whose element-level hypothesis `zeros(·) = 3` is supplied at the output level by SubAllocatorAxiom.Namespace — then makes any `A_C(d)` output distinct from any `A_L(d)` output. *Cross-document discharge:* all three clauses follow from the Cross-document disjointness chain lemma (below) instantiated at the relevant anchor pairs; the lemma's statement admits possibly-distinct subspace components, so the fourth clause `dom(A_C(d)) ∩ dom(A_L(d')) = ∅` (anchors `[d.0.s_C]` and `[d'.0.s_L]`) is dispatched by the same lemma at `(s₁, s₂) = (s_C, s_L)`.

**Lemma (Cross-document disjointness chain).** *Derivation chain: T10a.{2,5} → T10.*

*Statement.* For any two distinct entities `e₁, e₂` with `e₁ ≠ e₂` of the same allocator-hierarchy level (both with `zeros(eᵢ) = z` for some fixed `z`), and for any T10a-conforming sub-allocator with prefix `[e₁.0.s₁]` and `[e₂.0.s₂]` for components `s₁, s₂ ≥ 1` (possibly distinct), the prefixes `p₁ := [e₁.0.s₁]` and `p₂ := [e₂.0.s₂]` satisfy `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`. By T10 (PartitionIndependence, ASN-0034), every address extending `p₁` differs from every address extending `p₂`. The statement instantiates at the document level with `e₁ = d₁, e₂ = d₂ ∈ E_doc` and `s₁, s₂ ∈ {s_C, s_L}` (yielding anchors `b_C(d), b_L(d)` in any pairing, including the cross-subspace pairing `(s_C, s_L)`), and at the account level with `e₁ = A₁, e₂ = A₂ ∈ E_account` (where the sub-allocator under each account is the account's document sub-allocator, with first emission `inc(A, 2) = [A.0.1]`).

*Proof.* Case-split on the prefix relationship between `e₁` and `e₂`, which is exhaustive: every distinct pair is either prefix-comparable or prefix-incomparable. In both cases the divergence between `p₁` and `p₂` is located in the `e₁`/`e₂` portion (or at the zero separator immediately after the shorter entity), so the values of `s₁, s₂` are immaterial — the proof goes through identically whether `s₁ = s₂` or `s₁ ≠ s₂`.

*Case A — Prefix-comparable* (WLOG `e₁ ≺ e₂`). The length comparison `#e₁ < #e₂` is derived in one step: by Prefix (ASN-0034), `e₁ ≼ e₂` gives `#e₁ ≤ #e₂`; combined with `e₁ ≠ e₂` (distinct entities by hypothesis) and T3 (CanonicalRepresentation, ASN-0034) — equal-length tumblers agreeing on every component are equal — `#e₁ = #e₂` would force `e₁ = e₂` (since `e₁ ≼ e₂` already supplies positional agreement on positions `1..#e₁`), contradicting distinctness. Hence `#e₁ < #e₂`. Both entities satisfy `zeros = z` (their common level by T4) — this same-level precondition is load-bearing for the next step: it pins the zero count of `e₂` at `z`, matching `e₁`'s zero count exactly. Since e₂'s first `#e₁` positions reproduce e₁ exactly — including all `z` of e₁'s zero separators — the remaining positions `#e₁+1, ..., #e₂` of e₂ contain `zeros(e₂) − z = z − z = 0` zeros, so `e₂[#e₁+1] ≠ 0`. The prefix `p₁ = [e₁.0.s₁]` places its own zero separator at position `#e₁+1` (`p₁[#e₁+1] = 0`, independent of `s₁`), while `p₂[#e₁+1] = e₂[#e₁+1] ≠ 0` (independent of `s₂`, since the disagreement is at an `e₂`-position, not at the subspace-component slot at position `#e₂ + 2`). We verify the divergence index `#e₁ + 1` sits inside both prefixes: each `pᵢ = [eᵢ.0.sᵢ]` extends `eᵢ` by exactly two components (one zero separator at position `#eᵢ + 1`, one component `sᵢ` at position `#eᵢ + 2`), so `#p₁ = #e₁ + 2` and `#p₂ = #e₂ + 2`. From `#e₁ < #e₂` we obtain `#e₁ + 2 ≤ #e₂ + 2`, i.e., `#p₁ ≤ #p₂`; hence `min(#p₁, #p₂) = #p₁ = #e₁ + 2`, and `#e₁ + 1 < #e₁ + 2 = #p₁ ≤ #p₂` places `#e₁ + 1` strictly inside `#p₁` and a fortiori inside `#p₂`. Position-divergence at index `#e₁+1 ≤ min(#p₁, #p₂)` witnesses `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` by Prefix.

*Case B — Prefix-incomparable* (`e₁ ⋠ e₂ ∧ e₂ ⋠ e₁`). The hypothesis supplies a divergence position `k ≤ min(#e₁, #e₂)` with `e₁[k] ≠ e₂[k]`. Since each prefix `pᵢ = [eᵢ.0.sᵢ]` agrees with `eᵢ` on positions `1..#eᵢ`, `p₁[k] = e₁[k] ≠ e₂[k] = p₂[k]`, witnessing prefix-incomparability by Prefix. The subspace components `s₁, s₂` at positions `#e₁ + 2` and `#e₂ + 2` are never consulted — divergence is already established within the entity portion.

T10 (PartitionIndependence) then closes the lemma in both cases: every `a` extending `p₁` differs from every `b` extending `p₂`. ∎

We abbreviate this lemma **CrossDocDisjoint**. It is stated for any sub-allocator prefix pair of the form `[e₁.0.s₁]`, `[e₂.0.s₂]` with `e₁, e₂` distinct same-level entities and `s₁, s₂ ≥ 1` (possibly distinct). At the document level this covers all four anchor pairings between `b_C(d) = [d.0.s_C]` and `b_L(d') = [d'.0.s_L]` — same-subspace (`s₁ = s₂`) and cross-subspace (`s₁ ≠ s₂`) alike, dispatched by the same proof; at the account level the document sub-allocator's first emission `inc(A, 2) = [A.0.1]` is a similar prefix (the difference between minted-direct and minted-via-anchor is in the activation discharge, not in the cross-entity disjointness analysis).

Cross-subspace collisions are further prevented by L14 (StoreDisjointness) — ASN-0093's SD (StoreDisjointness), restated at *Link store and extended system state* above: every content address has `subspace_I(a) = s_C`, every link address has `subspace_I(ℓ) = s_L`, and `s_C ≠ s_L`, so no allocation in one subspace can produce an address inhabiting the other.

**Lemma (SubAllocatorFreshness).** *Single freshness-discharge for element-field sub-allocator emissions, parametric in `x ∈ {C, L}`.* Let `d ∈ E_doc` and let `A_x(d)` be d's content (`x = C`) or link (`x = L`) sub-allocator. Suppose a K.α (for `x = C`) or K.λ (for `x = L`) firing emits the address `a` per the operation's emission cases. Then `a ∉ dom(C) ∪ dom(L)` at the pre-state, discharged in three parts:

- *Seed* (first emission, predicate `{a' ∈ dom(x-store) : origin(a') = d} = ∅`): `a` is the determinate first emission `[d.0.s_x.1]`, fresh against `dom(C) ∪ dom(L)` by SubAllocatorAxiom.FirstEmission (ASN-0093).
- *Frontier advance* (subsequent emission, predicate non-empty): `a = inc(max{a' ∈ dom(x-store) : origin(a') = d}, 0)` (TA5(c)) is the next sibling on `A_x(d)`'s inc chain; freshness against the same-subspace store is T10a GlobalUniqueness on `A_x(d)`'s tracked chain (SubAllocatorAxiom.T10aConformance).
- *Cross-subspace*: freshness against the opposite store is SC-NEQ + T7 (FirstElementFieldDistinction, ASN-0034), equivalently L14 (StoreDisjointness) at the pre-state.

We abbreviate this **SubAllocFresh**. It is the single carrier of the first-vs-subsequent freshness argument; the operations and derived obligations below cite it by name rather than re-derive it.


## Link allocation

**K.λ (LinkAllocation).** Per ASN-0093 (foundation K.λ, LinkAllocation): a new entry is created in the link store. The precondition structure — `d ∈ E_doc` (home document exists; ASN-0093 writes this as `d ∈ dom(M)`, but under ASN-0047's totality framing where `M` is total with `M(d) = ∅` for `d ∉ E_doc`, `dom(M) = T` trivially and `d ∈ E_doc` is the substantive predicate), `ℓ ∉ dom(L) ∪ dom(C)` (fresh address), `zeros(ℓ) = 3 ∧ E(ℓ)₁ = s_L` (element-level, link subspace), `#E(ℓ) ≥ 2`, `origin(ℓ) = d`, the first/subsequent emission cases producing `ℓ` via d's link sub-allocator `A_L(d)`, and `N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅` — follows ASN-0093's K.λ. The emission cases:

- *First emission* (predicate: `{ℓ' ∈ dom(L) : origin(ℓ') = d} = ∅`): `ℓ = [d.0.s_L.1]`, the determinate first emission of `A_L(d)`.
- *Subsequent emission* (predicate: `{ℓ' ∈ dom(L) : origin(ℓ') = d} ≠ ∅`): `ℓ = inc(max{ℓ' ∈ dom(L) : origin(ℓ') = d}, 0)` (TA5(c)), the next sibling on `A_L(d)`'s inc chain.

Freshness `ℓ ∉ dom(L) ∪ dom(C)` in both cases is SubAllocFresh at `x = L`.

In addition, the forward-allocation conjunct `(A ℓ' : ℓ' ∈ dom(L) ∧ origin(ℓ') = d : ℓ' < ℓ)` (T9) holds: it is a consequence of `inc(·, 0)` on the frontier in the subsequent case, and is vacuous in the first-link case (the antecedent is empty).

*Effect:* `L' = L ∪ {ℓ ↦ (e₁, …, eₙ)}`.

*Frame:* `C' = C; E' = E; (A d' :: M'(d') = M(d')); R' = R`.

Cross-document disjointness is supplied by the Cross-document disjointness chain lemma (T10a.{2,5} → T10) above, applied with `p₁ := b_L(d)` and `p₂ := b_L(d')`.


## K.δ case (ii) discharge and parent-allocator activation

Each non-node K.δ event closes its `e ∉ E` freshness obligation by interpreting the step as a T10a transition on the parent's entity-level sub-allocator. The discharge applies uniformly across k ∈ {0, 1, 2}, but the parent-allocator regime differs by k:

- *k = 0 (sibling under existing allocator):* operand `t ∈ E` already inhabits the parent's tracked domain by K.δ's `parent(t) = parent(e)` precondition; the step `e = inc(t, 0)` is a T10a T1 sibling-increment on the activated parent allocator. The frontier conjunct on `t` (the maximality clause in K.δ k = 0's precondition) ensures `t` is the parent allocator's current frontier, so `(t, 0)` has not been previously consumed by any earlier K.δ event; T10a chain-advancement uniqueness at `(t, 0)` (FrontierEquivalence) then forces `e = inc(t, 0) ∉ E`. T10a GlobalUniqueness on the inc-chain delivers `e ∉ E` directly.

- *k = 1 (version under existing document allocator):* The step `e = inc(t, 1)` is the T10a T2 spawn step that activates `A_v(t)`, t's version sub-allocator. The unique parent allocator of `A_v(t)` is identified by the (a')/(b') dispatch of *Sub-allocator names* above (via T10a.6, DomainDisjointness, ASN-0034) from t's owning allocator at the present state; the minting K.δ event that placed t into its owning allocator supplies the T2 spawnPt premise. The precondition `t ∈ E_doc` therefore discharges the membership obligation; P1 preserves that membership across subsequent transitions. T2 admissibility: `k' = 1 ∈ {1, 2}` and no zero-count side condition fires at `k' = 1`. Under T10a's *direct* per-`(t, k')` uniqueness axiom (instantiated at `k' = 1`), this k = 1 step fires at most once per `t`, so it is always the T2 spawn step — never a T1 sibling. Subsequent versions of t arise from K.δ k = 0 events whose operand is a prior version of t (`inc(prev_version, 0)`); those are T1 sibling-increments on `A_v(t)`'s frontier and are dispatched by the k = 0 case above, not by k = 1. T10a GlobalUniqueness on the newly activated `A_v(t)` delivers `e ∉ E`.

- *k = 2 (descent producing the first child under a node or account):* this is the activation case, and care is required to identify *which* allocator is being spawned and *which* allocator is its parent in T10a's allocator tree. We name the participants explicitly. Let `t` be the K.δ operand (a node when creating an account; an account when creating a document) and `e = inc(t, 2)` the spawn output. The K.δ event itself spawns a *new entity-level sub-allocator* under `t`; the two cases admit specific names — when t is a node, the spawned allocator is `A_account(t)`, t's *account sub-allocator* (catalogued in *Sub-allocator names* above), emitting account-level children of t; when t is an account, the spawned allocator is `A_doc(t)`, t's *document sub-allocator* (also catalogued above), emitting document-level children of t. The K.δ event is the T10a T2 spawn step that *creates* the spawned allocator, with `t` as spawnPt and `e` as the first emission.

  T10a T2 admissibility requires the spawnPt `t` to inhabit `dom(parent_allocator)` at the spawn event — i.e., t must already lie in the tracked domain of whatever allocator sits *above* the newly-spawned allocator in the allocator tree. The parent allocator above is identified by `t`'s own provenance: it is precisely the allocator that minted `t`. *Sub-case A: t is an account.* Here the spawned allocator is `A_doc(t)`, and its parent allocator in T10a's tree is `A_account(parent(t))` — the account sub-allocator under t's node. The membership obligation `t ∈ dom(A_account(parent(t)))` is discharged by case-split on whether `t` is the first account under `parent(t)` or a subsequent sibling — the same allocator `A_account(parent(t))` emits both, but via different K.δ event kinds (T2 spawn versus T1 sibling-increment). *Sub-case A1: t is the first account under parent(t).* The K.δ event that minted `t` was a K.δ case (ii) k = 2 event whose operand was `parent(t)` (necessarily a node, since k = 2's structural identity `zeros(t) = zeros(parent(t)) + 1` at that prior event, combined with `zeros(t) = 1`, fixes `zeros(parent(t)) = 0` — IsNode(parent(t))). That minting event was dispatched via sub-case B (when `parent(t)` is a non-bootstrap node) or sub-case C (when `parent(t) = n₀`), and in either case its T2 spawn step activated `A_account(parent(t))` with `t` as the first emission, placing `t` into `dom(A_account(parent(t)))`. *Sub-case A2: t is a subsequent (non-first) account under parent(t).* Discharged together with A1 by the direct T10a.6 argument below — the membership obligation `t ∈ dom(A_account(parent(t)))` does not require recursion through prior emissions.

*Discharge of sub-case A2 via T10a.6.* Sub-case A2's membership obligation — `t ∈ dom(A_account(parent(t)))` — discharges directly. By T10a.6 (DomainDisjointness, ASN-0034), every emission of `A_account(parent(t))`, whether placed by the activating T2 spawn or by a subsequent T1 sibling-increment, inhabits that allocator's tracked domain; and `t ∈ E` with `parent(t)` a node forces `t` to be such an emission, independent of which K.δ event placed it. AllocatedSet's tracked-domain monotonicity (ASN-0034) preserves the membership across every subsequent transition, so the present sub-case A event reads `t ∈ dom(A_account(parent(t)))` directly, and T2 admissibility against the state-tracked `A_account(parent(t))` discharges in the standard T10a form. *Sub-case B: t is a non-bootstrap node.* The spawned allocator is `A_account(t)`; the T2 spawnPt premise — that `t` inhabits its minting allocator's tracked domain — is supplied by NodeUniqueAllocation clause (c) (registry tracking) for every `t ∈ Σ.E_node`. *Sub-case C: t = n₀ bootstrap.* The spawned allocator is `A_account(n₀)`; since `n₀` enters at `Σ₀` with no prior K.δ event, its T2 spawnPt premise is supplied by NodeRegistryBootstrap (`n₀` inhabits the node-allocation registry's tracked domain at `Σ₀`).

  In all three sub-cases (A, B, C) the K.δ precondition `t = parent(e) ∈ E` discharges the T2 spawnPt requirement against whichever allocator (or external commitment) is the minting source of t. The spawn step's `k' = 2 ∈ {1, 2}` is admissible by T10a's *direct* per-`(t, k')` uniqueness axiom (instantiated at `k' = 2`); K.δ's case-level zeros bound `zeros(t) ≤ 1` discharges T10a's zero-count side condition (T10a admits k' = 2 when `zeros(spawnPt) ≤ 2`, satisfied a fortiori). T10a GlobalUniqueness on the parent allocator's tracked domain — now extended to include `e` as the spawned allocator's first emission — then delivers `e ∉ E`. For sub-cases B and C this is GlobalUniqueness on the activated `A_account(t)`, a T10a sub-allocator with `t` as its base.

In all three K.δ case (ii) sub-cases, the row's "parent allocator's tracked domain" denotes the parent allocator at the moment of the K.δ event — which is either pre-activated (k = 0; k = 1 after first version) or activated by the K.δ event itself (k = 2; first k = 1 emission), with the parent allocator named explicitly above for each sub-case. T10a GlobalUniqueness then closes the freshness obligation directly.


## Generalized referential integrity

**S3★ (GeneralizedReferentialIntegrity).** The arrangement maps V-positions to addresses in the store appropriate to their subspace:

  `(A d, v : v ∈ dom(Σ.M(d)) : (subspace(v) = s_C ⟹ Σ.M(d)(v) ∈ dom(Σ.C)) ∧ (subspace(v) = s_L ⟹ Σ.M(d)(v) ∈ dom(Σ.L)))`

where `subspace(v)` denotes the first component of the V-position. S3★ supersedes S3 (ASN-0036) for the extended state Σ = (C, L, E, M, R): S3 requires every V-position to map into dom(C), which is violated by link-subspace mappings targeting dom(L). S3 remains valid when restricted to states with no link-subspace mappings — the four-component model of the prior sections has only content-subspace V-positions, for which S3★ reduces to S3.

Existing transitions preserve S3★: K.α, K.δ, K.ρ hold M in frame; K.μ⁺ creates only content-subspace V-positions (by its amended precondition `subspace(v) = s_C`), so new mappings target dom(C) and the link-subspace clause is unaffected; K.μ⁻ contracts dom(M(d)), preserving both clauses. K.μ~ preserves S3★ via its K.μ⁻ + K.μ⁺ decomposition, with link-subspace mappings pointwise fixed.

**S3★-aux (SubspaceExhaustiveness).** In every reachable state, all V-positions have subspace s_C or s_L:

  `(A d, v : v ∈ dom(M(d)) : subspace(v) = s_C ∨ subspace(v) = s_L)`

*Proof.* By induction on transition sequences from Σ₀. Base: M₀ = ∅, the property holds vacuously. Step: K.μ⁺ (amended) creates only s_C positions; K.μ⁺_L creates only s_L positions; K.μ⁻ removes positions without altering subspaces of survivors; K.μ~ decomposes into K.μ⁻ + K.μ⁺, each maintaining the property independently of fixity; K.α, K.δ, K.λ, K.ρ hold M in frame. ∎


## Link-subspace extension

**Link-subspace V-position depth (operational).** We write `m_L(d)` for the link-subspace V-position depth of document `d ∈ E_doc`. This depth is not fixed by a separate axiom — it is pinned operationally, exactly as the content subspace pins its first-insertion depth via ASN-0036's `ValidFirstInsertionPosition`. The depth is chosen at the first link-subspace insertion into `d` (K.μ⁺_L's precondition below), constrained only by the S8a lower bound `m_L(d) ≥ 2`, and is held constant thereafter by S8-depth (uniform depth within a subspace, ASN-0036). On a non-empty link subspace `m_L(d)` is therefore the common depth S8-depth already fixes; on an empty link subspace S8-depth is vacuous and K.μ⁺_L pins the depth at first insertion. No new axiom is needed: S8a supplies the lower bound, S8-depth supplies fixity, and the operation's precondition supplies the first-insertion choice.

**K.μ⁺_L (LinkSubspaceExtension).** Extends a document's arrangement in the link subspace.

*Precondition:*
- d ∈ E_doc
- ℓ ∈ dom(L)  (the target link must already exist in dom(L) — placed there by some prior K.λ)
- origin(ℓ) = d  (only home-document links may be arranged)
- ℓ ∉ ran(M(d))  (the link is not already arranged at any V-position in d's arrangement — first-arrangement constraint). This guarantees CL-UNIQ at the post-state: were `ℓ ∈ ran(M(d))` already, there would exist some `v' ∈ dom(M(d))` with `M(d)(v') = ℓ`, and adding `(v_ℓ, ℓ)` with `v_ℓ ∉ dom(M(d))` (verified below) would produce two distinct V-positions both mapping to `ℓ`, violating CL-UNIQ. Combined with CL-OWN (which restricts the link-subspace range of M(d) to links with `origin(·) = d`), the freshness condition `ℓ ∉ ran(M(d))` is equivalent — under the precondition `origin(ℓ) = d` — to `ℓ ∉ ran(M(d)|_{dom_L})`: a link can appear in M(d)'s range only as the value of a link-subspace V-position (by S3★, since `ℓ ∈ dom(L)` and `dom(L) ∩ dom(C) = ∅` by L14), so the unrestricted `ℓ ∉ ran(M(d))` clause suffices.
- V-position v_ℓ satisfies:
  - subspace(v_ℓ) = s_L
  - depth m_L(d) (the per-document link-subspace depth defined above). When V_{s_L}(d) ≠ ∅, m_L(d) is the common depth fixed by S8-depth on existing link-subspace positions; when V_{s_L}(d) = ∅, S8-depth is vacuous and this first insertion pins m_L(d) — any value ≥ 2 by S8a, the choice mirroring K.μ⁺'s realisation of `ValidFirstInsertionPosition` for the empty content subspace.
  - If V_{s_L}(d) = ∅: v_ℓ is the minimum position `[s_L, 1, ..., 1]` of depth m_L(d) (D-MIN★)
  - If V_{s_L}(d) ≠ ∅: v_ℓ = shift(max(V_{s_L}(d)), 1), extending the contiguous range (D-CTG★). OrdShiftHom (ASN-0036, clause (a) subspace preservation under shift and clause (b) S8a preservation under shift) is subspace-parametric in v₁, so it applies to v_ℓ at v₁ = s_L exactly as at v₁ = s_C; clause (a) supplies subspace(v_ℓ) = s_L, clause (b) supplies S8a preservation, and the TS-family shift lemmas (TS1–TS5, ASN-0034) together with S8-depth supply S8-depth preservation.
  - #v_ℓ = m_L(d) (S8-depth within the link subspace)

*Effect:* `M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}`, with `dom(M'(d)) = dom(M(d)) ∪ {v_ℓ} ⊃ dom(M(d))` (strict extension; the disjointness `v_ℓ ∉ dom(M(d))` discharging the strict inequality is verified immediately below).

*Frame:* `C' = C; L' = L; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R`

We verify `v_ℓ ∉ dom(M(d))`, as required for M'(d) to be a proper extension preserving S2 (ArrangementFunctionality) — and equivalently to discharge the strict-extension `⊃` in the effect clause above. The verification decomposes by subspace: by S3★-aux (SubspaceExhaustiveness), every `v ∈ dom(M(d))` satisfies `subspace(v) ∈ {s_C, s_L}`, so `dom(M(d)) = V_{s_C}(d) ∪ V_{s_L}(d)`. We discharge `v_ℓ ∉ V_{s_L}(d)` and `v_ℓ ∉ V_{s_C}(d)` separately.

(a) *Disjointness from link-subspace positions, `v_ℓ ∉ V_{s_L}(d)`.* Two cases:
 - *V_{s_L}(d) = ∅:* vacuously, `v_ℓ ∉ ∅`.
 - *V_{s_L}(d) ≠ ∅:* `v_ℓ = shift(max(V_{s_L}(d)), 1) > max(V_{s_L}(d))` by TS4 (ShiftStrictIncrease, ASN-0034), so v_ℓ strictly exceeds every member of V_{s_L}(d) and cannot equal any of them.

(b) *Disjointness from content-subspace positions, `v_ℓ ∉ V_{s_C}(d)`.* By construction `subspace(v_ℓ) = s_L`, while every `v ∈ V_{s_C}(d)` has `subspace(v) = s_C` (by definition of `V_{s_C}(d)`). Since `s_L ≠ s_C` (SC-NEQ), the two tumblers differ in their first component. By T3 (CanonicalRepresentation, ASN-0034), tumblers are extensionally identified by their component sequence — two tumblers differing in any component (and a fortiori in their first component) are distinct. Note: T7 (FirstElementFieldDistinction, ASN-0034) does not apply at V-positions because T7's hypothesis is element-level (zeros = 3) while V-positions have zeros = 0; T3 supplies the required distinctness at the V-position depth where T7 does not reach.

Combining (a) and (b) with S3★-aux's disjoint-union form: `v_ℓ ∉ V_{s_L}(d) ∪ V_{s_C}(d) = dom(M(d))`.

The preconditions ensure that after the extension, D-CTG★ (contiguity), D-MIN★ (minimum position), and S8-depth (uniform depth) hold for the link subspace of d. S3★ is satisfied: `subspace(v_ℓ) = s_L` and `M'(d)(v_ℓ) = ℓ ∈ dom(L')`.

The origin restriction `origin(ℓ) = d` distinguishes link-subspace extension from content-subspace extension, where K.μ⁺ intentionally permits `origin(a) ≠ d` — that is content transclusion, an established architectural feature. Link transclusion — arranging a foreign-origin link in a document's link subspace — is excluded by design. Nelson: "A document includes only the links of which it is the home document" (LM 4/31). The byte stream admits transclusion ("The virtual byte stream of a document may include bytes from any other document," LM 4/10); links do not. Links maintain "permanent order of arrival" in their home document, and home document determines ownership ("A link need not point anywhere in its home document. Its home document indicates who owns it," LM 4/12). Arranging a link with `origin(ℓ) ≠ d` would place an out-link in a document that does not own it — violating the ownership semantics that home-document identity is meant to carry. The architecture provides alternatives: bidirectional link search discovers all links attached to transcluded content regardless of which document houses them; creating a new link in one's own document is the natural analog of annotation. Gregory confirms that the implementation achieves origin matching by procedural atomicity — `docreatelink` both allocates the link ISA under the document's address and places it in the document's arrangement in a single operation — but no runtime guard exists; `acceptablevsa` unconditionally returns TRUE and `docopy` performs no origin check. The origin restriction in K.μ⁺_L formalizes the structural guarantee that the implementation achieves by construction.


## Link-subspace ownership

**CL-OWN (LinkSubspaceOwnership).** In every reachable state:

  `(A d, v : v ∈ dom(M(d)) ∧ subspace(v) = s_L : origin(M(d)(v)) = d)`

Every document's link-subspace arrangement contains only its own links. K.μ⁺_L's precondition `origin(ℓ) = d` ensures ownership at creation; link-subspace fixity under K.μ~ ensures preservation through reordering.

**CL-UNIQ (LinkSubspacePositionUniqueness).** Within each document's link-subspace arrangement, each link occupies exactly one V-position — the restriction of M(d) to dom_L is injective:

  `(A d, v₁, v₂ : v₁ ∈ dom(M(d)) ∧ v₂ ∈ dom(M(d)) ∧ subspace(v₁) = s_L ∧ subspace(v₂) = s_L ∧ M(d)(v₁) = M(d)(v₂) : v₁ = v₂)`

Equivalently, `M(d)|_{dom_L}` is a partial injection from V-positions to link addresses.


## Decomposition of K.μ~

*Preconditions of K.μ~.* The operation has two explicit preconditions:
- `d ∈ E_doc`
- `M(d)|_{dom_C(M(d))}` takes at least two distinct values (equivalently, `M(d)` restricted to `dom_C(M(d))` is not constant-valued; this entails `|dom_C(M(d))| ≥ 2` but is strictly stronger) — necessary and sufficient for clause (ii) (net effect `M'(d) ≠ M(d)`) to admit a witness. The necessity and sufficiency of this precondition are proved at *Necessity and sufficiency of the precondition* below, after the proof obligations they consume.

For `d ∈ E_doc` with `M(d)|_{dom_C}` taking at least two distinct values, K.μ~ realises the *bijection equation*:

  `(E π : π is a bijection dom(M(d)) → dom(M'(d)) : (A v ∈ dom(M(d)) :: M'(d)(π(v)) = M(d)(v)))`

π is admissible iff (i) the induced post-state `M'(d)` would satisfy S8a, S8-depth, D-CTG★, D-MIN★, and S3★, and (ii) the net effect is non-trivial, `M'(d) ≠ M(d)`. Clause (ii) makes K.μ~ a real reordering: a permutation whose net effect is the identity arrangement is not a K.μ~ transition (the system simply does not change). Note that `M'(d) ≠ M(d)` is strictly stronger than the map-level `π ≠ id`: under S5 (UnrestrictedSharing, ASN-0036) two distinct content V-positions may carry the same I-address (transclusion), so the swap of two such equal-valued positions is a non-identity *map* with net-identity *effect* — clause (ii)'s net-effect form excludes it. S8a at every `π(v)` is part of clause (i)'s post-state invariant package on M'(d); K.μ~-FIX gives `dom(M'(d)) = dom(M(d))`, so every `π(v) ∈ dom(M(d))` inherits S8a from the inductive hypothesis at Σ unconditionally — no separate per-`π(v)` check is needed. Admissibility (i) *filters* which π the operation admits, stipulating that the post-state satisfy S3★, S8a, S8-depth, D-CTG★, D-MIN★ on `M'(d)` — an assumed condition on π, shown realisable by Step (B) below. The S3★ matrix entry for K.μ~ in ExtendedReachableStateInvariants is stipulated by admissibility (i) and discharged at Step (B.3).

*Step (A) — Subspace preservation under π.* Admissibility clause (i) of K.μ~ stipulates that the post-state `M'(d)` satisfies S3★(Σ') as part of its post-state invariant package — the stipulation is part of the admissibility filter on π, not a derived consequence of preconditions. We derive subspace preservation `(A v ∈ dom(M(d)) :: subspace(π(v)) = subspace(v))` from S3★(Σ) (inductive hypothesis), the admissibility-stipulated S3★(Σ'), the bijection equation `M'(d)(π(v)) = M(d)(v)`, and L14 at both states (`dom(C) ∩ dom(L) = ∅`). S3★-aux constrains `subspace(v) ∈ {s_C, s_L}` everywhere, so a mismatch under π takes exactly one of two complementary forms — `s_C → s_L` or `s_L → s_C`; there is no third case. We close both by contradiction.

*Case `s_C → s_L`.* Suppose π maps a content-subspace `v` (i.e., `subspace(v) = s_C`) to a link-subspace `π(v)` (i.e., `subspace(π(v)) = s_L`). By S3★(Σ)'s content clause at `v`, `M(d)(v) ∈ dom(C)`; the bijection equation gives `M'(d)(π(v)) = M(d)(v) ∈ dom(C)`; by S3★(Σ')'s link clause at `π(v)`, `M'(d)(π(v)) ∈ dom(L)`. Combining, `M'(d)(π(v)) ∈ dom(C) ∩ dom(L) = ∅` by L14 — contradiction.

*Case `s_L → s_C`.* Suppose π maps a link-subspace `v` (i.e., `subspace(v) = s_L`) to a content-subspace `π(v)` (i.e., `subspace(π(v)) = s_C`). By S3★(Σ)'s link clause at `v`, `M(d)(v) ∈ dom(L)`; the bijection equation gives `M'(d)(π(v)) = M(d)(v) ∈ dom(L)`; by S3★(Σ')'s content clause at `π(v)`, `M'(d)(π(v)) ∈ dom(C)`. Combining, `M'(d)(π(v)) ∈ dom(L) ∩ dom(C) = ∅` by L14 — contradiction.

Both cases close by the same L14-driven disjointness, and S3★-aux's two-subspace exhaustion supplies no third case. Hence `(A v ∈ dom(M(d)) :: subspace(π(v)) = subspace(v))`. ∎ (Step (A))

*Proof of Step (B) — the K.μ⁻ + K.μ⁺ full-clearance decomposition realises any admissible π.* S3★(Σ') itself holds for K.μ~ by the admissibility filter (above); what remains is to show K.μ~ is non-vacuous — that the K.μ⁻ + K.μ⁺ (full-clearance) decomposition actually realises an admissible π and produces a post-state `Σ' = (C, L, E, M', R)` faithful to the admissibility-stipulated S3★(Σ'), consuming Step (A)'s subspace preservation as the input that lets K.μ⁺'s amendment fire on the full-clearance write set. Let `Σ_int = (C, L, E, M_int, R)` denote the intermediate state between the K.μ⁻ and K.μ⁺ atomic steps of the decomposition. Three sub-claims, dispatched in order:

  *(B.1) S3★(Σ_int).* K.μ⁻'s effect is `M_int(d) = M(d) ↾ R'` (restriction to a subset of `dom(M(d))`) with values unchanged on survivors, and `M_int(d') = M(d')` for every `d' ≠ d`; K.μ⁻'s frame on `C` and `L` gives `dom(C_int) = dom(C)` and `dom(L_int) = dom(L)`. For every `v ∈ dom(M_int(d))`: `v ∈ dom(M(d))` (survivors lie in the pre-state domain), and `M_int(d)(v) = M(d)(v)` (value-preservation on survivors); the subspace `subspace(v)` is a property of the V-position tumbler itself, unchanged by the restriction. By S3★(Σ) (inductive hypothesis at the pre-state) at `v`: when `subspace(v) = s_C`, `M(d)(v) ∈ dom(C)`; when `subspace(v) = s_L`, `M(d)(v) ∈ dom(L)`. Substituting `M_int(d)(v) = M(d)(v)` and `dom(C) = dom(C_int)`, `dom(L) = dom(L_int)`: when `subspace(v) = s_C`, `M_int(d)(v) ∈ dom(C_int)`; when `subspace(v) = s_L`, `M_int(d)(v) ∈ dom(L_int)`. The same dispatch on every untouched arrangement `M_int(d')` for `d' ≠ d` gives S3★(Σ_int) globally.

  *(B.2) K.μ⁺'s new content-subspace positions target dom(C).* The K.μ⁺ step in the K.μ~ decomposition (full-clearance form) writes `{π(v) ↦ M(d)(v) : v ∈ V_{s_C}(d)}` at fresh V-positions disjoint from `dom(M_int(d))`. By Step (A)'s subspace preservation, each `π(v)` for `v ∈ V_{s_C}(d)` satisfies `subspace(π(v)) = subspace(v) = s_C`, so the K.μ⁺ amendment (new positions have `subspace = s_C`) is satisfied on the entire write set — without Step (A)'s subspace preservation, the K.μ⁺ amendment could fail on a π that maps some content-subspace position to a link-subspace target, blocking the realisation. By K.μ⁺'s referential-integrity precondition `M'(d)(v) ∈ dom(C')` for every new content-subspace mapping (evaluated at the post-K.μ⁻ intermediate state, which `Σ_int` makes available): each newly written value lies in `dom(C_int) = dom(C')` (`C' = C_int = C` by frame across both atomic steps).

  *(B.3) The realised post-state is faithful to S3★(Σ').* The decomposition's post-state must not contradict the admissibility-stipulated S3★(Σ'); we check it does not. The post-state arrangement `M'(d)` is the union of two disjoint contributions: (i) survivors of K.μ⁻ that K.μ⁺ frames unchanged — these carry S3★ from S3★(Σ_int) at B.1; (ii) newly written content-subspace positions from K.μ⁺ — these satisfy S3★'s content clause directly by B.2. `dom(C') = dom(C)` and `dom(L') = dom(L)` by the composite frame. Combining (i) and (ii) over every `v ∈ dom(M'(d))`, the realised `M'(d)` satisfies S3★ at the affected document `d`, consistent with the filter's stipulation; the framed arrangements `M'(d') = M(d')` for `d' ≠ d` carry S3★ from S3★(Σ) at the pre-state directly. The decomposition therefore realises the admissible π without violating S3★(Σ'). ∎ (Step (B))

**K.μ~-FIX (Domain fixity).** `dom(M'(d)) = dom(M(d))`. D-SEQ★ at the pre- and post-states gives `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` and `V_S(d') = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}` for each subspace S; since π is a bijection and (by subspace preservation) bijects V_S(d) onto V_S(d'), `n'_S = n_S` and `V_S(d') = V_S(d)`. So π is a permutation of dom(M(d)).

**Link-subspace fixity (Steps (C)–(D)).** `π(v) = v` for every `v ∈ dom_L(M(d))`. Sub-steps (1)–(3) establish the link-subspace functional identity `M'(d)|_{dom_L} = M(d)|_{dom_L}` — this is Step (C); sub-step (4) derives pointwise fixity from it (premise: CL-UNIQ at the pre-state Σ) — this is Step (D). Proof:

(1) *Subspace-preserving bijection preserves per-subspace cardinality.* π is a bijection `dom(M(d)) → dom(M'(d))` (from the bijection equation) with `(A v ∈ dom(M(d)) :: subspace(π(v)) = subspace(v))` (subspace preservation). The restriction `π|_{dom_L(M(d))}` therefore maps dom_L(M(d)) bijectively onto dom_L(M'(d)); symmetrically, `π⁻¹|_{dom_L(M'(d))}` maps dom_L(M'(d)) bijectively onto dom_L(M(d)). Bijection between subsets of a finite set forces equal cardinality: `|dom_L(M'(d))| = |dom_L(M(d))|`. Combined with K.μ~-FIX's per-subspace decomposition (n'_S = n_S for every S), this gives `dom_L(M'(d)) = dom_L(M(d))` as sets.

(2) *K.μ⁻'s removal set lies in dom_C.* K.μ⁺ (amended) cannot create link-subspace V-positions, so any link-subspace V-position present in dom_L(M'(d)) must have been present in dom_L(M(d)) — the K.μ⁻ + K.μ⁺ pipeline through K.μ~'s decomposition cannot introduce new link-subspace positions. Combined with the cardinality equality from (1), K.μ⁻'s removal set X = dom(M(d)) \ dom(M_int(d)) must satisfy `X ∩ dom_L(M(d)) = ∅` — every removed position is content-subspace. (Were a link-subspace position removed by K.μ⁻, the subsequent K.μ⁺ could not restore it, leaving `|dom_L(M'(d))| < |dom_L(M(d))|` and contradicting (1).)

(3) *Pointwise preservation on dom_L.* For each `v ∈ dom_L(M(d))`: v survives K.μ⁻ (by (2), X ∩ dom_L = ∅), so `v ∈ dom(M_int(d))` and K.μ⁻'s value-preservation clause gives `M_int(d)(v) = M(d)(v) = ℓ`. K.μ⁺ then frames existing positions: `v ∈ dom(M_int(d)) ⊆ dom(M'(d))` and `M'(d)(v) = M_int(d)(v) = ℓ`. Therefore `M'(d)|_{dom_L} = M(d)|_{dom_L}` as functions.

(4) *Identity via CL-UNIQ at the pre-state.* From (3), `M'(d)|_{dom_L} = M(d)|_{dom_L}`, so for the V-position `v ∈ dom_L(M(d))` under consideration, `M(d)(v) = ℓ`. Subspace preservation places `π(v) ∈ dom_L(M(d))` (using (1)'s cardinality equality `dom_L(M'(d)) = dom_L(M(d))`), and the bijection equation gives `M(d)(π(v)) = M'(d)(π(v)) = M(d)(v) = ℓ` (the first equality by (3) applied at `π(v) ∈ dom_L`). Both `v` and `π(v)` are link-subspace V-positions in `dom(M(d))` mapping to the same link `ℓ`. CL-UNIQ at Σ — link-subspace injectivity of `M(d)|_{dom_L}`, supplied as the ExtendedReachableStateInvariants per-state hypothesis at the reachable pre-state Σ — forces `π(v) = v`. The same functional identity (3) also gives post-state CL-UNIQ preservation directly, without passing through the pointwise identity: equal functions share injectivity profiles, so `M(d)|_{dom_L}` injective (CL-UNIQ at Σ) together with `M'(d)|_{dom_L} = M(d)|_{dom_L}` gives `M'(d)|_{dom_L}` injective, i.e., CL-UNIQ at Σ'. ∎

*Necessity and sufficiency of the precondition.* The precondition is stated against the pre-state `Σ` of a K.μ~ event; its necessity direction consumes CL-UNIQ at `Σ`, which holds by the ExtendedReachableStateInvariants inductive hypothesis on the per-state invariants at the reachable pre-state. The two directions enter the argument independently and are kept separate here so the reader sees what each consumes:
  - *Necessity (universal closure over admissible π).* Suppose K.μ~ admits some π. Then π satisfies admissibility (i) (the post-state invariant package on M'(d), in particular S3★(Σ')) and admissibility (ii) (net effect `M'(d) ≠ M(d)`). From admissibility (i)'s S3★(Σ') stipulation, Step (A) of the dependency chain above derives subspace preservation `(A v ∈ dom(M(d)) :: subspace(π(v)) = subspace(v))` in a single step from S3★(Σ) (inductive hypothesis at the pre-state) + L14 — without consuming link-subspace fixity. From admissibility (i) again plus K.μ~-FIX (`dom(M'(d)) = dom(M(d))`, the Domain-fixity result established above), π is a bijection of a fixed domain. Subspace preservation then forces π to map `dom_L(M(d))` bijectively onto itself (link-subspace closure) and `dom_C(M(d))` bijectively onto itself (content-subspace closure). Step (C) (derived above) gives `M'(d)|_{dom_L} = M(d)|_{dom_L}` (appealing only to the bijection equation, subspace preservation, K.μ⁺'s amendment, and the K.μ⁻ value-preservation clause) and Step (D) gives `π|_{dom_L} = id` pointwise (premise: CL-UNIQ at the pre-state Σ), so the net change `M'(d) ≠ M(d)` cannot lie in the link subspace — it must lie in the content subspace, `M'(d)|_{dom_C} ≠ M(d)|_{dom_C}`. Suppose for contradiction `M(d)|_{dom_C}` were constant with common value `a`. Content-subspace closure places `π⁻¹(u) ∈ dom_C(M(d))` for every `u ∈ dom_C(M(d))`, so the bijection equation gives `M'(d)(u) = M(d)(π⁻¹(u)) = a = M(d)(u)` — whence `M'(d)|_{dom_C} = M(d)|_{dom_C}`, contradicting the content-subspace change. Therefore `M(d)|_{dom_C}` is non-constant: it takes at least two distinct values (which in turn entails `|dom_C(M(d))| ≥ 2`, but the bare cardinality bound is not sufficient — a constant-valued `M(d)|_{dom_C}` of cardinality ≥ 2 admits only net-identity permutations). ∎
  - *Sufficiency (explicit construction).* When `M(d)|_{dom_C}` takes at least two distinct values, an admissible π always exists; we exhibit a concrete witness. Pick two elements `v₁, v₂ ∈ dom_C(M(d))` with `M(d)(v₁) ≠ M(d)(v₂)` — such a pair exists precisely because `M(d)|_{dom_C}` is non-constant, and the value-distinctness forces `v₁ ≠ v₂`. Define the *transposition witness*
      `π_swap(v₁) = v₂, π_swap(v₂) = v₁, π_swap(v) = v for every v ∈ dom(M(d)) \ {v₁, v₂}`
    — a bijection from `dom(M(d))` to itself fixing every position outside `{v₁, v₂}`. We verify admissibility of `π_swap`:
    - *Clause (ii) (net effect `M'(d) ≠ M(d)`).* The bijection equation at `v₂` gives `M'(d)(π_swap(v₂)) = M(d)(v₂)`, i.e. `M'(d)(v₁) = M(d)(v₂) ≠ M(d)(v₁)`, so the post-state arrangement differs from the pre-state at `v₁` — the net effect is non-trivial. (Choosing `v₁, v₂` with *distinct values* is exactly what a no-op swap of equal-valued transcluded positions would fail to provide.)
    - *Subspace-preserving.* `v₁, v₂ ∈ dom_C(M(d))`, so `subspace(v₁) = subspace(v₂) = s_C`, and `π_swap` maps `v₁ ↔ v₂` within `dom_C` and fixes every position elsewhere (including all of `dom_L`) — every V-position retains its pre-state subspace.
    - *Clause (i) (post-state invariants on `M'(d)`).* By K.μ~-FIX, `dom(M'(d)) = dom(M(d))`, so `S8a`, `S8-depth`, `S8-fin`, `D-CTG★`, `D-MIN★`, `D-SEQ★` at the post-state inherit unchanged from the pre-state's per-state hypothesis (the V-position domain is fixed). `S3★` at the post-state: at every `v ∈ dom(M(d))`, `M'(d)(π_swap(v)) = M(d)(v)` by the bijection equation; subspace preservation routes content-subspace mappings to `dom(C')` and link-subspace mappings to `dom(L')` exactly as at the pre-state, so `S3★` carries forward.
    Hence `π_swap` is admissible, and the full-clearance form (`n'_{s_C} = 0`) of the K.μ⁻ + K.μ⁺ decomposition realises it: the full-clearance form — K.μ⁻ clearing the entire content subspace, K.μ⁺ rebuilding it at fresh positions — is admissible for *every* admissible π without per-π precondition checks, since K.μ⁻'s suffix-removal precondition holds vacuously at the full-subspace suffix and K.μ⁺ writes at fresh positions. The transposition witness is the simplest one; many other admissible π exist, but a single witness suffices for the sufficiency obligation.

  As a caller-checked precondition: a transition whose `M(d)|_{dom_C}` is constant-valued (in particular when `|dom_C(M(d))| ≤ 1`, but also any state in which every content V-position shares a single I-address by transclusion) does not fire, and the caller is responsible for verifying this condition before invoking K.μ~. Equivalently, the operation's discharge of admissibility clause (ii) is a sufficiency obligation that the operation realises by exhibiting an admissible `π`; the precondition makes that obligation discharge via the full-clearance form.

*Frame (derived).* C' = C; E' = E; R' = R; L' = L; (A d' : d' ≠ d : M'(d') = M(d')) — by composition of K.μ⁻ and K.μ⁺ frames.

**Decomposition.** Here we give the realisation of K.μ~ when the existence condition holds.

*Realisation of K.μ~ when the existence condition holds.* When `|dom_C(M(d))| ≥ 2`, K.μ~ is realised as *any* valid K.μ⁻ + K.μ⁺ pair on `V_{s_C}(d)` whose net effect achieves the bijection equation for π, subject to K.μ⁻'s admissibility (per-subspace suffix removal under D-CTG★/D-MIN★) and K.μ⁺'s preconditions at the intermediate state. The cardinality of the K.μ⁻ removal — equivalently, the choice of `n'_{s_C} ∈ {0, 1, ..., n_{s_C} − 1}` — depends on which content-subspace positions π actually moves:

- *Partial-suffix expansion* at `n'_{s_C} = k₀ − 1` for some `k₀ ≥ 1`: K.μ⁻ removes the suffix `Y := {[s_C, 1, ..., 1, k] : k₀ ≤ k ≤ n_{s_C}}` (retaining the cut-prefix `X := {[s_C, 1, ..., 1, k] : 1 ≤ k < k₀}`), then K.μ⁺ rebuilds Y with π applied. This expansion is admissible iff at every survivor position `u ∈ X`, the M(d)-value at `u` equals the M(d)-value at its π-source `π⁻¹(u)`: `(A u ∈ V_{s_C}(d) : u < [s_C, 1, ..., 1, k₀] under the V-ordering on s_C : M(d)(u) = M(d)(π⁻¹(u)))`. Equivalently, quantifying over the source `v` whose image lands below the cut: `(A v ∈ V_{s_C}(d) : π(v) < [s_C, 1, ..., 1, k₀] under the V-ordering on s_C : M(d)(π(v)) = M(d)(v))`. The "iff" follows from K.μ⁺'s value-preservation clause on the surviving positions: each retained `u ∈ X` carries `M_int(d)(u) = M(d)(u)` through K.μ⁻ and `M'(d)(u) = M_int(d)(u) = M(d)(u)` through K.μ⁺; the bijection equation `M'(d)(π(v)) = M(d)(v)` instantiated at the unique `v = π⁻¹(u)` gives `M'(d)(u) = M(d)(π⁻¹(u))`. Equating at `u` forces `M(d)(u) = M(d)(π⁻¹(u))`. The quantifier must range over the *image* `u` (equivalently, the survivor — every `u ∈ X`), not over the source `v < cut`, because the obligation arises wherever π maps *into* X: it covers both X→X moves (`v ∈ X` with `π(v) ∈ X`) and Y→X moves (`v ∈ Y` with `π(v) ∈ X`). The Y→X case is exactly where a `v < cut`-only quantifier fails — for `v ∈ Y` with `π(v) ∈ X`, K.μ⁺'s value-preservation pins `M'(d)(π(v))` to the pre-state value `M(d)(π(v))` at the surviving position, while the bijection equation demands `M'(d)(π(v)) = M(d)(v)`, so `M(d)(π(v)) = M(d)(v)` is required even though `v` lies *above* the cut. Conversely, when π satisfies the stated condition, the K.μ⁻ + K.μ⁺ pair at `n'_{s_C} = k₀ − 1` realises π: K.μ⁻ retains `X` with original values, K.μ⁺ rebuilds Y by assigning `{π(v) ↦ M(d)(v) : v ∈ V_{s_C}(d), π(v) ∈ Y}`, and at each survivor `u ∈ X` the retained value `M(d)(u)` matches the bijection-required `M(d)(π⁻¹(u))` by the stated condition. *Relation to pointwise fixity.* The value-preservation form is weaker than pointwise fixity `(A u ∈ V_{s_C}(d) : u < [s_C, 1, ..., 1, k₀] : π(u) = u)`: under S5 (UnrestrictedSharing, ASN-0036), distinct V-positions may share the same M(d) value (transclusion), so π may swap below-cut positions among themselves — and may even swap a below-cut position with an above-cut one of matching M(d) value — without violating value-preservation. On arrangements injective on `dom_C(M(d))`, `M(d)(u) = M(d)(π⁻¹(u))` together with injectivity forces `π⁻¹(u) = u`, i.e., `π(u) = u`, and the simpler "π fixes every position below the cut" form is then sufficient.
- *Full content-subspace clearance and rebuild* at `n'_{s_C} = 0`: K.μ⁻ removes V_{s_C}(d) entirely (maximal-suffix removal, with link-subspace retained) and K.μ⁺ then adds `{π(v) ↦ M(d)(v) : v ∈ V_{s_C}(d)}` in one step. This expansion works for *every* admissible π. The admissibility condition on the partial-suffix form is vacuous at `k₀ = 1` (no positions lie strictly below `[s_C, 1, ..., 1, 1]` under D-MIN★), so the full-clearance form is the `k₀ = 1` specialisation of the partial-suffix family and inherits its admissibility unconditionally; it is the form invoked by the K.μ~ verification arguments below. Verification-matrix entries for K.μ~ that name no cut point therefore read as the full-clearance form, which is always available regardless of π's structure on `dom_C`.

A π that breaks below-cut value-preservation at the smallest candidate cut admits only the full-clearance form (or partial-suffix forms with smaller `k₀` whose admissibility condition still holds). K.μ⁻ must retain link-subspace mappings under every expansion — K.μ⁺ (amended) is content-only and K.μ⁺_L only places at the contiguous min or max, so any removed link-subspace position could not be restored.

*Intermediate-state admissibility.* At Σ_int (post-K.μ⁻, pre-K.μ⁺): C_int = C, M_int(d) = M(d) ↾ V_{s_L}(d). K.μ⁺'s preconditions at Σ_int discharge: `d ∈ E_doc` (frame); referential integrity from `M(d)(v) ∈ dom(C)` for `v ∈ V_{s_C}(d)` at pre-state; content-subspace restriction from K.μ~'s subspace-preserving precondition; S8a/S8-depth/S8-fin/D-CTG★/D-MIN★ on M'(d) from K.μ~'s postcondition. S2 holds because π is a bijection.

Since K.μ~ preserves ran(M(d)), ran(M'(d)) \ ran(M(d)) is empty, and the J1 coupling has no new containment pairs to record.


## Coupling and isolation

The elementary transitions do not all occur independently. Some must co-occur to maintain invariants (coupling); some must leave other components unchanged (isolation). The weakest-precondition calculus makes the coupling constraints visible.

A clarification on scope. The frame conditions stated above describe individual elementary transitions: K.μ⁺ alone does not modify R, K.α alone does not modify M, and so on. Coupling constraints describe required co-occurrence — when K.μ⁺ occurs, K.ρ must also occur in the same composite transition.

**Definition (Current containment).** The *current containment* of state Σ is the set of all document-content pairs where the content is presently in the document's arrangement:

`Contains(Σ) = {(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))}`

This is a derived quantity of the state — it captures what each document currently displays. We will need it both in the valid composite definition (as a state invariant) and in the coupling derivations that follow.

**Definition (Valid composite transition).** A composite transition `Σ →* Σ'` is *valid* iff it is a finite sequence of atomic transitions Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ' satisfying two conditions:

(1) *Elementary preconditions:* each step Σᵢ → Σᵢ₊₁ satisfies the precondition of its elementary transition kind, evaluated at the intermediate state Σᵢ.

(2) *Coupling constraints:* J0, J1, and J1' hold for the composite — evaluated between the initial state Σ and the final state Σ'.

Intermediate states need not satisfy all system invariants; only the final state is required to. The ordering matters: J0 couples K.α with K.μ⁺, and S3 requires the I-address to exist before the V→I mapping is created, so K.α precedes K.μ⁺. Similarly, J4's fork compounds K.δ + K.μ⁺ + K.ρ, and K.μ⁺ requires d ∈ E_doc, which K.δ establishes — so K.δ precedes K.μ⁺. The net effect of a composite transition is the composition of its elementary effects.

For freshly created documents d ∈ E'_doc \ E_doc, the pre-state has d ∉ E_doc, so M(d) = ∅ by the totality of M. Consequently ran(M(d)) = ∅, and the set difference ran(M'(d)) \ ran(M(d)) reduces to ran(M'(d)): all content placed in a new document counts as newly introduced. The coupling constraints below quantify over E'_doc, not E_doc, making them applicable to freshly created documents without special cases.

**J0 (Allocation requires placement).** Content allocation K.α always co-occurs with arrangement extension K.μ⁺:

`(A Σ →* Σ', a : a ∈ dom(C') \ dom(C) : (E d, v : d ∈ E'_doc ∧ v ∈ dom(M'(d)) : M'(d)(v) = a))`

Every freshly allocated I-address appears in some arrangement in the post-state — the containing document may itself have been freshly created by K.δ in the same composite transition. J0 is an axiom of the state transition model: in Nelson's model content enters the docuverse only by being placed in a document, so there is no orphan content in Istream that no document displays.

**J1 (Extension records provenance).** Arrangement extension K.μ⁺ must co-occur with provenance recording K.ρ:

`(A Σ →* Σ', d ∈ E'_doc, a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R')`

J1 is the link-free (`dom(L) = ∅`) specialisation of the operative coupling J1★. The coupling does not fall out of the calculus alone; it is forced by a *design choice* — the invariant that every current containment is recorded in R (Nelson commits to a permanent reverse index, and Gregory confirms the implementation accumulates entries "from every content addition"). Because K.μ⁺ frames R, K.μ⁺ alone cannot preserve that invariant, so K.ρ must co-occur. J1 above is the `dom(L) = ∅` reading of the wp computation in its operative content-subspace form (invariant P4★) — see *Scoped coupling constraints*.

Gregory identifies one implementation anomaly where provenance recording is skipped for a particular command, "making content invisible to find_documents." The abstract specification treats this as a defect: the coupling is required.

For a freshly created document d ∈ E'_doc \ E_doc, M(d) = ∅ by totality, so ran(M(d)) = ∅, so ran(M'(d)) \ ran(M(d)) = ran(M'(d)): every I-address placed in a new document triggers provenance recording.

**J1' (Provenance requires extension).** Conversely, provenance recording K.ρ for (a, d) occurs only within a composite transition where K.μ⁺ introduces a into ran(M'(d)):

`(A Σ →* Σ', a, d ∈ E'_doc : (a, d) ∈ R' \ R : a ∈ ran(M'(d)) \ ran(M(d)))`

J1 ensures every new containment pair is recorded; J1' ensures every new provenance entry corresponds to an actual containment event. Together they characterise new provenance entries: (a, d) ∈ R' \ R if and only if K.μ⁺ introduces a into ran(M'(d)) and (a, d) ∉ R. When (a, d) ∈ R already — from a prior insertion-deletion cycle — K.μ⁺ re-introducing a into d's arrangement requires no new K.ρ, because J1's requirement (a, d) ∈ R' is satisfied by existing membership (P2 ensures prior entries persist). The totality of M ensures J1' is well-defined for freshly created documents: M(d) = ∅ for d ∉ E_doc gives ran(M'(d)) \ ran(M(d)) = ran(M'(d)). Gregory confirms this tight coupling — the provenance structure "accumulates entries from every content addition" and no mechanism exists to record provenance outside of content placement.

**P4a (Historical fidelity).** Every entry in R reflects an actual past *content-subspace* containment event:

`(A (a, d) ∈ R :: (E Σ_k in the transition history : (E v ∈ dom(M_k(d)) : subspace(v) = s_C ∧ M_k(d)(v) = a)))`

*Derivation (four-component state).* By induction on the transition sequence. *Base:* R₀ = ∅; the quantifier is vacuously satisfied. *Inductive step:* for (a, d) ∈ R' \ R, J1' gives a ∈ ran(M'(d)) \ ran(M(d)) — the post-state Σ' is a witnessing state where d's arrangement contains a (in the four-component state every V-position has subspace s_C, so the content-subspace qualifier is automatic). For (a, d) ∈ R, the inductive hypothesis provides a prior witnessing state; P2 ensures the entry persists in R'.

*Derivation (extended state, with J1'★).* The same induction discharges P4a in the extended state, with J1'★ replacing J1' as the coupling. *Base:* R₀ = ∅; vacuous. *Inductive step:* for `(a, d) ∈ R' \ R`, J1'★ gives that some content-subspace V-position in M'(d) maps to `a` while no content-subspace V-position in M(d) does — i.e., there exists `v ∈ dom(M'(d))` with `subspace(v) = s_C ∧ M'(d)(v) = a`. The post-state Σ' is therefore a witnessing state whose arrangement contains `a` at a content-subspace V-position, matching the strengthened P4a quantifier. For `(a, d) ∈ R`, the inductive hypothesis provides a prior content-subspace witnessing state; P2 carries the entry into R'. The content-subspace qualification is essential here: J1'★ scopes provenance recording to content-subspace range changes (link-subspace mappings target `dom(L)`, which is disjoint from `dom(C)` by L14, so no link-subspace V-position can witness provenance under P7's `a ∈ dom(C)` requirement). P4a in the extended state therefore reads as "every provenance entry corresponds to a past content-subspace arrangement," consistent with both P7's grounding in `dom(C)` and J1'★'s content-scoped coupling. ∎

**J2 (Contraction isolation).** The elementary transition K.μ⁻ requires no coupling — it is self-sufficient with respect to P0–P2, L12, and Contains(Σ) ⊆ R. As an elementary transition, K.μ⁻ satisfies:

`C' = C ∧ L' = L ∧ E' = E ∧ R' = R`

The wp analysis confirms this. For P0: K.μ⁻ does not touch C. For P1: does not touch E. For P2: does not touch R. For L12: does not touch L. For the provenance bound Contains(Σ) ⊆ R: contraction can only remove pairs from Contains, so Contains(Σ') ⊆ Contains(Σ) ⊆ R = R'. No co-occurring transition is needed to maintain any system invariant.

This is the deepest consequence of the design. Deletion is purely presentational — it changes what appears, not what exists or what has been. Gregory confirms: contraction "never triggers" provenance recording, and the provenance structure "is never pruned."

**J3 (Reordering isolation).** The named composite K.μ~ is likewise self-sufficient:

`C' = C ∧ L' = L ∧ E' = E ∧ R' = R`

Reordering preserves ran(M(d)), so Contains(Σ') = Contains(Σ). All invariants are trivially maintained; no co-occurring transition is needed.

**J4 (Fork composite).** Nelson's forking creation mode — version creation with ancestry indication (LM 4/66, CREATENEWVERSION) — is a composite whose elementary steps are exactly K.δ + K.μ⁺ + K.ρ, all serving the new document d_new. *Fork is strictly the k = 1 version-creation case:* d_new = inc(d_src, 1), a child of d_src in the address space (zeros(d_new) = 2 = zeros(d_src), parent(d_new) = parent(d_src)). The k = 0 sibling allocation under the source's account (`docreatenewdocument` in Gregory's implementation) and the k = 2 hierarchical descent are *not* forks under this definition; they are independent K.δ + K.μ⁺ + K.ρ composites without the ancestry-by-address indication. This restriction matches Nelson's specific "fork" terminology and Gregory's `docreatenewversion` (which dispatches `makehint(DOCUMENT, DOCUMENT, depth=1)` to obtain the k = 1 child address).

**Definition (Fork).** A *fork* of d_src to d_new is a composite transition `Σ →* Σ'`, with *precondition* d_src ∈ E_doc ∧ V_{s_C}(d_src) ≠ ∅, consisting of:

(i) K.δ case (ii) with k = 1 and t = d_src, producing d_new = inc(d_src, 1) with d_new ∉ E_doc,

(ii) K.μ⁺ populating M'(d_new) from d_src's content subspace under transclusion: `ran(M'(d_new)) ⊆ ran(M(d_src)|_{V_{s_C}(d_src)})` — no new content addresses are introduced, every target lies in the pre-existing content store,

(iii) K.ρ recording provenance for each a ∈ ran(M'(d_new)),

and no other elementary steps. Step (ii) must produce a content-subspace arrangement on d_new whose range is contained in d_src's content-subspace range and discharges the per-state arrangement invariants (S2, S3★, S8a, S8-depth, S8-fin, D-CTG★, D-MIN★) at the post-state.

*Discharge of arrangement-side invariants.* Step (ii)'s K.μ⁺ creates only content-subspace V-positions (by the K.μ⁺ amendment) targeting addresses in `ran(M(d_src)|_{V_{s_C}(d_src)}) ⊆ dom(C)` (by S3★'s content clause at the pre-state, which is the only S3★ clause supplying a dom(C) containment — the unrestricted `ran(M(d_src))` includes link-subspace targets in dom(L), which are excluded from dom(C) by L14); C is frame-preserved across the composite (none of K.δ, K.μ⁺, K.ρ modify C), so S3★'s content clause holds at the post-state. *Link-subspace clearance via K.δ initialisation.* Step (i)'s K.δ event places `d_new` into `E_doc` with the totality-convention effect `M(d_new) = ∅` at the intermediate state Σ_post-K.δ — explicitly: K.δ's "Effect on M, per case" clause for `IsDocument(e)` reads `M'(e) = ∅`, so at the fork's intermediate state after K.δ but before K.μ⁺, `dom(M(d_new)) = ∅` and therefore `V_{s_L}(d_new) = ∅`. Step (ii)'s K.μ⁺ then adds only content-subspace V-positions (by the K.μ⁺ amendment), so the link subspace remains empty across step (ii): at the post-K.μ⁺ state, `V_{s_L}(d_new) = ∅` still holds. The fork composite includes no K.μ⁺_L step, so no link-subspace V-position is ever placed in `M(d_new)`. Hence at the fork's post-state Σ', `V_{s_L}(d_new) = ∅`, and D-CTG★, D-MIN★, S8-depth, S8-fin, and S8a all hold vacuously on d_new's link subspace. Step (ii)'s K.μ⁺ must establish D-CTG★, D-MIN★, S8a, S8-depth, S8-fin on `V_{s_C}(d_new)` by its postconditions — the choice of V-positions in step (ii) must be invariant-discharging, but the specific V-positions are operation-specific. By choosing V-positions contiguously from the minimum `[s_C, 1, ..., 1]`, D-CTG★ and D-MIN★ hold for the content subspace of d_new.

*Discharge of coupling constraints under the amended K.μ⁺.* J1★ is satisfied because step (ii)'s K.μ⁺ creates only content-subspace V-positions (by the amendment) and step (iii)'s K.ρ records provenance for each `a ∈ ran(M'(d_new))`, covering every content-subspace extension. J1'★ is satisfied because each new `(a, d_new) ∈ R' \ R` has `a ∈ ran(M'(d_new))` from a content-subspace extension — S3★'s content clause gives `M'(d_new)(v) ∈ dom(C)` for each such v, so `ran(M'(d_new)) ⊆ dom(C)` and P7 compatibility is maintained. Link-subspace mappings from the source document are not copied — the forked document's link subspace starts empty. This is consistent with Nelson's design: each document owns only its home links, and links from the source remain discoverable through the shared I-addresses via refractive following — "a link to one version of a Prismatic Document is a link to all versions" (Nelson). A mechanism for link inheritance under forking, if desired, would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope.

Since none of K.δ, K.μ⁺, K.ρ modify C (each has C' = C in its frame), a fork satisfies dom(C') = dom(C) — no new content is created. The provenance conclusion — that (a, d_new) ∈ R' for every a ∈ ran(M'(d_new)) — follows from J1★ (the extended-state coupling that supersedes J1) applied to the fresh-document case: the convention M(d_new) = ∅ gives that every content-subspace mapping in M'(d_new) is new to d_new's content-subspace range, and J1★ directly requires provenance recording for each such address. No additional constraint beyond J1★ is needed.

The new document d_new is created empty (K.δ), its arrangement extended with mappings to the source's I-addresses (K.μ⁺, with `ran(M'(d_new)) ⊆ ran(M(d_src)|_{V_{s_C}(d_src)})`), and the new associations recorded (K.ρ). The precondition V_{s_C}(d_src) ≠ ∅ ensures K.μ⁺ is well-formed. Since K.μ⁺ (amended) creates only content-subspace V-positions, the I-addresses it maps to must lie in dom(C) (by S3★'s content clause). Only content-subspace V-positions in d_src have I-addresses in dom(C) — link-subspace V-positions map to dom(L), and dom(L) ∩ dom(C) = ∅ (L14). With V_{s_C}(d_src) ≠ ∅, there is at least one content I-address to transclude, so the strict domain extension dom(M'(d_new)) ⊃ dom(M(d_new)) = ∅ is satisfiable. The weaker condition M(d_src) ≠ ∅ is insufficient: a document with only link-subspace positions (reachable via K.δ + K.λ + K.μ⁺_L with no intervening K.μ⁺) has ran(M(d_src)) ⊆ dom(L), and no address in dom(L) can serve as the target of a content-subspace V-position. When the source's content subspace is empty — whether because M(d_src) = ∅ or because dom_C(M(d_src)) = ∅ — the fork definition does not apply; creation from such a source is ex nihilo (K.δ alone), not a fork. Nelson: "the new document's id will indicate its ancestry."

An immediate consequence of J1 and J2 is that the provenance relation diverges from current containment over time.

**P4 (Provenance bounds, link-free fragment).** Over the link-free fragment (no K.λ, no K.μ⁺_L, so `dom(L) = ∅`), every V-position is content-subspace and `Contains(Σ) = Contains_C(Σ)`; the provenance bound

`Contains(Σ) ⊆ R`

is then exactly the `dom(L) = ∅` specialisation of P4★ (`Contains_C(Σ) ⊆ R`) — see *Content-scoped containment and provenance*. Once link-subspace mappings exist, `Contains(Σ)` acquires pairs `(ℓ, d)` with `ℓ ∈ dom(L)` that no provenance entry can record (P7 grounds R in `dom(C)`, and `dom(L) ∩ dom(C) = ∅` by L14), so P4 is unsatisfiable for the unscoped relation and is superseded by P4★.

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

  `(A Σ →* Σ', d ∈ E'_doc, a : (E v ∈ dom(M'(d)) : subspace(v) = s_C ∧ M'(d)(v) = a) ∧ ¬(E v ∈ dom(M(d)) : subspace(v) = s_C ∧ M(d)(v) = a) : (a, d) ∈ R')`

J1★ is range-based: it triggers whenever an I-address `a` is new to the content-subspace range of M'(d), regardless of whether the V-position carrying it existed in dom(M(d)). This matches J1's range-based structure (`a ∈ ran(M'(d)) \ ran(M(d))`), scoped to the content subspace. A domain-based formulation — `v ∈ dom(M'(d)) \ dom(M(d))` — would fail for value replacement at a reused position: K.μ⁻ removing `[1,2]` followed by K.μ⁺ re-adding `[1,2] ↦ a₃` leaves the V-position in both domains, making `dom(M'(d)) \ dom(M(d))` empty at that position, while `a₃` is genuinely new to the content-subspace range and requires provenance recording.

*Derivation of J1★ from preserving P4★.* The design choice to preserve is P4★ (`Contains_C(Σ) ⊆ R`) — the form that retains Nelson's "every recorded containment is captured in the reverse index" intent in the two-subspace state, where the unscoped P4 is unsatisfiable once link-subspace mappings exist. Computing wp backward from `Contains_C(Σ') ⊆ R'` under the K.μ⁺ amendment (which adds only content-subspace V-positions) and the K.μ⁺ frame `R' = R`:

`wp(K.μ⁺ (amended), Contains_C(Σ') ⊆ R') = (A a : a ∈ ran(M'(d)|_{s_C}) \ ran(M(d)|_{s_C}) : (a, d) ∈ R)`

The right-hand side collapses to R because K.μ⁺ frames R, and the difference set on the left is content-subspace-scoped because the K.μ⁺ amendment introduces only content-subspace V-positions, so any new entry in `Contains_C(Σ') \ Contains_C(Σ)` is captured by `ran(M'(d)|_{s_C}) \ ran(M(d)|_{s_C})`. K.μ⁺_L extends only the link subspace, leaving `ran(M(d)|_{s_C})` unchanged and contributing nothing to the difference — the wp computation is vacuous for K.μ⁺_L on P4★. The requirement "every new content-subspace range entry already in R" is not generally true for fresh content; K.μ⁺ (amended) in isolation cannot maintain P4★. Therefore, to maintain P4★, K.ρ must co-occur within the composite, extending R so that the composite post-state satisfies `(A a : a ∈ ran(M'(d)|_{s_C}) \ ran(M(d)|_{s_C}) : (a, d) ∈ R')` — which is J1★ above. The matrix entry P4★ under K.μ⁺ in *Class (b)* below corresponds to this derivation's discharge: at the composite boundary, K.ρ (under J1★) supplies the missing `(a, d) ∈ R'` for every new content-subspace range entry, restoring P4★. Symmetrically, J1'★ is the converse coupling — every new entry in `R' \ R` corresponds to a content-subspace range change — derived in the same manner from the requirement that R have no extraneous entries unanchored in content-subspace arrangement.

**J1'★ (ProvenanceRequiresExtension, content-subspace).**

  `(A Σ →* Σ', a, d : (a, d) ∈ R' \ R : (E v ∈ dom(M'(d)) : subspace(v) = s_C ∧ M'(d)(v) = a) ∧ ¬(E v ∈ dom(M(d)) : subspace(v) = s_C ∧ M(d)(v) = a))`

J1'★ is likewise range-based, matching J1': every new provenance entry `(a, d) ∈ R' \ R` must correspond to an I-address `a` that is new to the content-subspace range — present in the content-subspace range of M'(d) but absent from the content-subspace range of M(d).

Link-subspace extensions (K.μ⁺_L) do not trigger provenance recording: the link address ℓ enters ran(M'(d)), but no content-subspace V-position maps to ℓ — `subspace(v_ℓ) = s_L ≠ s_C` (SC-NEQ) — so ℓ is not in the content-subspace range of M'(d), and J1★ is vacuous. P7 (ProvenanceGrounding) — `(A (a, d) ∈ R :: a ∈ dom(C))` — is preserved because R is unchanged (K.μ⁺_L holds R in frame).

**ValidComposite★ (ValidComposite, amended).** A composite transition `Σ →* Σ'` in the extended state Σ = (C, L, E, M, R) is *valid* iff it is a finite sequence of atomic transitions `Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ'` — drawn from K.α (amended), K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻ (amended), K.μ~, and K.ρ — satisfying:

1. *Transition preconditions (intra-composite sequencing).* Each step `Σᵢ → Σᵢ₊₁` satisfies the *elementary* precondition of its transition kind, evaluated at the *intermediate* state `Σᵢ`. K.μ~ appearing in the sequence is shorthand for its K.μ⁻ + K.μ⁺ decomposition (per its definition above): admissibility clause (ii) requires a non-trivial net effect `M'(d) ≠ M(d)`, whose necessary-and-sufficient existence condition is derived at *Necessity and sufficiency of the precondition* above. When the existence condition holds, K.μ~ always expands into two consecutive elementary steps, each satisfying its own precondition at the respective intermediate state. This clause is what enforces intra-composite ordering — e.g., that K.α precedes K.μ⁺ when the latter places a freshly allocated I-address `a`, since K.μ⁺'s referential-integrity precondition `a ∈ dom(C)` would fail at the pre-K.α intermediate state otherwise. Step preconditions are *local* to the elementary transition; they say nothing about the composite's endpoints.
2. *Coupling constraints (initial-to-final).* J0, J1★, and J1'★ hold for the composite as a whole — evaluated *only* between the initial state Σ and the final state Σ'. The coupling predicates quantify over the *net* change between Σ and Σ' (e.g., `a ∈ dom(C') \ dom(C)`); they do not constrain the order or shape of intermediate steps, only that the *aggregate* effect of the composite must satisfy them. A composite that satisfies clause (1) but violates clause (2) — for instance, K.α alone without an accompanying K.μ⁺ and K.ρ — is not a valid composite even though every elementary precondition holds at every intermediate state.

This supersedes the earlier ValidComposite definition by extending the elementary transition set with K.λ and K.μ⁺_L, and replacing J1/J1' with J1★/J1'★ — scoping provenance coupling to content-subspace arrangement changes. J0 (AllocationRequiresPlacement) is unchanged — it constrains content allocation (K.α), which remains content-subspace only.

## Orphan links and coupling flexibility

The coupling constraints do not require K.λ to be paired with K.μ⁺_L. A composite consisting of K.λ alone is valid: J0 is vacuous (no content allocated), J1★ is vacuous (no content-subspace extension), and J1'★ is vacuous (no provenance change). The result is a link in dom(L) with no placement in any document's arrangement — an *orphan link*. This is a valid system state, not an error condition. State invariants are preserved: M, C, E, R are all in K.λ's frame (unchanged), so all arrangement, content, entity, and provenance invariants hold identically. L grows by one entry: dom(L') = dom(L) ∪ {ℓ}. K.λ's preconditions guarantee L0 (ℓ has subspace s_L, and ℓ ∉ dom(C) ensures dom(L') ∩ dom(C) = ∅), L1 (zeros(ℓ) = 3), L1a (origin(ℓ) ∈ E_doc), L3 (K.λ requires `N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅`, so L3 is established for the new entry; L12 preserves all existing entries), L12 (existing entries unchanged: L'(ℓ') = L(ℓ') for all ℓ' ∈ dom(L)), and L14 (disjointness: ℓ ∉ dom(C), so dom(L') ∩ dom(C') = ∅). Nelson explicitly diagrams "deleted links" as a category of document content (LM 4/9): links that exist in permanent storage but are "not currently addressable, awaiting historical backtrack functions."

Link withdrawal via K.μ⁻ applied to the link subspace would in principle produce the same orphan-link state but is constrained to suffix truncations under D-CTG★ (per K.μ⁻'s case analysis).

We do not add a J0 analog for links — the orphan state is architecturally intentional, satisfying both the permanence guarantee (L12: links are immutable once created) and the owner's right to withdraw (Nelson, LM 2/29). The wp analysis above shows the *form* of this design choice: it consists of *not* asserting a link-coverage invariant, rather than asserting an "orphan-permitting" rule.


## Destruction confinement

We now state the central structural theorem — a generalisation of S9 (ASN-0036) to the extended state.

**P3 (ArrangementMutabilityOnly).** No component other than M admits contraction or value rewriting:

  `(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ dom(L) ⊆ dom(L') ∧ E ⊆ E' ∧ R ⊆ R' ∧ (A a ∈ dom(C) :: C'(a) = C(a)) ∧ (A ℓ ∈ dom(L) :: L'(ℓ) = L(ℓ)))`

The only component that can lose information is M.

*Proof.* By case analysis on the seven elementary transitions. K.α extends dom(C) preserving existing entries, with L, E, and R in its frame. K.δ extends E, with C, L, and R in its frame. K.λ extends dom(L) preserving existing entries, with C, E, and R in its frame. K.μ⁺ (amended), K.μ⁺_L, and K.μ⁻ have C, L, E, and R in their frames. K.ρ extends R, with C, L, and E in its frame. Each preserves every conjunct. The named composite K.μ~ decomposes into K.μ⁻ followed by K.μ⁺, both of which preserve the conjuncts, so K.μ~ does as well. General composite transitions, being finite sequences of elementary ones, preserve the conjuncts by transitivity of ⊆ and equality. ∎

P3 is the synthesis of P0 ∧ L12 ∧ P1 ∧ P2 — one named per-transition predicate over `Σ → Σ'` covering every component except M. The label carries no "★" because there is no four-component predecessor to amend: P0, P1, and P2 retain their identities under both the four-component and extended states, and P3 packages them together with the link-store clause L12.

P3 makes the confinement vivid. Every destructive state change — every removal, every reordering — is confined to the presentational layer. The permanent record (what content exists, what links exist, which entities have been created, what provenance has been recorded) can only grow.


## Worked example: entity hierarchy by K.δ

We exercise the four K.δ patterns — case (i) node baptism, case (ii) k = 2 account descent, case (ii) k = 2 document descent, case (ii) k = 0 sibling document allocation — by building the chain `n₀ = 1 → 1.2 → 1.2.0.1 → 1.2.0.1.0.1 → 1.2.0.1.0.2` from Σ₀ (with E₀ = {1}).

**Step 1: K.δ case (i) — baptise node `1.2`.** Address `1.2` is supplied by the node-allocation protocol, not by inc. Preconditions: `ValidAddress(1.2)`, `IsNode(1.2)` (zeros = 0), `1.2 ∉ E₀` (discharged by NodeUniqueAllocation clause (a)), `n₀ ≼ 1.2` (`[1] ≼ [1, 2]`, discharged by NodeUniqueAllocation clause (b)). Effect: `E₁ = {1, 1.2}`, all other components frame.

**Step 2: K.δ case (ii) k = 2 — allocate account `1.2.0.1 = inc(1.2, 2)`.** TA5(d) gives `zeros = 1`, `parent = 1.2`. Preconditions: `parent(e) = 1.2 ∈ E₁`; `zeros(1.2) = 0 ≤ 2`; `1.2.0.1 ∉ E₁` discharged by T10a's GlobalUniqueness at the account sub-allocator under node `1.2` (T2-spawning at the live operand `t = 1.2`). Effect: `E₂ = E₁ ∪ {1.2.0.1}`.

**Step 3: K.δ case (ii) k = 2 — allocate document `1.2.0.1.0.1 = inc(1.2.0.1, 2)`.** TA5(d) gives `zeros = 2`, `parent = 1.2.0.1`. Preconditions analogous to Step 2; T10a's GlobalUniqueness at the document sub-allocator `A_doc(1.2.0.1)` discharges `d ∉ E₂`. Effect: `E₃ = E₂ ∪ {1.2.0.1.0.1}`, with `M₃(1.2.0.1.0.1) = ∅` and SubAllocatorAxiom activating the content and link sub-allocators (anchors `b_C(d) = [d.0.1]`, `b_L(d) = [d.0.2]`).

**Step 4: K.δ case (ii) k = 0 — allocate sibling document `1.2.0.1.0.2 = inc(1.2.0.1.0.1, 0)` under the same account.** Operand `t = 1.2.0.1.0.1`, the document placed by Step 3. The k = 0 dispatch differs from k ∈ {1, 2} in two distinctive features: (a) freshness `inc(t, 0) ∉ E` is discharged via the *derived* form of T10a's chain-advancement uniqueness at `(t, 0)` (FrontierEquivalence), rather than the *direct* per-`(t, k')` uniqueness axiom available at k ∈ {1, 2}; and (b) the dispatch through T10a.6 (DomainDisjointness) routes the verification against t's actual provenance — for this t, `A_doc(parent(t)) = A_doc(1.2.0.1)`, the account's document sub-allocator activated by Step 3.

*Structural identities (K.δ-ID).* TA5(c) gives `inc(t, 0)` by advancing the rightmost nonzero component: `inc(1.2.0.1.0.1, 0) = 1.2.0.1.0.2`. The named identities discharge the structural side conditions:
- K.δ-ID.zeros-0/1 at k = 0: `zeros(e) = zeros(t) = 2` — `1.2.0.1.0.2` has zero separators at positions 2 and 4 (matching `1.2.0.1.0.1`), so `zeros(e) = 2 = zeros(t)` directly. The document-level stratum is preserved.
- K.δ-ID.parent-0/1 at k = 0: `parent(e) = parent(t) = 1.2.0.1` — T4b's parent projection truncates at the last separator, giving the prefix `[1, 2, 0, 1]` for both `t = [1, 2, 0, 1, 0, 1]` and `e = [1, 2, 0, 1, 0, 2]`. The account `1.2.0.1` is the shared parent.

*Precondition discharge.*
- `t = 1.2.0.1.0.1 ∈ E₃` (placed by Step 3 into `E₃`, preserved by P1).
- `¬IsNode(t)`: `zeros(t) = 2 ≥ 1`, so `t` is not a node. T4b's parent projection is therefore defined at `t`.
- `inc(t, 0) = 1.2.0.1.0.2 ∉ E₃`: discharged via FrontierEquivalence (forward direction) at the present pre-state `Σ₃ = (C₃, L₃, E₃, M₃, R₃)`. Step 3 is the only prior K.δ event on `A_doc(1.2.0.1)`'s chain — it activated that chain with `t = 1.2.0.1.0.1` as the first emission, and no subsequent K.δ k = 0 event has fired on its frontier — so `t` is the frontier of `A_doc(1.2.0.1)`'s (t, 0)-branch, and the lemma confirms `inc(t, 0) ∉ E₃`.

*T10a.6 dispatch identifying t's owning allocator.* The K.δ k = 0 operation is allocator-agnostic in its precondition (it makes no commitment about which sub-allocator `t` inhabits), but dispatches to a determinate parent allocator via T10a.6 at firing time. For `t = 1.2.0.1.0.1`, the question is whether `t` inhabits `A_doc(parent(t)) = A_doc(1.2.0.1)` (case (a') of the Sub-allocator names dispatch) or some version sub-allocator `A_v(t')` for some `t' ∈ E_doc` (case (b')). Here, Step 3 minted `t` via a K.δ k = 2 event whose operand was `parent(t) = 1.2.0.1` — that event was the T2 spawn step activating `A_doc(1.2.0.1)` with `t` as the first emission, placing `t` into `dom(A_doc(1.2.0.1))`. By T10a.6, `t ∈ dom(A_doc(1.2.0.1))` and `t ∉ dom(A_v(t'))` for any other `t'`; case (a') applies, and the K.δ k = 0 event produces a T1 sibling-increment on `A_doc(1.2.0.1)`'s frontier, yielding `e = inc(t, 0) = 1.2.0.1.0.2` as the second emission of that chain.

*Effect.* `E₄ = E₃ ∪ {1.2.0.1.0.2}`, with `M₄(1.2.0.1.0.2) = ∅` (the K.δ `IsDocument(e)` case effect) and SubAllocatorAxiom activating the content and link sub-allocators for the new sibling document (anchors `b_C(1.2.0.1.0.2) = [1.2.0.1.0.2.0.1]`, `b_L(1.2.0.1.0.2) = [1.2.0.1.0.2.0.2]`).

The zero-count progression `0 → 1 → 2` (Steps 1–3) exhausts the entity stratum at the document level: a hypothetical fourth k = 2 descent would produce `zeros = 3`, which is the IsElement stratum and falls outside E. Step 4's k = 0 sibling-increment preserves the document-level stratum (`zeros = 2`) while extending the population of `E_doc` under the same account.

A second K.δ case (i) attempting to re-baptise `1.2` is excluded by `e ∉ E`; a K.δ case (i) attempting to baptise a disconnected node `2.1` is excluded by `n₀ ≼ e`. A second Step 4 attempting `inc(1.2.0.1.0.1, 0)` again is excluded by `inc(t, 0) ∉ E₄`: after Step 4 fires, `1.2.0.1.0.2 ∈ E₄`, and FrontierEquivalence (forward direction) at any subsequent state forces `inc(1.2.0.1.0.1, 0) ∈ E` by P1's E-monotonicity, blocking the precondition. The next K.δ k = 0 dispatch on `A_doc(1.2.0.1)`'s frontier would operate on the *new* frontier `1.2.0.1.0.2`, producing `inc(1.2.0.1.0.2, 0) = 1.2.0.1.0.3` — a third sibling document, with the same dispatch route through T10a.6 at the updated frontier.


## Worked example: fork with subsequent insertion

We trace a concrete scenario to ground the abstract definitions. Let the starting state Σ₁ contain node 1, account 1.0.1, and document d₁ = 1.0.1.0.1 with two characters:

> C₁ = {1.0.1.0.1.0.1.1 ↦ 'H', 1.0.1.0.1.0.1.2 ↦ 'i'}
> E₁ = {1, 1.0.1, 1.0.1.0.1}
> M₁(d₁) = {[1,1] ↦ 1.0.1.0.1.0.1.1, [1,2] ↦ 1.0.1.0.1.0.1.2}
> R₁ = {(1.0.1.0.1.0.1.1, d₁), (1.0.1.0.1.0.1.2, d₁)}

We write a₁ = 1.0.1.0.1.0.1.1 and a₂ = 1.0.1.0.1.0.1.2 for brevity.

**Fork d₁ to d₂ = 1.0.1.0.1.1.** This is J4's compound K.δ + K.μ⁺ + K.ρ — the k = 1 version-creation case.

*K.δ:* E₂ = E₁ ∪ {1.0.1.0.1.1}. The address 1.0.1.0.1.1 = inc(1.0.1.0.1, 1) is obtained from d₁ = 1.0.1.0.1 by TA5's k = 1 child-allocation rule — a version of d₁ at the next address-space level. M₂(d₂) = ∅.

*A_v(d₁) activation discharge.* The K.δ step is k = 1 with operand t = d₁ ∈ (E₁)_doc. Per the K.δ k = 1 case discharge, this step IS the T10a T2 spawn step that activates `A_v(d₁)`, d₁'s version sub-allocator. The operand `d₁ = 1.0.1.0.1` is an *original* document (case (a) of the K.δ k = 1 provenance split — minted by an earlier K.δ k = 2 event under account `1.0.1`, not by a prior K.δ k = 1 event on some other document), so the parent allocator of `A_v(d₁)` in T10a's tree is `A_doc(parent(d₁)) = A_doc(1.0.1)`. The spawnPt premise — `d₁ ∈ dom(A_doc(1.0.1))` — is discharged by K.δ k = 1's precondition `t = d₁ ∈ (E₁)_doc`, which places d₁ in `A_doc(1.0.1)`'s tracked domain: parent(d₁) = 1.0.1 is the account that minted d₁ via that earlier K.δ k = 2 event, so d₁ inhabits the document sub-allocator under 1.0.1. T2 admissibility: spawn parameter `k' = 1 ∈ {1, 2}` and no zero-count side condition fires at `k' = 1`; T10a's *direct* per-`(d₁, 1)` uniqueness axiom (k' = 1 falling within the axiom's stated `k' ∈ {1, 2}` regime — the direct route per the K.δ gloss, not the derived chain-advancement form reserved for k = 0) ensures this spawn occurs at most once, satisfied trivially as this is the first invocation. T10a GlobalUniqueness on the newly activated `A_v(d₁)` delivers `1.0.1.0.1.1 ∉ E₁`. The output `inc(d₁, 1) = 1.0.1.0.1.1` is the first emission of `A_v(d₁)`, opening the chain for subsequent K.δ k = 0 versions (`inc(1.0.1.0.1.1, 0) = 1.0.1.0.1.2`, etc.) as T1 sibling-increments on `A_v(d₁)`'s frontier. (Forking the *version* d₂ to a further `d₃ = inc(d₂, 1) = 1.0.1.0.1.1.1` would be case (b): `A_v(d₂)` would be a child of `A_v(d₁)`, not of `A_doc(1.0.1)`, because d₂ inhabits `A_v(d₁)`'s tracked domain, not `A_doc(1.0.1)`'s.)

*K.μ⁺:* M₂(d₂) = {[1,1] ↦ a₁, [1,2] ↦ a₂}. The same I-addresses as d₁ — transclusion, case (ii). No new content enters C. The V-positions [1,1] and [1,2] satisfy S8a (all components strictly positive, zeros = 0) and S8-depth (uniform depth 2 within subspace s_C, matching the pre-existing arrangement of d₁); the shared first component 1 — identifying subspace s_C — is a subspace-identity fact via `subspace(v)` (ASN-0036) rather than a clause of S8-depth itself.

*K.ρ:* R₂ = R₁ ∪ {(a₁, d₂), (a₂, d₂)}.

Verification against the resulting state Σ₂:

- *J0:* No fresh content (dom(C₂) = dom(C₁)), so vacuously satisfied.
- *J1★:* ran(M₂(d₂)|_{s_C}) \ ran(M₁(d₂)|_{s_C}) = {a₁, a₂} \ ∅ = {a₁, a₂} (M₁(d₂) = ∅ since d₂ ∉ (E₁)_doc). Both (a₁, d₂) and (a₂, d₂) are in R₂. ✓
- *J1'★:* `R₂ \ R₁ = {(a₁, d₂), (a₂, d₂)}` — both are new provenance entries from the K.ρ step. For each, the address must be new to d₂'s content-subspace range: `a₁ ∈ ran(M₂(d₂)|_{s_C}) = {a₁, a₂}` and `a₁ ∉ ran(M₁(d₂)|_{s_C}) = ∅` (M₁(d₂) = ∅), and symmetrically for a₂. Both entries are anchored in content-subspace range extensions introduced by the K.μ⁺ step of this composite. ✓
- *J4:* d₂ ∈ E₂_doc \ E₁_doc, ran(M₂(d₂)) = {a₁, a₂} ⊆ ran(M₁(d₁)). ✓
- *S2 (Arrangement functionality) on d₂:* the K.μ⁺ step adds the mappings {[1,1] ↦ a₁, [1,2] ↦ a₂} at V-positions disjoint from `dom(M₂_int(d₂)) = ∅` (the K.δ step initialised `M₂_int(d₂) = ∅`); since the extension occurs at fresh positions, single-valuedness is preserved trivially. ✓
- *S3★:* every V-position in M₂(d₂) has `subspace(v) = s_C` (the K.μ⁺ amendment supplies this at every step that adds positions; the K.δ step initialised `M₂(d₂) = ∅`), and each maps to `a₁, a₂ ∈ dom(C₂)` by S3★'s content clause. S3★'s link clause is vacuous since `dom(L₂) = ∅`. ✓
- *S4 (Content distinctness, per ASN-0036) on d₂'s range:* a₁ ≠ a₂ as content addresses — both inhabit dom(C₁), and the inductive hypothesis at Σ₁ (S4 over dom(C₁)) supplies the distinctness from the pre-state. The K.δ + K.μ⁺ + K.ρ fork composite holds C in frame (no new K.α event), so the dom(C) population — and therefore S4 — is preserved exactly across the composite. ✓
- *D-CTG★ on V_{s_C}(d₂) = {[1,1], [1,2]}:* under the V-ordering on s_C (lex order on depth-2 positive tuples with first component 1), the only depth-2 positive tuple with first component 1 lex-between [1,1] and [1,2] is the bounds themselves — there is no third position to check; contiguity holds. ✓
- *D-MIN★ on V_{s_C}(d₂):* `min(V_{s_C}(d₂)) = [1,1] = [s_C, 1]` of depth m_{s_C} = 2 — matching the D-MIN★ canonical form `[S, 1, ..., 1]` (with zero intermediate 1s at m = 2). ✓
- *D-SEQ★ on V_{s_C}(d₂):* `V_{s_C}(d₂) = {[1,1], [1,2]}` matches the canonical form `{[s_C, k] : 1 ≤ k ≤ 2}` at `n_{s_C} = 2` and `m_{s_C} = 2` (with zero intermediate 1s). ✓
- *P4★:* Contains_C(Σ₂) = {(a₁, d₁), (a₂, d₁), (a₁, d₂), (a₂, d₂)} ⊆ R₂. ✓
- *P7a:* dom(C₂) = dom(C₁) = {a₁, a₂}; both a₁ and a₂ have provenance entries (a₁, d₁), (a₂, d₁) ∈ R₁ ⊆ R₂. ✓
- *P8:* parent(d₂) = parent(1.0.1.0.1.1) = 1.0.1 ∈ E₁ ⊆ E₂ (k = 1 preserves parent(d_new) = parent(d_src), so parent(d₂) = parent(d₁) = 1.0.1). The existing non-node entity 1.0.1 (account) retains parent(1.0.1) = 1 ∈ E₂. ✓
- *L-invariants vacuously satisfied:* `dom(L₂) = dom(L₁) = ∅` (K.δ, K.μ⁺, K.ρ each hold L in frame), so L0 (L-clause), L1, L1a, L1b, L1c, L3, L-fin, CL-OWN, and CL-UNIQ are vacuous at Σ₂; L14 is `dom(C₂) ∩ dom(L₂) = dom(C₂) ∩ ∅ = ∅`. L0 (C-clause) and the remaining per-state invariants (S3★-aux, S7a–S7d, S8a, S8-fin, S8-depth, S8★, C-fin, P6, P7, NodeLineage) are inherited unchanged from Σ₁ across the K.δ + K.μ⁺ + K.ρ frame, with the exceptions noted in the explicit rows above (J4-specific reasoning for the new document; S2/S4/S3★/D-CTG★/D-MIN★/D-SEQ★ verified explicitly for d₂; P4★/P7a/P8 above). ✓

**Insert new content into d₂.** Compound K.α + K.μ⁺ + K.ρ.

*K.α:* Allocate a₃ = 1.0.1.0.1.1.0.1.1 with C₃(a₃) = '!'. The address falls under d₂'s prefix (S7a): origin(a₃) = 1.0.1.0.1.1 = d₂. The freshness of a₃ — i.e., `a₃ ∉ dom(C₂)` — is discharged by two complementary premises. *(i) Distinctness from addresses under d₁ (cross-document).* The pre-state content store dom(C₂) = dom(C₁) = {a₁, a₂} contains only addresses with origin d₁ (≠ d₂), so the Cross-document disjointness lemma — the consequence of T10a.{2,5} → T10 — yields a₃ ∉ {a₁, a₂}. The lemma is applied at the document-pair (d₁, d₂) where d₁ ≺ d₂ (d₂ = inc(d₁, 1), so d₁ is a proper prefix of d₂), activating Case A of the lemma: the divergence at position #d₁ + 1 (d₂[#d₁ + 1] = 1 ≠ 0 = b_C(d₁)[#d₁ + 1], with b_C(d₁)'s zero separator at that position and d₂'s extension carrying a nonzero component there) puts every address under b_C(d₁) and every address under b_C(d₂) into prefix-incomparable subtrees, so T10 yields the disjointness of dom(A_C(d₁)) and dom(A_C(d₂)). *(ii) First-emission discharge at d₂'s content sub-allocator.* This K.α event is the first emission of d₂'s content sub-allocator A_C(d₂) — d₂ was created at the immediately preceding K.δ step with the convention dom_s(A_C(d₂)) = ∅ at activation. SubAllocatorAxiom.FirstEmission directly supplies `[d₂.0.s_C.1] ∉ dom(Σ.C) ∪ dom(Σ.L)` at the state of allocation, discharging `a₃ ∉ dom(C₂)`; the FirstEmission clause commits *only* the first emission of the activated sub-allocator, not every output, so subsequent emissions of A_C(d₂) would discharge freshness via T10a's GlobalUniqueness on its inc chain instead. Freshness against A_C(d₂)'s own prior emissions is vacuous at the empty initial domain. The two premises together close the obligation.

*K.μ⁺:* M₃(d₂) = M₂(d₂) ∪ {[1,3] ↦ a₃}. V-position [1,3] has `subspace([1,3]) = 1 = s_C` and depth 2, matching [1,1] and [1,2] — S8-depth holds at the common depth `m_{s_C} = 2`. Referential integrity: a₃ ∈ dom(C₃) (S3). ✓

*K.ρ:* R₃ = R₂ ∪ {(a₃, d₂)}.

Verification:

- *J0:* a₃ ∈ dom(C₃) \ dom(C₂), and d₂ ∈ E₃_doc with M₃(d₂)([1,3]) = a₃. ✓
- *J1★:* ran(M₃(d₂)|_{s_C}) \ ran(M₂(d₂)|_{s_C}) = {a₃}, and (a₃, d₂) ∈ R₃. ✓
- *J1'★:* `R₃ \ R₂ = {(a₃, d₂)}` — the K.ρ step adds exactly this entry. The address `a₃` is new to d₂'s content-subspace range: `a₃ ∈ ran(M₃(d₂)|_{s_C}) = {a₁, a₂, a₃}` and `a₃ ∉ ran(M₂(d₂)|_{s_C}) = {a₁, a₂}`. The new provenance is anchored in the K.μ⁺ step's content-subspace range extension. ✓
- *S3★:* the new V-position [1,3] has `subspace([1,3]) = s_C` (K.μ⁺ amendment) and maps to `a₃ ∈ dom(C₃)`; existing V-positions retain their mappings into dom(C₂) ⊆ dom(C₃) by frame and P0. S3★'s link clause is vacuous since `dom(L₃) = ∅`. ✓
- *P4★:* Contains_C(Σ₃) adds (a₃, d₂); this pair is in R₃. ✓
- *P6:* origin(a₃) = d₂ = 1.0.1.0.1.1 ∈ E₃_doc. ✓
- *P7:* (a₃, d₂) ∈ R₃ and a₃ ∈ dom(C₃). ✓
- *P7a:* dom(C₃) = {a₁, a₂, a₃}; a₁ and a₂ retain provenance from R₂ ⊆ R₃, and a₃ has new provenance (a₃, d₂) ∈ R₃. Every a ∈ dom(C₃) has at least one provenance entry. ✓
- *L-invariants vacuously satisfied:* `dom(L₃) = dom(L₂) = ∅` (K.α, K.μ⁺, K.ρ each hold L in frame), so L0 (L-clause), L1, L1a, L1b, L1c, L3, L-fin, CL-OWN, and CL-UNIQ are vacuous at Σ₃; L14 is `dom(C₃) ∩ dom(L₃) = ∅`. L0 (C-clause) carries forward from Σ₂ and is reaffirmed for a₃ by K.α's `E(a₃)₁ = s_C` precondition. Remaining per-state invariants (S2, S3★-aux, S4, S7a–S7d, S8a, S8-fin, S8-depth, S8★, C-fin, D-CTG★, D-MIN★, D-SEQ★, P8, NodeLineage) are inherited from Σ₂ or established by the elementary preconditions per the verification matrix; C-fin is preserved by single-element extension. ✓

**Delete a₃ from d₂'s arrangement (K.μ⁻).** Remove the mapping at V-position [1,3] — the maximum end of V_{s_C}(d₂), satisfying the K.μ⁻ amendment's D-CTG★/D-MIN★ postcondition.

*K.μ⁻:* dom(M₄(d₂)) = {[1,1], [1,2]} ⊂ dom(M₃(d₂)) = {[1,1], [1,2], [1,3]}. The surviving mappings are unchanged: M₄(d₂)([1,1]) = a₁, M₄(d₂)([1,2]) = a₂. D-MIN★: min(V_1(d₂)) = [1,1] = [s_C, 1]. D-CTG★: {[1,1], [1,2]} is contiguous.

Verification:

- *J2:* C₄ = C₃; E₄ = E₃; R₄ = R₃. All permanent and historical state unchanged. ✓
- *J1'★ (vacuous):* `R₄ \ R₃ = ∅` since K.μ⁻ holds R in frame. There are no new provenance entries to check; J1'★ is vacuously satisfied. ✓
- *P4★:* Contains_C(Σ₄) = {(a₁, d₁), (a₂, d₁), (a₁, d₂), (a₂, d₂)}. The pair (a₃, d₂) is no longer in Contains_C — d₂ no longer displays a₃. Yet (a₃, d₂) ∈ R₄: the stale entry persists. Contains_C(Σ₄) ⊂ Contains_C(Σ₃), while R₄ = R₃. ✓
- *P7a:* dom(C₄) = dom(C₃) and R₄ = R₃ (frame); every a ∈ dom(C₄) retains its provenance entry from R₃. ✓
- *S3★:* surviving mappings retain their content-subspace V-positions and dom(C₄) = dom(C₃) targets by restriction; the removed mapping at [1,3] no longer participates. S3★'s link clause is vacuous since `dom(L₄) = ∅`. ✓
- *D-CTG★ / D-MIN★ / D-SEQ★ at Σ₄:* `V_{s_C}(d₂) = {[1,1], [1,2]}` is the contiguous prefix `{[s_C, k] : 1 ≤ k ≤ 2}` with minimum [1,1] = [s_C, 1] — the suffix-removal shape required by K.μ⁻ at the post-state. ✓
- *L-invariants vacuously satisfied:* `dom(L₄) = dom(L₃) = ∅` (K.μ⁻ holds L in frame), so L0 (L-clause), L1, L1a, L1b, L1c, L3, L-fin, CL-OWN, and CL-UNIQ are vacuous at Σ₄; L14 is `dom(C₄) ∩ dom(L₄) = ∅`. The remaining per-state invariants (S2, S3★-aux, S4, S7a–S7d, S8a, S8-fin, S8-depth, S8★, C-fin, P6, P7, P8, NodeLineage, L0's C-clause) carry forward from Σ₃ by restriction or frame. ✓

The divergence is now concrete: R₄ records that d₂ once contained a₃, while the current arrangement does not. This is the historical memory that J2 preserves — deletion is purely presentational.

**Reorder d₂'s arrangement (K.μ~).** Swap V-positions [1,1] and [1,2].

*K.μ~:* The bijection π : {[1,1], [1,2]} → {[1,1], [1,2]} with π([1,1]) = [1,2] and π([1,2]) = [1,1]. The definition requires M₅(d₂)(π(v)) = M₄(d₂)(v) for all v ∈ dom(M₄(d₂)), giving M₅(d₂) = {[1,1] ↦ a₂, [1,2] ↦ a₁}. Both target V-positions satisfy S8a (all components strictly positive) and S8-depth (uniform depth 2 within subspace s_C), with subspace(v) = 1 for both positions.

Verification:

- *J3:* C₅ = C₄; E₅ = E₄; R₅ = R₄. All permanent and historical state unchanged. ✓
- *J1'★ (vacuous):* `R₅ \ R₄ = ∅` since K.μ~ holds R in frame. There are no new provenance entries to check; J1'★ is vacuously satisfied. ✓
- *ran preservation:* ran(M₅(d₂)) = {a₁, a₂} = ran(M₄(d₂)). The multiset of referenced I-addresses is identical; only V-positions changed. ✓
- *P4★:* Contains_C(Σ₅) = Contains_C(Σ₄) ⊆ R₄ = R₅. Since ran is preserved for d₂ and no other arrangement changed, the current containment set is unchanged. ✓
- *P7a:* dom(C₅) = dom(C₄) and R₅ = R₄ (frame); every a ∈ dom(C₅) retains its provenance entry. ✓
- *S3★:* both V-positions retain `subspace(v) = s_C` (the swap permutes content-subspace positions only) and map into dom(C₅) = dom(C₄). S3★'s link clause is vacuous since `dom(L₅) = ∅`. ✓
- *L-invariants vacuously satisfied:* `dom(L₅) = dom(L₄) = ∅` (K.μ~ holds L in frame, equivalently both K.μ⁻ and K.μ⁺ in its decomposition do), so L0 (L-clause), L1, L1a, L1b, L1c, L3, L-fin, CL-OWN, and CL-UNIQ are vacuous at Σ₅; L14 is `dom(C₅) ∩ dom(L₅) = ∅`. The remaining per-state invariants (S2, S3★-aux, S4, S7a–S7d, S8a, S8-fin, S8-depth, S8★, C-fin, D-CTG★, D-MIN★, D-SEQ★, P6, P7, P8, NodeLineage, L0's C-clause) carry forward from Σ₄ via the K.μ⁻ + K.μ⁺ decomposition (each step preserves them individually, with K.μ~-FIX establishing dom(M₅(d₂)) = dom(M₄(d₂)) for the per-subspace shape invariants). ✓

Reordering is the simplest transition to verify: it touches nothing beyond the V-position mapping, and all invariants hold by the frame conditions alone.


## Worked example: interior content replacement

We trace the interior-position case of the content-replacement decomposition (K.μ⁻ + K.μ⁺ with `n'_{s_C} = k₀ − 1` rather than the single-position pair at `k₀ = n_{s_C}`) introduced in the *Elementary transitions* section.

*Initial state.* Let document `d = 1.0.1.0.1` have four content-subspace mappings, with `aₖ := 1.0.1.0.1.0.1.k` for `k ∈ {1, 2, 3, 4}`:

> C ⊇ {a₁ ↦ char₁, a₂ ↦ char₂, a₃ ↦ char₃, a₄ ↦ char₄}
> M(d) = {[1,1] ↦ a₁, [1,2] ↦ a₂, [1,3] ↦ a₃, [1,4] ↦ a₄}
> R ⊇ {(a₁, d), (a₂, d), (a₃, d), (a₄, d)}

Content-subspace V-positions: `V_{s_C}(d) = {[1,1], [1,2], [1,3], [1,4]}` — contiguous (D-CTG★), minimum `[1,1] = [s_C, 1]` (D-MIN★), uniform depth 2 (S8-depth), structural form `{[s_C, k] : 1 ≤ k ≤ 4}` (D-SEQ★ at `n_{s_C} = 4`, `m_{s_C} = 2`; the general D-SEQ★ form `{[s_C, 1, ..., 1, k]}` has no intermediate 1s since the inner range from position 2 to position `m_{s_C} − 1 = 1` is empty). Link subspace: `V_{s_L}(d) = ∅`. The four pre-state provenance entries are assumed established by prior J0/J1★ couplings at d's initial population (the details are not material here).

**Goal.** Replace the I-address at the interior V-position `[1,2]` with a freshly allocated `a₂' ≠ a₂` of new content value. Positions `[1,3]` and `[1,4]` lie strictly above `[1,2]` under the V-ordering on `s_C` (T1 of ASN-0034 restricted to depth-2 positive tuples with first component 1), so a single-position K.μ⁻ + K.μ⁺ pair at `[1,2]` alone would leave `V_{s_C}(d)` with an interior hole at `[1,2]` between `[1,1]` and `[1,3]` at the intermediate state — the interior-hole shape excluded by D-CTG★. The replacement therefore decomposes as a multi-position K.μ⁻ removing the suffix from `[1,2]` upward, followed by K.α allocating `a₂'`, then a multi-position K.μ⁺ rebuilding the suffix with `a₂'` at `[1,2]` and the previously-mapped `a₃, a₄` at `[1,3], [1,4]`, and finally K.ρ recording the new provenance — four elementary steps in this order. (An alternative valid ordering, K.α before K.μ⁻, produces the same composite endpoints; the order chosen here keeps the K.μ⁻ removal at the head of the trace, matching the narrative of "interior replacement = remove suffix, then rebuild.")

**Step 1: K.μ⁻ — remove the interior suffix `{[1,2], [1,3], [1,4]}`.** Effect: `M_int(d) = {[1,1] ↦ a₁}`. Frame: `C_int = C`, `L_int = L`, `E_int = E`, `R_int = R`.

*Precondition discharge.* K.μ⁻'s explicit preconditions are: (a) `d ∈ E_doc` — satisfied by hypothesis (`d = 1.0.1.0.1 ∈ E_doc`); (b) `dom(M(d)) ≠ ∅` — satisfied (`dom(M(d)) = V_{s_C}(d) = {[1,1], [1,2], [1,3], [1,4]}` is non-empty, so the effect-clause requirement `dom(M_int(d)) ⊂ dom(M(d))` is satisfiable); (c) the contracted post-state `M_int(d)` must satisfy the per-state arrangement invariants S2, S3★, S8a, S8-depth, S8-fin, D-CTG★, and D-MIN★ — verified directly at `M_int` below under *Intermediate-state verification*.

*Chosen contraction shape (degree of freedom, not a precondition).* The K.μ⁻ amendment notes that no separate per-subspace shape precondition need be checked at firing time — D-CTG★ + D-MIN★ + D-SEQ★ at the post-state, together with K.μ⁻'s contractive effect clause, force the suffix-removal shape on each subspace as a *derived consequence* of the post-state invariants. The shape we *choose* for this trace (the operation's degree of freedom, designed-in to support the goal of replacing the interior position `[1,2]` by removing the suffix from `[1,2]` upward):
- *Content subspace.* `V_{s_C}(d) = {[1,1], [1,2], [1,3], [1,4]}` shrinks to `V_{s_C}(d_int) = {[1,1]}` — a partial suffix removal retaining `n'_{s_C} = 1` of the four pre-state positions. The retained prefix `{[s_C, 1]}` and the removed suffix `{[s_C, k] : 1 < k ≤ 4}` are the partition forced by the post-state D-CTG★ + D-MIN★ + D-SEQ★ once the contraction commits.
- *Link subspace.* `V_{s_L}(d) = V_{s_L}(d_int) = ∅` — no link-subspace positions to remove (the post-state shape is trivially the empty arrangement).

Since `dom(M(d)) ≠ ∅` (precondition (b)) and the chosen contraction shape produces strict contraction on the content subspace (4 → 1), the effect-clause requirement `dom(M_int(d)) ⊂ dom(M(d))` is satisfied at the whole-arrangement level. K.μ⁻ commits; the per-subspace shape is what the post-state invariants confirm ex post, not what was verified as a precondition ex ante.

*Intermediate-state verification at M_int.* Two classes of property must be distinguished. The *per-state invariants* (D-CTG★, D-MIN★, D-SEQ★, S2, S3★, S8a, S8-depth, S8-fin, P6, P7, P8, and others enumerated in ExtendedReachableStateInvariants Class (a)) hold at every intermediate state — including M_int — by elementary preservation, since K.μ⁻'s postconditions discharge them. The *composite-boundary properties* (P4★, P4a, P7a — Class (b)) need *not* hold at M_int as a precondition: ValidComposite★ scopes the J0/J1★/J1'★ couplings (and hence Class (b)'s discharge) between Σ and Σ', not at each intermediate state. We verify the Class (a) per-state invariants at M_int below; P4★ at M_int is a *consequence* of K.μ⁻'s contractive action on Contains_C, not a requirement we must establish to take the step.

- *D-CTG★ at M_int:* `V_{s_C}(d_int) = {[1,1]}` is a singleton — vacuously contiguous under the V-ordering on `s_C` (no two distinct members bracket an interval). ✓
- *D-MIN★ at M_int:* `min(V_{s_C}(d_int)) = [1,1] = [s_C, 1]` of depth `m_{s_C} = 2`. ✓
- *D-SEQ★ at M_int:* `V_{s_C}(d_int) = {[s_C, 1]}` matches `{[s_C, k] : 1 ≤ k ≤ 1}` at `n_{s_C} = 1` (`m_{s_C} = 2`, so the general form has zero intermediate 1s). ✓
- *S2, S3★, S8a, S8-depth, S8-fin at M_int:* the surviving mapping `[1,1] ↦ a₁` is functional, has all-positive components and uniform depth 2 in `s_C`, with `a₁ ∈ dom(C_int) = dom(C)`. ✓
- *Per-state invariants at M_int:* P6/P7/P8 preserved by K.μ⁻'s frame on C, E, R. ✓
- *P4★ at M_int (consequence, not requirement).* `Contains_C(M_int) = {(a₁, d)} ⊆ Contains_C(Σ) ⊆ R = R_int`. P4★ holds at M_int as a consequence of K.μ⁻'s monotonicity: K.μ⁻ can only shrink Contains_C and R is unchanged (J2). The pairs `(a₂, d), (a₃, d), (a₄, d)` exit Contains_C at this step but remain in R as stale entries. ValidComposite★ does not require P4★ at intermediate states; the next intermediate state M_post (after K.μ⁺ but before K.ρ) genuinely violates P4★ at the pair `(a₂', d)`, with restoration occurring at the trailing K.ρ.

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

**Composite verification at `Σ →* Σ'`.**

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
- *P4★ (Contains_C ⊆ R).* `Contains_C(Σ') ⊇ {(a₁, d), (a₂', d), (a₃, d), (a₄, d)}`; each pair is in R' — `(a₁, d), (a₃, d), (a₄, d) ∈ R ⊆ R'` by P2, and `(a₂', d) ∈ R'` by K.ρ. The stale pair `(a₂, d) ∈ R' \ Contains_C(Σ')` records that d once contained `a₂`, the historical fact that survives the replacement. ✓
- *P6 (Existential coherence).* `origin(a₂') = d ∈ E_doc`; pre-existing content addresses retain their origin entities by frame. ✓
- *P7 (Provenance grounding).* `(a₂', d) ∈ R'` has `a₂' ∈ dom(C')`; pre-existing R entries retain their grounding by P0. ✓
- *P7a (Provenance coverage).* every `a ∈ dom(C')` has at least one provenance entry — `a₁, a₂, a₃, a₄` retain their pre-state entries (R ⊆ R' by P2), and `a₂'` has the freshly added `(a₂', d)`. ✓
- *D-CTG★, D-MIN★ at Σ'.* `V_{s_C}(d') = {[1,1], [1,2], [1,3], [1,4]}` contiguous, minimum `[1,1] = [s_C, 1]`. ✓


## Worked example: prior-provenance and first-time-transcluded replacements

We trace the *two-step* and *three-step* replacement composite variants — distinct from the four-step *fresh-content* form exercised in *Worked example: interior content replacement* above by the I-address class involved. Both variants re-use a pre-existing `dom(C)` address (no K.α), but they differ in whether `d` has prior provenance for it: the two-step form uses `(aₓ, d) ∈ R` (P2-preserved from a prior insertion-deletion cycle), the three-step form adds a trailing K.ρ to record first-time provenance.

*Common pre-state Σ_a.* Document `d = 1.0.1.0.1 ∈ E_doc`, content store `C ⊇ {a₁ ↦ char₁, a₂ ↦ char₂, aₓ ↦ charₓ}`, arrangement `M(d) = {[1,1] ↦ a₁, [1,2] ↦ a₂}` (so `V_{s_C}(d) = {[1,1], [1,2]}`, satisfying D-CTG★/D-MIN★/D-SEQ★ at `n_{s_C} = 2`). The address `aₓ = 1.0.1.0.1.0.1.5` is already in `dom(C)` — its allocation history and `R` status differ between the two variants below. Goal in each: replace `[1,2] ↦ a₂` with `[1,2] ↦ aₓ`.

**Two-step variant — prior-provenance replacement.** Σ_a additionally has `(aₓ, d) ∈ R` (e.g., aₓ was previously arranged at some V-position of d, K.μ⁻ removed it, but P2 retained the entry). Composite: K.μ⁻ (remove `[1,2]`) → K.μ⁺ (add `[1,2] ↦ aₓ`). Net change: `dom(C') = dom(C)` (no K.α), `dom(M'(d)) = {[1,1], [1,2]}` (the V-position domain returns to its pre-state shape), `ran(M'(d)|_{s_C}) = {a₁, aₓ}`, `R' = R`.

*Step 1: K.μ⁻ — remove `[1,2]`.* Caller chooses `(n'_{s_C}, n'_{s_L}) = (1, 0)` against pre-state `(n_{s_C}, n_{s_L}) = (2, 0)`. Strict contraction `1 < 2` on the content subspace; K.μ⁻ fires. `M_int(d) = {[1,1] ↦ a₁}`.

*Step 2: K.μ⁺ — add `[1,2] ↦ aₓ`.* Precondition `aₓ ∈ dom(C_int) = dom(C)` ✓ (pre-existing in `dom(C)`); new V-position `[1,2]` satisfies the K.μ⁺ amendment (`subspace([1,2]) = s_C`) and is disjoint from `dom(M_int(d)) = {[1,1]}`. K.μ⁺ fires, producing `M'(d) = {[1,1] ↦ a₁, [1,2] ↦ aₓ}`. D-CTG★, D-MIN★, D-SEQ★ at the post-state read off `V_{s_C}(d') = {[1,1], [1,2]}` directly.

*Composite coupling verification at Σ →* Σ'.*
- *J0:* `dom(C') = dom(C)`, no fresh content allocation — vacuous. ✓
- *J1★ (range-new content-subspace coupling):* `ran(M'(d)|_{s_C}) \ ran(M(d)|_{s_C}) = {a₁, aₓ} \ {a₁, a₂} = {aₓ}`. J1★ requires `(aₓ, d) ∈ R'`. Pre-state has `(aₓ, d) ∈ R ⊆ R'` (P2). ✓ — *no K.ρ is invoked, and J1★ is discharged by the pre-state membership alone.* This is what distinguishes the two-step form: the substantive precondition `(aₓ, d) ∈ R` at the pre-state is what makes K.ρ unnecessary at the composite boundary.
- *J1'★ (new-provenance check):* `R' \ R = ∅` (no K.ρ in the composite). Vacuous. ✓

*Post-state invariants:* S2 (the new mapping at `[1,2]` is single-valued and at a position pairwise distinct from `[1,1]`); S3★ (the new content-subspace mapping targets `aₓ ∈ dom(C')`); P4★ (`Contains_C(Σ') ⊆ R'` holds because `(aₓ, d) ∈ R ⊆ R'`; the stale `(a₂, d) ∈ R' \ Contains_C(Σ')` records the historical fact that d once contained a₂); D-CTG★/D-MIN★/D-SEQ★ on `V_{s_C}(d') = {[1,1], [1,2]}` (the canonical shape at `n_{s_C} = 2`). The historical asymmetry is concrete: `R' = R ⊇ {(a₂, d), (aₓ, d)}` — both pre-state entries persist — while `Contains_C(Σ') = {(a₁, d), (aₓ, d)}` reflects only the current arrangement. ∎

**Three-step variant — first-time transcluded replacement.** Σ_a has `(aₓ, d) ∉ R` instead — aₓ was allocated by another document `d_src ≠ d` (its origin), and recorded as `(aₓ, d_src) ∈ R`, but d has never previously arranged aₓ. Composite: K.μ⁻ (remove `[1,2]`) → K.μ⁺ (add `[1,2] ↦ aₓ`) → K.ρ (record `(aₓ, d)`). Net change: `dom(C') = dom(C)`, `ran(M'(d)|_{s_C}) = {a₁, aₓ}`, `R' = R ∪ {(aₓ, d)}`.

*Steps 1 and 2 (K.μ⁻, K.μ⁺):* identical to the two-step variant's Steps 1 and 2. After K.μ⁺, the intermediate state `Σ_post-K.μ⁺` has `Contains_C(Σ_post-K.μ⁺) ⊇ {(aₓ, d)}` but `R_post-K.μ⁺ = R ∌ (aₓ, d)` — *P4★ transiently fails* at this composite-internal state. ValidComposite★ allows the transient failure; restoration comes at Step 3.

*Step 3: K.ρ — record `(aₓ, d)`.* Preconditions: `aₓ ∈ dom(C_post-K.μ⁺) = dom(C)` ✓; `d ∈ E_doc` ✓. K.ρ fires, producing `R' = R ∪ {(aₓ, d)}`. **P4★ restored**: `Contains_C(Σ') ⊆ R'` because the new pair `(aₓ, d)` is now in `R'`.

*Composite coupling verification at Σ →* Σ'.*
- *J0:* `dom(C') = dom(C)`, no fresh content allocation — vacuous. ✓
- *J1★:* `ran(M'(d)|_{s_C}) \ ran(M(d)|_{s_C}) = {aₓ}`. J1★ requires `(aₓ, d) ∈ R'`. Pre-state has `(aₓ, d) ∉ R`. K.ρ at Step 3 supplies `(aₓ, d) ∈ R'`. ✓ — *the K.ρ step is required*; without it, J1★ would fail at the composite boundary, invalidating the composite under ValidComposite★. The substantive precondition `(aₓ, d) ∉ R` at the pre-state is what forces the third K.ρ step versus the two-step form's pre-state membership.
- *J1'★:* `R' \ R = {(aₓ, d)}`. For the entry `(aₓ, d)`, the witnessing content-subspace V-position is `[1,2]` at the post-state: `aₓ ∈ ran(M'(d)|_{s_C})` (since `M'(d)([1,2]) = aₓ` with `subspace([1,2]) = s_C`) and `aₓ ∉ ran(M(d)|_{s_C}) = {a₁, a₂}`. The K.ρ entry is anchored in the K.μ⁺ extension. ✓

*Post-state invariants:* S2, S3★, P4★ (now restored), D-CTG★/D-MIN★/D-SEQ★ — all discharged analogously to the two-step variant. The notable difference at the historical layer: `R' = R ∪ {(aₓ, d)}` introduces a fresh provenance pair (`d` is now historically recorded as having contained aₓ for the first time), whereas the two-step variant added no new entry to R. ∎

**Contrast with the four-step fresh-content form.** The four-step composite K.μ⁻ + K.α + K.μ⁺ + K.ρ exercised in *Worked example: interior content replacement* allocates a fresh address `a₂'` extending `dom(C')`, requiring the K.α step (and an accompanying K.ρ for first-time provenance). The two- and three-step forms re-use a pre-existing `dom(C)` address `aₓ` and need only K.μ⁻ + K.μ⁺ for the arrangement change. The three forms partition by the (pre-state membership of `aₓ` in `dom(C)`, pre-state membership of `(aₓ, d)` in `R`) pair: (in C, in R) ⟹ two-step; (in C, not in R) ⟹ three-step; (not in C, not in R) ⟹ four-step. The (not in C, in R) combination is excluded by P7 (every provenance entry references `dom(C)`), so the three forms exhaust the valid cases.


## Worked example: link allocation and arrangement

We verify the central postconditions on concrete tumbler values. By SubspaceConventionAxiom (FixedSubspaceIdentifiers), `s_C = 1` and `s_L = 2` throughout (and SC-NEQ `1 ≠ 2` is satisfied automatically). Consider document `d` at address `1.0.1.0.1` with two text content addresses allocated and arranged.

*Initial state.* `dom(C) = {1.0.1.0.1.0.1.1, 1.0.1.0.1.0.1.2}`, `dom(L) = ∅`, `E_doc = {1.0.1.0.1}`, `R = {(1.0.1.0.1.0.1.1, d), (1.0.1.0.1.0.1.2, d)}` (implicit from prior J0/J1 of allocation).

Arrangement: `M(d) = {[1,1] ↦ 1.0.1.0.1.0.1.1, [1,2] ↦ 1.0.1.0.1.0.1.2}`.

Text-subspace V-positions: `V_1(d) = {[1,1], [1,2]}` — contiguous (D-CTG★), minimum at `[1,1]` (D-MIN★), depth 2 (S8-depth). Link subspace: `V_2(d) = ∅`.

**Step 1: K.λ — allocate link.** Create link `ℓ = 1.0.1.0.1.0.2.1` with value `(F, G, Θ)`.

Precondition verification:
- `d = 1.0.1.0.1 ∈ E_doc`
- `ℓ ∉ dom(L) ∪ dom(C)`: this is the first-emission case (no prior d-origin link), so freshness is SubAllocFresh at `x = L` (seed part for `dom(L)`; cross-subspace part — ℓ's element field `2.1` against content's `1.1`, `1.2` — for `dom(C)`)
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
- *L11a (Link distinctness for this K.λ event)*: this is the *first-link case* for `d` — the K.λ precondition predicate `{ℓ' ∈ dom(L) : origin(ℓ') = d} = ∅` holds because `dom(L) = ∅` at the pre-state, so the first-emission path of K.λ applies. The emitted address `ℓ = [d.0.s_L.1] = 1.0.1.0.1.0.2.1` is the first emission of d's link sub-allocator `A_L(d)`, and **SubAllocatorAxiom.FirstEmission** (per ASN-0093) directly supplies `ℓ ∉ dom(Σ.L) ∪ dom(Σ.C)` at the state of allocation — discharging both the freshness conjunct of K.λ's precondition and the L11a obligation that distinct K.λ events produce distinct link addresses. T10a GlobalUniqueness is *not* invoked for the first emission (the FirstEmission axiom is the load-bearing route here); GlobalUniqueness applies from the second emission onward, when the inc chain `A_L(d)` is in T10a's domain. ✓
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
- `V_{s_L}(d) = ∅`, so this first link-subspace insertion fixes `m_L(d) = 2` (any value ≥ 2 is admissible; we take 2 here), giving `v_ℓ = [s_L, 1] = [2, 1]` (D-MIN★ for empty link subspace)
- `#v_ℓ = 2 = m_L(d)` (S8-depth)

Effect: `M'(d) = {[1,1] ↦ 1.0.1.0.1.0.1.1, [1,2] ↦ 1.0.1.0.1.0.1.2, [2,1] ↦ 1.0.1.0.1.0.2.1}`.

Post-state verification:
- S3★: `subspace([1,1]) = 1 = s_C` and `M'(d)([1,1]) = 1.0.1.0.1.0.1.1 ∈ dom(C)`; `subspace([1,2]) = 1 = s_C` and `M'(d)([1,2]) = 1.0.1.0.1.0.1.2 ∈ dom(C)`; `subspace([2,1]) = 2 = s_L` and `M'(d)([2,1]) = 1.0.1.0.1.0.2.1 ∈ dom(L')`
- CL-OWN: the only link-subspace position is `[2,1]` with `origin(M'(d)([2,1])) = origin(1.0.1.0.1.0.2.1) = 1.0.1.0.1 = d`
- D-CTG★: `V_1(d) = {[1,1], [1,2]}` contiguous; `V_2(d) = {[2,1]}` singleton, trivially contiguous
- D-MIN★: `min(V_1(d)) = [1,1] = [s_C, 1]`; `min(V_2(d)) = [2,1] = [s_L, 1]`
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

**Step 4: K.λ + K.μ⁺_L — allocate and arrange a second link.** To exercise link-subspace contraction below we need a non-singleton link subspace. Allocate `ℓ₂ = 1.0.1.0.1.0.2.2 = inc(ℓ, 0)` (the next sibling on d's link frontier under TA5(c), per K.λ's subsequent-link case) with some value `(F', G', Θ')`; then arrange `ℓ₂` at `v_{ℓ₂} = shift(max(V_{s_L}(d)), 1) = shift([2,1], 1) = [2,2]` (D-CTG★ case of K.μ⁺_L).

Effect after both transitions: `L = {ℓ ↦ (F, G, Θ), ℓ₂ ↦ (F', G', Θ')}`, `M''(d) = {[1,1] ↦ a₂, [1,2] ↦ a₁, [2,1] ↦ ℓ, [2,2] ↦ ℓ₂}`. Link-subspace V-positions: `V_{s_L}(d) = {[2,1], [2,2]}` — contiguous (D-CTG★), minimum at `[2,1] = [s_L, 1]` (D-MIN★), depth 2 (S8-depth), structural form `{[s_L, k] : 1 ≤ k ≤ 2}` (D-SEQ★ with `n_{s_L} = 2`, `m_{s_L} = 2`; the general form `{[s_L, 1, ..., 1, k]}` has zero intermediate 1s). *J1'★ (vacuous):* both K.λ and K.μ⁺_L hold R in frame, so `R' \ R = ∅` for the composite — no new provenance entries are introduced, and J1'★ is vacuously satisfied. The K.μ⁺_L step adds only link-subspace V-positions, so the content-subspace range of M''(d) is unchanged across the composite, consistent with J1'★'s content-subspace scoping. ✓

Post-state verification (for the K.λ + K.μ⁺_L composite):
- *L11a (Link distinctness for this K.λ event)*: this is the *subsequent-link case* for `d` — the K.λ precondition predicate `{ℓ' ∈ dom(L) : origin(ℓ') = d} ≠ ∅` holds because Step 1's `ℓ ∈ dom(L)` has `origin(ℓ) = d`, so the subsequent-emission path of K.λ applies. The emitted address `ℓ₂ = inc(max{ℓ' ∈ dom(L) : origin(ℓ') = d}, 0) = inc(ℓ, 0) = 1.0.1.0.1.0.2.2` advances `A_L(d)`'s frontier by one sibling-increment via TA5(c). Freshness `ℓ₂ ∉ dom(L) ∪ dom(C)` is SubAllocFresh at `x = L` (frontier-advance part against `dom(L)`, cross-subspace part against `dom(C)`), giving `ℓ₂ ≠ ℓ` — the L11a obligation that this K.λ event produce an address distinct from every prior K.λ event under d (here, the single prior event at Step 1 producing ℓ). ✓
- *S3★:* the new link-subspace position `[2,2]` has `subspace([2,2]) = s_L` and maps to `ℓ₂ ∈ dom(L')`; existing positions retain their pre-state values. ✓
- *CL-OWN:* `origin(M''(d)([2,2])) = origin(ℓ₂) = d` (K.λ's `origin(ℓ₂) = d` precondition combined with the K.μ⁺_L placement). ✓
- *CL-UNIQ:* `ℓ₂` is fresh to `dom(L)` (K.λ's allocation precondition), so no prior V-position references it; the new V-position `[2,2]` is therefore the unique link-subspace V-position mapping to `ℓ₂`. ✓
- *L0/L1/L1a/L3/L-fin:* each established for `ℓ₂` by K.λ's preconditions and inherited at the post-state.
- *L14:* `dom(C) ∩ dom(L') = ∅` — the new link `ℓ₂` has `subspace_I(ℓ₂) = s_L = 2`, distinct from `s_C = 1`. ✓

**Step 5: K.μ⁻ — admissible suffix removal of links.** Remove the mapping at `[2,2]` — the maximum end of `V_{s_L}(d)`, a 1-element suffix of the link-subspace range.

*Constructive precondition (caller's choice, verified at the pre-state).* K.μ⁻'s constructive precondition asks the caller to commit to per-subspace retention counts `(n'_{s_C}, n'_{s_L})` against the pre-state values `(n_{s_C}, n_{s_L}) = (2, 2)` read from D-SEQ★ at Σ (the pre-state Σ has `V_{s_C}(d) = {[1,1], [1,2]}` and `V_{s_L}(d) = {[2,1], [2,2]}`, both matching the canonical `{[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` form at depth 2). For the goal of removing the maximum link-subspace position, the caller chooses `(n'_{s_C}, n'_{s_L}) = (2, 1)`. Precondition checks at the pre-state:
- `d ∈ E_doc`: ✓ (carried forward from earlier steps).
- `dom(M(d)) ≠ ∅`: ✓ — `V_{s_C}(d) ∪ V_{s_L}(d) = {[1,1], [1,2], [2,1], [2,2]}` is non-empty.
- Per-subspace retention counts in admissible range: `n'_{s_C} = 2 ∈ {0, 1, 2} = {0, …, n_{s_C}}`, ✓; `n'_{s_L} = 1 ∈ {0, 1, 2} = {0, …, n_{s_L}}`, ✓.
- Strict contraction on at least one subspace: `n'_{s_L} = 1 < 2 = n_{s_L}` (the link subspace shrinks strictly), ✓; the content subspace is held fixed (`n'_{s_C} = n_{s_C}`).

The precondition is satisfied; K.μ⁻ fires. The retained domain is `R := ∪_{S ∈ {s_C, s_L}} {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S} = {[1,1], [1,2], [2,1]}`, and the constructive effect is `M'''(d) = M''(d) ↾ R`.

*Post-state shape (derived from the constructive precondition).* `dom(M'''(d)) = {[1,1], [1,2], [2,1]} ⊂ dom(M''(d))`. Surviving mappings unchanged: `M'''(d)([1,1]) = a₂`, `M'''(d)([1,2]) = a₁`, `M'''(d)([2,1]) = ℓ`. The content subspace is unchanged: `V_{s_C}(d') = {[1,1], [1,2]}`. The link subspace contracts to a 1-element suffix prefix: `V_{s_L}(d') = {[2,1]}`. Per-subspace shape:
- *Content subspace.* `V_{s_C}(d') = V_{s_C}(d)` — zero-suffix removal at `n'_{s_C} = 2`.
- *Link subspace.* `V_{s_L}(d') = {[2,1]}` — 1-element suffix-prefix retention at `n'_{s_L} = 1`.

Post-state invariant verification:
- *S3★:* surviving mappings retain their pre-state values; `[2,1] ↦ ℓ ∈ dom(L)` satisfies the link clause. ✓
- *D-CTG★:* `V_{s_C}(d') = {[1,1], [1,2]}` and `V_{s_L}(d') = {[2,1]}` are each contiguous. ✓
- *D-MIN★:* `min(V_{s_C}(d')) = [1,1] = [s_C, 1]`; `min(V_{s_L}(d')) = [2,1] = [s_L, 1]`. ✓
- *D-SEQ★:* `V_{s_L}(d') = {[s_L, 1]}` matches `{[s_L, k] : 1 ≤ k ≤ 1}` at `n_{s_L} = 1` (`m_{s_L} = 2`, so the general D-SEQ★ form has zero intermediate 1s). ✓
- *CL-OWN:* `origin(M'''(d)([2,1])) = origin(ℓ) = d` (preserved from pre-state by frame on the surviving mapping). ✓
- *CL-UNIQ:* the surviving link-subspace mapping is the singleton `{[2,1] ↦ ℓ}`; vacuously injective. ✓
- *L12:* `dom(L)` unchanged — `ℓ₂` remains in `dom(L)` despite no longer being arranged. ✓ This is the *orphan link* state Nelson identifies (LM 4/9): `ℓ₂ ∈ dom(L)` but `ℓ₂ ∉ ran(M'''(d))` for any d.
- *J1'★ (vacuous):* K.μ⁻ holds R in frame, so `R' \ R = ∅`. No new provenance entries to check; J1'★ is vacuously satisfied. (J1'★ is range-based: the content-subspace range `ran(M'''(d)|_{s_C}) = ran(M''(d)|_{s_C}) = {a₁, a₂}` is unchanged across this link-subspace contraction — the link-subspace range loses ℓ₂, but the link subspace is outside J1'★'s scope.) ✓

An attempt to remove `[2,1]` while retaining `[2,2]` is excluded by D-MIN★ (the missing-minimum shape); an attempt to remove an interior position while retaining both endpoints is excluded by D-CTG★ (the interior-hole shape).


## Cross-layer invariants

**P6 (Existential coherence).** For every I-address in the content store, its origin document exists as an entity:

`(A a ∈ dom(C) :: origin(a) ∈ E_doc)`

*Derivation.* K.α allocates a under origin(a)'s prefix (S7a, ASN-0036), and requires origin(a) ∈ E_doc as a precondition — the allocation mechanism inc(·, k) operates on an existing tumbler within the ownership domain. P1 preserves entity membership across subsequent transitions; P0 preserves a ∈ dom(C). Initial state: dom(C₀) = ∅, so the quantifier is vacuously satisfied. Inductive step: each K.α has origin(a) ∈ E_doc by precondition; P0 preserves a; P1 preserves origin(a). ∎

**P7 (Provenance grounding).** Every provenance entry references allocated content:

`(A (a, d) ∈ R :: a ∈ dom(C))`

*Derivation.* K.ρ requires a ∈ dom(C) as a precondition. P0 preserves dom(C). By induction: initially R₀ = ∅ (vacuous). Each K.ρ adds (a, d) with a ∈ dom(C); P0 ensures a remains in dom(C') for all subsequent states; P2 ensures (a, d) remains in R'. ∎

**P7a (Provenance coverage).** Every I-address in the content store has at least one provenance record:

`(A a ∈ dom(C) :: (E d :: (a, d) ∈ R))`

*Derivation.* P7a is a composite-boundary property (Class (b)); its discharge is given in the *Extended reachable-state invariants* section under the P7a Class (b) argument — for `a ∈ dom(C') \ dom(C)`, J0 supplies a witnessing V-position `v`, the S3★ + L14 + S3★-aux step forces `subspace(v) = s_C`, and J1★ then supplies `(a, d) ∈ R'`. We do not restate it here. ∎

**GlobalLineage (Derived corollary, GlobalDescentFromBootstrap).** Every entity, content address, and link address descends structurally from the bootstrap node n₀:

`(A x ∈ E ∪ dom(C) ∪ dom(L) :: n₀ ≼ x)`

*Derivation.* The three components are discharged separately.

*(i) Entities.* `(A e ∈ E :: n₀ ≼ e)`. For `IsNode(e)`, NodeLineage gives `n₀ ≼ e` directly. For `¬IsNode(e)`, P8 supplies `parent(e) ∈ E` with `zeros(parent(e)) = zeros(e) − 1` (T4b's parent projection). By the parent definition — `parent(e)` is obtained by truncating e's last field and the preceding zero separator — we have `parent(e) ≼ e` under the tumbler-prefix order (ASN-0034). Recursive descent through parent chains terminates at a node (since each step strictly decreases `zeros`, and entities satisfy `zeros ∈ {0, 1, 2}` by the entity-set definition, the chain reaches `zeros = 0` in at most two steps — the longest case being a document with `zeros = 2`, whose parent is an account with `zeros = 1`, whose parent is a node with `zeros = 0`), where NodeLineage applies. Transitivity of ≼ over the parent chain `e ≽ parent(e) ≽ parent(parent(e)) ≽ ... ≽ node` together with NodeLineage at the node gives `n₀ ≼ e`.

*(ii) Content addresses.* `(A a ∈ dom(C) :: n₀ ≼ a)`. By P6, `origin(a) ∈ E_doc ⊆ E`, so (i) gives `n₀ ≼ origin(a)`. By S7a, `a` is allocated under `origin(a)`'s prefix — formally, `origin(a) ≼ a` (origin recovers the document-level prefix of a by truncating to `zeros = 2`). Transitivity of ≼ closes: `n₀ ≼ origin(a) ≼ a`.

*(iii) Link addresses.* `(A ℓ ∈ dom(L) :: n₀ ≼ ℓ)`. By L1a, `origin(ℓ) ∈ E_doc ⊆ E`, so (i) gives `n₀ ≼ origin(ℓ)`. By L1c, ℓ is reachable from `origin(ℓ)` by a structural inc-chain (per-step inc-rule conformance, not full T10a discipline; see L1c discharge) with `t₀ = origin(ℓ)`, `t_n = ℓ`, `k₁ = 2`, and each subsequent `kᵢ ∈ {0, 1, 2}`. We show the stronger claim that `origin(ℓ)`'s prefix is preserved across the entire chain — i.e., `tᵢ[j] = origin(ℓ)[j]` for every `j ≤ #origin(ℓ)` and every `i ≥ 0` — by induction on `i`, with auxiliary property `sig(tᵢ) > #origin(ℓ)` for `i ≥ 1`. *Base (i = 0):* `t₀ = origin(ℓ)` agrees with itself on positions `1..#origin(ℓ)`. *Step i = 1 (k₁ = 2):* `t₁ = inc(origin(ℓ), 2)` extends by two positions (one zero separator, then `1`), so TA5(d) gives `t₁[j] = origin(ℓ)[j]` for `j ≤ #origin(ℓ)`, `#t₁ = #origin(ℓ) + 2`, and the rightmost nonzero component of `t₁` is at position `#origin(ℓ) + 2` (the final `1`), so `sig(t₁) = #origin(ℓ) + 2 > #origin(ℓ)`. *Step i + 1 (i ≥ 1):* split on `kᵢ₊₁`. If `kᵢ₊₁ > 0`: TA5(b) preserves positions `1..#tᵢ` exactly, so positions `1..#origin(ℓ) ≤ #tᵢ` are preserved; TA5(d) at `kᵢ₊₁ > 0` places the new value `1` at position `#tᵢ + kᵢ₊₁`, the new rightmost nonzero component of `tᵢ₊₁`, so `sig(tᵢ₊₁) = #tᵢ + kᵢ₊₁ > #tᵢ ≥ #origin(ℓ) + 2 > #origin(ℓ)`. If `kᵢ₊₁ = 0`: TA5(c) modifies only position `sig(tᵢ)`, and by the inductive auxiliary `sig(tᵢ) > #origin(ℓ)`, so positions `1..#origin(ℓ)` are untouched and remain equal to `origin(ℓ)`'s; `sig(tᵢ₊₁) = sig(tᵢ) > #origin(ℓ)`. Hence `tᵢ[j] = origin(ℓ)[j]` for all `j ≤ #origin(ℓ)` and all `i ≥ 0`. Instantiating at `i = n` gives `origin(ℓ) ≼ ℓ`. Transitivity of ≼ closes: `n₀ ≼ origin(ℓ) ≼ ℓ`. ∎

GlobalLineage promotes NodeLineage from a node-restricted invariant to a docuverse-wide rooted-tree property: the entity hierarchy, content store, and link store all descend from the single bootstrap address n₀.


## Extended reachable-state invariants

The atomicity guarantee of SequentialTransitionAxiom commits *elementary* transitions to single-event atomicity — not composites. A composite Σ →* Σ' is a sequence of atomic elementary transitions, and the intermediate states between elementary steps are real, observable states of the transition system. Properties of the reachable-state space therefore partition by *temporal scope* into two classes:

- *Per-state invariants* hold at **every** reachable state — every initial state, every elementary-transition target state, every intermediate state within a composite. Each elementary transition preserves these individually, so they are true invariants of the elementary transition system.
- *Composite-boundary properties* hold only at *composite boundaries* (the initial Σ and final Σ' of any valid composite) and may transiently fail at intermediate states within a composite. They are not invariants of the elementary transition system — they are properties guaranteed by the J0/J1★/J1'★ couplings of ValidComposite★, restored at the close of each valid composite rather than preserved by each elementary step. Calling them "invariants" would be misleading in the strict state-machine sense; we name them *composite-boundary properties* throughout.

This distinction reflects Nelson's design: at the docuverse layer, compound user actions decompose into sequences of elementary commands whose intermediate states are conceptually observable to other agents (LM 4/63 — FEBE commands return acknowledgments individually, with no transaction wrapper around compound flows). Only CREATENEWVERSION is atomic at the protocol level; other compound flows expose intermediate states by design. Composite-boundary properties capture the design intent that *valid composites* must restore them — not that the system never observes states violating them.

*Concrete trace illustrating transient failure and restoration.* Consider a fresh-content insertion composite K.α → K.μ⁺ → K.ρ targeting document `d ∈ E_doc` and allocating new address `a` with value `v`. The trace exhibits P7a (every `a ∈ dom(C)` has at least one provenance entry) transitioning through its transient failure and restoration:

| Step | State after step | P7a status at `a` |
|------|------------------|------------------|
| (initial Σ) | `a ∉ dom(C)`, `(·, d) ∉ R` for any `·` involving `a` | vacuously satisfied — `a` not yet in dom(C) |
| K.α fires | `a ∈ dom(C')`, no `(a, ·) ∈ R` | **transient failure**: `a ∈ dom(C)` but no provenance entry exists |
| K.μ⁺ fires | `a ∈ dom(C)`, `v_a ∈ dom(M(d))` with `M(d)(v_a) = a`, still no `(a, ·) ∈ R` | still failing — K.μ⁺ holds R in frame |
| K.ρ fires (composite boundary Σ') | `a ∈ dom(C')`, `(a, d) ∈ R'` | **restored** — P7a satisfied with witness `(a, d) ∈ R'` |

Per-state invariants (e.g., S2, S3★, C-fin, L14) hold at every row, including the K.α and K.μ⁺ rows — these are elementary-preserved. P7a is a composite-boundary property and need hold only at the initial Σ and the final Σ'; the two interior rows admit it as transiently false. ValidComposite★'s J0 coupling forces the composite to end with K.μ⁺ followed by K.ρ (in some order, but both must fire), so the boundary-restoration is guaranteed by construction.

**ExtendedReachableStateInvariants.** Every state reachable from Σ₀ by a finite sequence of valid composite transitions satisfies the *per-state invariants* below; every state at a composite boundary (Σ or Σ' of a valid composite) additionally satisfies the *composite-boundary properties* below.

  *Per-state invariants* (Class (a) of the proof below — preserved step-by-step by each elementary transition):

  S2 ∧ S3★ ∧ S3★-aux ∧ S4 ∧ S7a ∧ S7b ∧ C1b ∧ S7d ∧ S8a ∧ S8-fin ∧ S8-depth ∧ S8★ ∧ C-fin ∧ D-CTG★ ∧ D-MIN★ ∧ D-SEQ★ ∧ P6 ∧ P7 ∧ P8 ∧ NodeLineage ∧ L0 ∧ L1 ∧ L1a ∧ L1b ∧ L1c ∧ L3 ∧ L14 ∧ L-fin ∧ CL-OWN ∧ CL-UNIQ

  *Composite-boundary properties* (Class (b) of the proof below — discharged at boundaries by J0/J1★/J1'★):

  P4★ ∧ P4a ∧ P7a

  The Class (b) properties may transiently fail at intermediate states; in particular, a composite that allocates fresh content (K.α) violates P7a at the post-K.α intermediate state (the new I-address is in dom(C') but no (·, d) entry yet sits in R'), with restoration by the composite-trailing K.ρ.

ASN-0036's S7d (document allocation discipline) is preserved unchanged: every `d ∈ E_doc` is T4-valid with `zeros(d) = 2`, placed in E_doc by a K.δ event satisfying `e ∉ E` discharged by T10a's GlobalUniqueness on the parent allocator's tracked domain.

**ExtendedTransitionInvariants (per-transition).** Every valid composite transition `Σ →* Σ'` satisfies:

  P3

P3 is the conjunction P0 ∧ P1 ∧ P2 ∧ L12 (extending ASN-0043's L12 with the four-component monotonicity predicates of this ASN), so naming P3 alone covers every per-transition monotonicity obligation. P0 subsumes ASN-0036's S0 (ContentImmutability) and S1 (StoreMonotonicity); ASN-0036's S9 (TwoStreamSeparation) — arrangement mutations cannot alter the content store — follows from P0 by the arrangement frames: every M-mutating transition (K.μ⁺, K.μ⁺_L, K.μ⁻, and K.μ~ by composition of the first two) carries `C' = C` in its frame, so no arrangement mutation touches `dom(C)` or any stored value, which is exactly what P0's append-only, value-immutable content store already guarantees.

*Proof.* The proof proceeds by induction on the number of valid composite transitions from Σ₀. The reachable-state property set partitions into two classes by temporal scope: *per-state invariants* preserved by each elementary transition individually, and *composite-boundary properties* that may be violated at intermediate states within a composite but hold at every composite boundary. The per-transition invariants are addressed last, in a single elementary-case check.

**Base.** The extended initial state Σ₀ satisfies every per-state invariant (verified in the Link store and extended system state section — L₀ = ∅ satisfies link invariants vacuously, including L3; S3★ and P4★ reduce to S3 and P4; S3★-aux holds vacuously since M₀(d) = ∅ for all d; D-CTG and D-MIN hold vacuously since V_S(d) = ∅ for every subspace S). The per-transition invariants have no base case — they are vacuous before any transition has occurred — and enter the induction at the first step.

**Class (a): Per-state invariants** — preserved by each elementary transition individually, holding at every reachable state including intermediate states within composites. These are all per-state properties except P4★, P4a, and P7a: S2, S3★, S3★-aux, S4, S7a, S7b, C1b, S7d, S8a, S8-fin, S8-depth, S8★, C-fin, D-CTG★, D-MIN★, D-SEQ★, P6, P7, P8, NodeLineage, L0, L1, L1a, L1b, L1c, L3, L14, L-fin, CL-OWN, CL-UNIQ.

*Verification matrix.* Each cell names the load-bearing discharge for that (invariant, transition) pair; `frame` indicates the transition holds the relevant state component unchanged and so trivially preserves the invariant; `n/a` indicates the invariant's scope does not intersect the transition's effect (e.g., L0's L-clause is `n/a` for transitions that frame both L and C). For link-store invariant rows (L0, L1, L1a, L1b, L1c, L3, L14, L-fin, CL-OWN, CL-UNIQ), `frame` under K.α, K.μ⁺, K.μ⁻ rests on the amended forms of *Amendments to existing transitions* above, which add the explicit `L' = L` conjunct (or, for K.α, ASN-0093's frame supplying it directly), not on the original pre-link transitions, which made no commitment about L. K.μ~ cells invoke the full-clearance form (`n'_{s_C} = 0`) of the K.μ⁻ + K.μ⁺ decomposition per the convention fixed at *Decomposition of K.μ~* (any cell not naming a cut point reads as full-clearance, which is admissible for every admissible π).

| Invariant | K.α | K.δ | K.λ | K.μ⁺ | K.μ⁺_L | K.μ⁻ | K.μ~ | K.ρ |
|-----------|-----|-----|-----|------|--------|------|------|-----|
| S2 | frame | frame (M(e)=∅ on new entity disjoint) | frame | new positions disjoint from dom(M(d)) by value-preservation clause | new v_ℓ ∉ dom(M(d)) (verified at K.μ⁺_L) | restriction of M(d) | K.μ⁻ (full-clearance) restriction preserves single-valuedness on link-subspace survivors; K.μ⁺ adds content-subspace positions at fresh positions disjoint from the intermediate domain (per its value-preservation clause) | frame |
| S3★ | frame | frame | frame | amendment: subspace(v)=s_C ⟹ M'(d)(v)∈dom(C); link clause framed | precondition: ℓ∈dom(L) and subspace(v_ℓ)=s_L | restriction (values unchanged) | holds by the admissibility filter; see *Decomposition of K.μ~* |  frame |
| S3★-aux | frame | frame | frame | amendment: new positions have subspace s_C | precondition: new v_ℓ has subspace s_L | restriction (subspaces of survivors unchanged) | K.μ⁻ (full-clearance) restriction preserves subspaces of link-subspace survivors; K.μ⁺ amendment adds only content-subspace positions, so every post-state V-position has subspace s_C or s_L | frame |
| S4 (content distinctness, per ASN-0036) | SubAllocFresh at x = C | frame (does not add to dom(C)) | frame (does not add to dom(C)) | frame (no new addresses) | frame | frame | frame | frame |
| Entity distinctness (derived; distinct K.δ events produce distinct entity addresses) | frame (does not add to E) | T10a GlobalUniqueness on parent allocator (¬IsNode); NodeUniqueAllocation (IsNode) | frame (does not add to E) | frame | frame | frame | frame | frame |
| Link distinctness (derived; distinct K.λ events produce distinct link addresses — the L11a obligation in the extended state) | frame (does not add to dom(L)) | frame (does not add to dom(L)) | SubAllocFresh at x = L | frame | frame | frame | frame | frame |
| S7a | precondition: origin(a)∈E_doc | frame (e∉dom(C)) | frame | frame | frame | frame | frame | frame |
| S7b | K.α's `zeros(a) = 3` precondition (per ASN-0093) | frame | frame (link addresses not in dom(C)) | frame | frame | frame | frame | frame |
| C1b (ASN-0093) | K.α allocator chain produces E(a)=[s_C,k] ⟹ #E(a)≥2 | frame | frame | frame | frame | frame | frame | frame |
| S7d | frame | establishes new d∈E_doc via T10a per-`(t,k')` discipline; preserved by P1 | frame | frame | frame | frame | frame | frame |
| S8a, S8-depth, S8-fin | frame | new doc has M(d)=∅ (vacuous) | frame | precondition: positivity, depth, finite extension | precondition: positivity, depth m_L(d), finite | restriction preserves all three | S8a and S8-depth stipulated by admissibility (i); S8-fin(Σ') discharged independently of K.μ~-FIX through the K.μ⁻ + K.μ⁺ decomposition: K.μ⁻ restricts dom(M(d)) (a subset of a finite set is finite) and K.μ⁺ adds finitely many positions (finite + finite = finite), so finiteness is preserved by elementary preservation through the two atomic steps. The K.μ⁻ (full-clearance) + K.μ⁺ decomposition mechanically realises the stipulated invariants (K.μ⁻ restriction preserves all three on link-subspace survivors; K.μ⁺ preconditions re-establish them on the rebuilt content arrangement: positivity / uniform depth / finite extension at the rebuild positions) | frame |
| S8★ | frame | frame | frame | per-subspace projection via ASN-0036's S8 on M(d')\|_{V_{s_C}(d')} | trivial length-1 decomposition on M(d')\|_{V_{s_L}(d')} | restriction to trivial length-1 decomposition on survivors per subspace (the trivial length-1 form survives any contraction; an arbitrary restriction of a pre-state decomposition may break a length-`n` run, but the trivial length-1 fall-back — the same route used for the link-subspace S8★(s_L) cell — is always available on each subspace after contraction) | K.μ⁻ (full-clearance): link-subspace via fixity (trivial length-1 decomposition preserved pointwise; M'(d)\|_{dom_L} = M(d)\|_{dom_L} from Steps 1–3 of the link-subspace fixity proof); content-subspace decomposition rebuilt at K.μ⁺ post-state via the route at the K.μ⁺ cell (ASN-0036's S8 on the content-subspace projection of the rebuilt arrangement) | frame |
| D-CTG★ / D-MIN★ | frame | frame | frame | precondition discharge (K.μ⁺'s original precondition list, in *Elementary transitions*, requires the resulting M'(d) to satisfy D-CTG / D-MIN — strengthened to D-CTG★ / D-MIN★ in the extended state: content-subspace contiguity + minimum preserved) | preconditions cover D-MIN★ (empty case) and D-CTG★ (shift case) | constructive precondition discharge — the per-subspace retention count `n'_S` directly produces the canonical suffix-prefix shape `V_S(d') = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}` which satisfies D-CTG★ and D-MIN★ at Σ' by construction | stipulated by admissibility (i); the K.μ⁻ (full-clearance) + K.μ⁺ decomposition mechanically realises the stipulation. K.μ⁻ (full-clearance) by construction retains `V_{s_L}(d)` pointwise (the form clears only the content subspace), so D-CTG★ / D-MIN★ on the link subspace carry forward from Σ via the inductive hypothesis; content subspace empty after the clearance (D-CTG★ / D-MIN★ vacuous on the intermediate state). K.μ⁺ preconditions re-establish D-CTG★ / D-MIN★ on the rebuilt content arrangement at Σ' (per the K.μ⁺ cell's discharge above), mechanically completing the realisation of the admissibility-stipulated invariants | frame |
| D-SEQ★ | frame | frame | frame | derived from D-CTG★ + D-MIN★ + S8-depth + S8-fin + S8a | derived | derived | derived at Σ' from the K.μ~-chain post-state values of D-CTG★ + D-MIN★ + S8-depth + S8-fin + S8a — the first four constituents (D-CTG★, D-MIN★, S8-depth, S8a) stipulated by admissibility (i); S8-fin(Σ') discharged independently of K.μ~-FIX through the K.μ⁻ + K.μ⁺ decomposition (subset of a finite set is finite; finite + finite is finite), per the S8-fin cell above. The K.μ⁻ (full-clearance) + K.μ⁺ decomposition mechanically realises each constituent (see their respective cells above), and D-SEQ★ then follows at Σ' by the standard derivation | frame |
| P6 | precondition: origin(a)∈E_doc; preserved by P0/P1 | frame (does not add to dom(C)) | frame | frame | frame | frame | frame | frame |
| P7 | frame (does not add to R) | frame | frame | frame | frame | frame | frame | precondition: a∈dom(C); preserved by P0 |
| P8 | frame | parent(e)∈E precondition for ¬IsNode(e); vacuous for IsNode | frame | frame | frame | frame | frame | frame |
| NodeLineage | frame | K.δ case (i): n₀≼e from NodeUniqueAllocation clause (b); case (ii): outside IsNode scope | frame | frame | frame | frame | frame | frame |
| L0 (C-clause) | K.α's `E(a)₁ = s_C` precondition (per ASN-0093): subspace_I(a)=s_C; preserved by P0 | frame | frame | frame | frame | frame | frame | frame |
| L0 (L-clause) | frame | frame | precondition: subspace_I(ℓ)=s_L; preserved by L12 | frame | frame | frame | frame | frame |
| L1, L1a, L1b | frame | frame | preconditions (zeros(ℓ)=3, origin(ℓ)∈E_doc, #E(ℓ)≥2); preserved by L12 | frame | frame | frame | frame | frame |
| L1c | frame | frame | structural inc-chain established per K.λ allocation (first via SubAllocatorAxiom, subsequent via TA5(c)); preserved by L12 | frame | frame | frame | frame | frame |
| L3 | frame | frame | precondition: N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅; preserved by L12 | frame | frame | frame | frame | frame |
| L14 | K.α's `E(a)₁ = s_C` precondition (per ASN-0093) ⟹ subspace_I(a)=s_C ≠ s_L; preserves disjointness | frame | precondition ℓ∉dom(C); subspace_I(ℓ)=s_L preserves disjointness | frame | frame | frame | frame | frame |
| L-fin | frame | frame | extends dom(L) by one (finite + 1 = finite) | frame | frame | frame | frame | frame |
| C-fin | extends dom(C) by one (finite + 1 = finite) | frame | frame | frame | frame | frame | frame | frame |
| CL-OWN | frame | frame | frame | frame (no link-subspace V-positions added) | precondition: origin(ℓ)=d | frame (survivors retain origin) | link-subspace fixity (pointwise pre-state values preserved) | frame |
| CL-UNIQ | frame | frame | frame | frame | precondition: ℓ∉ran(M(d)) ensures unique placement | restriction of an injection remains injective | functional identity on dom_L (Steps 1–3 of K.μ~ link-fixity proof) | frame |

The matrix is a navigational index; each cell summarises the load-bearing argument. The detailed per-invariant prose below substantiates each matrix entry, in particular for invariants whose discharge mechanism is non-trivial. The link-row "frame" cells under K.α, K.μ⁺, and K.μ⁻ are covered uniformly by the matrix note above; the prose below does not repeat that justification per row.

*S2 (ArrangementFunctionality).* K.μ⁺ adds at V-positions disjoint from dom(M(d)) (the K.μ⁺ definition's value-preservation clause forces new mappings to disjoint positions, so extending a partial function at disjoint elements preserves single-valuedness); K.μ⁺_L adds at `v_ℓ ∉ dom(M(d))` (verified in *Link-subspace extension*); K.μ⁻ restricts M(d) (restriction of a function is a function); K.μ~ inherits via the K.μ⁻ + K.μ⁺ decomposition; all others hold M in frame.

*S3★ (GeneralizedReferentialIntegrity)* and *S3★-aux (SubspaceExhaustiveness).* Established and preserved as per the dedicated paragraphs in the *Generalized referential integrity* section above: K.α, K.δ, K.ρ hold M in frame; K.μ⁺ (amended) creates only content-subspace positions targeting dom(C); K.μ⁺_L creates only link-subspace positions targeting dom(L); K.μ⁻ restricts dom(M(d)); K.μ~ inherits via decomposition with link-subspace fixity.

*S4 (Origin-based identity, content distinctness — per ASN-0036).* S4 (per ASN-0036) is stated strictly over `dom(C)`: `a₁, a₂ ∈ dom(C)` produced by distinct allocation events satisfy `a₁ ≠ a₂`. Under the elementary transitions of this ASN, only K.α touches `dom(C)`; every other transition holds C in frame and so preserves S4 trivially (`dom(C') = dom(C)` ⟹ no new allocation events on the content store). For K.α, freshness of `a` against `dom(C)` (same-document distinctness) is the same-subspace part of SubAllocFresh at `x = C`; cross-document distinctness for two K.α events under d₁ ≠ d₂ follows from the *Cross-document disjointness chain* lemma (T10a.{2,5} → T10) applied at `b_C(d₁)` and `b_C(d₂)`. The related allocator-discipline distinctness obligations for entities (K.δ) and link addresses (K.λ) are *not* S4 obligations — S4 is content-only — and are discharged separately under "Entity distinctness" and "Link distinctness" below.

*Entity distinctness (derived; distinct K.δ events produce distinct entity addresses).* Only K.δ touches `E`; every other transition holds E in frame and preserves entity-distinctness trivially. For K.δ on non-node entities, T10a GlobalUniqueness on the parent allocator's tracked domain discharges `e ∉ E`; for K.δ on nodes, NodeUniqueAllocation supplies `e ∉ E` directly. *Cross-document distinctness for K.δ documents* (parent(d₁) ≠ parent(d₂)): we apply T10 (PartitionIndependence, ASN-0034) directly at the account level with `p₁ = A₁, p₂ = A₂`. The non-nesting precondition `A₁ ⋠ A₂ ∧ A₂ ⋠ A₁` follows from T10a's discipline on accounts as a binary case-split: two distinct accounts emitted by the same account sub-allocator (siblings under a common parent node) are prefix-incomparable by T10a.2 (NonNestingSiblingPrefixes); two distinct accounts emitted by different account sub-allocators (under distinct parent nodes) are prefix-incomparable by T10a.5 (CrossAllocatorIncomparability), the two account sub-allocators being non-lineage as both are direct children of the node-allocation registry rather than ancestor-descendant of one another. With `A₁ ⋠ A₂ ∧ A₂ ⋠ A₁` established, T10 yields every address extending `A₁` differs from every address extending `A₂`. Every document `[A₁.0.k]` minted under `A₁` by its document sub-allocator `A_doc(A₁)` extends `A₁` (since `A₁ ≼ [A₁.0.k]` for every `k ≥ 1` by the emission rule `inc(A, 2)` for the first emission and `inc(·, 0)` for subsequent siblings, both of which preserve the parent's prefix per TA5(b)/(c)); symmetrically for `A₂`. T10 therefore yields `d₁ ≠ d₂` for documents minted under each account, across all sibling positions `k, k' ≥ 1` — not only the first emissions. Applying the Cross-document disjointness chain lemma at `e₁ = A₁, e₂ = A₂, s = 1` would deliver distinctness only for addresses extending `[A₁.0.1]` and `[A₂.0.1]`, excluding sibling documents `[Aᵢ.0.k]` for `k ≥ 2` (same length, prefix-incomparable to `[Aᵢ.0.1]`); direct application of T10 at the account level covers every sibling. Within a single parent account, two distinct documents need not inhabit the same sub-allocator chain: a direct document `[A.0.1]` lies on `A_doc(A)`, whereas a version `[A.0.1.1]` lies on `A_v([A.0.1])`, yet both have parent account `A` (a version preserves `parent(d_new) = parent(d_src)` by K.δ-ID.parent-0/1). Distinctness across such cross-chain same-parent pairs is discharged by plain GlobalUniqueness (ASN-0034) across distinct K.δ allocation events — which covers cross-chain pairs without requiring co-residence on one chain — or, equivalently for the document/version pair, by T10a.6 (DomainDisjointness) between `A_doc(A)` and the relevant `A_v(·)`. The single-chain sub-case (two siblings on the same `A_doc(A)`) is the special case where GlobalUniqueness reduces to within-chain enumeration injectivity.

*Link distinctness (derived; distinct K.λ events produce distinct link addresses — the L11a obligation in the extended state).* Only K.λ touches `dom(L)`; every other transition holds L in frame and preserves link-distinctness trivially. For K.λ, freshness `ℓ ∉ dom(L) ∪ dom(C)` — same-document distinctness and cross-store distinctness alike — is SubAllocFresh at `x = L`. *Cross-document distinctness for K.λ*: for two K.λ events under d₁ ≠ d₂ producing ℓ₁, ℓ₂, the Cross-document disjointness chain lemma applied at `b_L(d₁), b_L(d₂)` gives `ℓ₁ ≠ ℓ₂` because the link-allocator prefixes differ at depth ≤ 4 (d₁ ≠ d₂ at depth ≤ 4 by S7d), and every inc-chain emission preserves the prefix.

*S7a (Document-scoped allocation).* Established by K.α's precondition (allocation uses origin(a)'s content sub-allocator prefix); preserved by P0 thereafter.

*S7b (Element-level I-addresses).* `zeros(a) = 3`: K.α's `zeros(a) = 3` precondition (per ASN-0093) supplies the property directly at allocation; preserved by P0.

*C1b (ASN-0093) (ContentElementFieldDepth, Element-field depth).* `#E(a) ≥ 2`: K.α's allocator chain produces `E(a) = [s_C, k]` with `k ≥ 1`, so `#E(a) ≥ 2`; preserved by P0.

*S7d (Document allocation discipline).* Every `d ∈ E_doc` is T4-valid with `zeros(d) = 2`, placed in E_doc by a K.δ case (ii) k = 2 event satisfying T10a's per-`(t, k')` discipline (e ∉ E discharged by T10a GlobalUniqueness on the parent account's document sub-allocator); preserved by P1.

*S8a, S8-depth, S8-fin.* Established at arrangement-extending transitions: K.μ⁺ amendment's preconditions on new V-positions (positivity, depth, finiteness preserved by finite extension); K.μ⁺_L preconditions (positivity, fixed per-document depth `m_L(d)`, finite extension); K.μ⁻ restriction preserves all three; K.μ~ inherits via decomposition; all others hold M in frame.

*S8★ (Per-subspace span decomposition).* Established per-subspace by the two routes specified at S8★'s definition. *Content subspace:* S8★(s_C) follows from ASN-0036's S8 applied to the projection `M(d')|_{V_{s_C}(d')} : V_{s_C}(d') → dom(C')` (S3★'s content clause is exactly S3 restricted to V_{s_C}(d'); S2/S7b/C1b/S8a/S8-depth/S8-fin are elementary-preserved as above). *Link subspace:* S8★(s_L) is discharged by the *trivial length-1 decomposition* `{(v, M(d')(v), 1) : v ∈ V_{s_L}(d')}` directly, not by ASN-0036's S8 — its S3 precondition (and S7b/C1b) does not hold on the link-subspace projection because the target is `dom(L)` not `dom(C)`. Every link-subspace V-position constitutes its own singleton correspondence run, satisfying S8's conditions (a) and (b) on singletons by construction; finiteness of the decomposition follows from S8-fin. Depth-2-specific (`m_L = 2`) shift-aligned decompositions are admissible — for any `v ∈ V_{s_L}(d')` of form `[s_L, k]`, a sequence `{[s_L, k], [s_L, k+1], …, [s_L, k+n-1]}` mapping shift-aligned to `{M(d')([s_L, k+i]) : 0 ≤ i < n}` constitutes an n-element correspondence run — but they are not required: the trivial form suffices for the existence postcondition under K.μ⁺_L and every other transition. Each arrangement-extending or contracting transition discharges S8★ at its post-state by these per-subspace projections; others hold M in frame.

*D-CTG★ / D-MIN★.* K.μ⁺'s original precondition list (stated at the K.μ⁺ definition in *Elementary transitions*) requires the resulting `M'(d)` to satisfy D-CTG and D-MIN, strengthened to D-CTG★ / D-MIN★ in the extended state — contiguity and minimum-position preservation on the extended content subspace is therefore discharged by precondition, not by the K.μ⁺ amendment (which adds only the `subspace(v) = s_C` restriction). K.μ⁺_L preconditions cover the D-CTG case (non-empty link subspace) and the D-MIN case (empty); K.μ⁻'s constructive precondition specifies the per-subspace retention count `n'_S` and produces the canonical suffix-prefix shape `V_S(d') = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}` directly, satisfying D-CTG★ and D-MIN★ at Σ' by construction; K.μ~ inherits via decomposition; all others hold M in frame.

*D-SEQ★.* Derived at each reachable state from D-CTG★ + D-MIN★ + S8-depth + S8-fin + S8a per the D-SEQ★ definition paragraph in the *Amendments to existing transitions* section above. D-SEQ★ at each reachable state follows by the same derivation applied at that state.

*P6 (Existential coherence), P7 (Provenance grounding).* Derivations in the *Cross-layer invariants* section above. P6: K.α precondition `origin(a) ∈ E_doc`; preserved by P0/P1. P7: K.ρ precondition `a ∈ dom(C)`; preserved by P0; all other transitions hold R in frame.

*P8 (Entity hierarchy).* K.δ adds one entity `e` to E. (i) `IsNode(e)`: the universal quantifies over non-node entities, so `e` is outside its scope; existing non-nodes retain `parent(e') ∈ E ⊆ E'` by inductive hypothesis. (ii) `¬IsNode(e)`: K.δ's case-(ii) precondition requires `parent(e) ∈ E ⊆ E'`; existing non-nodes carry forward by inductive hypothesis. All other transitions hold E in frame.

*NodeLineage* `(A e ∈ E : IsNode(e) : n₀ ≼ e)`. Base: `E₀ = {n₀}` with `n₀ ≼ n₀` by reflexivity of the tumbler-prefix order. K.δ case (i) — `IsNode(e)` — has `n₀ ≼ e` as an explicit precondition, discharged by NodeUniqueAllocation clause (b) (the registry's bootstrap-lineage condition supplies `n₀ ≼ e` directly at every node-allocation event); the inductive hypothesis carries `n₀ ≼ e'` for every prior node. K.δ case (ii) — `¬IsNode(e)` — adds a non-node, outside the IsNode quantifier; existing nodes unchanged. All other transitions hold E in frame.

*L0 (SubspacePartition).* L-clause from K.λ's precondition `subspace_I(ℓ) = s_L`; preserved by L12. C-clause from K.α's `E(a)₁ = s_C` precondition (per ASN-0093) — equivalently `subspace_I(a) = s_C`; preserved by P0.

*L1 (LinkElementLevel).* K.λ precondition `zeros(ℓ) = 3`; preserved by L12.

*L1a (LinkScopedAllocation).* K.λ precondition `origin(ℓ) = d ∈ E_doc`; preserved by L12 + P1.

*L1b (Link element-field depth).* `#E(ℓ) ≥ 2`. *First-link case:* SubAllocatorAxiom emits `ℓ = [d.0.s_L.1]`. The address `d` is a document tumbler with `zeros(d) = 2`; the emission appends one zero separator and the two-component suffix `[s_L, 1]`, giving `zeros(ℓ) = 3` and T4-validity by SubAllocatorAxiom.Namespace's structural commitment. Applying T4b (UniqueParse, ASN-0034) to `ℓ` at `zeros = 3` makes all four projections N, U, D, E well-defined, with `E(ℓ) = [s_L, 1]` (the suffix following the third zero separator), so `#E(ℓ) = 2` directly. *Subsequent-link case:* K.λ emits `ℓ = inc(prev, 0)` (TA5(c)), a sibling extension preserving tumbler length and zero count: TA5(c) gives `#ℓ = #prev` (inc(·, 0) modifies only position sig(prev)), and TA5-SigValid gives `sig(prev) = #prev` — the modified position is the last component, which is nonzero and stays nonzero — so the zero count is unchanged: `zeros(ℓ) = zeros(prev) = 3` (`prev` is T4-valid by T10a.4). Same length and zero count force same element-field length: `#E(ℓ) = #ℓ − zeros(ℓ) − 1 = #E(prev) ≥ 2` inductively. Preserved by L12 thereafter.

*L1c (Link allocator conformance).* Every `ℓ ∈ dom(L)` must be reachable from a T4-valid document-level seed `s` (`zeros(s) = 2`) by a *structural inc-chain* with `k₁ = 2`. The chain property captured is per-step inc-rule conformance — each step `tᵢ = inc(tᵢ₋₁, kᵢ)` with `kᵢ ∈ {0, 1, 2}` satisfying TA5's structural preconditions (operand T4-validity, zeros bound at k = 2), plus length monotonicity `#tᵢ > #s` — *not* T10a's full discipline including allocator-frontier domain tracking. The distinction matters at the anchors `b_C(d), b_L(d)` and at the first emission `[d.0.s_L.1]`: these inhabit no T10a-tracked allocator domain (the anchors are virtual, outside dom(C) ∪ dom(L); the first emission is committed outside both stores by SubAllocatorAxiom.FirstEmission). Allocator-activation discharge for the anchor traversal and first emission goes through SubAllocatorAxiom; T10a's full discipline applies only to subsequent emissions on the activated A_L(d) frontier. Base: `dom(L₀) = ∅`, vacuous. K.λ *first-link case*: emits `ℓ = [d.0.s_L.1]` (SubAllocatorAxiom) under `d ∈ E_doc`. Under SubspaceConventionAxiom (`s_C = 1`, `s_L = 2`), the structural inc-chain `t₀ = d, t₁ = inc(d, 2) = b_C(d) = [d.0.1], t₂ = inc(t₁, 0) = b_L(d) = [d.0.2], t₃ = inc(t₂, 1) = ℓ = [d.0.2.1]` satisfies per-step inc-rule conformance: `s = d` is T4-valid with `zeros(s) = 2`; `k₁ = 2, k₂ = 0, k₃ = 1`, each in `{0, 1, 2}`; the only `k = 2` step is `k₁` whose operand `t₀ = d` has `zeros(d) = 2 ≤ 2`; and `#tᵢ > #d` at every step by TA5(d)'s length-extension and TA5(c)'s length-preservation. The step `t₂ = inc(t₁, 0) = b_L(d)` rests on SubspaceConventionAxiom's `s_L = s_C + 1 = 2`. K.λ *subsequent-link case*: emits `ℓ = inc(prev, 0)` (TA5(c)) under the same `d`, extending prev's chain by one additional step `kₙ₊₁ = 0`. All other transitions hold L in frame.

*L3 (NEndsetStructure).* K.λ precondition `N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅` establishes L3 at the new entry; L12 preserves it pointwise for existing entries; Σ₀ has `dom(L₀) = ∅` so L3 holds vacuously at the base. All other transitions hold L in frame.

*L14 (StoreDisjointness).* ASN-0093's SD restated; cited from ASN-0093 (see L14 at *Link store and extended system state*).

*L-fin (Link store finiteness).* `|dom(L)| < ∞`: base `|dom(L₀)| = 0`; K.λ extends dom(L) by exactly one address (finite extension preserves finiteness); all other transitions hold L in frame.

*C-fin (Content store finiteness).* `|dom(C)| < ∞`: base `|dom(C₀)| = 0`; K.α extends dom(C) by exactly one address (finite extension preserves finiteness); all other transitions hold C in frame. C-fin is load-bearing for K.α's subsequent-emission case formula `a = inc(max{a' ∈ dom(C) : origin(a') = d}, 0)` — the indexed set `{a' ∈ dom(C) : origin(a') = d}` is a subset of the finite `dom(C)`, so `max` is well-defined whenever the set is non-empty (which is exactly the subsequent-emission predicate).

*CL-OWN (LinkSubspaceOwnership).* K.μ⁺_L precondition `origin(ℓ) = d` at every new link-subspace mapping; K.μ⁻ frame on surviving mappings; K.μ~ via link-subspace fixity (`M'(d)|_{dom_L} = M(d)|_{dom_L}` as functions); all others hold M in frame.

*CL-UNIQ (LinkSubspacePositionUniqueness).* K.μ⁺_L's first-arrangement precondition `ℓ ∉ ran(M(d))` ensures each newly arranged link occupies a unique V-position. K.μ⁻ restriction of an injective function remains injective. K.μ~ preservation: Steps (1)–(4) of the link-subspace fixity proof (in the *Decomposition of K.μ~* section above), where the functional identity `M'(d)|_{dom_L} = M(d)|_{dom_L}` carries CL-UNIQ from Σ to Σ'. All other transitions hold M in frame.

**Class (b): Composite-boundary properties** — discharged at composite boundaries by the J0/J1★/J1'★ couplings of ValidComposite★, not preserved by each elementary transition. These are: P4★, P4a, and P7a.

*Composite-boundary verification matrix.* For each Class (b) property, the matrix records the discharge mechanism at composite boundaries. Cells flagged "may transiently fail" identify the elementary steps that violate the property in isolation; restoration is supplied by the named coupling at the composite boundary.

| Property | Discharge at composite boundary | Transient failure within composite |
|----------|--------------------------------|------------------------------------|
| P4★ (`Contains_C(Σ) ⊆ R`) | J1★ at boundary supplies `(a, d) ∈ R'` for each new content-subspace containment | After K.μ⁺ before K.ρ: `(a, d) ∈ Contains_C(M_post)` but not yet in R |
| P4a (every R-entry witnessed by past content-subspace containment) | J1'★ at boundary supplies content-subspace witness `v` with `M'(d)(v) = a` at the post-state Σ' itself | Transiently fails if K.ρ precedes the matching K.μ⁺ within the composite; restored at Σ', which carries the witness. |
| P7a (every `a ∈ dom(C)` has a provenance entry) | J0 supplies `v ∈ dom(M'(d))` with `M'(d)(v) = a`; S3★ + L14 + S3★-aux force `subspace(v) = s_C`; J1★ then supplies `(a, d) ∈ R'` | After K.α before K.μ⁺/K.ρ: `a ∈ dom(C')` but no `(·, d)` entry in R' |

The matrix corresponds to the per-property arguments below.

P4★ (`Contains_C(Σ) ⊆ R`): For each `(a, d) ∈ Contains_C(Σ') \ Contains_C(Σ)`, J1★ at the composite boundary requires `(a, d) ∈ R'`. K.μ⁺_L adds only link-subspace V-positions (excluded from Contains_C); K.μ⁻ can only shrink Contains_C; K.μ~ preserves Contains_C exactly; all other transitions hold M in frame.

P4a (`(A (a, d) ∈ R :: (E Σ_k in the transition history : (E v ∈ dom(M_k(d)) : subspace(v) = s_C ∧ M_k(d)(v) = a)))`): For `(a, d) ∈ R' \ R`, J1'★ supplies `v ∈ dom(M'(d))` with `subspace(v) = s_C ∧ M'(d)(v) = a`, so Σ' itself witnesses; for `(a, d) ∈ R`, the inductive hypothesis supplies a prior witnessing state Σ_k and P2 carries the entry into R'. All other transitions hold R in frame. ValidComposite★ does *not* enforce an ordering K.μ⁺ ⤳ K.ρ — orderings such as K.α → K.ρ → K.μ⁺ satisfy every elementary precondition (K.ρ requires only `a ∈ dom(C) ∧ d ∈ E_doc`, both established by the preceding K.α), and produce an intermediate state at which the fresh `(a, d) ∈ R` has no witnessing content-subspace V-position in any current arrangement. Restoration at the composite boundary is *not* by re-deriving from history but by the post-state itself: at Σ', J1'★ requires `(E v ∈ dom(M'(d)) : subspace(v) = s_C ∧ M'(d)(v) = a)`, so Σ' itself is the witnessing state for the P4a quantifier — the K.μ⁺ that ultimately fires in the composite supplies the witness in `M'(d)` directly. The "transient failure" thus describes a real observable mid-composite state; restoration is structural (Σ' carries the witness), not temporal (no earlier state need carry it).

P7a (`(A a ∈ dom(C) :: (E d :: (a, d) ∈ R))`): For `a ∈ dom(C') \ dom(C)`, J0 supplies `d ∈ E'_doc` and `v ∈ dom(M'(d))` with `M'(d)(v) = a`. *Temporal positioning of `v`.* The V-position `v` carrying the new I-address `a` is created by K.μ⁺ at the composite endpoint Σ', not at the post-K.α intermediate state — at the intermediate state immediately after K.α and before K.μ⁺, `v` does not yet inhabit `dom(M(d))` (K.α holds M in frame, so no V-position carries `a` at that point); J0's existential is realised only after K.μ⁺ has fired and placed `v ↦ a` into M'(d), which is the composite endpoint by ValidComposite★'s structure. The K.μ⁺ amendment forces `subspace(v) = s_C` directly at the moment the position is created (K.μ⁺ adds only content-subspace V-positions). We show the V-position `v` must be content-subspace by an independent chained derivation from J0 + S3★ + L14 — independent verification that no link-subspace V-position can carry a dom(C) target, evaluated at the composite endpoint Σ' where both `v` and `a` co-exist (not at the post-K.α intermediate, where `v` is absent from M(d)). The derivation does not rely on the K.μ⁺ amendment: J0's statement quantifies over `v ∈ dom(M'(d))` without subspace restriction, and the contradiction below proceeds without invoking K.μ⁺'s subspace-restriction clause. Suppose for contradiction `subspace(v) = s_L`. Then by S3★ at Σ' (link clause), `M'(d)(v) ∈ dom(L')`, i.e., `a ∈ dom(L')`. But `a ∈ dom(C')` (J0's defining membership) and L14 at Σ' gives `dom(C') ∩ dom(L') = ∅`, contradiction. By S3★-aux, `subspace(v) ∈ {s_C, s_L}`, so `subspace(v) = s_C`. *Range-new discharge for J1★.* J1★'s trigger predicate has two conjuncts — `a ∈ ran(M'(d)|_{s_C})` (the post-state range contains `a`) and `a ∉ ran(M(d)|_{s_C})` (the pre-state range did not contain `a`). The first conjunct follows directly: `subspace(v) = s_C` and `M'(d)(v) = a` place `v ∈ V_{s_C}(d')` with `M'(d)(v) = a`, hence `a ∈ ran(M'(d)|_{s_C})`. The second conjunct chains in one inference step: `a ∈ dom(C') \ dom(C)` forces `a ∉ dom(C)`; by S3★'s content clause at the pre-state Σ — `(A u : u ∈ dom(M(d)) ∧ subspace(u) = s_C : M(d)(u) ∈ dom(C))` — we have `ran(M(d)|_{s_C}) ⊆ dom(C)`; combining, `a ∉ ran(M(d)|_{s_C})`. With both J1★ trigger conjuncts discharged, J1★ supplies `(a, d) ∈ R'`. No transition removes from dom(C) (P0) or from R (P2), so P7a, once established, persists.

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
| Valid composite | Σ →* Σ' valid iff: (1) elementary preconditions at each intermediate state, (2) J0/J1/J1' for the composite; P0/P1/P2 derived as lemma |
| K.α | Content allocation — extend dom(C) with fresh address a at value v; precondition: IsElement(a), origin(a) ∈ E_doc, a ∉ dom(C), a ∉ dom(L), a produced by origin(a)'s content sub-allocator; effect C' = C ∪ {a ↦ v}; frame holds L, E, M, R |
| K.δ | Entity creation — extend E with fresh entity; precondition: parent(e) ∈ E when ¬IsNode(e); empty arrangement if IsDocument; frame holds C, L, R, other documents in M (new entity gets M'(e) = ∅ by totality convention) |
| K.μ⁺ | Arrangement extension — extend dom(M(d)) for d ∈ E_doc with new V→I mappings, preserving existing values; co-amended with content-subspace partitioning at the extended-state introduction (see Local extensions block); frame holds C, L, E, R, other documents |
| K.μ⁻ | Arrangement contraction — remove existing V→I mappings from some d ∈ E_doc, with surviving mappings unchanged: dom(M'(d)) ⊂ dom(M(d)) ∧ (A v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v)); per-subspace admissible removal pattern is suffix truncation (empty, proper, or full), with at least one subspace contracting strictly; frame holds C, L, E, R, other documents |
| K.μ~ | Arrangement reordering — named composite K.μ⁻ + K.μ⁺ (not a primitive transition) realising a bijection π : dom(M(d)) → dom(M'(d)) with M'(d)(π(v)) = M(d)(v); subspace-preserving with link-subspace fixity (π(v) = v for v ∈ dom_L); derived frame holds C, L, E, R, other documents |
| K.λ | Link allocation — extend dom(L) with fresh address ℓ at value (e₁, …, eₙ); precondition: d ∈ E_doc, ℓ ∉ dom(L) ∪ dom(C), zeros(ℓ) = 3, subspace_I(ℓ) = s_L, #E(ℓ) ≥ 2, origin(ℓ) = d, ℓ is produced by d's link sub-allocator (first emission [d.0.s_L.1] via SubAllocatorAxiom; subsequent inc(·, 0) on the frontier via TA5(c)), N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅; effect L' = L ∪ {ℓ ↦ (e₁, …, eₙ)}; frame holds C, E, M, R |
| K.ρ | Provenance recording — extend R with (a, d) pair where IsElement(a) ∧ a ∈ dom(C); frame holds C, L, E, M |
| K.μ⁺_L | Elementary transition: link-subspace arrangement extension, M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}, origin(ℓ) = d, ℓ ∉ ran(M(d)) (first-arrangement); frame holds C, L, E, R, other documents |
| K.μ~-FIX | Domain fixity under K.μ~: dom(M'(d)) = dom(M(d)), making π a permutation of a fixed domain — from D-SEQ + bijection cardinality + subspace preservation |
| J0 | Content allocation (K.α) always co-occurs with arrangement extension (K.μ⁺). **Axiomatic** — not derived from foundation |
| J1 | Arrangement extension (K.μ⁺) must co-occur with provenance recording (K.ρ), derived by wp; *superseded by J1★ in the extended state* (range-based content-subspace scoping) |
| J1' | (a, d) ∈ R' \ R only when a ∈ ran(M'(d)) \ ran(M(d)) — new provenance requires new containment; *superseded by J1'★ in the extended state* (range-based content-subspace scoping) |
| J2 | K.μ⁻ as elementary transition requires no coupling: C' = C ∧ L' = L ∧ E' = E ∧ R' = R |
| J3 | K.μ~ as named composite requires no coupling: C' = C ∧ L' = L ∧ E' = E ∧ R' = R |
| J4 | Fork composite: K.δ + K.μ⁺ + K.ρ (no other steps); precondition V_{s_C}(d_src) ≠ ∅; dom(C') = dom(C) follows from frames; provenance from J1★/J1'★ (extended-state couplings); content-subspace-empty source is ex nihilo (K.δ), not fork |
| P1 | Entity set is monotonically growing: E ⊆ E' for every transition, uniformly across levels |
| P2 | Provenance relation is monotonically growing: R ⊆ R' for every transition |
| P4 | Provenance bounds: Contains(Σ) ⊆ R, with stale entries possible from prior states |
| P4a | Historical fidelity: every (a, d) ∈ R has a witnessing state where a ∈ ran(M(d)) |
| P6 | Existential coherence: origin(a) ∈ E_doc for all a ∈ dom(C) |
| P7 | Provenance grounding: a ∈ dom(C) for all (a, d) ∈ R |
| P7a | Provenance coverage: (E d :: (a, d) ∈ R) for all a ∈ dom(C) — every I-address has provenance |
| P8 | Entity hierarchy: (A e ∈ E : ¬IsNode(e) : parent(e) ∈ E) — no orphan accounts or documents |
| m_L(d) | Per-document link-subspace V-position depth — pinned operationally at first link-subspace insertion (K.μ⁺_L precondition), bounded below by S8a (`≥ 2`) and held constant by S8-depth; not a separate axiom |
| NodeUniqueAllocation | Axiom: every K.δ node-allocation event produces (a) e ∉ E (freshness); (b) n₀ ≼ e (bootstrap lineage); and (c) registry tracking — every `t ∈ Σ.E_node` inhabits the external registry's tracked domain at every reachable state |
| NodeRegistryBootstrap | Axiom (BootstrapRegistrySeeding): at Σ₀, n₀ is committed to the *external* node-allocation registry's tracked domain. The registry is not a component of Σ; n₀ enters at Σ₀ rather than via a prior K.δ event |
| FrontierEquivalence | Derived lemma: `inc(t, 0) ∉ Σ.E ⟺ t is the frontier of its sub-allocator's (t, 0)-branch`, for every reachable Σ and every `t ∈ Σ.E` with `¬IsNode(t)`. Proved from TA5(c) functional determinism and P1 E-monotonicity (forward direction) and T10a GlobalUniqueness via T10a.6 (reverse direction), each cited at the consuming step; "frontier" is well-defined by T10a.7. Counterexample to T4b-based identification: T4b's `parent`/`zeros`/length stratification does not in general identify t as the frontier of its own sub-allocator |
| NodeLineage | Derived per-state invariant: `(A e ∈ E : IsNode(e) : n₀ ≼ e)` — every node in E descends structurally from the bootstrap node n₀ by tumbler-prefix relation. Discharged inductively from the base case `E₀ = {n₀}` (reflexivity) and the K.δ case (i) precondition `n₀ ≼ e` |
| GlobalLineage | Derived corollary: `(A x ∈ E ∪ dom(C) ∪ dom(L) :: n₀ ≼ x)` — every entity, content address, and link address descends from n₀ under tumbler-prefix order. Promotes NodeLineage to the full docuverse via P8 + P6 + L1a + L1c + transitivity of ≼ |
| b_C(d), b_L(d) | Virtual sub-allocator anchors under d: `b_C(d) = [d.0.s_C]`, `b_L(d) = [d.0.s_L]` — single-component element-field bases, not in dom(C) ∪ dom(L), serving as formal starting points for the content and link allocator chains under d |
| Allocator hierarchy | Content and link sub-allocators are sibling element-field allocators under d, sharing prefix `[d.0]`; T10a-conformance applies to each frontier separately; cross-document collisions prevented by T10, cross-subspace by L14 (= L0 + SC-NEQ) |
| S3★-aux | Subspace exhaustiveness: `(A d, v : v ∈ dom(M(d)) : subspace(v) = s_C ∨ subspace(v) = s_L)` in every reachable state |
| CL-OWN | LinkSubspaceOwnership: `(A d, v : v ∈ dom(M(d)) ∧ subspace(v) = s_L : origin(M(d)(v)) = d)` — every document's link subspace contains only its own links |
| CL-UNIQ | LinkSubspacePositionUniqueness: `(A d, v₁, v₂ ∈ dom(M(d)) : subspace(v₁) = subspace(v₂) = s_L ∧ M(d)(v₁) = M(d)(v₂) : v₁ = v₂)` — each link occupies exactly one V-position in its home document's link subspace; injectivity of M(d)\|_{dom_L}. Closes the K.μ~ link-subspace identity precondition derivation |

### Derived structural identities

The K.δ-ID identities below are *derived consequences* of TA5 (HierarchicalIncrement, ASN-0034) and T4b (UniqueParse, ASN-0034) applied to `e = inc(t, k)`, *not* primitive specifications introduced by this ASN. They are listed under separate naming so they can be cited by name (K.δ-ID.zeros-0/1, K.δ-ID.zeros-2, K.δ-ID.parent-0/1, K.δ-ID.parent-2) without unpacking the TA5 / T4b derivation chain at each invocation. The derivations live at the inline K.δ catalogue (*Elementary transitions*, K.δ case (ii)); this table records label and statement only, with a pointer to that site.

| Label | Statement | Derivation |
|-------|-----------|------------|
| K.δ-ID.zeros-0/1 | `zeros(e) = zeros(t)` for k ∈ {0, 1} on `e = inc(t, k)` | See K.δ case (ii) catalogue |
| K.δ-ID.zeros-2 | `zeros(e) = zeros(t) + 1` for k = 2 on `e = inc(t, 2)` | See K.δ case (ii) catalogue |
| K.δ-ID.parent-0/1 | `parent(e) = parent(t)` for k ∈ {0, 1} on `e = inc(t, k)` | See K.δ case (ii) catalogue |
| K.δ-ID.parent-2 | `parent(e) = t` for k = 2 on `e = inc(t, 2)` | See K.δ case (ii) catalogue |

### Inherited from foundation (restated for narrative continuity)

These properties are foundation invariants of ASN-0093 (or earlier foundation ASNs). They are restated in the body of this ASN purely for narrative continuity — every statement and every preservation argument is supplied by the cited foundation, not by local derivation.

| Label | Statement | Foundation source |
|-------|-----------|--------------------|
| SequentialTransitionAxiom | Axiom (SequentialAtomicTransitions): the transition relation `Σ → Σ'` is single-event sequential — each transition is an atomic, uninterruptible event in which the elementary precondition is evaluated against `Σ` and the elementary effect is committed to `Σ'` in one indivisible step, and transitions are totally ordered. Equivalently, the system admits no intermediate state in which a transition has begun but not yet committed | ASN-0093 (SequentialAtomicTransitions) |
| SubspaceConventionAxiom | Axiom (FixedSubspaceIdentifiers): `s_C = 1 ∧ s_L = 2`, with consequence `SC-NEQ ≡ s_C ≠ s_L` | ASN-0093 (FixedSubspaceIdentifiers) |
| SubAllocatorAxiom | Axiom (ContentLinkSubAllocatorExistence): for each d ∈ E_doc, the entity-allocation event placing d into E_doc simultaneously establishes two disjoint sub-allocators under d — a content sub-allocator with anchor `b_C(d) = [d.0.s_C]` and a link sub-allocator with anchor `b_L(d) = [d.0.s_L]` — each providing a forward-allocation frontier whose namespace property closes the uniqueness chain for K.α (content first-emit) and K.λ (link first-emit) | ASN-0093 (ContentLinkSubAllocatorExistence) |
| L0 | SubspacePartition: `(A a ∈ dom(Σ.L) :: subspace_I(a) = s_L)` and `(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)` — both clauses are foundation invariants of ASN-0093. (The L-clause appears in ASN-0043's original L0; the C-clause was added in ASN-0093's foundation L0 and is supplied at allocation time by ASN-0093's K.α precondition `E(a)₁ = s_C`.) | ASN-0093 (SubspacePartition) |
| L3 | NEndsetStructure: `(A a ∈ dom(Σ.L) :: |Σ.L(a)| ≥ 3 ∧ (A i : 1 ≤ i ≤ |Σ.L(a)| : Σ.L(a).eᵢ ∈ Endset) ∧ Σ.L(a).e₃ ≠ ∅)` — every link is a sequence of at least three endsets with the type endset (slot 3) non-empty. Inherited verbatim from ASN-0093's L3 (which itself inherits from ASN-0043's `Link` definition admitting arity `N ≥ 3`). | ASN-0093 (NEndsetStructure) |
| C-fin | ContentStoreFiniteness: `|dom(Σ.C)| < ∞`. Load-bearing for K.α's subsequent-emission case formula `a = inc(max{a' ∈ dom(C) : origin(a') = d}, 0)` — the indexed set is a subset of the finite `dom(C)`, so `max` is well-defined whenever non-empty. Inherited as a per-state invariant of the extended state; established at Σ₀ (`|dom(C₀)| = 0`) and preserved by K.α (extends by one) with frame on all other transitions. | ASN-0093 (ContentStoreFiniteness) |
| L1c | LinkAllocatorConformance: every `ℓ ∈ dom(L)` has a structural inc-chain from its home document to `ℓ` — a finite sequence `(t₀, …, tₙ)` with `t₀ = origin(ℓ)`, `tₙ = ℓ`, each step `tᵢ = inc(tᵢ₋₁, kᵢ)` with `kᵢ ∈ {0, 1, 2}` satisfying T10a's per-step admissibility (T4-validity preservation, zero-count side condition at `kᵢ = 2`), `k₁ = 2`, and `#tᵢ > #origin(ℓ)` at every step. Originated in ASN-0093 as the structural-inc-chain form (weakened from ASN-0043's "operates within a system conforming to T10a"); ASN-0047 inherits this form unchanged. The anchor traversal `d → b_C(d) → b_L(d) → [d.0.s_L.1]` and the first link emission inhabit no T10a-tracked allocator domain — their activation discharge goes through SubAllocatorAxiom rather than T10a's T2 spawning rule, as already captured by ASN-0093's L1c. | ASN-0093 (LinkAllocatorConformance) — itself weakened from ASN-0043's L1c |
| L14 | StoreDisjointness: `dom(C) ∩ dom(L) = ∅` — unscoped store disjointness. ASN-0093's SD restated under the local name L14, cited from ASN-0093. SD's unscoped form already supersedes ASN-0043's scoped L14 (DualPrimitive, `dom(L) ∩ dom(C)\|_{s_C} = ∅`), the unscoping being available because ASN-0093's K.α `E(a)₁ = s_C` precondition forces every `a ∈ dom(C)` to be `s_C`-resident. | ASN-0093 (SD, StoreDisjointness) |

### Local extensions and strengthenings of foundation properties

| Label | Statement | Foundation source |
|-------|-----------|--------------------|
| P0 | Content store is append-only with immutable values: dom(C) ⊆ dom(C') ∧ C'(a) = C(a) for a ∈ dom(C) | Subsumes ASN-0036's S0 (ContentImmutability) and S1 (StoreMonotonicity) into a single unified statement |
| L14a | Superseded by S3★ + CL-OWN in the extended state: S3★ routes every link-subspace V→I mapping to dom(L), and CL-OWN forces home-document ownership at each such mapping | ASN-0043's L14a (NonTranscludability — `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∉ dom(Σ.L))`, forbidding any V-position from mapping to a link). In the extended state S3★ permits link-subspace V→I mappings by routing them into dom(L), and CL-OWN constrains such mappings to the home document; S3★ + CL-OWN ⟹ ¬L14a |
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
| ExtendedReachableStateInvariants | Every reachable state satisfies the *per-state invariants* S2 ∧ S3★ ∧ S3★-aux ∧ S4 ∧ S7a–S7d ∧ S8a ∧ S8-fin ∧ S8-depth ∧ S8★ ∧ C-fin ∧ D-CTG★ ∧ D-MIN★ ∧ D-SEQ★ ∧ P6–P8 ∧ L0 ∧ L1 ∧ L1a ∧ L1b ∧ L1c ∧ L3 ∧ L14 ∧ L-fin ∧ CL-OWN ∧ CL-UNIQ (preserved by each elementary transition); every state at a composite boundary additionally satisfies the *composite-boundary properties* P4★ ∧ P4a ∧ P7a (discharged at boundaries by J0/J1★/J1'★, may transiently fail at intermediate states). P3 (which packages P0, P1, P2, L12) and S9 are *per-transition*: see ExtendedTransitionInvariants. Together supersedes ReachableStateInvariants | This ASN's own Reachable-state invariants synthesis extended to the two-subspace state |
| ExtendedTransitionInvariants | Every valid composite transition Σ →* Σ' satisfies P3, the conjunction P0 ∧ P1 ∧ P2 ∧ L12 (which subsumes ASN-0036's S0 and S1 via P0 and extends ASN-0043's L12). S9 follows from P0 via the arrangement frames (`C' = C` on every M-mutating transition leaves the content store untouched) | This ASN's own per-transition synthesis |
| K.α's `E(a)₁ = s_C` precondition (inherited) | Pins `subspace_I(a) = s_C`, cited downstream to preserve L0's C-clause and L14 in the extended state; see the *K.α (no local amendment in extended state)* paragraph in *Amendments to existing transitions* | Inherited from ASN-0093's K.α (ContentAllocation) precondition |
| K.μ⁺ amendment | Content-subspace restriction (`subspace(v) = s_C`); existing D-CTG/D-MIN postconditions carry forward; partitions arrangement extension by subspace with K.μ⁺_L | Strengthening of this ASN's K.μ⁺ (defined in *Elementary transitions* above) at the extended-state introduction |
| K.μ⁻ (per-subspace scope) | The per-subspace D-CTG★/D-MIN★ postconditions stated at K.μ⁻'s definition apply to each subspace independently; valid contractions per-subspace are per-subspace suffix removals or full clearances (forced by D-CTG★ + D-MIN★ + D-SEQ★ at the post-state) | ASN-0036's K.μ⁻ stated D-CTG/D-MIN with a link-subspace exemption; the per-subspace amendments D-CTG★/D-MIN★ above carry through K.μ⁻'s postconditions to two subspaces |

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
- Should K.λ require `e₁ ∪ e₂ ≠ ∅` to exclude type-only links, or admit them as valid markers per Nelson's one-sided link case (LM 4/48)? If admitted, do one-sided links (exactly one of e₁, e₂ empty) and type-only markers (both empty) carry distinguishable semantics in endset-iterating consumers like L8's `same_type` and the discovery-set unions?
- Should the entity-allocation discipline admit account-level depth-1 tumbler extension (K.δ with `k = 1` and `IsAccount(t)`), producing an account-shaped sibling at the same hierarchy level as t? The present ASN excludes this at the precondition, citing the consultation evidence that versioning is reserved to documents (Nelson, LM 4/29; Gregory, `docreatenewversion` for DOCUMENT→DOCUMENT only). The structural form `[N, 0, U, 1]` is itself well-typed (still `IsAccount`) under T4b, and admitting it would not violate any per-state invariant of the present model (the k = 1 harmlessness verification for documents would carry across); but no role for such an entity is documented in the design or implementation. The question is whether a future extension (e.g., account renaming, multi-account user identity) would require admitting account-level depth-1 extension; if so, the precondition restriction here can be relaxed without further structural reorganisation.
