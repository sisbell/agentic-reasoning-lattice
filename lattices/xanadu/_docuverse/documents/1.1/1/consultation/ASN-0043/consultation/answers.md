# Consultation Answers — Link Ontology

**Inquiry:** What is a link on the tumbler line? What structure must a connection between arbitrary spans of tumbler addresses have, and what properties must hold about those connections?
**Date:** 2026-03-16 20:58
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> What is the minimum structure of a link — what components must every connection between arbitrary spans of content contain?

### Nelson's Answer

# The Minimum Structure of a Link

Every Xanadu link contains exactly **four** structural components: a **home**, and **three endsets**.

## The Home

A link must reside somewhere. Its **home document** gives it a tumbler address and determines who owns it:

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user. It is put in by a user (or a front end), and thereafter maintained by the back end through the back end's inter-indexing mechanisms." [LM 4/41]

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

The home is not optional. Without it, the link has no address, no owner, and no place in the docuverse.

## The Three Endsets

Every link has three endsets, treated symmetrically:

| Endset | Also Called | Role |
|--------|------------|------|
| **From-set** | first endset | The bytes the link is "from" |
| **To-set** | second endset, 2-set | The bytes the link is "to" |
| **Type** | three-set, 3-set | Categorizes the connection |

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." [LM 4/43]

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." [LM 4/44]

The MAKELINK operation confirms this is the complete set:

> "This creates a link in document \<doc id\> from \<from set\> to \<to set\> connected to \<three set\>. It returns the id of the link made." [LM 4/68]

Four parameters: home document, from-set, to-set, type. Nothing else.

## What Each Endset IS

Each endset is an **arbitrary span-set** — not a single point, not a single span, but potentially multiple discontiguous regions of bytes scattered across the entire docuverse:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." [LM 4/42]

This generality is fundamental. A link does not connect "page A to page B" or even "passage A to passage B." It connects an arbitrary collection of byte-spans to another arbitrary collection of byte-spans, categorized by a third arbitrary collection of byte-spans.

## Why the Type Endset Is Not Optional

The type is structurally identical to from and to — it is an endset pointing anywhere. But its role is semantic classification, and it has a crucial property: **search matches on address, not content**.

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." [LM 4/44-4/45]

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [LM 4/45]

A link with no type would be unsearchable by kind — you could not ask "find all citations" or "find all comments." The type endset may point to a ghost address where nothing is stored, but it must point somewhere.

## The Degenerate Case: One-Sided Links

There is one acknowledged variation — the **one-sided link**, where only one content endset is populated:

> "Unfortunate terminological problem: since it has only one side, we use the first endset to designate the matter pointed at. To call this 'from' is inane." [LM 4/48]

Paragraph designators and heading links are examples. But even these still have a home and a type — they are structurally three-endset links where one content endset happens to be empty.

## Summary

The minimum link structure is:

1. **Home** — a tumbler address in a document (establishes ownership and identity)
2. **From-set** — an arbitrary span-set (the source side of the connection)
3. **To-set** — an arbitrary span-set (the target side of the connection)
4. **Type** — an arbitrary span-set (the semantic classification, matched by address)

Nothing less is a link. Nothing more is required. The entire link mechanism — the universal system of retrieval "quite unlike any other in the world" [LM 4/41] — is built from this single four-part primitive.

---

## Question 2 [nelson]

> Must a link distinguish a "from" endpoint and a "to" endpoint, or are the endpoints of a connection symmetric and unordered?

### Nelson's Answer

## Links Are Ordered but Semantically Flexible

The short answer: **links structurally distinguish a from-set and a to-set** (the endpoints are ordered), but the **meaning of that ordering is user-defined and type-dependent**, and Nelson explicitly acknowledges that directionality is not universal.

### The Key Quote

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" [LM 4/42]

Three things packed into that sentence:

1. **"Typically"** — not always. Some links may not have meaningful directionality.
2. **From-set and to-set are structurally distinct** — they are separate endsets, stored and searched independently.
3. **"Depend on the specific case"** — the system provides the slot distinction; the link type gives it meaning.

### Structural Ordering

The protocol treats from and to as separate parameters. MAKELINK takes them distinctly:

> "This creates a link in document \<doc id\> from \<from set\> to \<to set\> connected to \<three set\>." [LM 4/68]

And search distinguishes them:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

So the system knows which endset is "first" and which is "second." This ordering is real — it's baked into the protocol.

### But Directionality Is Semantic, Not Structural

A citation link goes *from* citing text *to* source. A comment link goes *from* commentary *to* subject. A counterpart link connects equivalents — where directionality may be meaningless. The system provides the two slots; the link type defines whether the ordering carries semantic weight.

### The One-Sided Case Reveals the Design

Nelson's treatment of one-sided links is telling:

> "Unfortunate terminological problem: since it has only one side, we use the first endset to designate the matter pointed at. To call this 'from' is inane." [LM 4/48]

He calls his own "from" label **inane** in this case. The label is a convention, not a deep structural commitment. The real structure is: a link has a first endset, a second endset, and a type endset — three ordered slots.

### Bidirectional Discovery Regardless

Even though from and to are distinguished structurally, **the system indexes both directions**. You can search for links *from* a span, *to* a span, or by type — from any direction. The ordering doesn't create a one-way gate.

### Summary

| Aspect | Answer |
|--------|--------|
| Are endpoints structurally distinct? | **Yes** — first endset vs. second endset, separate in protocol |
| Must they be semantically directional? | **No** — "typically directional," depends on link type |
| Who defines the meaning of from/to? | **The link type** — user-defined, open-ended |
| Can you search from either end? | **Yes** — bidirectional indexing on all three endsets |
| Are there non-directional links? | **Implied yes** — counterpart links mark equivalence; one-sided links use only one endset |

The design is: **ordered slots with user-defined semantics**. The system provides two distinguished positions; whether that distinction carries directional meaning is a property of the link type, not of the link mechanism itself.

---

## Question 3 [nelson]

> Can a single link connect more than two spans of content, or is every link strictly a pair of endpoints?

### Nelson's Answer

# A Single Link Connects Three Sets, Each Containing Arbitrary Spans

A Xanadu link is emphatically **not** a pair of endpoints. Every link has **three endsets** — from-set, to-set, and type — and each endset can itself be an **arbitrary collection of multiple discontiguous spans** scattered anywhere in the docuverse.

## Three Endsets, Not Two

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" [LM 4/42]

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." [LM 4/44]

The type (the "three-set") is not metadata bolted onto a binary connection — it is a full endset with the same power and structure as from and to.

## Each Endset Is a Set of Spans

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." [LM 4/43]

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." [LM 4/42]

Even the type endset can be multi-valued:

> "Note that a link's type--the three-set--may be several pointers." [LM 4/44]

## Concrete Example

A single critique link might have:

- **From-set**: three non-adjacent passages in the critic's essay (the arguments)
- **To-set**: two passages in different documents being criticized
- **Type**: a span pointing to the "critique" type address

That is one link connecting **five** separate spans of content across multiple documents, plus a type designation — all in a single connective unit.

## Beyond Three: Compound Links

For structures requiring even more complexity, Nelson describes **compound links** built from link-to-link chains:

> "Complex relational structures, such as the faceted link (discussed in Chapter 2), may be constructed with links to links. These use the two-sided link structure much like the CONS cell in LISP, and may be built into arbitrary compound links." [LM 4/51]

Just as LISP builds arbitrarily complex structures from pairs, Xanadu builds arbitrarily complex relational structures from three-endset links pointing to other links.

## Summary

Every link is a **three-way** connection (from, to, type), and each of those three ways can touch **multiple discontiguous spans** across the entire docuverse. The common mental model of a link as "a line between two points" is a severe understatement of what I designed. A Xanadu link is a typed strap binding arbitrary collections of bytes — a far more powerful primitive than the point-to-point links the web settled for.

---

## Question 4 [nelson]

> Must each endpoint of a link identify a specific contiguous span of content, or may an endpoint designate a non-contiguous selection or an entire document?

### Nelson's Answer

## An Endset Is an Arbitrary Span-Set, Not a Single Span

Each endpoint of a link — the from-set, the to-set, and the type (three-set) — may be a **non-contiguous collection of spans pointing anywhere in the docuverse**. A single contiguous span is merely the degenerate case.

Nelson is explicit on this point:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." [LM 4/42]

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." [LM 4/43]

The three endsets are treated symmetrically — all three follow the same convention. The type endset gets the same power as from and to.

## Entire Documents (and Larger Units) Are Valid Targets

An endset can also designate an entire document, an entire account, a server node, or even the whole docuverse. This works through the tumbler span mechanism:

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server — or the entire docuverse." [LM 4/38]

> "In fact, a tumbler-span may range in possible size from one byte to the whole docuverse on the whole network." [LM 4/24]

This applies even when nothing is physically stored at the target address (the "ghost element" case):

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

> "A link to or search of an account or node will find any of the documents under it." [LM 4/23]

## Summary

| Question | Answer |
|----------|--------|
| Must an endset be a single contiguous span? | **No.** It is an arbitrary collection of spans. |
| Can an endset be discontiguous? | **Yes.** "A broken, discontiguous set of bytes." |
| Can spans in one endset touch different documents? | **Yes.** "Anywhere in the docuverse." |
| Can an endset designate a whole document? | **Yes.** A single span covering the document's full range. |
| Can an endset designate something larger than a document? | **Yes.** Accounts, servers, the entire docuverse. |
| Are all three endsets treated the same way? | **Yes.** "We adopt the same convention for link types." |

---

## Question 5 [nelson]

> Does a link have its own unique, permanent identity within the system, distinct from the identities of the content it connects?

### Nelson's Answer

## Yes — Links Are First-Class Addressable Objects

A link has its own unique, permanent tumbler address in the docuverse, completely distinct from the addresses of the content its endsets connect. This is not an incidental property but a foundational architectural decision.

### The Link's Own Address

Links occupy the **2.x subspace** within their home document and are addressed by permanent creation order:

```
N.0.U.0.D.V.0.2.1      → first link created in this document
N.0.U.0.D.V.0.2.755    → 755th link created in this document
```

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" [LM 4/31]

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

This address is permanent. Deleting link 2.5 does not renumber 2.6 through 2.N.

### Links Are Stored Entities, Not Metadata

Of everything in the docuverse, only two kinds of entities are actually stored in tumbler-space — and links are one of them:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links." [LM 4/23]

Servers, accounts, and documents are "ghost elements" — conceptual positions with no stored representation. Links, by contrast, are concrete objects with real storage.

### The Link's Identity Is Separate from What It Connects

The Tumbler Square visualization [LM 4/46-4/47] makes the separation explicit. A link sits at its **home** position on the tumbler line, and its three endsets (from-set, to-set, type) **reach out** to other positions:

> "A link's home (any home) is an element located on one side; and its three endsets map to the other sides." [LM 4/46]

The link's address encodes **where it lives and who owns it**. The endsets encode **what it connects**. These are independent.

### Why This Matters: Links Can Be Linked To

Because links have their own addresses, other links can point at them — no special mechanism required:

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link (or, indeed, to point at several)." [LM 4/49]

> "The to-set of the link need simply point to the actual link address in the tumbler line, with a span of 1 to designate that unit only." [LM 4/49]

If links did not have their own distinct addresses, link-to-link would be impossible.

### Why This Matters: Ownership

The link's home address determines its owner — not what it points to:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

This separation of identity from reference is what makes it possible for you to annotate someone else's document without modifying it. Your link lives at your address, under your control, even though its endsets reach into their content.

### Summary

A Xanadu link is a **connective unit** [LM 4/41] with:
- Its own permanent tumbler address (identity)
- Its own home document (determines ownership)
- Three endsets that reach into the docuverse (what it connects)

The link's identity, the content it connects, and the content at its type address are three fully independent things unified by one object.

---

## Question 6 [nelson]

> Is a link itself a piece of content — something that can be addressed, quoted, and linked to in turn — or is it a separate category of object outside the content space?

### Nelson's Answer

## Links Are First-Class Objects in the Same Address Space as Content

The answer is **both**: a link is a stored, addressable object in tumbler-space — fully capable of being linked to in turn — but it is architecturally **distinct** from content bytes. Nelson designs links as a separate category of element that nonetheless shares the universal address space.

### Links Live in Tumbler-Space Alongside Bytes

The two types of entity actually stored in the docuverse are bytes and links, and nothing else:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents--bytes and links." [LM 4/23]

Links have their own tumbler addresses within each document, occupying the `2.x` subspace:

```
N.0.U.0.D.V.0.2.1    → first link in document
N.0.U.0.D.V.0.2.755  → 755th link in document
```

While content bytes occupy the `1.x` subspace. This subspace distinction is structural — links and bytes are different *kinds* of element sharing one address space, not different spaces entirely.

### Links Can Be Linked To

Because links have addresses on the tumbler line, they can be targets of other links. Nelson is explicit that this requires no special mechanism:

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link (or, indeed, to point at several)." [LM 4/49]

> "The to-set of the link need simply point to the actual link address in the tumbler line, with a span of 1 to designate that unit only." [LM 4/49]

This is not a special "meta-link" feature. It falls out of the uniform addressing: if you can point at an address, and links have addresses, then you can point at links. From this primitive, Nelson derives compound structures:

> "Complex relational structures, such as the faceted link, may be constructed with links to links. These use the two-sided link structure much like the CONS cell in LISP, and may be built into arbitrary compound links." [LM 4/51]

### But Links Are Not Ordinary Content

Nelson calls links "meta-virtual structures" — they are *about* content rather than *being* content in the way bytes are:

> "The Xanadu link is a meta-virtual structure connecting parts of documents (which are themselves virtual structures)." [LM 4/41]

Key differences from content bytes:

1. **Separate subspace.** Bytes are in `1.x`, links in `2.x`. The system distinguishes them structurally.

2. **Permanent order of arrival.** Unlike bytes (which can be rearranged in V-space), links keep their creation-order addresses permanently: "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

3. **Three-part internal structure.** Bytes are raw content. Links have structured internals: from-set, to-set, and type — each an arbitrary span-set pointing into the docuverse.

4. **Owned independently of what they connect.** "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

### The Architecture's Answer

Nelson's design resolves the question by refusing the dichotomy. Links are not "content" in the sense of being undifferentiated bytes in the permascroll. But they are not "outside the content space" either — they are fully within tumbler-space, fully addressable, fully linkable-to. The system has exactly two kinds of stored element (bytes and links), both first-class, both permanent, both addressable through the same tumbler mechanism.

The docuverse is built from these two primitives and nothing else:

> "The link mechanism ties together the whole corpus of materials on the Xanadu system. There is essentially nothing in the Xanadu system except documents and their arbitrary links." [LM 4/41]

So: a link is an addressable, ownable, linkable-to object that shares the universal address space with content — but is structurally and semantically distinct from content bytes. It is a **peer** of content in the address space, not a subordinate of it, and not external to it.

---

## Question 7 [nelson]

> Must the system support typed links — connections that carry a declared kind or role such as "comment," "quotation," or "correction" — or are all links structurally uniform?

### Nelson's Answer

# Typed Links Are Structurally Required

Every Xanadu link has **three endsets**, not two. The third endset — the "three-set" or "3-set" — IS the type. It is not optional metadata bolted onto a uniform two-ended link; it is a structural component of every link in the system.

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." [LM 4/44]

The three endsets are:

| Endset | Purpose |
|--------|---------|
| **From-set** | The bytes the link is "from" |
| **To-set** | The bytes the link is "to" |
| **Type (three-set)** | Categorizes the link |

The MAKELINK operation requires all three:

> "This creates a link in document \<doc id\> from \<from set\> to \<to set\> connected to \<three set\>." [LM 4/68]

## The Mechanism Is Deliberately Open-Ended

The type system is not a fixed enumeration. It is extensible by any user without system changes:

> "Links are meant to be extensible for the arbitrary needs of any user. Thus the set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose." [LM 4/43]

The crucial design insight: types are matched by **address**, not by content. The search mechanism never inspects what is stored at the type address — it only checks whether the address matches:

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." [LM 4/44-4/45]

This means type addresses need not point to anything at all:

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [LM 4/45]

## Why Three and Not Two

Two endsets establish WHAT is connected. The third establishes WHAT KIND of connection it is. Without the type endset, you cannot distinguish a citation from a comment from a refutation. You cannot search for "all citations" without also retrieving every comment and footnote. You need system schema changes to add new link meanings.

The link search operation FINDLINKSFROMTOTHREE constrains on all three endsets simultaneously:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

And the system guarantees that irrelevant types do not impede search:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

## Standard Types Proposed

I proposed a provisional set of standard types [LM 4/52-4/55], including connection, comment, counterpart, quote-link, citation, supersession, mail, heading, paragraph, footnote, and suggested-threading links. But I was explicit that this was provisional, not canonical:

> "Standardization of a working set of link types is now a high priority, but has less priority than establishing a robust demonstration rig." [LM 4/52]

The type mechanism also supports **hierarchical types** through link-to-link:

> "Note that this mechanism can be used for hierarchical link types, subtypes and supertypes. It is searchable for upper- and under-links, and all final data matter below." [LM 4/51]

## Summary

Links are **not** structurally uniform. Every link carries a type as its third endset, on equal footing with from-set and to-set. The type system is open-ended, address-matched, and user-extensible — but it is structurally present in every link. A link without a type endset is not a Xanadu link.

---

## Question 8 [nelson]

> Must two links that connect the same two spans of content be distinguishable as separate objects, or does the system treat identical connections as a single link?

### Nelson's Answer

## Two Links, Same Spans: Always Distinct Objects

Yes, two links connecting the same spans are always distinguishable as separate objects. The architecture makes this unavoidable — and intentional.

### Every link gets a unique address

Links occupy the `0.2.N` subspace of their home document, addressed sequentially by creation order:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" [LM 4/31]

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

Each call to MAKELINK produces a new link with a new sequential address:

> "This creates a link in document \<doc id\> from \<from set\> to \<to set\> connected to \<three set\>. It returns the id of the link made." [LM 4/68]

There is no "find-or-create" — MAKELINK always creates and always returns a fresh ID.

### Identity comes from home address, not endsets

A link's identity is its tumbler address, not what it connects:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

Two links with identical from-sets, to-sets, and type endsets are still distinct objects if they have different home addresses. Even two links in the *same* home document with identical endsets would get different sequential positions (`0.2.5` vs `0.2.6`).

### Link search returns all matches

FINDLINKSFROMTOTHREE returns "a list of all links" satisfying the search criteria [LM 4/69]. If two identical-endset links exist, both appear in results. There is no collapsing.

### Why this matters

Each link is an independent assertion of connection, owned by its creator:

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user." [LM 4/41]

If Alice and Bob both create a comment link from paragraph P to annotation Q, those are two separate owned objects — different home documents, different owners, independently deletable, independently targetable by link-to-link. Merging them would violate ownership semantics.

Even if the *same* user creates two links with identical endsets (perhaps with different type endsets, or even the same type), they remain distinct. Nothing in the specification suggests deduplication, uniqueness constraints, or identity-by-endset. The system is explicitly designed for open-ended, unrestricted link creation — the only constraint is ownership of the home document.

---

## Question 9 [nelson]

> Can a link connect two spans within the same document, or must a connection always cross a document boundary?

### Nelson's Answer

## Yes — Links Can Connect Spans Within the Same Document

Nelson explicitly contemplates intra-document links. The clearest evidence is this statement:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. **Conversely, links connecting parts of a document need not reside in that document.**" [LM 4/12]

The phrase "links connecting parts of a document" (singular) directly acknowledges links whose from-set and to-set both point within the same document. The sentence then adds that such links don't even need to *reside* in that document — they could live in a different document entirely.

### The Architecture Imposes No Boundary Requirement

Endsets point to arbitrary spans "anywhere in the docuverse":

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse." [LM 4/43]

"Anywhere" includes within the home document, within a different single document, or spanning multiple documents. The link mechanism is agnostic about document boundaries — it operates on byte addresses in tumbler-space, not on document containers.

### Standard Link Types That Are Explicitly Intra-Document

Several of the proposed standard link types only make sense within a single document:

| Type | Purpose |
|------|---------|
| **Heading Link** | "Internal heading or subtitle within document" [LM 4/53] |
| **Paragraph Link** | "Points front end to a paragraph for navigation" [LM 4/53] |
| **Footnote Link** | "Provides a break sequence for an author" [LM 4/53] |

These are structural markers — a heading link connects a title span to the section it names, all within the same document.

### Three Independent Concepts: Home, From, To

The MAKELINK operation makes the independence explicit:

> "The document must be specified because that determines the actual residence of the link — since a document may contain a link between two other documents." [LM 4/63]

The home document (ownership), the from-set targets, and the to-set targets are three independent concerns. All three can be the same document, all different, or any combination. The system doesn't distinguish these cases architecturally.

### Summary

Links are connections between byte-spans in tumbler-space. Document boundaries are organizational, not structural barriers. A link from paragraph 3 to paragraph 7 of the same document works identically to a link from your document to mine — same mechanism, same endset conventions, same search operations.

---

## Question 10 [nelson]

> Must a single endpoint be confined to content within one document, or may one endpoint of a link span content across multiple documents?

### Nelson's Answer

## A single endset MAY span content across multiple documents.

Nelson is explicit and unambiguous on this point. Each endset is an **arbitrary collection of spans** that can reference bytes scattered across the entire docuverse — including bytes in different documents.

### Direct evidence

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. **These may be anywhere in the docuverse.**"
> — [LM 4/42]

> "The from-set may be an arbitrary collection of spans, **pointing anywhere in the docuverse**. Similarly, the to-set may be an arbitrary collection of spans **pointing anywhere in the docuverse**. We adopt the same convention for link types."
> — [LM 4/43]

> "**ENDSETS MAY POINT TO SPANS ANYWHERE IN THE DOCUVERSE**"
> — [LM 4/45], diagram caption

### Why this works

Endsets are span-sets, and spans are pairs of tumbler addresses. Since tumbler addresses form a single universal address space covering all servers, accounts, and documents, a span-set can naturally include spans from document A, document B, and document C — all in a single endset.

From the spans concept: a span-set is "a series of spans" used to "designate a separated series of items exactly, including nothing else" [LM 4/25]. There is no constraint limiting those spans to one document.

### The design intent

This generality is deliberate. Nelson designed endsets to be maximally flexible — a link's from-set might touch three separate passages in three different works because the idea being connected genuinely spans those locations. Restricting an endset to a single document would undermine the vision of links as connections across the entire web of literature.

The MAKELINK operation accepts `<from set>` and `<to set>` as sets, not as single document-local positions [LM 4/68]. The link's home document determines **ownership**, not the scope of what it can connect:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to."
> — [LM 4/12]

---

## Question 11 [gregory]

> A link orgl stores three endsets (source, target, type) each containing I-address spans — is the three-endset structure the minimum necessary representation, or was it designed to be extensible to N endsets, and if so, what constrains it to exactly three?

### Gregory's Answer

## KB Synthesis

The three-endset structure is fixed by implementation — not a minimum viable design, but also not designed for N-extensibility. Three specific constraints enforce it.

## What the KB Shows

**The V-subspace encoding is hardcoded to exactly three values.**

`setlinkvsas()` in `do2.c:169-183` constructs link orgl V-addresses by incrementing mantissa[0] to the values 1, 2, and 3 for the FROM, TO, and THREE endpoints respectively [SS-SUBSPACE-CONVENTION Finding 0038]. This is a table of three, not a loop over N. The subspace convention then propagates through the entire stack:

- Internal POOM storage: text at `1.x`, link orgl refs at `2.x`, type endpoints at `3.x`
- Spanfilade indexing constants: `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3` [SS-RETRIEVE-ENDSETS]
- Link orgl extraction: `link2sporglset()` accepts endset position 1, 2, or 3 [SS-FOLLOWLINK Finding 0048]

**The protocol opcodes assume exactly three parameters.**

`FINDLINKSFROMTOTHREE`, `FINDNUMOFLINKSFROMTOTHREE`, and `RETRIEVEENDSETS` all take three endpoint specsets as separate parameters [SS-FIND-LINKS Finding 0035]. There is no variable-arity endset query.

## Why Three, Not Two

Two endsets (source + target) would be the structural minimum for a link. The third endset exists because **types are content references, not metadata**. Types are VSpecs into a type registry in the bootstrap document (`1.0.2.x`), with a hierarchy encoded in tumbler containment — `1.0.2.6.2` (MARGIN) nests under `1.0.2.6` (FOOTNOTE) [SS-LINK-ENDPOINT Finding 0024]. Storing types as content identity rather than enum flags means type queries can use the same I-address intersection mechanism as source/target discovery. This is architecturally consistent but requires a dedicated endset slot.

## Why Not Four

Nothing in the KB generalizes over N endsets. The tumbler hierarchy could theoretically accommodate digits 4, 5, etc. — nothing about tumbler arithmetic prevents it — but no code path loops or parameterizes over endset count. The naming "THREE" rather than "TYPE" in function names like `findlinksfromtothreesp` is telling: the third slot was conceptualized as "the third argument" rather than "the semantic type field," suggesting the designers might have intended it as a general-purpose third position rather than a locked-in type semantic. But the implementation wires all three slots at the V-subspace encoding level, making the count structurally three.

## Summary

Three is not minimum (two would suffice for bare source-target links) and not extensible (no N-endset generalization exists). It is a fixed architectural commitment: two semantic roles (source, target) plus one general-purpose third slot used for type classification, all wired into the V-subspace digit convention at `setlinkvsas()` and propagated rigidly through the spanfilade indexing and FEBE protocol.

---

## Code Exploration

I have everything needed. Here is the full answer.

---

## The Link Orgl Three-Endset Structure: Minimum Necessary or Extensible to N?

### Short Answer

The three-endset structure is **neither the minimum necessary nor designed for genuine N-way extensibility**. It was designed to stop at three, but incrementally — first two endsets, then a third added later. The implementation is fixed-arity throughout, and a concrete integer-collision barrier prevents a fourth endset without renumbering.

---

### Evidence 1: Two-endset `domakelink` predates `docreatelink`

`do1.c:169-193` contains a function `domakelink` that takes only `fromspecset` and `tospecset`:

```c
bool domakelink(typetask *taskptr, typeisa *docisaptr,
                typespecset fromspecset, typespecset tospecset,
                typeisa *linkisaptr)
```

It calls `setlinkvsas` with `NULL` for the third VSA, and `insertendsetsinorgl`/`insertendsetsinspanf` with `NULL, NULL` for the third endset pair:

```c
  && setlinkvsas (&fromvsa, &tovsa, NULL)                                         // do1.c:189
  && insertendsetsinorgl (... &fromvsa, fromsporglset, &tovsa, tosporglset, NULL, NULL) // do1.c:190
  && insertendsetsinspanf (... fromsporglset, tosporglset, NULL)                   // do1.c:191
```

The public `docreatelink` (`do1.c:195-221`) adds a third endset:

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
                  typespecset fromspecset, typespecset tospecset,
                  typespecset threespecset, typeisa *linkisaptr)
```

`domakelink` has no corresponding request code in `requests.h` — it is internal only. The public wire protocol exposes only `CREATELINK=27` which always passes three specsets. This means the codebase preserves the two-endset form as a relic of incremental design, but clients only ever see three.

---

### Evidence 2: The third endset is optional throughout — from and to are the mandatory minimum

`insertendsetsinspanf` (`do2.c:116-128`) makes the from+to pair mandatory and the third conditional:

```c
bool insertendsetsinspanf(..., typesporglset fromsporglset,
                               typesporglset tosporglset,
                               typesporglset threesporglset)
{
  if (!(insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)
      &&insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN)))
        return (FALSE);
  if (threesporglset) {                                           // do2.c:122 — conditional
    if(!insertspanf(taskptr,spanfptr,linkisaptr,threesporglset,LINKTHREESPAN)){
        return (FALSE);
    }
  }
  return(TRUE);
}
```

`insertendsetsinorgl` (`do2.c:130-149`) has the same structure:

```c
  if (threevsa && threesporglset) {                              // do2.c:136 — conditional
        if (!insertpm (taskptr, linkisaptr, link, threevsa, threesporglset))
```

The minimum required for a valid link is two endsets. Three is the current maximum.

---

### Evidence 3: `setlinkvsas` assigns mechanically regular but fixed VSA positions

`do2.c:169-183` assigns V-stream addresses within the link's own orgl:

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear (fromvsaptr);
    tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);   // 1.1
    tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);
    tumblerclear (tovsaptr);
    tumblerincrement (tovsaptr, 0, 2, tovsaptr);       // 2.1
    tumblerincrement (tovsaptr, 1, 1, tovsaptr);
    if (threevsaptr) {
        tumblerclear (threevsaptr);
        tumblerincrement (threevsaptr, 0, 3, threevsaptr);  // 3.1
        tumblerincrement (threevsaptr, 1, 1, threevsaptr);
    }
    return (TRUE);
}
```

The pattern `N.1` is mechanically regular — a fourth endset would naturally occupy `4.1`. The code checks `if (threevsaptr)` (do2.c:177), meaning the third is genuinely optional and was added as a generalization of the two-endset form. But nothing implements `4.1`.

---

### Evidence 4: The spanfilade integer namespace — `DOCISPAN=4` is the collision barrier

`xanadu.h:36-39` defines the four span type constants:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

The spanfilade uses these integers as the leading component of the key for each link record. A fourth link endset type would naturally want `4`, but `DOCISPAN=4` is already allocated to document content spans. This is the **hard structural barrier**: without renaming DOCISPAN (and changing its storage format throughout), there is no free integer for a fourth endset type in the spanfilade key space.

---

### Evidence 5: All query functions are fixed-arity at three

`spanf1.c:56-103`, `fns.c:189-234`, `do1.c:348-367` all encode three-endset queries end-to-end:

- `findlinksfromtothreesp(taskptr, spanfptr, fromvspecset, tovspecset, threevspecset, ...)` — `spanf1.c:56`
- `intersectlinksets(taskptr, linkset1, linkset2, linkset3, *linkset4ptr)` — `spanf2.c:46`

`intersectlinksets` takes exactly three input lists. The naming — `linkset1`, `linkset2`, `linkset3`, `*linkset4ptr` (the output pointer is called "4") — suggests the authors thought of this as "intersecting 3 sets to produce a 4th", not as "intersecting N sets". There is no loop, no count variable, no array of link sets.

---

### Evidence 6: The wire protocol encodes three exactly

`requests.h` defines:

```
#define CREATELINK              27
#define RETRIEVEENDSETS         28
#define FINDNUMOFLINKSFROMTOTHREE 29
#define FINDLINKSFROMTOTHREE    30
#define FINDNEXTNLINKSFROMTOTHREE 31
```

`fns.c:100-112` shows CREATELINK parses exactly three specsets:

```c
void createlink(typetask *taskptr)
{
  typeisa docisa, linkisa;
  typespecset fromspecset, tospecset, threespecset;
  ...
  if (
     getcreatelink (taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
  && docreatelink (taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa)) {
```

`fns.c:350-362` shows RETRIEVEENDSETS returns exactly three:

```c
void retrieveendsets(typetask *taskptr)
{
  typespecset specset, fromset, toset, threeset;
  ...
  doretrieveendsets (taskptr, specset, &fromset, &toset, &threeset)
  putretrieveendsets (taskptr, fromset, toset, threeset);
```

The wire protocol has no provision for N endsets — not a count field, not a list, not a variadic encoding.

---

### Conclusion

| Constraint | Nature | Source |
|---|---|---|
| Span type integers 1, 2, 3 | Hard-coded constants | `xanadu.h:36-38` |
| `DOCISPAN=4` collision | Integer namespace exhaustion | `xanadu.h:39` |
| `setlinkvsas` VSA assignment | Fixed-arity function, not a loop | `do2.c:169-183` |
| `insertendsetsinspanf`, `insertendsetsinorgl` | Fixed-arity with 3rd conditional | `do2.c:116-149` |
| `intersectlinksets` | Fixed 3-input signature | `spanf2.c:46` |
| FEBE wire protocol | Exactly 3 specsets in/out | `requests.h`, `fns.c:100-112`, `fns.c:350-362` |

**The minimum necessary is two** — `domakelink` (`do1.c:169`) implements a 2-endset link and is structurally valid. The third endset was a semantic addition (the link-type dimension, enabling typed hyperlinks), added incrementally on top of the from/to pair.

**The design was not built for N-way extensibility**. There is no data structure, no loop, no count variable, no variadic encoding that would let a fourth endset be added without touching every layer: the constants, the function signatures, the wire protocol serialization, and the span type integer assignment. The `DOCISPAN=4` collision is the most concrete expression of this: the spanfilade integer key space for link endsets was never reserved — the document content type was immediately assigned the next available integer, closing off the sequence at three.

---

## Question 12 [gregory]

> The type endset is itself an I-address span rather than a symbolic label or enumerated value — what was the design reasoning for making link type a content-identity reference on the tumbler line rather than a distinct categorical mechanism?

### Gregory's Answer

## KB Synthesis

The KB doesn't record Nelson's stated reasoning directly, but the design rationale is recoverable by synthesis.

**Uniformity of the three-endpoint structure**

The link data structure stores FROM, TO, and THREE as parallel constructs: all three are I-address spans inserted into the POOM at subspaces 2.x, and indexed in the spanfilade [SS-DUAL-ENFILADE, Finding 0038]. Making type a content reference means the link record is a homogeneous triple — no special categorical slot, no metadata field with a different type. The `LINKATOM` element type and `setlinkvsas()` assignment of digits 1, 2, 3 to the three endsets treats them structurally identically [SS-LINK-SUBSPACE].

**Hierarchical typing via tumbler containment**

The type registry in the bootstrap document uses tumbler addresses to encode subtype relationships: MARGIN at `1.0.2.6.2` is hierarchically nested under FOOTNOTE at `1.0.2.6` [SS-LINK-ENDPOINT, Finding 0024]. This is the same containment predicate used everywhere in the address space — truncate and compare [SS-TUMBLER-CONTAINMENT]. A query "find all footnote-family links" becomes an I-address range query, identical mechanically to any other span search. No separate subtyping mechanism is needed because the tumbler total order already provides containment for free [INV-TUMBLER-TOTAL-ORDER].

**The type registry is itself content**

The bootstrap document's type subspace (`1.0.2.x`) participates in the permascroll and content identity system [SS-CONTENT-IDENTITY]. This means the type definitions can be transcluded, versioned, and linked against. A type is not a categorical constant frozen in code; it is a named location in the docuverse. New types are new entries in a document, not schema changes.

**Discoverability symmetry**

Because type is indexed in the spanfilade the same way source and target are, `find_links` can in principle search by type just as it searches by content — passing the type VSpec as the THREE parameter [SS-FIND-LINKS, Finding 0029]. The design intent was that you could ask "find all QUOTE links touching this span" using a single spanfilade query with three simultaneous I-address constraints. The KB notes this is broken in practice [EC-TYPE-FILTER-NONFUNCTIONAL], but the architectural motivation is clear: a uniform three-way content-identity query with no special cases.

**What the KB cannot confirm**

Whether Nelson articulated this reasoning explicitly is not in the KB. The EC-ORPHANED-LINK matrix [Finding 0024] shows anomalous behavior when both endpoints are deleted (type endset also empties, despite the bootstrap document being intact), suggesting the implementation may not have fully realized the design. The design intent appears to be: *everything is content, type hierarchy is address hierarchy, and the link system needs no categorical mechanism outside the tumbler address space itself*.

---

## Code Exploration

Now I have everything I need. Here is the full answer.

---

## Why Endset Type Is an I-Address Span Rather Than a Categorical Mechanism

### The Evidence in the Code

**The type constants** (`xanadu.h:35-39`):

```c
/* spanfilade span types */
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

Four integers on the same number line. Crucially, `DOCISPAN = 4` sits right alongside the endset types — document content itself uses this same mechanism. There is no separate enum for "link semantics" vs. "content semantics." Every kind of thing in the system occupies a numeric band of address space.

**The type aliases** (`xanadu.h:73-76`):

```c
typedef typespan typevspan;
typedef typevspan * typevspanset;
typedef typespan typeispan;
typedef typeispan * typeispanset;
```

There is no `typeendset`. An endset IS a span, which IS a tumbler pair. The C type system makes no distinction between a document content span and a link endset span. They are the same struct.

---

### How Type Gets Encoded

**`prefixtumbler` (`tumble.c:641-651`)** is the encoding operation:

```c
int prefixtumbler(tumbler *aptr, INT bint, tumbler *cptr)
{
    tumbler temp1, temp2;
    tumblerclear (&temp1);
    temp1.mantissa[0] = bint;
    movetumbler (aptr, &temp2);
    if (!iszerotumbler (&temp2)) /* yuckh! */
        temp2.exp -= 1;
    tumbleradd (&temp1, &temp2, cptr);
}
```

It prepends `bint` as the leading digit of the tumbler: link ISA `L` becomes `1.L` for from, `2.L` for to, `3.L` for three. This is called directly in `insertspanf` (`spanf1.c:22`):

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

The endset type is baked into the ORGL-range coordinate of every crumb inserted into the spanfilade. Not as a flag. As a coordinate.

**`beheadtumbler` (`tumble.c:673-683`)** is the inverse — it strips the leading digit to recover the bare link ISA from a retrieved coordinate. It's called in `sporgl.c:264`:

```c
beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
```

`prefixtumbler` / `beheadtumbler` are the encode/decode pair. Type is a coordinate prefix, not a field.

---

### How Type Gets Retrieved

**`retrieveendsetsfromspanf` (`spanf1.c:206-217`)** constructs the query windows:

```c
fromspace.stream.mantissa[0] = LINKFROMSPAN;   // = 1
fromspace.width.mantissa[0] = 1;

tospace.stream.mantissa[0] = LINKTOSPAN;       // = 2
tospace.width.mantissa[0] = 1;

threespace.stream.mantissa[0] = LINKTHREESPAN; // = 3
threespace.width.mantissa[0] = 1;
```

To retrieve from-endsets, restrict ORGLRANGE to `[1, 2)`. To-endsets: `[2, 3)`. Three-endsets: `[3, 4)`. These are literal I-address spans passed to `retrieverestricted`, the same function used for all enfilade lookups. There is no conditional branching on type — just a geometric window into address space.

Similarly, `sporglset2linkset` (`sporgl.c:257-258`) prefixes the orglrange with the spantype before querying:

```c
prefixtumbler(&orglrange->stream, spantype, &range.stream);
prefixtumbler(&orglrange->width, 0, &range.width);
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, ...);
```

The type selection is done by coordinate restriction, not by branching on an enum.

---

### The V-Dimension Mirrors It

**`setlinkvsas` (`do2.c:169-183`)** places each endset at a V-address that mirrors its type integer:

```c
tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);   // from at V = 1.1
tumblerincrement(tovsaptr,   0, 2, tovsaptr);     // to   at V = 2.1
tumblerincrement(threevsaptr,0, 3, threevsaptr);  // three at V = 3.1
```

The link's private POOM (permutation matrix) stores from-content at V = 1.x, to-content at V = 2.x, three-content at V = 3.x. The V-space is partitioned by type, using the same numeric values as the ORGL-space partitioning. The "type" is a consistent coordinate convention across both dimensions of the enfilade.

---

### Type as Position, Not Metadata

The deepest confirmation is `islinkcrum` (`orglinks.c:255-261`):

```c
bool islinkcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0) {
        return TRUE;
    }
    return FALSE;
}
```

The distinction between text content and link data in the POOM is made by inspecting V-coordinate digits — not a flag, not a type field, not an enum. A crum is a "link crum" if its V coordinate has mantissa[0] == 1 and a nonzero second digit. Type IS position. This applies at every layer: in the spanfilade (ORGL bands), in the POOM (V bands), and in the query machinery (coordinate windows).

The optionality of the three-endset (`do1.c:216`, `do2.c:122-126`) is handled the same way: the `[3,4)` band simply isn't populated. An absent type is an empty address range. No "null" enum value is needed. Non-existence of a type is non-existence of content at that coordinate.

---

### The Design Reasoning

The choice follows from three compounding constraints of the Xanadu model:

**1. The POOM has no metadata fields.** A crumb in the enfilade stores only its position and a `homedoc` tumbler (`type2dbottomcruminfo`). There is no field for "endset type." If type must be stored, it must be stored as position. The enfilade's node structure is a pure geometric object.

**2. The spanfilade must answer the query "find all links whose from-endset overlaps this I-span" in a single geometric operation.** If type were a separate categorical field, the query would require two-pass filtering: first retrieve by I-span, then filter by type field. Instead, encoding type as a coordinate prefix on the ORGL dimension means the query is simply: intersect SPANRANGE against the requested content spans, restrict ORGLRANGE to `[1,2)`. Both constraints are handled by a single call to `retrieverestricted`. No secondary filter needed.

**3. Document content, link identity, and link endsets all live in the same indexed structure.** `DOCISPAN = 4` sits on the same number line as `LINKFROMSPAN = 1`, `LINKTOSPAN = 2`, `LINKTHREESPAN = 3`. The spanfilade is a single uniform index over all of them. A query for "what document contains this I-span" restricts ORGLRANGE to `[4,5)`. A query for "what links reference this I-span as a from-endset" restricts to `[1,2)`. The same machinery, the same function call, different numeric window. This uniformity would be broken if link endsets used a categorical mechanism instead of a position in address space.

The from/to/three distinction is not a type system. It is a coordinate convention: endset N occupies the `[N, N+1)` band of address space. What would be a tag or enum value in a conventional system is here a spatial partition, because the Xanadu model has no concept of metadata separate from content — a thing's identity IS its address, and a thing's kind IS which part of the address space it occupies.

---

## Question 13 [gregory]

> What are the cardinality constraints on an individual endset — can an endset contain zero spans, exactly one span, or an unbounded number of spans, and does this differ between source, target, and type?

### Gregory's Answer

## KB Synthesis

## Endset Cardinality

Endsets have variable cardinality at all three endpoints, with distinct mechanisms driving each bound.

---

### Zero spans — when and why

An endset returns zero spans when its stored I-addresses have no POOM mapping in the queried document. The filtering is silent: `linksporglset2specset` → `span2spanset` → `retrieverestricted` drops any I-address that returns NULL from the POOM lookup, with no error [SS-FOLLOWLINK, Finding 0048].

This occurs in two scenarios:

1. **Content deleted**: All content at the endpoint has been removed from the document. [EC-GHOST-LINK] documents this as a "ghost link" — the link orgl is intact and FOLLOWLINK succeeds, but the result is `[]`.

2. **Querying from the wrong document**: FOLLOWLINK resolves I-addresses through a caller-specified `homedoc`. If that document's POOM has no mappings for the endset I-addresses, the result is empty [SS-FOLLOWLINK, Finding 0048].

The [EC-ORPHANED-LINK] behavior matrix (Finding 0024) shows the full picture:
- Source deleted → source endset = `[]`
- Target deleted → target endset = `[]`
- Both deleted → type endset also becomes `[]` (anomalous — see below)

---

### One span — the normal case

At creation time, endpoints require width >= 1; zero-width crashes [PRE-ZERO-WIDTH, Finding 0028]. Content inserted from a single, contiguous source maps to a single contiguous I-span, producing one sporgl and thus one V-span in the endset.

---

### Multiple spans — causes

The endset structure is `set<Sporgl>` where `|Endset| >= |input_vspans|` [SS-LINK-ENDPOINT, Finding 0037]. Three distinct mechanisms produce multiple spans:

**1. Multi-source transclusion at link creation** [ST-LINK-CREATE, Finding 0037]: If the V-span used to define the endpoint covers content from multiple source documents, `vspanset2sporglset` splits it into one sporgl per contiguous I-address region. Example: document C contains "AA" (I-addresses from doc A) and "BB" (I-addresses from doc B); creating a link on "AABB" produces 2 sporgls despite 1 input V-span.

**2. Rearrangement/pivot fragmentation** [EC-PIVOT-LINK-FRAGMENTATION, Finding 0019]: After a pivot on linked content, the endset can fragment — a 2-character link can produce 4 spans, and `find_links` may return the link twice.

**3. Multi-span link creation** [EC-MULTISPAN-LINK-DUPLICATION, Finding 0019]: Creating a link with multiple source spans (e.g., "First" and "second") produces more spans than provided at creation — 3 spans observed from 2 input spans, with duplication.

---

### Differences between source, target, and type

**Source and target** endsets follow the same rules: zero to unbounded, determined by I-address resolvability and content I-address contiguity.

**Type** endsets behave differently:
- Normally return **exactly one span**, pointing to a specific address in the bootstrap document's type registry at `1.0.2.x` [SS-LINK-ENDPOINT, Finding 0024]. The type subspace uses tumbler containment to encode hierarchy (`1.0.2.6.2` is a subtype of `1.0.2.6`).
- The bootstrap document is not deleted by user operations, so the type endset should always resolve.
- **Exception**: When both source and target endpoints are deleted, the type endset also returns empty — "either a bug or an undocumented dependency of type resolution on endpoint resolution" [EC-ORPHANED-LINK, Finding 0024]. This is anomalous since the type references the permanently available bootstrap document.

---

### Summary

| Endpoint | Zero? | One? | Many? |
|----------|-------|------|-------|
| Source | Yes — when endpoint I-addresses unresolvable | Yes — normal | Yes — multi-source transclusion, rearrangement, multi-span creation |
| Target | Yes — same mechanism | Yes — normal | Yes — same mechanisms |
| Type | Yes — anomalously, when both source+target also empty | Yes — normal case | Not documented |

---

## Code Exploration

Now I have everything I need for a complete, cited answer.

---

## Endset Cardinality in udanax-green

### Data Model

An endset is represented as a `typesporglset` — a NULL-terminated singly-linked list of `typesporgl` items [xanadu.h:115-127]:

```c
typedef struct structsporgl {
    struct structsporgl *next;       // linked list chain
    typeitemid  itemid;
    tumbler sporglorigin;
    tumbler sporglwidth;
    typeisa sporgladdress;
} typesporgl;

typedef typesporglitem * typesporglset;  // xanadu.h:127
```

There is no `count` field and no min/max constraint on the list. Cardinality is determined purely by how many nodes are chained through `next`.

---

### Zero Spans

**Write side — allowed silently.** Both insertion functions use a simple `for (; sporglset; ...)` loop that does nothing if the pointer is NULL:

`insertspanf` [spanf1.c:25-53]:
```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    ...
}
return (TRUE);  // always returns TRUE
```

`insertpm` [orglinks.c:99-133]:
```c
logbertmodified(orglisa, user);  // always called
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    ...
}
return (TRUE);
```

If `sporglset` is NULL, nothing is inserted into the spanfilade or POOM, but the function returns TRUE. Even `logbertmodified` fires on an empty endset, marking the link as modified.

**Read side — followlink returns FALSE.** `link2sporglset` [sporgl.c:83-94] uses an `if (context = retrieverestricted(...))` idiom — if the enfilade has no crums in the queried region (because nothing was ever inserted), `context` is NULL, the if-block is skipped, and the function returns FALSE:

```c
if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
    for (c = context; c; c = c->nextcontext) { ... }
    return (TRUE);
} else {
    return (FALSE);  // no spans → FALSE
}
```

Since `dofollowlink` [do1.c:228-231] short-circuits on FALSE:
```c
return (
    link2sporglset(taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset(...));
```
…a zero-span endset causes `followlink` to fail.

**Conclusion for zero:** A zero-span endset is *structurally writable* but yields a followlink failure. There is no creation-time rejection guard.

---

### Exactly One Span

The common and fully-supported case. One entry in the sporglset linked list is inserted once and retrieved once. No special handling required.

---

### Unbounded Multiple Spans

All code paths are list-iterating loops with no upper bound.

**Conversion** from vspansets to sporglsets in `vspanset2sporglset` [sporgl.c:47-64] is a double loop — one iteration per vspan, one per resulting ispan — producing one sporgl per ispan with no limit:

```c
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {
        sporglset = (typesporgl *) taskalloc(taskptr, sizeof(typesporgl));
        ...
        *sporglsetptr = (typesporglset)sporglset;
        sporglsetptr = (typesporglset *)&sporglset->next;
    }
}
```

**Insertion** via `insertspanf` [spanf1.c:25-52] calls `insertnd` once per sporgl, appending a crum to the spanfilade for each span — unbounded.

**Retrieval** via `link2sporglset` [sporgl.c:84-89] allocates one `typesporgl` per context item returned by `retrieverestricted`, and chains them:

```c
for (c = context; c; c = c->nextcontext) {
    sporglptr = (typesporgl *)taskalloc(taskptr, sizeof(typesporgl));
    contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
    *sporglsetptr = (typesporglset)sporglptr;
    sporglsetptr = (typesporglset *)&sporglptr->next;
}
```

And `linksporglset2specset` [sporgl.c:103-121] similarly iterates all sporgls to produce the returned specset. No cap anywhere.

**Conclusion for multiple:** Unbounded. The entire architecture is linked-list traversal at every stage.

---

### Source vs. Target vs. Type

The three endsets are distinguished by constants defined in [xanadu.h:36-38]:

```c
#define LINKFROMSPAN    1   // source
#define LINKTOSPAN      2   // target
#define LINKTHREESPAN   3   // type
```

These are used only as V-subspace prefixes in `setlinkvsas` [do2.c:169-182] and as spantype arguments to `insertspanf`. They determine *where* in the spanfilade each endset's spans are stored, not *how many* spans they may contain.

**Structural symmetry at insertion:** `insertendsetsinspanf` [do2.c:116-128] and `insertendsetsinorgl` [do2.c:130-148] call the same functions for all three:

```c
// insertendsetsinspanf:
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)
if (threesporglset)
    insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)

// insertendsetsinorgl:
insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)
insertpm(taskptr, linkisaptr, link, tovsa,   tosporglset)
if (threevsa && threesporglset)
    insertpm(taskptr, linkisaptr, link, threevsa, threesporglset)
```

**The only asymmetry:** The type endset (`LINKTHREESPAN`) is guarded by a null check in both insertion functions. Source and target are called unconditionally. This means:
- Source and target endsets are **required** (with NULL/empty sporglset silently creating empty endsets as described above)
- Type endset is **optional** — if `NULL` is passed, it is simply skipped

**At retrieval:** `dofollowlink` [do1.c:223-232] uses `whichend` (1=from, 2=to, 3=type) to pass to `link2sporglset`, which translates it directly into the V-range query. The retrieval logic is identical for all three endset types.

---

### Summary Table

| Property | Source | Target | Type |
|---|---|---|---|
| Zero spans storable | Yes (silent) | Yes (silent) | Yes (silent) |
| Zero spans followable | No (returns FALSE) | No (returns FALSE) | No (returns FALSE) |
| One span | Yes | Yes | Yes |
| N spans (unbounded) | Yes | Yes | Yes |
| Optional at creation | No | No | **Yes** |
| Span-handling code | `insertspanf` / `insertpm` | same | same |
| Wire discriminator | `LINKFROMSPAN = 1` | `LINKTOSPAN = 2` | `LINKTHREESPAN = 3` |

The only cardinality difference between endset types is that the type endset is *optionally present* at the link level, while source and target are always structurally instantiated. Once present, all three endsets are subject to identical constraints: zero-to-unbounded spans, with zero being silent-but-unfollowable and N being architecturally unlimited.

---

## Question 14 [gregory]

> Can a single endset span I-addresses originating from multiple documents (i.e., a source endset referencing content created in doc A and content created in doc B), or must each endset be confined to a single document's I-address range?

### Gregory's Answer

## KB Synthesis

A single endset can reference I-addresses originating from multiple documents. There is no confinement to a single document's I-address range.

The mechanism is documented in [ST-LINK-CREATE] / [SS-LINK-ENDPOINT] (Finding 0037). When `domakelink` receives a V-span that maps to non-contiguous I-addresses from multiple sources, `vspanset2sporglset` walks every I-span returned by `vspanset2ispanset` and creates a **separate sporgl per contiguous I-address region**. Each sporgl independently carries:

- `sporglorigin` — the I-address of that region
- `sporglwidth` — its width
- `sporgladdress` — the **document** where that content resides

So if content in document C consists of "AA" transcluded from A and "BB" transcluded from B, selecting that entire V-span as a link endpoint produces two sporgls in the endset: one pointing into A's permascroll range, one into B's. The endset type is `set<Sporgl>`, not `set<ISpan>` — provenance is per-sporgl, not per-endset [SS-SPORGL].

The cardinality rule from [SS-LINK-ENDPOINT]: `|Endset| >= |input_vspans|`. When the input V-span covers content from N distinct source documents (or N disjoint I-address regions), the endset contains at least N sporgls.

This is also why [EC-LINK-PARTIAL-SURVIVAL] holds: if document A is deleted but document B survives, the endset retains the B-originated sporgl intact while the A-originated sporgl becomes unresolvable. Partial survival is per-sporgl.

The constraint that does exist is the inverse: each **sporgl** within an endset is confined to a single contiguous I-address region from a single document. Multi-document I-address mixing within one sporgl is structurally impossible — a sporgl has exactly one `sporgladdress`.

---

## Code Exploration

Now I have everything I need to answer comprehensively. Here is my analysis:

---

## Can a Single Endset Reference I-Addresses From Multiple Documents?

**Yes.** The code imposes no restriction confining an endset to a single document's I-address range. The architecture explicitly supports multi-document endsets at every level.

---

### 1. The Data Type Is Already Multi-Document

The `typespecset` type is a **linked list of `typespec`**, and each `typespec` is either:

```c
// xanadu.h:78-89
typedef struct structtypevspec {
    struct structtypevspec *next;
    typeitemid itemid;
    typeisa docisa;          // ← document-specific ISA
    typevspanset vspanset;   // ← V-spans within that document
} typevspec;

typedef union {
    typevspec xxxvspec;
    typeispan xxxispan;
} typespec;
typedef typespec * typespecset;
```

A `typespecset` passed as a from/to/three endset to `docreatelink` [do1.c:195] can therefore be a list of `typevspec` nodes each with a **distinct `docisa`**. Nothing in the type prevents it.

---

### 2. Link Creation Iterates the Entire Multi-Document Specset

In `docreatelink` [do1.c:195-221], for each endset:

```c
specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
```

`specset2sporglset` [sporgl.c:14-33] loops over every element:

```c
for (; specset; specset = (typespecset)((typeitemheader*)specset)->next) {
    if (((typeitemheader *)specset)->itemid == VSPECID) {
        sporglsetptr = vspanset2sporglset(taskptr,
            &((typevspec *)specset)->docisa,   // ← each element's own docisa
            ((typevspec *)specset)->vspanset,
            sporglsetptr, type);
    }
}
```

For each `typevspec`, `vspanset2sporglset` [sporgl.c:35-65] looks up the ORGL for *that document*, translates its V-spans to I-spans, and creates `typesporgl` entries:

```c
sporglset->sporgladdress = *docisa;  // source document for this I-span
sporglset->sporglorigin  = ispanset->stream;
sporglset->sporglwidth   = ispanset->width;
```

So the output `fromsporglset` is a **flat linked list whose entries may carry different `sporgladdress` values** if the input specset referenced multiple documents. No filtering, no validation, no error.

---

### 3. Insertion Into the Spanfilade Processes Each Sporgl Independently

`insertendsetsinspanf` [do2.c:116-128] calls `insertspanf` per endset type. Inside `insertspanf` [spanf1.c:15-54]:

```c
for (; sporglset; sporglset = ...) {
    if (itemid == SPORGLID) {
        movetumbler(&sporglset->sporglorigin,  &lstream);
        movetumbler(&sporglset->sporglwidth,   &lwidth);
        movetumbler(&sporglset->sporgladdress, &linfo.homedoc);  // per-entry doc
    }
    ...
    insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
}
```

Each sporgl is inserted into the spanfilade with its own `homedoc`. The enfilade crum for a span from Doc A carries Doc A's ISA as `homedoc`; a span from Doc B carries Doc B's ISA. They are stored as separate crums because `isanextensionnd` [insertnd.c:301-309] requires matching `homedoc` before merging adjacent crums:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr,
                     type2dbottomcruminfo *infoptr)
{
    if (!tumblereq(&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);   // ← different doc = never merged, but never rejected
    ...
}
```

Critically: **different-doc crums are rejected from merging but are never rejected from insertion**. They simply live in the spanfilade as separate crums.

---

### 4. Insertion Into the Link's Own POOM Also Accepts Multi-Document Sporgls

`insertendsetsinorgl` [do2.c:130-149] calls `insertpm` [orglinks.c:75-134] for each endset. Inside `insertpm`:

```c
for (; sporglset; sporglset = ...) {
    unpacksporgl(sporglset, &lstream, &lwidth, &linfo);
    // linfo.homedoc = sporglset->sporgladdress (per-entry doc)
    ...
    insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
    tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);
}
```

`unpacksporgl` [sporgl.c:178-203] sets `infoptr->homedoc` from each sporgl's `sporgladdress`. Each I-span from each source document gets its own V-address slot in the link's POOM, tagged with that document's ISA. No single-document constraint is checked.

---

### 5. Retrieval Also Handles Multi-Document Endsets

When `dofollowlink` [do1.c:223] or `doretrieveendsets` [do1.c:369] reconstructs an endset, `link2sporglset` [sporgl.c:67-95] retrieves the sporgl list from the link's POOM. `linksporglset2specset` [sporgl.c:97-122] then calls `linksporglset2vspec` → `sporglset2vspanset` [sporgl.c:141-176], which groups consecutive sporgls by matching `sporgladdress`:

```c
if (!tumblereq(&((typesporgl *)sporglptr)->sporgladdress,
               &((typesporgl *)(*sporglsetptr))->sporgladdress))
    return(0);  // stop this vspec group, new document begins
```

Different-document sporgls are recovered as **separate `typevspec` entries** in the returned `typespecset` — one per source document. The reconstructed endset is a multi-element specset, exactly parallel to what was inserted.

---

### Summary

| Stage | File | Lines | Behavior |
|---|---|---|---|
| Type definition | `xanadu.h` | 78-89 | `typespecset` is a linked list; each `typevspec` carries its own `docisa` |
| Specset → sporglset | `sporgl.c` | 14-33 | Iterates all specset elements; calls `vspanset2sporglset` per element with its own `docisa` |
| Sporgl carries doc ISA | `sporgl.c` | 35-65 | Each `typesporgl.sporgladdress` = source document |
| Spanfilade insert | `spanf1.c` | 25-51 | Each sporgl inserted with its own `linfo.homedoc`; no cross-document validation |
| Crum extension check | `insertnd.c` | 301-309 | Different-doc spans not merged, but also **not rejected** |
| Link POOM insert | `orglinks.c` | 100-131 | Each sporgl inserted independently with its own `homedoc` |
| Follow/retrieve | `sporgl.c` | 141-176 | Consecutive same-doc sporgls group into one `typevspec`; doc boundary stops the group |

**A single endset (from, to, or three) can reference I-addresses originating in multiple documents.** The `typespecset` input is a linked list of per-document specs; `specset2sporglset` expands them all into a flat sporglset; and both the spanfilade and the link's POOM store each resulting I-span tagged with its source document's ISA. No validation anywhere in the pipeline enforces single-document confinement. On retrieval, the spans are reconstituted as a multi-element specset, one `typevspec` per source document.

---

## Question 15 [gregory]

> Is the source/target distinction on a link an intrinsic structural asymmetry in the orgl representation, or is it a naming convention over two structurally identical endset slots — could a link be meaningfully "followed" in either direction with equal validity?

### Gregory's Answer

## KB Synthesis

The source/target distinction is **a naming convention over two structurally identical endset slots**, not an intrinsic asymmetry. Here's the evidence:

## Storage Structure

The link orgl stores three sub-positions: 0.1 (FROM), 0.2 (TO), and 0.3 (TYPE). Per [SS-DUAL-ENFILADE] Finding 0038, `setlinkvsas()` constructs these by hardcoding digit-0 values of 1, 2, and 3. The FROM and TO slots use exactly the same storage format — both are sporglsets, both indexed in the spanfilade via the same mechanism, distinguished only by their ORGLRANGE subspace constant (LINKFROMSPAN=1 vs LINKTOSPAN=2) per [SS-RETRIEVE-ENDSETS] Finding 0035.

## Symmetric Discovery

[SS-LINK-ENDPOINT] Finding 0005 states both endpoints "participate symmetrically in discovery":

- `find_links(source_specs, NOSPECS)` = links whose **source** I-addresses intersect
- `find_links(NOSPECS, target_specs)` = links whose **target** I-addresses intersect

The search mechanism is identical — both convert V-spans to I-addresses and query the spanfilade. Neither direction has priority.

## Symmetric Traversal

[SS-FOLLOW-LINK] Finding 0028 confirms both are fully traversable:
```
follow_link(L, SOURCE) == L.source_specset
follow_link(L, TARGET) == L.target_specset
```

Per [SS-FOLLOWLINK] Finding 0048, `link2sporglset()` extracts endsets from the link orgl at position 0.1, 0.2, or 0.3 via `retrieverestricted()` — the same code path with a position parameter. There is no code-level asymmetry between retrieving FROM vs TO.

## Where Asymmetry Actually Lives

The only **genuine** structural asymmetry is between the content endsets (0.1, 0.2) and the **TYPE** endset (0.3). Per [SS-ADDRESS-SPACE] Finding 0024, the type slot points to the bootstrap document's type registry (`1.0.2.x`), not to arbitrary content. It occupies its own spanfilade subspace (LINKTHREESPAN=3) and is retrieved conditionally in [SS-RETRIEVE-ENDSETS].

## Conclusion

A link can meaningfully be "followed" in either direction with equal structural validity. The semantic meaning of "source implies origin, target implies destination" is application-level convention, enforced by the link type (e.g., JUMP, QUOTE) and by how the client interprets the two slots — not by any storage asymmetry. The KB contains no evidence that the backend enforces or even models directionality; it simply treats FROM and TO as slot-1 and slot-2 of the same orgl structure.

---

## Code Exploration

Now I have a complete picture. Here is my full answer:

---

## Is source/target a structural asymmetry or a naming convention?

**Both, at different layers — and the answer differs between storage and traversal.**

---

### 1. Creation: Three Parallel Slots, Hardcoded Addresses

In `docreatelink` [`do1.c:195-221`], creating a link calls two key routines:

```c
&& setlinkvsas (&fromvsa, &tovsa, &threevsa)
&& insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset,
                        &tovsa, tosporglset, &threevsa, threesporglset)
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset,
                         tosporglset, threesporglset)
```

**`setlinkvsas` assigns fixed, distinct V-addresses to each endset** [`do2.c:169-183`]:

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr) {
    tumblerclear (fromvsaptr);
    tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);   // → 1.x
    tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);   // → 1.1

    tumblerclear (tovsaptr);
    tumblerincrement (tovsaptr, 0, 2, tovsaptr);       // → 2.x
    tumblerincrement (tovsaptr, 1, 1, tovsaptr);       // → 2.1

    if (threevsaptr) {
        tumblerclear (threevsaptr);
        tumblerincrement (threevsaptr, 0, 3, threevsaptr);  // → 3.1
        tumblerincrement (threevsaptr, 1, 1, threevsaptr);
    }
    return (TRUE);
}
```

- **from-endset** → V-address `1.1` in the link's POOM  
- **to-endset** → V-address `2.1`  
- **three-endset** → V-address `3.1`

These addresses are not arbitrary labels — they are hardcoded into the virtual coordinate space of every link's permutation matrix.

---

### 2. Spanfilade: Three Distinct Index Columns

`insertendsetsinspanf` [`do2.c:116-128`] indexes each endset under a different span-type constant:

```c
bool insertendsetsinspanf(...) {
    insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
    && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)
    ...
    insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)
}
```

The constants are defined in `xanadu.h:36-39`:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

Inside `insertspanf` [`spanf1.c:22`], the span-type becomes an ORGLRANGE prefix key:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

So the spanfilade has **three structurally distinct columns** — one per role — not one combined column with a label attached. The from-endset and to-endset exist in physically separate regions of the spanfilade address space.

---

### 3. Search: The Asymmetry Is Load-Bearing

`findlinksfromtothreesp` [`spanf1.c:56-103`] searches each spanfilade column independently, then intersects:

```c
sporglset2linkset (taskptr, spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
sporglset2linkset (taskptr, spanfptr, tosporglset, &tolinkset, orglrange, LINKTOSPAN);
sporglset2linkset (taskptr, spanfptr, threesporglset, &threelinkset, orglrange, LINKTHREESPAN);
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```

And in `retrieveendsetsfromspanf` [`spanf1.c:190-235`]:

```c
fromspace.stream.mantissa[0] = LINKFROMSPAN;    // column 1
tospace.stream.mantissa[0] = LINKTOSPAN;         // column 2
threespace.stream.mantissa[0] = LINKTHREESPAN;   // column 3
```

These columns are not interchangeable. A query for "links from A" will not accidentally find "links to A" — they live in distinct ORGLRANGE address regions. **Swapping from/to in a query requires explicitly swapping which column you search.** There is no "reverse link" operation built into the search layer.

---

### 4. Traversal: Fully Symmetric

Despite the structural asymmetry in storage and search, **traversal is entirely symmetric and parameterized**.

`followlink` in `fns.c:114-127` passes `whichend` directly from the client:

```c
void followlink(typetask *taskptr) {
    INT whichend;
    getfollowlink (taskptr, &linkisa, &whichend)
    && dofollowlink (taskptr, &linkisa, &specset, whichend)
}
```

`dofollowlink` [`do1.c:223-232`] forwards it unchanged to `link2sporglset` [`sporgl.c:67-95`]:

```c
bool link2sporglset(typetask *taskptr, typeisa *linkisa, typesporglset *sporglsetptr, INT whichend, int type) {
    ...
    tumblerincrement (&zero, 0, whichend, &vspan.stream);  // queries V-slot whichend
    tumblerincrement (&zero, 0,        1, &vspan.width);   // unit-wide range
    context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, ...);
}
```

`whichend=1` queries the V-range `[1, 2)` → hits the from-endset stored at `1.1`.  
`whichend=2` queries `[2, 3)` → hits the to-endset stored at `2.1`.  
`whichend=3` queries `[3, 4)` → hits the three-endset at `3.1`.

The human-interactive input parser even validates all three explicitly [`get1.c:70-71`]:

```c
getnumber (taskptr, whichendptr)
&& (*whichendptr == 1 || *whichendptr == 2 || *whichendptr == 3)
```

**There is no code in the traversal path that privileges one endset over another.** A client can call `followlink` with `whichend=2` to arrive at the "to" endset, then use `retrieveendsets` to get both endsets and follow again from `whichend=1`. From the traversal machinery's perspective, the three slots are mechanically identical.

---

### Conclusion

The from/to/three distinction is **a genuine structural asymmetry at the representation level**, encoded at two independent levels:

| Layer | How the asymmetry is encoded |
|---|---|
| **POOM (orgl)** | V-addresses `1.1`, `2.1`, `3.1` assigned by `setlinkvsas` |
| **Spanfilade** | ORGLRANGE prefix columns `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3` set by `prefixtumbler` in `insertspanf` |

It is **not** a naming convention over two structurally identical slots — the slots have distinct addresses baked into both storage structures.

**However**, the traversal operation (`followlink` / `link2sporglset`) is fully agnostic to which slot is "source" and which is "target." Any endset can be retrieved with equal mechanical validity by supplying the corresponding integer `whichend`. A link can be "followed" from the to-endset as easily as from the from-endset — the machinery does not care.

The asymmetry is therefore real and structural, but it is **semantic**, not mechanically enforced in traversal. The labels from/to/three are a contract baked into the storage addresses and search indexes, but the traversal machinery exposes all three slots symmetrically to the caller.

---

## Question 16 [gregory]

> A link has its own I-address (the link orgl at `docISA.0.2.N`) — can a link's endset reference another link's I-address, creating link-to-link connections, and if so, was this an intentional design capability or an emergent consequence of uniform I-address treatment?

### Gregory's Answer

## KB Synthesis

## Link-to-Link Endsets: Technically Possible, Not Intentional

The short answer: **yes, technically possible as an emergent consequence of uniform I-address treatment; not an intentional design capability.**

---

### The Mechanism

Link orgls occupy I-addresses in the granfilade (e.g., `docISA.0.2.N` per [SS-ADDRESS-SPACE] Finding 0065). Within a document's V-space, link references are stored at positions `2.x` (internally) or `0.x` (normalized output), where the mapped I-address is the link orgl's ISA [SS-DUAL-ENFILADE] Finding 0009, [SS-ADDRESS-SPACE] Finding 0024.

When `domakelink` creates a link, the endpoint V-span is converted to sporgls via `vspanset2sporglset` → `vspanset2ispanset` → `permute` → `retrieverestricted`. This chain is **entirely type-agnostic** [SS-DUAL-ENFILADE] Finding 0011:

> "I-addresses likewise have no type distinction: permascroll I-addresses (content) and document ISAs (references) are both tumblers with no runtime type tag."

So if the endpoint V-span covers positions in the link subspace (`2.x`/`0.x`), the POOM lookup returns whatever I-address maps there — which is a link orgl ISA. That ISA lands in the sporgl origin field and gets stored in the spanfilade via `insertendsetsinspanf`. No type guard prevents this. `acceptablevsa()` is a no-op stub [PRE-INSERT] Finding 0011, so the creation itself would succeed.

---

### Why It Breaks Downstream

The design **assumes** link endsets contain permascroll I-addresses. Multiple subsystems fail when that assumption is violated:

- **`find_links`**: The spanfilade search expects the sporgl's I-address to be a permascroll address that other documents might share via transclusion. A link orgl ISA is unique and non-shareable [SS-CONTENT-IDENTITY] Finding 0015 — no other document will ever transclude it, so the link would be permanently undiscoverable.

- **`compare_versions`**: Requires text-subspace-only input [PRE-COMPARE-VERSIONS]. Feeding it link ISAs crashes the backend (Bug 0009) [EC-COMPARE-VERSIONS-LINK-CRASH].

- **`retrieve_contents`** on endset: `ispanset2vstuffset` treats I-addresses as permascroll positions. A link ISA dereferenced in the permascroll returns NULL/garbage [PRE-RETRIEVE-CONTENTS] Finding 0010.

- **Content identity semantics**: Link ISAs are "identity-bearing, unique" not "content-bearing, shareable" [SS-CONTENT-IDENTITY] Finding 0015. Transitive identity (INV-TRANSITIVE-IDENTITY) and link-follows-content (INV-LINK-CONTENT-TRACKING) both depend on permascroll I-addresses.

---

### Intentional or Emergent?

**Emergent.** The type-agnostic storage architecture — justified by simplicity and the convention-over-enforcement philosophy [SS-SUBSPACE-CONVENTION] Finding 0010, [SS-DUAL-ENFILADE] Finding 0011 — makes link-to-link endsets mechanically possible but semantically unsound. The KB contains no evidence that Nelson or Gregory discussed link-to-link connections as a design capability. The entire link infrastructure (spanfilade indexing, endset resolution, `compare_versions`) is built on the invariant that endsets reference permascroll content.

The correct characterization: it is a **hole in the type system**, not a feature. Just as INSERT at `2.x` with text content is technically accepted but violates the subspace convention [PRE-ENF0-PLACEMENT-GAP] Finding 0049, a link-to-link endset would be accepted at creation time but corrupted in every downstream operation that processes it.

---

## Code Exploration

Now I have everything I need. Here is the full analysis.

---

# Can a Link's Endset Reference Another Link's I-Address?

**Short answer: Yes — and the evidence points to intentional architectural design, not accident.**

---

## 1. How Link I-Addresses Are Assigned

Links are created in `docreatelink()` [do1.c:195-221]:

```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)
  ...
```

The `LINKATOM` hint routes to `findisatoinsertmolecule()` [granf2.c:158-181]:

```c
} else if (hintptr->atomtype == LINKATOM) {
    tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);   // docISA.0.2 base
    if (tumblercmp (&lowerbound, isaptr) == LESS)
        tumblerincrement (isaptr, 1, 1, isaptr);           // → docISA.0.2.N
    else
        tumblerincrement (&lowerbound , 0, 1, isaptr);
}
```

A link gets address `docISA.0.2.N` — a tumbler, indistinguishable at the type level from any other address. The key definition [xanadu.h:23]:

```c
typedef tumbler typeisa;
```

A link's I-address is just a tumbler. There is no "link flag," no tagged union, no type discriminant in the address itself.

---

## 2. How Endsets Accept Any I-Address

`docreatelink()` [do1.c:214-216] converts incoming specsets without any validation:

```c
&& specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
&& specset2sporglset (taskptr, tospecset, &tosporglset, NOBERTREQUIRED)
&& specset2sporglset (taskptr, threespecset, &threesporglset, NOBERTREQUIRED)
```

`specset2sporglset()` [sporgl.c:14-33] converts a `typevspec` to a sporglset. The vspec has a `docisa` field:

```c
} else if (((typeitemheader *)specset)->itemid == VSPECID) {
    if (!(sporglsetptr = vspanset2sporglset (taskptr,
            &((typevspec *)specset)->docisa,    // ← whatever ISA is here
            ((typevspec *)specset)->vspanset, sporglsetptr, type))){
```

`vspanset2sporglset()` [sporgl.c:44-58]:

```c
if (!findorgl (taskptr, granf, docisa, &orgl, type)){
    return (NULL);
}
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {
       sporglset = (typesporgl *) taskalloc (taskptr, sizeof(typesporgl));
       sporglset->itemid = SPORGLID;
       sporglset->next = NULL;
       movetumbler (docisa, &sporglset->sporgladdress);   // ← stored verbatim
```

The function calls `findorgl()` on whatever `docisa` is — if an orgl exists at that address, conversion proceeds. The `docisa` is then stored verbatim into `sporglset->sporgladdress`. **No check whatsoever that `docisa` refers to a document rather than a link.**

The sporgl's `sporgladdress` field [xanadu.h:120]:

```c
typedef struct structsporgl{
    struct structsporgl *next;
    typeitemid  itemid;
    tumbler sporglorigin;
    tumbler sporglwidth;
    typeisa sporgladdress;    // ← just a tumbler
} typesporgl;
```

That `sporgladdress` is later stored directly into `linfo.homedoc` in `insertspanf()` [spanf1.c:33]:

```c
} else if (((typeitemheader *)sporglset)->itemid == SPORGLID) {
    movetumbler (&((typesporgl *)sporglset)->sporglorigin, &lstream);
    movetumbler (&((typesporgl *)sporglset)->sporglwidth, &lwidth);
    movetumbler (&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc);  // verbatim
```

No guard. No type check. Any tumbler address that resolves to a valid granfilade orgl gets stored as the home document for that endset.

---

## 3. What Happens When You Follow a Link-to-Link Reference

`dofollowlink()` [do1.c:223-231]:

```c
return (
   link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
&& linksporglset2specset (taskptr, &((typesporgl *)sporglset)->sporgladdress,
                          sporglset, specsetptr, NOBERTREQUIRED));
```

`linksporglset2specset()` [sporgl.c:97-123] reconstructs a specset from the stored sporgl. When `sporgladdress` is non-zero (i.e., a real document/object address, not an ispan-only record), it calls `linksporglset2vspec()` [sporgl.c:116], which calls `sporglset2vspanset()` [sporgl.c:141-176]:

```c
(void) findorgl (taskptr, granf, homedoc, &orgl, type);   // look up the orgl
ispan.itemid = ISPANID;
movetumbler (&sporglptr->sporglorigin, &ispan.stream);
movetumbler (&sporglptr->sporglwidth, &ispan.width);
vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr);
```

If `homedoc` is a link's I-address, `findorgl()` will resolve to the link's orgl. Then `ispan2vspanset()` runs against that orgl — translating I-space positions into V-space positions within the link's content structure (which encodes the link's own from/to/three endsets at V positions 1.x, 2.x, 3.x). The retrieved vspan would point into the link's V-space.

**The retrieval path treats all orgls uniformly.** `retrievecrums()` [retrie.c:15-31] and `intervalcmp()` [retrie.c:144-160] perform pure tumbler arithmetic — no orgl-type dispatch, no object-type guards.

---

## 4. The Only Type Information That Exists

`LINKATOM` [xanadu.h:146] and `TEXTATOM` [xanadu.h:145] exist solely to route address *allocation* in `findisatoinsertmolecule()`. They determine where in the address space the new orgl gets placed. They are not stored on the orgl. They are not consulted on retrieval. Nothing in the granfilade's stored structure distinguishes "this is a link's orgl" from "this is a document's orgl."

Similarly, `LINKFROMSPAN` (1), `LINKTOSPAN` (2), `LINKTHREESPAN` (3), `DOCISPAN` (4) [xanadu.h:35-38] tag *which endset slot* an entry occupies in the spanfilade — they are the ORGLRANGE prefix on the endset entry — but they say nothing about the target I-address stored in the spanfilade's SPANRANGE data.

---

## 5. Intentional Design or Emergent Consequence?

The evidence points to **intentional design**, for three structural reasons:

**First, the address space has uniform semantics by construction.** The Xanadu model's core principle is that every stored object — text atom, link, document, account — has an I-address. This is not accidental: the entire design of the granfilade, with `typeisa` as bare `tumbler`, reflects a commitment to address uniformity. If link orgls were meant to be unreferenceable, the type system would have enforced it.

**Second, the `specset2sporglset()` conversion is the natural choke point for type validation, and it contains none.** This function could trivially have called `findorgl()` and checked the retrieved orgl's atom type before proceeding. It doesn't. The comment in `sporgl.c:60-64` notes that the return value of `vspanset2sporglset()` is used to build a linked list — the design assumes any orgl at any address is fair game.

**Third, `dofollowlink()` at do1.c:230 uses `sporgladdress` directly as the `homedoc` for reconstruction.** This means the retrieval path is already wired to handle any ISA as the home for an endset. If link orgls had been meant to be excluded from endset targets, this would have required special-casing here, and there is none.

The most coherent reading: the architects of udanax-green built a uniform I-address space deliberately, and link-to-link references follow as a natural consequence of that uniformity — the code simply never draws a line between "object you can point to" and "object you cannot point to." Whether the hypertext model *intended* meta-links (links-about-links) is a semantic question the code neither enforces nor forecloses. The infrastructure supports them by doing nothing to prevent them.

---

## Summary

| Question | Answer | Where |
|---|---|---|
| Does `typeisa` distinguish document vs. link addresses? | No — `typedef tumbler typeisa` | xanadu.h:23 |
| Does `specset2sporglset()` validate the target ISA type? | No | sporgl.c:14-33 |
| Does `vspanset2sporglset()` validate the target ISA type? | No | sporgl.c:35-65 |
| Does `insertspanf()` validate `sporgladdress`? | No | spanf1.c:30-33 |
| Does `sporglset2vspanset()` validate `homedoc`? | No | sporgl.c:141-157 |
| Can `findorgl()` resolve a link's I-address? | Yes, if the orgl exists | granf1.c (findorgl) |
| Is `LINKATOM` used during retrieval? | No — allocation only | granf2.c:170 |

**A link's endset can reference another link's I-address.** The code never draws a type boundary between "addressable objects" at any point in the create-or-follow path. Given that `typeisa` is a bare tumbler with no type discriminant, and that every major conversion function passes it through without validation, this is the emergent consequence of a deliberately uniform address space — not an oversight.

---

## Question 17 [gregory]

> The type namespace lives at `1.0.2.x` in the global address space — what structure do type tumblers have, how are new types created, and is there a base set of built-in types that the system assumes?

### Gregory's Answer

## KB Synthesis

## Type Namespace Structure and Built-in Types

### Type Tumbler Structure

Type tumblers are VSpec references into a type registry embedded in the bootstrap document at address prefix `1.0.2.*`. [SS-LINK-ENDPOINT Finding 0024]

The known type addresses follow a hierarchical containment structure:

| Type | Address | Structural interpretation |
|------|---------|--------------------------|
| JUMP | `1.0.2.2` | version.0.types.2 |
| QUOTE | `1.0.2.3` | version.0.types.3 |
| FOOTNOTE | `1.0.2.6` | version.0.types.6 |
| MARGIN | `1.0.2.6.2` | version.0.types.6.subtype.2 |

The addresses `1.0.2.2`, `1.0.2.3`, `1.0.2.6` are first-level types under the type namespace. `1.0.2.6.2` (MARGIN) is a subtype — it is tumbler-contained within `1.0.2.6` (FOOTNOTE), enabling range-based subtype queries: any search for links of type `1.0.2.6` will match MARGIN links because `1.0.2.6.2` falls within the span `[1.0.2.6, 1.0.2.7)`. [SS-LINK-ENDPOINT Finding 0024, SS-TUMBLER-CONTAINMENT]

A link's type field is structurally `link.type : VSpec` where `VSpec.docid = bootstrap_doc ∧ VSpec.spans ⊆ addresses(1.0.2.*)`. Types are content references participating in the same address and identity system as all other content — they are not enums or flags. [SS-LINK-ENDPOINT Finding 0024]

### Built-in Base Set

The KB documents exactly four types from the client implementation (`QUOTE_TYPE`, `MARGIN_TYPE`, and by extension JUMP and FOOTNOTE from the address table). These are the types that `febe/client.py` constructs as VSpec objects against the bootstrap document. Whether positions `1.0.2.1`, `1.0.2.4`, `1.0.2.5`, etc. are reserved, occupied by undocumented types, or available, is **not answerable from the KB**.

### Type Creation

**Not answerable from the KB.** The KB does not document the mechanism by which new type addresses are created or registered. What is known is:

1. Type addresses exist in the bootstrap document's address space [SS-LINK-ENDPOINT Finding 0024]
2. Address allocation in general is via `findisatoinsertnonmolecule` — query-and-increment under a parent address [SS-ADDRESS-ALLOC Finding 0021]
3. Type containment (subtyping) is implicit in tumbler prefix matching, so creating a subtype of FOOTNOTE would mean allocating an address under `1.0.2.6` [SS-TUMBLER-CONTAINMENT]

Whether type creation is a privileged bootstrap-document operation, a special FEBE opcode, or simply a content insert into the type namespace is not documented in the KB.

---

## Code Exploration

Now I have everything I need. Let me synthesize the complete answer.

---

## Type Tumblers, Creation, and Built-in Types in udanax-green

### The Short Answer: `1.0.2.x` Does Not Exist in This Backend

After a full search of the source, **no such address range** is defined, initialized, or referenced anywhere in the C code. The premise that "the type namespace lives at `1.0.2.x`" comes from Xanadu conceptual specification documents, not from anything implemented in udanax-green. The backend has no "type registry" stored in the global address space at all.

What follows is what the code actually says.

---

### 1. What Structure Do Type Tumblers Have?

#### Tumbler Data Structure

Defined in `backend/common.h:59-65`:

```c
typedef struct structtumbler {
    humber xvartumbler;       /* variable-length form (unused in practice) */
    char varandnotfixed;      /* flag for variable form */
    char sign;                /* 1 if negative, otherwise 0 */
    short exp;                /* exponent, always <= 0; counts leading-zero fields */
    tdigit mantissa[NPLACES]; /* NPLACES = 16, unsigned 32-bit integers */
} tumbler;
```

`tdigit` is `UINT` (`common.h:57`). `NPLACES` was `11` originally, expanded to 16 to support deeper version chains (`common.h:53`).

#### Dot Notation

The `puttumbler` function (`backend/put.c:26-46`) prints tumblers as:

```c
for (i = tumblerptr->exp; i < 0; ++i)
    fprintf(outfile, "0.");             // leading zero fields from exp
for (i = 0; i <= place; ++i) {
    putnum(outfile, tumblerptr->mantissa[i]);
    if (i < place) putc('.', outfile);  // dot-separated mantissa
}
```

So `{exp=-0, mantissa={1,1,0,1,...}}` prints as `1.1.0.1`.

#### Four-Field Global Address Structure

Per `docs/tumbler-technical.md`, full addresses have four fields separated by `.0.`:

```
Node.0.User.0.Document.0.Element
```

Example: `1.1.0.2.0.1` = Node `1.1`, User `2`, first Document `1`. There are at most three zeros (field separators) in an address tumbler.

The only hardcoded addresses in the source:
- `backend/be.c:37`: `tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */` — Node `1.1`, User `1`
- `backend/socketbe.c:35`: `tumbler defaultaccount = {0,0,0,0, 1,1,0,14,0};` — Node `1.1`, User `14`
- `backend/do1.c:86`: `tumbler fivetumbler = {0,0,0,0,500,0,...}` — a debug constant

There is no `1.0.2` anywhere.

---

### 2. How Are New Types Created?

**There is no mechanism to create new types in udanax-green.** The type system is hardcoded as compile-time constants. What the backend calls "types" are:

#### Level 1: The `typehint` Hierarchy (Object Creation)

Defined in `backend/xanadu.h:140-153`:

```c
#define NODE      1
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4
#define TEXTATOM  1   /* atom types */
#define LINKATOM  2

typedef struct {
    INT supertype;   /* NODE=1, ACCOUNT=2, DOCUMENT=3 */
    INT subtype;     /* ACCOUNT=2, DOCUMENT=3, ATOM=4 */
    INT atomtype;    /* 0=none, TEXTATOM=1, LINKATOM=2 */
    typeisa hintisa; /* parent address */
} typehint;
```

These are validated in `backend/do2.c:86-108` (`validhint`). The constraints are:
- `supertype ∈ {NODE, ACCOUNT, DOCUMENT}` (1–3)
- `subtype ∈ {ACCOUNT, DOCUMENT, ATOM}` (2–4)
- `subtype >= supertype` and `(subtype - supertype) <= 1`
- `(subtype == ATOM) == !atomtype`

The `makehint` call at `backend/do1.c:239` for document creation:
```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
```

And at `backend/do1.c:251` for node creation:
```c
makehint(NODE, NODE, 0, &isa, &hint);
```

**New "type" addresses cannot be created** — only new instances of the four fixed types.

#### Level 2: Item Type Tags (In-Memory)

Defined in `backend/xanadu.h:26-33`:
```c
#define TEXTID    0
#define ISPANID   1
#define VSPANID   2
#define VSPECID   3
#define NODEID    4
#define ADDRESSID 5
#define SPORGLID  6
```

These are the `typeitemid` field in every in-memory struct (e.g., `typetext`, `typespan`, `typeaddress`). They are type tags in the C sense — not stored in the address space.

#### Level 3: Spanfilade Span Types

Defined in `backend/xanadu.h:36-39`:
```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

Used in `backend/spanf1.c` to identify what kind of span is being inserted into the spanfilade.

---

### 3. Is There a Base Set of Built-in Types?

Yes — the entire type system is built-in and fixed. Here is the complete inventory:

| Category | Name | Value | Where Defined |
|----------|------|-------|---------------|
| Object hierarchy | `NODE` | 1 | `xanadu.h:140` |
| Object hierarchy | `ACCOUNT` | 2 | `xanadu.h:141` |
| Object hierarchy | `DOCUMENT` | 3 | `xanadu.h:142` |
| Object hierarchy | `ATOM` | 4 | `xanadu.h:143` |
| Atom subtypes | `TEXTATOM` | 1 | `xanadu.h:145` |
| Atom subtypes | `LINKATOM` | 2 | `xanadu.h:146` |
| V-space subspaces | link subspace | `0.x` | `do1.c:393` |
| V-space subspaces | text subspace | `1.x+` | `do1.c:395` |
| Span types | `LINKFROMSPAN` | 1 | `xanadu.h:36` |
| Span types | `LINKTOSPAN` | 2 | `xanadu.h:37` |
| Span types | `LINKTHREESPAN` | 3 | `xanadu.h:38` |
| Span types | `DOCISPAN` | 4 | `xanadu.h:39` |

The system also requires at initialization:
- A valid `account` tumbler in `taskptr->account` (set in `be.c:88`)
- A `granf` (granfilade) and `spanf` (spanfilade) initialized via `inittask` (`task.c:15`)

---

### Why `1.0.2.x` Doesn't Appear

With the four-field format `Node.0.User.0.Document.0.Element`, the address `1.0.2.x` would mean Node=`1`, User=`2.x`. This is a structurally valid account address (same format as the real account `1.1.0.1` = Node=`1.1`, User=`1`). But:

1. No such account is created or referenced anywhere in the source
2. The backend stores no data about types in any granfilade entry — types are purely in-memory constants
3. All type-dispatching logic uses C `#define` constants and the `typehint.supertype/subtype/atomtype` fields, not address lookups

If the Xanadu conceptual design designated `1.0.2.x` as a type registry, **udanax-green never implemented it**. The backend's type system is a flat four-level hierarchy (`NODE > ACCOUNT > DOCUMENT > ATOM`) with two atom subtypes, all hardcoded in `xanadu.h` and validated in `do2.c:validhint`.

---

## Question 18 [gregory]

> A link orgl is stored in the granfilade alongside text content — is a link ontologically a special kind of content on the permascroll (occupying I-space positions just as characters do), or is it a categorically different entity that merely uses the same storage substrate?

### Gregory's Answer

## KB Synthesis

A link orgl is a **categorically different entity** from permascroll content — it merely uses the same storage substrate. Several KB threads converge on this.

## Different allocation paths

[SS-ADDRESS-SPACE] Finding 0077 is definitive: the granfilade dispatcher `findisatoinsertgr` routes to two distinct sub-allocators. Text uses `findisatoinsertmolecule` (TEXTATOM hint, depth 3+, content subspace). Link orgls use `findisatoinsertnonmolecule` (LINKATOM hint, the same path used for *document address allocation*). This is the machinery telling you: link orgls are structural entities, not content atoms.

## Different identity semantics

[SS-CONTENT-IDENTITY] Finding 0009 draws the sharpest line: permascroll I-addresses represent **content identity** — two documents can share the same I-address via transclusion, meaning they share the same content. Link orgl ISAs represent **object identity** — each link is a unique, non-shareable instance. [SS-CONTENT-IDENTITY] Finding 0015 reinforces: "two documents cannot 'share' a link ISA via transclusion because each link is a distinct object."

## Different V-space treatment

[SS-SUBSPACE-CONVENTION] (Findings 0009, 0010, 0038) encodes the categorical distinction directly into V-space: text lives at mantissa[0]=1, link orgls at mantissa[0]=2, link type endpoints at mantissa[0]=3. The subspace is a type discriminator. [FC-SUBSPACE] confirms these are kept structurally isolated by the two-blade knife mechanism.

## Observable consequence: the contiguity break

[INT-LINK-INSERT] Finding 0063 makes the categorical difference concrete. CREATELINK consumes I-address space in the granfilade (advancing `findpreviousisagr`'s ceiling), so a subsequent text INSERT allocates I-addresses that are non-contiguous with pre-CREATELINK text. Link orgls and text characters compete for the same monotonic allocation sequence — this is the shared substrate — but they are distinct kinds of occupants. `compare_versions` after `INSERT "ABC" → CREATELINK → INSERT "DEF"` returns **two** shared span pairs, not one, precisely because the link orgl sits between the two text runs in I-space.

## Summary

Link orgls and text share the granfilade as a storage substrate, and link orgls do occupy I-space positions (hence the contiguity effect). But ontologically they are structural objects, not content: allocated via the non-molecule path, representing unique object identity rather than shareable content identity, living in a dedicated V-space subspace, and incapable of being transcluded. The granfilade is a general-purpose enfilade that happens to host both; the categorical distinction is enforced by allocation type, V-address convention, and deref semantics, not by separate physical storage.

---

## Code Exploration

Now I have everything I need from the source code. Here is the full answer:

---

## Are Links and Text Content the Same Kind of Entity in Udanax-Green?

**Short answer: No. They share the same granfilade storage substrate and both receive I-space positions, but they are ontologically distinct. A link is not permascroll content — it is a relational entity whose I-space position names a container, not a sequence of characters.**

---

### 1. The Granfilade Type System

The granfilade has exactly two leaf types, defined at [`wisp.h:69-70`]:

```c
#define GRANTEXT  1
#define GRANORGL  2
```

Both inhabit the same node structure ([`wisp.h:94-104`]):

```c
typedef union uniongranstuff {
    typegrantext textstuff;
    typegranorgl orglstuff;
} typegranstuff;

typedef struct structgranbottomcruminfo {
    typegranstuff granstuff;
    INT infotype;       /* the discriminator: GRANTEXT or GRANORGL */
} typegranbottomcruminfo;
```

The `infotype` field is the categorical boundary. The storage is shared; the meaning is not.

---

### 2. Both Receive I-Space Positions — But For Different Reasons

`inserttextgr` ([`granf2.c:83-109`]):
```c
locinfo.infotype = GRANTEXT;
locinfo.granstuff.textstuff.textlength = textset->length;
movmem(textset->string, locinfo.granstuff.textstuff.textstring, ...);
insertseq((typecuc*)fullcrumptr, &lsa, &locinfo);   // inserts at I-space address lsa
tumblerincrement(&lsa, 0, textset->length, &lsa);   // advances by character count
```

`createorglgr` ([`granf2.c:111-128`]):
```c
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf(POOM);   // allocates a nested enfilade
...
insertseq((typecuc*)fullcrumptr, isaptr, &locinfo);    // inserts at I-space address isaptr
```

Both call `insertseq` with an I-space address. But text stores *bytes* at its I-address. A link orgl stores a *pointer to a nested POOM enfilade* — the I-address is the name of a container, not a character.

---

### 3. The I-Space Addresses Are Structurally Different

`findisatoinsertmolecule` ([`granf2.c:158-181`]) allocates I-addresses differently by atom type:

```c
} else if (hintptr->atomtype == TEXTATOM) {          // line 168
    tumblerincrement(&lowerbound, 0, 1, isaptr);     // increment in mantissa[0]
} else if (hintptr->atomtype == LINKATOM) {          // line 170
    tumblerincrement(&hintptr->hintisa, 2, 2, isaptr); // branch at mantissa[2], offset 2
    ...
}
```

`TEXTATOM` and `LINKATOM` are defined at [`xanadu.h:145-146`]:
```c
#define TEXTATOM  1
#define LINKATOM  2
```

And `doinsert` passes `TEXTATOM` while `docreatelink` passes `LINKATOM` ([`do1.c:117`] and [`do1.c:207`]):
```c
/* text: */    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
/* link: */    makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
```

Link I-addresses branch at a deeper mantissa component than text, placing them in a structurally distinct region of I-space even before V-space segregation enters the picture.

---

### 4. Links Are Segregated in V-Space, Not Just I-Space

After getting an I-address, a link is installed in the document's POOM (permutation matrix enfilade) at a V-space address explicitly reserved for links. `findnextlinkvsa` ([`do2.c:151-167`]):

```c
tumblerclear(&firstlink);
tumblerincrement(&firstlink, 0, 2, &firstlink);   // 2.0
tumblerincrement(&firstlink, 1, 1, &firstlink);   // 2.1  ← "link subspace" starts here

(void) doretrievedocvspan(taskptr, docisaptr, &vspan);
tumbleradd(&vspan.stream, &vspan.width, &vspanreach);
if (tumblercmp(&vspanreach, &firstlink) == LESS)
    movetumbler(&firstlink, vsaptr);    // first link: V = 2.1
else
    movetumbler(&vspanreach, vsaptr);   // subsequent links: append after last
```

Text content occupies V-addresses starting at 1.1. Links are kept at V ≥ 2.1. `findvsatoappend` ([`orglinks.c:37`]) names the sentinel `linkspacevstart = 2.0` and actively steers text insertions below it.

The V-address of a link is *not* a content position readable by a user. It is a slot in a metadata subspace.

---

### 5. Runtime Tests Confirm the Categorical Split

`istextcrum` and `islinkcrum` ([`orglinks.c:246-261`]):

```c
bool istextcrum(typecorecrum *crumptr) {
    if (crumptr->cdsp.dsas[V].mantissa[1] == 0 && is1story(&crumptr->cwid.dsas[V]))
        return TRUE;
    return FALSE;
}

bool islinkcrum(typecorecrum *crumptr) {
    /* if the whole crum is displaced into link space it is a link crum
     * this is true if the tumbler is a 1.n tumbler where n != 0 */
    if (crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0)
        return TRUE;
    return FALSE;
}
```

These are runtime predicates used during V-space traversal (e.g., in `maxtextwid` at [`orglinks.c:224`]) to skip link crums when computing text extent. The code does not treat them as the same kind of thing — it explicitly tests for and excludes link crums from text operations.

---

### 6. What a Link Orgl Actually Is

When `createorglgr` stores the link at an I-address, it allocates a fresh nested POOM: `createenf(POOM)` ([`granf2.c:120`]). Then `docreatelink` fills that nested POOM with the endpoints ([`do1.c:208-220`]):

```c
createorglingranf(taskptr, granf, &hint, linkisaptr)           // I-address assigned
&& tumbler2spanset(taskptr, linkisaptr, &ispanset)              // I-address as I-span
&& findnextlinkvsa(taskptr, docisaptr, &linkvsa)                // V-address in link subspace
&& docopy(taskptr, docisaptr, &linkvsa, ispanset)               // install in POOM
&& insertendsetsinorgl(taskptr, linkisaptr, link, ...)          // store from/to in nested POOM
&& insertendsetsinspanf(taskptr, spanf, linkisaptr, ...)        // index in span filade
```

`setlinkvsas` ([`do2.c:169-183`]) reveals where the endpoints live inside the nested POOM: "from" at V=1.1, "to" at V=2.1. The link's nested POOM is a private coordinate system; its V-positions address endpoint roles, not document content positions.

---

### Conclusion

A link is **not** a special kind of permascroll content. The comparison breaks down at the fundamental level:

| | Text | Link |
|---|---|---|
| `infotype` | `GRANTEXT` (1) | `GRANORGL` (2) |
| Granfilade payload | Raw bytes (characters) | Pointer to nested enfilade |
| I-address semantics | **Permascroll identity of the characters** | Name of a container/envelope |
| V-address in POOM | Content position (≥ 1.1, text subspace) | Metadata slot (≥ 2.1, link subspace) |
| `islinkcrum` test | False | True |
| Returned as | `TEXTID` | `ADDRESSID` |

Text's I-address *is* the content — the character sequence is at that position on the permascroll, permanently. A link's I-address *names* a relational entity whose content is a (from, to) pair of V-space endpoint references stored inside a nested POOM. The granfilade is the common storage substrate, and both receive I-space coordinates, but the `GRANTEXT`/`GRANORGL` discriminator encodes a genuine categorical difference that the rest of the system respects consistently.

---

## Question 19 [gregory]

> When multiple I-address spans compose an endset, does their ordering within the endset carry semantic meaning (first span is primary, etc.), or is the endset an unordered set where only membership matters?

### Gregory's Answer

## KB Synthesis

The KB does not explicitly address whether endset span ordering carries semantic primacy (e.g., "first span is primary"), but the relevant entries let me give a clear synthesis.

## Endsets are semantically sets — ordering is a V-sorted artifact

**At the I-span (internal) level**, Finding 0037 [SS-LINK-ENDPOINT] explicitly calls an endset "a set of I-spans (sporgls)." The creation path (`vspanset2sporglset` at `sporgl.c:35-65`) iterates over every I-span returned by `vspanset2ispanset` and creates one sporgl per contiguous I-address region. There is no weighting, ranking, or primacy — the loop accumulates all qualifying regions unconditionally.

**The ordering that does exist is V-sorted.** [SS-CONTEXT-LIST] (Finding 0078) establishes that `incontextlistnd()` — used during POOM retrieval — maintains ascending V-address order via insertion-sort, regardless of tree structure. Since sporgls are produced from POOM retrieval results, the I-spans in an endset will be ordered by the V-address of the content they represent in the source document.

**At the SpecSet (output) level**, [INV-SPECSET-ORDER] and [SS-SPECSET] confirm that SpecSet operations (retrieve, vcopy, compare) process VSpecs in sequence order and results are order-sensitive. But this ordering is determined by the V-sorted POOM retrieval, not by any "primary span" designation at link creation time.

## No primary-span semantics are documented

[SS-FOLLOW-LINK] (Finding 0028) and [SS-FOLLOWLINK] (Finding 0048) describe `follow_link` as returning "the complete, original SpecSet for the requested endpoint" — the full set without any filtering or ordering based on semantic priority. [PRE-FOLLOWLINK] confirms the operation has no precondition tied to endset span count or ordering.

The [EC-MULTISPAN-LINK-DUPLICATION] edge case (Finding 0019) shows that multi-span links can produce *duplicate* spans in endset results. If ordering carried semantic meaning (first = primary), duplicates would require disambiguation, but no such logic exists.

## Summary

Endset membership matters; ordering does not carry defined semantics. The V-sorted order is an implementation artifact of `incontextlistnd` [SS-CONTEXT-LIST] and should not be interpreted as expressing primacy among spans. Any code depending on "first span = primary" would be relying on an undocumented convention not supported by the KB.

---

## Code Exploration

I now have all the evidence needed for a definitive answer. Here it is:

---

## Endset Span Ordering: Semantics in udanax-green

**Short answer: The ordering of I-address spans within an endset carries no semantic meaning. The endset is an unordered set — only membership (the set of I-addresses covered) matters.**

---

### 1. The Three Endsets Are Distinguished by V-Address Range

`setlinkvsas` in `do2.c:169-182` hard-codes the starting V-addresses for the three endsets:

```c
tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);  // from-endset: V starts at 1.1
tumblerincrement (tovsaptr,   0, 2, tovsaptr);    // to-endset:   V starts at 2.1
tumblerincrement (threevsaptr,0, 3, threevsaptr); // three-endset: V starts at 3.1
```

This is what distinguishes FROM from TO from THREE. The distinction is *between* endsets, not *within* them.

---

### 2. Storage: Spans Get Sequential V-Addresses Based on Insertion Order

`insertpm` in `orglinks.c:100-131` iterates through a sporglset and inserts each I-span at the current V-address, then advances it:

```c
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);    // line 101
    movetumbler (&lstream, &crumorigin.dsas[I]);            // line 105
    movetumbler (vsaptr,   &crumorigin.dsas[V]);            // line 113
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // line 130
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);        // line 131 — advance V-cursor
}
```

The first span in the sporglset gets V-address 1.1, the second gets 1.1+width1, etc. So insertion order does determine *where* each span sits in the permutation matrix. But that V-address assignment is an implementation detail of enfilade storage, not a semantic role.

---

### 3. Retrieval: Order Is Lost — Spans Come Back Ordered by I-Address

`link2sporglset` in `sporgl.c:67-95` retrieves an endset with a single `retrieverestricted` call over the V-range of that endset:

```c
tumblerincrement (&zero, 0, whichend, &vspan.stream);  // line 81 — V-range = (whichend, 1)
tumblerincrement (&zero, 0, 1, &vspan.width);          // line 82
if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
    for (c = context; c; c = c->nextcontext) {         // line 84
        contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglptr, I); // line 86
        *sporglsetptr = (typesporglset)sporglptr;      // line 87
    }
}
```

`retrieverestricted` traverses the enfilade and returns contexts ordered by the **I-axis** value (enfilade traversal order), not by V-axis insertion order. The retrieved sporglset is therefore ordered by I-address stream value — which may differ from the original insertion sequence. Insertion order is not preserved or recoverable.

---

### 4. Link-Finding Is Purely Set-Based

`sporglset2linksetinrange` in `sporgl.c:250-268` iterates every span in the sporglset, looks up which link addresses overlap it in the spanfilade, and accumulates results. The iteration order is irrelevant — each span contributes its links to the same output set.

`onlinklist` in `spanf2.c:26-44` deduplicates by equality (`tumblereq`) as it builds the result:

```c
for (temp = *linksetptr; nextlink = temp->next; temp = nextlink) {
    if (tumblereq (&temp->address, linkisaptr))  // line 39
        return(0);  // already present — skip
}
```

No position is consulted.

---

### 5. Link Intersection Is Purely Set-Based

`intersectlinksets` in `spanf2.c:96-118` computes intersection with nested loops comparing addresses by value:

```c
for (; temp1; temp1 = temp1->next) {
    for (temp2 = linkset2; temp2; temp2 = temp2->next) {
        if (tumblereq (&temp1->address, &temp2->address)) {  // line 98
            // include in result
        }
    }
}
```

Order within each input set is irrelevant to the result.

---

### 6. The Commented-Out Consolidation Code

`orglinks.c:412-413` and `456-462` contain a commented-out (and incomplete) `consolidatespanset` function:

```c
/*consolidatespans(restrictionspanset);
foospanset("restrictionset after consolidation is ",restrictionspanset); */
```

```c
/*
consolidatespanset(spanset);
  typespan *spanset;
{
    for(;spanset->next;spanset = spanset->next){
        if(
    }
}*/
```

This was never implemented. The system works correctly without normalizing or reordering spans — further evidence that span order has no operational significance.

---

### 7. No Code Treats Any Span as Primary or Indexed

A search across all endset construction and traversal code finds:
- No index-based access (e.g., `sporglset[0]`)
- No guard that checks whether a span is first or last
- No "primary span" flag or convention
- No logic that short-circuits on the first span found

All traversals over a sporglset (endset) are uniform: `for (; sporglset; sporglset = sporglset->next)` iterating every element equivalently.

---

### Conclusion

An endset is architecturally an **unordered set of I-address spans**. The specific ordering that appears during construction (`insertpm`, `orglinks.c:100-131`) is a consequence of linked-list traversal order and determines which V-address each span occupies within the link document — but that assignment is never consulted by any higher-level operation. Upon retrieval, the original insertion order is not preserved; spans come back ordered by I-address value. All link-following (`link2sporglset`), link-finding (`sporglset2linksetinrange`), and intersection (`intersectlinksets`) operations treat the endset as a plain set: only address membership matters.

---

## Question 20 [gregory]

> Nelson described links as connecting arbitrary spans across the entire address space — was there a design constraint that both endpoints of a link must reference content that actually exists at link creation time, or can a link be created with endsets pointing to I-addresses that have not yet been allocated (forward references)?

### Gregory's Answer

## KB Synthesis

The KB documents the answer through the V-to-I conversion chain at link creation time, not through any explicit "forward reference" test.

**Link creation converts V-spans to I-spans immediately.**

When `domakelink` receives endpoint specsets, it calls `vspanset2sporglset`, which immediately invokes `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` to look up the I-addresses corresponding to those V-spans in the document's current POOM [ST-LINK-CREATE, Finding 0037]. The endset stored in the link orgl is a set of sporgls (I-address ranges), not the original V-spans. The V-spans are transient inputs to link creation; the I-addresses are what get persisted.

This means: **if the V-span doesn't map to anything in the POOM, there are no I-addresses to store.** The I-to-V filtering invariant confirms this: "If an I-address has no POOM mapping, `retrieverestricted` returns NULL and the I-address is silently dropped" [INV-ITOV-FILTERING, Finding 0048]. An endpoint specset pointing at non-existent V-positions would produce an empty sporgl set.

**The I-address space has no reservation or forward-allocation mechanism.**

I-addresses are allocated strictly during INSERT, using a stateless query-and-increment over the granfilade [SS-ADDRESS-SPACE, Finding 0061; INV-MONOTONIC]. There is no mechanism to obtain an I-address before content is placed. The allocation function `next_iaddr(granf) = max_iaddr(granf) + 1` requires content to already exist in the granfilade before the resulting I-address can be referenced [SS-ADDRESS-SPACE, Finding 0077].

**The stated precondition is content existence.**

The combined precondition from the KB is: "source content exists AND target content exists AND both endpoint widths >= 1 AND home_doc is valid" [PRE-LINK-CREATE, Finding 0028]. The zero-width crash (Bug 0017) documents that the backend does enforce at least the width check, and a zero-width endpoint is semantically equivalent to an endset pointing at nothing [PRE-ZERO-WIDTH].

**The short answer:** No forward references. Link creation is a pure V→I lookup at call time. If content doesn't exist in the POOM at that moment, the endset is empty or the operation misbehaves. The system has no "create link now, bind it to content later" mechanism — I-addresses only exist after INSERT, and that's what links actually store.

---

## Code Exploration

I now have a complete picture of the full execution path. Here is my answer:

---

## Link Creation and Forward References in udanax-green

### Short Answer

There is no hard code-level constraint requiring endset content to exist at link creation time — but the *behavior* differs depending on how endsets are specified, and one practical constraint does exist: **if endsets are given as V-specs, the referenced document must exist in the granfilade**. Content at specific V-addresses does not need to exist.

---

### Execution Path

**`fns.c:100-112`** — Top-level handler:
```c
void createlink(typetask *taskptr) {
    if (getcreatelink(taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
    && docreatelink(taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa))
        putcreatelink(taskptr, &linkisa);
    else
        putrequestfailed(taskptr);
}
```

**`get2fe.c:147-180`** — Wire protocol parsing in `getspecset()`:

Each item in a specset is prefixed on the wire with either `'s'` (SPANFLAG) or `'v'` (VSPECFLAG):
```c
if (c == SPANFLAG) {
    specset = (typespecset)taskalloc(taskptr, sizeof(typespan));
    if (!getspan(taskptr, specset, ISPANID))   // raw I-span
        return(FALSE);
} else {
    specset = (typespecset)taskalloc(taskptr, sizeof(typevspec));
    if (!getvspec(taskptr, specset))            // V-spec (docisa + vspans)
        return(FALSE);
}
```

**Both wire formats are accepted.** FEBE clients can send either raw I-spans (`ISPANID`) or V-specs (`VSPECID`) as endsets. The Python client exclusively uses V-specs (via `SpecSet(VSpec(...))`), but the protocol is not restricted to them.

---

**`do1.c:207-220`** — Core of `docreatelink()`:
```c
makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
return (
     createorglingranf(taskptr, granf, &hint, linkisaptr)   // allocate link ISA
  && tumbler2spanset(taskptr, linkisaptr, &ispanset)
  && findnextlinkvsa(taskptr, docisaptr, &linkvsa)
  && docopy(taskptr, docisaptr, &linkvsa, ispanset)
  && findorgl(taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)
  && specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)  // line 214
  && specset2sporglset(taskptr, tospecset, &tosporglset, NOBERTREQUIRED)      // line 215
  && specset2sporglset(taskptr, threespecset, &threesporglset, NOBERTREQUIRED)// line 216
  && setlinkvsas(&fromvsa, &tovsa, &threevsa)
  && insertendsetsinorgl(taskptr, linkisaptr, link, ...)
  && insertendsetsinspanf(taskptr, spanf, linkisaptr, ...)
);
```

All three endset conversions pass `NOBERTREQUIRED`. From `bert.c:52-61`:
```c
int checkforopen(tumbler *tp, int type, int connection) {
    if (type == NOBERTREQUIRED) {
        return 1;   /* Random > 0 — always passes */
    }
    ...
```
**No document needs to be open** for the endset lookup.

---

### Case 1: Raw I-span Endsets (`ISPANID`)

In `sporgl.c:19-22`:
```c
if (((typeitemheader *)specset)->itemid == ISPANID) {
    *sporglsetptr = (typesporglset)specset;
    sporglsetptr = (typesporglset *)&((typeitemheader *)specset)->next;
}
```

The I-span is accepted and threaded into the sporglset **with no existence check of any kind**. There is no call to `findorgl`, no permascroll lookup, no validation that the tumbler addresses correspond to actual allocated content. A client sending `s\n<any_tumbler>~<any_width>~` as an endset will have it stored verbatim in the link's orgl and spanfilade.

**Conclusion: Raw I-span endsets admit true forward references to unallocated I-addresses.**

---

### Case 2: V-spec Endsets, Non-Existent Document (`VSPECID`, bad docisa)

In `sporgl.c:44-46`:
```c
if (!findorgl(taskptr, granf, docisa, &orgl, type)) {
    return(NULL);
}
```

`findorgl` (`granf1.c:17-41`) calls `fetchorglgr` to locate the document's node in the granfilade. If the document doesn't exist, `fetchorglgr` returns NULL, `findorgl` returns FALSE, `vspanset2sporglset` returns NULL, `specset2sporglset` returns FALSE, and `docreatelink` fails.

**Conclusion: If endsets are specified as V-specs, the referenced document must exist in the granfilade.** This is the only hard constraint uncovered in the code.

---

### Case 3: V-spec Endsets, Document Exists but V-Addresses Have No Content

`vspanset2sporglset` (`sporgl.c:47-58`) calls `vspanset2ispanset` to translate V-coordinates to I-coordinates:
```c
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {
        // build sporgl entries
    }
}
```

`vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` queries the POOM enfilade for content at those V-coordinates. **If nothing has been written there, `retrieverestricted` returns NULL** and `ispanset` is never set. The inner loop body never executes. No sporgl entries are created for that endset. The function returns `sporglsetptr` (not NULL), so `specset2sporglset` returns TRUE.

`docreatelink` completes and succeeds, creating a link with an empty (dangling) endset.

**Conclusion: If a V-spec endset points to V-addresses with no content, the link is created with an empty endset. No failure, no error.**

---

### Critical Architectural Point: V-to-I Translation at Creation Time

The endsets are stored as **sporgls** — `(docisa, I-origin, I-width)` triples — not as V-specs. The translation from V-coordinates to I-addresses happens **at link creation time**, inside `vspanset2sporglset`. The link structure stores resolved I-coordinates, not the original V-spec.

This has a sharp implication for the "forward reference" question with V-specs: if you create a link pointing at a V-address before content is written there, the endset is stored empty. When content is later written to that V-address, following the link still returns nothing — the link was created with an empty endset and that emptiness is permanent.

Raw I-span endsets bypass this entirely: the I-address is stored directly, with no V-to-I translation and no validation. Whether that I-address will ever have content allocated to it is the client's concern, not the backend's.

---

### Summary Table

| Endset type | Document must exist? | Content must exist at V-addresses? | Forward reference to unallocated I-addr? |
|---|---|---|---|
| Raw I-span (`ISPANID`) | N/A | N/A | **Yes — no check at all** |
| V-spec (`VSPECID`) | **Yes** (`findorgl` fails otherwise) | No (empty endset stored) | Moot — V→I resolved at creation time |

**The design does not enforce that both endpoints reference existing content at link creation time.** Nelson's model of links as address-space entities is implemented permissively: a link can be created with endsets pointing to anything the client sends, including I-addresses never yet allocated. When endsets are given as V-specs, the document boundary is enforced but not the content boundary — a V-address with no content silently produces a null endset rather than a rejected request.
