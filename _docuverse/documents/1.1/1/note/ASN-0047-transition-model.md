# ASN-0047: Transition Model

*2026-03-17, revised 2026-03-22*

ASN-0036 established two components of system state — a permanent content store C and mutable document arrangements M(d) — and proved their separation: content, once stored, is immutable (S0); arrangement mutations cannot alter the content store (S9). These are properties of the invariants. We have not yet classified the transitions. In what primitive ways can the state change, and what must each change preserve?

The consultation answers reveal a state model richer than the two-space analysis captured. Nelson enumerates the ways the docuverse changes — new documents created, new content inserted, new links established, views rearranged — and is equally precise about what cannot happen: content is never destroyed, addresses are never reassigned, history is never erased. Gregory reduces eight protocol commands to six kinds of persistent modification, distributed across three storage layers with distinct permanence contracts.

We seek the abstract taxonomy. Not the protocol commands, which are interface design, but the primitive modifications and their invariants. The central result is a *mutability hierarchy*: the state components arrange into three temporal layers, each with its own permanence contract. Destructive change — removal and reordering — is confined entirely to the most mutable layer.


## Notation

This ASN draws on projection functions and predicates established in the foundation ASNs (ASN-0034 Tumbler Algebra, ASN-0036 Strand Model, ASN-0043 Link Model, ASN-0045 Tumbler Fields). For reader convenience we list them here, fixing one notation per concept and pointing to the defining ASN. Notation introduced for the first time in this ASN is marked "introduced here."

*I-address (element-level) projections.* For each `a ∈ T_elem`:

- `E(a)` (ASN-0034, T4b): the element-field projection — the sequence of components after the last zero separator. `E(a)` is itself a positive-component tumbler with `#E(a) ≥ 1`. We define `fields(a) := E(a)` as a *local abbreviation* used throughout this ASN for readability when the I-address being projected is the natural subject of the sentence; `fields(a)` is *not* a foundation function and carries no semantics beyond `E(a)`. Both notations are used interchangeably in this ASN.
- `fields(a).E₁` (local notation; equals `E(a)₁` of ASN-0034, T4b): the first component of `E(a)` — the subspace identifier at the I-address level. This ASN uses `fields(a).E₁` as its primary notation for the I-address subspace identifier in original predicates and definitions. Where `fields(a).E₁` appears in a predicate, it should be read as "the subspace identifier of the I-address a" — i.e., `E(a)₁`.
- `subspace_I(a)` (bridge to foundation notation): defined by `subspace_I(a) := fields(a).E₁` for every `a ∈ T_elem`. ASN-0036's ShiftPreservation lemma (postcondition iv) is stated using `subspace_I`, preserving `subspace_I(shift(a, k)) = subspace_I(a)` for `a ∈ dom(Σ.C)` under T10a-conforming shift. The bridge admits citing ShiftPreservation verbatim in this ASN without restating its postcondition in `fields(a).E₁` form; conversely, every occurrence of `subspace_I(·)` in foundation-citation contexts is interchangeable with `fields(·).E₁`. The two notations co-exist by definition; new predicates of this ASN use `fields(a).E₁`, while foundation citations may use either form.
- `origin(a)` (ASN-0036, S7a): the document address `d ∈ E_doc` under whose allocator a was minted. For each `a ∈ dom(C)`, `origin(a) ∈ E_doc`; for each `ℓ ∈ dom(L)`, `origin(ℓ) ∈ E_doc` (L1a). origin is recovered by truncating a to the document prefix (zeros = 2).
- `home(a)` (ASN-0043 for links, ASN-0036 implicit for content): equivalent to `origin(a)` in the present ASN's vocabulary — Nelson's "home document." This ASN uses `origin(·)` uniformly and avoids `home(·)`.
- `IsElement(a)`, `IsNode(a)`, `IsAccount(a)`, `IsDocument(a)` (ASN-0045): level predicates parameterised by `zeros(a)` ∈ {0, 1, 2, 3}.
- `#E(a)` (ASN-0034): the depth (component count) of `fields(a)` — equivalently `#a − zeros(a) − 1` if a has zero separators, or `#a` if a has no zero separators.

*V-position (arrangement-domain) projections.* For each `v ∈ dom(M(d))`:

- `subspace(v)` (ASN-0036): the first component `v₁` of the V-position tumbler — the subspace identifier at the V-position level. By S8a, every `v ∈ dom(M(d))` satisfies `v₁ ≥ 1`, so `subspace(v) ∈ ℕ⁺`. In this ASN the two subspaces are `s_C` (content/text) and `s_L` (link), with `s_C ≠ s_L` (SC-NEQ axiom, introduced here).
- `#v` (ASN-0034): the depth of v. By S8-depth, V-positions within a fixed subspace under a fixed document share a common depth `m_S`.

*Entity-hierarchy projections.* For each non-node entity `e ∈ E`:

- `parent(e)` (introduced here, §The state model): the tumbler obtained by truncating e's last field together with its preceding zero separator. `parent(e)` is the entity-hierarchy spine — defined only for non-node entities (`¬IsNode(e)`), and producing a valid address at the next-higher level: `zeros(parent(e)) = zeros(e) − 1`.

*A note on the relationship between subspace(v) and fields(a).E₁.* For each `(v, a) ∈ M(d)` with `a ∈ dom(C)`, S3 (ASN-0036) gives `v₁ = fields(a).E₁` — the V-position's subspace identifier coincides with the I-address's element-field first component. The same correspondence extends to the link subspace under S3★ (introduced here) for `a ∈ dom(L)`. Hence `subspace(v) = fields(M(d)(v)).E₁` whenever `v ∈ dom(M(d))`. We retain both notations because they apply at different state-component levels: `subspace(v)` is a V-position projection (left domain of M), while `fields(a).E₁` is an I-address projection (right range of M). Predicates over V-positions use `subspace(v)`; predicates over I-addresses use `fields(a).E₁`.


## The state model

ASN-0036 gave us C and M(d). Two phenomena require additional state components.

First, entities come into existence. Nelson describes exactly two document creation modes: ex nihilo (a fresh empty document) and forking (a new document derived from an existing one). Gregory confirms both use the same allocation mechanism, differing only in whether the new arrangement starts empty or populated. We need an explicit record of which entities exist.

**Definition (Entity set).** **Σ.E ⊆ T** — the set of allocated entity addresses. Every e ∈ E satisfies ValidAddress(e) (T4, ASN-0034). Entities are organisational — nodes, accounts, documents — not content; element-level addresses live in dom(C), not E:

`(A e ∈ E :: ¬IsElement(e))`

Equivalently, E ⊆ {t : ValidAddress(t) ∧ zeros(t) ≤ 2}. Given this exclusion, the level predicates of ASN-0045 partition E into exactly three strata:

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

**Structural form of n₀.** The bootstrap node is fixed as the single-component tumbler `[1]`: a one-element tumbler whose sole component is `1`. This satisfies ValidAddress(n₀) (T4, ASN-0034: `[1]` is a non-empty sequence of strictly-positive integers), and `zeros(n₀) = 0` (the tumbler contains no zero separator), so `IsNode(n₀)` holds (ASN-0045). The choice is not arbitrary: Nelson specifies at LM 4/28 that "the server address always begins with the digit 1, since all other servers are descended from it... it permits referring to the entire docuverse by '1' on the first position" — establishing `[1]` as the unique root from which all other server (node) addresses descend by prefix extension. Gregory's implementation realises the same structural shape: the granfilade has a single canonical root (the global `granf` fullcrum, `xanadu.h:13–14`, `corediskout.c:21`), and every node address is allocated as a descendant of that single root by the same query-and-increment that governs accounts and documents. Both consultations therefore concur that the bootstrap is a *single canonical root*, not "any tumbler with zeros = 0."

**Consequence for subsequent K.δ node allocations.** With n₀ fixed as `[1]`, the NodeLineage axiom (`n₀ ≼ e` for every node e ∈ E) constrains every node added by a K.δ event to have `[1]` as a tumbler prefix — that is, every node address either *is* `[1]` (only n₀ itself, by reflexivity) or has the form `[1, c₂, c₃, ...]` with `c_i ≥ 1` (a strictly-positive multi-component extension of `[1]`). This rules out node addresses such as `[2]`, `[3]`, or `[2, 1]` that would stand outside `[1]`'s prefix subtree; under the present specification, no such allocation is admitted. Multi-component node tumblers (`[1, 2]`, `[1, 2, 3]`, etc.) remain admissible — they are *interior nodes of the forking tree* in Nelson's sense, baptized by the owner of a parent node within n₀'s subtree, or equivalently emitted by Gregory's granfilade with `depth ≥ 1` under the single root. K.δ's node-allocation case (case (i), below) is unchanged structurally — it imposes ValidAddress(e) ∧ IsNode(e) ∧ e ∉ E plus the protocol-established freshness from NodeUniqueAllocation — but the binding `n₀ = [1]` together with NodeLineage rules out the disconnected-forest scenario that an unbounded `n₀` would have admitted. The cross-document T10a.{2,5} → T10 chain (which relies on prefix-incomparability between document-rooted sub-allocators, supplied by T10a.2 for same-account sibling documents and T10a.5 for different-account documents) is unaffected: it operates within each document's subtree, downstream of node-level lineage, and the binding `n₀ = [1]` merely fixes the single root at which all such subtrees meet.

The bootstrap node seeds the entity hierarchy. Without at least one node, K.δ cannot create accounts (which require a parent node), and without accounts, no documents, and without documents, no content. The choice of n₀ as `[1]` is a stipulation of this ASN, not a state transition. At Σ₀, (E₀)_doc = ∅, so the arrangement invariants S2, S3, S8a, S8-depth, S8-fin, D-CTG, and D-MIN hold vacuously — no arrangements exist.


## Link store and extended system state

This ASN uses properties of the link store. For self-containment, we restate the definitions and invariants needed.

**Definition (Endset).** An *endset* is a finite set of well-formed spans: `Endset = 𝒫_fin(Span)`, where `Span` is the set of well-formed span pairs `(s, ℓ)` satisfying T12 (ASN-0034). The empty set ∅ is a valid endset — `∅ ∈ 𝒫_fin(Span)` trivially — matching ASN-0043's `Endset` definition.

**Definition (Link).** A *link value* is a triple `(F, G, Θ)` where `F, G, Θ ∈ Endset` — the *from-endset*, *to-endset*, and *type-endset* respectively.

**Definition (Subspace identifiers).** We write `s_C` for the content subspace identifier and `s_L` for the link subspace identifier. These are the first components of the element field for content and link addresses respectively: `fields(a).E₁ = s_C` for content addresses, `fields(ℓ).E₁ = s_L` for link addresses. The same identifiers serve for V-positions: `subspace(v) = v₁`.

**SC-NEQ (Axiom, SubspaceDistinctness).** `s_C ≠ s_L`.

This is an axiom of this ASN. Neither ASN-0034 nor ASN-0036 nor ASN-0043 derives it; without it, L0 would not partition addresses (the L-clause and C-clause would coincide), L14 would be vacuous, and the link-subspace fixity argument under K.μ~ would collapse. SC-NEQ stands alongside NoDeallocation (ASN-0034) and S0 (ASN-0036) as a load-bearing axiomatic premise.

This is the structural precondition for every disjointness argument in this ASN. The derivation of L14 (StoreDisjointness, dom(C) ∩ dom(L) = ∅) is a three-premise chain, not a single appeal to T7:

  - **L0 (SubspacePartition, this ASN, below).** Every a ∈ dom(C) has fields(a).E₁ = s_C; every a ∈ dom(L) has fields(a).E₁ = s_L. (L0's C-clause is added in this ASN; the L-clause is from ASN-0043.)
  - **SC-NEQ (axiom of this ASN).** s_C ≠ s_L.
  - **T7 (FirstElementFieldDistinction, ASN-0034).** Two tumblers with distinct first element-field components (and otherwise equal upstream structure being immaterial) are themselves distinct addresses; equivalently, the value of fields(a).E₁ partitions tumblers into disjoint subspaces.

  Chaining: suppose a ∈ dom(C) ∩ dom(L). By L0's C-clause, fields(a).E₁ = s_C; by L0's L-clause, fields(a).E₁ = s_L. Since fields(a).E₁ is a single value for a single tumbler, s_C = s_L, contradicting SC-NEQ. Therefore dom(C) ∩ dom(L) = ∅, i.e., L14 holds. T7 underwrites the partition-by-E₁ structure that makes L0's two clauses meaningful as a per-store partition; the contradiction itself closes via L0 + SC-NEQ alone.

Without SC-NEQ, L0's two clauses would not partition (the C-clause and L-clause could pick out the same subspace), and L14 would be vacuous. Without L0, the per-store fixity of fields(a).E₁ would not be available, and the chain would have nothing to extract a contradiction from. T7's role is structural rather than derivational: it underwrites the global picture that fields(a).E₁ partitions the tumbler space into disjoint subspaces, justifying the use of s_C and s_L as subspace identifiers rather than mere first-component values. The L14 chain itself appeals only to the function-value uniqueness of fields(a).E₁ for a single a, which holds by the definition of fields(·), not by T7.

We note that `s_C ≥ 1` follows from S7b and T4: content I-addresses are element-level by S7b (`zeros(a) = 3`), and T4 requires every element-field component to be strictly positive, so `fields(a).E₁ = s_C > 0`. The same derivation gives `s_L ≥ 1`: link I-addresses are element-level by L1 below (`zeros(ℓ) = 3`), so by T4, `fields(ℓ).E₁ = s_L > 0`.

**L0 (SubspacePartition, local extension of ASN-0043's L0).**

  `(A a ∈ dom(Σ.L) :: fields(a).E₁ = s_L)`

  `(A a ∈ dom(Σ.C) :: fields(a).E₁ = s_C)`

ASN-0043's L0 carries only the L-clause; the second (C-clause) is introduced here as a local extension for this ASN's extended state, because the four-component state of ASN-0036 had no need to constrain content addresses to a fixed subspace identifier (only one subspace was in use). With the link store admitted as a distinct component, L0's C-clause is the structural counterpart needed to underwrite L14 (StoreDisjointness) below. This ASN's K.α amendment (below) supplies the C-clause as a content-subspace allocation precondition; the C-clause is then a property of this ASN's extended state, not a retroactive modification of ASN-0043.

**L1 (LinkElementLevel).**

  `(A a ∈ dom(Σ.L) :: zeros(a) = 3)`

Every link address is an element-level tumbler.

**L1a (LinkScopedAllocation).**

  `(A a ∈ dom(Σ.L) :: origin(a) ∈ E_doc)`

Every link address is allocated under the tumbler prefix of a document in E_doc.

**L3 (TripleEndsetStructure, local extension of ASN-0043's L3).**

  `(A a ∈ dom(Σ.L) :: Σ.L(a) = (F, G, Θ) where F, G, Θ ∈ Endset ∧ Θ ≠ ∅)`

Every link in the link store has exactly three endsets, with the type endset non-empty. This is a local extension of ASN-0043's L3 (NEndsetStructure: `|Σ.L(a)| ≥ 3 ∧ Σ.L(a).e₃ ≠ ∅`) — a stronger property than the foundation's, applied within this ASN's extended state — narrowing the foundation's `N ≥ 3` to a fixed-three arity. The udanax-green realisation places exactly three endsets per link — from, to, and type — at three fixed positions, and Nelson's design uses the same three uniformly ("a package of connecting or marking information" with from/to/type — LM 4/12). The non-empty type-endset clause of the foundation is preserved verbatim: `Σ.L(a).e₃ ≠ ∅` (equivalently, `Θ ≠ ∅`) is mandatory for every link in dom(Σ.L). The N ≥ 3 generality of ASN-0043 is preserved in principle for future extensions; this ASN's transition model is closed under the realised arity. Consequently, K.λ's precondition `(F, G, Θ) ∈ Link` is supplemented with the implicit `Θ ≠ ∅` requirement carried by L3, so K.λ refuses to allocate an untyped link.

*Consistency with the foundation.* ASN-0043's L3 carries `Σ.L(a).e₃ ≠ ∅` as a verified-stable invariant of the foundation. A downstream ASN cannot relax it without first revising ASN-0043 — this ASN preserves the constraint. Were a future revision to admit empty Θ (the "untyped link" extension), the appropriate vehicle is an ASN-0043 amendment, with the downstream consequences for L8 (TypeByAddress)'s `same_type` domain made explicit at the foundation level; the present ASN does not anticipate that work. The protocol-level asymmetries Gregory documents — `followlink` with `whichend = 3` requiring a non-empty Θ, `endsetqueries` asymmetric across the three slots, `LINKTHREESPAN` indexing — are consistent with the foundation's mandatory Θ ≠ ∅ clause and require no special accommodation here.

**L12 (LinkImmutability).**

  `(A Σ → Σ' : (A a : a ∈ dom(Σ.L) : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)))`

Once created, a link's address persists in dom(L) and its value is permanently fixed.

**L14 (StoreDisjointness).**

  `dom(Σ.C) ∩ dom(Σ.L) = ∅`

Derived from L0 and SC-NEQ via T7: if `a ∈ dom(C)` then `fields(a).E₁ = s_C`, and if `a ∈ dom(L)` then `fields(a).E₁ = s_L`; since `s_C ≠ s_L`, no address inhabits both domains.

**L-fin (LinkStoreFiniteness).**

  `|dom(Σ.L)| < ∞`

The link store is finite at every reachable state. ASN-0043 names this invariant; here we establish it by induction over the elementary transitions of *this* ASN's transition system, since K.λ is introduced here and is the sole link-allocating transition. *Base:* the extended initial state has `dom(L₀) = ∅`, with `|∅| = 0 < ∞`. *Inductive step:* K.λ extends `dom(L)` by exactly one element (`|dom(L')| = |dom(L)| + 1`), and finiteness is closed under adding one element; every other elementary transition (K.α, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ) holds L in frame (`L' = L`, so `|dom(L')| = |dom(L)|`). Composing over any finite sequence of valid composites yields `|dom(L)| < ∞` at every reachable state. L-fin underwrites the well-definedness of `max{ℓ' ∈ dom(L) : origin(ℓ') = d}` in K.λ's subsequent-link case and bounds the number of orphan links produced by repeated K.λ-alone composites at any finite point in the transition sequence.

**Extended system state.** The extended system state is **Σ = (C, L, E, M, R)**, where L : T ⇀ Link is the link store.

**Extended initial state.** Σ₀ = (C₀, L₀, E₀, M₀, R₀) with L₀ = ∅. The extended invariants hold vacuously at Σ₀: L0, L1, L1a, L3, L12, L14, L-fin are satisfied by empty L (L-fin: `|∅| = 0 < ∞`); S3★'s link-subspace clause is vacuous (no link-subspace V-positions exist in M₀); P4★ reduces to P4 (which holds at Σ₀ per ASN-0047); D-CTG and D-MIN hold vacuously since M₀(d) = ∅ for all d, so V_S(d) = ∅ for every subspace S. This closes the inductive base for the ExtendedReachableStateInvariants theorem.

All existing elementary transitions from ASN-0047 hold L in their frame: L' = L.


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

**P3 (Arrangement as sole locus of destructive change).** Arrangements admit three modes of change:

(a) *Extension*: new V→I mappings may be added to M(d).

(b) *Contraction*: existing V→I mappings may be removed from M(d).

(c) *Reordering*: V-positions of existing mappings may change while the multiset of referenced I-addresses is preserved.

No other component admits contraction or reordering. Gregory states this explicitly: the arrangement layer is "the sole locus of destructive mutation." P3 here is a *qualitative* claim about which components admit which mutability modes; the *quantitative* monotonicity content — domain growth plus value preservation across all non-M components — is supplied separately by P0–P2 (and, in the extended state, L12). P3★ below consolidates the qualitative and quantitative content under one label, with explicit value-preservation conjuncts; that consolidation is therefore a strengthening of P3, not merely an extension of its enumeration to include L.


## Elementary transitions

We seek the elementary modifications — the state changes from which all system operations compose. Each is defined by its effect and its frame: what changes and what does not.

**K.α (Content allocation).** A fresh I-address is bound to a value in the content store:

`C' = C ∪ {a ↦ v}` where `a ∉ dom(C)`

*Precondition:* `IsElement(a)` (S7b, ASN-0036) ∧ `origin(a) ∈ E_doc` ∧ `a ∉ dom(C)` ∧ `a ∉ dom(L)` ∧ `a` is produced by origin(a)'s content sub-allocator (established by SubAllocatorAxiom, defined in the Allocator hierarchy section below). The freshness conjuncts `a ∉ dom(C)` and `a ∉ dom(L)` are listed explicitly so K.α's input contract is closed at the definition site rather than relying on the effect clause (`a ∉ dom(C)` appears there as a side condition of the union) or on the derivation prose for L-disjointness. The first content address under a document is `[d.0.s_C.1]`, supplied by the axiom's content namespace property; subsequent content addresses are inc-produced over the content sub-allocator's frontier (TA5(c), ASN-0034), and T10a's GlobalUniqueness then gives `a ∉ dom(C)` as a consequence — the precondition records the requirement, and the allocator discipline discharges it. The axiom underwrites the first emission (where T10a alone cannot, since the content sub-allocator's anchor `b_C(d)` is a virtual predecessor with no inc-history), and T10a underwrites every subsequent emission. Disjointness from the link sub-allocator (`a ∉ dom(L)`) is supplied by SubAllocatorAxiom's disjointness clause and by SC-NEQ + T7 + L14; again, the precondition records the requirement and the allocator/axiom discipline discharges it. Without these conditions, weaker phrasings ("a is allocated under origin(a)'s prefix") would admit non-conforming allocations that break the uniqueness chain. By the axiom or by GlobalUniqueness (depending on case), a is distinct from every previously allocated content address.

*Frame:* E' = E; (A d :: M'(d) = M(d)); R' = R.

**NodeLineage (Axiom, NodeDescentFromBootstrap).** Every node in E descends structurally from the bootstrap node n₀ by a tumbler-prefix relation:

  `(A e ∈ E : IsNode(e) : n₀ ≼ e)`

where `≼` is the prefix order on tumblers (ASN-0034). Equivalently, every node-level address has n₀ as a tumbler prefix, including n₀ itself (since `n₀ ≼ n₀` by reflexivity of the prefix order). This binds the node hierarchy to a single rooted tree under n₀ — there are no "orphan" nodes unrelated to the bootstrap root.

*Scope.* The axiom covers every node in E at every reachable state, including (i) the bootstrap node n₀ trivially (by reflexivity) and (ii) every node added by a K.δ node-allocation event (where the protocol mechanism establishes prefix descent from n₀ at the moment of allocation). It does *not* constrain accounts (`IsAccount(e)`) or documents (`IsDocument(e)`), whose lineage is governed by the entity-hierarchy spine P8 with `parent(e) ∈ E` — accounts root under nodes and documents root under accounts via the parent(·) chain, and the chain ultimately terminates at some node which then descends from n₀ by the present axiom.

*Structural mechanism.* This is an axiom of this ASN. Consultation evidence documents two equivalent realisations, both of which produce n₀-rooted node lineage: Nelson's *hierarchical baptism* (LM 4/19–4/20), under which a parent node ceremonially issues a child node's identifier as a top-level sibling under its own root, and Gregory's *single global granfilade with query-and-increment dispatch* (granf2.c:209), under which all node identifiers descend from a single granfilade tree by the same query-and-increment that governs accounts and documents. Both protocols produce node addresses whose tumblers extend n₀ by prefix — Nelson's by ownership-rooted baptism under a single root, Gregory's by granfilade descent from a single global tree. The abstract specification leaves the protocol mechanism unspecified — any allocator satisfying `n₀ ≼ e` for every emitted node `e` suffices — and treats the prefix-descent property as the operative axiom. T10 (PartitionIndependence, ASN-0034) and the prefix-extension closure used in the cross-document T10a.{2,5} → T10 chain rely on tumbler-prefix incomparability between sub-allocator anchors `b_L(d₁)` and `b_L(d₂)` for distinct documents (supplied by T10a.2 for same-account sibling documents and by T10a.5 for different-account documents) — that chain operates at the document/account/element levels under parent(·) descent from the documents' root node, and is unaffected by inter-node lineage. NodeLineage operates one level above: it constrains the node-level addresses themselves to be rooted at n₀, ensuring that the *whole entity tree*, not merely each document-subtree, is anchored at a single bootstrap root. Without NodeLineage, K.δ could in principle allocate nodes whose tumblers stand outside n₀'s prefix subtree, producing an entity set with multiple disconnected node-rooted forests; the consultation evidence rejects this scenario uniformly. NodeLineage stands alongside NodeUniqueAllocation, SC-NEQ, SubAllocatorAxiom, NoDeallocation (ASN-0034), and S0 (ASN-0036) as a load-bearing axiomatic premise.

**NodeUniqueAllocation (Axiom, FreshNodeAddress).** Every K.δ node-allocation event — that is, every elementary transition of K.δ whose effect places an entity `e` with `IsNode(e)` into E — produces an address fresh to the entity set: for any such e emitted at state Σ, `e ∉ Σ.E`.

*Scope.* The axiom covers exactly the K.δ events with IsNode(e). It does *not* cover the bootstrap node `n₀`, which is not a K.δ event but a parameter of the initial state Σ₀: `E₀ = {n₀}` by the definition of Σ₀, so `n₀ ∈ E` from the start, and no K.δ ever attempts to allocate it (the K.δ precondition `e ∉ E` would in any case prevent it). The axiom's quantification over "every K.δ node-allocation event" is therefore disjoint from the bootstrap initialization; together, the axiom and the initial-state parameter cover every node in E at every reachable state — `n₀` by stipulation, every subsequent node by the axiom.

*Structural mechanism.* This is an axiom of this ASN. It is not a tautology that the namespace property `e ∉ E` "underwrites itself"; rather, the axiom presumes the following structural mechanism for the node-allocation protocol, under which `e ∉ E` becomes a derivable property at every K.δ node event: **every node address descends from the single bootstrap root n₀ by a chain of ownership-derived baptism events**, where each baptism event extends n₀'s ownership-tree frontier by minting one new identifier within the parent owner's namespace. Two equally admissible realisations of this mechanism are documented in the consultation evidence: Nelson's hierarchical baptism (LM 4/19–4/20), under which a parent node ceremonially issues a child node's identifier as a top-level sibling under its own root; and Gregory's single global granfilade with query-and-increment dispatch (granf2.c:209), under which all node identifiers descend from a single granfilade tree by the same query-and-increment that governs accounts and documents. Both protocols guarantee that each newly-minted identifier is fresh within the root's namespace — neither admits a duplicate emission — and the freshness property is the operative content of the axiom. T10a (ASN-0034) does *not* by itself supply this guarantee: the inc operator extends an existing tumbler within a single ownership domain rather than minting a top-level identifier across independent node-allocating actors, and node addresses (which may be multi-component, per Gregory's granfilade with depth = 1) need not arise from a single inc operation under a single owner. The axiom therefore states the freshness property abstractly while citing the structural mechanism that realises it; the protocol-specific choice (Nelson's baptism vs. Gregory's granfilade vs. any equivalent) is left unspecified, but the *existence* of such a mechanism is what the axiom asserts. Without NodeUniqueAllocation, the K.δ precondition `e ∉ E` for node allocations would have no underwriter, and the inductive entity-set invariants (P1, P8) would lose their base step at every K.δ node event. NodeUniqueAllocation stands alongside SC-NEQ (this ASN), SubAllocatorAxiom (this ASN), NoDeallocation (ASN-0034), and S0 (ASN-0036) as a load-bearing axiomatic premise.

**K.δ (Entity creation).** A fresh entity address enters E with initial state:

`E' = E ∪ {e}` where `e ∉ E ∧ ValidAddress(e) ∧ ¬IsElement(e)`

*Precondition.* The precondition splits on IsNode(e), reflecting the two distinct allocation disciplines — protocol-established node baptism versus T10a-conforming inc-allocation under a parent entity:

**(i) When IsNode(e).** No parent is required: node addresses are not restricted to single-component tumblers, and the consultation evidence confirms multi-component node forms in both the design (Nelson, LM 4/19–4/20, where 1.1, 1.2, 1.3 are nodes "forked" from a root node 1) and the implementation (Gregory, granf2.c:209, which allocates NODE→NODE with depth = 1, producing forms such as 1.1.0.1.1). The structural constraints are ValidAddress(e) ∧ IsNode(e) ∧ e ∉ E ∧ n₀ ≼ e, with zeros(e) = 0 (per the IsNode predicate of ASN-0045) — the tumbler may have any number of strictly-positive components, but must extend the bootstrap root n₀ by prefix. The lineage clause `n₀ ≼ e` enforces NodeLineage at the point of allocation: every K.δ node event must produce an address rooted at the bootstrap, ruling out the disconnected-forest scenario in which an emitted node `e` stands outside `n₀`'s prefix subtree. Together with the base case `n₀ ≼ n₀` at Σ₀ (by reflexivity of `≼`), this precondition discharges NodeLineage as an inductive invariant of every reachable state: the property holds at Σ₀ trivially, and each K.δ node event preserves it by establishing `n₀ ≼ e` at the moment of allocation; all other transitions hold E in frame. The Xanadu design admits node creation beyond the bootstrap n₀; Nelson's hierarchical baptism (a parent node ceremonially issues a child node's identifier as a top-level sibling under its own root) and Gregory's single global granfilade with query-and-increment dispatch are two realisations of the same uniqueness guarantee. Node uniqueness is therefore a *protocol-established* property — every new node descends from the single bootstrap root by a chain of baptism events under that root's ownership, and ownership-derived uniqueness yields the namespace property `e ∉ E` for each fresh node — rather than a T10a consequence: the inc(·, k) operator is defined to extend an existing tumbler within an ownership domain rather than to mint a top-level identifier, so it does not by itself underwrite uniqueness across independent node-allocating actors. The abstract specification leaves the protocol mechanism unspecified — any allocator satisfying the namespace property `e ∉ E` suffices — and treats the resulting `e ∉ E` as the operative axiom NodeUniqueAllocation (introduced above), closing the GlobalUniqueness chain for nodes through this protocol guarantee rather than through T10a. K.δ for nodes therefore imposes no inc-conformance requirement; the address is supplied by the (unspecified) node-allocation protocol, and NodeUniqueAllocation alone guarantees `e ∉ E`.

**(ii) When ¬IsNode(e)** (accounts and documents). The formal precondition list:

- `parent(e) ∈ E` — the parent entity must already exist.
- `e = inc(t, k)` for some `t ∈ T` (the universe of allocated tumblers, per T10a), with `k ∈ {0, 1, 2}` subject to T10a's zeros-count constraints (ASN-0034). T10a's GlobalUniqueness operates on `t ∈ T`. For `k ∈ {0, 2}` we additionally require `t ∈ E`, the entity-level analog of the address-level "previously allocated" requirement: a same-level sibling (k = 0) or a hierarchical-descent step (k = 2) extends a previously-emitted entity address, so the operand must inhabit the entity set. For `k = 1` (the versioning sub-case below) we *do not* lift `t ∈ E` — the k = 1 sub-case admits ghost-base versioning, consistent with Nelson's ghost-element doctrine applied at the immediate version base. See *Scope, base-liveness, and discharge of `e ∉ E` in the ghost-operand case* below for the rationale.
- `k = 1 ⟹ IsDocument(t)` — restated below as part of the k = 1 sub-case discussion, and lifted here to the formal precondition list so the case discipline is visible at the precondition gate. The conjunction with the `e = inc(t, k)` clause requires `IsDocument(t)` but does *not* require `t ∈ E`; in particular, the k = 1 precondition does *not* enforce `t ∈ E_doc`.

  The two sub-cases below differ in what t must be:

  - *Sibling case (k = 0, TA5(c)).* t is a previously allocated entity address at the same level as e under parent(e), so parent(t) = parent(e) and `zeros(t) = zeros(e)`. The increment produces a new sibling at the same depth: `zeros(e) = zeros(t)`. The entity-level relation parent(t) = parent(e) is the appropriate analog of origin here — origin is defined only for element-level addresses (ASN-0036's S7a), whereas t and parent(e) are both entity-level (zeros ≤ 2), so we use parent(·) throughout the entity-allocation analysis. The condition parent(t) = parent(e) means t is a child of parent(e) at the same level as the new entity.
  - *Tumbler-depth extension cases (k ∈ {1, 2}, TA5(b)+TA5(d)).* For k > 0, the constructive clause is TA5(d): `#e = #t + k`, with positions `#t + 1, ..., #t + k − 1` set to `0` (the `k − 1` zero separators) and position `#t + k` set to `1` (the appended terminal). TA5(b) supplies the agreement on the preserved prefix (positions `1..#t`). The two sub-cases differ structurally in `zeros(e)` and in the hierarchical-level relationship between e and t:
    - *Sibling-at-deeper-tumbler-depth (k = 1) — restricted to documents.* TA5(d) with `k = 1` appends `.1` and introduces no new zero separator (the range `#t + 1, ..., #t` of zero positions is empty for `k = 1`), so `zeros(e) = zeros(t)`. Hierarchically e remains at t's level (same zero count); only the tumbler length grows by one component. We restrict this sub-case to `IsDocument(t)` (equivalently, `IsDocument(e)`): the k = 1 form is the structural shape Nelson identifies as a *document version* (LM 4/29), and the consultation evidence is unambiguous that versioning is reserved to documents — Nelson treats versioning solely at the document level, and Gregory's `docreatenewversion` (do1.c:271) realises depth-1 tumbler-extension only as `makehint(DOCUMENT, DOCUMENT, 0, ...)`. Account-level k = 1 would produce a structurally well-formed `[N, 0, U, 1]` (still IsAccount), but the design admits no account "version" semantics — accounts subdivide hierarchically (parent owns children at deeper zero count, k = 2), not by depth-1 tumbler extension. Admitting account-level k = 1 would create an entity with no documented role in the model; we therefore exclude it at the precondition. See the note on version semantics below for the document case. (The complementary case for nodes is handled separately: case (i) above governs all node allocations and does not invoke k at all, since node addresses are not constrained to single-component tumblers but are emitted via the protocol-established NodeUniqueAllocation axiom rather than by inc.)
    - *True hierarchical descent (k = 2).* TA5(d) with `k = 2` appends `.0.1` — one new zero separator followed by the terminal `1` — so `zeros(e) = zeros(t) + 1`. Hierarchically e drops one level: node → account or account → document. The descent step crosses a level boundary, so the same allocator's frontier need not have produced a child at e's level before.
  Combined: `zeros(e) = zeros(t) + max(0, k − 1)`. Equivalently by case: `zeros(e) = zeros(t)` for k ∈ {0, 1} (no new zero separator is introduced — k = 0 is a same-level sibling, k = 1 appends `.1` directly), and `zeros(e) = zeros(t) + 1` for k = 2 (TA5(d) introduces one new zero separator before the terminal `.1`). The earlier "Combined: `zeros(e) = zeros(t) + (k − 1)`" expression — which would give `zeros(t) − 1` at k = 0 — is corrected here by the `max(0, ·)` clamp; the per-case identities above are the operative statement and the closed form is a convenience. The "parent matches parent(e)" condition resolves directly from the inc relationship: for k ∈ {0, 1} the inc step preserves the parent, so parent(e) = parent(t) and t is a sibling of e under their shared parent; for k = 2 the inc step appends `.0.1`, so parent(e) = t and t is itself the parent of e. (These two shapes are exhaustive of the case (ii) sub-cases: k = 0 admits only the shared-parent shape by construction, and k = 2 admits only the parent-is-t shape because parent strips the trailing `.0.1` produced by inc(·, 2).) The unqualified term "descent" elsewhere in this ASN denotes *tumbler-depth descent* — length extension `#e = #t + k` — and coincides with zeros-count descent only at k = 2; the k = 1 sub-case is descent in the tumbler-depth sense but a same-level sibling in the zeros-count sense.

In both sub-cases of (ii) — sibling (k = 0) and tumbler-depth extension (k ∈ {1, 2}) — the resulting e lies within parent(e)'s ownership domain (its tumbler-prefix subtree), and `zeros(e) ≤ 2` (since e ∈ E is non-element). The split makes explicit that "parent(t) = parent(e)" carries different content for k = 0 (t is itself in parent(e)'s child-level) versus k > 0 (t is at parent(e)'s level, descent then enters the child-level). The discharge of `e ∉ E` is sub-case-dependent. For the *live-operand* sub-cases of case (ii) — k = 0 sibling (where `t ∈ E` is required), k = 2 hierarchical descent (where `t ∈ E` is required), and k = 1 with `t ∈ E_doc` — T10a's GlobalUniqueness (ASN-0034) applies: every inc-produced address from an operand in a T10a allocator's domain is distinct from every previously allocated address in that domain, so `e ∉ E` follows. This is the same chain that governs K.α: T10a-conforming allocations carry the uniqueness guarantee, and weaker phrasings ("typically allocated") would admit non-conforming allocations that break the chain. For the *ghost-operand* k = 1 sub-case (where `t ∉ E_doc` — admitted by the precondition list above, which does not require `t ∈ E` at k = 1), T10a's GlobalUniqueness does *not* underwrite `e ∉ E`: T10a governs inc events whose operand lies in some T10a allocator's domain, and a ghost operand is by stipulation outside every entity allocator's domain. The discharge in that sub-case is treated separately in *Scope, base-liveness, and discharge of `e ∉ E` in the ghost-operand case* below, via the K.δ precondition `e ∉ E` itself, combined with TA5 determinism on the candidate address. For nodes (case (i)), `e ∉ E` is supplied by NodeUniqueAllocation rather than by T10a — the three discharge paths (T10a for live-operand case (ii), K.δ precondition + TA5 for ghost-operand k = 1, NodeUniqueAllocation for case (i)) close the same `e ∉ E` chain through different premises.

When IsDocument(e): M'(e) = ∅ (empty arrangement). Gregory confirms that document creation and account creation share the same inc-based allocation discipline, differing only in the allocation level (document vs. account); node creation alone falls outside this discipline, using the external allocator described above.

*Note on k = 1 (version semantics).* The k = 1 sub-case admits a structurally distinguished use: when t is a document at form `[N, 0, U, 0, D]` (zeros = 2), `e = inc(t, 1) = [N, 0, U, 0, D, 1]` is again zeros = 2 — still document-level (per IsDocument, ASN-0045) — but with one additional terminal component. The consultation evidence identifies this form as a *document version*: Nelson describes versions as new documents whose addresses indicate ancestry (LM 4/29, conflating version and sub-document), and Gregory's `docreatenewversion` (do1.c:271) realises it as `makehint(DOCUMENT, DOCUMENT, 0, ...)` with depth = 1 — a k = 1 tumbler-depth extension from an existing document address. In purely structural terms, the present ASN admits this allocation: K.δ's k = 1 sub-case (TA5(d) appending the terminal `.1`, TA5(b) preserving the prefix) applies, with t = the originating document.

*Scope, base-liveness, and discharge of `e ∉ E` in the ghost-operand case.* K.δ as stated above admits, for k = 1 events from a document address, an inc operand `t` that need not be in E_doc — i.e., the version base `[N, 0, U, 0, D]` may be a ghost document (a valid document address that was never allocated, or whose entity record is otherwise absent from E). This is the abstract-spec reflection of Nelson's ghost-element doctrine (LM 4/23: "no specific element need be stored in tumbler-space to correspond to them"), which is general — Nelson explicitly extends it to documents — and version addressing inherits it (LM 4/29; LM 2/19). Consultation evidence (consultation-54, answer-05) underwrites the relaxation from two directions: Nelson confirms "documents are explicitly named, not just servers and accounts" and that version addressing places "no requirement that an immediate parent be a live entity"; Gregory confirms that `docreatenewversion` does *not* enforce a bert-style liveness check on the source (it uses `NOBERTREQUIRED` and falls through to `fetchorglgr`, which checks only that the source ISA is a structurally valid granfilade leaf, not that the document is in the open list), and further documents an ordering bug (the version ISA is allocated at `do1.c:277` *before* the source check at `do1.c:281`, so a non-existent source causes an allocated-but-leaked granfilade slot). Inheriting the implementation's structural-existence check at the abstract layer would also inherit the leak as an admissible state; the implementation's source-liveness requirement is therefore a FEBE-layer concern, not an abstract invariant — a subsequent version-management ASN may introduce a versioning-specific lineage axiom for *specific composite operations* (such as "version-with-content-copy"), but the elementary K.δ transition admits the bare ghost-base case. The relaxation is invariant-safe by a routine frame argument: K.δ frames every state component except E (and `M(e) = ∅` for documents), so every per-state invariant beyond the entity layer (S0–S9, L0–L14, J0–J4 and their starred forms) holds by frame; the entity-hierarchy spine P8 — the only invariant that could touch the new entity's relationship to t — is preserved through `parent(·)` rather than through the inc operand, since the version step `[N,0,U,0,D] → [N,0,U,0,D,k]` crosses no zero separator (`parent(e) = parent(t)`), and `parent(e) ∈ E` is itself a K.δ precondition independent of whether t is in E. Any subsequent K.α + K.μ⁺ + K.ρ activity under the new document anchors through `e` itself, never through t. Detailed per-invariant verification on a concrete state is exhibited in the *Worked example: ghost-base document versioning* below, where each step enumerates the check on E, M, C, L, R against the named invariant set (P8 by parent chain, NodeUniqueAllocation and NodeLineage vacuously on non-node entities, S0–S9 and L0–L14 by frame, J0–J4 vacuously at K.δ with empty arrangement). Three positions were available — (a) identify an invariant that demands the strengthening (none was found), (b) relax to the weaker precondition and admit ghost-base versioning at the abstract level, or (c) adopt the stronger precondition as a deliberate scope decision; the present ASN takes position (b), on the grounds that the abstract specification should constrain implementations rather than inherit implementation choices that have no invariant-level grounding. The companion question of intermediate-version liveness — whether `[N,0,U,0,D,k]` with k ≥ 2 (allocated as an inc-k=0 sibling of the prior version) requires `[N,0,U,0,D,k−1] ∈ E_doc` — is decided affirmatively as an immediate consequence of the k = 0 sub-case's `t ∈ E` requirement: every k ≥ 2 version event proceeds via k = 0 sibling allocation with the prior version as inc operand, which must therefore be in E; chains of versions allocated within this ASN's transition history exhibit live intermediates by construction, and the relaxation applies only to the *initial* version step. Discharge of `e ∉ E` in the ghost-operand case proceeds via the K.δ precondition itself rather than via T10a: T10a's GlobalUniqueness conclusion is conditional on the operand inhabiting some T10a allocator's domain (the resulting address is distinct from every prior allocation *within that domain*), but a ghost operand by stipulation lies outside every entity allocator's domain, so the caller of K.δ at the k = 1 ghost-operand sub-case must verify `inc(t, 1) ∉ E` directly against the current entity set, by inspection of E rather than by appeal to T10a. TA5 (ASN-0034) supplies the structural fact that `inc(t, 1) = t.1` is deterministically determined by t (TA5(b) preserves the prefix `1..#t`, TA5(d) at k = 1 appends `.1` with no intervening zero separator), so the candidate address is exhibitable from t alone, and the precondition reduces to checking that this exhibited address is not already in E. The three discharge paths — T10a for live-operand case (ii); K.δ precondition + TA5 for ghost-operand k = 1; NodeUniqueAllocation for case (i) — close the same `e ∉ E` chain through different external premises, and no path silently substitutes for another.

*Deferred semantics.* The richer version contract — what arrangement-transition invariants must hold between successive versions, whether content allocators of base and version are linked, how provenance flows between them, and whether version lineage must be acyclic — lies outside the entity-hierarchy spine that P8 governs (parent(·) truncates by zero separators; a version's terminal field has no preceding zero, so the version-to-base relationship is not on the parent spine). These questions are deferred to the open question "What relationship must hold between a document's version lineage and its sequence of arrangement transitions?" below, and a comprehensive resolution belongs to a subsequent version-management ASN. The present ASN treats `[N, 0, U, 0, D, k]` for k ≥ 1 as an admissible K.δ output under T10a's structural discipline combined with `IsDocument(t)`; ghost-base versioning is admitted at the initial step, intermediate liveness is enforced through the inc operand at k ≥ 2 sibling allocations, and the arrangement/provenance/lineage contract beyond bare entity membership remains deferred.

Nelson identifies two document-creation modes — ex nihilo and forking. At the elementary level, both begin with K.δ producing an empty document. When the source's content subspace is non-empty, forking is compound: K.δ followed by arrangement extension and provenance recording (J4 below). When the source's content subspace is empty — whether M(d_src) = ∅ or M(d_src) contains only link-subspace positions — fork reduces to K.δ alone, structurally identical to ex nihilo creation.

*Frame:* C' = C; (A d' :: M'(d') = M(d')); R' = R.

**K.μ⁺ (Arrangement extension).** New V→I mappings are added to some d ∈ E_doc, with existing mappings unchanged:

`dom(M'(d)) ⊃ dom(M(d)) ∧ (A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))`

Extension is pure addition — the domain grows, and no existing value is altered. Without the value-preservation clause, K.μ⁺ could silently replace values at existing positions, conflating extension with replacement. The decomposition of replacement into K.μ⁻ followed by K.μ⁺ depends on each being a pure operation.

The two conjuncts together force new mappings at positions disjoint from dom(M(d)). For any v ∈ dom(M'(d)) \ dom(M(d)), v is a new position by construction. For any v ∈ dom(M(d)), the value-preservation clause pins M'(d)(v) = M(d)(v), so that position cannot be the site of a "new" mapping carrying a different value. Hence dom(M'(d)) \ dom(M(d)) — the set of newly-mapped positions — is exactly the set of positions disjoint from dom(M(d)) that K.μ⁺ adds. The K.μ~ decomposition (replacement as K.μ⁻ then K.μ⁺) relies on this disjointness: the K.μ⁻ step empties the affected positions from dom, and the subsequent K.μ⁺ step adds mappings at positions that — having been removed — are now disjoint from the intermediate domain.

*Precondition:* `d ∈ E_doc`; for every new mapping M'(d)(v) = a, `a ∈ dom(C)` (S3, ASN-0036 — since K.μ⁺'s frame holds C' = C, referential integrity reduces to membership in the pre-state content store); new V-positions satisfy S8a (all components strictly positive), and the resulting arrangement M'(d) satisfies S8-depth (uniform depth within each subspace); dom(M'(d)) is finite (S8-fin); the resulting arrangement satisfies D-CTG (contiguity within each subspace, ASN-0036) and D-MIN (minimum position in each non-empty subspace, ASN-0036). Functionality (S2) is preserved: dom(M'(d)) ⊃ dom(M(d)) with value preservation at existing positions means new entries are assigned at positions outside dom(M(d)), so M'(d) remains a function — extending a partial function at disjoint domain elements cannot introduce ambiguity.

In a composite transition, K.α may precede K.μ⁺, extending dom(C) before K.μ⁺ executes. At that intermediate state the freshly allocated address is already in the content store, satisfying the precondition. From the composite perspective, the I-address in a new mapping falls into one of two cases:

(i) Freshly allocated — co-occurring K.α places a into dom(C) before K.μ⁺ maps to it. Nelson: "new content enters Istream permanently."

(ii) Previously existing — a ∈ dom(C) at the composite's initial state. This is transclusion: "the copy shares I-addresses with the source. No new content is created in Istream."

*Frame:* C' = C; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R.

**Per-state arrangement shape (D-SEQ★).** For each non-empty subspace S in M(d), V_S(d) takes the canonical sequential shape

  `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` for some `n_S ≥ 1`,

with the inner positions of uniform depth m_S (the common depth within subspace S, by S8-depth) and `n_S = |V_S(d)|`. This is the *D-SEQ★* per-state invariant. It is derived from D-CTG★ + D-MIN★ + S8-depth + S8-fin + S8a; the full derivation is given in *Amendments to existing transitions* below under D-SEQ★'s own heading, after D-CTG★ and D-MIN★ are introduced (the derivation cannot be staged here because it consumes the strengthened-postcondition versions of D-CTG and D-MIN that the Amendments section establishes). The preamble's role is to license citing D-SEQ★ by name at the K.μ⁻ admissible-removal precondition immediately below, at the K.μ~-FIX domain-fixity argument, at the link-subspace fixity proof, and at the ExtendedReachableStateInvariants induction, without re-derivation at each site. The per-state guarantee is inductively established without appeal to K.μ⁻'s precondition, so the forward-derivation pointer is non-circular: K.μ⁻'s precondition consumes D-SEQ★ at the pre-state (where it is established by the inductive hypothesis), the case-analysis verifies the D-CTG★/D-MIN★ postconditions at the post-state, and the D-SEQ★ derivation below reads its hypotheses from invariants K.μ⁻ either preserves or has frame on.

**K.μ⁻ (Arrangement contraction).** Existing V→I mappings are removed from some d ∈ E_doc, with surviving mappings unchanged:

`dom(M'(d)) ⊂ dom(M(d)) ∧ (A v : v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v))`

The strict-subset clause `dom(M'(d)) ⊂ dom(M(d))` is unsatisfiable when `dom(M(d)) = ∅` (no proper subset of the empty set exists); the precondition below makes this explicit by requiring `dom(M(d)) ≠ ∅`, so K.μ⁻ is undefined at states where d has nothing to contract.

*Precondition:*
- `d ∈ E_doc`.
- `dom(M(d)) ≠ ∅` — d's arrangement must contain at least one mapping to be contracted; combined with the effect clause `dom(M'(d)) ⊂ dom(M(d))`, this ensures K.μ⁻ is a strict contraction at a state where contraction is well-defined.
- *Admissible removal pattern (per-subspace suffix or full clearance).* For each subspace S, the removed positions in `V_S(d)` form either a suffix of `V_S(d)` under the D-SEQ★-shaped enumeration or all of `V_S(d)`. The shape is the per-state D-SEQ★ invariant stated in *Per-state arrangement shape (D-SEQ★)* immediately above and derived in full below: `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` for some `n_S ≥ 1`, with inner positions of uniform depth m_S. Under that pre-state shape, there exists `0 ≤ n'_S ≤ n_S` per subspace such that the post-state subspace satisfies `V_S(d') = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}` — partial suffix removal when `1 ≤ n'_S < n_S`, full clearance when `n'_S = 0`, and no change in S when `n'_S = n_S`. The per-subspace patterns are independent across the two subspaces `s_C` and `s_L`: each subspace may independently exhibit partial suffix removal, full clearance, or no change, provided at least one subspace contracts strictly so the effect-clause requirement `dom(M'(d)) ⊂ dom(M(d))` is satisfied at the whole-arrangement level.

The case analysis below is a *verification* that this admissible-pattern precondition is exactly what the D-CTG★ and D-MIN★ postconditions (inherited from the amendments below) admit at the post-state, by exhibiting the two complementary forbidden patterns — interior removal (forbidden by D-CTG★) and prefix removal (forbidden by D-MIN★) — that the precondition excludes. The verification establishes bidirectional equivalence: every pattern satisfying the precondition discharges D-CTG★ and D-MIN★ at the post-state, and every post-state satisfying D-CTG★ and D-MIN★ under the D-SEQ★-shaped pre-state arises from a per-subspace pattern matching the precondition. Stating admissibility as an explicit precondition aligns K.μ⁻'s contract with the form used by every other elementary transition in this ASN (K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L all state explicit preconditions), so the case analysis below acts as a closed verification rather than the sole source of admissibility content.

Contraction preserves functionality (S2), referential integrity of survivors (S3, since C' = C), V-position well-formedness (S8a), uniform depth within subspace (S8-depth), and finiteness (S8-fin) by restriction of M(d). The post-state must additionally satisfy D-CTG★ and D-MIN★ (per-subspace contiguity and minimum-anchoring, including the link subspace `s_L`); these are the load-bearing constraints that determine which contractions are admissible. Given the D-SEQ★-shaped pre-state — stated in *Per-state arrangement shape (D-SEQ★)* above and derived in full below — `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` for some `n_S ≥ 1` with uniform depth `m_S ≥ 2` in every non-empty subspace S. Under this pre-state shape, the D-CTG★/D-MIN★ postconditions admit exactly the per-subspace patterns where the removed positions in each subspace form a suffix `{[S, 1, ..., 1, k] : n'_S < k ≤ n_S}` for some `0 ≤ n'_S ≤ n_S` (full-subspace clearance corresponds to n'_S = 0). The case analysis below partitions per-subspace removal patterns into three classes — suffix removal (compatible), interior removal (incompatible with D-CTG★), and prefix removal (incompatible with D-MIN★) — exhibiting how the postconditions force the suffix discipline:

(a) *Suffix removal (matches the precondition's admissible pattern).* Removing `{[S, 1, ..., 1, k] : n'_S < k ≤ n_S}` for some `0 ≤ n'_S ≤ n_S` leaves `V_S(d') = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}` — still contiguous (D-CTG★) and, when n'_S ≥ 1, still minimum-anchored at `[S, 1, ..., 1] = [S, 1, ..., 1, 1]` (D-MIN★). When n'_S = 0 (full-subspace clearance), V_S(d') = ∅ and D-CTG★ and D-MIN★ hold vacuously. The case verifies that the precondition's per-subspace shape discharges both postconditions on the affected subspace.

(b) *Interior removal (excluded by the precondition; D-CTG★ verifies the exclusion).* Suppose K.μ⁻ were to remove some position `[S, 1, ..., 1, k₀]` with `1 ≤ k₀ < n_S` while retaining at least one position `[S, 1, ..., 1, k']` with `k' > k₀` *and* at least one position `[S, 1, ..., 1, k'']` with `k'' < k₀`. (The complementary subcase — `k₀` removed, some `k' > k₀` retained, but *no* `k'' < k₀` retained — implies every index strictly below `min{k : [S, 1, ..., 1, k] ∈ V_S(d')}` is removed; since `1 ≤ k₀ < min{k : ...}`, the index 1 lies in that removed range, so `[S, 1, ..., 1, 1]` is itself removed. That subcase therefore falls under (c) below, which forbids it via D-MIN★; (b) treats only the "true interior" pattern where the removed `k₀` has retained neighbours on both sides.) Under the present hypothesis, set `k_min := min{k : [S, 1, ..., 1, k] ∈ V_S(d')}`; the retained `k''` gives `k_min ≤ k'' < k₀`. Under the lex order on terminal-varying tuples, `[S, 1, ..., 1, k₀]` then lies strictly between `[S, 1, ..., 1, k_min]` and `[S, 1, ..., 1, k']`, yet is absent from V_S(d'). This violates D-CTG★'s requirement that V_S(d') be contiguous under the V-ordering.

(c) *Prefix removal (excluded by the precondition; D-MIN★ verifies the exclusion).* Suppose K.μ⁻ were to remove `[S, 1, ..., 1, 1]` while retaining at least one position `[S, 1, ..., 1, k]` with `k ≥ 2`. Then `V_S(d') ≠ ∅` and the smallest surviving terminal index is some `k_min ≥ 2` (since the position at k = 1 has been removed). Hence `min(V_S(d')) = [S, 1, ..., 1, k_min]` with `k_min ≥ 2`, so `min(V_S(d')) ≠ [S, 1, ..., 1, 1] = [S, 1, ..., 1]` of depth m_S. This violates D-MIN★'s requirement at the post-state that the minimum of every non-empty subspace be the all-1 tuple of depth m_S. (The full-subspace clearance n'_S = 0, which removes [S, 1, ..., 1, 1] *together with* every other position, falls under (a), not (c): there V_S(d') = ∅ and D-MIN★ is vacuous.)

Together, (a) realises the precondition's admissible pattern and is consistent with the D-CTG★/D-MIN★ postconditions; (b) and (c) are the complementary forbidden patterns whose exclusion by the precondition is verified through D-CTG★ and D-MIN★ respectively. The case analysis is exhaustive across the D-SEQ★-shaped pre-state: every per-subspace contraction falls into one of the three cases, and the precondition-side and postcondition-side characterisations of admissibility coincide on (a). The admissibility content thus appears once at the precondition gate (per the precondition list above) and is verified once at the postcondition gate (per the case analysis); the two are equivalent, and downstream proofs may discharge through either side.

Contraction is pure removal — the domain shrinks, and no surviving value is altered. Without the value-preservation clause, K.μ⁻ could modify values at remaining positions, conflating contraction with rewriting.

Nelson: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." Contraction changes what a document displays; it does not change what exists.

*Frame:* C' = C; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d')).

**K.μ~ (Arrangement reordering, named composite — pointer only).** K.μ~ is *not an elementary transition*. It is a *named composite* of K.μ⁻ + K.μ⁺, analogous to J0/J1★/J2/J3/J4 and outside the seven-element elementary set {K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ}. The full contract — bijection equation, admissibility constraints, derived frame — together with the link-subspace fixity derivation, the case decomposition, and the K.μ~-FIX domain-fixity result, is stated and proved in *Decomposition of K.μ~* below (placed after S3★-aux in *Generalized referential integrity* and CL-UNIQ in *Link-subspace ownership* to discharge the per-state invariants on which the link-subspace fixity argument depends, so the resulting placement is structurally non-circular). Every reference to "K.μ~" elsewhere in this ASN — in the Frame extension catalogue, in the elementary case analysis of *ExtendedReachableStateInvariants*, in the structural-sufficiency claim, in worked examples, in the ValidComposite★ definition, and in the J3 isolation discussion — denotes any K.μ⁻ + K.μ⁺ realisation of the contract, with invariant preservation, frame, and coupling all routed through the underlying elementary steps; treating K.μ~ as a "case" in proofs is presentational shorthand for "K.μ⁻ + K.μ⁺ realisation."

**K.ρ (Provenance recording).** A document-content association enters R:

`R' = R ∪ {(a, d)}` where `a ∈ dom(C) ∧ d ∈ E_doc`

*Precondition:* `a ∈ dom(C)` ∧ `d ∈ E_doc`. The level constraint IsElement(a) follows from S7b (every a ∈ dom(C) satisfies IsElement(a)).

*Frame:* C' = C; E' = E; (A d :: M'(d) = M(d)).

Five primitive kinds — K.α, K.δ, K.μ⁺, K.μ⁻, K.ρ — are *structurally sufficient* for the modification kinds catalogued in this ASN. By "structurally sufficient" we mean: for each component of the four-component state (C, E, M, R), the elementary set covers each admissible direction of change recognised by the design enumeration. The argument is structural: (C, E, M, R) admits exactly one growth mode for C (K.α), one for E (K.δ), one for R (K.ρ), and two independent mutation modes for M — entry addition (K.μ⁺) and entry removal (K.μ⁻); Gregory's independent reduction of the protocol surface to six persistent-modification kinds confirms the enumeration. Any modification to a finite partial function decomposes into additions and removals; *replacement* — changing which I-address a V-position maps to — decomposes into K.μ⁻ followed by K.μ⁺, but the granularity of the decomposition depends on which V-position is being replaced under the D-CTG★/D-MIN★ postconditions of K.μ⁻ (which admit per-subspace suffix removal or full clearance, as established by the case analysis above):

- **Replacement at the maximum position of a subspace.** When the replaced V-position is `max(V_S(d))` for its subspace S, K.μ⁻ removes that single position (a 1-element suffix of V_S(d)) and K.μ⁺ then re-adds it with the new value. Replacement is a single-position K.μ⁻ + K.μ⁺ pair.

- **Replacement at an interior position of a subspace.** When the replaced V-position is `[S, 1, ..., 1, k₀]` with `k₀ < n_S` (some positions above it remain), the D-CTG★ postcondition does *not* admit removing position k₀ alone — that would leave a gap above k₀ within the subspace, violating D-CTG★ at the intermediate state. Replacement at an interior position therefore decomposes as follows: K.μ⁻ removes the suffix `{[S, 1, ..., 1, k] : k₀ ≤ k ≤ n_S}` (every position from k₀ to the maximum), and K.μ⁺ then re-adds the entire suffix `{[S, 1, ..., 1, k] : k₀ ≤ k ≤ n_S}` with the replaced position k₀ now carrying the new value and all other positions k ∈ {k₀+1, ..., n_S} carrying their previously mapped values. This is a multi-position K.μ⁻ + K.μ⁺ pair; the count of positions removed and re-added equals `n_S − k₀ + 1`.

A *worked decomposition* of the interior case appears in the K.μ~ subsection below (Decomposition of K.μ~ into K.μ⁻ + K.μ⁺), where full-clearance K.μ⁻ + content-rebuild K.μ⁺ is treated in full detail; interior replacement is the same shape with `n'_S = k₀ − 1` rather than `n'_S = 0`. The simple "K.μ⁻ followed by K.μ⁺" gloss is correct when read as a pair of operations, but the *cardinality* of each operation depends on position: replacement at the maximum is one position; replacement at the interior is the suffix from the replaced position to the maximum, all rebuilt in one K.μ⁻ + K.μ⁺ pair.

K.μ~ is a named composite (analogous to J0/J1★/J2/J3/J4), not a primitive transition. The decomposition account — including the K.μ~-FIX domain-fixity argument and the degenerate-case analysis — is deferred to the dedicated *Decomposition of K.μ~* section below, placed after the per-state invariants S3★-aux (defined in *Generalized referential integrity*) and CL-UNIQ (defined in *Link-subspace ownership*) on which it depends. This presentation order avoids forward references; the per-state invariants are inductively established without appeal to the decomposition account or its corollaries, so the resulting placement is structurally non-circular.

We observe that neither split nor merge appears as an elementary transition. Nelson addresses this explicitly: the effect of splitting a document is achieved by creating two new documents and transcluding different portions of the original into each. Merging is creating a new document and transcluding from multiple sources. Both compose from K.δ, K.μ⁺, and K.ρ — the elementary transitions suffice.

The sufficiency claim above is bounded — it is structural (one growth mode per append-only component, two mutation modes for M, closure under composition), not exhaustive over the admissible-state-difference lattice — and one specific known gap (Nelson's tombstone-style interior link withdrawal at LM 4/9, not expressible as any K.μ⁻ contraction or composite under the amended D-CTG★/D-MIN★) lies outside it. The open-completeness caveat, the tombstoning gap, two further scope exclusions, and the cross-references to deferred open questions are consolidated in *Structural sufficiency and known gaps* below; earlier occurrences are deliberately terse so that the consolidated section is the single point of reference.

**Lemma (Arrangement invariants from elementary preservation).** Every valid composite transition preserves S2, S3, S8a, S8-depth, S8-fin, D-CTG, and D-MIN. Each elementary transition preserves these per-state properties: K.μ⁺ establishes them via its preconditions (disjoint extension for S2, referential integrity for S3, explicit S8a/S8-depth/S8-fin/D-CTG/D-MIN requirements); K.μ⁻ preserves S2/S3/S8a/S8-depth/S8-fin by restriction of M(d) and D-CTG/D-MIN by its explicit postcondition; K.δ for documents produces the empty arrangement (vacuously satisfying all seven); all other transitions hold M in frame. Since each step of a valid composite preserves these per-state properties, they hold at every intermediate and final state.


## Amendments to existing transitions

**Frame extension (all existing transitions).** In the extended state Σ = (C, L, E, M, R), each existing elementary transition's frame is extended with `L' = L`. The K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, and K.ρ transitions hold L in frame: none of them allocates, deallocates, or mutates the link store. The original frames at each operator's definition site predate the introduction of L as a state component and omit the L clause; the formal frame for each in the extended state is:

- *K.α (extended frame):* L' = L; E' = E; (A d :: M'(d) = M(d)); R' = R.
- *K.δ (extended frame):* L' = L; C' = C; (A d' :: M'(d') = M(d')); R' = R.
- *K.μ⁺ (extended frame):* L' = L; C' = C; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R.
- *K.μ⁻ (extended frame):* L' = L; C' = C; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d')).
- *K.μ~ (extended frame):* L' = L; C' = C; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d')) — derived from the K.μ⁻ + K.μ⁺ decomposition under the amended frames (composition preserves L' = L).
- *K.ρ (extended frame):* L' = L; C' = C; E' = E; (A d :: M'(d) = M(d)).

This makes the frame extension explicit at the amendment site, parallel to the frames stated at the K.λ definition (`(A d' :: M'(d') = M(d'))` among the components K.λ holds in frame) and the K.μ⁺_L definition (`L' = L` among its frame clauses). The line in the Link store section above — "All existing elementary transitions from ASN-0047 hold L in their frame: L' = L" — states this fact informally; the listing here records the formal frame for each operator and supports the ExtendedReachableStateInvariants proof's appeals to L-frame preservation. L12 (LinkImmutability) is the direct consequence: dom(L) ⊆ dom(L') with values fixed at every existing entry, satisfied trivially when L' = L.

**K.α amendment (ContentSubspaceRestriction).** In the extended state, K.α is amended with a content-subspace restriction: the allocated address must satisfy `fields(a).E₁ = s_C`. This parallels K.λ's `fields(ℓ).E₁ = s_L` and is required by L0 clause 2 — without it, K.α could allocate an address with subspace s_L, placing it in dom(C') and violating the partition. The amendment also preserves L14: since `fields(a).E₁ = s_C` and `s_C ≠ s_L` (SC-NEQ), the address `a` cannot appear in dom(L) — L0 clause 1 at the pre-state ensures all dom(L) addresses have subspace s_L — so `dom(C') ∩ dom(L') = ∅`.

**K.μ⁺ amendment (ContentSubspaceRestriction).** K.μ⁺ is amended with a content-subspace restriction: new V-positions must satisfy `subspace(v) = s_C`. This complements K.μ⁺_L (defined below), which handles link-subspace extensions exclusively. The restriction is necessary — without it, K.μ⁺ could create a link-subspace V-position mapping to dom(C), violating S3★. With this amendment, the two transitions partition arrangement extensions by subspace. The existing D-CTG and D-MIN postconditions carry forward, now complemented by K.μ⁺_L's parallel contiguity and minimum-position preconditions in the link subspace.

**L14a amendment (NonTranscludability superseded in the extended state).** ASN-0043 establishes L14a (NonTranscludability) as a per-state invariant of the four-component model: `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∉ dom(Σ.L))` — no V-position maps to a link address. This ASN's extended state admits K.μ⁺_L (defined below), which places `(v_ℓ, ℓ)` in M(d) with `ℓ ∈ dom(L)`, directly contradicting L14a's range exclusion. We supersede L14a in the extended state by the joint pair S3★ + CL-OWN. S3★'s link clause (`subspace(v) = s_L ⟹ M(d)(v) ∈ dom(L)`) permits link-subspace V-positions to target dom(L), inverting L14a's range exclusion. CL-OWN (`origin(M(d)(v)) = d` for v in d's link subspace) restricts those targets to the document's own links. Together they preserve L14a's *architectural intent* — that link identity is not transcludable, no document arranges a foreign link — while admitting the home-document arrangement that the four-component model could not express because it had no link subspace to arrange links in. The K.μ⁺_L precondition `origin(ℓ) = d` is the operative mechanism that enforces CL-OWN at every K.μ⁺_L event; subsequent transitions hold M's link subspace fixed (per K.μ~'s link-subspace identity clause and K.μ⁻'s admissible-suffix discipline), so CL-OWN is preserved inductively. ASN-0043's L14a remains authoritative within the four-component scope — where the link-subspace branch of the present ASN's V-position structure does not yet exist, and `Σ.M(d)(v) ∉ dom(Σ.L)` holds vacuously by S3 (every V-position targets dom(C)) combined with L14 — and this ASN's S3★ + CL-OWN is the local replacement, not a retroactive modification of ASN-0043. Downstream uses in this ASN appeal to S3★ + CL-OWN; no further reference to L14a is invoked.

**D-CTG★ / D-MIN★ (per-subspace scope, local strengthening of ASN-0036).** ASN-0036's D-CTG (Frame: "The link subspace V_2(d) is exempt — sparse with tombstones is permitted") and D-MIN (Frame: "gaps below the minimum, e.g., from tombstoning, are admissible") are stated for the text subspace V_1(d) with explicit link-subspace exemptions. This ASN introduces locally strengthened forms — D-CTG★ and D-MIN★ — that drop the link-subspace exemption clauses, applying contiguity and minimum-position uniformly across both subspaces. The star-superscripted forms are new properties of this ASN's extended state; ASN-0036's D-CTG and D-MIN remain authoritative in their original scope (the four-component model with only the text subspace), and this ASN's strengthening operates as a local extension applicable to the extended state's per-subspace structure, not as a retroactive modification of ASN-0036. The strengthening trades ASN-0036's tombstoning provision for uniform structural simplicity across subspaces:

  **D-CTG★ (per-subspace contiguity).** `(A d, S : V_S(d) ≠ ∅ : V_S(d) is contiguous under the V-ordering on subspace S)`, where *contiguous* unpacks as closed-interval membership: for every `v_lo, v_hi ∈ V_S(d)` and every depth-m_S positive tuple `z` with subspace identifier S and `v_lo ≤ z ≤ v_hi` under the V-ordering, `z ∈ V_S(d)`. The closed-interval formulation is the operative content of D-CTG★ in the derivations below — appeals to D-CTG★ discharge to "every depth-m_S positive tuple lex-between two named members of V_S(d) is itself in V_S(d)" without further unpacking.

  **D-MIN★ (per-subspace minimum position).** `(A d, S : V_S(d) ≠ ∅ : min(V_S(d)) = [S, 1, ..., 1] of depth m_S)`

The amendment trades ASN-0036's link-subspace tombstoning provision for uniform structural simplicity across subspaces. Tombstoning — the "not currently addressable" status Nelson describes for withdrawn links (LM 4/9) — is reserved for the open withdrawal mechanism (see Open Questions); until that mechanism is specified, link-subspace contractions are suffix truncations satisfying D-CTG★ and D-MIN★. All subsequent references to D-CTG and D-MIN in this ASN denote the amended (per-subspace) forms D-CTG★ and D-MIN★ — including the K.μ⁺, K.μ⁻, K.μ⁺_L, and K.μ~ postconditions and the per-subspace arrangement invariants below.

  **V-ordering on subspace S (definition).** *Anchoring the "V-ordering" language used by D-CTG★, D-MIN★, and D-SEQ★ below; by the K.μ⁻ admissibility case analysis above (which speaks of "lex order on terminal-varying tuples" — a special case under this definition); by the K.μ~-FIX domain-fixity argument; and by the link-subspace fixity proof.* The *V-ordering on subspace S* is the restriction of T1 (LexicographicOrder, ASN-0034) to the depth-m_S positive-component tuples whose first component is S — equivalently, the standard lexicographic order on ℕ⁺-valued tuples of length m_S, scoped to the slice with `v_1 = S`. (The depth m_S is the common depth of V_S(d) under S8-depth on each non-empty subspace; on an empty subspace the V-ordering's domain is empty, consistent with the vacuous form of the per-subspace clauses at empty subspaces.) The minimum `[S, 1, ..., 1]` of depth m_S cited by D-MIN★, the closed-interval/contiguity content cited by D-CTG★, and the "v_min < u_M < v" lex-comparison steps in the D-SEQ★ derivation below are all formulated under this restricted order. Every subsequent appeal to "the V-ordering" — at any depth and either subspace — discharges through this definition.

*Consequence for link withdrawal.* The strengthening has a sharp pragmatic consequence: under D-CTG★, a user cannot withdraw a single link at a non-maximum link-subspace position while leaving subsequent links in place. K.μ⁻'s D-CTG★/D-MIN★ postconditions admit only suffix truncations within each subspace, so withdrawing one interior link requires withdrawing every link allocated after it as well. Under the unamended D-CTG of ASN-0036 (which exempts the link subspace), single-link withdrawal at any position would have been admissible, with the gap representing the withdrawn link's "tombstone." The amended forms forbid that gap, and Nelson's tombstoning design — under which a withdrawn link transitions to "not currently addressable" status while retaining its position and permanent serial address (LM 4/9) — is therefore not expressible as a K.μ⁻ contraction in the present ASN. The consultation responses confirm tombstoning as essentially the only model Nelson contemplates for link withdrawal; reconciling that design with D-CTG★ requires a separate withdrawal mechanism (status flag, tombstone marker, or explicit retraction link) that operates outside K.μ⁻'s presentational-removal contract. The precise mechanism is deferred to the open question on withdrawal invariants below; this paragraph flags only that the amended D-CTG★ alone does not provide it.

**D-SEQ★ (per-subspace sequential positions, derived).** For each non-empty subspace S in M(d):

  `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` for some `n_S ≥ 1`,

where the inner positions are of uniform depth m_S (the common depth within subspace S, by S8-depth), and `n_S = |V_S(d)|`.

D-SEQ★ is the per-state invariant stated in *Per-state arrangement shape (D-SEQ★)* in the Elementary transitions section above (as a pointer ahead of K.μ⁻'s use of the shape) and re-established in full detail here from the amended D-CTG★ + D-MIN★ + S8-depth + S8-fin + S8a. The derivation cannot move upstream because it consumes D-CTG★ and D-MIN★, both introduced in this Amendments section. The K.μ⁻ case analysis treats the D-SEQ★-shaped pre-state as a structural input assumption discharged by D-SEQ★'s per-state guarantee. Downstream sections (the K.μ~-FIX domain-fixity argument, the link-subspace fixity proof, and the ExtendedReachableStateInvariants induction) also appeal to D-SEQ★ by name.

*Derivation.* Fix d and a non-empty subspace S, and abbreviate `m := m_S`, `n := n_S`. By D-MIN★, V_S(d) contains the minimum position `v_min = [S, 1, ..., 1]` of depth m. By S8-depth, every v ∈ V_S(d) has #v = m. By S8a, every component of every v ∈ V_S(d) is strictly positive (in ℕ⁺). By S8-fin, V_S(d) is finite; let n := |V_S(d)|. The V-ordering on a fixed subspace at a fixed depth is the standard lexicographic order on ℕ⁺-valued tuples; we show that under this ordering, D-CTG★ + S8-fin force every element of V_S(d) into the all-1-inner form `[S, 1, ..., 1, k]`.

*Step 1: inner positions are fixed at 1.* We show that every v ∈ V_S(d) satisfies `v_j = 1` for `2 ≤ j ≤ m - 1` (when m = 2 there are no inner positions and the claim is vacuous).

Suppose for contradiction that some v ∈ V_S(d) has v_j ≥ 2 at the *minimal* inner position j with `2 ≤ j ≤ m - 1`. By minimality, `v_l = 1` for `2 ≤ l < j`; combined with v_1 = S, v agrees with v_min on positions 1..j - 1, and `v_j > v_min[j] = 1`, so `v_min < v` in lex order. For each integer `M ≥ 2`, define the depth-m tuple
  `u_M := [S, 1, ..., 1, 1, M, 1, ..., 1]`
with `S` at position 1, `1` at every position from 2 through j, `M` at position j + 1, and `1` at every remaining position from j + 2 through m. (When j = m - 1, the trailing range j + 2..m is empty; the tuple becomes `[S, 1, ..., 1, 1, M]` with M at the terminal.) Each u_M has all positive components, so it inhabits the V-ordering's domain at depth m.

We verify `v_min < u_M < v` for each M ≥ 2:
  - `v_min < u_M`: v_min and u_M agree on positions 1..j (both have `S` at 1 and `1` everywhere through position j); they first differ at position j + 1, where `v_min[j+1] = 1 < M = u_M[j+1]`.
  - `u_M < v`: u_M and v agree on positions 1..j - 1 (both have `S` at 1 and `1` at positions 2..j - 1); they first differ at position j, where `u_M[j] = 1 < v_j` (since v_j ≥ 2 by hypothesis).
By D-CTG★'s closed-interval-membership content, every depth-m positive tuple z with subspace identifier S satisfying `v_min ≤ z ≤ v` lies in V_S(d) (v_min and v are both in V_S(d), so they bracket a closed interval admissible to the D-CTG★ premise). Each u_M satisfies `v_min < u_M < v` and is a depth-m positive tuple with subspace identifier S, hence u_M ∈ V_S(d) for each M ≥ 2; i.e., `{u_M : M ∈ ℕ⁺ ∧ M ≥ 2} ⊆ V_S(d)`. These u_M are pairwise distinct (they differ at position j + 1), giving an infinite subset of V_S(d), which contradicts `|V_S(d)| = n < ∞` (S8-fin).

Therefore no v ∈ V_S(d) has an inner position ≥ 2: every v has `v_j = 1` for `2 ≤ j ≤ m - 1`, and the only remaining freedom is in the terminal position v_m. So every v ∈ V_S(d) has the form `[S, 1, ..., 1, k]` for some `k ∈ ℕ⁺`.

*Step 2: terminal contiguity.* Restricted to terminal-varying tuples `[S, 1, ..., 1, k]`, the V-ordering coincides with the natural order on `k`. By S8-fin, n < ∞; let `v_max = max(V_S(d)) = [S, 1, ..., 1, k_max]` for some k_max ∈ ℕ⁺ (well-defined since V_S(d) is finite and non-empty). By D-CTG★'s closed-interval-membership content, every depth-m positive tuple z with subspace identifier S satisfying `v_min ≤ z ≤ v_max` is in V_S(d) (v_min and v_max are both in V_S(d), bracketing a closed interval admissible to the D-CTG★ premise); restricted to terminal-varying tuples `[S, 1, ..., 1, k]`, this gives `{[S, 1, ..., 1, k] : 1 ≤ k ≤ k_max} ⊆ V_S(d)`. The reverse inclusion follows from v_max being the maximum: any `[S, 1, ..., 1, k]` with `k > k_max` would exceed v_max in lex order. Hence `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ k_max}`, and counting gives `k_max = n`.

The infinite-cardinality contradiction in Step 1 supplies, for an arbitrary subspace S, the per-subspace analogue of the D-CTG-depth property that ASN-0036 states specifically for the text subspace V_1(d). Here it is derived directly from D-CTG★ + S8-fin + S8a, so D-SEQ★ does not require a separate D-CTG-depth axiom for non-text subspaces. ∎

This per-subspace D-SEQ★ underwrites all subsequent appeals to a "V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}" structure in this ASN — including the K.μ⁻ amendment, the K.μ~-FIX domain-fixity argument, the link-subspace fixity proof, and the ExtendedReachableStateInvariants induction.

**K.μ⁻ amendment (PerSubspaceContiguity).** K.μ⁻'s D-CTG and D-MIN postconditions extend naturally to the two-subspace case under the per-subspace amendment above: contraction must satisfy D-CTG★ and D-MIN★ for each subspace independently. The structural consequence is unchanged from the pre-extension analysis — D-SEQ★ (derived above for the extended state) gives, at the input state, V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n} for each non-empty subspace, which is the per-state guarantee that the K.μ⁻ case analysis cites by name and which — combined with the D-CTG★/D-MIN★ postconditions — implicitly constrains valid contractions to removal from the maximum end or removal of all positions within each subspace.

**Consequence for J4 (Fork, ASN-0047).** Since J4's K.μ⁺ step is now restricted to content-subspace V-positions, forking a document populates only the content subspace of the new document. Link-subspace mappings from the source document are not copied — the forked document's link subspace starts empty. The K.μ⁺ amendment also requires strengthening J4's precondition from `M(d_src) ≠ ∅` to `V_{s_C}(d_src) ≠ ∅`: K.μ⁺ can only transclude I-addresses in dom(C), and only content-subspace V-positions in d_src map to dom(C). J4 remains a valid composite under the amended coupling constraints. J1★ is satisfied because J4's K.μ⁺ creates only content-subspace V-positions (by the amendment) and J4's K.ρ records provenance for each `a ∈ ran(M'(d_new))`, covering every content-subspace extension. J1'★ is satisfied because each new `(a, d_new) ∈ R' \ R` has `a ∈ ran(M'(d_new))` from content-subspace extensions — J4's K.μ⁺ step creates only content-subspace V-positions (by the K.μ⁺ amendment), and S3★'s content clause gives `M'(d_new)(v) ∈ dom(C)` for each such `v`, so `ran(M'(d_new)) ⊆ dom(C)` and P7 compatibility is maintained. D-CTG and D-MIN are satisfied: J4's K.μ⁺ step operates on a freshly created document (M(d_new) = ∅ after K.δ), constructing the entire content-subspace arrangement; by choosing V-positions contiguously from the minimum [s_C, 1, ..., 1], D-CTG and D-MIN hold for the content subspace, and the link subspace of d_new is empty (J4's K.μ⁺ is content-subspace-only by the amendment), so D-CTG and D-MIN hold vacuously for it. This is consistent with Nelson's design: each document owns only its home links, and links from the source remain discoverable through the shared I-addresses via refractive following — "a link to one version of a Prismatic Document is a link to all versions" (Nelson). A mechanism for link inheritance under forking, if desired, would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope.


## Allocator hierarchy under documents

The content- and link-subspace allocators are organized as sibling element-field sub-allocators rooted at each document. We formalize this structure to underwrite the K.λ first-link case's allocation discipline and to make uniqueness precise for the multi-subspace state.

For each `d ∈ E_doc`, the document-level address `d` (zeros = 2) is the root of d's allocator subtree. Two element-field bases sit immediately under d:

- `b_C(d) := [d.0.s_C]` (single-component element field with E₁ = s_C; zeros = 3, #E = 1) — the **content sub-allocator anchor**.
- `b_L(d) := [d.0.s_L]` (single-component element field with E₁ = s_L; zeros = 3, #E = 1) — the **link sub-allocator anchor**.

These anchors are *structurally producible* via T10a inc steps from `d` itself: under the canonical subspace convention `s_C = 1`, `s_L = 2` (Nelson's "subspaces by position-digit reservation" at LM 4/30–4/31; Gregory's `TEXTATOM=1`/`LINKATOM=2` atomtype-prefix encoding at `xanadu.h:144`), `b_C(d) = inc(d, 2)` (TA5(d) with k = 2 — a descent step appending `.0.1` to `d`, where the new zero separator and the terminal `1 = s_C` together identify the content-subspace element-field anchor), and `b_L(d) = inc(b_C(d), 0)` (TA5(c) — a same-level sibling step from `b_C(d)`, advancing the terminal from `1 = s_C` to `2 = s_L`). The two-step chain `d → inc(d, 2) = b_C(d) → inc(b_C(d), 0) = b_L(d)` exhibits both anchors as inc-witnessed extensions of `d` under T10a's per-step structural admissibility. The anchors are *not* themselves in `dom(C) ∪ dom(L)` — content addresses have `#E ≥ 2` by S7c; link addresses have `#E ≥ 2` by L1b; the anchors have `#E = 1` — so structural producibility places them in T10a's tumbler universe `T` but not in any state component of Σ.

What the inc derivations do *not* supply is the *operational* claim that these structural addresses serve as named entry points for two distinct, simultaneously-active sub-allocator frontiers under `d`, each with its own namespace property at first emission. T10a (ASN-0034) governs sequential allocation *within* a single ownership domain by inc-extension; its at-most-once spawning constraint admits the structural inc-chain above but forbids a single operational allocator rooted at `d` from minting `b_C(d)` and `b_L(d)` as two distinct forward-frontier roots via one spawning event. The sub-allocator frontiers must therefore be admitted by a separate axiom — **SubAllocatorAxiom** below — which packages the *operational* claim: sub-allocator existence under `d`, cross-subspace disjointness, and the namespace property at each first emission (`a ∉ dom(C)`, `ℓ ∉ dom(L) ∪ dom(C)`). (The anchors are inc-reachable from `d` as exhibited above, but operationally lie outside T10a's per-owner forward-frontier tree at `d`; consultation-54 confirms that the content and link sub-allocators are siblings-by-convention under each document, structurally inc-witnessed at document-creation time rather than minted by a sequence of separate operational spawning events.) This is the same pattern as NodeUniqueAllocation: T10a's inc discipline does not by itself underwrite node baptism either, and a separate axiom supplies the operational uniqueness premise. Once each anchor is established as a forward frontier, the sub-allocator it heads is *itself* a T10a-conforming allocator: subsequent allocations within that frontier are inc(·, 0) sibling steps and inherit T10a's machinery in full. So T10a applies to *each* sub-allocator independently from its first inc-produced output onward, and SubAllocatorAxiom supplies only the bootstrap — the namespace property at the first emission — that T10a cannot itself produce from `d` alone. Successive allocations advance each anchor's frontier:

- *Content sub-allocator:* the first content address under d is `[d.0.s_C.1]`; subsequent siblings are `[d.0.s_C.k+1] = inc([d.0.s_C.k], 0)` (TA5(c)).
- *Link sub-allocator:* the first link address under d is `[d.0.s_L.1]`; subsequent siblings advance by `inc(ℓ_prev, 0)` over the link frontier.

The two sub-allocators share the prefix `[d.0]` and differ only in the first element-field component — they are siblings in the tumbler-algebra sense (their addresses sit at the same depth under `d.0`, distinguished by their first element-field component s_C vs s_L). They are *not* "sibling allocators in T10a's tree" in the spawning-event sense — T10a's at-most-once constraint precludes a single spawning event yielding both. Their disjointness and existence are axiomatized separately (SubAllocatorAxiom below), not derived from T10a's spawning discipline. Their frontiers advance independently: content allocation does not perturb the link sub-allocator's state and vice versa, because each inc step operates locally on the receiving allocator's own frontier under its subspace prefix.

**SubAllocatorAxiom (Axiom, ContentLinkSubAllocatorExistence).** For each `d ∈ E_doc`, the entity-allocation event that places d into E_doc simultaneously establishes two distinct sub-allocators under d: a content sub-allocator with anchor `b_C(d) = [d.0.s_C]` and a link sub-allocator with anchor `b_L(d) = [d.0.s_L]`. The two sub-allocators are disjoint (each addresses tumblers in its own subspace exclusively), and each provides a forward-allocation frontier producing addresses that satisfy a namespace property:

  *Content sub-allocator namespace property:* every address `a` produced by d's content sub-allocator satisfies `a ∉ dom(Σ.C)` at the state of allocation and has `fields(a).E₁ = s_C`, `origin(a) = d`, `#E(a) ≥ 2`.

  *Link sub-allocator namespace property:* every address `ℓ` produced by d's link sub-allocator satisfies `ℓ ∉ dom(Σ.L) ∪ dom(Σ.C)` at the state of allocation and has `fields(ℓ).E₁ = s_L`, `origin(ℓ) = d`, `#E(ℓ) ≥ 2`.

This is an axiom of this ASN. T10a (ASN-0034) governs inc-produced addresses within a *single* ownership domain — its at-most-once spawning constraint forbids a single allocator (the document `d`) from emitting two distinct sub-allocators via one inc operation. The two sub-subspaces must therefore be admitted by separate construction: the design intent (Nelson, LM 4/30–4/31, who reserves subspaces "1" and "2" by position-digit convention under each document, with link subspace "established by convention at document creation, not by a separate FEBE operation") and the implementation (udanax-green, whose first link VSA `2.1` is a hardcoded constant from `findnextlinkvsa` (do2.c:151–167), not derived from the document's own ISA) both treat the two sub-allocators as established structurally at document creation time, with their namespace property — `a ∉ dom(C)` and `ℓ ∉ dom(L)`, respectively, at every allocation event — being the operative premise that closes the uniqueness chain for K.α and K.λ. SubAllocatorAxiom stands alongside SC-NEQ (this ASN), NodeUniqueAllocation (this ASN), NoDeallocation (ASN-0034), and S0 (ASN-0036) as a load-bearing axiomatic premise.

*Relationship to T10a's allocator tree.* The sub-allocator anchors are structurally inc-reachable from `d` via the chain `d → inc(d, 2) = b_C(d) → inc(b_C(d), 0) = b_L(d)` exhibited above, but operationally lie outside T10a's per-owner forward-frontier tree rooted at `d`: T10a's at-most-once spawning constraint forbids a single operational allocator at `d` from minting `b_C(d)` and `b_L(d)` as two distinct forward-frontier roots via one spawning event. The anchors are not in any operational T10a frontier rooted directly at `d` as a forward-allocation source — they are admitted by SubAllocatorAxiom as named entry points fixed by document-creation convention, with the structural inc-chain above serving simultaneously as the producibility witness that L1c (ASN-0043) requires for downstream link addresses. Three properties of T10a remain in force downstream:
- *Within-frontier uniqueness.* Once an anchor has emitted its first address (by the axiom's namespace property), subsequent allocations within that sub-allocator's frontier are `inc(·, 0)` sibling steps. Each such frontier is itself a T10a-conforming chain rooted at its first inc-produced output, and T10a's GlobalUniqueness applies to it: every subsequent emission is distinct from every prior emission within the same frontier.
- *Cross-document disjointness.* Stated once as the **Cross-document disjointness chain (Lemma)** below, instantiated at the document level (operating on `d₁, d₂` themselves, which are T10a-allocated under their owning accounts by S7d, ASN-0036), not directly on sub-allocator anchors.
- *Cross-subspace disjointness within a single document.* Provided by the axiom's disjointness clause (the content and link sub-allocators address disjoint tumbler subspaces under `d`), and reinforced downstream by L14 + SC-NEQ + T7. T10a is not invoked here, since the two sub-allocators are not co-located in a single T10a allocator's tree under `d`.

Without SubAllocatorAxiom, K.λ's first-link precondition `ℓ ∉ dom(L) ∪ dom(C)` would have no underwriter — T10a alone cannot supply it for the first-link case, since `b_L(d)` is not in any allocator's domain and the first link emitted from d's link frontier cannot be derived as `inc(t, k)` from a previously inc-produced t within a single ownership domain. The same gap exists for K.α's first content address under a fresh document. SubAllocatorAxiom underwrites both. For subsequent allocations within a single sub-allocator's frontier (`inc(prev, 0)` sibling steps), T10a's GlobalUniqueness *does* apply — once the sub-allocator's frontier has at least one inc-produced address, subsequent siblings are inc-conforming and inherit T10a's uniqueness guarantee within that frontier. Cross-frontier disjointness (content vs. link within the same document) is provided by the axiom's disjointness clause. Cross-document disjointness follows by the labeled lemma below.

*Reconciliation with ASN-0043's L1c.* ASN-0043's L1c (LinkAllocatorConformance) requires, for every `ℓ ∈ dom(Σ.L)`, the existence of a T10a-conforming chain `s = t₀ → t₁ → ... → tₙ = ℓ` with `s` a T4-valid document-level seed (`zeros(s) = 2`), `k₁ = 2`, and each subsequent `kᵢ ∈ {0, 1, 2}`. For a first-emit link `ℓ = [d.0.s_L.1]` with `s_L = 2`, the witnessing chain is `t₀ = d`, `t₁ = inc(d, 2) = [d.0.1]`, `t₂ = inc(t₁, 0) = [d.0.2]`, `t₃ = inc(t₂, 1) = [d.0.2.1] = ℓ` — a length-3 chain whose intermediates `[d.0.1]` and `[d.0.2]` are structurally valid tumblers under T10a's per-step admissibility but are *not in any state component of Σ* (not in `dom(C)`, not in `dom(L)`, not in `E`). L1c is explicit (ASN-0043, line 102) that it is "a structural producibility statement about each address presently in `dom(Σ.L)`, not a log of past allocator firings" — the chain is required to exist *structurally* (as a sequence of T10a-admissible inc steps), not to record any actual operational allocator event at each intermediate. SubAllocatorAxiom is therefore consistent with L1c under the following reading: the axiom abstracts over the L1c chain by treating `b_L(d) = [d.0.s_L]` as a *named entry point* (the structural witness for the chain prefix `s → inc(s,2) → ... → b_L(d)`) and the first-emit address `[d.0.s_L.1] = inc(b_L(d), 1)` as the chain's terminus. The intermediates `[d.0.1], [d.0.2]` traversed by the s_L = 2 chain are L1c's structural witnesses, not allocated state; SubAllocatorAxiom's phrase "outside T10a's per-owner inc tree rooted at `d`" refers to the *operational* tree — the sub-allocators are not spawned by an operational inc event at `d` (per T10a's at-most-once spawning constraint) — and does not deny the structural producibility chain that L1c's existential requires. The two are compatible: L1c is discharged by exhibiting the inc-chain structurally; SubAllocatorAxiom packages the same chain as a named entry point and adds the namespace property (`ℓ ∉ dom(L) ∪ dom(C)` at the state of allocation), which L1c alone does not supply. The disjointness clause of SubAllocatorAxiom and the chain-existential of L1c are independent — disjointness is a cross-subspace/cross-document state-level claim, producibility is a per-address structural claim — and the present ASN's K.λ first-link precondition cites both: SubAllocatorAxiom for `ℓ ∉ dom(L) ∪ dom(C)`, and L1c (implicitly, through the structural chain SubAllocatorAxiom abstracts over) for producibility from `d`.

**Cross-document disjointness chain (Lemma; T10a.{2,5} → T10).** For any two distinct documents `d₁, d₂ ∈ E_doc` with `d₁ ≠ d₂`, the link sub-allocator anchors `p₁ := b_L(d₁) = [d₁.0.s_L]` and `p₂ := b_L(d₂) = [d₂.0.s_L]` satisfy `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`, so by T10 (PartitionIndependence, ASN-0034) every address extending `p₁` differs from every address extending `p₂`. The same lemma holds with `b_C` in place of `b_L` for content allocations.

*Proof.* By S7d (ASN-0036) every document is produced by a T10a-conforming allocation event under its owning account, so `d₁` and `d₂` are outputs of T10a-conforming allocators. The prefix-incomparability `d₁ ⋠ d₂ ∧ d₂ ⋠ d₁` splits by parent-account relationship. *Same-account sibling case:* `d₁` and `d₂` share a parent account `a` and are siblings produced by `a`'s document sub-allocator (a T10a-conforming inc(·, 0) frontier rooted at `inc(a, 2) = [a.0.1]`); T10a.2 (NonNestingSiblingPrefixes, ASN-0034) directly gives `d₁ ⋠ d₂ ∧ d₂ ⋠ d₁` as distinct sibling outputs of the same allocator (T10a.1 supplies uniform sibling length and T3 supplies divergence-by-position). *Different-account case:* `d₁` and `d₂` are emitted by document sub-allocators rooted under different parent accounts; these two allocators are not in an ancestor-descendant relationship in T10a's allocator tree (the two account-chains back to the bootstrap root diverge at their most recent common account ancestor, so neither document-sub-allocator inhabits the other's lineage), and T10a.5 (CrossAllocatorIncomparability, ASN-0034) then gives prefix-incomparability of outputs across non-lineage allocator pairs. T10a.6 (DomainDisjointness, ASN-0034) packages both cases as the higher-level theorem — domain disjointness of distinct allocators, equivalent under reflexivity of `≼` (`t ≼ t`) to no shared output across the two domains — but the load-bearing sub-claims for the prefix-incomparability premise of T10 are T10a.2 for the sibling case and T10a.5 for the non-sibling case; T10a.6 stands as the packaging citation rather than the operative one. Prefix-incomparability is preserved under suffix extension. By Prefix (ASN-0034) — `t₁ ≼ t₂ ⟺ #t₁ ≤ #t₂ ∧ (A k : 1 ≤ k ≤ #t₁ : t₁[k] = t₂[k])` — the negation `t₁ ⋠ t₂` decomposes into either a length disparity (`#t₁ > #t₂`) or a position divergence (some `k ≤ min(#t₁, #t₂)` with `t₁[k] ≠ t₂[k]`). Length disparity alone is asymmetric — the shorter tuple is a prefix of the longer when their shared positions agree — so the joint conjunction `d₁ ⋠ d₂ ∧ d₂ ⋠ d₁` forces a position divergence: there exists `k ≤ min(#d₁, #d₂)` with `d₁[k] ≠ d₂[k]`. The anchors are length-2 suffix extensions: `p_i = [d_i.0.s_L]` with `#p_i = #d_i + 2` and `p_i[j] = d_i[j]` for `1 ≤ j ≤ #d_i`. The same index `k ≤ min(#d₁, #d₂) ≤ min(#p₁, #p₂)` then satisfies `p₁[k] = d₁[k] ≠ d₂[k] = p₂[k]`, witnessing both `p₁ ⋠ p₂` and `p₂ ⋠ p₁` via the position-divergence clause of Prefix. T10 (PartitionIndependence, ASN-0034) now applies: for any `a, b ∈ T` with `p₁ ≼ a` and `p₂ ≼ b`, we have `a ≠ b`. Every address emitted by d₁'s link sub-allocator extends `p₁ = b_L(d₁)` (`b_L(d₁) ≼ [d₁.0.s_L.k]` for every k ≥ 1 by Prefix), and every address emitted by d₂'s link sub-allocator extends `p₂ = b_L(d₂)`. Therefore no link address allocated under d₁ can coincide with any link address allocated under d₂. The same proof, with `b_C(d₁), b_C(d₂)` in place of `b_L(d₁), b_L(d₂)`, gives cross-document disjointness for content allocations. ∎

Cross-subspace collisions are further prevented by L14 (StoreDisjointness), itself derived from L0 and SC-NEQ via T7 (SubspaceDisjointness, ASN-0034): every content address has `fields(a).E₁ = s_C`, every link address has `fields(ℓ).E₁ = s_L`, and `s_C ≠ s_L`, so no allocation in one subspace can produce an address inhabiting the other.


## Link allocation

**K.λ (LinkAllocation).** Creates a new entry in the link store.

*Precondition:*
- d ∈ E_doc  (home document exists)
- ℓ ∉ dom(L) ∪ dom(C)  (fresh address — L14)
- zeros(ℓ) = 3 ∧ fields(ℓ).E₁ = s_L  (element-level, link subspace — L0, L1)
- #E(ℓ) ≥ 2  (link element field has at least two components — L1b, ASN-0043; established by the inc(t, 1) descent in the first-link case and preserved by the inc(t, 0) sibling step in subsequent cases)
- origin(ℓ) = d  (scoped to home document — L1a)
- ℓ is produced by d's link sub-allocator (established by SubAllocatorAxiom above), with the production rule depending on the case:
  - *First link case.* If `V_{s_L}(d) = ∅` and `dom(L) ∩ {a : origin(a) = d} = ∅` (no link yet allocated under d), the link sub-allocator emits `ℓ = [d.0.s_L.1]` — the first address on d's link frontier, with `#E(ℓ) = 2` and `fields(ℓ).E₁ = s_L`. SubAllocatorAxiom's link namespace property gives `ℓ ∉ dom(L) ∪ dom(C)` directly; no inc derivation from a previously allocated `t` is invoked, because the axiom underwrites the first allocation by structural construction rather than by T10a's per-owner inc discipline. (T10a cannot supply this guarantee in the first-link case: `b_L(d)` is a virtual anchor with no inc-history, and the document `d` cannot spawn two sibling sub-allocators by a single inc(d, 2) operation under T10a's at-most-once constraint.)
  - *Subsequent link case.* If `V_{s_L}(d) ≠ ∅` or `dom(L) ∩ {a : origin(a) = d} ≠ ∅`, set t = max{ℓ' ∈ dom(L) : origin(ℓ') = d} and ℓ = inc(t, 0) (TA5(c)) — the next sibling on d's link frontier at the same depth. This is a T10a-conforming inc step within the link sub-allocator's frontier once the frontier has at least one inc-produced address, so T10a's GlobalUniqueness gives `ℓ ∉ dom(L)` and SubAllocatorAxiom's disjointness gives `ℓ ∉ dom(C)`.
- `(A ℓ' : ℓ' ∈ dom(L) ∧ origin(ℓ') = d : ℓ' < ℓ)`  (forward allocation — T9; consequence of inc(·, 0) on the frontier in the subsequent case, and of the first-emit position [d.0.s_L.1] being greater than any pre-existing d-scoped link in the first-link case, where the antecedent is vacuous)
- (F, G, Θ) ∈ Link ∧ Θ ≠ ∅  (well-formed link value with mandatory non-empty type endset — L3)

*Effect:* `L' = L ∪ {ℓ ↦ (F, G, Θ)}`

*Frame:* `C' = C; E' = E; (A d' :: M'(d') = M(d')); R' = R`

The address ℓ is produced by d's link sub-allocator. In the first-link case the axiom (SubAllocatorAxiom) supplies `ℓ = [d.0.s_L.1]` with the namespace property `ℓ ∉ dom(L) ∪ dom(C)`; in the subsequent case `ℓ = inc(prev, 0)` is a T10a-conforming inc step within the sub-allocator's frontier, with GlobalUniqueness giving `ℓ ∉ dom(L)` and the axiom's disjointness giving `ℓ ∉ dom(C)`. The structural requirement closes the uniqueness chain across both cases: the axiom underwrites the first emission, and T10a underwrites every subsequent emission. By T7 (SubspaceDisjointness, ASN-0034) and SC-NEQ, the link subspace s_L is disjoint from the content subspace s_C, so ℓ cannot collide with any content address. Cross-document disjointness — that `ℓ` cannot collide with any link address allocated under a different document `d' ≠ d` — is supplied by the **Cross-document disjointness chain (Lemma; T10a.{2,5} → T10)** stated and proved in the *Allocator hierarchy under documents* section above, applied with `p₁ := b_L(d)` and `p₂ := b_L(d')`: since `ℓ` extends `b_L(d)` and every link address allocated under `d'` extends `b_L(d')`, the lemma yields `ℓ` distinct from every such address.


## Generalized referential integrity

**S3★ (GeneralizedReferentialIntegrity).** The arrangement maps V-positions to addresses in the store appropriate to their subspace:

  `(A d, v : v ∈ dom(Σ.M(d)) : (subspace(v) = s_C ⟹ Σ.M(d)(v) ∈ dom(Σ.C)) ∧ (subspace(v) = s_L ⟹ Σ.M(d)(v) ∈ dom(Σ.L)))`

where `subspace(v)` denotes the first component of the V-position. S3★ supersedes S3 (ASN-0036) for the extended state Σ = (C, L, E, M, R): S3 requires every V-position to map into dom(C), which is violated by link-subspace mappings targeting dom(L). S3 remains valid when restricted to states with no link-subspace mappings — the four-component model of the prior sections has only content-subspace V-positions, for which S3★ reduces to S3.

Existing transitions preserve S3★: K.α, K.δ, K.ρ hold M in frame; K.μ⁺ creates only content-subspace V-positions (by its amended precondition `subspace(v) = s_C`), so new mappings target dom(C) and the link-subspace clause is unaffected; K.μ⁻ contracts dom(M(d)), preserving both clauses; K.μ~ is a distinguished composite K.μ⁻ + K.μ⁺ (per its definition above) with a bijection `π : dom(M(d)) → dom(M'(d))` satisfying `M'(d)(π(v)) = M(d)(v)`. K.μ~ preserves S3★ by direct decomposition: K.μ⁻ restricts dom(M(d)) with values unchanged — content-subspace mappings still target dom(C), link-subspace mappings still target dom(L) — so S3★ holds for the intermediate state; K.μ⁺ (amended) adds only content-subspace V-positions targeting dom(C) by precondition, preserving existing mappings by frame — S3★ holds for M'(d). The stronger derived property — that link-subspace mappings under K.μ~ are pointwise fixed — is established in *Decomposition of K.μ~* below.

**S3★-aux (SubspaceExhaustiveness).** In every reachable state, all V-positions have subspace s_C or s_L:

  `(A d, v : v ∈ dom(M(d)) : subspace(v) = s_C ∨ subspace(v) = s_L)`

*Proof.* By induction on transition sequences from Σ₀. Base: M₀ = ∅, the property holds vacuously. Step: K.μ⁺ (amended) creates only s_C positions; K.μ⁺_L creates only s_L positions; K.μ⁻ removes positions without altering subspaces of survivors; K.μ~ decomposes into K.μ⁻ + K.μ⁺, each maintaining the property independently of fixity; K.α, K.δ, K.λ, K.ρ hold M in frame. ∎


## Link-subspace extension

**K.μ⁺_L (LinkSubspaceExtension).** Extends a document's arrangement in the link subspace.

*Precondition:*
- d ∈ E_doc
- ℓ ∈ dom(L)  (the target link must already exist in dom(L) — placed there by some prior K.λ)
- origin(ℓ) = d  (only home-document links may be arranged)
- ℓ ∉ ran(M(d))  (the link is not already arranged at any V-position in d's arrangement — first-arrangement constraint). This guarantees CL-UNIQ at the post-state: were `ℓ ∈ ran(M(d))` already, there would exist some `v' ∈ dom(M(d))` with `M(d)(v') = ℓ`, and adding `(v_ℓ, ℓ)` with `v_ℓ ∉ dom(M(d))` (verified below) would produce two distinct V-positions both mapping to `ℓ`, violating CL-UNIQ. Combined with CL-OWN (which restricts the link-subspace range of M(d) to links with `origin(·) = d`), the freshness condition `ℓ ∉ ran(M(d))` is equivalent — under the precondition `origin(ℓ) = d` — to `ℓ ∉ ran(M(d)|_{dom_L})`: a link can appear in M(d)'s range only as the value of a link-subspace V-position (by S3★, since `ℓ ∈ dom(L)` and `dom(L) ∩ dom(C) = ∅` by L14), so the unrestricted `ℓ ∉ ran(M(d))` clause suffices.
- V-position v_ℓ satisfies:
  - subspace(v_ℓ) = s_L
  - m_L ≥ 2, where: if V_{s_L}(d) ≠ ∅, m_L is the common depth of existing link-subspace V-positions (determined by S8-depth); if V_{s_L}(d) = ∅, m_L is a parameter of the transition, subject only to m_L ≥ 2. The lower bound is structural: ordinal shift at depth 1 alters the subspace identifier (`shift([s_L], 1) = [s_L + 1]`, violating subspace closure TA7a), so the link subspace requires depth at least 2
  - If V_{s_L}(d) = ∅: v_ℓ is the minimum position `[s_L, 1, ..., 1]` of depth m_L (D-MIN)
  - If V_{s_L}(d) ≠ ∅: v_ℓ = shift(max(V_{s_L}(d)), 1), extending the contiguous range (D-CTG)
  - #v_ℓ = m_L (S8-depth within the link subspace)

  *Shift-lemma applicability for link-subspace v_ℓ.* The shift expression `shift(max(V_{s_L}(d)), 1)` invokes ASN-0036's V-position shift lemmas at a link-subspace V-position; we record the subspace-independence of those lemmas here for completeness. OrdShiftHom (ASN-0036) is stated as an addition homomorphism on positive depth-m tuples sharing first component, with `δ(n, m)` having `v₁`-position zero — its hypothesis is parametric in the first component v₁, so it applies uniformly to v₁ = s_C and v₁ = s_L. Clause (b) of OrdShiftHom — `subspace(shift(v, 1)) = subspace(v)` — therefore gives `subspace(v_ℓ) = subspace(max(V_{s_L}(d))) = s_L`, justifying the subspace(v_ℓ) = s_L precondition above without re-derivation. Clause (c) of OrdShiftHom (ASN-0036) — "when `v` satisfies S8a, `shift(v, n)` satisfies S8a unconditionally" — preserves the all-positive-components property under shift at V-positions directly; it is stated for V-positions (zeros = 0) and is the correct citation for V-position S8a preservation. (ShiftPreservation, the kindred ASN-0036 lemma, is stated for I-addresses `a ∈ dom(Σ.C)` with `zeros = 3` and preserves `zeros(shift(a, k)) = 3`, T4-validity, `#E`, and `subspace_I`; it does *not* address V-position S8a and is not invoked here.) OrdAddS8a (ASN-0036) — preservation of S8-depth (uniform depth) under ordinal addition — is likewise stated parametrically in v₁: its hypothesis quantifies over `(A v : v₁ ≥ 1 ∧ #v = m ∧ ...)` without restricting v₁ to s_C. Both OrdShiftHom (c) and OrdAddS8a therefore apply to v_ℓ = shift(max(V_{s_L}(d)), 1) provided `s_L ≥ 1` and `#max(V_{s_L}(d)) = m_L`; the former is supplied by `fields(ℓ).E₁ = s_L > 0` (T4, ASN-0034, on the link's element-level address; the V-position's first component is the same identifier s_L), and the latter by S8-depth at the pre-state. Hence v_ℓ inherits S8a from max(V_{s_L}(d)) via OrdShiftHom (c) and S8-depth via OrdAddS8a, both subspace-independent.

*Effect:* `M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}`

*Frame:* `C' = C; L' = L; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R`

We verify `v_ℓ ∉ dom(M(d))`, as required for M'(d) to be a proper extension preserving S2 (ArrangementFunctionality). When `V_{s_L}(d) = ∅`: no link-subspace V-position exists in dom(M(d)), and `subspace(v_ℓ) = s_L`, so `v_ℓ ∉ dom(M(d))`. When `V_{s_L}(d) ≠ ∅`: `v_ℓ = shift(max(V_{s_L}(d)), 1) > max(V_{s_L}(d))` by TS4 (ShiftStrictIncrease, ASN-0034), placing v_ℓ beyond all existing link-subspace positions. In both cases, `subspace(v_ℓ) = s_L` and `s_L ≠ s_C` (SC-NEQ) ensures no collision with text-subspace positions (T3, CanonicalRepresentation, ASN-0034: tumblers are extensionally identified by their component sequence, so two tumblers differing in their first component are distinct). T7 (FirstElementFieldDistinction, ASN-0034) does not apply at V-positions because T7's hypothesis is element-level (zeros = 3) while V-positions have zeros = 0; the structural fact required here — that distinct first components yield distinct tumblers — is supplied by T3, which holds at every depth. Therefore `v_ℓ ∉ dom(M(d))`.

The preconditions ensure that after the extension, D-CTG (contiguity), D-MIN (minimum position), and S8-depth (uniform depth) hold for the link subspace of d. S3★ is satisfied: `subspace(v_ℓ) = s_L` and `M'(d)(v_ℓ) = ℓ ∈ dom(L')`.

The origin restriction `origin(ℓ) = d` distinguishes link-subspace extension from content-subspace extension, where K.μ⁺ intentionally permits `origin(a) ≠ d` — that is content transclusion, an established architectural feature. Link transclusion — arranging a foreign-origin link in a document's link subspace — is excluded by design. Nelson: "A document includes only the links of which it is the home document" (LM 4/31). The byte stream admits transclusion ("The virtual byte stream of a document may include bytes from any other document," LM 4/10); links do not. Links maintain "permanent order of arrival" in their home document, and home document determines ownership ("A link need not point anywhere in its home document. Its home document indicates who owns it," LM 4/12). Arranging a link with `origin(ℓ) ≠ d` would place an out-link in a document that does not own it — violating the ownership semantics that home-document identity is meant to carry. The architecture provides alternatives: bidirectional link search discovers all links attached to transcluded content regardless of which document houses them; creating a new link in one's own document is the natural analog of annotation. Gregory confirms that the implementation achieves origin matching by procedural atomicity — `docreatelink` both allocates the link ISA under the document's address and places it in the document's arrangement in a single operation — but no runtime guard exists; `acceptablevsa` unconditionally returns TRUE and `docopy` performs no origin check. The origin restriction in K.μ⁺_L formalizes the structural guarantee that the implementation achieves by construction.

**Per-subspace arrangement invariants under K.μ⁺_L.** S8a (VPositionWellFormedness): the quantifier `(A v ∈ dom(M(d)) : v₁ ≥ 1 : zeros(v) = 0 ∧ v > 0)` covers *all* V-positions with `v₁ ≥ 1`, including link-subspace positions. We must establish that `s_L ≥ 1`: by L1, every link address is element-level (`zeros(ℓ) = 3`), so by T4 (ASN-0034), every element-field component is strictly positive — in particular `fields(ℓ).E₁ = s_L > 0`. Since K.μ⁺_L uses the same identifier s_L for V-positions, link-subspace V-positions have `v₁ = s_L ≥ 1` and fall under S8a's quantifier. For text-subspace positions: unchanged. For the new link-subspace position v_ℓ: K.μ⁺_L places `v_ℓ = [s_L, 1, ..., 1]` (D-MIN) or `shift(max(V_{s_L}(d)), 1)` (D-CTG). In the D-MIN case, v_ℓ = [s_L, 1, ..., 1] has every component strictly positive directly (s_L ≥ 1 by the above; the inner and terminal 1s are positive). In the D-CTG (shift) case, S8a is supplied by OrdShiftHom (c) (ASN-0036) — "when `v` satisfies S8a, `shift(v, n)` satisfies S8a unconditionally" — which preserves the all-positive-components property under shift at V-positions directly (this is the V-position-targeted clause; ShiftPreservation, the I-address `zeros = 3` shift lemma, is not the correct citation for V-position S8a). OrdShiftHom (b) (ASN-0036) gives `subspace(v_ℓ) = subspace(max(V_{s_L}(d))) = s_L`, confirming v_ℓ inhabits the link subspace. In both cases, `zeros(v_ℓ) = 0 ∧ v_ℓ > 0`. S8-fin: adding one position to a finite set preserves finiteness. For the link subspace specifically: S8-depth is satisfied by K.μ⁺_L's precondition (`#v_ℓ = m_L`); in the D-CTG (shift) case this follows from OrdAddS8a (ASN-0036), which preserves uniform depth under ordinal addition uniformly in v₁ — applying it to max(V_{s_L}(d)) (depth m_L) gives `#shift(max(V_{s_L}(d)), 1) = m_L` without re-derivation for the link subspace. D-CTG (VContiguity) and D-MIN (VMinimumPosition) are quantified over *all* subspaces S. For the text subspace (S = s_C): V_{s_C}(d) is unchanged. For the link subspace (S = s_L): K.μ⁺_L's precondition places v_ℓ at the minimum position if V_{s_L}(d) was empty, or at the next contiguous position if non-empty, satisfying both D-CTG and D-MIN. D-SEQ follows from D-CTG, D-MIN, S8-fin, and S8-depth (as derived in ASN-0036). S8 (SpanDecomposition): S8's quantifier `v₁ ≥ 1` captures all V-positions in the extended state — since both `s_C ≥ 1` and `s_L ≥ 1` (established above for S8a) — extending coverage to the link subspace. S8 is derived from S8-fin, S8a, S2, and S8-depth (ASN-0036), all verified above. The new link-subspace mapping `(v_ℓ, ℓ)` either forms a new width-1 correspondence run or extends the last existing link-subspace run by one position if I-adjacent. All existing runs — both text-subspace and link-subspace — are unchanged: K.μ⁺_L preserves existing mappings (frame), and the new position `v_ℓ ∉ dom(M(d))` falls in no existing run, so no existing run is split or modified.


## Link-subspace ownership

**CL-OWN (LinkSubspaceOwnership).** In every reachable state:

  `(A d, v : v ∈ dom(M(d)) ∧ subspace(v) = s_L : origin(M(d)(v)) = d)`

Every document's link-subspace arrangement contains only its own links. This is maintained by two mechanisms: K.μ⁺_L's precondition `origin(ℓ) = d` ensures ownership at creation, and link-subspace fixity under K.μ~ ensures preservation through reordering — no transition can place a foreign-origin link in a document's link subspace.

*Proof.* By induction on transition sequences from Σ₀. Base: M₀(d) = ∅ for all d, so the property holds vacuously. Step: K.μ⁺_L adds `(v_ℓ, ℓ)` with `origin(ℓ) = d` (precondition) and preserves existing mappings (frame); K.μ⁺ (amended) adds only content-subspace positions (`subspace(v) = s_C`), so no link-subspace change; K.μ⁻ removes positions without altering values of survivors; K.μ~ preserves link-subspace mappings identically (link-subspace fixity); K.α, K.δ, K.λ, K.ρ hold M in frame. ∎

**CL-UNIQ (LinkSubspacePositionUniqueness).** Within each document's link-subspace arrangement, each link occupies exactly one V-position — the restriction of M(d) to dom_L is injective:

  `(A d, v₁, v₂ : v₁ ∈ dom(M(d)) ∧ v₂ ∈ dom(M(d)) ∧ subspace(v₁) = s_L ∧ subspace(v₂) = s_L ∧ M(d)(v₁) = M(d)(v₂) : v₁ = v₂)`

Equivalently, `M(d)|_{dom_L}` is a partial injection from V-positions to link addresses. This is the structural counterpart of Nelson's "permanent order of arrival" (LM 4/31): a link entered into its home document's link subspace occupies exactly one ordinal slot at the moment of arrival, and the slot is never duplicated. The udanax-green realisation matches this contract by construction — `docreatelink` allocates the link's ISA, queries the next available link VSA via `findnextlinkvsa`, and performs exactly one `docopy` placing the link at that single VSA (do2.c:151–167) — but the structural property required here is independent of the protocol mechanism.

*Proof.* By induction on transition sequences from Σ₀. *Base:* M₀(d) = ∅ for all d, so the universal-quantified premise is vacuously satisfied. *Inductive step:* fix d and suppose CL-UNIQ holds at the pre-state.
- *K.μ⁺_L.* Adds one mapping `(v_ℓ, ℓ)` with `subspace(v_ℓ) = s_L` and `v_ℓ ∉ dom(M(d))` (verified at K.μ⁺_L's definition site under the empty-link-subspace and non-empty cases respectively). The first-arrangement precondition `ℓ ∉ ran(M(d))` gives that no pre-state V-position in M(d) maps to ℓ — in particular no link-subspace V-position does. Existing link-subspace mappings are preserved by frame. The post-state has exactly one link-subspace V-position mapping to ℓ — namely `v_ℓ` — and the pre-state had zero such V-positions mapping to ℓ (by the freshness precondition); for any other link `ℓ' ≠ ℓ` in the link-subspace range of M(d), the inductive hypothesis CL-UNIQ at the pre-state gives at most one link-subspace V-position mapping to `ℓ'`, and that V-position survives unchanged into M'(d) by frame. CL-UNIQ holds at the post-state.
- *K.μ⁻.* Restricts dom(M(d)); cannot introduce new collisions. CL-UNIQ preserved.
- *K.μ~.* The bijection π : dom(M(d)) → dom(M'(d)) preserves the multiset of mappings (`M'(d)(π(v)) = M(d)(v)`) and is subspace-preserving by K.μ~'s admissibility constraints. Suppose `v₁, v₂ ∈ dom(M'(d))` with `subspace(v₁) = subspace(v₂) = s_L` and `M'(d)(v₁) = M'(d)(v₂) = ℓ`. Write `vᵢ = π(uᵢ)` for unique `uᵢ ∈ dom(M(d))`; subspace preservation gives `subspace(uᵢ) = s_L`, and `M(d)(uᵢ) = M'(d)(π(uᵢ)) = ℓ`. CL-UNIQ at the pre-state gives `u₁ = u₂`, and π's injectivity gives `v₁ = π(u₁) = π(u₂) = v₂`. CL-UNIQ preserved. (This argument uses only subspace-preservation + bijectivity of π + CL-UNIQ at the pre-state; it does not invoke the link-subspace identity property `π(v) = v` — which is itself a derived consequence proved separately in *Link-subspace fixity under K.μ~* — so the CL-UNIQ induction is non-circular with respect to that derivation.)
- *K.μ⁺ (amended), K.α, K.δ, K.λ, K.ρ.* Either hold M in frame entirely or extend only content-subspace V-positions; the link-subspace restriction of M(d) is unchanged. CL-UNIQ preserved. ∎

CL-UNIQ is the operative invariant for deriving K.μ~'s link-subspace identity property (`π(v) = v` for v link-subspace) from the surrounding invariants rather than stating it as a precondition. The derivation appears as *Link-subspace fixity under K.μ~* in the *Decomposition of K.μ~* section below, which appeals to CL-UNIQ at the output state to conclude π = id on dom_L from the function-equality established by the cardinality squeeze.


## Decomposition of K.μ~

This section provides the primary statement and the realisation account for the named composite K.μ~ pointed to from *Elementary transitions* above. The K.μ~ *contract* — bijection equation, admissibility constraints, and derived frame — is stated below as the authoritative definition; invariant preservation under K.μ~ is verified within the contract section directly from subspace preservation + bijectivity + the postcondition admissibility constraints, without recourse to link-subspace fixity. This section then proves (i) link-subspace fixity as a *separately-derived corollary* of the contract plus S3★ + the K.μ⁺ amendment + CL-UNIQ (downstream of invariant preservation, used in case-classification and in the K.μ~ branch of the CL-UNIQ induction), (ii) the existence of at least one admissible K.μ⁻ + K.μ⁺ realisation for every contract instance, and (iii) frame consistency between the composite signature and the K.μ⁻ ∘ K.μ⁺ trace. The placement here — after S3★-aux (*Generalized referential integrity*) and CL-UNIQ (*Link-subspace ownership*) — discharges the forward references flagged at K.μ~'s pointer site: every per-state invariant cited below has already been established, so the argument proceeds without circularity. The contract (with embedded invariant-preservation verification) is stated below; link-subspace fixity is then derived as a corollary; the realisation cases follow.

**K.μ~ — contract.** The contract for K.μ~, for some `d ∈ E_doc`, is the *bijection equation*

`(E π : π is a bijection dom(M(d)) → dom(M'(d)) : (A v ∈ dom(M(d)) :: M'(d)(π(v)) = M(d)(v)))`

together with the admissibility constraints and derived frame stated below. Downstream proofs that appeal to K.μ~'s contract (the K.μ~-FIX domain-fixity argument; the link-subspace fixity argument; J3 isolation) discharge through the elementary K.μ⁻ + K.μ⁺ frames of any realisation, not through a primitive K.μ~ frame.

*Admissibility constraints.* π is subspace-preserving — `(A v ∈ dom(M(d)) :: subspace(π(v)) = subspace(v))` — so each V-position is permuted within its own subspace; π produces V-positions satisfying S8a (all components strictly positive); and the resulting arrangement M'(d) satisfies S8-depth (uniform depth within each subspace), D-CTG★ (contiguity within each subspace), and D-MIN★ (minimum position in each non-empty subspace). The link-subspace identity property `(A v ∈ dom(M(d)) : subspace(v) = s_L : π(v) = v)` is *not* among these admissibility constraints — it is a *corollary* of the contract plus S3★ + the K.μ⁺ amendment + CL-UNIQ, established in *Link-subspace fixity under K.μ~* below, and is downstream of the invariant-preservation argument rather than upstream of it.

The bijection preserves the mapping pointwise — each V-position retains its I-address — so the multiset of referenced I-addresses is identical. As a corollary, ran(M'(d)) = ran(M(d)). Nelson: content "changes Vstream positions but touches nothing in Istream. The same bytes appear in a different order." Gregory confirms that reordering is the only transition kind that leaves all persistent structures outside the arrangement unchanged.

*Invariant preservation under K.μ~ — direct verification from subspace preservation + bijectivity.* The per-state invariants this ASN attaches to the post-state arrangement M'(d) — S3★ (subspace-routed referential integrity), S2 (functionality), S8a (positive components), S8-depth (uniform depth per subspace), D-CTG★ (per-subspace contiguity), D-MIN★ (per-subspace minimum), and S8-fin (finite domain) — are each preserved under K.μ~ from the admissibility constraints alone, without recourse to link-subspace fixity:
- *S3★:* for each `v ∈ dom(M(d))`, the bijection equation `M'(d)(π(v)) = M(d)(v)` pins the targeted address pointwise; subspace preservation gives `subspace(π(v)) = subspace(v)`, so a content-subspace pre-position (with `M(d)(v) ∈ dom(C)` by pre-state S3★) maps to a content-subspace post-position with the same `dom(C)` target, and a link-subspace pre-position (with `M(d)(v) ∈ dom(L)` by pre-state S3★) maps to a link-subspace post-position with the same `dom(L)` target. S3★'s content/link branch alignment is preserved pointwise. A π violating subspace preservation would yield `M'(d)(π(v)) = M(d)(v) ∈ dom(L)` at a content-subspace post-position (or symmetrically `∈ dom(C)` at a link-subspace post-position), contradicting S3★; the admissibility constraint excludes that case at the contract level.
- *S2 (functionality):* π is a bijection, so the image positions `{π(v) : v ∈ dom(M(d))}` are pairwise distinct; each π(v) receives exactly the value M(d)(v) by the bijection equation, giving a well-defined function M'(d) — no two V-positions in the post-state collide on conflicting values.
- *S8a, S8-depth, D-CTG★, D-MIN★, S8-fin:* each is required as a postcondition on M'(d) by the admissibility constraints listed above (S8-fin is inherited from the pre-state via π's bijectivity from the finite dom(M(d))), so each holds at the K.μ~ post-state by stipulation.

Link-subspace fixity is *not* invoked in any of these preservation arguments — invariant preservation under K.μ~ closes through subspace preservation + bijectivity + the postcondition admissibility constraints alone, and the fixity corollary supplies a *structural* fact about K.μ~'s effect on the link subspace (downstream of invariant preservation, used in the decomposition's case-classification and in CL-UNIQ-related downstream arguments) rather than a hypothesis on which invariant preservation rests.

*Frame (derived).* C' = C; E' = E; R' = R; L' = L; (A d' : d' ≠ d : M'(d') = M(d')). Each clause is the composition of the constituent operators' frames: K.μ⁻ and K.μ⁺ both hold C, E, R fixed and act on the single document d, so the composite holds the same; L is also held fixed by the same composition (consistent with the uniform K.μ~ entry in *Frame extension (all existing transitions)* above). The frame consistency check appears below at *Frame consistency check*, where the composite frame is verified clause-for-clause against the K.μ⁻ ∘ K.μ⁺ trace.

**Link-subspace fixity under K.μ~ (corollary).** The invariant-preservation argument under K.μ~ has already discharged in the contract section above from subspace preservation + bijectivity + the postcondition admissibility constraints, without recourse to any link-subspace identity property. We now establish link-subspace fixity as a *separately-derived corollary* of the K.μ~ contract plus the surrounding invariants S3★ + the K.μ⁺ amendment + CL-UNIQ: any candidate transition satisfying only the weaker subspace-preservation clause on π is forced into link-subspace identity at every reachable state where K.μ~ is invoked. The corollary is placed here, *before* the decomposition cases below, so that Case 2 of the decomposition (which uses the fixity result to characterize when π = id) can cite it without forward reference; its role downstream is to supply a structural fact about K.μ~'s effect on the link subspace (used in case-classification and in the K.μ~ branch of the CL-UNIQ induction), not to underwrite invariant preservation — that closure was already obtained above.

The consistency argument proceeds in two steps: function equality on dom_L (step 1, the cardinality squeeze), and closure from function equality to π-identity via CL-UNIQ (step 2).

*Step 1 — function equality on dom_L.* Since K.μ⁺ (amended) requires `subspace(v) = s_C` for new V-positions, K.μ⁺ cannot create link-subspace V-positions. Let `dom_L(M(d)) = {v ∈ dom(M(d)) : subspace(v) = s_L}` denote the link-subspace V-positions. Assume only the weaker subspace-preservation clause on π. With S3★ established for M'(d), π must map link-subspace positions to link-subspace positions: if `v ∈ dom_L(M(d))` then `M(d)(v) ∈ dom(L)`, and `M'(d)(π(v)) = M(d)(v) ∈ dom(L)`, so `subspace(π(v)) = s_L`: by S3★-aux, `subspace(π(v)) ∈ {s_C, s_L}`; the case `subspace(π(v)) = s_C` is eliminated because a content-subspace position mapping to dom(L) would violate S3★'s content clause, since `M'(d)(π(v)) ∈ dom(L)` and `dom(L) ∩ dom(C) = ∅` (L14, which depends on SC-NEQ). Thus `π` restricted to `dom_L(M(d))` is an injection into `dom_L(M'(d))`. Since K.μ⁺ cannot create link-subspace V-positions, `|dom_L(M'(d))| ≤ |dom_L(M(d))|`. If K.μ⁻ removed `r ≥ 1` link-subspace positions, then `|dom_L(M'(d))| ≤ |dom_L(M(d))| − r`, and the injection from `dom_L(M(d))` (size N) into `dom_L(M'(d))` (size at most N − r) cannot exist. Therefore `r = 0` — no link-subspace positions are removed. It follows that `M'(d)` restricted to `dom_L(M(d))` equals `M(d)` restricted to `dom_L(M(d))` *as a function from V-positions to link addresses*: i.e., for each `v ∈ dom_L(M(d))`, `v ∈ dom_L(M'(d))` and `M'(d)(v) = M(d)(v)`. Let `M_int(d)` denote the intermediate arrangement after K.μ⁻ but before K.μ⁺. K.μ⁻ removes none of the link-subspace positions (`r = 0`) and preserves the values of all surviving positions, so `M_int(d)|_{dom_L} = M(d)|_{dom_L}`. K.μ⁺ (amended) operates on `M_int(d)`: its frame preserves pre-existing mappings (`(A v : v ∈ dom(M_int(d)) : M'(d)(v) = M_int(d)(v))`), and its subspace restriction prevents creating new link-subspace positions. Chaining: `M'(d)|_{dom_L} = M_int(d)|_{dom_L} = M(d)|_{dom_L}` as functions.

*Step 2 — from function equality to π-identity (closure via CL-UNIQ).* Function equality on dom_L tells us that the link-subspace map of M'(d) coincides pointwise with that of M(d) — but the K.μ~ definition gives `M'(d)(π(v)) = M(d)(v)`, which says π(v) is *some* V-position in M'(d) mapping to `M(d)(v)`, not necessarily v itself. To compel `π(v) = v` we need the link-subspace map to be injective: if M'(d)(π(v)) = ℓ and M'(d)(v) = ℓ, then π(v) = v iff ℓ appears at a unique V-position in M'(d). This is exactly CL-UNIQ at the output state. Combining: for each `v ∈ dom_L(M(d))`, let `ℓ := M(d)(v)`. By the function equality just established, `M'(d)(v) = ℓ`. By K.μ~'s definition, `M'(d)(π(v)) = M(d)(v) = ℓ`. By S3★ at M'(d), `subspace(π(v)) = s_L` (eliminated as above), so `π(v) ∈ dom_L(M'(d))`. CL-UNIQ at M'(d) — invoked here as an inductively-established invariant of every reachable state, with the K.μ~ post-state being one such — gives: any two link-subspace V-positions in M'(d) mapping to the same link address are equal. Applied with v₁ = v, v₂ = π(v), both in dom_L(M'(d)), both mapping to ℓ: v = π(v), i.e., `π(v) = v`. The link-subspace identity therefore follows from S3★ + the K.μ⁺ amendment + CL-UNIQ alone, justifying its omission from the K.μ~ precondition catalogue. ∎

**Decomposition of K.μ~ into K.μ⁻ + K.μ⁺.** With link-subspace fixity in hand, we organize the decomposition into three exhaustive cases by the post-state of the bijection and the content of the domain, and verify intermediate-state admissibility exactly once for the non-trivial case.

*Case 1: π = id (zero elementary steps).* When π is the identity on dom(M(d)), K.μ~ produces M'(d) = M(d) and expands into *zero elementary steps*. The case covers both `dom(M(d)) = ∅` (the empty bijection on ∅) and `dom(M(d)) ≠ ∅` with π = id on a non-empty domain; both are valid K.μ~ invocations — the empty bijection vacuously satisfies subspace preservation and link-subspace identity, while the identity bijection on a non-empty domain satisfies every K.μ~ precondition since π(v) = v makes subspace preservation and link-subspace identity trivial and the M'-side requirements (S8a, S8-depth, D-CTG★, D-MIN★) are inherited from M(d). Neither subcase invokes a literal K.μ⁻ + K.μ⁺ round-trip: K.μ⁻'s strict-contraction precondition `dom(M'(d)) ⊂ dom(M(d))` cannot be met when M'(d) = M(d), so a vacuous round-trip is not a valid elementary path; the correct expansion is the empty sequence. All invariants are trivially preserved.

*Case 2: π ≠ id implies dom_C(M(d)) ≠ ∅ (link-subspace-only arrangements force π = id).* The link-subspace identity property (established in *Link-subspace fixity under K.μ~* immediately above) gives `(A v ∈ dom(M(d)) : subspace(v) = s_L : π(v) = v)`. By S3★-aux (*Generalized referential integrity* above), every v ∈ dom(M(d)) has `subspace(v) ∈ {s_C, s_L}`. When dom_C(M(d)) = ∅, every v ∈ dom(M(d)) has subspace s_L; the link-subspace identity property then applies to every v, forcing π = id throughout. Contrapositively, π ≠ id implies dom_C(M(d)) ≠ ∅. (A consistency check via the K.μ⁻ + K.μ⁺ decomposition: were we to attempt a nonzero-step decomposition when dom_C(M(d)) = ∅, K.μ⁻ would remove r ≥ 1 link-subspace positions, and the K.μ⁺ amendment — restricting K.μ⁺ to content-subspace V-positions — would force the r re-added positions to be content-subspace; the K.μ~ definition gives M'(d)(π(v)) = M(d)(v), and S3★ at the pre-state gives M(d)(v) ∈ dom(L) for v link-subspace, contradicting K.μ⁺'s referential-integrity precondition M'(d)(π(v)) ∈ dom(C) under L14 (dom(C) ∩ dom(L) = ∅). The zero-step expansion is the unique admissible decomposition.)

*Case 3: π ≠ id with dom_C(M(d)) ≠ ∅ (the non-trivial decomposition).* This is the only case requiring genuine elementary steps. We exhibit one admissible decomposition — *full content-subspace clearance and rebuild* — and use its existence to establish completeness; the K.μ~ contract is the bijection clause stated at the definition site (the semantic statement), and the decomposition is a *constructive witness* showing every such K.μ~ can be realised as a sequence of elementary K.μ⁻ + K.μ⁺ steps. Other admissible decompositions may exist for particular π shapes (see *Other admissible decompositions* below); the full-clearance form is selected here because it is uniformly admissible for *every* valid π in Case 3 — a single witness pattern whose admissibility verification works irrespective of π's specific structure. The decomposition has the explicit form:

  **K.μ⁻ step.** Remove V_{s_C}(d) entirely from M(d) — i.e., full content-subspace clearance with n'_{s_C} = 0. Link-subspace mappings are retained (n'_{s_L} = n_{s_L}, the full pre-state link-subspace cardinality). Admissibility under K.μ⁻'s D-CTG★/D-MIN★ postconditions: the content-subspace removal pattern is "n'_S = 0" (full-subspace clearance, case (a) of K.μ⁻'s case analysis, compatible) and the link-subspace removal pattern is "n'_S = n_S" (empty suffix, also case (a), compatible). D-CTG★ and D-MIN★ hold at the intermediate state: V_{s_C}(d_int) = ∅ satisfies both vacuously, and V_{s_L}(d_int) = V_{s_L}(d) is unchanged so inherits both from the pre-state.

  **K.μ⁺ step.** Add `{π(v) ↦ M(d)(v) : v ∈ V_{s_C}(d)}` — re-adding every content-subspace mapping at its permuted position. This rebuilds the content subspace at positions π(V_{s_C}(d)). By K.μ~'s subspace-preserving precondition, `subspace(π(v)) = subspace(v) = s_C` for each v ∈ V_{s_C}(d), so every new V-position is content-subspace, consistent with the K.μ⁺ content-subspace amendment.

*Existence of an admissible decomposition for every valid π in Case 3.* The full-clearance + rebuild decomposition just exhibited is admissible *unconditionally* for every valid K.μ~ transition falling in Case 3: the K.μ⁻ step's D-CTG★/D-MIN★ postconditions reduce to "case (a) on both subspaces" (full content-subspace clearance and empty link-subspace removal), which require no further conditions on π beyond what K.μ~ already supplies; and the K.μ⁺ step's preconditions reduce uniformly to checks verified in *Intermediate-state admissibility* below, all of which discharge from K.μ~'s preconditions and postconditions without reference to π's particular shape. Therefore, for every valid bijection π satisfying K.μ~'s preconditions in Case 3, at least one admissible K.μ⁻ + K.μ⁺ decomposition exists — namely the full-clearance witness — and the elementary-kinds catalogue is complete with respect to K.μ~. This is an *existence* claim, not a construction claim: the abstract specification asserts that *some* admissible elementary decomposition exists for every K.μ~; it does not legislate which decomposition an implementation must use, and the full-clearance witness here serves only to discharge the existence obligation.

*Other admissible decompositions.* For specific π shapes, more economical decompositions exist:
- *Swap of the two maximum content-subspace positions.* When π swaps `[s_C, 1, ..., 1, n_{s_C}]` and `[s_C, 1, ..., 1, n_{s_C} − 1]` and fixes all other V-positions, the decomposition need only remove the top two content-subspace positions (K.μ⁻ with n'_{s_C} = n_{s_C} − 2, case (a) of the case analysis) and re-add them in swapped order (a two-position K.μ⁺). This is a "minimum-suffix swap" that touches only the affected positions.
- *Permutation acting on the top-k content-subspace positions only.* When π fixes the bottom n_{s_C} − k content-subspace positions and permutes only the top k, the decomposition need only remove and rebuild the top-k suffix (K.μ⁻ with n'_{s_C} = n_{s_C} − k, K.μ⁺ rebuilding k positions). This is a "minimum-suffix permutation."
- *Permutation acting on the link-subspace minimum.* Ruled out by the derived link-subspace identity property `π(v) = v` for v link-subspace; the link subspace cannot be permuted at all, so no decomposition needs to touch link-subspace positions beyond holding them in K.μ⁻'s retained set.

These optimisations realise the same K.μ~ contract with fewer elementary steps and a smaller intermediate-state footprint. They are *consistent witnesses* — alternative decompositions that satisfy the same K.μ~ definition — not separate K.μ~ semantics. The abstract specification is silent on which witness an implementation chooses: any admissible K.μ⁻ + K.μ⁺ pair realising the bijection equality M'(d)(π(v)) = M(d)(v) at the same frame discharges the K.μ~ contract. The existence claim above (full-clearance witness applies uniformly) suffices to establish that the elementary kinds are complete with respect to K.μ~; the optimisations illustrate that completeness does not force a unique realisation, only the availability of *at least one* admissible decomposition per valid π.

*Why link-subspace mappings must be retained by K.μ⁻ rather than removed and rebuilt.* The K.μ⁺ amendment restricts K.μ⁺ to content-subspace V-positions, so link-subspace mappings removed by K.μ⁻ could not be restored by any subsequent K.μ⁺ — the only available extension operator. Were K.μ⁻ to remove a link-subspace mapping `(v, ℓ)` with v ∈ V_{s_L}(d), no K.μ⁺ step could re-add the position v (forbidden by the K.μ⁺ amendment) and no K.μ⁺_L step could re-add it either (K.μ⁺_L's link-subspace contiguity precondition requires placement at the next contiguous position from the link-subspace minimum or maximum, not at an arbitrary previously-removed position). The decomposition would fail to reconstruct M'(d), violating the K.μ~ definition's bijection equality. Hence K.μ⁻ must retain all link-subspace mappings.

*Intermediate-state admissibility (verified once).* Let Σ_int be the state after the K.μ⁻ step. K.μ⁻'s frame gives C_int = C, E_int = E, R_int = R, L_int = L, and M_int(d') = M(d') for d' ≠ d, with M_int(d) = M(d) ↾ V_{s_L}(d) (link-subspace mappings only). The K.μ⁺ step's preconditions at Σ_int:
- (i) `d ∈ (E_int)_doc` — holds because E_int = E and d ∈ E_doc.
- (ii) *Referential integrity.* For each re-added position π(v) (with v ∈ V_{s_C}(d)), the assigned I-address `M(d)(v) ∈ dom(C)` at the pre-state by S3★'s content clause; since C_int = C, `M(d)(v) ∈ dom(C_int)`.
- (iii) *Content-subspace restriction (K.μ⁺ amendment).* Every new V-position π(v) has `subspace(π(v)) = s_C` by K.μ~'s subspace-preserving precondition.
- (iv) *S8a, S8-depth.* π produces V-positions with all components strictly positive (K.μ~ precondition) and uniform depth within the content subspace (K.μ~ requires S8-depth on the result M'(d)).
- (v) *S8-fin.* dom(M'(d)) is finite because π is a bijection from the finite dom(M(d)) (S8-fin at the pre-state); the K.μ⁺ step adds |V_{s_C}(d)| < ∞ new positions to the finite M_int(d).
- (vi) *D-CTG★ and D-MIN★ at the post-state.* K.μ~'s postcondition requires these on M'(d); the K.μ⁺ step's postcondition establishes them for the rebuilt content subspace.

Functionality (S2) of the result M'(d) follows from the injectivity of π: each target position π(v) receives exactly one value M(d)(v), and since π is a bijection no two source positions collide.

*Frame consistency check.* The frame derived for K.μ~ (stated at *K.μ~ — contract* above in this section) must equal the composition of the constituent operators' frames. K.μ⁻ gives C_int = C, E_int = E, R_int = R, L_int = L, and M_int(d') = M(d') for d' ≠ d. K.μ⁺ gives C' = C_int = C, E' = E_int = E, R' = R_int = R, L' = L_int = L, and M'(d') = M_int(d') for d' ≠ d. Composing: C' = C, E' = E, R' = R, L' = L, (A d' : d' ≠ d : M'(d') = M(d')) — matching the K.μ~ frame stated above clause for clause. The decomposition is therefore consistent with K.μ~'s composite signature.

**K.μ~-FIX (Domain fixity under K.μ~).** `dom(M'(d)) = dom(M(d))` — the bijection π is a permutation of a fixed domain. In the four-component state, dom(M(d)) consists of content-subspace positions only. D-SEQ at the pre-state gives V_{s_C}(d) = {[s_C, 1, ..., 1, k] : 1 ≤ k ≤ n}; D-SEQ at the post-state (from K.μ~'s D-CTG and D-MIN postcondition) gives V_{s_C}(d') = {[s_C, 1, ..., 1, k] : 1 ≤ k ≤ n'}. Since π is a bijection, |dom(M'(d))| = |dom(M(d))|, so n' = n, giving V_{s_C}(d') = V_{s_C}(d) and dom(M'(d)) = dom(M(d)). In the extended state, subspace preservation (link-subspace fixity under K.μ~ just established) gives |V_S(d')| = |V_S(d)| for each subspace S independently; the same D-SEQ argument yields V_S(d') = V_S(d) for each S, hence dom(M'(d)) = dom(M(d)). This makes π : dom(M(d)) → dom(M(d)) a permutation, simplifying the decomposition: the K.μ⁻ + K.μ⁺ round-trip restores the same domain with permuted values.

When dom(M(d)) = ∅, K.μ~ is the identity — the empty bijection π : ∅ → ∅ satisfies the definition, producing zero elementary steps. When dom(M(d)) is non-empty, π = id is also permitted — the identity bijection produces M'(d) = M(d), a degenerate reordering that changes nothing. In this case K.μ~ expands into zero elementary steps, regardless of whether dom_C(M(d)) is empty or non-empty: since M'(d) = M(d), there is no content-subspace position to remove and re-add, and the K.μ⁻ + K.μ⁺ decomposition is not invoked (K.μ⁻'s strict-contraction precondition `dom(M'(d)) ⊂ dom(M(d))` would not be satisfied by a vacuous K.μ⁻ in any case, so a literal "vacuous round-trip" is not a valid elementary path). Uniformly: π = id ⟹ zero elementary steps ⟹ M'(d) = M(d). In all degenerate cases (empty domain or identity bijection) all invariants are trivially preserved. We do not restrict π to non-identity bijections; the formal definition subsumes both degenerate cases cleanly under the zero-elementary-steps reading. The coupling constraint J1 is vacuously satisfied at the composite level: since K.μ~ preserves ran(M(d)), the set difference ran(M'(d)) \ ran(M(d)) is empty — no new containment pairs arise, so no provenance recording is needed. We retain K.μ~ as a named transition because its isolation property (J3) and semantic clarity — reordering as a single atomic concept — justify separate treatment. Gregory's independent analysis of the implementation identifies the same six persistent modification kinds, confirming this classification.


## Coupling and isolation

The elementary transitions do not all occur independently. Some must co-occur to maintain invariants (coupling); some must leave other components unchanged (isolation). The weakest-precondition calculus makes the coupling constraints visible.

A clarification on scope. The frame conditions stated above describe individual elementary transitions: K.μ⁺ alone does not modify R, K.α alone does not modify M, and so on. Coupling constraints describe required co-occurrence — when K.μ⁺ occurs, K.ρ must also occur in the same composite transition.

**Definition (Current containment).** The *current containment* of state Σ is the set of all document-content pairs where the content is presently in the document's arrangement:

`Contains(Σ) = {(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))}`

This is a derived quantity of the state — it captures what each document currently displays. We will need it both in the valid composite definition (as a state invariant) and in the coupling derivations that follow.

**Definition (Valid composite transition).** A composite transition Σ → Σ' is *valid* iff it is a finite sequence of elementary transitions Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ' satisfying two conditions:

(1) *Elementary preconditions:* each step Σᵢ → Σᵢ₊₁ satisfies the precondition of its elementary transition kind, evaluated at the intermediate state Σᵢ.

(2) *Coupling constraints:* J0, J1, and J1' hold for the composite — evaluated between the initial state Σ and the final state Σ'.

**Lemma (Permanence from elementary frames).** Every valid composite transition satisfies P0, P1, P2, and — in the extended state — L12. Each elementary transition's frame ensures: K.α extends dom(C) preserving existing entries (all others hold C' = C), giving P0; K.δ extends E (all others hold E' = E), giving P1; K.ρ extends R (all others hold R' = R), giving P2; K.λ extends dom(L) preserving existing entries (all others hold L' = L), giving L12. By transitivity over any finite sequence satisfying (1), the composite inherits all four append-only-with-value-preservation properties. The L12 clause is vacuous in the four-component state (where L is not yet a state component); in the extended state it provides the link-store analog of P0, completing the structural symmetry between the content store and the link store.

The invariants of the four-component state partition by quantification *type* into two well-typed statements: a per-state theorem whose conjuncts are properties of a single state Σ, and a per-transition theorem whose conjuncts are properties of a step `Σ → Σ'`. Stating the first as "every reachable state satisfies P0" would be type-incorrect — P0's foundation form `(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ (A a : a ∈ dom(C) : C'(a) = C(a)))` quantifies over `Σ → Σ'`, not over a single Σ, so the assertion is well-typed only as a per-transition statement. P1 and P2 take the same shape (`(A Σ → Σ' :: E ⊆ E')` and `(A Σ → Σ' :: R ⊆ R')`), and are therefore separated from the per-state invariants below. (The extended-state split in *Extended reachable-state invariants* below applies the same pattern to the five-component state, with ExtendedReachableStateInvariants and ExtendedTransitionInvariants standing in analogous roles to the two theorems here.)

**Theorem (Reachable-state invariants, per-state).** Every state reachable from Σ₀ by a finite sequence of valid composite transitions satisfies P4 (Contains(Σ) ⊆ R), P6, P7, P7a, P8, S2, S3, S8a, S8-depth, S8-fin, D-CTG, and D-MIN.

*Base case.* At Σ₀: dom(C₀) = ∅ makes P6 vacuous (no content, so no origin to check); R₀ = ∅ makes P7 vacuous (no provenance entries to ground); dom(C₀) = ∅ makes P7a vacuous (no content to require provenance for); (E₀)_doc = ∅ makes P4 vacuous (no documents, so Contains(Σ₀) = ∅ ⊆ R₀); E₀ = {n₀} with IsNode(n₀) makes P8 vacuous (no non-node entities); (E₀)_doc = ∅ makes S2–S8-fin, D-CTG, and D-MIN vacuous (no arrangements exist).

*Inductive step.* For any reachable state Σ satisfying the per-state invariants above, every valid composite Σ → Σ' produces Σ' satisfying the same — S2/S3/S8a/S8-depth/S8-fin/D-CTG/D-MIN by the arrangement invariants lemma; P8 as derived above; P4, P6, P7, and P7a as derived below.

**Theorem (Reachable-state invariants, per-transition).** Every valid composite transition Σ → Σ' between reachable states satisfies P0, P1, P2.

*Proof.* Direct from the permanence lemma above: each elementary transition's frame ensures append-only-with-value-preservation on C (P0 — K.α extends dom(C) preserving existing entries, all others hold C' = C), E (P1 — K.δ extends E, all others hold E' = E), and R (P2 — K.ρ extends R, all others hold R' = R). Each conjunct is formally stated with the quantifier `(A Σ → Σ' :: ...)` and is closed under finite composition (transitive inclusion of dom and equality of values), so it carries from each elementary step to every composite boundary in any valid composite. The per-transition theorem has no base case — the properties are vacuous before any transition has occurred — and enters the induction at the first step. ∎

The two theorems together supersede the earlier single-theorem formulation that conflated per-state and per-transition conjuncts; the earlier conjunction is recovered as `(Reachable-state invariants, per-state) ∧ (Reachable-state invariants, per-transition)`. The split mirrors the extended-state pair *ExtendedReachableStateInvariants ∧ ExtendedTransitionInvariants* defined below.

Intermediate states need not satisfy all system invariants; only the final state is required to. The ordering matters: J0 couples K.α with K.μ⁺, and S3 requires the I-address to exist before the V→I mapping is created, so K.α precedes K.μ⁺. Similarly, J4's fork compounds K.δ + K.μ⁺ + K.ρ, and K.μ⁺ requires d ∈ E_doc, which K.δ establishes — so K.δ precedes K.μ⁺. The net effect of a composite transition is the composition of its elementary effects.

For freshly created documents d ∈ E'_doc \ E_doc, the pre-state has d ∉ E_doc, so M(d) = ∅ by the totality of M. Consequently ran(M(d)) = ∅, and the set difference ran(M'(d)) \ ran(M(d)) reduces to ran(M'(d)): all content placed in a new document counts as newly introduced. The coupling constraints below quantify over E'_doc, not E_doc, making them applicable to freshly created documents without special cases.

**J0 (Allocation requires placement).** Content allocation K.α always co-occurs with arrangement extension K.μ⁺:

`(A Σ → Σ', a : a ∈ dom(C') \ dom(C) : (E d, v : d ∈ E'_doc ∧ v ∈ dom(M'(d)) : M'(d)(v) = a))`

Every freshly allocated I-address appears in some arrangement in the post-state — the containing document may itself have been freshly created by K.δ in the same composite transition. This is an axiom of the state transition model, not a theorem of ASN-0036. S7a tells us that the prefix of a identifies the creating document, but it does not tell us that the creating document's arrangement must contain a — an address could be allocated into dom(C) with the correct prefix while appearing in no arrangement. The justification for J0 is design intent: in Nelson's model, content enters the docuverse by being placed in a document. There is no mechanism for creating "orphan" content that exists in Istream without any document displaying it. Gregory confirms: allocation always occurs in the context of a document operation that inserts the new content.

**J1 (Extension records provenance).** Arrangement extension K.μ⁺ must co-occur with provenance recording K.ρ:

`(A Σ → Σ', d ∈ E'_doc, a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R')`

We derive this by wp. The invariant we need — Contains(Σ) ⊆ R — must hold after the composite transition. After K.μ⁺, Contains(Σ') ⊇ Contains(Σ), so new pairs appear. K.μ⁺ alone does not modify R (its frame holds R' = R). Computing the wp of K.μ⁺ alone, substituting R for R':

`wp(K.μ⁺, Contains(Σ') ⊆ R) = (A a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R)`

This requires every new containment pair to already be in R — not generally true for fresh content. K.μ⁺ in isolation cannot maintain the invariant; K.ρ must co-occur, extending R so that the composite post-state satisfies `(A a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R')`.

Gregory identifies one implementation anomaly where provenance recording is skipped for a particular command, "making content invisible to find_documents." The abstract specification treats this as a defect: the coupling is required.

For a freshly created document d ∈ E'_doc \ E_doc, M(d) = ∅ by totality, so ran(M(d)) = ∅, so ran(M'(d)) \ ran(M(d)) = ran(M'(d)): every I-address placed in a new document triggers provenance recording.

**J1' (Provenance requires extension).** Conversely, provenance recording K.ρ for (a, d) occurs only within a composite transition where K.μ⁺ introduces a into ran(M'(d)):

`(A Σ → Σ', a, d ∈ E'_doc : (a, d) ∈ R' \ R : a ∈ ran(M'(d)) \ ran(M(d)))`

J1 ensures every new containment pair is recorded; J1' ensures every new provenance entry corresponds to an actual containment event. Together they characterise new provenance entries: (a, d) ∈ R' \ R if and only if K.μ⁺ introduces a into ran(M'(d)) and (a, d) ∉ R. When (a, d) ∈ R already — from a prior insertion-deletion cycle — K.μ⁺ re-introducing a into d's arrangement requires no new K.ρ, because J1's requirement (a, d) ∈ R' is satisfied by existing membership (P2 ensures prior entries persist). The totality of M ensures J1' is well-defined for freshly created documents: M(d) = ∅ for d ∉ E_doc gives ran(M'(d)) \ ran(M(d)) = ran(M'(d)). Gregory confirms this tight coupling — the provenance structure "accumulates entries from every content addition" and no mechanism exists to record provenance outside of content placement.

**P4a (Historical fidelity).** Every entry in R reflects an actual past *content-subspace* containment event:

`(A (a, d) ∈ R :: (E Σ_k in the transition history : (E v ∈ dom(M_k(d)) : subspace(v) = s_C ∧ M_k(d)(v) = a)))`

*Derivation (four-component state).* By induction on the transition sequence. *Base:* R₀ = ∅; the quantifier is vacuously satisfied. *Inductive step:* for (a, d) ∈ R' \ R, J1' gives a ∈ ran(M'(d)) \ ran(M(d)) — the post-state Σ' is a witnessing state where d's arrangement contains a (in the four-component state every V-position has subspace s_C, so the content-subspace qualifier is automatic). For (a, d) ∈ R, the inductive hypothesis provides a prior witnessing state; P2 ensures the entry persists in R'.

*Derivation (extended state, with J1'★).* The same induction discharges P4a in the extended state, with J1'★ replacing J1' as the load-bearing coupling. *Base:* R₀ = ∅; vacuous. *Inductive step:* for `(a, d) ∈ R' \ R`, J1'★ gives that some content-subspace V-position in M'(d) maps to `a` while no content-subspace V-position in M(d) does — i.e., there exists `v ∈ dom(M'(d))` with `subspace(v) = s_C ∧ M'(d)(v) = a`. The post-state Σ' is therefore a witnessing state whose arrangement contains `a` at a content-subspace V-position, matching the strengthened P4a quantifier. For `(a, d) ∈ R`, the inductive hypothesis provides a prior content-subspace witnessing state; P2 carries the entry into R'. The content-subspace qualification is essential here: J1'★ scopes provenance recording to content-subspace range changes (link-subspace mappings target `dom(L)`, which is disjoint from `dom(C)` by L14, so no link-subspace V-position can witness provenance under P7's `a ∈ dom(C)` requirement). P4a in the extended state therefore reads as "every provenance entry corresponds to a past content-subspace arrangement," consistent with both P7's grounding in `dom(C)` and J1'★'s content-scoped coupling. ∎

**J2 (Contraction isolation).** The elementary transition K.μ⁻ requires no coupling — it is self-sufficient with respect to P0–P2 and Contains(Σ) ⊆ R. As an elementary transition, K.μ⁻ satisfies:

`C' = C ∧ E' = E ∧ R' = R`

The wp analysis confirms this. For P0: K.μ⁻ does not touch C. For P1: does not touch E. For P2: does not touch R. For the provenance bound Contains(Σ) ⊆ R: contraction can only remove pairs from Contains, so Contains(Σ') ⊆ Contains(Σ) ⊆ R = R'. No co-occurring transition is needed to maintain any system invariant.

This is the deepest consequence of the design. Deletion is purely presentational — it changes what appears, not what exists or what has been. Gregory confirms: contraction "never triggers" provenance recording, and the provenance structure "is never pruned."

**J3 (Reordering isolation).** The named composite K.μ~ is likewise self-sufficient:

`C' = C ∧ E' = E ∧ R' = R`

Reordering preserves ran(M(d)), so Contains(Σ') = Contains(Σ). All invariants are trivially maintained; no co-occurring transition is needed.

**J4 (Fork composite).** Nelson's forking creation mode — when the source's content subspace is non-empty — is a composite whose elementary steps are exactly K.δ + K.μ⁺ + K.ρ, all serving the new document d_new:

**Definition (Fork).** A *fork* of d_src to d_new is a composite transition Σ → Σ', with *precondition* d_src ∈ E_doc ∧ V_{s_C}(d_src) ≠ ∅, consisting of:

(i) K.δ creating d_new with d_new ∉ E_doc,

(ii) K.μ⁺ populating M'(d_new) with ran(M'(d_new)) ⊆ ran(M(d_src)),

(iii) K.ρ recording provenance for each a ∈ ran(M'(d_new)),

and no other elementary steps.

Since none of K.δ, K.μ⁺, K.ρ modify C (each has C' = C in its frame), a fork satisfies dom(C') = dom(C) — no new content is created. The provenance conclusion — that (a, d_new) ∈ R' for every a ∈ ran(M'(d_new)) — follows from J1 applied to the fresh-document case: the convention M(d_new) = ∅ gives ran(M'(d_new)) \ ran(M(d_new)) = ran(M'(d_new)), and J1 directly requires provenance recording for each such address. No additional constraint beyond J1 is needed.

The new document d_new is created empty (K.δ), its arrangement extended with mappings to the source's I-addresses (K.μ⁺), and the new associations recorded (K.ρ). The precondition V_{s_C}(d_src) ≠ ∅ ensures K.μ⁺ is well-formed. Since K.μ⁺ (amended) creates only content-subspace V-positions, the I-addresses it maps to must lie in dom(C) (by S3★'s content clause). Only content-subspace V-positions in d_src have I-addresses in dom(C) — link-subspace V-positions map to dom(L), and dom(L) ∩ dom(C) = ∅ (L14). With V_{s_C}(d_src) ≠ ∅, there is at least one content I-address to transclude, so the strict domain extension dom(M'(d_new)) ⊃ dom(M(d_new)) = ∅ is satisfiable. The weaker condition M(d_src) ≠ ∅ is insufficient: a document with only link-subspace positions (reachable via K.δ + K.λ + K.μ⁺_L with no intervening K.μ⁺) has ran(M(d_src)) ⊆ dom(L), and no address in dom(L) can serve as the target of a content-subspace V-position. When the source's content subspace is empty — whether because M(d_src) = ∅ or because dom_C(M(d_src)) = ∅ — the fork definition does not apply; creation from such a source is ex nihilo (K.δ alone), not a fork. Nelson: "the new document's id will indicate its ancestry."

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

P4★ supersedes P4 for the extended state. In pre-extension states (no link-subspace mappings), `Contains_C(Σ) = Contains(Σ)`, so P4★ reduces to P4. Existing transitions preserve P4★: K.α, K.δ, K.ρ hold M in frame; K.μ⁻ contracts dom(M(d)), which can only shrink Contains_C; K.μ~ preserves P4★ by the link-subspace fixity established in the S3★ analysis above. Since π bijects dom(M(d)) onto dom(M'(d)) and maps dom_L bijectively onto dom_L (by fixity), it maps the complement dom_C(M(d)) = dom(M(d)) \ dom_L(M(d)) bijectively onto dom_C(M'(d)) = dom(M'(d)) \ dom_L(M'(d)). These complements are exactly the content-subspace positions by S3★-aux: every V-position has subspace s_C or s_L, so `dom(M(d)) \ dom_L(M(d)) = {v ∈ dom(M(d)) : subspace(v) = s_C}`. With `M'(d)(π(v)) = M(d)(v)` for each such v, the set `{a : (E v ∈ dom_C(M(d)) : M(d)(v) = a)} = {a : (E u ∈ dom_C(M'(d)) : M'(d)(u) = a)}`, so `Contains_C(Σ') = Contains_C(Σ) ⊆ R = R'`.

**Note on K.μ⁺ and P4★.** K.μ⁺ alone adds a content-subspace V-position mapping to address `a`, placing `(a, d) ∈ Contains_C(Σ')`. Its frame has `R' = R`, so if `(a, d) ∉ R`, P4★ is violated at the intermediate state. P4★ is restored at composite boundaries by the coupling constraint J1★, which requires K.ρ to record provenance for every content-subspace arrangement extension. See the two-layer proof structure in ExtendedReachableStateInvariants.


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

1. *Transition preconditions (intra-composite sequencing).* Each step `Σᵢ → Σᵢ₊₁` satisfies the *elementary* precondition of its transition kind, evaluated at the *intermediate* state `Σᵢ`. K.μ~ appearing in the sequence is shorthand for its decomposition (per its definition above): if π = id (including the degenerate cases `dom(M(d)) = ∅` and `dom_C(M(d)) = ∅`, in which link-subspace fixity forces π = id), K.μ~ expands into *zero* elementary steps, producing M'(d) = M(d); otherwise (π ≠ id, which requires `dom_C(M(d)) ≠ ∅`) it expands into two consecutive elementary steps (K.μ⁻ + K.μ⁺), each satisfying its own precondition at the respective intermediate state. This clause is what enforces intra-composite ordering — e.g., that K.α precedes K.μ⁺ when the latter places a freshly allocated I-address `a`, since K.μ⁺'s referential-integrity precondition `a ∈ dom(C)` would fail at the pre-K.α intermediate state otherwise. Step preconditions are *local* to the elementary transition; they say nothing about the composite's endpoints.
2. *Coupling constraints (initial-to-final).* J0, J1★, and J1'★ hold for the composite as a whole — evaluated *only* between the initial state Σ and the final state Σ'. The coupling predicates quantify over the *net* change between Σ and Σ' (e.g., `a ∈ dom(C') \ dom(C)`); they do not constrain the order or shape of intermediate steps, only that the *aggregate* effect of the composite must satisfy them. A composite that satisfies clause (1) but violates clause (2) — for instance, K.α alone without an accompanying K.μ⁺ and K.ρ — is not a valid composite even though every elementary precondition holds at every intermediate state.

The two clauses serve different roles and must not be conflated: clause (1) determines *whether each elementary step can fire at the state at hand*; clause (2) determines *whether the composite, viewed as an atomic transition Σ → Σ', is admissible*. Clause (1) is what makes K.α precede K.μ⁺ when both occur (the K.μ⁺ step cannot satisfy its own precondition `a ∈ dom(C)` until K.α has placed `a` in dom(C)); J0 does *not* impose this ordering — J0 simply requires that the net effect of the composite include a K.μ⁺ for every K.α. Two different elementary sequences (K.α before K.μ⁺ vs. an erroneous K.μ⁺ before K.α) might both satisfy J0 in terms of their endpoints, but only the first satisfies clause (1) at the intermediate states.

This supersedes the earlier ValidComposite definition by extending the elementary transition set with K.λ and K.μ⁺_L, and replacing J1/J1' with J1★/J1'★ — scoping provenance coupling to content-subspace arrangement changes. J0 (AllocationRequiresPlacement) is unchanged — it constrains content allocation (K.α), which remains content-subspace only.

**Extended structural sufficiency.** Seven elementary transition kinds — K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ — plus the named composite K.μ~, are *structurally sufficient* for the modification kinds catalogued in the extended five-component state (C, L, E, M, R). The structural argument from the four-component case lifts directly: C admits one growth mode (K.α); L admits one growth mode (K.λ); E admits one growth mode (K.δ); R admits one growth mode (K.ρ); M's growth partitions by subspace — K.μ⁺ for content-subspace extension, K.μ⁺_L for link-subspace extension — and K.μ⁻ handles contraction; replacement decomposes into K.μ⁻ followed by K.μ⁺ at the granularity dictated by D-CTG★/D-MIN★. The bounded scope of this claim, the named tombstoning gap, two further scope exclusions (account-level k = 1 and non-T10a allocators), and the cross-references to deferred open questions are treated in *Structural sufficiency and known gaps* below.


## Structural sufficiency and known gaps

The two structural-sufficiency claims above — the five-primitive claim at the end of *Elementary transitions* (for the four-component state (C, E, M, R)) and the extended seven-elementary-plus-K.μ~ claim at the end of *Scoped coupling constraints* (for the five-component state (C, L, E, M, R)) — appear at the natural locations in the document, each accompanied by its own bounded-sufficiency caveat and known gap. This subsection consolidates what *is* and what *is not* covered, so that a reader scanning for the elementary set's reach has a single statement to consult.

*What is covered (the elementary set is structurally sufficient for these modification kinds).* The seven elementary transitions K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ — together with the named composites K.μ~ (K.μ⁻ + K.μ⁺) and J0/J1★/J2/J3/J4 — realise every modification kind in Nelson's design enumeration and Gregory's protocol-command catalogue:

- *Content allocation* — K.α (one growth mode for C).
- *Link allocation* — K.λ (one growth mode for L).
- *Entity creation* — K.δ, in both its sub-cases: case (i) node baptism under NodeUniqueAllocation, and case (ii) non-node allocation under T10a's GlobalUniqueness (sub-sub-cases: k = 0 sibling, k = 1 document-only versioning including ghost-base versioning, k = 2 hierarchical descent).
- *Content-subspace arrangement extension* — K.μ⁺ (one growth mode for M's content-subspace component within d, paired with K.α + K.ρ via J0/J1★ when introducing fresh content; standing alone or with K.ρ when transcluding existing content).
- *Link-subspace arrangement extension* — K.μ⁺_L (one growth mode for M's link-subspace component within d, paired with K.λ as a J0-style coupling when a fresh link is being placed, or standing alone when arranging a previously orphaned link; orphaned-link state is permitted, see *Orphan links and coupling flexibility* below).
- *Arrangement contraction* — K.μ⁻, admissible patterns per the explicit precondition (per-subspace suffix removal or full clearance, in either content or link subspace, with at least one subspace contracting strictly).
- *Arrangement reordering* — K.μ~, via its K.μ⁻ + K.μ⁺ decomposition. Subspace-preserving by precondition; link-subspace mappings are additionally fixed (π = id on `V_{s_L}(d)`) as a derived consequence (see *Link-subspace fixity under K.μ~* above). The degenerate cases (`dom(M(d)) = ∅`, `dom_C(M(d)) = ∅`) collapse to π = id and expand into zero elementary steps.
- *Provenance recording* — K.ρ (one growth mode for R).
- *Document fork* — J4 as a K.δ + K.μ⁺ + K.ρ composite (empty fork: K.δ alone when M(d_src) = ∅ or contains only link-subspace positions).
- *Document split / merge* — composites of K.δ, K.μ⁺, and K.ρ (per Nelson's reduction; no primitive split or merge needed).
- *Content replacement* — K.μ⁻ + K.μ⁺ pair, with the K.μ⁻ rebuild scoped per the K.μ⁻ admissibility precondition (single-position pair at the subspace maximum; suffix-from-position pair at an interior position, with the rebuild restoring all suffix elements above the replaced position).

For each four-component direction of change (additions to C, E, M, R; contractions of M) the four-component claim above gives a single elementary realisation. For each five-component direction of change (additions to C, L, E, M; contractions of M; reorderings of M; provenance recordings to R) the extended claim adds the link-side primitives K.λ and K.μ⁺_L without disturbing the content-side reductions. Composite operations (replacement, fork, split, merge) decompose into the elementary set per the case analyses at their respective definitions.

*What is not covered (named known gaps).* Two structural caveats accompany the sufficiency claims, plus one explicit named gap; we enumerate all three together:

- *Open-completeness caveat (both four-component and five-component claims).* "Every admissible state difference Σ → Σ' under the permanence and arrangement invariants is realisable as a finite sequence of elementary transitions" is *not* claimed at either layer. Proving such a claim would require (a) a separate axiomatisation of admissible state differences as a closure property of the state space, independent of the transition set, and (b) a constructive realisation theorem deriving the elementary sequence from any such difference. Neither is offered here. The sufficiency claim, as defended above, is *structural* (one growth mode per append-only component, two mutation modes for M, plus closure under composition) rather than *exhaustive over the difference lattice*. This caveat is general to both the four-component and five-component sufficiency claims.
- *Tombstone-style link withdrawal (named gap).* Withdrawal of a single link at an interior link-subspace position while leaving subsequent links in place — the mechanism Nelson identifies at LM 4/9 ("not currently addressable, awaiting historical backtrack functions") under which a withdrawn link retains its permanent serial address and arrangement position but transitions to inactive status — is *not* expressible as any K.μ⁻ contraction or composite of the present elementary transitions, because the K.μ⁻ amendment's D-CTG★/D-MIN★ postconditions restrict link-subspace contractions to suffix truncations or full clearance, and no other elementary transition deactivates an existing dom(L) entry or marks an arrangement position as inactive without removing it. The K.μ⁻ counterfactual at Step 5 of the *link allocation and arrangement* worked example exhibits this gap concretely (interior removal is rejected by D-CTG★; prefix removal by D-MIN★). Closing the gap would require a state-model extension — a per-link status flag, a tombstone marker on M(d), an explicit retraction-link convention, or a per-link liveness predicate — none of which inhabit the present five-component state. This is the principal named gap.
- *Account-level k = 1.* K.δ's k = 1 sub-case is restricted to `IsDocument(t)`; account-level k = 1 (which would produce a structurally well-formed `[N, 0, U, 1]`, still IsAccount) is excluded at the precondition gate because the design admits no account "version" semantics (accounts subdivide hierarchically at k = 2, not by depth-1 tumbler extension). Admitting it would create an entity with no documented role in the model. This is a *deliberate scope exclusion* rather than an expressiveness gap: the elementary set could realise the transition if its precondition admitted it, but the design does not assign meaning to the resulting state, so the exclusion is intentional.
- *Account and document arrangement under non-T10a allocators.* The elementary set assumes T10a-conforming allocation for content (K.α), links (K.λ), and non-node entities (K.δ case (ii)); GlobalUniqueness on the inc operator is what closes the freshness guarantee for these. Allocations produced by allocators that do not conform to T10a (e.g., implementation-specific reuse of decommissioned addresses, externally injected addresses without inc-derivation, or address spaces governed by alternative uniqueness disciplines) fall outside the elementary set's contract. Nodes are a stipulated exception — case (i) of K.δ uses an unspecified protocol-established allocator and treats `e ∉ E` as the operative NodeUniqueAllocation axiom — so node allocation under any protocol satisfying that axiom is admitted, but no other allocator escape is provided. Non-T10a allocators for content, links, or non-node entities are deferred to the *Allocator hierarchy under documents* section's discussion of allocator scope and to any future ASN that admits a broader allocator discipline.

*Cross-references to deferred questions.* The Open Questions section below treats:
- *Withdrawal invariants* — the formal status of tombstoned links, the state-model extension needed to support Nelson's mechanism, and the per-link liveness or status-flag predicates that would compose with K.μ⁻ to admit interior link-subspace withdrawal.
- *Version-management semantics* — the arrangement-transition invariants between successive versions, content-allocator linkage between version base and version, provenance flow across versions, and version-lineage acyclicity; deferred to a subsequent version-management ASN.
- *Account version semantics* (implicit in the k = 1 restriction) — if a downstream design admits depth-1 tumbler-extension at the account level, the K.δ precondition would need to lift the `IsDocument(t)` restriction and a corresponding "account-version" semantics would need to be added.
- *Non-T10a allocator admissibility* — the formal contract that would let a non-T10a allocator participate in the elementary set without breaking the GlobalUniqueness chain that closes `e ∉ E` for K.δ case (ii), `a ∉ dom(C)` for K.α, and `ℓ ∉ dom(L)` for K.λ.

The present ASN's elementary set thus covers the modification kinds named above under T10a-conforming allocation, with K.δ's node sub-case as the one named protocol exception. The four enumerated gaps — open-completeness, tombstoning, account-level k = 1, and non-T10a allocators — together circumscribe what falls outside this contract.


## Orphan links and coupling flexibility

The coupling constraints do not require K.λ to be paired with K.μ⁺_L. A composite consisting of K.λ alone is valid: J0 is vacuous (no content allocated), J1★ is vacuous (no content-subspace extension), and J1'★ is vacuous (no provenance change). The result is a link in dom(L) with no placement in any document's arrangement — an *orphan link*. This is a valid system state, not an error condition. State invariants are preserved: M, C, E, R are all in K.λ's frame (unchanged), so all arrangement, content, entity, and provenance invariants hold identically. L grows by one entry: dom(L') = dom(L) ∪ {ℓ}. K.λ's preconditions guarantee L0 (ℓ has subspace s_L, and ℓ ∉ dom(C) ensures dom(L') ∩ dom(C) = ∅), L1 (zeros(ℓ) = 3), L1a (origin(ℓ) ∈ E_doc), L3 (K.λ requires (F, G, Θ) ∈ Link, so L3 is established for the new entry; L12 preserves all existing entries), L12 (existing entries unchanged: L'(ℓ') = L(ℓ') for all ℓ' ∈ dom(L)), and L14 (disjointness: ℓ ∉ dom(C), so dom(L') ∩ dom(C') = ∅). Nelson explicitly diagrams "deleted links" as a category of document content (LM 4/9): links that exist in permanent storage but are "not currently addressable, awaiting historical backtrack functions."

*Asymmetry derivation (wp analysis).* The decision *not* to couple K.λ with K.μ⁺_L is invariant-driven, not design-asserted. The coupling between K.μ⁺ and K.ρ (J1★) was forced by a wp calculation: K.μ⁺ alone fails to maintain `Contains_C(Σ) ⊆ R` (P4★), because K.μ⁺ extends `Contains_C` while holding R in frame, so `wp(K.μ⁺, P4★) = (A a : a ∈ ran_C(M'(d)) \ ran_C(M(d)) : (a, d) ∈ R)` — false in general, hence K.ρ must co-occur to restore P4★ at the composite boundary. The analogous question for K.λ is: is there an invariant of the form `LinkContains(Σ) ⊆ X` (for some historical-record component X analogous to R) that K.λ alone would violate? Surveying the invariant set of ExtendedReachableStateInvariants:

  - **P7 (ProvenanceGrounding).** `(A (a, d) ∈ R :: a ∈ dom(C))` — R records only content addresses, by definition. No link-provenance relation `R_L ⊆ T_link × E_doc` exists in the five-component state; therefore no "Contains_L ⊆ R_L" invariant is on the books for K.λ to violate.
  - **P4★ (ProvenanceBounds, content-scoped).** `Contains_C(Σ) ⊆ R` — explicitly content-scoped (the `Contains_L` analog is excluded by definition, since R's range is restricted to dom(C) by P7). K.λ holds C, M, R in frame, so `wp(K.λ, P4★) = Contains_C(Σ) ⊆ R = P4★` (unchanged). P4★ is preserved trivially.
  - **CL-OWN (LinkSubspaceOwnership).** `(A d, v : v ∈ dom(M(d)) ∧ subspace(v) = s_L : origin(M(d)(v)) = d)` — a constraint on link-subspace V-positions already in M, not on dom(L) membership. K.λ holds M in frame, so `wp(K.λ, CL-OWN) = CL-OWN` (unchanged). The constraint fires only when K.μ⁺_L places a link in some document's arrangement; it imposes no requirement on the link's mere existence in dom(L).
  - **L0, L1, L1a, L3, L12, L14, L-fin.** All link-store invariants are about properties of `ℓ ∈ dom(L)` itself (subspace, depth, origin, value, immutability, disjointness, finiteness) — none requires a link to also appear in some `M(d)`. K.λ's preconditions establish each for the new entry; K.λ alone preserves all of them.

No invariant of the extended state requires every `ℓ ∈ dom(L)` to inhabit some document's arrangement. Consequently `wp(K.λ, I) = I` for every state invariant I in the elementary class, and the only composite-class invariants (P4★, P7a) are content-scoped — they do not predicate over dom(L). The coupling that would force K.λ + K.μ⁺_L co-occurrence simply has no invariant to anchor it.

This is the structural counterpart of J0's wp derivation. J0 was forced by P7a (`(A a ∈ dom(C) :: (E d :: (a, d) ∈ R))`): K.α alone adds `a` to dom(C') without provenance, so P7a fails unless `a` enters some arrangement (J0) and provenance is recorded (J1★). For links, no `(A ℓ ∈ dom(L) :: (E d :: ℓ ∈ ran(M(d))))` invariant is stipulated; orphan links are admissible precisely because *no rule forbids them*. The wp analysis confirms the absence of the rule as the operative reason — not a design preference for orphan links, but the absence of an invariant that would render them ill-formed.

Nelson's design corroborates this absence rather than supplying an alternative coupling: "deleted links" (LM 4/9) — links present in storage but absent from current arrangements — are part of the intended state space, and no historical-coverage analog of P7a is asserted for links. Were such an invariant to be added later (e.g., a hypothetical "every link has appeared in some arrangement at some past state"), the same wp logic that produced J0 + J1★ for content would mechanically yield a corresponding K.λ + K.μ⁺_L coupling. The framework's openness on this point is structural, not omitted.

Link withdrawal via K.μ⁻ applied to the link subspace would in principle produce the same state — a link present in L but absent from all current arrangements — but is constrained by D-CTG: removing an interior link-subspace V-position creates a gap in the contiguous range, and K.μ~ cannot close it (link-subspace mappings are fixed, as shown above). Valid link-subspace contractions are suffix truncations: for `V_{s_L}(d) = {[s_L, 1, …, 1, k] : 1 ≤ k ≤ n}` (by D-SEQ), the result must be `{[s_L, 1, …, 1, k] : 1 ≤ k ≤ n'}` for some `0 ≤ n' < n`. Removing an interior position breaks contiguity (violating D-CTG), and removing the minimum while positions above it remain violates D-MIN. Any suffix `{[s_L, 1, …, 1, k] : n' < k ≤ n}` can be removed at once — including all positions when `n' = 0`, since D-CTG and D-MIN hold vacuously for the empty set. Nelson's design suggests a different mechanism: link addresses are permanent and "not currently addressable" when withdrawn (LM 4/9), paralleling deleted bytes — the link transitions to inactive status while preserving its arrangement position, rather than being removed from M(d). The precise withdrawal mechanism is deferred to the open question on withdrawal invariants.

We do not add a J0 analog for links — the orphan state is architecturally intentional, satisfying both the permanence guarantee (L12: links are immutable once created) and the owner's right to withdraw (Nelson, LM 2/29). The wp analysis above shows the *form* of this design choice: it consists of *not* asserting a link-coverage invariant, rather than asserting an "orphan-permitting" rule. The decision-point lives at the invariant set, not at the transition set.


## Destruction confinement

We now state the central structural theorem — a generalisation of S9 (ASN-0036) from two components to four.

**P5 (Destruction confinement).** For every state transition Σ → Σ':

(a) `dom(C') ⊇ dom(C) ∧ (A a : a ∈ dom(C) : C'(a) = C(a))`

(b) `E' ⊇ E`

(c) `R' ⊇ R`

The only component that can lose information is M.

*Proof.* By case analysis on the five elementary transitions. K.α extends dom(C) preserving existing entries, with E and R in its frame. K.δ extends E, with C and R in its frame. K.μ⁺ and K.μ⁻ have C, E, and R in their frames. K.ρ extends R, with C and E in its frame. Each preserves (a) through (c). The distinguished composite K.μ~ decomposes into K.μ⁻ followed by K.μ⁺, both of which preserve (a)–(c), so K.μ~ does as well. General composite transitions, being finite sequences of elementary ones, preserve (a)–(c) by transitivity of ⊇ and ∧. ∎

P5 makes the confinement vivid. Every destructive state change — every removal, every reordering — is confined to the presentational layer. The permanent record (what content exists, which entities have been created, what provenance has been recorded) can only grow.


## Extended monotonicity invariants

**P3★ (ArrangementMutabilityOnly, extended).** Arrangements admit three modes of change: (a) extension, (b) contraction, (c) reordering. No other component — specifically C, L, E, R — admits contraction *or value rewriting*:

  `(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ dom(L) ⊆ dom(L') ∧ E ⊆ E' ∧ R ⊆ R' ∧ (A a ∈ dom(C) :: C'(a) = C(a)) ∧ (A ℓ ∈ dom(L) :: L'(ℓ) = L(ℓ)))`

P3★ both *extends* and *strengthens* the earlier P3. The extension adds L to the enumeration of components that admit only growth, parallel to C, E, and R; this is the cosmetic move forced by the new state component. The strengthening is the more substantive move: P3★ is a *quantitative monotonicity conjunction* (a formal predicate over Σ → Σ' with explicit domain-inclusion and value-preservation conjuncts), whereas P3 is a *qualitative observation* about which components admit which mutability modes (extension/contraction/reordering as named change-modes, without value-preservation predicates). P3★'s two value-preservation conjuncts state that existing entries in C and L are immutable — content of P3 alone does not formalise. In effect P3★ synthesises P0 ∧ L12 ∧ P1 ∧ P2 with the qualitative "no contraction, no reordering" of C, L, E, R; without the value-preservation conjuncts, P3★ would be strictly weaker than P0 ∧ L12 combined, and would not capture the verbal claim of value immutability that P3's prose asserts but does not formalise. Readers reaching for "the formal version of P3" should reach for P3★; readers reaching for "the qualitative statement about mutability modes" still reach for P3.

**P5★ (DestructionConfinement, extended).** For every state transition Σ → Σ':

  (a) `dom(C') ⊇ dom(C) ∧ (A a : a ∈ dom(C) : C'(a) = C(a))`

  (b) `dom(L') ⊇ dom(L) ∧ (A ℓ : ℓ ∈ dom(L) : L'(ℓ) = L(ℓ))`

  (c) `E' ⊇ E`

  (d) `R' ⊇ R`

The only component that can lose information is M. P5★ supersedes the earlier P5 by adding clause (b), immediate from L12.


## Worked example: node baptism under the bootstrap root

We exercise K.δ case (i) — protocol-established node allocation — by baptising a fresh node `n = 1.2` under the bootstrap node `n₀ = 1`. The example verifies (i) discharge of the case (i) preconditions, (ii) NodeUniqueAllocation as the operative discharge of `e ∉ E` at the node layer (T10a's GlobalUniqueness is *not* invoked, since node allocations do not pass through inc), (iii) NodeLineage as both an inductive invariant and a precondition at the allocation event (`n₀ ≼ e`), and (iv) frame preservation of every non-entity invariant — K.δ on a node modifies E alone.

*Initial state.* Let Σ₀ be the bootstrap state with only the root node and an empty content/link/arrangement/provenance layer:

> C₀ = ∅
> L₀ = ∅
> E₀ = {1} (the bootstrap node n₀)
> M₀(e) = ∅ for all e
> R₀ = ∅

NodeLineage at Σ₀: the only node in E₀ is `n₀ = 1`, and `1 ≼ 1` by reflexivity of `≼` (Prefix, ASN-0034). ✓

**Step 1: K.δ case (i) — baptise node `n = 1.2` under `n₀`.** The protocol-allocator (Nelson's hierarchical baptism / Gregory's granfilade query-and-increment, treated abstractly here) issues address `1.2`, identifying it as a node and asserting its membership in E.

*Precondition discharge (case (i)).*
- *ValidAddress(n):* `1.2` is a positive-component tumbler of length 2 — every position carries a value in ℕ⁺. ✓
- *IsNode(n):* zeros(`1.2`) = 0 — no zero separator appears in `1.2`. ✓ (Per ASN-0045's IsNode predicate: zeros(e) = 0 with at least one strictly-positive component.)
- *n ∉ E₀:* `1.2 ∉ {1}` by direct inspection. ✓ The discharge here is *NodeUniqueAllocation*, not T10a: the node-allocation protocol guarantees `e ∉ E` by ownership-derived uniqueness at the moment of allocation, and the inc operator — which would underwrite freshness through T10a's GlobalUniqueness in case (ii) — is not invoked at all for node baptism, since `1.2` is not produced by `inc` applied to a previously-allocated tumbler. (See K.δ case (i) discussion above for the protocol/T10a distinction.)
- *n₀ ≼ n:* `1 ≼ 1.2` — `[1]` is a prefix of `[1, 2]` under Prefix (ASN-0034): `#[1] = 1 ≤ 2 = #[1, 2]` and `[1][1] = 1 = [1, 2][1]`. ✓ This is the NodeLineage precondition discharged at the allocation event.
- *zeros(n) = 0:* verified above (IsNode). ✓

The case (ii) precondition list (`parent(e) ∈ E`, `e = inc(t, k)`, `k ∈ {0, 1, 2}` constraints, etc.) is *not* invoked: case (i) governs all node allocations and does not pass through inc.

*Effect.* E₁ = E₀ ∪ {`1.2`} = {1, `1.2`}; M₁(e) = M₀(e) for all e (K.δ at IsNode produces no document, so the `M'(e) = ∅` clause that K.δ applies for documents does not fire here; M is held in frame across all entities); C₁ = C₀ = ∅; L₁ = L₀ = ∅; R₁ = R₀ = ∅.

*Verification against Σ₁.*
- *NodeUniqueAllocation (operative axiom for this step):* the precondition `e ∉ E` is the operative claim of NodeUniqueAllocation at this allocation event; with `n = 1.2 ∉ E₀ = {1}` discharged above, the axiom is satisfied. ✓
- *NodeLineage `(A e ∈ E : IsNode(e) : n₀ ≼ e)`:* The pre-state lineage `1 ≼ 1` is preserved (E₁ ⊇ E₀, no node removal), and the freshly added node `1.2` satisfies `1 ≼ 1.2` by precondition discharge above. The universal therefore holds at Σ₁. ✓ This is the inductive step closing NodeLineage at a K.δ case (i) event: K.δ case (i)'s precondition `n₀ ≼ e` is exactly what NodeLineage requires for the new node, so case (i)'s admissibility check and NodeLineage's inductive step coincide.
- *P8 (`(A e ∈ E : ¬IsNode(e) : parent(e) ∈ E)`):* The new entity `1.2` is a node (IsNode(`1.2`) holds), so it is outside P8's quantifier scope. Every pre-existing entity in E₀ = {1} is also a node, also outside scope. P8 holds vacuously at Σ₁. ✓
- *Frame-preserved invariants:* P0 (C₁ = C₀); P1 (E₁ ⊇ E₀); P2 (R₁ = R₀); P3★/P5★ (compositions of P0, L12, P1, P2 — all extension/equality); P6 (dom(C₁) = ∅, vacuous); P7/P7a (R₁ = ∅ and dom(C₁) = ∅, vacuous); L0/L1/L1a/L1b/L3/L12/L14/L-fin (L₁ = L₀ = ∅, all vacuous); S0–S9 and S3★/S3★-aux (M₁ unchanged from M₀, all vacuous on M₀(d) = ∅); D-CTG★/D-MIN★/D-SEQ★ (vacuous on empty arrangements); CL-OWN/CL-UNIQ (vacuous on empty link-subspace ranges); J0–J4 and J1★/J1'★ (K.δ at IsNode introduces no content, no arrangement extension, no provenance — all coupling clauses are vacuous on this step's elementary footprint).
- *S4 (Origin-based identity at the node layer):* node addresses do not inhabit dom(C) ∪ dom(L), so S4's T10a-mediated identity guarantee for I-addresses and link addresses is not the operative claim here; the protocol-established uniqueness premise carried by NodeUniqueAllocation underwrites the analogous identity property at the node layer (distinct K.δ case (i) events produce distinct node addresses). ✓

**Step 2 (counterfactual): a second K.δ case (i) attempting to re-baptise `1.2` is blocked.** Suppose, after Step 1, the protocol attempts to allocate a second node at address `1.2`. The K.δ case (i) precondition `e ∉ E` fails directly: `1.2 ∈ E₁` by Step 1, and E is monotone under all transitions (P1), so `1.2` remains in every reachable successor of Σ₁. The transition is rejected. NodeUniqueAllocation is the upstream guarantee that a correctly-functioning protocol does not issue the address twice; K.δ's own `e ∉ E` precondition is the downstream catch that rejects any such attempt at the entity-allocation layer regardless of how the address was generated. The two guardrails (protocol-level NodeUniqueAllocation, K.δ-level `e ∉ E`) close the question of node uniqueness identically to how T10a's GlobalUniqueness combined with K.δ's `e ∉ E` closes it for case (ii) live-operand allocations.

**Step 3 (counterfactual): a K.δ case (i) attempting to baptise a disconnected node `n' = 2.1` is blocked.** Suppose an allocator attempts to introduce `2.1` — a structurally valid two-component tumbler with zeros = 0, satisfying ValidAddress and IsNode — into E as a node. The case (i) precondition `n₀ ≼ n'` fails: `1 ⋠ 2.1` by the position-divergence clause of Prefix (ASN-0034), since `n₀[1] = 1` while `2.1[1] = 2`. The transition is rejected, preserving NodeLineage as an inductive invariant. The Xanadu design admits node creation only as descent from the bootstrap root; this counterfactual confirms that the K.δ case (i) precondition `n₀ ≼ e` is the load-bearing discharge of NodeLineage at every node-allocation event — without it, a disconnected-forest scenario would be admissible at the entity layer.

**Synthesis.** Step 1 exercises K.δ case (i) at its operative form (ground-truth node baptism under the bootstrap root), discharging NodeUniqueAllocation as the freshness premise and NodeLineage as the descent precondition. Steps 2–3 confirm the two rejection paths — duplicate address (closed by `e ∉ E`) and disconnected node (closed by `n₀ ≼ e`) — that distinguish case (i)'s protocol-established discipline from case (ii)'s inc-based discipline. Arrangement-side, content-side, link-side, and provenance-side invariants verify vacuously at every step, since K.δ at IsNode produces no change outside E. The example complements the *fork with subsequent insertion* and *ghost-base document versioning* worked examples below by exercising the third K.δ branch — case (i), the protocol-established node allocation that case (ii)'s inc-based machinery does not cover.


## Worked example: fork with subsequent insertion

We trace a concrete scenario to ground the abstract definitions. Let the starting state Σ₁ contain node 1, account 1.0.1, and document d₁ = 1.0.1.0.1 with two characters:

> C₁ = {1.0.1.0.1.0.1.1 ↦ 'H', 1.0.1.0.1.0.1.2 ↦ 'i'}
> E₁ = {1, 1.0.1, 1.0.1.0.1}
> M₁(d₁) = {[1,1] ↦ 1.0.1.0.1.0.1.1, [1,2] ↦ 1.0.1.0.1.0.1.2}
> R₁ = {(1.0.1.0.1.0.1.1, d₁), (1.0.1.0.1.0.1.2, d₁)}

We write a₁ = 1.0.1.0.1.0.1.1 and a₂ = 1.0.1.0.1.0.1.2 for brevity.

**Fork d₁ to d₂ = 1.0.1.0.2.** This is J4's compound K.δ + K.μ⁺ + K.ρ.

*K.δ:* E₂ = E₁ ∪ {1.0.1.0.2}. The address 1.0.1.0.2 is obtained from 1.0.1.0.1 by inc(·, 0) at the document field — a sibling allocation (TA5(c), ASN-0034). M₂(d₂) = ∅.

*K.μ⁺:* M₂(d₂) = {[1,1] ↦ a₁, [1,2] ↦ a₂}. The same I-addresses as d₁ — transclusion, case (ii). No new content enters C. The V-positions [1,1] and [1,2] satisfy S8a (all components strictly positive, zeros = 0) and S8-depth (uniform depth 2 within subspace s_C, matching the pre-existing arrangement of d₁); the shared first component 1 — identifying subspace s_C — is a subspace-identity fact via `subspace(v)` (ASN-0036) rather than a clause of S8-depth itself.

*K.ρ:* R₂ = R₁ ∪ {(a₁, d₂), (a₂, d₂)}.

Verification against the resulting state Σ₂:

- *J0:* No fresh content (dom(C₂) = dom(C₁)), so vacuously satisfied.
- *J1★:* ran(M₂(d₂)|_{s_C}) \ ran(M₁(d₂)|_{s_C}) = {a₁, a₂} \ ∅ = {a₁, a₂} (M₁(d₂) = ∅ since d₂ ∉ (E₁)_doc; this example uses content-subspace mappings only, so the content-subspace restriction is vacuous and J1★ here reduces to J1 of the four-component model). Both (a₁, d₂) and (a₂, d₂) are in R₂. ✓
- *J1'★:* `R₂ \ R₁ = {(a₁, d₂), (a₂, d₂)}` — both are new provenance entries from the K.ρ step. For each, the address must be new to d₂'s content-subspace range: `a₁ ∈ ran(M₂(d₂)|_{s_C}) = {a₁, a₂}` and `a₁ ∉ ran(M₁(d₂)|_{s_C}) = ∅` (M₁(d₂) = ∅), and symmetrically for a₂. Both entries are anchored in content-subspace range extensions introduced by the K.μ⁺ step of this composite. (J1'★ reduces to J1' of the four-component model in this example, since no link-subspace positions exist; the ★ label is used throughout the worked examples for uniform notation.) ✓
- *J4:* d₂ ∈ E₂_doc \ E₁_doc, ran(M₂(d₂)) = {a₁, a₂} ⊆ ran(M₁(d₁)). ✓
- *P4:* Contains(Σ₂) = {(a₁, d₁), (a₂, d₁), (a₁, d₂), (a₂, d₂)} ⊆ R₂. ✓
- *P5:* C₂ = C₁; E₂ ⊇ E₁; R₂ ⊇ R₁. Only M changed. ✓
- *P7a:* dom(C₂) = dom(C₁) = {a₁, a₂}; both a₁ and a₂ have provenance entries (a₁, d₁), (a₂, d₁) ∈ R₁ ⊆ R₂. ✓
- *P8:* parent(d₂) = parent(1.0.1.0.2) = 1.0.1 ∈ E₁ ⊆ E₂. The existing non-node entity 1.0.1 (account) retains parent(1.0.1) = 1 ∈ E₂. ✓
- *Frame-preserved invariants:* P0 (dom(C₂) ⊇ dom(C₁) with values fixed), P1 (E₂ ⊇ E₁), P2 (R₂ ⊇ R₁), P6 (origin of every a ∈ dom(C₂) = dom(C₁) lies in E₁ ⊆ E₂), P7 (every (a, d) ∈ R₂ \ R₁ has a ∈ dom(C₂) by J1 and inductive hypothesis), S2/S3/S8a/S8-depth/S8-fin/D-CTG/D-MIN (arrangement-invariants lemma applied to the K.δ + K.μ⁺ + K.ρ composite).

**Insert new content into d₂.** Compound K.α + K.μ⁺ + K.ρ.

*K.α:* Allocate a₃ = 1.0.1.0.2.0.1.1 with C₃(a₃) = '!'. The address falls under d₂'s prefix (S7a): origin(a₃) = 1.0.1.0.2 = d₂. By GlobalUniqueness, a₃ is fresh.

*K.μ⁺:* M₃(d₂) = M₂(d₂) ∪ {[1,3] ↦ a₃}. V-position [1,3] has first component 1 and depth 2, matching [1,1] and [1,2] (S8-depth, non-vacuously: shared first component). Referential integrity: a₃ ∈ dom(C₃) (S3). ✓

*K.ρ:* R₃ = R₂ ∪ {(a₃, d₂)}.

Verification:

- *J0:* a₃ ∈ dom(C₃) \ dom(C₂), and d₂ ∈ E₃_doc with M₃(d₂)([1,3]) = a₃. ✓
- *J1★:* ran(M₃(d₂)|_{s_C}) \ ran(M₂(d₂)|_{s_C}) = {a₃} (content-subspace only; J1★ reduces to J1 here), and (a₃, d₂) ∈ R₃. ✓
- *J1'★:* `R₃ \ R₂ = {(a₃, d₂)}` — the K.ρ step adds exactly this entry. The address `a₃` is new to d₂'s content-subspace range: `a₃ ∈ ran(M₃(d₂)|_{s_C}) = {a₁, a₂, a₃}` and `a₃ ∉ ran(M₂(d₂)|_{s_C}) = {a₁, a₂}`. The new provenance is anchored in the K.μ⁺ step's content-subspace range extension. ✓
- *P4:* Contains(Σ₃) adds (a₃, d₂); this pair is in R₃. ✓
- *P6:* origin(a₃) = d₂ = 1.0.1.0.2 ∈ E₃_doc. ✓
- *P7:* (a₃, d₂) ∈ R₃ and a₃ ∈ dom(C₃). ✓
- *P7a:* dom(C₃) = {a₁, a₂, a₃}; a₁ and a₂ retain provenance from R₂ ⊆ R₃, and a₃ has new provenance (a₃, d₂) ∈ R₃. Every a ∈ dom(C₃) has at least one provenance entry. ✓
- *Frame-preserved invariants:* P0 (dom(C₃) ⊇ dom(C₂) with values fixed), P1 (E₃ = E₂), P2 (R₃ ⊇ R₂), P5 (C₃ ⊇ C₂, R₃ ⊇ R₂, E₃ = E₂ — extensions only), P8 (E₃ = E₂, no new non-node entities), S2/S3/S8a/S8-depth/S8-fin/D-CTG/D-MIN (arrangement-invariants lemma).

**Delete a₃ from d₂'s arrangement (K.μ⁻).** Remove the mapping at V-position [1,3] — the maximum end of V_{s_C}(d₂), satisfying the K.μ⁻ amendment's D-CTG/D-MIN postcondition.

*K.μ⁻:* dom(M₄(d₂)) = {[1,1], [1,2]} ⊂ dom(M₃(d₂)) = {[1,1], [1,2], [1,3]}. The surviving mappings are unchanged: M₄(d₂)([1,1]) = a₁, M₄(d₂)([1,2]) = a₂. D-MIN: min(V_1(d₂)) = [1,1] = [s_C, 1]. D-CTG: {[1,1], [1,2]} is contiguous.

Verification:

- *J2:* C₄ = C₃; E₄ = E₃; R₄ = R₃. All permanent and historical state unchanged. ✓
- *J1'★ (vacuous):* `R₄ \ R₃ = ∅` since K.μ⁻ holds R in frame. There are no new provenance entries to check; J1'★ is vacuously satisfied. ✓
- *P4:* Contains(Σ₄) = {(a₁, d₁), (a₂, d₁), (a₁, d₂), (a₂, d₂)}. The pair (a₃, d₂) is no longer in Contains — d₂ no longer displays a₃. Yet (a₃, d₂) ∈ R₄: the stale entry persists. Contains(Σ₄) ⊂ Contains(Σ₃), while R₄ = R₃. ✓
- *P5:* C₄ = C₃; E₄ = E₃; R₄ = R₃. Only M changed. ✓
- *P7a:* dom(C₄) = dom(C₃) and R₄ = R₃ (frame); every a ∈ dom(C₄) retains its provenance entry from R₃. ✓
- *Frame-preserved invariants:* P0/P1/P2 (no extensions, just M contraction), P6 (origin of every a ∈ dom(C₄) = dom(C₃) lies in E₄ = E₃), P7 ((a, d) ∈ R₄ = R₃ with a ∈ dom(C₄) = dom(C₃)), P8 (E₄ = E₃), S2/S3/S8a/S8-depth/S8-fin/D-CTG/D-MIN (arrangement-invariants lemma — K.μ⁻ at the maximum end preserves contiguity and minimum).

The divergence is now concrete: R₄ records that d₂ once contained a₃, while the current arrangement does not. This is the historical memory that J2 preserves — deletion is purely presentational.

**Reorder d₂'s arrangement (K.μ~).** Swap V-positions [1,1] and [1,2].

*K.μ~:* The bijection π : {[1,1], [1,2]} → {[1,1], [1,2]} with π([1,1]) = [1,2] and π([1,2]) = [1,1]. The definition requires M₅(d₂)(π(v)) = M₄(d₂)(v) for all v ∈ dom(M₄(d₂)), giving M₅(d₂) = {[1,1] ↦ a₂, [1,2] ↦ a₁}. Both target V-positions satisfy S8a (all components strictly positive) and S8-depth (uniform depth 2, shared first component 1).

Verification:

- *J3:* C₅ = C₄; E₅ = E₄; R₅ = R₄. All permanent and historical state unchanged. ✓
- *J1'★ (vacuous):* `R₅ \ R₄ = ∅` since K.μ~ holds R in frame. There are no new provenance entries to check; J1'★ is vacuously satisfied. ✓
- *ran preservation:* ran(M₅(d₂)) = {a₁, a₂} = ran(M₄(d₂)). The multiset of referenced I-addresses is identical; only V-positions changed. ✓
- *P4:* Contains(Σ₅) = Contains(Σ₄) ⊆ R₄ = R₅. Since ran is preserved for d₂ and no other arrangement changed, the current containment set is unchanged. ✓
- *P5:* C₅ = C₄; E₅ = E₄; R₅ = R₄. Only M changed. ✓
- *P7a:* dom(C₅) = dom(C₄) and R₅ = R₄ (frame); every a ∈ dom(C₅) retains its provenance entry. ✓
- *Frame-preserved invariants:* P0/P1/P2 (frame), P6, P7, P8 (E₅ = E₄), S2/S3/S8a/S8-depth/S8-fin/D-CTG/D-MIN (arrangement-invariants lemma — K.μ~'s subspace-preserving precondition forces V_{s_C}(d₂') = V_{s_C}(d₂), so contiguity and minimum are preserved).

Reordering is the simplest transition to verify: it touches nothing beyond the V-position mapping, and all invariants hold by the frame conditions alone.

The four steps exercise J0, J1, J2, J3, J4, P4, P5, P6, P7, P7a, and P8 — covering every invariant of the four-component reachable-state theorem either explicitly or via the frame-preserved annotations — and demonstrate M(d) = ∅ for freshly created documents (by totality of M) (J1 verification of the fork), the divergence between current containment and historical provenance (J2 verification of the deletion), and the presentational isolation of reordering (J3 verification of the swap).


## Worked example: interior content replacement

We trace the interior-position case of the content-replacement decomposition (K.μ⁻ + K.μ⁺ with `n'_{s_C} = k₀ − 1` rather than the single-position pair at `k₀ = n_{s_C}`) introduced in the *Elementary transitions* section. The example exercises the multi-position K.μ⁻ + K.μ⁺ pair, the intermediate-state admissibility verification at M_int, the K.μ⁺ amendment's content-subspace restriction on the rebuild, and the asymmetric coupling of J1★ and J1'★ to new versus re-added addresses at the composite boundary.

*Initial state.* Let document `d = 1.0.1.0.1` have four content-subspace mappings, with `aₖ := 1.0.1.0.1.0.1.k` for `k ∈ {1, 2, 3, 4}`:

> C ⊇ {a₁ ↦ char₁, a₂ ↦ char₂, a₃ ↦ char₃, a₄ ↦ char₄}
> M(d) = {[1,1] ↦ a₁, [1,2] ↦ a₂, [1,3] ↦ a₃, [1,4] ↦ a₄}
> R ⊇ {(a₁, d), (a₂, d), (a₃, d), (a₄, d)}

Content-subspace V-positions: `V_{s_C}(d) = {[1,1], [1,2], [1,3], [1,4]}` — contiguous (D-CTG★), minimum `[1,1] = [s_C, 1]` (D-MIN★), uniform depth 2 (S8-depth), structural form `{[s_C, 1, k] : 1 ≤ k ≤ 4}` (D-SEQ★ at `n_{s_C} = 4`). Link subspace: `V_{s_L}(d) = ∅`. The four pre-state provenance entries are assumed established by prior J0/J1★ couplings at d's initial population (the details are not material here).

**Goal.** Replace the I-address at the interior V-position `[1,2]` with a freshly allocated `a₂' ≠ a₂` of new content value. Positions `[1,3]` and `[1,4]` lie strictly above `[1,2]` under the V-ordering on `s_C` (T1 of ASN-0034 restricted to depth-2 positive tuples with first component 1), so a single-position K.μ⁻ + K.μ⁺ pair at `[1,2]` alone would leave `V_{s_C}(d)` with a gap at `[1,2]` between `[1,1]` and `[1,3]` at the intermediate state — case (b) of the K.μ⁻ admissibility analysis, forbidden by D-CTG★. The replacement therefore decomposes as a multi-position K.μ⁻ removing the suffix from `[1,2]` upward, followed by K.α allocating `a₂'`, then a multi-position K.μ⁺ rebuilding the suffix with `a₂'` at `[1,2]` and the previously-mapped `a₃, a₄` at `[1,3], [1,4]`, and finally K.ρ recording the new provenance — four elementary steps in this order. (An alternative valid ordering, K.α before K.μ⁻, produces the same composite endpoints; the order chosen here keeps the K.μ⁻ removal at the head of the trace, matching the narrative of "interior replacement = remove suffix, then rebuild.")

**Step 1: K.μ⁻ — remove the interior suffix `{[1,2], [1,3], [1,4]}`.** Effect: `M_int(d) = {[1,1] ↦ a₁}`. Frame: `C_int = C`, `L_int = L`, `E_int = E`, `R_int = R`.

*Admissibility (per-subspace).*
- *Content subspace.* `V_{s_C}(d) = {[1,1], [1,2], [1,3], [1,4]}` shrinks to `V_{s_C}(d_int) = {[1,1]}` — case-(a) partial suffix removal with `n'_{s_C} = 1`; the removed set `{[s_C, 1, k] : 1 < k ≤ 4}` is exactly the n'_{s_C} = 1 suffix in the D-SEQ★-shaped pre-state.
- *Link subspace.* `V_{s_L}(d) = V_{s_L}(d_int) = ∅` — vacuous (case-(a) zero-suffix at `n'_{s_L} = n_{s_L} = 0`).

At least one subspace contracts strictly (content: 4 → 1), so the effect clause `dom(M_int(d)) ⊂ dom(M(d))` is satisfied at the whole-arrangement level. K.μ⁻ commits.

*Intermediate-state verification at M_int.* The decomposition routes the composite through M_int, which must itself satisfy the per-state invariant set.
- *D-CTG★ at M_int:* `V_{s_C}(d_int) = {[1,1]}` is a singleton — vacuously contiguous under the V-ordering on `s_C` (no two distinct members bracket an interval). ✓
- *D-MIN★ at M_int:* `min(V_{s_C}(d_int)) = [1,1] = [s_C, 1]` of depth `m_{s_C} = 2`. ✓
- *D-SEQ★ at M_int:* `V_{s_C}(d_int) = {[s_C, 1, 1]}` matches `{[s_C, 1, ..., 1, k] : 1 ≤ k ≤ 1}` at `n_{s_C} = 1`. ✓
- *S2, S3, S8a, S8-depth, S8-fin at M_int:* the surviving mapping `[1,1] ↦ a₁` is functional, has all-positive components and uniform depth 2 in `s_C`, with `a₁ ∈ dom(C_int) = dom(C)`. ✓
- *Frame-preserved invariants at M_int:* P0/P1/P2/P6/P7/P7a/P8 preserved by K.μ⁻'s frame on C, E, R; P4 specifically — `Contains(Σ_int) = {(a₁, d), ...}` is a subset of `Contains(Σ) ⊆ R = R_int`, since K.μ⁻ can only shrink Contains by J2. The pairs `(a₂, d), (a₃, d), (a₄, d)` exit Contains at this step but remain in R as stale entries (the divergence J2 institutionalises). ✓

**Step 2: K.α — allocate the replacement address `a₂'`.** Allocate `a₂' = 1.0.1.0.1.0.1.5 = inc(a₄, 0)` (the next sibling on d's content sub-allocator's frontier under TA5(c)) with `C'(a₂') = char₂'` for some new content value. Effect: `C' = C ∪ {a₂' ↦ char₂'}`. Frame: L, E, M (= M_int), R unchanged.

Preconditions: IsElement(a₂') (zeros = 3, element-field `[1, 5]`); origin(a₂') = `1.0.1.0.1` = d ∈ E_doc; `fields(a₂').E₁ = 1 = s_C`; `a₂' ∉ dom(C)` by GlobalUniqueness (T10a) on the content sub-allocator's inc chain; `a₂' ∉ dom(L) = ∅` vacuously. ✓

**Step 3: K.μ⁺ — rebuild the suffix `{[1,2] ↦ a₂', [1,3] ↦ a₃, [1,4] ↦ a₄}`.** Effect: `M_post(d) = {[1,1] ↦ a₁, [1,2] ↦ a₂', [1,3] ↦ a₃, [1,4] ↦ a₄}`. Frame: C', L, E, R unchanged.

Preconditions at the post-K.α intermediate state:
- *d ∈ E_doc; disjoint extension; value preservation.* New positions `{[1,2], [1,3], [1,4]}` are disjoint from `dom(M_int(d)) = {[1,1]}`; the existing mapping at `[1,1]` retains its value `a₁`. ✓
- *K.μ⁺ amendment (content-subspace restriction).* Each new V-position has `subspace(v) = s_C` — first components of `[1,2], [1,3], [1,4]` are all `1 = s_C`. ✓ The amendment is the operative gate that scopes the rebuild to the content subspace; on a state with a non-empty link subspace, the same K.μ⁻ + K.μ⁺ replacement pair would re-add only content-subspace positions, leaving the link subspace untouched.
- *Referential integrity (S3 content clause).* `a₂' ∈ dom(C')` (post-K.α); `a₃, a₄ ∈ dom(C) ⊆ dom(C')` by P0 frame on the prior content addresses. ✓
- *S8a, S8-depth, S8-fin on M_post.* New positions have all strictly positive components; `V_{s_C}(d_post) = {[1,1], [1,2], [1,3], [1,4]}` of uniform depth 2; cardinality 4 < ∞. ✓
- *D-CTG★, D-MIN★ on M_post.* `V_{s_C}(d_post)` is contiguous under the V-ordering on `s_C` (every depth-2 positive tuple with first component 1 lex-between `[1,1]` and `[1,4]` — i.e., `[1,2]` and `[1,3]` — is present), with `min = [1, 1] = [s_C, 1]`. ✓

**Step 4: K.ρ — record provenance for the new address.** Effect: `R' = R ∪ {(a₂', d)}`. Preconditions: `a₂' ∈ dom(C')` (post-K.α); `d ∈ E_doc`. ✓

**Composite verification at Σ → Σ'.**

Net change across the composite:
- `dom(C') \ dom(C) = {a₂'}` — one new content address.
- `dom(M'(d)) = dom(M(d)) = {[1,1], [1,2], [1,3], [1,4]}` — the V-position domain returns to its pre-state shape after the K.μ⁻ + K.μ⁺ round-trip.
- `ran(M'(d)|_{s_C}) \ ran(M(d)|_{s_C}) = {a₁, a₂', a₃, a₄} \ {a₁, a₂, a₃, a₄} = {a₂'}` — only `a₂'` is new to d's content-subspace range; `a₃` and `a₄` are re-added but were already in the pre-state range.
- `R' \ R = {(a₂', d)}` — one new provenance entry.

Coupling verification:
- *J0.* `a₂' ∈ dom(C') \ dom(C)`, and the placement clause is witnessed by `M'(d)([1,2]) = a₂'` at d ∈ E'_doc. ✓
- *J1★ (new-address coupling).* `ran(M'(d)|_{s_C}) \ ran(M(d)|_{s_C}) = {a₂'}`, and `(a₂', d) ∈ R'` from K.ρ. The re-added addresses `a₃` and `a₄` are *not* new to d's content-subspace range — they appear in both the pre-state range and the post-state range — so J1★ does not require fresh provenance for them, even though they pass through the K.μ⁻ + K.μ⁺ cycle internally. J1★ is range-based and evaluated only between Σ and Σ', so the intermediate dispossession at M_int is invisible to the coupling. ✓
- *J1'★ (new-provenance check; vacuity on re-added addresses).* The single new provenance entry `(a₂', d) ∈ R' \ R` corresponds to `a₂'` being new to d's content-subspace range (`a₂' ∈ ran(M'(d)|_{s_C}) ∧ a₂' ∉ ran(M(d)|_{s_C})`). *Vacuity on re-added addresses:* `a₃` and `a₄` pass through the K.μ⁻ + K.μ⁺ cycle but generate no entries in `R' \ R` — the pre-existing `(a₃, d), (a₄, d) ∈ R` carry through by P2, no fresh K.ρ is invoked for them, and J1'★ therefore has nothing to check for them at the composite boundary. The asymmetry between J1★'s and J1'★'s handling of re-added addresses is the operative content of this example: K.μ⁻ + K.μ⁺ on a previously-arranged address is *transparent* to provenance coupling, because the provenance bookkeeping is tied to content novelty in the range rather than to V-position movement in the domain. ✓

Post-state invariant verification:
- *P4 (Contains ⊆ R).* `Contains(Σ') ⊇ {(a₁, d), (a₂', d), (a₃, d), (a₄, d)}`; each pair is in R' — `(a₁, d), (a₃, d), (a₄, d) ∈ R ⊆ R'` by P2, and `(a₂', d) ∈ R'` by K.ρ. The stale pair `(a₂, d) ∈ R' \ Contains(Σ')` records that d once contained `a₂`, the historical fact that survives the replacement. ✓
- *P6 (Existential coherence).* `origin(a₂') = d ∈ E_doc`; pre-existing content addresses retain their origin entities by frame. ✓
- *P7 (Provenance grounding).* `(a₂', d) ∈ R'` has `a₂' ∈ dom(C')`; pre-existing R entries retain their grounding by P0. ✓
- *P7a (Provenance coverage).* every `a ∈ dom(C')` has at least one provenance entry — `a₁, a₂, a₃, a₄` retain their pre-state entries (R ⊆ R' by P2), and `a₂'` has the freshly added `(a₂', d)`. ✓
- *D-CTG, D-MIN at Σ'.* `V_{s_C}(d') = {[1,1], [1,2], [1,3], [1,4]}` contiguous, minimum `[1,1] = [s_C, 1]`. ✓
- *Per-transition (P0/P1/P2).* `dom(C) ⊆ dom(C')` with values fixed (K.α extends, all other steps frame C); `E = E'` (no entity allocation in this composite); `R ⊆ R'` (K.ρ extends, all other steps frame R). ✓
- *Frame-preserved invariants:* S2 (functionality preserved at every step), S3 (every value in dom(C')), S4/S7a–c (the new address `a₂'` satisfies the allocator discipline; pre-existing addresses retain their identity), S8 (foundation-level finite-span decomposition holds by the arrangement-invariants lemma), P5 (extension-only on C and R; M's V-position domain returns to its pre-state shape but its range changes — P5 governs C, L, E, R, all of which are extension-only), P8 (no new non-node entities).

This example concretely realises the *interior* case of the content-replacement decomposition catalogued in the *Elementary transitions* section: the multi-position K.μ⁻ + K.μ⁺ pair with three positions rebuilt (`n_{s_C} − k₀ + 1 = 4 − 2 + 1 = 3`) rather than the single-position pair at the subspace maximum. The contrast with the fork-with-insertion example above — where K.μ⁻ at `[1,3]` is a single-position suffix at the subspace maximum — exhibits both branches of the per-position case analysis in the *Elementary transitions* section ("Replacement at the maximum position" and "Replacement at an interior position"). The intermediate-state verification at M_int — a singleton arrangement at which every per-state invariant must independently hold — illustrates the general discipline that any K.μ⁻ + K.μ⁺ composite (replacement, reordering, or arbitrary rebuild) must routes its admissibility through the intermediate state's invariants. The asymmetric J1★/J1'★ handling of re-added addresses — fresh provenance for novel range elements, vacuous discharge for round-tripped ones — is the mechanism by which the provenance accumulation stays tied to content novelty rather than to arrangement choreography.


## Worked example: ghost-base document versioning

The K.δ k = 1 sub-case admits, under the *Scope and base-liveness* analysis above, an inc operand `t` that is *not* required to be in E_doc — the ghost-base versioning case. We trace a concrete instance to verify (i) that K.δ proceeds without `t ∈ E_doc`, (ii) that P8 holds at the new version through `parent(·)` rather than through `t`, (iii) that subsequent same-account versions allocated as k = 0 siblings under that account require their inc operand to be in E (and hence chain through live intermediates), and (iv) that any attempt to repeat the ghost-base step at the same `(t, 1)` pair is blocked by T10a's at-most-once combined with the `e ∉ E` precondition of K.δ.

*Initial state.* Let Σ₆ contain node `1`, account `1.0.1`, and the document `d₁ = 1.0.1.0.1` from the prior worked example, but *not* the document at address `1.0.1.0.5`:

> E₆ = {1, 1.0.1, 1.0.1.0.1}

Define the *ghost* document address `t = 1.0.1.0.5` — a valid document tumbler (IsDocument(t): zeros(t) = 2, ValidAddress(t)) that has never been allocated, so `t ∉ E₆`. The address may have been issued externally by an actor inside `1.0.1`'s ownership domain, may be a hypothesised future allocation, or may be entirely fictive in the Nelson ghost-element sense (LM 4/23) — at the abstract level, the only structural fact about `t` that K.δ's k = 1 sub-case relies on is `IsDocument(t)`. We take `T₆` (T10a's universe of allocated tumblers) to include `t` — the address has been issued at the tumbler-allocation layer (so T10a's GlobalUniqueness governs subsequent inc operations on it) without the corresponding entity record being created in E. In Gregory's terms this corresponds to a granfilade slot that has been claimed at the namespace layer but where the document's bert record was never created or has been demoted.

**Step 1: K.δ — allocate the first version from the ghost base.** Apply K.δ case (ii) with `t = 1.0.1.0.5 ∉ E_doc` and `k = 1`, producing `e₁ = inc(t, 1) = 1.0.1.0.5.1`.

*Precondition discharge.*
- *`parent(e₁) ∈ E`:* parent(`1.0.1.0.5.1`) truncates back to the last zero-separator boundary. Since `e₁` has zeros = 2 (the trailing `.1` adds no separator under k = 1), parent strips the trailing tumbler-length extension at the document level back to the account: parent(e₁) = `1.0.1` ∈ E₆. ✓ The K.δ precondition `parent(e) ∈ E` is independent of whether `t ∈ E`.
- *`e₁ = inc(t, k)` for some `t ∈ T` with `k ∈ {0, 1, 2}`:* `t = 1.0.1.0.5 ∈ T₆`; `k = 1`. ✓ (T10a's quantifier is over `T`, not `E`.)
- *`k = 1 ⟹ IsDocument(t)`:* IsDocument(`1.0.1.0.5`) holds (zeros = 2, terminal positive). ✓
- *`e₁ ∉ E`:* `e₁ = 1.0.1.0.5.1` is fresh to E₆ by direct inspection: E₆ = {1, 1.0.1, 1.0.1.0.1} does not contain `1.0.1.0.5.1`. ✓ The discharge here is *K.δ precondition + TA5 determinism*, not T10a: because `t = 1.0.1.0.5 ∉ E_doc` (ghost), T10a's GlobalUniqueness does not apply (T10a underwrites freshness only when the operand inhabits some T10a allocator's domain, and the ghost operand by stipulation lies outside every entity allocator's domain). TA5 (ASN-0034) supplies the structural exhibition `inc(t, 1) = t.1 = 1.0.1.0.5.1` from t alone (TA5(b) + TA5(d) at k = 1), and the K.δ precondition `e ∉ E` is then discharged by inspection against E₆. This is the third of the three `e ∉ E` discharge paths catalogued in K.δ's *Discharge of `e ∉ E` in the ghost-operand case* above.
- *Note: the k = 1 sub-case does not require `t ∈ E`.* This is the ghost-base relaxation under analysis. The case admits `t ∉ E_doc` per the *Scope and base-liveness* discussion above.

*Effect.* E₇ = E₆ ∪ {`1.0.1.0.5.1`}; M₇(`1.0.1.0.5.1`) = ∅ (K.δ for documents). C₇ = C₆; L₇ = L₆; R₇ = R₆; for every d' ≠ `1.0.1.0.5.1`, M₇(d') = M₆(d').

*Verification against Σ₇.*
- *P8:* The new entity `1.0.1.0.5.1` is non-node (zeros = 2); P8 requires `parent(1.0.1.0.5.1) ∈ E₇`. parent(`1.0.1.0.5.1`) = `1.0.1` ∈ E₆ ⊆ E₇. ✓ Critically, P8 is discharged through `parent(e₁)` rather than through `t`: the inductive spine traverses zero-separator boundaries upward to the account `1.0.1`, never visiting the ghost document `t = 1.0.1.0.5`. The version's existence does *not* require its base to be in E — the parent chain skips past the depth-1 base directly to the depth-2 enclosing account. (As noted in K.δ's *Scope and base-liveness*: "the version step `[N,0,U,0,D] → [N,0,U,0,D,k]` crosses no zero separator, so `parent(e) = parent(t)`, and `parent(e) ∈ E` is itself a K.δ precondition (independent of whether t is in E).") Every other non-node entity in E₇ retains its pre-state parent in E₇ ⊇ E₆. ✓
- *NodeUniqueAllocation (vacuous):* K.δ at k = 1 with non-node t produces a non-node entity (zeros(e₁) = 2 = zeros(t), still IsDocument); no node-allocation event. ✓
- *NodeLineage:* Holds frame-preserved for all existing nodes; `e₁` is not a node, so the universal quantifier extends vacuously over `e₁`. ✓
- *P0/P1/P2/P5/P6/P7/P7a:* Frame-preserved by K.δ's frame on C, R and the extension-only effect on E. ✓
- *S0–S9, L0–L14:* Frame-preserved by K.δ's frame on C, L, M, R. The new document `1.0.1.0.5.1` has M₇(`1.0.1.0.5.1`) = ∅, so all arrangement-side invariants (S2, S3★, S3★-aux, S8a, S8-depth, S8-fin, S8, D-CTG★, D-MIN★, D-SEQ★, CL-OWN, CL-UNIQ) hold vacuously at the new document. ✓
- *J0–J4 (vacuous at K.δ for documents):* No content allocation (J0 vacuous), no arrangement extension (J1, J1'★ vacuous), no removal (J2 vacuous), no reordering (J3 vacuous), no fork-with-content (J4 vacuous: ran(M₇(`1.0.1.0.5.1`)) = ∅ trivially satisfies any subset relation; the J4 fork shape applies when the K.δ is composed with a content-introducing K.μ⁺, which is not the case here). ✓

**Step 2: K.δ — chain a second version as a k = 0 sibling of e₁.** To allocate `e₂ = 1.0.1.0.5.2 = inc(e₁, 0)`, apply K.δ case (ii) with `t = e₁ = 1.0.1.0.5.1` and `k = 0`.

*Precondition discharge.*
- *`parent(e₂) ∈ E`:* parent(`1.0.1.0.5.2`) = `1.0.1` (the depth-2 account) ∈ E₇. ✓
- *`e₂ = inc(t, k)` with `t ∈ T`*: `t = 1.0.1.0.5.1 ∈ T₈` (allocated at Step 1). ✓
- *`t ∈ E` (required for k ∈ {0, 2}):* `t = e₁ ∈ E₇`. ✓ This is the load-bearing precondition that distinguishes the k = 0 sibling step from the ghost-tolerant k = 1 step: at k = 0 the inc operand must inhabit the entity set, so chains of versions allocated *as k = 0 siblings* anchor on live intermediates by construction.
- *`e₂ ∉ E`:* fresh by T10a's GlobalUniqueness on the `(1.0.1.0.5.1, 0)` event. ✓
- *Sibling discipline:* parent(e₂) = parent(t) = `1.0.1`; zeros(e₂) = zeros(t) = 2; the two share parent `1.0.1` at the same level. ✓

*Effect.* E₈ = E₇ ∪ {`1.0.1.0.5.2`}; M₈(`1.0.1.0.5.2`) = ∅. All other components frame.

*Verification.* P8: parent(`1.0.1.0.5.2`) = `1.0.1` ∈ E₈. ✓ The chain `1.0.1.0.5.1 → 1.0.1.0.5.2` is *not* itself on the parent spine (both have parent `1.0.1`); the version-chain relationship belongs to the deferred version-lineage semantics noted at K.δ. Arrangement-side and provenance-side invariants verify vacuously as in Step 1 (M₈(`1.0.1.0.5.2`) = ∅). ✓

**Step 3 (counterfactual): a second K.δ with `(t, 1) = (1.0.1.0.5, 1)` is blocked.** Suppose, after Step 1, an attempt is made to allocate a second entity by `inc(1.0.1.0.5, 1)`. We show that two independent guardrails — T10a's at-most-once on a given `(operand, k)` pair, and K.δ's `e ∉ E` precondition — concur to reject the attempt.

*T10a-side rejection.* T10a's GlobalUniqueness (ASN-0034) governs the inc operator: for any `(t, k)` pair with `t ∈ T` and `k ∈ {0, 1, 2}`, the address `inc(t, k)` is uniquely determined and constitutes a single allocation event at the tumbler-allocation layer. T10a does not admit a second distinct address `e₁' ≠ e₁` from a repeated `inc(1.0.1.0.5, 1)`: inc is deterministic in its operands, and the at-most-once allocation event at `(t, 1)` was consumed when `e₁ = 1.0.1.0.5.1` was emitted at Step 1. The candidate `e₁' = inc(1.0.1.0.5, 1)` therefore *equals* `e₁ = 1.0.1.0.5.1` — there is no second address to allocate.

*K.δ-side rejection.* K.δ's `e ∉ E` precondition then settles the matter at the entity-allocation layer: the candidate address `e₁ = 1.0.1.0.5.1` is in E₇ (from Step 1) and remains in E₈ (E is monotone under all transitions); hence `e₁ ∉ E₈` is false, and K.δ's precondition fails. The transition is rejected.

*Composite reading.* The two guardrails are not redundant — they reject the attempt at distinct layers and would each suffice in isolation. T10a establishes that no *new distinct address* can arise from a repeated `(t, 1)` inc event; K.δ establishes that the *one address* that does arise (`e₁`) cannot be re-emitted into E because it is already there. Together they close the question of "how many version-1 entities can be allocated from the ghost base `1.0.1.0.5`?" at exactly one.

A symmetric counterfactual, attempting `inc(e₁, 1) = 1.0.1.0.5.1.1`, would *not* be blocked at the tumbler layer (the `(e₁, 1)` pair is fresh) and would be admissible under K.δ if all preconditions held — including IsDocument(`1.0.1.0.5.1.1`). However, IsDocument requires zeros = 2 (per ASN-0045's level discipline), and `1.0.1.0.5.1.1` has zeros = 2 (no new zero-separator from the k = 1 extension), so IsDocument holds. The candidate is structurally admissible as a *version of the first version* `e₁`. Whether the design *admits* version-of-version semantics belongs to the deferred version-lineage discussion at K.δ; the present ASN's elementary set does not prohibit it at the structural layer.

**Synthesis.** The four-step sequence (Step 1: ghost-base k = 1; Step 2: live-base k = 0 chain; Step 3: counterfactual repeated k = 1) confirms the K.δ design points:

- *Ghost-base initial versioning is admitted at the abstract level* — the inc operand at k = 1 need not be in E_doc; P8 is discharged through parent(·) at the depth-2 account, bypassing the depth-1 base.
- *Intermediate version-chain liveness is enforced* — k = 0 sibling allocations require their operand in E, so subsequent versions anchor on live predecessors (the relaxation applies only to the initial version step from a ghost base).
- *T10a's at-most-once combines with K.δ's `e ∉ E` to bound `(ghost, 1)` to a single version* — the ghost base does not admit multiple distinct "first versions"; precisely one entity is allocated by the `(t, 1)` inc event, and any subsequent attempt is rejected at both the tumbler-allocation and entity-allocation layers.

The example exercises K.δ in both its k = 1 (ghost-tolerant, document-restricted) and k = 0 (live-required) sub-cases, NodeUniqueAllocation and NodeLineage in their vacuous form (no node events), P8 at the parent-spine discharge under a ghost-base intermediate, and T10a's interaction with K.δ at the version-base boundary. The arrangement-side invariants are exercised only vacuously here (each new document has M(d) = ∅); their non-vacuous exercise is the subject of the *link allocation and arrangement* worked example below.


## Worked example: link allocation and arrangement

We verify the central postconditions on concrete tumbler values. Let `s_C = 1` and `s_L = 2` (satisfying SC-NEQ: `1 ≠ 2`). Consider document `d` at address `1.0.1.0.1` with two text content addresses allocated and arranged.

*Initial state.* `dom(C) = {1.0.1.0.1.0.1.1, 1.0.1.0.1.0.1.2}`, `dom(L) = ∅`, `E_doc = {1.0.1.0.1}`, `R = {(1.0.1.0.1.0.1.1, d), (1.0.1.0.1.0.1.2, d)}` (implicit from prior J0/J1 of allocation).

Arrangement: `M(d) = {[1,1] ↦ 1.0.1.0.1.0.1.1, [1,2] ↦ 1.0.1.0.1.0.1.2}`.

Text-subspace V-positions: `V_1(d) = {[1,1], [1,2]}` — contiguous (D-CTG), minimum at `[1,1]` (D-MIN), depth 2 (S8-depth). Link subspace: `V_2(d) = ∅`.

**Step 1: K.λ — allocate link.** Create link `ℓ = 1.0.1.0.1.0.2.1` with value `(F, G, Θ)`.

Precondition verification:
- `d = 1.0.1.0.1 ∈ E_doc`
- `ℓ ∉ dom(L) ∪ dom(C)`: `dom(L) = ∅`; content addresses have element field `1.1` and `1.2` (subspace 1), while ℓ has element field `2.1` (subspace 2) — by T7 and SC-NEQ, disjoint
- `zeros(ℓ) = 3`: zeros at positions 2, 4, 6 in the tumbler `1.0.1.0.1.0.2.1`
- `fields(ℓ).E₁ = 2 = s_L`
- `origin(ℓ) = 1.0.1.0.1 = d`
- Forward allocation: no prior links in dom(L) with origin d, so vacuously satisfied
- `(F, G, Θ) ∈ Link` by assumption (L3)

Effect: `L' = {1.0.1.0.1.0.2.1 ↦ (F, G, Θ)}`. Frame: C, E, M, R unchanged.

Post-state verification:
- L14: `dom(C) ∩ dom(L') = ∅` — content addresses have `fields(a).E₁ = 1`, link has `fields(ℓ).E₁ = 2`, and `1 ≠ 2`
- L0: all dom(L') addresses have subspace s_L = 2; all dom(C) addresses have subspace s_C = 1
- L3: `L'(ℓ) = (F, G, Θ)` with `F, G, Θ ∈ Endset`
- L-fin: `dom(L') = {ℓ}` is a singleton, hence finite. ✓
- S3★, CL-OWN: M unchanged, hold from pre-state
- *P3★:* K.λ extends L only; C, E, M, R are held in frame (no contraction or value rewriting on any non-M component). ✓
- *P7a:* dom(C) is unchanged; every a ∈ dom(C) retains its provenance entry from R. ✓
- *J1'★ (vacuous):* K.λ holds R in frame, so `R' \ R = ∅`. No new provenance entries to check; J1'★ is vacuously satisfied. ✓
- *Frame-preserved invariants:* P0/P1/P2/P5★/P6/P7/P8/S2/S3★-aux/S4/S7a–d/S8a/S8-depth/S8-fin/S8/S9/D-CTG★/D-MIN★/D-SEQ★ — none of C, E, M, or R changed, and K.λ's effect is restricted to L.

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
- *P3★:* K.μ⁺_L extends M only; C, L, E, R are held in frame. ✓
- *P7a:* dom(C) is unchanged; every a ∈ dom(C) retains its provenance entry from R. ✓
- *J1'★ (vacuous):* K.μ⁺_L holds R in frame, so `R' \ R = ∅`. The new M extension is link-subspace only (`subspace(v_ℓ) = s_L`), so the content-subspace range `ran(M'(d)|_{s_C})` is unchanged — no provenance coupling is triggered, consistent with J1'★'s content-subspace scoping. ✓
- *Frame-preserved invariants:* P0/P1/P2/P5★/P6/P7/P8/S2 (functionality preserved by disjoint extension at new V-position)/S3★-aux/S4/S7a–d/S8a/S8-fin/S8-depth/S8/S9/D-SEQ★ — verified above for the link subspace, unchanged for the content subspace.

**Step 3: K.μ~ — reorder text, verify link fixity.** Swap the two text positions: `π([1,1]) = [1,2]`, `π([1,2]) = [1,1]`, `π([2,1]) = [2,1]`.

Let `a₁ = 1.0.1.0.1.0.1.1` and `a₂ = 1.0.1.0.1.0.1.2`. Pre-state arrangement: `M'(d) = {[1,1] ↦ a₁, [1,2] ↦ a₂, [2,1] ↦ ℓ}`.

Because K.μ~ is a named composite (K.μ⁻ followed by K.μ⁺), we trace it through its intermediate state explicitly.

*K.μ⁻ sub-step.* Remove the two content-subspace mappings `{[1,1], [1,2]}` while retaining the link-subspace mapping at `[2,1]`. The intermediate-state arrangement is `M_int(d) = {[2,1] ↦ ℓ}`. The content subspace contracts to empty (`V_{s_C}(d_int) = ∅`); the link subspace is unchanged (`V_{s_L}(d_int) = {[2,1]}`). Other stores frame: `C_int = C`, `L_int = L'`, `E_int = E`, `R_int = R`.

*K.μ⁻ admissibility at M_int.* The removal pattern is per-subspace:
- *Content-subspace pattern.* `V_{s_C}(d) = {[1,1], [1,2]}`, `V_{s_C}(d_int) = ∅` — full removal with `n'_{s_C} = 0`. This is the case-(a) full-clearance admissible pattern of K.μ⁻ (case (a) with `n'_{s_C} = 0`: subspace emptied; D-MIN★/D-CTG★/D-SEQ★ become vacuous on the cleared subspace).
- *Link-subspace pattern.* `V_{s_L}(d) = V_{s_L}(d_int) = {[2,1]}` — empty removal with `n'_{s_L} = n_{s_L} = 1`. This is the case-(a) zero-suffix admissible pattern.

Both patterns admissible; K.μ⁻ commits.

*Intermediate-state verification at M_int.* The intermediate state must itself be a member of the per-state invariant set, since K.μ~'s decomposition routes through it.
- *S3★ at M_int:* the surviving mapping `[2,1] ↦ ℓ` satisfies `subspace([2,1]) = s_L` and `ℓ ∈ dom(L_int) = dom(L')`. ✓ The two content-subspace positions are removed, so the content clause is vacuous on `dom(M_int(d))`.
- *S3★-aux at M_int:* `subspace([2,1]) = s_L ∈ {s_C, s_L}`. ✓
- *D-CTG★/D-MIN★/D-SEQ★ at M_int:* `V_{s_C}(d_int) = ∅` (clauses vacuous on the empty content subspace); `V_{s_L}(d_int) = {[2,1]}` is contiguous, with `min(V_{s_L}(d_int)) = [s_L, 1]` and structural form `{[s_L, 1, 1, 1]}` matching D-SEQ★ at `n_{s_L} = 1`. ✓
- *CL-OWN at M_int:* `origin(M_int(d)([2,1])) = origin(ℓ) = d` (frame on the surviving mapping). ✓
- *CL-UNIQ at M_int:* `M_int(d)|_{dom_L} = {[2,1] ↦ ℓ}` is a singleton, vacuously injective. ✓
- *L14/L-fin at M_int:* `dom(C_int) = dom(C)` and `dom(L_int) = dom(L')` unchanged, so `dom(C_int) ∩ dom(L_int) = ∅` and `|dom(L_int)| < ω` are inherited. ✓
- *Frame-preserved invariants at M_int:* every entity-layer and provenance-layer invariant (P0–P8, S0–S2, S4, S7a–d, S8a/S8/S8-fin/S8-depth, S9, J0–J4) is preserved by K.μ⁻'s frame on E, C, L, R.

*K.μ⁺ sub-step preconditions at M_int.* The K.μ⁺ step re-adds `{[1,1] ↦ a₂, [1,2] ↦ a₁}` (swapped values). At the intermediate state:
- *`d ∈ E_doc` at M_int:* unchanged from pre-state. ✓
- *New V-positions disjoint from `dom(M_int(d))`:* `dom(M_int(d)) = {[2,1]}`; the rebuilt positions `[1,1], [1,2]` are content-subspace and disjoint from `{[2,1]}`. ✓
- *Subspace assignment of new mappings:* `subspace([1,1]) = subspace([1,2]) = s_C`, and the values `a₁, a₂ ∈ dom(C_int) = dom(C)` (frame-preserved from pre-state, where they were already in dom(C)). ✓ (S3★ holds on the new mappings.)
- *S8a on new V-positions:* both `[1,1]` and `[1,2]` have all components strictly positive. ✓
- *S8-depth and S8-fin on the resulting arrangement:* `V_{s_C}(d_post) = {[1,1], [1,2]}` uniform depth 2 within s_C; `V_{s_L}(d_post) = {[2,1]}` uniform depth 2 within s_L; total dom finite. ✓
- *D-CTG, D-MIN at M_post:* content subspace becomes `{[1,1], [1,2]}`, contiguous with min `[s_C, 1] = [1,1]`; link subspace unchanged. ✓
- *CL-OWN/CL-UNIQ at M_post:* both new mappings are content-subspace (CL-OWN/CL-UNIQ are link-subspace clauses, vacuous on the new mappings); the surviving link-subspace mapping is unchanged. ✓

Both K.μ⁺ preconditions hold at M_int; K.μ⁺ commits, yielding the post-state.

Post-state: `M''(d) = {[1,1] ↦ a₂, [1,2] ↦ a₁, [2,1] ↦ ℓ}`.

Link-subspace fixity: `M''(d)|_{dom_L} = {[2,1] ↦ ℓ} = M'(d)|_{dom_L}` — the link-subspace mapping is unchanged. The fixity argument: π maps `[2,1]` to some position `u`; `M''(d)(u) = M'(d)([2,1]) = ℓ ∈ dom(L')`. By S3★-aux, `subspace(u) ∈ {s_C, s_L}`. If `subspace(u) = s_C = 1`, then S3★ requires `M''(d)(u) ∈ dom(C)`, but `ℓ ∈ dom(L')` and `dom(L') ∩ dom(C) = ∅` (L14) — contradiction. So `subspace(u) = s_L = 2`. Since K.μ⁺ cannot create link-subspace positions, `u` must have existed in the pre-state's link subspace: `u = [2,1]`. Therefore `π([2,1]) = [2,1]` — the link-subspace mapping is fixed by logical necessity, not by fiat. The intermediate-state trace above realises this fixity mechanically: K.μ⁻ does not touch `[2,1] ↦ ℓ`, and K.μ⁺ cannot recreate or relocate it, so the link mapping passes through unchanged.

Post-state verification:
- *S3★:* `subspace([1,1]) = 1 = s_C` and `M''(d)([1,1]) = a₂ ∈ dom(C)`; `subspace([1,2]) = 1 = s_C` and `M''(d)([1,2]) = a₁ ∈ dom(C)`; `subspace([2,1]) = s_L` and `M''(d)([2,1]) = ℓ ∈ dom(L')`. ✓
- *L14:* dom(C) ∩ dom(L') = ∅ unchanged from Step 2. ✓
- *L-fin:* dom(L') = {ℓ} unchanged; still finite. ✓
- *D-CTG★/D-MIN★:* V_{s_C}(d) = {[1,1], [1,2]} and V_{s_L}(d) = {[2,1]} are both unchanged from Step 2 (K.μ~ preserves dom by K.μ~-FIX); contiguity and minima are inherited.
- *CL-OWN:* the link-subspace mapping is fixed pointwise, so origin(M''(d)([2,1])) = origin(ℓ) = d remains satisfied. ✓
- *P3★:* K.μ~ permutes M's V-positions only; C, L, E, R are held in frame. ✓
- *P7a:* dom(C) is unchanged and R is unchanged; every a ∈ dom(C) retains its provenance entry. ✓
- *J1'★ (vacuous):* K.μ~ holds R in frame, so `R' \ R = ∅`. No new provenance entries to check; J1'★ is vacuously satisfied. (Note: K.μ~ also preserves the content-subspace range `ran(M'(d)|_{s_C}) = ran(M(d)|_{s_C})` exactly — π is a bijection on dom(M(d)) and the multiset of values is preserved — so even if a provenance entry were added it would have no new content-subspace range entry to anchor against.) ✓
- *Frame-preserved invariants:* P0/P1/P2/P4★/P5★/P6/P7/P8/S2 (π is a bijection so functionality is preserved)/S3★-aux/S4/S7a–d/S8a/S8-fin/S8-depth/S8/S9/D-SEQ★.

**Step 4: K.λ + K.μ⁺_L — allocate and arrange a second link.** To exercise link-subspace contraction below we need a non-singleton link subspace. Allocate `ℓ₂ = 1.0.1.0.1.0.2.2 = inc(ℓ, 0)` (the next sibling on d's link frontier under TA5(c), per K.λ's subsequent-link case) with some value `(F', G', Θ')`; then arrange `ℓ₂` at `v_{ℓ₂} = shift(max(V_{s_L}(d)), 1) = shift([2,1], 1) = [2,2]` (D-CTG case of K.μ⁺_L).

Effect after both transitions: `L = {ℓ ↦ (F, G, Θ), ℓ₂ ↦ (F', G', Θ')}`, `M''(d) = {[1,1] ↦ a₂, [1,2] ↦ a₁, [2,1] ↦ ℓ, [2,2] ↦ ℓ₂}`. Link-subspace V-positions: `V_{s_L}(d) = {[2,1], [2,2]}` — contiguous (D-CTG★), minimum at `[2,1] = [s_L, 1]` (D-MIN★), depth 2 (S8-depth), structural form `{[s_L, 1, 1, k] : 1 ≤ k ≤ 2}` (D-SEQ★ with `n_{s_L} = 2`). *J1'★ (vacuous):* both K.λ and K.μ⁺_L hold R in frame, so `R' \ R = ∅` for the composite — no new provenance entries are introduced, and J1'★ is vacuously satisfied. The K.μ⁺_L step adds only link-subspace V-positions, so the content-subspace range of M''(d) is unchanged across the composite, consistent with J1'★'s content-subspace scoping. ✓

Post-state verification (for the K.λ + K.μ⁺_L composite):
- *S3★:* the new link-subspace position `[2,2]` has `subspace([2,2]) = s_L` and maps to `ℓ₂ ∈ dom(L')`; existing positions retain their pre-state values. ✓
- *CL-OWN:* `origin(M''(d)([2,2])) = origin(ℓ₂) = d` (K.λ's `origin(ℓ₂) = d` precondition combined with the K.μ⁺_L placement). ✓
- *CL-UNIQ:* `ℓ₂` is fresh to `dom(L)` (K.λ's allocation precondition), so no prior V-position references it; the new V-position `[2,2]` is therefore the unique link-subspace V-position mapping to `ℓ₂`. ✓
- *L0/L1/L1a/L3/L-fin:* each established for `ℓ₂` by K.λ's preconditions and inherited at the post-state.
- *L14:* `dom(C) ∩ dom(L') = ∅` — the new link `ℓ₂` has `fields(ℓ₂).E₁ = s_L = 2`, distinct from `s_C = 1`. ✓
- *Frame-preserved invariants:* P0/P1/P2/P3★/P5★/P6/P7/P7a/P8/S2 (extension at a disjoint V-position preserves functionality)/S3★-aux/S4 (each content address appears in d only, unchanged)/S7a–d (subspace prefix discipline holds by the choice of subspace identifiers)/S8a/S8-depth/S8-fin/S8/S9 — the content subspace is held in frame across both K.λ and K.μ⁺_L; the link subspace receives one disjoint extension under K.μ⁺_L's CL-OWN/CL-UNIQ-preserving discipline.

**Step 5: K.μ⁻ — admissible suffix removal of links.** Remove the mapping at `[2,2]` — the maximum end of `V_{s_L}(d)`, a 1-element suffix of the link-subspace range.

*K.μ⁻:* `dom(M'''(d)) = {[1,1], [1,2], [2,1]} ⊂ dom(M''(d))`. Surviving mappings unchanged: `M'''(d)([1,1]) = a₂`, `M'''(d)([1,2]) = a₁`, `M'''(d)([2,1]) = ℓ`. The content subspace is unchanged: `V_{s_C}(d') = {[1,1], [1,2]}`. The link subspace contracts to a 1-element suffix prefix: `V_{s_L}(d') = {[2,1]}`.

Admissibility verification (per K.μ⁻'s per-subspace precondition):
- *Content-subspace pattern.* `V_{s_C}(d') = V_{s_C}(d)` — empty removal, `n'_{s_C} = n_{s_C} = 2`. This is the case-(a) zero-suffix admissible pattern.
- *Link-subspace pattern.* `V_{s_L}(d) = {[2,1], [2,2]}`, `V_{s_L}(d') = {[2,1]}` — a 1-element suffix removal with `n'_{s_L} = 1` (case (a) admissible).

Post-state invariant verification:
- *S3★:* surviving mappings retain their pre-state values; `[2,1] ↦ ℓ ∈ dom(L)` satisfies the link clause. ✓
- *D-CTG★:* `V_{s_C}(d') = {[1,1], [1,2]}` and `V_{s_L}(d') = {[2,1]}` are each contiguous. ✓
- *D-MIN★:* `min(V_{s_C}(d')) = [1,1] = [s_C, 1]`; `min(V_{s_L}(d')) = [2,1] = [s_L, 1]`. ✓
- *D-SEQ★:* `V_{s_L}(d') = {[s_L, 1, 1, 1]}` matches `{[s_L, 1, ..., 1, k] : 1 ≤ k ≤ 1}`. ✓
- *CL-OWN:* `origin(M'''(d)([2,1])) = origin(ℓ) = d` (preserved from pre-state by frame on the surviving mapping). ✓
- *CL-UNIQ:* the surviving link-subspace mapping is the singleton `{[2,1] ↦ ℓ}`; vacuously injective. ✓
- *L12:* `dom(L)` unchanged — `ℓ₂` remains in `dom(L)` despite no longer being arranged. ✓ This is the *orphan link* state Nelson identifies (LM 4/9): `ℓ₂ ∈ dom(L)` but `ℓ₂ ∉ ran(M'''(d))` for any d.
- *J1'★ (vacuous):* K.μ⁻ holds R in frame, so `R' \ R = ∅`. No new provenance entries to check; J1'★ is vacuously satisfied. (J1'★ is range-based: the content-subspace range `ran(M'''(d)|_{s_C}) = ran(M''(d)|_{s_C}) = {a₁, a₂}` is unchanged across this link-subspace contraction — the link-subspace range loses ℓ₂, but the link subspace is outside J1'★'s scope.) ✓
- *Frame-preserved invariants:* P0, P1, P2, P3★, P5★, P6, P7, P7a, P8, L0, L1, L1a, L3, L14, L-fin, S2, S3★-aux, S4, S7a–d, S8a, S8-depth, S8-fin, S8, S9.

**Step 5 (counterfactual): K.μ⁻ — inadmissible interior removal.** Suppose instead we attempted to remove `[2,1]` while retaining `[2,2]`. The proposed `V_{s_L}(d') = {[2,2]}` would be the prefix-removal pattern (case (c) of K.μ⁻'s case analysis): the minimum link-subspace position `[2,1] = [s_L, 1]` is removed, while `[2,2]` is retained. By case (c), this is forbidden by D-MIN★: the smallest surviving terminal index would be `k_min = 2 ≥ 2`, so `min(V_{s_L}(d')) = [2, 2] ≠ [2, 1] = [s_L, 1]` of depth `m_{s_L} = 2`, violating D-MIN★. (At `m_{s_L} = 2`, the general form `[s_L, 1, ..., 1, k]` collapses to `[s_L, k]` — no intermediate `1`s appear, since the inner range from position 2 to position `m_{s_L} − 1 = 1` is empty.) The D-MIN★ postcondition is violated, and the transition is rejected as inadmissible — no intermediate state with `V_{s_L}(d') = {[2,2]}` is reachable under K.μ⁻'s contract.

A symmetric counterfactual — attempting to remove an interior position of a longer link-subspace range, e.g., remove `[2,2]` while retaining both `[2,1]` and a hypothetical `[2,3]` — would be forbidden by D-CTG★ (case (b)): `[2,2]` lies strictly between `[2,1]` and `[2,3]` under lex order on terminal-varying tuples, so its absence from `V_{s_L}(d')` breaks contiguity.

The link-withdrawal mechanism Nelson contemplates (LM 4/9: "not currently addressable, awaiting historical backtrack functions") — under which a withdrawn link transitions to inactive status while preserving its arrangement position — is therefore *not expressible* as a K.μ⁻ transition in this ASN. Withdrawing the link at `[2,1]` requires withdrawing every link allocated after it as well (suffix-only removal); alternatively, a separate withdrawal mechanism (status flag, tombstone marker, retraction link) would be needed to operate outside K.μ⁻'s presentational-removal contract. The precise mechanism is deferred to the open question on withdrawal invariants.

Steps 1–5 of this example exercise most invariants in the conjunction of ExtendedReachableStateInvariants (per-state) and ExtendedTransitionInvariants (per-transition), providing a worked confirmation of the inductive step for the K.λ, K.μ⁺_L, K.μ~, and K.μ⁻ transition kinds on a concrete two-subspace state, and concretely illustrating the contrast between admissible suffix-style link-subspace contraction and inadmissible interior/prefix patterns. Invariants exercised *directly* (verified at some step from new ground introduced by that transition): S2, S3★, S3★-aux, S8a, S8-depth, S8, D-CTG★, D-MIN★, D-SEQ★, P3★, P4★, P5★, L0, L1, L1a, L3, L14, L-fin, CL-OWN, CL-UNIQ, J1'★ (vacuous at Steps 3, 4, 5; established at Step 2). Invariants exercised *only as frame-preserved* across all five steps (the example does not introduce ground that newly establishes them, but no step disturbs them either): S4 (OriginBasedIdentity — no node-identity events arise; document `d` and accounts `a₁`, `a₂` are baptised in the pre-state, no new nodes are allocated), S7a, S7c, S7d (BridgeBaseSpan invariants for accounts, link bases, references — no bridge-base events arise after the pre-state), S9 (TwoStreamSeparation — `dom(C) ∩ dom(L) = ∅` holds in the pre-state and every step preserves it; this is the per-transition projection of L14, established at Step 2 and frame-preserved thereafter), S7b (BridgeBaseSpan for the content stream — exercised at Step 2 via the content link allocation), P0, P1, P2, P6, P7, P7a, P8 (transition-frame and permanence invariants — uniformly frame-preserved at every step, since no transition reduces `dom` of any store). NodeUniqueAllocation and NodeLineage do not arise in this example because no `K.α` or `K.δ` events occur after the pre-state; their verification is the subject of the *ghost-base document versioning* worked example above. The bounded-sufficiency caveat from the *Elementary transitions* section applies: completeness in the sense of "every admissible reachable transition pattern instantiated" is not claimed by this example.


## Extended reachable-state invariants

The invariants of the extended state partition by quantification *type* into two well-typed statements: a per-state theorem whose conjuncts are properties of a single state, and a per-transition theorem whose conjuncts are properties of an ordered pair `(Σ, Σ')` with `Σ → Σ'`. Stating the first as "every reachable state satisfies P3★" would be type-incorrect — P3★ quantifies over `Σ → Σ'`, not over a single Σ — so the two are separated below.

**ExtendedReachableStateInvariants (per-state).** Every state reachable from Σ₀ = (C₀, L₀, E₀, M₀, R₀) by a finite sequence of valid composite transitions — composed from the transitions K.α (amended), K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻ (amended), K.μ~ (shorthand for its K.μ⁻ + K.μ⁺ decomposition), and K.ρ — satisfies:

  S2 ∧ S3★ ∧ S3★-aux ∧ S4 ∧ S7a ∧ S7b ∧ S7c ∧ S7d ∧ S8a ∧ S8-fin ∧ S8-depth ∧ S8 ∧ D-CTG★ ∧ D-MIN★ ∧ D-SEQ★ ∧ P4★ ∧ P6 ∧ P7 ∧ P7a ∧ P8 ∧ NodeLineage ∧ L0 ∧ L1 ∧ L1a ∧ L1b ∧ L3 ∧ L14 ∧ L-fin ∧ CL-OWN ∧ CL-UNIQ

S0 (ContentImmutability), S1 (StoreMonotonicity), and S9 (TwoStreamSeparation) of ASN-0036 are *per-transition* properties quantified over `Σ → Σ'`, not per-state properties; they appear instead in ExtendedTransitionInvariants below. S0 and S1 are subsumed there by P0; S9 stands as its own per-transition conjunct.

The D-CTG★/D-MIN★/D-SEQ★ conjuncts are the per-subspace forms introduced in the *Amendments to existing transitions* section (D-CTG★ and D-MIN★ drop ASN-0036's link-subspace exemption; D-SEQ★ is derived from D-CTG★ + D-MIN★ + S8-fin + S8-depth + S8a). The unamended D-CTG and D-MIN of ASN-0036 are stronger only in the text subspace and weaker in the link subspace, and would conflict with D-SEQ★'s per-subspace scope; the per-state theorem therefore commits to the starred forms exclusively. ASN-0036's unstarred D-CTG and D-MIN remain authoritative within their original four-component scope, where they are equivalent to the starred forms (no link subspace exists).

Every named conjunct is a predicate on a single state — `(A v ∈ V_S(Σ.M(d)) : ...)`, `(A a ∈ dom(Σ.C) : ...)`, `Contains_C(Σ) ⊆ Σ.R`, and so on — so the assertion "every reachable Σ satisfies this conjunction" is well-typed.

**ExtendedTransitionInvariants (per-transition).** Every valid composite transition `Σ → Σ'` between reachable states satisfies:

  P0 ∧ P1 ∧ P2 ∧ P3★ ∧ P5★ ∧ S9 ∧ L12

Each conjunct is formally stated with the quantifier `(A Σ → Σ' :: ...)` — they are properties of the *step*, not of the endpoint Σ' alone. ASN-0036's S0 (ContentImmutability) and S1 (StoreMonotonicity) are not listed as separate conjuncts here because P0 subsumes both: P0's value-preservation clause `(A a ∈ dom(C) : C'(a) = C(a))` is exactly S0, and P0's domain-monotonicity clause `dom(C) ⊆ dom(C')` is exactly S1. S9 (TwoStreamSeparation) is per-transition by its original ASN-0036 form `(A Σ → Σ' : (E d : M'(d) ≠ M(d)) : (A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)))` — the foundation statement (ASN-0036 line 799) requires only value preservation of existing content entries on arrangement-modifying transitions, *not* the stronger `dom(C') = dom(C)` (which would be incompatible with composites such as K.α + K.μ⁺ + K.ρ that allocate new content while also modifying an arrangement). Under the foundation form, S9 is strictly subsumed by P0 — every clause of S9's consequent appears unconditionally in P0 — but it is retained as its own named conjunct here for cross-foundation traceability with ASN-0036. The first theorem governs what is true *at* each reachable state; the second governs what is true *across* each reachable step.

Together the two theorems supersede the earlier ReachableStateInvariants theorem by replacing S3 with S3★, P4 with P4★, P3 with P3★, P5 with P5★, adding S3★-aux (subspace exhaustiveness), CL-OWN (link-subspace ownership), L3 (triple endset structure), the per-subspace amendment D-SEQ★, and the foundation invariants previously inherited tacitly from ASN-0036 (S4, S7a–S7d, S9) and from ASN-0043 (L1b, L-fin); covering the extended transition set including K.λ and K.μ⁺_L. The earlier theorem's conjunction is recovered as `ExtendedReachableStateInvariants ∧ ExtendedTransitionInvariants`.

*Proof.* The proof proceeds by induction on the number of valid composite transitions from Σ₀. The per-state invariant set partitions into two classes: *elementary invariants* preserved by each elementary transition individually, and *composite invariants* that may be violated at intermediate states within a composite but hold at every composite boundary. The per-transition invariants are addressed last, in a single elementary-case check.

**Base.** The extended initial state Σ₀ satisfies every per-state invariant (verified in the Link store and extended system state section — L₀ = ∅ satisfies link invariants vacuously, including L3; S3★ and P4★ reduce to S3 and P4; S3★-aux holds vacuously since M₀(d) = ∅ for all d; D-CTG and D-MIN hold vacuously since V_S(d) = ∅ for every subspace S). The per-transition invariants have no base case — they are vacuous before any transition has occurred — and enter the induction at the first step.

**Class (a): Elementary per-state invariants** — preserved by each elementary transition individually. These are all per-state invariants except P4★ and P7a: S2, S3★, S3★-aux, S4, S7a, S7b, S7c, S7d, S8a, S8-fin, S8-depth, S8, D-CTG★, D-MIN★, D-SEQ★, P6, P7, P8, NodeLineage, L0, L1, L1a, L1b, L3, L14, L-fin, CL-OWN, CL-UNIQ.

For K.α (amended): holds M and L in frame; S3★, S3★-aux preserved (M unchanged); content, entity, and provenance invariants preserved; P8 preserved since E is unchanged (K.α holds E in frame, so the entity-hierarchy spine is identical at pre- and post-state). L0 clause 2: `fields(a).E₁ = s_C` by the K.α amendment, so the new content address satisfies `(A a ∈ dom(C') :: fields(a).E₁ = s_C)`. L14: `fields(a).E₁ = s_C` and `s_C ≠ s_L` (SC-NEQ), and L0 clause 1 at the pre-state gives `(A ℓ ∈ dom(L) :: fields(ℓ).E₁ = s_L)`, so `a ∉ dom(L)` and `dom(C') ∩ dom(L') = (dom(C) ∪ {a}) ∩ dom(L) = ∅`. L1, L1a, L3, L12 preserved (L unchanged). For K.δ: holds both M and L in frame; C, L unchanged; S3★, S3★-aux preserved (M unchanged); link invariants preserved since neither L nor dom(C) is modified. *P8 (entity-hierarchy spine).* K.δ adds one entity `e` to E with `E' = E ∪ {e}`. Two cases: (i) `IsNode(e)` — the universal `(A e' ∈ E' : ¬IsNode(e') : parent(e') ∈ E')` quantifies over non-node entities only, so the freshly added node `e` is outside its scope; for every existing non-node `e' ∈ E ⊆ E'`, the inductive hypothesis gives `parent(e') ∈ E ⊆ E'`. (ii) `¬IsNode(e)` — K.δ's case-(ii) precondition requires `parent(e) ∈ E`, and P1 gives `E ⊆ E'`, so `parent(e) ∈ E'`; for every other non-node entity `e' ∈ E ⊆ E'`, the inductive hypothesis carries `parent(e') ∈ E ⊆ E'`. In both cases P8 holds at the post-state. For K.ρ: holds both M and L in frame; C, E, L unchanged; S3★, S3★-aux preserved (M unchanged); link invariants preserved since neither L nor dom(C) is modified; P8 preserved since E is unchanged. P7 (ProvenanceGrounding) is elementary: K.ρ adds (a, d) with a ∈ dom(C) (precondition), and P0 ensures a ∈ dom(C') for all subsequent states; all other transitions hold R in frame, adding no new provenance entries, so existing entries retain their grounding in dom(C') (by P0). For K.μ⁺ (amended): holds L in frame; S3★ preserved (analyses above); S3★-aux preserved (new positions have subspace s_C by amendment); D-CTG, D-MIN preserved by the K.μ⁺ postcondition requirement; S8 holds at the post-state by *S8 (Finite span decomposition)* of ASN-0036, applied at Σ'; its formal contract there names exactly the preconditions S2, S3, S7b, S7c, S8a, S8-depth, and S8-fin (foundation-layer dependencies T1, T3, T4, T5, T10, TS4, TumblerAdd, OrdinalShift, OrdinalDisplacement, ShiftPreservation, and the NAT-* claims are internal to S8's proof and require no re-establishment here). Each of those preconditions is preserved or established at Σ' by the clauses of this case above: S2 (a per-state-functionality property of M(d)) is preserved by the explicit M-clause of this transition; S3 is supplied by the stronger S3★ established above; S7b and S7c hold for every address in dom(C') by the K.α clauses (above); S8a, S8-depth, and S8-fin are themselves elementary-preserved invariants whose preservation by this transition has been discharged above in this same Class (a) enumeration; link invariants preserved since L is unchanged. For K.μ⁻: holds L in frame; S3★ preserved (restriction of M(d) preserves both clauses); S3★-aux preserved (removal does not alter subspaces of surviving positions); D-CTG, D-MIN preserved by the K.μ⁻ amendment postcondition — by D-SEQ at the input state, V_S(d) is {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}, so valid contractions remove from the maximum end or remove all positions; S8 holds at the post-state by *S8 (Finite span decomposition)* of ASN-0036, applied at Σ'; its formal contract there names exactly the preconditions S2, S3, S7b, S7c, S8a, S8-depth, and S8-fin (foundation-layer dependencies T1, T3, T4, T5, T10, TS4, TumblerAdd, OrdinalShift, OrdinalDisplacement, ShiftPreservation, and the NAT-* claims are internal to S8's proof and require no re-establishment here). Each of those preconditions is preserved or established at Σ' by the clauses of this case above: S2 (a per-state-functionality property of M(d)) is preserved by the explicit M-clause of this transition; S3 is supplied by the stronger S3★ established above; S7b and S7c hold for every address in dom(C') by the K.α clauses (above); S8a, S8-depth, and S8-fin are themselves elementary-preserved invariants whose preservation by this transition has been discharged above in this same Class (a) enumeration; link invariants preserved since L is unchanged. For K.μ~ (named composite, treated here via its K.μ⁻ + K.μ⁺ realisation rather than as an elementary case): holds L in frame. When π = id (including the case dom_C(M(d)) = ∅, where the K.μ~ definition section establishes π = id via S3★ + L14 + SC-NEQ and the cardinality consequence r = 0), K.μ~ expands into zero elementary steps producing M'(d) = M(d) — all invariants hold trivially. When π ≠ id (which requires dom_C(M(d)) ≠ ∅), K.μ~ decomposes into K.μ⁻ + K.μ⁺ (per its definition above), and each invariant is preserved through the underlying elementary steps; the discussion below summarises the joint result at the composite boundary. S3★ preserved (decomposition analysis above); S3★-aux preserved (K.μ⁻ removes positions without altering subspaces, K.μ⁺ adds only s_C positions); link-subspace positions are fixed (link-subspace fixity, which requires S3★ and S3★-aux at the output — both now established). D-CTG and D-MIN hold at every intermediate state of the K.μ⁻ + K.μ⁺ decomposition and at the output: link-subspace fixity (r = 0) implies K.μ⁻ removes only content-subspace positions; by D-SEQ at the input, content-subspace positions form {[s_C, 1, ..., 1, k] : 1 ≤ k ≤ n}, so K.μ⁻ can remove a suffix leaving {[s_C, 1, ..., 1, k] : 1 ≤ k ≤ n'} for some 0 ≤ n' ≤ n, which satisfies D-CTG and D-MIN; the link subspace at the intermediate state equals the input (r = 0), preserving D-CTG/D-MIN. K.μ⁺ (amended) then rebuilds the content subspace satisfying D-CTG and D-MIN as a postcondition. For any bijection π with dom_C(M(d)) ≠ ∅, a valid two-step decomposition always exists — in particular, n' = 0 (remove all content-subspace positions, then re-add with new mappings) satisfies D-CTG/D-MIN at the intermediate state vacuously for the content subspace. (When dom_C(M(d)) = ∅, π is the identity and zero elementary steps suffice, as established above.) D-SEQ then applies at the output state. π bijects dom(M(d)) onto dom(M'(d)) preserving S8a, S8-depth, S8-fin (K.μ~ preconditions, above), and link-subspace fixity forces π to biject dom_C(M(d)) onto dom_C(M'(d)); equal cardinality combined with D-SEQ at both input and output yields V_S(d') = V_S(d) for each content subspace S. S8 holds at the post-state by *S8 (Finite span decomposition)* of ASN-0036, applied at Σ'; its formal contract there names exactly the preconditions S2, S3, S7b, S7c, S8a, S8-depth, and S8-fin (foundation-layer dependencies T1, T3, T4, T5, T10, TS4, TumblerAdd, OrdinalShift, OrdinalDisplacement, ShiftPreservation, and the NAT-* claims are internal to S8's proof and require no re-establishment here). Each of those preconditions is preserved or established at Σ' by the clauses of this case above: S2 (a per-state-functionality property of M(d)) is preserved by the explicit M-clause of this transition; S3 is supplied by the stronger S3★ established above; S7b and S7c hold for every address in dom(C') by the K.α clauses (above); S8a, S8-depth, and S8-fin are themselves elementary-preserved invariants whose preservation by this transition has been discharged above in this same Class (a) enumeration; CL-OWN preserved by link-subspace fixity; link invariants preserved since L is unchanged. For K.λ: holds M, C, E, R in frame; S3★, S3★-aux preserved (M unchanged); link invariants verified (orphan link analysis in the Orphan links and coupling flexibility section); L3 is established for the new entry (K.λ requires `(F, G, Θ) ∈ Link`) and preserved for all existing entries (L12); L-fin preserved — `|dom(L')| = |dom(L)| + 1`, and finiteness is closed under adding one element. For K.μ⁺_L: holds C, L, E, R in frame; S3★-aux preserved (new position has subspace s_L); per-subspace arrangement invariants verified in the Link-subspace extension section — S8a, S8-fin, S8-depth, D-CTG, D-MIN, D-SEQ, S8 all hold; S3★ satisfied by precondition (`ℓ ∈ dom(L)`); CL-OWN preserved (new mapping satisfies `origin(ℓ) = d` by precondition; existing link-subspace mappings unchanged by frame); CL-UNIQ preserved by the first-arrangement precondition `ℓ ∉ ran(M(d))` (see the CL-UNIQ inductive proof in the *Link-subspace ownership* section above); L3 preserved (L unchanged); L-fin preserved (L unchanged).

**Foundation invariants previously implicit.** The following invariants are preserved uniformly across every elementary transition by the structure of allocation and frame discipline, and are listed explicitly here for completeness:

- *S4 (Origin-based identity)* — distinct allocation events produce distinct addresses. Each K.α produces `a` via the T10a allocator under origin(a) (S7a, ASN-0036), so GlobalUniqueness (T10a) gives `a ∉ dom(C)`; for K.δ on non-node entities, the same allocator discipline applies; for K.δ on nodes, NodeUniqueAllocation (the axiom introduced above) supplies `e ∉ E` directly. K.λ produces `ℓ` via the inc chain under origin(ℓ), with GlobalUniqueness giving `ℓ ∉ dom(L) ∪ dom(C)` (jointly with L14). All other transitions hold C, L, E in frame and add no addresses.
- *S7a (Document-scoped allocation)* — established by K.α's precondition that allocation uses origin(a)'s content-allocator prefix; preserved by P0 thereafter. For pre-existing addresses, S7a is inherited from the inductive hypothesis and P0.
- *S7b (Element-level I-addresses)* — `zeros(a) = 3`: K.α's amendment fixes `fields(a).E₁ = s_C` and inc chains under a document-level prefix give `zeros(a) = 3`. Preserved by P0 thereafter.
- *S7c (Element-field depth)* — `#E(a) ≥ 2`: enforced by K.α's allocator chain (`fields(a) = [s_C, k]` with `k ≥ 1` at minimum, i.e., depth ≥ 2). Preserved by P0 thereafter.
- *S7d (Document allocation discipline)* — every K.δ on `IsDocument(e)` allocates via the T10a discipline under the owning account's prefix; distinct K.δ events produce distinct documents (GlobalUniqueness). Preserved by P1 thereafter.
- *L1b (Link element-field depth)* — `#E(ℓ) ≥ 2`: in K.λ's *first-link case*, SubAllocatorAxiom emits `ℓ = [d.0.s_L.1]` with element field `[s_L, 1]`, so `#E(ℓ) = 2` by construction — no `inc` step is invoked. In the *subsequent-link case*, K.λ produces `ℓ = inc(prev, 0)` (TA5(c)), which is a sibling extension preserving the element-field length: TA5(c)'s length-preservation clause gives `#E(ℓ) = #E(prev)`, and `#E(prev) ≥ 2` holds inductively (the first link emitted under d has `#E = 2` by the axiom; every subsequent sibling preserves this depth). Hence `#E(ℓ) ≥ 2` for every link emission. Preserved by L12 thereafter.
- *L-fin (Link store finiteness)* — `|dom(L)| < ∞`: base `|dom(L₀)| = 0 < ∞`. K.λ extends dom(L) by exactly one address (a finite extension preserves finiteness); all other transitions hold L in frame (`L' = L` preserves `|dom(L')| = |dom(L)| < ∞`). Composing over a finite sequence of valid composites yields `|dom(L)| < ∞` at every reachable state.
- *D-SEQ★ (Per-subspace lex-sequential range)* — derived above in the Per-subspace amendment to D-SEQ section from D-CTG★, D-MIN★, S8-depth, S8-fin, and S8a, all of which are elementary-preserved. D-SEQ★ at each reachable state follows by the same derivation applied at that state.
- *NodeLineage* `(A e ∈ E : IsNode(e) : n₀ ≼ e)` — base case: `E₀ = {n₀}` with `n₀ ≼ n₀` by reflexivity of the tumbler-prefix order. Inductive step: only K.δ extends E. K.δ case (i) — `IsNode(e)` — has `n₀ ≼ e` as an explicit precondition (verified at the K.δ definition site under *Precondition (i)*), and the inductive hypothesis carries `n₀ ≼ e'` for every prior node `e' ∈ E ⊆ E'`. K.δ case (ii) — `¬IsNode(e)` — adds a non-node entity, leaving the universal quantification over nodes unchanged: existing nodes retain their lineage by inductive hypothesis, and the freshly added non-node falls outside the quantifier scope. All other elementary transitions hold E in frame, so the node set is unchanged and the quantifier ranges over the same nodes with the same prefix relationships. NodeLineage therefore holds at every reachable state.

**Class (b): Composite invariants** — may be violated at intermediate states within a composite, but hold at every valid composite boundary. These are: P4★ and P7a.

P4★ (`Contains_C(Σ) ⊆ R`): An elementary K.μ⁺ alone adds a content-subspace V-position mapping to address `a`, placing `(a, d) ∈ Contains_C(Σ')`. Its frame has `R' = R`, so if `(a, d) ∉ R`, P4★ is violated at the intermediate state. The coupling constraint J1★, evaluated at composite boundaries, guarantees restoration: for each `(a, d) ∈ Contains_C(Σ') \ Contains_C(Σ)`, some content-subspace V-position in M'(d) maps to `a` (by definition of Contains_C), and no content-subspace V-position in M(d) maps to `a` (since `(a, d) ∉ Contains_C(Σ)`), so J1★ requires `(a, d) ∈ R'`. This holds regardless of whether the V-position carrying `a` in M'(d) existed in dom(M(d)) with a different value — J1★'s range-based trigger detects new I-addresses in the content-subspace range, not new V-positions in the domain. Therefore `Contains_C(Σ') ⊆ R'` at the composite boundary. K.μ⁺_L does not affect P4★: it adds only link-subspace V-positions, which are excluded from Contains_C by definition. K.μ⁻ can only shrink Contains_C. K.μ~ preserves Contains_C exactly (analysis in the Content-scoped containment and provenance section). All other transitions hold M in frame.

P7a (`(A a ∈ dom(C) :: (E d :: (a, d) ∈ R))`): An elementary K.α alone adds `a` to `dom(C')` with `R' = R`, so `(a, d) ∉ R` for the newly allocated address — P7a is violated at the intermediate state immediately after a stand-alone K.α step. P7a's restoration depends on the two ValidComposite★ clauses operating jointly. *Clause (2), J0 evaluated at the composite boundary*, guarantees that every `a ∈ dom(C') \ dom(C)` is placed in some document's arrangement in the final state: `(E d, v : d ∈ E'_doc ∧ v ∈ dom(M'(d)) : M'(d)(v) = a)`. This is a statement about the *net* composite effect — J0 does not say *which* elementary step places `a` or *when*. *Clause (1), elementary preconditions at intermediate states*, governs *how* this net effect is realised: K.μ⁺'s referential-integrity precondition (`a ∈ dom(C)`) requires K.α to precede K.μ⁺ in the elementary sequence, since `a ∉ dom(C)` at every state prior to K.α. The K.μ⁺ amendment then constrains the placement to a content-subspace V-position (`subspace(v) = s_C`). With `(a, d) ∈ Contains_C(Σ') \ Contains_C(Σ)` established, J1★ — also a clause-(2) coupling, evaluated at the composite boundary — requires `(a, d) ∈ R'`. Therefore P7a holds at the composite boundary. The two clauses are jointly necessary: J0 alone (clause (2)) would not specify *when* the K.μ⁺ step must occur in the sequence, and clause (1) alone would admit a K.α-without-K.μ⁺ composite that violates J0. No other elementary transition removes addresses from dom(C) (by P0) or entries from R (by P2), so P7a, once established, is not broken by subsequent composites.

Coupling constraints J0, J1★, J1'★ hold for all valid composites by the analysis in the Scoped coupling constraints section.

**Per-transition invariants** (ExtendedTransitionInvariants: P0, P1, P2, P3★, P5★, S9, L12). These are properties of `Σ → Σ'`; we discharge each by elementary case analysis, observing that every valid composite is a finite sequence of elementary steps and each per-transition invariant is closed under composition (extension and value-preservation compose transitively).

- *P0 (`dom(C) ⊆ dom(C') ∧ (A a ∈ dom(C) : C'(a) = C(a))`).* K.α extends dom(C) by `{a}` and assigns `C'(a)` without modifying existing entries (extension is at `a ∉ dom(C)`). All other elementary transitions hold C in frame: `C' = C`, so both clauses hold by equality. P0 subsumes ASN-0036's S0 (value-preservation clause) and S1 (domain-monotonicity clause), so neither is listed as a separate conjunct.
- *P1 (`E ⊆ E'`).* K.δ extends E by `{e}`. All other elementary transitions hold E in frame: `E' = E`.
- *P2 (`R ⊆ R'`).* K.ρ extends R by `{(a, d)}`. All other elementary transitions hold R in frame: `R' = R`.
- *P3★ (`dom(C) ⊆ dom(C') ∧ dom(L) ⊆ dom(L') ∧ E ⊆ E' ∧ R ⊆ R' ∧ (A a ∈ dom(C) : C'(a) = C(a)) ∧ (A ℓ ∈ dom(L) : L'(ℓ) = L(ℓ))`).* The C-clauses are P0; the L-clauses are L12 (below); the E-clause is P1; the R-clause is P2. P3★ is the conjunction of the established per-transition invariants; no separate derivation is needed.
- *P5★ (`dom(C') ⊇ dom(C) ∧ (a ∈ dom(C) : C'(a) = C(a))`; `dom(L') ⊇ dom(L) ∧ (ℓ ∈ dom(L) : L'(ℓ) = L(ℓ))`; `E' ⊇ E`; `R' ⊇ R`).* Each clause is one of P0, L12, P1, P2.
- *S9 (TwoStreamSeparation).* `(A Σ → Σ' : (E d : M'(d) ≠ M(d)) : (A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)))` — every transition that alters some document's arrangement preserves the value of every existing content entry (foundation ASN-0036, line 799; value preservation only, *not* `dom(C') = dom(C)`). Under this form S9's consequent is strictly subsumed by P0 (`dom(C) ⊆ dom(C') ∧ (A a ∈ dom(C) : C'(a) = C(a))`), which holds unconditionally for every elementary transition (established above). The implication therefore holds whether the antecedent is true (P0 supplies the consequent directly) or false (vacuous). Closure under composition: P0 itself is closed under finite composition, so S9 — being a weakening of P0 by an additional antecedent — is also preserved at the composite boundary. In particular, the composite K.α + K.μ⁺ + K.ρ (content-insertion) genuinely fires S9's antecedent (M(d) changes at the K.μ⁺ step) and genuinely extends dom(C) at the K.α step; this is consistent with foundation S9 because the consequent only asserts that existing C-entries persist with their values, which P0 supplies.
- *L12 (`(A a ∈ dom(L) : a ∈ dom(L') ∧ L'(a) = L(a))`).* K.λ extends dom(L) by `{ℓ}` at `ℓ ∉ dom(L)` (precondition) and assigns `L'(ℓ)` without modifying existing entries. All other elementary transitions hold L in frame: `L' = L`.

Each per-transition invariant therefore holds across every elementary step; transitivity of inclusion and equality over a finite composite sequence gives the per-transition invariant at the composite boundary. ∎


## Temporal decomposition

We have arrived at the structural insight underlying the entire design. The state Σ = (C, L, E, M, R) decomposes into three temporal layers, each answering a different question about the docuverse.

**The existential layer** (C, L, E) answers *what is*. Content, links, and entities, once created, exist permanently. Addresses are permanent (T8, ASN-0034). Content values are immutable (P0). Link values are immutable (L12). Entity membership is monotonic (P1). This layer only grows, and its entries are individually immutable once created. Gregory: "once text or a link-orgl is written at an ISA address, that binding is permanent."

**The historical layer** (R) answers *what has happened*. Provenance, once recorded, persists permanently. R records which documents have ever contained which content — a question about history, not current state. This layer only grows, though its entries may become stale: R may assert that document d once contained address a when d's current arrangement no longer references a.

**The presentational layer** (M) answers *what appears now*. Arrangements — the mapping from virtual positions to content identities — are freely mutable. Content can be added, removed, or rearranged. This is the sole locus of destructive change.

| Layer | Components | Mutability | Elementary transitions |
|-------|-----------|------------|----------------------|
| Existential (functional) | C, L | Append-only domain; values immutable | K.α, K.λ |
| Existential (set) | E | Append-only membership; no value structure | K.δ |
| Historical | R | Append-only, entries may stale | K.ρ |
| Presentational | M | Fully mutable | K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~ (composite) |

(K.δ creates a new entity whose arrangement is initially empty. Since M is total with M(e) = ∅ for e ∉ E_doc, entity creation determines which empty arrangements become semantically meaningful — but it does not modify M.)

The invariants bind the layers together, making the temporal contracts precise. Within the existential layer: P6 ties C to E (every I-address's origin document exists as an entity); L1a is the link analog, tying L to E (every link address is scoped to an existing document); L14 constrains C and L to disjoint address subspaces. Bridging presentational to existential: S3★ bridges M to {C, L} — content-subspace V-positions reference dom(C), link-subspace V-positions reference dom(L); CL-OWN further constrains the link-subspace bridge (every document arranges only its own links). Bridging existential to historical: P7 ties R to C (every provenance entry references allocated content), and P7a ties C to R (every I-address has provenance — no content exists without a historical trail). And P4★ (Contains_C(Σ) ⊆ R, derived in the coupling section) bridges the presentational and historical layers — it is the load-bearing constraint that necessitates J1★'s coupling (by wp, K.μ⁺ alone cannot maintain P4★).

The two coupling constraints play different logical roles. J1★ is *derived*: P4★ together with the wp calculus forces it — K.μ⁺ in isolation fails to maintain Contains_C(Σ) ⊆ R, so K.ρ must co-occur. J0 is *axiomatic*: it is declared as a primitive coupling on K.α (every content allocation co-occurs with an arrangement extension placing the fresh address) and is *not* derived from a more primitive invariant. P7a — the provenance-coverage theorem `(A a ∈ dom(C) :: (E d :: (a, d) ∈ R))` — is the operational *consequence* of {J0, J1★, P0, P2}: J0 places the fresh address into some `ran(M'(d))`; J1★ records the resulting new containment in R; P0 and P2 propagate both facts to all subsequent reachable states. This is the orientation discharged in the P7a derivation in *Reachable-state invariants* below. The alternative orientation — taking P7a as an axiomatic design constraint and treating J0 as a derived operational consequence — is logically possible but not the one adopted here, because J0 must be stated in any case (the wp calculus over P7a alone does not determine which `d` receives the fresh address, so a coupling axiom is needed at the K.α/K.μ⁺ boundary independent of how P7a is justified). S3★ is orthogonal to both coupling constraints — it constrains the M→{C, L} direction (arrangements reference allocated content or links), while J0 constrains the C→M direction (allocated content enters an arrangement). A system satisfying S3★ but not J0 could permit orphan content: K.α extends dom(C), and if no K.μ⁺ follows, S3★ is trivially preserved because no new M entry was added — but P7a would fail for the orphan, witnessing the necessity of an axiomatic J0.

**P6 (Existential coherence).** For every I-address in the content store, its origin document exists as an entity:

`(A a ∈ dom(C) :: origin(a) ∈ E_doc)`

*Derivation.* K.α allocates a under origin(a)'s prefix (S7a, ASN-0036), and requires origin(a) ∈ E_doc as a precondition — the allocation mechanism inc(·, k) operates on an existing tumbler within the ownership domain. P1 preserves entity membership across subsequent transitions; P0 preserves a ∈ dom(C). Initial state: dom(C₀) = ∅, so the quantifier is vacuously satisfied. Inductive step: each K.α has origin(a) ∈ E_doc by precondition; P0 preserves a; P1 preserves origin(a). ∎

**P7 (Provenance grounding).** Every provenance entry references allocated content:

`(A (a, d) ∈ R :: a ∈ dom(C))`

*Derivation.* K.ρ requires a ∈ dom(C) as a precondition. P0 preserves dom(C). By induction: initially R₀ = ∅ (vacuous). Each K.ρ adds (a, d) with a ∈ dom(C); P0 ensures a remains in dom(C') for all subsequent states; P2 ensures (a, d) remains in R'. ∎

**P7a (Provenance coverage).** Every I-address in the content store has at least one provenance record:

`(A a ∈ dom(C) :: (E d :: (a, d) ∈ R))`

*Derivation.* By induction. *Base:* dom(C₀) = ∅; vacuous. *Inductive step:* for a ∈ dom(C) (pre-existing), the inductive hypothesis gives (a, d) ∈ R for some d, and P2 preserves it. For a ∈ dom(C') \ dom(C) (freshly allocated), J0 gives a ∈ ran(M'(d)) for some d; since a is fresh, S3 gives a ∉ ran(M(d)) for all d, so a ∈ ran(M'(d)) \ ran(M(d)); J1 gives (a, d) ∈ R'. ∎

The decomposition constrains the elementary transitions cleanly. Each elementary transition modifies components in exactly one temporal layer. Composite transitions routinely span all three: content insertion compounds K.α (existential) + K.μ⁺ (presentational) + K.ρ (historical); link creation compounds K.λ (existential) + K.μ⁺_L (presentational). The point is that each elementary step has bounded scope. The transitions admitting destructive change — K.μ⁻ (removal) and K.μ~ (rearrangement) — are confined to the presentational layer alone, the one layer where impermanence is by design. Cross-layer coupling occurs only in constructive directions: K.α (existential) couples with K.μ⁺ (presentational) via J0; K.μ⁺ (presentational) couples with K.ρ (historical) via J1★/J1'★. The existential and historical layers never shrink.

The existential and historical layers differ in semantics despite sharing the append-only contract. Existential entries state *current facts*: content value v exists at address a, and this remains true permanently. Historical entries state *past events*: document d once contained address a, and this record persists even when the current arrangement no longer agrees. The distinction matters because existential entries are both permanent and accurate (content *is* at address a), while historical entries are permanent but may be stale (document d *was* associated with address a, but may no longer be).

Nelson captures the whole architecture in a sentence: "The braid only grows more complex. It never unravels." The existential and historical layers are the braid. The presentational layer is the current view of it.


## Properties Introduced

The table is partitioned by provenance into three subsections:

- **New properties** are first introduced in this ASN; they have no foundation analog.
- **Local extensions and strengthenings** refine a foundation property — or an earlier property of this ASN — to fit the extended state (typically by partitioning across content and link subspaces, scoping over additional state components, merging multiple foundation invariants, or amending an existing transition's contract).
- **Foundation restatements** reproduce a *selected subset* of foundation properties for self-contained reference. The scope is deliberately restricted: an item is restated here only when (a) the property is referenced under a notational convention or compact name first coined in this ASN (the elementary transitions K.α, K.μ⁺, K.μ⁻, K.μ~ — restated under this ASN's `K.·` notation), or (b) the property belongs to ASN-0043's link model and is required to make the extended state's L component self-contained (Σ.L, Endset, Link, s_C/s_L, K.λ, L1, L1a, L1b, L12, L-fin). ASN-0036's per-state invariants (S2 functionality, S3 referential integrity, S4 subspace coincidence, S7a–d origin/parent structural properties, S8a positive components, S8-depth uniform subspace depth, S8-fin arrangement finiteness, S8 combined, S9 two-stream separation, D-CTG contiguity, D-MIN minimum position, D-SEQ lex-sequential range) are *not* duplicated in this table — they are referenced by name throughout the body of this ASN, and their formal statements are owned by ASN-0036. Where this ASN strengthens or supersedes one (S3 → S3★, D-CTG → D-CTG★, D-MIN → D-MIN★, D-SEQ → D-SEQ★, P3 → P3★, P4 → P4★, P5 → P5★, J1 → J1★, J1' → J1'★), the strengthened form appears under *Local extensions and strengthenings*; the original foundation form remains authoritative in its original scope. A reader needing the verbatim ASN-0036 statement of an unstrengthened invariant should consult ASN-0036 directly.

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
| Arrangement invariants lemma | Every valid composite preserves S2/S3/S8a/S8-depth/S8-fin/D-CTG/D-MIN — each elementary transition preserves these per-state properties; composition by transitivity |
| Reachable-state invariants | Every state reachable from Σ₀ satisfies P0, P1, P2, P4, P6, P7, P7a, P8, S2–S8-fin, D-CTG, D-MIN — by induction: base at Σ₀, permanence lemma + arrangement invariants lemma + per-property derivations |
| K.δ | Entity creation — extend E with fresh entity; precondition: parent(e) ∈ E when ¬IsNode(e); empty arrangement if IsDocument |
| K.ρ | Provenance recording — extend R with (a, d) pair where IsElement(a) ∧ a ∈ dom(C) |
| K.μ⁺_L | Elementary transition: link-subspace arrangement extension, M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}, origin(ℓ) = d, ℓ ∉ ran(M(d)) (first-arrangement) |
| K.μ~-FIX | Domain fixity under K.μ~: dom(M'(d)) = dom(M(d)), making π a permutation of a fixed domain — from D-SEQ + bijection cardinality + subspace preservation |
| J0 | Content allocation (K.α) always co-occurs with arrangement extension (K.μ⁺) |
| J1 | Arrangement extension (K.μ⁺) must co-occur with provenance recording (K.ρ), derived by wp |
| J1' | (a, d) ∈ R' \ R only when a ∈ ran(M'(d)) \ ran(M(d)) — new provenance requires new containment |
| J2 | K.μ⁻ as elementary transition requires no coupling: C' = C ∧ E' = E ∧ R' = R |
| J3 | K.μ~ as named composite requires no coupling: C' = C ∧ E' = E ∧ R' = R |
| J4 | Fork composite: K.δ + K.μ⁺ + K.ρ (no other steps); precondition V_{s_C}(d_src) ≠ ∅; dom(C') = dom(C) follows from frames; provenance from J1; content-subspace-empty source is ex nihilo (K.δ), not fork |
| P1 | Entity set is monotonically growing: E ⊆ E' for every transition, uniformly across levels |
| P2 | Provenance relation is monotonically growing: R ⊆ R' for every transition |
| P3 | Arrangements are the sole state component admitting destructive change (contraction, reordering) |
| P4 | Provenance bounds: Contains(Σ) ⊆ R, with stale entries possible from prior states |
| P4a | Historical fidelity: every (a, d) ∈ R has a witnessing state where a ∈ ran(M(d)) |
| P5 | Destruction confinement: C, E, R are all monotonic across every transition; only M can lose information |
| P6 | Existential coherence: origin(a) ∈ E_doc for all a ∈ dom(C) |
| P7 | Provenance grounding: a ∈ dom(C) for all (a, d) ∈ R |
| P7a | Provenance coverage: (E d :: (a, d) ∈ R) for all a ∈ dom(C) — every I-address has provenance |
| P8 | Entity hierarchy: (A e ∈ E : ¬IsNode(e) : parent(e) ∈ E) — no orphan accounts or documents |
| SC-NEQ | Axiom: `s_C ≠ s_L` — subspace identifiers are distinct. ASN-0043 states the inequality inline as a definitional stipulation but does not elevate it to a named axiom; this ASN names it because it is load-bearing for L0's two-clause partition, L14, and the link-subspace fixity argument under K.μ~ |
| NodeUniqueAllocation | Axiom: every K.δ node-allocation event produces e ∉ E; closes the GlobalUniqueness chain for nodes where T10a does not apply |
| NodeLineage | Axiom: `(A e ∈ E : IsNode(e) : n₀ ≼ e)` — every node in E descends structurally from the bootstrap node n₀ by tumbler-prefix relation; enforced as K.δ case (i) precondition and discharged as an inductive invariant of every reachable state |
| SubAllocatorAxiom | Axiom (ContentLinkSubAllocatorExistence): for each d ∈ E_doc, the entity-allocation event placing d into E_doc simultaneously establishes two disjoint sub-allocators under d — a content sub-allocator with anchor `b_C(d) = [d.0.s_C]` and a link sub-allocator with anchor `b_L(d) = [d.0.s_L]` — each providing a forward-allocation frontier whose namespace property closes the uniqueness chain for K.α (content first-emit) and K.λ (link first-emit) |
| b_C(d), b_L(d) | Virtual sub-allocator anchors under d: `b_C(d) = [d.0.s_C]`, `b_L(d) = [d.0.s_L]` — single-component element-field bases, not in dom(C) ∪ dom(L), serving as formal starting points for the content and link allocator chains under d |
| Allocator hierarchy | Content and link sub-allocators are sibling element-field allocators under d, sharing prefix `[d.0]`; T10a-conformance applies to each frontier separately; cross-document collisions prevented by T10, cross-subspace by L14 + SC-NEQ + T7 |
| S3★-aux | Subspace exhaustiveness: `(A d, v : v ∈ dom(M(d)) : subspace(v) = s_C ∨ subspace(v) = s_L)` in every reachable state |
| L14 | StoreDisjointness: `dom(C) ∩ dom(L) = ∅` — derived from L0 and SC-NEQ via T7 (new derivation; no L14 label in the foundation) |
| CL-OWN | LinkSubspaceOwnership: `(A d, v : v ∈ dom(M(d)) ∧ subspace(v) = s_L : origin(M(d)(v)) = d)` — every document's link subspace contains only its own links |
| CL-UNIQ | LinkSubspacePositionUniqueness: `(A d, v₁, v₂ ∈ dom(M(d)) : subspace(v₁) = subspace(v₂) = s_L ∧ M(d)(v₁) = M(d)(v₂) : v₁ = v₂)` — each link occupies exactly one V-position in its home document's link subspace; injectivity of M(d)\|_{dom_L}. Closes the K.μ~ link-subspace identity precondition derivation |

### Local extensions and strengthenings of foundation properties

| Label | Statement | Foundation source |
|-------|-----------|--------------------|
| P0 | Content store is append-only with immutable values: dom(C) ⊆ dom(C') ∧ C'(a) = C(a) for a ∈ dom(C) | Subsumes ASN-0036's S0 (ContentImmutability) and S1 (StoreMonotonicity) into a single unified statement |
| L0 | SubspacePartition: `dom(L)` addresses have `fields(a).E₁ = s_L`; `dom(C)` addresses have `fields(a).E₁ = s_C` | L-clause from ASN-0043's L0 (SubspacePartition); the C-clause is the new content-side companion required by the extended state |
| L3 | TripleEndsetStructure: `(A a ∈ dom(L) :: L(a) = (F, G, Θ) where F, G, Θ ∈ Endset ∧ Θ ≠ ∅)` — local extension of ASN-0043's L3 fixing arity at exactly three; non-empty type endset preserved from foundation | ASN-0043's L3 (NEndsetStructure) admits arity ≥ 3; this ASN fixes arity at exactly three |
| S3★ | Subspace-conditional referential integrity: text → dom(C), link → dom(L); supersedes S3 | ASN-0036's S3 (ReferentialIntegrity) is single-store; this ASN partitions the target by subspace |
| D-CTG★ | Per-subspace contiguity: `(A d, S : V_S(d) ≠ ∅ : V_S(d) is contiguous under the V-ordering on subspace S)` — local strengthening of ASN-0036's D-CTG dropping the link-subspace exemption; supersedes D-CTG within the extended state | ASN-0036's D-CTG (Contiguity) had a link-subspace exemption |
| D-MIN★ | Per-subspace minimum position: `(A d, S : V_S(d) ≠ ∅ : min(V_S(d)) = [S, 1, ..., 1] of depth m_S)` — local strengthening of ASN-0036's D-MIN dropping the link-subspace exemption; supersedes D-MIN within the extended state | ASN-0036's D-MIN (MinimumPosition) had a link-subspace exemption |
| D-SEQ★ | Per-subspace lex-sequential range: for each non-empty subspace S in M(d), `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` of uniform depth m_S — derived from D-CTG★ + D-MIN★ + S8-depth + S8-fin + S8a, per-subspace promotion of ASN-0036's D-SEQ to a system-wide invariant of the extended state | ASN-0036's D-SEQ (LexSequential) was per-document; this ASN promotes per-subspace and elevates to system-wide invariant |
| P3★ | No component other than M — specifically C, L, E, R — admits contraction or reordering; supersedes P3 | This ASN's own P3 extended to include L |
| P4★ | `Contains_C(Σ) ⊆ R` — provenance bounds scoped to content subspace; supersedes P4 | This ASN's own P4 with subspace scoping |
| P5★ | dom(C), dom(L), E, R can only grow; only M can lose information; supersedes P5 | This ASN's own P5 with L added |
| J1★ | Range-based content-subspace scoping of J1: provenance recording for I-addresses new to content-subspace range | This ASN's own J1 with subspace scoping |
| J1'★ | Range-based content-subspace scoping of J1': provenance entries only from content-subspace range changes | This ASN's own J1' with subspace scoping |
| ValidComposite★ | Valid composite in extended state: transition preconditions at each step (K.μ~ as shorthand for K.μ⁻ + K.μ⁺) + J0, J1★, J1'★ at composite boundary; supersedes ValidComposite | This ASN's own Valid composite definition extended for the two-subspace state |
| ExtendedReachableStateInvariants | Every reachable state satisfies S2 ∧ S3★ ∧ S3★-aux ∧ S4 ∧ S7a–S7d ∧ S8a ∧ S8-fin ∧ S8-depth ∧ S8 ∧ D-CTG★ ∧ D-MIN★ ∧ D-SEQ★ ∧ P4★ ∧ P6–P8 ∧ L0 ∧ L1 ∧ L1a ∧ L1b ∧ L3 ∧ L14 ∧ L-fin ∧ CL-OWN ∧ CL-UNIQ (per-state). P0, P1, P2, P3★, P5★, S9, L12 are *per-transition*: see ExtendedTransitionInvariants. Together supersedes ReachableStateInvariants | This ASN's own Reachable-state invariants synthesis extended to the two-subspace state |
| ExtendedTransitionInvariants | Every valid composite transition Σ → Σ' between reachable states satisfies P0 ∧ P1 ∧ P2 ∧ P3★ ∧ P5★ ∧ S9 ∧ L12 (per-transition). Conjuncts are properties of the step, not of the endpoint alone; ASN-0036's S0 (ContentImmutability) and S1 (StoreMonotonicity) are subsumed by P0 and are not listed as separate conjuncts. S9 (TwoStreamSeparation) stands as its own conjunct | This ASN's own per-transition synthesis, extended for the two-subspace state |
| K.α amendment | Content-subspace restriction (`fields(a).E₁ = s_C`); preserves L0 clause 2 and L14 in the extended state | Amendment to ASN-0036's K.α adding subspace constraint |
| K.μ⁺ amendment | Content-subspace restriction (`subspace(v) = s_C`); existing D-CTG/D-MIN postconditions carry forward; partitions arrangement extension by subspace with K.μ⁺_L | Amendment to ASN-0036's K.μ⁺ adding subspace partitioning |
| K.μ⁻ amendment | D-CTG/D-MIN postconditions extend to two-subspace case; valid contractions per-subspace independently | Amendment to ASN-0036's K.μ⁻ extending postconditions to two subspaces |

### Foundation restatements (recapitulated for self-contained reference)

| Label | Statement | Foundation source |
|-------|-----------|--------------------|
| Σ.L | L : T ⇀ Link — link store, partial function from link addresses to link values | ASN-0043 |
| Endset | `𝒫_fin(Span)` — finite set of well-formed spans (T12); type for link endpoints | ASN-0043 |
| Link | `(F, G, Θ)` where `F, G, Θ ∈ Endset` — link value with from, to, and type endsets | ASN-0043 |
| s_C, s_L | Content and link subspace identifiers — first component of element field; `s_C ≥ 1`, `s_L ≥ 1` | ASN-0043 |
| K.α | Content allocation — extend dom(C) with fresh IsElement(a) address and value | ASN-0036 (notation coined here; semantics from the strand model's content-allocation step) |
| K.μ⁺ | Arrangement extension — add V→I mappings to M(d), existing values preserved, referential integrity (S3), D-CTG/D-MIN postcondition | ASN-0036 (notation coined here; semantics from the strand model's arrangement-extension step) |
| K.μ⁻ | Arrangement contraction — remove V→I mappings from M(d), surviving values preserved, D-CTG/D-MIN postcondition, no effect on C, E, R | ASN-0036 (notation coined here; semantics from the strand model's arrangement-contraction step) |
| K.μ~ | Arrangement reordering — named composite (K.μ⁻ + K.μ⁺), bijection on V-positions preserving I-address multiset, D-CTG/D-MIN postcondition; not an elementary transition | ASN-0036 (notation coined here; semantics from the strand model's arrangement-reordering step) |
| K.λ | Elementary transition: L' = L ∪ {ℓ ↦ (F, G, Θ)}, frame C' = C, E' = E, M' = M, R' = R | ASN-0043 (notation coined here; semantics from the link model's link-creation step) |
| L1 | LinkElementLevel: `(A a ∈ dom(L) :: zeros(a) = 3)` — every link address is element-level | ASN-0043 |
| L1a | LinkScopedAllocation: `(A a ∈ dom(L) :: origin(a) ∈ E_doc)` — link addresses scoped to documents | ASN-0043 |
| L1b | LinkElementFieldDepth (restated from ASN-0043 for self-contained use): `#E(ℓ) ≥ 2` for every ℓ ∈ dom(L); established in K.λ's first-link case by SubAllocatorAxiom emitting `[d.0.s_L.1]` (#E = 2) and preserved by sibling extension `inc(prev, 0)` in the subsequent case (TA5(c) length-preservation), then by L12 thereafter | ASN-0043 |
| L12 | LinkImmutability: `a ∈ dom(L) ⟹ a ∈ dom(L') ∧ L'(a) = L(a)` — once created, permanent and fixed | ASN-0043 |
| L-fin | LinkStoreFiniteness: `\|dom(Σ.L)\| < ∞` — restated from ASN-0043 for self-contained use; preserved by K.λ (single-element extension) and L-frame in all other transitions | ASN-0043 |


## Open Questions

- What invariants must a forked document's initial arrangement satisfy with respect to its source's current arrangement — must it be identical, or may it be a proper subset?
- What guarantees must the system provide about provenance when content is transitively shared through chains of transclusion?
- Can arrangement contraction on one document affect the discoverability of links attached to the same I-addresses from another document?
- What relationship must hold between a document's version lineage and its sequence of arrangement transitions?
- What additional permanence properties must the provenance relation satisfy for content that participates in link endsets?
- What invariants must the link subspace satisfy beyond those inherited from D-CTG, D-MIN, and S8-depth — are there link-specific ordering constraints, capacity bounds, or structural properties that D-SEQ does not capture?
- Must the system guarantee that a fresh link address is always available within a document's link subspace, or can link allocation fail due to address space exhaustion?
- What must the system guarantee when concurrent operations target the same home document — must link address allocation be serialized, or can concurrent allocations produce distinct addresses without coordination?
- What invariants must link withdrawal maintain — must withdrawn links remain arranged, or does withdrawal remove them from M(d)? The transition framework constrains link-subspace contractions to suffix truncations (by D-CTG and link-subspace fixity under K.μ~); Nelson's design suggests an inactive-status mechanism rather than arrangement removal. The precise withdrawal mechanism is an open question.
- Should the entity-allocation discipline admit account-level depth-1 tumbler extension (K.δ with `k = 1` and `IsAccount(t)`), producing an account-shaped sibling at the same hierarchy level as t? The present ASN excludes this at the precondition, citing the consultation evidence that versioning is reserved to documents (Nelson, LM 4/29; Gregory, `docreatenewversion` for DOCUMENT→DOCUMENT only). The structural form `[N, 0, U, 1]` is itself well-typed (still `IsAccount`) under T4b, and admitting it would not violate any per-state invariant of the present model (the k = 1 harmlessness verification for documents would carry across); but no role for such an entity is documented in the design or implementation. The question is whether a future extension (e.g., account renaming, multi-account user identity) would require admitting account-level depth-1 extension; if so, the precondition restriction here can be relaxed without further structural reorganisation.
