# ASN-0046: State Transitions

*2026-03-17*

ASN-0036 established two components of system state — a permanent content store C and mutable document arrangements M(d) — and proved their separation: content, once stored, is immutable (S0); arrangement mutations cannot alter the content store (S9). These are properties of the invariants. We have not yet classified the transitions. In what primitive ways can the state change, and what must each change preserve?

The consultation answers reveal a state model richer than the two-space analysis captured. Nelson enumerates the ways the docuverse changes — new documents created, new content inserted, new links established, views rearranged, documents published — and is equally precise about what cannot happen: content is never destroyed, addresses are never reassigned, history is never erased. Gregory reduces eight protocol commands to six kinds of persistent modification, distributed across three storage layers with distinct permanence contracts.

We seek the abstract taxonomy. Not the protocol commands, which are interface design, but the primitive modifications and their invariants. The central result is a *mutability hierarchy*: the state components arrange into three temporal layers, each with its own permanence contract. Destructive change — removal and reordering — is confined entirely to the most mutable layer.


## The state model

ASN-0036 gave us C and M(d). Three phenomena require additional state components.

First, entities come into existence. Nelson describes exactly two document creation modes: ex nihilo (a fresh empty document) and forking (a new document derived from an existing one). Gregory confirms both use the same allocation mechanism, differing only in whether the new arrangement starts empty or populated. We need an explicit record of which entities exist.

**Definition (Entity set).** **Σ.E ⊆ T** — the set of allocated entity addresses. Every e ∈ E satisfies ValidAddress(e) (T4, ASN-0034). The level predicates of ASN-0045 partition E into three strata:

- E_node = {e ∈ E : IsNode(e)} — server nodes
- E_account = {e ∈ E : IsAccount(e)} — user accounts
- E_doc = {e ∈ E : IsDocument(e)} — documents and links

Arrangements M(d) are defined iff d ∈ E_doc. We include links in E_doc: Nelson describes them as owned entities with internal structure ("a package of connecting or marking information... owned by a user... thereafter maintained by the back end"), and Gregory confirms link creation uses the same allocation mechanism as document creation. The structural distinction between documents and links — endset semantics, subspace layout — belongs to a separate analysis; here both participate identically in transitions.

Second, removal of content from an arrangement does not erase the historical fact of prior containment. Gregory: the reverse index "accumulates entries from every content addition but is never trimmed." Nelson: "every previous arrangement remains reconstructable." The system must answer "which documents have ever contained content with origin *a*?" — a question about history, not about current state.

**Definition (Provenance relation).** **Σ.R ⊆ T_elem × E_doc** — where T_elem = {a ∈ T : IsElement(a)} (ASN-0045). The pair (a, d) ∈ R records that document d has, at some point in the system's history, contained I-address a in its arrangement.

Third, Nelson describes a state transition orthogonal to content: publication. "A document may be private or published... Once published, a document creates permanent obligations... its author may not withdraw it except by lengthy due process."

**Definition (Publication state).** **Σ.pub : E_doc → {private, published}**

The full system state is:

> **Σ = (C, E, M, R, pub)**

where C : T ⇀ Val and M : E_doc → (T ⇀ T) are as defined in ASN-0036.


## Permanence

We classify each component by the transitions it admits. Five components, three distinct permanence contracts.

**P0 (Content permanence).** The content store admits only extensions, and existing entries are immutable:

`(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ (A a : a ∈ dom(C) : C'(a) = C(a)))`

This is S0 of ASN-0036, restated for the full state model. C is *append-only with immutable values*. Nelson: "Instead, suppose we create an append-only storage system." Gregory confirms: no `deletegr()`, no `updategr()`, no "replace at address X" operation exists.

**P1 (Entity permanence).** The entity set admits only extensions:

`(A Σ → Σ' :: E ⊆ E')`

No transition removes an entity. This specialises T8 (AllocationPermanence, ASN-0034) to the entity set. P1 holds uniformly across levels:

`[e ∈ E ∧ IsNode(e) ⟹ e ∈ E']`
`[e ∈ E ∧ IsAccount(e) ⟹ e ∈ E']`
`[e ∈ E ∧ IsDocument(e) ⟹ e ∈ E']`

Nelson: "New items may be continually inserted in tumbler-space while the other addresses remain valid." The address space is a growing tree; entities are born but never die.

**P2 (Provenance permanence).** The provenance relation admits only extensions:

`(A Σ → Σ' :: R ⊆ R')`

Once the system records that d referenced a, that record persists. Gregory: the provenance structure is "a permanently-growing reverse index that accumulates entries from every content addition but is never trimmed."

**P3 (Publication irreversibility).** Publication is a one-way transition:

`(A Σ → Σ', d : d ∈ E_doc ∧ pub(d) = published : pub'(d) = published)`

Nelson: "It is in the common interest that a thing once published stay published, as in the world of paper."

**P4 (Arrangement as sole locus of destructive change).** Arrangements admit three modes of change:

(a) *Extension*: new V→I mappings may be added to M(d).

(b) *Contraction*: existing V→I mappings may be removed from M(d).

(c) *Reordering*: V-positions of existing mappings may change while the multiset of referenced I-addresses is preserved.

No other component admits contraction or reordering. Gregory states this explicitly: the arrangement layer is "the sole locus of destructive mutation." P0–P3 make this formal: C, E, R, and pub are all monotonic; only M can shrink.


## Elementary transitions

We seek the elementary modifications — the minimal state changes from which all system operations compose. Each is defined by its effect and its frame: what changes and what does not.

**K.α (Content allocation).** A fresh I-address is bound to a value in the content store:

`C' = C ∪ {a ↦ v}` where `a ∉ dom(C)`

The address a satisfies IsElement(a) (S7b, ASN-0036) and is allocated under the creating document's prefix (S7a). By GlobalUniqueness (ASN-0034), a is distinct from every previously allocated address.

*Frame:* E' = E; (A d :: M'(d) = M(d)); R' = R; pub' = pub.

**K.δ (Entity creation).** A fresh entity address enters E with initial state:

`E' = E ∪ {e}` where `e ∉ E`

When IsDocument(e): M'(e) = ∅ (empty arrangement) and pub'(e) = private. The address is allocated via inc(·, k) (TA5, ASN-0034) under the parent's prefix. Gregory confirms that document creation and node creation use the same mechanism, differing only in the allocation hint.

Nelson identifies two document-creation modes — ex nihilo and forking. At the elementary level, both begin with K.δ producing an empty document. Forking is compound: K.δ followed by arrangement extension and provenance recording (J4 below).

*Frame:* C' = C; (A d ∈ E_doc : d ≠ e : M'(d) = M(d)); R' = R; pub unchanged for existing entities.

**K.μ⁺ (Arrangement extension).** New V→I mappings are added to some d ∈ E_doc:

`dom(M'(d)) ⊃ dom(M(d))`

For every new mapping M'(d)(v) = a, referential integrity requires a ∈ dom(C') (S3, ASN-0036). Two cases arise:

(i) a ∈ dom(C') \ dom(C) — freshly allocated, co-occurring with K.α. Nelson: "new content enters I-space permanently."

(ii) a ∈ dom(C) — existing content. This is transclusion: "the copy shares I-addresses with the source. No new content is created in I-space."

*Frame:* E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R; pub' = pub.

**K.μ⁻ (Arrangement contraction).** Existing V→I mappings are removed from some d ∈ E_doc:

`dom(M'(d)) ⊂ dom(M(d))`

Nelson: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." Contraction changes what a document displays; it does not change what exists.

*Frame:* C' = C; E' = E; R' = R; pub' = pub; (A d' : d' ≠ d : M'(d') = M(d')).

**K.μ~ (Arrangement reordering).** V-positions change without adding or removing mappings. For some d ∈ E_doc, there exists a bijection π : dom(M(d)) → dom(M'(d)) such that:

`(A v : v ∈ dom(M(d)) : M'(d)(π(v)) = M(d)(v))`

The multiset of referenced I-addresses is preserved; only V-positions change. Nelson: content "changes V-space positions but touches nothing in I-space. The same bytes appear in a different order." Gregory confirms that reordering is the only transition kind that leaves all persistent structures outside the arrangement unchanged.

*Frame:* C' = C; E' = E; R' = R; pub' = pub; ran(M'(d)) = ran(M(d)); (A d' : d' ≠ d : M'(d') = M(d')).

**K.ρ (Provenance recording).** A document-content association enters R:

`R' = R ∪ {(a, d)}` where `a ∈ dom(C) ∧ d ∈ E_doc`

The requirement a ∈ dom(C) ensures only associations with allocated content are recorded. The level constraint IsElement(a) follows from S7b (every a ∈ dom(C) satisfies IsElement(a)).

*Frame:* C' = C; E' = E; (A d :: M'(d) = M(d)); pub' = pub.

**K.π (Publication).** A document transitions from private to published:

`pub'(d) = published` where `pub(d) = private` and `d ∈ E_doc`

*Frame:* C' = C; E' = E; (A d :: M'(d) = M(d)); R' = R.

These seven kinds — α, δ, μ⁺, μ⁻, μ~, ρ, π — are complete. Gregory's independent analysis of the implementation identifies six persistent modification kinds (corresponding to our α, δ, μ⁺, μ⁻, μ~, ρ); we add π from Nelson's description of publication as a distinct state transition. No other kind of modification appears in either the design literature or the implementation.

We also observe that neither split nor merge appears as an elementary transition. Nelson addresses this explicitly: the effect of splitting a document is achieved by creating two new documents and transcluding different portions of the original into each. Merging is creating a new document and transcluding from multiple sources. Both compose from K.δ, K.μ⁺, and K.ρ — the elementary transitions suffice.


## Coupling and isolation

The elementary transitions do not all occur independently. Some must co-occur to maintain invariants (coupling); some must leave other components unchanged (isolation). The weakest-precondition calculus makes the coupling constraints visible.

**J0 (Allocation requires placement).** Content allocation K.α always co-occurs with arrangement extension K.μ⁺:

`(A Σ → Σ', a : a ∈ dom(C') \ dom(C) : (E d, v : d ∈ E_doc ∧ v ∈ dom(M'(d)) : M'(d)(v) = a))`

Every freshly allocated I-address appears in some arrangement. This follows from S7a (ASN-0036): the address a bears the creating document's prefix, identifying a document d₀ ∈ E_doc whose arrangement must contain the new content.

**J1 (Extension records provenance).** Arrangement extension K.μ⁺ should co-occur with provenance recording K.ρ:

`(A Σ → Σ', d, a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R')`

We derive this by wp. Define the *current containment*:

`Contains(Σ) = {(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))}`

The invariant we need — Contains(Σ) ⊆ R — must hold after extension. After K.μ⁺, Contains(Σ') ⊇ Contains(Σ), so new pairs appear. K.μ⁺ alone does not modify R (its frame holds R' = R). Hence:

`wp(K.μ⁺, Contains(Σ') ⊆ R') = (A a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R')`

This requires K.ρ to co-occur, adding the new pairs to R.

Gregory identifies one implementation anomaly where provenance recording is skipped for a particular command, "making content invisible to find_documents." The abstract specification treats this as a defect: the coupling is required.

**J2 (Contraction isolation).** Arrangement contraction K.μ⁻ is isolated from all permanent and historical state:

`(A Σ → Σ', d : dom(M'(d)) ⊂ dom(M(d)) : C' = C ∧ E' = E ∧ R' = R ∧ pub' = pub)`

That this isolation is correct follows by wp. For P0: K.μ⁻ does not touch C. For P1: does not touch E. For P2: does not touch R. For P3: does not touch pub. For the provenance bound Contains(Σ) ⊆ R: contraction can only remove pairs from Contains, so Contains(Σ') ⊆ Contains(Σ) ⊆ R = R'. No coupling needed.

This is the deepest consequence of the design. Deletion is purely presentational — it changes what appears, not what exists or what has been. Gregory confirms: contraction "never triggers" provenance recording, and the provenance structure "is never pruned."

**J3 (Reordering isolation).** Arrangement reordering K.μ~ is isolated identically:

`C' = C ∧ E' = E ∧ R' = R ∧ pub' = pub`

Reordering preserves ran(M(d)), so Contains(Σ') = Contains(Σ). All invariants are trivially maintained.

**J4 (Fork is compound).** Nelson's forking creation mode composes K.δ + K.μ⁺ + K.ρ:

`(A Σ → Σ', d_new, d_src : d_new ∈ E'_doc \ E_doc ∧ ran(M'(d_new)) ⊆ ran(M(d_src)) :`
`  (A a : a ∈ ran(M'(d_new)) : (a, d_new) ∈ R'))`

The new document d_new is created empty (K.δ), its arrangement extended with mappings to the source's I-addresses (K.μ⁺), and the new associations recorded (K.ρ). The content store C is unchanged — forking shares existing I-addresses, creating no new content. Nelson: "the new document's id will indicate its ancestry."

An immediate consequence of J1 and J2 is that the provenance relation diverges from current containment over time.

**P5 (Provenance bounds).** In any reachable state where J1 has been satisfied for all prior transitions:

`Contains(Σ) ⊆ R`

Every I-address currently in some arrangement is recorded in R. But the converse does not hold: (a, d) ∈ R does not imply a ∈ ran(M(d)). Stale entries persist from earlier states where d contained a before contraction removed it. These entries are not errors — they are the system's historical memory of content associations, monotonically truthful, never retracting a claim once made. Gregory: "find_documents returns historically accurate results, not current state."


## Destruction confinement

We now state the central structural theorem — a generalisation of S9 (ASN-0036) from two components to five.

**P6 (Destruction confinement).** For every state transition Σ → Σ':

(a) `dom(C') ⊇ dom(C) ∧ (A a : a ∈ dom(C) : C'(a) = C(a))`

(b) `E' ⊇ E`

(c) `R' ⊇ R`

(d) `(A d : d ∈ E_doc ∧ pub(d) = published : pub'(d) = published)`

The only component that can lose information is M.

*Proof.* By case analysis on K.α–K.π. Each elementary transition preserves (a) through (d): K.α extends dom(C) preserving existing entries, with E, R, pub in its frame. K.δ extends E, with C, R, pub in its frame. K.μ⁺, K.μ⁻, K.μ~ have C, E, R, pub in their frames. K.ρ extends R, with C, E, pub in its frame. K.π may change pub(d) for one document but only from private to published, never the reverse. Composite transitions, being finite sequences of elementary ones, preserve (a)–(d) by transitivity of ⊇ and ∧. ∎

P6 makes the confinement vivid. Every destructive state change — every removal, every reordering — is confined to the presentational layer. The permanent record (what content exists, which entities have been created, what provenance has been recorded, which publications have been made) can only grow.


## Temporal decomposition

We have arrived at the structural insight underlying the entire design. The state Σ = (C, E, M, R, pub) decomposes into three temporal layers, each answering a different question about the docuverse.

**The existential layer** (C, E) answers *what is*. Content and entities, once created, exist permanently. Addresses are permanent (T8, ASN-0034). Content values are immutable (P0). Entity membership is monotonic (P1). This layer only grows, and its entries are individually immutable once created. Gregory: "once text or a link-orgl is written at an ISA address, that binding is permanent."

**The historical layer** (R, pub) answers *what has happened*. Provenance and publication, once recorded, persist permanently. R records which documents have ever contained which content — a question about history, not current state. Publication records that a document has entered a permanent social contract. This layer only grows, though its entries may become stale: R may assert that document d once contained address a when d's current arrangement no longer references a.

**The presentational layer** (M) answers *what appears now*. Arrangements — the mapping from virtual positions to content identities — are freely mutable. Content can be added, removed, or rearranged. This is the sole locus of destructive change.

| Layer | Components | Mutability | Elementary transitions |
|-------|-----------|------------|----------------------|
| Existential | C, E | Append-only, values immutable | K.α, K.δ |
| Historical | R, pub | Append-only, entries may stale | K.ρ, K.π |
| Presentational | M | Fully mutable | K.μ⁺, K.μ⁻, K.μ~ |

The decomposition constrains the elementary transitions cleanly. No transition modifies all three layers simultaneously. The purely destructive transitions — K.μ⁻ and K.μ~ — are confined to the presentational layer alone, the one layer where impermanence is by design. Cross-layer coupling occurs only in constructive directions: K.α (existential) couples with K.μ⁺ (presentational) via J0; K.μ⁺ (presentational) couples with K.ρ (historical) via J1. The existential and historical layers never shrink.

The existential and historical layers differ in semantics despite sharing the append-only contract. Existential entries state *current facts*: content value v exists at address a, and this remains true permanently. Historical entries state *past events*: document d once contained address a, and this record persists even when the current arrangement no longer agrees. Publication straddles both: it records a historical event (the act of publishing) that creates a permanent existential fact (the document is henceforth public).

Nelson captures the whole architecture in a sentence: "The braid only grows more complex. It never unravels." The existential and historical layers are the braid. The presentational layer is the current view of it.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| Σ.E | E ⊆ T — set of allocated entity addresses, partitioned by IsNode / IsAccount / IsDocument | introduced |
| Σ.R | R ⊆ T_elem × E_doc — provenance relation recording historical content associations | introduced |
| Σ.pub | pub : E_doc → {private, published} — publication state per document | introduced |
| P0 | Content store is append-only with immutable values: dom(C) ⊆ dom(C') ∧ C'(a) = C(a) for a ∈ dom(C) | introduced |
| P1 | Entity set is monotonically growing: E ⊆ E' for every transition, uniformly across levels | introduced |
| P2 | Provenance relation is monotonically growing: R ⊆ R' for every transition | introduced |
| P3 | Publication is irreversible: pub(d) = published ⟹ pub'(d) = published | introduced |
| P4 | Arrangements are the sole state component admitting destructive change (contraction, reordering) | introduced |
| P5 | Provenance bounds: Contains(Σ) ⊆ R, with stale entries possible from prior states | introduced |
| P6 | Destruction confinement: C, E, R, pub are all monotonic across every transition; only M can lose information | introduced |
| K.α | Content allocation — extend dom(C) with fresh IsElement(a) address and value | introduced |
| K.δ | Entity creation — extend E with fresh entity, empty arrangement and private status if IsDocument | introduced |
| K.μ⁺ | Arrangement extension — add V→I mappings to M(d), referential integrity required (S3) | introduced |
| K.μ⁻ | Arrangement contraction — remove V→I mappings from M(d), no permanent-tier changes | introduced |
| K.μ~ | Arrangement reordering — bijection on V-positions preserving I-address multiset | introduced |
| K.ρ | Provenance recording — extend R with (a, d) pair where IsElement(a) ∧ a ∈ dom(C) | introduced |
| K.π | Publication — transition pub(d) from private to published | introduced |
| J0 | Content allocation (K.α) always co-occurs with arrangement extension (K.μ⁺) | introduced |
| J1 | Arrangement extension (K.μ⁺) should co-occur with provenance recording (K.ρ), derived by wp | introduced |
| J2 | Arrangement contraction (K.μ⁻) is isolated: C, E, R, pub unchanged | introduced |
| J3 | Arrangement reordering (K.μ~) is isolated: C, E, R, pub unchanged | introduced |
| J4 | Document fork compounds K.δ + K.μ⁺ + K.ρ with no new content in C | introduced |


## Open Questions

- What invariants must a forked document's initial arrangement satisfy with respect to its source's current arrangement — must it be identical, or may it be a proper subset?
- What constraints does publication impose on subsequent arrangement mutations to the published document?
- Must arrangement reordering respect subspace boundaries within a document (text content at element subspace ≥ 1, link references at subspace 0)?
- What guarantees must the system provide about provenance when content is transitively shared through chains of transclusion?
- Can arrangement contraction on one document affect the discoverability of links attached to the same I-addresses from another document?
- What relationship must hold between a document's version lineage and its sequence of arrangement transitions?
- What additional permanence properties must the provenance relation satisfy for content that participates in link endsets?
