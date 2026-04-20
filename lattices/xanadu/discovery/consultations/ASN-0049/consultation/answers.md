# Consultation Answers — COPY Operation (Transclusion)

**Inquiry:** What happens when content from one document appears in another without duplication? What is shared, what is independent, and what guarantees hold across the connection?
**Date:** 2026-03-18 12:49
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> When the same content appears in two documents, does the system guarantee that both documents reference one stored instance rather than maintaining separate copies?

### Nelson's Answer

## Yes — But the Guarantee Is Structural, Not About Storage Efficiency

The system guarantees that transcluded content shares a single I-space identity. This is not an optimization; it is the architecture itself.

### The Mechanism: I-Space Is Append-Only; V-Space Is Reference

Content is created once in I-space and receives a permanent address. Documents are V-space arrangements that *reference* I-space content. When document B includes content from document A, B's V-stream maps to A's I-space bytes. No duplication occurs.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The COPY operation — the mechanism for transclusion — creates a V-space mapping to existing I-space content, not a duplicate:

> "The material determined by \<spec set\> is copied to the document \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

Nelson is explicit that this eliminates copying:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

### The Guarantee Is About Identity, Not Deduplication

The deeper point: shared I-space addresses are what make attribution, royalty tracking, and version comparison *work*. The system can answer "which documents contain this content?" (FINDDOCSCONTAINING) precisely because transcluded content shares I-addresses with the original:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

If content were duplicated, this operation would be impossible — there would be no structural link between the copy and the original.

### The Critical Distinction: Transclusion vs. Independent Creation

The guarantee applies **only to content that enters the second document through transclusion** (the COPY operation or CREATENEWVERSION). If two users independently type the same words, each gets separate I-space bytes with different permanent addresses. The system distinguishes "quoted from the original" (shared I-address) from "wrote the same words independently" (different I-addresses).

This is by design. Content identity is based on *creation*, not *value*. The I-address encodes provenance — which document created which bytes — and that relationship is what makes attribution structural rather than metadata.

### Summary

| Scenario | Shared instance? | Why |
|----------|-----------------|-----|
| Transclusion (COPY) | **Yes** — V-space maps to existing I-space | The whole point of transclusion |
| New version (CREATENEWVERSION) | **Yes** — new V-arrangement over same I-content | Versions share I-space by definition |
| Independent creation of identical text | **No** — separate I-space bytes | Identity is by creation, not value |

The guarantee is not "we won't waste storage on duplicates." It is: **transcluded content maintains a permanent, structural connection to its origin that cannot be severed.** Single-instance storage is how that connection is implemented.

---

## Question 2 [nelson]

> If a document includes shared content from another document, must the origin of that content always be traceable back to the document where it was first created?

### Nelson's Answer

# Yes — Origin Traceability Is Structural and Absolute

This is one of the most fundamental guarantees of the entire system. The origin of shared content is **always** traceable to the document where it was first created, and this traceability **cannot be severed** by any operation within the system.

## The Mechanism: I-Space Addresses

Every byte ever created in Xanadu receives a permanent I-Space address — a tumbler of the form:

```
Node.0.User.0.Document.0.Element
```

The **Document field** directly encodes which document originally created that byte. This is not metadata attached to content — it IS the address. To fetch the content at all, the system must request it from its home location:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

When you transclude content into your document, you do not copy it. You create a V-space reference to the same I-space address. The fetching mechanism itself requires knowing the origin.

## The User-Facing Guarantee

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This is stated as a permanent structural property — not a feature that might be turned off, but a consequence of how the system works.

## Why This Cannot Be Severed

Content identity in Xanadu is based on **creation**, not value. Two documents containing identical text created independently have **different** I-addresses. Transcluded content **shares** the same I-address as the original. This is how the system distinguishes "wrote the same words independently" from "quoted from the original."

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The inclusion is structurally a reference to the original's I-address. The connection is the address itself — there is no way to "strip" it without destroying the reference entirely.

## The Layered Glass Metaphor

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

No matter how many layers deep the transclusion goes, each layer is transparent — you can always trace through to the original source. The glass panes don't obscure origin; they preserve it.

## What This Serves

Origin traceability is load-bearing for several other guarantees:

- **Attribution**: Authors get credit automatically because the system knows whose I-space the bytes live in
- **Royalties**: The system knows whom to pay because the Document field identifies the owner
- **Non-destruction**: Others can build upon your work "without damaging the originals" [LM 2/45] precisely because they reference your content rather than copying it
- **Verification**: Readers can always say "Show me what this originally was" and follow the reference back

> "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes." [LM 2/37]

## Summary

Yes — not merely "must" but "necessarily." The system is designed so that traceability is not a policy but a structural consequence of the addressing scheme. The I-address of every byte encodes its origin document. Transclusion works by referencing that address. The origin cannot be hidden, stripped, or falsified within the system because it is the address itself.

---

## Question 3 [nelson]

> Can a document owner control the ordering and arrangement of shared content within their document independently of how it appears in the source document?

### Nelson's Answer

**Yes, absolutely.** This is one of the most fundamental architectural properties of Xanadu. Each document has its own independent V-space arrangement, and the document owner has full control over it — regardless of how the same content is arranged in its source document.

## The Architectural Basis: I-Space / V-Space Separation

The entire Xanadu model rests on separating **content identity** (I-space) from **content arrangement** (V-space):

- **I-Space**: Where content permanently lives. Immutable. Shared across documents.
- **V-Space**: The document's current arrangement. Mutable. Per-document, per-version.

When you transclude content, you are creating a V-space mapping in *your* document that points to I-space content owned by *someone else*. Your V-space is entirely yours to arrange.

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The phrase "just as if they were native" is the key guarantee. Transcluded bytes participate in your V-space on equal footing with bytes you wrote yourself. They have positions in *your* virtual byte stream that *you* control.

## Operations Confirm Owner Control

The FEBE protocol makes this explicit. The COPY operation (which creates transclusions) places content at a V-address the owner specifies:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

The owner chooses *where* in their document the transcluded content goes. And REARRANGE lets them move it later:

> "Rearrange transposes two regions of text." [LM 4/67]

INSERT and DELETE also operate on the owner's V-space freely, regardless of whether the affected regions contain native or transcluded content.

## The Shakespeare Example

Nelson provides a vivid illustration. If *Hamlet* is already published in the system, E.G. Jewett can create his own version:

> "a quote-link to the first part of the original, just up to 'in the soliloquy'; then the word 'luge'; then a quote-link to the rest of the play." [LM 2/33]

Jewett has taken Shakespeare's content and arranged it in his own V-space — splitting it, inserting his own material between the pieces, creating a completely different arrangement than the original. The original *Hamlet* is untouched:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

## The Glass Pane Metaphor

Nelson's metaphor makes the independence visual:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

Your glass pane is *yours*. You decide where to paint, where to leave windows, and in what order. The content visible through those windows comes from elsewhere, but the arrangement of the pane itself — where each window is placed relative to your painted text — is entirely under your control.

## Compound Documents as Independent Entities

Nelson explicitly states that compound documents (those containing transclusions) are full documents with independent ownership:

> "Each compound document is like the other documents: it has an owner and receives royalties." [LM 2/33]

And the version-by-inclusion model confirms that alternative arrangements are first-class:

> "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

## Summary

The answer is an unqualified yes. V-space arrangement is per-document and under the document owner's exclusive control. What is *shared* across documents is I-space identity (the permanent bytes). What is *independent* is V-space arrangement (how those bytes are ordered and composed). This separation is the architectural core of Xanadu — it is what makes editing non-destructive, versions meaningful, and compound documents possible.

---

## Question 4 [nelson]

> When content is shared into a second document, does editing the original document's structure affect how that content appears in the receiving document?

### Nelson's Answer

## No — structural edits to the source do not affect the receiving document

The answer follows directly from Xanadu's two-address-space architecture.

### The mechanism

When Document B transcludes content from Document A, it creates a V-space mapping in B that points to I-space bytes native to A. The COPY operation "shares I-addresses with the source" — B references the same permanent bytes, not A's arrangement of them.

Editing Document A (INSERT, DELETE, REARRANGE) changes only A's V-space — its current arrangement. The I-space bytes are immutable:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

This is explicit and unambiguous. DELETE removes content from the source's view; transclusions elsewhere are unaffected.

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

While that quote is about links, the same principle applies to transclusions — both reference I-space addresses, not V-space positions.

### Why this works

The separation is fundamental to the design:

- **I-space** (permanent): content lives here forever, addresses never change
- **V-space** (ephemeral): each document arranges its own view over I-space content

Document A rearranging its V-space is like rearranging books on your shelf. Document B holds references to specific books (I-space addresses), not to shelf positions. The books don't move; only the arrangement does.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

### The two window modes — a nuance

Nelson does describe two windowing modes with different behavior regarding *content updates* (not structural rearrangement):

> "A quotation — an inclusion window — may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

A **time-fixed** window shows content as it was at a specific version — completely insulated from all changes.

A **location-fixed** window tracks a position in the source document's V-space. If the source author publishes a *new version* that reorganizes content around that location, the window could show different content. But this is a front-end presentation choice about *which version to display*, not a back-end change to the transcluded bytes.

### Summary

| Source document operation | Effect on receiving document |
|--------------------------|------------------------------|
| REARRANGE | None — I-space bytes unchanged |
| INSERT new content | None — new bytes have new I-addresses |
| DELETE content | None — bytes remain in I-space and in all transclusions |
| Publish new version | Time-fixed windows: none. Location-fixed windows: may show updated content at that position, depending on front-end resolution |

The design guarantee is clear: transclusion references permanent content identity, not ephemeral arrangement. Structural edits to the source cannot corrupt, break, or alter what the receiving document shows.

---

## Question 5 [nelson]

> Must the system preserve the identity of shared content — meaning a reader can always determine that the same content appears in multiple documents?

### Nelson's Answer

# Yes — Preserving Shared Content Identity Is Architecturally Fundamental

This is not merely a feature of Xanadu. It is the central architectural invariant from which most other guarantees flow.

## The Structural Mechanism

Xanadu separates content storage (I-space) from content arrangement (V-space). Every byte ever created has a permanent I-space address that never changes. When content appears in multiple documents, it does so through **transclusion** — inclusion by reference to the same I-space address, not duplication.

This means shared content is not merely "the same text" — it is **the same bytes at the same address**. The system distinguishes identity from coincidence:

> "Content identity is based on creation, not value. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address."
> — sporgl-provenance design intent

## The User-Facing Guarantee

Nelson states this directly:

> "This world nevertheless remains simple in design. The virtuality is simple in structure and regular in layout. You always know where you are, and can at once ascertain the home document of any specific word or character."
> — [LM 2/40]

This is not aspirational. It is a design requirement that the architecture enforces structurally:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations."
> — [LM 4/11]

When you view a compound document containing transcluded content, the system fetches that content from its home location. The fetching mechanism itself encodes the origin. Attribution cannot be severed because **the connection is the retrieval path**.

## The Explicit Discovery Operation

Nelson provides a dedicated FEBE operation for exactly this purpose:

> **FINDDOCSCONTAINING**: "This returns a list of all documents containing any portion of the material included by \<vspec set\>."
> — [LM 4/70]

This operation answers the question: "Where else does this content appear?" It works because transclusions share I-addresses — the system can trace from any content to every document that includes it.

## Why This Matters: Three Consequences

**1. Correspondence across versions.** When two versions of a document share I-space content, the system can identify which parts correspond without explicit annotation:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same."
> — [LM 2/20]

**2. Automatic royalty attribution.** The economic model depends on knowing whose content is being delivered:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically."
> — [LM 2/45]

This "determined automatically" is possible only because the system preserves content identity through I-addresses.

**3. Non-destructive quotation.** The entire publishing model rests on content identity being preserved through transclusion:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document."
> — [LM 2/36]

## The Contrast: Live vs Dead

Nelson draws a sharp line between content within the system (identity preserved) and content extracted from it (identity lost):

> "Note also that he or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy. And that will be a considerable deprivation in the world we are talking about."
> — [LM 2/48]

A copy outside the system is "frozen and dead" precisely because it severs the identity relationship. Inside the system, the identity relationship is what makes content *alive* — discoverable, attributable, compensable, and interconnected.

## Summary

The system **must** preserve the identity of shared content. This is not one guarantee among many — it is the architectural foundation. The I-space/V-space separation exists to make this possible. Transclusion depends on it. Royalties depend on it. Version comparison depends on it. Link survivability depends on it. The FINDDOCSCONTAINING operation exists to expose it. A reader can always determine that content appearing in their document originated elsewhere, trace it to its home, and discover every other document that shares it.

---

## Question 6 [nelson]

> Does the author of the original content retain any rights or privileges over that content when it appears in another author's document through sharing?

### Nelson's Answer

# Original Author's Rights Over Transcluded Content

Yes — the original author retains significant rights and privileges. This is one of Nelson's most carefully designed aspects of Xanadu. The architecture structurally guarantees these rights rather than relying on policy.

## Rights Retained

### 1. Ownership Is Never Transferred

Content included in another document remains the original author's property. Transclusion is reference, not copy — the bytes never leave the original author's I-space address.

> "Document A can include Document B, even though Document B is owned by someone else." [LM 2/35]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The compound document's author owns their arrangement and their original writing. The transcluded content remains owned by its creator.

### 2. Automatic Per-Byte Royalty

Every time the original content is delivered to a reader — even through someone else's document — the original author is paid automatically.

> "In our planned service, there is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned, as part of the proportional use of byte delivery." [LM 2/43]

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

This is proportional and automatic. If someone builds a compound document that is 70% your content and 30% theirs, you receive 70% of the royalty. No negotiation, no contracts, no tracking — the system handles it.

### 3. Structural Attribution

The original author's identity is encoded in the I-space address itself. Attribution cannot be stripped because it IS the address.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

A reader of the compound document can always identify which words came from the original author and navigate directly to the original context. This is not metadata that can be removed — it is how the system fetches the content in the first place.

### 4. Non-Destruction of the Original

The original document cannot be damaged, modified, or altered by transclusion or derivative works.

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals. This is done by inclusion links." [LM 2/45]

> "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes." [LM 2/37]

### 5. Control Over Modification and Withdrawal

Only the original owner can change or withdraw their document.

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

No one who transcludes your content gains any ability to modify it.

## What the Original Author Gives Up

There is an explicit trade-off. By publishing, the author relinquishes two things:

### 1. Permission Control Over Quotation

> "Since the copyright holder gets an automatic royalty, anything may be quoted without further permission. That is, permission has already been granted: for part of the publication contract is the provision, 'I agree that anyone may link and window to my document.'" [LM 2/45]

### 2. Control Over Incoming Links

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." [LM 2/43]

## The Design Principle

Nelson separates **control over use** from **compensation for use**. Traditional copyright conflates the two. Xanadu decouples them:

- **Control over use**: relinquished upon publication (anyone may quote, link, transclude)
- **Compensation for use**: permanently guaranteed (automatic per-byte royalty)
- **Attribution**: permanently guaranteed (structural, in the address)
- **Integrity of original**: permanently guaranteed (non-destructive architecture)

The author gives up the ability to say "no, you may not quote me" — but never gives up being paid, being credited, or having their original preserved intact.

## Summary Table

| Right | Retained? | Mechanism |
|-------|-----------|-----------|
| Ownership of content | Yes | I-space addresses are permanent |
| Per-byte royalty | Yes | Automatic with every delivery |
| Attribution | Yes | Structural (I-address encodes origin) |
| Original integrity | Yes | Append-only storage; transclusion is reference |
| Right to modify/withdraw | Yes | Only owner can change their document |
| Permission over quotation | **No** | Relinquished by publication contract |
| Control over incoming links | **No** | Relinquished by publication contract |

---

## Question 7 [nelson]

> If a document shares content from multiple sources, must the system guarantee that a reader can distinguish which portions came from which original documents?

### Nelson's Answer

# Yes — Absolutely and Structurally

This is one of the firmest guarantees in the entire system. It is not a feature bolted on; it is a consequence of the architecture itself.

## The Guarantee

> "This world nevertheless remains simple in design. The virtuality is simple in structure and repeats in layers. You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

For *any* character in *any* compound document, the system can identify which original document created it. This applies regardless of how many sources contribute content, how deeply nested the transclusions are, or how many times content has been re-transcluded.

## Why It Is Structural, Not Metadata

Every byte in the docuverse has a permanent I-space address encoding its origin:

```
Node.0.User.0.Document.0.Element
```

The Document field directly identifies which document created that byte. When content is transcluded, it is not copied — it is referenced at its permanent I-address:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The system structurally distinguishes native bytes (created in this document) from included bytes (transcluded from elsewhere). To fetch transcluded content, the system *must* request it from its home location. The connection to the source cannot be severed because the retrieval mechanism requires it.

## The Glass Pane Model

Nelson's metaphor makes the distinction visual:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

A compound document has two kinds of content:
- **Painted content** — native bytes, created by this document's author
- **Windows** — transparent openings showing content from other documents

The layering can go arbitrarily deep. Document A windows to B, which windows to C. At every layer, the system knows which glass pane each character lives on.

## Content Identity vs. Content Value

The distinction goes deeper than "where did this come from." The system distinguishes *identity* from *coincidence*:

Two documents with identical text created independently have **different** I-addresses. Transcluded content **shares** the same I-address as the original. This is how the system distinguishes "wrote the same words" from "quoted from the original" — a distinction impossible in copy-based systems.

## The Reader's Power

The reader can always investigate provenance:

> "As already stated, it is possible for the reader to ask to see the materials which are windowed to by a given document. However, it must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time." [LM 2/37-2/38]

And the FEBE protocol provides a specific operation:

> **FINDDOCSCONTAINING**: "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

This lets you trace content in either direction — from a compound document, find all sources; from a source, find all documents that include it.

## One Nuance: Display vs. Structure

Nelson distinguishes between a **quote-link** (which explicitly marks quotation to the reader) and an **inclusion** (which may not be visually indicated by default) [LM 4/53]. This means the front end may not *always* visually highlight every transcluded portion by default.

But the structural guarantee is absolute. The system *always* knows. The reader can *always* ask. The front end chooses how prominently to display provenance, but it cannot hide what the architecture makes permanently discoverable.

## Summary

The guarantee is threefold:

1. **Structural** — Every byte's I-address encodes its home document. This cannot be stripped.
2. **Queryable** — The reader can always ask "where did this come from?" for any character.
3. **Bidirectional** — From any document, find its sources; from any source, find all documents that include it.

This is not an optional feature. It falls out of the I-space/V-space separation, the transclusion-not-copying model, and the permanent addressing system. A system that copies content instead of referencing it cannot provide this guarantee. That is precisely why Nelson rejected copying.

---

## Question 8 [nelson]

> Can shared content carry its own links, and if so, must those links remain active and visible in every document where that content appears?

### Nelson's Answer

# Can Shared Content Carry Its Own Links?

The short answer: content doesn't "carry" links in Xanadu. But through I-space identity, all links connected to shared content remain discoverable everywhere that content appears.

## Links Are Independent Objects

In Xanadu, links are not embedded in content. They are separate first-class objects stored in their own home documents:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

A document has **out-links** (links stored in it) and **in-links** (links stored elsewhere that point to it):

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it." [LM 2/31]

When you transclude content from document A into document B, document A's out-links do not become document B's out-links. They remain in document A.

## But I-Space Identity Makes Links Follow Content

Here is the critical architectural point. Links attach to **I-space addresses** (permanent content identity), not V-space positions:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

Transclusion preserves I-space identity — the transcluded bytes share the same permanent addresses as the original:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

So when someone creates a link pointing to bytes in document A, and those same bytes appear in document B via transclusion, a link search on those bytes finds the link **regardless of which document the reader is viewing**. The link doesn't travel with the content — the shared I-space address means the search finds the same results from either context.

The FINDLINKSFROMTOTHREE operation searches by I-space span constraints, not by document container. If the home-set is the whole docuverse, it finds all links connected to those bytes wherever they are stored.

## Links "Reach Through" Across Versions and Documents

Nelson explicitly describes this "reaching through" behavior for versions:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

And for prismatic documents generally:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

The mechanism is the same for transclusion: shared I-space origin means links resolve across document boundaries.

## Must They Be Visible?

Nelson says readers **must be able to discover** all connections:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?' — and be shown all these outside connections without appreciable delay." [LM 2/46]

But **filtering is a front-end responsibility**:

> "This filtering by different attributes we call 'sieving', and it can only be set up for a comparatively small number of traits — say, location and author and time." [LM 2/47]

So the system guarantees **discoverability**, not mandatory display. The back end indexes all links bidirectionally. The front end decides which to show. A reader viewing transcluded content can always ask "what links connect here?" and get the full set — but the front end may filter by type, author, recency, or other criteria.

## Summary

| Question | Answer |
|----------|--------|
| Do links live inside content? | No — links are separate objects in their home documents |
| Does transclusion copy links? | No — nothing is copied; content is referenced |
| Are links discoverable on transcluded content? | Yes — shared I-space addresses mean searches find the same links |
| Must the front end show all links? | No — but it must be *able* to show them; filtering is the front end's job |
| Can links "reach through" to new contexts? | Yes — Nelson explicitly describes this for versions and transclusions |

The design is elegant: by making links point to permanent content identity (I-space) rather than ephemeral arrangement (V-space), and by making transclusion preserve that identity, links automatically follow content wherever it appears — without any special "link carrying" mechanism.

---

## Question 9 [nelson]

> Does the permanence guarantee apply equally to shared content and to content that exists in only one document, or can shared content ever become unavailable?

### Nelson's Answer

## Permanence and Shared Content

The short answer: the permanence guarantee applies to **all published content equally**, but shared content actually has **stronger practical protection** because others' property depends on it.

### The Blanket Rule

Nelson states the permanence guarantee as a universal principle applying to all published content:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

This applies regardless of whether anyone has linked to or transcluded the content. Publication itself is the trigger.

### Shared Content Has Stronger Protection

While the rule covers all published content, Nelson's **justification** for it is precisely that sharing creates dependency. When others link to or transclude your content, their property depends on yours:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

Transclusion makes this dependency structural. Non-native bytes are "obtained by front-end or back-end requests to their home locations" [LM 4/11]. If document A transcludes from document B, A's content literally requires B's I-space to be accessible. Withdrawing B would not merely break a navigational convenience — it would destroy part of A's content.

### The Economic Tension

There is one area where Nelson's design creates an unresolved vulnerability for all content, shared or not. Storage requires **ongoing payment**:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Nelson specifies ongoing storage rental paid by the owner. He does **not** specify what happens when that payment lapses. This creates a gap: the permanence guarantee says you cannot *voluntarily withdraw* published content, but what if you simply stop paying?

For shared content, this gap is arguably more dangerous than for unshared content, because a lapse in one owner's payment could cascade — breaking transclusions in many other documents simultaneously.

### The Hierarchy of Protection

Reading across the curated sources, there is an implicit hierarchy:

| Content State | Permanence | Basis |
|---|---|---|
| Published + actively shared (linked/transcluded) | Strongest | Contractual + others' property depends on it |
| Published + not yet shared | Strong | Publication contract prevents withdrawal |
| "Privashed" (private with unrestricted access) | Weak | Owner can withdraw at any time; "no recourse" for linkers |
| Private | None (to others) | Owner has full control |

Nelson explicitly designed "privashing" as an escape valve for those unwilling to accept the permanence obligation:

> "An author who wishes to render his work universally available, but wishes also to retain the right to withdraw it at any time, has a simple means for so doing. The author simply designates his or her document as a private document with unrestricted distribution." [LM 2/48]

The tradeoff is explicit: no royalties, and anyone who linked to privashed content has no recourse.

### I-Space vs. Accessibility

It is worth distinguishing two senses of "available":

1. **I-space existence**: Content in I-space is permanent by architecture. DELETE removes from V-space only — "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions)" [LM 4/9]. Even "deleted" content remains in I-space and can be reached through other versions or historical backtrack. This applies equally to all content.

2. **Network accessibility**: Whether content can actually be retrieved across the network depends on the storage vendor remaining operational and the owner maintaining storage rental. Nelson provides some protection through vendor contracts — "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations" [LM 5/16] — and through distributed backup. But the economic sustainability question remains unresolved.

### Conclusion

Nelson designed the system so that **shared content can never become unavailable through the owner's voluntary action** — the publication contract forbids it, precisely because others depend on it. The permanence guarantee applies to all published content, but sharing creates the moral and practical foundation for that guarantee.

The one scenario Nelson does not fully address is **involuntary unavailability** — what happens when an owner cannot or does not pay storage costs. In this scenario, shared content is more vulnerable than unshared content in one sense (more downstream damage) but also more likely to be preserved in another (greater incentive for the network to maintain it, and its bytes may exist in backup copies across multiple vendors).

---

## Question 10 [nelson]

> When content is shared rather than copied, must the system guarantee that all parties see identical content, or can the receiving document present a version that diverges over time?

### Nelson's Answer

## Shared Content: Identity vs. Arrangement

The answer is precise and has two layers, because Xanadu separates **content identity** (I-space) from **content arrangement** (V-space).

### Layer 1: Bytes Are Immutable — Always Identical

At the I-space level, there is no possibility of divergence. Content at an I-address never changes. When a receiving document transcludes bytes, it references their permanent I-address, and those bytes are fetched from their home location:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The system does not copy bytes into the receiving document. It references them. Everyone who references I-address X sees the same bytes at X, always.

### Layer 2: Windows Can Diverge by Design — Two Explicit Modes

However, the *source document's arrangement* can change (its V-space evolves through editing and versioning). Nelson explicitly provides **two window modes** that handle this differently:

> "A quotation — an inclusion window — may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

**Location-fixed (floating in time):** The receiving document tracks the source's current arrangement. Updates propagate automatically. All parties see the same current state. This is Nelson's solution to the distributed update problem:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." [LM 2/36]

**Time-fixed (fixed in time):** The receiving document freezes at a specific version. The source may evolve, but the window shows what it showed at the moment of citation. The user can explicitly ask to see the current state, but divergence is the default behavior in this mode.

### So: Divergence Is Permitted, But Not Silent

The system guarantees that:

1. **Bytes are always identical** — I-space content is immutable
2. **Location-fixed windows track the source** — no divergence
3. **Time-fixed windows deliberately diverge** — but the user can always query "What has this passage become?"
4. **You always know where you are** — attribution is structural, so even in a divergent window, you can trace back to the source and compare

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

The critical design insight: divergence in Xanadu is never *accidental* or *hidden*. It is either (a) impossible (I-space immutability) or (b) an explicit user choice (time-fixed windowing) with a built-in mechanism to reconcile ("What has this passage become?"). The receiving document cannot *silently* present different content from the source — either the window tracks the source, or the window is frozen at a declared point in time, and the system knows the difference.

### What About Derivative Documents?

There is a third case. A user can create a **derivative document** that explicitly modifies transcluded content:

> "A particular form of compound document is one which consists explicitly of an original and changes to it — which may be made by anyone." [LM 2/38]

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

Here, the derivative document *does* present different content — but the original is untouched, and the reader can always navigate back:

> "The old viewpoint is still present too — you can always say, 'Show me what this originally was.'" [LM 2/45]

### Summary

| Scenario | Divergence? | Guarantee |
|----------|-------------|-----------|
| Same I-address bytes | Never | I-space is immutable |
| Location-fixed window | No | Tracks source automatically |
| Time-fixed window | Yes, by design | User can query current state |
| Derivative document | Yes, by design | Original always accessible |

The system never allows *silent, undetectable* divergence. It either prevents it (immutable bytes), or makes it explicit and traceable (frozen windows, derivative documents with navigable originals).

---

## Question 11 [gregory]

> When `docopy` creates a new POOM entry in the target document, does the bottom crum's I-displacement point to the exact same I-address as the source POOM entry, or is there any indirection or remapping layer between the source's I-address and the target's?

### Gregory's Answer

## KB Synthesis

**Direct answer: The I-displacement in the target POOM bottom crum is the exact same I-address as in the source — no indirection, no remapping.**

## Mechanism

The call chain makes this explicit [ST-VCOPY, Finding 0046]:

```
docopy(src, dst, vsa, ispanset)
  → insertpm(dst, vsa, ispanset)
  → insertnd(...)
  → isanextensionnd() or new crum creation
```

The sporgl is the carrier [INT-SPORGL-TRANSCLUSION]:

> "During vcopy, the data flow is: source V-spec → sporgls (via `vspanset2sporglset`) → `insertpm` into destination document. The sporgl carries the content's I-address identity through the copy operation. Because the sporgl preserves the original I-address (not a new one), the destination document ends up referencing the same content identities as the source."

The resulting bottom crum [SS-POOM-BOTTOM-CRUM] has:
- `cdsp.dsas[I]` = the I-address extracted from the source POOM — the **binary tumbler value is copied directly**
- `cdsp.dsas[V]` = the target V-position (re-encoded at V-space precision per [SS-INSERT-VWIDTH-ENCODING])

## No New Allocation

`docopy` never calls `findisatoinsertgr` or `inserttextingranf`. Contrast with INSERT, which calls those to allocate fresh I-addresses. [INV-IADDR-PROVENANCE]:

> "Every I-address has exactly one native document — the document where INSERT first allocated it. COPY does not allocate new I-addresses; it creates V→I mappings that reference existing ones."

## The `homedoc` Field

The `isanextensionnd` check [ST-VCOPY, Finding 0046] uses the `homedoc` field to test I-address origin — and this field records the **original allocation document**, not the current copy source. After a chain of three COPYs (A → B → C → D), the bottom crum in D's POOM still has `homedoc = A`. This is what makes transitive I-address contiguity work (or fail to consolidate across different origins).

## What Confirms This

[ST-COPY, Finding 0064]:

> "COPY is the identity-preserving operation... COPY shares the source's existing I-addresses in the target document's POOM via `insertpm`. When used to 'undelete' content... COPY restores both the V-space content AND the I-space identity."

[INV-TRANSITIVE-IDENTITY] — transitive transclusion works exactly because the I-addresses flow unchanged through the chain. If there were any remapping layer, the I-address intersection in `find_links` and `compare_versions` would break.

**Conclusion:** The target POOM bottom crum's `cdsp.dsas[I]` is the same tumbler bit-pattern as in the source entry. The sporgl is the literal carrier of that address through the copy path, and `insertpm` writes it directly into the new crum without transformation.

---

## Code Exploration

I now have everything needed to answer definitively. Here is the full analysis.

---

## Answer: I-Address in `docopy` — Direct Reference, No Remapping

The bottom crum in the target POOM gets the **exact same I-address** as the source. There is no indirection, offset, or remapping layer. Here is the full call chain with citations.

---

### Step 1 — `docopy` converts V-specs to I-spans

`do1.c:53-64`:
```c
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
...
/* the meat of docopy: */
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
...
```

The `specset` parameter is typically a `VSPECID` (V-addresses in the *source* document). `specset2ispanset` converts them to I-spans by calling `vspanset2ispanset` → `permute(..., V, ispansetptr, I)` — walking the **source document's POOM** to find which I-addresses back those V-positions [`do2.c:34-38`]:
```c
findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
&& (ispansetptr = vspanset2ispanset (taskptr, docorgl, 
                    ((typevspec *)specset)->vspanset, ispansetptr))
```

The resulting `ispanset` contains the **raw permascroll I-addresses** of the content. These are copied verbatim — `permute` does not relativize or offset them.

---

### Step 2 — `insertpm` builds the new crum from those I-addresses

`orglinks.c:100-131`:
```c
for (; sporglset; sporglset = ...) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);   // extracts I-addr

    movetumbler (&lstream, &crumorigin.dsas[I]);   // I-address goes in directly
    movetumbler (&lwidth,  &crumwidth.dsas[I]);    // I-width goes in directly
    movetumbler (vsaptr,   &crumorigin.dsas[V]);   // target V-address

    shift = tumblerlength (vsaptr) - 1;
    inc   = tumblerintdiff (&lwidth, &zero);
    tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]); // derives V-width

    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);  // advance V for next span
}
```

`lstream` is placed **directly** into `crumorigin.dsas[I]` with a plain `movetumbler` — a raw value copy with no arithmetic.

---

### Step 3 — `unpacksporgl` confirms no transformation on the I-side

`sporgl.c:178-202`. For an ISPANID element (which is what `specset2ispanset` produces):
```c
if (((typeitemheader *)sporglptr)->itemid == ISPANID) {
    movetumbler (&((typeispan *)sporglptr)->stream, streamptr);  // straight copy
    movetumbler (&((typeispan *)sporglptr)->width,  widthptr);
    tumblerclear (&infoptr->homedoc);                            // no home doc
}
```

No addition, no indirection. The `stream` field — which is the I-address produced by `permute` from the source POOM — passes through unchanged as `lstream`, and then becomes `crumorigin.dsas[I]` in the new target crum.

---

### Step 4 — `isanextensionnd` shows I-address identity is the crum's identity

`insertnd.c:301-309`: when deciding whether to extend an existing crum rather than create a new one, the check is:
```c
bool isanextensionnd(typecbc *ptr, ..., type2dbottomcruminfo *infoptr)
{
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, dspsize(ptr->cenftype)));
}
```

Two POOM entries are considered the *same run* of I-space only if they share the same `homedoc` and are I-address-contiguous. This only makes sense because I-addresses in both source and target POOMs are the same permascroll-absolute values.

---

### Conclusion

When `docopy` creates a new POOM entry in the target document:

1. The input V-addresses (in the source document) are **translated to I-addresses** by walking the *source document's* POOM via `specset2ispanset` / `vspanset2ispanset` / `permute`.
2. Those I-addresses are then placed **verbatim** into `crumorigin.dsas[I]` of the new target crum — `movetumbler` with no arithmetic [`orglinks.c:105`].
3. The only thing that changes is the `dsas[V]` component — the target V-address, supplied by the caller as `vsaptr`.

The target POOM crum's I-displacement points to the **identical permascroll I-address** as the source POOM crum. There is no indirection, remapping, or offset layer between them. Both documents' POOM trees point to the same I-space location; only the V-space position differs. This is the structural mechanism that makes transclu- content-sharing possible in udanax-green.

---

## Question 12 [gregory]

> If document B transcludes a span from document A, and then document C transcludes the same span from document B, does C's POOM reference the original I-addresses from A's granfilade entry — making the transclusion chain A→B→C fully transparent to `find_links` — or does the second copy introduce any new identity?

### Gregory's Answer

## KB Synthesis

Yes — the chain is fully transparent. C's POOM entries reference A's original I-addresses directly, with no new identity introduced at any hop.

## Mechanism

When B transcludes a span from A, the call chain is:

```
source V-spec → vspanset2sporglset(B_or_A) → insertpm(C's POOM)
```

`vspanset2sporglset` converts B's V-span to sporgls by reading B's POOM — which maps B's V-positions to A's original I-addresses [INT-SPORGL-TRANSCLUSION]. The sporgl carries those I-addresses (the `sporglorigin` field) unchanged into `insertpm`. No allocation step occurs; `docopy` shares existing I-addresses rather than calling `findisatoinsertgr` [ST-COPY, Finding 0064].

So after A→B transclusion:
- `poom(B)[v_b] = I_a` (A's original I-address)

After B→C transclusion, `vspanset2sporglset` runs against B, reads the same `I_a` from B's POOM, and writes it into C:
- `poom(C)[v_c] = I_a` (still A's original I-address)

The chain telescopes to a single flat identity assignment: C holds A's I-addresses without any intermediate layer.

## Consequence for `find_links`

`find_links` operates purely on I-address intersection in the spanf enfilade [SS-FIND-LINKS, Finding 0028]. Since C holds `I_a`, and the spanf was indexed on `I_a` when the link was created on A's content, `find_links` on C returns the link.

This is the mechanism behind [INV-TRANSITIVE-IDENTITY] (confirmed experimentally as Finding 0018, Key Finding 6):

> "If A transcludes from B, and B transcludes from C, then A and C share content identity... `FINDDOCSCONTAINING` and `compare_versions` both respect this transitivity."

And [INT-LINK-TRANSCLUSION] (Finding 0008) confirms the same holds for link discovery across arbitrarily long transclusion and version chains.

## No new identity is ever created

[ST-VCOPY] states the postcondition explicitly: vcopy creates **no new content identities**. [INV-IADDR-IMMUTABILITY] guarantees I-addresses are permanent and immutable — there is nothing to substitute at each hop. The transclusion chain A→B→C is semantically equivalent to A→C directly from the perspective of `find_links`, `compare_versions`, and `find_documents`.

---

## Code Exploration

I now have all the pieces. Let me write the complete answer.

---

## Transclusion Chain Transparency: A→B→C in udanax-green

**Short answer:** C's POOM references A's original I-addresses, without any intermediate identity. The chain A→B→C is fully transparent to `find_links`. No new identity is introduced at the second copy.

---

### 1. How I-addresses originate: text insertion into A

When text is first inserted (`doinsert`, `do1.c:87`):

```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)
```

`inserttextingranf` (→ `inserttextgr`, `granf2.c:83`) calls `findisatoinsertgr` to allocate a new tumbler address `lsa` in the global granfilade, stores the bytes there, and returns an `ispanset` whose `stream` is that address:

```c
movetumbler (&spanorigin, &ispanptr->stream);   // granf2.c:105
tumblersub (&lsa, &spanorigin, &ispanptr->width); // granf2.c:106
```

This `ispanset` is the I-address: **a permanent, globally unique permascroll coordinate for the bytes**. Nothing else assigns or reassigns I-addresses. The granfilade entry is never duplicated.

---

### 2. A's POOM is populated: `insertpm`

`docopy` then calls `insertpm` (`orglinks.c:75`):

```c
unpacksporgl (sporglset, &lstream, &lwidth, &linfo);  // orglinks.c:101
movetumbler (&lstream, &crumorigin.dsas[I]);           // orglinks.c:105 — I-axis = I-address
movetumbler (vsaptr,   &crumorigin.dsas[V]);           // orglinks.c:113 — V-axis = V-address in A
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // orglinks.c:130
```

A's POOM now holds a crum mapping: **V-address-in-A ↔ I-address**.

---

### 3. B transcludes from A: `specset2ispanset` traverses A's POOM

`docopy` (`do1.c:45`) begins with:

```c
specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
```

`specset2ispanset` (`do2.c:14`) handles a VSPECID by:

```c
findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)  // do2.c:35
&& (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr))  // do2.c:36
```

`vspanset2ispanset` (`orglinks.c:397`):

```c
return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
```

`permute` (`orglinks.c:404`) traverses A's POOM restricted to the requested V-span and returns the corresponding I-spans. **The result is A's original permascroll I-address.**

Then `insertpm` writes B's POOM with:
- `crumorigin.dsas[I]` = **A's I-address** (from the permute result)
- `crumorigin.dsas[V]` = B's V-address

**B's POOM contains no new identity. It stores A's original I-address in its I-dimension.**

---

### 4. C transcludes from B: the same path, one level deeper

When C transcludes from B, `specset2ispanset` is again called, this time with B's POOM:

```c
vspanset2ispanset(taskptr, docorgl_B, B_vspanset, ispansetptr)  // do2.c:36
→ permute(taskptr, docorgl_B, B_vspanset, V, ispansetptr, I)     // orglinks.c:404
```

B's POOM maps B's V-address to A's I-address (written in step 3). **`permute` returns A's original I-address directly** — there is no second lookup into the granfilade.

C's `insertpm` then writes:
- `crumorigin.dsas[I]` = **A's I-address** (unchanged from step 3)
- `crumorigin.dsas[V]` = C's V-address

**C's POOM also contains A's original I-address. The second hop introduces no new identity.**

---

### 5. The spanfilade: both B and C indexed by A's I-address

`insertspanf` (`spanf1.c:15`) is called for both B and C with `ispanset` = A's I-address:

```c
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);   // spanf1.c:49 — key = I-address
movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);  // spanf1.c:51
```

The ORGLRANGE dimension carries B's ISA (for the B entry) and C's ISA (for the C entry). Both entries are indexed by A's I-address in the SPANRANGE dimension.

---

### 6. `find_links` is transparent: I-address is the only key

`dofindlinksfromtothree` (`do1.c:348`) → `findlinksfromtothreesp` (`spanf1.c:56`):

```c
specset2sporglset (taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);  // spanf1.c:71
sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);  // spanf1.c:77
```

`specset2sporglset` (`sporgl.c:14`) → `vspanset2sporglset` (`sporgl.c:35`):

```c
vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);         // sporgl.c:48
movetumbler(docisa,          &sporglset->sporgladdress);        // sporgl.c:53
movetumbler(&ispanset->stream, &sporglset->sporglorigin);       // sporgl.c:54
```

Whether you query from A, B, or C, the `sporglorigin` ends up as A's I-address (after passing through the respective POOM).

`sporglset2linksetinrange` (`sporgl.c:239`) then searches the spanfilade:

```c
if (FALSE/*trying to kluge links followable thru versions */&&...) {
    infoptr = &linfo; ...
} else
    infoptr = NULL;  // sporgl.c:254-255
...
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
// sporgl.c:259
```

The `if (FALSE ...)` permanently disables homedoc filtering. `infoptr = NULL`. The search key is **only the SPANRANGE dimension** — which is A's I-address. The spanfilade returns all ORGLRANGE entries (link ISAs) whose SPANRANGE overlaps the queried I-address, regardless of which document (A, B, or C) holds the content.

**Links attached to content in A, B, or C are all findable from any of the three perspectives**, because all three reference the same I-address.

---

### Summary

The transclusion chain A→B→C is **fully transparent** to `find_links` by design:

| Layer | What's stored |
|-------|--------------|
| Granfilade | Text bytes at I-address (only ever written once, by `inserttextgr`) |
| A's POOM | `V_A ↔ I_A` |
| B's POOM | `V_B ↔ I_A` (A's I-address — from `permute` over A's POOM) |
| C's POOM | `V_C ↔ I_A` (A's I-address — from `permute` over B's POOM) |
| Spanfilade | A's I-address indexed, carrying A's ISA, B's ISA, and C's ISA as ORGLRANGE entries |

The POOM is a permutation matrix (V↔I mapping), not a content store. Each transclusion hop adds a new V-axis entry pointing at the pre-existing I-address. `vspanset2ispanset` (`orglinks.c:397`) collapses the chain in one step — it traverses the POOM of whichever document you name, and falls straight through to the original permascroll I-address.

**No new identity is created at the second copy.** C holds no I-address of its own for the transcluded content — only a V-address within its own document space. The I-address remains A's, permanently.

---

## Question 13 [gregory]

> When `isanextensionnd` detects that a COPY's I-addresses are contiguous with an existing POOM entry in the target document, it coalesces them into a single crum — does this silent merging ever cause problems for `retrievedocvspanset` or `compare_versions`, where the system might need to distinguish separately-copied spans that happened to be I-address-adjacent?

### Gregory's Answer

## KB Synthesis

No, the silent coalescing never causes problems for either operation. Here's why:

**`isanextensionnd` only coalesces when both conditions hold:**

From `[ST-VCOPY]` (Finding 0046): extension requires (1) same `homedoc` (I-address origin document) AND (2) contiguous in both V and I dimensions. The `homedoc` field records which document originally allocated the I-addresses — not which document the content was copied *from* most recently.

This guard prevents the problematic case. If you copy "AB" from source S1 and then "CD" from source S2, even if those I-addresses happen to be numerically adjacent and the V-positions are contiguous, they have different homedoc values and are never merged. Cross-provenance spans stay separate.

**For `retrievedocvspanset`:**

Coalescing of adjacent same-homedoc content is not an information loss — it is the explicitly intended behavior. `[INV-VSPAN-CONSOLIDATION]` states this directly: "the span representation returned by retrieve_vspanset is always maximally consolidated — adjacent spans with consecutive V-positions are merged." This is an invariant, not a side effect. Two separately-copied but I-address-contiguous spans from the same source *are* the same logical block of content; consolidating them is semantically correct.

**For `compare_versions`:**

From `[SS-COMPARE-VERSIONS]` (Finding 0015) and `[INT-SPORGL-VERSION-COMPARE]`, the operation works via I-address intersection: V-spans are converted to I-spans via sporgls, then intersected. Crum structure is invisible to this path — the I-address range produced by one coalesced crum is identical to the union of two separate crums covering the same range. The comparison result is the same either way.

**The one scenario that might look suspicious:**

If document T copies "AB" (i1–i2) from S at V 1.1, then separately copies "CDE" (i3–i5) from S at V 1.3, and these are I-address-contiguous and V-address-contiguous, coalescing produces one crum [V 1.1, V 1.6) → [i1, i5]. `compare_versions(T, S)` finds one large shared span. This is correct — T genuinely shares that entire contiguous I-address range with S. There is nothing to distinguish about the assembly history; Xanadu's content identity model (`[INV-CONTENT-IMMUTABILITY]`) concerns *which* I-addresses are present, not *how many operations* placed them there.

The `homedoc` guard is the key: it ensures that only content of genuinely identical provenance ever gets coalesced, making the merge semantically lossless for both retrieval and comparison purposes.

---

## Code Exploration

Now I have everything needed for a complete, sourced answer.

---

## Answer: `isanextensionnd` Coalescing and Its Effects on `retrievedocvspanset` and `compare_versions`

### The Coalescing Mechanism

`isanextensionnd` [insertnd.c:301–309] fires inside `insertcbcnd` [insertnd.c:242–275] during POOM insertion. When it returns TRUE, the new span is silently absorbed into the existing crum by extending its width rather than creating a new node:

```c
// insertnd.c:250-258
if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
    dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
    ivemodified (ptr);
    setwispupwards (father,1);
    ...
    return(FALSE);
}
```

The coalesce condition is:

```c
// insertnd.c:301-309
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr,
                     type2dbottomcruminfo *infoptr)
{
    if (!tumblereq(&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq(reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

Two conditions must hold simultaneously:

**Condition 1 — Same `homedoc`.** The source document of the new insertion must match the existing crum's `c2dinfo.homedoc`.

**Condition 2 — 2D adjacency in BOTH I and V.** The key is `dspsize(POOM)`. From [wisp.h:26–27]:

```c
#define DSPSIZEPM 2
#define dspsize(A) ((A)==GRAN?DSPSIZEGR:((A)==SPAN?DSPSIZESP:DSPSIZEPM))
```

`DSPSIZEPM = 2`, so `lockeq` [wisp.c:261–266] compares **both** `dsas[I]` and `dsas[V]` of the reach vs. the new origin. Coalescing only fires when the existing crum ends at exactly the same point in BOTH I-space AND V-space as the new insertion begins.

---

### Why the 2D Adjacency Condition Is the Load-Bearing Safety Invariant

Each POOM bottom crum created by `insertpm` [orglinks.c:75–134] has equal I-width and V-width. `insertpm` sets them together:

```c
// orglinks.c:115-117
inc = tumblerintdiff (&lwidth, &zero);
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
```

This encodes a **stride-1** linear mapping between I-space and V-space inside every crum. A crum with absolute grasp (I=i₁, V=v₁) and width w represents the bijection: V-position v₁+k ↔ I-position i₁+k for k ∈ [0, w).

When `isanextensionnd` fires on two crums A and B:
- Crum A: V=[v₁, v₁+w₁), I=[i₁, i₁+w₁)
- Crum B: V=[v₁+w₁, v₁+w₁+w₂), I=[i₁+w₁, i₁+w₁+w₂)

The 2D adjacency condition guarantees A's reach equals B's origin in **both** dimensions. After coalescing to V=[v₁, v₁+w₁+w₂), I=[i₁, i₁+w₁+w₂):

- For any k < w₁: V↔I via merged crum = i₁+k = same as A alone ✓
- For any k ≥ w₁: V↔I via merged crum = i₁+k = i₁+w₁+(k-w₁) = same as B alone ✓

The linear formula **remains continuous and correct** across the join point because the 2D adjacency requirement is exactly the condition that makes this true.

---

### Effect on `retrievedocvspanset`

`doretrievedocvspanset` [do1.c:322–336] calls `retrievevspansetpm` [orglinks.c:173–221], which reads **only the POOM root's top-level summary**:

```c
// orglinks.c:184-190
if (is1story (&ccptr->cwid.dsas[V])) {
    vspan.itemid = VSPANID;
    movetumbler (&ccptr->cdsp.dsas[V], &vspan.stream);
    movetumbler (&ccptr->cwid.dsas[V], &vspan.width);
    ...
}
```

Internal tree structure — whether a range is stored as one merged crum or two separate crums — is completely invisible here. The root's `cwid` summary reflects the same total V-coverage either way.

**Verdict: coalescing is irrelevant to `retrievedocvspanset`.**

---

### Effect on `compare_versions`

`doshowrelationof2versions` [do1.c:428–449] follows this pipeline:

```
filter_specset_to_text_subspace
  → specset2ispanset [do2.c:14–46]
    → vspanset2ispanset [orglinks.c:397–402]
      → permute [orglinks.c:404–422]
        → span2spanset [orglinks.c:425–454]
          → retrieverestricted [retrie.c:56–85]
            → findcbcinarea2d [retrie.c:229–268]
              → makecontextfromcbc [context.c:151–174]
              → incontextlistnd [context.c:75–111]
          → context2span [context.c:176–212]
```

`findcbcinarea2d` walks the POOM tree to bottom crums that intersect the query V-range, then `context2span` clips each crum to the queried sub-range:

```c
// context.c:191-203
if (tumblercmp (&grasp.dsas[idx1], &lowerbound) == LESS) {
    tumblerincrement (&grasp.dsas[idx2], 0,
                      (INT)tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
                      &grasp.dsas[idx2]);
}
if (tumblercmp (&reach.dsas[idx1], &upperbound) == GREATER) {
    tumblerincrement (&reach.dsas[idx2], 0,
                      -tumblerintdiff(&reach.dsas[idx1], &upperbound),
                      &reach.dsas[idx2]);
}
```

This is linear arithmetic. For a merged crum spanning V=[v₁, v₁+w₁+w₂), I=[i₁, i₁+w₁+w₂), a query for V=[v₁+w₁, v₁+w₁+w₂) clips:
- Bottom: `grasp.dsas[I]` advances by `w₁` → yields i₁+w₁
- Top: no clip needed
- Result: I=[i₁+w₁, i₁+w₁+w₂)

This is **identical** to what two separate crums would produce. The merged crum cannot be distinguished from the pair.

**Verdict: coalescing is transparent to `compare_versions`.**

---

### The One Real Information Loss — and Why It Doesn't Matter

After coalescing, the merged crum retains `c2dinfo.homedoc` (source document identity) but loses track of the **source V-positions** of the two contributing spans. The `type2dbottomcruminfo` struct [crum.h:107–110] holds only `homedoc`:

```c
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;
} type2dbottomcruminfo;
```

If you copy source V=[1,3) and then source V=[10,13) from the same document into a target consecutively — and the underlying I-addresses happen to be contiguous — the resulting POOM cannot distinguish "these came from two non-contiguous source locations."

But **`compare_versions` doesn't need to distinguish this**. Its job is to find common I-addresses between two versions. The I-coverage of the merged crum is correct. The back-mapping from I-addresses to source V-positions is performed by querying the **source document's** POOM (via `ispan2vspanset` on the source orgl in `restrictvspecsetovercommonispans` [correspond.c:52–80]), which was never modified during the copy. The source POOM correctly records whether those I-addresses came from V=[1,3) and V=[10,13) as separate non-contiguous regions.

The target POOM's coalesced crum records only that I=[100,106) occupies V=[1,6) in the target — which is correct. The source structure is preserved in the source document.

---

### Conditions Under Which Problems WOULD Arise

There is one hypothetical edge that would be unsafe: if two crums from **different** V→I linear offsets ended up satisfying the `isanextensionnd` condition. But this is ruled out by the 2D check. To satisfy `lockeq(..., dspsize(POOM))` [insertnd.c:308, wisp.h:26]:

> Both the I-reach and the V-reach of the existing crum must equal the I-origin and V-origin of the new insertion.

Combined with the stride-1 invariant from `insertpm`, this condition is the **unique** relationship that makes the two crums representable as a single contiguous parallelogram. Any configuration that would produce incorrect `context2span` output necessarily fails this 2D check and is never coalesced.

---

### Summary Table

| Caller | How it uses POOM | Affected by coalescing? |
|--------|-----------------|------------------------|
| `retrievedocvspanset` → `retrievevspansetpm` | Reads root `cwid.dsas[V]` only | **No** — invisible |
| `compare_versions` → `findcbcinarea2d` | Walks to bottom crums | **No** — `context2span` linear clipping handles merged crums correctly |
| `context2span` clipping logic | Linear I↔V arithmetic | **No** — 2D adjacency condition preserves linear stride-1 map |

The silent merging is safe by construction. `isanextensionnd`'s 2D adjacency gate (`dspsize(POOM) = 2` in `lockeq`) is precisely calibrated to admit only merges that preserve the linear V↔I bijection that the rest of the system assumes.

---

## Question 14 [gregory]

> Does `insertspanf` create one DOCISPAN entry per COPY operation in the target document, or does it create one entry per contiguous I-span within the copied specset — and if the source specset contains three non-contiguous I-ranges, does the target get exactly three DOCISPAN entries?

### Gregory's Answer

## KB Synthesis

`insertspanf` creates one DOCISPAN entry **per contiguous I-span**, not per COPY operation. A specset covering three non-contiguous I-ranges produces exactly three DOCISPAN entries.

The mechanism is documented in [SS-DOCISPAN] (Finding 0047):

> `insertspanf` iterates over the `ispanset` linked list and makes one `insertnd` call per `typeispan` struct. Each `typeispan` represents a contiguous range of I-addresses with a `stream` start and `width`.

The loop in `spanf1.c:15-53` is:
```c
for (; sporglset; sporglset = next) { ... insertnd(...); }
```
— one `insertnd` per I-span, not per operation.

**What determines the I-span count?** The conversion upstream. `docopy` calls `specset2ispanset`, which converts V-spans to I-spans by walking the source document's POOM. The POOM returns one I-span per *contiguous I-address region*. If your source specset selects content that maps to three non-contiguous I-address regions (because the content was assembled from three independent insertions, or from insertions interleaved with CREATELINK operations per [INT-LINK-INSERT]), you get three I-spans, and therefore three DOCISPAN entries.

Confirmed by [ST-COPY] (Finding 0047):

> COPY of fragmented source content (e.g., 3 non-contiguous regions) creates 3 DOCISPAN entries. The number of new index entries depends on the I-space fragmentation of the copied content, not its V-space extent.

**Corollary:** A single COPY of a V-span covering contiguous text (even if large) creates exactly **1** DOCISPAN entry, because `vspanset2ispanset` collapses it into one I-span [SS-DOCISPAN, Finding 0033].

**Storage cost** therefore tracks editorial fragmentation, not byte count — [INV-SPANF-GROWTH] formalizes this: `|DOCISPAN| ≤ Σ_{all INSERT/COPY ops} |ispanset(op)|`, where `|ispanset(op)|` equals the number of contiguous I-address runs in the content placed by that operation.

---

## Code Exploration

I now have all the evidence needed. Here is the complete answer.

---

## Answer: One DOCISPAN entry per contiguous I-span, not per COPY operation

### The call chain

`docopy` [`do1.c:45–65`] is the entry point for a COPY:

```c
specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)   // [do1.c:54]
&& insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)       // [do1.c:60]
&& insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)    // [do1.c:62]
```

The **same `ispanset`** feeds both `insertpm` (into the POOM) and `insertspanf` (into the spanfilade).

---

### Step 1: How `specset2ispanset` builds the `ispanset`

`specset2ispanset` [`do2.c:14–46`] walks the specset. For each `VSPECID` item it calls `vspanset2ispanset` → `permute` [`orglinks.c:397–422`] → `span2spanset` per V-span → `retrieverestricted` to map each V-span to its constituent I-spans, appending one `typeispan` per contiguous I-range to the output list.

The result is a **flat linked list of `typeispan` nodes**, one node per contiguous I-range that the V-span maps to in the permascroll. If the V-specset projects onto three non-contiguous I-ranges, `ispanset` is a three-element linked list.

---

### Step 2: The `insertspanf` loop is per-item

`insertspanf` [`spanf1.c:15–54`]:

```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    if (((typeitemheader *)sporglset)->itemid == ISPANID) {
        movetumbler(&((typeispan *)sporglset)->stream, &lstream);   // [spanf1.c:27]
        movetumbler(&((typeispan *)sporglset)->width,  &lwidth);    // [spanf1.c:28]
        movetumbler(isaptr, &linfo.homedoc);                        // [spanf1.c:29]
    } ...
    movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);             // [spanf1.c:49]
    movetumbler(&lwidth,  &crumwidth.dsas[SPANRANGE]);              // [spanf1.c:50]
    insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE); // [spanf1.c:51]
}
```

**`insertnd` is called exactly once per iteration — one call per item in the list.** There is no batching, no consolidation before calling `insertnd`.

The ORGLRANGE key — the spanfilade's "which document" axis — is set once before the loop:
```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // [spanf1.c:22]
tumblerclear(&crumwidth.dsas[ORGLRANGE]);                       // [spanf1.c:23]
```
`prefixtumbler` [`tumble.c:641–651`] prepends the `spantype` integer (`DOCISPAN`) as the high digit of the tumbler address, then appends the document ISA. This is identical for every iteration — all three crums get the same ORGLRANGE origin, recording them as belonging to the same target document.

---

### Step 3: Does `insertnd` merge adjacent spans?

`insertcbcnd` [`insertnd.c:242–275`] contains the only place where a new insertion might be collapsed into an existing bottom crum. It calls `isanextensionnd` [`insertnd.c:301–309`]:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    if (!tumblereq(&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))  // [insertnd.c:305]
        return(FALSE);
    prologuend((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return(lockeq(reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype))); // [insertnd.c:308]
}
```

Merging requires **both**:
1. Same `homedoc` (target document ISA) — this is satisfied, all three crums have the same `isaptr`
2. The existing crum's `reach` (end boundary across **all** dimensions) equals the new crum's `origin` — i.e., the new I-span starts exactly where the previous one ends in SPANRANGE

For three **non-contiguous** I-ranges, condition 2 fails for every pair. The SPANRANGE end of crum N does not equal the SPANRANGE start of crum N+1. `isanextensionnd` returns `FALSE`, and `insertcbcnd` falls through to `createcrum` + `adopt` [`insertnd.c:260–274`], allocating a new bottom crum each time.

---

### Conclusion

**`insertspanf` creates one DOCISPAN entry (one spanfilade bottom crum) per contiguous I-span in the `ispanset` passed to it — not one per COPY operation.**

If the source specset converts to an `ispanset` with three non-contiguous I-ranges, `insertspanf` calls `insertnd` three times [`spanf1.c:51`], and the spanfilade gains exactly **three** new DOCISPAN bottom crums. They share the same ORGLRANGE key (target document ISA + `DOCISPAN` type) but have distinct SPANRANGE coordinates corresponding to each of the three I-ranges.

The only case where fewer than N crums would result is if two of the I-ranges are **contiguous** (adjacent with no gap) and were inserted in sequence — `isanextensionnd` would then merge the second into the first. By definition, non-contiguous ranges cannot trigger this merge.

---

## Question 15 [gregory]

> After COPY creates shared I-addresses between doc1 and doc2, does an INSERT into doc1 at a position within the transcluded range affect doc2's POOM in any way — specifically, does `makegappm` operate only on the single `fullcrumptr` passed to `insertnd`, with no mechanism to locate or modify doc2's tree?

### Gregory's Answer

## KB Synthesis

No. An INSERT into doc1 has zero effect on doc2's POOM, regardless of shared I-addresses. The reasoning is structural:

**`makegappm` operates on a single POOM tree.** The function receives `fullcrumptr` — the root of the target document's orgl enfilade [SS-TWO-BLADE-KNIFE]. It constructs a two-blade knife and calls `insertcutsectionnd` to shift entries within `[blade[0], blade[1])` in that one tree. There is no global POOM registry, no mechanism to enumerate other documents' orgl trees, and no lookup path from a V-position to "all POOMs that share I-addresses at this position."

**POOM trees are per-document and fully independent.** Each document's POOM is a separate B-tree structure at its own memory/disk address [SS-POOM-MUTABILITY]. Doc2's tree has its own root pointer, its own nodes, and its own V-space coordinate system. `insertnd` operates on the single `fullcrumptr` passed to it — doc2's tree is not reachable from doc1's tree traversal.

**Transclusion shares I-addresses, not V-space.** COPY places the same I-addresses into multiple POOM trees, but each tree independently maps its own V-positions to those I-addresses [SS-CONTENT-IDENTITY], [FC-DOC-ISOLATION]. When INSERT into doc1 shifts V-positions in doc1's POOM (entries in `[blade[0], blade[1])`), doc2's corresponding V-positions are untouched. Doc2 still maps its own (unchanged) V-positions to the shared I-addresses.

**The I-addresses themselves are immutable.** INSERT allocates fresh I-addresses for new content — it does not modify the granfilade entries that doc2 already references [INV-IADDR-IMMUTABILITY], [FC-INSERT-IADDR]. Doc2 continues to read identical bytes at the same I-addresses.

**Explicit frame condition.** [FC-DELETE-CROSS-DOC] states this same invariant for DELETE: "DELETE in one document has zero effect on any other document's POOM mappings." INSERT is strictly additive and the same isolation applies — the shift mechanism in `makegappm` is scoped to the single orgl tree being modified [ST-INSERT] Finding 0054.

Summary: after `COPY(doc1 → doc2)` and then `INSERT(doc1, pos, text)`, doc2's POOM is bit-for-bit identical to what it was immediately after the COPY. The shared I-addresses remain accessible from doc2 at the same V-positions, with the same content bytes, as if the INSERT never happened.

---

## Code Exploration

---

## Answer

**Yes — `makegappm` operates exclusively on the single `fullcrumptr` passed to `insertnd`. There is no mechanism by which INSERT into doc1 can locate or modify doc2's POOM.**

The proof runs through every layer of the call stack.

---

### 1. INSERT entry point — `fns.c:84–98`

```c
void insert(typetask *taskptr)
{
    (void) getinsert (taskptr, &docisa, &vsa, &textset);
    putinsert (taskptr);
    if (!doinsert (taskptr, &docisa, &vsa, textset)) ...
}
```

INSERT takes a single `docisa`. Everything downstream is keyed to that one document identity.

---

### 2. `doinsert` — `do1.c:87–123`

```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
        && docopy (taskptr, docisaptr, vsaptr, ispanset)
    );
    return(ret);
}
```

Two operations: `inserttextingranf` writes the new text bytes into the permascroll (granfilade), assigning them fresh I-addresses. `docopy` records the resulting I-span into **one document's** POOM.

---

### 3. `docopy` — `do1.c:45–65`

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && acceptablevsa (vsaptr, docorgl)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
    );
}
```

`findorgl` is called with `docisaptr` — the address of doc1. It returns exactly one orgl: doc1's.

---

### 4. `findorgl` → `fetchorglgr` — `granf1.c:17–41` and `granf2.c:22–80`

```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)
{
    ...
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);
    return (*orglptr ? TRUE : FALSE);
}
```

```c
typeorgl fetchorglgr(typetask *taskptr, typegranf fullcrumptr, typeisa *address)
{
    context = retrievecrums ((typecuc*)fullcrumptr, address, WIDTH);
    ...
    ret = context->corecrum->cinfo.granstuff.orglstuff.orglptr;
    ...
    return ((typeorgl)ret);
}
```

`fetchorglgr` uses `retrievecrums` to look up the granfilade node whose ISA matches `address`. It then returns the `orglptr` stored in that specific node's `cinfo.granstuff.orglstuff` — **the POOM tree belonging to that one document**. doc2's orgl is stored at doc2's ISA address; it is never touched here.

---

### 5. `insertpm` — `orglinks.c:75–134`

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl, tumbler *vsaptr, typesporglset sporglset)
{
    logbertmodified(orglisa, user);
    for (; sporglset; sporglset = ...) {
        unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
        movetumbler (&lstream, &crumorigin.dsas[I]);
        movetumbler (&lwidth,  &crumwidth.dsas[I]);
        movetumbler (vsaptr,   &crumorigin.dsas[V]);
        ...
        insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // line 130
        tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);
    }
    return (TRUE);
}
```

`insertpm` constructs a 2D crum address (`crumorigin` has both I and V coordinates) and calls `insertnd` on `orgl` — **a single orgl, passed in, never looked up again**. doc2's orgl is never passed here.

---

### 6. `insertnd` — `insertnd.c:15–111`

```c
int insertnd(typetask *taskptr, typecuc *fullcrumptr, typewid *origin, typewid *width, type2dbottomcruminfo *infoptr, INT index)
{
    ...
    switch (fullcrumptr->cenftype) {
      case POOM:
          makegappm (taskptr, fullcrumptr, origin, width);   // line 54
          setwispupwards(fullcrumptr, 0);
          bothertorecombine = doinsertnd(fullcrumptr, origin, width, infoptr, index);
          setwispupwards(fullcrumptr, 1);
          break;
      ...
    }
    if (bothertorecombine || ...) recombine(fullcrumptr);
}
```

`insertnd` receives `fullcrumptr` as its sole tree parameter. Every subsequent operation — `makegappm`, `setwispupwards`, `doinsertnd`, `recombine` — is called with that same pointer or a pointer derived from walking its subtree.

---

### 7. `makegappm` — `insertnd.c:124–172`

```c
int makegappm(typetask *taskptr, typecuc *fullcrumptr, typewid *origin, typewid *width)
{
    ...
    prologuend ((typecorecrum*)fullcrumptr, &offset, &grasp, &reach);
    if (iszerotumbler(&fullcrumptr->cwid.dsas[V]) || ...) return(0);

    movetumbler (&origin->dsas[V], &knives.blades[0]);
    findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]);
    knives.nblades = 2;
    knives.dimension = V;
    makecutsnd (fullcrumptr, &knives);                    // cuts within fullcrumptr's tree
    newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);  // finds father within fullcrumptr's tree
    prologuend ((typecorecrum*)father, &foffset, &fgrasp, NULL);
    for (ptr = findleftson(father); ptr; ptr = findrightbro(ptr)) {  // iterates children of father
        i = insertcutsectionnd(ptr, &fgrasp, &knives);
        switch (i) {
          case 1:
              tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);  // line 162
              ivemodified(ptr);
              break;
          ...
        }
    }
    setwidnd(father);
    setwispupwards(findfather((typecorecrum*)father), 1);
}
```

Every pointer used in `makegappm` is derived from `fullcrumptr`:
- `makecutsnd(fullcrumptr, &knives)` — splits nodes within this tree
- `newfindintersectionnd(fullcrumptr, ...)` — locates `father` by walking this tree
- `findleftson(father)` / `findrightbro(ptr)` — iterates children **within this tree**
- `findfather((typecorecrum*)father)` — walks up within this tree

The displacement update at line 162 — `tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V])` — moves sibling crums in doc1's V-space to the right of the insertion point. These `ptr` nodes are children of `father`, which is a node in doc1's POOM tree. No function call in `makegappm` takes a document ISA, queries the granfilade for another document, or produces a pointer to any structure outside `fullcrumptr`'s tree.

---

### Why shared I-addresses don't create coupling

After COPY, both doc1's POOM and doc2's POOM contain bottom crums whose **I-dimension** (`cdsp.dsas[I]`, `cwid.dsas[I]`) points to the same permascroll range. But this is just a stored tumbler value — a number. There is no back-pointer from the granfilade content store to every POOM that references it, and no lookup of "all documents referencing this I-span." The granfilade node for a document stores only one orgl pointer (`cinfo.granstuff.orglstuff.orglptr`); there is no reverse index.

The V-space trees of doc1 and doc2 are structurally independent POOM enfilades. `makegappm` creates a gap in doc1's V-axis by cutting nodes and adjusting displacements within doc1's tree. doc2's V-axis — which has its own independent layout of V→I mappings — is not touched.

---

### Summary

| Step | Code | What it touches |
|------|------|-----------------|
| `insert()` | `fns.c:84` | Passes `docisa` (doc1) through |
| `doinsert()` | `do1.c:87` | Writes text to granfilade; calls `docopy(doc1)` |
| `docopy()` | `do1.c:45` | Calls `findorgl(doc1)` → returns doc1's orgl only |
| `fetchorglgr()` | `granf2.c:22` | Looks up ISA address; returns single orgl pointer |
| `insertpm()` | `orglinks.c:75` | Calls `insertnd(orgl)` — single orgl, no re-lookup |
| `insertnd()` | `insertnd.c:15` | Calls `makegappm(fullcrumptr)` — single tree |
| `makegappm()` | `insertnd.c:124` | All pointers derived from `fullcrumptr`; adjusts V-displacements within doc1's tree only |

**doc2's POOM is completely unaffected.** The shared I-addresses are a shared *content citation* (two documents happen to cite the same permascroll range), not a shared *structural node*. The POOM trees are entirely independent, and there is no mechanism — no reverse index, no broadcast, no shared node — by which a V-space operation on doc1 propagates to doc2.

---

## Question 16 [gregory]

> When `find_links` is called on doc2 and discovers a link originally created in doc1 through shared I-addresses, does `linksporglset2specset` resolve the link's endset I-addresses against doc2's POOM — returning V-positions within doc2 — or does it return the V-positions from doc1 where the link was originally created?

### Gregory's Answer

## KB Synthesis

`linksporglset2specset` resolves endset I-addresses against **whichever document's POOM is passed as the query context** — not necessarily doc1 or doc2 universally. The behavior differs by operation:

## For RETRIEVEENDSETS

[SS-RETRIEVE-ENDSETS] (Finding 0035) is explicit:

> Results are converted back to V-addresses using the querying document's docid.
> **Key: endsets are resolved in terms of the querying document's V-space, not the link's home document.**

So if RETRIEVEENDSETS is invoked from doc2's context, `linksporglset2specset` looks up the link's endset I-addresses in **doc2's POOM**. If those I-addresses exist there (because doc2 transcluded the content), it returns V-positions within doc2. If doc2 doesn't have them, they are silently dropped [INV-ITOV-FILTERING].

[INT-LINK-VERSION] (Finding 0019) confirms this empirically: "When queried from a version, endsets report the version's docid rather than the original's."

## For FOLLOWLINK

[SS-FOLLOWLINK] (Finding 0048) shows it's parametric:

> `followlink(link, whichend, homedoc) = { v | ∃ i ∈ endset(link, whichend) : poom.homedoc(v) = i }`

The caller explicitly specifies which document's POOM to resolve against. Passing doc1 returns V-positions in doc1; passing doc2 returns V-positions in doc2 (or empty if doc2's POOM has no mapping for those I-addresses).

## What `find_links` itself returns

`find_links` returns **link ISAs** (identifiers), not resolved V-positions [SS-FIND-LINKS]. The I-address intersection happens in spanfilade search [SS-SPANF-OPERATIONS] — it determines *which links* are discovered. Resolution of those links' endpoints to V-positions only happens in a subsequent RETRIEVEENDSETS or FOLLOWLINK call, where the document context determines which POOM is consulted.

## Summary

| Operation | POOM consulted |
|---|---|
| `find_links(doc2, ...)` | No POOM — returns link ISAs only |
| RETRIEVEENDSETS from doc2 | doc2's POOM |
| FOLLOWLINK(link, end, doc2) | doc2's POOM |
| FOLLOWLINK(link, end, doc1) | doc1's POOM |

A concrete consequence: if doc2 transcluded "hyperlink text" from doc1, and a link was created on doc1's "hyperlink text", then RETRIEVEENDSETS from doc2 would return V-positions within doc2 where the transcluded content lives — not doc1's original positions. If those I-addresses don't appear in doc2's POOM at all, the result is empty [EC-GHOST-LINK].

---

## Code Exploration

I have all the information needed. Let me now trace the complete execution path and produce the answer.

---

## Answer

### Short answer

`linksporglset2specset` resolves the link's endset I-addresses against **the document that owns the link's POOM** — which is **doc1** (where the link was originally created) — not doc2. This is what the `follow_link` path does. The `retrieve_endsets` path does it differently; see below.

---

### Detailed trace

#### 1. `find_links` does NOT call `linksporglset2specset`

`find_links` maps to `findlinksfromtothree` [`fns.c:189`], which calls `dofindlinksfromtothree` [`do1.c:348`], which calls `findlinksfromtothreesp` [`spanf1.c:56`]:

```c
bool findlinksfromtothreesp(typetask *taskptr, typespanf spanfptr, ...)
{
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
    sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, ...);
    ...
    intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
    return (TRUE);
}
```
[`spanf1.c:56–103`]

This function converts V-specs → sporgls → searches the spanfilade by I-address range → returns only **link ISAs** (tumblers). There is no call to `linksporglset2specset` here. The question of V-position resolution doesn't arise at the `find_links` stage.

---

#### 2. `follow_link` — the primary endset-retrieval path after `find_links`

After `find_links` returns a link ISA, the natural follow-up is `follow_link` → `dofollowlink` [`do1.c:223`]:

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
    typesporglset sporglset;
    ...
    return (
       link2sporglset(taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset(taskptr, &((typesporgl *)sporglset)->sporgladdress,
                             sporglset, specsetptr, NOBERTREQUIRED));
}
```
[`do1.c:228–231`]

The `homedoc` argument passed to `linksporglset2specset` is `&((typesporgl *)sporglset)->sporgladdress` — the document address packed inside the first sporgl returned by `link2sporglset`.

##### How `sporgladdress` gets set — tracing `link2sporglset`

`link2sporglset` [`sporgl.c:67`] retrieves I-addresses from the link's own POOM and builds sporgls via `contextintosporgl` [`sporgl.c:205`]:

```c
int contextintosporgl(type2dcontext *context, tumbler *linkid, typesporgl *sporglptr, INT index)
{
    sporglptr->itemid = SPORGLID;
    sporglptr->next = NULL;
    movetumbler(/*linkid*/&context->context2dinfo.homedoc, &sporglptr->sporgladdress);
    /* ^^^^^ zzz foo kluge 11/23/84 ^^^^^ */
    movetumbler(&context->totaloffset.dsas[index], &sporglptr->sporglorigin);
    movetumbler(&context->contextwid.dsas[index], &sporglptr->sporglwidth);
}
```
[`sporgl.c:205–220`]

`sporglptr->sporgladdress` is set to `context->context2dinfo.homedoc` — the document that was recorded in the POOM crum when the link was created. This was set originally by `insertpm` [`orglinks.c:75`] via `insertnd`, which stores the `linfo.homedoc` from `unpacksporgl`:

```c
int unpacksporgl(typesporglset sporglptr, tumbler *streamptr, tumbler *widthptr, type2dbottomcruminfo *infoptr)
{
    ...
    } else if (((typeitemheader *)sporglptr)->itemid == SPORGLID) {
        movetumbler(&((typesporgl *)sporglptr)->sporglorigin, streamptr);
        movetumbler(&((typesporgl *)sporglptr)->sporglwidth, widthptr);
        movetumbler(&((typesporgl *)sporglptr)->sporgladdress, &infoptr->homedoc);
    }
}
```
[`sporgl.c:178–203`]

And in `vspanset2sporglset`, when a link is created, the sporgls store `docisa` (doc1) as `sporgladdress`:

```c
movetumbler(docisa, &sporglset->sporgladdress);
movetumbler(&ispanset->stream, &sporglset->sporglorigin);
movetumbler(&ispanset->width, &sporglset->sporglwidth);
```
[`sporgl.c:53–55`]

Therefore `context->context2dinfo.homedoc` in `contextintosporgl` recovers **doc1's ISA** — the document with which the link was created. So `sporgladdress = doc1`.

---

#### 3. What `linksporglset2specset` does with that `homedoc`

`linksporglset2specset` [`sporgl.c:97`]:

```c
bool linksporglset2specset(typetask *taskptr, typeisa *homedoc,
                           typesporglset sporglset, typespecset *specsetptr, int type)
{
    ...
    for (; sporglset; ...) {
        if (iszerotumbler(&sporglset->sporgladdress)) {
            /* treat as a raw I-span */
            ((typeitemheader *)specset)->itemid = ISPANID;
            movetumbler(&sporglset->sporglorigin, &specset->stream);
            movetumbler(&sporglset->sporglwidth, &specset->width);
        } else {
            linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
        }
    }
}
```
[`sporgl.c:97–123`]

For a non-zero `sporgladdress` it calls `linksporglset2vspec` [`sporgl.c:127`]:

```c
int linksporglset2vspec(typetask *taskptr, typeisa *homedoc,
                        typesporglset *sporglsetptr, typevspec *specptr, int type)
{
    specptr->itemid = VSPECID;
    specptr->next = NULL;
    movetumbler(homedoc/*&sporglset->sporgladdress*/, &specptr->docisa);
    specptr->vspanset = NULL;
    sporglset2vspanset(taskptr, homedoc, sporglsetptr, &specptr->vspanset, type);
}
```
[`sporgl.c:127–137`]

**Critical observation:** `&specptr->docisa` is set to `homedoc`, not to `sporglset->sporgladdress`. The commented-out alternative `/*&sporglset->sporgladdress*/` shows the original design. In `dofollowlink` these are the same value (since `homedoc` was initialized from `sporglset->sporgladdress`), so the change is a no-op for this path.

`sporglset2vspanset` [`sporgl.c:141`]:

```c
int sporglset2vspanset(typetask *taskptr, typeisa *homedoc,
                       typesporglset *sporglsetptr, typevspanset *vspansetptr, int type)
{
    sporglptr = (typesporgl *)*sporglsetptr;
    (void) findorgl(taskptr, granf, homedoc/*&sporglptr->sporgladdress*/, &orgl, type);
    ispan.itemid = ISPANID;
    ispan.next = NULL;
    movetumbler(&sporglptr->sporglorigin, &ispan.stream);
    movetumbler(&sporglptr->sporglwidth, &ispan.width);
    vspansetptr = ispan2vspanset(taskptr, orgl, &ispan, vspansetptr);
    ...
}
```
[`sporgl.c:141–176`]

Again `homedoc` is used in the `findorgl` call. In the `follow_link` path `homedoc = doc1`, so `findorgl` loads **doc1's POOM**. The sporgl's `sporglorigin` / `sporglwidth` (the I-address range) is then mapped to V-positions using `ispan2vspanset` [`orglinks.c:389`]:

```c
typevspanset *ispan2vspanset(typetask *taskptr, typeorgl orgl, typeispan *ispanptr, typevspanset *vspansetptr)
{
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}
```

`permute` walks doc1's POOM, intersecting the stored I-address range with the endset's I-addresses and reading out the corresponding V-coordinates from **doc1's POOM tree**.

---

#### 4. The `retrieve_endsets` path — behaves differently

`retrieve_endsets` → `doretrieveendsets` [`do1.c:369`] → `retrieveendsetsfromspanf` [`spanf1.c:190`]:

```c
linksporglset2specset(taskptr, &((typevspec *)specset)->docisa,
                      fromsporglset, fromsetptr, NOBERTREQUIRED)
```
[`spanf1.c:224`]

Here `homedoc = &((typevspec *)specset)->docisa`, where `specset` is what the **client passed** to identify the link. If the client supplies a vspec whose `docisa` is doc2, then `linksporglset2specset` will call `findorgl` for doc2's POOM and return V-positions in **doc2**. The commented-out code `/*&sporglset->sporgladdress*/` is the only thing that would have forced it back to doc1 in this path.

---

### Summary

| Path | `homedoc` passed to `linksporglset2specset` | POOM used for I→V conversion | Result |
|---|---|---|---|
| `follow_link` (`dofollowlink`) | `sporglset->sporgladdress` = doc1 (set by `contextintosporgl` from the link's POOM crum) | doc1's POOM via `findorgl` | V-positions **in doc1** |
| `retrieve_endsets` (`retrieveendsetsfromspanf`) | `specset->docisa` = whatever the client passed | `findorgl` of client's docisa | V-positions **in whichever doc the client named** |

**For the `follow_link` path** (the natural post-`find_links` call): `linksporglset2specset` resolves the link's endset I-addresses against **doc1's POOM**, returning V-positions from doc1 where the link was originally created. The fact that the link was *discovered* via doc2's shared I-addresses is irrelevant — the resolution is anchored to the document recorded in the link's POOM crums at creation time.

The two commented-out alternatives in `sporgl.c:134` (`/*&sporglset->sporgladdress*/`) and `sporgl.c:152` (`/*&sporglptr->sporgladdress*/`) are relics of a design that would have always used the sporgl's stored doc (doc1) regardless of caller. The current code parameterizes this as `homedoc`, but in `dofollowlink` the caller passes `sporglset->sporgladdress` — which is doc1 — so the behavior is identical on that path.

---

## Question 17 [gregory]

> If doc1 contains "ABCDE" and doc2 transcludes "BCD" (a partial span), does doc2's POOM entry store a V-width of 3 with an I-displacement pointing to I-address of "B" — and does `compare_versions` correctly identify the 3-character overlap between doc1 and doc2 despite the differing V-address ranges?

### Gregory's Answer

## KB Synthesis

Yes to both parts. Here is the synthesis:

---

## doc2's POOM entry after transcluding "BCD"

From [SS-POOM-BOTTOM-CRUM] (Finding 0076), each POOM bottom crum stores dual-space coordinates:

```
BottomCrum = {
  origin: { dsas[I]: I-address of "B",  dsas[V]: V-address of "B" in doc2 }
  width:  { dsas[I]: tumbler for 3 (I-precision),
             dsas[V]: tumbler for 3 (V-precision, different encoding) }
}
```

The I-origin is precisely the I-address of "B" in the permascroll — whatever was allocated when "ABCDE" was first inserted into doc1. From [ST-VCOPY] (Finding 0018), vcopy preserves I-addresses: the transcluded "BCD" in doc2 holds the same I-addresses as "BCD" in doc1. No new I-addresses are allocated.

From [SS-INSERT-VWIDTH-ENCODING] (Finding 0076), the V-width encoding uses `shift = tumblerlength(vsaptr) - 1` and `tumblerincrement(zero, shift, 3)` — so if the V-address is `1.1` (tumblerlength=2), the V-width is encoded as `0.3` (exp=-1, mantissa[0]=3), while the I-width is copied directly at I-space precision. From [INV-WIDTH-VALUE-EQUIVALENCE], both encode the integer 3 but as structurally distinct tumblers.

From [ST-VCOPY-CONTIGUITY] (Finding 0033), because "BCD" in doc1 occupies a contiguous V-span (and thus maps to contiguous I-addresses), the transcluded result in doc2 is a single consolidated I-span — one POOM crum, not three.

---

## compare_versions correctly finds the 3-character overlap

From [SS-COMPARE-VERSIONS] (Finding 0015), compare_versions operates in I-space:

> Each pair `(span_a, span_b)` satisfies: `VSpanToISpan(doc_a, span_a) == VSpanToISpan(doc_b, span_b)`

The algorithm ([INT-SPORGL-VERSION-COMPARE], Finding 0013):
1. Convert both documents' V-spans to sporgls (carrying I-address + document provenance)
2. Intersect on I-address ranges
3. Map intersection back to V-spans in each document

For this scenario:
- doc1's "ABCDE" → I-addresses I.1..I.5
- doc2's "BCD" → I-addresses I.2..I.4 (identical to doc1's "BCD" — preserved by vcopy)
- Intersection: I.2..I.4 (width 3)
- Map back: doc1 at e.g. `1.2 for 0.3`, doc2 at e.g. `1.1 for 0.3`

The differing V-address ranges are irrelevant — comparison is purely I-address-based. The result would be:

```
[(doc1: {start: "1.2", width: "0.3"}, doc2: {start: "1.1", width: "0.3"})]
```

This works because the precondition from [PRE-COMPARE-VERSIONS] (Finding 0015) is satisfied — both spans are in the text subspace (V ≥ 1.0), so I-address intersection is meaningful (permascroll addresses, not link orgl ISAs).

---

## Summary

| Property | Answer | Source |
|----------|--------|--------|
| doc2 POOM I-origin = I-address of "B" | Yes | [ST-VCOPY] F0018, [SS-POOM-BOTTOM-CRUM] F0076 |
| doc2 POOM V-width and I-width both encode 3 | Yes, different encodings | [SS-INSERT-VWIDTH-ENCODING] F0076, [INV-WIDTH-VALUE-EQUIVALENCE] F0076 |
| One consolidated POOM crum for "BCD" | Yes | [ST-VCOPY-CONTIGUITY] F0033 |
| compare_versions finds the overlap | Yes | [SS-COMPARE-VERSIONS] F0015, [INT-SPORGL-VERSION-COMPARE] F0013 |
| V-address difference is irrelevant | Yes — comparison is I-space only | [SS-COMPARE-VERSIONS] F0015 |

---

## Code Exploration

Now I have the full picture. Let me compose the complete answer.

---

## Answer

### Part 1: What Doc2's POOM Entry Stores

**Yes — the leaf crum in doc2's POOM stores an I-displacement pointing to the permascroll address of "B" and a V-width of 3.**

Here is the exact call chain when `docopy` is invoked to transclud "BCD" from doc1 into doc2:

#### Step 1 — V→I Conversion of the Source Span

`docopy` [do1.c:53] first calls `specset2ispanset` [do2.c:14] which drives `vspanset2ispanset` [orglinks.c:397], which calls `permute` [orglinks.c:404], which calls `span2spanset` [orglinks.c:425]:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex, ...);
// orglinks.c:435 — searches doc1's POOM restricted to the V-span of "BCD"
```

`retrieverestricted` [retrie.c:56] passes through to `findcbcinarea2d` [retrie.c:229], which walks doc1's POOM tree, finds the crum covering "ABCDE", and calls `makecontextfromcbc` [context.c:151] to capture that crum's absolute coordinates.

Back in `span2spanset`, `context2span` [context.c:176] clips the found crum to the "BCD" restriction:

```c
// context.c:191-196 — if crum starts before lowerbound, shift the I-start
if (tumblercmp(&grasp.dsas[idx1], &lowerbound) == LESS) {
    tumblerincrement(&grasp.dsas[idx2], 0,
        (INT)tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
        &grasp.dsas[idx2]);
}
// context.c:197-202 — if crum ends after upperbound, trim the I-end
if (tumblercmp(&reach.dsas[idx1], &upperbound) == GREATER) {
    tumblerincrement(&reach.dsas[idx2], 0,
        -tumblerintdiff(&reach.dsas[idx1], &upperbound),
        &reach.dsas[idx2]);
}
movetumbler(&grasp.dsas[idx2], &foundspanptr->stream); // I("B")
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width); // width=3
```

So: doc1's POOM crum covers "ABCDE". The V-start of "BCD" is V("A")+1, so the I-start shifts by 1: I("A")+1 = **I("B")**. The V-end of "BCD" is V("A")+3, so the I-end is also clipped correspondingly. Result: `ispanset` = {stream: I("B"), width: 3}.

#### Step 2 — Insertion into Doc2's POOM

`insertpm` [orglinks.c:75] is called with `vsaptr` = the V-address in doc2 (e.g. 1.1) and `sporglset` carrying the I-span {I("B"), 3}:

```c
// orglinks.c:101
unpacksporgl(sporglset, &lstream, &lwidth, &linfo);
//   lstream = I("B"), lwidth = 3

// orglinks.c:105
movetumbler(&lstream, &crumorigin.dsas[I]);     // I-displacement = I("B")
// orglinks.c:109
movetumbler(&lwidth, &crumwidth.dsas[I]);       // I-width = 3
// orglinks.c:113
movetumbler(vsaptr, &crumorigin.dsas[V]);       // V-address in doc2

// orglinks.c:115-117 — V-width derived from I-width
shift = tumblerlength(vsaptr) - 1;
inc = tumblerintdiff(&lwidth, &zero);            // = 3
tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]);  // V-width = 3
```

`insertnd` [insertnd.c:15] is then called, and for a fresh doc2 the call reaches `firstinsertionnd` [insertnd.c:199]:

```c
movewisp(origin, &ptr->cdsp);  // cdsp.I = I("B"), cdsp.V = doc2's V-address
movewisp(width, &ptr->cwid);   // cwid.I = 3,       cwid.V = 3
```

**The crum stored in doc2's POOM therefore has:**
- `cdsp.dsas[I]` = I("B") — the permascroll address of "B"
- `cwid.dsas[I]` = 3 — I-width (3 characters)
- `cwid.dsas[V]` = 3 — V-width (computed identically from the integer 3 at `orglinks.c:117`)

---

### Part 2: Does `compare_versions` Correctly Find the 3-Character Overlap?

**Yes — and it works precisely because the comparison occurs entirely in I-space (the permascroll), where both documents agree on the addresses of "B", "C", and "D".**

The entry point is `doshowrelationof2versions` [do1.c:428]:

```c
filter_specset_to_text_subspace(taskptr, version1);  // do1.c:440
filter_specset_to_text_subspace(taskptr, version2);  // do1.c:441
// (removes link subspace spans at V < 1.0; both ABCDE and BCD survive)

specset2ispanset(taskptr, version1, &version1ispans, READBERT)  // → {I("A"), 5}
&& specset2ispanset(taskptr, version2, &version2ispans, READBERT) // → {I("B"), 3}
&& intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
&& ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation)
```

#### The V→I Conversion

- **Doc1**: `specset2ispanset` walks doc1's POOM (which has a crum for "ABCDE") and maps the full V-range → I-span {stream: I("A"), width: 5}.
- **Doc2**: `specset2ispanset` walks doc2's POOM (the crum just created above) and maps doc2's V-range → I-span {stream: I("B"), width: 3}.

Both use the same `permute`→`span2spanset`→`retrieverestricted`→`context2span` path described above. The V-addresses in the two documents are irrelevant at this point — only the I-addresses survive.

#### The Intersection

`intersectspansets` [correspond.c:145] calls `comparespans` [correspond.c:191] → `spanintersection` [correspond.c:210]:

```c
// correspond.c:247-256 — case where aptr.stream < bptr.stream (I("A") < I("B"))
case LESS:
    movetumbler(&bptr->stream, &cptr->stream);   // result.stream = I("B")
    switch (tumblercmp(&aend, &bend)) {
      case GREATER:   // aend=I("A")+5 > bend=I("B")+3, so:
          movetumbler(&bptr->width, &cptr->width); // result.width = 3
    }
```

Result: `commonispans` = {stream: I("B"), width: 3} — the 3-character overlap in permascroll space.

#### Mapping Back to V-Addresses

`ispansetandspecsets2spanpairset` [do2.c:185] calls `restrictspecsetsaccordingtoispans` [correspond.c:18], which calls `restrictvspecsetovercommonispans` [correspond.c:52]:

```c
// correspond.c:74 — for each document, convert the common I-span back to V-spans
ispan2vspanset(taskptr, versionorgl, ispanset, &docvspanset);
```

`ispan2vspanset` [orglinks.c:389] calls `permute` in the reverse direction (I→V), querying each document's POOM restricted to {I("B"), 3}. Doc1's POOM maps this back to V("B")..V("D") in doc1; doc2's POOM maps it back to V("B_in_doc2")..V("D_in_doc2").

Finally `makespanpairset` [correspond.c:267] → `makespanpairsforispan` [correspond.c:290] zips these two V-span sequences together character-by-character, producing a `spanpair` with:
- `stream1` = V-address of "BCD" in doc1
- `stream2` = V-address of "BCD" in doc2 (the entire V-content of doc2)
- `widthofspan` = 3

---

### Summary

| Question | Answer | Key cite |
|---|---|---|
| Does doc2's POOM crum store I-displacement = I("B")? | **Yes** | `orglinks.c:105`, `context.c:194` |
| Does doc2's POOM crum store V-width = 3? | **Yes** | `orglinks.c:115–117` |
| Is the V-width computed from the I-width? | **Yes** — `tumblerintdiff` on `lwidth` gives integer 3, placed at the correct tumbler level | `orglinks.c:116–117` |
| Does `compare_versions` find the 3-char overlap despite different V-ranges? | **Yes** | `do1.c:428–449`, `correspond.c:210–258` |
| How? | Both docs' V-spans are mapped to the same permascroll I-addresses; the intersection is performed in I-space where doc1's [I("A"),5) ∩ doc2's [I("B"),3) = [I("B"),3) | `retrie.c:56`, `context.c:176`, `correspond.c:210` |

The differing V-address ranges are never compared against each other. The POOM acts as a pure bijection between each document's private V-space and the shared permascroll I-space. `compare_versions` exploits that both POOM enfilades point into the same I-space — the intersection there is authoritative, and the result is then projected back to each document's V-space independently.

---

## Question 18 [gregory]

> When DELETE removes transcluded content from doc2 (content originally from doc1), the DOCISPAN entry for doc2 remains in the spanfilade — does `find_documents_containing` then return doc2 as still containing that content, and is there any mechanism in the retrieval path that verifies the DOCISPAN against doc2's current POOM before returning results?

### Gregory's Answer

## KB Synthesis

## find_documents_containing After DELETE of Transcluded Content

**Short answer:** Yes, `find_documents_containing` returns doc2 as still containing the content. No, there is no POOM-verification step in the retrieval path — `find_documents_containing` queries the spanfilade directly, and the spanfilade is never updated by DELETE.

---

### Why the DOCISPAN entry persists

DELETE operates exclusively on the POOM (granf layer) via `deletevspanpm` → `deletend`. The spanfilade is never touched:

> `dodeletevspan`: calls `findorgl` + `deletevspanpm`, no spanf call. Contrast with `docopy`: calls both `insertpm` AND `insertspanf`. [ST-DELETE, Finding 0057]

The spanfilade is structurally append-only — no deletion function exists anywhere in `spanf1.c` or `spanf2.c`:

> "No `deletespanf`, `removespanf`, or any removal mechanism exists." [INV-SPANF-WRITE-ONLY, Finding 0057]

So when doc2 originally received the transcluded content via COPY/VCOPY, `insertspanf(..., DOCISPAN)` was called and recorded doc2 as a container of those I-addresses. That entry is permanent.

---

### What find_documents_containing actually returns

The result is a **superset** of documents currently containing the I-addresses:

> `actual_docs(i) ⊆ find_documents(i)` where `actual_docs(i) = {D | ∃ v : poom.D(v) = i}`. The reverse inclusion does NOT hold. [EC-STALE-SPANF-REFERENCE, Finding 0057]

Doc2 appears in the result because the DOCISPAN entry asserts it, even though doc2's POOM no longer maps those I-addresses to any V-position. This creates a permanent divergence between the two layers:

> "Before DELETE, both layers agree... After DELETE, the POOM no longer contains the mapping, but the spanfilade still claims the document contains those I-addresses. This divergence is permanent." [INT-DELETE-SPANF-DIVERGENCE, Finding 0057]

This is also explicitly confirmed for the doc1-persists case in [INV-IADDRESS-PERMANENT] (Finding 0023) and [FC-CONTENT-SPANF-ISOLATION] (Finding 0018): even after deletion from doc2's V-stream, `find_documents` returns doc2.

---

### No POOM verification in find_documents_containing

`finddocscontainingsp` queries the spanfilade and returns whatever documents are registered there. There is no cross-check against those documents' current POOM state at query time.

The only verification that exists is downstream, in the **I-to-V conversion path**:

> "Both FOLLOWLINK and RETRIEVEENDSETS share the same I-to-V conversion path that silently filters unreferenced I-addresses. At `span2spanset()`, `retrieverestricted()` searches the target document's POOM for the I-address. If not found (returns NULL), the I-address is silently dropped." [INV-ITOV-FILTERING, Finding 0048]

This filtering happens when a caller subsequently attempts to resolve the I-addresses to V-positions within doc2 (e.g., via FOLLOWLINK or RETRIEVEENDSETS). It does not happen inside `find_documents_containing` itself.

---

### Summary

| Operation | Queries | Filters stale DOCISPAN? |
|-----------|---------|------------------------|
| `find_documents_containing` | Spanfilade only | **No** — returns superset |
| I-to-V conversion (FOLLOWLINK, RETRIEVEENDSETS) | Doc POOM | **Yes** — silently drops unresolvable I-addresses |

Consumers of `find_documents_containing` must post-filter via I-to-V conversion to distinguish live from stale results [EC-STALE-SPANF-REFERENCE]. The spanfilade is a historical journal of all content placements ever made, not a current-state index.

---

## Code Exploration

I now have everything needed. Here is the complete answer.

---

## Answer: Spanfilade Ghost Entries After DELETE

### The Short Answer

**Yes** — the DOCISPAN entry for doc2 persists in the spanfilade after a DELETE. **Yes** — `finddocscontainingsp` returns doc2 as still containing that content. **No** — there is no mechanism anywhere in the retrieval path that cross-checks the spanfilade against doc2's current POOM.

---

### 1. How the DOCISPAN Entry Gets Written (INSERT/COPY)

When content is transcluded into doc2 via `docopy` [`do1.c:45-65`], two independent writes happen:

```c
/* the meat of docopy: */
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)   // → POOM
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)  // → spanfilade
```

`insertpm` [`orglinks.c:75-134`] writes a crum into doc2's POOM mapping V-space → I-space. `insertspanf` [`spanf1.c:15-54`] writes a separate crum into the global `spanf`, keyed on the content's I-span in SPANRANGE and doc2's ISA in ORGLRANGE, with type `DOCISPAN`. These are entirely independent data structures — the POOM lives inside doc2's granfilade entry; the spanfilade is a global index.

---

### 2. What DELETE Actually Touches

`dodeletevspan` [`do1.c:158-167`]:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  bool findorgl(), deletevspanpm();

    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    /*&& TRUE*/ /* ht stuff */ );
}
```

`deletevspanpm` [`orglinks.c:145-152`]:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend` [`edit.c:31-76`] operates on `(typecuc*)docorgl` — **doc2's POOM only** — in dimension `V`. It calls `makecutsnd`, `newfindintersectionnd`, and a loop over children that calls `deletecutsectionnd` and `disown`/`subtreefree` on matching crums. These crums live in doc2's POOM.

**There is no `deletend` or any other call on `spanf` in this entire path.** The DELETE operation is POOM-only.

---

### 3. What `finddocscontainingsp` Actually Does

The call chain: `finddocscontaining` [`fns.c:20-32`] → `dofinddocscontaining` [`do1.c:15-23`] → `finddocscontainingsp` [`spanf1.c:151-188`].

```c
bool dofinddocscontaining(typetask *taskptr, typespecset specset, typelinkset *addresssetptr)
{
  typeispanset ispanset;
    return (
       specset2ispanset (taskptr, specset, &ispanset,NOBERTREQUIRED)
    && finddocscontainingsp (taskptr, ispanset, addresssetptr));
}
```

Inside `finddocscontainingsp` [`spanf1.c:151-188`]:

```c
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);
tumblerincrement (&docspace.width, 0, 1, &docspace.width);
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE,
                                  ispanset, SPANRANGE, (typeisa*)NULL);
    for (c = context; c; c = c->nextcontext) {
        movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
        beheadtumbler (&docid, &document.address);
        ...
        addresssetptr = (typelinkset *) onitemlist(taskptr, (typeitem*)&document, (typeitemset*)addresssetptr);
    }
}
```

This queries the **global `spanf`** (not any document's POOM) with `retrieverestricted`, restricting:
- ORGLRANGE to the `DOCISPAN` bucket (spans that record "document X contains I-span Y")
- SPANRANGE to the requested `ispanset`

It extracts doc ISAs from `ORGLRANGE` and returns them. **It never opens, reads, or consults doc2's POOM.** The spanfilade is the sole oracle for this query.

---

### 4. Is There Any POOM Verification in the Retrieval Path?

`retrieverestricted` [`retrie.c:56-85`] is called with the last argument `(typeisa*)NULL` — no `docisaptr`. This means `infoptr` is set to `NULL`:

```c
if (docisaptr) {
    movetumbler(docisaptr, &info.homedoc);
    infoptr = &info;
} else {
    infoptr = NULL;
}
temp = retrieveinarea(fullcrumptr, ..., (typebottomcruminfo*)infoptr);
```

Inside `findcbcinarea2d` [`retrie.c:229-268`], the per-leaf filter `crumqualifies2d` is:

```c
if ((crumptr->height == 0) && infoptr && !tumblereq (&infoptr->homedoc, &(((type2dcbc *)crumptr)->c2dinfo.homedoc))){
    return (FALSE);
}
```

Because `infoptr == NULL`, this guard is **never evaluated**. Even if it were, it would only filter by document identity (restricting to one specific doc's entries), not by whether the POOM actually contains those spans anymore. There is no POOM lookup, no V-space range check, no cross-referencing of the retrieved spanfilade crum against doc2's current content tree.

---

### 5. Conclusion

The spanfilade and the POOM are **write-paired on INSERT but not on DELETE**. At `docopy` time, both `insertpm` and `insertspanf` are called [`do1.c:60-62`]. At `dodeletevspan` time, only `deletevspanpm` → `deletend` on the POOM is called [`do1.c:163-166`]; the corresponding spanfilade crum is never removed.

After doc2 deletes transcluded content:
- doc2's **POOM** correctly reflects the removal — the V→I mapping for those spans is gone
- the **spanfilade** still holds the DOCISPAN crum claiming doc2 contains those I-spans
- `finddocscontainingsp` queries only the spanfilade and returns doc2 as a positive match
- `retrieverestricted` / `findcbcinarea2d` / `crumqualifies2d` perform **no POOM cross-check** at any level

The DOCISPAN crum in the spanfilade is a **permanent ghost entry**. The only way it would be cleaned up is if something explicitly deleted it from `spanf`, and no such call exists in the delete path.

---

## Question 19 [gregory]

> In the case of self-transclusion — COPY within the same document creating two V-positions for the same I-addresses — does `incontextlistnd` accumulate both V-positions during I→V conversion, and does `find_links` return both V-positions as separate entries in the endset specset?

### Gregory's Answer

## KB Synthesis

Yes to both parts.

**`incontextlistnd` accumulates both V-positions.**

The POOM is a multimap, not a bijection [SS-POOM-MULTIMAP]. After self-transclusion, the two copies of the content sit at distinct V-positions but share the same I-addresses — they are separate leaf crums in the POOM tree. When `findcbcinarea2d` searches by I-address range, it traverses all siblings at every level and recurses into every qualifying subtree, collecting every matching leaf [SS-POOM-MULTIMAP]. `incontextlistnd` performs insertion-sort into a linked list and **never replaces** existing entries [SS-CONTEXT-LIST]. Both V-positions are discovered in tree-traversal order and both are inserted into the sorted result list. The output is a `SortedSeq<Context>` ordered by V-address, with one entry per matching crum — so both V-positions appear as distinct contexts [INV-RETRIEVAL-V-SORTED].

**The endset specset from follow-link and retrieve-endsets contains both V-positions as separate entries.**

The I→V conversion path shared by `FOLLOWLINK` and `RETRIEVEENDSETS` is: `link2sporglset`/`retrieveendsetsfromspanf` → `linksporglset2specset` → `span2spanset` → `retrieverestricted` [SS-FOLLOWLINK]. `retrieverestricted` calls down into the POOM query machinery, which uses `findcbcinarea2d` + `incontextlistnd` — the same multimap accumulation described above. Both V-positions produce separate contexts, and each context yields a separate entry in the output specset.

This is confirmed empirically in [INV-LINK-IDENTITY-DISCOVERY]: a link created at one copy is discoverable (and its endset resolves) from the other copy within the same document, and vice versa. [EC-MULTISPAN-LINK-DUPLICATION] and [EC-PIVOT-LINK-FRAGMENTATION] further show the system produces multiple spans when the same content identity appears at more than one V-position — self-transclusion is exactly this case.

**Important caveat:** `find_links` itself (`FINDLINKSFROMTOTHREE`) returns link ISAs, not endset specsets. The link ISA appears once in the spanfilade regardless of how many V-positions reference its endpoint I-addresses, so `find_links` returns the link once. The multiplicity surfaces only when you resolve endsets via `FOLLOWLINK`, `RETRIEVEENDSETS`, or the retrieve-endsets path [SS-RETRIEVE-ENDSETS].

---

## Code Exploration

Now I have a complete trace through the code. Let me compile the full answer.

---

## Self-Transclusion: `incontextlistnd` and `find_links` Behavior

### Background: What COPY creates in the POOM

`docopy` [do1.c:45-65] does two things:
1. Calls `insertpm` to write new V↔I mapping crums into the document's POOM
2. Calls `insertspanf` to record the I-spans in the spanfilade

After `docopy(taskptr, docisa, &v2, ispanset)` where `ispanset` encodes I-span `[i1..i1+w]` (originally at V-position `v1`), the POOM now contains two leaf crums that reference the same I-addresses:

- **Crum A**: `V=[v1..v1+w]`, `I=[i1..i1+w]` (original insertion)  
- **Crum B**: `V=[v2..v2+w]`, `I=[i1..i1+w]` (self-transclusion copy)

---

### Question 1: Does `incontextlistnd` accumulate both V-positions during I→V?

**Yes.** Here is the full call path:

```
ispan2vspanset         [orglinks.c:389]
  → permute            [orglinks.c:404]
    → span2spanset     [orglinks.c:425]
      → retrieverestricted  [retrie.c:56]
        → retrieveinarea    [retrie.c:87]
          → findcbcinarea2d [retrie.c:229]
```

In `span2spanset` [orglinks.c:435], `retrieverestricted` is called with:
- `span1ptr = restrictionspanptr` (the I-span to look up), `index1 = I`
- `span2ptr = NULL` (no V constraint), `index2 = V`

```c
// orglinks.c:435
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                             (typespan*)NULL, targindex, (typeisa*)NULL);
```

`retrieverestricted` [retrie.c:56-85] clears `span2start` and `span2end` to zero when `span2ptr` is NULL:

```c
// retrie.c:71-76
if (span2ptr) { ... } else {
    tumblerclear (&span2start);
    tumblerclear (&span2end);
}
```

Then `crumqualifies2d` [retrie.c:270-305] evaluates the V constraint:

```c
// retrie.c:292-300
endcmp = iszerotumbler (span2end) ? TOMYRIGHT : whereoncrum (crumptr, offset, span2end, index2);
if ( endcmp < ONMYLEFTBORDER) { return(FALSE); }
startcmp = whereoncrum (crumptr, offset, span2start, index2);
if( (startcmp > THRUME)) { return(FALSE); }
```

When `span2end == 0`, `iszerotumbler` returns true → `endcmp = TOMYRIGHT` → check passes.  
When `span2start == 0`, `whereoncrum` returns `TOMYLEFT` for any crum with positive V-displacement → `TOMYLEFT < THRUME` → `startcmp > THRUME` is false → check passes.

The V constraint eliminates nothing. The I-span constraint (`span1`) matches both Crum A and Crum B, since they both map the same I-addresses. `findcbcinarea2d` [retrie.c:252-265] iterates all sibling crums:

```c
// retrie.c:252-264
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (...)) { continue; }
    if (crumptr->height != 0) {
        ...findcbcinarea2d recursively...
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);
    }
}
```

`incontextlistnd` [context.c:75-111] inserts each context into a linked list ordered by their I-position (`index1 = I`). Since both Crum A and Crum B have the same I-address range, both are inserted — one will be placed before/after the other in sorted order. Both contexts appear in the returned list.

Back in `span2spanset` [orglinks.c:439-445]:

```c
// orglinks.c:439-445
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

`context2span` [context.c:176-212] computes the V-span for each context by projecting the context's coverage onto the V-dimension (`targindex = V`). Crum A yields a V-span at `[v1..v1+w]`; Crum B yields a V-span at `[v2..v2+w]`. Both are appended via `onitemlist` [orglinks.c:464-537], which does **not** merge spans — it simply chains them as separate list items.

**`incontextlistnd` accumulates both V-positions. The resulting context list has two entries, one per crum.**

---

### Question 2: Does `find_links` return both V-positions as separate entries?

The relevant path for `RETRIEVE_ENDSETS` is:

```
doretrieveendsets         [do1.c:369]
  → retrieveendsetsfromspanf  [spanf1.c:190]
    → specset2sporglset        [sporgl.c:14]   V→I: converts link ISA vspec to I-sporgl
    → retrievesporglsetinrange [spanf1.c:237]  finds endset crums in spanfilade
    → linksporglset2specset    [sporgl.c:97]
        → linksporglset2vspec  [sporgl.c:127]
          → sporglset2vspanset [sporgl.c:141]
            → ispan2vspanset   [orglinks.c:389] I→V: converts I-span back to V-spans
```

In `retrieveendsetsfromspanf` [spanf1.c:237-266], `retrievesporglsetinrange` finds the spanfilade crums that store the endset's I-span. Each such crum was written by `insertspanf` [spanf1.c:15-54] during link creation, indexed by:
- `SPANRANGE`: I-span of the referenced content
- `ORGLRANGE`: link ISA prefixed with `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN`

The retrieved sporgl carries the raw **I-span** `[i1..i1+w]` of the referenced content.

Then `sporglset2vspanset` [sporgl.c:141-176] calls `ispan2vspanset` for that I-span:

```c
// sporgl.c:157
vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr);
```

As traced above, `ispan2vspanset` → `permute` → `span2spanset` → `findcbcinarea2d` finds **both** Crum A and Crum B, yielding two V-span entries: `[v1..v1+w]` and `[v2..v2+w]`.

These are accumulated into `*vspansetptr` via `onitemlist`, which chains them without merging (since `v1 ≠ v2`, they are disjoint and would not be merged even by `putvspaninlist`'s merge logic).

The final specset returned to the client is a single `typevspec` with:
- `docisa` = the document ISA
- `vspanset` = `[v1..v1+w] → [v2..v2+w]` (two separate V-span entries)

**`find_links` / `RETRIEVE_ENDSETS` does return both V-positions as separate V-span entries within the endset specset.** The single `typevspec` item has a `vspanset` list with two elements, one for each V-position where the transcluded content appears.

---

### Summary

| Step | Both V-positions? | Mechanism |
|------|:-----------------:|-----------|
| `findcbcinarea2d` walks POOM crums | **Yes** | Iterates all siblings; both crums qualify when V-constraint is unconstrained |
| `incontextlistnd` accumulates them | **Yes** | Inserts both into sorted context list [context.c:75-111] |
| `ispan2vspanset` returns both V-spans | **Yes** | Both contexts survive `context2span` + `onitemlist` loop [orglinks.c:439-445] |
| `RETRIEVE_ENDSETS` endset specset | **Yes** | `sporglset2vspanset` → `ispan2vspanset` → two V-span entries in `vspanset` field |

The key architectural reason this works correctly: I-addresses are stable identifiers in the permascroll. The POOM records every V↔I mapping independently. I→V conversion does an unconstrained scan over the V-dimension, so **all** V-positions that share an I-address are found. Self-transclusion is not a special case — it falls out naturally from the enfilade structure.

---

## Question 20 [gregory]

> When `docreatenewversion` copies the text subspace of a document that itself contains transcluded content (shared I-addresses with other documents), does the version's POOM preserve the original I-addresses from the transclusion source — making the version discoverable through `find_links` for links created against any document in the transclusion chain?

### Gregory's Answer

## KB Synthesis

Yes. The version's POOM preserves the original I-addresses from the transclusion source, and the version is fully discoverable through `find_links` for links anywhere in the transclusion chain.

**Mechanism: CREATENEWVERSION shares, not copies, I-addresses**

`docreatenewversion` copies the text subspace by calling `docopyinternal` → `insertpm`, which places existing I-addresses into the new POOM without allocating fresh ones [ST-VERSION-CREATE, Finding 0046]. If the source document's text subspace contains I-addresses that originated in a transclusion source (placed there by a prior `docopy`/vcopy), those same I-addresses appear verbatim in the version's POOM.

**Why transclusion I-addresses are preserved through version creation**

Vcopy preserves I-addresses from its source [ST-VCOPY, Finding 0018]. So if document A transcluded "shared text" from document B, A's POOM contains B's I-addresses at those V-positions. When V = CREATENEWVERSION(A), `docopyinternal` reads A's current vspan and copies all its I-addresses — including the ones that originated in B — into V's POOM. V now holds B's I-addresses directly [INT-VERSION-TRANSCLUSION, Finding 0032].

**Why find_links works across the full chain**

`find_links` operates entirely in I-space via the spanf index: it converts the query V-span to I-spans, then searches the spanfilade for links whose endpoints intersect those I-addresses [INT-LINK-VERSION, Finding 0046]. Since V shares I-addresses with both A and B, `find_links(V)` will discover:
- Links created against A's text (same I-addresses)
- Links created against B's text (same I-addresses, shared through transclusion)
- Links created against any document in the transclusion chain, by transitivity [INV-TRANSITIVE-IDENTITY, Findings 0007, 0008]

This is confirmed experimentally: CREATENEWVERSION of a document with transcluded linked content produces a version where `find_links` returns links from the original chain [INT-LINK-TRANSCLUSION, Finding 0043]:

> "Despite CREATENEWVERSION not copying link subspace entries to the version's POOM, find_links still works on the version. This is because link discovery operates on content identity (I-addresses), not POOM structure."

**The version has no link subspace entries but that is irrelevant**

The version's POOM contains no entries in the 2.x subspace — it has no link orgls of its own [ST-VERSION-CREATE, Finding 0043]. But link discoverability is independent of POOM link storage; it depends solely on I-address intersection in the spanf [INT-LINK-TRANSCLUSION, Finding 0043]. The spanf was populated when the original INSERT/COPY operations occurred and is never modified by version creation [INV-SPANF-WRITE-ONLY].

**Summary**

The invariant is: `version(doc) inherits the complete I-address set of doc.text_subspace`, and `find_links` is a pure function of I-address intersection, so the version is discoverable for every link reachable through any document sharing those I-addresses — the full transclusion chain, including transitive chains of transclusion and versioning [INV-TRANSITIVE-IDENTITY, Finding 0008].

---

## Code Exploration

Now I have everything I need to give a complete, code-grounded answer.

---

## Answer

**Yes — `docreatenewversion` preserves original I-addresses from the transclusion source, and those preserved I-addresses make the version discoverable via `find_links` for links targeting any document in the transclusion chain.**

Here is the precise mechanism, traced from source:

---

### 1. What `docreatenewversion` actually copies

`docreatenewversion` [do1.c:260–299]:

```c
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) return FALSE;   // line 281

vspec.itemid = VSPECID;
movetumbler(isaptr, &vspec.docisa);   // vspec points to the SOURCE document
vspec.vspanset = &vspan;              // ...over its full V-span

docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);   // line 293
```

The `vspec` passed to `docopyinternal` identifies the **source** document (`docisa = isaptr`) and covers its entire V-span. `doretrievedocvspanfoo` calls `retrievedocumentpartofvspanpm` [orglinks.c:155–162], which reads `cdsp.dsas[V]` and `cwid.dsas[V]` from the root crum — the bounding box of the source's entire V-space (including all transcluded content within it).

---

### 2. V→I translation: the source document's POOM is the oracle

`docopyinternal` [do1.c:74] calls `specset2ispanset`:

```c
if (!specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)) return FALSE;
```

`specset2ispanset` [do2.c:34–38] handles a `VSPECID`:

```c
findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)  // source doc's ORGL
&& (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr))
```

It looks up the **source document's** enfilade (not the new version's) and calls `vspanset2ispanset` [orglinks.c:397–402]:

```c
typeispanset *vspanset2ispanset(...) {
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

`permute` [orglinks.c:414–416] calls `span2spanset` for each span, which in turn calls:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);   // [orglinks.c:435]
```

The `(typeisa*)NULL` last argument means **no ISA filtering**. `retrieverestricted` walks the source POOM enfilade and returns every (I-range, V-range) crum whose V-coordinates intersect the query. `context2span` then extracts the **I-coordinates** from those crums.

**Outcome:** The `ispanset` produced is the complete set of permascroll I-addresses that the source document's V-space maps to — including any shared I-addresses from transcluded content (content that was itself inserted via `docopy` from another document, carrying over the same permascroll I-addresses).

---

### 3. I-addresses inserted into the new version's POOM unchanged

`docopyinternal` [do1.c:78] then calls:

```c
insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
```

In `insertpm` [orglinks.c:100–131]:

```c
for (; sporglset; sporglset = ...) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (&lstream, &crumorigin.dsas[I]);   // I-address placed here UNCHANGED
    movetumbler (&lwidth, &crumwidth.dsas[I]);
    movetumbler (vsaptr, &crumorigin.dsas[V]);     // new V-address assigned here
    ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);   // line 130
}
```

The I-coordinates (`lstream`, `lwidth`) come from the `ispanset` derived above and are placed into `crumorigin.dsas[I]` / `crumwidth.dsas[I]` **without modification**. Only the V-coordinates are freshly assigned (from `vsaptr`). The resulting POOM crums in the new version map new V-positions to exactly the same permascroll I-addresses as the source document had.

---

### 4. The spanfilade also records the shared I-addresses

`docopyinternal` [do1.c:79] also calls:

```c
insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

`insertspanf` [spanf1.c:15–54] indexes into the global spanfilade using the I-addresses from `ispanset` (the `ISPANID` branch, lines 26–29), keyed under the new document's ISA. This is what allows `find_links` to locate the version when searched by I-address.

---

### 5. How `find_links` discovers the version

`find_links` calls `dofindlinksfromtothree` [do1.c:348] → `findlinksfromtothreesp` [spanf1.c:56–103].

The query path: V-specs → `specset2sporglset` (V→I translation through the **queried** document's POOM) → `sporglset2linkset` (spanfilade search by I-address).

When a link was created against document A pointing to content at permascroll I-address X (stored in the spanfilade at I-address X), and document B's POOM maps some V-position to that same I-address X:

- B's `find_links` query translates B's V-position → I-address X → finds the link
- After versioning B → C via `docreatenewversion`, C's POOM also maps a V-position to I-address X (because `insertpm` preserved it unchanged)
- C's `find_links` query likewise resolves to I-address X → finds the same link

Links index the spanfilade by permascroll I-address. Transclusion and versioning both preserve those I-addresses. The identity of content _is_ its I-address.

---

### Summary

| Step | Code | What happens |
|------|------|-------------|
| `doretrievedocvspanfoo` | do1.c:281, orglinks.c:155 | Retrieves bounding V-span of source doc |
| `specset2ispanset` | do2.c:34–38 | Translates source doc's V-span → I-spans via **source's** POOM |
| `vspanset2ispanset` → `retrieverestricted` | orglinks.c:397, 435 | Walks source POOM; produces actual permascroll I-addresses including those from any transclusions |
| `insertpm` | orglinks.c:105–109 | Writes I-addresses **unchanged** into new version's POOM crums |
| `insertspanf` | spanf1.c:49–51 | Indexes those same I-addresses in global spanfilade under new version's ISA |
| `find_links` query | spanf1.c:70–100 | Converts query V-spec → I-addresses via new version's POOM; hits same spanfilade entries |

The POOM of the new version is not a snapshot of V-coordinates — it is a new mapping of new V-positions onto the **same underlying permascroll I-addresses**. Those addresses are the stable content identity in Xanadu. Any link ever created against content at those I-addresses — regardless of which document's V-space it was expressed in at link-creation time — is discoverable through the version.
