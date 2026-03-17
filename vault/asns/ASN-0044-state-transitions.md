# ASN-0044: State Transitions

*2026-03-17*

We ask what seems a simple question: in what ways can the system state change? ASN-0036 established two state components — a permanent content store and mutable document arrangements — and proved their separation. But that analysis was static: it described what the invariants are, not what the transitions are. We now close that gap. The consultation answers reveal a richer state model and a precise taxonomy of elementary modifications. The central discovery is a *mutability hierarchy*: the components of system state arrange themselves into three temporal layers, each with a distinct permanence contract, and destructive change is confined entirely to the lowest layer.


## The state model

ASN-0036 gave us two components: the content store **C : T ⇀ Val** and the arrangement family **M(d) : T ⇀ T** for each document *d*. These are necessary but insufficient. The consultation evidence reveals three phenomena that neither component records.

First, documents themselves come into existence. Nelson describes exactly two creation modes — *ex nihilo* (an empty document with a fresh address) and *forking* (a new document whose arrangement initially references the source's I-space content). Gregory confirms both use the same allocation mechanism, differing only in whether the new arrangement starts empty or populated. We need an explicit component tracking which documents exist.

Second, content removal from an arrangement does not erase the historical fact that the content was once present. Gregory is direct: the structure recording document-content associations "accumulates entries from every content addition but is never trimmed." Nelson's intent is equally clear: "every previous arrangement remains reconstructable." The system must answer "which documents have ever contained content with origin *a*?" — a question about history, not about current state. This requires a persistent record that survives arrangement mutations.

Third, Nelson describes a state transition orthogonal to content: publication. "A document may be private or published... Once published, a document creates permanent obligations... its author may not withdraw it except by lengthy due process." Publication is a one-way transition affecting document status, independent of the content layer.

We are thus led to a richer model.

**Definition (Document set).** **Σ.D ⊆ DocId** — the set of existing documents, where DocId is the set of document-level tumblers (zeros(t) = 2, per ASN-0034 T4). The arrangement M(d) is defined iff d ∈ D.

We treat links as documents for state-transition purposes. Nelson: "A Xanadu link is a connective unit... owned by a user." Gregory confirms that link creation uses the same allocation mechanism as document creation — both produce named containers with arrangements, both are members of D. The structural distinction between documents and links — their internal subspace layout and endset semantics — is a concern for a separate ASN; here both participate identically in state transitions.

**Definition (Provenance relation).** **Σ.R ⊆ T × DocId** — the pair (a, d) ∈ R records that document d has, at some point in the system's history, contained content with I-address a in its arrangement.

**Definition (Publication state).** **Σ.pub : D → {private, published}** — assigns each document its access classification.

The full system state is:

> **Σ = (C, D, M, R, pub)**

where C and M are as defined in ASN-0036, and D, R, pub are introduced here.


## Mutability contracts

We classify each component by the transitions it admits and discover that the five components obey a strict hierarchy.

**P0 (Content permanence).** The content store admits only extensions, and existing entries are immutable:

`(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ (A a : a ∈ dom(C) : C'(a) = C(a)))`

This is S0 of ASN-0036, restated for the full state model. C is *append-only with immutable values*. Nelson: "Instead, suppose we create an append-only storage system." Gregory: "no `deletegr()`, no `updategr()`, no 'replace at address X' operation anywhere."

**P1 (Document permanence).** The document set admits only extensions:

`(A Σ → Σ' :: D ⊆ D')`

No transition removes a document. Nelson: "New items may be continually inserted in tumbler-space while the other addresses remain valid." Gregory confirms no document-deletion primitive exists.

**P2 (Provenance permanence).** The provenance relation admits only extensions:

`(A Σ → Σ' :: R ⊆ R')`

Once the system records that document d referenced I-address a, that record persists. Gregory: the provenance structure is "a permanently-growing reverse index that accumulates entries from every content addition but is never trimmed."

**P3 (Publication irreversibility).** Publication is a one-way transition:

`(A Σ → Σ', d : d ∈ D ∧ pub(d) = published : pub'(d) = published)`

Nelson: "It is in the common interest that a thing once published stay published, as in the world of paper."

**P4 (Arrangement as sole locus of destructive change).** Arrangements admit three modes of change:

(a) *Extension*: new V→I mappings may be added to M(d).

(b) *Contraction*: existing V→I mappings may be removed from M(d).

(c) *Reordering*: V-positions of existing mappings may be changed while preserving the multiset of I-addresses referenced.

No other state component admits contraction or reordering. Arrangements are the sole locus of destructive change. Gregory states this explicitly for the implementation: the arrangement layer is "the sole locus of destructive mutation." We can now see why: C, D, R, and pub are all monotonic; only M(d) can shrink.


## Elementary transitions

We are looking for the elementary modifications — the minimal state changes that maintain all invariants. Every system operation is a composition of these.

**K.α (Content allocation).** A fresh I-address is bound to a value in the content store:

`C' = C ∪ {a ↦ v}` where `a ∉ dom(C)`

The address a must be an element-level tumbler (zeros(a) = 3, per S7b) allocated under the creating document's prefix (per S7a). By GlobalUniqueness (ASN-0034), a is distinct from every previously allocated address.

**K.δ (Document creation).** A fresh document address is added with an empty arrangement:

`D' = D ∪ {d}` where `d ∉ D`, `M'(d) = ∅`, `pub'(d) = private`

The address d is a document-level tumbler (zeros(d) = 2) allocated under the creating account's prefix. As with content, GlobalUniqueness guarantees that d has never been used.

Nelson identifies two creation modes — ex nihilo and fork — but the fork is not elementary. Forking is K.δ followed by arrangement extension and provenance recording (see J4 below). At the elementary level, all documents begin empty.

**K.μ⁺ (Arrangement extension).** New V→I mappings are added to a document's arrangement. For some d ∈ D:

`dom(M'(d)) ⊃ dom(M(d))`

and for every new mapping M'(d)(v) = a, we require `a ∈ dom(C')` (referential integrity, per S3). Two cases arise naturally:

- The I-address is freshly allocated (a ∈ dom(C') \ dom(C)) — co-occurs with K.α. Nelson: "new content enters I-space permanently."
- The I-address already exists (a ∈ dom(C)) — this is transclusion. Nelson: "the copy shares I-addresses with the source. No new content is created in I-space."

In both cases the arrangement gains mappings; the difference is whether the content store also grows.

**K.μ⁻ (Arrangement contraction).** Existing V→I mappings are removed from a document's arrangement. For some d ∈ D:

`dom(M'(d)) ⊂ dom(M(d))`

Nelson is emphatic about what this does not mean: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." Contraction changes what a document displays; it does not change what exists.

**K.μ~ (Arrangement reordering).** V-positions change without adding or removing mappings. For some d ∈ D, there exists a bijection π : dom(M(d)) → dom(M'(d)) such that:

`(A v : v ∈ dom(M(d)) : M'(d)(π(v)) = M(d)(v))`

The multiset of referenced I-addresses is preserved; only V-positions change. Nelson: content "changes V-space positions but touches nothing in I-space. The same bytes appear in a different order." Gregory confirms reordering is the only kind of transition that affects nothing outside the arrangement itself.

**K.ρ (Provenance recording).** A document-content association is added to the provenance relation:

`R' = R ∪ {(a, d)}` where `a ∈ dom(C)` and `d ∈ D`

**K.π (Publication).** A document transitions from private to published:

`pub'(d) = published` where `pub(d) = private`

All other components are unchanged. Publication does not alter content or arrangement; it changes only the document's access classification.

We observe that these seven kinds — α, δ, μ⁺, μ⁻, μ~, ρ, π — are complete. Gregory's independent analysis of the implementation identifies six persistent state modification kinds (corresponding to our α, δ, μ⁺, μ⁻, μ~, ρ); we add π from Nelson's description of publication as a distinct state transition. No other kind of modification appears in either the design literature or the implementation.

We also observe that neither split nor merge appears as an elementary transition. Nelson addresses this explicitly: the effect of splitting a document is achieved by creating two new documents and using transclusion to reference different portions of the original. Merging is similarly achieved by creating a new document and transcluding from multiple sources. Both are compositions of K.δ, K.μ⁺, and K.ρ — the elementary transitions suffice.


## Coupling and isolation

The elementary transitions do not all occur independently. Some must co-occur to maintain invariants (coupling); some must leave other components unchanged (isolation).

**J0 (Allocation requires placement).** Content allocation K.α always co-occurs with arrangement extension K.μ⁺. Content is allocated under a specific document's tumbler prefix (S7a) and simultaneously placed into that document's arrangement. There is no "allocate content without placing it" — content exists to be arranged.

`(A Σ → Σ', a : a ∈ dom(C') \ dom(C) : (E d, v : d ∈ D' ∧ v ∈ dom(M'(d)) : M'(d)(v) = a))`

Every freshly allocated I-address appears in some document's arrangement.

**J1 (Extension requires recording).** Arrangement extension K.μ⁺ should co-occur with provenance recording K.ρ — when M(d) gains a reference to I-address a, the pair (a, d) should enter R:

`(A Σ → Σ', d, a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R')`

We state *should* advisedly. Gregory identifies one implementation anomaly where provenance recording is skipped, "making content invisible to find_documents." The abstract specification requires the coupling; the anomaly is a defect, not a design choice.

**J2 (Contraction isolation).** Arrangement contraction K.μ⁻ is isolated from all permanent state. When content is removed from an arrangement, C, D, R, and pub are unchanged:

`(A Σ → Σ', d : dom(M'(d)) ⊂ dom(M(d)) : C' = C ∧ D' = D ∧ R' = R ∧ pub' = pub)`

This is the deepest consequence of the design. Deletion is purely presentational — it changes what appears, not what exists or what has been. Gregory confirms: contraction "never triggers" provenance recording, and the provenance structure "is never pruned."

**J3 (Reordering isolation).** Arrangement reordering K.μ~ is isolated from all other state:

`(A Σ → Σ', d : M'(d) is a reordering of M(d) : C' = C ∧ D' = D ∧ R' = R ∧ pub' = pub)`

Reordering does not even update provenance — no new content associations are created. The same I-addresses are referenced, merely at different V-positions.

**J4 (Fork is compound).** Nelson's second document-creation mode — forking from an existing document — is a compound transition. It composes document creation K.δ with arrangement extension K.μ⁺ (populating the new arrangement with mappings to the source's I-addresses) and provenance recording K.ρ (recording the new document's content associations):

`(A Σ → Σ', d_new, d_src : d_new ∈ D' \ D ∧ ran(M'(d_new)) ⊆ ran(M(d_src)) :`
`  (A a : a ∈ ran(M'(d_new)) : (a, d_new) ∈ R'))`

Crucially, the content store C is unchanged — forking creates a new document that *references* existing I-addresses. Nelson: "the new document's id will indicate its ancestry." No new content enters I-space; a new arrangement over existing content enters V-space.


## The provenance gap

An immediate consequence of J1 (extension records provenance) and J2 (contraction does not retract provenance) is that the provenance relation diverges from the current "contains" relation over time.

Define the *current containment*:

`Contains(Σ) = {(a, d) : d ∈ D ∧ a ∈ ran(M(d))}`

**P5 (Provenance bounds).** In any reachable state where J1 has been satisfied for all prior transitions:

`Contains(Σ) ⊆ R`

That is, every I-address currently in some arrangement is recorded in R. But the converse does not hold:

`(a, d) ∈ R` does NOT imply `(a, d) ∈ Contains(Σ)`

The provenance relation may contain *stale* entries from earlier states where some document referenced an I-address it has since removed via K.μ⁻. These entries are not errors — they are memories. Every pair in R was placed there by a K.ρ transition that co-occurred with a K.μ⁺ transition establishing `a ∈ ran(M(d))`. At that moment, `(a, d) ∈ Contains(Σ)` held. The pair remains in R permanently (by P2) even if `(a, d)` later leaves Contains through contraction.

Gregory identifies this as the intended behavior: "find_documents returns historically accurate results, not current state." The provenance relation answers *what has been*, not *what is now*. It is the system's historical memory of content associations — monotonically truthful, never retracting a claim once made.


## Destruction confinement

We can now state the central structural theorem — a generalization of ASN-0036's S9 (two-space separation) to the full five-component state.

**P6 (Destruction confinement).** For every state transition Σ → Σ':

(a) `dom(C') ⊇ dom(C) ∧ (A a : a ∈ dom(C) : C'(a) = C(a))`

(b) `D' ⊇ D`

(c) `R' ⊇ R`

(d) `(A d : d ∈ D ∧ pub(d) = published : pub'(d) = published)`

The only component that can lose information is M.

*Proof.* (a) is P0; (b) is P1; (c) is P2; (d) is P3. P6 combines them into a single statement: every component except arrangements is monotonically non-decreasing across every transition. ∎

P6 makes the confinement vivid. Every destructive state change — every removal, every reordering — is confined to the presentational layer. The permanent record (what content exists, which documents have been created, what provenance has been recorded, which publications have been made) can only grow.


## Temporal decomposition

We have arrived at the structural insight underlying the entire design. The state Σ = (C, D, M, R, pub) decomposes into three temporal layers, each answering a different question about the docuverse.

**The existential layer (C, D)** answers *what is*. Content and documents, once created, exist permanently. Their addresses are permanent (T8, ASN-0034). Their values are immutable (P0). This layer only grows, and its entries are individually immutable once created. Gregory: "once text or a link-orgl is written at an ISA address, that binding is permanent."

**The historical layer (R, pub)** answers *what has happened*. Provenance associations and publication events, once recorded, persist permanently. R records which documents have ever contained which content — a question about history, not about current state. Publication records that a document has entered a permanent social contract. This layer only grows, though its entries may become stale: R may assert that document d once contained address a when d's current arrangement no longer references a.

**The presentational layer (M)** answers *what appears now*. Document arrangements — the mapping from virtual positions to content identities — are freely mutable. Content can be added, removed, or rearranged. This is the sole locus of destructive change.

The design's central guarantee is that the presentational layer cannot corrupt the other two. Nelson captures this:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes [go] difflessly into the storage system."

The changes live in the presentational layer. What they change lives in the existential layer. The two grow together but only one can shrink.

| Layer | Components | Question | Mutability | Temporal scope |
|-------|-----------|----------|------------|----------------|
| Existential | C, D | What is? | Append-only, immutable values | Permanent |
| Historical | R, pub | What has happened? | Append-only, entries may become stale | Permanent |
| Presentational | M | What appears now? | Fully mutable | Current |

The existential and historical layers are both monotonically growing, but they differ in semantics. Existential entries state *current facts* — content value v exists at address a, and this is true now and forever. Historical entries state *past events* — document d once contained address a, and this record persists even if the current arrangement no longer agrees. Publication straddles both: it records a historical event (the act of publishing) that creates a permanent existential fact (the document is henceforth public).

We observe that the decomposition constrains the elementary transitions cleanly. Each transition modifies components within at most two layers:

- K.α (allocation) and K.δ (creation) modify only the existential layer.
- K.ρ (recording) and K.π (publication) modify only the historical layer.
- K.μ⁺ (extension) modifies the presentational layer, typically coupled with K.ρ in the historical layer.
- K.μ⁻ (contraction) and K.μ~ (reordering) modify only the presentational layer.

No elementary transition modifies all three layers simultaneously. And the two purely destructive transitions — contraction and reordering — are confined to the presentational layer alone, the one layer where impermanence is by design.

Nelson: "The braid only grows more complex. It never unravels." The existential and historical layers are the braid. The presentational layer is the current view of it.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| Σ.D | D ⊆ DocId — set of existing documents (zeros(t) = 2) | introduced |
| Σ.R | R ⊆ T × DocId — provenance relation recording historical content associations | introduced |
| Σ.pub | pub : D → {private, published} — publication state per document | introduced |
| P0 | Content store is append-only with immutable values: dom(C) ⊆ dom(C') ∧ C'(a) = C(a) for a ∈ dom(C) | introduced |
| P1 | Document set is monotonically growing: D ⊆ D' for every transition | introduced |
| P2 | Provenance relation is monotonically growing: R ⊆ R' for every transition | introduced |
| P3 | Publication is irreversible: pub(d) = published ⟹ pub'(d) = published | introduced |
| P4 | Arrangements are the sole state component admitting destructive change (contraction, reordering) | introduced |
| P5 | Provenance bounds: Contains(Σ) ⊆ R, with stale entries possible from prior states | introduced |
| P6 | Destruction confinement: C, D, R, pub are all monotonic across every transition | introduced |
| K.α | Content allocation — extend dom(C) with fresh address and value | introduced |
| K.δ | Document creation — extend D with fresh document, empty arrangement, private | introduced |
| K.μ⁺ | Arrangement extension — add V→I mappings, referential integrity required | introduced |
| K.μ⁻ | Arrangement contraction — remove V→I mappings, no permanent state changes | introduced |
| K.μ~ | Arrangement reordering — bijection on V-positions preserving I-address multiset | introduced |
| K.ρ | Provenance recording — extend R with (a, d) pair | introduced |
| K.π | Publication — transition pub(d) from private to published | introduced |
| J0 | Content allocation (K.α) always co-occurs with arrangement extension (K.μ⁺) | introduced |
| J1 | Arrangement extension (K.μ⁺) should co-occur with provenance recording (K.ρ) | introduced |
| J2 | Arrangement contraction (K.μ⁻) is isolated: C, D, R, pub unchanged | introduced |
| J3 | Arrangement reordering (K.μ~) is isolated: C, D, R, pub unchanged | introduced |
| J4 | Document fork compounds K.δ + K.μ⁺ + K.ρ with no new content in C | introduced |


## Open Questions

- What invariants must the provenance relation satisfy when content is transitively shared through chains of transclusion?
- Must a forked document's arrangement initially be identical to its source's, or may it be a proper subset?
- What constraints does publication impose on subsequent arrangement modifications to the published document?
- What invariants must arrangement reordering preserve beyond the multiset of I-addresses — must it respect subspace boundaries?
- Can arrangement contraction on one document affect the discoverability of content in another document that shares the same I-addresses?
- What guarantees must the system provide about the relationship between a document's version lineage and its arrangement history?
- Under what conditions can two documents share the same provenance entry while having no current arrangement overlap?
