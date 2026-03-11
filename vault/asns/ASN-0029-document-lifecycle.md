# ASN-0029: Document Lifecycle

*2026-03-11*

We are looking for the invariants that govern document creation, ownership, and the relationship between documents in the docuverse. The question is deceptively broad: "What is a document?" touches addressing, content storage, access control, and the social contract of publication. We narrow the inquiry by asking: what must ANY implementation maintain about documents, regardless of mechanism?

The thread connecting every answer turns out to be the tumbler address. A document's address is not a locator that can be reassigned; it is the document's identity. Everything that follows — who owns it, where it came from, what it means to publish it — is a consequence of that one design choice.

---

## The Document as Position

A document is not an object stored somewhere. It is a **position** in the tumbler address space — a prefix under which content may accumulate. Nelson is explicit: "While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents — bytes and links." The document is the address, and the address is the document.

We write `d` for a document identifier: a tumbler satisfying T4 (HierarchicalParsing, ASN-0001) with `zeros(d) = 2`, having the form `N.0.U.0.D`. The function `fields(d)` extracts the node, user, and document components. We define:

**AccountAddr.** An account address is a tumbler identifying a user within a node:

    AccountAddr = {a ∈ T : zeros(a) = 1}

By T4 (HierarchicalParsing), these are precisely the tumblers of the form `N.0.U` — the node and user fields with no document or element fields.

**account.** For document `d`, its *account prefix* is:

    account(d) = max≼ {a ∈ AccountAddr : a ≼ d}

where `≼` is the prefix relation from ASN-0001. The maximum is well-defined: the set `{a ∈ AccountAddr : a ≼ d}` is a finite chain under ≼ (any two prefixes of the same tumbler are comparable), so it has a unique maximum. Concretely, `account(d)` is the full `N.0.U` from T4's decomposition of `d` — the longest AccountAddr prefix, whose user field matches the complete user field extracted by `fields(d)`. This is a pure function of the address, computable without consulting any mutable state.

A document can be empty. The CREATENEWDOCUMENT operation creates a document with zero bytes and zero links — an empty container at a freshly allocated address. Nelson: "This creates an empty document. It returns the id of the new document." A document of nothing but links is valid; a document of nothing at all is the degenerate case. "A document is really an evolving ONGOING BRAID" — and a braid with zero strands is still a braid.

Gregory confirms that creation is explicit and non-lazy. The system allocates an address, initializes a structurally valid but content-free container, and returns the address. Attempting to insert content into an address where no document was created is rejected — the system checks for the document's existence before accepting content operations.

Let Σ.D denote the set of existing documents, Σ.I the I-space, and Σ.V(d) the V-space arrangement for document d (all as defined in ASN-0026).

**D0 (EmptyCreation).** CREATENEWDOCUMENT, given an account address `a`, produces a document `d` not previously in existence, with empty content:

    pre:  a ∈ AccountAddr ∧ actor(op) = a
    post ∧ frame:
      (E d : d ∉ Σ.D ∧ d ∈ Σ'.D ∧ account(d) = a :
           |Σ'.V(d)| = 0 ∧ Σ'.pub(d) = private
         ∧ parent(d) undefined                          (root document; D14)
         ∧ (A d' : d' ∈ Σ.D ∧ account(d') = a : d' < d)
         ∧ Σ'.D = Σ.D ∪ {d} ∧ Σ'.I = Σ.I
         ∧ (A d' : d' ∈ Σ.D : Σ'.V(d') = Σ.V(d') ∧ Σ'.pub(d') = Σ.pub(d')))

The existential scopes over both postcondition and frame — the `d` that is freshly created is the same `d` added to `Σ'.D` and quantified over in the frame. The `parent(d) undefined` constraint makes explicit that D0 uses the account's root allocator (T10a sibling stream via `inc(·, 0)`), producing a root document — one whose document field is single-component. This is essential for the monotonicity clause: a root document `a.0.K` with `K` exceeding all existing root document numbers also exceeds all children of lower-numbered roots (since `a.0.K'.x < a.0.K` when `K' < K` by T1), so `(A d' : d' ∈ Σ.D ∧ account(d') = a : d' < d)` holds. A non-root document would not satisfy this — see the discussion of per-allocator monotonicity in D1. Only the account owner may create documents under that account — matching D5(d) and the pattern of D10a and D15. No I-space content is allocated. No existing document is disturbed. The new document exists but contains nothing — a position claimed, a container awaiting content. It begins as `private`; the owner must explicitly publish it.

---

## Address Allocation

The address `d` in D0 is not chosen by the creator — it is *allocated* by the system. Within each account, documents receive sequential addresses. Gregory traces the mechanism: the system walks the existing address structure under the account to find the current maximum, then returns max+1. There is no separate counter; the address structure *is* the counter.

The abstract property is a specialization of T9 (ForwardAllocation, ASN-0001):

**D1 (DocumentAllocation).** Document allocation is per-allocator monotonic, specializing T9 (ForwardAllocation, ASN-0001). Two kinds of document allocators operate under each account:

- The *root allocator* for account `a` produces root documents (single-component document field) via `inc(·, 0)` (T10a sibling stream). D0 uses this allocator.
- A *child allocator* for document `d_s` produces children of `d_s` via `inc(d_s, 1)` (T10a child stream). D12 Case 1 uses this allocator. D12 Case 2 uses the root allocator for the requester's account.

Within each allocator, successive allocations are strictly increasing:

    (A d₁, d₂ : same_allocator(d₁, d₂) ∧ allocated_before(d₁, d₂) : d₁ < d₂)

where `same_allocator(d₁, d₂)` holds iff both are root documents under the same account, or `parent(d₁) = parent(d₂)` (siblings under the same source document).

Different allocators under the same account are NOT jointly monotonic. If account `1.0.1` creates root documents `1.0.1.0.3`, then `1.0.1.0.5`, then versions `1.0.1.0.3` producing child `1.0.1.0.3.1`, we have `1.0.1.0.3.1 < 1.0.1.0.5` by T1 (diverge at position 5: `3 < 5`), yet `1.0.1.0.3.1` was allocated later. The root allocator and the child allocator for `1.0.1.0.3` are independent — each monotonic in its own stream, but not jointly ordered. Per-account uniqueness is guaranteed by T10 (PartitionIndependence): different allocators operate in non-nesting prefix domains, so their outputs are always distinct. By T5 (ContiguousSubtrees), all documents sharing a prefix form a contiguous interval in the tumbler order.

Creation is irrevocable:

**D2 (DocumentPermanence).** Once a document enters the system, its address persists:

    [d ∈ Σ.D ⟹ d ∈ Σ'.D]

for every state transition Σ → Σ'. This is an independent invariant — analogous in spirit to P1 (ISpaceMonotone, ASN-0026), but requiring its own verification, since P1 governs `dom(Σ.I)` while D2 governs `Σ.D`. We verify against each operation: D0 (CREATENEWDOCUMENT) adds a fresh document; its frame explicitly preserves all existing members. D10a (PUBLISH) modifies only `Σ.pub(d)`, not `Σ.D` membership. D12 (CREATENEWVERSION) adds a fresh document; its frame preserves all existing members. The ASN-0026 operations — INSERT, DELETE, COPY, REARRANGE — modify V-space within an existing document but never remove a document from `Σ.D`: P7 (CrossDocVIndependent) preserves non-target documents, and the target document retains its V-space (modified but not destroyed). No defined operation removes a document from `Σ.D`.

Nelson's design has an overwhelming bias toward permanence: even "withdrawal" means removing accessibility, not destroying the address or its I-space content. Nelson: "It is in the common interest that a thing once published stay published, as in the world of paper." The I-space bytes allocated under a document are permanent by P0 and P1 — even when the owner "deletes" them from the document's V-space, they persist and remain available in other documents that transclude them.

We note a subtlety: D2 says the document persists as a member of Σ.D. A separate concept — *accessibility* — governs whether operations on `d` succeed. A withdrawn document has `d ∈ Σ.D` but may reject operations. We return to this distinction in the discussion of publication.

---

## Structural Ownership

Ownership is the most distinctive feature of Nelson's document model. It is not metadata — it is the address itself.

Nelson states this directly: "Ownership is not metadata attached to the document — it IS the User field of the tumbler address. Since the address never changes, ownership never changes."

**D3 (StructuralOwnership).** The function `account(d)` determines the owner of document `d`. It is computable from `d`'s tumbler address alone, without consulting any mutable state. By T6 (DecidableContainment, ASN-0001), whether two documents share the same owner is decidable from their addresses.

**D4 (OwnershipPermanence).** The function `account(d)` is a pure function of the value `d`. Since `d` is a mathematical value — a member of `Σ.D` whose membership is permanent by D2 — and `account` consults no mutable state (D3), the result cannot vary across state transitions:

    account(d) in Σ = account(d) in Σ'

for all state transitions. No operation changes a document's owner. Ownership is immutable by construction, not by policy.

Nelson acknowledges that ownership *transfer* is a real-world need — "someone who has bought the document rights." But there is no protocol operation for transfer. The tumbler records *provenance* — where the document was born — and provenance is permanent. Transfer of economic or editorial rights would operate at the contractual layer, outside the addressing system, just as a painting by Picasso retains its provenance when sold to a collector.

What does ownership guarantee? Nelson defines a specific bundle of rights:

**D5 (OwnershipRights).** For document `d` with owner `account(d)`:

    (a) content modification: only the owner may alter Σ.V(d)
    (b) outgoing links: only the owner may create or remove links stored in d
    (c) visibility (when private): only the owner and designated associates may access d
    (d) address subdivision: only the owner may allocate new tumblers extending d's prefix

D5(c) records Nelson's design intent for private-document visibility. The mechanism for designating associates — what state tracks the designation, which operations establish it — is not formalized in this ASN. All operations defined here (D0, D10a, D12, D15) require ownership for private-document access; the associate access model remains open.

These are normative rights — design requirements on correct participants, not mechanically enforced invariants. Gregory reveals that the backend's account-validation function unconditionally accepts any account address — the backend trusts its front-ends. Nelson confirms this cooperative model: "Because the conceptual structure expects participants to behave in certain ways, these are embraced in the contract offered to users." Enforcement is contractual, not cryptographic. The property D15 (below) states the formal requirement that correct implementations must satisfy.

---

## Document Identity

We are looking for what distinguishes one document from another. The answer: identity is address, not content.

Two users can independently type the same text. Alice's bytes live at I-addresses under her account; Bob's at I-addresses under his. Different addresses, different content in the system's sense, even if the byte values are identical. Nelson: "The system does not examine what you store — it only tracks where you store it and who owns it." There is no uniqueness check, no deduplication, no content hashing.

**D6 (IdentityByAddress).** Document identity is tumbler equality:

    d₁ = d₂ ⟺ fields(d₁) = fields(d₂)

Content comparison plays no role in determining whether two documents are the same document.

The operational consequence is decisive: `FINDDOCSCONTAINING` discovers documents sharing I-space content through *transclusion* — through COPY operations that mapped V-space positions to existing I-addresses. Independent creation of identical text produces different I-addresses; no content-similarity search can discover the relationship. This is precisely what makes transclusion meaningful. COPY says "this content came from there." Independent creation says "this content originated here." The distinction is structural, not metadata.

The complementary property at the content level:

**D7 (OriginTraceability).** For any position `p` in any document `d`, the home document of the displayed content is determinable from the I-address alone:

    home(Σ.V(d)(p)) = max≼ {d' : zeros(d') = 2 ∧ d' ≼ Σ.V(d)(p)}

The `max≼` is necessary: a versioned document like `1.0.1.0.3.1` has multiple prefixes with `zeros = 2` — both `1.0.1.0.3` and `1.0.1.0.3.1` qualify. The home document is the *longest* such prefix, corresponding to the complete document field in T4's decomposition via `fields()`. Since `fields()` uniquely decomposes any I-address (T4, HierarchicalParsing), the set has a well-defined maximum. No additional metadata, no lookup table — the address IS the provenance record. Nelson: "You always know where you are, and can at once ascertain the home document of any specific word or character."

The semantic force of this claim — that `home(a)` identifies the *home document* — requires not just computability but membership: `home(a) ∈ Σ.D` for every I-address appearing in any V-space. This depends on WHERE INSERT allocates fresh addresses.

**D7a (DocumentScopedAllocation).** INSERT on document `d` allocates fresh I-addresses under `d`'s tumbler prefix:

    (A a ∈ fresh : d ≼ a)

where `fresh` is the set of newly allocated I-addresses per P9 (FreshPositions, ASN-0026). This property is not derivable from ASN-0001 or ASN-0026, which constrain uniqueness (GlobalUniqueness, `fresh ∩ dom(Σ.I) = ∅`) but not placement. Gregory's implementation provides the evidence: the allocation mechanism stamps `d`'s address into the search bounds, verifies `d ∈ Σ.D` before accepting any insertion, and computes fresh addresses by incrementing within `d`'s subtree. Each fresh address has the form `d.0.E₁...Eδ` — extending `d` with the element-field separator and element components. Since only INSERT extends I-space (+_ext, ASN-0026), every address in `dom(Σ.I)` was allocated by some INSERT on a document in Σ.D at allocation time.

From D7a we observe that `home(a) = d` for each `a ∈ fresh`. The element-field separator — the zero at position `#d + 1` in `a` — prevents any structural child of `d` from being a longer document-level prefix: a child `d'` extends `d` with a positive component (T4, non-separator components strictly positive), so at position `#d + 1` the child has a positive value while `a` has zero, giving `d' ⋠ a`. The document `d` is therefore the longest document-level prefix, and `home(a) = d`.

**D7b (HomeDocumentMembership).**

    (A d ∈ Σ.D, p : 1 ≤ p ≤ n_d : home(Σ.V(d)(p)) ∈ Σ.D)

Derivation: let `a = Σ.V(d)(p)`. By P2 (ReferentiallyComplete, ASN-0026), `a ∈ dom(Σ.I)`. The address `a` entered `dom(Σ.I)` through some INSERT(d', ...) as a fresh address. By D7a, `home(a) = d'`. INSERT requires `d' ∈ Σ.D`; by D2 (DocumentPermanence), `d'` persists. So `home(Σ.V(d)(p)) = d' ∈ Σ.D`.

---

## Inclusion

When document `d₂` transcludes content from `d₁` — when COPY creates V-space positions in `d₂` that map to I-addresses belonging to `d₁` — the system must maintain several relationships. We derive them from the I-space/V-space separation of ASN-0026.

**D8 (InclusionNonDestruction).** Transclusion does not modify the source. COPY into `d₂` from `d₁` leaves `Σ.V(d₁)` unchanged:

    [target(COPY) = d₂ ∧ d₁ ≠ d₂ ⟹ Σ'.V(d₁) = Σ.V(d₁)]

This is P7 (CrossDocVIndependent, ASN-0026) applied to the source of a COPY. The guarantee is structural: COPY's write target is `d₂`, not `d₁`. Nelson: "Users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals."

The converse is equally important:

**D9 (EditIsolation).** Editing `d₁` does not affect what `d₂` displays:

    [op modifies Σ.V(d₁) ∧ d₁ ≠ d₂ ⟹ Σ'.V(d₂) = Σ.V(d₂)]

This is P7 stated from the other direction. The reasoning: editing `d₁` changes only `Σ.V(d₁)`. I-space is immutable (P0) and monotone (P1). Since `d₂`'s V-space maps to I-addresses, and those addresses still exist with the same content, `d₂` is entirely immune to `d₁`'s structural changes.

Nelson confirms the specific case: "The owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." If Alice deletes a paragraph from her document, Bob's document — which transcludes that paragraph — still displays it. Alice's delete modified her V-space; the I-space bytes persist.

The inclusion relationship also preserves **dual ownership**. The including document's owner controls the arrangement (V-space) — deciding where the transcluded content appears, what surrounds it. The included content's creator retains ownership of the I-space bytes — receiving royalties, being identified as the origin. These two ownership claims coexist without conflict. Nelson: "Each compound document is like the other documents: it has an owner and receives royalties." The arrangement owner gets royalties on the arrangement; the content owners get royalties on the bytes. Proportional, automatic, structural.

---

## Publication

Nelson's publication model partitions documents by accessibility and defines a largely irreversible transition that reshapes the ownership-rights bundle. We extend the state:

**Σ.pub.** `Σ.pub : Σ.D → {private, published, privashed}` assigns a publication status to every document.

Three states. *Private*: accessible only to the owner and designees; the owner retains full control. *Published*: accessible to all; the owner surrenders specific rights in exchange for automatic compensation. *Privashed*: universally accessible but withdrawable at any time — Nelson's escape valve for those who want distribution without binding commitment.

**D10 (PublicationMonotonicity).** No protocol operation transitions a document out of the `published` state:

    [Σ.pub(d) = published ⟹ Σ'.pub(d) = published]

for every state transition Σ → Σ'. This is unconditional. Nelson: "Its author may not withdraw it except by lengthy due process." The reason is structural: other users will have made links to `d` — links at their addresses, constituting their property. Withdrawal would destroy their work. Even superseded documents must remain: "The former version must remain on the network. This is vital because of the links other users may have made to it."

Withdrawal is not a protocol operation — it is a **contractual** mechanism operating outside the technical system. Nelson distinguishes editing (technical) from withdrawal (contractual): "Editing is technical. Withdrawal is contractual." The publication contract provides for withdrawal with deliberate friction — one year's notice and a fee — precisely because easy withdrawal would enable historical revision. The preferred resolution is *supersession*: publishing a new version while leaving the old one accessible. The system provides a Document Supersession Link to direct readers from the old version to the new one. If a future ASN formalizes withdrawal, it would introduce a new contractual operation with its own preconditions — it would not weaken D10 over protocol operations.

We must also establish D10 for operations defined in ASN-0026 (INSERT, DELETE, COPY, REARRANGE). Since `Σ.pub` is introduced in this ASN, those operations naturally say nothing about it.

**D10-ext (PublicationFrameForASN26).** Operations defined in ASN-0026 do not modify publication status:

    (A d : d ∈ Σ.D : Σ'.pub(d) = Σ.pub(d))

for any ASN-0026 operation. Those operations modify only I-space (append) and V-space (rearrangement) — they have no mechanism to alter the publication status field. With D10-ext, D10 holds universally: D0 sets `Σ'.pub(d) = private` for the new document and preserves `Σ.pub` for all existing documents (frame); D10a transitions only from `private` and cannot produce a non-published result from `published`; D12 sets `Σ'.pub(d_v) = private` for the new version and preserves `Σ.pub` for all existing documents (frame); ASN-0026 operations preserve `Σ.pub` by D10-ext.

Within the current formal model, `privashed` is also permanent — no defined operation transitions a document out of `privashed`. D10a requires `Σ.pub(d) = private`; D0 and D12 set new documents to `private` and preserve existing statuses in their frames; ASN-0026 operations preserve `Σ.pub` by D10-ext; D17 is a pure query. Nelson's design intent, however, is that `privashed` should NOT share this permanence — a privashed document should be freely revertible to `private`, with the understanding that anyone who linked to it has no recourse. Realizing this intent requires a WITHDRAW or UNPRIVASH operation with precondition `Σ.pub(d) = privashed`, which is deferred to a future ASN.

**D10a (PublishOperation).** PUBLISH(d, status) transitions a document's publication state:

    pre:  d ∈ Σ.D ∧ account(d) = actor(op) ∧ Σ.pub(d) = private ∧ status ∈ {published, privashed}
    post: Σ'.pub(d) = status
    frame: Σ'.D = Σ.D ∧ Σ'.I = Σ.I ∧ Σ'.V(d) = Σ.V(d) ∧ (A d' : d' ∈ Σ.D ∧ d' ≠ d : Σ'.V(d') = Σ.V(d') ∧ Σ'.pub(d') = Σ.pub(d'))

Only the owner may publish. Publication does not alter content — it changes only accessibility and the rights bundle. The transitions from `privashed` to `private` and from `privashed` to `published` are permitted but deferred to open questions; only the `private → published` and `private → privashed` paths are specified here.

**D11 (PublicationSurrender).** Publication changes the rights bundle. Upon transition to `published`:

    Σ.pub(d) = published ⟹
        (a) any session may read d
        (b) any session may create links into d (incoming links)
        (c) any session may transclude from d (quotation)
        (d) withdrawal requires extraordinary process

Nelson frames (b) and (c) as a deliberate surrender: "Each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." And: "Since the copyright holder gets an automatic royalty, anything may be quoted without further permission."

What publication does NOT surrender: D5(a) and D15 — the owner retains exclusive content modification rights. D5(b) — the owner controls outgoing links. You can still edit your published document; you simply cannot prevent the world from quoting, linking to, and annotating it. Nelson splits traditional copyright's goals — compensation and control — and keeps only the first:

    ownership guarantees content integrity + economic rights
    ownership does NOT guarantee control over response, connection, or quotation

Nelson is unambiguous about the tradeoff: "There is no way whatever to ascertain or control what happens at the users' terminals. Therefore perforce all use whatever is legitimate, and anyone who plans to be vulnerable to 'misuse,' whatever he or she thinks that may be, had better keep his or her stuff off the system."

---

## Versioning

A version is not a patch or diff — it is a **new document** created from an existing one.

The CREATENEWVERSION operation takes a source document `d_s` and produces a fresh document `d_v` whose initial V-space is a complete transclusion of the source. The new document shares I-space addresses with the source but has independent V-space from that point forward.

**D12 (VersionCreation).** CREATENEWVERSION(d_s, a_req) — where `a_req = actor(op)` is the requesting account — produces `d_v` such that:

    pre:  d_s ∈ Σ.D ∧ a_req = actor(op) ∧ (Σ.pub(d_s) ∈ {published, privashed} ∨ account(d_s) = a_req)
    post:
    (a) d_v ∉ Σ.D ∧ d_v ∈ Σ'.D
    (b) |Σ'.V(d_v)| = |Σ.V(d_s)|
    (c) (A p : 1 ≤ p ≤ |Σ.V(d_s)| : Σ'.V(d_v)(p) = Σ.V(d_s)(p))
    (d) Σ'.V(d_s) = Σ.V(d_s)
    (e) Σ'.I = Σ.I
    (f) Σ'.pub(d_v) = private
    (g₁) account(d_s) = a_req ⟹ (A d' : d' ∈ Σ.D ∧ parent(d') = d_s : d' < d_v)
    (g₂) account(d_s) ≠ a_req ⟹ (A d' : d' ∈ Σ.D ∧ account(d') = a_req : d' < d_v)
    frame: Σ'.D = Σ.D ∪ {d_v} ∧ (A d' : d' ∈ Σ.D : Σ'.V(d') = Σ.V(d') ∧ Σ'.pub(d') = Σ.pub(d'))

Condition (c) is crucial: the version shares I-addresses with the source. This is transclusion, not copying. Both documents display the same bytes, traceable to the same origin, subject to the same royalty accounting. Condition (e) confirms: no new I-space content is allocated. Condition (f) establishes that a version begins as private, regardless of the source's publication status. A version starts as pure reference. From this moment, `d_v` and `d_s` evolve independently — edits to one do not affect the other (D9).

The placement of the new version's address depends on ownership. Gregory's code reveals a conditional: the system tests whether the source document's account matches the requesting account — a tumbler prefix match.

**D13 (VersionPlacement).** For CREATENEWVERSION(d_s, a_req) creating d_v:

    account(d_s) = a_req ⟹ parent(d_v) = d_s
    account(d_s) ≠ a_req ⟹ account(d_v) = a_req

In the first case (own document), the version is allocated as an immediate structural child of the source — `parent(d_v) = d_s` per D14's definition. Its address extends the source's tumbler by exactly one document level — if `d_s = A.0.D₁`, then `d_v = A.0.D₁.D₂`. This follows from T10a (AllocatorDiscipline) with `k' = 1`: the parent allocator spawns a child via `inc(d_s, 1)`. By TA5(d), `inc(d_s, 1)` appends a single component (no intermediate zeros, final component 1), so `zeros(d_v) = zeros(d_s) = 2` — the child is a document-level address, satisfying T4. The constraint `k' = 1` is essential: `k' = 2` would introduce a new zero separator, producing `zeros = 3` (element-level); `k' ≥ 3` would exceed T4's maximum of three zeros. Nelson: "The new document's id will indicate its ancestry." The ancestry is encoded in the address and permanent — `account(d_v)` is a pure function of the value `d_v`, which does not change.

In the second case (someone else's document), the version lives under the versioner's own account — just like any new document. There is no structural record of the ancestry. Nelson: "The Document field of the tumbler may be continually subdivided, with new subfields indicating daughter documents and versions."

**D14 (VersionForest).** Define the *structural parent* of a document `d` as the longest proper document-level prefix of `d`:

    parent(d) = max≼ {d' : d' ≺ d}    (partial — undefined when {d' : d' ≺ d} = ∅)

where `d_s ≺ d_v` iff `d_s ≼ d_v ∧ d_s ≠ d_v ∧ zeros(d_s) = zeros(d_v) = 2`. The relation ≺ is a partial order (it includes all ancestors, not just the immediate parent). The *covering relation* — the Hasse diagram of ≺ — forms a forest: each document has at most one immediate structural parent, and there are no cycles. A root document (single-component document field, such as `1.0.1.0.3`) has no document-level proper prefix, so `parent` is undefined — these are the roots of the forest. For non-root documents, the tumbler hierarchy gives a unique longest proper prefix at the document level, so `parent(d)` is well-defined.

We derive that the forest connects to the document set:

    (A d : d ∈ Σ.D ∧ parent(d) defined : parent(d) ∈ Σ.D)

The argument: the only operations that add documents to Σ.D are D0 and D12. D0 produces only root documents (postcondition: `parent(d)` undefined), so non-root documents in Σ.D are created only by D12 Case 1 (own-account versioning), which requires `d_s ∈ Σ.D` as a precondition and produces `d_v` with `parent(d_v) = d_s` (D13). So `parent(d_v) = d_s ∈ Σ.D` at creation time. By D2 (DocumentPermanence), `d_s` persists in all subsequent states. D12 Case 2 uses the requester's root allocator, producing root documents with no structural parent. Thus the parent of every non-root document in Σ.D is itself a member of Σ.D.

**Worked example.** Let Σ contain documents `d_s = 1.0.1.0.3` with `Σ.V(d_s) = {1 ↦ a₁, 2 ↦ a₂}`, `Σ.pub(d_s) = published`, and a later root document `d_r = 1.0.1.0.5` (allocated after `d_s` by the root allocator). Both have `account = 1.0.1`.

*Case 1: own-account version.* CREATENEWVERSION(d_s, 1.0.1) — the owner versions their own document. Since `account(d_s) = 1.0.1 = a_req`, D13 gives `parent(d_v) = d_s`. The child allocator for `d_s` (T10a with `k' = 1`) produces `d_v = 1.0.1.0.3.1` — the first structural child of `d_s`. We verify the postconditions:

- (a): `1.0.1.0.3.1 ∉ Σ.D` (fresh) and `1.0.1.0.3.1 ∈ Σ'.D` ✓
- (b): `|Σ'.V(d_v)| = |Σ.V(d_s)| = 2` ✓
- (c): `Σ'.V(d_v)(1) = a₁`, `Σ'.V(d_v)(2) = a₂` — same I-addresses as source ✓
- (d): `Σ'.V(d_s) = {1 ↦ a₁, 2 ↦ a₂}` — source unchanged ✓
- (e): `Σ'.I = Σ.I` — no new I-content allocated ✓
- (f): `Σ'.pub(d_v) = private` — version starts private despite source being published ✓
- (g₁): no existing children of `d_s` in Σ.D (no `d'` with `parent(d') = d_s`), so the quantifier is vacuously satisfied ✓
- D13 placement: `parent(1.0.1.0.3.1) = 1.0.1.0.3 = d_s` ✓ (immediate child via `inc(d_s, 1)`)

Note the interleaving: `d_v = 1.0.1.0.3.1 < d_r = 1.0.1.0.5` by T1 (diverge at position 5: `3 < 5`). The old per-account monotonicity `d_v > d_r` would fail — this is why D12(g) is split by case: (g₁) requires only that `d_v` exceeds existing children of `d_s`, not all documents under the account.

A second own-account version produces `d_v' = 1.0.1.0.3.2` (monotonic within the child allocator for `d_s`), and `parent(d_v') = d_s` as well — both versions are siblings under `d_s`.

*Case 2: cross-account version.* CREATENEWVERSION(d_s, 2.0.1) — user `2.0.1` versions Alice's document. Since `account(d_s) = 1.0.1 ≠ 2.0.1 = a_req`, D13 gives `account(d_v) = 2.0.1`. The version is allocated under the requester's account, say `d_v = 2.0.1.0.4`. Postconditions (a)–(f) hold identically. But `d_s ⋠ d_v` — there is no structural ancestry in the address. The version relationship exists only through shared I-addresses: both `Σ'.V(d_v)` and `Σ'.V(d_s)` map to `{a₁, a₂}`.

Note that version numbering carries no semantic weight. Nelson is emphatic: "The version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." And: "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." The ordering is a consequence of sequential allocation, not a statement about quality or primacy.

---

## Access Control: The Abstract Principles

Nelson's FEBE commands are stateless — there is no session concept in the original design. No OPEN, no CLOSE, no session state. You name a tumbler, issue a command, the system responds. Gregory's implementation introduces a session layer via the BERT mechanism for concurrency control: sessions must OPEN a document before operating on it, acquiring a Back-End Request Token; CLOSE releases the token.

The session mechanism is implementation. The principles it serves are abstract.

Every operation in the system is issued by some account. We write `actor(op)` for the account address on whose behalf operation `op` is performed — the account claiming authorship of the action. In a correct system, this corresponds to the account that initiated the request.

**D15 (OwnerExclusiveModification).** Only the owner may modify a document's content:

    [op modifies Σ.V(d) ⟹ account(d) = actor(op)]

This is a design requirement on correct participants: any implementation that satisfies the Xanadu protocol must ensure D15 holds. It is not a mechanically enforced invariant — the backend trusts its front-ends to supply truthful account identities. But a front-end that violates D15 is non-conforming.

This is Nelson's fundamental access rule. A non-owner who wishes to modify creates a version (D12) rather than altering the original. The original is protected absolutely: "Only the owner has a right to withdraw a document or change it."

**D16 (NonOwnerForking).** When a non-owner requests modification of document `d`, the resolution is to create a new version under the requester's account:

    account(d) ≠ actor(op) ∧ op requests modification of d
    ⟹ system applies CREATENEWVERSION(d, actor(op)) with account(d_v) = actor(op)

This is Nelson's resolution to the tension between collaboration and ownership. Rather than competing for access to a shared mutable object, users create independent versions. Gregory implements this directly: when write access is requested on a document and the requester is not the owner, the system creates a new version for the requester and opens that instead. The original is never touched.

The consequence is striking: **there are no write-write conflicts between different users.** If Alice owns document `d` and Bob wants to modify it, Bob gets a new version `d'` under his own account. Alice continues editing `d`; Bob edits `d'`. Both evolve independently (D9). The conflict between "I want to edit this" and "someone else is editing this" evaporates — or rather, it is resolved structurally by the address space.

Gregory's implementation reveals additional detail about the single-owner case. When the same owner has multiple sessions, only one can hold write access at a time — the system does not allow upgrading from read access to write access in place; the session must close and reopen. But this is concurrency mechanism, not abstract invariant. The abstract content is D15: one owner, one authority.

---

## Document Discovery

Finally, how are documents *found*? Nelson provides exactly one mechanism:

**D17 (ContentBasedDiscovery).** The operation FINDDOCSCONTAINING takes a set of I-address spans `S`, where each `(s, l) ∈ S` is well-formed per T12 (SpanWellDefined, ASN-0001) — in particular `l > 0`, ensuring `s ⊕ l` is defined by TA0. Each span denotes the contiguous range `{t : s ≤ t < s ⊕ l}`. The operation returns every document whose V-space maps to any address within those spans:

    FINDDOCSCONTAINING(S) = {d ∈ Σ.D : (E p : 1 ≤ p ≤ n_d : (E (s,l) ∈ S : s ≤ Σ.V(d)(p) < s ⊕ l))}
    frame: Σ' = Σ

FINDDOCSCONTAINING is a pure query — it inspects state but modifies nothing. The frame `Σ' = Σ` (equivalently: `Σ'.D = Σ.D ∧ Σ'.I = Σ.I ∧ (A d : d ∈ Σ.D : Σ'.V(d) = Σ.V(d) ∧ Σ'.pub(d) = Σ.pub(d))`) ensures that D2 (DocumentPermanence) and D10 (PublicationMonotonicity) are trivially preserved.

There is no enumeration operation — no way to ask "what documents exist?" Gregory confirms: no LISTDOCUMENTS, no ENUMERATEDOCUMENTS, no namespace walk. The system can answer "which documents contain this content?" but not "what is in the docuverse?"

This is not an oversight but a consequence of the design. The tumbler space is sparse and partitioned by ownership. Each owner knows their own documents (they created them). The system connects documents through shared I-addresses — the transclusion graph. Navigation is through content identity, not through directories.

The asymmetry is precise. Documents related by transclusion are discoverable: they share I-addresses, so FINDDOCSCONTAINING finds them. Documents with independently created identical content are invisible to each other: different I-addresses, no structural connection. The only way to establish a discoverable relationship is through COPY — through intentional transclusion. Independently retyping the same words creates new I-space bytes and leaves the documents in separate worlds.

This connects back to D6 (IdentityByAddress) and D7 (OriginTraceability): identity is address, provenance is structural, and discovery follows the structure.

---

## Summary of State

Collecting what this ASN establishes. The state Σ from ASN-0026 (Σ.D, Σ.I, Σ.V) is extended with:

    Σ.pub : Σ.D → {private, published, privashed}

The function `account : DocId → AccountAddr` is derived from the tumbler structure, not stored as independent state. The structural subordination relation `≺` for version ancestry is likewise determined by the tumbler hierarchy. No new mutable state beyond `Σ.pub` is introduced.

The key insight across all properties: the tumbler address does extraordinary work. It encodes identity (D6), ownership (D3, D4), provenance (D7), and ancestry (D13, D14). Because documents are permanent members of Σ.D (D2) and these encodings are pure functions of the address value, all of them are permanent — no mutable state is consulted, so no state transition can alter them. A single design decision — permanent addresses — gives the entire lifecycle its character: immutable ownership, structural provenance, non-destructive collaboration, and version forests that grow but never reorganize.

---

## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| AccountAddr | `{a ∈ T : zeros(a) = 1}` — the set of account-level tumblers | introduced |
| account(d) | account prefix function: DocId → AccountAddr, `max≼ {a ∈ AccountAddr : a ≼ d}` — the longest AccountAddr prefix | introduced |
| actor(op) | the account address on whose behalf operation `op` is performed | introduced |
| D0 | CREATENEWDOCUMENT produces root document `d` with `d ∈ Σ'.D`, `\|Σ'.V(d)\| = 0`, `Σ'.pub(d) = private`, `parent(d)` undefined, `(A d' ∈ Σ.D ∩ account⁻¹(a) : d' < d)`; pre: `actor(op) = a` | introduced |
| D1 | per-allocator monotonicity: `same_allocator(d₁, d₂) ∧ allocated_before(d₁, d₂) ⟹ d₁ < d₂`; root and child allocators are independently monotonic | introduced |
| D2 | `[d ∈ Σ.D ⟹ d ∈ Σ'.D]` for all transitions — documents are permanent | introduced |
| D3 | `account(d)` is computable from `d`'s tumbler alone, no mutable state consulted | introduced |
| D4 | `account(d)` is immutable across all state transitions | introduced |
| D5 | owner has exclusive rights: content modification, out-links, visibility, address subdivision (design requirement on correct participants) | introduced |
| D6 | document identity is tumbler equality; content comparison plays no role | introduced |
| D7 | `home(a) = max≼ {d' : zeros(d') = 2 ∧ d' ≼ a}` — home document determinable from address alone | introduced |
| D7a | `(A a ∈ fresh : d ≼ a)` — INSERT allocates I-addresses under the creating document's prefix | introduced |
| D7b | `(A d ∈ Σ.D, p : 1 ≤ p ≤ n_d : home(Σ.V(d)(p)) ∈ Σ.D)` — home document is always in Σ.D | introduced |
| D8 | transclusion (COPY) does not modify the source document's V-space | introduced |
| D9 | editing `d₁` does not affect `Σ.V(d₂)` for `d₂ ≠ d₁` | introduced |
| Σ.pub | publication status: `DocId → {private, published, privashed}` | introduced |
| D10 | `[Σ.pub(d) = published ⟹ Σ'.pub(d) = published]` unconditionally for all protocol operations | introduced |
| D10-ext | `(A d : d ∈ Σ.D : Σ'.pub(d) = Σ.pub(d))` for ASN-0026 operations — publication status frame | introduced |
| D10a | PUBLISH(d, status): transitions `private → published` or `private → privashed`, owner only | introduced |
| D11 | publication surrenders control over incoming links, quotation, and easy withdrawal | introduced |
| D12 | CREATENEWVERSION(d_s, a_req) produces `d_v` sharing all I-addresses, `Σ'.pub(d_v) = private`; monotonicity split: (g₁) own-account — exceeds children of `d_s`; (g₂) cross-account — exceeds all docs under `a_req`; pre: `a_req = actor(op)`, source accessible | introduced |
| D13 | own-account: `parent(d_v) = d_s` via `inc(d_s, 1)` (`k' = 1` preserves `zeros = 2`); cross-account: `account(d_v) = a_req` | introduced |
| D14 | covering relation of `≺` forms a forest; `(A d : d ∈ Σ.D ∧ parent(d) defined : parent(d) ∈ Σ.D)` | introduced |
| D15 | only owner may modify document content: `account(d) = actor(op)` (design requirement) | introduced |
| D16 | non-owner modification requests resolve by creating a new version | introduced |
| D17 | `FINDDOCSCONTAINING(S)` — content-based discovery via span membership; frame: `Σ' = Σ` | introduced |

## Open Questions

- What invariants must location-fixed windows satisfy, where an inclusion tracks a position in the source document's evolving V-space rather than fixed I-addresses?
- What must the royalty accounting model guarantee about proportional compensation when transcluded content is delivered?
- Under what conditions may a published document's accessibility be revoked, and what must the withdrawal process preserve about existing links?
- What must the system guarantee about document persistence when storage funding lapses?
- Must the transition from `privashed` to `published` be permitted, and if so, does it retroactively bind the owner to the non-withdrawal obligation of D10?
- What abstract properties must concurrent access satisfy to ensure D15 holds when multiple sessions operate simultaneously?
- What must the system preserve about the relationship between a version and its source when the version is created by a non-owner and has no structural ancestry link?
- Does FINDDOCSCONTAINING (D17) operate over all documents in Σ.D, or only over published and accessible documents?
