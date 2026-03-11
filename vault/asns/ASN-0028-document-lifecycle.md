# ASN-0028: Document Lifecycle

*2026-03-10*

We are looking for the invariants that govern document creation, ownership, and the transitions a document undergoes from inception to publication. ASN-0026 introduced `Σ.D` — the set of all documents — and treated it as monotonically growing, deferring the full lifecycle to later analysis. ASN-0027 established the permanence of I-space content but revealed that *reachability* is contingent — dependent on V-space arrangements held within documents. Our task now is to specify what a document IS, what creation establishes, what ownership guarantees, and what publication commits the system and its participants to.

---

## The Document as Position

What is a document? The temptation is to say: a container of content. But Nelson's design rejects this. A document is a *position* in the address space — a location in the universal forking tree where content can accumulate. Nelson: "While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents — bytes and links."

A document is a tumbler address under which bytes live. The address exists whether content does or not. An empty document is as real as a full one — "A document is really an evolving ONGOING BRAID," and a braid with zero strands is still a braid. The FEBE protocol confirms this: CREATENEWDOCUMENT is defined as "This creates an empty document. It returns the id of the new document." Creation and population are separate operations.

We formalize this. Each document `d ∈ Σ.D` has an address `addr(d) ∈ T` satisfying T4 from ASN-0001 — a valid tumbler with `zeros(addr(d)) ≥ 2`, placing it at or below the document level of the hierarchy. We identify documents with their addresses.

> **D0** (StructuralIdentity). Documents are identified by address, not by content value:
>
>     (A d₁, d₂ ∈ Σ.D : d₁ = d₂  ⟺  addr(d₁) = addr(d₂))
>
> Two documents at different addresses are distinct even if `Σ.V(d₁) = Σ.V(d₂)` as functions.

Nelson: "There is no uniqueness check, no deduplication, no content hashing. The system does not examine what you store — it only tracks where you store it and who owns it." If Alice creates document `1.1.0.2.0.1` and Bob creates `1.1.0.3.0.1` with byte-for-byte identical text, the system treats them as entirely unrelated. Their I-space addresses differ (by P4 from ASN-0026: distinct allocations produce distinct I-addresses), and their document addresses differ. Identity is structural.

The consequence is that the *only* mechanism for expressing shared origin is transclusion (COPY). If content appears in two documents, the system can determine whether they share I-addresses (one was transcluded from the other) or merely share content value (independently typed). The distinction separates provenance from coincidence.

---

## Creation

What does CREATENEWDOCUMENT establish? We enumerate the properties that hold the instant a document is baptized and that persist thereafter.

> **D1** (DocumentCreation).
>
> *Precondition:* An account address `acct` exists (the creator's account).
>
> *Post (existence):* `d ∈ Σ'.D ∧ d ∉ Σ.D` — the document is new.
>
> *Post (address):* `addr(d)` is a fresh tumbler satisfying `fields(addr(d)).user = fields(acct).user` and `fields(addr(d)).node = fields(acct).node`. The address is allocated as the next sequential child of the account prefix per T9 (ForwardAllocation from ASN-0001).
>
> *Post (empty):* `|Σ'.V(d)| = 0` — the document starts with no content.
>
> *Frame (I-space):* `Σ'.I = Σ.I` — creation allocates no content.
>
> *Frame (existing documents):* `(A d' : d' ∈ Σ.D : Σ'.V(d') = Σ.V(d'))`

The emptiness clause answers a question deferred from ASN-0026: under what conditions can `Σ.V(d)` have length zero? At creation, always. An empty document is a well-formed state — a valid position with nothing yet stored beneath it. Nelson confirms this explicitly: "Documents can contain only links" — and by extension, zero links and zero bytes.

Gregory confirms: `docreatenewdocument` calls `createorglingranf`, which allocates a granfilade entry (the document's position in the address index) and an empty POOM (the document's V-space tree). No spanfilade entries are written. No content is allocated. The document exists — structurally real, content-empty.

The address allocation follows a strict pattern. The session supplies an account address (e.g., `1.1.0.2`). The backend walks the granfilade tree to find the highest existing document address under that prefix and returns the next value: `1.1.0.2.0.3` after two existing documents. No counter is stored; the tree itself is the counter. This is T9 instantiated at the document level.

> **D2** (CreationPrecedesContent). No content operation (INSERT, DELETE, REARRANGE, COPY) succeeds on a document unless the document has been previously created:
>
>     d ∈ Σ.D
>
> is a precondition of every content operation on document `d`.

This is not an accidental property. Gregory confirms: the backend checks `isaexistsgr` before allowing atom insertion — if no document exists at the target address, the operation fails with "nothing at hintisa for atom." Documents do not come into existence lazily. Creation is an explicit, mandatory act that precedes all content manipulation. The design intent is that baptizing a new position in the address space is a deliberate commitment by its owner — irrevocable, since the address is permanently assigned (T8 from ASN-0001).

---

## Ownership

Who controls a document, and what does control mean?

Ownership is encoded in the tumbler address. A document at address `N.0.U.0.D.0.E` belongs to the account `N.0.U`. This is not metadata attached to the document — it IS the address. Since the address is permanent (T8), the creator-document relationship is permanent.

> **Definition (creator).** For a document `d` with address `addr(d)`:
>
>     creator(d) = fields(addr(d)).user
>
> where `fields` is the hierarchical parser from T4 (ASN-0001). This function is computable from `addr(d)` alone and returns the user-level tumbler prefix.

> **D3** (CreatorPermanent). The creator of a document never changes:
>
>     (A Σ, Σ' : d ∈ Σ.D ∧ d ∈ Σ'.D : creator(d) is invariant)
>
> This follows from T8: the address never changes, and `creator` is a pure function of the address. There is no operation that reassigns a document to a different position in the address space.

Nelson acknowledges a subtlety here: ownership can *transfer* in the legal sense. "The rightful copyright holder, or someone who has bought the document rights" is recognized as an owner. But this transfer is contractual — a matter of law and agreement external to the system. No FEBE operation transfers ownership. The tumbler address records *provenance* (where the document was born), and the system enforces rights based on this provenance. Just as a painting by Picasso retains its provenance even when sold to a collector, a Xanadu document retains its creation address even when rights transfer.

We adopt the convention that `owner(d) = creator(d)` throughout this specification. If ownership transfer were modeled, it would require extending the state with a mutable ownership mapping separate from the address structure. Nelson specifies no such mechanism.

### The Ownership Bundle

Ownership is a bundle of rights, not a single privilege.

> **D4** (OwnershipRights). For a document `d` with `owner(d) = u`:
>
> (a) **Content modification**: Only `u` may perform INSERT, DELETE, REARRANGE, or COPY-into on `d`:
>
>         target(op) = d  ⟹  session_account(op) = u
>
> (b) **Out-link control**: Only `u` may create or delete links stored in `d`.
>
> (c) **Address subdivision**: Only `u` may create versions or subdocuments under `d`'s address prefix.
>
> (d) **Visibility control** (pre-publication): `u` determines who may read `d`.
>
> (e) **Economic rights**: When `d`'s content is delivered to a reader, `u` receives royalties proportional to the bytes transmitted.

Nelson is emphatic about the asymmetry between (a)–(c) and the rights that others hold. Ownership does NOT grant control over how others respond to the document. In-links — links that others create pointing into `d` — belong to their creators, not to `d`'s owner. Nelson: "A document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not."

If someone wants to modify your work, they do not request edit access. They create a version — "without damaging the originals." The version lives at their address, under their ownership. This is the architectural boundary between "I control my document" and "I cannot control how the world engages with it."

*Observation (enforcement boundary).* Gregory's evidence reveals that the authorization boundary is *porous* in the implementation: the `validaccount` function unconditionally returns TRUE. A session can call `XACCOUNT` with any tumbler and operate as that account. The ownership model is conventionally enforced by compliant front ends, not architecturally enforced by the backend. Nelson anticipated this: "Because the conceptual structure expects participants to behave in certain ways, these are embraced in the contract offered to users." The abstract specification takes D4 as normative. The enforcement mechanism — whether cryptographic, contractual, or conventional — is an implementation concern.

---

## The Lifecycle

A document undergoes one architecturally significant transition: publication. Content edits and link additions modify the document's V-space but do not alter its relationship to the rest of the docuverse. Publication does.

We extend the system state.

> **Definition (published).** `Σ.published ⊆ Σ.D` is the set of documents that have been published. A document in `Σ.D \ Σ.published` is *private*.

> **D5** (PublicationTransition).
>
> *Forward:* An owner may transition a private document to published:
>
>     d ∈ Σ.D \ Σ.published  ∧  session_account(op) = owner(d)
>     ⟹  d ∈ Σ'.published  is permitted
>
> *Backward:* Publication is effectively irreversible:
>
>     d ∈ Σ.published  ⟹  d ∈ Σ'.published
>
> for all normal transitions. Withdrawal requires "lengthy due process" — a procedure Nelson requires but does not fully specify.

The reasoning for irreversibility is structural, not arbitrary. Once a document is published, others create links pointing to it — links that *they* own, at *their* addresses. Withdrawing the published document would destroy their property. "It is in the common interest that a thing once published stay published, as in the world of paper." The franchise contracts reinforce this: publishers may withdraw "only with one year's notice and fee."

Publication changes the ownership bundle:

> **D6** (PublicationSurrender). For `d ∈ Σ.published`:
>
> (a) **In-link control surrendered**: Anyone may create links pointing into `d`. The owner cannot prevent or remove such links. Nelson: "Each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract."
>
> (b) **Quotation control surrendered**: Anyone may transclude (COPY) content from `d`. "Permission has already been granted: for part of the publication contract is the provision, 'I agree that anyone may link and window to my document.'"
>
> (c) **Easy withdrawal surrendered**: The owner may publish corrections and superseding versions, but "the former version must remain on the network."
>
> (d) **Content modification retained**: The owner retains exclusive modification rights (D4a).
>
> (e) **Economic rights retained**: Royalties flow automatically on every byte transmitted. "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically."

The tradeoff is deliberate. The owner gives up *control over use* in exchange for *automatic, guaranteed, proportional compensation*. This is what enables the web of connections — if published authors could prevent linking, annotation, or quotation, the connective tissue of the docuverse could not form.

Nelson provides a middle path: "privashing." A privashed document is structurally private (the owner retains withdrawal rights) but distributed without restriction. The tradeoff: no royalties, and anyone who linked to it has no recourse upon withdrawal. This is a design-level workaround for authors unwilling to commit to irrevocable publication.

> **D5a** (AccessByStatus). The access rules:
>
>     d ∈ Σ.published  ⟹  anyone may read and link to d
>     d ∉ Σ.published  ⟹  only owner(d) and designated associates may read and link to d

---

## The Session Layer

Nelson's seventeen FEBE commands are stateless. A user names an address, issues a command, the backend responds. There is no concept of "opening" or "closing" a document. The distinction that matters to Nelson is private versus published — a property of the document, not of the session.

Gregory's implementation adds a session management layer: the BERT (Back-End Request Token) mechanism. This layer provides three functions that Nelson left unspecified: access gating, write exclusion, and copy-on-write conflict resolution.

We extract the abstract requirements — what any implementation must provide — without prescribing the BERT mechanism.

> **D7** (WriteExclusion). At most one principal may hold write access to a document at any given time:
>
>     (A d ∈ Σ.D : |{s : s holds write access to d}| ≤ 1)

This is a consequence of the V-space model. V-space operations are not commutative: INSERT at position 2 followed by INSERT at position 5 yields a different state than the reverse order (because the first INSERT shifts subsequent positions). Without serialization, the document's V-space becomes ill-defined. Nelson resolves this by design: "If you want to change something, create a version." There is no concurrent editing of the same document — only the owner modifies, and the owner is singular.

> **D8** (ConflictResolution). When write access is requested on a document that cannot be exclusively claimed, the system may resolve the conflict by creating a new version under the requester's ownership — applying CREATENEWVERSION (A5 from ASN-0027) rather than blocking or failing.

Gregory confirms: when `OPENDOCUMENT` is called with `BERTMODECOPYIF` on a document held by another writer, the backend calls `docreatenewversion` automatically. The requester receives write access to the new version, not the original. The conflict becomes a fork.

*Observation (session mechanics).* Gregory's BERT is lightweight: OPENDOCUMENT inserts a hash-table entry and nothing more — the document's content tree is not loaded until the first actual operation. CLOSEDOCUMENT removes the hash-table entry — no cache flush, no disk I/O. There is no mechanism to upgrade from read access to write access; the session must close and reopen. These are implementation choices that serve the abstract requirements without being required by them.

---

## Versioning as Lifecycle

CREATENEWVERSION is simultaneously a content-sharing operation (A5 from ASN-0027) and a lifecycle event. It creates a new document — a new position in the address space — that begins life with the same V-space mapping as its source.

The placement of the new document depends on the relationship between the session's account and the source document's owner:

> **D9** (VersionPlacement). Let `d_s` be the source document and `u` be the account of the session requesting the version.
>
> *Owned source:* If `owner(d_s) = u`, the new document `d'` is allocated as a child of `d_s` in the address hierarchy:
>
>     fields(addr(d')).doc  is an extension of  fields(addr(d_s)).doc
>
> *Unowned source:* If `owner(d_s) ≠ u`, the new document `d'` is allocated under `u`'s account — as if by CREATENEWDOCUMENT (D1):
>
>     fields(addr(d')).user = u

The ownership test is a tumbler prefix match — `tumbleraccounteq` in Gregory's code: the source document's address must share the account prefix of the session's account. When the match succeeds (owned source), the version nests under the source document in the forking tree. When it fails, the version goes to the requester's own namespace.

Nelson assigns no semantic weight to the resulting hierarchy: "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." The tree position records *who created the version under whose authority*, not *what the version means*. Even the numbering within a version chain — `D.1`, `D.2`, `D.3` — is purely a sequential allocation artifact.

The critical property is that the new document shares I-space identity with the source. A5 from ASN-0027 gives: `(A j : 1 ≤ j ≤ n_{d_s} : Σ'.V(d')(j) = Σ.V(d_s)(j))`. The version starts with position-for-position identical I-address mappings. From this point forward, the two documents evolve independently — edits to one do not affect the other (P7 from ASN-0026). But the shared I-addresses persist in both until explicitly removed by DELETE. The system can always compute which content the two versions share, because shared I-addresses mean shared origin (P4).

---

## Document Set Monotonicity

We now make good on the commitment deferred from ASN-0026: the document set `Σ.D` is monotonically non-decreasing.

> **D10** (DocumentSetMonotone).
>
>     (A d : d ∈ Σ.D : d ∈ Σ'.D)
>
> for any state transition `Σ → Σ'`. Once a document enters `Σ.D`, it remains.

Nelson's evidence is stratified by publication status. For published documents: "It is in the common interest that a thing once published stay published." For private documents: the owner may "withdraw" a document, but withdrawal does not destroy the tumbler address — it removes accessibility. For I-space content: the storage model is append-only — "filed, as it were, chronologically" — bytes are never overwritten or removed.

The subtlety is in what "withdrawal" means. Nelson distinguishes between a document's *existence* (its position in the address space) and its *accessibility* (whether content can be retrieved through it). A withdrawn document still occupies its tumbler address. Its I-space content persists (P0, P1 from ASN-0026). What changes is whether the system will serve content from that position.

At the abstract level, D10 states that the *address* is permanently allocated. The V-space mapping may become empty (all content deleted), but the document remains in `Σ.D`. Combined with T8 (address permanence from ASN-0001), the tumbler address can never be reused for a different document.

Gregory confirms: the granfilade entry for a document is never removed. The `deleteversion` function — the only code path that could conceptually remove a document — is a stub with an empty body.

> **D11** (DocumentSetGrowing). The document set strictly grows over the system's lifetime. Three operations add to `Σ.D`:
>
> - CREATENEWDOCUMENT (D1)
> - CREATENEWVERSION (A5 from ASN-0027)
> - Copy-on-write conflict resolution (D8)
>
> No operation removes from `Σ.D`.

---

## The Inclusion Invariant

When document A includes content from document B through transclusion (COPY), the system must maintain structural relationships that are consequences of the I-space/V-space architecture.

> **D12** (InclusionPreservation). Let `d_t` contain content transcluded from `d_s` — that is, `(E p, q : Σ.V(d_t)(p) = Σ.V(d_s)(q))`. Then:
>
> (a) **Origin traceability**: The I-address `Σ.V(d_t)(p)` structurally encodes `d_s` as the home document via `fields` (T4). This is the address itself, not metadata — to retrieve the content, the system must contact the home location.
>
> (b) **Ownership preservation**: `owner(d_s)` retains ownership of the content at the shared I-address. The owner of `d_t` controls the arrangement (V-space); the I-space content belongs to its creator.
>
> (c) **Non-destruction**: Operations on `d_t` cannot alter `d_s`'s content or arrangement (P7 from ASN-0026).
>
> (d) **Independent evolution**: Operations on `d_s` cannot alter `d_t`'s content or arrangement (P7, applied symmetrically).

Nelson: "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals."

Properties (c) and (d) are already established by P7 (cross-document V-independence from ASN-0026). We restate them here to connect the lifecycle perspective with the content-layer perspective. The inclusion invariant is a direct consequence of the I/V separation: since transclusion shares I-addresses and all editing operations modify only V-space, the included content is immune to the including document's edits, and the source is immune to the includer's edits. Nelson: "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included."

---

## Document Discovery

The system provides no general mechanism to enumerate documents.

> **D13** (DiscoveryByContent). The only reverse-lookup operation is FINDDOCSCONTAINING, which accepts a set of I-address ranges and returns documents whose V-space maps (or has historically mapped) positions to those addresses. Document discovery requires prior possession of I-addresses:
>
>     FINDDOCSCONTAINING : Set(ISpan) → Set(DocId)

There is no LISTDOCUMENTS, no directory, no catalog. Gregory confirms: the FEBE dispatch table contains no enumeration opcode. The granfilade is a point-lookup structure — `fetchorglgr` performs exact-match lookups by document address. The internal tree-walk function `findpreviousisagr` exists only as an allocation helper and is never exposed through the protocol.

The consequence is architecturally significant: documents are found through the *content graph*, not through a namespace. You discover documents because you already possess content they include (and can query FINDDOCSCONTAINING), or because someone communicated their address to you. The system has no concept of browsing or listing.

This is consistent with Nelson's vision of a *literature*, not a *filesystem*. In a filesystem, you navigate by name to find content. In the docuverse, you navigate by content to find connections.

*Observation (index soundness).* As noted in ASN-0027, the FINDDOCSCONTAINING result may be a superset of documents currently containing the queried content, because the content index (spanfilade DOCISPAN entries) is write-only — DELETE does not remove index entries. The consumer must filter stale results by cross-checking V-space.

---

## The Initial State

We verify consistency with ASN-0026's initial state:

- `Σ₀.D = ∅` — no documents exist
- `Σ₀.published = ∅` — nothing published
- `Σ₀.I = ∅` — no content stored
- `Σ₀.V` undefined for all arguments

All properties hold vacuously. D0 through D13 have empty antecedents. The first operation that produces a document is CREATENEWDOCUMENT, which establishes D1's postconditions and brings the first document into `Σ.D`.

---

## Verification Under Operations

We verify that every primitive operation preserves the document lifecycle invariants.

| Operation | D0 (identity) | D3 (creator) | D4 (ownership) | D5 (publication) | D10 (monotone) |
|-----------|---------------|--------------|-----------------|-------------------|----------------|
| CREATENEWDOCUMENT | ✓ unique addr (GlobalUniqueness) | ✓ addr determines creator | ✓ new doc, owner = session | ✓ new doc is private | ✓ adds to Σ.D |
| INSERT | ✓ no addr change | ✓ no addr change | ✓ owner-only precondition | ✓ no pub change | ✓ no doc removed |
| DELETE | ✓ no addr change | ✓ no addr change | ✓ owner-only precondition | ✓ no pub change | ✓ doc survives even if emptied |
| REARRANGE | ✓ no addr change | ✓ no addr change | ✓ owner-only precondition | ✓ no pub change | ✓ no doc removed |
| COPY | ✓ no addr change | ✓ no addr change | ✓ target owner precondition | ✓ no pub change | ✓ no doc removed |
| CREATENEWVERSION | ✓ unique addr | ✓ addr determines creator | ✓ D9 placement | ✓ new doc is private | ✓ adds to Σ.D |
| PUBLISH | ✓ no addr change | ✓ no addr change | ✓ owner-only | ✓ forward only (D5) | ✓ no doc removed |

DELETE deserves particular attention: even when `|Σ'.V(d)| = 0` (all content deleted), the document remains in `Σ.D`. The document is empty but not destroyed. Its address remains permanently occupied. This is the gap between "reachability" (which DELETE can reduce to zero) and "existence" (which D10 guarantees). ASN-0027's A0 and A9 established that reachability is contingent; D10 establishes that existence is not.

---

## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| D0 | Documents are identified by address, not content value: `d₁ = d₂ ⟺ addr(d₁) = addr(d₂)` | introduced |
| D1 | CREATENEWDOCUMENT produces a new document with a fresh address, empty V-space, no I-space allocation | introduced |
| D2 | All content operations require `d ∈ Σ.D` as precondition — creation is explicit, not lazy | introduced |
| creator(d) | `creator(d) = fields(addr(d)).user` — the user-level prefix of the document's address | introduced |
| D3 | Creator is permanent: `creator(d)` is a pure function of the address and never changes | introduced |
| D4 | Ownership rights bundle: content modification, out-link control, address subdivision, visibility (pre-pub), economic rights — all reserved to owner | introduced |
| Σ.published | `Σ.published ⊆ Σ.D` — the set of published documents | introduced |
| D5 | Publication is a forward-only transition: `d ∈ Σ.published ⟹ d ∈ Σ'.published` for normal transitions | introduced |
| D5a | Access by status: published documents are universally accessible; private documents are restricted to owner and associates | introduced |
| D6 | Publication surrenders in-link control, quotation control, and easy withdrawal; retains content modification and economic rights | introduced |
| D7 | Write exclusion: at most one principal may hold write access to a document at any time | introduced |
| D8 | Conflict resolution by versioning: write conflicts may be resolved by CREATENEWVERSION rather than blocking | introduced |
| D9 | Version placement: owned-source versions nest under the source's subtree; unowned-source versions go under requester's account | introduced |
| D10 | Document set monotone: `d ∈ Σ.D ⟹ d ∈ Σ'.D` for all transitions | introduced |
| D11 | Document set only grows: three operations add to `Σ.D`; no operation removes | introduced |
| D12 | Inclusion preserves origin traceability, ownership, non-destruction, and independent evolution — all structurally | introduced |
| D13 | Document discovery is content-identity-driven via FINDDOCSCONTAINING; no enumeration mechanism exists | introduced |

---

## Open Questions

What invariants must a "withdrawal" mechanism satisfy — must the document's V-space be emptied, must its address be marked as withdrawn, or is withdrawal purely an access-control change that leaves content intact?

Must the system provide a formal transition between private and "privashed" (publicly accessible but retractable), and what obligations does privashing create toward users who have linked to the privashed content?

What must the system guarantee about the atomicity of CREATENEWDOCUMENT — if the operation fails after address allocation but before the document becomes operational, is the address permanently consumed?

Must the ownership authorization model be enforced architecturally (by the backend) or is contractual enforcement (by compliant front ends) sufficient for a correct system?

What invariants must the system maintain between a document and its version children — must the parent remain accessible for the children's shared I-addresses to resolve, or are I-addresses independently resolvable regardless of their home document's lifecycle state?

What must the system guarantee about royalty accounting when content is transcluded through multiple levels — if document C transcludes from B which transcludes from A, does the original creator receive royalties proportional to their content when C is read?

Must the system distinguish between "never-populated document" (created but never received INSERT) and "emptied document" (all content deleted) — are these observationally different states, or may an implementation treat them identically?

What must the "lengthy due process" for publication withdrawal guarantee about the system's state during the withdrawal period — must content remain accessible while the process is underway?
