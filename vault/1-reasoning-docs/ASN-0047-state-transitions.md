# ASN-0047: State Transitions

*2026-03-17, revised 2026-03-22*

ASN-0036 established two components of system state — a permanent content store C and mutable document arrangements M(d) — and proved their separation: content, once stored, is immutable (S0); arrangement mutations cannot alter the content store (S9). These are properties of the invariants. We have not yet classified the transitions. In what primitive ways can the state change, and what must each change preserve?

The consultation answers reveal a state model richer than the two-space analysis captured. Nelson enumerates the ways the docuverse changes — new documents created, new content inserted, new links established, views rearranged — and is equally precise about what cannot happen: content is never destroyed, addresses are never reassigned, history is never erased. Gregory reduces eight protocol commands to six kinds of persistent modification, distributed across three storage layers with distinct permanence contracts.

We seek the abstract taxonomy. Not the protocol commands, which are interface design, but the primitive modifications and their invariants. The central result is a *mutability hierarchy*: the state components arrange into three temporal layers, each with its own permanence contract. Destructive change — removal and reordering — is confined entirely to the most mutable layer.


## The state model

ASN-0036 gave us C and M(d). Two phenomena require additional state components.

First, entities come into existence. Nelson describes exactly two document creation modes: ex nihilo (a fresh empty document) and forking (a new document derived from an existing one). Gregory confirms both use the same allocation mechanism, differing only in whether the new arrangement starts empty or populated. We need an explicit record of which entities exist.

**Definition (Entity set).** **Σ.E ⊆ T** — the set of allocated entity addresses. Every e ∈ E satisfies ValidAddress(e) (T4, ASN-0034). Entities are organisational — nodes, accounts, documents — not content; element-level addresses live in dom(C), not E:

`(A e ∈ E :: ¬IsElement(e))`

Equivalently, E ⊆ {t : ValidAddress(t) ∧ zeros(t) ≤ 2}. Given this exclusion, the level predicates of ASN-0045 partition E into exactly three strata:

- E_node = {e ∈ E : IsNode(e)} — server nodes
- E_account = {e ∈ E : IsAccount(e)} — user accounts
- E_doc = {e ∈ E : IsDocument(e)} — documents and links

For a non-node entity e (where ¬IsNode(e)), define **parent(e)** as the tumbler obtained by truncating the last field and its preceding zero separator. If IsAccount(e) with form N.0.U, then parent(e) = N. If IsDocument(e) with form N.0.U.0.D, then parent(e) = N.0.U. In each case parent(e) is a valid address at the next higher level: zeros(parent(e)) = zeros(e) − 1.

M is a total function with M(d) = ∅ (the empty partial function) when d ∉ E_doc; non-empty arrangements arise only for document entities. We include links in E_doc: Nelson describes them as owned entities with internal structure ("a package of connecting or marking information... owned by a user... thereafter maintained by the back end"), and Gregory confirms link creation uses the same allocation mechanism as document creation. The structural distinction between documents and links — endset semantics, subspace layout — belongs to a separate analysis; here both participate identically in transitions.

Second, removal of content from an arrangement does not erase the historical fact of prior containment. Gregory: the reverse index "accumulates entries from every content addition but is never trimmed." Nelson: "every previous arrangement remains reconstructable." The system must answer "which documents have ever contained content with origin *a*?" — a question about history, not about current state.

**Definition (Provenance relation).** **Σ.R ⊆ T_elem × E_doc** — where T_elem = {a ∈ T : IsElement(a)} (ASN-0045). The pair (a, d) ∈ R records that document d has, at some point in the system's history, contained I-address a in its arrangement. This historical fidelity — that every entry reflects an actual past containment event, not merely eligibility — is not assumed by the definition alone; it is established as P4a below, by induction over J1', P2, and P0.

The full system state is:

> **Σ = (C, E, M, R)**

where C : T ⇀ Val is as defined in ASN-0036, and M : T → (T ⇀ T) is total, satisfying M(d) = ∅ for d ∉ E_doc.

**Definition (Initial state).** The initial state Σ₀ = (C₀, E₀, M₀, R₀) is:

- C₀ = ∅ (no content allocated)
- E₀ = {n₀} for a designated bootstrap node n₀ with IsNode(n₀)
- M₀(d) = ∅ for all d — (E₀)_doc = ∅, so every arrangement is the empty partial function
- R₀ = ∅ (no provenance recorded)

The bootstrap node seeds the entity hierarchy. Without at least one node, K.δ cannot create accounts (which require a parent node), and without accounts, no documents, and without documents, no content. The choice of n₀ is a system parameter, not a state transition. At Σ₀, (E₀)_doc = ∅, so the arrangement invariants S2, S3, S8a, S8-depth, S8-fin, D-CTG, and D-MIN hold vacuously — no arrangements exist.


## Link store and extended system state

This ASN uses properties of the link store. For self-containment, we restate the definitions and invariants needed.

**Definition (Endset).** An *endset* is a finite set of well-formed spans: `Endset = 𝒫_fin(Span)`, where `Span` is the set of well-formed span pairs `(s, ℓ)` satisfying T12 (ASN-0034). The empty set ∅ is a valid endset.

**Definition (Link).** A *link value* is a triple `(F, G, Θ)` where `F, G, Θ ∈ Endset` — the *from-endset*, *to-endset*, and *type-endset* respectively.

**Definition (Subspace identifiers).** We write `s_C` for the content subspace identifier and `s_L` for the link subspace identifier. These are the first components of the element field for content and link addresses respectively: `fields(a).E₁ = s_C` for content addresses, `fields(ℓ).E₁ = s_L` for link addresses. The same identifiers serve for V-positions: `subspace(v) = v₁`.

**SC-NEQ (SubspaceDistinctness).** `s_C ≠ s_L`.

This is the structural precondition for every disjointness argument in this ASN. By T7 (SubspaceDisjointness, ASN-0034), `s_C ≠ s_L` implies that no tumbler can be both a content address and a link address. Without SC-NEQ, L0 and L14 would be vacuous. We note that `s_C ≥ 1` follows from S7b and T4: content I-addresses are element-level by S7b (`zeros(a) = 3`), and T4 requires every element-field component to be strictly positive, so `fields(a).E₁ = s_C > 0`. The same derivation gives `s_L ≥ 1`: link I-addresses are element-level by L1 below (`zeros(ℓ) = 3`), so by T4, `fields(ℓ).E₁ = s_L > 0`.

**L0 (SubspacePartition).**

  `(A a ∈ dom(Σ.L) :: fields(a).E₁ = s_L)`

  `(A a ∈ dom(Σ.C) :: fields(a).E₁ = s_C)`

**L1 (LinkElementLevel).**

  `(A a ∈ dom(Σ.L) :: zeros(a) = 3)`

Every link address is an element-level tumbler.

**L1a (LinkScopedAllocation).**

  `(A a ∈ dom(Σ.L) :: origin(a) ∈ E_doc)`

Every link address is allocated under the tumbler prefix of a document in E_doc.

**L3 (TripleEndsetStructure).**

  `(A a ∈ dom(Σ.L) :: Σ.L(a) = (F, G, Θ) where F, G, Θ ∈ Endset)`

Every link in the link store has exactly three endsets.

**L12 (LinkImmutability).**

  `(A Σ → Σ' : (A a : a ∈ dom(Σ.L) : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)))`

Once created, a link's address persists in dom(L) and its value is permanently fixed.

**L14 (StoreDisjointness).**

  `dom(Σ.C) ∩ dom(Σ.L) = ∅`

Derived from L0 and SC-NEQ via T7: if `a ∈ dom(C)` then `fields(a).E₁ = s_C`, and if `a ∈ dom(L)` then `fields(a).E₁ = s_L`; since `s_C ≠ s_L`, no address inhabits both domains.

**Extended system state.** The extended system state is **Σ = (C, L, E, M, R)**, where L : T ⇀ Link is the link store.

**Extended initial state.** Σ₀ = (C₀, L₀, E₀, M₀, R₀) with L₀ = ∅. The extended invariants hold vacuously at Σ₀: L0, L1, L1a, L3, L12, L14 are satisfied by empty L; S3★'s link-subspace clause is vacuous (no link-subspace V-positions exist in M₀); P4★ reduces to P4 (which holds at Σ₀ per ASN-0047); D-CTG and D-MIN hold vacuously since M₀(d) = ∅ for all d, so V_S(d) = ∅ for every subspace S. This closes the inductive base for the ExtendedReachableStateInvariants theorem.

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

No other component admits contraction or reordering. Gregory states this explicitly: the arrangement layer is "the sole locus of destructive mutation." P0–P2 make this formal: C, E, and R are all monotonic; only M can shrink.


## Elementary transitions

We seek the elementary modifications — the state changes from which all system operations compose. Each is defined by its effect and its frame: what changes and what does not.

**K.α (Content allocation).** A fresh I-address is bound to a value in the content store:

`C' = C ∪ {a ↦ v}` where `a ∉ dom(C)`

*Precondition:* `IsElement(a)` (S7b, ASN-0036) ∧ `origin(a) ∈ E_doc`. The address is allocated under the creating document's prefix (S7a), and the allocation mechanism inc(·, k) (TA5, ASN-0034) operates within an ownership domain, requiring the document entity to exist before content can be allocated under its prefix. By GlobalUniqueness (ASN-0034), a is distinct from every previously allocated address.

*Frame:* E' = E; (A d :: M'(d) = M(d)); R' = R.

**K.δ (Entity creation).** A fresh entity address enters E with initial state:

`E' = E ∪ {e}` where `e ∉ E ∧ ValidAddress(e) ∧ ¬IsElement(e)`

*Precondition:* when ¬IsNode(e), parent(e) ∈ E — the parent entity must already exist. For root nodes (IsNode(e)), no parent is required; node creation is the bootstrap case that seeds new branches of the hierarchy. By GlobalUniqueness (ASN-0034) — the same result that governs K.α — e is distinct from every previously allocated address, so e ∉ E.

When IsDocument(e): M'(e) = ∅ (empty arrangement). For non-root entities, the address is typically allocated via inc(·, k) (TA5, ASN-0034) within the parent's ownership domain. Gregory confirms that document creation and node creation use the same allocation mechanism, differing only in the allocation level.

Nelson identifies two document-creation modes — ex nihilo and forking. At the elementary level, both begin with K.δ producing an empty document. When the source arrangement is non-empty, forking is compound: K.δ followed by arrangement extension and provenance recording (J4 below). When the source arrangement is empty, fork reduces to K.δ alone — structurally identical to ex nihilo creation.

*Frame:* C' = C; (A d' :: M'(d') = M(d')); R' = R.

**K.μ⁺ (Arrangement extension).** New V→I mappings are added to some d ∈ E_doc, with existing mappings unchanged:

`dom(M'(d)) ⊃ dom(M(d)) ∧ (A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))`

Extension is pure addition — the domain grows, and no existing value is altered. Without the value-preservation clause, K.μ⁺ could silently replace values at existing positions, conflating extension with replacement. The decomposition of replacement into K.μ⁻ followed by K.μ⁺ depends on each being a pure operation.

*Precondition:* `d ∈ E_doc`; for every new mapping M'(d)(v) = a, `a ∈ dom(C)` (S3, ASN-0036 — since K.μ⁺'s frame holds C' = C, referential integrity reduces to membership in the pre-state content store); new V-positions satisfy S8a (all components strictly positive), and the resulting arrangement M'(d) satisfies S8-depth (uniform depth within each subspace); dom(M'(d)) is finite (S8-fin); the resulting arrangement satisfies D-CTG (contiguity within each subspace, ASN-0036) and D-MIN (minimum position in each non-empty subspace, ASN-0036). Functionality (S2) is preserved: dom(M'(d)) ⊃ dom(M(d)) with value preservation at existing positions means new entries are assigned at positions outside dom(M(d)), so M'(d) remains a function — extending a partial function at disjoint domain elements cannot introduce ambiguity.

In a composite transition, K.α may precede K.μ⁺, extending dom(C) before K.μ⁺ executes. At that intermediate state the freshly allocated address is already in the content store, satisfying the precondition. From the composite perspective, the I-address in a new mapping falls into one of two cases:

(i) Freshly allocated — co-occurring K.α places a into dom(C) before K.μ⁺ maps to it. Nelson: "new content enters Istream permanently."

(ii) Previously existing — a ∈ dom(C) at the composite's initial state. This is transclusion: "the copy shares I-addresses with the source. No new content is created in Istream."

*Frame:* C' = C; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R.

**K.μ⁻ (Arrangement contraction).** Existing V→I mappings are removed from some d ∈ E_doc, with surviving mappings unchanged:

`dom(M'(d)) ⊂ dom(M(d)) ∧ (A v : v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v))`

*Precondition:* `d ∈ E_doc`.

Contraction preserves functionality (S2), referential integrity of survivors (S3, since C' = C), V-position well-formedness (S8a), uniform depth within subspace (S8-depth), and finiteness (S8-fin) by restriction of M(d). D-CTG and D-MIN are not preserved by arbitrary restriction — removing an interior position from a contiguous range creates a gap. The postcondition requires M'(d) to satisfy D-CTG and D-MIN for each subspace. By D-SEQ at the input state (ASN-0036), V_S(d) for each non-empty subspace S is a contiguous ordinal range {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}; valid contractions are constrained to removal from the maximum end of V_S(d) or removal of all positions in V_S(d).

Contraction is pure removal — the domain shrinks, and no surviving value is altered. Without the value-preservation clause, K.μ⁻ could modify values at remaining positions, conflating contraction with rewriting.

Nelson: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." Contraction changes what a document displays; it does not change what exists.

*Frame:* C' = C; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d')).

**K.μ~ (Arrangement reordering).** V-positions may change without adding or removing mappings. For some d ∈ E_doc, there exists a bijection π : dom(M(d)) → dom(M'(d)) such that:

`(A v : v ∈ dom(M(d)) : M'(d)(π(v)) = M(d)(v))`

*Precondition:* `d ∈ E_doc`; π produces V-positions satisfying S8a (all components strictly positive), and the resulting arrangement M'(d) satisfies S8-depth (uniform depth within each subspace), D-CTG (contiguity within each subspace), and D-MIN (minimum position in each non-empty subspace).

The bijection preserves the mapping pointwise — each V-position retains its I-address — so the multiset of referenced I-addresses is identical. As a corollary, ran(M'(d)) = ran(M(d)). This is a defining property of reordering, not a frame condition: it constrains how M(d) is modified, while frame conditions describe what is unchanged in other components. Nelson: content "changes Vstream positions but touches nothing in Istream. The same bytes appear in a different order." Gregory confirms that reordering is the only transition kind that leaves all persistent structures outside the arrangement unchanged.

*Frame (derived below):* C' = C; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d')).

**K.ρ (Provenance recording).** A document-content association enters R:

`R' = R ∪ {(a, d)}` where `a ∈ dom(C) ∧ d ∈ E_doc`

*Precondition:* `a ∈ dom(C)` ∧ `d ∈ E_doc`. The level constraint IsElement(a) follows from S7b (every a ∈ dom(C) satisfies IsElement(a)).

*Frame:* C' = C; E' = E; (A d :: M'(d) = M(d)).

Five primitive kinds — K.α, K.δ, K.μ⁺, K.μ⁻, K.ρ — are complete. The argument is structural: the four-component state (C, E, M, R) admits exactly one growth mode for C (K.α), one for E (K.δ), one for R (K.ρ), and two independent mutation modes for M — entry addition (K.μ⁺) and entry removal (K.μ⁻). Any modification to a finite partial function decomposes into additions and removals; replacement — changing which I-address a V-position maps to — decomposes into K.μ⁻ followed by K.μ⁺.

K.μ~ is a distinguished composite, not a primitive transition. When dom(M(d)) is non-empty, it decomposes into K.μ⁻ (removing content-subspace mappings) followed by K.μ⁺ (re-adding content-subspace mappings at new positions). In the extended state, link-subspace mappings are preserved through the decomposition: the K.μ⁺ amendment (below) restricts K.μ⁺ to content-subspace V-positions, so link-subspace mappings removed by K.μ⁻ could not be restored — forcing K.μ⁻ to retain them. The full argument establishing link-subspace fixity under K.μ~ is developed in the S3★ analysis and ExtendedReachableStateInvariants theorem below. We verify the intermediate-state preconditions and derive the frame.

Let dom_C(M(d)) = {v ∈ dom(M(d)) : subspace(v) = s_C} denote the content-subspace positions. Let Σ_int be the state after K.μ⁻ removes dom_C(M(d)) from M(d), leaving M_int(d) containing only link-subspace mappings (if any). K.μ⁻'s frame gives C_int = C, E_int = E, R_int = R, and M_int(d') = M(d') for d' ≠ d. The K.μ⁺ step re-adds content-subspace mappings at the new V-positions π(v) for v ∈ dom_C(M(d)), and its preconditions at Σ_int are: (i) d ∈ (E_int)_doc — holds because E_int = E and d ∈ E_doc; (ii) referential integrity — every re-added I-address a has a content-subspace V-position, and a ∈ dom(C) at the pre-state (by S3 for content-subspace positions; the extended-state analysis below establishes S3★, which gives the same conclusion via its content clause), so a ∈ dom(C_int) since C_int = C by K.μ⁻'s frame; (iii) S8a and S8-depth — the new V-positions satisfy these by K.μ~'s precondition on π; (iv) S8-fin — dom(M'(d)) is finite because π is a bijection from the finite dom(M(d)) (S8-fin at the pre-state); (v) D-CTG and D-MIN — at the intermediate state, K.μ⁻'s postcondition ensures contiguity and minimum position; at the final state, K.μ⁺'s postcondition establishes them for the rebuilt arrangement. Functionality (S2) of the result M'(d) follows from the injectivity of π: each target position π(v) receives exactly one value M(d)(v), and since π is a bijection, no two source positions map to the same target.

The frame follows by composition. K.μ⁻ gives C_int = C, E_int = E, R_int = R, and preserves other arrangements. K.μ⁺ gives C' = C_int = C, E' = E_int = E, R' = R_int = R, and preserves other arrangements. Composing: C' = C, E' = E, R' = R, (A d' : d' ≠ d : M'(d') = M(d')) — matching the frame stated above.

When dom(M(d)) = ∅, K.μ~ is the identity — the empty bijection π : ∅ → ∅ satisfies the definition, producing zero elementary steps. When dom(M(d)) is non-empty, π = id is also permitted — the identity bijection produces M'(d) = M(d), a degenerate reordering that changes nothing. The decomposition into K.μ⁻ + K.μ⁺ is a vacuous round-trip, and all invariants are trivially preserved. We do not restrict π to non-identity bijections; the formal definition subsumes both degenerate cases cleanly. The coupling constraint J1 is vacuously satisfied at the composite level: since K.μ~ preserves ran(M(d)), the set difference ran(M'(d)) \ ran(M(d)) is empty — no new containment pairs arise, so no provenance recording is needed. We retain K.μ~ as a named transition because its isolation property (J3) and semantic clarity — reordering as a single atomic concept — justify separate treatment. Gregory's independent analysis of the implementation identifies the same six persistent modification kinds, confirming this classification.

We also observe that neither split nor merge appears as an elementary transition. Nelson addresses this explicitly: the effect of splitting a document is achieved by creating two new documents and transcluding different portions of the original into each. Merging is creating a new document and transcluding from multiple sources. Both compose from K.δ, K.μ⁺, and K.ρ — the elementary transitions suffice.

**Lemma (Arrangement invariants from elementary preservation).** Every valid composite transition preserves S2, S3, S8a, S8-depth, S8-fin, D-CTG, and D-MIN. Each elementary transition preserves these per-state properties: K.μ⁺ establishes them via its preconditions (disjoint extension for S2, referential integrity for S3, explicit S8a/S8-depth/S8-fin/D-CTG/D-MIN requirements); K.μ⁻ preserves S2/S3/S8a/S8-depth/S8-fin by restriction of M(d) and D-CTG/D-MIN by its explicit postcondition; K.δ for documents produces the empty arrangement (vacuously satisfying all seven); all other transitions hold M in frame. Since each step of a valid composite preserves these per-state properties, they hold at every intermediate and final state.


## Amendments to existing transitions

**K.α amendment (ContentSubspaceRestriction).** In the extended state, K.α is amended with a content-subspace restriction: the allocated address must satisfy `fields(a).E₁ = s_C`. This parallels K.λ's `fields(ℓ).E₁ = s_L` and is required by L0 clause 2 — without it, K.α could allocate an address with subspace s_L, placing it in dom(C') and violating the partition. The amendment also preserves L14: since `fields(a).E₁ = s_C` and `s_C ≠ s_L` (SC-NEQ), the address `a` cannot appear in dom(L) — L0 clause 1 at the pre-state ensures all dom(L) addresses have subspace s_L — so `dom(C') ∩ dom(L') = ∅`.

**K.μ⁺ amendment (ContentSubspaceRestriction).** K.μ⁺ is amended with a content-subspace restriction: new V-positions must satisfy `subspace(v) = s_C`. This complements K.μ⁺_L (defined below), which handles link-subspace extensions exclusively. The restriction is necessary — without it, K.μ⁺ could create a link-subspace V-position mapping to dom(C), violating S3★. With this amendment, the two transitions partition arrangement extensions by subspace. The existing D-CTG and D-MIN postconditions carry forward, now complemented by K.μ⁺_L's parallel contiguity and minimum-position preconditions in the link subspace.

**K.μ⁻ amendment (PerSubspaceContiguity).** K.μ⁻'s D-CTG and D-MIN postconditions extend naturally to the two-subspace case: in the extended state, contraction must satisfy D-CTG and D-MIN for each subspace independently. The structural consequence is unchanged from the pre-extension analysis — by D-SEQ at the input state, each non-empty subspace has V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}, constraining valid contractions to removal from the maximum end or removal of all positions within each subspace.

**Consequence for J4 (Fork, ASN-0047).** Since J4's K.μ⁺ step is now restricted to content-subspace V-positions, forking a document populates only the content subspace of the new document. Link-subspace mappings from the source document are not copied — the forked document's link subspace starts empty. J4 remains a valid composite under the amended coupling constraints. J1★ is satisfied because J4's K.μ⁺ creates only content-subspace V-positions (by the amendment) and J4's K.ρ records provenance for each `a ∈ ran(M'(d_new))`, covering every content-subspace extension. J1'★ is satisfied because each new `(a, d_new) ∈ R' \ R` has `a ∈ ran(M'(d_new))` from content-subspace extensions — J4's K.μ⁺ step creates only content-subspace V-positions (by the K.μ⁺ amendment), and S3★'s content clause gives `M'(d_new)(v) ∈ dom(C)` for each such `v`, so `ran(M'(d_new)) ⊆ dom(C)` and P7 compatibility is maintained. D-CTG and D-MIN are satisfied: J4's K.μ⁺ step operates on a freshly created document (M(d_new) = ∅ after K.δ), constructing the entire content-subspace arrangement; by choosing V-positions contiguously from the minimum [s_C, 1, ..., 1], D-CTG and D-MIN hold for the content subspace, and the link subspace of d_new is empty (J4's K.μ⁺ is content-subspace-only by the amendment), so D-CTG and D-MIN hold vacuously for it. This is consistent with Nelson's design: each document owns only its home links, and links from the source remain discoverable through the shared I-addresses via refractive following — "a link to one version of a Prismatic Document is a link to all versions" (Nelson). A mechanism for link inheritance under forking, if desired, would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope.


## Link allocation

**K.λ (LinkAllocation).** Creates a new entry in the link store.

*Precondition:*
- d ∈ E_doc  (home document exists)
- ℓ ∉ dom(L) ∪ dom(C)  (fresh address — L14)
- zeros(ℓ) = 3 ∧ fields(ℓ).E₁ = s_L  (element-level, link subspace — L0, L1)
- origin(ℓ) = d  (scoped to home document — L1a)
- `(A ℓ' : ℓ' ∈ dom(L) ∧ origin(ℓ') = d : ℓ' < ℓ)`  (forward allocation — T9)
- (F, G, Θ) ∈ Link  (well-formed link value — L3)

*Effect:* `L' = L ∪ {ℓ ↦ (F, G, Θ)}`

*Frame:* `C' = C; E' = E; (A d' :: M'(d') = M(d')); R' = R`

The address ℓ is produced by the same forward-allocation discipline as content addresses (T9, ASN-0034): within each document's link subspace, addresses are monotonically increasing. By T7 (SubspaceDisjointness, ASN-0034) and SC-NEQ, the link subspace s_L is disjoint from the content subspace s_C, so ℓ cannot collide with any content address. By T10 (PartitionIndependence, ASN-0034), link addresses in different documents cannot collide either.


## Generalized referential integrity

**S3★ (GeneralizedReferentialIntegrity).** The arrangement maps V-positions to addresses in the store appropriate to their subspace:

  `(A d, v : v ∈ dom(Σ.M(d)) : (subspace(v) = s_C ⟹ Σ.M(d)(v) ∈ dom(Σ.C)) ∧ (subspace(v) = s_L ⟹ Σ.M(d)(v) ∈ dom(Σ.L)))`

where `subspace(v)` denotes the first component of the V-position. S3★ supersedes S3 (ASN-0036) for the extended state Σ = (C, L, E, M, R): S3 requires every V-position to map into dom(C), which is violated by link-subspace mappings targeting dom(L). S3 remains valid when restricted to states with no link-subspace mappings — the pre-extension states of ASN-0047 have only content-subspace V-positions, for which S3★ reduces to S3.

Existing transitions preserve S3★: K.α, K.δ, K.ρ hold M in frame; K.μ⁺ creates only content-subspace V-positions (by its amended precondition `subspace(v) = s_C`), so new mappings target dom(C) and the link-subspace clause is unaffected; K.μ⁻ contracts dom(M(d)), preserving both clauses; K.μ~ is a distinguished composite K.μ⁻ + K.μ⁺ (ASN-0047) with a bijection `π : dom(M(d)) → dom(M'(d))` satisfying `M'(d)(π(v)) = M(d)(v)`. We establish S3★ preservation first by direct decomposition, then derive the stronger property that link-subspace mappings are fixed.

*S3★ by decomposition.* K.μ~ decomposes into K.μ⁻ followed by K.μ⁺. K.μ⁻ restricts dom(M(d)) with values unchanged — content-subspace mappings still target dom(C), link-subspace mappings still target dom(L) — so S3★ holds for the intermediate state. K.μ⁺ (amended) adds only content-subspace V-positions targeting dom(C) by precondition, preserving existing mappings by frame — S3★ holds for M'(d).

**S3★-aux (SubspaceExhaustiveness).** In every reachable state, all V-positions have subspace s_C or s_L:

  `(A d, v : v ∈ dom(M(d)) : subspace(v) = s_C ∨ subspace(v) = s_L)`

*Proof.* By induction on transition sequences from Σ₀. Base: M₀ = ∅, the property holds vacuously. Step: K.μ⁺ (amended) creates only s_C positions; K.μ⁺_L creates only s_L positions; K.μ⁻ removes positions without altering subspaces of survivors; K.μ~ decomposes into K.μ⁻ + K.μ⁺, each maintaining the property independently of fixity; K.α, K.δ, K.λ, K.ρ hold M in frame. ∎

**Link-subspace fixity under K.μ~.** Since K.μ⁺ (amended) requires `subspace(v) = s_C` for new V-positions, K.μ⁺ cannot create link-subspace V-positions. Let `dom_L(M(d)) = {v ∈ dom(M(d)) : subspace(v) = s_L}` denote the link-subspace V-positions. With S3★ now established for M'(d), π must map link-subspace positions to link-subspace positions: if `v ∈ dom_L(M(d))` then `M(d)(v) ∈ dom(L)`, and `M'(d)(π(v)) = M(d)(v) ∈ dom(L)`, so `subspace(π(v)) = s_L`: by S3★-aux, `subspace(π(v)) ∈ {s_C, s_L}`; the case `subspace(π(v)) = s_C` is eliminated because a content-subspace position mapping to dom(L) would violate S3★'s content clause, since `M'(d)(π(v)) ∈ dom(L)` and `dom(L) ∩ dom(C) = ∅` (L14, which depends on SC-NEQ). Thus `π` restricted to `dom_L(M(d))` is an injection into `dom_L(M'(d))`. Since K.μ⁺ cannot create link-subspace V-positions, `|dom_L(M'(d))| ≤ |dom_L(M(d))|`. If K.μ⁻ removed `r ≥ 1` link-subspace positions, then `|dom_L(M'(d))| ≤ |dom_L(M(d))| − r`, and the injection from `dom_L(M(d))` (size N) into `dom_L(M'(d))` (size at most N − r) cannot exist. Therefore `r = 0` — no link-subspace positions are removed. It follows that `M'(d)` restricted to `dom_L(M(d))` equals `M(d)` restricted to `dom_L(M(d))`. Let `M_int(d)` denote the intermediate arrangement after K.μ⁻ but before K.μ⁺. K.μ⁻ removes none of the link-subspace positions (`r = 0`) and preserves the values of all surviving positions, so `M_int(d)|_{dom_L} = M(d)|_{dom_L}`. K.μ⁺ (amended) operates on `M_int(d)`: its frame preserves pre-existing mappings (`(A v : v ∈ dom(M_int(d)) : M'(d)(v) = M_int(d)(v))`), and its subspace restriction prevents creating new link-subspace positions. Chaining: `M'(d)|_{dom_L} = M_int(d)|_{dom_L} = M(d)|_{dom_L}`. Each surviving link-subspace mapping retains its value in dom(L).


## Link-subspace extension

**K.μ⁺_L (LinkSubspaceExtension).** Extends a document's arrangement in the link subspace.

*Precondition:*
- d ∈ E_doc
- ℓ ∈ dom(L)  (the target link must already exist in dom(L) — placed there by some prior K.λ)
- origin(ℓ) = d  (only home-document links may be arranged)
- V-position v_ℓ satisfies:
  - subspace(v_ℓ) = s_L
  - m_L ≥ 2, where: if V_{s_L}(d) ≠ ∅, m_L is the common depth of existing link-subspace V-positions (determined by S8-depth); if V_{s_L}(d) = ∅, m_L is a parameter of the transition, subject only to m_L ≥ 2. The lower bound is structural: ordinal shift at depth 1 alters the subspace identifier (`shift([s_L], 1) = [s_L + 1]`, violating subspace closure TA7a), so the link subspace requires depth at least 2
  - If V_{s_L}(d) = ∅: v_ℓ is the minimum position `[s_L, 1, ..., 1]` of depth m_L (D-MIN)
  - If V_{s_L}(d) ≠ ∅: v_ℓ = shift(max(V_{s_L}(d)), 1), extending the contiguous range (D-CTG)
  - #v_ℓ = m_L (S8-depth within the link subspace)

*Effect:* `M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}`

*Frame:* `C' = C; L' = L; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R`

We verify `v_ℓ ∉ dom(M(d))`, as required for M'(d) to be a proper extension preserving S2 (ArrangementFunctionality). When `V_{s_L}(d) = ∅`: no link-subspace V-position exists in dom(M(d)), and `subspace(v_ℓ) = s_L`, so `v_ℓ ∉ dom(M(d))`. When `V_{s_L}(d) ≠ ∅`: `v_ℓ = shift(max(V_{s_L}(d)), 1) > max(V_{s_L}(d))` by TS4 (ShiftStrictIncrease, ASN-0034), placing v_ℓ beyond all existing link-subspace positions. In both cases, `subspace(v_ℓ) = s_L` and `s_L ≠ s_C` (SC-NEQ) ensures no collision with text-subspace positions (T7). Therefore `v_ℓ ∉ dom(M(d))`.

The preconditions ensure that after the extension, D-CTG (contiguity), D-MIN (minimum position), and S8-depth (uniform depth) hold for the link subspace of d. S3★ is satisfied: `subspace(v_ℓ) = s_L` and `M'(d)(v_ℓ) = ℓ ∈ dom(L')`.

The origin restriction `origin(ℓ) = d` distinguishes link-subspace extension from content-subspace extension, where K.μ⁺ intentionally permits `origin(a) ≠ d` — that is content transclusion, an established architectural feature. Link transclusion — arranging a foreign-origin link in a document's link subspace — is excluded by design. Nelson: "A document includes only the links of which it is the home document" (LM 4/31). The byte stream admits transclusion ("The virtual byte stream of a document may include bytes from any other document," LM 4/10); links do not. Links maintain "permanent order of arrival" in their home document, and home document determines ownership ("A link need not point anywhere in its home document. Its home document indicates who owns it," LM 4/12). Arranging a link with `origin(ℓ) ≠ d` would place an out-link in a document that does not own it — violating the ownership semantics that home-document identity is meant to carry. The architecture provides alternatives: bidirectional link search discovers all links attached to transcluded content regardless of which document houses them; creating a new link in one's own document is the natural analog of annotation. Gregory confirms that the implementation achieves origin matching by procedural atomicity — `docreatelink` both allocates the link ISA under the document's address and places it in the document's arrangement in a single operation — but no runtime guard exists; `acceptablevsa` unconditionally returns TRUE and `docopy` performs no origin check. The origin restriction in K.μ⁺_L formalizes the structural guarantee that the implementation achieves by construction.

**Per-subspace arrangement invariants under K.μ⁺_L.** S8a (VPositionWellFormedness): the quantifier `(A v ∈ dom(M(d)) : v₁ ≥ 1 : zeros(v) = 0 ∧ v > 0)` covers *all* V-positions with `v₁ ≥ 1`, including link-subspace positions. We must establish that `s_L ≥ 1`: by L1, every link address is element-level (`zeros(ℓ) = 3`), so by T4 (ASN-0034), every element-field component is strictly positive — in particular `fields(ℓ).E₁ = s_L > 0`. Since K.μ⁺_L uses the same identifier s_L for V-positions, link-subspace V-positions have `v₁ = s_L ≥ 1` and fall under S8a's quantifier. For text-subspace positions: unchanged. For the new link-subspace position v_ℓ: K.μ⁺_L places `v_ℓ = [s_L, 1, ..., 1]` (D-MIN) or `shift(max(V_{s_L}(d)), 1)` (D-CTG). In either case, every component of v_ℓ is strictly positive — s_L > 0 by the above, and the remaining components are 1 or incremented from positive values — so `zeros(v_ℓ) = 0 ∧ v_ℓ > 0`. S8-fin: adding one position to a finite set preserves finiteness. For the link subspace specifically: S8-depth is satisfied by K.μ⁺_L's precondition (`#v_ℓ = m_L`). D-CTG (VContiguity) and D-MIN (VMinimumPosition) are quantified over *all* subspaces S. For the text subspace (S = s_C): V_{s_C}(d) is unchanged. For the link subspace (S = s_L): K.μ⁺_L's precondition places v_ℓ at the minimum position if V_{s_L}(d) was empty, or at the next contiguous position if non-empty, satisfying both D-CTG and D-MIN. D-SEQ follows from D-CTG, D-MIN, S8-fin, and S8-depth (as derived in ASN-0036). S8 (SpanDecomposition): S8's quantifier `v₁ ≥ 1` captures all V-positions in the extended state — since both `s_C ≥ 1` and `s_L ≥ 1` (established above for S8a) — extending coverage to the link subspace. S8 is derived from S8-fin, S8a, S2, and S8-depth (ASN-0036), all verified above. The new link-subspace mapping `(v_ℓ, ℓ)` either forms a new width-1 correspondence run or extends the last existing link-subspace run by one position if I-adjacent. All existing runs — both text-subspace and link-subspace — are unchanged: K.μ⁺_L preserves existing mappings (frame), and the new position `v_ℓ ∉ dom(M(d))` falls in no existing run, so no existing run is split or modified.


## Link-subspace ownership

**CL-OWN (LinkSubspaceOwnership).** In every reachable state:

  `(A d, v : v ∈ dom(M(d)) ∧ subspace(v) = s_L : origin(M(d)(v)) = d)`

Every document's link-subspace arrangement contains only its own links. This is maintained by two mechanisms: K.μ⁺_L's precondition `origin(ℓ) = d` ensures ownership at creation, and link-subspace fixity under K.μ~ ensures preservation through reordering — no transition can place a foreign-origin link in a document's link subspace.

*Proof.* By induction on transition sequences from Σ₀. Base: M₀(d) = ∅ for all d, so the property holds vacuously. Step: K.μ⁺_L adds `(v_ℓ, ℓ)` with `origin(ℓ) = d` (precondition) and preserves existing mappings (frame); K.μ⁺ (amended) adds only content-subspace positions (`subspace(v) = s_C`), so no link-subspace change; K.μ⁻ removes positions without altering values of survivors; K.μ~ preserves link-subspace mappings identically (link-subspace fixity); K.α, K.δ, K.λ, K.ρ hold M in frame. ∎


## Coupling and isolation

The elementary transitions do not all occur independently. Some must co-occur to maintain invariants (coupling); some must leave other components unchanged (isolation). The weakest-precondition calculus makes the coupling constraints visible.

A clarification on scope. The frame conditions stated above describe individual elementary transitions: K.μ⁺ alone does not modify R, K.α alone does not modify M, and so on. Coupling constraints describe required co-occurrence — when K.μ⁺ occurs, K.ρ must also occur in the same composite transition.

**Definition (Current containment).** The *current containment* of state Σ is the set of all document-content pairs where the content is presently in the document's arrangement:

`Contains(Σ) = {(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))}`

This is a derived quantity of the state — it captures what each document currently displays. We will need it both in the valid composite definition (as a state invariant) and in the coupling derivations that follow.

**Definition (Valid composite transition).** A composite transition Σ → Σ' is *valid* iff it is a finite sequence of elementary transitions Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ' satisfying two conditions:

(1) *Elementary preconditions:* each step Σᵢ → Σᵢ₊₁ satisfies the precondition of its elementary transition kind, evaluated at the intermediate state Σᵢ.

(2) *Coupling constraints:* J0, J1, and J1' hold for the composite — evaluated between the initial state Σ and the final state Σ'.

**Lemma (Permanence from elementary frames).** Every valid composite transition satisfies P0, P1, and P2. Each elementary transition's frame ensures: K.α extends dom(C) preserving existing entries (all others hold C' = C), giving P0; K.δ extends E (all others hold E' = E), giving P1; K.ρ extends R (all others hold R' = R), giving P2. By transitivity over any finite sequence satisfying (1), the composite inherits all three permanence properties.

**Theorem (Reachable-state invariants).** Every state reachable from Σ₀ by a finite sequence of valid composite transitions satisfies P4 (Contains(Σ) ⊆ R), P6, P7, P7a, P8, S2, S3, S8a, S8-depth, S8-fin, D-CTG, and D-MIN.

*Base case.* At Σ₀: dom(C₀) = ∅ makes P6 vacuous (no content, so no origin to check); R₀ = ∅ makes P7 vacuous (no provenance entries to ground); dom(C₀) = ∅ makes P7a vacuous (no content to require provenance for); (E₀)_doc = ∅ makes P4 vacuous (no documents, so Contains(Σ₀) = ∅ ⊆ R₀); E₀ = {n₀} with IsNode(n₀) makes P8 vacuous (no non-node entities); (E₀)_doc = ∅ makes S2–S8-fin, D-CTG, and D-MIN vacuous (no arrangements exist).

*Inductive step.* For any reachable state Σ satisfying the above, every valid composite Σ → Σ' produces Σ' satisfying the same — P0/P1/P2 by the permanence lemma; S2/S3/S8a/S8-depth/S8-fin/D-CTG/D-MIN by the arrangement invariants lemma; P8 as derived above; P4, P6, P7, and P7a as derived below.

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

**P4a (Historical fidelity).** Every entry in R reflects an actual past containment event:

`(A (a, d) ∈ R :: (E Σ_k in the transition history : a ∈ ran(M_k(d))))`

*Derivation.* By induction on the transition sequence. *Base:* R₀ = ∅; the quantifier is vacuously satisfied. *Inductive step:* for (a, d) ∈ R' \ R, J1' gives a ∈ ran(M'(d)) \ ran(M(d)) — the post-state Σ' is a witnessing state where d's arrangement contains a. For (a, d) ∈ R, the inductive hypothesis provides a prior witnessing state; P2 ensures the entry persists in R'. ∎

**J2 (Contraction isolation).** The elementary transition K.μ⁻ requires no coupling — it is self-sufficient with respect to P0–P2 and Contains(Σ) ⊆ R. As an elementary transition, K.μ⁻ satisfies:

`C' = C ∧ E' = E ∧ R' = R`

The wp analysis confirms this. For P0: K.μ⁻ does not touch C. For P1: does not touch E. For P2: does not touch R. For the provenance bound Contains(Σ) ⊆ R: contraction can only remove pairs from Contains, so Contains(Σ') ⊆ Contains(Σ) ⊆ R = R'. No co-occurring transition is needed to maintain any system invariant.

This is the deepest consequence of the design. Deletion is purely presentational — it changes what appears, not what exists or what has been. Gregory confirms: contraction "never triggers" provenance recording, and the provenance structure "is never pruned."

**J3 (Reordering isolation).** The distinguished composite K.μ~ is likewise self-sufficient:

`C' = C ∧ E' = E ∧ R' = R`

Reordering preserves ran(M(d)), so Contains(Σ') = Contains(Σ). All invariants are trivially maintained; no co-occurring transition is needed.

**J4 (Fork composite).** Nelson's forking creation mode — when the source arrangement is non-empty — is a composite whose elementary steps are exactly K.δ + K.μ⁺ + K.ρ, all serving the new document d_new:

**Definition (Fork).** A *fork* of d_src to d_new is a composite transition Σ → Σ', with *precondition* d_src ∈ E_doc ∧ M(d_src) ≠ ∅, consisting of:

(i) K.δ creating d_new with d_new ∉ E_doc,

(ii) K.μ⁺ populating M'(d_new) with ran(M'(d_new)) ⊆ ran(M(d_src)),

(iii) K.ρ recording provenance for each a ∈ ran(M'(d_new)),

and no other elementary steps.

Since none of K.δ, K.μ⁺, K.ρ modify C (each has C' = C in its frame), a fork satisfies dom(C') = dom(C) — no new content is created. The provenance conclusion — that (a, d_new) ∈ R' for every a ∈ ran(M'(d_new)) — follows from J1 applied to the fresh-document case: the convention M(d_new) = ∅ gives ran(M'(d_new)) \ ran(M(d_new)) = ran(M'(d_new)), and J1 directly requires provenance recording for each such address. No additional constraint beyond J1 is needed.

The new document d_new is created empty (K.δ), its arrangement extended with mappings to the source's I-addresses (K.μ⁺), and the new associations recorded (K.ρ). The precondition M(d_src) ≠ ∅ ensures K.μ⁺ is well-formed: with at least one I-address to transclude, the strict domain extension dom(M'(d_new)) ⊃ dom(M(d_new)) = ∅ is satisfiable. When the source arrangement is empty, the fork definition does not apply — creation from an empty source is ex nihilo (K.δ alone), not a fork. Nelson: "the new document's id will indicate its ancestry."

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

The containment relation `Contains(Σ)` (ASN-0047) is defined as `{(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))}` — unscoped across all subspaces. With link-subspace mappings, `Contains(Σ')` includes `(ℓ, d)` for every link ℓ mapped in d's arrangement. P4 requires `Contains(Σ) ⊆ R`, but provenance entries satisfy P7: `(A (a, d) ∈ R :: a ∈ dom(C))`. Since `ℓ ∈ dom(L)` and `dom(L) ∩ dom(C) = ∅` (L14), `(ℓ, d) ∉ R` — P4 is unsatisfiable for the unscoped relation once link-subspace mappings exist.

**Contains_C(Σ) (ContentContainment).**

  `Contains_C(Σ) = {(a, d) : d ∈ E_doc ∧ (E v : v ∈ dom(M(d)) ∧ subspace(v) = s_C : M(d)(v) = a)}`

**P4★ (ProvenanceBounds, content-subspace).**

  `Contains_C(Σ) ⊆ R`

P4★ supersedes P4 for the extended state. In pre-extension states (no link-subspace mappings), `Contains_C(Σ) = Contains(Σ)`, so P4★ reduces to P4. Existing transitions preserve P4★: K.α, K.δ, K.ρ hold M in frame; K.μ⁻ contracts dom(M(d)), which can only shrink Contains_C; K.μ~ preserves P4★ by the link-subspace fixity established in the S3★ analysis above. Since π bijects dom(M(d)) onto dom(M'(d)) and maps dom_L bijectively onto dom_L (by fixity), it maps the complement dom_C(M(d)) = dom(M(d)) \ dom_L(M(d)) bijectively onto dom_C(M'(d)) = dom(M'(d)) \ dom_L(M'(d)). These complements are exactly the content-subspace positions by S3★-aux: every V-position has subspace s_C or s_L, so `dom(M(d)) \ dom_L(M(d)) = {v ∈ dom(M(d)) : subspace(v) = s_C}`. With `M'(d)(π(v)) = M(d)(v)` for each such v, the set `{a : (E v ∈ dom_C(M(d)) : M(d)(v) = a)} = {a : (E u ∈ dom_C(M'(d)) : M'(d)(u) = a)}`, so `Contains_C(Σ') = Contains_C(Σ) ⊆ R = R'`.

**Note on K.μ⁺ and P4★.** K.μ⁺ alone adds a content-subspace V-position mapping to address `a`, placing `(a, d) ∈ Contains_C(Σ')`. Its frame has `R' = R`, so if `(a, d) ∉ R`, P4★ is violated at the intermediate state. P4★ is restored at composite boundaries by the coupling constraint J1★, which requires K.ρ to record provenance for every content-subspace arrangement extension. See the two-layer proof structure in ExtendedReachableStateInvariants.


## Scoped coupling constraints

The coupling constraints J1, J1' (ASN-0047) were formulated before link-subspace mappings existed. They must be scoped to content-subspace arrangement extensions; otherwise J1 and P7 are mutually unsatisfiable — J1 would require provenance recording for the link address ℓ entering ran(M'(d)), but P7 requires every provenance entry to reference dom(C), and ℓ ∈ dom(L) with dom(L) ∩ dom(C) = ∅ (L14).

**J1★ (ExtensionRecordsProvenance, content-subspace).**

  `(A Σ → Σ', d ∈ E'_doc, a : (E v ∈ dom(M'(d)) : subspace(v) = s_C ∧ M'(d)(v) = a) ∧ ¬(E v ∈ dom(M(d)) : subspace(v) = s_C ∧ M(d)(v) = a) : (a, d) ∈ R')`

J1★ is range-based: it triggers whenever an I-address `a` is new to the content-subspace range of M'(d), regardless of whether the V-position carrying it existed in dom(M(d)). This matches J1's range-based structure (`a ∈ ran(M'(d)) \ ran(M(d))`), scoped to the content subspace. A domain-based formulation — `v ∈ dom(M'(d)) \ dom(M(d))` — would fail for value replacement at a reused position: K.μ⁻ removing `[1,2]` followed by K.μ⁺ re-adding `[1,2] ↦ a₃` leaves the V-position in both domains, making `dom(M'(d)) \ dom(M(d))` empty at that position, while `a₃` is genuinely new to the content-subspace range and requires provenance recording.

**J1'★ (ProvenanceRequiresExtension, content-subspace).**

  `(A Σ → Σ', a, d : (a, d) ∈ R' \ R : (E v ∈ dom(M'(d)) : subspace(v) = s_C ∧ M'(d)(v) = a) ∧ ¬(E v ∈ dom(M(d)) : subspace(v) = s_C ∧ M(d)(v) = a))`

J1'★ is likewise range-based, matching J1': every new provenance entry `(a, d) ∈ R' \ R` must correspond to an I-address `a` that is new to the content-subspace range — present in the content-subspace range of M'(d) but absent from the content-subspace range of M(d).

Link-subspace extensions (K.μ⁺_L) do not trigger provenance recording: the link address ℓ enters ran(M'(d)), but no content-subspace V-position maps to ℓ — `subspace(v_ℓ) = s_L ≠ s_C` (SC-NEQ) — so ℓ is not in the content-subspace range of M'(d), and J1★ is vacuous. P7 (ProvenanceGrounding) — `(A (a, d) ∈ R :: a ∈ dom(C))` — is preserved because R is unchanged (K.μ⁺_L holds R in frame).

**ValidComposite★ (ValidComposite, amended).** A composite transition Σ → Σ' in the extended state Σ = (C, L, E, M, R) is *valid* iff it is a finite sequence of transitions `Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ'` — drawn from K.α (amended), K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻ (amended), K.μ~, and K.ρ — satisfying:

1. *Transition preconditions:* each step `Σᵢ → Σᵢ₊₁` satisfies the precondition of its transition kind, evaluated at the intermediate state `Σᵢ`. K.μ~ appearing in the sequence is shorthand for its K.μ⁻ + K.μ⁺ decomposition (ASN-0047) — it expands into two consecutive elementary steps, each satisfying its own precondition at the respective intermediate state.
2. *Coupling constraints:* J0, J1★, and J1'★ hold for the composite — evaluated between the initial state Σ and the final state Σ'.

This supersedes ValidComposite (ASN-0047) by extending the elementary transition set with K.λ and K.μ⁺_L, and replacing J1/J1' with J1★/J1'★ — scoping provenance coupling to content-subspace arrangement changes. J0 (AllocationRequiresPlacement) is unchanged — it constrains content allocation (K.α), which remains content-subspace only.

**Extended completeness.** Seven elementary transition kinds — K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ — plus the distinguished composite K.μ~, are complete for the five-component state (C, L, E, M, R). The argument extends structurally: C admits one growth mode (K.α); L admits one growth mode (K.λ); E admits one growth mode (K.δ); R admits one growth mode (K.ρ); M's growth partitions by subspace — K.μ⁺ for content-subspace extension, K.μ⁺_L for link-subspace extension — and K.μ⁻ handles contraction. Any modification to a finite partial function decomposes into additions and removals; replacement decomposes into K.μ⁻ followed by K.μ⁺. The same reasoning — one growth mode per append-only component, addition and removal as the two mutation modes for M — yields completeness for the extended state.


## Orphan links and coupling flexibility

The coupling constraints do not require K.λ to be paired with K.μ⁺_L. A composite consisting of K.λ alone is valid: J0 is vacuous (no content allocated), J1★ is vacuous (no content-subspace extension), and J1'★ is vacuous (no provenance change). The result is a link in dom(L) with no placement in any document's arrangement — an *orphan link*. This is a valid system state, not an error condition. State invariants are preserved: M, C, E, R are all in K.λ's frame (unchanged), so all arrangement, content, entity, and provenance invariants hold identically. L grows by one entry: dom(L') = dom(L) ∪ {ℓ}. K.λ's preconditions guarantee L0 (ℓ has subspace s_L, and ℓ ∉ dom(C) ensures dom(L') ∩ dom(C) = ∅), L1 (zeros(ℓ) = 3), L1a (origin(ℓ) ∈ E_doc), L3 (K.λ requires (F, G, Θ) ∈ Link, so L3 is established for the new entry; L12 preserves all existing entries), L12 (existing entries unchanged: L'(ℓ') = L(ℓ') for all ℓ' ∈ dom(L)), and L14 (disjointness: ℓ ∉ dom(C), so dom(L') ∩ dom(C') = ∅). Nelson explicitly diagrams "deleted links" as a category of document content (LM 4/9): links that exist in permanent storage but are "not currently addressable, awaiting historical backtrack functions."

Link withdrawal via K.μ⁻ applied to the link subspace would in principle produce the same state — a link present in L but absent from all current arrangements — but is constrained by D-CTG: removing an interior link-subspace V-position creates a gap in the contiguous range, and K.μ~ cannot close it (link-subspace mappings are fixed, as shown above). Valid link-subspace contractions are suffix truncations: for `V_{s_L}(d) = {[s_L, 1, …, 1, k] : 1 ≤ k ≤ n}` (by D-SEQ), the result must be `{[s_L, 1, …, 1, k] : 1 ≤ k ≤ n'}` for some `0 ≤ n' < n`. Removing an interior position breaks contiguity (violating D-CTG), and removing the minimum while positions above it remain violates D-MIN. Any suffix `{[s_L, 1, …, 1, k] : n' < k ≤ n}` can be removed at once — including all positions when `n' = 0`, since D-CTG and D-MIN hold vacuously for the empty set. Nelson's design suggests a different mechanism: link addresses are permanent and "not currently addressable" when withdrawn (LM 4/9), paralleling deleted bytes — the link transitions to inactive status while preserving its arrangement position, rather than being removed from M(d). The precise withdrawal mechanism is deferred to the open question on withdrawal invariants.

We do not add a J0 analog for links — the orphan state is architecturally intentional, satisfying both the permanence guarantee (L12: links are immutable once created) and the owner's right to withdraw (Nelson, LM 2/29).


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

**P3★ (ArrangementMutabilityOnly, extended).** Arrangements admit three modes of change: (a) extension, (b) contraction, (c) reordering. No other component — specifically C, L, E, R — admits contraction or reordering:

  `(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ dom(L) ⊆ dom(L') ∧ E ⊆ E' ∧ R ⊆ R')`

P3★ supersedes P3 (ASN-0047) by including L in the enumeration. L admits only extension, by L12: `dom(L) ⊆ dom(L') ∧ (A ℓ ∈ dom(L) : L'(ℓ) = L(ℓ))`.

**P5★ (DestructionConfinement, extended).** For every state transition Σ → Σ':

  (a) `dom(C') ⊇ dom(C) ∧ (A a : a ∈ dom(C) : C'(a) = C(a))`

  (b) `dom(L') ⊇ dom(L) ∧ (A ℓ : ℓ ∈ dom(L) : L'(ℓ) = L(ℓ))`

  (c) `E' ⊇ E`

  (d) `R' ⊇ R`

The only component that can lose information is M. P5★ supersedes P5 (ASN-0047) by adding clause (b), immediate from L12.


## Worked example: fork with subsequent insertion

We trace a concrete scenario to ground the abstract definitions. Let the starting state Σ₁ contain node 1, account 1.0.1, and document d₁ = 1.0.1.0.1 with two characters:

> C₁ = {1.0.1.0.1.0.1.1 ↦ 'H', 1.0.1.0.1.0.1.2 ↦ 'i'}
> E₁ = {1, 1.0.1, 1.0.1.0.1}
> M₁(d₁) = {[1,1] ↦ 1.0.1.0.1.0.1.1, [1,2] ↦ 1.0.1.0.1.0.1.2}
> R₁ = {(1.0.1.0.1.0.1.1, d₁), (1.0.1.0.1.0.1.2, d₁)}

We write a₁ = 1.0.1.0.1.0.1.1 and a₂ = 1.0.1.0.1.0.1.2 for brevity.

**Fork d₁ to d₂ = 1.0.1.0.2.** This is J4's compound K.δ + K.μ⁺ + K.ρ.

*K.δ:* E₂ = E₁ ∪ {1.0.1.0.2}. The address 1.0.1.0.2 is obtained from 1.0.1.0.1 by inc(·, 0) at the document field — a sibling allocation (TA5(c), ASN-0034). M₂(d₂) = ∅.

*K.μ⁺:* M₂(d₂) = {[1,1] ↦ a₁, [1,2] ↦ a₂}. The same I-addresses as d₁ — transclusion, case (ii). No new content enters C. The V-positions [1,1] and [1,2] satisfy S8a (all components strictly positive, zeros = 0) and S8-depth (shared first component 1, uniform depth 2).

*K.ρ:* R₂ = R₁ ∪ {(a₁, d₂), (a₂, d₂)}.

Verification against the resulting state Σ₂:

- *J0:* No fresh content (dom(C₂) = dom(C₁)), so vacuously satisfied.
- *J1:* ran(M₂(d₂)) \ ran(M₁(d₂)) = {a₁, a₂} \ ∅ = {a₁, a₂} (M₁(d₂) = ∅ since d₂ ∉ (E₁)_doc). Both (a₁, d₂) and (a₂, d₂) are in R₂. ✓
- *J4:* d₂ ∈ E₂_doc \ E₁_doc, ran(M₂(d₂)) = {a₁, a₂} ⊆ ran(M₁(d₁)). ✓
- *P4:* Contains(Σ₂) = {(a₁, d₁), (a₂, d₁), (a₁, d₂), (a₂, d₂)} ⊆ R₂. ✓
- *P5:* C₂ = C₁; E₂ ⊇ E₁; R₂ ⊇ R₁. Only M changed. ✓
- *P8:* parent(d₂) = parent(1.0.1.0.2) = 1.0.1 ∈ E₁ ⊆ E₂. The existing non-node entity 1.0.1 (account) retains parent(1.0.1) = 1 ∈ E₂. ✓

**Insert new content into d₂.** Compound K.α + K.μ⁺ + K.ρ.

*K.α:* Allocate a₃ = 1.0.1.0.2.0.1.1 with C₃(a₃) = '!'. The address falls under d₂'s prefix (S7a): origin(a₃) = 1.0.1.0.2 = d₂. By GlobalUniqueness, a₃ is fresh.

*K.μ⁺:* M₃(d₂) = M₂(d₂) ∪ {[1,3] ↦ a₃}. V-position [1,3] has first component 1 and depth 2, matching [1,1] and [1,2] (S8-depth, non-vacuously: shared first component). Referential integrity: a₃ ∈ dom(C₃) (S3). ✓

*K.ρ:* R₃ = R₂ ∪ {(a₃, d₂)}.

Verification:

- *J0:* a₃ ∈ dom(C₃) \ dom(C₂), and d₂ ∈ E₃_doc with M₃(d₂)([1,3]) = a₃. ✓
- *J1:* ran(M₃(d₂)) \ ran(M₂(d₂)) = {a₃}, and (a₃, d₂) ∈ R₃. ✓
- *P4:* Contains(Σ₃) adds (a₃, d₂); this pair is in R₃. ✓
- *P6:* origin(a₃) = d₂ = 1.0.1.0.2 ∈ E₃_doc. ✓
- *P7:* (a₃, d₂) ∈ R₃ and a₃ ∈ dom(C₃). ✓

**Delete a₃ from d₂'s arrangement (K.μ⁻).** Remove the mapping at V-position [1,3] — the maximum end of V_{s_C}(d₂), satisfying the K.μ⁻ amendment's D-CTG/D-MIN postcondition.

*K.μ⁻:* dom(M₄(d₂)) = {[1,1], [1,2]} ⊂ dom(M₃(d₂)) = {[1,1], [1,2], [1,3]}. The surviving mappings are unchanged: M₄(d₂)([1,1]) = a₁, M₄(d₂)([1,2]) = a₂. D-MIN: min(V_1(d₂)) = [1,1] = [s_C, 1]. D-CTG: {[1,1], [1,2]} is contiguous.

Verification:

- *J2:* C₄ = C₃; E₄ = E₃; R₄ = R₃. All permanent and historical state unchanged. ✓
- *P4:* Contains(Σ₄) = {(a₁, d₁), (a₂, d₁), (a₁, d₂), (a₂, d₂)}. The pair (a₃, d₂) is no longer in Contains — d₂ no longer displays a₃. Yet (a₃, d₂) ∈ R₄: the stale entry persists. Contains(Σ₄) ⊂ Contains(Σ₃), while R₄ = R₃. ✓
- *P5:* C₄ = C₃; E₄ = E₃; R₄ = R₃. Only M changed. ✓

The divergence is now concrete: R₄ records that d₂ once contained a₃, while the current arrangement does not. This is the historical memory that J2 preserves — deletion is purely presentational.

**Reorder d₂'s arrangement (K.μ~).** Swap V-positions [1,1] and [1,2].

*K.μ~:* The bijection π : {[1,1], [1,2]} → {[1,1], [1,2]} with π([1,1]) = [1,2] and π([1,2]) = [1,1]. The definition requires M₅(d₂)(π(v)) = M₄(d₂)(v) for all v ∈ dom(M₄(d₂)), giving M₅(d₂) = {[1,1] ↦ a₂, [1,2] ↦ a₁}. Both target V-positions satisfy S8a (all components strictly positive) and S8-depth (uniform depth 2, shared first component 1).

Verification:

- *J3:* C₅ = C₄; E₅ = E₄; R₅ = R₄. All permanent and historical state unchanged. ✓
- *ran preservation:* ran(M₅(d₂)) = {a₁, a₂} = ran(M₄(d₂)). The multiset of referenced I-addresses is identical; only V-positions changed. ✓
- *P4:* Contains(Σ₅) = Contains(Σ₄) ⊆ R₄ = R₅. Since ran is preserved for d₂ and no other arrangement changed, the current containment set is unchanged. ✓
- *P5:* C₅ = C₄; E₅ = E₄; R₅ = R₄. Only M changed. ✓

Reordering is the simplest transition to verify: it touches nothing beyond the V-position mapping, and all invariants hold by the frame conditions alone.

The four steps exercise J0, J1, J2, J3, J4, P4, P5, P6, P7, and P8, and demonstrate M(d) = ∅ for freshly created documents (by totality of M) (J1 verification of the fork), the divergence between current containment and historical provenance (J2 verification of the deletion), and the presentational isolation of reordering (J3 verification of the swap).


## Worked example: link allocation and arrangement

We verify the central postconditions on concrete tumbler values. Let `s_C = 1` and `s_L = 2` (satisfying SC-NEQ: `1 ≠ 2`). Consider document `d` at address `1.0.1.0.1` with two text content addresses allocated and arranged.

*Initial state.* `dom(C) = {1.0.1.0.1.0.1.1, 1.0.1.0.1.0.1.2}`, `dom(L) = ∅`, `E_doc = {1.0.1.0.1}`.

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
- S3★, CL-OWN: M unchanged, hold from pre-state

**Step 2: K.μ⁺_L — arrange link.** Place ℓ at V-position `v_ℓ = [2, 1]`.

Precondition verification:
- `d ∈ E_doc`
- `ℓ = 1.0.1.0.1.0.2.1 ∈ dom(L')`
- `origin(ℓ) = 1.0.1.0.1 = d`
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

**Step 3: K.μ~ — reorder text, verify link fixity.** Swap the two text positions: `π([1,1]) = [1,2]`, `π([1,2]) = [1,1]`, `π([2,1]) = [2,1]`.

Let `a₁ = 1.0.1.0.1.0.1.1` and `a₂ = 1.0.1.0.1.0.1.2`. Pre-state arrangement: `M'(d) = {[1,1] ↦ a₁, [1,2] ↦ a₂, [2,1] ↦ ℓ}`.

Post-state: `M''(d) = {[1,1] ↦ a₂, [1,2] ↦ a₁, [2,1] ↦ ℓ}`.

Link-subspace fixity: `M''(d)|_{dom_L} = {[2,1] ↦ ℓ} = M'(d)|_{dom_L}` — the link-subspace mapping is unchanged. The fixity argument: π maps `[2,1]` to some position `u`; `M''(d)(u) = M'(d)([2,1]) = ℓ ∈ dom(L')`. By S3★-aux, `subspace(u) ∈ {s_C, s_L}`. If `subspace(u) = s_C = 1`, then S3★ requires `M''(d)(u) ∈ dom(C)`, but `ℓ ∈ dom(L')` and `dom(L') ∩ dom(C) = ∅` (L14) — contradiction. So `subspace(u) = s_L = 2`. Since K.μ⁺ cannot create link-subspace positions, `u` must have existed in the pre-state's link subspace: `u = [2,1]`. Therefore `π([2,1]) = [2,1]` — the link-subspace mapping is fixed by logical necessity, not by fiat.


## Extended reachable-state invariants

**ExtendedReachableStateInvariants.** Every state reachable from Σ₀ = (C₀, L₀, E₀, M₀, R₀) by a finite sequence of valid composite transitions — composed from the transitions K.α (amended), K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻ (amended), K.μ~ (shorthand for its K.μ⁻ + K.μ⁺ decomposition), and K.ρ — satisfies:

  S0 ∧ S1 ∧ S2 ∧ S3★ ∧ S3★-aux ∧ S8a ∧ S8-fin ∧ S8-depth ∧ S8 ∧ D-CTG ∧ D-MIN ∧ P0 ∧ P1 ∧ P2 ∧ P3★ ∧ P4★ ∧ P5★ ∧ P6 ∧ P7 ∧ P7a ∧ P8 ∧ L0 ∧ L1 ∧ L1a ∧ L3 ∧ L12 ∧ L14 ∧ CL-OWN

This supersedes the ReachableStateInvariants theorem (ASN-0047) by replacing S3 with S3★, P4 with P4★, P3 with P3★, P5 with P5★, adding S3★-aux (subspace exhaustiveness), CL-OWN (link-subspace ownership), L3 (triple endset structure), and the remaining link invariants L0, L1, L1a, L12, L14, and covering the extended transition set including K.λ and K.μ⁺_L.

*Proof.* The proof proceeds by induction on the number of valid composite transitions from Σ₀. The invariant set partitions into two classes: *elementary invariants* preserved by each elementary transition individually, and *composite invariants* that may be violated at intermediate states within a composite but hold at every composite boundary.

**Base.** The extended initial state Σ₀ satisfies all invariants (verified in the Link store and extended system state section — L₀ = ∅ satisfies link invariants vacuously, including L3; S3★ and P4★ reduce to S3 and P4; S3★-aux holds vacuously since M₀(d) = ∅ for all d; D-CTG and D-MIN hold vacuously since V_S(d) = ∅ for every subspace S).

**Class (a): Elementary invariants** — preserved by each elementary transition individually. These are all invariants except P4★ and P7a: S0, S1, S2, S3★, S3★-aux, S8a, S8-fin, S8-depth, S8, D-CTG, D-MIN, P0, P1, P2, P3★, P5★, P6, P7, P8, L0, L1, L1a, L3, L12, L14, CL-OWN.

For K.α (amended): holds M and L in frame; S3★, S3★-aux preserved (M unchanged); content, entity, and provenance invariants preserved. L0 clause 2: `fields(a).E₁ = s_C` by the K.α amendment, so the new content address satisfies `(A a ∈ dom(C') :: fields(a).E₁ = s_C)`. L14: `fields(a).E₁ = s_C` and `s_C ≠ s_L` (SC-NEQ), and L0 clause 1 at the pre-state gives `(A ℓ ∈ dom(L) :: fields(ℓ).E₁ = s_L)`, so `a ∉ dom(L)` and `dom(C') ∩ dom(L') = (dom(C) ∪ {a}) ∩ dom(L) = ∅`. L1, L1a, L3, L12 preserved (L unchanged). For K.δ, K.ρ: hold both M and L in frame; C, L unchanged; S3★, S3★-aux preserved (M unchanged); link invariants preserved since neither L nor dom(C) is modified. P7 (ProvenanceGrounding) is elementary: K.ρ adds (a, d) with a ∈ dom(C) (precondition), and P0 ensures a ∈ dom(C') for all subsequent states; all other transitions hold R in frame, adding no new provenance entries, so existing entries retain their grounding in dom(C') (by P0). For K.μ⁺ (amended): holds L in frame; S3★ preserved (analyses above); S3★-aux preserved (new positions have subspace s_C by amendment); D-CTG, D-MIN preserved by the K.μ⁺ postcondition requirement; S8 follows from S8-fin, S8a, S2, S8-depth, T5, TA5(c), TA7a via the derivation chain in ASN-0036; link invariants preserved since L is unchanged. For K.μ⁻: holds L in frame; S3★ preserved (restriction of M(d) preserves both clauses); S3★-aux preserved (removal does not alter subspaces of surviving positions); D-CTG, D-MIN preserved by the K.μ⁻ amendment postcondition — by D-SEQ at the input state, V_S(d) is {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}, so valid contractions remove from the maximum end or remove all positions; S8 follows from S8-fin, S8a, S2, S8-depth, T5, TA5(c), TA7a via the derivation chain in ASN-0036; link invariants preserved since L is unchanged. For K.μ~: holds L in frame; K.μ~ decomposes into K.μ⁻ + K.μ⁺ (ASN-0047). S3★ preserved (decomposition analysis above); S3★-aux preserved (K.μ⁻ removes positions without altering subspaces, K.μ⁺ adds only s_C positions); link-subspace positions are fixed (link-subspace fixity, which requires S3★ and S3★-aux at the output — both now established). D-CTG and D-MIN hold at every intermediate state of the K.μ⁻ + K.μ⁺ decomposition and at the output: link-subspace fixity (r = 0) implies K.μ⁻ removes only content-subspace positions; by D-SEQ at the input, content-subspace positions form {[s_C, 1, ..., 1, k] : 1 ≤ k ≤ n}, so K.μ⁻ can remove a suffix leaving {[s_C, 1, ..., 1, k] : 1 ≤ k ≤ n'} for some 0 ≤ n' ≤ n, which satisfies D-CTG and D-MIN; the link subspace at the intermediate state equals the input (r = 0), preserving D-CTG/D-MIN. K.μ⁺ (amended) then rebuilds the content subspace satisfying D-CTG and D-MIN as a postcondition. For any bijection π, a valid decomposition always exists — in particular, n' = 0 (remove all content-subspace positions, then re-add with new mappings) satisfies D-CTG/D-MIN at the intermediate state vacuously for the content subspace. D-SEQ then applies at the output state. π bijects dom(M(d)) onto dom(M'(d)) preserving S8a, S8-depth, S8-fin (K.μ~ preconditions, ASN-0047), and link-subspace fixity forces π to biject dom_C(M(d)) onto dom_C(M'(d)); equal cardinality combined with D-SEQ at both input and output yields V_S(d') = V_S(d) for each content subspace S. S8 follows from S8-fin, S8a, S2, S8-depth, T5, TA5(c), TA7a via the derivation chain in ASN-0036; CL-OWN preserved by link-subspace fixity; link invariants preserved since L is unchanged. For K.λ: holds M, C, E, R in frame; S3★, S3★-aux preserved (M unchanged); link invariants verified (orphan link analysis in the Orphan links and coupling flexibility section); L3 is established for the new entry (K.λ requires `(F, G, Θ) ∈ Link`) and preserved for all existing entries (L12). For K.μ⁺_L: holds C, L, E, R in frame; S3★-aux preserved (new position has subspace s_L); per-subspace arrangement invariants verified in the Link-subspace extension section — S8a, S8-fin, S8-depth, D-CTG, D-MIN, D-SEQ, S8 all hold; S3★ satisfied by precondition (`ℓ ∈ dom(L)`); CL-OWN preserved (new mapping satisfies `origin(ℓ) = d` by precondition; existing link-subspace mappings unchanged by frame); L3 preserved (L unchanged).

**Class (b): Composite invariants** — may be violated at intermediate states within a composite, but hold at every valid composite boundary. These are: P4★ and P7a.

P4★ (`Contains_C(Σ) ⊆ R`): An elementary K.μ⁺ alone adds a content-subspace V-position mapping to address `a`, placing `(a, d) ∈ Contains_C(Σ')`. Its frame has `R' = R`, so if `(a, d) ∉ R`, P4★ is violated at the intermediate state. The coupling constraint J1★, evaluated at composite boundaries, guarantees restoration: for each `(a, d) ∈ Contains_C(Σ') \ Contains_C(Σ)`, some content-subspace V-position in M'(d) maps to `a` (by definition of Contains_C), and no content-subspace V-position in M(d) maps to `a` (since `(a, d) ∉ Contains_C(Σ)`), so J1★ requires `(a, d) ∈ R'`. This holds regardless of whether the V-position carrying `a` in M'(d) existed in dom(M(d)) with a different value — J1★'s range-based trigger detects new I-addresses in the content-subspace range, not new V-positions in the domain. Therefore `Contains_C(Σ') ⊆ R'` at the composite boundary. K.μ⁺_L does not affect P4★: it adds only link-subspace V-positions, which are excluded from Contains_C by definition. K.μ⁻ can only shrink Contains_C. K.μ~ preserves Contains_C exactly (analysis in the Content-scoped containment and provenance section). All other transitions hold M in frame.

P7a (`(A a ∈ dom(C) :: (E d :: (a, d) ∈ R))`): An elementary K.α alone adds `a` to `dom(C')` with `R' = R`, so `(a, d) ∉ R` for the newly allocated address — P7a is violated at the intermediate state. At composite boundaries, J0 guarantees every newly allocated content address is placed in some document's arrangement: `(E d, v :: M'(d)(v) = a)`. By the K.μ⁺ amendment, this V-position has `subspace(v) = s_C`. J1★ then requires `(a, d) ∈ R'`. Therefore P7a holds at the composite boundary. No other elementary transition removes addresses from dom(C) (by P0) or entries from R (by P2), so P7a, once established, is not broken by subsequent composites.

Coupling constraints J0, J1★, J1'★ hold for all valid composites by the analysis in the Scoped coupling constraints section. ∎


## Temporal decomposition

We have arrived at the structural insight underlying the entire design. The state Σ = (C, L, E, M, R) decomposes into three temporal layers, each answering a different question about the docuverse.

**The existential layer** (C, L, E) answers *what is*. Content, links, and entities, once created, exist permanently. Addresses are permanent (T8, ASN-0034). Content values are immutable (P0). Link values are immutable (L12). Entity membership is monotonic (P1). This layer only grows, and its entries are individually immutable once created. Gregory: "once text or a link-orgl is written at an ISA address, that binding is permanent."

**The historical layer** (R) answers *what has happened*. Provenance, once recorded, persists permanently. R records which documents have ever contained which content — a question about history, not current state. This layer only grows, though its entries may become stale: R may assert that document d once contained address a when d's current arrangement no longer references a.

**The presentational layer** (M) answers *what appears now*. Arrangements — the mapping from virtual positions to content identities — are freely mutable. Content can be added, removed, or rearranged. This is the sole locus of destructive change.

| Layer | Components | Mutability | Elementary transitions |
|-------|-----------|------------|----------------------|
| Existential | C, L, E | Append-only, values immutable | K.α, K.δ, K.λ |
| Historical | R | Append-only, entries may stale | K.ρ |
| Presentational | M | Fully mutable | K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~ (composite) |

(K.δ creates a new entity whose arrangement is initially empty. Since M is total with M(e) = ∅ for e ∉ E_doc, entity creation determines which empty arrangements become semantically meaningful — but it does not modify M.)

The invariants bind the layers together, making the temporal contracts precise. Within the existential layer: P6 ties C to E (every I-address's origin document exists as an entity); L1a is the link analog, tying L to E (every link address is scoped to an existing document); L14 constrains C and L to disjoint address subspaces. Bridging presentational to existential: S3★ bridges M to {C, L} — content-subspace V-positions reference dom(C), link-subspace V-positions reference dom(L); CL-OWN further constrains the link-subspace bridge (every document arranges only its own links). Bridging existential to historical: P7 ties R to C (every provenance entry references allocated content), and P7a ties C to R (every I-address has provenance — no content exists without a historical trail). And P4★ (Contains_C(Σ) ⊆ R, derived in the coupling section) bridges the presentational and historical layers — it is the load-bearing constraint that necessitates J1★'s coupling (by wp, K.μ⁺ alone cannot maintain P4★).

The two coupling constraints arise from different invariants through different mechanisms. P4★ directly necessitates J1★: the wp derivation shows K.μ⁺ in isolation fails to maintain Contains_C(Σ) ⊆ R, forcing K.ρ to co-occur. J0 is necessitated by P7a through a longer chain: P7a requires every I-address to have provenance; provenance is created by J1★ when content enters an arrangement; therefore freshly allocated content must enter some arrangement (J0) or P7a would fail for that address. S3★ is orthogonal to this — it constrains the M→{C, L} direction (arrangements reference allocated content or links), while J0 constrains the C→M direction (allocated content enters an arrangement). A system satisfying S3★ could permit orphan content: K.α extends dom(C), and if no K.μ⁺ follows, S3★ is trivially preserved because no new M entry was added.

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

| Label | Statement | Status |
|-------|-----------|--------|
| Σ.E | E ⊆ {t : ValidAddress(t) ∧ zeros(t) ≤ 2} — entity addresses, partitioned by IsNode / IsAccount / IsDocument | introduced |
| Σ.R | R ⊆ T_elem × E_doc — provenance relation recording historical content associations | introduced |
| Σ₀ | Initial state: C₀ = ∅, E₀ = {n₀} (bootstrap node), M₀(d) = ∅ for all d, R₀ = ∅ | introduced |
| parent(e) | For ¬IsNode(e): tumbler obtained by truncating last field and preceding separator | introduced |
| Contains(Σ) | {(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))} — current containment, derived quantity of state | introduced |
| Valid composite | Σ → Σ' valid iff: (1) elementary preconditions at each intermediate state, (2) J0/J1/J1' for the composite; P0/P1/P2 derived as lemma | introduced |
| Arrangement invariants lemma | Every valid composite preserves S2/S3/S8a/S8-depth/S8-fin/D-CTG/D-MIN — each elementary transition preserves these per-state properties; composition by transitivity | introduced |
| Reachable-state invariants | Every state reachable from Σ₀ satisfies P4, P6, P7, P7a, P8, S2–S8-fin, D-CTG, D-MIN — by induction: base at Σ₀, permanence lemma + arrangement invariants lemma + per-property derivations | introduced |
| P0 | Content store is append-only with immutable values: dom(C) ⊆ dom(C') ∧ C'(a) = C(a) for a ∈ dom(C) | introduced |
| P1 | Entity set is monotonically growing: E ⊆ E' for every transition, uniformly across levels | introduced |
| P8 | Entity hierarchy: (A e ∈ E : ¬IsNode(e) : parent(e) ∈ E) — no orphan accounts or documents | introduced |
| P2 | Provenance relation is monotonically growing: R ⊆ R' for every transition | introduced |
| P3 | Arrangements are the sole state component admitting destructive change (contraction, reordering) | introduced |
| P4 | Provenance bounds: Contains(Σ) ⊆ R, with stale entries possible from prior states | introduced |
| P4a | Historical fidelity: every (a, d) ∈ R has a witnessing state where a ∈ ran(M(d)) | introduced |
| P5 | Destruction confinement: C, E, R are all monotonic across every transition; only M can lose information | introduced |
| K.α | Content allocation — extend dom(C) with fresh IsElement(a) address and value | introduced |
| K.δ | Entity creation — extend E with fresh entity; precondition: parent(e) ∈ E when ¬IsNode(e); empty arrangement if IsDocument | introduced |
| K.μ⁺ | Arrangement extension — add V→I mappings to M(d), existing values preserved, referential integrity (S3), D-CTG/D-MIN postcondition | introduced |
| K.μ⁻ | Arrangement contraction — remove V→I mappings from M(d), surviving values preserved, D-CTG/D-MIN postcondition, no effect on C, E, R | introduced |
| K.μ~ | Arrangement reordering — distinguished composite (K.μ⁻ + K.μ⁺), bijection on V-positions preserving I-address multiset, D-CTG/D-MIN postcondition | introduced |
| K.ρ | Provenance recording — extend R with (a, d) pair where IsElement(a) ∧ a ∈ dom(C) | introduced |
| J0 | Content allocation (K.α) always co-occurs with arrangement extension (K.μ⁺) | introduced |
| J1 | Arrangement extension (K.μ⁺) must co-occur with provenance recording (K.ρ), derived by wp | introduced |
| J1' | (a, d) ∈ R' \ R only when a ∈ ran(M'(d)) \ ran(M(d)) — new provenance requires new containment | introduced |
| J2 | K.μ⁻ as elementary transition requires no coupling: C' = C ∧ E' = E ∧ R' = R | introduced |
| J3 | K.μ~ as distinguished composite requires no coupling: C' = C ∧ E' = E ∧ R' = R | introduced |
| J4 | Fork composite: K.δ + K.μ⁺ + K.ρ (no other steps); precondition M(d_src) ≠ ∅; dom(C') = dom(C) follows from frames; provenance from J1; empty source is ex nihilo (K.δ), not fork | introduced |
| P6 | Existential coherence: origin(a) ∈ E_doc for all a ∈ dom(C) | introduced |
| P7 | Provenance grounding: a ∈ dom(C) for all (a, d) ∈ R | introduced |
| P7a | Provenance coverage: (E d :: (a, d) ∈ R) for all a ∈ dom(C) — every I-address has provenance | introduced |
| SC-NEQ | `s_C ≠ s_L` — subspace identifiers are distinct | introduced |
| K.α amendment | Content-subspace restriction (`fields(a).E₁ = s_C`); preserves L0 clause 2 and L14 in the extended state | introduced |
| K.μ⁺ amendment | Content-subspace restriction (`subspace(v) = s_C`); existing D-CTG/D-MIN postconditions carry forward; partitions arrangement extension by subspace with K.μ⁺_L | introduced |
| K.μ⁻ amendment | D-CTG/D-MIN postconditions extend to two-subspace case; valid contractions per-subspace independently | introduced |
| K.λ | Elementary transition: L' = L ∪ {ℓ ↦ (F, G, Θ)}, frame C' = C, E' = E, M' = M, R' = R | introduced |
| K.μ⁺_L | Elementary transition: link-subspace arrangement extension, M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}, origin(ℓ) = d | introduced |
| S3★ | Subspace-conditional referential integrity: text → dom(C), link → dom(L); supersedes S3 | introduced |
| S3★-aux | Subspace exhaustiveness: `(A d, v : v ∈ dom(M(d)) : subspace(v) = s_C ∨ subspace(v) = s_L)` in every reachable state | introduced |
| Contains_C(Σ) | `{(a, d) : d ∈ E_doc ∧ (E v : v ∈ dom(M(d)) ∧ subspace(v) = s_C : M(d)(v) = a)}` — content-scoped containment | introduced |
| P4★ | `Contains_C(Σ) ⊆ R` — provenance bounds scoped to content subspace; supersedes P4 | introduced |
| J1★ | Range-based content-subspace scoping of J1: provenance recording for I-addresses new to content-subspace range | introduced |
| J1'★ | Range-based content-subspace scoping of J1': provenance entries only from content-subspace range changes | introduced |
| ValidComposite★ | Valid composite in extended state: transition preconditions at each step (K.μ~ as shorthand for K.μ⁻ + K.μ⁺) + J0, J1★, J1'★ at composite boundary; supersedes ValidComposite | introduced |
| P3★ | No component other than M — specifically C, L, E, R — admits contraction or reordering; supersedes P3 | introduced |
| P5★ | dom(C), dom(L), E, R can only grow; only M can lose information; supersedes P5 | introduced |
| CL-OWN | LinkSubspaceOwnership: `(A d, v : v ∈ dom(M(d)) ∧ subspace(v) = s_L : origin(M(d)(v)) = d)` — every document's link subspace contains only its own links | introduced |
| ExtendedReachableStateInvariants | Every reachable state satisfies S0 ∧ S1 ∧ S2 ∧ S3★ ∧ S3★-aux ∧ S8a ∧ S8-fin ∧ S8-depth ∧ S8 ∧ D-CTG ∧ D-MIN ∧ P0–P2 ∧ P3★ ∧ P4★ ∧ P5★ ∧ P6–P8 ∧ L0 ∧ L1 ∧ L1a ∧ L3 ∧ L12 ∧ L14 ∧ CL-OWN; supersedes ReachableStateInvariants | introduced |


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
