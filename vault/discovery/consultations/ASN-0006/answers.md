# Consultation Answers — Transclusion (COPY)

**Inquiry:** What must content sharing through transclusion guarantee? How does transclusion differ from duplication? What properties of the original are preserved in the copy?
**Date:** 2026-02-23 11:58
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> When content from one document appears in another through transclusion, must the system guarantee that both occurrences share the same identity rather than being independent copies?

### Nelson's Answer

## Yes — Shared Identity Is the Entire Point

Transclusion is not "copying with a link back." It is inclusion by reference to the *same* I-space content. The system **must** guarantee that both occurrences share identity. This is not one feature among many — it is the architectural foundation on which permanence, attribution, royalties, correspondence, and the distributed update solution all depend.

### The Architectural Guarantee

Xanadu has two address spaces precisely to make this work:

- **I-space** stores content permanently. Every byte has one permanent address.
- **V-space** arranges references to I-space content into documents.

When content appears in two documents, both documents' V-space mappings point to the *same* I-space addresses. There is one set of bytes, referenced from two places.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The term "virtual copies" is precise — they are *virtual*, not actual. The bytes exist once in I-space; V-space creates the appearance of their presence in multiple documents.

### Nelson's Explicit Statement

Nelson is unambiguous that transclusion involves no duplication:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." [LM 2/36]

The COPY operation in the FEBE protocol creates a V-space mapping to existing I-space content — it does not allocate new I-space bytes. The word "copy" in the protocol name is misleading by modern standards; it means "include by reference."

### Why Independent Copies Would Break Everything

If two occurrences were independent copies with separate I-space addresses, five guarantees would collapse:

**1. Attribution.** Nelson promises: "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40] This works because the I-address encodes the originating document. An independent copy would have a *different* I-address pointing to the *copying* document, severing the chain to the original author.

**2. Correspondence.** Version comparison depends on shared I-addresses. "A facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20] The system identifies corresponding parts by checking whether V-space positions in different documents map to the same I-address. Independent copies would destroy this.

**3. Royalties.** "There is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned." [LM 2/43] Royalties flow to the *owner* of the I-space content. If transclusion created independent copies at the copier's I-address, the original author would receive nothing when their words were delivered through someone else's document.

**4. The Distributed Update Solution.** Nelson identifies this as a key achievement. If transclusion created independent copies, the copies would diverge from the original — which is exactly the problem Xanadu was built to solve.

**5. Link Survivability.** Links attach to I-space addresses. A link to a passage in document A should resolve when that passage appears (via transclusion) in document B — but only if both reference the same I-address.

### The Glass Pane Metaphor

Nelson's metaphor makes the design intent vivid:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

Your document has painted content (your I-space bytes) and transparent windows (V-space references to others' I-space bytes). When you look through the window, you see the *original* — not a photograph of it.

### The Live vs. Dead Distinction

Nelson draws this contrast explicitly:

> "Remember the analogy between text and water. Water flows freely, ice does not. The free-flowing, live documents on the network are subject to constant new use and linkage, and those new links continually become interactively available. Any detached copy someone keeps is frozen and dead, lacking access to the new linkage." [LM 2/48]

Transclusion produces *live* references — connected to the original, participating in the network. Independent copies are *dead* — severed, frozen, disconnected.

### Summary

The guarantee of shared identity is not merely a technical optimization. It is the mechanism through which Xanadu delivers its core promises: permanent attribution, automatic royalties, version correspondence, distributed update, and the interconnected structure of literature. Two documents referencing the same content must share the same I-space addresses, because the I-address *is* the identity.

---

## Question 2 [nelson]

> If a reader encounters transcluded content in a document, must the system always be able to reveal the original document and position from which that content originated?

### Nelson's Answer

## Yes — unconditionally

Revealing the origin of transcluded content is not merely a feature but a **structural invariant** of the system. Nelson makes this guarantee in the strongest possible terms:

> "This world nevertheless remains simple in design. The virtuality is simple in structure and repeats in layers. You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

The word "at once" is deliberate. This is not a search operation that might fail — it is an immediate property of the content itself.

## Why it is structural, not metadata

The guarantee follows from the I-space addressing architecture. Every byte in the docuverse has a permanent I-space address — a tumbler with the form:

```
Node.0.User.0.Document.0.Element
```

The **Document field** directly encodes which document originally created that byte. When content is transcluded, it is not copied — it is referenced by its permanent I-address:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The distinction between native and non-native bytes is intrinsic to the address — you cannot strip it. To *fetch* the content, the system must request it from its home location. The connection cannot be severed because the fetching mechanism requires it.

## What the reader can do

Nelson describes the reader's experience in terms of navigation through layered windows:

> "Only when you step through the window — turning one glass page and going on in the next — do you reach the original that you wanted. But stepping through the window means you are now in another work." [LM 2/34]

The reader can also ask the reverse question — given some content, what else includes it:

> "FINDDOCSCONTAINING: This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

And the two-way reading guarantee:

> "It must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time." [LM 2/40]

## A subtlety: home document vs. current position

The system can always reveal the **home document** (which document created the bytes). Whether those bytes still appear in the home document's **current V-space arrangement** is a separate question — the owner may have "deleted" the content from their current version, which removes it from V-space but not from I-space:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

So the origin document is always identifiable (from the I-address), but the content may no longer appear in the origin document's current view. It will still be recoverable through historical backtrack to a previous version where it was present.

## Summary

The system **must** always be able to reveal the original document from which transcluded content originated. This is not a policy choice — it is a consequence of the addressing architecture. The I-address IS the proof of origin, and fetching content through transclusion requires consulting that address. Nelson's guarantee — "you can at once ascertain the home document of any specific word or character" — is absolute and unconditional.

---

## Question 3 [nelson]

> Can an author who transcludes content from another document ever modify the transcluded portion independently, or must it remain identical to the original?

### Nelson's Answer

## Transcluded Content Cannot Be Modified Independently

The transcluded portion **must remain identical to the original**. This is not a limitation but a fundamental architectural guarantee. However, Nelson provides a powerful mechanism for creating what *appears* to be a modified version.

### Why Modification Is Impossible

Transcluded content lives in someone else's I-space. Your document's V-stream points to those bytes at their permanent home location:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

You cannot change bytes you do not own:

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

The COPY operation (which creates transclusion) shares I-addresses with the source rather than creating new bytes. There is nothing to modify — your document contains a reference, not a duplicate.

### The Mechanism for "Modification": Versioning by Inclusion

Nelson solves this through **derivative documents** — new documents that interleave transclusions of the original with the author's own new content:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

> "A particular form of compound document is one which consists explicitly of an original and changes to it — which may be made by anyone. (We may call this a derivative document.)" [LM 2/37]

The Shakespeare example makes this concrete. If Hamlet is already published, E.G. Jewett can create his own version by: transcluding the first part of the original up to "in the soliloquy," inserting his own word "luge," then transcluding the rest of the play. The result reads as a modified Hamlet, but structurally it is transclusions plus one new native byte-span.

### The Glass Pane Metaphor

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

The "painted" portions are your native content (modifications). The "clear glass" portions are windows showing the original unchanged. You never paint on someone else's glass — you add your own pane with a mix of paint and windows.

### Transparency and Recoverability

This design ensures modifications are always transparent:

> "This means a whole new pluralistic publishing form. If anything which is already published can be included in anything newly published, any new viewpoint can be freely presented by an easily-made annotated collage. (The old viewpoint is still present too — you can always say, 'Show me what this originally was.')" [LM 2/45]

Because transcluded bytes and native bytes have different I-space origins, the system can always distinguish what the derivative author wrote from what they transcluded. Attribution is structural, not metadata:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

### Royalty Implications

The structural separation also drives fair compensation:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

The system knows exactly which bytes are transcluded (royalty to original author) and which are native (royalty to modifier) because they have different I-addresses.

### Summary

| What you want | How Xanadu does it |
|---|---|
| Show original content unchanged | Transclude it (COPY operation) |
| Show modified content | Create a derivative document mixing transclusions with your own new text |
| Let readers see both | Structural — the system always knows which bytes are yours vs. transcluded |
| Compensate both authors | Automatic — royalty splits by I-space origin |

The answer is architecturally clean: you never touch someone else's bytes. You compose a new document from references to their bytes and your own new bytes. The reader sees a unified result; the system preserves the full provenance.

---

## Question 4 [nelson]

> When content is transcluded, do links that point to that content in its original document also apply when the same content appears in the transcluding document?

### Nelson's Answer

# Links and Transcluded Content

**Yes.** Links that point to content in its original document also apply when that same content appears in a transcluding document. This is not a special feature but an architectural consequence of how I-space, V-space, links, and transclusion interact.

## The Mechanism

The answer follows from three design facts:

**1. Links attach to I-space addresses, not V-space positions.**

> "A Xanadu link is not between points, but between spans of data." [LM 4/42]

Links point to the permanent identity of bytes (I-space), not to their current arrangement in any particular document (V-space).

**2. Transclusion shares I-space addresses.**

> "Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." [LM 4/11]

When Bob transcludes content from Alice's document, Bob's document creates a V-space mapping to the *same* I-space addresses. The bytes are not copied — they are referenced. Both documents point to identical I-space content.

**3. Therefore, any link targeting those I-space addresses applies in both documents.**

If Carol creates a link whose endset points to I-addresses X through Y, and those addresses appear in both Alice's document (natively) and Bob's document (by transclusion), Carol's link connects to the content in both places.

## Nelson's Explicit Confirmation (for Versions)

Nelson states this principle explicitly for the case of versions, which share I-space content through the same mechanism as transclusion:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

Versions share I-space addresses just as transclusions do. The principle is identical: shared I-space identity means shared link applicability.

## Supporting Operations

Two FEBE operations confirm the system is designed to work this way:

**FINDDOCSCONTAINING** — finds all documents containing specified material, regardless of where native copies are located:

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." [LM 4/63]

This operation exists precisely because the system tracks where content appears across transclusions.

**FINDLINKSFROMTOTHREE** — searches links by endset address ranges:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

When a reader asks "what links connect to this passage?" while reading Bob's transcluding document, the system resolves the V-space position to I-space, finds the same I-addresses as in Alice's original, and discovers all links targeting that content.

## Bidirectional Discovery

Nelson explicitly requires that readers can discover all connections to any content they are viewing:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." [LM 2/46]

This guarantee applies regardless of whether you are reading the content in its native document or in a transcluding document. The content is the same bytes at the same I-addresses; the links are the same links.

## The Deeper Point

This behavior is what makes transclusion fundamentally different from copying. A copy severs the content from its identity — and therefore from its links. A transclusion preserves identity — and therefore preserves all connections.

> "Note also that he or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy. And that will be a considerable deprivation in the world we are talking about." [LM 2/48]

The "dynamic link connections" that copying destroys are precisely the connections that transclusion preserves. When content appears by transclusion, it brings its entire web of links with it — annotations, citations, comments, counterpart links — because those links attach to the content's permanent identity, not to the document that happens to display it.

---

## Question 5 [nelson]

> Must the original author of content always be discoverable when that content appears through transclusion in someone else's document?

### Nelson's Answer

## Yes — Structural Traceability Is a Fundamental Guarantee

The original author's home document is **always** discoverable for transcluded content. This is not a feature that can be turned off — it is inherent in how content is addressed.

### The Structural Basis

Every byte in Xanadu has a permanent I-space address encoding its origin:

```
Node.0.User.0.Document.0.Element
```

The **User** and **Document** fields directly identify who created the content and in which document. When content is transcluded, it is fetched from its home location, not copied:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

This means the connection to the source is the **delivery mechanism itself** — you cannot receive the bytes without knowing where they came from.

### Nelson's Explicit Guarantee

Nelson states this as a user-facing promise, not merely an implementation detail:

> "This world nevertheless remains simple in design. The virtuality is simple in structure and regular in layout. You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

The phrase "any specific word or character" is crucial. It applies to every byte in a compound document, whether native or transcluded. The user can always ask "where did this come from?" and receive a definitive answer.

### Why This Cannot Be Circumvented

Attribution in Xanadu is structural, not metadata:

- In conventional systems, attribution is a property *attached* to content (an author field, a copyright notice). These can be stripped or falsified.
- In Xanadu, the origin **is** the address. To fetch transcluded content, the system must request it from its permanent I-space location. The connection cannot be severed because the fetching mechanism requires it.

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The bytes appear seamlessly in the compound document's V-stream, but their I-addresses permanently encode their origin.

### A Subtlety: Visible vs. Available

There is one nuance. Nelson distinguishes between what the system **knows** and what the front end **displays by default**. In the context of link types, he notes:

> "Note that a quote-link is not the same as an inclusion, which is not ordinarily indicated" [LM 4/53]

This suggests that a front end might not visually flag every transcluded passage by default. But the information is always structurally available — the user can "at once ascertain" the home document of any character on demand. The front end chooses presentation; the back end guarantees traceability.

### A Second Subtlety: Author Identity vs. Account

The I-address always reveals the **account** that created the content. Whether the real-world person behind that account is identifiable depends on whether they published under their own name or anonymously ("John Doe publication" [LM 2/60]). But even for anonymous publications, the account and document of origin are permanently encoded in the address. You always know *which document* the content came from, even if you don't know *who* is behind that document.

### Summary

| What is guaranteed | How |
|---|---|
| Home document of any byte | I-address encodes document origin |
| Account that created it | I-address encodes user field |
| Discoverability on demand | Structural — cannot be stripped |
| Visual indication by default | Front-end choice — not guaranteed |
| Real-world author identity | Only if not anonymous publication |

The answer to your question is **yes**: the system guarantees that for any transcluded content, the original document and account are always discoverable. This is one of Xanadu's fundamental guarantees — attribution through addressing, not through metadata.

---

## Question 6 [nelson]

> If the system supports compensation for content use, must transclusion trigger a payment or royalty obligation to the original creator that mere duplication would not?

### Nelson's Answer

# Transclusion and Royalty Obligation

## Yes — But the Mechanism Is More Precise Than "Transclusion Triggers Payment"

The royalty obligation is not triggered by the *act of transclusion* itself but by the *delivery of bytes* to a reader. Transclusion is the mechanism that ensures delivery routes through the original creator's accounting. The distinction matters.

## Royalty Attaches to Delivery, Not to Reference

Nelson's royalty model is per-byte-delivered:

> "In our planned service, there is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned, as part of the proportional use of byte delivery." [LM 2/43]

When Bob transcludes Alice's content into his document, nothing happens economically at the moment of transclusion. But when a reader views Bob's compound document, Alice's bytes are delivered from their home location, and her cash register increments:

> "Each published document has a cash register. This is a system-maintained counter which increments whenever bytes or links are delivered out of the document." [LM 5/13]

The split is proportional:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

## Within the System, There IS No "Mere Duplication"

This is the critical architectural point. The FEBE COPY operation *is* transclusion — it shares I-addresses with the source rather than creating new content:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

The "copy" creates a V-space mapping to existing I-space content. The bytes remain native to their original document. There is no FEBE command that creates a true byte-for-byte duplicate with fresh I-addresses. To create genuinely new content at new I-addresses, you would have to INSERT — physically retyping the text.

So within Xanadu, the question dissolves: **there is no "mere duplication" mechanism that could evade royalty**. Every way of incorporating existing content (COPY, CREATENEWVERSION, windowing) preserves the I-address connection that enables royalty tracking.

## Outside the System, Enforcement Is Impossible

Nelson is explicit that copying content *out of* the system — to paper, to disk — evades royalty, and this cannot be technically prevented:

> "There is no way whatever to ascertain or control what happens at the users' terminals. Therefore perforce all use whatever is legitimate." [LM 2/47]

> "Publisher acknowledges, however, that no means for enforcement of this provision is possible within the Xanadu network unless violating users re-store copies of the material on the Xanadu network at a later time for resale and this resale comes to the attention of Publisher." [LM 5/20]

But Nelson argues the incentive structure makes external copying self-defeating:

> "Note also that he or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy. And that will be a considerable deprivation in the world we are talking about." [LM 2/47]

> "Remember the analogy between text and water. Water flows freely, ice does not. The free-flowing, live documents on the network are subject to constant new use and linkage, and those new links continually become interactively available. Any detached copy someone keeps is frozen and dead, lacking access to the new linkage." [LM 2/48]

## Summary

| Scenario | Royalty to Original Creator? |
|----------|------------------------------|
| Transclusion viewed by reader | **Yes** — bytes delivered from home location, cash register increments |
| COPY within system | **Yes** — COPY *is* transclusion (shares I-addresses) |
| CREATENEWVERSION | **Yes** — shares I-addresses with source version |
| Content re-typed via INSERT | **No** — new I-addresses, new content; no structural connection |
| Copied to paper/disk outside system | **No** — technically unenforceable; socially self-defeating |

The design is elegant: transclusion is not merely a payment trigger bolted onto quotation. It is the *only* way to incorporate existing content within the system, and the royalty mechanism is built into the delivery path that transclusion creates. The system does not distinguish "quotation that pays" from "quotation that doesn't" — all in-system quotation pays, by construction.

---

## Question 7 [nelson]

> When a new version of the original document is created, must transcluded content in other documents reflect the original version that was shared, or track the latest version?

### Nelson's Answer

# Transclusion and Versioning: Both Modes by Design

Nelson explicitly addresses this question and provides for **both behaviors** — the choice belongs to the user and front end, not the system.

## The Two Window Modes

Nelson specifies two distinct ways a transclusion (which he calls a "quote-window" or "inclusion") can relate to its source:

> "A quotation — an inclusion window — may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

**Time-fixed (frozen reference):** The transclusion shows the content as it was at a specific moment. If the original is later revised, the transclusion does not change. The reader can explicitly ask "What has this passage become?" to see the current state — but must opt in.

**Location-fixed (floating in time):** The transclusion tracks the current state of the source location. If the original document is revised, the transclusion automatically reflects the changes.

## Why Both Modes Are Architecturally Possible

The I-space/V-space separation makes this work:

- **I-space** is permanent. Every byte ever created has an immutable address. When you transclude content, you reference those permanent I-addresses.
- **V-space** is the document's current arrangement — a mapping from reading positions to I-space addresses. Editing changes V-space; I-space is untouched.

A **time-fixed** transclusion references specific I-addresses. Those bytes never change, so the transclusion is frozen by nature. This is the architectural default — COPY in the FEBE protocol creates a V-space mapping to existing I-space addresses, and those addresses are permanent.

A **location-fixed** transclusion requires the front end to re-resolve through the source document's current V-space arrangement. When the source is edited, its V-space changes (new content gets new I-addresses, rearrangements change the mapping), and the transclusion follows.

## Version-Spanning Links Support This

Nelson describes how links (and by extension, transclusions) can follow through versions:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

> "When a document is updated, a reader will ordinarily want to see the new version — but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version — if it's still there." [LM 2/43]

The correspondence mechanism (shared I-space origin between versions) enables this refractive following. The system can trace which parts of a new version correspond to parts of an old version, because they share I-addresses.

## The Distributed Update Solution

Nelson frames location-fixed windowing as solving a fundamental problem:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." [LM 2/36]

This is the location-fixed mode: your document windows to a living source, and when that source changes, your view updates.

## Summary

| Mode | Behavior | Use Case |
|------|----------|----------|
| **Time-fixed** | Shows content as it was when window was created | Frozen citation, legal reference, scholarly quotation of a specific edition |
| **Location-fixed** | Automatically reflects current version | Living reference, documentation that should track updates |

The answer to your question is: **it depends on which mode the user chooses.** Nelson designed for both. The system does not force one behavior — it provides the architectural primitives (permanent I-addresses, version correspondence, refractive following) that let the front end implement either mode at the user's discretion.

---

## Question 8 [nelson]

> Is there a limit to how many times content can be transitively transcluded — that is, can a document transclude content that is itself a transclusion from a third document?

### Nelson's Answer

## No Limit: Transclusion Depth Is Explicitly Unbounded

Nelson directly addresses this question and the answer is unambiguous: **there is no limit**. Transclusion can be layered indefinitely.

### Nelson's Explicit Statement

From the windowing discussion [LM 2/34]:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, **and so on indefinitely.**"

And more directly [LM 2/36, from the windowing concept]:

> "A document may have a window to another document, and that one to yet another, **indefinitely.** Thus A contains part of B, and so on. One document can be built upon another, and yet another document can be built upon that one, **indefinitely**: each having links to what was already in place."

### Why There Is No Architectural Bottleneck

The reason unlimited depth works is the I-space/V-space separation. Transclusion is not chain-following — it is always a direct reference to permanent I-space content.

When document B transcludes a passage from document A, B's V-space maps directly to A's I-space addresses. When document C then transcludes that same passage from B, C's V-space maps to the *same* I-space addresses — A's original bytes. The content always lives at its original home location:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to **their home locations.**" [LM 4/11]

So regardless of how many documents transclude the same content through however many intermediaries, retrieval always resolves to the single permanent I-space location. There is no cascading chain of indirection to follow — just a V-to-I mapping that points to the origin.

### The Attribution Guarantee Holds at Any Depth

Even through arbitrary layers of transclusion, origin traceability is preserved:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This works because the I-address *encodes* the originating document. No matter how many layers of glass panes you look through, the bytes you see are identified by their permanent I-address, which names their home document.

### Economic Robustness

The royalty model also handles arbitrary depth. Nelson specifies that royalties are per-byte-delivered and flow to the content owner:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

Since every byte traces to its I-space origin regardless of transclusion depth, the royalty always reaches the right person.

### Summary

Nelson's design explicitly permits and anticipates unlimited transitive transclusion. This is not a theoretical edge case he overlooked — it is a feature he highlighted with the glass-pane metaphor and the word "indefinitely." The I-space/V-space architecture makes it work without performance degradation, because every transclusion is structurally a direct reference to permanent content, not a pointer-to-a-pointer chain.

---

## Question 9 [nelson]

> Must the system guarantee that deleting a transclusion reference from a document leaves the original content completely unaffected in its source document?

### Nelson's Answer

## Yes — Absolutely and by Multiple Independent Principles

Nelson's design makes this guarantee through several interlocking mechanisms, any one of which would be sufficient on its own.

### 1. Transclusion Is Reference, Not Copy

A transclusion creates a V-space mapping in the *referencing* document that points to I-space content owned by the *source* document. No bytes are moved or duplicated:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "No copying operations are required among the documents throughout the system." [LM 2/36]

Deleting the transclusion reference removes a V-space mapping in *your* document. The source document's V-space and I-space are untouched — they were never involved in the operation.

### 2. DELETE Operates on V-Space Only

DELETE removes content from the current document's virtual arrangement. It does not touch I-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

Nelson is explicit that this applies across document boundaries:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

### 3. The Non-Destruction Guarantee

This is one of Nelson's fundamental guarantees:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

### 4. Ownership Isolation

Only the owner may modify a document:

> "Every document has an owner... Only the owner has a right to withdraw a document or change it." [LM 2/29]

Bob's operations on Bob's document cannot affect Alice's document. The ownership boundary is absolute. Deleting a transclusion reference in Bob's document is an operation on Bob's V-space — Alice's document is architecturally unreachable from that operation.

### 5. I-Space Immutability

Even setting aside all the above, I-space content is immutable by definition. Content at an I-space address never changes, period. The source document's content lives in I-space. No operation anywhere in the docuverse can alter it.

### Summary

Deleting a transclusion reference is a purely local operation on the referencing document's V-space arrangement. The original content in the source document is unaffected because:

- No bytes were ever copied (reference, not copy)
- DELETE modifies V-space, not I-space
- I-space is immutable
- Ownership boundaries prevent cross-document modification
- Nelson explicitly guarantees that modifications never damage originals

This is not merely a design choice — it is a structural consequence of the I-space/V-space separation that is foundational to the entire system.

---

## Question 10 [nelson]

> Can an author prevent their content from being transcluded by others, or does the design guarantee that all published content is available for transclusion by anyone?

### Nelson's Answer

# No. Published Content Cannot Be Withheld from Transclusion.

This is one of the most explicitly settled questions in Literary Machines. The design **guarantees** that all published content is available for transclusion by anyone. An author who publishes relinquishes the right to prevent it.

## The Publication Contract

The act of publication is an irrevocable grant of transclusion permission. Nelson makes this a contractual requirement:

> "Since the copyright holder gets an automatic royalty, anything may be quoted without further permission. That is, permission has already been granted: for part of the publication contract is the provision, 'I agree that anyone may link and window to my document.'" [LM 2/45]

This is not optional. It is a term of the publishing contract that every participant signs:

> "To bypass some legal problems, we foresee establishing copyright convention internal to the network and contractually agreed upon by all participants. To wit, if you publish a thing through the network, you have to agree to the same rules as everybody else-- which are intended to create a fair balance of incentives." [LM 2/41-2/45]

## The Explicit Relinquishment

Nelson frames this as a two-sided coin — you get the freedom to transclude others' work, and in return you give up the power to prevent others from transcluding yours:

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." [LM 2/43]

The word "relinquishing" is deliberate. It is a permanent surrender, not a revocable preference.

## The Tradeoff: Control for Compensation

The logic is clear: traditional copyright conflates two goals — compensating creators and controlling use. Nelson separates them. You lose control but never lose compensation:

> "In our planned service, there is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned, as part of the proportional use of byte delivery." [LM 2/43]

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

Every transclusion pays the original author. The economic right is preserved; the control right is surrendered.

## The Resulting Freedom

This creates what Nelson calls "a whole new pluralistic publishing form":

> "This means a whole new pluralistic publishing form. If anything which is already published can be included in anything newly published, any new viewpoint can be freely presented by an easily-made annotated collage. (The old viewpoint is still present too — you can always say, 'Show me what this originally was.')" [LM 2/45]

And concretely:

> "Document A can include Document B, even though Document B is owned by someone else." [LM 2/35]

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate-- without damaging the originals. This is done by inclusion links." [LM 2/45]

## The One Exception: Private Documents

The only way to prevent transclusion is to **not publish**. Private documents are accessible only to the owner and designees:

> "A document may be private or published. [...] A private document may be read and linked-to only by the owner and his or her associates." [LM 2/42]

There is also "privashing" — making a document universally accessible but retaining the right to withdraw it. But note: privashed documents receive no royalty, which is an incentive to publish formally.

## What About Withdrawal?

Once published, withdrawal is extremely difficult by design:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

The reason is precisely because others will have linked to and transcluded the content. Their links and transclusions — which are *their* property at *their* addresses — depend on continued access.

## Summary

| Status | Can prevent transclusion? | Receives royalty? |
|--------|--------------------------|-------------------|
| **Private** | Yes (only owner/designees access) | N/A |
| **Privashed** | Yes (can withdraw at any time) | No |
| **Published** | **No — permanently relinquished** | **Yes — automatic per-byte** |

The design is unambiguous: publication is a permanent, contractual grant of universal transclusion rights. The author trades control for guaranteed compensation. This is not a side effect — it is the foundation of the entire system.

---

## Question 11 [gregory]

> When COPY transfers a V-span from document A to document B, does docopy reuse the exact same I-addresses from A's POOM in B's new POOM entries, or does it allocate fresh I-addresses and duplicate the granfilade content?

### Gregory's Answer

## KB Synthesis

# Answer: COPY Reuses Existing I-Addresses

COPY (vcopy/transclusion) **reuses the exact same I-addresses** from document A's POOM in document B's new POOM entries. It does **NOT** allocate fresh I-addresses or duplicate granfilade content.

## Evidence

### Core Mechanism

[ST-VCOPY] (Finding 0002): "The vcopy operation adds references to existing content identities into the target document. It does not copy the content itself — it creates new references to the same identities that the source document references."

[INT-SPORGL-TRANSCLUSION]: "During vcopy, the sporgl carries the content's I-address identity through the copy operation. Because the sporgl preserves the original I-address (not a new one), the destination document ends up referencing the same content identities as the source."

### Postcondition

[ST-VCOPY] (Finding 0018): "Vcopy postcondition: for the copied span, `I-addresses(target[v_target..v_target+len]) = I-addresses(source[v_source..v_source+len])`. This is what makes transitive identity work and distinguishes vcopy from insert (which creates new I-addresses)."

### Contrast with INSERT

[INV-IADDR-PROVENANCE]: "Every I-address has exactly one native document — the document where INSERT first allocated it. COPY does not allocate new I-addresses; it creates V→I mappings that reference existing ones."

[INV-DELETE-NOT-INVERSE] (Finding 0064): "The only identity-preserving restoration is VCOPY from a document that still references the original I-addresses. VCOPY shares existing I-addresses rather than allocating new ones."

### Implementation Evidence

[ST-VCOPY] (Finding 0046): "COPY shares the source's existing I-addresses in the target document's POOM via `insertpm`."

## Why This Matters

This I-address sharing is the mechanism that enables:

1. **Transitive identity** [INV-TRANSITIVE-IDENTITY]: Document C can transclude from B, which transcluded from A, creating a three-way identity relationship
2. **Link discovery** [INT-LINK-TRANSCLUSION]: Links on transcluded content are discoverable from all documents sharing those I-addresses
3. **Version comparison** [INT-SPORGL-VERSION-COMPARE]: `compare_versions` works by I-address intersection across documents

The key architectural distinction: INSERT allocates fresh I-addresses (extending the granfilade), while COPY creates new V→I mappings in the POOM that reference existing I-addresses (no granfilade growth).

## Code Exploration

Perfect! Finding 0046 directly answers your question. Let me trace through the code with full citations to provide the complete answer.

---

# Answer: COPY Reuses Exact I-Addresses

**docopy reuses the exact same I-addresses from document A's POOM in document B's new POOM entries.** It does NOT allocate fresh I-addresses or duplicate granfilade content.

## Evidence Chain

### 1. docopy's Operation Flow

`backend/do1.c:45-65` - The complete COPY operation:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
	return (
	   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)  // [1]
	&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
	&& acceptablevsa (vsaptr, docorgl)
	
	/* the meat of docopy: */
	&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)        // [2]
	&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)    // [3]
	);
}
```

**Key operations:**
1. **[1] specset2ispanset** - Extracts I-addresses from source document A's POOM
2. **[2] insertpm** - Inserts those SAME I-addresses into destination document B's POOM  
3. **[3] insertspanf** - Updates the spanfilade index (no content allocation)

**Critically: No call to `inserttextgr` or any content allocation function.**

### 2. I-Address Extraction from Source

`backend/do2.c:13-45` - Converting V-spans to I-spans:

```c
bool specset2ispanset(typetask *taskptr, typespec *specset, typeispanset *ispansetptr, int type)
{
	// ...
	if (((typeitemheader *)specset)->itemid == VSPECID) {
		findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl,type)
		&& (ispansetptr = vspanset2ispanset (taskptr, docorgl, 
		                   ((typevspec *)specset)->vspanset, ispansetptr))
	}
	// ...
}
```

This calls `vspanset2ispanset` at `backend/orglinks.c:397-402`:

```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, 
                                 typevspanset vspanptr, typeispanset *ispansetptr)
{
	return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

The `permute` function walks source document A's POOM tree and extracts the I-addresses that correspond to the specified V-span. **These are the EXISTING I-addresses allocated when content was first INSERTed into document A.**

### 3. I-Address Reuse in Destination

`backend/orglinks.c:75-134` - **THE SMOKING GUN:**

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl, 
              tumbler *vsaptr, typesporglset sporglset)
{
	tumbler lstream, lwidth;
	typewid crumorigin, crumwidth;
	
	for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
		unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
		
		movetumbler (&lstream, &crumorigin.dsas[I]);    // [LINE 105] ← I-address from SOURCE
		movetumbler (&lwidth, &crumwidth.dsas[I]);      // [LINE 109] ← I-width from SOURCE
		movetumbler (vsaptr, &crumorigin.dsas[V]);      // [LINE 113] ← V-address in TARGET
		
		shift = tumblerlength (vsaptr) - 1;
		inc = tumblerintdiff (&lwidth, &zero);
		tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
		
		insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
		tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);
	}
	return (TRUE);
}
```

**Lines 105-113 are the definitive proof:**
- **Line 105:** `movetumbler (&lstream, &crumorigin.dsas[I])` - Copies the I-address from the source sporgl directly into the destination POOM entry
- **Line 109:** `movetumbler (&lwidth, &crumwidth.dsas[I])` - Copies the I-width from the source
- **Line 113:** `movetumbler (vsaptr, &crumorigin.dsas[V])` - Sets the NEW V-address in the destination

The destination POOM entry contains the EXACT SAME I-address that existed in the source document.

### 4. Spanfilade Index Update (Not Content Allocation)

`backend/spanf1.c:14-53` - The spanfilade insertion:

```c
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr, 
                 typesporglset sporglset, INT spantype)
{
	for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
		if (((typeitemheader *)sporglset)->itemid == ISPANID) {
			movetumbler (&((typeispan *)sporglset)->stream, &lstream);
			movetumbler (&((typeispan *)sporglset)->width, &lwidth);
			movetumbler (isaptr,&linfo.homedoc);
		}
		// ...
		movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
		insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
	}
	return (TRUE);
}
```

This function updates the spanfilade index to record: "document B now contains I-span X." **It does NOT allocate new content** - it merely updates the reverse index that allows queries like "which documents contain I-address X?"

## Contrast with INSERT

`backend/do1.c:87-123` - INSERT operation:

```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
	makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
	ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)  // [ALLOCATES]
		&& docopy (taskptr, docisaptr, vsaptr, ispanset)                 // [THEN MAPS]
	);
	return(ret);
}
```

**INSERT does TWO steps:**
1. `inserttextingranf` - Allocates FRESH I-addresses in the granfilade and stores the text content
2. `docopy` - Maps those new I-addresses into the document's POOM

**COPY does ONLY step 2** - it maps existing I-addresses without allocating new ones.

## Content Allocation Function

`backend/granf2.c:82-99` - What content allocation looks like:

```c
bool inserttextgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, 
                  typetextset textset, typeispanset *ispansetptr)
{
	tumbler lsa, spanorigin;
	
	if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))  // [ALLOCATE I-ADDRESS]
		return (FALSE);
	movetumbler (&lsa, &spanorigin);
	for (; textset; textset = textset->next) {
		locinfo.infotype = GRANTEXT;
		locinfo.granstuff.textstuff.textlength = textset->length;
		movmem(textset->string,locinfo.granstuff.textstuff.textstring, 
		       locinfo.granstuff.textstuff.textlength);
		insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);            // [STORE CONTENT]
		tumblerincrement (&lsa, 0, textset->length, &lsa);
```

**Note:** `docopy` NEVER calls this function. Only `doinsert` does.

## From Finding 0046

The existing finding confirms:

> "When INSERT creates text, it allocates fresh I-addresses. COPY does NOT create new I-addresses; it references existing ones. Therefore each I-address has exactly ONE native document (where it was first INSERTed)." [`findings/0046-poom-duplicate-iaddresses.md:145-146`]

> "The ONLY difference is the I-address range:
> - INSERT: allocates NEW I-addresses under target document  
> - COPY: references EXISTING I-addresses from source document" [`findings/0046-poom-duplicate-iaddresses.md:153-155`]

## Summary

**When COPY transfers V-span [1.1, 1.5) from document A to document B:**

1. Read A's POOM to find I-addresses for V-span [1.1, 1.5) → e.g., I-span [A.100, A.105)
2. Write B's POOM entry: V-position 1.x → **SAME I-address A.100** (not a fresh allocation)
3. Update spanfilade index: "Document B now contains I-span [A.100, A.105)"

**Result:** Both documents' POOMs point to the SAME I-addresses in the shared granfilade. The text content exists ONCE in the granfilade, referenced by TWO POOMs.

**This is the foundation of transclusion in udanax-green:** Content identity (I-addresses) is preserved across COPY operations. Multiple documents can reference the same content without duplication.

---

## Question 12 [gregory]

> If document A contains "Hello" (I-addresses .0.1.1-.0.1.5) and document B transcludes that span via COPY, does find_links on document B discover links whose endsets reference I-addresses .0.1.1-.0.1.5 that were originally created against document A?

### Gregory's Answer

## KB Synthesis

# Answer: YES

Links are discoverable from document B through transclusion. Here's the mechanism:

## Content Identity Sharing

When document B transcludes content from document A via COPY, B shares the same I-addresses as A for that content [ST-VCOPY, Finding 0002]:

> "The vcopy (virtual copy / transclusion) operation adds references to existing content identities into the target document. It does not copy the content itself — it creates new references to the same identities that the source document references."

So both A and B reference I-addresses .0.1.1-.0.1.5 for "Hello".

## Link Discovery Mechanism

Links are discovered through I-address intersection, not document membership [ST-FIND-LINKS, Finding 0028]:

> "`find_links(search_specset)` discovers links by I-address intersection, not by document or V-address matching. The search specset is converted to I-addresses, and links are returned if any I-address in the search overlaps with I-addresses in a link endpoint."

## Transclusion Enables Discovery

The explicit interaction property [INT-LINK-TRANSCLUSION, Finding 0004]:

> "When content with a link is transcluded (vcopy'd) to another document, the link can be found from the copy. Calling `find_links` with a search specifying the target document returns the original link. This is because the vcopy shares the content identities, and the link is indexed by content identity."

And the formal property [INT-LINK-TRANSCLUSION, Finding 0008]:

> "Links are discoverable from ANY document that shares content identity with a link's endpoint — whether through transclusion, versioning, or chains of both."

## Storage Architecture

This works because links are indexed in the spanfilade by I-address [SS-SPANF-OPERATIONS, Finding 0012]:

> "The `spanf` enfilade supports... `findlinksfromtothreesp()` — queries for links whose endpoints intersect with given I-address ranges."

The spanfilade maps I-addresses to link ISAs globally. When B shares I-addresses with A through transclusion, those I-addresses retrieve the same link entries from the spanf index.

## Concrete Example

```
Document A: "Hello" at I-addresses .0.1.1-.0.1.5
Link created: source on "Hello" in A
Document B: COPY "Hello" from A → B references .0.1.1-.0.1.5

find_links(B, "Hello") → [link_id]
```

The link was created against A, but B discovers it because B shares the I-addresses that the link endpoints reference [INT-LINK-TRANSCLUSION, Finding 0028].

## Code Exploration

I need your permission to add this test scenario. Once approved, I'll run it to verify the behavior.

---

## Question 13 [gregory]

> After COPY creates a transclusion in document B, does INSERT into document A (shifting A's V-positions) alter any POOM entries in document B, or does B's POOM remain completely unchanged?

### Gregory's Answer

## KB Synthesis

# Answer: B's POOM Remains Completely Unchanged

After COPY creates a transclusion in document B, INSERT into document A does **not** alter any POOM entries in document B. Document B's POOM remains completely unchanged.

## The Mechanism

**1. What COPY does** [ST-VCOPY]

When B transcludes content from A, COPY adds entries to B's POOM that reference the **same I-addresses** that A uses:
- A's POOM: `V_A → I_x` (maps A's V-positions to I-addresses)  
- After COPY: B's POOM: `V_B → I_x` (B now also references those I-addresses)

**2. What INSERT does** [ST-INSERT, INV-IADDR-IMMUTABILITY]

When text is inserted into A:
- A's **V-addresses shift** (content after the insertion point moves to higher V-positions)
- A's **I-addresses remain unchanged** — "Each character's V-address shifts by +n. Its I-address is unchanged"
- Fresh I-addresses are allocated only for the newly inserted content

**3. The isolation boundary** [FC-INSERT-IADDR]

INSERT has an explicit frame condition on cross-document effects:

> "INSERT does not modify the I-address of any pre-existing content, in the target document or in any other document... All existing V-to-I mappings outside the target document are completely untouched."

Formally: `forall doc d != target, forall v in d :: d.mapping(v) is unchanged`

## Why Transclusion Still Works

The transclusion relationship survives because it operates in **I-space**, not **V-space** [INT-TRANSCLUSION]:

- Before INSERT: A maps `V_A(1.3) → I.3`, B maps `V_B(2.1) → I.3` (shared I-address)
- After INSERT at A's position 1.1: A maps `V_A(1.5) → I.3` (V-shifted), B maps `V_B(2.1) → I.3` (unchanged)  
- Both documents still reference `I.3` — the transclusion remains valid

As stated: "Transclusion is an I-space relationship, invariant under V-space mutations."

## Structural Independence

Each document maintains its **own POOM** enfilade [SS-DUAL-ENFILADE]. These are separate B-tree structures with no shared nodes. Operations on A's POOM physically cannot modify B's POOM because they are distinct data structures stored in separate regions of the granfilade.

The same isolation holds for DELETE [FC-DELETE-CROSS-DOC]: "DELETE in one document has zero effect on any other document's POOM mappings."

## Conclusion

**Answer:** B's POOM remains completely unchanged. The only state modification is to A's POOM (V-positions shift, I-addresses preserved). Document B continues to reference the same I-addresses as before, and since those I-addresses haven't changed, the transclusion continues to work correctly.

## Code Exploration

Based on my analysis of the source code, I can definitively answer your question:

## Answer: B's POOM remains completely unchanged

After COPY creates a transclusion in document B, INSERT into document A does **not** alter any POOM entries in document B. B's POOM is completely isolated from A's POOM modifications.

## Why: POOMs are Document-Specific Data Structures

### 1. Each document has its own POOM enfilade

From **granf1.c:16-41**, `findorgl` retrieves a document-specific POOM:

```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, 
              typeorgl *orglptr, int type)
{
    typeorgl fetchorglgr();
    ...
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);  // Line 39
    return (*orglptr ? TRUE : FALSE);
}
```

The POOM is looked up by document ISA. Document A has POOM_A, document B has POOM_B — completely separate enfilade structures [enf.h:34].

### 2. COPY stores I-addresses in B's POOM, not V-addresses from A

When COPY executes **do1.c:45-65**:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, 
            typespecset specset)
{
    ...
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)  // Line 54
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)       // Line 55
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)        // Line 60
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)     // Line 62
```

The key transformation happens in **do2.c:14-46** (`specset2ispanset`):

```c
bool specset2ispanset(typetask *taskptr, typespec *specset, 
                      typeispanset *ispansetptr, int type)
{
    ...
    if (((typeitemheader *)specset)->itemid == VSPECID) {
        if (!(
          findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl,type)  // Line 35
        && (ispansetptr = vspanset2ispanset (taskptr, docorgl, 
                          ((typevspec *)specset)->vspanset, ispansetptr))))  // Line 36
```

**Line 35** finds document A's POOM, then **line 36** converts A's V-spans to I-spans using A's POOM.

The resulting I-spans are then stored in B's POOM via `insertpm` **orglinks.c:75-134**:

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl, 
              tumbler *vsaptr, typesporglset sporglset)
{
    ...
    for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
        unpacksporgl (sporglset, &lstream, &lwidth, &linfo);        // Line 101
        movetumbler (&lstream, &crumorigin.dsas[I]);                // Line 105
        movetumbler (&lwidth, &crumwidth.dsas[I]);                  // Line 109
        movetumbler (vsaptr, &crumorigin.dsas[V]);                  // Line 113
        ...
        insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, 
                  &linfo, V);                                        // Line 130
```

**Lines 105, 109**: I-coordinates come from the ispanset (A's original addresses)  
**Line 113**: V-coordinates are B's V-positions  
**Line 130**: Inserts into B's POOM the mapping **(B's V-position → I-address)**

### 3. INSERT in A modifies A's POOM only

When INSERT executes in document A **do1.c:87-123**:

```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, 
              typetextset textset)
{
    ...
    return (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)  // Line 118
         && docopy (taskptr, docisaptr, vsaptr, ispanset)                  // Line 119
```

**Line 119** calls `docopy` on document A, which calls `insertpm` on **A's POOM** (via `findorgl` with A's ISA).

When `insertpm` is called on A's POOM, it invokes `makegappm` **insertnd.c:124-150**:

```c
int makegappm(typetask *taskptr, typecuc *fullcrumptr, 
              typewid *origin, typewid *width)
{
    ...
    movetumbler (&origin->dsas[V], &knives.blades[0]);              // Line 144
    findaddressofsecondcutforinsert(&origin->dsas[V],
                                    &knives.blades[1]);              // Line 145
    knives.dimension = V;                                            // Line 147
    makecutsnd (fullcrumptr, &knives);                               // Line 148
```

This creates a "gap" in A's POOM by cutting at the V-dimension insertion point. This shifts V-coordinates of A's existing POOM entries that come after the insertion point.

**But this operates on `fullcrumptr`** — which is A's POOM enfilade. B's POOM enfilade is a completely separate tree structure.

### 4. B's POOM references I-addresses, which don't change

The crucial architectural fact: B's POOM contains entries of the form:

```
(V-position-in-B, I-address-in-granfilade)
```

The I-addresses are **permanent identifiers** in the granfilade [enf.h:12-14]. When INSERT happens in A:

1. New content gets a new I-address in the granfilade
2. A's POOM gets new entries mapping A's V-positions to I-addresses
3. A's POOM entries shift their V-coordinates (within A's coordinate space)
4. **The I-addresses themselves never change** — they're permanent
5. B's POOM entries contain the same I-addresses as before
6. B's POOM tree structure is never touched

## Existing Test Evidence

The test suite includes **febe/scenarios/document_isolation.py** which verifies the frame axiom (F0): operations on document A don't affect document B. Specifically, `scenario_cross_document_transclusion_isolation` (lines 351-442) confirms that operations on B don't affect A or C when transclusion exists.

While no existing test explicitly checks INSERT-in-source-after-COPY, the architectural isolation is absolute: each document's POOM is a separate enfilade tree, and I-addresses are invariant references to the shared granfilade.

## Conclusion

**B's POOM remains completely unchanged** when INSERT modifies A's V-positions. The POOM entries in B continue to reference the same I-addresses, which are permanent identifiers in the granfilade. The fact that A's POOM shifts its V-coordinates is irrelevant to B, since B's POOM contains no references to A's V-space.

This is the fundamental architectural guarantee of Udanax-green's transclusion model: **I-addresses provide stable references across documents**, while **V-addresses are document-local coordinate systems** maintained by per-document POOMs.

---

## Question 14 [gregory]

> When document B holds a transclusion of document A's content and that content is DELETEd from A's POOM, do B's POOM entries and the underlying granfilade content remain intact and retrievable?

### Gregory's Answer

## KB Synthesis

Yes, **document B's POOM entries and the underlying granfilade content remain completely intact and retrievable** after document A deletes that content.

## Why This Works

**DELETE is POOM-only** — [ST-DELETE] and [FC-DELETE-CROSS-DOC] establish that DELETE operates exclusively on the target document's POOM tree. When A deletes content, `deletend` removes V→I mappings from A's POOM by calling `disown` + `subtreefree` on A's bottom crums. No other document is touched.

**Frame condition** — [FC-DELETE-CROSS-DOC] states: `∀ D' ≠ D : delete(D, vspan) ⟹ poom(D') = poom_before(D')`. Document B's POOM structure is completely unchanged by operations on A.

**Granfilade is permanent** — [INV-IADDR-IMMUTABILITY] and [FC-GRANF-ON-DELETE] establish that I-addresses persist permanently in the granfilade. DELETE removes POOM entries (V→I references) but never touches granfilade content. The content bytes at those I-addresses remain in the granfilade unconditionally.

**Transclusion shares I-addresses** — [ST-VCOPY] and [INT-TRANSCLUSION] establish that when B transcluded A's content via vcopy, B's POOM received V→I mappings pointing to the same I-addresses. B doesn't hold copies — it holds references to shared identity.

## Concrete Example

```
Initial state:
  A's POOM: V(1.1)→I(5.1), V(1.2)→I(5.2), V(1.3)→I(5.3)  ["ABC"]
  B's POOM: V(2.1)→I(5.1), V(2.2)→I(5.2), V(2.3)→I(5.3)  [transclusion]
  Granfilade: I(5.1)="A", I(5.2)="B", I(5.3)="C"

After DELETE from A:
  A's POOM: empty (mappings removed)
  B's POOM: V(2.1)→I(5.1), V(2.2)→I(5.2), V(2.3)→I(5.3)  [UNCHANGED]
  Granfilade: I(5.1)="A", I(5.2)="B", I(5.3)="C"          [UNCHANGED]

Result: B still retrieves "ABC" — its POOM mappings are intact and resolve through the permanent granfilade content.
```

This is the fundamental architectural separation documented in [SS-DUAL-ENFILADE] and [SS-POOM-MUTABILITY]: the granfilade (content store) is append-only and shared, while POOMs (document views) are mutable and isolated.

## Code Exploration

I need permission to create the test file. Once approved, I'll run the test to verify the behavior.

---

## Question 15 [gregory]

> Does COPY create DOCISPAN entries in the spanfilade for the target document, making the target independently discoverable via FINDDOCSCONTAINING even if the source document is later emptied?

### Gregory's Answer

## KB Synthesis

# Answer

**Yes, COPY creates DOCISPAN entries in the spanfilade for the target document, making it independently discoverable via FINDDOCSCONTAINING regardless of what happens to the source document.**

## Evidence Chain

**1. COPY creates DOCISPAN entries**

From [ST-COPY] Finding 0047: "COPY creates DOCISPAN entries proportional to the number of contiguous I-spans in the source content, not the number of bytes."

The operation flow is documented in [ST-INSERT] Finding 0036 for the shared code path: `docopy` → `insertpm` + `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)`. Both INSERT and COPY use this same `docopy` function to place content, and both create DOCISPAN entries.

**2. DOCISPAN entries are permanent**

From [INV-SPANF-WRITE-ONLY] Finding 0057: "The spanfilade is a write-only (append-only) index. Entries are added by `insertspanf` during COPY and INSERT operations, but no deletion function exists anywhere in the spanf codebase."

Once created, DOCISPAN entries persist indefinitely. There is no mechanism to remove them.

**3. Source deletion has zero effect on target document**

From [FC-DELETE-CROSS-DOC] Finding 0064: "DELETE in one document has zero effect on any other document's POOM mappings. If document T transcluded content from document D (sharing I-addresses via COPY), and D subsequently deletes that content, T's POOM still maps to the shared I-addresses."

DELETE is strictly local to the document being modified. The target document's POOM and spanfilade entries remain completely unchanged.

**4. Target remains discoverable**

From [INV-IADDRESS-PERMANENT] Finding 0023: "Once an I-address is associated with a document (via insert or vcopy), `find_documents` continues to report that document even after the content is deleted from the document's V-stream."

This quote specifically covers the case where content is deleted from the TARGET document itself — the DOCISPAN entry persists. By extension, source deletion (which doesn't touch the target at all) certainly cannot remove the target's DOCISPAN entries.

## Example

```
Initial state:
  Source doc S: contains "shared content" at I-addresses α₁..α₁₀
  Target doc T: empty

After COPY from S to T:
  Source doc S: still contains "shared content" at α₁..α₁₀
  Target doc T: now contains "shared content" at α₁..α₁₀ (shared I-addresses)
  Spanfilade DOCISPAN: α₁..α₁₀ → {S, T}
  FINDDOCSCONTAINING("shared") → {S, T} ✓

After DELETE all content from S:
  Source doc S: empty (POOM has no V→I mappings)
  Target doc T: UNCHANGED — still contains "shared content" at α₁..α₁₀
  Spanfilade DOCISPAN: α₁..α₁₀ → {S, T} (UNCHANGED - no delete mechanism)
  FINDDOCSCONTAINING("shared") → {S, T} ✓
    (S is now a "stale reference" per [EC-STALE-SPANF-REFERENCE], 
     but T is a live reference)
```

The target document T remains independently discoverable via its own DOCISPAN entries, which were created during the COPY operation and cannot be removed by any operation on the source document.

## Code Exploration

Based on my analysis of the C source code, I can now provide a definitive answer to your question.

---

## Answer: Yes, COPY Creates Independent DOCISPAN Entries

**COPY does create DOCISPAN entries in the spanfilade for the target document, making it independently discoverable via FINDDOCSCONTAINING even if the source document is later emptied.**

### Code Analysis

#### 1. COPY Operation Creates DOCISPAN Entries

The `docopy` function [backend/do1.c:45-65] performs two critical operations:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    // ... setup code ...
    
    return (
       // ... validation ...
       
       /* the meat of docopy: */
       && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
       
       &&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
       // ... 
    );
}
```

**Line 62** is the key: `insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)`

This call:
- Passes the **target** document's ISA (`docisaptr`)  
- Passes the content being copied (`ispanset`)
- Specifies span type as `DOCISPAN`

#### 2. insertspanf Writes to the Spanfilade

The `insertspanf` function [backend/spanf1.c:15-54] constructs spanfilade keys:

```c
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr, 
                 typesporglset sporglset, INT spantype)
{
    // Line 22: Construct the ORGLRANGE key
    prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
    // ...
    
    for (; sporglset; sporglset = ...) {
        // Line 49-50: Set up SPANRANGE dimension
        movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
        movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
        
        // Line 51: Insert into spanfilade
        insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
    }
}
```

**Line 22** creates a tumbler prefix of `<target-docisa>.DOCISPAN` in the ORGLRANGE dimension.

**Line 51** inserts entries into the spanfilade mapping:
- **Key**: `<target-docisa>.DOCISPAN` (ORGLRANGE) × `<ispan>` (SPANRANGE)
- **Value**: The content's home document and positioning info

#### 3. FINDDOCSCONTAINING Queries These Entries

The `finddocscontainingsp` function [backend/spanf1.c:151-188] searches the spanfilade:

```c
bool finddocscontainingsp(typetask *taskptr, typespanset ispanset, typelinkset *addresssetptr)
{
    // Lines 167-169: Define the DOCISPAN subspace
    clear (&docspace, sizeof(typespan));
    tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);
    tumblerincrement (&docspace.width, 0, 1, &docspace.width);
    
    for (; ispanset; ispanset = ispanset->next) {
        // Line 171: Query spanfilade for all docs in DOCISPAN subspace
        context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE, 
                                      ispanset, SPANRANGE, (typeisa*)NULL);
        
        for (c = context; c; c = c->nextcontext) {
            // Lines 173-174: Extract document ISA
            movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
            beheadtumbler (&docid, &document.address);
            // ... add to results ...
        }
    }
}
```

**Lines 167-169** create a search range covering all DOCISPAN entries (from `DOCISPAN.0` to `(DOCISPAN+1).0`).

**Line 171** performs a restricted retrieve operation that finds all spanfilade entries where:
- ORGLRANGE falls within the DOCISPAN subspace  
- SPANRANGE matches the query content

**Lines 173-174** extract the document ISA by removing the DOCISPAN prefix from the ORGLRANGE key.

#### 4. DELETE Does NOT Remove DOCISPAN Entries

The `deletevspanpm` function [backend/orglinks.c:145-152] only deletes from the POOM:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, 
                   typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    
    // Line 149: Delete from the document's POOM tree (granfilade)
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

**Line 149** deletes from the document's orgl (POOM tree) in the V dimension.

**There is NO corresponding deletion from the spanfilade.** The DOCISPAN entries persist.

I verified this with: `grep -r "deletend.*spanf\|delete.*DOCISPAN" backend/` → No matches found.

### Conclusion

1. **COPY calls insertspanf** [do1.c:62] with the target document's ISA and span type DOCISPAN
2. **insertspanf creates persistent entries** [spanf1.c:22,51] in the spanfilade keyed by `<target-docisa>.DOCISPAN`
3. **FINDDOCSCONTAINING queries the DOCISPAN subspace** [spanf1.c:167-171] and extracts document ISAs from matching entries
4. **DELETE only removes from the POOM** [orglinks.c:149], not from the spanfilade

Therefore, **copied content creates independent content identity for the target document that persists even after the source is emptied.**

### Empirical Verification

I've prepared a golden test scenario `find_documents_after_source_emptied` to verify this behavior empirically. Once you approve the file write, I'll run it and add the results to the findings.

---

## Question 16 [gregory]

> When COPY transfers a V-span that maps to non-contiguous I-addresses (e.g., after an INSERT split the original span), does vspanset2sporglset automatically split the specset into multiple sporgls, each preserving the correct I-address mapping in the target?

### Gregory's Answer

## KB Synthesis

Yes, `vspanset2sporglset` automatically splits a V-span into multiple sporgls when it maps to non-contiguous I-addresses, preserving the exact I-address structure in the target.

## Mechanism

The conversion chain is documented in [ST-LINK-CREATE] (Finding 0037):

```
V-span → vspanset2ispanset → permute → span2spanset → retrieverestricted
```

This walks the POOM (V-to-I mapping) and discovers all I-address regions. The key property: **it produces one I-span per contiguous I-address region**, then creates one sporgl per I-span.

[INT-SPORGL-TRANSCLUSION] confirms this applies to COPY:
> "During vcopy (transclusion), the data flow is: source V-spec → sporgls (via `vspanset2sporglset`) → `insertpm` into destination document."

## When Non-Contiguity Arises

From [ST-INSERT] (Finding 0030), INSERT shifts V-positions but preserves I-addresses:

```
Original: "ABCDE" at V 1.1-1.5, I.1-I.5 (contiguous)
After INSERT "XY" at V 1.3:
  "ABXYCDE" at V 1.1-1.7
  - V 1.1-1.2 → I.1-I.2   (original AB)
  - V 1.3-1.4 → I.6-I.7   (fresh allocation for XY)
  - V 1.5-1.7 → I.3-I.5   (original CDE, shifted V-positions)
```

The I-addresses are now: I.1, I.2, I.6, I.7, I.3, I.4, I.5 — **three non-contiguous regions**.

## Concrete Example

From [ST-LINK-CREATE] (Finding 0037):

```
Document C contains "AABB" at V 1.1..1.4 where:
  "AA" from document A (I-addresses from A's region)
  "BB" from document B (I-addresses from B's region)

Input:  1 V-span covering all of "AABB"
Output: 2 sporgls in endset:
  sporgl₁: origin = I-addr(A,"AA"), width = 0.2, doc = C
  sporgl₂: origin = I-addr(B,"BB"), width = 0.2, doc = C
```

When you COPY the full V-span 1.1-1.7 from the fragmented "ABXYCDE" document:
1. `vspanset2ispanset` discovers three I-spans: [I.1-I.2], [I.6-I.7], [I.3-I.5]
2. Creates three sporgls preserving this structure
3. `insertpm` maps these to the target document's V-space, maintaining the I-address relationships

## Supporting Evidence

[SS-DOCISPAN] (Finding 0047) confirms: "COPY of fragmented source content (e.g., 3 non-contiguous regions) creates 3 DOCISPAN entries" — one per I-span.

[ST-VCOPY] (Finding 0002) guarantees identity preservation: the target references **exactly** the content identities from the source specset, including their non-contiguous structure.

**Answer: Yes, automatic splitting preserves exact I-address mapping.**

## Code Exploration

---

## Answer: YES — COPY Automatically Splits Non-Contiguous I-Address Mappings

When COPY transfers a V-span that maps to non-contiguous I-addresses (e.g., after an INSERT operation splits the original content), **the system automatically splits the copy into multiple independent insertions**, each preserving the correct I-address mapping in the target.

### How It Works

#### 1. V→I Conversion Creates Multiple Spans

The critical function is `retrieverestricted()` [`backend/retrie.c:56`], which returns a **linked list of contexts** — one context per contiguous I-address region.

**Execution path:**
- `docopy()` [`backend/do1.c:54`] calls `specset2ispanset()`
- → `vspanset2ispanset()` [`backend/orglinks.c:397`] calls `permute()` for V→I conversion
- → `permute()` [`backend/orglinks.c:414`] loops through V-spans, calling `span2spanset()` for each
- → `span2spanset()` [`backend/orglinks.c:435`] calls `retrieverestricted()`:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                            (typespan*)NULL, targindex, (typeisa*)NULL);
```

- → `span2spanset()` [`backend/orglinks.c:439-444`] loops through **each context**:

```c
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan,
                                     (typeitemset*)targspansetptr);
}
```

**Key insight**: `retrieverestricted()` returns multiple contexts via `c->nextcontext`. Each context represents a **single contiguous I-address region**. The loop creates a **separate I-span for each context**.

#### 2. Each I-Span Is Inserted Separately

From `insertpm()` [`backend/orglinks.c:100-132`]:

```c
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (&lstream, &crumorigin.dsas[I]);
    movetumbler (&lwidth, &crumwidth.dsas[I]);
    movetumbler (vsaptr, &crumorigin.dsas[V]);
    // ... set up width ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);  // increment vsa
}
```

- **Line 100**: Loops through each sporgl
- **Line 130**: Calls `insertnd()` for each sporgl individually
- **Line 131**: Increments `vsaptr` (V-address) after each insertion

### Example

**Initial state:**
- Document has "ABC" at contiguous I-addresses 1000.1, 1000.2, 1000.3

**After INSERT "XYZ" at V=1.2:**
- V-span 1.1-1.2 → I-span 1000.1-1000.2 ("AB")
- V-span 1.5-1.6 → I-span 2000.1-2000.3 ("XYZ")
- V-span 1.6-1.7 → I-span 1000.3 ("C")

**COPY V-span 1.1-1.7 to target at V=2.1:**
- `retrieverestricted()` returns **3 contexts** (3 contiguous I-regions)
- `span2spanset()` creates **3 I-spans**
- `insertpm()` inserts each separately:
  - Sporgl 1 (I=1000.1-1000.2, "AB") → V=2.1-2.2
  - Sporgl 2 (I=2000.1-2000.3, "XYZ") → V=2.3-2.5
  - Sporgl 3 (I=1000.3, "C") → V=2.6

**Result**: The target POOM has **3 separate crums** (one per sporgl), each preserving its original I-address mapping, with **consecutive V-addresses** (no gaps).

### Source Code Citations

**V→I conversion:**
- `backend/do1.c:54` — `docopy()` calls `specset2ispanset()`
- `backend/orglinks.c:397-402` — `vspanset2ispanset()` calls `permute()`
- `backend/orglinks.c:404-422` — `permute()` loops through V-spans
- `backend/orglinks.c:425-454` — `span2spanset()` processes each context from `retrieverestricted()`
- `backend/retrie.c:56-85` — `retrieverestricted()` returns context list

**Insertion:**
- `backend/do1.c:60` — `docopy()` calls `insertpm()`
- `backend/orglinks.c:100-132` — `insertpm()` loops through sporgls, calling `insertnd()` for each

**Sporgl conversion:**
- `backend/sporgl.c:35-65` — `vspanset2sporglset()` shows nested loop at line 49: loops through each I-span returned by `vspanset2ispanset()`, creating a separate sporgl for each

### Implications

1. **Transclusion preserves granfilade identity** — Each character maintains its exact I-address from source
2. **POOM structure reflects fragmentation** — Non-contiguous I-addresses result in multiple crums
3. **V-space remains contiguous** — Despite non-contiguous I-addresses, V-addresses have no gaps
4. **Automatic splitting** — No special handling needed; the system naturally handles this through `retrieverestricted()`

---

## Question 17 [gregory]

> Does SHOWRELATIONOF2VERSIONS detect content overlap between a document and its transclusion target — that is, does compare_versions identify shared I-address spans between two documents that share content solely through COPY rather than through CREATENEWVERSION?

### Gregory's Answer

## KB Synthesis

# Yes, SHOWRELATIONOF2VERSIONS detects transclusion-based content sharing

Despite its name suggesting version-specific functionality, `compare_versions` (FEBE opcode 10: SHOWRELATIONOF2VERSIONS) operates on **any two documents** that share I-addresses, regardless of how that sharing occurred.

## Core Mechanism

From [SS-COMPARE-VERSIONS]:
> "The `compare_versions` operation answers the question: 'What text content do these two documents share by common origin?' The operation produces a list of ordered pairs of V-spans — one from each document — where the paired spans reference the same permascroll I-address range."

The operation works by I-address intersection, not by checking version relationships. From [ST-COMPARE-VERSIONS]:
> "Each pair `(span_a, span_b)` in the result satisfies: `VSpanToISpan(doc_a, span_a) == VSpanToISpan(doc_b, span_b)` where both I-spans are permascroll addresses."

## Direct Evidence for COPY/Transclusion

[ST-VCOPY] Finding 0002 explicitly confirms this:
> "After vcopy, `compare_versions` between source and target reports shared content, confirming that both documents reference the same content identities."

Concrete example from the same entry:
```
Source: "Shared content that will be transcluded"
Target: vcopy from Source
Result: compare_versions(source, target) returns the shared span
```

## Transitive Detection

From [INV-TRANSITIVE-IDENTITY] Finding 0002:
> "Content identity is preserved transitively through chains of transclusion. If document B transcludes from C, and document A transcludes from B, then A and C share content identity even though A never directly referenced C. The `compare_versions` operation between A and C correctly reports the shared content."

## Implementation Details

[INT-SPORGL-VERSION-COMPARE] describes the mechanism:
> "Version comparison (`compare_versions` / `correspond.c`) uses sporgls to find shared content between documents. Both documents' content is converted to sporgls, then intersection is computed by I-address (the `sporglorigin` field)."

There is no version-specific logic in this implementation. The operation simply:
1. Converts both documents' V-spans to I-spans
2. Finds I-address intersections
3. Maps shared I-addresses back to V-spans in each document

## Limitations

The only constraint is from [PRE-COMPARE-VERSIONS]:
> "For `compare_versions` to operate correctly, the input V-span sets must be restricted to the text subspace (`V >= 1.0`)."

This is a subspace filtering requirement, not a restriction on document relationships.

**Conclusion:** The operation name "SHOWRELATIONOF2VERSIONS" is misleading. `compare_versions` detects I-address overlap between any two documents, whether the sharing occurred through VERSION, COPY, or transitive transclusion chains.

## Code Exploration

Based on my analysis of the source code, I can now provide a definitive answer:

## YES — SHOWRELATIONOF2VERSIONS detects I-address overlap from COPY operations

### Evidence from Source Code

**1. SHOWRELATIONOF2VERSIONS compares I-addresses** [backend/do1.c:428-449]

```c
bool doshowrelationof2versions(..., typespecset version1, typespecset version2, typespanpairset *relation)
{
  typeispanset version1ispans = NULL;
  typeispanset version2ispans = NULL;
  typeispanset commonispans = NULL;
  
  return
    specset2ispanset(taskptr, version1, &version1ispans, READBERT)
  &&  specset2ispanset(taskptr, version2, &version2ispans, READBERT)
  &&  intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
  &&  ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation);
}
```

The function converts both documents' V-addresses to I-addresses (lines 444-445), then uses `intersectspansets` (line 446) to find **shared I-address spans**.

**2. COPY reuses existing I-addresses** [backend/do1.c:45-65]

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
  typeispanset ispanset;
  
  return (
    specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)  // Line 54
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)      // Line 60
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
  );
}
```

Line 54 retrieves the **existing I-addresses** from the source document. Line 60 passes those same I-addresses to `insertpm`.

**3. insertpm preserves I-addresses** [backend/orglinks.c:75-133]

```c
bool insertpm(..., tumbler *vsaptr, typesporglset sporglset)
{
  for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (&lstream, &crumorigin.dsas[I]);      // Line 105: Copy source I-address
    movetumbler (vsaptr, &crumorigin.dsas[V]);        // Line 113: Set new V-address
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
  }
}
```

Line 105 copies the I-address from the source (`lstream`) directly into the POOM node being inserted. The content gets a **new V-address** but keeps the **same I-address**.

### Contrast: INSERT creates new I-addresses

When you INSERT new text (not COPY), the system allocates fresh I-addresses [backend/granf2.c:92, 130-142]:

```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))  // Allocates NEW I-address
```

### Semantic Caveat

The implementation includes a filter for text subspace [backend/do1.c:437-441]:

```c
/* SEMANTIC FIX: Filter to text subspace before comparison.
 * Link references (V < 1.0) are not content with "common origin".
 * See Finding 015 for the semantic definition. */
filter_specset_to_text_subspace(taskptr, version1);
filter_specset_to_text_subspace(taskptr, version2);
```

This means SHOWRELATIONOF2VERSIONS only detects overlap in **text content (V ≥ 1.0)**, not link references (V < 1.0).

## Conclusion

**Yes**, `compare_versions` (via `doshowrelationof2versions`) identifies shared I-address spans between documents that share content through COPY. This works because:

1. COPY reuses I-addresses from the source [do1.c:54, orglinks.c:105]
2. SHOWRELATIONOF2VERSIONS detects I-address intersection [do1.c:446]
3. The relationship exists independently of CREATENEWVERSION genealogy

The detection is based on **permascroll identity** (shared I-addresses), not V-address version trees.

---

## Question 18 [gregory]

> If document B transcludes content from A, and document C then transcludes the same V-span from B, does C's POOM contain the same I-addresses as A's original content — making links created against A discoverable from C through the transitive chain?

### Gregory's Answer

## KB Synthesis

# Answer: YES, transitive transclusion preserves I-address identity

Document C will contain the **same I-addresses** as A's original content, making links created against A discoverable from C through the transitive chain B→C.

## The Mechanism

[ST-VCOPY] defines transclusion as adding "references to existing content identities" — it does not create new I-addresses. When B transcludes from A, B's POOM maps V-positions to A's I-addresses. When C transcludes from B, C's POOM maps V-positions to B's I-addresses — which are still A's I-addresses. The sporgl data structure carries the I-address through this chain [INT-SPORGL-TRANSCLUSION].

## Transitive Identity Invariant

[INV-TRANSITIVE-IDENTITY] from Finding 0002 explicitly covers this scenario:

> "Content identity is preserved transitively through chains of transclusion. If document B transcludes from C, and document A transcludes from B, then A and C share content identity even though A never directly referenced C."

The finding provides a concrete example:
```
C: "ABCDEFGHIJ"
B: vcopy(all of C)
A: vcopy("DEFGH" from B)

compare_versions(A, C) → "DEFGH" shared
```

This demonstrates that A and C share I-addresses despite A copying from B, not directly from C.

## Link Discovery Consequence

[INT-LINK-TRANSCLUSION] from Finding 0008 confirms the link discovery implication:

> "Links are discoverable from ANY document that shares content identity with a link's endpoint — whether through transclusion, versioning, or chains of both."

The mechanism is:
1. A creates content → allocates I-addresses α₁..αₙ  
2. B transcludes from A → B's POOM references α₁..αₙ  
3. C transcludes from B → C's POOM references α₁..αₙ  
4. Link created on A's content → indexed in spanf by α₁..αₙ  
5. `find_links(C)` converts C's V-positions to I-addresses → gets α₁..αₙ → intersects with spanf → discovers the link

## No Special Case Needed

[INV-TRANSITIVE-IDENTITY] notes that "the spec need not add a special transitivity rule; it falls out of the state-transition definition of vcopy." Since transclusion preserves I-addresses (postcondition of [ST-VCOPY]) and composition of I-address-preserving operations preserves I-addresses (by transitivity), the property holds automatically. No N-hop limit exists — tested with chains of 2 and 3 transclusions [EC-SELF-TRANSCLUSION] from Finding 0039.

**In formal terms**: `vcopy(A→B) ∧ vcopy(B→C) ⟹ iaddrs(C) ⊇ iaddrs(A)` for the transcluded span. Links indexed by `iaddrs(A)` are discoverable from any document containing those I-addresses, including C.

## Code Exploration

Based on my analysis of the udanax-green source code, I can now provide a definitive answer to your question.

## Answer: YES — Transitive Transclusion Preserves I-Address Identity

When document C transcludes content from B that B previously transcluded from A, **C's POOM contains the exact same I-addresses as A's original content**. This makes links created against A fully discoverable from C through the transitive chain.

---

## Code Analysis

### 1. The Copy Operation (do1.c:45-65)

The `docopy` function performs transclusion:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
  typeispanset ispanset;
  typeorgl docorgl;
  
  return (
     specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)  // [line 54]
  && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)      // [line 55]
  && acceptablevsa (vsaptr, docorgl)
  && asserttreeisok(docorgl)
  
  /* the meat of docopy: */
  && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)       // [line 60]
  
  &&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)   // [line 62]
  && asserttreeisok(docorgl)
  );
}
```

**Key insight:** Line 54 converts V-specs to I-spans by reading the source document's POOM. Line 60 inserts those I-spans into the target document's POOM.

### 2. V→I Conversion (do2.c:14-46)

The `specset2ispanset` function reads the source document's POOM:

```c
bool specset2ispanset(typetask *taskptr, typespec *specset, typeispanset *ispansetptr, int type)
{
  typeorgl docorgl;
  
  for (; specset; specset = (typespec *)((typeitemheader *)specset)->next) {
    if (((typeitemheader *)specset)->itemid == VSPECID) {
      if (!(
        findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl,type)  // [line 35]
      && (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr))))  // [line 36]
        return (FALSE);
    }
  }
  return (TRUE);
}
```

**Key insight:** Line 36 calls `vspanset2ispanset`, which reads the POOM to find what I-addresses are at the requested V-position.

### 3. POOM Lookup (orglinks.c:397-402)

The `vspanset2ispanset` function retrieves I-spans from the POOM:

```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, typevspanset vspanptr, typeispanset *ispansetptr)
{
  typespanset *permute();
  return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);  // [line 393]
}
```

The `permute` function (orglinks.c:404-422) calls `retrieverestricted` (retrie.c:55-84) to look up crums at the V-position and extract their I-addresses.

### 4. I-Address Insertion (orglinks.c:75-134)

The `insertpm` function inserts I-addresses into the target POOM:

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl, tumbler *vsaptr, typesporglset sporglset)
{
  tumbler lstream, lwidth;
  type2dbottomcruminfo linfo;
  typewid crumorigin, crumwidth;
  
  for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    
    movetumbler (&lstream, &crumorigin.dsas[I]);   // [line 105] - Copy I-stream directly
    movetumbler (&lwidth, &crumwidth.dsas[I]);     // [line 109] - Copy I-width directly
    movetumbler (vsaptr, &crumorigin.dsas[V]);     // [line 113] - Set V-position
    
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // [line 130]
  }
  return (TRUE);
}
```

**Critical observation:** Lines 105-109 copy I-addresses **directly without transformation**. The I-stream and I-width are preserved exactly as they appear in the source document.

---

## Execution Trace

**Scenario: A → B → C transitive transclusion**

### Step 1: A creates original content
- A inserts text at V-address `1.1`
- Backend allocates I-address `X` (e.g., `5.2.3.1`)
- A's POOM: `V[1.1] → I[X]`

### Step 2: B transcludes from A
- B calls `docopy` with source vspec `{docisa=A, vspan=1.1-1.2}`
- `specset2ispanset` reads A's POOM at V-position `1.1`
- Finds I-address `X`
- `insertpm` inserts I-address `X` at B's V-position `2.1`
- **B's POOM: `V[2.1] → I[X]`** ✓ Same I-address

### Step 3: C transcludes from B
- C calls `docopy` with source vspec `{docisa=B, vspan=2.1-2.2}`
- `specset2ispanset` reads **B's POOM** at V-position `2.1`
- Finds I-address `X` (the same one from A!)
- `insertpm` inserts I-address `X` at C's V-position `3.1`
- **C's POOM: `V[3.1] → I[X]`** ✓ Same I-address

### Result
All three documents — A, B, and C — map to the **identical I-address `X`** in the content identity space. Any links created against A's content at I-address `X` are discoverable when searching from C's content, because C also references I-address `X`.

---

## Empirical Verification

The test harness includes `scenario_find_documents_transitive` (febe/scenarios/identity.py:66-126), which verifies this behavior:

```python
# C → B → A transclusion chain
# Find documents containing the original content from C
query_vspec = VSpec(c_read2, [Span(Address(1, 1), Offset(0, 8))])  # "Original"
found_docs = session.find_documents(query_specset)

# Expected result: Should find A, B, and C
# Comment: "content identity is transitive"
```

This test confirms that `FINDDOCSCONTAINING` discovers all three documents when querying for content originally from C, because they all share the same I-addresses.

---

## Conclusion

**Yes**, C's POOM contains the same I-addresses as A's original content. The POOM (Permutation Matrix) stores V↔I mappings, and transclusion copies I-addresses directly without transformation. This means:

1. **Link discovery works transitively** — Links created against A's content are findable when searching from C
2. **Content identity is preserved** — The `find_documents` operation discovers all documents in the transclusion chain
3. **Version comparison works** — `compare_versions` can detect common origin across transitive transclusions

The I-address is the **immutable identity** of content in Xanadu's permascroll. Transclusion creates new V-address mappings to existing I-addresses, preserving identity across any number of transclusion hops.

---

## Question 19 [gregory]

> When COPY places content at a V-position in the target where adjacent POOM entries happen to have contiguous I-addresses with the copied content, does isanextensionnd merge the copy into the existing crum rather than creating a separate entry, and does this merging affect any observable query behavior?

### Gregory's Answer

## KB Synthesis

# Answer: COPY Coalescing via `isanextensionnd`

**Yes, `isanextensionnd` can merge COPY content into existing crums, but only under specific conditions. This merging affects internal crum count but has no observable effect on query behavior.**

## The Mechanism

From [ST-VCOPY], Finding 0046, and [ST-INSERT], Finding 0062: when COPY uses `insertpm` to place V→I mappings into the target document's POOM, the insertion follows an extension-or-create rule. The function `isanextensionnd()` at `insertnd.c:293-301` checks two conditions:

1. **Same homedoc**: The new mapping references the same I-address origin document as the existing crum
2. **Contiguous I-addresses**: The new mapping starts exactly where the existing crum ends (reach == origin)

If both hold → existing crum's width is extended in place  
If either fails → new crum is created

## The Critical Constraint: homedoc

From [INV-IADDR-PROVENANCE], Finding 0046: **Every I-address has exactly one native document** where INSERT first allocated it. The `homedoc` field in each POOM crum records this I-address origin document — **not the document from which content was most recently copied.**

### Scenario 1: Merging DOES occur
```
Source A has content at I-addresses α₁..α₁₀

Target B: COPY α₁..α₅ from A → places at V-positions 1.1-1.5 (homedoc=A)
Target B: COPY α₆..α₁₀ from A → places at V-position 1.6

Check:
- Same homedoc? YES (both reference A)
- Contiguous I-addresses? YES (α₅ reach equals α₆ origin)
- Result: crums MERGE (existing crum extended from width 0.5 to 1.0)
```

### Scenario 2: Merging does NOT occur
```
Source A has content at I-addresses α₁..α₅
Source B has content at I-addresses β₁..β₅

Target C: COPY from A → places α₁..α₅ at V-positions 1.1-1.5 (homedoc=A)
Target C: COPY from B → places β₁..β₅ at V-position 1.6 (homedoc=B)

Check:
- Same homedoc? NO (A vs B)
- Result: separate crums created, even if α₅ and β₁ happen to be numerically contiguous
```

### Scenario 3: INSERT vs COPY adjacency
```
Target D: INSERT "ABC" → allocates α₁..α₃ (homedoc=D)
Target D: COPY from source S → places β₁..β₃ at adjacent position (homedoc=S)

Check:
- Same homedoc? NO (D vs S)
- Result: separate crums, no merge
```

## Transitive COPY Preserves homedoc

From [INV-IADDR-PROVENANCE]: If you COPY from A to B, then COPY from B to C, the I-addresses in C **still have homedoc=A** (not B). This means two COPYs from the same ultimate source into the same target CAN merge even if they came through different intermediate documents.

## Observable Behavior: None

From [INV-VSPAN-CONSOLIDATION], Finding 0028: The enfilade **consolidates logically contiguous V-space regions into a single span regardless of insertion history**. The operation `retrieve_vspanset` returns maximally consolidated spans — adjacent spans with consecutive V-positions are merged in the output. The internal crum structure (whether merged or separate) does not affect the vspanset representation.

Similarly:
- From [ST-COMPARE-VERSIONS]: operates on I-addresses after V-to-I conversion; internal crum structure is below this abstraction
- From [SS-POOM-MULTIMAP], Finding 0039: `ispan2vspanset` returns all V-positions referencing an I-address; internal crum structure doesn't affect this mapping

### Confirmed: No Observable Difference

The only observable effect of crum merging is **internal storage efficiency** — fewer crums means smaller tree depth and fewer disk blocks. But:
- Query results are identical (vspanset consolidation masks crum boundaries)
- Identity relationships are identical (determined by I-addresses, not crums)
- Link discovery is identical (operates in I-space)

## Comparison: COPY vs INSERT Coalescing

From [ST-INSERT], Finding 0062: Sequential INSERTs into the same document **always** coalesce when at adjacent positions because:
- INSERT allocates I-addresses natively to the target document
- All INSERT content has matching homedoc (the target itself)
- Contiguity is guaranteed for sequential inserts (from [INV-MONOTONIC])

In contrast, COPY coalescing requires the **source** of adjacent COPYs to be the same ultimate origin document. This makes COPY coalescing less predictable from the target document's perspective alone.

---

**Summary**: `isanextensionnd` merges COPY content into existing crums when both (1) I-addresses share the same origin document (homedoc) and (2) I-addresses are contiguous. The merging reduces internal crum count but has zero observable effect on query behavior due to vspanset consolidation and I-address-based query semantics [INV-VSPAN-CONSOLIDATION], [ST-COMPARE-VERSIONS], [SS-POOM-MULTIMAP].

## Code Exploration

# Answer: YES — COPY Merges Crums via isanextensionnd, and It IS Observable

## Summary

When COPY places content at a V-position where adjacent POOM entries have contiguous I-addresses with the copied content, `isanextensionnd` **DOES merge** the copy into the existing crum rather than creating a separate entry, and this merging **IS observable** via RETRIEVE queries.

---

## Mechanism

### 1. COPY Insertion Flow

COPY executes through this call chain:

- `docopy` [`do1.c:60`] → `insertpm` [`orglinks.c:130`] → `insertnd` [`insertnd.c:54`] → `insertmorend` [`insertnd.c:234`] → **`insertcbcnd`** [`insertnd.c:242`]

### 2. The Merging Decision

At `insertcbcnd` [`insertnd.c:242-275`], the code loops through existing bottom crums:

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        // MERGE: Extend existing crum's width
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
        ivemodified (ptr);
        return(FALSE);  // Done - no new crum created
    }
}
// If no match, create new crum
new = createcrum (0, (INT)father->cenftype);
```

### 3. Merge Conditions in isanextensionnd

`isanextensionnd` [`insertnd.c:301-309`] checks **three conditions**:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    // Condition 1: Same source document
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    
    // Condition 2 & 3: Both V-continuity AND I-continuity
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

Where:
- `reach` = right edge of existing crum = `offset + ptr->cdsp + ptr->cwid` (computed by `prologuend` [`retrie.c:334-339`])
- `lockeq` [`wisp.c:261-267`] compares **both dimensions** element-by-element
- `dspsize(POOM)` = `DSPSIZEPM` = **2** [`wisp.h:26`]

**Merging occurs when:**
1. **Same homedoc** — content from the same source document
2. **V-continuity** — `reach.dsas[V]` equals `originptr->dsas[V]`
3. **I-continuity** — `reach.dsas[I]` equals `originptr->dsas[I]`

---

## Observable Behavior

### Retrieval Flow

RETRIEVE converts V-spans to I-spans through:

1. `vspanset2ispanset` [`orglinks.c:401`] → `permute` → `span2spanset` [`orglinks.c:425`]
2. `span2spanset` calls `retrieverestricted` [`retrie.c:56`] which calls `findcbcinarea2d` [`retrie.c:97`]
3. For each qualifying bottom crum, `makecontextfromcbc` creates **one context** [`context.c:151-174`]
4. Each context is inserted into the result list via `incontextlistnd` [`context.c:75`]
5. Each context is converted to **exactly one I-span** via `context2span` [`context.c:176-212`]

### The Observable Difference

**Each bottom crum produces exactly one I-span in RETRIEVE results.**

#### Example: COPY with Adjacent Contiguous Content

**Merged case** (single crum):
```
Bottom crum: V=[1..10], I=[100..110]
RETRIEVE result: 1 I-span = [(100.1, 10)]
```

**Separate case** (two crums):
```
Bottom crum 1: V=[1..5],  I=[100..105]
Bottom crum 2: V=[5..10], I=[105..110]
RETRIEVE result: 2 I-spans = [(100.1, 5), (105.1, 5)]
```

Both represent **the same logical content range I=[100..110]**, but:
- Merged: **1 span** in result
- Separate: **2 spans** in result

This difference is **directly observable** — clients can count the number of I-spans returned.

---

## Key Code Citations

| Location | Function | Key Line |
|----------|----------|----------|
| `insertnd.c:250` | `insertcbcnd` | Calls `isanextensionnd` to check for merge |
| `insertnd.c:251` | `insertcbcnd` | Extends crum width if merge condition met |
| `insertnd.c:305` | `isanextensionnd` | Checks homedoc equality |
| `insertnd.c:308` | `isanextensionnd` | Checks 2D continuity: `lockeq(reach.dsas, originptr->dsas, 2)` |
| `wisp.c:261` | `lockeq` | Compares both V and I dimensions element-by-element |
| `context.c:151` | `makecontextfromcbc` | Creates one context per bottom crum |
| `context.c:176` | `context2span` | Converts one context to one I-span |
| `orglinks.c:439` | `span2spanset` | Loops contexts, each producing one span |

---

## Implications

1. **Span count is non-deterministic** — depends on whether copied content happens to be contiguous with existing content in **both V-space and I-space**
2. **RETRIEVE results vary** — same logical content may return different numbers of I-spans
3. **Performance optimization** — merged crums reduce POOM tree size
4. **Semantic equivalence preserved** — despite different span counts, both cover the same I-address range

The merging is an internal optimization that preserves semantic correctness while reducing storage overhead. However, it **is observable** through the structure of RETRIEVE results.

---

## Question 20 [gregory]

> Does COPY transfer any link subspace (0.2.x) entries from the source document's POOM to the target, or does it only copy the V-spans explicitly specified in the source specset — meaning a COPY of a full document's text carries no links into the target?

### Gregory's Answer

## KB Synthesis

# Answer: COPY is Specset-Driven, Not Subspace-Filtered

**COPY transfers exactly what is specified in the source specset** — it does NOT automatically filter out link subspace entries. Whether links are copied depends entirely on what V-spans the caller includes in the source specset.

## Three Distinct Scenarios

### 1. COPY with Text-Only Specset (Common Case)
If the source specset covers only text subspace V-spans (1.x), **no link POOM entries are transferred**:
```
Source doc: text at 1.1..1.16 (text) + link at 2.1 (link subspace)
Target: COPY(source specset covering 1.1..1.16 only)
Result: Target has text, NO link POOM entries
```

### 2. COPY with Full Document Specset (Dangerous)
If the source specset covers the entire document extent including link subspace (0.x/2.x), **link ISAs ARE copied** — but this violates the subspace convention [INV-SUBSPACE-CONVENTION]:

From [EC-RETRIEVE-VSPANSET-BOTH-SUBSPACES] and [PRE-VCOPY]:
> "Any caller that uses 'full document extent' as input to vcopy inadvertently includes link references... `retrieve_vspanset` returns spans for both `0.x` and `1.x`, and if a caller creates a specset from the full vspanset, `vcopy` copies ALL content including link references to the destination."

Concrete example from [PRE-VCOPY]:
```
Document A: V 0.1 → link ISA 1.1.0.1.0.2
            V 1.1..1.16 → permascroll text

vcopy full content of A into document B at V 1.1:
  specset includes link ISA
  B now contains: V 1.1 → I 1.1.0.1.0.2 (link ISA in text subspace)
  retrieve_contents(B) → garbage bytes (link ISA dereferenced as text)
```

### 3. VERSION is Special-Cased
VERSION is the ONE operation that explicitly filters to text-only, regardless of source content [ST-VERSION-CREATE]:
> "CREATENEWVERSION copies ONLY the text subspace (V-dimension 1.x) from the source document's POOM, not the link subspace (2.x)"

From [ST-VERSION-CREATE] Finding 0046:
> "The function `retrievedocumentpartofvspanpm()` returns only the V-dimension displacement and width — `cdsp.dsas[V]` and `cwid.dsas[V]` — which point to position `1` (the text subspace start). The link subspace at positions before `1` is structurally outside this vspan."

## Link Discovery vs Link POOM Transfer

Critically, **link discovery is independent of link POOM transfer** [INT-LINK-VERSION], [SS-THREE-LAYER-MODEL]:

Even when link POOM entries are NOT transferred, the target can still discover links through the spanf index if it shares content identity with linked content:

From [INT-LINK-VERSION] Finding 0046:
> "A version discovers links from the original document even though the version's POOM contains no link entries. This works because: (1) the version shares text I-addresses with the original, (2) links are stored in the spanf (span enfilade) index keyed by I-address."

## Summary

| Operation | Source Specset | Link POOM Entries Transferred? | Link Discovery Works? |
|-----------|----------------|-------------------------------|---------------------|
| COPY text-only | 1.x spans | NO | YES (via I-address sharing) |
| COPY full document | 0.x + 1.x spans | YES (bug/violation) | YES |
| VERSION | N/A (automatic) | NO (filtered) | YES (via I-address sharing) |

**The answer to your question**: COPY does NOT automatically exclude link subspace entries — it is entirely specset-driven. Links are transferred if and only if the source specset includes link subspace V-spans. VERSION is the exception that explicitly filters to text-only.

The implementation provides no safeguard [PRE-VCOPY]: `docopy` "performs no validation that the source I-address types match the destination subspace." The subspace convention [INV-SUBSPACE-CONVENTION] is caller-enforced, not storage-enforced.

## Code Exploration

Based on my analysis of the C source code, I can now answer your question definitively:

---

## Answer: COPY Does NOT Transfer Links from 0.2.x Unless Explicitly Specified

**COPY only transfers the V-spans explicitly specified in the source specset.** A COPY of a document's text (V-spans from 1.x) carries NO links into the target, because links are stored in a separate V-subspace (0.2.x).

### Code Path Analysis

**1. COPY Entry Point** [`fns.c:35-47`]
```c
void copy(typetask *taskptr) {
    if (getcopy (taskptr, &docisa, &vsa, &localspecset)
    && docopy (taskptr, &docisa, &vsa, localspecset))
        putcopy (taskptr);
    ...
}
```

**2. docopy Implementation** [`do1.c:45-65`]
```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset) {
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)  // Line 54
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && acceptablevsa (vsaptr, docorgl)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)        // Line 60
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)     // Line 62
    );
}
```

The critical operation is **line 54**: `specset2ispanset` converts the V-spans in the source specset to I-spans (permascroll addresses). This determines WHAT content gets copied.

**3. V→I Conversion** [`do2.c:14-46`]
```c
bool specset2ispanset(typetask *taskptr, typespec *specset, typeispanset *ispansetptr, int type) {
    for (; specset; specset = (typespec *)((typeitemheader *)specset)->next) {
        if (((typeitemheader *)specset)->itemid == VSPECID) {
            if (!(findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl,type)
               && (ispansetptr = vspanset2ispanset (taskptr, docorgl, 
                       ((typevspec *)specset)->vspanset, ispansetptr))))  // Line 36
                return (FALSE);
        }
    }
    return (TRUE);
}
```

**4. The Filtering Mechanism** [`retrie.c:270-305`]

`vspanset2ispanset` calls `permute` → `span2spanset` → `retrieverestricted` → `findcbcinarea2d` → **`crumqualifies2d`**

```c
bool crumqualifies2d(typecorecrum *crumptr, typedsp *offset, 
                     tumbler *span1start, tumbler *span1end, INT index1,
                     tumbler *span2start, tumbler *span2end, INT index2, 
                     type2dbottomcruminfo *infoptr) {
    // Check if crum intersects with V-span [span1start, span1end)
    endcmp = iszerotumbler (span1end) ? TOMYRIGHT : 
             whereoncrum (crumptr, offset, span1end, index1);
    if (endcmp <= ONMYLEFTBORDER)     // Lines 282-284
        return(FALSE);
    
    startcmp = whereoncrum (crumptr, offset, span1start, index1);
    if (startcmp > THRUME)            // Lines 286-289
        return (FALSE);
    
    // ... similar check for I-dimension ...
    return (TRUE);
}
```

**This function returns TRUE only if the crum's V-position intersects with the specified V-span.**

### Key Insight: V-Subspace Isolation

- **Text content** is stored at V-positions ≥ 1.0 (e.g., 1.1, 1.2, ...)
- **Links** are stored at V-positions in 0.2.x range (see `setlinkvsas` in [`do2.c:169-183`])
- **From-endset**: 0.1.x
- **To-endset**: 0.2.x  
- **Type-endset**: 0.3.x

When you specify a source specset with V-spans from 1.0 to 1.999..., `crumqualifies2d` filters OUT all crums at V=0.2.x because:
- A crum at V=0.2.x has `startcmp > THRUME` relative to span1start=1.0
- Therefore it does NOT qualify for retrieval
- Therefore its I-address is NOT included in the ispanset
- Therefore it is NOT copied to the target

### Verification from Link Creation Code [`do1.c:195-221`]

```c
bool docreatelink(...) {
    return (
         createorglingranf (taskptr, granf, &hint, linkisaptr)      // Allocate link ISA
      && tumbler2spanset (taskptr, linkisaptr, &ispanset)          // Convert to spanset
      && findnextlinkvsa (taskptr, docisaptr, &linkvsa)            // Get V-pos in 0.2.x
      && docopy (taskptr, docisaptr, &linkvsa, ispanset)           // Copy link to 0.2.x
      && ... // endset operations
    );
}
```

Links are explicitly placed at 0.2.x V-positions. They exist as POOM entries mapping:
- **V-dimension**: 0.2.x (link subspace)
- **I-dimension**: Link's ISA (granf address)

### Conclusion

**To copy links, you must explicitly include 0.2.x V-spans in the source specset.** A "full document copy" of text content (1.x range) will NOT include links unless the specset explicitly covers 0.2.x.

The COPY operation has **no special link-awareness** — it simply:
1. Converts the specified V-spans to I-spans via POOM lookup
2. Copies those I-spans to the target at the specified V-position
3. V-spans at 0.2.x are independent from V-spans at 1.x

---

**Files cited:**
- `febe/fns.c:35-47`
- `backend/do1.c:45-65, 195-221`
- `backend/do2.c:14-46, 169-183`
- `backend/orglinks.c:75-134, 397-402, 404-454`
- `backend/retrie.c:56-85, 229-268, 270-305`
