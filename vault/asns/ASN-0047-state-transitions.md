# ASN-0047: State Transitions

*2026-03-17*

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

Arrangements M(d) are defined iff d ∈ E_doc. We include links in E_doc: Nelson describes them as owned entities with internal structure ("a package of connecting or marking information... owned by a user... thereafter maintained by the back end"), and Gregory confirms link creation uses the same allocation mechanism as document creation. The structural distinction between documents and links — endset semantics, subspace layout — belongs to a separate analysis; here both participate identically in transitions.

Second, removal of content from an arrangement does not erase the historical fact of prior containment. Gregory: the reverse index "accumulates entries from every content addition but is never trimmed." Nelson: "every previous arrangement remains reconstructable." The system must answer "which documents have ever contained content with origin *a*?" — a question about history, not about current state.

**Definition (Provenance relation).** **Σ.R ⊆ T_elem × E_doc** — where T_elem = {a ∈ T : IsElement(a)} (ASN-0045). The pair (a, d) ∈ R records that document d has, at some point in the system's history, contained I-address a in its arrangement. This historical fidelity — that every entry reflects an actual past containment event, not merely eligibility — is not assumed by the definition alone; it is established as P4a below, by induction over J1', P2, and P0.

The full system state is:

> **Σ = (C, E, M, R)**

where C : T ⇀ Val and M : E_doc → (T ⇀ T) are as defined in ASN-0036.

**Definition (Initial state).** The initial state Σ₀ = (C₀, E₀, M₀, R₀) is:

- C₀ = ∅ (no content allocated)
- E₀ = {n₀} for a designated bootstrap node n₀ with IsNode(n₀)
- M₀ is the empty function — (E₀)_doc = ∅, so no arrangements exist
- R₀ = ∅ (no provenance recorded)

The bootstrap node seeds the entity hierarchy. Without at least one node, K.δ cannot create accounts (which require a parent node), and without accounts, no documents, and without documents, no content. The choice of n₀ is a system parameter, not a state transition. At Σ₀, (E₀)_doc = ∅, so the arrangement invariants S2, S3, S8a, S8-depth, and S8-fin hold vacuously — no arrangements exist.


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

*Frame:* C' = C; (A d ∈ E_doc : d ≠ e : M'(d) = M(d)); R' = R.

**K.μ⁺ (Arrangement extension).** New V→I mappings are added to some d ∈ E_doc, with existing mappings unchanged:

`dom(M'(d)) ⊃ dom(M(d)) ∧ (A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))`

Extension is pure addition — the domain grows, and no existing value is altered. Without the value-preservation clause, K.μ⁺ could silently replace values at existing positions, conflating extension with replacement. The decomposition of replacement into K.μ⁻ followed by K.μ⁺ depends on each being a pure operation.

*Precondition:* `d ∈ E_doc`; for every new mapping M'(d)(v) = a, `a ∈ dom(C)` (S3, ASN-0036 — since K.μ⁺'s frame holds C' = C, referential integrity reduces to membership in the pre-state content store); new V-positions satisfy S8a (all components strictly positive), and the resulting arrangement M'(d) satisfies S8-depth (uniform depth within each subspace); dom(M'(d)) is finite (S8-fin). Functionality (S2) is preserved: dom(M'(d)) ⊃ dom(M(d)) with value preservation at existing positions means new entries are assigned at positions outside dom(M(d)), so M'(d) remains a function — extending a partial function at disjoint domain elements cannot introduce ambiguity.

In a composite transition, K.α may precede K.μ⁺, extending dom(C) before K.μ⁺ executes. At that intermediate state the freshly allocated address is already in the content store, satisfying the precondition. From the composite perspective, the I-address in a new mapping falls into one of two cases:

(i) Freshly allocated — co-occurring K.α places a into dom(C) before K.μ⁺ maps to it. Nelson: "new content enters I-space permanently."

(ii) Previously existing — a ∈ dom(C) at the composite's initial state. This is transclusion: "the copy shares I-addresses with the source. No new content is created in I-space."

*Frame:* C' = C; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R.

**K.μ⁻ (Arrangement contraction).** Existing V→I mappings are removed from some d ∈ E_doc, with surviving mappings unchanged:

`dom(M'(d)) ⊂ dom(M(d)) ∧ (A v : v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v))`

*Precondition:* `d ∈ E_doc`.

Contraction trivially preserves the ASN-0036 arrangement invariants: M'(d) is a restriction of M(d), so functionality (S2), referential integrity of survivors (S3, since C' = C), V-position well-formedness (S8a), uniform depth within subspace (S8-depth), and finiteness (S8-fin) all carry over from the pre-state arrangement.

Contraction is pure removal — the domain shrinks, and no surviving value is altered. Without the value-preservation clause, K.μ⁻ could modify values at remaining positions, conflating contraction with rewriting.

Nelson: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." Contraction changes what a document displays; it does not change what exists.

*Frame:* C' = C; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d')).

**K.μ~ (Arrangement reordering).** V-positions may change without adding or removing mappings. For some d ∈ E_doc, there exists a bijection π : dom(M(d)) → dom(M'(d)) such that:

`(A v : v ∈ dom(M(d)) : M'(d)(π(v)) = M(d)(v))`

*Precondition:* `d ∈ E_doc`; π produces V-positions satisfying S8a (all components strictly positive), and the resulting arrangement M'(d) satisfies S8-depth (uniform depth within each subspace).

The bijection preserves the mapping pointwise — each V-position retains its I-address — so the multiset of referenced I-addresses is identical. As a corollary, ran(M'(d)) = ran(M(d)). This is a defining property of reordering, not a frame condition: it constrains how M(d) is modified, while frame conditions describe what is unchanged in other components. Nelson: content "changes V-space positions but touches nothing in I-space. The same bytes appear in a different order." Gregory confirms that reordering is the only transition kind that leaves all persistent structures outside the arrangement unchanged.

*Frame (derived below):* C' = C; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d')).

**K.ρ (Provenance recording).** A document-content association enters R:

`R' = R ∪ {(a, d)}` where `a ∈ dom(C) ∧ d ∈ E_doc`

*Precondition:* `a ∈ dom(C)` ∧ `d ∈ E_doc`. The level constraint IsElement(a) follows from S7b (every a ∈ dom(C) satisfies IsElement(a)).

*Frame:* C' = C; E' = E; (A d :: M'(d) = M(d)).

Five primitive kinds — K.α, K.δ, K.μ⁺, K.μ⁻, K.ρ — are complete. The argument is structural: the four-component state (C, E, M, R) admits exactly one growth mode for C (K.α), one for E (K.δ), one for R (K.ρ), and two independent mutation modes for M — entry addition (K.μ⁺) and entry removal (K.μ⁻). Any modification to a finite partial function decomposes into additions and removals; replacement — changing which I-address a V-position maps to — decomposes into K.μ⁻ followed by K.μ⁺.

K.μ~ is a distinguished composite, not a primitive transition. When dom(M(d)) is non-empty, it decomposes into K.μ⁻ (removing all mappings) followed by K.μ⁺ (re-adding them at new positions). We verify the intermediate-state preconditions and derive the frame.

Let Σ_int be the state after K.μ⁻ empties M(d). K.μ⁻'s frame gives C_int = C, E_int = E, R_int = R, and M_int(d') = M(d') for d' ≠ d. The K.μ⁺ step re-adds mappings at the new V-positions π(v), and its preconditions at Σ_int are: (i) d ∈ (E_int)_doc — holds because E_int = E and d ∈ E_doc; (ii) referential integrity (S3) — every re-added I-address a satisfies a ∈ ran(M(d)) ⊆ dom(C) = dom(C_int), where the inclusion follows from S3 at the pre-state and the equality from K.μ⁻'s frame; (iii) S8a and S8-depth — the new V-positions satisfy these by K.μ~'s precondition on π; (iv) S8-fin — dom(M'(d)) is finite because π is a bijection from the finite dom(M(d)) (S8-fin at the pre-state). Functionality (S2) of the result M'(d) follows from the injectivity of π: each target position π(v) receives exactly one value M(d)(v), and since π is a bijection, no two source positions map to the same target.

The frame follows by composition. K.μ⁻ gives C_int = C, E_int = E, R_int = R, and preserves other arrangements. K.μ⁺ gives C' = C_int = C, E' = E_int = E, R' = R_int = R, and preserves other arrangements. Composing: C' = C, E' = E, R' = R, (A d' : d' ≠ d : M'(d') = M(d')) — matching the frame stated above.

When dom(M(d)) = ∅, K.μ~ is the identity — the empty bijection π : ∅ → ∅ satisfies the definition, producing zero elementary steps. When dom(M(d)) is non-empty, π = id is also permitted — the identity bijection produces M'(d) = M(d), a degenerate reordering that changes nothing. The decomposition into K.μ⁻ + K.μ⁺ is a vacuous round-trip, and all invariants are trivially preserved. We do not restrict π to non-identity bijections; the formal definition subsumes both degenerate cases cleanly. The coupling constraint J1 is vacuously satisfied at the composite level: since K.μ~ preserves ran(M(d)), the set difference ran(M'(d)) \ ran(M(d)) is empty — no new containment pairs arise, so no provenance recording is needed. We retain K.μ~ as a named transition because its isolation property (J3) and semantic clarity — reordering as a single atomic concept — justify separate treatment. Gregory's independent analysis of the implementation identifies the same six persistent modification kinds, confirming this classification.

We also observe that neither split nor merge appears as an elementary transition. Nelson addresses this explicitly: the effect of splitting a document is achieved by creating two new documents and transcluding different portions of the original into each. Merging is creating a new document and transcluding from multiple sources. Both compose from K.δ, K.μ⁺, and K.ρ — the elementary transitions suffice.

**Lemma (Arrangement invariants from elementary preservation).** Every valid composite transition preserves S2, S3, S8a, S8-depth, and S8-fin. Each elementary transition preserves these per-state properties: K.μ⁺ establishes them via its preconditions (disjoint extension for S2, referential integrity for S3, explicit S8a/S8-depth/S8-fin requirements); K.μ⁻ preserves them by restriction of M(d); K.δ for documents produces the empty arrangement (vacuously satisfying all five); all other transitions hold M in frame. Since each step of a valid composite preserves these per-state properties, they hold at every intermediate and final state.


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

**Theorem (Reachable-state invariants).** Every state reachable from Σ₀ by a finite sequence of valid composite transitions satisfies P4 (Contains(Σ) ⊆ R), P6, P7, P8, S2, S3, S8a, S8-depth, and S8-fin.

*Base case.* At Σ₀: dom(C₀) = ∅ makes P6 vacuous (no content, so no origin to check); R₀ = ∅ makes P7 vacuous (no provenance entries to ground); (E₀)_doc = ∅ makes P4 vacuous (no documents, so Contains(Σ₀) = ∅ ⊆ R₀); E₀ = {n₀} with IsNode(n₀) makes P8 vacuous (no non-node entities); (E₀)_doc = ∅ makes S2–S8-fin vacuous (no arrangements exist).

*Inductive step.* For any reachable state Σ satisfying the above, every valid composite Σ → Σ' produces Σ' satisfying the same — P0/P1/P2 by the permanence lemma; S2/S3/S8a/S8-depth/S8-fin by the arrangement invariants lemma; P8 as derived above; P4, P6, and P7 as derived below.

Intermediate states need not satisfy all system invariants; only the final state is required to. The ordering matters: J0 couples K.α with K.μ⁺, and S3 requires the I-address to exist before the V→I mapping is created, so K.α precedes K.μ⁺. Similarly, J4's fork compounds K.δ + K.μ⁺ + K.ρ, and K.μ⁺ requires d ∈ E_doc, which K.δ establishes — so K.δ precedes K.μ⁺. The net effect of a composite transition is the composition of its elementary effects.

A convention on freshly created documents. When a composite transition creates a new document d via K.δ, the pre-state has no arrangement for d (since d ∉ E_doc). To state the coupling constraints uniformly, we adopt M(d) = ∅ for d ∈ E'_doc \ E_doc — documents that do not yet exist in the pre-state have an empty arrangement. Under this convention, ran(M(d)) = ∅ for freshly created documents, so the set difference ran(M'(d)) \ ran(M(d)) reduces to ran(M'(d)): all content placed in a new document counts as newly introduced. The coupling constraints below quantify over E'_doc, not E_doc, making them applicable to freshly created documents without special cases.

**J0 (Allocation requires placement).** Content allocation K.α always co-occurs with arrangement extension K.μ⁺:

`(A Σ → Σ', a : a ∈ dom(C') \ dom(C) : (E d, v : d ∈ E'_doc ∧ v ∈ dom(M'(d)) : M'(d)(v) = a))`

Every freshly allocated I-address appears in some arrangement in the post-state — the containing document may itself have been freshly created by K.δ in the same composite transition. This is an axiom of the state transition model, not a theorem of ASN-0036. S7a tells us that the prefix of a identifies the creating document, but it does not tell us that the creating document's arrangement must contain a — an address could be allocated into dom(C) with the correct prefix while appearing in no arrangement. The justification for J0 is design intent: in Nelson's model, content enters the docuverse by being placed in a document. There is no mechanism for creating "orphan" content that exists in I-space without any document displaying it. Gregory confirms: allocation always occurs in the context of a document operation that inserts the new content.

**J1 (Extension records provenance).** Arrangement extension K.μ⁺ must co-occur with provenance recording K.ρ:

`(A Σ → Σ', d ∈ E'_doc, a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R')`

We derive this by wp. The invariant we need — Contains(Σ) ⊆ R — must hold after the composite transition. After K.μ⁺, Contains(Σ') ⊇ Contains(Σ), so new pairs appear. K.μ⁺ alone does not modify R (its frame holds R' = R). Computing the wp of K.μ⁺ alone, substituting R for R':

`wp(K.μ⁺, Contains(Σ') ⊆ R) = (A a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R)`

This requires every new containment pair to already be in R — not generally true for fresh content. K.μ⁺ in isolation cannot maintain the invariant; K.ρ must co-occur, extending R so that the composite post-state satisfies `(A a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R')`.

Gregory identifies one implementation anomaly where provenance recording is skipped for a particular command, "making content invisible to find_documents." The abstract specification treats this as a defect: the coupling is required.

For a freshly created document d ∈ E'_doc \ E_doc, the convention M(d) = ∅ gives ran(M(d)) = ∅, so ran(M'(d)) \ ran(M(d)) = ran(M'(d)): every I-address placed in a new document triggers provenance recording.

**J1' (Provenance requires extension).** Conversely, provenance recording K.ρ for (a, d) occurs only within a composite transition where K.μ⁺ introduces a into ran(M'(d)):

`(A Σ → Σ', a, d ∈ E'_doc : (a, d) ∈ R' \ R : a ∈ ran(M'(d)) \ ran(M(d)))`

J1 ensures every new containment pair is recorded; J1' ensures every new provenance entry corresponds to an actual containment event. Together they characterise new provenance entries: (a, d) ∈ R' \ R if and only if K.μ⁺ introduces a into ran(M'(d)) and (a, d) ∉ R. When (a, d) ∈ R already — from a prior insertion-deletion cycle — K.μ⁺ re-introducing a into d's arrangement requires no new K.ρ, because J1's requirement (a, d) ∈ R' is satisfied by existing membership (P2 ensures prior entries persist). The convention M(d) = ∅ for d ∈ E'_doc \ E_doc ensures J1' is well-defined for freshly created documents: ran(M'(d)) \ ran(M(d)) = ran(M'(d)). Gregory confirms this tight coupling — the provenance structure "accumulates entries from every content addition" and no mechanism exists to record provenance outside of content placement.

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

(i) *Pre-existing containment:* a ∈ ran(M(d)) — using the convention M(d) = ∅ for d ∈ E'_doc \ E_doc. Then (a, d) ∈ Contains(Σ) ⊆ R (inductive hypothesis), and P2 gives R ⊆ R', so (a, d) ∈ R'.

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


## Destruction confinement

We now state the central structural theorem — a generalisation of S9 (ASN-0036) from two components to four.

**P5 (Destruction confinement).** For every state transition Σ → Σ':

(a) `dom(C') ⊇ dom(C) ∧ (A a : a ∈ dom(C) : C'(a) = C(a))`

(b) `E' ⊇ E`

(c) `R' ⊇ R`

The only component that can lose information is M.

*Proof.* By case analysis on the five elementary transitions. K.α extends dom(C) preserving existing entries, with E and R in its frame. K.δ extends E, with C and R in its frame. K.μ⁺ and K.μ⁻ have C, E, and R in their frames. K.ρ extends R, with C and E in its frame. Each preserves (a) through (c). The distinguished composite K.μ~ decomposes into K.μ⁻ followed by K.μ⁺, both of which preserve (a)–(c), so K.μ~ does as well. General composite transitions, being finite sequences of elementary ones, preserve (a)–(c) by transitivity of ⊇ and ∧. ∎

P5 makes the confinement vivid. Every destructive state change — every removal, every reordering — is confined to the presentational layer. The permanent record (what content exists, which entities have been created, what provenance has been recorded) can only grow.


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
- *J1:* ran(M₂(d₂)) \ ran(M₁(d₂)) = {a₁, a₂} \ ∅ = {a₁, a₂} (convention: M₁(d₂) = ∅). Both (a₁, d₂) and (a₂, d₂) are in R₂. ✓
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

**Delete a₁ from d₂'s arrangement (K.μ⁻).** Remove the mapping at V-position [1,1].

*K.μ⁻:* dom(M₄(d₂)) = {[1,2], [1,3]} ⊂ dom(M₃(d₂)) = {[1,1], [1,2], [1,3]}. The surviving mappings are unchanged: M₄(d₂)([1,2]) = a₂, M₄(d₂)([1,3]) = a₃.

Verification:

- *J2:* C₄ = C₃; E₄ = E₃; R₄ = R₃. All permanent and historical state unchanged. ✓
- *P4:* Contains(Σ₄) = {(a₁, d₁), (a₂, d₁), (a₂, d₂), (a₃, d₂)}. The pair (a₁, d₂) is no longer in Contains — d₂ no longer displays a₁. Yet (a₁, d₂) ∈ R₄: the stale entry persists. Contains(Σ₄) ⊂ Contains(Σ₃), while R₄ = R₃. ✓
- *P5:* C₄ = C₃; E₄ = E₃; R₄ = R₃. Only M changed. ✓

The divergence is now concrete: R₄ records that d₂ once contained a₁, while the current arrangement does not. This is the historical memory that J2 preserves — deletion is purely presentational.

**Reorder d₂'s arrangement (K.μ~).** Swap V-positions [1,2] and [1,3].

*K.μ~:* The bijection π : {[1,2], [1,3]} → {[1,2], [1,3]} with π([1,2]) = [1,3] and π([1,3]) = [1,2]. The definition requires M₅(d₂)(π(v)) = M₄(d₂)(v) for all v ∈ dom(M₄(d₂)), giving M₅(d₂) = {[1,2] ↦ a₃, [1,3] ↦ a₂}. Both target V-positions satisfy S8a (all components strictly positive) and S8-depth (uniform depth 2, shared first component 1).

Verification:

- *J3:* C₅ = C₄; E₅ = E₄; R₅ = R₄. All permanent and historical state unchanged. ✓
- *ran preservation:* ran(M₅(d₂)) = {a₂, a₃} = ran(M₄(d₂)). The multiset of referenced I-addresses is identical; only V-positions changed. ✓
- *P4:* Contains(Σ₅) = Contains(Σ₄) ⊆ R₄ = R₅. Since ran is preserved for d₂ and no other arrangement changed, the current containment set is unchanged. ✓
- *P5:* C₅ = C₄; E₅ = E₄; R₅ = R₄. Only M changed. ✓

Reordering is the simplest transition to verify: it touches nothing beyond the V-position mapping, and all invariants hold by the frame conditions alone.

The four steps exercise J0, J1, J2, J3, J4, P4, P5, P6, P7, and P8, and demonstrate the convention M(d) = ∅ for freshly created documents (J1 verification of the fork), the divergence between current containment and historical provenance (J2 verification of the deletion), and the presentational isolation of reordering (J3 verification of the swap).


## Temporal decomposition

We have arrived at the structural insight underlying the entire design. The state Σ = (C, E, M, R) decomposes into three temporal layers, each answering a different question about the docuverse.

**The existential layer** (C, E) answers *what is*. Content and entities, once created, exist permanently. Addresses are permanent (T8, ASN-0034). Content values are immutable (P0). Entity membership is monotonic (P1). This layer only grows, and its entries are individually immutable once created. Gregory: "once text or a link-orgl is written at an ISA address, that binding is permanent."

**The historical layer** (R) answers *what has happened*. Provenance, once recorded, persists permanently. R records which documents have ever contained which content — a question about history, not current state. This layer only grows, though its entries may become stale: R may assert that document d once contained address a when d's current arrangement no longer references a.

**The presentational layer** (M) answers *what appears now*. Arrangements — the mapping from virtual positions to content identities — are freely mutable. Content can be added, removed, or rearranged. This is the sole locus of destructive change.

| Layer | Components | Mutability | Elementary transitions |
|-------|-----------|------------|----------------------|
| Existential | C, E | Append-only, values immutable | K.α, K.δ |
| Historical | R | Append-only, entries may stale | K.ρ |
| Presentational | M | Fully mutable | K.μ⁺, K.μ⁻, K.μ~ (composite), K.δ† |

†K.δ for documents also initialises M'(e) = ∅, extending M's domain — a presentational-layer effect. We classify K.δ as primarily existential because its defining purpose is entity creation; the empty arrangement initialisation is a structural consequence (extending the domain with an empty entry, not mutating an existing arrangement). The broader claim holds: no elementary transition touches all three layers.

Three invariants bind the layers together, making the temporal contracts precise. P6 is intra-existential — a coherence constraint between C and E, both within the same layer. P7 bridges the existential and historical layers, tying R to C. And P4 (Contains(Σ) ⊆ R, derived in the coupling section) bridges the presentational and historical layers — it is the load-bearing constraint that necessitates J1's coupling.

**P6 (Existential coherence).** For every I-address in the content store, its origin document exists as an entity:

`(A a ∈ dom(C) :: origin(a) ∈ E_doc)`

*Derivation.* K.α allocates a under origin(a)'s prefix (S7a, ASN-0036), and requires origin(a) ∈ E_doc as a precondition — the allocation mechanism inc(·, k) operates on an existing tumbler within the ownership domain. P1 preserves entity membership across subsequent transitions; P0 preserves a ∈ dom(C). Initial state: dom(C₀) = ∅, so the quantifier is vacuously satisfied. Inductive step: each K.α has origin(a) ∈ E_doc by precondition; P0 preserves a; P1 preserves origin(a). ∎

**P7 (Provenance grounding).** Every provenance entry references allocated content:

`(A (a, d) ∈ R :: a ∈ dom(C))`

*Derivation.* K.ρ requires a ∈ dom(C) as a precondition. P0 preserves dom(C). By induction: initially R₀ = ∅ (vacuous). Each K.ρ adds (a, d) with a ∈ dom(C); P0 ensures a remains in dom(C') for all subsequent states; P2 ensures (a, d) remains in R'. ∎

The decomposition constrains the elementary transitions cleanly. No *elementary* transition modifies all three layers simultaneously — each touches at most two (K.δ for documents touches the existential and presentational layers; all others touch exactly one). Composite transitions routinely span all three: insertion compounds K.α (existential) + K.μ⁺ (presentational) + K.ρ (historical). The point is that each elementary step has bounded scope. The purely destructive transitions — K.μ⁻ and K.μ~ — are confined to the presentational layer alone, the one layer where impermanence is by design. Cross-layer coupling occurs only in constructive directions: K.α (existential) couples with K.μ⁺ (presentational) via J0; K.μ⁺ (presentational) couples with K.ρ (historical) via J1/J1'. The existential and historical layers never shrink.

The existential and historical layers differ in semantics despite sharing the append-only contract. Existential entries state *current facts*: content value v exists at address a, and this remains true permanently. Historical entries state *past events*: document d once contained address a, and this record persists even when the current arrangement no longer agrees. The distinction matters because existential entries are both permanent and accurate (content *is* at address a), while historical entries are permanent but may be stale (document d *was* associated with address a, but may no longer be).

Nelson captures the whole architecture in a sentence: "The braid only grows more complex. It never unravels." The existential and historical layers are the braid. The presentational layer is the current view of it.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| Σ.E | E ⊆ {t : ValidAddress(t) ∧ zeros(t) ≤ 2} — entity addresses, partitioned by IsNode / IsAccount / IsDocument | introduced |
| Σ.R | R ⊆ T_elem × E_doc — provenance relation recording historical content associations | introduced |
| Σ₀ | Initial state: C₀ = ∅, E₀ = {n₀} (bootstrap node), M₀ empty, R₀ = ∅ | introduced |
| parent(e) | For ¬IsNode(e): tumbler obtained by truncating last field and preceding separator | introduced |
| Contains(Σ) | {(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))} — current containment, derived quantity of state | introduced |
| Valid composite | Σ → Σ' valid iff: (1) elementary preconditions at each intermediate state, (2) J0/J1/J1' for the composite; P0/P1/P2 derived as lemma | introduced |
| Arrangement invariants lemma | Every valid composite preserves S2/S3/S8a/S8-depth/S8-fin — each elementary transition preserves these per-state properties; composition by transitivity | introduced |
| Reachable-state invariants | Every state reachable from Σ₀ satisfies P4, P6, P7, P8, S2–S8-fin — by induction: base at Σ₀, permanence lemma + arrangement invariants lemma + per-property derivations | introduced |
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
| K.μ⁺ | Arrangement extension — add V→I mappings to M(d), existing values preserved, referential integrity required (S3) | introduced |
| K.μ⁻ | Arrangement contraction — remove V→I mappings from M(d), surviving values preserved, no effect on C, E, R | introduced |
| K.μ~ | Arrangement reordering — distinguished composite (K.μ⁻ + K.μ⁺), bijection on V-positions preserving I-address multiset | introduced |
| K.ρ | Provenance recording — extend R with (a, d) pair where IsElement(a) ∧ a ∈ dom(C) | introduced |
| J0 | Content allocation (K.α) always co-occurs with arrangement extension (K.μ⁺) | introduced |
| J1 | Arrangement extension (K.μ⁺) must co-occur with provenance recording (K.ρ), derived by wp | introduced |
| J1' | (a, d) ∈ R' \ R only when a ∈ ran(M'(d)) \ ran(M(d)) — new provenance requires new containment | introduced |
| J2 | K.μ⁻ as elementary transition requires no coupling: C' = C ∧ E' = E ∧ R' = R | introduced |
| J3 | K.μ~ as distinguished composite requires no coupling: C' = C ∧ E' = E ∧ R' = R | introduced |
| J4 | Fork composite: K.δ + K.μ⁺ + K.ρ (no other steps); precondition M(d_src) ≠ ∅; dom(C') = dom(C) follows from frames; provenance from J1; empty source is ex nihilo (K.δ), not fork | introduced |
| P6 | Existential coherence: origin(a) ∈ E_doc for all a ∈ dom(C) | introduced |
| P7 | Provenance grounding: a ∈ dom(C) for all (a, d) ∈ R | introduced |


## Open Questions

- What invariants must a forked document's initial arrangement satisfy with respect to its source's current arrangement — must it be identical, or may it be a proper subset?
- Must arrangement reordering respect subspace boundaries within a document (text content at element subspace ≥ 1, link references at subspace 0)?
- What guarantees must the system provide about provenance when content is transitively shared through chains of transclusion?
- Can arrangement contraction on one document affect the discoverability of links attached to the same I-addresses from another document?
- What relationship must hold between a document's version lineage and its sequence of arrangement transitions?
- What additional permanence properties must the provenance relation satisfy for content that participates in link endsets?
