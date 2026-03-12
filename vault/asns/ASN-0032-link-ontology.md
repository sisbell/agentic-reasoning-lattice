# ASN-0032: Link Ontology

*2026-03-12*

## The Problem

We are looking for the specification of a *link* in the Xanadu system. The question seems simple: what is a connection between pieces of content? But the question cannot be answered in isolation from the environment in which links exist — a universe of permanent content identity, mutable document arrangement, transclusion across documents, and version derivation. A link specification that ignores these properties would be vacuous; one that depends on implementation details would be fragile. We need the abstract guarantees.

Four concerns must be resolved simultaneously. What does a link *connect* — positions in documents, whole documents, or something else? What must be true about a link as a *permanent object* — can it break, can it be destroyed? How are links *discovered* — given content, how do we find what connects to it? And who *owns* a link — the creator, or the author of the connected content?

We shall find that a single architectural decision resolves all four.

## The Foundational Decision

Consider a link connecting paragraph A in one document to paragraph B in another. If the link records V-space positions — "position 47 in document X, position 112 in document Y" — then every INSERT or DELETE that shifts those positions invalidates the link. The link would be as fragile as the arrangement it references.

We observe that I-space is immutable (P0, ASN-0026) and monotone (P1, ASN-0026). Content at an I-address never changes and never disappears. If a link references I-space addresses instead of V-space positions, it is immune to every V-space operation. No INSERT, DELETE, or REARRANGE can alter what the link references, because those operations modify V-space while leaving I-space unchanged.

This is the foundational decision: **a link's endpoints are sets of I-space spans.** Nelson's metaphor is precise: "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." The strap holds because bytes have permanent I-space identity. The metaphor would fail if the strap were tied to positions rather than to the bytes themselves.

Everything that follows — survivability, bidirectional discovery, version transparency, resurrection after apparent destruction — is a derived consequence of this one decision. We trace those consequences now.

---

## State Extension

### Endsets

An *endset* is a finite set of I-spans, where each I-span is a pair `(s, ℓ)` with `s` an allocated I-address and `ℓ > 0`, denoting the contiguous set `{a : s ≤ a < s ⊕ ℓ}` per T12 (SpanWellDefined, ASN-0001). We write:

    Endset = P_fin({(s, ℓ) : s ∈ dom(Σ.I) ∪ dom(Σ.L), ℓ > 0})

The *covered set* of an endset is the union of its constituent spans:

    covered(E) = ∪{[s, s ⊕ ℓ) : (s, ℓ) ∈ E}

An endset is *non-empty* when `covered(E) ≠ ∅`, which holds when `E ≠ ∅` since each span contains at least its start address (TA-strict, ASN-0001: `s ⊕ ℓ > s`).

Note the domain of `s`: an endset may reference content I-addresses (`dom(Σ.I)`) or link I-addresses (`dom(Σ.L)`). The address space is uniform — a link may point to content or to another link. We return to this in L14.

An endset may reference I-addresses originating from multiple documents simultaneously. A passage of composite content — text in a document that includes transcluded material from several sources — occupies I-addresses from several distinct INSERT operations. An endset covering such a passage captures all constituent I-addresses. The endset does not "belong to" any single document; it identifies content by permanent identity, which is document-neutral.

### Links

A *link* is a triple of endsets:

    LinkRecord = (from : Endset, to : Endset, type : Endset)

The system state is extended with a partial function from link I-addresses to link records:

    Σ.L : IAddr ⇀ LinkRecord

and a *visibility* function recording which links appear in each document's current V-stream:

    Σ.visible : DocId → P_fin(dom(Σ.L))

The domain `dom(Σ.L)` is the set of all links that have been created. The *home document* of a link is determined by its I-address:

    home(l) = max≼ {d' : zeros(d') = 2 ∧ d' ≼ l}

per D7 (OriginTraceability, ASN-0029). This is a structural property of the address, not mutable state — it is computable from the tumbler alone.

### The Link Subspace

Within a document's V-space, the text subspace and the link subspace occupy disjoint regions identified by the first component of the element field (T7, SubspaceDisjointness, ASN-0001). Let subspace 1 denote text content and subspace 2 denote link references. A link `l` with `home(l) = d` appears in d's V-stream at a position in the link subspace when `l ∈ Σ.visible(d)`.

The subspace separation ensures that operations on text content do not shift link references and vice versa (TA7b, SubspaceFrame, ASN-0001). An INSERT of new text into a document displaces text positions but leaves link-subspace positions unchanged.

---

## Link Permanence

### L0 — Link Immutability

Once a link is created, its record is immutable:

    [l ∈ dom(Σ.L)  ⟹  Σ'.L(l) = Σ.L(l)]

for any state transition Σ → Σ'. The endsets of a link never change. This follows the same permanence discipline as content bytes: I-space is write-once. The parallel is exact — P0 (ISpaceImmutable, ASN-0026) says `Σ'.I(a) = Σ.I(a)` for content; L0 says `Σ'.L(l) = Σ.L(l)` for links. Nelson's design stores exactly two kinds of things in tumbler-space — content bytes and links — and both enjoy the same immutability.

### L1 — Link Monotonicity

The set of links grows monotonically:

    [l ∈ dom(Σ.L)  ⟹  l ∈ dom(Σ'.L)]

for any state transition Σ → Σ'. A link, once created, is never removed from the link store. Combined with L0, this means no operation modifies or removes any link record.

L0 and L1 are the link-specific instances of T8 (AddressPermanence, ASN-0001): "If tumbler `a` is assigned to content `c` at any point in the system's history, then for all subsequent states, `a` remains assigned to `c`." Links occupy the same permanent address space as content. This is not a coincidence; it is the architectural choice that makes links first-class objects in the docuverse.

### Derived: No Link Reuse

From L0 and L1: a link I-address, once allocated, is never freed and its record never changes. The proof mirrors NO-REUSE (ASN-0026). Suppose `l ∈ dom(Σ.L)` with `Σ.L(l) = R`. By L1, `l ∈ dom(Σ'.L)` for every successor state. By L0, `Σ'.L(l) = R`. The address is never available for reallocation.

The implementation evidence confirms this is deliberate: the FEBE protocol defines no DELETELINK operation. Forty command slots were allocated; link creation has a slot, link discovery has a slot, link following has a slot. No slot was assigned to link deletion. The three storage layers — granfilade (permanent I-address), span index (append-only), document V-stream (mutable) — provide deletion paths only at the V-stream layer. We return to this asymmetry in L15.

---

## Link Survivability

We can now state and derive the central survivability property.

### L2 — Endset Stability Under All Operations

For any operation `op` producing state transition Σ → Σ':

    (A l ∈ dom(Σ.L), E ∈ {from, to, type} :
        covered(Σ'.L(l).E) = covered(Σ.L(l).E))

The set of I-addresses an endset covers is invariant under all operations.

The derivation is immediate from L0: `Σ'.L(l) = Σ.L(l)`, so the endsets are identical records, and `covered` is a pure function of the record. But the deeper point is not merely that the *record* doesn't change — it is that the *content* it references doesn't change either:

    (A (s, ℓ) ∈ Σ.L(l).E, a : s ≤ a < s ⊕ ℓ :
        Σ'.I(a) = Σ.I(a))

This follows from P0 (ISpaceImmutable, ASN-0026): the bytes at those I-addresses are unchanged. A link that meant "these bytes" before an edit still means "these bytes" after the edit. The edit changed how those bytes are arranged in some document's V-space, but the link does not reference V-space.

We can now catalog the survivability per operation:

| Operation | V-space effect | Link effect |
|-----------|---------------|-------------|
| **INSERT** | Shifts positions after insertion point | None — I-addresses unchanged |
| **DELETE** | Removes positions from V-stream | None — I-addresses persist in I-space |
| **REARRANGE** | Changes V-position ordering | None — link follows bytes, not positions |
| **COPY** | Adds shared I-addresses to target | None — existing endsets unchanged |
| **CREATENEWVERSION** | Creates new V-stream sharing I-addresses | None — existing endsets unchanged |

No operation in the system changes what a link references. What *does* change is which V-space positions correspond to a link's I-addresses. After a REARRANGE, the same I-address may appear at a different V-position. After a DELETE, the I-address may have no V-position at all in that document. But the link has not changed — only the lens through which we view it has changed.

Nelson: "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." The technical content of that clause — "if anything is left at each end" — refers to V-space resolution, not to link integrity. The link itself is always intact; the question is whether its endsets currently resolve to visible V-space positions.

---

## Link Creation

### L3 — MAKELINK Specification

    MAKELINK(d, F, T, Y) → l

where `d` is the home document, `F` the from endset, `T` the to endset, and `Y` the type endset.

    pre:   d ∈ Σ.D ∧ account(d) = actor(op)
         ∧ (A (s, ℓ) ∈ F ∪ T ∪ Y : s ∈ dom(Σ.I) ∪ dom(Σ.L) ∧ ℓ > 0)

    post:
      (a)  l ∉ dom(Σ.L) ∧ l ∈ dom(Σ'.L)
      (b)  home(l) = d
      (c)  Σ'.L(l) = (from: F, to: T, type: Y)
      (d)  l ∈ Σ'.visible(d)

    frame:
      (e)  Σ'.I = Σ.I
      (f)  Σ'.D = Σ.D
      (g)  (A l' ∈ dom(Σ.L) : Σ'.L(l') = Σ.L(l'))
      (h)  (A d' : d' ∈ Σ.D ∧ d' ≠ d : Σ'.V(d') = Σ.V(d'))
      (i)  (A d' ∈ Σ.D : Σ'.pub(d') = Σ.pub(d'))

MAKELINK extends the link store with one new entry and adds the link to the home document's visible set. It modifies no existing links, no I-space content, no other document's V-stream, and no publication states.

The precondition requires that the actor own the home document (D5, OwnershipRights, ASN-0029). There is no requirement that the actor own or have any relationship to the documents whose content the endsets reference. This asymmetry is critical and deliberate: ownership governs *where* a link lives, not *what* it connects.

Note that MAKELINK accepts endsets already expressed as I-spans. In practice, a user specifies V-spans in some document, and the front end converts these to I-spans by consulting the document's V→I mapping. The conversion is well-defined because P2 (ReferentiallyComplete, ASN-0026) guarantees every V-position maps to a valid I-address. The abstract specification concerns itself with the stored I-span form; the V-to-I conversion is a presentation concern.

### L3a — Link Address Allocation

The link I-address is allocated within d's address space:

    d ≼ l ∧ zeros(l) = 3

The link's address is scoped to its home document, just as content I-addresses are scoped to the document that performed the INSERT (D7a, DocumentScopedAllocation, ASN-0026). Sequential links within the same document receive monotonically increasing I-addresses:

    (A l₁, l₂ : home(l₁) = home(l₂) ∧ allocated_before(l₁, l₂) : l₁ < l₂)

per T9 (ForwardAllocation, ASN-0001). The link's creation-order position is permanent and its address is never reused.

---

## Link Discovery

We now develop the specification of link discovery — the operation that, given content, returns all links whose endsets cover any of that content. This is where the I-space-based endset design pays its largest dividend.

### The Discovery Predicate

Define the *overlap* predicate between an endset `E` and a set of I-addresses `Q`:

    overlaps(E, Q)  ≡  covered(E) ∩ Q ≠ ∅

The link discovery function FINDLINKS takes a query set `Q` (derived from a V-spec by converting V-positions to their underlying I-addresses) and an endset selector:

    FINDLINKS(Q, end) = {l ∈ dom(Σ.L) : overlaps(Σ.L(l).end, Q)}

where `end ∈ {from, to, type}` selects which endset to match against.

### L4 — Bidirectional Discovery

For any link `l` with non-empty endsets:

    (A Q ⊆ dom(Σ.I) : Q ∩ covered(Σ.L(l).from) ≠ ∅
        ⟹  l ∈ FINDLINKS(Q, from))

    (A Q ⊆ dom(Σ.I) : Q ∩ covered(Σ.L(l).to) ≠ ∅
        ⟹  l ∈ FINDLINKS(Q, to))

This is immediate from the definition of FINDLINKS. The point is architectural: the function is symmetric in that it queries against any endset. Given content, one can find everything that links *from* it, everything that links *to* it, and everything that has it as a *type*. There is no privileged direction.

Nelson is emphatic: "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?' — and be shown all these outside connections without appreciable delay." The architecture delivers this guarantee because links are indexed by all three endsets. Bidirectionality is not an implementation convenience; it is a structural consequence of the triple-endset design combined with I-address-based indexing.

### L5 — Discovery Completeness

FINDLINKS returns *all* matching links:

    [l ∈ dom(Σ.L) ∧ overlaps(Σ.L(l).end, Q)  ⟹  l ∈ FINDLINKS(Q, end)]

No link that matches the query is omitted. Nelson guarantees this scales: "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS."

### L6 — Discovery Is Content-Identity-Based

FINDLINKS operates on I-addresses, not on document identifiers or V-positions:

    (A d₁, d₂, p₁, p₂ :
        Σ.V(d₁)(p₁) = Σ.V(d₂)(p₂) = a
        ⟹  {l : l ∈ FINDLINKS({a}, end)} is determined solely by a)

If documents `d₁` and `d₂` share content at I-address `a` — through transclusion, versioning, or independent inclusion — the same links are discoverable from both. The discovery index knows about I-addresses, not about which document currently displays them.

This is the property that makes link discovery global. A link created by Carol in her document, connecting content in Alice's document to content in Bob's document, is discoverable by *anyone* reading *any* document that contains the relevant I-addresses. The home document of the link is irrelevant to discoverability; only content identity matters.

### L6a — Discovery Frame

    FINDLINKS(Q, end) :  frame  Σ' = Σ

Discovery is a pure query — it does not modify any state.

---

## Transclusion Propagates Link Discovery

We now derive a consequence that emerges from the composition of links with transclusion. Neither COPY nor MAKELINK was designed "for" the other — they operate on different layers of the system. Yet their interaction produces a property of considerable power.

### L7 — Transclusion Carries Link Discovery

Let COPY place content from document `d_s` at I-addresses `A ⊆ range(Σ.V(d_s))` into document `d_t`, so that:

    (A a ∈ A : a ∈ range(Σ'.V(d_t)))

Then for every link `l` whose endset covers any address in `A`:

    a ∈ A ∧ a ∈ covered(Σ.L(l).end)  ⟹  l ∈ FINDLINKS({a}, end) in state Σ'

Derivation: COPY does not modify I-space (+_ext with `fresh = ∅`, ASN-0026). COPY does not modify existing links (L0). The I-addresses placed in `d_t` are the *same* addresses that were in `d_s` — this is the definition of transclusion. By L6, FINDLINKS is determined by I-address, so the same links are discoverable from the new location.

This is the formal content of the claim that "links follow transclusion." It is not a feature requiring special machinery — it is a theorem derived from endsets (I-space reference), transclusion (I-address sharing), and discovery (I-address overlap). Any alternative implementation satisfying these definitions will exhibit the same behavior.

### L8 — Link Resurrection Through Transclusion

A stronger consequence. Suppose all documents have deleted a particular I-address `a` from their V-streams. The link `l` whose endset covers `a` remains in `dom(Σ.L)` (by L1), and its endset still covers `a` (by L0). The link is merely undiscoverable through normal V-spec queries, because no V-spec resolves to address `a`.

Now suppose a COPY operation places `a` back into some document's V-stream. Immediately, `l` is discoverable again:

    [l ∈ dom(Σ.L) ∧ a ∈ covered(Σ.L(l).end) ∧ a ∈ range(Σ'.V(d))
     ⟹  l ∈ FINDLINKS({a}, end) in state Σ']

regardless of whether `a` was reachable from any V-stream in the preceding state.

The resurrection is precise in a way that confirms it is an intended architectural property, not an accident. Only COPY (transclusion) produces this effect, because only COPY preserves I-addresses. INSERT allocates fresh I-addresses (P9, FreshPositions, ASN-0026). If a user retypes the same text, the new bytes receive new I-addresses that have no relationship to the original link's endset (P4, CreationBasedIdentity, ASN-0026). There is nothing to resurrect because there is no shared identity. The system consistently distinguishes "same content" (same I-addresses, via COPY) from "new content that happens to look the same" (new I-addresses, via INSERT).

---

## Version Transparency

### L9 — Links Are Discoverable From Versions

CREATENEWVERSION(`d_s`, `actor`) creates `d_v` with:

    (A p : 1 ≤ p ≤ |Σ.V(d_s)| : Σ'.V(d_v)(p) = Σ.V(d_s)(p))

per D12(c) (VersionCreation, ASN-0029). The version `d_v` shares all I-addresses with `d_s`. Therefore, by L6:

    (A l ∈ dom(Σ.L), end ∈ {from, to, type} :
        covered(Σ.L(l).end) ∩ range(Σ.V(d_s)) ≠ ∅
        ⟹  covered(Σ.L(l).end) ∩ range(Σ'.V(d_v)) ≠ ∅)

Every link discoverable from `d_s` at the time of versioning is discoverable from `d_v`. Versioning does not copy link records and does not need to — shared I-addresses are sufficient. The link store `Σ.L` is unmodified by versioning (D12(e), `Σ'.I = Σ.I`, and L0).

The converse is also notable: links created *after* versioning, whose endsets cover I-addresses shared by both `d_s` and `d_v`, are discoverable from *both*. The version is not a frozen snapshot of discoverability — it is a live participant in the content-identity web.

This property is asymmetric in an instructive way. A version inherits link *discoverability* (because it shares I-addresses) but not link *ownership* (link records in the source's link subspace are not copied to the version's link subspace). The distinction between "discoverable from" and "owned by" is precisely the distinction between the I-space index (which knows about content identity) and the V-space link subspace (which knows about document membership).

---

## Following Links

### FOLLOWLINK

Given a link and an endset selector, FOLLOWLINK returns the current V-space manifestation of that endset.

    FOLLOWLINK(l, end) → VSpec

The operation converts each I-span in the selected endset to V-positions by consulting the relevant document's V→I mapping. I-addresses that currently have no V-space position are silently omitted.

### L10 — Partial Endset Resolution

Define the *resolvable portion* of an endset `E`:

    resolvable(E) = {a ∈ covered(E) :
        (E d ∈ Σ.D, p : 1 ≤ p ≤ n_d : Σ.V(d)(p) = a)}

This is the set of I-addresses in `E` that are currently mapped to at least one V-position in some document.

FOLLOWLINK returns V-positions corresponding to `resolvable(Σ.L(l).end)`. Three cases are possible:

    |resolvable(E)| = |covered(E)|       full resolution
    0 < |resolvable(E)| < |covered(E)|   partial resolution
    |resolvable(E)| = 0                   empty resolution

All three cases are operationally successful — FOLLOWLINK does not signal incompleteness. The caller cannot distinguish a narrow endset that was always small from a wide endset that has been partially orphaned. This is consistent with the permanence model: V-space is a mutable view over permanent I-space, and the current view is the only view FOLLOWLINK provides.

### L10a — FOLLOWLINK Frame

    FOLLOWLINK(l, end) :  frame  Σ' = Σ

FOLLOWLINK is a pure query.

### On the Absence of an Incompleteness Signal

One might ask whether the system should report that an endset was only partially resolved. Within the Xanadu permanence model, the I-space record is the ground truth — a link's endsets are permanently stored and always retrievable by direct I-address query. V-space resolution is a convenience mapping from I-addresses to current document positions. Reporting incompleteness would require the system to maintain an opinion about the endset's "intended" extent versus its current resolution — introducing mutable metadata about an immutable object.

Applications needing integrity checking must compare the endset's stored I-spans (available from the link record) against the V-space resolution. The system provides both pieces of information; combining them is a presentation concern.

---

## Ownership and Free Linking

### L11 — Link Ownership

The owner of a link is the owner of its home document:

    owner(l) = account(home(l))

This is a structural property of the link's I-address — computable from the tumbler alone, consulting no mutable state (D3, StructuralOwnership, ASN-0029).

### L11a — Owner-Exclusive Link Creation

Only the owner of a document may create links stored in it:

    [op = MAKELINK(d, ...) ⟹ account(d) = actor(op)]

This follows from D5 (OwnershipRights, ASN-0029): only the owner may modify a document's V-stream, and MAKELINK adds a link reference to the home document's V-stream.

### L12 — Independence from Connected Documents

A link's home document need not be either of the documents referenced by its endsets:

    (E l ∈ dom(Σ.L), d_f, d_t :
        home(l) ≠ d_f ∧ home(l) ≠ d_t
      ∧ covered(Σ.L(l).from) ∩ range(Σ.V(d_f)) ≠ ∅
      ∧ covered(Σ.L(l).to)   ∩ range(Σ.V(d_t)) ≠ ∅)

is permitted. Carol may create a link in her own document connecting passages in Alice's document to passages in Bob's document. Neither Alice nor Bob can delete Carol's link — it is Carol's property at Carol's address.

Nelson: "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." This separation of link *residence* from link *application* is the solution to the marginalia problem: how do you annotate someone else's work without modifying it? Your annotations are links that you own, stored at your address, but visible to anyone reading the annotated material. The target author has no veto power over your commentary.

### L13 — Free Linking

Any session may create a link whose endsets reference published content, without permission from the content's author:

    [Σ.pub(d_target) = published
     ∧ (E (s, ℓ) ∈ Σ.L(l).to : (E p : 1 ≤ p ≤ n_{d_target} :
            s ≤ Σ.V(d_target)(p) < s ⊕ ℓ))
     ⟹ no permission from account(d_target) is required]

This is the linking corollary of D11 (PublicationSurrender, ASN-0029). Nelson: "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract."

The only exception is private (unpublished) documents: you cannot link to content you cannot see. This is an access control, not a link permission — the restriction is on *reading*, and link creation requires reading.

### L13a — Incoming Links Are Not Controllable

The author of a published document cannot delete or modify links created by other users:

    [home(l) ≠ d ∧ l ∈ dom(Σ.L)
     ⟹ account(d) has no operation to remove l from dom(Σ.L)]

This follows from L11: only `account(home(l))` controls `l`. The target author's only recourse is to delete the *content* that the link references — which may cause the link to lose V-space resolution (L10) but does not destroy the link or its endset record (L0, L1).

### Out-Links and In-Links

We distinguish two categories of link relationship to a document:

    outlinks(d) = {l ∈ dom(Σ.L) : home(l) = d}

    inlinks(d) = {l ∈ dom(Σ.L) :
        covered(Σ.L(l).to) ∩ range(Σ.V(d)) ≠ ∅
        ∧ home(l) ≠ d}

Out-links are under the owner's control — they live in the owner's document. In-links are not — they live in other users' documents. This asymmetry is the mechanism that enables free linking while preserving ownership integrity: you control what you create, not what others create about you.

---

## Links as Targets

Because links occupy the same I-address space as content, they can appear in endsets:

### L14 — Links as Endset Targets

    (E l₁, l₂ ∈ dom(Σ.L) : l₁ ∈ covered(Σ.L(l₂).to))

is permitted. A link may point to another link.

Nelson: "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link." He gives the mechanism: "The to-set of the link need simply point to the actual link address in the tumbler line, with a span of 1 to designate that unit only."

This enables meta-annotation: a comment link can itself be annotated, endorsed, or disputed by further links. The uniform address space makes no architectural distinction between content addresses and link addresses for endset membership. A link-to-link is simply a link whose endset happens to cover an I-address in the link subspace rather than the text subspace.

---

## Link Deletion: The Three-Layer Model

We have established (L0, L1) that no operation removes a link from the link store or modifies its endsets. Yet Nelson explicitly describes "DELETED LINKS" as a valid document state, and an owner must be able to retract their own links. How is this reconciled?

The resolution lies in the three layers of link existence, which have different mutability properties:

1. **Identity layer** (I-space): the link's permanent I-address and stored endsets. Immutable by L0, L1.
2. **Index layer**: the I-address-to-link mapping used by FINDLINKS. Append-only — entries are added when links are created, never removed.
3. **Presentation layer** (V-space): the link's reference in its home document's V-stream. Mutable.

### L15 — Visibility Is the Mutable Layer

"Deletion" of a link modifies only the presentation layer:

    REMOVELINK(d, l):
      pre:   l ∈ Σ.visible(d) ∧ home(l) = d ∧ account(d) = actor(op)
      post:  l ∉ Σ'.visible(d)
      frame: Σ'.L = Σ.L ∧ Σ'.I = Σ.I ∧ Σ'.D = Σ.D
           ∧ (A d' : d' ≠ d : Σ'.visible(d') = Σ.visible(d'))

The link is removed from the home document's V-stream. It remains in `dom(Σ.L)` with unchanged endsets. It remains indexed. It remains discoverable through FINDLINKS (because the index layer is append-only).

Nelson's description of deleted links — "not currently addressable, awaiting historical backtrack functions, may remain included in other versions" — maps precisely to this three-layer model. "Not currently addressable" means removed from the presentation layer. "Awaiting historical backtrack" means the identity layer preserves the record. "May remain included in other versions" means that if the document was versioned before the link was removed, the version's V-stream still contains the link reference, and `l ∈ Σ.visible(d_version)` remains true.

The three-layer separation also explains a subtlety in deletion semantics. When `l` is removed from `Σ.visible(d)`:

- `l ∈ dom(Σ'.L)` — the link still *exists* (identity layer intact)
- `l ∈ FINDLINKS(Q, end)` for appropriate Q — the link is still *discoverable* (index layer intact)
- `l ∉ Σ'.visible(d)` — the link is no longer *presented* in `d`

This is the formal meaning of a "reverse orphan": a link that exists and is globally discoverable but is not contained in any document's V-stream. The link has not been destroyed; it has merely been removed from display.

---

## Links and Transclusion Are Distinct

### L16 — COPY and MAKELINK Are Independent Operations

COPY (transclusion) is a V-space structural operation: it causes content I-addresses from one document to appear in another document's V-stream. MAKELINK is a link-store creation operation: it allocates a new link object with three endsets. They are performed by different operations and produce different kinds of state change:

    (A op : op = COPY(...) : dom(Σ'.L) = dom(Σ.L))
    (A op : op = MAKELINK(d, F, T, Y) :
        range(Σ'.V(d)) ∖ range(Σ.V(d)) ⊆ {l})

COPY creates no new links. MAKELINK adds only the link's own I-address to the home document's V-stream — no content I-addresses are placed in any document's text subspace.

They compose freely. A *quote-link* is a MAKELINK that marks a prior COPY — Nelson calls it "the author's acknowledgment of material origin." A transclusion without a quote-link is structurally present but not visually marked. A link without a transclusion is a navigable connection that does not include content.

Nelson: "Note that a quote-link is not the same as an inclusion, which is not ordinarily indicated." The inclusion (transclusion) is the structural fact; the quote-link is an optional annotation layered on top. The glass pane metaphor captures it: the clear glass (content showing through from another document) is the transclusion; a quote-link would be a frame painted around that window, telling the reader "you are looking through to another document here."

The formal independence means that transclusion can exist without cluttering the link space, and links can exist without requiring structural inclusion. You can link to a passage without quoting it. You can include a passage without explicitly marking it. The two mechanisms compose because they share the same I-space addressing, but they are orthogonal in what they produce.

---

## The Link Type System

### L17 — Type Endset Is a Content Reference

The type endset of a link is structurally identical to the from and to endsets — it is a set of I-spans referencing content at specific I-addresses. Type identity is content identity: two links have the same type when their type endsets cover the same I-addresses.

The intended mechanism is a designated *type registry document* whose content at specific addresses defines each type. The registry is an ordinary document — not a special data structure — and type definitions are content at I-addresses, not metadata. This means the type system inherits all properties of the content system: permanence, addressability, and uniform access.

### L17a — Type Hierarchy Through Address Containment

Types can be organized hierarchically by tumbler prefix containment. If type FOOTNOTE occupies I-address range `[f, f ⊕ w)` and type MARGIN occupies `[f.x, f.x ⊕ w')` where `f ≼ f.x`, then MARGIN is a subtype of FOOTNOTE. A query for "all footnote-family links" searches the range `[f, f ⊕ w)`, which by T5 (ContiguousSubtrees, ASN-0001) includes all addresses with prefix `f` — capturing both FOOTNOTE and MARGIN.

This is not a new mechanism but a consequence of the tumbler algebra applied to the type address space. The hierarchy is structural, permanent, and requires no special subtype machinery beyond range queries.

The known type vocabulary includes JUMP (navigational), QUOTE (marks a transclusion), FOOTNOTE (reference mark to annotation), and MARGIN (a subtype of FOOTNOTE for marginal annotations). The vocabulary is extensible: creating a new type means inserting content at a new address in the type registry.

---

## Multi-Document Endsets

### L18 — Endsets May Span Multiple Documents

A single endset may contain I-addresses originating from different documents:

    (E l ∈ dom(Σ.L), E = Σ.L(l).from, d₁ ≠ d₂ :
        (E a₁ ∈ covered(E) : home(a₁) = d₁)
      ∧ (E a₂ ∈ covered(E) : home(a₂) = d₂))

is permitted. This arises naturally when a link is created over a passage of composite content — text that includes transcluded material from multiple sources. The V-to-I conversion at link creation time decomposes the V-span into its constituent I-spans, which may belong to different document origins.

The semantic is that the link asserts a relationship across the composite selection as a whole, binding to the union of all constituent content identities regardless of their provenance. Each I-span in the endset independently tracks its source, and partial survival (L10) applies per-I-span: if one source document's content is deleted, the endset retains the I-spans from other sources.

---

## Internal Links

### L19 — Same-Document Links

A link whose from and to endsets both reference content in the same document is permitted:

    (E l ∈ dom(Σ.L), d :
        covered(Σ.L(l).from) ∩ range(Σ.V(d)) ≠ ∅
      ∧ covered(Σ.L(l).to)   ∩ range(Σ.V(d)) ≠ ∅
      ∧ home(l) = d)

is a valid configuration. The specifications of MAKELINK (L3), FOLLOWLINK (L10), and FINDLINKS (L4–L6) make no distinction between same-document and cross-document links. These operations are defined over I-addresses, which carry no same-document/cross-document semantics.

Internal links serve standard literary functions: footnote marks connected to footnote text, glossary terms connected to definitions, intra-document cross-references. These are not a separate category requiring special treatment — they are the same mechanism applied within a single document.

---

## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| Σ.L | `Σ.L : IAddr ⇀ LinkRecord` — partial function from link I-addresses to link records | introduced |
| Σ.visible | `Σ.visible : DocId → P_fin(dom(Σ.L))` — which links appear in each document's V-stream | introduced |
| Endset | `Endset = P_fin({(s, ℓ) : s ∈ dom(Σ.I) ∪ dom(Σ.L), ℓ > 0})` — finite set of I-spans | introduced |
| covered(E) | `covered(E) = ∪{[s, s⊕ℓ) : (s,ℓ) ∈ E}` — the I-addresses an endset references | introduced |
| overlaps(E,Q) | `overlaps(E, Q) ≡ covered(E) ∩ Q ≠ ∅` — endset-query overlap predicate | introduced |
| outlinks(d) | `{l ∈ dom(Σ.L) : home(l) = d}` — links owned by document d | introduced |
| inlinks(d) | `{l ∈ dom(Σ.L) : covered(Σ.L(l).to) ∩ range(Σ.V(d)) ≠ ∅ ∧ home(l) ≠ d}` — incoming links to d | introduced |
| L0 | Link records are immutable: `l ∈ dom(Σ.L) ⟹ Σ'.L(l) = Σ.L(l)` | introduced |
| L1 | Link set is monotone: `l ∈ dom(Σ.L) ⟹ l ∈ dom(Σ'.L)` | introduced |
| L2 | Endsets are stable under all operations: `covered(Σ'.L(l).E) = covered(Σ.L(l).E)` | introduced |
| L3 | MAKELINK creates a link with permanent I-address, three endsets, home document | introduced |
| L3a | Link I-addresses are allocated within the home document's address space | introduced |
| L4 | Bidirectional discovery: links findable from both from-end and to-end queries | introduced |
| L5 | Discovery completeness: FINDLINKS returns all matching links | introduced |
| L6 | Discovery is content-identity-based: same I-address yields same results regardless of querying document | introduced |
| L6a | FINDLINKS frame: pure query, no state modification | introduced |
| L7 | Transclusion propagates link discovery through shared I-addresses | introduced |
| L8 | Link resurrection: orphaned links become discoverable when I-addresses reappear via COPY | introduced |
| L9 | Version transparency: links discoverable from versions through shared I-addresses | introduced |
| L10 | Partial endset resolution: FOLLOWLINK silently omits unresolvable I-addresses | introduced |
| L10a | FOLLOWLINK frame: pure query, no state modification | introduced |
| L11 | Link ownership: `owner(l) = account(home(l))` | introduced |
| L11a | Owner-exclusive link creation: only home document owner may create links in it | introduced |
| L12 | Link home document is independent of connected documents | introduced |
| L13 | Free linking: any session may link to published content without permission | introduced |
| L13a | Incoming links are not controllable by target author | introduced |
| L14 | Links may be endset targets: links can point to other links | introduced |
| L15 | Visibility is the mutable layer: "deletion" modifies only V-space presentation | introduced |
| L16 | COPY and MAKELINK are independent operations | introduced |
| L17 | Type endset is a content reference in the type registry document | introduced |
| L17a | Type hierarchy via tumbler address containment | introduced |
| L18 | Endsets may span I-addresses from multiple documents | introduced |
| L19 | Same-document links use the same mechanism as cross-document links | introduced |

## Open Questions

What must the type registry guarantee about the permanence and availability of type definitions — must the registry document be published, and what happens when a type address has no stored content?

Must the system provide a mechanism to distinguish full endset resolution from partial resolution, or is silent filtering the only contract?

What invariants must FINDLINKS satisfy regarding result ordering — is any ordering of the returned link set guaranteed, or only set membership?

When a link targets another link (L14), must FOLLOWLINK on the target endset resolve to the targeted link's home-document V-position, or to some other representation of the link object?

Must the system bound the cost of FINDLINKS in the number of matching links, or may response time be proportional to the total link population?

What must a link sieving (filtering) mechanism guarantee about the composability of filter predicates — must filters over FINDLINKS results compose conjunctively, and must the system provide standard filter dimensions (time, location, author)?

Under what conditions, if any, may the extraordinary withdrawal process (D11, ASN-0029) remove a published document whose content is covered by other users' link endsets?

Must FOLLOWLINK return V-positions in document reading order, or may the order reflect I-space allocation order?

What must the system preserve about a link's visibility state across version creation — does the new version inherit the source's `Σ.visible` set?

Can two distinct links have identical endsets (same from, to, and type), and if so, must the system provide a means to distinguish them beyond their I-addresses?

Must the three-endset structure (from, to, type) be fixed, or may future link kinds require additional or fewer endsets — and what must the system guarantee about endset count?
